"""Tests for the NexusAI Local Gateway prototype."""

from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from nexusai_core.local_gateway.app import create_app
from nexusai_core.local_gateway.security import is_loopback_host


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

    def test_gateway_routes_exist(self) -> None:
        app = create_app()
        paths = {route.path for route in app.routes}

        self.assertIn("/health", paths)
        self.assertIn("/api/tags", paths)
        self.assertIn("/api/generate", paths)
        self.assertIn("/api/chat", paths)


if __name__ == "__main__":
    unittest.main()
