# Project Definition v0.1

**Status:** Authoritative for confirmed product direction.  
**Scope:** Pre-production baseline for the initial vertical slice.

## Vision

Create a polished, AI-assisted narrative journalism game that combines authored branching drama with free-text player interaction. The game is set in a fictional modern country, allowing inspiration from and satire of real-world politics and media while retaining a distinct fictional world.

## Target experience

- PC-first, 2D, narrative/interface-driven presentation.
- Keyboard free-text interaction is the primary input mode.
- Players experience a focused 20–30 minute vertical slice.
- AI makes dialogue interactions feel responsive while authored systems preserve narrative intention and consequence.

## Core loop

1. Investigate through interface-driven journalism actions and conversations.
2. Use free text to question or respond to NPCs.
3. Interpret information, including AI-assisted headline analysis.
4. Make authored narrative choices.
5. Resolve deterministic consequences in the game state.

The first railyard case now has a versioned authored design and an Experimental scripted implementation under DEC-023. Later cases and the full day-by-day structure remain to be authored. The Unity presentation plan adds authored dramatic beats and a current-run recap without changing the existing case rules.

## Vertical slice scope

The slice will prove the central investigative/narrative loop and the priority-zero AI features. It is deliberately bounded to 20–30 minutes and excludes building the full 14-day game.

## Global variables

The legacy variables remain part of the product direction:

- Reputation
- Public Opinion
- Threat Level
- Money

Their exact formulas, thresholds, and content consequences are not yet defined.

## NPC state

NPCs will be grounded using dynamic state alongside authored world constraints. At minimum, the design direction includes character cards, knowledge boundaries, world canon, and relevant dynamic game state. The exact state schema remains to be defined.

## NPC card concept

Each NPC will have an authored character card that gives the language model bounded context. Cards are intended to define identity, voice, knowledge boundaries, relevant world canon, and state-aware constraints. Detailed characters and card schema are intentionally not yet authored.

## AI boundaries

- AI controls language, not reality.
- Deterministic game systems control reality.
- Unity owns authoritative game state and rule evaluation.
- LLM output is non-authoritative and must never directly alter canonical game state.
- The plot remains authored and branching; it is not fully AI-generated.

## AI feature roadmap

| Priority | Confirmed direction |
| --- | --- |
| P0 | Semantic parsing of player dialogue; grounded AI NPC dialogue; AI headline analysis. |
| P1 | NPC memory; evidence/contradiction detection; narrative QA; AI evaluation. |
| P2 | Dynamic world reactions; voice interaction. |

## Headline mechanic

AI headline analysis is a P0 feature. It supports the player’s interpretation of headlines; its exact interface, prompts, inputs, and deterministic gameplay consequences remain to be validated.

## Technology direction

- Unity is planned as the game client and authoritative owner of state/rules.
- The first Unity release uses static pixel-art scenes with clear, high-resolution Chinese text and interface-driven choices, following [DEC-024](05_DECISION_LOG.md#dec-024) and the [production plan](planning/2026-10-25-sol/UNITY_2D_PRODUCTION_PLAN.md). It is an offline scripted milestone; arbitrary-text AI/P0 goals remain later work, not completed or removed.
- The first migration uses one scene and reusable UI, preserving the existing case data and deterministic policies. Multi-protagonist cinematics, free movement, QTEs and a full campaign are outside that release.
- Dify is planned as an AI orchestration and prototyping layer.
- Dify implementation and integration have not yet been validated.
- Backend/API architecture remains undecided.
- A Unity project must not be created until explicitly authorised.

## Success criteria

- A polished 20–30 minute playable vertical slice demonstrates the intended narrative journalism loop.
- The slice clearly demonstrates game/system design and AI product/orchestration ability.
- P0 AI interactions are useful, grounded, and constrained by deterministic state.
- Canonical game state remains deterministic and auditable.
- The slice uses authored branching narrative rather than an unconstrained generated plot.
