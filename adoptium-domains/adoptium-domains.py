#!/usr/bin/env python3.12
"""Generate the Eclipse Adoptium (Temurin) domains EDL.

Source: https://adoptium.net/installation/
The Eclipse Foundation's Adoptium project install-docs page. Adoptium
serves binaries from its own API + the Eclipse / GitHub release CDNs;
we anchor on the install instructions, extract hostname tokens, and
filter to the project-owned and GitHub-release suffixes.
"""
import sys

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


SOURCE_URL = 'https://adoptium.net/installation/'
OUTPUT_PATH = 'adoptium-domains/adoptium-domains.txt'

ALLOW_SUFFIXES = (
    'adoptium.net',
    'eclipse.org',
    'eclipse.dev',
    'github.com',
    'githubusercontent.com',
)

# Core Adoptium endpoints: the marketing/download site, the release API,
# and the GitHub release CDNs that actually serve the Temurin binaries.
# The install page renders most of these client-side, so seeding keeps
# the list complete regardless of what the static HTML exposes.
SEED_HOSTS = (
    'adoptium.net',
    'api.adoptium.net',
    'github.com',
    'objects.githubusercontent.com',
)


def parse_adoptium_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'article', 'div.container', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = set(SEED_HOSTS)
    try:
        hosts.update(parse_adoptium_page(fetch_html(SOURCE_URL)))
    except Exception as exc:  # install page is supplementary; never fatal
        print(f"warning: page scrape failed, using seed hosts only: {exc}", file=sys.stderr)
    report = write_edl(sorted(hosts), OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
