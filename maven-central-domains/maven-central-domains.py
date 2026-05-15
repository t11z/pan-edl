#!/usr/bin/env python3.12
"""Generate the Maven Central domains EDL.

Hosts curated from Sonatype vendor documentation:
- https://central.sonatype.org/
- https://central.sonatype.org/publish/publish-guide/
- https://maven.apache.org/repository/  (Apache Maven primary docs)
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'maven-central-domains/maven-central-domains.txt'

HOSTS = [
    'repo.maven.apache.org',
    'repo1.maven.org',
    'repo2.maven.org',
    'search.maven.org',
    'central.sonatype.com',
    'central.sonatype.org',
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
