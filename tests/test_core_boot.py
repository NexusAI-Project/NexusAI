"""Tests for NexusAI Foundation v0.1 core boot."""

from __future__ import annotations

import unittest

from nexusai_core import NexusCore, boot_core


class TestNexusCoreBoot(unittest.TestCase):
    """Validate that the minimal NexusAI core starts correctly."""

    def test_core_boots_successfully(self) -> None:
        core = boot_core()

        self.assertIsInstance(core, NexusCore)
        self.assertTrue(core.is_running)
        self.assertEqual(core.heart.name, "NexusAI")
        self.assertEqual(core.memory.recall("core.status"), "running")
        self.assertIsNotNone(core.module_registry.get("nexusai_core"))
        self.assertIn("core.booted", [event.name for event in core.event_bus.history])


if __name__ == "__main__":
    unittest.main()
