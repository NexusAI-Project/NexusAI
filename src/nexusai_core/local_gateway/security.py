"""Security helpers for the NexusAI Local Gateway."""

from __future__ import annotations

import ipaddress
import os
from urllib.parse import urlsplit

LOCAL_GATEWAY_TOKEN_ENV = "NEXUSAI_LOCAL_GATEWAY_TOKEN"


def is_loopback_host(host: str) -> bool:
    """Return True when a host resolves to a local loopback target."""

    normalized = _normalize_host(host)
    if normalized in {"localhost", "localhost."}:
        return True

    try:
        return ipaddress.ip_address(normalized).is_loopback
    except ValueError:
        return False


def get_optional_local_token() -> str | None:
    """Return a future optional local token without requiring one in v0."""

    token = os.getenv(LOCAL_GATEWAY_TOKEN_ENV)
    if token is None:
        return None

    token = token.strip()
    return token or None


def _normalize_host(host: str) -> str:
    """Normalize host strings, URLs, IPv6 brackets, and host:port values."""

    value = host.strip().lower()
    if not value:
        return ""

    if "://" in value:
        parsed = urlsplit(value)
        return (parsed.hostname or "").strip().lower()

    if value.startswith("[") and "]" in value:
        return value[1 : value.index("]")]

    if value.count(":") == 1:
        host_part, port_part = value.rsplit(":", 1)
        if port_part.isdigit():
            return host_part

    return value
