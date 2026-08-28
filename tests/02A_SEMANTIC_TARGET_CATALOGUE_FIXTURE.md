# 02A Semantic Target Catalogue & Vertical-Slice Fixture Validation

**Validation Increment:** 02  
**Specialist:** 02A  
**Status:** Accepted by 02 Master  
**Fixture status:** Experimental / Validation-only / Non-canonical  
**Contract baseline:** `docs/08_AI_INTERACTION_CONTRACT.md` — Frozen v0.1

## 1. Purpose

This fixture validates whether one small authored reality can instantiate all three P0 AI interaction contracts without delegating consequential gameplay meaning to the LLM:

1. Dialogue Semantic Parser;
2. Grounded NPC Response Contract;
3. Headline Claim Analyzer.

The governing boundary remains:

> AI controls language. Deterministic game systems control reality.

No Dify, Unity, backend, production prompt, final world canon, final NPC roster, or final gameplay-variable formulas are defined here.

## 2. Temporary validation scenario

Event:

- `EVENT_RAILYARD_CLASH`

Temporary NPCs:

- `NPC_WITNESS_A`
- `NPC_CLERK_A`

Shared propositions:

- `PROP_FIRE_FIRST`
  - allowed values: `SECURITY_FORCES`, `MILITIA`
- `PROP_FUNDED_OPERATION`
  - allowed values: `COMPANY_A`, `MAYOR_OFFICE`

Temporary canonical oracle used only for deterministic fixture testing:

- `PROP_FIRE_FIRST = MILITIA`
- `PROP_FUNDED_OPERATION = COMPANY_A`

Authored statement by `NPC_WITNESS_A`:

- `PROP_FIRE_FIRST = SECURITY_FORCES`

The NPC generator does not determine whether that statement is true, false, deceptive, or mistaken.

## 3. Evidence and source registry

Temporary evidence:

- `EV_AUDIO_A` — records Witness A saying security forces fired first.
- `EV_VIDEO_A` — depicts militia firing first.
- `EV_LEDGER_A` — contains a Company A payment record.

Temporary source:

- `SRC_WITNESS_A`
  - actor reference: `NPC_WITNESS_A`

Evidence and sources are separate deterministic registries/context. Their IDs may be supplied to AI systems only when player-visible and relevant to the current interaction.

## 4. Request, deal, and pending-interaction registry

Temporary request target:

- `REQ_HAND_OVER_LEDGER`

Temporary authored bilateral deal targets:

- `DEAL_LEDGER_FOR_500` — currently exposed.
- `DEAL_LEDGER_FOR_300` — authored but currently unavailable.

Temporary pending interaction:

- `PENDING_LEDGER_500`
  - references `DEAL_LEDGER_FOR_500`;
  - valid consequential player responses: `ACCEPT`, `REFUSE`.

No free-form request or deal terms may be created by the LLM.

## 5. Accepted catalogue architecture

The accepted VI02 baseline is:

```text
Global Authored Semantic Registry
        ↓
Deterministic Runtime Projection
        ↓
Parser-specific Catalogue Views
```

Identical authored propositions reuse one globally unique proposition ID across relevant systems. For example, `PROP_FIRE_FIRST` may be used by Dialogue, Headline Claim Atoms, deterministic NPC response content, and later Evidence–Claim rules.

Dialogue-only meanings such as `REQ_HAND_OVER_LEDGER` and `DEAL_LEDGER_FOR_500` are filtered out of the Headline Catalogue View.

This architecture does not add a new field to the Frozen semantic-output schemas.

### Minimum target metadata required by this fixture

- `target_id`;
- authored semantic description;
- target kind;
- parser usage scope;
- allowed acts;
- allowed value IDs;
- conditional value requirement;
- conditional polarity requirement;
- tactic compatibility where applicable;
- current exposure state.

REQUEST and DEAL targets may additionally reference deterministic authored request/deal data.

Evidence, sources, and Pending Interactions remain separate runtime registries/context rather than target semantic fields.

## 6. Runtime availability classes

### Currently available

Authored and present in the current Runtime Catalogue View.

### Authored but unavailable

Exists in the global authored registry but is omitted from the current Runtime Catalogue View.

### Completely out-of-catalogue

No authored registry entry exists.

No new semantic status is introduced.

Player language attempting a meaning that is not currently supported may resolve as `UNSUPPORTED / OUT_OF_CATALOGUE` where appropriate.

If a model illegally returns an authored-but-unavailable ID or a nonexistent ID, deterministic validation rejects the candidate as an AI/System Failure rather than accepting it as gameplay meaning.

## 7. Representative dialogue cases

| Case | Player language / condition | Expected result |
| --- | --- | --- |
| D01 | “Who fired first?” | `QUESTION → PROP_FIRE_FIRST` |
| D02 | “Security forces fired first.” | `ASSERTION → PROP_FIRE_FIRST → SECURITY_FORCES → AFFIRM` |
| D03 | “Company A funded the operation.” | `ASSERTION → PROP_FUNDED_OPERATION → COMPANY_A → AFFIRM` |
| D04 | “Give me the ledger.” | `REQUEST → REQ_HAND_OVER_LEDGER` |
| D05 | “I’ll pay 500 for the ledger.” | `OFFER → DEAL_LEDGER_FOR_500` |
| D06 | “I’ll pay 300 for the ledger.” while the target is authored but unavailable | `UNSUPPORTED / OUT_OF_CATALOGUE` |
| D07 | Free-form car-for-ledger exchange with no authored deal target | `UNSUPPORTED / OUT_OF_CATALOGUE` |
| D08 | One request supported by a threat and explicit visible evidence reference | One `REQUEST`, plus authored `THREAT` tactic and evidence reference; not a second consequential action |
| D09 | “Give me the ledger and tell me who funded the operation.” | `UNSUPPORTED / MULTIPLE_ACTIONS` |
| D10 | Model returns a nonexistent or currently unavailable target ID | Deterministic validator rejects as AI/System Failure |
| D11 | ACCEPT / REFUSE with `PENDING_LEDGER_500` as the unique deterministic Pending Interaction | Binds to the pending interaction; LLM does not select an unrelated deal |

The Frozen single-consequential-action rule and REQUEST / authored bilateral OFFER distinction remain valid.

## 8. Representative NPC Response Plan cases

The fixture supports:

```text
Validated Semantic Action
→ Deterministic NPC Decision
→ Deterministic Response Plan
→ Surface-generation boundary
```

Representative plans must demonstrate that:

- required propositions are authored deterministically;
- safe permitted context may be supplied for wording;
- forbidden propositions prevent hidden evidence/world leakage;
- refusal remains a deterministic NPC decision rather than a generator choice;
- acceptance of an authored deal may be surfaced without allowing the generator to execute the deal;
- hidden canonical truth can be withheld from generation context where unnecessary.

No NPC gameplay decision, clue unlock, trade execution, state delta, or deception decision is delegated to the LLM.

## 9. Representative headline cases

The Headline Catalogue View contains proposition targets, not dialogue-only REQUEST/DEAL meanings.

The fixture supports validation of:

- direct asserted Claim Atoms;
- source-attributed Claim Atoms using `SRC_WITNESS_A`;
- attributed speculative Claim Atoms;
- multi-claim headlines using `PROP_FIRE_FIRST` and `PROP_FUNDED_OPERATION`;
- consequential presuppositions;
- `RESOLVED + claims=[]` for a headline with no consequential proposition and no unresolved consequential content;
- atomic failure when any consequential claim is out-of-catalogue.

Detailed deterministic Evidence–Claim sufficiency evaluation is deferred to 02B.

## 10. Deterministic catalogue validation rules

Where applicable, the validator must check:

- target ID exists in the current Runtime Catalogue View;
- target is legal for the current parser scope;
- act is allowed for the target;
- required value exists;
- value belongs to the target’s authored domain;
- polarity satisfies conditional rules;
- tactic set is authored, unique, complete, and compatible;
- evidence references are player-visible;
- source references are player-visible;
- REQUEST refers to an exposed request target;
- OFFER refers to an exposed authored bilateral deal;
- ACCEPT / REFUSE has one valid Pending Interaction;
- headline claims use only headline-eligible proposition targets;
- headline atomic resolution is preserved;
- invalid or unavailable IDs never enter deterministic gameplay;
- current NPC/event/scene IDs remain deterministic context rather than LLM-selected output.

## 11. Edge cases retained for later work

### NPC-originated offers

The current fixture can instantiate a Pending Interaction deterministically without requiring the LLM to originate a deal.

If future design requires the Grounded NPC Response Contract to represent an NPC dynamically initiating a new authored deal and this cannot be represented by the existing Response Plan semantics, the issue must return for shared Contract review before any Frozen authority semantics are changed.

### Unknown / anonymous sources

Unknown-source attribution must not be silently discarded. If anonymous sources become a gameplay requirement, they should receive authored source IDs rather than free-form canonical identities.

No Claim Atom schema change is required by this fixture.

## 12. 02A outcome

The following Frozen Contract assumptions survive concrete instantiation:

- free vocabulary maps to bounded authored meanings;
- Dialogue and Headline may share authored proposition IDs;
- request/deal semantics remain dialogue-only;
- invalid canonical IDs are rejected deterministically;
- target availability requires no new semantic status;
- REQUEST / OFFER distinction remains coherent;
- single-action dialogue remains coherent;
- tactics remain supporting semantics rather than additional actions;
- Pending Interaction remains deterministic;
- NPC Response Plans remain deterministic;
- Headline atomic resolution remains coherent;
- evidence/source reference grants the LLM no evidence authority.

No consequential gameplay meaning had to be invented by the LLM.

**02A specialist result:** `READY FOR 02 MASTER REVIEW`  
**02 Master result:** `ACCEPTED — proceed to 02B + 02C`  
**01 Master review required:** No  
**Frozen Contract change required:** No

## 13. Still unresolved

- production catalogue serialization/file format;
- final exposure/availability rules;
- final Evidence–Claim deterministic relationship rules;
- publication snapshot persistence;
- final NPC state / knowledge / character-card schema;
- whether Response Plan proposition data directly reuses semantic proposition IDs or uses a separate authored response-content registry;
- NPC-originated authored-offer lifecycle;
- production catalogue authoring tools.

These remain unresolved and must not be treated as confirmed by this fixture.
