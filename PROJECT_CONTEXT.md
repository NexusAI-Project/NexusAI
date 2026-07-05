# NexusAI Project Context

This document provides a public, practical context for NexusAI.

Its purpose is to help contributors, tools, and future work sessions understand the current state of the repository without exposing detailed private strategy or long-term implementation plans.

---

## 1. Project Identity

- **Project name:** NexusAI
- **Founder:** Damien / Pain
- **Repository:** `NexusAI-Project/NexusAI`
- **Stable branch:** `main`
- **Project nature:** an evolving AI framework built around a clean core and future extensibility.

NexusAI explores how a small, well-structured foundation can grow into a larger intelligent system over time.

---

## 2. Public Vision

NexusAI is a long-term project focused on modular AI architecture, clean software foundations, and gradual evolution.

The public vision is intentionally broad:

- keep the core simple and understandable;
- preserve a clean project structure;
- support future extensions without locking the project into one narrow direction;
- improve through small, reviewed, testable phases.

More detailed strategic notes, private roadmap items, and future implementation ideas should be kept outside the public repository.

---

## 3. Current State

NexusAI has completed its first technical foundation:

- **Phase:** Foundation v0.1
- **Status:** merged into `main`
- **Merge source:** Pull Request #1
- **Current foundation:** a minimal Python core with development commands, tests, and CI.

The repository now contains both project identity documents and a first working Python foundation.

---

## 4. Current Repository Areas

Important public files and areas:

| Path | Purpose |
|---|---|
| `README.md` | Public overview and development commands. |
| `THE_FIRST_STONE.md` | Founding symbolic document. |
| `PROJECT_CONTEXT.md` | Public project context and recovery guide. |
| `CHANGELOG.md` | Public change history. |
| `.github/workflows/ci.yml` | CI workflow for tests. |
| `src/nexusai_core/` | Current Python foundation. |
| `tests/` | Current test suite. |
| `docs/chronicles/` | Historical project milestones. |

Current core files:

```txt
src/nexusai_core/
```

The current core remains intentionally small and should stay easy to understand, test, and evolve.

---

## 5. Important Public Rules

When continuing NexusAI, preserve the existing foundations.

Do not break or remove:

- `README.md`
- `THE_FIRST_STONE.md`
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `tests/test_core_boot.py`
- existing files under `src/nexusai_core/` unless the task explicitly targets the core implementation.

The project must remain installable with:

```bash
python -m pip install -e .
```

The core must remain runnable with:

```bash
python -m nexusai_core.main
```

Tests must remain runnable with:

```bash
python -m unittest discover -s tests
```

---

## 6. Public Development Workflow

Use a clean branch and Pull Request workflow.

Recommended workflow:

1. Create a new branch from `main`.
2. Make focused changes only for the requested scope.
3. Open a Pull Request into `main`.
4. Review the Pull Request before merge.
5. Wait for CI to pass.
6. Merge only after validation.
7. Prefer squash merge for clean project history.

Avoid direct changes to `main` unless the change is explicitly approved and validated.

---

## 7. Current Stable Foundation

Foundation v0.1 established:

- Python `src/` layout;
- minimal typed core package;
- no unnecessary runtime dependencies;
- development commands;
- test coverage for core boot;
- CI validation;
- public project history.

This is the public stable base for future versions.

---

## 8. Recommended Next Phase

The next phase should continue strengthening the core runtime and improving test coverage.

Detailed roadmap items and strategic implementation notes should be kept outside this public context file until they are ready to be published.

---

## 9. How to Resume Work

Read `README.md`, `PROJECT_CONTEXT.md`, `THE_FIRST_STONE.md`, inspect `src/nexusai_core/`, run tests, continue through a scoped branch and Pull Request.

Useful commands:

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

Guiding principle:

> Keep the public foundation clean, understandable, and safe to evolve.
