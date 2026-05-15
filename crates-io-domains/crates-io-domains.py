#!/usr/bin/env python3.12
"""Generate the crates.io domains EDL.

Hosts curated from the Rust Foundation / crates.io vendor documentation:
- https://crates.io/
- https://doc.rust-lang.org/cargo/reference/registries.html
- https://doc.rust-lang.org/cargo/reference/registry-index.html
"""
import sys

from lib.edl_utils import EDLType, write_edl


OUTPUT_PATH = 'crates-io-domains/crates-io-domains.txt'

HOSTS = [
    'crates.io',
    'static.crates.io',
    'index.crates.io',
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
