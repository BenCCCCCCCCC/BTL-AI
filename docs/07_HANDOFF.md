# Handoff

## Project identity

**Between the Lines: AI Remake (BTL-AI)** is a pre-production, PC-first 2D narrative/interface-driven journalism game. Its first deliverable is a polished 20–30 minute AI-assisted vertical slice, not the full legacy 14-day experience.

## Current milestone

Validation Increment 01 — AI Interaction Contract. The repository baseline is committed to `main` and backed up to a private GitHub repository. No Unity project or runtime AI integration exists yet.

## Important architecture rules

- AI controls language; deterministic game systems control reality.
- Unity will own authoritative game state and rule evaluation.
- LLM output must never directly modify canonical state.
- NPC language must be grounded by character cards, knowledge boundaries, world canon, and dynamic state.
- Narrative structure remains authored and branching.

## What has been completed

- Initial repository structure created.
- Project definition, decision log, current-state note, and working agreement recorded.
- Repository baseline committed to `main` and published to a private GitHub repository.
- Confirmed priorities captured: P0 semantic dialogue parsing, grounded NPC dialogue, and AI headline analysis; P1 memory/contradiction/QA/evaluation; P2 world reactions/voice.

## Immediate next task

Define the semantic parser input/output contract and deterministic authority boundary before implementing Dify or Unity.

## Files to read

1. `README.md`
2. `AGENTS.md`
3. `docs/01_PROJECT_DEFINITION.md`
4. `docs/05_DECISION_LOG.md`
5. `docs/06_CURRENT_STATE.md`

## Known unresolved questions

- What backend/API architecture should connect future game systems and AI orchestration?
- How will Dify be validated and integrated, if retained?
- What exact deterministic rules govern the four global variables and narrative outcomes?
- What is the detailed 20–30 minute story slice, NPC set, data schema, and UI flow?
