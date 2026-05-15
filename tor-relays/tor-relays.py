#!/usr/bin/env python3.12
"""Generate the Tor relays EDL from the official Onionoo API.

Source: https://onionoo.torproject.org/details
Onionoo is the Tor Project's own metrics service. We request only the
or_addresses field (the relay's OR-port endpoints, host:port form) and
only running relays.
"""
import sys
from typing import Any

from lib.edl_utils import EDLType, fetch_json, write_edl


SOURCE_URL = 'https://onionoo.torproject.org/details?fields=or_addresses&running=true'
OUTPUT_PATH = 'tor-relays/tor-relays.txt'


def _strip_port(host_port: str) -> str | None:
    """Parse 'IP:port' or '[IPv6]:port'; return the IP portion."""
    if host_port.startswith('['):
        end = host_port.find(']')
        if end == -1:
            return None
        return host_port[1:end]
    if ':' in host_port:
        return host_port.rsplit(':', 1)[0]
    return host_port


def parse_relay_addresses(data: dict[str, Any]) -> list[str]:
    """Extract IPs from Onionoo relays JSON payload."""
    ips: list[str] = []
    for relay in data.get('relays', []):
        for addr in relay.get('or_addresses', []):
            ip = _strip_port(addr)
            if ip:
                ips.append(ip)
    return ips


def main() -> None:
    data = fetch_json(SOURCE_URL)
    ips = parse_relay_addresses(data)
    if not ips:
        raise RuntimeError("Onionoo returned no relays")

    report = write_edl(ips, OUTPUT_PATH, EDLType.IP_LIST, strict=True)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
