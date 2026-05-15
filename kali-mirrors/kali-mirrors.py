#!/usr/bin/env python3.12
"""Generate the Kali Linux mirrors EDL.

Source: https://http.kali.org/README.mirrorlist
Plain text file from Offensive Security / Kali Linux, listing the
official Kali repository mirrors.
"""
import sys
import re
from urllib.parse import urlparse

from lib.edl_utils import EDLType, fetch_html, write_edl


SOURCE_URL = 'https://http.kali.org/README.mirrorlist'
OUTPUT_PATH = 'kali-mirrors/kali-mirrors.txt'

_URL_RE = re.compile(r'https?://[^\s<>"\']+')


def parse_kali_mirror_list(body: str) -> list[str]:
    """Extract mirror hostnames from the Kali README.mirrorlist file."""
    domains: list[str] = []
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        for url in _URL_RE.findall(line):
            netloc = urlparse(url).netloc
            if netloc:
                domains.append(netloc)
    return domains


def main() -> None:
    body = fetch_html(SOURCE_URL)
    domains = ['http.kali.org', 'archive.kali.org', 'cdimage.kali.org']
    domains.extend(parse_kali_mirror_list(body))
    if len(domains) <= 3:
        raise RuntimeError("no mirror URLs parsed from source")

    report = write_edl(domains, OUTPUT_PATH, EDLType.URL_LIST, strict=True)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
