"""Boot entry point for NexusAI Foundation v0.1."""

from __future__ import annotations

from dataclasses import dataclass, field

from .event_bus import EventBus
from .heart import NexusHeart
from .memory import NexusMemory
from .module_registry import ModuleDefinition, ModuleRegistry


@dataclass(slots=True)
class NexusCore:
    """Minimal NexusAI core used to coordinate early system components."""

    heart: NexusHeart = field(default_factory=NexusHeart)
    memory: NexusMemory = field(default_factory=NexusMemory)
    module_registry: ModuleRegistry = field(default_factory=ModuleRegistry)
    event_bus: EventBus = field(default_factory=EventBus)
    is_running: bool = False

    def boot(self) -> "NexusCore":
        """Start the core and register Foundation v0.1 metadata."""

        self.is_running = True
        self.memory.remember("core.status", "running")
        self.memory.remember("core.version", self.heart.version)
        self.module_registry.register(
            ModuleDefinition(
                name="nexusai_core",
                version=self.heart.version,
                enabled=True,
                description="Foundation v0.1 central core module.",
            )
        )
        self.event_bus.publish(
            "core.booted",
            {
                "name": self.heart.name,
                "version": self.heart.version,
                "status": "running",
            },
        )
        return self

    def status(self) -> dict[str, object]:
        """Return the current core status."""

        return {
            "name": self.heart.name,
            "version": self.heart.version,
            "running": self.is_running,
            "modules": [module.name for module in self.module_registry.list_modules()],
            "events": [event.name for event in self.event_bus.history],
        }


def boot_core() -> NexusCore:
    """Create and boot a NexusAI core instance."""

    return NexusCore().boot()


def main() -> None:
    """Command-line entry point for manual core boot checks."""

    core = boot_core()
    print(core.status())


if __name__ == "__main__":
    main()
