"""Shared HTTP fetch helpers for EDL generator scripts."""
from __future__ import annotations

import time
from typing import Any

import requests


USER_AGENT = 'pan-edl/1.0 (github.com/t11z/pan-edl)'
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3


def _request(method: str, url: str, **kwargs: Any) -> requests.Response:
    headers = kwargs.pop('headers', {}) or {}
    headers.setdefault('User-Agent', USER_AGENT)
    timeout = kwargs.pop('timeout', DEFAULT_TIMEOUT)
    retries = kwargs.pop('retries', DEFAULT_RETRIES)

    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            response = requests.request(method, url, headers=headers, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as exc:
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed to fetch {url} after {retries} attempts: {last_exc}")


def fetch_html(url: str, **kwargs: Any) -> str:
    """Fetch a URL and return the response body as text."""
    return _request('GET', url, **kwargs).text


def fetch_json(url: str, **kwargs: Any) -> Any:
    """Fetch a URL and return the response body parsed as JSON."""
    return _request('GET', url, **kwargs).json()
