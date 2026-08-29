# Current State

## Current phase

Pre-production — **Pre-Prototype Gate 03 complete and integrated into `main`.**

`main` is now the current stable validated baseline for completed VI01 + VI02 + Pre-Prototype Gate 03 work.

01 Master final checkpoint passed. **AI Interaction Contract v0.1.1 is Frozen** as the current Contract baseline on the active prototype branch; v0.1 remains preserved in Git history and historical VI01, VI02, and Pre-Prototype Gate 03 reports. Dialogue/Headline schemas, semantic taxonomies, authority boundaries, P0 scope, and the existing eight Hard Safety Gates remain unchanged. v0.1.1 is not yet integrated into `main`.

No Unity project, production Dify workflow, backend runtime, final balance model, or final four-global-variable implementation is authorised by this state.

## Technical Prototype 01 — Batch 1 branch milestone

**Status:** Technical Prototype 01 Batch 1 / 1.2 implementation and targeted regression are complete on `prototype/technical-prototype-01`. 01 Master final checkpoint passed; Contract v0.1.1 is Frozen, DEC-022 remains Confirmed, and Batch 2 is **AUTHORISED** after this documentation freeze checkpoint.

Batch 1 adds:

- a small versioned P0 baseline manifest traced to the Frozen 01A/01B/02C fixture cases;
- Frozen-v0.1 structural JSON Schemas for Dialogue and Headline semantic candidates;
- deterministic current-catalogue contract validators for Dialogue and Headline candidates;
- a separate fixture ground-truth oracle for tactic and Claim Set omissions/extras;
- an explicitly Experimental, fixture-scoped lexical NPC Output Validation Gate;
- an isolated deterministic Consequence Event stub with immutable Experimental authoritative test state and placeholder effects for all four global variables;
- automated fault-injection and authority-boundary tests.

Existing Batch 1 full-suite baseline: `48 passed`. Batch 1.2 pre-checkpoint full suite: `61 passed` (`48` existing + `13` v0.1.1 regression tests) with Python 3.12, pytest, and jsonschema.

The v0.1.1 assurance responsibilities are explicit and separate:

1. **Deterministic runtime contract validity** covers observable schema, enum, current-catalogue, context, compatibility, visibility, Pending Interaction, structured single-action, Claim Atom legality, and authority-boundary conditions.
2. **Semantic fidelity/completeness** covers tactic omission, consequential Claim Atom omission, catalogue-valid but source-text-unsupported extra Claim Atoms, and general interpretation fidelity. Batch 1 measures this against authored fixture ground truth; D19/F04/F05 are detected only by this evaluation oracle, not by candidate-only runtime validation.

Runtime contract PASS and semantic fidelity PASS are not interchangeable. Candidate-only runtime inability to prove arbitrary free-text completeness is no longer itself a blocker once this separation is explicit and the mandatory baseline detects the required errors. Blocking conditions remain if the baseline cannot detect tactic/Claim omissions or extra Claim Atoms, if runtime PASS is conflated with fidelity PASS, if a Hard Safety Gate is breached, or if the model path requires shared schema/authority/P0 changes.

The Experimental fixture-scoped lexical NPC Output Validation Gate limitation remains recorded. It is validation tooling, not the final production Output Validation Gate, and is not promoted to a Contract change by v0.1.1.

**Review routing:** Runtime contract validity and semantic fidelity/completeness are formally separated in Frozen Contract v0.1.1. No further 01 Master review is required unless later work produces a new shared Contract, schema, authority, or P0-scope issue. Batch 2 is **AUTHORISED**; it has not begun in this documentation checkpoint.

## Completed

- Repository baseline and product definition completed.
- Validation Increment 01 completed; AI Interaction Contract v0.1 frozen.
- Validation Increment 02 completed and integrated into `main`.
- Pre-Prototype Gate 03 completed, Master-reviewed, and integrated into `main`.
- 03 confirmed the minimal deterministic consequence boundary (DEC-020).
- 03 confirmed the real-model P0 baseline protocol (DEC-021).
- 01 Master final Contract checkpoint passed: AI Interaction Contract v0.1.1 Frozen; DEC-022 Confirmed; Batch 2 authorised.
- Detailed 03 result recorded in `docs/11_PRE_PROTOTYPE_GATE_03_REPORT.md`.

## Confirmed Pre-Prototype Gate 03 result

### DEC-020 — Minimal deterministic consequence boundary

```text
Deterministically Resolved Gameplay Result
        ↓
Authored Consequence Event
        ↓
Deterministic Variable Effect
        ↓
Authoritative Global-Variable State Update
```

Only authored deterministic consequence rules may change Reputation, Public Opinion, Threat Level, or Money.

AI semantic candidates, validated Claim Atoms, evidence/publication support labels, and NPC surface language never directly create variable deltas. Result type only determines possible eligibility; an authored consequence rule determines whether an effect actually exists.

Exact deltas, ranges, balancing, cross-variable formulas, decay, and ending thresholds remain deferred. Experimental placeholder deltas may be used later only to exercise the technical interface.

Legacy BTL variable formulas remain historical evidence, not confirmed Remake rules.

### DEC-021 — First real-model P0 baseline

The first measured AI baseline will reuse the Frozen 01/02 fixtures through a versioned manifest and separately test:

1. Dialogue Semantic Parser;
2. Headline Analyzer;
3. Grounded NPC Surface Generator.

The baseline includes deterministic validator/gate checks, deliberate invalid-output/fault injection, retry/fallback execution, Frozen quality metrics, and latency/token/cost logging. No numerical acceptance threshold is defined before the first baseline is measured.

`02B` remains deterministic downstream evaluation and is not converted into an LLM evidence/truth task.

Dify feasibility is evaluated after a direct baseline harness exists, so model performance and orchestration overhead can be separated.

## Historical Gate 03 Contract status

Pre-Prototype Gate 03 requires **no change** to:

- AI authority boundary;
- P0 scope;
- Dialogue semantic schema or status taxonomy;
- Claim Atom schema;
- Response Plan authority semantics;
- hard safety gates.

**At Gate 03, 01 Master review required:** No.

## Prototype entry assessment

The project now has enough pre-production definition to stop adding abstract architecture and begin a narrowly scoped technical prototype.

The first technical prototype should prove:

- a versioned P0 baseline manifest derived from existing fixtures;
- model calls for the three P0 language boundaries;
- deterministic contract validators and a minimal NPC Output Validation Gate;
- retry/fallback behaviour;
- reproducible measurement/logging;
- a thin deterministic Consequence Event stub capable of exercising all four global variables with Experimental placeholder effects.

No Unity client is required for this first technical prototype.

## Still unresolved / deferred

- actual real-model baseline measurements and acceptance thresholds;
- Dify feasibility and orchestration overhead;
- final vertical-slice story canon and NPC/faction/world roster;
- production catalogue/evidence/NPC serialization and authoring tooling;
- production evidence persistence/authenticity policy;
- exact non-world Response Plan serialization;
- NPC-originated authored-offer lifecycle;
- final NPC relationship system or richer epistemic model;
- final Reputation / Public Opinion / Threat Level / Money ranges, deltas, formulas, balancing, decay, and ending thresholds;
- backend/API architecture;
- Unity architecture and implementation;
- P1/P2 AI features.

## Next

1. Next authorised work: Technical Prototype 01 Batch 2, under a separately scoped task.
2. Return to 01 Master only if later work produces a new shared Contract, schema, authority, or P0-scope issue.

## Repository baseline

Current stable validated branch:

`main`

Completed historical 03 branch:

`design/pre-prototype-gate-03`
