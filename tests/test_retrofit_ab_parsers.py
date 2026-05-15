"""Tests for the Batch A + B retrofitted scrapers.

Each test feeds the parser realistic fixture HTML from the vendor's
docs page and confirms expected hosts make it through the allow-suffix
filter. Live fetch is exercised by CI.
"""
import importlib.util
import pathlib

import pytest


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def _import(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pypi = _import('pypi', REPO_ROOT / 'pypi-domains' / 'pypi-domains.py')
npm = _import('npm', REPO_ROOT / 'npm-domains' / 'npm-domains.py')
maven = _import('maven', REPO_ROOT / 'maven-central-domains' / 'maven-central-domains.py')
nuget = _import('nuget', REPO_ROOT / 'nuget-domains' / 'nuget-domains.py')
crates = _import('crates', REPO_ROOT / 'crates-io-domains' / 'crates-io-domains.py')
go = _import('go', REPO_ROOT / 'go-proxy-domains' / 'go-proxy-domains.py')
rubygems = _import('rubygems', REPO_ROOT / 'rubygems-domains' / 'rubygems-domains.py')

quay = _import('quay', REPO_ROOT / 'quay-io-domains' / 'quay-io-domains.py')
ghcr = _import('ghcr', REPO_ROOT / 'ghcr-domains' / 'ghcr-domains.py')
gcr = _import('gcr', REPO_ROOT / 'gcr-domains' / 'gcr-domains.py')
mcr = _import('mcr', REPO_ROOT / 'mcr-microsoft-domains' / 'mcr-microsoft-domains.py')
redhat = _import('redhat', REPO_ROOT / 'redhat-registry-domains' / 'redhat-registry-domains.py')


def _wrap(body: str, anchor: str = 'main') -> str:
    return f"<html><body><{anchor}>{body}</{anchor}></body></html>"


class TestPypi:
    def test_extracts_pypi_hosts(self):
        html = _wrap("""
          <p>Visit <a href="https://pypi.org/">PyPI</a> and
             <a href="https://files.pythonhosted.org/packages/...">files</a>.</p>
          <p><code>docs.python.org</code> documents the language.</p>
          <p>Unrelated: <a href="https://github.com/">GitHub</a></p>
        """)
        result = pypi.parse_pypi_help_page(html)
        assert 'pypi.org' in result
        assert 'files.pythonhosted.org' in result
        assert 'docs.python.org' in result
        assert 'github.com' not in result


class TestNpm:
    def test_extracts_npm_hosts(self):
        html = _wrap("""
          <p>Default registry: <code>https://registry.npmjs.org/</code></p>
          <p>Web UI at <a href="https://www.npmjs.com/">npmjs.com</a></p>
          <p>Unrelated: <code>github.com</code></p>
        """)
        result = npm.parse_npm_docs_page(html)
        assert 'registry.npmjs.org' in result
        assert 'www.npmjs.com' in result
        assert 'github.com' not in result


class TestMaven:
    def test_extracts_maven_hosts(self):
        html = _wrap("""
          <p>Use <code>repo1.maven.org</code> or <code>repo.maven.apache.org</code>.</p>
          <p>Sonatype: <a href="https://central.sonatype.com/">Central</a></p>
        """)
        result = maven.parse_maven_central_page(html)
        assert 'repo1.maven.org' in result
        assert 'repo.maven.apache.org' in result
        assert 'central.sonatype.com' in result


class TestNugetServiceIndex:
    def test_extracts_from_v3_index(self):
        data = {
            "version": "3.0.0",
            "resources": [
                {"@id": "https://api.nuget.org/v3/registration5/", "@type": "RegistrationsBaseUrl"},
                {"@id": "https://azuresearch-usnc.nuget.org/query", "@type": "SearchQueryService"},
                {"@id": "https://www.nuget.org/api/v2/", "@type": "LegacyGallery"},
                {"@id": "https://malicious.example.com/", "@type": "Whatever"},
            ]
        }
        result = nuget.parse_nuget_service_index(data)
        assert 'api.nuget.org' in result
        assert 'azuresearch-usnc.nuget.org' in result
        assert 'www.nuget.org' in result
        assert 'malicious.example.com' not in result


class TestCrates:
    def test_extracts_crates_hosts(self):
        html = _wrap("""
          <p>Default registry: <code>crates.io</code>.</p>
          <p>Index at <code>https://index.crates.io/</code>.</p>
          <p>Static at <code>static.crates.io</code>.</p>
        """)
        result = crates.parse_crates_docs_page(html)
        assert 'crates.io' in result
        assert 'index.crates.io' in result


class TestGo:
    def test_extracts_go_hosts(self):
        html = _wrap("""
          <p>GOPROXY defaults to <code>https://proxy.golang.org</code>.</p>
          <p>GOSUMDB defaults to <code>sum.golang.org</code>.</p>
          <p>Docs at <a href="https://go.dev/">go.dev</a></p>
        """)
        result = go.parse_go_mod_ref_page(html)
        assert 'proxy.golang.org' in result
        assert 'sum.golang.org' in result
        assert 'go.dev' in result


class TestRubygems:
    def test_extracts_rubygems_hosts(self):
        html = _wrap("""
          <p>API at <code>https://rubygems.org/api/v1/</code>.</p>
          <p>Index served from <code>index.rubygems.org</code>.</p>
        """)
        result = rubygems.parse_rubygems_guides_page(html)
        assert 'rubygems.org' in result
        assert 'index.rubygems.org' in result


class TestQuay:
    def test_extracts_quay_hosts(self):
        html = _wrap("""
          <p>Quay is at <code>quay.io</code>.</p>
          <p>CDN at <code>cdn.quay.io</code>.</p>
        """)
        result = quay.parse_quay_docs_page(html)
        assert 'quay.io' in result
        assert 'cdn.quay.io' in result


class TestGhcr:
    def test_extracts_ghcr_hosts(self):
        html = _wrap("""
          <p>Pull from <code>ghcr.io</code>.</p>
          <p>Blobs from <code>pkg-containers.githubusercontent.com</code>.</p>
        """, anchor='article')
        result = ghcr.parse_ghcr_docs_page(html)
        assert 'ghcr.io' in result
        assert 'pkg-containers.githubusercontent.com' in result

    def test_drops_bare_github_com(self):
        html = _wrap("<p><a href='https://github.com/'>x</a></p>", anchor='article')
        result = ghcr.parse_ghcr_docs_page(html)
        assert 'github.com' not in result


class TestGcr:
    def test_extracts_gcr_and_artifact_registry_hosts(self):
        html = _wrap("""
          <p>Hosts: <code>gcr.io</code>, <code>us-docker.pkg.dev</code>,
             <code>europe-docker.pkg.dev</code>, <code>asia.gcr.io</code>.</p>
        """)
        result = gcr.parse_gcr_docs_page(html)
        assert 'gcr.io' in result
        assert 'us-docker.pkg.dev' in result
        assert 'asia.gcr.io' in result


class TestMcr:
    def test_extracts_mcr_hosts(self):
        html = _wrap("""
          <table><tbody>
            <tr><td><code>mcr.microsoft.com</code></td></tr>
            <tr><td><code>eastus.data.mcr.microsoft.com</code></td></tr>
          </tbody></table>
        """, anchor='main id="main"')
        # We can't easily set attr in this f-string wrapper; use plain main
        html = "<html><body><main id='main'><table><tbody>" \
               "<tr><td><code>mcr.microsoft.com</code></td></tr>" \
               "<tr><td><code>eastus.data.mcr.microsoft.com</code></td></tr>" \
               "</tbody></table></main></body></html>"
        result = mcr.parse_mcr_docs_page(html)
        assert 'mcr.microsoft.com' in result
        assert 'eastus.data.mcr.microsoft.com' in result


class TestRedhat:
    def test_extracts_redhat_registry_hosts(self):
        html = _wrap("""
          <p>Registries: <code>registry.redhat.io</code>,
             <code>registry.access.redhat.com</code>,
             <code>registry.connect.redhat.com</code>.</p>
        """)
        result = redhat.parse_redhat_registry_page(html)
        assert 'registry.redhat.io' in result
        assert 'registry.access.redhat.com' in result
        assert 'registry.connect.redhat.com' in result
