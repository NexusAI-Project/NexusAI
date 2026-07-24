"""FastAPI application for the NexusAI Local Gateway.

The gateway is intended to run on 127.0.0.1 only. It must not be exposed on
0.0.0.0 by default. In v0, it only proxies selected Ollama-compatible routes
to the local Ollama service at http://127.0.0.1:11434.
"""

from __future__ import annotations

from typing import Any, Awaitable

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from .homepage import homepage_html
from .ollama_client import OllamaClient

SERVICE_NAME = "NexusAI Local Gateway"
DEFAULT_BIND_HOST = "127.0.0.1"
MAX_REQUEST_BYTES = 65_536


def create_app(ollama_client: OllamaClient | None = None) -> FastAPI:
    """Create the local-only NexusAI Gateway app."""

    client = ollama_client or OllamaClient()
    app = FastAPI(
        title=SERVICE_NAME,
        description="Local-first gateway for NexusAI.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/api/schema.json",
    )

    @app.get("/", response_class=HTMLResponse)
    async def homepage() -> str:
        """Return the local NexusAI dashboard homepage."""

        return homepage_html()

    @app.get("/health")
    async def health() -> dict[str, str]:
        """Return local gateway health information."""

        return {
            "status": "ok",
            "service": SERVICE_NAME,
            "bind": DEFAULT_BIND_HOST,
        }

    @app.get("/api/tags")
    async def api_tags() -> Any:
        """Proxy Ollama /api/tags."""

        return await _proxy_ollama_call(client.get_tags())

    @app.post("/api/generate")
    async def api_generate(request: Request) -> Any:
        """Proxy Ollama /api/generate without logging prompt content."""

        payload = await _read_json_object(request)
        return await _proxy_ollama_call(client.generate(payload))

    @app.post("/api/chat")
    async def api_chat(request: Request) -> Any:
        """Proxy Ollama /api/chat without logging message content."""

        payload = await _read_json_object(request)
        return await _proxy_ollama_call(client.chat(payload))

    return app


async def _read_json_object(request: Request) -> dict[str, Any]:
    """Read a size-limited JSON object without retaining prompt content."""

    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_REQUEST_BYTES:
                raise HTTPException(status_code=413, detail="Request body is too large.")
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid Content-Length header.") from exc

    body = await request.body()
    if len(body) > MAX_REQUEST_BYTES:
        raise HTTPException(status_code=413, detail="Request body is too large.")
    try:
        payload = await request.json()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Request body must be valid JSON.") from exc
    if not isinstance(payload, dict):
        raise HTTPException(status_code=422, detail="Request body must be a JSON object.")
    return payload


async def _proxy_ollama_call(call: Awaitable[Any]) -> Any:
    """Convert local Ollama errors into safe HTTP responses."""

    try:
        return await call
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail="Local Ollama returned an error.",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to reach local Ollama service.",
        ) from exc


app = create_app()
