"""Module registry for NexusAI Foundation v0.1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ModuleDefinition:
    """Description of a NexusAI module known by the core."""

    name: str
    version: str = "0.1.0"
    enabled: bool = True
    description: str = ""


class ModuleRegistry:
    """Keeps track of modules available to the NexusAI core."""

    def __init__(self) -> None:
        self._modules: dict[str, ModuleDefinition] = {}

    def register(self, module: ModuleDefinition) -> None:
        """Register or replace a module definition."""

        if not module.name.strip():
            raise ValueError("module name cannot be empty")
        self._modules[module.name] = module

    def get(self, name: str) -> ModuleDefinition | None:
        """Return a module by name, if it exists."""

        if not name.strip():
            raise ValueError("name cannot be empty")
        return self._modules.get(name)

    def list_modules(self) -> tuple[ModuleDefinition, ...]:
        """Return all registered modules ordered by name."""

        return tuple(self._modules[name] for name in sorted(self._modules))

    def enabled_modules(self) -> tuple[ModuleDefinition, ...]:
        """Return enabled modules only."""

        return tuple(module for module in self.list_modules() if module.enabled)
