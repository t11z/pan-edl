#!/usr/bin/env python3.12
"""Generate the RubyGems domains EDL by scraping the RubyGems guides.

Source: https://guides.rubygems.org/rubygems-org-api/
RubyGems.org's own guides — describes the public API endpoints
served by rubygems.org and friends.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://guides.rubygems.org/rubygems-org-api/'
OUTPUT_PATH = 'rubygems-domains/rubygems-domains.txt'

ALLOW_SUFFIXES = (
    'rubygems.org',
)


def parse_rubygems_guides_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'article', 'div#content', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_rubygems_guides_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
