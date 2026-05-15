"""Public API for writing PAN-OS External Dynamic Lists."""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

from lib.fetchers import fetch_html, fetch_json
from lib.validators import VALIDATORS, ValidationError


class EDLType(str, Enum):
    IP_LIST = "ip"
    DOMAIN_LIST = "domain"
    URL_LIST = "url"


@dataclass
class WriteReport:
    filepath: str
    edl_type: EDLType
    written: int
    skipped: int = 0
    invalid: list[ValidationError] = field(default_factory=list)

    def __str__(self) -> str:
        msg = f"[{self.edl_type.value}] {self.filepath}: {self.written} entries"
        if self.skipped:
            msg += f", {self.skipped} skipped"
            examples = ', '.join(f"{e.entry!r} ({e.reason})" for e in self.invalid[:3])
            msg += f" (e.g. {examples})"
        return msg


def _format_entry(entry: str, edl_type: EDLType) -> str:
    if edl_type is EDLType.URL_LIST:
        return entry + '/'
    return entry


def write_edl(
    entries: Iterable[str],
    filepath: str,
    edl_type: EDLType,
    *,
    strict: bool = False,
) -> WriteReport:
    """Deduplicate, validate, sort and write EDL entries to a file.

    Output format: UTF-8, LF line endings, one entry per line.
    URL_LIST entries get a trailing '/' (preserves historical pan-edl behaviour).

    Args:
        entries: raw entries to write.
        filepath: output path.
        edl_type: PAN-OS EDL type, governs validation and formatting.
        strict: if True, raise on any invalid entry; if False, skip invalid
                entries silently (reported in the returned WriteReport).
    """
    validator = VALIDATORS[edl_type.value]
    unique = sorted({e.strip() for e in entries if e and e.strip()})

    valid: list[str] = []
    invalid: list[ValidationError] = []
    for entry in unique:
        err = validator(entry)
        if err is None:
            valid.append(entry)
        else:
            invalid.append(err)
            if strict:
                raise ValueError(f"Invalid {edl_type.value} entry: {err.entry!r} ({err.reason})")

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        for entry in valid:
            f.write(_format_entry(entry, edl_type) + '\n')

    return WriteReport(
        filepath=filepath,
        edl_type=edl_type,
        written=len(valid),
        skipped=len(invalid),
        invalid=invalid,
    )


__all__ = ['EDLType', 'WriteReport', 'write_edl', 'fetch_html', 'fetch_json']
