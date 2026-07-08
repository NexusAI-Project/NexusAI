# NexusAI Agent Instructions

These instructions apply to AI coding agents working in this repository.

## Project identity

- NexusAI is a long-term modular AI ecosystem.
- Preserve the Founder vision in all changes.
- `THE_FIRST_STONE.md` is sacred and must never be modified unless the Founder explicitly asks.

## Architecture rules

- Keep the NexusAI Core independent from Minecraft, Discord, VR, Desktop, or any specific platform.
- Platform integrations must be implemented as modules or adapters, never as the center of the architecture.
- Prefer small, reviewed, testable changes.
- Update documentation when architecture changes.

## Testing rules

- Run tests when code changes.

## Local gateway safety

- Keep the local gateway local-only by default.
- Never expose the gateway on `0.0.0.0` by default.

## Forbidden defaults

Never add any of the following by default:

- hidden surveillance;
- cloud upload;
- arbitrary command execution;
- remote exposure.

## Pull request requirements

Pull requests must include:

- summary;
- files changed;
- tests run;
- risks;
- next step.
