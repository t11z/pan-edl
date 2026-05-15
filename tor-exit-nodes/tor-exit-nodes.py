#!/usr/bin/env python3.12
"""Generate the Tor exit nodes EDL from the official Tor Project bulk exit list.

Source: https://check.torproject.org/exit-addresses
This is the canonical list maintained by the Tor Project itself.
Format: blocks of four lines per relay; the IP appears on 'ExitAddress' lines.
"""
import sys

from lib.edl_utils import EDLType, fetch_html, write_edl


SOURCE_URL = 'https://check.torproject.org/exit-addresses'
OUTPUT_PATH = 'tor-exit-nodes/tor-exit-nodes.txt'


def parse_exit_addresses(body: str) -> list[str]:
    """Extract IPs from 'ExitAddress <ip> <timestamp>' lines."""
    ips: list[str] = []
    for line in body.splitlines():
        if line.startswith('ExitAddress '):
            parts = line.split()
            if len(parts) >= 2:
                ips.append(parts[1])
    return ips


def main() -> None:
    body = fetch_html(SOURCE_URL)
    ips = parse_exit_addresses(body)
    if not ips:
        raise RuntimeError("no ExitAddress lines found in source")

    report = write_edl(ips, OUTPUT_PATH, EDLType.IP_LIST, strict=True)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
