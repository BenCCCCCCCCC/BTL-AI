# Decision Log

Only confirmed decisions belong here. Unresolved choices are recorded in `06_CURRENT_STATE.md` and `07_HANDOFF.md`, not converted into decisions.

## DEC-001

**Status:** Confirmed  
**Date:** 2026-08-15  
**Decision:** Set the game in a fictional modern country, allowing inspiration from and satire of real-world politics and media.  
**Rationale:** Preserves the desired political and media themes while keeping the setting distinct.  
**Consequences:** Detailed world canon, factions, and story content require future authored definition.

## DEC-002

**Status:** Confirmed  
**Date:** 2026-08-15  
**Decision:** Target PC first with a 2D, narrative/interface-driven presentation.  
**Rationale:** Focuses the initial product and supports journalism-oriented interaction.  
**Consequences:** Early design and validation should prioritise desktop UI and keyboard use.

## DEC-003

**Status:** Confirmed  
**Date:** 2026-08-15  
**Decision:** Use keyboard free-text interaction as the primary input mode.  
**Rationale:** Supports expressive player dialogue and semantic parsing.  
**Consequences:** Input handling, interpretation, and fallback UX need validation during prototyping.

## DEC-004

**Status:** Confirmed  
**Date:** 2026-08-15  
**Decision:** Use authored branching narrative rather than a fully AI-generated plot.  
**Rationale:** Retains narrative intention, scope control, and testable consequences.  
**Consequences:** AI assists language and selected interpretation, while content structure remains authored.

## DEC-005

**Status:** Confirmed  
**Date:** 2026-08-15  
**Decision:** Retain the legacy global variables: Reputation, Public Opinion, Threat Level, and Money.  
**Rationale:** These remain confirmed pillars of the game-system direction.  
**Consequences:** Their rules and thresholds must be explicitly designed before implementation.

## DEC-006

**Status:** Confirmed  
**Date:** 2026-08-15  
**Decision:** Ground AI NPC dialogue using character cards, knowledge boundaries, world canon, and dynamic state.  
**Rationale:** Constrains NPC language to the authored world and current game context.  
**Consequences:** Character-card and state schemas need future definition and validation.

## DEC-007

**Status:** Confirmed  
**Date:** 2026-08-15  
**Decision:** AI controls language; deterministic game systems control reality. Unity owns authoritative game state and rule evaluation, and LLM output cannot directly modify canonical state.  
**Rationale:** Maintains reliable, testable, and auditable game consequences.  
**Consequences:** AI integrations require a deterministic validation/translation boundary before state changes.

## DEC-008

**Status:** Confirmed  
**Date:** 2026-08-15  
**Decision:** Prioritise P0 AI features: semantic parsing of player dialogue, grounded AI NPC dialogue, and AI headline analysis.  
**Rationale:** These features best demonstrate the intended AI-assisted experience in the vertical slice.  
**Consequences:** P1 and P2 features remain out of initial-slice scope unless explicitly re-prioritised.

## DEC-009

**Status:** Confirmed  
**Date:** 2026-08-15  
**Decision:** Plan Dify as an AI orchestration/prototyping layer, pending validation.  
**Rationale:** It is the current intended experimentation layer, not yet a locked implementation dependency.  
**Consequences:** No Dify runtime work should begin until its integration approach is validated.

## DEC-010

**Status:** Confirmed  
**Date:** 2026-08-15  
**Decision:** Limit the initial product target to a polished 20–30 minute vertical slice rather than the full 14-day content.  
**Rationale:** Keeps the project focused on proving its core design and AI orchestration goals.  
**Consequences:** Scope decisions must be evaluated against vertical-slice value and polish.

## DEC-011

**Status:** Confirmed  
**Date:** 2026-08-18  
**Decision:** Evaluate player-written headlines primarily through an evidence-based journalism model rather than an omniscient truth-based model. Publication evaluation considers whether a claim was sufficiently supported by the evidence and information available to the player at publication time, separately from whether the claim is canonically true.

**Rationale:** The player is acting as a journalist under uncertainty rather than solving a hidden-answer quiz. This makes investigation, evidence gathering, attribution, and publication responsibility part of the same gameplay loop.

**Consequences:**  
- Canonical truth and journalistic evidence support are separate concepts.
- A claim may be canonically true but insufficiently supported when published.
- A claim may be reasonably supported when published but later proven factually wrong.
- The LLM does not determine evidence sufficiency or canonical truth.
- Evidence support evaluation must remain deterministic.


## DEC-012

**Status:** Confirmed  
**Date:** 2026-08-18  
**Decision:** Use neutral, behaviour-based pre-publication warnings for high-risk headlines rather than explicitly revealing hidden evidence-support judgments. Players retain the option to edit the headline or publish anyway.

**Rationale:** Players should understand when they are making a strong journalistic claim without turning the interface into an automatic correctness checker or revealing hidden information.

**Consequences:**  
- Warnings describe the nature of the player's language, such as making a direct allegation or presenting responsibility as fact.
- Warnings must not state that the player's evidence is sufficient or insufficient.
- Warnings must not reveal canonical truth.
- Valid risky reporting remains an intentional gameplay choice.
- Publication may proceed after the warning if the player chooses Publish Anyway.

## DEC-013

**Status:** Confirmed

**Date:** 2026-08-18
**Decision:** Dialogue v0.1 distinguishes unilateral `REQUEST` from an authored bilateral `OFFER`. A counteroffer is an `OFFER` only when it maps to an available authored deal target; richer free-form negotiation remains deferred. `tactics[]` is an order-insensitive unique set with no arbitrary fixed maximum, and every gameplay-relevant tactic must be retained for validation.

**Rationale:** This preserves a small deterministic action space without silently changing the player's intended deal or tactic meaning.

**Consequences:**

- Unsupported free-form deals and counteroffers fail safely rather than creating new game terms.
- Dialogue still permits one consequential action per turn; supporting tactics do not create a second action.
- A duplicate tactic or omission/truncation of a gameplay-relevant tactic is invalid semantic output.

## DEC-014

**Status:** Confirmed

**Date:** 2026-08-18
**Decision:** Grounded NPC output follows `Deterministic NPC Response Plan → LLM Surface Candidate → NPC Output Validation Gate → Display`. The Response Plan separates required propositions, permitted context, and forbidden propositions. Failed validation retries once, revalidates, then uses a semantically faithful deterministic/template fallback. `DECEIVE` is not a response mode: deception is a deterministic content/narrative decision orthogonal to response mode.

**Rationale:** Deterministic rules must control NPC commitments and consequential disclosure, while the LLM only renders authorised language.

**Consequences:**

- Gameplay-relevant optional clue disclosure must be explicitly authorised in the Response Plan, never selected by the LLM from permitted context.
- Parser-level Semantic Clarification remains separate from a resolved-action NPC `CLARIFY` response mode.
- `Unauthorized NPC action / commitment expressed = 0` and `Response-plan-invalid NPC output displayed = 0` are hard safety gates.

## DEC-015

**Status:** Confirmed

**Date:** 2026-08-18
**Decision:** A headline Claim Set contains all consequential claims with no fixed count limit or silent truncation. `RESOLVED + claims=[]` is valid when the headline contains neither a consequential proposition nor unresolved consequential content. Each Claim Atom uses `commitment_mode` (`ASSERTED`, `SPECULATIVE`, or `QUESTIONED`) plus optional, orthogonal `source_ref_id`; consequential presuppositions produce atoms and use `ASSERTED` in v0.1 unless a further gameplay distinction is needed.

**Rationale:** Claim count, commitment, attribution, polarity, and presupposition are independent semantic concerns that must remain available for deterministic evaluation.

**Consequences:**

- Atomic resolution remains: unresolved consequential content blocks the complete headline from publication resolution.
- Claim omission, extra claims, and claim-count-based truncation are safety defects.
- Generic rhetorical framing, sentiment, bias, propaganda, and misinformation scores remain deferred.

## DEC-016

**Status:** Confirmed

**Date:** 2026-08-18
**Decision:** Headline evaluation keeps attribution support, underlying-proposition support, and canonical reality as separate deterministic concepts. Publication responsibility uses an auditable evidence/knowledge basis at publication time and is not retroactively rewritten by later evidence. Retry-exhausted headline parser failure may present only a non-consequential UX fallback; it must not fabricate a Claim Set or enter publication resolution.

**Rationale:** The game evaluates responsible journalism under the information available when the player publishes, while preserving deterministic and auditable authority boundaries.

**Consequences:**

- Evidence-based journalism and neutral behaviour-based pre-publish warnings remain confirmed.
- The LLM does not determine evidence sufficiency, attribution support, or canonical truth.
- A semantic fallback is forbidden for retry-exhausted headline parsing; a preserved draft and edit/retry UX is allowed.
