#!/usr/bin/env python3.12
"""Generate the Microsoft Edge update / endpoints EDL.

Source: https://learn.microsoft.com/en-us/deployedge/microsoft-edge-security-endpoints
Microsoft Learn's official Edge security endpoints page. We anchor on
the main docs content area, extract hostname tokens, and filter to
Microsoft / Edge-related suffixes.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://learn.microsoft.com/en-us/deployedge/microsoft-edge-security-endpoints'
OUTPUT_PATH = 'edge-update-domains/edge-update-domains.txt'

ALLOW_SUFFIXES = (
    'microsoft.com',
    'microsoftedgeinsider.com',
    'msedge.net',
    'msocdn.com',
    'msftconnecttest.com',
    'office.com',
    'office.net',
    'azureedge.net',
    'edgeassetservice.azureedge.net',
    'edgesuite.net',
    'live.com',
    'msn.com',
    'bing.com',
    'edgemicrosoft.net',
)


def parse_edge_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main#main', 'main', 'article', 'div.content', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_edge_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=3)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
