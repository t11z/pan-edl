#!/usr/bin/env python3.12
"""Generate the AlmaLinux mirrors EDL.

Source: https://mirrors.almalinux.org/
The AlmaLinux OS Foundation's official mirror list page.
"""
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl


SOURCE_URL = 'https://mirrors.almalinux.org/'
OUTPUT_PATH = 'almalinux-mirrors/almalinux-mirrors.txt'


def parse_almalinux_mirror_page(html: str) -> list[str]:
    """Extract mirror hostnames from the AlmaLinux mirror list HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    domains: list[str] = []
    for link in soup.find_all('a'):
        href = link.get('href') or ''
        if href.startswith(('http://', 'https://', 'rsync://', 'ftp://')):
            netloc = urlparse(href).netloc
            if netloc:
                domains.append(netloc)
    return domains


def main() -> None:
    html = fetch_html(SOURCE_URL)
    domains = ['mirrors.almalinux.org', 'repo.almalinux.org']
    domains.extend(parse_almalinux_mirror_page(html))
    if len(domains) <= 2:
        raise RuntimeError("no mirror URLs parsed from source")

    report = write_edl(domains, OUTPUT_PATH, EDLType.URL_LIST, strict=True)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
