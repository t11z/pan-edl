#!/usr/bin/env python3.12
"""Generate the Alpine Linux mirrors EDL.

Source: https://mirrors.alpinelinux.org/mirrors.json
Authoritative JSON mirror list maintained by the Alpine project itself.
Each entry carries a `urls` array (http/https/rsync); we take the
hostname of every URL. (The old plain-text MIRRORS.txt endpoint was
retired and now 404s.)
"""
import sys
from urllib.parse import urlparse

from lib.edl_utils import EDLType, fetch_json, write_edl


SOURCE_URL = 'https://mirrors.alpinelinux.org/mirrors.json'
OUTPUT_PATH = 'alpine-mirrors/alpine-mirrors.txt'

# Alpine's primary CDN — always part of the list.
SEED_HOSTS = ('dl-cdn.alpinelinux.org',)


def parse_alpine_mirror_json(data: list) -> list[str]:
    """Extract mirror hostnames from the mirrors.json document."""
    domains: list[str] = []
    for entry in data:
        for url in entry.get('urls', []):
            netloc = urlparse(url).netloc
            if netloc:
                domains.append(netloc)
    return domains


def main() -> None:
    domains = list(SEED_HOSTS)
    domains.extend(parse_alpine_mirror_json(fetch_json(SOURCE_URL)))
    if len(set(domains)) <= 1:
        raise RuntimeError("no mirror URLs found in source")

    report = write_edl(domains, OUTPUT_PATH, EDLType.URL_LIST, strict=True)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
