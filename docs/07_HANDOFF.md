# Handoff

## Project identity

**Between the Lines: AI Remake (BTL-AI)** is a pre-production, PC-first 2D narrative/interface-driven journalism game. Its first deliverable is a polished 20–30 minute AI-assisted vertical slice, not the full legacy 14-day experience.

## Current milestone

Establish the pre-production baseline and define the first small validation increment. No Unity project or runtime AI integration exists yet.

## Important architecture rules

- AI controls language; deterministic game systems control reality.
- Unity will own authoritative game state and rule evaluation.
- LLM output must never directly modify canonical state.
- NPC language must be grounded by character cards, knowledge boundaries, world canon, and dynamic state.
- Narrative structure remains authored and branching.

## What has been completed

- Initial repository structure created.
- Project definition, decision log, current-state note, and working agreement recorded.
- Confirmed priorities captured: P0 semantic dialogue parsing, grounded NPC dialogue, and AI headline analysis; P1 memory/contradiction/QA/evaluation; P2 world reactions/voice.

## Immediate next task

Define and validate the smallest prototype increment for the core investigative loop and the deterministic boundary that converts interpreted player intent into system-controlled outcomes. Do not create a Unity project or implement Dify/runtime AI until explicitly authorised and the relevant approach is validated.

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
