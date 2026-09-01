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

VI01, VI02, and Pre-Prototype Gate 03 are integrated into the stable `main` baseline. The active prototype branch now carries **Frozen AI Interaction Contract v0.1.1**, which supersedes v0.1 while preserving v0.1 in Git history and the historical VI01/VI02/03 reports. Dialogue/Headline schemas, semantic taxonomies, authority boundaries, P0 scope, and the eight Hard Safety Gates remain unchanged.

No Unity project, production Dify workflow, backend runtime, final balance model, or final global-variable implementation is authorised by 03.

## Core architecture invariant

> **AI controls language. Deterministic game systems control reality.**

LLM output remains non-authoritative. It cannot create or mutate canonical state, evidence, branches, global-variable deltas, NPC commitments, evidence verdicts, or endings.

## Active technical-prototype handoff — Technical Prototype 01

Active working branch:

`prototype/technical-prototype-01`

Starting baseline:

`main @ aa87d39959e6a4b2f6cad31883528cb8e8d1cc42`

Technical Prototype 01 Batch 1 / 1.2 implementation and Contract documentation freeze checkpoint are complete on the prototype branch. The existing Batch 1 full-suite baseline is `48 passed`; the Batch 1.2 pre-checkpoint full suite is `61 passed / 0 failed` (`48` existing + `13` v0.1.1 regression tests) with Python 3.12, pytest, and jsonschema.

**Batch 2A — complete and accepted by 04 Master.** Commit `5f14abf8ddd759f9dcefd864cf9d7de213150ae7` adds a provider-independent `ScriptedAdapter`, component baseline runner, deterministic retry/fallback policy, and JSONL-compatible measurement logging. The full suite result is `82 passed / 0 failed`.

**Batch 2B.0 — implementation and final experiment-governance checkpoint complete.** The branch now contains an Experimental direct OpenAI Responses adapter, three versioned Experimental baseline prompts, two provider-specific transport schemas, a zero-call preflight, mock/fake-client coverage, and an explicit paid-smoke authorization sheet. The full suite result is `104 passed / 0 failed`. No OpenAI model request was made, cost remains `USD 0.00`, and no credential or secret was configured or tracked.

Paid smoke remains **PROPOSED_NOT_AUTHORIZED**. The proposed boundary is `gpt-5.6-terra`, `reasoning=low`, four logical cases, at most eight provider calls, SDK retries `0`, unchanged Frozen-runner retry policy, `8,192` input tokens and `1,024` output tokens per call, aggregate ceilings of `65,536` input and `8,192` output tokens, calculated worst case `USD 0.229376`, and an absolute planning ceiling of `USD 0.25`. If a prepared request is expected to exceed the per-call input ceiling, execution must stop before send; automatic ceiling expansion is forbidden.

01 Master completed the final Contract checkpoint and approved v0.1.1 as the new Frozen Contract baseline. The accepted implementation finding remains:

> Frozen v0.1 semantic completeness is not genuinely runtime-enforceable under the current free-text → semantic candidate → deterministic validator input boundary.

The implementation has three separate layers:

1. structural/schema validation checks candidate shape, legal fields/enums, and collection uniqueness;
2. deterministic runtime/context validation checks catalogue availability, allowed acts/values/polarity/tactics, visible evidence/sources, headline eligibility, and Pending Interaction validity;
3. the baseline fixture ground-truth oracle compares a candidate with a fixture-authored expected candidate for evaluation only.

The runtime validator has no independent authoritative semantic representation of arbitrary original player text. Therefore D19 tactic truncation, F04 incomplete Claim Set, and F05 invented but otherwise catalogue-valid extra Claim Atom pass structural and runtime/context validation and are rejected only by the evaluation fixture oracle. That oracle is not available for arbitrary production player input, is not a production validator, and does not create a production runtime retry signal.

Frozen v0.1.1 formally separates runtime contract validity and semantic fidelity/completeness. D18/T01/T10 are runtime PASS + fidelity PASS; D19/F04/F05 are runtime PASS + fidelity FAIL. Representative invalid enums/IDs/commitment modes, unresolved statuses, duplicate tactics, and unauthorised structured output remain deterministic runtime rejections.

Frozen Contract v0.1.1 and confirmed DEC-022 clarify that candidate-only inability to prove arbitrary free-text completeness is not itself a blocker once the responsibilities are explicit and the mandatory baseline detects fidelity failures. A blocker remains if the baseline misses tactic/Claim omissions or extra Claim Atoms, runtime PASS is conflated with fidelity PASS, a Hard Safety Gate is breached, or the model path requires shared schema/authority/P0 changes.

The v0.1.1 Contract is Frozen and DEC-022 is Confirmed. Historical VI01/VI02/03 reports remain unchanged. Dialogue/Headline schemas, semantic statuses, AI authority, Response Plan authority, P0 scope, and the eight Hard Safety Gates are unchanged. The Experimental fixture-scoped NPC lexical gate remains a recorded prototype limitation and is not a production Output Validation Gate.

Technical Prototype 01 Batch 1 / 1.2 → Contract v0.1.1 Frozen → Batch 2A complete → Batch 2B.0 preflight complete. Batch 2B.1 has not started, and paid smoke still requires separate explicit authorization.

Batch 2A confirms the operational policy boundary:

1. Dialogue retries only `AI_SYSTEM_FAILURE` once; valid `AMBIGUOUS` / `UNSUPPORTED` output does not model-retry.
2. Semantic-fidelity mismatch remains evaluation-only and never becomes a runtime retry signal.
3. Headline retry exhaustion has no Validated Claim Set, blocks publication, and preserves the draft; it is not `RESOLVED + claims=[]`.
4. NPC gate failure retries once, then may display only an authored fallback that preserves the deterministic Response Plan semantics and passes the Experimental fixture-scoped gate.
5. The Consequence Event stub remains isolated. No Hard Safety Gate breach or new Contract/schema/authority/P0 issue was found.

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

Next gated work: **Technical Prototype 01 paid smoke**, only after separate explicit authorization. Batch 2B.0 does not authorise credentials, model requests, paid calls, or Batch 2B.1.

Keep the next scope bounded: no Unity, no Dify yet, no backend architecture, no final story/world canon, no final balance model, and no P1/P2 expansion.

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
4. `docs/08_AI_INTERACTION_CONTRACT.md` — Frozen v0.1.1
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
15. `ai/prototype/validation.py`
16. `ai/eval/p0_baseline_manifest.v0.1.1.json`
17. `tests/test_contract_v011_regression.py`
18. `ai/prototype/adapters.py`
19. `ai/prototype/measurement.py`
20. `ai/prototype/runner.py`
21. `tests/test_baseline_runner.py`
22. `ai/eval/paid_smoke_authorization.experimental.v0.1.json`
23. `ai/prototype/openai_responses_adapter.py`
24. `ai/prototype/openai_preflight.py`

## Repository baseline

Current stable validated branch:

`main`

Active Experimental prototype branch:

`prototype/technical-prototype-01`

Completed historical 03 branch:

`design/pre-prototype-gate-03`
