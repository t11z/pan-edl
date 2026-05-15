"""Validators for Palo Alto Networks External Dynamic List entries.

Rules derived from official PAN-OS documentation:
https://docs.paloaltonetworks.com/network-security/security-policy/administration/objects/external-dynamic-lists/formatting-guidelines-for-an-external-dynamic-list
"""
from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass


_FQDN_LABEL = re.compile(r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$')
_MAX_FQDN_LENGTH = 255


@dataclass(frozen=True)
class ValidationError:
    entry: str
    reason: str


def _strip_inline_comment(entry: str) -> str:
    idx = entry.find(' #')
    return entry[:idx].rstrip() if idx >= 0 else entry


def validate_ip_entry(raw: str) -> ValidationError | None:
    """Validate an IP-List entry.

    Accepts: IPv4/IPv6 address, CIDR (IPv4 /8-/32, IPv6 up to /128),
    IPv4 ranges 'a.b.c.d-e.f.g.h'. Inline comments allowed after ' #'.
    """
    entry = _strip_inline_comment(raw).strip()
    if not entry:
        return ValidationError(raw, "empty entry")

    if '-' in entry and '/' not in entry and ':' not in entry:
        parts = entry.split('-')
        if len(parts) != 2:
            return ValidationError(raw, "malformed IPv4 range")
        try:
            start = ipaddress.IPv4Address(parts[0].strip())
            end = ipaddress.IPv4Address(parts[1].strip())
        except ValueError as exc:
            return ValidationError(raw, f"invalid IPv4 range: {exc}")
        if int(end) < int(start):
            return ValidationError(raw, "IPv4 range end before start")
        return None

    try:
        if '/' in entry:
            network = ipaddress.ip_network(entry, strict=False)
            if isinstance(network, ipaddress.IPv4Network) and network.prefixlen < 8:
                return ValidationError(raw, f"IPv4 CIDR smaller than /8 rejected by PAN-OS")
        else:
            ipaddress.ip_address(entry)
    except ValueError as exc:
        return ValidationError(raw, f"invalid IP: {exc}")

    return None


def validate_domain_entry(raw: str) -> ValidationError | None:
    """Validate a Domain-List entry.

    Accepts: FQDN, optional '*.' prefix wildcard, optional '^' exact-match prefix.
    Rejects: leading dot, URL schemes, paths, IPs.
    """
    entry = _strip_inline_comment(raw).strip()
    if not entry:
        return ValidationError(raw, "empty entry")

    if '://' in entry:
        return ValidationError(raw, "URL scheme not allowed in Domain List")
    if '/' in entry:
        return ValidationError(raw, "path not allowed in Domain List")

    if entry.startswith('^'):
        entry = entry[1:]
    elif entry.startswith('*.'):
        entry = entry[2:]
    elif entry.startswith('.'):
        return ValidationError(raw, "leading dot not allowed; use '*.' wildcard")

    if len(entry) > _MAX_FQDN_LENGTH:
        return ValidationError(raw, f"FQDN exceeds {_MAX_FQDN_LENGTH} chars")

    try:
        ipaddress.ip_address(entry)
    except ValueError:
        pass
    else:
        return ValidationError(raw, "IP not allowed in Domain List")

    labels = entry.split('.')
    if len(labels) < 2:
        return ValidationError(raw, "FQDN must have at least 2 labels")
    for label in labels:
        if not _FQDN_LABEL.match(label):
            return ValidationError(raw, f"invalid label '{label}'")

    return None


def validate_url_entry(raw: str) -> ValidationError | None:
    """Validate a URL-List entry.

    Accepts: domain[/path], optional '*' or '^' wildcards (not mixed in same entry).
    Rejects: URL scheme prefix (PAN-OS strips it but flag for cleanliness),
    inline '#' comments, mixing '*' and '^', >9 consecutive carets.
    """
    entry = raw.strip()
    if not entry:
        return ValidationError(raw, "empty entry")

    if entry.startswith(('http://', 'https://', 'ftp://')):
        return ValidationError(raw, "URL scheme prefix not allowed")
    if '#' in entry:
        return ValidationError(raw, "'#' not allowed in URL List (parser conflict)")
    if '*' in entry and '^' in entry:
        return ValidationError(raw, "cannot mix '*' and '^' in same URL entry")
    if '^^^^^^^^^^' in entry:
        return ValidationError(raw, "more than 9 consecutive carets")

    host = entry.split('/', 1)[0]
    host = host.replace('*.', '').replace('^', '').lstrip('*')
    if host and not any(c.isalpha() for c in host):
        try:
            ipaddress.ip_address(host)
        except ValueError:
            return ValidationError(raw, f"invalid host portion '{host}'")

    return None


VALIDATORS = {
    "ip": validate_ip_entry,
    "domain": validate_domain_entry,
    "url": validate_url_entry,
}
