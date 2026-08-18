# Between the Lines: AI Remake (BTL-AI)

**Pre-production** — this repository is establishing the foundation for a polished 20–30 minute vertical slice of an AI-assisted narrative journalism game.

## Goals

- Demonstrate game design and game-system design ability.
- Demonstrate AI product and AI orchestration ability.
- Build a focused, polished vertical slice rather than a full 14-day game.

## Current status

The project is in pre-production. No Unity project, runtime AI integration, Dify implementation, or backend/API architecture has been validated yet.

## Architecture at a glance

AI controls language; deterministic game systems control reality. Unity will own authoritative game state and rule evaluation. LLM output is advisory and must never directly modify canonical state.

## Repository structure

- `docs/` — project definition, decisions, current status, and handoff material.
- `ai/` — future Dify experiments, prompts, schemas, and evaluation work.
- `data/` — authored NPC, evidence, story, and world data.
- `tests/` — automated and manual-test support.
- `tools/` — development utilities.

Start with [the project overview](docs/00_PROJECT_OVERVIEW.md) and [the authoritative project definition](docs/01_PROJECT_DEFINITION.md).
