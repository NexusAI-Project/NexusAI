"""Internal event bus for NexusAI.

The event bus is intentionally small in Foundation v0.1. It gives the core
and future modules a clean way to communicate without introducing external
dependencies or hidden coupling.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(slots=True, frozen=True)
class Event:
    """A message emitted inside the NexusAI core."""

    name: str
    payload: dict[str, Any] = field(default_factory=dict)


EventHandler = Callable[[Event], None]


class EventBus:
    """Simple synchronous event bus used by the NexusAI core."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[EventHandler]] = defaultdict(list)
        self._history: list[Event] = []

    @property
    def history(self) -> tuple[Event, ...]:
        """Return emitted events in chronological order."""

        return tuple(self._history)

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        """Register a handler for an event name."""

        if not event_name.strip():
            raise ValueError("event_name cannot be empty")
        self._listeners[event_name].append(handler)

    def publish(self, event_name: str, payload: dict[str, Any] | None = None) -> Event:
        """Publish an event and notify all listeners registered for it."""

        if not event_name.strip():
            raise ValueError("event_name cannot be empty")

        event = Event(name=event_name, payload=dict(payload or {}))
        self._history.append(event)

        for handler in self._listeners.get(event_name, []):
            handler(event)

        return event
