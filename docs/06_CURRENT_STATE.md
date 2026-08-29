# Current State

## Current phase

Pre-production — **Pre-Prototype Gate 03 complete and integrated into `main`.**

`main` is now the current stable validated baseline for completed VI01 + VI02 + Pre-Prototype Gate 03 work.

The **AI Interaction Contract v0.1 remains Frozen and unchanged**.

No Unity project, production Dify workflow, backend runtime, final balance model, or final four-global-variable implementation is authorised by this state.

## Technical Prototype 01 — Batch 1 branch milestone

**Status:** Implemented and locally verified on `prototype/technical-prototype-01`, but **not accepted**. 04 Master accepted the Batch 1.1 technical finding as a Contract-review blocker. Batch 1 now requires 01 Master Contract review before any resolution is selected or implemented. It is not integrated or promoted to a production architecture decision.

Batch 1 adds:

- a small versioned P0 baseline manifest traced to the Frozen 01A/01B/02C fixture cases;
- Frozen-v0.1 structural JSON Schemas for Dialogue and Headline semantic candidates;
- deterministic current-catalogue contract validators for Dialogue and Headline candidates;
- a separate fixture ground-truth oracle for tactic and Claim Set omissions/extras;
- an explicitly Experimental, fixture-scoped lexical NPC Output Validation Gate;
- an isolated deterministic Consequence Event stub with immutable Experimental authoritative test state and placeholder effects for all four global variables;
- automated fault-injection and authority-boundary tests.

Local verification: `48 passed` with Python 3.12, pytest, and jsonschema.

One active prototype blocker and one Experimental limitation are explicit rather than hidden:

1. **Active Gate 03 blocker:** Candidate-only runtime validation cannot prove natural-language tactic completeness, Claim Set completeness, or absence of an invented but otherwise catalogue-valid Claim Atom. Batch 1 detects D19/F04/F05 only by comparing candidates with fixture-authored expected semantics. That baseline oracle is evaluation-only and is not available for arbitrary production player text. Therefore the Frozen Contract requirements that all expressed tactics be present with no silent truncation and that the Claim Set be complete with no omitted or extra consequential claim are not currently runtime-enforceable under the implemented input boundary. Gate 03 section 4.8 item 2 applies; Batch 2 must not start while this remains unresolved.
2. Natural-language required/forbidden NPC proposition coverage is lexical and fixture-specific in Batch 1. It is validation tooling, not the final production Output Validation Gate.

Frozen Contract v0.1, the AI authority boundary, and all confirmed semantic taxonomies remain unchanged.

**Review routing:** 04 Master has accepted the completeness finding. **01 Master Contract review is now required** to reconcile the Frozen completeness requirements with the current free-text → semantic candidate → deterministic validator input boundary. No Frozen Contract change has been made, and no resolution category is selected or confirmed by this branch.

## Completed

- Repository baseline and product definition completed.
- Validation Increment 01 completed; AI Interaction Contract v0.1 frozen.
- Validation Increment 02 completed and integrated into `main`.
- Pre-Prototype Gate 03 completed, Master-reviewed, and integrated into `main`.
- 03 confirmed the minimal deterministic consequence boundary (DEC-020).
- 03 confirmed the real-model P0 baseline protocol (DEC-021).
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

## Contract status

Pre-Prototype Gate 03 requires **no change** to:

- AI authority boundary;
- P0 scope;
- Dialogue semantic schema or status taxonomy;
- Claim Atom schema;
- Response Plan authority semantics;
- hard safety gates.

**01 Master review required:** No.

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

1. Hand the accepted Batch 1.1 Completeness Enforcement finding to 01 Master for Contract review.
2. Keep Batch 1 unaccepted and keep Batch 2 paused while the blocker remains unresolved.
3. Do not change Frozen Contract semantics, the authorised input/authority boundary, or P0 scope until 01 Master selects and confirms a resolution.

## Repository baseline

Current stable validated branch:

`main`

Completed historical 03 branch:

`design/pre-prototype-gate-03`
