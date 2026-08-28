# Handoff

## Project identity

**Between the Lines: AI Remake (BTL-AI)** is a pre-production, PC-first, 2D, narrative/interface-driven journalism game targeting a polished **20–30 minute AI-assisted vertical slice**.

Portfolio goals:

1. demonstrate professional Game Design / Game System Design ability;
2. demonstrate professional AI Product / AI Orchestration ability.

## Current milestone

**Validation Increment 02 — Authored Semantic & Deterministic Fixture Validation**

Status:

**COMPLETE — integrated into `main`.**

`main` is now the current stable validated baseline for completed VI01 + VI02 work.

The **AI Interaction Contract v0.1 remains Frozen and unchanged**.

No Dify runtime workflow, Unity implementation, backend runtime, production prompt, or final four-global-variable implementation is authorised by this milestone.

## Core architecture invariant

> **AI controls language. Deterministic game systems control reality.**

LLM output remains non-authoritative. It may interpret or render language, but it cannot create or mutate canonical state, evidence, branch decisions, gameplay-variable deltas, NPC commitments, publication evidence verdicts, or endings.

## Validation Increment 02 result

Detailed report:

- `docs/10_VALIDATION_INCREMENT_02_REPORT.md`

### 02A — Semantic Target Catalogue

Evidence:

- `tests/02A_SEMANTIC_TARGET_CATALOGUE_FIXTURE.md`

Confirmed as DEC-017:

```text
Global Authored Semantic Registry
        ↓
Deterministic Runtime Projection
        ↓
Parser-specific Runtime Catalogue Views
```

Shared world propositions reuse global authored IDs. Dialogue-only REQUEST/DEAL meanings remain dialogue-scoped. Only currently exposed meanings enter parser views. Evidence, sources, and Pending Interactions remain separate deterministic registries/context.

### 02B — Evidence–Claim deterministic rules

Evidence:

- `tests/02B_EVIDENCE_CLAIM_RULES_FIXTURE.md`

Confirmed as DEC-018:

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

Critical separation:

```text
Attribution Support
≠
Underlying Proposition Support
≠
Canonical Reality
```

Later evidence cannot overwrite the original publication-time responsibility result. The LLM does not judge evidence sufficiency, source reliability, or truth.

The railyard relationship rows and sufficiency examples remain validation-only rather than final journalism policy/content.

### 02C — NPC State & Character Card

Evidence:

- `tests/02C_NPC_STATE_CHARACTER_CARD_SCHEMA_FIXTURE.md`

Confirmed as DEC-019:

1. Static Character Card;
2. Authored Knowledge Boundary;
3. Authoritative Dynamic NPC State;
4. Current Interaction State;
5. relevant Canonical World Context;
6. Deterministic Response Plan;
7. minimal Generator-only Language Context.

Critical separation:

```text
NPC knows X
≠
NPC may reveal X
≠
NPC must say X now
```

The generator receives least-knowledge context and surface-language authority only. Hidden canon, locked clues, state deltas, branch IDs, raw relationship values, and unrelated evidence should be withheld where unnecessary.

Shared `PROP_*` IDs may be reused for world propositions in Response Plan content.

Exact internal representation for non-world response obligations remains deferred serialization/schema detail; VI02 does not redefine Frozen `required_propositions[]` semantics.

## Shared validation fixture status

`EVENT_RAILYARD_CLASH` and all temporary NPC/evidence/deal IDs remain:

**Experimental / Validation-only / Non-canonical.**

They are validation evidence, not final vertical-slice story content.

## Contract-impact result

VI02 requires no change to semantic statuses, Dialogue Acts, Dialogue single-action rule, REQUEST/OFFER distinction, Claim Atom schema, commitment/source semantics, NPC response modes, deterministic deception rule, AI authority boundary, P0 scope, or hard safety gates.

Therefore:

**Frozen AI Interaction Contract v0.1 remains unchanged.**

**01 Master review required: No.**

## Important deferred issues

Do not silently treat the following as Confirmed:

- NPC-originated authored-offer lifecycle;
- exact response-layer serialization for non-world Response Plan obligations;
- attributed-paraphrase commitment weakening policy;
- final evidence authenticity/verification rules;
- final NPC relationship formulas or richer epistemic model;
- final story canon/NPC/faction roster;
- final catalogue/evidence authoring formats/tools;
- Reputation / Public Opinion / Threat Level / Money formulas and thresholds;
- real-model acceptance thresholds;
- Dify integration;
- backend/API architecture;
- Unity implementation;
- production Output Validation Gate implementation;
- P1 NPC memory.

If NPC-originated offers or Response Plan serialization later require new response modes or changed authority semantics, return to Contract review before implementation.

## Next project step

Open a **new Master planning thread** for the post-VI02 phase rather than continuing specialist work in this thread.

Recommended planning scope:

- deterministic four-global-variable consequence-rule validation;
- real-model / Dify feasibility baseline using frozen 01/02 fixtures;
- sequencing/parallelisation of those streams;
- success criteria for the next increment;
- backend/runtime architecture only after those needs are evidenced.

Do not enter Unity implementation yet.

## Documentation protocol

The Git repository is the canonical working copy.

At substantial checkpoints:

- detailed reproducible validation evidence → `tests/`;
- Confirmed decisions → `docs/05_DECISION_LOG.md`;
- current phase/progress/blockers → `docs/06_CURRENT_STATE.md`;
- concise cross-thread resume state → `docs/07_HANDOFF.md`;
- completed validation increment → milestone report.

Chat history alone is not the canonical project record. When tooling allows, repository documentation should be synchronised directly rather than requiring manual user edits.

## Local repository and Project Sources sync protocol

GitHub is the canonical working copy, but the user's local repository and ChatGPT Project Sources are separate copies and do **not** update automatically when GitHub is changed through ChatGPT tooling.

After every substantial GitHub checkpoint in which files are created, updated, deleted, merged, or otherwise corrected, the assistant must explicitly report:

1. **GitHub files changed** — exact repository paths that changed;
2. **Local repository sync required: Yes / No** — if Yes, tell the user to switch to the relevant canonical branch in GitHub Desktop, Fetch origin, then Pull origin so the local working copy matches GitHub;
3. **Project Sources refresh required: Yes / No** — if Yes, list the exact Project Sources files that should be replaced or newly added;
4. **Project Sources currently stale: Yes / No** — if GitHub has newer authoritative files than the uploaded Project Sources, state this explicitly until the user confirms refresh;
5. **User manual action required** — only the minimal steps that cannot be performed automatically from ChatGPT.

For milestone completions and major Master integrations, local repository sync and Project Sources refresh should be treated as part of the checkpoint rather than omitted from the handoff.

Do not assume that a GitHub write automatically updates either the user's local files or Project Sources.

## Files next Master thread should read first

1. BTL-AI ChatGPT Project Instructions
2. `docs/01_PROJECT_DEFINITION.md`
3. `docs/05_DECISION_LOG.md`
4. `docs/08_AI_INTERACTION_CONTRACT.md` — Frozen v0.1
5. `docs/06_CURRENT_STATE.md`
6. `docs/07_HANDOFF.md`
7. `docs/09_VALIDATION_INCREMENT_01_REPORT.md`
8. `docs/10_VALIDATION_INCREMENT_02_REPORT.md`
9. `tests/02A_SEMANTIC_TARGET_CATALOGUE_FIXTURE.md`
10. `tests/02B_EVIDENCE_CLAIM_RULES_FIXTURE.md`
11. `tests/02C_NPC_STATE_CHARACTER_CARD_SCHEMA_FIXTURE.md`

## Repository baseline

Current stable validated branch:

`main`

Completed historical VI02 branch:

`design/validation-increment-02`

Future substantial work should begin on a new branch only after the next increment is authorised.
