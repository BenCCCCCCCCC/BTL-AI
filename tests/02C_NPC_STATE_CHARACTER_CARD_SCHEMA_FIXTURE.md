# 02C NPC State & Character-Card Schema Validation

**Validation Increment:** 02  
**Specialist:** 02C  
**Status:** READY FOR 02 MASTER REVIEW  
**Fixture status:** Experimental / Validation-only / Non-canonical  
**Contract baseline:** `docs/08_AI_INTERACTION_CONTRACT.md` — Frozen v0.1

## 1. Purpose

This fixture validates whether the Frozen Grounded NPC Response Contract can be supported by a minimal deterministic NPC data model without giving the LLM gameplay authority.

Required pipeline:

```text
Authored Character Card
+ Authoritative Dynamic NPC State
+ Current Interaction State
+ Relevant World / Knowledge Boundary
→ Deterministic NPC Rule Resolution
→ Deterministic NPC Response Plan
→ Minimal LLM Generation Context
→ Surface Candidate
→ NPC Output Validation Gate
```

The governing boundary remains:

> AI controls language. Deterministic game systems control reality.

No production LLM is run here. No Unity state classes, Dify workflow, production prompt, final NPC roster, final world bible, final relationship formula, global-variable formula, backend architecture, or P1 memory implementation is defined.

## 2. Shared 02A validation reality

This fixture reuses the accepted 02A temporary reality unchanged.

Event:

- `EVENT_RAILYARD_CLASH`

Temporary NPCs:

- `NPC_WITNESS_A`
- `NPC_CLERK_A`

Shared propositions:

- `PROP_FIRE_FIRST`
  - values: `SECURITY_FORCES`, `MILITIA`
- `PROP_FUNDED_OPERATION`
  - values: `COMPANY_A`, `MAYOR_OFFICE`

Evidence:

- `EV_AUDIO_A`
- `EV_VIDEO_A`
- `EV_LEDGER_A`

Request / deal / pending interaction:

- `REQ_HAND_OVER_LEDGER`
- `DEAL_LEDGER_FOR_500` — currently exposed
- `DEAL_LEDGER_FOR_300` — authored but unavailable
- `PENDING_LEDGER_500`

Temporary canonical oracle remains:

- `PROP_FIRE_FIRST = MILITIA`
- `PROP_FUNDED_OPERATION = COMPANY_A`

Existing authored Witness A statement remains:

- `PROP_FIRE_FIRST = SECURITY_FORCES`

All story and NPC content remains Experimental / Validation-only / Non-canonical.

## 3. Proposed NPC data-layer model

The minimum safe model requires seven distinct layers.

| Layer | Authority | Purpose | Must not become |
| --- | --- | --- | --- |
| 1. Static Character Card | Authored deterministic data | Identity, role, voice, dialogue-relevant background, references to other policy/state definitions | Giant world bible or dynamic state store |
| 2. Authored Knowledge Boundary | Authored deterministic data | Defines what the NPC may be aware of, what is excluded, and baseline knowledge-policy constraints | Canonical truth store or disclosure decision |
| 3. Authoritative Dynamic NPC State | Deterministic runtime state | Relationship/attitude state refs, current knowledge, already-revealed content, disclosure state, narrative flags | Free-text LLM memory or generator-authored state |
| 4. Current Interaction State | Deterministic runtime context | Validated player action, current NPC/event, relevant evidence refs, pending interaction, immediate dialogue context | Full game state or model-selected context |
| 5. Canonical World Context | Authoritative deterministic reality | Relevant canonical proposition/evidence/event facts for rule resolution | Automatic generator context |
| 6. Response Plan | Deterministic decision output | Fixes response mode and authorised semantic content before generation | LLM suggestion or state mutation request |
| 7. Generator-only Language Context | Ephemeral non-authoritative projection | Gives the LLM only the language facts it needs to render the already-decided response | Authoritative state, hidden canon, or gameplay rule input |

The key separation is:

```text
NPC may know X
≠
NPC may reveal X now
≠
NPC is required to say X now
```

`permitted_context` is a wording resource, not clue authority.

## 4. Static Character Card schema

The Character Card should remain small. It should reference knowledge/state policies instead of embedding the world.

Conceptual minimum:

```text
npc_id
identity
role
dialogue_relevant_background_refs[]
voice_profile
hard_language_constraints[]
soft_voice_guidance[]
knowledge_boundary_ref
relationship_rule_profile_ref?  # opaque reference only; no final formula here
```

### Required field intent

- `identity`: enough to keep surface language grounded to the current speaker.
- `role`: only gameplay-relevant social/professional role.
- `dialogue_relevant_background_refs[]`: a small set of authored background facts required for current dialogue behaviour; no biography dump.
- `voice_profile`: register, terseness/verbosity preference, speech texture, allowed language style.
- `hard_language_constraints[]`: constraints that may be validated before display when violation would break authored identity or gameplay safety.
- `soft_voice_guidance[]`: preferences used for quality, not hard authority.
- `knowledge_boundary_ref`: points to a separate knowledge policy object.
- `relationship_rule_profile_ref`: optional authored rule reference; it does not define a numerical relationship system.

### 02C temporary cards

`NPC_WITNESS_A` needs only:

- identity label: Witness A;
- role: witness relevant to `EVENT_RAILYARD_CLASH`;
- concise/cautious voice guidance;
- reference to Witness A knowledge boundary;
- no final biography.

`NPC_CLERK_A` needs only:

- identity label: Clerk A;
- role: clerk relevant to the ledger interaction;
- concise/formal voice guidance;
- reference to Clerk A knowledge boundary;
- no final biography.

## 5. Authored Knowledge Boundary representation

Knowledge boundary is separate from both canonical truth and current disclosure permission.

Conceptual minimum:

```text
knowledge_boundary_id
npc_id
allowed_event_refs[]
allowed_proposition_refs[]
allowed_evidence_awareness_refs[]
excluded_event_refs[]
excluded_proposition_refs[]
excluded_evidence_refs[]
baseline_knowledge_seed_refs[]
disclosure_rule_refs[]
```

Interpretation:

- `allowed_*` means the NPC may legitimately become aware of that authored content under deterministic rules.
- `excluded_*` means the content must not enter the NPC's knowledge/generator path for this character.
- `baseline_knowledge_seed_refs[]` seeds initial authoritative NPC knowledge; it is not the entire world canon.
- `disclosure_rule_refs[]` defines deterministic rule references controlling whether known content is eligible for disclosure.

A knowledge permission does not itself mean the NPC currently knows the content, and neither permission nor current knowledge authorises disclosure.

## 6. Authoritative Dynamic NPC State schema

Conceptual minimum:

```text
npc_id
relationship_state_ref?
attitude_state_ref?
current_knowledge_refs[]
current_evidence_awareness_refs[]
already_revealed_content_refs[]
disclosure_state_by_content_ref{}
narrative_flags[]
interaction_history_flags[]
```

### Findings

- Relationship/attitude needs deterministic representation only as an opaque authored state reference when it affects rule resolution. 02C does not define points, thresholds, formulas, or final bands.
- Cooperation/refusal eligibility should normally be **derived by the deterministic rule engine** from authored rules plus current state, rather than being decided by the generator.
- Clue-disclosure eligibility should likewise be a deterministic derived result from `current_knowledge`, `disclosure_state`, interaction conditions, and authored rules.
- `already_revealed_content_refs[]` is required to prevent the LLM from deciding whether a clue is new, repeated, or newly unlocked.
- Active pending interactions belong primarily to the deterministic Pending Interaction registry / Current Interaction State, not duplicated as free-form NPC memory.
- `narrative_flags[]` may carry authored deterministic conditions such as an active deception/narrative variant. `DECEIVE` is not a response mode.
- No open-ended free-text long-term NPC memory is required for P0.

A useful minimal disclosure state for validation is:

- `LOCKED`
- `ELIGIBLE`
- `REVEALED`

These are validation-only conceptual states, not a final production enum. `ELIGIBLE` still does not mean `REQUIRED_NOW`.

## 7. Current Interaction State representation

Conceptual minimum:

```text
interaction_id
npc_id
event_id
validated_player_semantic_action
explicit_evidence_ref_ids[]
active_pending_interaction_ref?
current_request_or_deal_ref?
player_visible_clarification_context?
minimal_recent_visible_turn_refs[]
```

Rules:

- `npc_id` and `event_id` come from deterministic game/UI context, not the LLM.
- `validated_player_semantic_action` is already past the Dialogue Contract validator.
- evidence refs indicate explicit player references only; they do not prove ownership/relevance/truth.
- `active_pending_interaction_ref` must be the unique deterministic pending interaction used by ACCEPT/REFUSE when relevant.
- recent conversation context is bounded and player-visible; it is not a hidden-state channel.

## 8. Canonical World Context

Canonical World Context is authoritative input to deterministic rule resolution, not a generator knowledge dump.

For this fixture, relevant canonical truth includes:

- `PROP_FIRE_FIRST = MILITIA`
- `PROP_FUNDED_OPERATION = COMPANY_A`

The rule engine may also inspect relevant evidence state and authored event facts. The generator receives only the subset deliberately projected by the Response Plan / generator-context builder.

Character Card and NPC knowledge must not be treated as substitutes for canonical world state.

## 9. Deterministic NPC Rule Resolution inputs

The minimum input set is:

```text
Validated Player Semantic Action
+ Static Character Card refs
+ Authored Knowledge Boundary
+ Authoritative Dynamic NPC State
+ Current Interaction State
+ Relevant Canonical World Context
+ Authored NPC rule table / narrative rules
```

The deterministic rule engine decides:

- whether the NPC answers, partially answers, evades, refuses, clarifies, counterquestions, accepts, or rejects;
- whether a known clue is eligible and whether it is actually authorised for this turn;
- whether an authored deception/narrative variant is active;
- whether a request/deal is accepted or rejected;
- any authoritative state transition outside the LLM surface-generation path.

The LLM does not decide any of these.

## 10. Response Plan representation

Frozen response modes remain unchanged:

- `ANSWER`
- `PARTIAL_ANSWER`
- `EVADE`
- `REFUSE`
- `CLARIFY`
- `COUNTERQUESTION`
- `ACCEPT`
- `REJECT`

Conceptual Response Plan:

```text
response_mode
required_propositions[]
permitted_context[]
forbidden_propositions[]
player_visible_clarification_options[]?
language_constraints
minimal_conversation_context_ref?
```

### Shared proposition ID reuse finding

For gameplay-relevant world propositions, direct reuse of the accepted shared proposition IDs is valid and preferred.

Example:

```text
required proposition:
PROP_FIRE_FIRST = SECURITY_FORCES
```

This avoids creating a duplicate response-only semantic identity for the same world proposition.

However, not every required response obligation is a world proposition. REFUSE, EVADE, CLARIFY, COUNTERQUESTION, ACCEPT, and REJECT may require authored interaction-content clauses such as “refuse this request” or “ask which timeframe”. These should not be forced into the global `PROP_*` world-proposition registry.

02C therefore proposes a **hybrid internal representation** under the existing Frozen `required_propositions[]` concept:

1. shared world-proposition clauses reuse `PROP_*` IDs;
2. non-world interaction obligations use authored response-content clause IDs scoped to the Response Plan layer.

This is an implementation/schema representation recommendation, not a change to Response Plan authority. If 02 Master considers this a semantic broadening of the Frozen `required_propositions[]` field rather than deferred serialization detail, it must be escalated to 01 Master before confirmation.

## 11. Minimal LLM Generation Context

The LLM generator should receive an ephemeral projection, not the full Response Plan/state stack.

Minimum useful context:

```text
speaker identity label
role if needed for wording
voice / language constraints
response_mode
required authorised utterance content
safe permitted wording context only
minimal player-visible recent conversation needed for fluency
```

It should normally NOT receive:

- hidden canonical truth;
- full NPC knowledge state;
- locked clues;
- unneeded evidence content;
- relationship points/thresholds;
- cooperation/disclosure eligibility rules;
- state deltas;
- branch IDs;
- global variables;
- full world bible;
- full conversation history.

### Forbidden propositions and least knowledge

The deterministic Response Plan / Output Validation Gate may retain full forbidden proposition data. The generator does not always need the semantic content of hidden forbidden facts.

If telling the generator “do not say MILITIA fired first” would itself reveal the hidden truth to the model, the generator context should instead receive a safer abstract restriction such as “do not identify any alternative actor beyond the authorised statement”. The full hidden forbidden proposition remains available to the deterministic pre-display gate.

## 12. Least-knowledge validation

### LK01 — Deterministic deceptive statement

Canonical truth:

- `PROP_FIRE_FIRST = MILITIA`

Deterministic authored narrative decision:

- Witness A must state `PROP_FIRE_FIRST = SECURITY_FORCES` on this turn.

Rule engine sees both canonical truth and the authored narrative flag.

Generator receives:

- speaker/voice constraints;
- `response_mode=ANSWER`;
- required utterance `PROP_FIRE_FIRST = SECURITY_FORCES`;
- no `PROP_FIRE_FIRST = MILITIA` truth;
- no `EV_VIDEO_A` content revealing the truth.

Valid surface candidate:

> “Security forces fired first.”

The gate rejects:

- any alternative invented actor;
- hidden `MILITIA` truth leakage;
- extra unauthorised evidence/world facts.

**Finding:** least-knowledge is sufficient. The generator does not need hidden canonical truth to render deterministic deception.

### LK02 — Locked known clue

If an NPC currently knows a gameplay-relevant proposition but its disclosure state is `LOCKED`, the proposition remains outside generator context. `permitted_context` cannot expose it as an optional clue.

### LK03 — Relationship-derived wording

If deterministic state says the NPC is guarded, the generator may receive only a surface directive such as “guarded, terse tone”. It does not need the raw relationship state value or the rule that produced it.

## 13. Representative Response Plan cases

The response-only clause labels below exist only to validate Response Plan construction. They are not new global semantic targets or final production IDs.

| Case | Deterministic inputs | Response Plan | Generator authority check |
| --- | --- | --- | --- |
| RP01 `ANSWER` | Witness A; `QUESTION → PROP_FIRE_FIRST`; authored deceptive/narrative flag active | `ANSWER`; required shared proposition `PROP_FIRE_FIRST=SECURITY_FORCES`; hidden canonical alternative forbidden at gate | Generator only verbalises the authorised statement; cannot choose truth/deception |
| RP02 `PARTIAL_ANSWER` | Clerk A; question about `PROP_FUNDED_OPERATION`; NPC knows relevant content but value disclosure remains locked | `PARTIAL_ANSWER`; required response-content clause `RC_ACKNOWLEDGE_TOPIC_WITHHOLD_VALUE`; forbid disclosing `COMPANY_A` or `MAYOR_OFFICE` | Generator cannot upgrade a partial answer into a full clue |
| RP03 `EVADE` | Same topic; authored deterministic rule selects evasion | `EVADE`; required `RC_EVADE_FUNDER_TOPIC`; forbid both funder values | Generator cannot answer anyway |
| RP04 `REFUSE` | `REQUEST → REQ_HAND_OVER_LEDGER`; deterministic compliance rule resolves refusal | `REFUSE`; required `RC_REFUSE_LEDGER_REQUEST`; forbid handover promise/commitment | Generator cannot comply or create state |
| RP05 `CLARIFY` | Resolved `QUESTION → PROP_FIRE_FIRST`; deterministic NPC rule requires timeframe clarification | `CLARIFY`; required `RC_ASK_TIMEFRAME`; forbid answering either actor value | Resolved-action CLARIFY remains separate from parser semantic clarification |
| RP06 `COUNTERQUESTION` | Validated question; deterministic rule requires the NPC to ask for the player's basis/source | `COUNTERQUESTION`; required `RC_ASK_PLAYER_BASIS`; no new clue authorised | Generator cannot invent a different interrogation goal |
| RP07 `ACCEPT` | Player `OFFER → DEAL_LEDGER_FOR_500`; deterministic deal rule accepts | `ACCEPT`; required `RC_ACCEPT_DEAL_LEDGER_FOR_500`; no state delta in generator context | Generator may express acceptance but cannot deduct money, add ledger, or create evidence |
| RP08 `REJECT` | Player `OFFER → DEAL_LEDGER_FOR_500`; deterministic deal rule rejects | `REJECT`; required `RC_REJECT_DEAL_LEDGER_FOR_500`; `DEAL_LEDGER_FOR_300` unavailable and not authorised | Generator cannot create a counteroffer or expose unavailable deal meaning |

All eight Frozen response modes can be constructed from deterministic state/rules without adding `DECEIVE`.

## 14. State / disclosure / canon validation rules

The deterministic system should enforce the following invariants before generation and at the pre-display gate where applicable.

1. Every NPC/state/content ID exists in the appropriate authored registry.
2. Dynamic knowledge entries must respect the NPC's authored awareness boundary or a deterministic authored transition that updates that boundary/state.
3. Canonical truth is never inferred from Character Card or NPC surface output.
4. `current knowledge` and `disclosure eligibility` are separate state dimensions.
5. `disclosure eligibility` and `required-now` are separate; only deterministic rule resolution can create required authorised disclosure.
6. Gameplay-relevant clues must not be exposed merely through `permitted_context`.
7. A truthful required world proposition must be compatible with authorised NPC knowledge; an intentional contradictory utterance requires an explicit deterministic authored narrative/deception rule.
8. The generator cannot create relationship changes, evidence, clue unlocks, pending interactions, state deltas, branch IDs, or deal execution.
9. ACCEPT/REJECT text may surface only an already-resolved deterministic deal decision.
10. Active Pending Interaction must be authoritative, current, unique where required, and never selected from old history by the LLM.
11. Authored-but-unavailable `DEAL_LEDGER_FOR_300` cannot be emitted as a new counteroffer unless deterministic rules explicitly expose it in a later state.
12. Hidden canonical facts and locked clues should be excluded from generator context whenever they are not necessary to wording.
13. Output Gate validates required-content coverage, forbidden/unauthorised proposition leakage, canon hallucination, unauthorised commitment, and attempts to express state/evidence consequences.
14. Retry/fallback receives the same deterministic semantic decision; fallback cannot change ANSWER to REFUSE, ACCEPT to REJECT, or otherwise alter plan semantics.

## 15. Edge cases

### E01 — NPC knows X but cannot reveal X

Valid state. X stays in deterministic NPC knowledge but remains absent from generator context. A model cannot choose to reveal it.

### E02 — NPC can reveal X but current plan does not require X

`ELIGIBLE` is not `REQUIRED_NOW`. Gameplay-relevant X must not be placed in optional permitted context where the model could disclose it randomly.

### E03 — Required proposition not supported by NPC knowledge

For an ordinary truthful answer, Response Plan construction is invalid and should fail deterministic validation before generation.

Exception: an explicit authored deception/narrative rule may authorise a contradictory utterance without making it canonical truth.

### E04 — Already revealed clue

`already_revealed_content_refs[]` allows deterministic rules to decide whether to restate, refuse repetition, or move on. The generator does not decide whether a clue is “new”.

### E05 — Relationship change

A relationship change is applied only by deterministic game rules. A generated line such as “I trust you now” cannot itself mutate relationship state; if that statement is gameplay-significant and unauthorised by the plan, the gate rejects it.

### E06 — Evidence creation

Any surface line that invents a new recording, ledger, source, or copy as a gameplay fact is rejected unless the item already exists and the plan authorises mentioning it. Text cannot create evidence.

### E07 — Expired or mismatched pending interaction

If `PENDING_LEDGER_500` is no longer current, ACCEPT/REFUSE cannot bind to it. No consequential response plan is produced from an invalid semantic action.

### E08 — Soft voice variation

Soft style variation should affect quality metrics, not canonical authority. Only specifically authored hard language constraints should cause gate failure.

### E09 — Giant card regression

Supplying the entire event truth, evidence registry, relationship state, and clue graph inside Character Card is invalid architecture even if generation quality appears good, because it defeats least-knowledge and duplicates authoritative state.

## 16. NPC-originated authored-offer lifecycle

The current fixture can represent `PENDING_LEDGER_500` as a deterministic Pending Interaction and can bind player ACCEPT/REFUSE to it.

02C can also safely state the authority order for a future NPC-originated deal:

```text
Deterministic authored deal decision / pending-interaction creation
→ Response Plan authorises surface wording
→ LLM verbalises only
```

However, the Frozen response-mode taxonomy contains no NPC `OFFER` mode. If the design requires the Response Plan itself to originate a new consequential NPC offer/commitment and the existing modes cannot represent that without semantic distortion, specialist 02C must not add a new response mode or broaden generator authority.

**Finding:** NPC-originated authored-offer lifecycle remains unresolved beyond deterministic Pending Interaction representation. If it becomes required by the vertical slice, return to 02 Master. If 02 Master determines a new Response Plan authority semantic or response mode is needed, the issue must return to 01 Master for Frozen Contract review.

## 17. Contract-impact assessment

### No Frozen Contract change required for the validated 02C core

The following are compatible with Frozen v0.1:

- small static Character Card plus separate knowledge boundary;
- authoritative dynamic NPC state;
- deterministic knowledge/disclosure separation;
- deterministic Response Plan construction;
- least-knowledge generator projection;
- hidden-canon exclusion;
- all eight existing response modes;
- deterministic deception as content decision rather than response mode;
- generator output remaining surface text only;
- retry/fallback preserving Response Plan semantics.

### Master review note

The hybrid internal representation of `required_propositions[]` — shared `PROP_*` IDs for world propositions plus response-layer authored clauses for non-world interaction obligations — should be reviewed by 02 Master. It does not change AI authority, response modes, or P0 scope, but if Master judges it to change the Frozen meaning of `required_propositions[]`, it must be escalated to 01 Master before becoming Confirmed.

### Unresolved, not a blocker for current 02C

- production serialization/file format;
- final relationship dimensions/formula;
- richer epistemic distinctions such as mistaken belief vs hearsay, unless later gameplay requires them;
- NPC-originated authored-offer lifecycle;
- production output-gate implementation strategy;
- P1 long-term NPC memory.

## 18. 02C outcome

The shared 02A fixture can support the Frozen Grounded NPC Response Contract with a minimal deterministic state/card model while preserving the authority boundary.

Key validated findings:

- Character Card should be small and static, not a giant world/state prompt.
- Knowledge permission, current knowledge, disclosure eligibility, and required-now content are separate.
- Relationship/attitude can be represented deterministically without defining a final numeric system.
- Clue release, compliance, deal acceptance, relationship changes, evidence creation, and state changes remain deterministic.
- Hidden canon can be withheld from the generator.
- The generator needs only a minimal language projection and returns only surface text.
- Fallback can preserve Response Plan semantic fidelity.
- No `DECEIVE` response mode is required.
- No current fixture case requires changing the Frozen AI authority boundary.

**02C specialist result:** `READY FOR 02 MASTER REVIEW`  
**Validation Increment 02 complete:** No  
**Frozen Contract change required:** No for the validated core  
**01 Master review required now:** No  
**02 Master review required:** Yes
