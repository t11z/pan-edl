#!/usr/bin/env python3.12
"""Generate the Google Container Registry / Artifact Registry domains EDL.

Hosts curated from Google Cloud vendor documentation:
- https://cloud.google.com/container-registry/docs/pushing-and-pulling
- https://cloud.google.com/artifact-registry/docs/repositories/remote-repo
- https://cloud.google.com/artifact-registry/docs/docker  (gcr.io regional hosts)
- https://cloud.google.com/vpc/docs/configure-private-google-access  (private endpoints)
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'gcr-domains/gcr-domains.txt'

HOSTS = [
    'gcr.io',
    'us.gcr.io',
    'eu.gcr.io',
    'asia.gcr.io',
    'marketplace.gcr.io',
    'k8s.gcr.io',
    'registry.k8s.io',
    '*.pkg.dev',
    'storage.googleapis.com',
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
