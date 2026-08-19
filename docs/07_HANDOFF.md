# Handoff

## Project identity

**Between the Lines: AI Remake (BTL-AI)** is a pre-production, PC-first, 2D, narrative/interface-driven journalism game.

The initial product target is a polished **20–30 minute AI-assisted vertical slice**, not the full legacy 14-day experience.

The project has two parallel portfolio goals:

1. demonstrate professional Game Design / Game System Design ability;
2. demonstrate professional AI Product / AI Orchestration ability.

---

## Current milestone

**Validation Increment 01 — AI Interaction Contract**

Status:

**Complete — AI Interaction Contract v0.1 Frozen**

Milestone 0 — Repository Bootstrap is complete.

No Unity project, Dify runtime integration, backend runtime, or production AI implementation exists yet.

---

## Core architecture invariant

> **AI controls language. Deterministic game systems control reality.**

Unity is currently planned to own authoritative game state and deterministic rule evaluation.

LLM output is non-authoritative and must never directly:

- modify canonical game state;
- change gameplay variables;
- create canonical evidence;
- unlock narrative branches;
- determine endings;
- invent critical canonical world facts;
- override authored narrative rules.

---

## Confirmed P0 AI features

The vertical slice currently prioritises:

1. semantic parsing of player-to-NPC dialogue;
2. grounded AI NPC dialogue generation;
3. AI-assisted player-written headline analysis.

These three functions are being designed as separate narrow AI contracts rather than one unrestricted game-controlling LLM.

---

## What changed during Validation Increment 01

An integrated **AI Interaction Contract v0.1** has been validated and frozen.

The contract currently defines:

- a finite authored semantic space behind free-text interaction;
- dialogue semantic interpretation;
- headline Claim Atom interpretation;
- grounded NPC response generation;
- deterministic validation boundaries;
- evidence-reference boundaries;
- ambiguity and unsupported-input handling;
- AI/system failure handling;
- initial evaluation test categories;
- frozen hard safety gates.

Both specialist threads and their targeted regressions are complete:

- `01A | Dialogue & Grounded NPC Response Validation` — complete at `659be28db16bea586136ac00a053f1f01452df96`.
- `01B | Headline Analysis Validation` — complete at `477086429c6beee7fae4da439383708803cf16f4`.

They are paused unless a narrowly scoped regression is requested. This milestone does not authorise runtime implementation.

---

## Shared design principle: Closed Semantic Catalogue

Free-text player language does not imply unlimited gameplay meaning.

The player may express themselves freely, but the AI parser may only map language onto semantic concepts exposed by the authored game catalogue.

The parser must not create new:

- canonical characters;
- factions;
- events;
- evidence;
- gameplay targets;
- narrative facts.

This evolves the legacy constrained-word-bank design into:

> **free vocabulary + bounded gameplay semantics**

rather than unrestricted generative narrative control.

---

## Frozen Dialogue Contract v0.1

Player dialogue v0.1 is represented through a minimal gameplay-oriented semantic candidate.

### Frozen semantic concepts

- status;
- optional resolution reason;
- act;
- optional authored target;
- optional authored value;
- optional polarity;
- an order-insensitive unique set of all gameplay-relevant tactics;
- explicit player-visible evidence references.

### v0.1 Acts

- QUESTION
- ASSERTION
- REQUEST
- OFFER
- ACCEPT
- REFUSE

### v0.1 Tactics

- THREAT
- ACCUSATION
- INDIRECT_PROBE

There is no arbitrary fixed maximum for tactics. Every gameplay-relevant tactic supporting the one consequential action must appear once; duplicate entries and silent truncation are invalid.

Dialogue v0.1 permits only one consequential semantic action per player turn.

Compound consequential actions fail safely rather than being partially executed.
---

## Player truth and deception boundary

The LLM does not classify the player as truthful or lying.

It represents the player's assertion.

Deterministic systems may then compare:

- the assertion;
- canonical world state;
- player knowledge state;
- player evidence/inventory state.

Bluffing may be supported when the player refers to canonical information or evidence known to the player.

The LLM may not create nonexistent evidence to support a bluff.

---

## Frozen Grounded NPC Response Contract v0.1
NPC language generation occurs only after deterministic gameplay resolution.

The intended flow is:

```text
Validated Player Semantic Action
→ Deterministic NPC Rule Resolution
→ Deterministic NPC Response Plan
→ LLM Surface Candidate
→ NPC Output Validation Gate
→ Display
```

The NPC generator does not independently decide:

- clue release;
- relationship changes;
- NPC compliance;
- NPC deception;
- gameplay variables;
- branch changes.

NPC deception is an authored/deterministic content decision orthogonal to response mode; `DECEIVE` is not a response mode.

Where possible, the language model should receive only the utterance proposition required for the current response rather than hidden canonical truth.

This follows a least-knowledge / context-minimisation principle.

---

## Frozen Headline Contract v0.1

Headline analysis is separate from NPC dialogue parsing.

The Headline Analyzer converts a player's headline into one or more authored **Claim Atoms**.

Frozen Claim Atom semantics include:

- target;
- value where required;
- polarity;
- commitment mode (`ASSERTED`, `SPECULATIVE`, `QUESTIONED`);
- explicit source attribution where relevant.

`source_ref_id` is optional and orthogonal to commitment mode. Claim Sets contain all consequential claims with no fixed cap or silent truncation; `RESOLVED + claims=[]` is valid only when no consequential proposition or unresolved consequential content exists. Consequential presuppositions produce Claim Atoms and use `ASSERTED` in v0.1 unless a further gameplay distinction is required.

---

## Confirmed headline evaluation philosophy

Headline gameplay uses an **evidence-based journalism model**.

The main gameplay question is:

> Was the published claim sufficiently supported by the evidence and information available to the player at publication time?

This is separate from canonical truth.

Therefore a headline may be:

- canonically true but insufficiently supported when published;
- reasonably supported at publication time but later proven wrong;
- explicitly attributed to a source without asserting the source's claim as established fact.

The LLM does not determine evidence sufficiency.

Evidence evaluation remains deterministic. Attribution support, underlying-proposition support, and canonical reality are distinct; publication responsibility uses an auditable publication-time evidence/knowledge basis and later evidence cannot rewrite that original judgement.

---

## Confirmed pre-publish feedback direction

High-risk headlines may trigger a neutral warning before publication.

The warning describes the **kind of journalistic claim being made**, rather than revealing hidden evidence evaluation or canonical truth.

Example:

> “This headline makes a direct allegation of responsibility.”

The warning must not say:

> “You do not have enough evidence.”

Players retain the choice to:

- Edit
- Publish Anyway

This preserves meaningful uncertainty.

---

## Headline atomic-resolution rule

Frozen rule:

A headline should not be partially simulated if it contains an unresolved consequential claim.

If one gameplay-relevant claim cannot be mapped into the authored semantic space, the complete headline should not proceed into publication resolution.

Stylistic language does not require semantic representation unless gameplay rules depend on it.

This behaviour passed `01B` targeted regression and is frozen.

---

## Current semantic status model

Current shared semantic statuses:

- RESOLVED
- AMBIGUOUS
- UNSUPPORTED

Candidate non-authoritative reasons include:

- AMBIGUOUS_REFERENCE
- INSUFFICIENT_CONTEXT
- MULTIPLE_ACTIONS
- OUT_OF_CATALOGUE
- UNSUPPORTED_ACTION

Model/API/schema failures are system failures and are not semantic statuses.

---

## Failure model

Three failure/behaviour classes are currently distinguished.

### Semantic Failure

The system cannot safely determine gameplay meaning.

Examples:

- ambiguous reference;
- unsupported concept;
- multiple dialogue actions.

Result:

safe no-op or clarification; no canonical consequence.

### AI / System Failure

Examples:

- timeout;
- malformed structured output;
- invalid enum;
- validator rejection;
- NPC generator violating response constraints.

NPC surface failure fallback:

Retry once → revalidate → semantically faithful deterministic/template fallback.

Headline parser retry exhaustion may only preserve the draft and show non-consequential edit/retry UX; it cannot fabricate a Claim Set or continue publication resolution.

AI/system failure should not itself consume a consequential player action or create irreversible consequences.

### Valid Risky Gameplay

Examples:

- bluffing;
- threats;
- false assertions;
- evidence-insufficient publication.

These are not AI failures.

Once safely interpreted, they proceed to deterministic rules.

---

## Frozen hard safety gates

The following are frozen correctness constraints for AI Interaction Contract v0.1 rather than average-quality metrics:

- Unauthorized canonical state mutation = 0
- Invalid canonical ID accepted = 0
- Unauthorized NPC fact disclosure = 0
- Unauthorized NPC action / commitment expressed = 0
- Response-plan-invalid NPC output displayed = 0
- LLM-generated state or branch decisions accepted = 0
- Semantically unresolved headline entering publication resolution = 0
- AI/system failure creating irreversible gameplay consequence = 0

Any occurrence of these conditions is treated as a defect rather than averaged away through an overall quality score.

---

## Current quality-metric candidates

Potential measurable metrics include:

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
- NPC Response Plan Compliance
- Required Proposition Coverage

Numerical acceptance thresholds must not be invented before a real baseline is measured.

---

## Validation-thread record

Validation Increment 01 used a Master reconciliation thread and two specialist threads. All three have completed their assigned milestone work.

### Master

**01 | AI Interaction Contract — Validation Increment 01**

Purpose:

- maintain shared contract;
- resolve cross-system architecture issues;
- approve significant schema changes;
- integrate findings from specialised threads;
- reconciled the findings and froze Contract v0.1.

The Master thread should only reopen this scope for an authorised, narrowly scoped regression or a later design increment.

### 01A

**01A | Dialogue & Grounded NPC Response Validation**

Completed scope:

- dialogue semantics, tactics, evidence references, bluffing, ambiguity, and failure handling;
- deterministic NPC Response Plans, deception, information leakage, hallucination, and pre-display validation;
- the first dialogue/NPC evaluation fixture and targeted regression at `659be28db16bea586136ac00a053f1f01452df96`.

**Status:** Complete and paused unless a narrowly scoped regression is requested.

### 01B

**01B | Headline Analysis Validation**

Completed scope:

- Claim Atom extraction, multi-claim headlines, commitment, attribution, presupposition, and zero-claim cases;
- evidence-based journalism semantics, atomic resolution, parser failure, neutral warnings, and rhetorical deferrals;
- the first headline evaluation fixture and targeted regression at `477086429c6beee7fae4da439383708803cf16f4`.

**Status:** Complete and paused unless a narrowly scoped regression is requested.

---

## Next permitted work

Keep this frozen Contract and its fixtures as the baseline. Do not resume 01A or 01B except for an explicitly requested, narrowly scoped regression. Any implementation or orchestration work requires a separate authorised increment and must preserve the Contract's deterministic authority boundary.

---

## Do not do yet

Do not:

- create a Unity project;
- implement gameplay state classes;
- build a Dify runtime workflow;
- choose production prompts;
- lock a backend/API architecture;
- design full 14-day content;
- define arbitrary Reputation/Public Opinion/Threat/Money formulas;
- create full NPC/world canon merely to make the tests easier.

Temporary validation fixtures may be used, but they are non-canonical unless explicitly approved later.

---

## Files future threads should read first

Priority:

1. Project Instructions
2. `docs/01_PROJECT_DEFINITION.md`
3. `docs/05_DECISION_LOG.md`
4. `docs/08_AI_INTERACTION_CONTRACT.md` (Frozen)
5. `docs/06_CURRENT_STATE.md`
6. `docs/07_HANDOFF.md`

Legacy Design is historical design evidence only.

It does not automatically override the Remake's confirmed design.

---

## Known unresolved questions

- Detailed vertical-slice story canon
- Final NPC roster
- Final faction design
- Semantic Target Catalogue contents
- Evidence–Claim Relationship Table
- NPC state schema
- Reputation/Public Opinion/Threat/Money rules
- AI model baseline performance
- Evaluation acceptance thresholds
- Backend/API architecture
- Dify feasibility and integration
- Unity implementation architecture
- Whether rhetorical framing needs an authoritative gameplay field

These remain unresolved unless explicitly confirmed in a future Decision Log entry.

## Repository baseline

Current stable validated branch:

`main`

Validation Increment 01 was developed and validated on:

`design/validation-increment-01`

and has now been integrated into `main`.

The completed validation branch may be retained as historical development evidence. Future substantial work should use a new branch appropriate to the next authorised increment.