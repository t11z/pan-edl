#!/usr/bin/env python3.12
"""Generate the npm domains EDL by scraping the official npm config docs.

Source: https://docs.npmjs.com/cli/v10/configuring-npm/npmrc
npm's own CLI configuration documentation. The page references the
default registry and related npm hosts in inline code blocks; we
anchor on the article body and filter to npmjs-owned suffixes.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://docs.npmjs.com/cli/v10/configuring-npm/npmrc'
OUTPUT_PATH = 'npm-domains/npm-domains.txt'

ALLOW_SUFFIXES = (
    'npmjs.org',
    'npmjs.com',
)


def parse_npm_docs_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'article', 'div#content', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_npm_docs_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
