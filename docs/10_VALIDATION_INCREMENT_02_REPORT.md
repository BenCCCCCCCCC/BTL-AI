# Validation Increment 02 Report

**Project:** Between the Lines: AI Remake (BTL-AI)  
**Status:** Complete  
**Date:** 2026-08-29  
**Contract baseline:** `docs/08_AI_INTERACTION_CONTRACT.md` — Frozen v0.1

## 1. Purpose

Validation Increment 02 tested whether the Frozen AI Interaction Contract v0.1 could be instantiated by a small authored reality and supported by deterministic game-data/rule structures without giving the LLM authority over gameplay reality.

The governing principle remained:

> **AI controls language. Deterministic game systems control reality.**

No Dify runtime workflow, Unity implementation, backend runtime, production prompt, final story/world canon, final NPC roster, or four-global-variable formula was implemented.

## 2. Specialist scopes

### 02A — Semantic Target Catalogue & Vertical-Slice Fixture Validation

02A established one shared Experimental / Validation-only / Non-canonical authored fixture and validated:

- global authored semantic registry;
- deterministic runtime projection;
- parser-specific Runtime Catalogue Views;
- shared proposition IDs across relevant P0 systems;
- dialogue-only REQUEST/DEAL meanings;
- evidence/source/Pending Interaction separation;
- current exposure and invalid-ID rejection;
- Dialogue single-action and REQUEST/OFFER rules;
- Headline atomic resolution;
- deterministic NPC Response Plan authority.

Evidence:

- `tests/02A_SEMANTIC_TARGET_CATALOGUE_FIXTURE.md`

Master result:

**Accepted.** Recorded in DEC-017.

### 02B — Evidence–Claim Deterministic Rules Validation

02B validated that headline publication responsibility can be evaluated through:

```text
Validated Claim Atom
+
Immutable Publication-Time Snapshot
+
Authored Evidence–Claim Relationships
+
Deterministic Commitment-Mode Rules
→
Auditable Publication Evaluation
```

Key validated separations:

- attribution support ≠ underlying-proposition support;
- evidence support ≠ canonical reality;
- evidence existing in the world ≠ evidence available to the player;
- publication-time responsibility ≠ later evidence/state;
- semantic validity ≠ evidence sufficiency.

The LLM does not judge evidence quality, source reliability, truth, or publication responsibility.

Evidence:

- `tests/02B_EVIDENCE_CLAIM_RULES_FIXTURE.md`

Master result:

**Accepted.** Recorded in DEC-018.

The specific railyard Evidence–Claim rows and sufficiency examples remain validation-only and do not become final journalism policy/content.

### 02C — NPC State & Character-Card Schema Validation

02C validated a seven-layer deterministic NPC grounding architecture:

1. Static Character Card;
2. Authored Knowledge Boundary;
3. Authoritative Dynamic NPC State;
4. Current Interaction State;
5. Canonical World Context;
6. Deterministic Response Plan;
7. Minimal Generator-only Language Context.

Key validated separation:

```text
NPC knows X
≠
NPC may reveal X
≠
NPC must say X now
```

The generator receives least-knowledge context and remains responsible only for surface language. Hidden canonical truth, locked clues, raw relationship values, state deltas, branch IDs, and unrelated evidence are excluded where unnecessary.

All Frozen NPC response modes remain sufficient for the validated fixture. `DECEIVE` remains unnecessary because deception is a deterministic authored/narrative content decision.

Evidence:

- `tests/02C_NPC_STATE_CHARACTER_CARD_SCHEMA_FIXTURE.md`

Master result:

**Accepted.** Recorded in DEC-019.

Shared `PROP_*` IDs may be reused for world propositions in Response Plans. Exact internal representation for non-world response obligations remains deferred serialization/schema detail rather than a Contract change.

## 3. Shared temporary fixture

Validation Increment 02 reused one temporary authored reality:

- `EVENT_RAILYARD_CLASH`
- `NPC_WITNESS_A`
- `NPC_CLERK_A`
- `PROP_FIRE_FIRST`
- `PROP_FUNDED_OPERATION`
- `EV_AUDIO_A`
- `EV_VIDEO_A`
- `EV_LEDGER_A`
- `SRC_WITNESS_A`
- `REQ_HAND_OVER_LEDGER`
- `DEAL_LEDGER_FOR_500`
- `DEAL_LEDGER_FOR_300`
- `PENDING_LEDGER_500`

All of the above remain **Experimental / Validation-only / Non-canonical**. Acceptance of the architecture does not promote these names, events, NPCs, evidence items, deals, or story facts into final vertical-slice canon.

## 4. Contract impact

Validation Increment 02 requires no change to:

- shared semantic status taxonomy;
- Dialogue Act taxonomy;
- Dialogue single-consequential-action rule;
- REQUEST / authored bilateral OFFER distinction;
- Claim Atom schema;
- commitment-mode semantics;
- source-attribution semantics;
- NPC response-mode taxonomy;
- deception authority;
- generator output authority;
- AI authority boundary;
- P0 scope;
- Frozen hard safety gates.

Therefore:

**Frozen AI Interaction Contract v0.1 remains unchanged.**

**01 Master review required: No.**

## 5. Deferred / unresolved work

The following remain unresolved and are not silently confirmed by VI02:

- final 20–30 minute vertical-slice story canon;
- final NPC/faction/world roster;
- production catalogue serialization, exposure rules, and authoring tooling;
- production Evidence–Claim serialization/persistence/tooling;
- production evidence authenticity/verification model if needed;
- attributed-paraphrase commitment weakening policy;
- final relationship dimensions/formulas;
- richer NPC epistemic distinctions if needed;
- exact internal serialization for non-world Response Plan obligations;
- NPC-originated authored-offer lifecycle;
- Reputation / Public Opinion / Threat Level / Money deterministic formulas and thresholds;
- real-model AI baseline and acceptance thresholds;
- Dify feasibility/integration;
- backend/API architecture;
- Unity implementation architecture;
- production Output Validation Gate implementation;
- P1 long-term NPC memory;
- generic rhetorical framing unless future validation demonstrates gameplay need.

NPC-originated authored offers remain specifically deferred. If a future vertical-slice requirement cannot represent them without changing Frozen Response Plan authority semantics or adding a response mode, the issue must return through the current Master process to Contract review before implementation.

## 6. Success-condition assessment

Validation Increment 02 succeeds because:

1. one authored fixture supports Dialogue, Headline, and NPC P0 boundaries without AI-created gameplay meaning;
2. deterministic Evidence–Claim evaluation is specified and pressure-tested;
3. deterministic NPC state/card/context boundaries are specified and pressure-tested;
4. no validated core result requires changing the Frozen Contract;
5. the resulting data/rule boundary is stable enough to support a later real-model/Dify feasibility baseline without expanding game scope.

## 7. Final status

**Validation Increment 02 — COMPLETE**

The Frozen AI Interaction Contract v0.1 remains the authoritative AI-language boundary.

The next project step should be separately scoped and authorised. VI02 itself does not authorise Dify runtime work, Unity implementation, backend implementation, or arbitrary global-variable formulas.
