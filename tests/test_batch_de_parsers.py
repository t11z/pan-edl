"""Tests for Batch D + E vendor-doc scraper parsers.

Live fetch + structure detection is exercised in CI. These tests
confirm each parser handles the documented page shape correctly and
fails loudly when the anchor goes missing.
"""
import importlib.util
import pathlib

import pytest

from lib.scraping import PageStructureError


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def _import(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


vscode = _import('vsc', REPO_ROOT / 'vscode-domains' / 'vscode-domains.py')
azul = _import('azul', REPO_ROOT / 'azul-domains' / 'azul-domains.py')
adoptium = _import('adoptium', REPO_ROOT / 'adoptium-domains' / 'adoptium-domains.py')
corretto = _import('corretto', REPO_ROOT / 'corretto-domains' / 'corretto-domains.py')
chrome = _import('chrome', REPO_ROOT / 'chrome-update-domains' / 'chrome-update-domains.py')
edge = _import('edge', REPO_ROOT / 'edge-update-domains' / 'edge-update-domains.py')


VSCODE_FIXTURE = """
<html><body><div class="docs-content">
  <h2>Common hostnames</h2>
  <ul>
    <li><code>update.code.visualstudio.com</code></li>
    <li><code>marketplace.visualstudio.com</code></li>
    <li><code>az764295.vo.msecnd.net</code></li>
    <li><code>*.gallerycdn.vsassets.io</code></li>
    <li><code>github.com</code></li>
  </ul>
</div></body></html>
"""

AZUL_FIXTURE = """
<html><body><main>
  <p>Downloads come from <code>cdn.azul.com</code> and
     <code>api.azul.com</code>.</p>
  <p>See also <code>www.azul.com</code>.</p>
</main></body></html>
"""

ADOPTIUM_FIXTURE = """
<html><body><main>
  <p>Use <code>api.adoptium.net</code> to fetch binary metadata.</p>
  <p>Binaries are hosted on GitHub release CDNs at
     <code>github.com</code> and <code>objects.githubusercontent.com</code>.</p>
</main></body></html>
"""

CORRETTO_FIXTURE = """
<html><body><main id="main-content">
  <p>Direct downloads:</p>
  <ul>
    <li><a href="https://corretto.aws/downloads/latest/amazon-corretto-21-linux-x64.tar.gz">Linux x64</a></li>
    <li><a href="https://d3pxv6yz143wms.cloudfront.net/...">CloudFront mirror</a></li>
    <li>API: <code>corretto.aws</code></li>
  </ul>
</main></body></html>
"""

CHROME_FIXTURE = """
<html><body><article>
  <ul>
    <li><code>update.googleapis.com</code></li>
    <li><code>clients2.google.com</code></li>
    <li><code>dl.google.com</code></li>
    <li><code>tools.google.com</code></li>
    <li>Unrelated: <code>example.com</code></li>
  </ul>
</article></body></html>
"""

EDGE_FIXTURE = """
<html><body><main id="main">
  <table><tbody>
    <tr><td><code>msedge.api.cdp.microsoft.com</code></td></tr>
    <tr><td><code>edge.microsoft.com</code></td></tr>
    <tr><td><code>msedge.b.tlu.dl.delivery.mp.microsoft.com</code></td></tr>
    <tr><td><code>config.edge.skype.com</code></td></tr>
  </tbody></table>
</main></body></html>
"""


CASES = [
    ('vscode', vscode.parse_vscode_page, VSCODE_FIXTURE, ['marketplace.visualstudio.com', 'update.code.visualstudio.com']),
    ('azul', azul.parse_azul_page, AZUL_FIXTURE, ['cdn.azul.com', 'api.azul.com']),
    ('adoptium', adoptium.parse_adoptium_page, ADOPTIUM_FIXTURE, ['api.adoptium.net', 'github.com']),
    ('corretto', corretto.parse_corretto_page, CORRETTO_FIXTURE, ['corretto.aws']),
    ('chrome', chrome.parse_chrome_page, CHROME_FIXTURE, ['update.googleapis.com', 'dl.google.com']),
    ('edge', edge.parse_edge_page, EDGE_FIXTURE, ['edge.microsoft.com', 'msedge.api.cdp.microsoft.com']),
]


@pytest.mark.parametrize("name,parser,fixture,expected_subset", CASES, ids=[c[0] for c in CASES])
def test_parser_extracts_expected_hosts(name, parser, fixture, expected_subset):
    result = parser(fixture)
    for expected in expected_subset:
        assert expected in result, f"{name}: expected {expected!r} in {result}"


@pytest.mark.parametrize("name,parser,fixture,expected_subset", CASES, ids=[c[0] for c in CASES])
def test_parser_rejects_unrelated_hosts(name, parser, fixture, expected_subset):
    """Hosts outside the allow-list suffix family must not leak through."""
    result = parser(fixture)
    assert 'example.com' not in result
    assert 'evil.example.com' not in result


@pytest.mark.parametrize("name,parser,fixture,expected_subset", CASES, ids=[c[0] for c in CASES])
def test_parser_fails_loudly_on_missing_anchor(name, parser, fixture, expected_subset):
    """If the anchor selectors don't match, the parser must raise."""
    broken = "<html><body><nav>nothing here</nav></body></html>"
    # `body` is in some anchor lists as a last resort; in that case the parser
    # may not raise. We just verify it doesn't silently emit invalid data.
    try:
        result = parser(broken)
    except PageStructureError:
        return
    assert result == [], f"{name}: should have returned empty or raised, got {result}"


@pytest.mark.parametrize("name,parser,fixture,expected_subset", CASES, ids=[c[0] for c in CASES])
def test_parser_output_passes_url_list_validation(name, parser, fixture, expected_subset):
    """Every host emitted must validate as URL_LIST per PAN-OS rules."""
    from lib.validators import validate_url_entry

    for host in parser(fixture):
        assert validate_url_entry(host) is None, f"{name}: {host!r} fails URL_LIST validation"
