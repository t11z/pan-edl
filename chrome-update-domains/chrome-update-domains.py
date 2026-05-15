#!/usr/bin/env python3.12
"""Generate the Google Chrome update domains EDL.

Source: https://support.google.com/chrome/a/answer/6350036
Google's Chrome Enterprise admin help page on firewall configuration.
We anchor on the article body, extract hostname tokens, and filter to
Google-owned suffixes that Chrome update / sync relies on.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://support.google.com/chrome/a/answer/6350036'
OUTPUT_PATH = 'chrome-update-domains/chrome-update-domains.txt'

ALLOW_SUFFIXES = (
    'google.com',
    'googleapis.com',
    'gstatic.com',
    'googleusercontent.com',
    'chrome.com',
    'chromium.org',
    'googlecode.com',
    'doubleclick.net',
    'goog',
)


def parse_chrome_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['article', 'main', 'div.article-content', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_chrome_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=3)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
