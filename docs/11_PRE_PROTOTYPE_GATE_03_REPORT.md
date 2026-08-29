# Pre-Prototype Gate 03 Report

**Project:** Between the Lines: AI Remake (BTL-AI)  
**Status:** Complete  
**Date:** 2026-08-29  
**Working branch:** `design/pre-prototype-gate-03`  
**Contract baseline:** `docs/08_AI_INTERACTION_CONTRACT.md` — Frozen v0.1

## 1. Purpose

03 is a short exit gate between completed paper validation and the first technical prototype. It answers only two questions:

1. what is the smallest deterministic interface needed to connect resolved gameplay outcomes to Reputation, Public Opinion, Threat Level, and Money;
2. how the existing VI01/VI02 fixtures should be used for the first real-model P0 baseline.

It does not define final balance, story canon, production Dify architecture, backend architecture, or Unity implementation.

The governing principle remains:

> **AI controls language. Deterministic game systems control reality.**

## 2. Baseline reviewed

03 starts from the integrated VI01 + VI02 baseline in `main`:

- Frozen AI Interaction Contract v0.1;
- accepted semantic registry / Runtime Catalogue architecture (DEC-017);
- deterministic Evidence–Claim publication model (DEC-018);
- deterministic NPC grounding / least-knowledge boundary (DEC-019);
- reproducible fixtures in `tests/01A`, `01B`, `02A`, `02B`, and `02C`.

No 03 finding requires changing the Frozen Contract.

## 3. A — Minimal deterministic consequence model

### 3.1 Required interface

The accepted minimum consequence path is:

```text
Deterministically Resolved Gameplay Result
        ↓
Authored Consequence Event
        ↓
Deterministic Variable Effect
        ↓
Authoritative Global-Variable State Update
```

Only the deterministic game layer may create/apply a Consequence Event.

The following are never direct variable-change triggers:

- raw LLM output;
- semantic candidates;
- validated Dialogue semantic actions by themselves;
- Claim Atoms by themselves;
- publication `SUPPORTED` / `CONTRADICTED` / `INSUFFICIENT` labels by themselves;
- NPC surface text;
- model retry/fallback events.

### 3.2 Consequence eligibility

The result category determines only whether an authored variable consequence is plausible. It does not automatically create an effect.

| Deterministic result category | Reputation | Public Opinion | Threat Level | Money |
| --- | --- | --- | --- | --- |
| Completed authored publication outcome | Eligible when it changes the journalist's public/professional standing | Eligible when it creates an authored public reaction | Eligible when it changes authored exposure, retaliation, or protection risk | Only when an explicit economic consequence exists |
| Resolved NPC/request/deal outcome | Only with an authored public/professional consequence | Only when the interaction creates an authored public consequence | Eligible for authored exposure/protection/retaliation outcomes | Eligible for explicit transaction, cost, reward, or payment outcomes |
| Authored story/external event | Eligible when explicitly authored | Eligible when explicitly authored | Eligible when explicitly authored | Eligible when explicitly authored |
| Evidence/clue acquisition alone | No automatic effect | No automatic effect | No automatic effect | No automatic effect |
| Semantic / Claim / surface-language output | Never direct | Never direct | Never direct | Never direct |

This is a routing/authority rule, not a balance model.

### 3.3 Explicit non-decisions

03 does not define:

- variable ranges;
- numeric deltas;
- decay;
- cross-variable formulas;
- daily update formulas;
- ending thresholds;
- a complete economy or public-opinion simulation.

A later technical prototype may use clearly labelled **Experimental placeholder deltas** solely to prove that the consequence interface works. Those values are not Confirmed balance.

Legacy BTL formulas and thresholds remain historical evidence only.

**03 result for A:** Accepted and recorded as DEC-020.

## 4. B — First real-model / AI baseline protocol

### 4.1 Dataset source

Do not create a new large conceptual fixture milestone. Build a versioned baseline manifest that references/copies the expected cases already established by VI01/VI02.

| Component | Primary fixture evidence | Role |
| --- | --- | --- |
| Dialogue Semantic Parser | `tests/01A_DIALOGUE_NPC_VALIDATION_FIXTURE.md` + relevant `02A` catalogue cases | Real-model semantic baseline |
| Headline Analyzer | `tests/01B_HEADLINE_VALIDATION_FIXTURE.md` + relevant `02A` catalogue cases | Real-model Claim Atom baseline |
| Grounded NPC Surface Generator | `01A` NPC Response cases + `02C` Response Plan / least-knowledge cases | Real-model surface-generation baseline |
| Evidence–Claim evaluation | `tests/02B_EVIDENCE_CLAIM_RULES_FIXTURE.md` | Deterministic downstream regression only; not an LLM judging task |

The shared railyard content remains Experimental / Validation-only / Non-canonical.

### 4.2 Model input and output boundaries

#### Dialogue Semantic Parser

Model may receive:

- player text;
- current parser-specific Runtime Catalogue View;
- relevant player-visible evidence references;
- deterministic Pending Interaction/context required by the Frozen Contract.

Model must not receive authority over hidden canon, global-variable rules, branch rules, or unavailable meanings.

Expected output is the Frozen Dialogue structured candidate only.

#### Headline Analyzer

Model may receive:

- headline text;
- Headline Runtime Catalogue View;
- relevant visible authored sources;
- deterministic current-event context where already known by the UI/game.

Model does not receive Evidence–Claim sufficiency rules, evidence verdict authority, canonical truth, or variable-consequence rules.

Expected output is Frozen `status + claims[]` only.

#### Grounded NPC Surface Generator

Model receives only the minimal generator-language projection validated in VI02:

- speaker identity/role if needed for wording;
- voice/language constraints;
- deterministic response mode;
- required authorised utterance content;
- safe permitted wording context;
- minimum player-visible recent context needed for fluency.

It should not receive hidden canonical truth, locked clues, raw relationship numbers/rules, branch IDs, state deltas, unrelated evidence, or full world state.

Expected authoritative model output is NPC surface text only.

### 4.3 Deterministic validators and fault injection

The baseline has two mandatory test paths.

**Path 1 — real-model cases**

```text
Fixture input
→ real model
→ non-authoritative output
→ deterministic validator/gate
→ measured result
```

**Path 2 — deliberate invalid-output cases**

Inject malformed or unauthorised candidates directly into the validator/gate, including invalid enums/IDs, incomplete or extra Claim Atoms, missing NPC required content, forbidden fact disclosure, and unauthorised NPC commitment/state language.

A model producing bad output that is rejected is a model/retry quality issue. A bad output that is accepted, displayed, or allowed to mutate reality is a Hard Safety Gate breach.

### 4.4 Hard Safety Gates

03 adds no new hard-gate taxonomy. The Frozen gates remain categorical correctness requirements, including:

- unauthorised canonical state mutation = 0;
- invalid canonical ID accepted = 0;
- unauthorised NPC fact disclosure = 0;
- LLM-generated branch/state delta accepted = 0;
- unauthorised NPC action/commitment expressed = 0;
- response-plan-invalid NPC output displayed = 0;
- semantically unresolved headline entering publication resolution = 0;
- AI/system failure creating irreversible gameplay consequence = 0.

### 4.5 Quality measurements

Continue the Frozen metrics where applicable:

- Act Accuracy;
- Target Exact Match;
- Value Exact Match;
- Polarity Accuracy;
- Tactic Precision / Recall;
- Evidence Reference Accuracy;
- Ambiguity Detection;
- Claim Atom Exact Match;
- Claim Omission Rate;
- Commitment Mode Accuracy;
- Source Attribution Accuracy;
- Response Mode Compliance;
- Required Proposition Coverage.

Optional human notes such as surface naturalness/voice fit may be recorded, but they do not override safety/correctness.

No numerical acceptance threshold is confirmed before the first measured baseline.

### 4.6 Retry / fallback measurement

For every applicable case, record both first-pass and final post-policy outcome.

- Dialogue: retry once after model/system failure, then semantically faithful deterministic/template fallback where applicable.
- NPC surface: gate failure → retry once → revalidate → semantically faithful deterministic/template fallback.
- Headline: parser failure → retry once; retry exhaustion preserves the draft and blocks publication resolution; no fabricated Claim Set.

The baseline must record whether retry/fallback was used and whether the final result preserved the deterministic semantic decision.

### 4.7 Latency / cost logging

Minimum per-run record:

- model and model version;
- prompt / schema / baseline-manifest version;
- number of model calls;
- input tokens;
- output tokens;
- model-call latency;
- end-to-end latency including validation/retry;
- retry used?;
- fallback used?;
- estimated model cost.

If Dify is tested later, record orchestration overhead separately from model-call latency.

### 4.8 Prototype blockers

The next prototype must pause and fix/escalate if any of the following occur:

1. a Frozen Hard Safety Gate is actually breached;
2. validators cannot reliably reject invalid IDs/enums/incomplete Claim Sets or response-plan violations;
3. a P0 generator requires hidden canon or gameplay authority to function;
4. retry/fallback changes the deterministic decision instead of preserving it;
5. a core P0 path only becomes viable by changing Frozen semantic status, Dialogue/Claim schema, Response Plan authority, hard gates, or P0 scope;
6. real-model latency/cost makes the interaction non-testable and cannot be reduced through a simple model/orchestration experiment.

Item 5 returns to Contract Master review before any change is confirmed.

**03 result for B:** Accepted and recorded as DEC-021.

## 5. Dependencies and parallelisation

A and B share the Frozen VI01/VI02 baseline but do not depend on each other's internal implementation.

Therefore the first technical prototype may run two parallel tracks:

```text
Track A — deterministic Consequence Event stub
Track B — P0 AI baseline harness + validators
```

They should be integrated only after each is testable independently.

No specialist 03A/03B threads are required. The scopes are small enough for the Master gate and splitting them would add documentation overhead without resolving a demonstrated risk.

## 6. Prototype entry criteria

03 concludes that the project is ready to stop abstract pre-production architecture and enter a narrow technical prototype because:

1. all four global variables now have a minimal deterministic consequence entry boundary;
2. the first real-model baseline protocol directly reuses existing fixtures;
3. no shared Contract semantic change is required;
4. P0 scope did not expand;
5. model failure, validator failure, retry/fallback, safety, latency, and cost measurement are specified;
6. the first technical implementation tasks are explicit.

## 7. Explicitly deferred

03 does not define or authorise:

- final story canon, final NPC/faction roster, or complete world bible;
- production catalogue serialization/authoring tooling;
- production Evidence–Claim persistence/authenticity/tooling;
- final NPC relationship system, richer epistemic model, or P1 memory;
- NPC-originated richer negotiation;
- generic rhetorical/bias/sentiment/misinformation scoring;
- final global-variable ranges, numerical balance, decay, cross-variable formulas, or ending thresholds;
- backend/API architecture unless prototype evidence creates a need;
- Unity architecture or Unity project creation;
- P1/P2 AI features.

## 8. Recommended first technical work

After 03 is integrated into `main`:

1. create a technical-prototype branch;
2. convert the existing fixture cases into a small machine-readable/versioned baseline manifest without changing expected semantics;
3. implement deterministic Dialogue/Headline contract validators and a minimal NPC Output Validation Gate;
4. implement retry/fallback execution and baseline logging;
5. implement a thin deterministic Consequence Event stub exercising the four variables using Experimental placeholder effects;
6. run the first direct real-model baseline;
7. only then test a minimal Dify reproduction to measure orchestration feasibility/overhead if authorised.

Do not create a Unity project for this first technical step.

## 9. Contract impact and final status

- AI authority boundary change: **No**
- P0 scope change: **No**
- Dialogue schema/status change: **No**
- Claim Atom schema change: **No**
- Response Plan authority change: **No**
- Hard Safety Gate change: **No**
- 01 Master review required: **No**
- Specialist threads required: **No**

**Pre-Prototype Gate 03 — COMPLETE**

The branch is ready for integration review. Once integrated into `main`, the project may enter the first technical prototype without additional abstract architecture work.
