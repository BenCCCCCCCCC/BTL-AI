# Working Agreement

## Before significant changes

Read `README.md`, `docs/01_PROJECT_DEFINITION.md`, `docs/05_DECISION_LOG.md`, and `docs/06_CURRENT_STATE.md`. Read `docs/07_HANDOFF.md` when taking over work from another environment or tool.

## Architecture invariants

- AI controls language; deterministic game systems control reality.
- Unity is the authoritative owner of game state and rule evaluation.
- LLM output must never directly modify canonical game state.
- AI NPC output must be grounded by character cards, knowledge boundaries, world canon, and dynamic state.

## Do not

- Do not create a Unity project unless explicitly requested.
- Do not implement Dify or runtime AI features until their design and integration are validated.
- Do not replace authored branching narrative with fully AI-generated plot.
- Do not invent detailed story canon, NPCs, factions, or unresolved technical architecture.
- Do not commit, push, or alter unrelated work without explicit approval.

## Delivery approach

Work in the smallest testable increment. State assumptions, keep changes narrowly scoped, and update the decision log only for confirmed decisions.

## Testing and documentation

Add or update appropriate tests for behavior changes. Update `06_CURRENT_STATE.md` for milestone progress and relevant docs when a confirmed product or architecture decision changes.

## Definition of done

The requested increment is implemented, appropriately verified, documented where needed, and leaves canonical state ownership and AI boundaries intact.
