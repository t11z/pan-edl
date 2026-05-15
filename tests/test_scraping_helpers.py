"""Tests for the defensive scraping helpers in lib/scraping.py."""
import pytest
from bs4 import BeautifulSoup

from lib.scraping import (
    PageStructureError,
    extract_host_tokens,
    filter_hosts,
    find_anchor,
)


class TestFindAnchor:
    def test_returns_first_matching_selector(self):
        soup = BeautifulSoup("<div class='b'>x</div>", 'html.parser')
        assert find_anchor(soup, ['div.a', 'div.b']).get_text() == 'x'

    def test_raises_when_nothing_matches(self):
        soup = BeautifulSoup("<p>nope</p>", 'html.parser')
        with pytest.raises(PageStructureError, match="anchor selectors"):
            find_anchor(soup, ['div.a', 'section.b'])


class TestExtractHostTokens:
    def test_from_href(self):
        html = '<div><a href="https://api.example.com/path">x</a></div>'
        node = BeautifulSoup(html, 'html.parser').div
        assert 'api.example.com' in extract_host_tokens(node)

    def test_from_inline_code(self):
        html = '<div><code>files.pythonhosted.org</code></div>'
        node = BeautifulSoup(html, 'html.parser').div
        assert 'files.pythonhosted.org' in extract_host_tokens(node)

    def test_from_list_items_and_wildcards(self):
        html = '<div><ul><li>*.azureedge.net</li><li>plain.example.com text</li></ul></div>'
        node = BeautifulSoup(html, 'html.parser').div
        tokens = extract_host_tokens(node)
        assert '*.azureedge.net' in tokens or 'azureedge.net' in tokens
        assert 'plain.example.com' in tokens

    def test_strips_url_port_and_path(self):
        html = '<div><a href="https://reg.example.com:8443/v2/manifests">x</a></div>'
        node = BeautifulSoup(html, 'html.parser').div
        assert 'reg.example.com' in extract_host_tokens(node)


class TestFilterHosts:
    def test_keeps_valid_url_list_entries(self):
        result = filter_hosts(['vendor.com', 'foo.vendor.com'])
        assert sorted(result) == ['foo.vendor.com', 'vendor.com']

    def test_drops_invalid_entries(self):
        result = filter_hosts(['', 'http://has-scheme.com', 'has#hash.com'])
        assert result == []

    def test_allow_suffix_filter(self):
        result = filter_hosts(
            ['code.jetbrains.com', 'unrelated.acme.org', 'plugins.jetbrains.com'],
            allow_suffixes=('jetbrains.com',),
        )
        assert sorted(result) == ['code.jetbrains.com', 'plugins.jetbrains.com']

    def test_allow_suffix_matches_wildcard_form(self):
        result = filter_hosts(
            ['*.jetbrains.com', 'evil.acme.org'],
            allow_suffixes=('jetbrains.com',),
        )
        assert result == ['*.jetbrains.com']

    def test_default_reject_rfc2606_zones(self):
        result = filter_hosts(['vendor.com', 'foo.localhost', 'bar.test', 'demo.example'])
        assert result == ['vendor.com']

    def test_allow_suffix_matches_bare_domain(self):
        result = filter_hosts(
            ['jetbrains.com', 'unrelated.acme.org'],
            allow_suffixes=('jetbrains.com',),
        )
        assert result == ['jetbrains.com']
