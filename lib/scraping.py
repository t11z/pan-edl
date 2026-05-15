"""Defensive scraping helpers for vendor documentation pages.

Pattern: each generator picks a stable anchor in the vendor's docs HTML
(section heading, container div, table) and extracts candidate hostnames
from the bounded region. Candidates pass through the URL_LIST validator
and an optional allow-suffix filter to reject false positives from
unrelated examples in the same page.

If the anchor or the region is missing the helpers raise loudly — the
generator then exits non-zero, the existing .txt is preserved, and the
hourly workflow surfaces a failure visible to maintainers (and to the
planned auto-issue bot).
"""
from __future__ import annotations

import re
from typing import Iterable

from bs4 import BeautifulSoup, Tag

from lib.validators import validate_url_entry


# Match anything that could plausibly be an FQDN / wildcard FQDN.
# Permissive on purpose: real validation happens via validate_url_entry.
_HOST_TOKEN_RE = re.compile(r'\*?\.?[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+')


class PageStructureError(RuntimeError):
    """Raised when a vendor page doesn't match the expected structure.

    Carries an actionable message so the workflow log (and any future
    auto-issue bot) can point at the specific assumption that broke.
    """


def find_anchor(soup: BeautifulSoup, selectors: list[str]) -> Tag:
    """Find the first matching element among multiple candidate selectors.

    Provide several selectors so minor markup changes (e.g. div→section,
    class rename) don't immediately break the scraper. Raises
    PageStructureError if none match.
    """
    for selector in selectors:
        el = soup.select_one(selector)
        if el is not None:
            return el
    raise PageStructureError(
        f"none of the expected anchor selectors found: {selectors}"
    )


def extract_host_tokens(node: Tag) -> set[str]:
    """Scan a DOM subtree for hostname-shaped tokens.

    Pulls candidates from:
    - <a href="..."> attributes
    - text content of <code>, <tt>, <kbd>, <pre>, <samp>
    - free text inside <li> / <td>

    Returned tokens are deduped but NOT yet validated.
    """
    tokens: set[str] = set()

    for a in node.find_all('a'):
        href = a.get('href') or ''
        if '://' in href:
            host = href.split('://', 1)[1].split('/', 1)[0].split(':', 1)[0]
            if host:
                tokens.add(host.strip().lower())

    inline_tags = ('code', 'tt', 'kbd', 'pre', 'samp')
    for tag in node.find_all(inline_tags):
        text = tag.get_text(' ', strip=True)
        for m in _HOST_TOKEN_RE.findall(text):
            tokens.add(m.strip('.').lower())

    for tag in node.find_all(['li', 'td', 'p']):
        text = tag.get_text(' ', strip=True)
        for m in _HOST_TOKEN_RE.findall(text):
            tokens.add(m.strip('.').lower())

    return tokens


def filter_hosts(
    candidates: Iterable[str],
    allow_suffixes: tuple[str, ...] | None = None,
    reject_suffixes: tuple[str, ...] = ('.example', '.example.com', '.localhost', '.test'),
) -> list[str]:
    """Apply URL_LIST validation + optional suffix allow-list.

    allow_suffixes: if provided, only tokens ending with one of these
        suffixes are kept. Use this when the vendor page contains many
        unrelated hostnames in examples (the common case).
    reject_suffixes: always-discarded suffixes (RFC reserved zones etc.).
    """
    out: list[str] = []
    for c in candidates:
        if not c:
            continue
        if any(c.endswith(s) for s in reject_suffixes):
            continue
        if validate_url_entry(c) is not None:
            continue
        if allow_suffixes is not None:
            stripped = c[2:] if c.startswith('*.') else c
            if not any(
                stripped == suf or stripped.endswith('.' + suf)
                for suf in allow_suffixes
            ):
                continue
        out.append(c)
    return out
