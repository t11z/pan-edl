#!/usr/bin/env python3.12
"""Generate the Go module proxy domains EDL.

Hosts curated from the Go team's vendor documentation:
- https://go.dev/ref/mod#environment-variables  (GOPROXY, GOSUMDB defaults)
- https://proxy.golang.org/  (the default module proxy)
- https://sum.golang.org/  (the default checksum database)
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'go-proxy-domains/go-proxy-domains.txt'

HOSTS = [
    'proxy.golang.org',
    'sum.golang.org',
    'index.golang.org',
    'go.dev',
    'golang.org',
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
