# NexusAI Project Context

This document is the official project memory for NexusAI.

Its purpose is to help ChatGPT, Codex, future contributors, and the founder resume work on the project without confusion, even if the original conversation context is lost.

---

## 1. Project Identity

- **Project name:** NexusAI
- **Founder:** Damien / Pain
- **Repository:** `NexusAI-Project/NexusAI`
- **Current branch for stable work:** `main`
- **Project nature:** long-term intelligent ecosystem with a central core and modular extensions.

NexusAI is not intended to be a single isolated AI tool. It is designed as a living architecture: a central intelligence layer able to coordinate modules, evolve over time, and become the foundation for future platforms, integrations, and intelligent systems.

---

## 2. Vision

NexusAI aims to become an intelligent ecosystem composed of:

- a central core;
- internal memory;
- a modular runtime;
- communication between independent modules;
- future integrations with APIs, desktop systems, games, automation tools, and AI agents.

The long-term vision is to build a system where each module can communicate with the central core while staying cleanly separated, testable, replaceable, and extensible.

---

## 3. Current State

NexusAI has completed its first technical foundation:

- **Phase:** Foundation v0.1
- **Status:** merged into `main`
- **Merge source:** Pull Request #1
- **Foundation goal:** create a minimal Python core able to boot, expose identity, keep temporary memory, register modules, and publish internal events.

The repository now contains both symbolic project identity and a first working Python foundation.

---

## 4. Current Core Modules

The current Python package is located in:

```txt
src/nexusai_core/
```

Current components:

| Component | Role |
|---|---|
| `heart.py` | Stores NexusAI identity, purpose, version, and values. |
| `memory.py` | Provides minimal in-memory key-value storage. |
| `module_registry.py` | Registers and lists known NexusAI modules. |
| `event_bus.py` | Publishes internal events and keeps event history. |
| `main.py` | Boots the minimal `NexusCore` runtime. |
| `__init__.py` | Exposes the public package API and version. |

Current tests:

```txt
tests/test_core_boot.py
```

The boot test verifies that NexusAI starts correctly, registers its core module, writes boot state to memory, and emits a `core.booted` event.

---

## 5. Important Rules

When continuing NexusAI, preserve the existing foundations.

Do not break or remove:

- `README.md`
- `THE_FIRST_STONE.md`
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `tests/test_core_boot.py`
- existing files under `src/nexusai_core/` unless the task explicitly targets the core implementation.

Special care:

- `THE_FIRST_STONE.md` is a symbolic founding document. Do not rewrite it casually.
- The CI workflow must keep validating the Python test suite.
- The package must remain installable with:

```bash
python -m pip install -e .
```

- The core must remain runnable with:

```bash
python -m nexusai_core.main
```

- Tests must remain runnable with:

```bash
python -m unittest discover -s tests
```

---

## 6. Development Workflow

Use a clean branch and Pull Request workflow.

Recommended workflow:

1. Create a new branch from `main`.
2. Make focused changes only for the requested phase.
3. Open a Pull Request into `main`.
4. Audit the Pull Request before merge.
5. Wait for CI to pass.
6. Merge only after explicit validation.
7. Prefer squash merge for clean project history.

Do not merge directly into `main` unless explicitly requested and validation has already happened.

---

## 7. Current Stable Foundation

Foundation v0.1 established:

- Python `src/` layout;
- typed core package;
- no unnecessary runtime dependencies;
- minimal runtime boot;
- internal event bus;
- memory layer;
- module registry;
- project changelog;
- CI test workflow;
- development instructions in `README.md`.

This is the stable base for future versions.

---

## 8. Recommended Next Phase

The recommended next phase is:

```txt
Core Runtime v0.2
```

Suggested goals for Core Runtime v0.2:

- introduce a clearer runtime lifecycle: `boot`, `start`, `stop`, `status`;
- add module states: `registered`, `enabled`, `disabled`, `failed`;
- add stronger event payload validation;
- add more tests for memory, events, and module registry;
- prepare a future configuration system;
- keep the core simple and dependency-light.

Do not rush into external modules before the runtime lifecycle is stable.

---

## 9. How to Resume If Conversation Context Is Lost

If a future assistant, Codex session, or contributor loses the original conversation context, resume from this file.

Recommended recovery steps:

1. Read `PROJECT_CONTEXT.md` first.
2. Read `README.md` for usage instructions.
3. Read `THE_FIRST_STONE.md` to understand the founding spirit.
4. Inspect `src/nexusai_core/` to understand the technical foundation.
5. Run the test suite:

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

6. Check open issues and Pull Requests before creating new work.
7. Continue with a small scoped branch and PR.

The guiding rule is simple:

> Protect the foundation, improve the core, and grow NexusAI one clean phase at a time.
