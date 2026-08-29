# AI Interaction Contract v0.1.1 — Validation Increment 01

**Project:** Between the Lines: AI Remake (BTL-AI)  
**Status:** Candidate revision — pending 01 Master final checkpoint
**Phase:** Pre-production / Validation Increment 01  
**Scope:** Player–NPC dialogue parsing, grounded NPC dialogue generation, player-written headline analysis

---

## v0.1.1 Revision Note

Technical Prototype 01 demonstrated that candidate-only deterministic runtime validation cannot independently prove semantic fidelity or completeness against arbitrary natural-language source text. v0.1.1 clarifies two separate assurance responsibilities: deterministic runtime contract validation of observable candidate/context conditions, and reproducible semantic-fidelity/completeness evaluation against authored fixture ground truth.

This patch does not change the v0.1 Dialogue schema, Headline schema, semantic statuses, NPC Response Plan authority, AI authority boundary, P0 scope, or Hard Safety Gate set. Git history preserves v0.1, and the historical VI01/VI02/03 reports remain unchanged.

---

## 1. Purpose

This contract defines the boundary between free-text player language and deterministic game systems.

Its purpose is not to make the LLM understand unrestricted game meaning. Its purpose is to translate flexible natural-language expression into a **finite, authored semantic space** that can be safely validated and consumed by deterministic game rules.

The governing architecture rule is:

> **AI controls language. Deterministic game systems control reality.**

The LLM may interpret or render language, but it MUST NOT directly modify canonical game state, determine narrative branches, create evidence, calculate gameplay variables, determine endings, or override authored rules.

---

# 2. Core Architecture

Validation Increment 01 contains three P0 AI interaction contracts.

### A. Dialogue Semantic Parser

**Player language → semantic candidate**

Purpose:

- understand what communicative action the player is attempting;
- map free text onto authored gameplay meanings;
- identify explicit tactics and evidence references;
- identify when the input cannot be safely mapped.

### B. Grounded NPC Response Generator

**Deterministic response plan → natural NPC language**

Purpose:

- express an already resolved NPC action naturally;
- respect character voice and knowledge boundaries;
- never independently decide what the NPC reveals or what happens.

### C. Headline Analyzer

**Player-written headline → structured claim candidates**

Purpose:

- identify consequential claims contained in a headline;
- represent attribution, negation, and commitment mode;
- make those claims available for deterministic evidence and publication evaluation.

These three systems MUST remain separated by deterministic validation boundaries.

---

# 3. Closed Semantic Catalogue

Free-text interaction does not create an unlimited semantic game space.

At runtime, each AI parser receives only an authored catalogue of meanings that are currently valid and player-visible.

The catalogue MAY contain:

- semantic targets;
- allowed target values;
- allowed acts;
- player-visible evidence;
- player-visible sources;
- current pending interactions.

The parser MUST NOT invent IDs, factions, evidence, characters, events or gameplay concepts outside this catalogue.

The design principle is:

> **Legacy BTL limited the player's vocabulary.  
> BTL-AI limits the meanings the game is allowed to assign to the player's vocabulary.**

This retains narrative controllability while allowing keyboard-first free-text interaction.

---

# 4. Shared Semantic Resolution

Both Dialogue Parsing and Headline Analysis use a semantic status.

## Status

### `RESOLVED`

There is one valid interpretation within the currently available authored semantic space.

Only RESOLVED output may proceed to deterministic contract validation.

### `AMBIGUOUS`

Two or more plausible gameplay interpretations remain.

No consequential action may execute.

### `UNSUPPORTED`

The language may be understandable, but it cannot be mapped to a currently supported gameplay meaning.

No consequential action may execute.

---

## Resolution Reason

When status is not RESOLVED, a non-authoritative reason MAY be returned for fallback UX and evaluation.

Initial v0.1 reasons:

- `AMBIGUOUS_REFERENCE`
- `INSUFFICIENT_CONTEXT`
- `MULTIPLE_ACTIONS`
- `OUT_OF_CATALOGUE`
- `UNSUPPORTED_ACTION`

These reasons MUST NOT independently trigger gameplay consequences.

API failure, timeout, malformed structured output or schema validation failure are **system failures**, not semantic statuses.

---

# 5. Semantic Schema v0.1 — Dialogue

The Dialogue Semantic Parser represents one player turn as:

**Status → Act → Authored Target → Optional Value / Polarity → Optional Tactics / Evidence References**

## Core Fields

### `status`

Always required.

### `reason`

Only meaningful when status is not RESOLVED.

### `act`

Required when status is RESOLVED.

Allowed v0.1 acts:

- `QUESTION`
- `ASSERTION`
- `REQUEST`
- `OFFER`
- `ACCEPT`
- `REFUSE`

Additional language categories MUST NOT be added unless a deterministic gameplay rule genuinely needs to distinguish them.

### `target_id`

Identifies the authored gameplay meaning the player is addressing.

Required when the selected Act and Target Catalogue require it.

Current NPC, scene and event IDs MUST NOT be returned by the LLM when those are already known from deterministic UI/game context.

### `value_id`

Represents an authored value associated with a target.

It MUST be selected only from that target's allowed value domain.

It MUST NOT contain arbitrary free-text world information.

### `polarity`

Used when the player affirms or denies a proposition.

Initial values:

- `AFFIRM`
- `DENY`

Polarity is conditional rather than universally required.

### `tactics[]`

Represents gameplay-relevant conversational strategies as an order-insensitive unique set. There is no arbitrary fixed maximum: the set contains every gameplay-relevant authored tactic expressed by the single consequential action.

Initial tactics:

- `THREAT`
- `ACCUSATION`
- `INDIRECT_PROBE`

No tactic is represented by an empty collection. Duplicate values are invalid, and gameplay-relevant tactics MUST NOT be silently truncated.

The parser identifies that a tactic is being attempted.

It MUST NOT determine whether that tactic succeeds.

### `evidence_ref_ids[]`

Represents explicit references to canonical, player-visible evidence.

A reference indicates only that the player mentioned the evidence.

It does NOT establish:

- evidence ownership;
- authenticity;
- relevance;
- evidentiary strength;
- whether the evidence proves the player's claim.

Those are deterministic responsibilities.

---

# 6. Dialogue Conditional Rules

A RESOLVED output MUST satisfy the current Target Catalogue.

Examples:

**QUESTION**

May identify a target without specifying a value.

Example:

> “Who paid you?”

may resolve to:

`QUESTION → PAYMENT_PAYER`

---

**ASSERTION**

A valued proposition normally requires:

Target + Value + Polarity.

Example:

> “The mayor's office paid you.”

corresponds conceptually to:

`ASSERTION → PAYMENT_PAYER → MAYOR_OFFICE → AFFIRM`

---

**REQUEST**

Must identify an authored requestable target.

Example:

> “Give me the ledger.”

maps to the authored `HAND_OVER_LEDGER` target.

The AI does not decide whether the NPC complies.

---

**OFFER**

Must identify an authored bilateral deal target. A surface imperative may still be an OFFER when it expresses that deal.

Counteroffers are OFFERs only when they map to another available authored deal target. The parser MUST NOT create free-form deal terms or targets; unsupported negotiation fails safely. Richer free-form negotiation remains deferred.

---

**ACCEPT / REFUSE**

Bind to the unique deterministic Pending Interaction.

The LLM MUST NOT independently select an old or unrelated offer.

If no suitable pending interaction exists, the input cannot resolve as a valid consequential ACCEPT or REFUSE.

---

## Single Consequential Action Rule

Dialogue v0.1 permits one consequential semantic action per player turn.

Example:

> “Tell me who paid you and where you were last night.”

becomes:

`UNSUPPORTED / MULTIPLE_ACTIONS`

The system MUST NOT execute one part and silently ignore another.

A single action may still contain tactics and evidence references.

Example:

> “Tell me who paid you or I release the photograph.”

remains one REQUEST with a THREAT tactic and evidence reference.

---

# 7. Player Deception

`LIE` is not an LLM semantic field.

The parser represents what the player asserts.

Deterministic systems compare that assertion against:

- canonical world state;
- player knowledge state;
- evidence ownership where relevant.

Therefore:

**False statement ≠ automatically intentional lie.**

A deception attempt may only be inferred through deterministic game logic when the required conditions exist.

---

## Bluffing

v0.1 may support bluffing about canonical information or evidence known to the player.

Example:

The player knows PHOTO_01 exists but does not possess it and says:

> “I have the photograph.”

The parser may identify the PHOTO_01 reference and possession assertion.

The deterministic system determines that the player does not actually possess it.

The LLM MUST NOT create a previously nonexistent `SECRET_PHOTO_99` in response to a bluff.

---

# 8. Semantic Schema v0.1 — Headline

Headline analysis uses a separate schema from NPC dialogue.

The Headline Analyzer represents:

**Status → all consequential Claim Atoms, including zero when none are present**

`RESOLVED + claims=[]` is valid only when the headline contains no consequential proposition and no unresolved consequential content. There is no fixed Claim Atom limit, and consequential claims MUST NOT be silently truncated.

The current event SHOULD come from deterministic UI context when the player entered the headline editor from a known story/event.

The LLM should not repeat an event ID the game already knows.

---

## Claim Atom

Each consequential claim contains:

### `target_id`

The authored proposition being expressed.

### `value_id`

The authored value assigned to the proposition where required.

### `polarity`

Affirmation or denial when required.

### `commitment_mode`

How the headline commits to the proposition, independently of whether a source is named.

v0.1 values:

- `ASSERTED`
- `SPECULATIVE`
- `QUESTIONED`

Consequential presuppositions also produce Claim Atoms. In v0.1, use `ASSERTED` when the presupposition does not require an additional gameplay distinction.

### `source_ref_id`

Optional when the headline explicitly attributes the proposition to a known source.

It indicates linguistic attribution only.

It MUST NOT mean that the source is truthful or reliable.

---

# 9. Headline Atomic Resolution

Headline semantic interpretation is **all-or-nothing** at the consequential-claim level.

If a headline contains a consequential claim that cannot be mapped into the current catalogue, the full headline MUST NOT proceed to publication resolution.

The system MUST NOT simulate only the parts it understood while displaying a materially different complete headline to the player.

Example:

> “Security forces fired first as CIA agents directed the operation.”

If `CIA` is outside the authored semantic catalogue, the headline does not partially resolve only the first clause.

It must be revised before deterministic publication evaluation.

Stylistic language does not require semantic IDs unless gameplay rules depend on it.

---

# 10. Headline Evaluation Philosophy

Headline consequences use an **evidence-based journalism model**, not an omniscient truth-answer model.

The primary deterministic question is:

> **Was the published claim sufficiently supported by the information and evidence available to the player at publication time?**

This is separate from whether the claim later proves canonically true.

A player may therefore publish a claim that is:

- canonically true but insufficiently supported when published;
- supported by apparently reliable evidence but later proven factually wrong;
- explicitly presented as an attributed allegation rather than asserted as fact.

This distinction is intentional gameplay.

---

# 11. Commitment, Attribution, and Evidence Responsibility

The same underlying proposition may create different journalistic responsibilities.

Example:

> “Security forces fired first.”

is `ASSERTED` without attribution.

> “Witness says security forces fired first.”

is `ASSERTED` with a source reference.

Attribution support (whether the source expressed the proposition), underlying-proposition support, and canonical reality are separate deterministic concepts. Evidence sufficient to support the second form does not automatically establish the first as fact.

Publication responsibility MUST use an auditable evidence / knowledge basis captured at publication time. Later evidence or later player knowledge MUST NOT retroactively rewrite the responsibility judgement for the original publication.

This allows journalistic language itself to become gameplay without requiring generic morality, bias or misinformation scores.

---

# 12. Pre-Publish Risk Feedback

The game may warn the player before a high-risk publication.

The warning MUST describe the player's **language behaviour**, not reveal hidden evidence evaluation or canonical truth.

Example acceptable warning:

> “This headline makes a direct allegation of responsibility.”

Unacceptable:

> “You do not have enough evidence to support this allegation.”

The player retains the option to:

**Edit** or **Publish Anyway**.

The warning system MUST NOT become an automatic correctness checker.

---

# 13. Rhetorical Tone

Generic sentiment, emotionality, political bias or sensationalism scores are excluded from authoritative v0.1 headline semantics.

Terms such as:

“killed”, “murdered”, “slaughtered”, “neutralised”

will remain Evaluation Dataset cases.

A separate authored `rhetorical_frame` field MAY be considered in a later increment only if testing demonstrates that meaningful gameplay distinctions cannot be represented through Claim Atoms.

---

# 14. Grounded NPC Response Contract

NPC response generation occurs only after deterministic gameplay resolution.

The required flow is:

```text
Validated Player Semantic Action
→ Deterministic NPC Rule Resolution
→ Deterministic NPC Response Plan
→ LLM Surface Candidate
→ NPC Output Validation Gate
→ Display
```

The LLM MUST NOT independently decide what the NPC does.

---

## NPC Response Plan

The deterministic system supplies information such as:

- response mode;
- required propositions;
- permitted context;
- forbidden propositions;
- player-visible clarification options;
- relevant dynamic state;
- language/personality constraints from the NPC card;
- minimal conversation context required for generation.

Initial response modes:

- `ANSWER`
- `PARTIAL_ANSWER`
- `EVADE`
- `REFUSE`
- `CLARIFY`
- `COUNTERQUESTION`
- `ACCEPT`
- `REJECT`

`DECEIVE` is not a response mode. Deception is a deterministic content/narrative decision orthogonal to response mode: the plan authorises the precise deceptive proposition, where applicable.

`permitted_context` may ground safe wording, but it does not authorise gameplay-relevant optional clue disclosure. Such disclosure MUST be expressly represented in the required/authorised response content.

---

## Generator Output

The authoritative v0.1 generator output is only:

> **NPC surface response text**

The generator MUST NOT output authoritative:

- relationship changes;
- clue unlocks;
- NPC decisions;
- evidence;
- state changes;
- branch IDs;
- truth evaluations.

---

# 15. NPC Output Validation Gate and Deception

The Gate validates the Surface Candidate before display. It MUST reject a candidate that omits a required proposition; expresses a forbidden or unauthorised gameplay-relevant proposition; invents canon; expresses an unauthorised action, promise, commitment, trade, compliance, or refusal; contradicts the Response Plan; or attempts to create state, evidence, or branch consequences.

On a gate failure: **retry once → revalidate → semantically faithful deterministic/template fallback → Display**. A response-plan-invalid candidate MUST never be displayed. The fallback preserves the deterministic response decision; it does not convert an authorised answer into a refusal or otherwise alter semantic content.

Parser-level Semantic Clarification is separate from resolved-action NPC `CLARIFY`: semantic clarification has no Validated Player Semantic Action and produces no normal Response Plan, whereas NPC `CLARIFY` is an authorised deterministic response mode after action resolution.

## NPC Deception

NPC deception is a deterministic narrative decision, not LLM hallucination.

If canonical reality is:

> COMPANY_A paid the NPC

but deterministic NPC rules resolve:

> the NPC lies and claims MILITIA paid them

the generator should receive only the utterance proposition it is authorised to express.

Where practical, hidden canonical truth SHOULD NOT be included in the generation context.

This implements a **least-knowledge / context-minimisation** principle.

---

# 16. Authority Boundary

The formal authority boundary is:

```text
PLAYER LANGUAGE
      ↓
LLM Semantic Interpretation
      ↓
Non-authoritative Semantic Candidate
      ↓
====================================
          AI AUTHORITY ENDS
====================================
      ↓
Contract Validator
      ↓
Canonical / Context / Evidence Validation
      ↓
Deterministic Game Rule Engine
      ↓
State / Clue / NPC Decision / Branch
```

NPC language generation occurs after deterministic resolution:

```text
Deterministic NPC Response Plan
      ↓
LLM Surface Candidate
      ↓
NPC Output Validation Gate
      ↓
Display
```

Headline analysis similarly ends before evidence evaluation:

```text
Player Headline
      ↓
LLM Claim Extraction
      ↓
====================================
          AI AUTHORITY ENDS
====================================
      ↓
Claim Validation
      ↓
Player Knowledge + Evidence Rules
      ↓
Publication Rule Engine
      ↓
Gameplay Consequences
```

---

# 17. Information the LLM MUST NOT Determine

P0 AI systems MUST NOT authoritatively determine:

- whether the player is intentionally lying;
- whether an NPC believes the player;
- whether a threat succeeds;
- whether evidence is authentic;
- whether the player owns evidence;
- whether evidence proves a proposition;
- canonical truth;
- clue unlocks;
- relationship changes;
- narrative branches;
- Reputation changes;
- Public Opinion changes;
- Threat Level changes;
- Money changes;
- endings;
- canonical new people, factions, events or evidence.

---

# 18. Runtime Contract Validation and Semantic Fidelity Evaluation

A RESOLVED semantic candidate is not automatically trusted.

## A. Deterministic Runtime Contract Validation

The deterministic runtime validator MUST verify observable candidate and context conditions where relevant:

- valid enum values;
- target ID exists;
- target is currently available;
- selected act is allowed for the target;
- required value exists;
- value belongs to the target;
- polarity is structurally valid;
- reported tactic values are legal, target-compatible, and unique;
- evidence IDs exist in the supplied player-visible catalogue;
- ACCEPT / REFUSE has a valid pending interaction;
- the candidate structurally represents one consequential Dialogue action;
- each reported Claim Atom has legal fields and satisfies current target/value/polarity/commitment/source requirements;
- headline targets are currently available and headline-eligible;
- the candidate contains no unauthorised structured authority output.

Only runtime-contract-valid output may become a **Validated Semantic Action** or **Validated Claim Set** and proceed to deterministic game rules. Runtime contract validity is not, by itself, a certification that an arbitrary source utterance or headline was interpreted completely or faithfully.

## B. Semantic Fidelity / Completeness Evaluation

The following remain REQUIRED parser behaviours and mandatory evaluation correctness requirements:

- every gameplay-relevant authored tactic expressed by the single consequential Dialogue action is retained with no silent truncation;
- every consequential Claim Atom expressed by the headline is retained with no silent truncation;
- no catalogue-valid but source-text-unsupported Claim Atom is invented;
- general act/target/value/polarity/commitment/source interpretation remains faithful to the source text.

Candidate-only runtime validation cannot independently observe or prove these properties for arbitrary natural-language input. During the reproducible baseline, they are measured by comparing the non-authoritative candidate with authored fixture ground truth. Tactic omission, Claim Atom omission, semantic truncation, and extra Claim Atoms are mandatory semantic-fidelity evaluation failures.

The fixture ground-truth oracle is evaluation-only. It MUST NOT be represented as a production runtime validator, a second authoritative LLM judge, or a deterministic full-natural-language parser. A ground-truth mismatch does not create a production runtime contract-failure or retry signal because that authored expected semantic result is not available for arbitrary runtime player input.

---

# 19. Failure / Fallback Policy v0.1

Failures are divided into three classes.

## A. Semantic Failure

Examples:

- ambiguous reference;
- unsupported target;
- multiple dialogue actions;
- insufficient interaction context.

Behaviour:

- do not change canonical state;
- request clarification or use safe no-op feedback;
- do not guess the closest consequential branch.

---

## B. AI / System Failure

Examples:

- timeout;
- malformed structured response;
- illegal enum;
- invalid canonical ID;
- schema violation;
- NPC generator violates response plan.

Default handling:

For dialogue and NPC surface generation: **Retry once → validate again → semantically faithful deterministic/template fallback**.

For headline parsing: retry once and validate again. If retry is exhausted, preserve the player's draft and show non-consequential edit/retry UX only. The system MUST NOT fabricate a Claim Set, and publication resolution MUST NOT continue.

A model/system failure MUST NOT itself create an irreversible gameplay consequence.

A model/system failure SHOULD NOT consume a limited consequential player action.

An authored-baseline semantic-fidelity mismatch is an evaluation correctness failure, not by itself an observable production runtime AI/System Failure or retry trigger.

---

## C. Valid Risky Gameplay

Examples:

- player makes a false assertion;
- player threatens an NPC;
- player bluffs about evidence;
- player publishes an evidence-insufficient allegation;
- player publishes information contradicted by available evidence.

These are not parser failures.

Once safely understood and validated, they proceed into deterministic gameplay rules.

---

# 20. Headline Failure Rule

`SEMANTIC_UNRESOLVED` and `EVIDENCE_INSUFFICIENT` are fundamentally different conditions.

Semantic unresolved means:

> the game cannot safely determine what the player is publishing.

The headline does not proceed.

Evidence insufficient means:

> the game understands the headline, but the player's reporting choice is risky.

The player may Publish Anyway.

---

# 21. Evaluation Test Categories v0.1

## Dialogue Semantic Parser

Test categories include:

- clear semantic mapping;
- paraphrase robustness;
- negation;
- questioning vs assertion;
- threats;
- accusations;
- indirect probing;
- evidence references;
- bluff statements;
- context-dependent ACCEPT / REFUSE;
- ambiguous references;
- multiple actions;
- out-of-catalogue input;
- prompt injection;
- malformed model output.

## Grounded NPC Generator

Test categories include:

- required proposition coverage;
- partial disclosure;
- forbidden fact leakage;
- evasion;
- refusal;
- clarification;
- deterministic NPC deception;
- character-card grounding;
- dynamic-state grounding;
- canon hallucination;
- prompt injection resistance;
- response-plan compliance.

## Headline Analyzer

Test categories include:

- single-claim extraction;
- multi-claim extraction;
- attribution;
- negation;
- commitment mode;
- source attribution;
- speculation vs assertion;
- question vs assertion;
- unsupported entities;
- claim omission;
- emotionally loaded wording;
- prompt injection;
- malformed output.

---

# 22. Hard Safety Gates

The following are correctness constraints rather than average quality metrics:

- **Unauthorized canonical state mutation = 0**
- **Invalid canonical ID accepted = 0**
- **Unauthorized NPC fact disclosure = 0**
- **LLM-generated branch/state delta accepted = 0**
- **Unauthorized NPC action / commitment expressed = 0**
- **Response-plan-invalid NPC output displayed = 0**
- **Semantically unresolved headline entering publication resolution = 0**
- **AI/system failure creating irreversible gameplay consequence = 0**

Any occurrence should be treated as a defect rather than averaged away through an overall accuracy score.

`Semantically unresolved headline entering publication resolution = 0` applies whenever unresolved or invalid state is observable at runtime, including `AMBIGUOUS`, `UNSUPPORTED`, schema failure, or deterministic runtime contract-validation failure. It does not assert that every `RESOLVED` runtime-contract-valid candidate has been independently proven semantically complete against arbitrary original free text.

Semantic tactic omission, consequential Claim Atom omission, and catalogue-valid but source-text-unsupported extra Claim Atoms remain mandatory baseline evaluation correctness failures. This clarification does not add or remove a Hard Safety Gate.

---

# 23. Quality Metrics

Initial measurable quality metrics include:

- Act Accuracy
- Target Exact Match
- Value Exact Match
- Polarity Accuracy
- Tactic Precision / Recall
- Evidence Reference Accuracy
- Ambiguity Detection
- Claim Atom Exact Match
- Claim Omission Rate
- Commitment Mode Accuracy
- Source Attribution Accuracy
- Response Mode Compliance
- Required Proposition Coverage

Tactic Precision / Recall, Claim Atom Exact Match, Claim Omission Rate, and the other source-interpretation accuracy metrics belong to authored-ground-truth semantic-fidelity baseline evaluation. They are not claims that candidate-only deterministic runtime validation can independently re-derive arbitrary source-text meaning.

Acceptance thresholds are intentionally deferred until a real model baseline has been measured during validation.

---

# 24. Explicitly Deferred

Validation Increment 01 does not define:

- detailed vertical-slice story canon;
- final NPC roster;
- final Target Catalogue content;
- final Evidence–Claim Relationship Table;
- Reputation formulas;
- Public Opinion formulas;
- Threat Level formulas;
- Money formulas;
- narrative branch thresholds;
- backend/API architecture;
- production Dify architecture;
- Unity implementation;
- generic rhetorical framing mechanics;
- full NPC memory implementation.

These belong to later validation/design increments.

---

# 25. Contract Success Condition

Validation Increment 01 succeeds when:

1. Free-text dialogue can be converted into constrained semantic candidates.
2. Player-written headlines can be converted into constrained Claim Atoms.
3. NPC language can be generated from deterministic response plans without acquiring gameplay authority.
4. Invalid, ambiguous and unsupported AI outputs fail safely.
5. Evidence and canonical truth remain deterministic.
6. AI output cannot directly alter game reality.
7. A reproducible evaluation set can measure semantic quality and authority-boundary failures before runtime implementation begins.

These conditions are the v0.1.1 candidate revision, pending 01 Master final checkpoint. Any Dify or Unity work still requires a separately authorised implementation-validation increment; this Contract does not authorise implementation.
