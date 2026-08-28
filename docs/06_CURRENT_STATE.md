# Current State

## Current phase

Pre-production — **Validation Increment 02 complete and integrated into `main`.**

`main` is the current stable validated project baseline for completed Validation Increment 01 + Validation Increment 02 work.

The **AI Interaction Contract v0.1 remains Frozen and unchanged**.

No Dify runtime, Unity implementation, backend runtime, production prompt, or final global-variable implementation is authorised by this state.

## Completed

- Repository bootstrap and baseline documentation completed.
- Validation Increment 01 completed; AI Interaction Contract v0.1 frozen.
- Validation Increment 02 completed, Master-reviewed, and integrated into `main`.
- 02A Semantic Target Catalogue & Vertical-Slice Fixture Validation completed and accepted.
- 02B Evidence–Claim Deterministic Rules Validation completed and accepted.
- 02C NPC State & Character-Card Schema Validation completed and accepted.
- VI02 integration report recorded in `docs/10_VALIDATION_INCREMENT_02_REPORT.md`.

## Confirmed VI02 architecture

### DEC-017 — Authored semantic catalogue

```text
Global Authored Semantic Registry
        ↓
Deterministic Runtime Projection
        ↓
Parser-specific Runtime Catalogue Views
```

- Shared world propositions reuse globally unique authored `PROP_*` IDs across relevant P0 systems.
- Dialogue-only REQUEST/DEAL meanings remain scoped to dialogue.
- Only currently exposed authored meanings are supplied to AI parsers.
- Evidence, sources, and Pending Interactions remain separate deterministic registries/context.
- Unavailable/nonexistent IDs returned by AI are rejected deterministically.

### DEC-018 — Evidence–Claim publication evaluation

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

Confirmed separations:

- attribution support ≠ underlying-proposition support;
- publication-time support ≠ canonical reality;
- evidence existing in the world ≠ evidence available to the player;
- original publication responsibility ≠ later evidence/state.

The LLM does not judge evidence sufficiency, source reliability, or canonical truth.

### DEC-019 — NPC grounding data boundary

P0 NPC response grounding uses seven separated layers:

1. Static Character Card;
2. Authored Knowledge Boundary;
3. Authoritative Dynamic NPC State;
4. Current Interaction State;
5. relevant Canonical World Context;
6. Deterministic Response Plan;
7. minimal Generator-only Language Context.

Key invariant:

```text
NPC knows X
≠
NPC may reveal X
≠
NPC must say X now
```

The generator receives least-knowledge context and retains surface-language authority only.

## Frozen Contract status

Validation Increment 02 requires **no change** to the Frozen AI Interaction Contract v0.1.

No change is required to semantic status taxonomy, Dialogue Act taxonomy, single-action Dialogue rule, REQUEST/OFFER distinction, Claim Atom schema, commitment/source semantics, NPC response-mode taxonomy, deception authority, generator authority, P0 scope, or hard safety gates.

**01 Master review required:** No.

## Validation evidence

- `tests/01A_DIALOGUE_NPC_VALIDATION_FIXTURE.md`
- `tests/01B_HEADLINE_VALIDATION_FIXTURE.md`
- `tests/02A_SEMANTIC_TARGET_CATALOGUE_FIXTURE.md`
- `tests/02B_EVIDENCE_CLAIM_RULES_FIXTURE.md`
- `tests/02C_NPC_STATE_CHARACTER_CARD_SCHEMA_FIXTURE.md`
- `docs/09_VALIDATION_INCREMENT_01_REPORT.md`
- `docs/10_VALIDATION_INCREMENT_02_REPORT.md`

The `EVENT_RAILYARD_CLASH` fixture and its NPC/evidence/deal content remain **Experimental / Validation-only / Non-canonical**.

## Still unresolved

- final 20–30 minute vertical-slice story canon;
- final NPC/faction/world roster;
- production catalogue serialization/exposure/authoring tooling;
- production Evidence–Claim serialization/persistence/tooling;
- evidence authenticity/verification model if needed;
- attributed-paraphrase commitment weakening policy;
- exact Response Plan serialization for non-world response obligations;
- NPC-originated authored-offer lifecycle;
- final NPC relationship dimensions/formulas;
- richer NPC epistemic distinctions if gameplay later needs them;
- Reputation / Public Opinion / Threat Level / Money deterministic rules and thresholds;
- real-model P0 baseline and acceptance thresholds;
- Dify feasibility/integration;
- backend/API architecture;
- Unity implementation architecture;
- production Output Validation Gate implementation;
- P1 long-term NPC memory;
- generic rhetorical framing unless later validation demonstrates gameplay need.

## Next

The next work must be a separately scoped post-VI02 planning increment rather than silently continuing implementation.

Recommended next planning questions:

1. define the smallest useful deterministic consequence model for Reputation / Public Opinion / Threat Level / Money without inventing arbitrary formulas;
2. define a real-model / Dify feasibility baseline using the stable 01/02 fixtures, without yet making Dify a production dependency;
3. decide whether those two validation streams can run in parallel;
4. defer backend/runtime architecture until deterministic-rule and orchestration needs are evidenced;
5. do not create a Unity project until explicitly authorised.

## Repository baseline

Current stable validated branch:

`main`

Completed historical VI02 branch:

`design/validation-increment-02`

Future substantial work should begin on a new branch only after the next validation/planning increment is authorised.
