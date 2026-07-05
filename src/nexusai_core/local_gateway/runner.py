"""Official local runner for the NexusAI Local Gateway.

This runner intentionally binds to 127.0.0.1 only by default.
It must not expose the gateway on 0.0.0.0 by default.
"""

from __future__ import annotations

import uvicorn

DEFAULT_GATEWAY_HOST = "127.0.0.1"
DEFAULT_GATEWAY_PORT = 11435
APP_IMPORT_PATH = "nexusai_core.local_gateway.app:app"


def main() -> None:
    """Run the NexusAI Local Gateway on the safe local default address."""

    uvicorn.run(
        APP_IMPORT_PATH,
        host=DEFAULT_GATEWAY_HOST,
        port=DEFAULT_GATEWAY_PORT,
        log_level="info",
    )


if __name__ == "__main__":
    main()
