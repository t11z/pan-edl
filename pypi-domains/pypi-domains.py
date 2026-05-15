#!/usr/bin/env python3.12
"""Generate the PyPI domains EDL.

Hosts curated from the PSF/PyPI vendor documentation:
- https://pypi.org/help/  (FAQ: "Why is my pip install not working through my company proxy?")
- https://warehouse.pypa.io/development/  (Warehouse is the PyPI implementation)
- https://packaging.python.org/en/latest/guides/index-mirrors-and-caches/
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'pypi-domains/pypi-domains.txt'

HOSTS = [
    'pypi.org',
    'files.pythonhosted.org',
    'test.pypi.org',
    'docs.pypi.org',
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
