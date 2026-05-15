#!/usr/bin/env python3.12
"""Generate the Google Container Registry / Artifact Registry domains EDL.

Source: https://cloud.google.com/artifact-registry/docs/docker/authentication
Google Cloud's official Artifact Registry / GCR Docker auth docs.
References the GCR + Artifact Registry regional hosts inline.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://cloud.google.com/artifact-registry/docs/docker/authentication'
OUTPUT_PATH = 'gcr-domains/gcr-domains.txt'

ALLOW_SUFFIXES = (
    'gcr.io',
    'pkg.dev',
    'googleapis.com',
    'googleusercontent.com',
)


def parse_gcr_docs_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main article', 'main', 'div.devsite-article', 'article', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_gcr_docs_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
