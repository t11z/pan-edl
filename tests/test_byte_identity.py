"""Verify write_edl produces byte-identical output to the legacy implementation.

Existing URLs are in production use; the refactor must not change a single
byte in the output files for the three legacy lists.
"""
import pathlib

import pytest

from lib.edl_utils import EDLType, write_edl


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
LEGACY_FILES = [
    REPO_ROOT / 'debian-mirrors' / 'debian-mirrors.txt',
    REPO_ROOT / 'ubuntu-mirrors' / 'ubuntu-mirrors.txt',
    REPO_ROOT / 'docker-domains' / 'docker-domains.txt',
]


@pytest.mark.parametrize("filepath", LEGACY_FILES, ids=lambda p: p.name)
def test_url_list_roundtrip_is_byte_identical(filepath, tmp_path):
    """Strip the trailing '/' from each line, feed back through write_edl,
    and confirm the output matches the original byte for byte."""
    original_bytes = filepath.read_bytes()
    raw_entries = [line.rstrip('/') for line in original_bytes.decode('utf-8').splitlines()]

    output = tmp_path / filepath.name
    report = write_edl(raw_entries, str(output), EDLType.URL_LIST)

    new_bytes = output.read_bytes()
    assert new_bytes == original_bytes, (
        f"Byte-identity broken for {filepath.name}: "
        f"{len(new_bytes)} bytes vs {len(original_bytes)} bytes original, "
        f"{report.skipped} skipped entries"
    )
    assert report.skipped == 0, (
        f"Legacy entries unexpectedly rejected by validator: "
        f"{[(e.entry, e.reason) for e in report.invalid[:5]]}"
    )
