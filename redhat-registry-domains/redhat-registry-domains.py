#!/usr/bin/env python3.12
"""Generate the Red Hat container registry domains EDL.

Source: https://access.redhat.com/RegistryAuthentication
Red Hat's own Registry Authentication article — the canonical place
that describes registry.redhat.io / registry.access.redhat.com /
registry.connect.redhat.com endpoints.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://access.redhat.com/RegistryAuthentication'
OUTPUT_PATH = 'redhat-registry-domains/redhat-registry-domains.txt'

ALLOW_SUFFIXES = (
    'redhat.io',
    'redhat.com',
)


def parse_redhat_registry_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'article', 'div.article-body', 'div.content', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_redhat_registry_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
