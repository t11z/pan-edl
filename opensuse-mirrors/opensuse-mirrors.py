#!/usr/bin/env python3.12
"""Generate the openSUSE mirrors EDL.

Source: https://mirrors.opensuse.org/
The SUSE / openSUSE Project's official mirror list page, which links out
to every mirror. (The old /list/all.html path was retired and now 404s;
the site root serves the full list.)
"""
import re
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl


SOURCE_URL = 'https://mirrors.opensuse.org/'
OUTPUT_PATH = 'opensuse-mirrors/opensuse-mirrors.txt'

# The mirror-list page also carries operator-label anchors whose href is
# a malformed 'https://<Operator Name>' (e.g. 'https://Adfinis AG'). Their
# netloc contains spaces / non-host characters, so we keep only netlocs
# shaped like a real hostname or IP.
_HOSTISH = re.compile(r'^[A-Za-z0-9.-]+$')


def parse_opensuse_mirror_page(html: str) -> list[str]:
    """Extract mirror hostnames from the openSUSE mirror list HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    domains: list[str] = []
    for link in soup.find_all('a'):
        href = link.get('href') or ''
        if href.startswith(('http://', 'https://', 'rsync://', 'ftp://')):
            netloc = urlparse(href).netloc
            host = netloc.split('@')[-1].split(':')[0].lower()
            if host and '.' in host and _HOSTISH.match(host):
                domains.append(host)
    return domains


def main() -> None:
    html = fetch_html(SOURCE_URL)
    domains = [
        'mirrors.opensuse.org',
        'download.opensuse.org',
        'cdn.opensuse.org',
    ]
    domains.extend(parse_opensuse_mirror_page(html))
    if len(domains) <= 3:
        raise RuntimeError("no mirror URLs parsed from source")

    report = write_edl(domains, OUTPUT_PATH, EDLType.URL_LIST, strict=True)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
