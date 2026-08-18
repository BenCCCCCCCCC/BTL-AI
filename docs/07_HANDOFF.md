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

**Draft — Freeze Candidate / Validation in progress**

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

An integrated **AI Interaction Contract v0.1 Draft** has been designed.

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
- hard safety-gate candidates.

The contract is not yet frozen.

It must first be pressure-tested in two specialised validation threads.

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

## Current Dialogue Contract direction

Player dialogue is currently represented through a minimal gameplay-oriented semantic candidate.

Current proposed semantic concepts:

- status;
- optional resolution reason;
- act;
- optional authored target;
- optional authored value;
- optional polarity;
- limited gameplay-relevant tactics;
- explicit player-visible evidence references.

Current Act candidates:

- QUESTION
- ASSERTION
- REQUEST
- OFFER
- ACCEPT
- REFUSE

Current Tactic candidates:

- THREAT
- ACCUSATION
- INDIRECT_PROBE

Current proposal allows zero to two tactics in one otherwise single consequential dialogue action.

Dialogue v0.1 currently permits only one consequential semantic action per player turn.

Compound consequential actions are expected to fail safely rather than being partially executed.

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

## Current Grounded NPC Response direction

NPC language generation occurs only after deterministic gameplay resolution.

The intended flow is:

Validated Player Semantic Action  
→ Deterministic NPC Rule Resolution  
→ NPC Response Plan  
→ LLM Surface Language

The NPC generator does not independently decide:

- clue release;
- relationship changes;
- NPC compliance;
- NPC deception;
- gameplay variables;
- branch changes.

NPC deception is an authored/deterministic response decision.

Where possible, the language model should receive only the utterance proposition required for the current response rather than hidden canonical truth.

This follows a least-knowledge / context-minimisation principle.

---

## Current Headline Contract direction

Headline analysis is separate from NPC dialogue parsing.

The Headline Analyzer converts a player's headline into one or more authored **Claim Atoms**.

Current proposed Claim Atom semantics include:

- target;
- value where required;
- polarity;
- claim posture;
- explicit source attribution where relevant.

Current Claim Posture candidates:

- FACT_ASSERTION
- ATTRIBUTED_CLAIM
- SPECULATION
- QUESTION

The current proposed limit is one to three consequential Claim Atoms per headline.

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

Evidence evaluation remains deterministic.

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

## Headline atomic-resolution proposal

Current Freeze Candidate:

A headline should not be partially simulated if it contains an unresolved consequential claim.

If one gameplay-relevant claim cannot be mapped into the authored semantic space, the complete headline should not proceed into publication resolution.

Stylistic language does not require semantic representation unless gameplay rules depend on it.

This proposal must be pressure-tested in `01B`.

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

Current proposed fallback:

Retry once  
→ validate again  
→ deterministic authored/template fallback.

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

## Current hard safety candidates

The following are intended as hard correctness constraints rather than average-quality metrics:

- Unauthorized canonical state mutation = 0
- Invalid canonical ID accepted = 0
- Unauthorized NPC fact disclosure = 0
- LLM-generated branch/state delta accepted = 0
- Semantically unresolved headline entering publication resolution = 0
- AI/system failure creating irreversible gameplay consequence = 0

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
- Claim Posture Accuracy
- Source Attribution Accuracy
- NPC Response Plan Compliance
- Required Proposition Coverage

Numerical acceptance thresholds must not be invented before a real baseline is measured.

---

## Validation thread split

Validation Increment 01 is now split into three conversations.

### Master

**01 | AI Interaction Contract — Validation Increment 01**

Purpose:

- maintain shared contract;
- resolve cross-system architecture issues;
- approve significant schema changes;
- integrate findings from specialised threads;
- decide when Contract v0.1 can be frozen.

Do not use the Master thread for large numbers of detailed test cases once specialised threads are active.

### 01A

**01A | Dialogue & Grounded NPC Response Validation**

Purpose:

- pressure-test Dialogue Semantic Schema;
- test contextual interpretation;
- test tactics;
- test evidence references and bluffing;
- test semantic ambiguity/fallback;
- pressure-test deterministic NPC Response Plans;
- test NPC knowledge boundaries, deception, leakage and hallucination;
- build the first dialogue/NPC evaluation dataset.

Cross-cutting changes must return to Master.

### 01B

**01B | Headline Analysis Validation**

Purpose:

- pressure-test the Claim Atom model;
- test multi-claim headlines;
- test negation, attribution, speculation and questions;
- test evidence-based journalism semantics;
- test atomic headline resolution;
- test neutral pre-publish warnings;
- retain difficult rhetorical cases for future framing decisions;
- build the first headline evaluation dataset.

Cross-cutting changes must return to Master.

---

## Immediate next tasks

1. Save the integrated AI Interaction Contract v0.1 Draft into the repository.
2. Update Decision Log with newly confirmed headline decisions.
3. Update Current State and this Handoff.
4. Commit the documentation checkpoint.
5. Refresh the latest project-source snapshots used by ChatGPT.
6. Start `01A`.
7. Start `01B`.
8. Run both validation tracks in parallel.
9. Return structural conflicts to the Master thread.
10. Freeze AI Interaction Contract v0.1 only after both validation tracks have completed their first pressure-test pass.

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
4. latest AI Interaction Contract v0.1 Draft
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