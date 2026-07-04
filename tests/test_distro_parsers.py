"""Tests for Linux-distro mirror generator parsers (Batch C).

Each test feeds realistic fixture data sampled from the vendor's
documented response format. Live network fetch is exercised in CI.
"""
import importlib.util
import pathlib


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def _import_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


arch = _import_module('arch_mirrors', REPO_ROOT / 'arch-mirrors' / 'arch-mirrors.py')
alpine = _import_module('alpine_mirrors', REPO_ROOT / 'alpine-mirrors' / 'alpine-mirrors.py')
kali = _import_module('kali_mirrors', REPO_ROOT / 'kali-mirrors' / 'kali-mirrors.py')
rocky = _import_module('rocky_linux_mirrors', REPO_ROOT / 'rocky-linux-mirrors' / 'rocky-linux-mirrors.py')
almalinux = _import_module('almalinux_mirrors', REPO_ROOT / 'almalinux-mirrors' / 'almalinux-mirrors.py')
fedora = _import_module('fedora_mirrors', REPO_ROOT / 'fedora-mirrors' / 'fedora-mirrors.py')
opensuse = _import_module('opensuse_mirrors', REPO_ROOT / 'opensuse-mirrors' / 'opensuse-mirrors.py')


class TestArchParser:
    def test_extracts_hosts_from_status_json(self):
        data = {
            "urls": [
                {"url": "https://mirror.example.com/archlinux/", "country": "DE"},
                {"url": "https://arch.example.org/", "country": "US"},
                {"url": "rsync://rsync.example.com/archlinux/"},
            ]
        }
        result = arch.parse_arch_mirror_status(data)
        assert "mirror.example.com" in result
        assert "arch.example.org" in result
        assert "rsync.example.com" in result

    def test_skips_entries_without_url(self):
        data = {"urls": [{}, {"url": ""}, {"url": "https://valid.example/"}]}
        assert arch.parse_arch_mirror_status(data) == ["valid.example"]


class TestAlpineParser:
    def test_extracts_hosts_from_mirrors_json(self):
        data = [
            {"name": "dl-cdn", "urls": [
                "http://dl-cdn.alpinelinux.org/alpine/",
                "https://dl-cdn.alpinelinux.org/alpine/",
            ]},
            {"name": "example", "urls": ["https://mirror.example.com/alpine/"]},
            {"name": "rsync-only", "urls": ["rsync://alpine.example.org/alpine/"]},
        ]
        result = alpine.parse_alpine_mirror_json(data)
        assert "dl-cdn.alpinelinux.org" in result
        assert "mirror.example.com" in result
        assert "alpine.example.org" in result

    def test_ignores_entries_without_urls(self):
        assert alpine.parse_alpine_mirror_json([{}, {"urls": []}]) == []


class TestKaliParser:
    def test_extracts_urls_from_mirrorlist(self):
        body = (
            "# Kali mirrors\n"
            "URL=https://http.kali.org/kali/\n"
            "URL=https://archive-4.kali.org/kali/\n"
            "URL=https://mirror.example.org/kali/\n"
        )
        result = kali.parse_kali_mirror_list(body)
        assert "http.kali.org" in result
        assert "archive-4.kali.org" in result
        assert "mirror.example.org" in result

    def test_ignores_pure_comment_lines(self):
        body = "# just a comment\n"
        assert kali.parse_kali_mirror_list(body) == []


class TestRockyParser:
    def test_extracts_hosts_from_mirrormanager_html(self):
        html = """
        <html><body>
          <table>
            <tr><td><a href="https://mirror.example.com/rocky/">Mirror 1</a></td></tr>
            <tr><td><a href="rsync://rsync.example.org/rocky/">RSync</a></td></tr>
            <tr><td><a href="/internal/page">Internal</a></td></tr>
          </table>
        </body></html>
        """
        result = rocky.parse_rocky_mirror_page(html)
        assert "mirror.example.com" in result
        assert "rsync.example.org" in result
        assert "/internal/page" not in result


class TestAlmaParser:
    def test_extracts_hosts_from_mirror_list_html(self):
        html = """
        <html><body>
          <a href="https://mirror1.example.com/almalinux/">Mirror 1</a>
          <a href="https://mirror2.example.org/almalinux/">Mirror 2</a>
        </body></html>
        """
        result = almalinux.parse_almalinux_mirror_page(html)
        assert result == ["mirror1.example.com", "mirror2.example.org"]


class TestFedoraParser:
    def test_extracts_mirror_links(self):
        html = """
        <html><body>
          <a href="https://mirror.example.com/fedora/">Mirror</a>
          <a href="https://dl.fedoraproject.org/pub/fedora/">Master</a>
        </body></html>
        """
        result = fedora.parse_fedora_mirror_links(html)
        assert "mirror.example.com" in result
        assert "dl.fedoraproject.org" in result

    def test_finds_release_subpages(self):
        html = """
        <html><body>
          <a href="Fedora/">Fedora</a>
          <a href="EPEL/">EPEL</a>
          <a href="?sort=name">Sort</a>
          <a href="https://external.example/">External</a>
        </body></html>
        """
        result = fedora.parse_fedora_release_subpages(html)
        assert "Fedora/" in result
        assert "EPEL/" in result
        assert "?sort=name" not in result


class TestOpenSUSEParser:
    def test_extracts_hosts_from_full_mirror_list(self):
        html = """
        <html><body>
          <a href="https://download.opensuse.org/">Master</a>
          <a href="https://mirror.example.com/opensuse/">Mirror</a>
          <a href="rsync://rsync.example.org/opensuse/">RSync</a>
        </body></html>
        """
        result = opensuse.parse_opensuse_mirror_page(html)
        assert "download.opensuse.org" in result
        assert "mirror.example.com" in result
        assert "rsync.example.org" in result


class TestAllOutputsAreValidURLList:
    """Every parser's output must pass the URL_LIST validator."""

    def test_validates(self):
        from lib.validators import validate_url_entry

        all_hosts: list[str] = []
        all_hosts.extend(arch.parse_arch_mirror_status(
            {"urls": [{"url": "https://m1.example.com/"}, {"url": "https://m2.example.org/"}]}
        ))
        all_hosts.extend(alpine.parse_alpine_mirror_json([{"urls": ["https://m.example.com/"]}]))
        all_hosts.extend(kali.parse_kali_mirror_list("URL=https://m.example.com/\n"))
        all_hosts.extend(rocky.parse_rocky_mirror_page(
            '<a href="https://m.example.com/">x</a>'
        ))
        all_hosts.extend(almalinux.parse_almalinux_mirror_page(
            '<a href="https://m.example.com/">x</a>'
        ))
        all_hosts.extend(fedora.parse_fedora_mirror_links(
            '<a href="https://m.example.com/">x</a>'
        ))
        all_hosts.extend(opensuse.parse_opensuse_mirror_page(
            '<a href="https://m.example.com/">x</a>'
        ))

        assert all_hosts, "no hosts parsed"
        for host in all_hosts:
            assert validate_url_entry(host) is None, f"{host!r} failed URL_LIST validation"
