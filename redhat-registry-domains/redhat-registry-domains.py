#!/usr/bin/env python3.12
"""Generate the Red Hat container registry domains EDL.

Hosts curated from Red Hat vendor documentation:
- https://access.redhat.com/RegistryAuthentication
- https://access.redhat.com/articles/2208611  (registry firewall rules)
- https://access.redhat.com/articles/4408891  (registry.redhat.io endpoints)
- https://catalog.redhat.com/software/containers/explore
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'redhat-registry-domains/redhat-registry-domains.txt'

HOSTS = [
    'registry.redhat.io',
    'registry.access.redhat.com',
    'registry.connect.redhat.com',
    'cdn.registry.redhat.io',
    'access.redhat.com',
    'sso.redhat.com',
    'catalog.redhat.com',
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
