#!/usr/bin/env python3.12
"""Generate the VS Code domains EDL by scraping the official network doc.

Source: https://code.visualstudio.com/docs/setup/network
        ("Network connections in Visual Studio Code")

Microsoft's own vendor page. We anchor on the main docs container,
extract hostname-like tokens, then filter to Microsoft/GitHub-related
suffixes that VS Code depends on.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://code.visualstudio.com/docs/setup/network'
OUTPUT_PATH = 'vscode-domains/vscode-domains.txt'

ALLOW_SUFFIXES = (
    'visualstudio.com',
    'vscode.dev',
    'vscode-cdn.net',
    'vscode-unpkg.net',
    'vscode-sync.trafficmanager.net',
    'vo.msecnd.net',
    'microsoft.com',
    'azureedge.net',
    'githubusercontent.com',
    'github.com',
    'gallerycdn.vsassets.io',
    'gallery.vsassets.io',
)


def parse_vscode_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['div.docs-content', 'main', 'article'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_vscode_page(fetch_html(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=3)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
