#!/usr/bin/env python3.12
"""Generate the Azul Zulu / Platform Prime domains EDL.

Source: https://docs.azul.com/core/getting-started
Azul Systems' own documentation portal. We anchor on the page main
container, extract hostname-like tokens, and filter to Azul-owned
suffixes. This catches Azul's CDN (cdn.azul.com), API, and download
hosts as they appear in the install instructions.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://docs.azul.com/core/getting-started'
OUTPUT_PATH = 'azul-domains/azul-domains.txt'

ALLOW_SUFFIXES = (
    'azul.com',
    'azulsystems.com',
)


def parse_azul_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'article', 'div.content', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_azul_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
