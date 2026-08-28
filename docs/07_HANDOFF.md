# Handoff

## Project identity

**Between the Lines: AI Remake (BTL-AI)** is a pre-production, PC-first, 2D, narrative/interface-driven journalism game.

The initial target is a polished **20–30 minute AI-assisted vertical slice**, not the full legacy 14-day experience.

Portfolio goals:

1. demonstrate professional Game Design / Game System Design ability;
2. demonstrate professional AI Product / AI Orchestration ability.

## Current milestone

**Validation Increment 02 — Authored Semantic & Deterministic Fixture Validation**

Status:

**Active — 02A accepted; 02B and 02C authorised in parallel**

Validation Increment 01 is complete and the **AI Interaction Contract v0.1 remains Frozen**.

No Unity project, Dify runtime workflow, backend runtime, production prompt, or production AI implementation is authorised by the current milestone.

## Core architecture invariant

> **AI controls language. Deterministic game systems control reality.**

LLM output is non-authoritative and must not directly:

- modify canonical game state;
- change gameplay variables;
- create canonical evidence;
- unlock narrative branches;
- determine endings;
- invent critical canonical world facts;
- override authored narrative rules.

## Frozen P0 interaction boundary

### Dialogue Semantic Parser

Frozen v0.1 represents a player turn through semantic status, act, authored target, conditional value/polarity, all gameplay-relevant tactics, and explicit player-visible evidence references.

Dialogue allows one consequential semantic action per turn. `REQUEST` is unilateral. `OFFER` is an authored bilateral deal. Unsupported free-form deals fail safely.

### Grounded NPC response

The Frozen pipeline is:

```text
Validated Player Semantic Action
→ Deterministic NPC Rule Resolution
→ Deterministic NPC Response Plan
→ LLM Surface Candidate
→ NPC Output Validation Gate
→ Display
```

The generator does not decide clue release, relationship changes, compliance, deception, state changes, deals, or branches.

### Headline analysis

The Headline Analyzer returns all consequential Claim Atoms with authored target/value, polarity, commitment mode, and optional source attribution.

Attribution support, underlying-proposition support, canonical reality, and publication responsibility are separate deterministic concepts. Publication responsibility is evaluated against an auditable publication-time evidence/knowledge basis and is not rewritten by later evidence.

## Validation Increment 01 record

Validation Increment 01 completed and froze the shared AI Interaction Contract v0.1.

Specialist evidence:

- `tests/01A_DIALOGUE_NPC_VALIDATION_FIXTURE.md`
- `tests/01B_HEADLINE_VALIDATION_FIXTURE.md`

Targeted regression commits:

- 01A: `659be28db16bea586136ac00a053f1f01452df96`
- 01B: `477086429c6beee7fae4da439383708803cf16f4`

VI01 was integrated into `main` at `28a6a9650fca8d6ad8ade992794d5d2f140e4b6f`.

## Validation Increment 02 — 02A accepted baseline

02A tested whether the Frozen Contract can be instantiated by one small authored reality shared across Dialogue, Grounded NPC Response, and Headline analysis.

Result:

**02A ACCEPTED — Frozen Contract change not required.**

Reproducible evidence:

- `tests/02A_SEMANTIC_TARGET_CATALOGUE_FIXTURE.md`

The fixture is **Experimental / Validation-only / Non-canonical**.

### Shared validation fixture

Event:

- `EVENT_RAILYARD_CLASH`

Temporary NPCs:

- `NPC_WITNESS_A`
- `NPC_CLERK_A`

Shared propositions:

- `PROP_FIRE_FIRST`
- `PROP_FUNDED_OPERATION`

Temporary evidence/source IDs:

- `EV_AUDIO_A`
- `EV_VIDEO_A`
- `EV_LEDGER_A`
- `SRC_WITNESS_A`

Dialogue-only request/deal/pending IDs:

- `REQ_HAND_OVER_LEDGER`
- `DEAL_LEDGER_FOR_500` — currently exposed in the fixture
- `DEAL_LEDGER_FOR_300` — authored but unavailable in the fixture
- `PENDING_LEDGER_500`

None of these story/NPC details are final canon.

### Confirmed catalogue architecture

DEC-017 confirms:

```text
Global Authored Semantic Registry
        ↓
Deterministic Runtime Projection
        ↓
Parser-specific Runtime Catalogue Views
```

Key rules:

- identical propositions reuse one globally unique authored ID across relevant P0 systems;
- dialogue-only REQUEST/DEAL meanings remain scoped to dialogue;
- only currently exposed meanings are supplied to AI parsers;
- authored-but-unavailable meanings are omitted from the current Runtime View;
- evidence, sources, and Pending Interactions remain separate deterministic runtime registries/context;
- unavailable or nonexistent model-returned IDs are rejected deterministically and never become gameplay reality;
- no new semantic status or Frozen output field was required.

## 02B specialist assignment

Thread:

**`02B｜Evidence–Claim Deterministic Rules Validation`**

Use the 02A fixture without inventing a new scenario.

Primary questions:

- how Evidence–Claim relationships are authored deterministically;
- how attribution support differs from underlying-proposition support;
- how canonical reality remains separate;
- what a publication-time player knowledge/evidence snapshot minimally contains;
- how later evidence is prevented from retroactively rewriting original publication responsibility;
- how multi-evidence and contradictory-evidence cases resolve deterministically.

02B must not define Reputation/Public Opinion/Threat/Money deltas or use an LLM to decide evidence sufficiency.

## 02C specialist assignment

Thread:

**`02C｜NPC State & Character-Card Schema Validation`**

Use `NPC_WITNESS_A` and `NPC_CLERK_A` only as temporary validation subjects.

Primary questions:

- what belongs in the static authored NPC card;
- what belongs in authoritative dynamic NPC state;
- how knowledge boundaries are represented;
- what current interaction state is required;
- what deterministic inputs produce NPC rule resolution and a Response Plan;
- what minimal information the LLM generator needs;
- what hidden canonical information should be withheld under least-knowledge/context-minimisation.

02C must not turn the temporary fixture into final character/world canon.

## Shared-change escalation rule

02B and 02C must stop specialist-level confirmation and return to the 02 Master if they require changes to:

- shared semantic schema;
- semantic statuses;
- Dialogue Act taxonomy;
- Claim Atom schema;
- Response Plan authority semantics;
- AI authority boundary;
- P0 scope;
- shared cross-system evidence assumptions;
- hard safety gates.

If 02 Master determines that the Frozen AI Interaction Contract must change, the issue must return to **01｜AI Interaction Contract — Validation Increment 01** for a narrowly scoped Master review before becoming Confirmed.

## Do not do yet

Do not:

- create a Unity project;
- implement gameplay state classes;
- build a Dify runtime workflow;
- choose production prompts;
- measure a production AI-model baseline;
- lock backend/API architecture;
- define final four-global-variable formulas or thresholds;
- design the full 14-day game;
- promote the temporary railyard fixture into final canon merely because it is convenient for validation.

## Known unresolved questions

- final Evidence–Claim Relationship rules;
- publication snapshot persistence details;
- final NPC state / knowledge / character-card schema;
- whether Response Plan proposition data directly reuses shared proposition IDs or a separate authored response-content registry;
- NPC-originated authored-offer lifecycle;
- production catalogue serialization/exposure rules/authoring tools;
- final vertical-slice story canon, NPC roster, and faction design;
- Reputation/Public Opinion/Threat/Money deterministic rules;
- AI model baseline and acceptance thresholds;
- Dify feasibility/integration;
- backend/API architecture;
- Unity implementation architecture;
- whether rhetorical framing eventually needs authoritative gameplay semantics.

## Documentation protocol

The Git repository is the canonical working copy.

At each substantial specialist or Master checkpoint:

- preserve detailed reproducible validation evidence in the relevant `tests/` fixture file;
- update `06_CURRENT_STATE.md` when active/completed work or unresolved blockers change;
- update this `07_HANDOFF.md` with the concise cross-thread state needed to resume work;
- update `05_DECISION_LOG.md` only when a decision has become Confirmed;
- do not use the Handoff as a full transcript or duplicate all fixture cases;
- create/update a milestone report only when that validation increment reaches a real integration checkpoint.

Chat discussion alone is not the canonical project record. When tooling allows, repository documentation should be synchronised directly rather than requiring the user to manually edit text.

## Files future VI02 specialist threads should read first

1. BTL-AI ChatGPT Project Instructions
2. `docs/01_PROJECT_DEFINITION.md`
3. `docs/05_DECISION_LOG.md`
4. `docs/08_AI_INTERACTION_CONTRACT.md` — Frozen v0.1
5. `docs/06_CURRENT_STATE.md`
6. `docs/07_HANDOFF.md`
7. `docs/09_VALIDATION_INCREMENT_01_REPORT.md`
8. `tests/01A_DIALOGUE_NPC_VALIDATION_FIXTURE.md`
9. `tests/01B_HEADLINE_VALIDATION_FIXTURE.md`
10. `tests/02A_SEMANTIC_TARGET_CATALOGUE_FIXTURE.md`

## Repository baseline

Stable validated branch:

`main`

Current active working branch:

`design/validation-increment-02`

Do not assume the default branch is the newest working state during VI02. Specialist threads should read the active working branch identified here.
