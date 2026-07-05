"""Minimal local Ollama HTTP client for the NexusAI Local Gateway."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

import httpx

from .security import is_loopback_host

DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434"


class OllamaClient:
    """Small async client restricted to a local Ollama endpoint."""

    def __init__(
        self,
        base_url: str = DEFAULT_OLLAMA_BASE_URL,
        timeout_seconds: float = 120.0,
    ) -> None:
        parsed = urlsplit(base_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Ollama base URL must use http or https")
        if not parsed.hostname or not is_loopback_host(parsed.hostname):
            raise ValueError("Ollama base URL must point to a loopback host")

        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    async def get_tags(self) -> Any:
        """Proxy Ollama model tags."""

        return await self._request("GET", "/api/tags")

    async def generate(self, payload: dict[str, Any]) -> Any:
        """Proxy Ollama generate requests."""

        return await self._request("POST", "/api/generate", json=payload)

    async def chat(self, payload: dict[str, Any]) -> Any:
        """Proxy Ollama chat requests."""

        return await self._request("POST", "/api/chat", json=payload)

    async def _request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Send a local request to Ollama and return the JSON response."""

        async with httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout_seconds,
        ) as client:
            response = await client.request(method, path, json=json)
            response.raise_for_status()
            return response.json()
