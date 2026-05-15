#!/usr/bin/env python3.12
"""Generate the Amazon Corretto domains EDL.

Source: https://docs.aws.amazon.com/corretto/latest/corretto-21-ug/downloads-list.html
AWS's official Corretto download list. We anchor on the docs main
container, pull hostname tokens from inline code + download links, and
filter to AWS and Corretto-related suffixes.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://docs.aws.amazon.com/corretto/latest/corretto-21-ug/downloads-list.html'
OUTPUT_PATH = 'corretto-domains/corretto-domains.txt'

ALLOW_SUFFIXES = (
    'corretto.aws',
    'amazonaws.com',
    'amazon.com',
    'aws.amazon.com',
)


def parse_corretto_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main#main-content', 'main', 'article', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_corretto_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
