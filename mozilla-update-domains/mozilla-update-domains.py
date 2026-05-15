#!/usr/bin/env python3.12
"""Generate the Mozilla / Firefox update domains EDL.

Source: https://support.mozilla.org/en-US/kb/configure-firewalls-so-firefox-can-access-internet
Mozilla's own support article on firewall configuration for Firefox.
We anchor on the article body, extract hostname tokens, and filter
to Mozilla-owned suffixes.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://support.mozilla.org/en-US/kb/configure-firewalls-so-firefox-can-access-internet'
OUTPUT_PATH = 'mozilla-update-domains/mozilla-update-domains.txt'

ALLOW_SUFFIXES = (
    'mozilla.org',
    'mozilla.com',
    'mozilla.net',
    'firefox.com',
    'mozaws.net',
    'services.mozilla.com',
)


def parse_mozilla_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['article#sumo-article-body', 'div.main-content', 'article', 'main'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_mozilla_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
