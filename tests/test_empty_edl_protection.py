"""Tests for the never-write-empty-EDL safety net.

Users depend on the published EDL URLs serving usable data even when
upstream vendor pages change structure. write_edl must refuse to
truncate the file when the parser produces zero entries.
"""
import pathlib

import pytest

from lib.edl_utils import EDLType, EmptyEDLError, write_edl


def test_empty_input_raises_and_does_not_create_file(tmp_path):
    output = tmp_path / 'unchanged.txt'
    assert not output.exists()

    with pytest.raises(EmptyEDLError):
        write_edl([], str(output), EDLType.URL_LIST)

    assert not output.exists(), "empty input must not create a file"


def test_empty_input_preserves_existing_file(tmp_path):
    output = tmp_path / 'preserved.txt'
    original = b"existing.example.com/\nlast-known-good.example.com/\n"
    output.write_bytes(original)

    with pytest.raises(EmptyEDLError):
        write_edl([], str(output), EDLType.URL_LIST)

    assert output.read_bytes() == original, "existing file must be byte-identical"


def test_all_invalid_input_preserves_existing_file(tmp_path):
    """If validation strips everything, treat as empty: don't overwrite."""
    output = tmp_path / 'preserved.txt'
    original = b"existing.example.com/\n"
    output.write_bytes(original)

    with pytest.raises(EmptyEDLError):
        write_edl(["not a valid hostname", ""], str(output), EDLType.DOMAIN_LIST)

    assert output.read_bytes() == original


def test_custom_min_entries_threshold(tmp_path):
    """A generator that knows its source produces > N entries can guard."""
    output = tmp_path / 'preserved.txt'
    original = b"existing.example.com/\n"
    output.write_bytes(original)

    with pytest.raises(EmptyEDLError, match="min_entries=10"):
        write_edl(
            [f"host{i}.example.com" for i in range(3)],
            str(output),
            EDLType.URL_LIST,
            min_entries=10,
        )

    assert output.read_bytes() == original


def test_one_valid_entry_writes_when_min_is_default(tmp_path):
    """Default min_entries=1 must allow a single-entry result through."""
    output = tmp_path / 'single.txt'

    report = write_edl(["example.com"], str(output), EDLType.URL_LIST)

    assert report.written == 1
    assert output.read_bytes() == b"example.com/\n"
