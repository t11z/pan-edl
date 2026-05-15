#!/usr/bin/env python3.12
"""Generate the Go module proxy domains EDL by scraping go.dev.

Source: https://go.dev/ref/mod
The Go team's official module reference (the canonical place that
defines GOPROXY/GOSUMDB defaults and the Go module ecosystem hosts).
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://go.dev/ref/mod'
OUTPUT_PATH = 'go-proxy-domains/go-proxy-domains.txt'

ALLOW_SUFFIXES = (
    'golang.org',
    'go.dev',
)


def parse_go_mod_ref_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'article', 'div.Documentation', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_go_mod_ref_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
