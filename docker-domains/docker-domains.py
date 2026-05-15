#!/usr/bin/env python3.12
"""Generate the Docker domains EDL from the official Docker Desktop allow-list."""
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl


SOURCE_URL = 'https://docs.docker.com/desktop/allow-list/'
OUTPUT_PATH = 'docker-domains/docker-domains.txt'


def main() -> None:
    soup = BeautifulSoup(fetch_html(SOURCE_URL), 'html.parser')

    domains: list[str] = ['download.docker.com']
    h2 = soup.find('h2', attrs={'id': 'domain-urls-to-allow'})
    if h2 is None:
        raise RuntimeError("expected section 'domain-urls-to-allow' not found in source")

    div = h2.find_next('div', class_='overflow-x-auto')
    if div is None:
        raise RuntimeError("expected overflow-x-auto div not found in source")

    table = div.find('table')
    if table is None:
        raise RuntimeError("expected table not found inside overflow-x-auto div")

    for link in table.find_all('a'):
        href = link.get('href')
        if href:
            netloc = urlparse(href).netloc
            if netloc:
                domains.append(netloc)

    report = write_edl(domains, OUTPUT_PATH, EDLType.URL_LIST)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
