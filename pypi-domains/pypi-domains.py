#!/usr/bin/env python3.12
"""Generate the PyPI / PSF domains EDL by scraping vendor-native sources.

Sources (both pypi.org-served, vendor-native):
- https://pypi.org/help/        PSF help page, references PyPI/python.org hosts
- https://pypi.org/simple/pip/  simple-index for the pip package, references
                                files.pythonhosted.org (the binary CDN)

Combining both ensures we pick up both the public PyPI surface and the
package-file CDN (which is hosted on a different domain).
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCES = [
    'https://pypi.org/help/',
    'https://pypi.org/simple/pip/',
]
OUTPUT_PATH = 'pypi-domains/pypi-domains.txt'

ALLOW_SUFFIXES = (
    'python.org',
    'pypi.org',
    'pythonhosted.org',
    'pypa.io',
)


def parse_pypi_help_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'div.container', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts: set[str] = set()
    for url in SOURCES:
        hosts.update(parse_pypi_help_page(fetch_html(url)))
    report = write_edl(sorted(hosts), OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=3)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
