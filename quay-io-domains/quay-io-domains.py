#!/usr/bin/env python3.12
"""Generate the Quay.io domains EDL.

Hosts curated from Red Hat / Quay vendor documentation:
- https://docs.quay.io/  (Quay documentation)
- https://access.redhat.com/articles/2477561  (Quay endpoints article)
- https://access.redhat.com/solutions/3422001  (registry connectivity)
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'quay-io-domains/quay-io-domains.txt'

HOSTS = [
    'quay.io',
    '*.quay.io',
    'cdn.quay.io',
    'cdn01.quay.io',
    'cdn02.quay.io',
    'cdn03.quay.io',
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
