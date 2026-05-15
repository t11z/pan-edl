#!/usr/bin/env python3.12
"""Generate the crates.io domains EDL by scraping the Cargo book.

Source: https://doc.rust-lang.org/cargo/reference/registries.html
The Rust Foundation's official Cargo book — registries reference page.
References crates.io endpoint hosts inline.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://doc.rust-lang.org/cargo/reference/registries.html'
OUTPUT_PATH = 'crates-io-domains/crates-io-domains.txt'

ALLOW_SUFFIXES = (
    'crates.io',
    'rust-lang.org',
)


def parse_crates_docs_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'div.content', 'article', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_crates_docs_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
