# Current State

## Current phase

Pre-production — Validation Increment 02 active.

Validation Increment 01 is complete and the AI Interaction Contract v0.1 remains Frozen. Validation Increment 02A has been accepted by the 02 Master. 02B Evidence–Claim deterministic rules and 02C NPC state / character-card schema are authorised to proceed in parallel on the shared 02A fixture.

No Dify runtime, Unity implementation, backend runtime, or production prompt work is authorised by this state.

## Completed

- Repository bootstrap and baseline documentation completed and integrated into `main`.
- Confirmed product direction and architecture invariants recorded.
- Validation Increment 01 completed; AI Interaction Contract v0.1 frozen.
- 01A Dialogue & Grounded NPC Response validation and targeted regression completed (`659be28db16bea586136ac00a053f1f01452df96`).
- 01B Headline Analysis validation and targeted regression completed (`477086429c6beee7fae4da439383708803cf16f4`).
- Validation Increment 01 integrated into `main` at `28a6a9650fca8d6ad8ade992794d5d2f140e4b6f`.
- Validation Increment 02 started on `design/validation-increment-02`.
- 02A Semantic Target Catalogue & Vertical-Slice Fixture Validation completed and accepted by 02 Master.
- 02A reproducible evidence recorded in `tests/02A_SEMANTIC_TARGET_CATALOGUE_FIXTURE.md`.
- DEC-017 confirms the VI02 catalogue architecture: global authored semantic registry → deterministic runtime projection → parser-specific Runtime Catalogue Views.

## In progress

### 02B — Evidence–Claim Deterministic Rules Validation

Authorised to use the shared 02A fixture to validate:

- attribution support;
- underlying-proposition support;
- canonical reality separation;
- deterministic Evidence–Claim relationships;
- publication-time evidence/knowledge snapshots;
- non-retroactive publication responsibility.

02B must not define Reputation, Public Opinion, Threat Level, or Money consequences.

### 02C — NPC State & Character-Card Schema Validation

Authorised to use the shared 02A fixture to validate:

- static authored NPC card data;
- dynamic NPC state;
- NPC knowledge boundaries;
- current interaction state;
- deterministic NPC rule-resolution inputs;
- Response Plan inputs;
- minimal / least-knowledge generator context.

02C must not turn the temporary fixture NPCs into final canon.

## Frozen contract direction

### Dialogue

The Frozen semantic interpretation contains only gameplay-relevant information:

- semantic status;
- resolution reason where applicable;
- communicative act;
- authored target;
- authored value where required;
- polarity where required;
- an order-insensitive unique set of all gameplay-relevant tactics;
- explicit canonical evidence references.

The LLM does not determine success, truth, deception, state changes, narrative branches, evidence validity, or NPC reactions.

### Grounded NPC response

NPC response generation occurs only after deterministic rule resolution:

`Validated Semantic Action → Deterministic NPC Rule Resolution → Response Plan → LLM Surface Candidate → NPC Output Validation Gate → Display`.

Canonical NPC decisions, clue release, deception, relationship changes, and state changes remain deterministic.

### Headline analysis

Player-written headlines are represented through authored Claim Atoms. Attribution support, underlying-proposition support, canonical reality, and publication-time responsibility remain separate deterministic concepts.

## Validation Increment 02 accepted baseline

02A established a small Experimental / Validation-only / Non-canonical shared fixture around `EVENT_RAILYARD_CLASH`.

Shared proposition IDs:

- `PROP_FIRE_FIRST`;
- `PROP_FUNDED_OPERATION`.

Temporary evidence/source IDs:

- `EV_AUDIO_A`;
- `EV_VIDEO_A`;
- `EV_LEDGER_A`;
- `SRC_WITNESS_A`.

Temporary NPC IDs:

- `NPC_WITNESS_A`;
- `NPC_CLERK_A`.

Temporary dialogue-only meanings:

- `REQ_HAND_OVER_LEDGER`;
- `DEAL_LEDGER_FOR_500`;
- `DEAL_LEDGER_FOR_300`;
- `PENDING_LEDGER_500`.

The story content above is not canonical. It exists only to keep 02B and 02C on one shared authored reality.

### Catalogue architecture

```text
Global Authored Semantic Registry
        ↓
Deterministic Runtime Projection
        ↓
Parser-specific Runtime Catalogue Views
```

Identical propositions reuse one globally unique authored ID across relevant systems. Dialogue-only meanings are filtered out of the Headline view. Evidence, sources, and Pending Interactions remain separate deterministic registries/context.

Only currently exposed meanings are supplied to AI parsers. An authored-but-unavailable or nonexistent ID returned by a model is rejected deterministically and never enters gameplay.

## Safety direction

Frozen hard safety gates remain unchanged, including:

- Unauthorized canonical state mutation = 0
- Invalid canonical ID accepted = 0
- Unauthorized NPC fact disclosure = 0
- Unauthorized NPC action / commitment expressed = 0
- Response-plan-invalid NPC output displayed = 0
- LLM-generated state or branch decisions accepted = 0
- Semantically unresolved headline entering publication resolution = 0
- AI/system failure creating irreversible gameplay consequence = 0

## Next

1. Run 02B and 02C as separate specialist threads using the 02A fixture.
2. Return both handbacks to `02｜Post-Contract Planning — Validation Increment 02` for Master integration.
3. If either specialist requires changing shared semantic schema, semantic status, Dialogue Act taxonomy, Claim Atom schema, Response Plan authority semantics, AI authority boundary, P0 scope, shared cross-system evidence assumptions, or hard safety gates, stop specialist-level confirmation and return to 02 Master; a required Frozen Contract change must then go to 01 Master for narrowly scoped review.
4. Do not begin four-global-variable formulas, Dify/model baseline work, backend/runtime architecture, or Unity implementation until the appropriate later checkpoint is authorised.

## Blocked / unresolved

- Detailed 20–30 minute vertical-slice story canon remains undefined.
- Final NPC roster and faction/world canon remain undefined.
- Final Semantic Target Catalogue content remains undefined; only the VI02 architecture/fixture is validated.
- Final Evidence–Claim Relationship rules remain unresolved pending 02B.
- Publication snapshot persistence details remain unresolved pending 02B.
- Final NPC state / knowledge / character-card schema remains unresolved pending 02C.
- Whether Response Plan proposition data directly reuses semantic proposition IDs or a separate authored response-content registry remains unresolved.
- NPC-originated authored-offer lifecycle remains unresolved.
- Exact rules and thresholds for Reputation, Public Opinion, Threat Level, and Money remain undefined.
- AI model baseline performance and acceptance thresholds remain undefined.
- Backend/API architecture remains undecided.
- Dify implementation/integration remains unvalidated.
- Unity remains unimplemented.
- Generic rhetorical framing mechanics remain deferred unless validation demonstrates gameplay value.

## Validation Increment 02 success condition

VI02 is not complete yet. It should complete only when:

1. the shared authored fixture supports the three P0 interaction boundaries without AI-created gameplay meaning;
2. deterministic Evidence–Claim evaluation is sufficiently specified and pressure-tested;
3. deterministic NPC state/card boundaries are sufficiently specified and pressure-tested;
4. any cross-contract issue is either resolved without changing the Frozen Contract or explicitly returned to 01 Master;
5. the resulting design is stable enough to become the basis for a later real-model/Dify feasibility baseline without expanding game scope.

## Active repository branches

Current stable validated branch:

`main`

Current active working branch for Validation Increment 02:

`design/validation-increment-02`

`main` remains the stable VI01 baseline until VI02 is completed and deliberately integrated.
