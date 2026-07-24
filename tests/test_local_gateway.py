"""Tests for the NexusAI Local Gateway prototype."""

from __future__ import annotations

import unittest
from typing import Any

from fastapi.testclient import TestClient

from nexusai_core.local_gateway.app import create_app
from nexusai_core.local_gateway.runner import (
    APP_IMPORT_PATH,
    DEFAULT_GATEWAY_HOST,
    DEFAULT_GATEWAY_PORT,
)
from nexusai_core.local_gateway.security import is_loopback_host


class FakeOllamaClient:
    """Return deterministic local-model responses without network access."""

    def __init__(self) -> None:
        self.chat_payload: dict[str, Any] | None = None

    async def get_tags(self) -> dict[str, list[dict[str, str]]]:
        return {"models": [{"name": "test-model"}]}

    async def generate(self, payload: dict[str, Any]) -> dict[str, bool]:
        return {"done": True}

    async def chat(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.chat_payload = payload
        return {"message": {"role": "assistant", "content": "Local response"}}


class TestLocalGateway(unittest.TestCase):
    """Validate the local gateway without requiring Ollama to run."""

    def test_health_endpoint(self) -> None:
        client = TestClient(create_app())

        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "service": "NexusAI Local Gateway",
                "bind": "127.0.0.1",
            },
        )

    def test_loopback_host_detection(self) -> None:
        self.assertTrue(is_loopback_host("127.0.0.1"))
        self.assertTrue(is_loopback_host("127.0.0.1:11434"))
        self.assertTrue(is_loopback_host("localhost"))
        self.assertTrue(is_loopback_host("::1"))
        self.assertTrue(is_loopback_host("[::1]:11434"))

        self.assertFalse(is_loopback_host("0.0.0.0"))
        self.assertFalse(is_loopback_host("192.168.1.10"))
        self.assertFalse(is_loopback_host("example.com"))

    def test_homepage(self) -> None:
        client = TestClient(create_app())

        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("One core.", response.text)
        self.assertIn("NexusAI Chatbox", response.text)
        self.assertIn("Memory", response.text)
        self.assertIn("Discord community", response.text)
        self.assertIn("127.0.0.1", response.text)
        self.assertNotIn("innerHTML", response.text)

    def test_chat_proxies_valid_json_object(self) -> None:
        ollama = FakeOllamaClient()
        client = TestClient(create_app(ollama))
        payload = {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": False,
        }

        response = client.post("/api/chat", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"]["content"], "Local response")
        self.assertEqual(ollama.chat_payload, payload)

    def test_chat_rejects_non_object_json(self) -> None:
        client = TestClient(create_app(FakeOllamaClient()))

        response = client.post("/api/chat", json=["not", "an", "object"])

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], "Request body must be a JSON object.")

    def test_chat_rejects_oversized_request(self) -> None:
        client = TestClient(create_app(FakeOllamaClient()))

        response = client.post("/api/chat", json={"prompt": "x" * 66_000})

        self.assertEqual(response.status_code, 413)

    def test_schema_route(self) -> None:
        client = TestClient(create_app())

        response = client.get("/api/schema.json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["info"]["title"], "NexusAI Local Gateway")
        self.assertEqual(client.get("/openapi.json").status_code, 404)

    def test_gateway_routes_exist(self) -> None:
        app = create_app()
        paths = {route.path for route in app.routes}

        self.assertIn("/", paths)
        self.assertIn("/health", paths)
        self.assertIn("/api/tags", paths)
        self.assertIn("/api/generate", paths)
        self.assertIn("/api/chat", paths)
        self.assertIn("/api/schema.json", paths)
        self.assertNotIn("/openapi.json", paths)

    def test_runner_safe_defaults(self) -> None:
        self.assertEqual(DEFAULT_GATEWAY_HOST, "127.0.0.1")
        self.assertNotEqual(DEFAULT_GATEWAY_HOST, "0.0.0.0")
        self.assertEqual(DEFAULT_GATEWAY_PORT, 11435)
        self.assertEqual(APP_IMPORT_PATH, "nexusai_core.local_gateway.app:app")


if __name__ == "__main__":
    unittest.main()
