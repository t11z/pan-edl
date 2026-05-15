#!/usr/bin/env python3.12
"""Generate the Microsoft Container Registry domains EDL.

Hosts curated from Microsoft vendor documentation:
- https://learn.microsoft.com/en-us/azure/container-registry/container-registry-firewall-access-rules
- https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility
- https://mcr.microsoft.com/  (Microsoft Artifact Registry service index)
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'mcr-microsoft-domains/mcr-microsoft-domains.txt'

HOSTS = [
    'mcr.microsoft.com',
    '*.data.mcr.microsoft.com',
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
