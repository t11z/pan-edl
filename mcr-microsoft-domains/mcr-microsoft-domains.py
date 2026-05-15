#!/usr/bin/env python3.12
"""Generate the Microsoft Container Registry domains EDL.

Source: https://learn.microsoft.com/en-us/azure/container-registry/container-registry-firewall-access-rules
Microsoft's own firewall-access-rules article for Azure Container
Registry. References MCR + ACR backend hosts in tables.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://learn.microsoft.com/en-us/azure/container-registry/container-registry-firewall-access-rules'
OUTPUT_PATH = 'mcr-microsoft-domains/mcr-microsoft-domains.txt'

ALLOW_SUFFIXES = (
    'mcr.microsoft.com',
    'data.mcr.microsoft.com',
    'azurecr.io',
    'azureedge.net',
)


def parse_mcr_docs_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main#main', 'main', 'div.content', 'article', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_mcr_docs_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=1)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
