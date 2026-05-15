#!/usr/bin/env python3.12
"""Generate the Quay.io domains EDL by scraping Project Quay docs.

Source: https://docs.projectquay.io/welcome.html
Project Quay's own documentation. Quay.io is hosted by Red Hat;
hosts appear inline in setup / registry-endpoint references.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://docs.projectquay.io/welcome.html'
OUTPUT_PATH = 'quay-io-domains/quay-io-domains.txt'

ALLOW_SUFFIXES = (
    'quay.io',
    'projectquay.io',
)


def parse_quay_docs_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'article', 'div.section', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_quay_docs_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=1)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
