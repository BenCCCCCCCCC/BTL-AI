# Current State

## Current phase

Pre-production — Validation Increment 01: AI Interaction Contract validation.

## Completed

- Repository bootstrap and baseline documentation completed, committed to `main`, and published to a private GitHub repository.
- Confirmed product direction and architecture invariants recorded.
- Initial AI Interaction Contract v0.1 integrated draft completed.
- Initial semantic models defined for:
  - player-to-NPC dialogue interpretation;
  - deterministic-to-NPC grounded response generation;
  - player-written headline analysis.
- Initial authority boundary defined:
  - AI interprets or renders language;
  - deterministic systems validate meaning and control canonical reality.
- Initial Failure / Fallback Policy defined.
- Initial Evaluation Test Categories defined.
- Evidence-based headline evaluation direction confirmed.
- Neutral behaviour-based pre-publish warning direction confirmed.

## In progress

AI Interaction Contract v0.1 is currently a **Draft — Freeze Candidate**.

The next validation work will pressure-test the shared contract through two parallel design threads:

1. `01A | Dialogue & Grounded NPC Response Validation`
2. `01B | Headline Analysis Validation`

The purpose of these threads is to identify structural problems in the contract before implementation.

## Current contract direction

### Dialogue

Current proposed semantic interpretation contains only gameplay-relevant information:

- semantic status;
- resolution reason where applicable;
- communicative act;
- authored target;
- authored value where required;
- polarity where required;
- limited gameplay-relevant tactics;
- explicit canonical evidence references.

The LLM does not determine success, truth, deception, state changes, narrative branches, evidence validity, or NPC reactions.

### Grounded NPC response

NPC response generation occurs only after deterministic rule resolution.

The LLM receives a bounded NPC Response Plan and generates surface language.

Canonical NPC decisions, clue release, deception, relationship changes, and state changes are deterministic.

### Headline analysis

Player-written headlines are represented through authored Claim Atoms rather than generic sentiment or misinformation scores.

Current proposed claim semantics include:

- authored claim target;
- authored value where required;
- polarity;
- claim posture;
- explicit source attribution where relevant.

Headline evaluation uses the evidence available to the player at publication time rather than treating canonical truth as the primary correctness score.

## Validation architecture

The current design separates three P0 AI responsibilities:

1. Dialogue Semantic Parser
2. Grounded NPC Response Generator
3. Headline Analyzer

Each AI component has narrow language authority and is separated from gameplay state by deterministic validation.

## Safety direction

Current hard safety candidates include:

- Unauthorized canonical state mutation = 0
- Invalid canonical ID accepted = 0
- Unauthorized NPC fact disclosure = 0
- LLM-generated state or branch decisions accepted = 0
- Semantically unresolved headline entering publication resolution = 0
- AI/system failure creating irreversible gameplay consequence = 0

## Next

Run the two parallel validation threads.

### 01A

Pressure-test:

- dialogue semantic schema;
- conditional field rules;
- threats, accusations, indirect probing and bluffing;
- ambiguity and unsupported input;
- grounded NPC response plans;
- NPC deception;
- information leakage and hallucination;
- dialogue evaluation cases.

### 01B

Pressure-test:

- headline Claim Atom model;
- multi-claim extraction;
- attribution and claim posture;
- evidence-support separation;
- headline atomic semantic resolution;
- neutral pre-publish warning behaviour;
- rhetorical edge cases;
- headline evaluation cases.

Cross-cutting contract changes must return to the master `01 | AI Interaction Contract` thread before becoming confirmed.

## Blocked / unresolved

- Detailed 20–30 minute vertical-slice story canon remains undefined.
- Final NPC roster remains undefined.
- Final faction and world canon remain undefined.
- Final Semantic Target Catalogue remains undefined.
- Final Evidence–Claim Relationship rules remain undefined.
- Exact rules and thresholds for Reputation, Public Opinion, Threat Level, and Money remain undefined.
- Acceptance thresholds for AI semantic accuracy remain undefined until a real model baseline exists.
- Backend/API architecture remains undecided.
- Dify implementation/integration remains unvalidated.
- Unity remains unimplemented.
- Generic rhetorical framing mechanics remain deferred unless validation demonstrates gameplay value.

## Current milestone success condition

Validation Increment 01 succeeds when:

- the semantic interpretation contract survives dialogue and headline pressure testing;
- deterministic authority boundaries are explicit and auditable;
- ambiguous and invalid AI output fails safely;
- the initial evaluation dataset can reproduce expected interpretations and failure cases;
- no structural contract issue remains that would require redesign during implementation.

Only after this should AI Interaction Contract v0.1 be frozen and implementation validation in Dify be considered.