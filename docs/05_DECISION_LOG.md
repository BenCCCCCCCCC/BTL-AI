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
