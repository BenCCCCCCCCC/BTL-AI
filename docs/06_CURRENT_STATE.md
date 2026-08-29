# Current State

## Current phase

Pre-production — **Pre-Prototype Gate 03 complete on `design/pre-prototype-gate-03`, pending integration into `main`.**

`main` remains the current stable integrated VI01 + VI02 baseline until the 03 branch is merged.

The **AI Interaction Contract v0.1 remains Frozen and unchanged**.

No Unity project, production Dify workflow, backend runtime, final balance model, or final four-global-variable implementation is authorised by this state.

## Completed

- Repository baseline and product definition completed.
- Validation Increment 01 completed; AI Interaction Contract v0.1 frozen.
- Validation Increment 02 completed and integrated into `main`.
- Pre-Prototype Gate 03 completed in the current design branch.
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

The project now has enough pre-production definition to stop adding abstract architecture and begin a narrowly scoped technical prototype after 03 is integrated.

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

1. Review and integrate `design/pre-prototype-gate-03` into `main`.
2. Open a new technical-prototype implementation thread rather than extending 03.
3. Build the P0 AI baseline harness and deterministic consequence stub before Dify or Unity production work.
4. Run a direct real-model baseline and measure it.
5. Then evaluate a minimal Dify reproduction/feasibility path if authorised.

## Repository baseline

Stable integrated branch before 03 merge:

`main`

Current 03 working branch:

`design/pre-prototype-gate-03`
