#!/usr/bin/env python3.12
"""Generate the GitHub Container Registry domains EDL.

Source: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
GitHub's own container-registry docs. References ghcr.io and the
container blob CDN hostnames inline.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry'
OUTPUT_PATH = 'ghcr-domains/ghcr-domains.txt'

ALLOW_SUFFIXES = (
    'ghcr.io',
    'githubusercontent.com',
    'github.com',
)


def parse_ghcr_docs_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['article', 'main', 'div.article-body', 'body'])
    tokens = extract_host_tokens(article)
    hosts = filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)
    # github.com proper is too broad for a container-registry EDL; only keep
    # subdomains that are container/package related.
    return [h for h in hosts if not (h == 'github.com' or h == 'www.github.com')]


def main() -> None:
    hosts = parse_ghcr_docs_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=1)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
