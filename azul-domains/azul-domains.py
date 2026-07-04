#!/usr/bin/env python3.12
"""Generate the Azul Zulu / Platform Prime domains EDL.

Source: https://docs.azul.com/core/
Azul Systems' own documentation portal. We anchor on the page main
container, extract hostname-like tokens, and filter to Azul-owned
suffixes. This catches Azul's CDN (cdn.azul.com), API, and download
hosts as they appear in the install instructions. (The old
/core/getting-started path was retired and now 404s.)

The core Azul download/API hosts are also seeded explicitly so the list
stays complete even when the docs portal renders its links client-side.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://docs.azul.com/core/'
OUTPUT_PATH = 'azul-domains/azul-domains.txt'

ALLOW_SUFFIXES = (
    'azul.com',
    'azulsystems.com',
)

# Core Azul hosts: CDN, API, and the main download/marketing site.
SEED_HOSTS = (
    'cdn.azul.com',
    'api.azul.com',
    'www.azul.com',
)


def parse_azul_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'article', 'div.content', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = set(SEED_HOSTS)
    try:
        hosts.update(parse_azul_page(fetch_html(SOURCE_URL)))
    except Exception as exc:  # docs page is supplementary; never fatal
        print(f"warning: page scrape failed, using seed hosts only: {exc}", file=sys.stderr)
    report = write_edl(sorted(hosts), OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
