# Handoff

## Project identity

**Between the Lines: AI Remake (BTL-AI)** is a PC-first, 2D, narrative/interface-driven journalism game targeting a polished **20–30 minute AI-assisted vertical slice**.

Portfolio goals:

1. demonstrate professional Game Design / Game System Design ability;
2. demonstrate professional AI Product / AI Orchestration ability.

## Current milestone

**03 — Pre-Prototype Gate: Core Consequences & AI Baseline**

Status:

**COMPLETE — integrated into `main`.**

VI01, VI02, and Pre-Prototype Gate 03 are now integrated into the stable `main` baseline. The **AI Interaction Contract v0.1 remains Frozen and unchanged**.

No Unity project, production Dify workflow, backend runtime, final balance model, or final global-variable implementation is authorised by 03.

## Core architecture invariant

> **AI controls language. Deterministic game systems control reality.**

LLM output remains non-authoritative. It cannot create or mutate canonical state, evidence, branches, global-variable deltas, NPC commitments, evidence verdicts, or endings.

## Active Contract-review handoff — Technical Prototype 01

Active working branch:

`prototype/technical-prototype-01`

Starting baseline:

`main @ aa87d39959e6a4b2f6cad31883528cb8e8d1cc42`

Technical Prototype 01 Batch 1 is implemented on the prototype branch and locally verified, but it is **not accepted**, integrated, or a production architecture decision. The latest full test result is `48 passed` with Python 3.12, pytest, and jsonschema.

04 Master accepted the Batch 1.1 Completeness Enforcement finding as a Contract-review blocker:

> Frozen v0.1 semantic completeness is not genuinely runtime-enforceable under the current free-text → semantic candidate → deterministic validator input boundary.

The implementation has three separate layers:

1. structural/schema validation checks candidate shape, legal fields/enums, and collection uniqueness;
2. deterministic runtime/context validation checks catalogue availability, allowed acts/values/polarity/tactics, visible evidence/sources, headline eligibility, and Pending Interaction validity;
3. the baseline fixture ground-truth oracle compares a candidate with a fixture-authored expected candidate for evaluation only.

The runtime validator has no independent authoritative semantic representation of arbitrary original player text. Therefore D19 tactic truncation, F04 incomplete Claim Set, and F05 invented but otherwise catalogue-valid extra Claim Atom pass structural and runtime/context validation and are rejected only by the evaluation fixture oracle. That oracle is not available for arbitrary production player input and must not be represented as a production validator.

Gate 03 section 4.8 item 2 and the DEC-021 incomplete-Claim-Set blocker apply. Batch 2 is paused. No Frozen Contract or Decision Log change has been made.

**Issue requiring 01 Master review:** reconcile the Frozen requirements that all expressed gameplay-relevant tactics be present and that every Claim Set be complete with no omitted or invented consequential Claim Atom, against a runtime boundary that currently has only the original free text, a non-authoritative semantic candidate, and deterministic catalogue/context data. No resolution category has been selected or confirmed.

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

Return the accepted Batch 1.1 technical finding to **01 Master Contract review**.

01 Master must resolve or clarify the mismatch between the Frozen semantic-completeness requirements and the currently authorised runtime input/authority boundary before implementation continues. Batch 1 remains unaccepted and Batch 2 must not start while the blocker remains unresolved.

Do not change the Frozen Contract, Decision Log, semantic schemas, AI authority boundary, or P0 scope before that review.

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

Current stable validated branch:

`main`

Active Experimental prototype branch:

`prototype/technical-prototype-01`

Completed historical 03 branch:

`design/pre-prototype-gate-03`
