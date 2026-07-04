#!/usr/bin/env python3.12
"""Generate the RubyGems domains EDL.

Source: https://guides.rubygems.org/rubygems-org-api/
RubyGems.org's own guides — describes the public API endpoints
served by rubygems.org and friends.

The guides page is scraped for currently documented hosts, but the
core RubyGems.org service hosts are also seeded explicitly: the guides
prose only mentions `rubygems.org` inline these days, while the CDN
(`fastly.rubygems.org`) and the compact index (`index.rubygems.org`)
are stable, documented parts of the same infrastructure. Seeding keeps
the published list complete even when the prose changes.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://guides.rubygems.org/rubygems-org-api/'
OUTPUT_PATH = 'rubygems-domains/rubygems-domains.txt'

ALLOW_SUFFIXES = (
    'rubygems.org',
)

# Core RubyGems.org service hosts (API, CDN, compact index).
SEED_HOSTS = (
    'rubygems.org',
    'index.rubygems.org',
    'fastly.rubygems.org',
)


def parse_rubygems_guides_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'article', 'div#content', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = set(SEED_HOSTS)
    try:
        hosts.update(parse_rubygems_guides_page(fetch_html(SOURCE_URL)))
    except Exception as exc:  # guides page is supplementary; never fatal
        print(f"warning: guides scrape failed, using seed hosts only: {exc}", file=sys.stderr)
    report = write_edl(sorted(hosts), OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
