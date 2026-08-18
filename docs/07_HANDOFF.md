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


## Working protocol

All project threads must follow the Operational Routing, Documentation Checkpoint, Project Sources Sync, and Conversation Management rules defined in the current Project Instructions.

At major checkpoints, the active thread must explicitly tell the user which repository files and Project Sources require updating before work moves to another thread or implementation environment.

## Active repository branch

`design/validation-increment-01`

Future project threads must check this branch for the newest Validation Increment 01 documents. Do not assume `main` contains the latest working state.

## Master escalation rules

Specialist validation threads must return an issue to
`01 | AI Interaction Contract — Validation Increment 01`
before confirmation when the proposed change affects:

- shared semantic status or resolution reasons;
- shared Semantic Schema concepts;
- AI Authority Boundary;
- shared Failure / Fallback behaviour;
- cross-system evidence semantics;
- P0 feature scope;
- confirmed headline evaluation philosophy;
- canonical game/system design;
- assumptions used by both 01A and 01B;
- any change that materially rewrites `08_AI_INTERACTION_CONTRACT.md`.

Specialist threads may continue unrelated validation work while the escalated issue remains unresolved.

Local test-fixture changes, evaluation-case additions, wording refinements, and specialist-only non-authoritative proposals do not require immediate Master escalation.