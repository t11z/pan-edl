#!/usr/bin/env python3.12
"""Generate the NuGet domains EDL from the v3 service index JSON.

Source: https://api.nuget.org/v3/index.json
This is the canonical NuGet v3 service index — a machine-readable JSON
document published by NuGet itself that lists every service endpoint
URL. Each resource entry has an '@id' URL whose host we pick up.
"""
import sys
from typing import Any
from urllib.parse import urlparse

from lib.edl_utils import EDLType, fetch_json, write_edl
from lib.scraping import filter_hosts


SOURCE_URL = 'https://api.nuget.org/v3/index.json'
OUTPUT_PATH = 'nuget-domains/nuget-domains.txt'

ALLOW_SUFFIXES = (
    'nuget.org',
)


def parse_nuget_service_index(data: dict[str, Any]) -> list[str]:
    hosts: list[str] = []
    for resource in data.get('resources', []):
        url = resource.get('@id', '')
        if '://' in url:
            netloc = urlparse(url).netloc
            if netloc:
                hosts.append(netloc)
    return filter_hosts(hosts, allow_suffixes=ALLOW_SUFFIXES)


def main() -> None:
    hosts = parse_nuget_service_index(fetch_json(SOURCE_URL))
    report = write_edl(hosts, OUTPUT_PATH, EDLType.URL_LIST, strict=True, min_entries=2)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
