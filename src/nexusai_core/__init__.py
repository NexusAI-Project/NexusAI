"""NexusAI core package.

Foundation v0.1 exposes the minimal building blocks required to boot
NexusAI as a small, typed, extensible Python core.
"""

from .event_bus import Event, EventBus
from .heart import NexusHeart
from .main import NexusCore, boot_core
from .memory import NexusMemory
from .module_registry import ModuleDefinition, ModuleRegistry

__all__ = [
    "Event",
    "EventBus",
    "ModuleDefinition",
    "ModuleRegistry",
    "NexusCore",
    "NexusHeart",
    "NexusMemory",
    "boot_core",
]

__version__ = "0.1.0"
