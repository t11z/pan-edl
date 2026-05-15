#!/usr/bin/env python3.12
"""Generate the NuGet domains EDL.

Hosts curated from Microsoft vendor documentation:
- https://learn.microsoft.com/en-us/nuget/
- https://learn.microsoft.com/en-us/nuget/install-nuget-client-tools
- https://api.nuget.org/v3/index.json  (NuGet v3 service index, vendor)
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'nuget-domains/nuget-domains.txt'

HOSTS = [
    'api.nuget.org',
    'www.nuget.org',
    'nuget.org',
    'pkgs.dev.azure.com',
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
