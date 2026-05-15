#!/usr/bin/env python3.12
"""Generate the Fedora mirrors EDL.

Source: https://mirrors.fedoraproject.org/publiclist/
The Fedora Project's MirrorManager public list. We aggregate the
per-release public mirror lists from the index page.
"""
import sys
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl


INDEX_URL = 'https://mirrors.fedoraproject.org/publiclist/'
OUTPUT_PATH = 'fedora-mirrors/fedora-mirrors.txt'


def parse_fedora_mirror_links(html: str) -> list[str]:
    """Extract mirror hostnames from a Fedora MirrorManager publiclist page."""
    soup = BeautifulSoup(html, 'html.parser')
    domains: list[str] = []
    for link in soup.find_all('a'):
        href = link.get('href') or ''
        if href.startswith(('http://', 'https://', 'rsync://', 'ftp://')):
            netloc = urlparse(href).netloc
            if netloc:
                domains.append(netloc)
    return domains


def parse_fedora_release_subpages(html: str) -> list[str]:
    """Extract per-release subpage URLs (e.g. 'Fedora/', 'EPEL/')."""
    soup = BeautifulSoup(html, 'html.parser')
    subpages: list[str] = []
    for link in soup.find_all('a'):
        href = link.get('href') or ''
        if href and not href.startswith(('http', '/', '?', '#')) and href.endswith('/'):
            subpages.append(href)
    return subpages


def main() -> None:
    domains = [
        'mirrors.fedoraproject.org',
        'download.fedoraproject.org',
        'getfedora.org',
        'dl.fedoraproject.org',
    ]
    index_html = fetch_html(INDEX_URL)
    domains.extend(parse_fedora_mirror_links(index_html))

    for sub in parse_fedora_release_subpages(index_html):
        try:
            sub_html = fetch_html(urljoin(INDEX_URL, sub))
            domains.extend(parse_fedora_mirror_links(sub_html))
        except Exception as exc:
            print(f"warning: failed to fetch subpage {sub}: {exc}", file=sys.stderr)

    if len(domains) <= 4:
        raise RuntimeError("no mirror URLs parsed from source")

    report = write_edl(domains, OUTPUT_PATH, EDLType.URL_LIST, strict=True)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
