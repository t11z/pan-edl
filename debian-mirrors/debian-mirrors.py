#!/usr/bin/env python3.12
"""Generate the Debian mirrors EDL from the official mirror list."""
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl


SOURCE_URL = 'https://www.debian.org/mirror/list'
OUTPUT_PATH = 'debian-mirrors/debian-mirrors.txt'


def main() -> None:
    soup = BeautifulSoup(fetch_html(SOURCE_URL), 'html.parser')

    domains: list[str] = ['deb.debian.org', 'security.debian.org']
    for table in soup.find_all('table'):
        for link in table.find_all('a'):
            href = link.get('href')
            if href:
                netloc = urlparse(href).netloc
                if netloc:
                    domains.append(netloc)

    report = write_edl(domains, OUTPUT_PATH, EDLType.URL_LIST)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
