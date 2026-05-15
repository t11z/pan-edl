"""Tests for Tor generator parsing logic.

The fetch step is exercised by CI against the live Tor Project endpoints;
these tests cover only the parsers, with realistic fixture data sampled
from the documented response formats.
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


exit_nodes = _import_module(
    'tor_exit_nodes',
    REPO_ROOT / 'tor-exit-nodes' / 'tor-exit-nodes.py',
)
relays = _import_module(
    'tor_relays',
    REPO_ROOT / 'tor-relays' / 'tor-relays.py',
)


class TestExitAddressParser:
    def test_extracts_ipv4_from_documented_format(self):
        sample = (
            "ExitNode 0011BD2485AD45D984EC4159C88FC066E5E3300E\n"
            "Published 2026-05-15 10:00:00\n"
            "LastStatus 2026-05-15 11:00:00\n"
            "ExitAddress 185.220.101.5 2026-05-15 10:30:00\n"
            "\n"
            "ExitNode 1A2B3C4D5E6F7081920304050607080910111213\n"
            "Published 2026-05-15 10:00:00\n"
            "LastStatus 2026-05-15 11:00:00\n"
            "ExitAddress 51.158.108.222 2026-05-15 10:31:00\n"
        )
        result = exit_nodes.parse_exit_addresses(sample)
        assert result == ['185.220.101.5', '51.158.108.222']

    def test_returns_empty_for_empty_input(self):
        assert exit_nodes.parse_exit_addresses("") == []

    def test_ignores_non_exitaddress_lines(self):
        sample = "Published 2026-05-15\nLastStatus 2026-05-15\n"
        assert exit_nodes.parse_exit_addresses(sample) == []


class TestRelayJSONParser:
    def test_extracts_ipv4(self):
        data = {
            "relays": [
                {"or_addresses": ["192.0.2.1:9001"]},
                {"or_addresses": ["198.51.100.5:443"]},
            ]
        }
        assert relays.parse_relay_addresses(data) == ['192.0.2.1', '198.51.100.5']

    def test_extracts_ipv6_with_brackets(self):
        data = {"relays": [{"or_addresses": ["[2001:db8::1]:9001"]}]}
        assert relays.parse_relay_addresses(data) == ['2001:db8::1']

    def test_combines_multi_address_relays(self):
        data = {
            "relays": [
                {"or_addresses": ["192.0.2.1:9001", "[2001:db8::1]:9001"]},
            ]
        }
        assert relays.parse_relay_addresses(data) == ['192.0.2.1', '2001:db8::1']

    def test_returns_empty_for_no_relays(self):
        assert relays.parse_relay_addresses({"relays": []}) == []
        assert relays.parse_relay_addresses({}) == []


class TestParsedOutputValidates:
    """Parsed IPs must pass the IP_LIST validator (PAN-OS rules)."""

    def test_exit_address_output_is_valid_ip_list(self):
        from lib.validators import validate_ip_entry

        sample = "ExitAddress 185.220.101.5 2026-05-15 10:30:00\n"
        for ip in exit_nodes.parse_exit_addresses(sample):
            assert validate_ip_entry(ip) is None

    def test_relay_output_is_valid_ip_list(self):
        from lib.validators import validate_ip_entry

        data = {"relays": [
            {"or_addresses": ["192.0.2.1:9001", "[2001:db8::1]:9001"]},
        ]}
        for ip in relays.parse_relay_addresses(data):
            assert validate_ip_entry(ip) is None
