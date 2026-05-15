"""Tests for PAN-OS EDL validators."""
import pytest

from lib.validators import validate_domain_entry, validate_ip_entry, validate_url_entry


class TestIPValidator:
    @pytest.mark.parametrize("entry", [
        "1.2.3.4",
        "10.0.0.0/8",
        "192.168.1.0/24",
        "2001:db8::1",
        "2001:db8::/32",
        "::1",
        "10.0.0.1-10.0.0.50",
        "1.2.3.4 # comment",
    ])
    def test_valid(self, entry):
        assert validate_ip_entry(entry) is None

    @pytest.mark.parametrize("entry,reason_contains", [
        ("", "empty"),
        ("not_an_ip", "invalid IP"),
        ("example.com", "invalid IP"),
        ("1.2.3.4/2", "smaller than /8"),
        ("10.0.0.50-10.0.0.1", "before start"),
        ("10.0.0.1-not-ip", "malformed IPv4 range"),
        ("10.0.0.1-bad", "invalid IPv4 range"),
    ])
    def test_invalid(self, entry, reason_contains):
        err = validate_ip_entry(entry)
        assert err is not None, f"expected validation error for {entry!r}"
        assert reason_contains in err.reason, f"got reason {err.reason!r}"


class TestDomainValidator:
    @pytest.mark.parametrize("entry", [
        "example.com",
        "*.example.com",
        "^example.com",
        "sub.domain.example.com",
        "deb.debian.org",
        "archive-1.ubuntu.com",
    ])
    def test_valid(self, entry):
        assert validate_domain_entry(entry) is None

    @pytest.mark.parametrize("entry,reason_contains", [
        ("", "empty"),
        (".example.com", "leading dot"),
        ("http://example.com", "URL scheme"),
        ("example.com/path", "path not allowed"),
        ("1.2.3.4", "IP not allowed"),
        ("singlelabel", "at least 2 labels"),
        ("-bad.com", "invalid label"),
        ("bad-.com", "invalid label"),
    ])
    def test_invalid(self, entry, reason_contains):
        err = validate_domain_entry(entry)
        assert err is not None
        assert reason_contains in err.reason


class TestURLValidator:
    @pytest.mark.parametrize("entry", [
        "example.com",
        "example.com/path",
        "*.example.com",
        "*.example.com/path/*",
        "^example.com",
        "deb.debian.org",
        "archive.ubuntu.com",
    ])
    def test_valid(self, entry):
        assert validate_url_entry(entry) is None

    @pytest.mark.parametrize("entry,reason_contains", [
        ("", "empty"),
        ("http://example.com", "scheme prefix"),
        ("https://example.com", "scheme prefix"),
        ("example.com#fragment", "'#' not allowed"),
        ("*.^example.com", "cannot mix"),
        ("example.com/^^^^^^^^^^/path", "more than 9"),
    ])
    def test_invalid(self, entry, reason_contains):
        err = validate_url_entry(entry)
        assert err is not None
        assert reason_contains in err.reason


class TestExistingProductionEntries:
    """Real entries from production .txt files must validate as URL_LIST."""

    @pytest.mark.parametrize("entry", [
        "deb.debian.org",
        "security.debian.org",
        "archive.ubuntu.com",
        "*.archive.ubuntu.com",
        "security.ubuntu.com",
        "download.docker.com",
        "api.docker.com",
        "cdn.auth0.com",
        "debian-archive.trafficmanager.net",
        "deb-mir1.naitways.net",
    ])
    def test_existing_url_entries(self, entry):
        assert validate_url_entry(entry) is None, f"Production entry {entry!r} must validate"
