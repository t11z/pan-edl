#!/usr/bin/env python3.12
"""Generate the Arch Linux mirrors EDL.

Source: https://archlinux.org/mirrors/status/json/
This is the canonical, machine-readable mirror status feed maintained by
the Arch Linux project itself.
"""
import sys
from typing import Any
from urllib.parse import urlparse

from lib.edl_utils import EDLType, fetch_json, write_edl


SOURCE_URL = 'https://archlinux.org/mirrors/status/json/'
OUTPUT_PATH = 'arch-mirrors/arch-mirrors.txt'


def parse_arch_mirror_status(data: dict[str, Any]) -> list[str]:
    """Extract mirror hostnames from the Arch mirror status JSON."""
    domains: list[str] = []
    for mirror in data.get('urls', []):
        url = mirror.get('url')
        if not url:
            continue
        netloc = urlparse(url).netloc
        if netloc:
            domains.append(netloc)
    return domains


def main() -> None:
    data = fetch_json(SOURCE_URL)
    domains = parse_arch_mirror_status(data)
    if not domains:
        raise RuntimeError("no mirror URLs found in source")

    report = write_edl(domains, OUTPUT_PATH, EDLType.URL_LIST, strict=True)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
