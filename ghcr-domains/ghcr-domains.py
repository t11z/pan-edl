#!/usr/bin/env python3.12
"""Generate the GitHub Container Registry domains EDL.

Hosts curated from GitHub vendor documentation:
- https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
- https://docs.github.com/en/actions/learn-github-actions/usage-limits-billing-and-administration#about-github-hosted-runners-networking
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-githubs-ip-addresses
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'ghcr-domains/ghcr-domains.txt'

HOSTS = [
    'ghcr.io',
    '*.ghcr.io',
    'pkg-containers.githubusercontent.com',
    'pkg.github.com',
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
