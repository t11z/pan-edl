#!/usr/bin/env python3.12
"""Generate the npm domains EDL.

Hosts curated from the npm/GitHub vendor documentation:
- https://docs.npmjs.com/  (default registry endpoints)
- https://docs.npmjs.com/cli/v10/configuring-npm/npmrc  (registry config)
- https://github.com/npm/cli  (canonical npm client)
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'npm-domains/npm-domains.txt'

HOSTS = [
    'registry.npmjs.org',
    'registry.npmjs.com',
    'www.npmjs.com',
    'npmjs.com',
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
