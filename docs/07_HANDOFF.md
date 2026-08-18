# Handoff

## Project identity

**Between the Lines: AI Remake (BTL-AI)** is a pre-production, PC-first 2D narrative/interface-driven journalism game. Its first deliverable is a polished 20–30 minute AI-assisted vertical slice, not the full legacy 14-day experience.

## Current milestone

Validation Increment 01 — AI Interaction Contract. The repository baseline is committed to `main` and backed up to a private GitHub repository. No Unity project or runtime AI integration exists yet.

## Important architecture rules

- AI controls language; deterministic game systems control reality.
- Unity will own authoritative game state and rule evaluation.
- LLM output must never directly modify canonical state.
- NPC language must be grounded by character cards, knowledge boundaries, world canon, and dynamic state.
- Narrative structure remains authored and branching.

## What has been completed

- Initial repository structure created.
- Project definition, decision log, current-state note, and working agreement recorded.
- Repository baseline committed to `main` and published to a private GitHub repository.
- Confirmed priorities captured: P0 semantic dialogue parsing, grounded NPC dialogue, and AI headline analysis; P1 memory/contradiction/QA/evaluation; P2 world reactions/voice.

## Immediate next task

Define the semantic parser input/output contract and deterministic authority boundary before implementing Dify or Unity.

## Files to read

1. `README.md`
2. `AGENTS.md`
3. `docs/01_PROJECT_DEFINITION.md`
4. `docs/05_DECISION_LOG.md`
5. `docs/06_CURRENT_STATE.md`

## Known unresolved questions

- What backend/API architecture should connect future game systems and AI orchestration?
- How will Dify be validated and integrated, if retained?
- What exact deterministic rules govern the four global variables and narrative outcomes?
- What is the detailed 20–30 minute story slice, NPC set, data schema, and UI flow?


## Working protocol

All project threads must follow the Operational Routing, Documentation Checkpoint, Project Sources Sync, and Conversation Management rules defined in the current Project Instructions.

At major checkpoints, the active thread must explicitly tell the user which repository files and Project Sources require updating before work moves to another thread or implementation environment.

## Active repository branch

`design/validation-increment-01`

Future project threads must check this branch for the newest Validation Increment 01 documents. Do not assume `main` contains the latest working state.

## Master escalation rules

Specialist validation threads must return an issue to
`01 | AI Interaction Contract — Validation Increment 01`
before confirmation when the proposed change affects:

- shared semantic status or resolution reasons;
- shared Semantic Schema concepts;
- AI Authority Boundary;
- shared Failure / Fallback behaviour;
- cross-system evidence semantics;
- P0 feature scope;
- confirmed headline evaluation philosophy;
- canonical game/system design;
- assumptions used by both 01A and 01B;
- any change that materially rewrites `08_AI_INTERACTION_CONTRACT.md`.

Specialist threads may continue unrelated validation work while the escalated issue remains unresolved.

Local test-fixture changes, evaluation-case additions, wording refinements, and specialist-only non-authoritative proposals do not require immediate Master escalation.

# Specialist Thread Completion & Return Protocol

## Purpose

This protocol defines when the Validation Increment 01 specialist threads are considered complete enough to return to the Master thread.

Specialist completion means:

**Ready for Master Review**

It does not mean that AI Interaction Contract v0.1 is frozen or that Dify / Unity implementation may begin.

Only the Master thread may determine whether Validation Increment 01 is ready to freeze.

---

## Thread Status Vocabulary

Each specialist thread must use one of the following statuses when reporting progress:

### CONTINUE VALIDATION

The specialist scope still contains important untested cases, unresolved local design questions, or incomplete evaluation fixtures.

The thread should continue working.

### BLOCKED ON MASTER DECISION

Further progress on a specific issue requires a shared Contract decision.

The issue must be returned to:

`01 | AI Interaction Contract — Validation Increment 01`

The specialist thread may continue unrelated work while the shared decision is pending.

### READY FOR MASTER REVIEW

The first specialist pressure-test pass is complete.

The thread must explicitly tell the user that it is ready to return findings to the Master thread and provide the required Return Packet.

This does not independently confirm shared Contract changes.

---

## 01A Completion Criteria

`01A | Dialogue & Grounded NPC Response Validation` is Ready for Master Review when all of the following have been completed sufficiently for a first contract-level validation pass:

- Dialogue semantic fields and conditional rules have been pressure-tested.
- A reproducible non-canonical Dialogue Validation Fixture exists.
- Representative expected semantic outputs exist for:
  - QUESTION
  - ASSERTION
  - REQUEST
  - OFFER
  - ACCEPT
  - REFUSE
  - negation
  - threat
  - accusation
  - indirect probing
  - multiple tactics
  - bluffing
  - evidence references
  - ambiguous references
  - unsupported input
  - compound input
  - prompt injection
  - malformed structured output.
- The one-consequential-action-per-turn proposal has been pressure-tested.
- Dialogue Validator Rules are sufficiently specified to identify invalid semantic candidates.
- NPC Response Plan modes have been pressure-tested, including:
  - ANSWER
  - PARTIAL_ANSWER
  - EVADE
  - REFUSE
  - CLARIFY
  - COUNTERQUESTION
  - DECEIVE
  - ACCEPT
  - REJECT.
- NPC tests cover:
  - required proposition coverage
  - forbidden fact leakage
  - partial disclosure
  - deterministic deception
  - knowledge boundaries
  - hallucinated canon
  - prompt injection
  - response-plan non-compliance.
- Semantic Failure, AI/System Failure, and Valid Risky Gameplay remain clearly separated.
- Hard Safety Gates and Quality Metrics have been proposed.
- All shared-contract implications have been explicitly identified as `Return to 01 Master`.
- No unresolved 01A-local issue prevents Master review.

01A does not need a production prompt, Dify workflow, Unity implementation, final NPC roster, or final story canon before it may become Ready for Master Review.

---

## 01B Completion Criteria

`01B | Headline Analysis Validation` is Ready for Master Review when all of the following have been completed sufficiently for a first contract-level validation pass:

- Claim Atom has been pressure-tested as the minimum semantic unit.
- A reproducible non-canonical Headline / Evidence Validation Fixture exists.
- Representative expected outputs exist for:
  - single claims
  - multiple claims
  - FACT_ASSERTION
  - ATTRIBUTED_CLAIM
  - SPECULATION
  - QUESTION
  - attribution
  - source attribution
  - polarity / negation
  - unsupported entities
  - prompt injection
  - malformed structured output.
- Claim omission cases have been tested.
- Atomic headline resolution has been explicitly pressure-tested.
- Evidence-supported, evidence-insufficient, evidence-contradicted, canonically-true-but-unsupported, and apparently-supported-but-later-false cases remain conceptually distinct.
- Evidence sufficiency remains outside LLM authority.
- Neutral pre-publish warning categories have been pressure-tested without revealing hidden evidence verdicts or canonical truth.
- Rhetorical wording cases have been tested sufficiently to recommend either:
  - keeping rhetorical framing deferred; or
  - returning a justified framing-field proposal to Master.
- Hard Safety Gates and Quality Metrics have been proposed.
- All shared-contract implications have been explicitly identified as `Return to 01 Master`.
- No unresolved 01B-local issue prevents Master review.

01B does not need production prompts, final gameplay consequence formulas, Dify implementation, Unity implementation, or final story canon before it may become Ready for Master Review.

---

## Required Return Packet

When a specialist thread reaches `READY FOR MASTER REVIEW`, it must explicitly tell the user to return to the Master thread.

It must produce a Return Packet containing:

**Thread:** 01A or 01B  
**Status:** READY FOR MASTER REVIEW

### Scope completed

What was actually pressure-tested.

### Findings

What survived testing and appears sound.

### Proposed specialist-local changes

Changes that remain within the specialist thread's authority.

### Return to 01 Master

Every proposed change affecting shared Contract assumptions, including the exact reason Master review is required.

### Rejected / unnecessary ideas

Fields, mechanisms, or approaches considered but not justified by gameplay value.

### Remaining unresolved issues

Items that can safely remain deferred.

### Validation assets produced

Fixtures, test categories, expected outputs, metrics, and other reproducible validation material.

### Repository update recommendation

Which files should be created or updated.

### Project Sources refresh recommendation

Which Project Sources need replacement, if any.

### Git checkpoint recommendation

Whether a commit is appropriate and the recommended scope.

### Next routing recommendation

State the recommended next environment:

- Chat
- Work
- Codex

If recommending a mode switch, also state the recommended model and reasoning level.

---

## Master Integration Rule

The Master thread may consider Validation Increment 01 ready to freeze only after:

1. both 01A and 01B are `READY FOR MASTER REVIEW`;
2. both Return Packets have been reviewed;
3. all shared Contract escalations have been resolved or explicitly deferred;
4. `08_AI_INTERACTION_CONTRACT.md` has been reconciled with accepted findings;
5. new Confirmed decisions, if any, have been recorded in Decision Log;
6. Current State and Handoff accurately describe the post-validation state;
7. the Master confirms that no known structural contract issue would require implementation-time redesign.

Only after this review may the Master change AI Interaction Contract v0.1 from:

`Draft — Freeze Candidate`

to:

`Frozen`

and consider authorising the next validation / implementation stage.