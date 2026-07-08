# NexusAI Core Map

## NexusAI Foundation v0.1 overview

NexusAI Foundation v0.1 is the first small, typed, and testable foundation for the NexusAI ecosystem. It defines a platform-independent core that can boot, declare its identity, store minimal runtime state, register modules, and emit internal events. The foundation keeps Minecraft, Discord, VR, desktop, browser, and other future surfaces outside the center of the architecture; those surfaces should remain modules or adapters around the core.

Foundation v0.1 currently consists of:

- `NexusCore`, the coordinator that boots and reports core status.
- `NexusHeart`, the identity and purpose layer.
- `NexusMemory`, a small in-memory key-value store for early bootstrapping state.
- `EventBus`, a synchronous in-process event channel.
- `ModuleRegistry`, the catalog of known modules.
- `Local Gateway`, a local-only FastAPI gateway and dashboard for browser access and selected Ollama-compatible routes.

## Text architecture diagram

```text
                 Human / Local Browser
                         |
                         v
        +----------------------------------+
        | Local Gateway                    |
        | 127.0.0.1:11435 by default      |
        | Dashboard + selected API proxy   |
        +----------------+-----------------+
                         |
                         | optional local Ollama proxy
                         v
              Local Ollama on loopback

        +----------------------------------+
        | NexusAI Core                     |
        | platform-independent foundation  |
        +----------------+-----------------+
                         |
      +------------------+------------------+
      |                  |                  |
      v                  v                  v
+-------------+   +--------------+   +---------------+
| NexusHeart  |   | NexusMemory  |   | ModuleRegistry|
| identity,   |   | bootstrap    |   | module catalog|
| purpose,    |   | runtime      |   | and enabled   |
| values      |   | state        |   | metadata      |
+-------------+   +--------------+   +---------------+
                         |
                         v
                  +--------------+
                  | EventBus     |
                  | core/module  |
                  | events       |
                  +--------------+
```

## NexusCore role

`NexusCore` is the central coordinator for Foundation v0.1. On boot it marks the core as running, writes core status and version into memory, registers the `nexusai_core` foundation module, publishes a `core.booted` event, and exposes a serializable status view. It should stay independent of any specific platform integration.

## NexusHeart role

`NexusHeart` stores the project identity: name, version, purpose, and guiding values. It is the architectural reminder that NexusAI is intended to be modular, evolving, secure, and human-centered rather than a single platform-specific bot or app.

## NexusMemory role

`NexusMemory` is the current minimal memory layer. In Foundation v0.1 it is an in-memory key-value store used during early bootstrapping, with validation for non-empty keys and a snapshot method for safe inspection. It is not yet persistent memory and should not be treated as long-term storage.

## EventBus role

`EventBus` is the internal synchronous event channel. It lets the core and future modules publish named events, subscribe handlers, and inspect chronological event history without introducing external messaging infrastructure or hidden coupling.

## ModuleRegistry role

`ModuleRegistry` is the catalog for known modules. Foundation v0.1 uses it to register the core module at boot. Future platform integrations should be registered here as modules or adapters, while the core remains the independent center.

## Local Gateway role

The Local Gateway is a local-only FastAPI surface for browser access and selected Ollama-compatible API routes. Its safe default bind address is `127.0.0.1:11435`, and its default Ollama target is `127.0.0.1:11434`. It provides the local dashboard homepage, `/health`, `/api/tags`, `/api/generate`, `/api/chat`, and `/api/schema.json`.

The gateway was started locally during this documentation update with `PYTHONPATH=src python -m nexusai_core.local_gateway.runner`, and the homepage returned HTTP 200 at `http://127.0.0.1:11435/`. A screenshot was not added because this container does not currently provide a browser or screenshot renderer such as Chromium, Chrome, Firefox, Playwright, Selenium, or `wkhtmltoimage`. No image has been invented.

## Safety rules

- Keep NexusAI Core independent from Minecraft, Discord, VR, desktop, and other platform surfaces.
- Implement platform integrations as modules or adapters, never as the center of the architecture.
- Keep the Local Gateway local-only by default.
- Never bind the Local Gateway to `0.0.0.0` by default.
- Do not add hidden surveillance by default.
- Do not add cloud upload by default.
- Do not add arbitrary command execution by default.
- Do not add remote exposure by default.
- Avoid logging prompt or message content through gateway proxy routes.
- Prefer small, reviewed, testable changes.

## Next safest development step

The next safest development step is to add a small read-only core status route to the Local Gateway that reports `NexusCore.status()` without exposing remote access, command execution, cloud upload, or persistent storage. That would connect the browser dashboard to the platform-independent core while preserving the local-only boundary and keeping future integrations modular.
