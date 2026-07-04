"""Identity and purpose layer for NexusAI."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class NexusHeart:
    """Stores the founding identity and guiding purpose of NexusAI."""

    name: str = "NexusAI"
    version: str = "0.1.0"
    purpose: str = "A living AI framework designed to think, evolve and grow."
    values: tuple[str, ...] = field(
        default_factory=lambda: (
            "clarity",
            "modularity",
            "evolution",
            "security",
            "human-centered design",
        )
    )

    def identity(self) -> dict[str, str | tuple[str, ...]]:
        """Return a serializable view of the NexusAI identity."""

        return {
            "name": self.name,
            "version": self.version,
            "purpose": self.purpose,
            "values": self.values,
        }
