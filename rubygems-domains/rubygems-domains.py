#!/usr/bin/env python3.12
"""Generate the RubyGems domains EDL.

Hosts curated from the RubyGems vendor documentation:
- https://rubygems.org/
- https://guides.rubygems.org/
- https://guides.rubygems.org/rubygems-org-api/  (canonical API endpoints)
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'rubygems-domains/rubygems-domains.txt'

HOSTS = [
    'rubygems.org',
    'index.rubygems.org',
    'fastly.rubygems.org',
]


def main() -> None:
    report = write_edl(HOSTS, OUTPUT_PATH, EDLType.URL_LIST, strict=True)
    print(report)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
