#!/usr/bin/env python3.12
"""Generate the JetBrains domains EDL by scraping the official firewall doc.

Source: https://intellij-support.jetbrains.com/hc/en-us/articles/360001214939
        ("IDE domains and ports to allow-list for the firewall")

This is JetBrains' own vendor page. The article is a Zendesk Help Center
entry; we anchor on the article body container and extract hostname-like
tokens from inline code / list items / table cells, then filter by a
JetBrains-owned suffix set so unrelated example URLs don't slip in.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://intellij-support.jetbrains.com/hc/en-us/articles/360001214939'
OUTPUT_PATH = 'jetbrains-domains/jetbrains-domains.txt'

ALLOW_SUFFIXES = (
    'jetbrains.com',
    'intellij.net',
    'jetbrains.space',
    'jetbrains.team',
    'jetbrains.ai',
)


def parse_jetbrains_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['div.article-body', 'article', 'main'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_jetbrains_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=3)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
