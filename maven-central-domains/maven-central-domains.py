#!/usr/bin/env python3.12
"""Generate the Maven Central domains EDL.

Source: https://central.sonatype.org/
Sonatype's official Maven Central documentation portal. We anchor on
the main content container and extract Sonatype / Apache Maven hosts.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://central.sonatype.org/'
OUTPUT_PATH = 'maven-central-domains/maven-central-domains.txt'

ALLOW_SUFFIXES = (
    'sonatype.org',
    'sonatype.com',
    'maven.apache.org',
    'maven.org',
)


def parse_maven_central_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'article', 'div.theme-doc-markdown', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_maven_central_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
