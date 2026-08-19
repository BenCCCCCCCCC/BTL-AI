# Current State

## Current phase

Pre-production — Validation Increment 01 complete; AI Interaction Contract v0.1 frozen.

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
- 01A Dialogue & Grounded NPC Response specialist validation and targeted regression completed (`659be28db16bea586136ac00a053f1f01452df96`).
- 01B Headline Analysis specialist validation and targeted regression completed (`477086429c6beee7fae4da439383708803cf16f4`).
- Master decisions reconciled into the frozen AI Interaction Contract v0.1.

## In progress

Final Contract reconciliation / freeze is complete. Validation Increment 01 is complete; the specialist threads are paused unless a narrowly scoped regression is requested. No runtime implementation work is authorised by this status.

## Frozen contract direction

### Dialogue

The frozen semantic interpretation contains only gameplay-relevant information:

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

NPC response generation occurs only after deterministic rule resolution.

The deterministic pipeline is Response Plan → LLM Surface Candidate → NPC Output Validation Gate → Display; failed candidates retry once, then use a semantically faithful deterministic/template fallback.

Canonical NPC decisions, clue release, deception, relationship changes, and state changes are deterministic.

### Headline analysis

Player-written headlines are represented through authored Claim Atoms rather than generic sentiment or misinformation scores.

Frozen Claim Atom semantics include:

- authored claim target;
- authored value where required;
- polarity;
- commitment mode plus optional source attribution;
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
- Unauthorized NPC action / commitment expressed = 0
- Response-plan-invalid NPC output displayed = 0
- LLM-generated state or branch decisions accepted = 0
- Semantically unresolved headline entering publication resolution = 0
- AI/system failure creating irreversible gameplay consequence = 0

## Next

Keep the frozen contract and its validation fixtures as the baseline. Any subsequent work must be a separately authorised, narrowly scoped regression or later design increment; Dify, Unity, backend runtime, prompts, and gameplay implementation remain out of scope.

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

Validation Increment 01 succeeded because:

- the semantic interpretation contract survives dialogue and headline pressure testing;
- deterministic authority boundaries are explicit and auditable;
- ambiguous and invalid AI output fails safely;
- the initial evaluation dataset can reproduce expected interpretations and failure cases;
- no structural contract issue remains that would require redesign during implementation.

The contract is frozen. A future, separately approved implementation-validation increment may consider Dify only after its design and integration are validated; no such work is currently authorised.


## Active repository branch

Current stable branch:

`main`

Validation Increment 01 was completed on:

`design/validation-increment-01`

and has now been integrated into `main`.

`main` is the current stable validated project baseline.

Future substantial work should begin on a new branch appropriate to the next authorised increment rather than continuing implementation directly on the completed Validation Increment 01 branch.