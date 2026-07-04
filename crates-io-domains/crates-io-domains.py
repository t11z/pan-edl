#!/usr/bin/env python3.12
"""Generate the crates.io domains EDL.

Primary source: the crates.io sparse-index config at
https://index.crates.io/config.json — vendor-native and authoritative,
it advertises the registry's `api` and `dl` hosts. We add the sparse
index host itself (the endpoint clients fetch that config from).

The Cargo book registries page is scraped as a supplementary signal so
newly documented crates.io hosts still get picked up, but it is never
fatal: the config endpoint alone yields a complete, stable list even
when the docs page drops the endpoint hostnames from its prose.
"""
import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from lib.edl_utils import EDLType, fetch_html, fetch_json, write_edl
from lib.scraping import extract_host_tokens, filter_hosts, find_anchor


CONFIG_URL = 'https://index.crates.io/config.json'
DOCS_URL = 'https://doc.rust-lang.org/cargo/reference/registries.html'
OUTPUT_PATH = 'crates-io-domains/crates-io-domains.txt'

# The sparse-index host is where clients fetch config.json (and package
# metadata) from; it isn't listed inside the config document itself.
INDEX_HOST = 'index.crates.io'

ALLOW_SUFFIXES = (
    'crates.io',
)


def parse_crates_config(config: dict) -> list[str]:
    """Extract the api/dl hosts advertised by the sparse-index config."""
    hosts = {INDEX_HOST}
    for key in ('api', 'dl'):
        value = config.get(key)
        if not value:
            continue
        netloc = urlparse(value).netloc
        if netloc:
            hosts.add(netloc.lower())
    return sorted(hosts)


def parse_crates_docs_page(html: str) -> list[str]:
    soup = BeautifulSoup(html, 'html.parser')
    article = find_anchor(soup, ['main', 'div.content', 'article', 'body'])
    tokens = extract_host_tokens(article)
    return filter_hosts(tokens, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = set(parse_crates_config(fetch_json(CONFIG_URL)))
    try:
        hosts.update(parse_crates_docs_page(fetch_html(DOCS_URL)))
    except Exception as exc:  # docs page is supplementary; never fatal
        print(f"warning: docs scrape failed, using config only: {exc}", file=sys.stderr)
    report = write_edl(sorted(hosts), OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
