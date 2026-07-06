"""NexusAI Local Gateway package.

The gateway is designed as a local-only bridge between browser interfaces
and a local Ollama service.
"""

from .app import create_app
from .security import get_optional_local_token, is_loopback_host

__all__ = ["create_app", "get_optional_local_token", "is_loopback_host"]
