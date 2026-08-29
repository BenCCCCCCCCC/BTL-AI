# Handoff

## Project identity

**Between the Lines: AI Remake (BTL-AI)** is a PC-first, 2D, narrative/interface-driven journalism game targeting a polished **20–30 minute AI-assisted vertical slice**.

Portfolio goals:

1. demonstrate professional Game Design / Game System Design ability;
2. demonstrate professional AI Product / AI Orchestration ability.

## Current milestone

**03 — Pre-Prototype Gate: Core Consequences & AI Baseline**

Status:

**COMPLETE on `design/pre-prototype-gate-03` — pending integration into `main`.**

VI01 and VI02 remain integrated in `main`. The **AI Interaction Contract v0.1 remains Frozen and unchanged**.

No Unity project, production Dify workflow, backend runtime, final balance model, or final global-variable implementation is authorised by 03.

## Core architecture invariant

> **AI controls language. Deterministic game systems control reality.**

LLM output remains non-authoritative. It cannot create or mutate canonical state, evidence, branches, global-variable deltas, NPC commitments, evidence verdicts, or endings.

## 03 result

Detailed report:

- `docs/11_PRE_PROTOTYPE_GATE_03_REPORT.md`

### DEC-020 — Minimal consequence interface

```text
Deterministically Resolved Gameplay Result
        ↓
Authored Consequence Event
        ↓
Deterministic Variable Effect
        ↓
Reputation / Public Opinion / Threat Level / Money
```

A semantic candidate, Claim Atom, publication support label, or NPC surface response can never directly alter a global variable. There is no automatic Evidence–Claim-status-to-Reputation mapping and no implicit cross-variable formula.

Exact balance remains deferred; later technical tests may use clearly marked Experimental placeholder deltas.

### DEC-021 — Real-model baseline protocol

The first baseline reuses the Frozen 01/02 fixture evidence through a versioned manifest and tests the three P0 model boundaries separately:

- Dialogue Semantic Parser;
- Headline Analyzer;
- Grounded NPC Surface Generator.

The baseline must run deterministic validators/gates, deliberate invalid-output/fault-injection cases, retry/fallback paths, Frozen quality metrics, and latency/token/cost logging. Numerical acceptance thresholds are intentionally deferred until the first measurements exist.

`02B` stays deterministic downstream Evidence–Claim evaluation; the model does not judge evidence sufficiency or truth.

A Hard Safety Gate breach, inability to reject invalid structured output, fallback semantic drift, or a need to change Frozen semantics merely to make the model path work blocks progression and returns to the appropriate Master/Contract review.

## Dependencies / parallelisation

The consequence interface and AI baseline protocol are independent after the shared Frozen 01/02 baseline. During technical prototyping, the following may be implemented in parallel:

```text
Track A — deterministic Consequence Event stub
Track B — P0 AI baseline harness + validators
```

They should only be integrated after both work independently.

## Prototype entry criteria

03's pre-prototype exit criteria are satisfied:

- all four global variables have a minimal deterministic entry interface;
- the real-model baseline protocol is defined from existing fixtures;
- no new shared Contract semantics are required;
- P0 scope did not expand;
- first technical tasks are explicit;
- additional abstract pre-production architecture is not required before prototyping.

## Explicitly deferred

Do not expand the next implementation scope into:

- final story/world canon or complete NPC roster;
- production catalogue/evidence/NPC authoring systems;
- final evidence authenticity/persistence policy;
- relationship formulas, richer epistemic models, or P1 NPC memory;
- NPC-originated free-form negotiation;
- generic rhetorical scoring;
- final four-variable balance, decay, cross-variable formulas, or ending thresholds;
- backend/API architecture unless the prototype evidences a need;
- Unity architecture/client implementation;
- P1/P2 AI features.

## Next project step

After 03 is integrated into `main`, open a new implementation thread:

**04｜Technical Prototype 01 — P0 AI Baseline Harness**

Scope:

1. convert existing fixture cases into a machine-readable/versioned baseline manifest without changing their semantics;
2. implement deterministic schema/contract validators and a minimal NPC Output Validation Gate;
3. implement retry/fallback execution and measurement logging;
4. implement a thin deterministic Consequence Event stub with Experimental placeholder effects;
5. run the first direct real-model baseline;
6. only after that, evaluate minimal Dify reproduction/overhead if separately authorised.

Do **not** create a Unity project for this step.

## Documentation protocol

The Git repository is the canonical working copy. Project Sources are stable cross-chat snapshots and do not update automatically when GitHub changes.

At substantial GitHub checkpoints, report:

- exact GitHub files changed;
- whether local repository sync is required;
- which Project Sources must be refreshed;
- whether Project Sources are currently stale;
- the minimum manual user action required.

## Files the next thread should read first

1. BTL-AI ChatGPT Project Instructions
2. `docs/01_PROJECT_DEFINITION.md`
3. `docs/05_DECISION_LOG.md`
4. `docs/08_AI_INTERACTION_CONTRACT.md` — Frozen v0.1
5. `docs/06_CURRENT_STATE.md`
6. `docs/07_HANDOFF.md`
7. `docs/09_VALIDATION_INCREMENT_01_REPORT.md`
8. `docs/10_VALIDATION_INCREMENT_02_REPORT.md`
9. `docs/11_PRE_PROTOTYPE_GATE_03_REPORT.md`
10. `tests/01A_DIALOGUE_NPC_VALIDATION_FIXTURE.md`
11. `tests/01B_HEADLINE_VALIDATION_FIXTURE.md`
12. `tests/02A_SEMANTIC_TARGET_CATALOGUE_FIXTURE.md`
13. `tests/02B_EVIDENCE_CLAIM_RULES_FIXTURE.md`
14. `tests/02C_NPC_STATE_CHARACTER_CARD_SCHEMA_FIXTURE.md`

## Repository baseline

Stable integrated branch before 03 merge:

`main`

Current 03 working branch:

`design/pre-prototype-gate-03`
