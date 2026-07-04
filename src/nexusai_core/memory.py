"""Minimal in-memory storage for NexusAI Foundation v0.1."""

from __future__ import annotations

from typing import Any


class NexusMemory:
    """Small key-value memory used by the core during early bootstrapping."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def remember(self, key: str, value: Any) -> None:
        """Store a value under a non-empty key."""

        if not key.strip():
            raise ValueError("key cannot be empty")
        self._store[key] = value

    def recall(self, key: str, default: Any | None = None) -> Any:
        """Read a value from memory."""

        if not key.strip():
            raise ValueError("key cannot be empty")
        return self._store.get(key, default)

    def snapshot(self) -> dict[str, Any]:
        """Return a copy of the current memory state."""

        return dict(self._store)

    def clear(self) -> None:
        """Clear all temporary memory entries."""

        self._store.clear()
