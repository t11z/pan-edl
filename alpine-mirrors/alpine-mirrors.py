#!/usr/bin/env python3.12
"""Generate the Alpine Linux mirrors EDL.

Source: https://mirrors.alpinelinux.org/MIRRORS.txt
Plain text file with one mirror URL per line, maintained by the Alpine
project itself.
"""
import sys
from urllib.parse import urlparse

from lib.edl_utils import EDLType, fetch_html, write_edl


SOURCE_URL = 'https://mirrors.alpinelinux.org/MIRRORS.txt'
OUTPUT_PATH = 'alpine-mirrors/alpine-mirrors.txt'


def parse_alpine_mirror_list(body: str) -> list[str]:
    """Extract mirror hostnames from the plain-text MIRRORS.txt file."""
    domains: list[str] = []
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        netloc = urlparse(line).netloc
        if netloc:
            domains.append(netloc)
    return domains


def main() -> None:
    body = fetch_html(SOURCE_URL)
    domains = ['dl-cdn.alpinelinux.org']
    domains.extend(parse_alpine_mirror_list(body))
    if len(domains) <= 1:
        raise RuntimeError("no mirror URLs found in source")

    report = write_edl(domains, OUTPUT_PATH, EDLType.URL_LIST, strict=True)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
