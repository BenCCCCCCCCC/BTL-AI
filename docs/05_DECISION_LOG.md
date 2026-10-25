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

## DEC-017

**Status:** Confirmed

**Date:** 2026-08-28
**Decision:** Represent authored semantic meanings through a globally unique authored semantic registry that is deterministically projected into parser-specific Runtime Catalogue Views. Shared propositions reuse the same authored proposition IDs across relevant P0 interactions; dialogue-only REQUEST and DEAL meanings remain scoped to dialogue. Only currently exposed meanings are supplied to AI parsers, while evidence, sources, and Pending Interactions remain separate deterministic runtime registries/context.

**Rationale:** Validation Increment 02A demonstrated that one small authored reality can instantiate Dialogue, Grounded NPC Response, and Headline analysis without requiring the LLM to invent consequential gameplay meanings. Deterministic runtime projection keeps the language interface flexible while preserving a bounded, auditable gameplay space.

**Consequences:**

- Authored-but-unavailable meanings are omitted from the current Runtime Catalogue View.
- Completely nonexistent meanings have no authored registry entry.
- If an AI output returns an unavailable or nonexistent ID, deterministic validation rejects it; the ID cannot become gameplay reality.
- No new semantic status or Frozen semantic-output field is introduced by this catalogue architecture.
- Shared proposition IDs may support Dialogue, Headline Claim Atoms, deterministic NPC response content, and later Evidence–Claim relationship data.
- The 02A railyard-clash fixture remains Experimental / Validation-only / Non-canonical; acceptance of its architecture does not confirm its story content.
- Production serialization, exposure rules, and authoring tooling remain unresolved.

## DEC-018

**Status:** Confirmed

**Date:** 2026-08-29
**Decision:** Evaluate headline publication support through an authored deterministic Evidence–Claim Relationship layer operating on an immutable publication-time evidence/knowledge snapshot. Attribution support, underlying-proposition support, and canonical reality remain independent axes. Publication evaluations are auditable and versioned, and later evidence or later rule changes do not overwrite the original publication-time result.

**Rationale:** Validation Increment 02B demonstrated that the Frozen Claim Atom schema is sufficient for deterministic journalism evaluation without asking an LLM to judge evidence sufficiency, source reliability, or truth. A frozen snapshot preserves the player's actual information basis at the moment of publication.

**Consequences:**

- Evidence–Claim relationships are authored deterministic data, not Claim Atom fields or LLM output.
- Attribution relationships never automatically create underlying-proposition relationships.
- Evidence that exists in the world but was not known/content-accessible to the player is excluded from the original publication evaluation.
- Publication evaluation may use deterministic labels such as `SUPPORTED`, `CONTRADICTED`, and `INSUFFICIENT`; these are gameplay-evaluation results, not additions to the Frozen semantic status taxonomy.
- Conflicting evidence is resolved by authored deterministic commitment-mode rules rather than majority voting, model judgement, or hidden truth scores.
- The specific railyard Evidence–Claim rows and sufficiency examples remain validation-only, not final journalism content/policy.
- Persistence technology, serialization, authoring tooling, authenticity states, and attributed-paraphrase weakening policy remain unresolved.

## DEC-019

**Status:** Confirmed

**Date:** 2026-08-29
**Decision:** Ground P0 NPC responses through separated deterministic data layers: a small Static Character Card, Authored Knowledge Boundary, Authoritative Dynamic NPC State, Current Interaction State, relevant Canonical World Context, a Deterministic Response Plan, and a minimal Generator-only Language Context. NPC knowledge, disclosure permission, and required response content are separate concepts. The generator receives least-knowledge context and retains surface-language authority only.

**Rationale:** Validation Increment 02C demonstrated that all Frozen NPC response modes, deterministic deception, clue control, request/deal decisions, and fallback semantics can be supported without exposing the full world state or giving the LLM gameplay authority.

**Consequences:**

- Character Cards remain small and must not become world-bible, memory, or authoritative runtime-state dumps.
- Hidden canonical truth, locked clues, raw relationship values, rule thresholds, branch IDs, state deltas, and unrelated evidence should be omitted from generator context when unnecessary.
- `NPC knows X`, `NPC may reveal X`, and `NPC must say X now` are distinct deterministic states.
- Shared world propositions may reuse the globally unique `PROP_*` IDs in Response Plan content.
- The exact internal representation for non-world response obligations (for example refusal, clarification, counterquestion, acceptance wording) remains deferred serialization/schema detail and is not a Frozen Contract change at this checkpoint.
- NPC-originated authored-offer lifecycle remains unresolved. If a future vertical-slice requirement needs a new response mode or changed Response Plan authority semantics, it must return through the current Master process to Contract review before implementation.
- Final NPC roster, relationship formulas, richer epistemic distinctions, production serialization, P1 memory, and Output Validation Gate implementation remain unresolved.

## DEC-020

**Status:** Confirmed  
**Date:** 2026-08-29  
**Decision:** All changes to the four confirmed global variables — Reputation, Public Opinion, Threat Level, and Money — must originate from an authored deterministic Consequence Event created only after a deterministic gameplay result has been resolved. Validated AI semantic output, Claim Atoms, publication-support labels, and NPC surface text are not direct variable-change triggers. A result type may make a variable consequence eligible, but an authored deterministic rule must explicitly select the consequence; no implicit mapping or cross-variable formula is created by the AI layer.

**Rationale:** The four variables need a minimal testable interface before prototyping without coupling language interpretation, evidence evaluation, or NPC wording directly to game-state mutation. An explicit consequence layer preserves the core authority boundary and keeps future balancing auditable.

**Consequences:**

- The minimal flow is `Deterministically Resolved Gameplay Result → Authored Consequence Event → Deterministic Variable Effect → Authoritative State Update`.
- Publication outcomes may affect Reputation, Public Opinion, or Threat Level only when an authored consequence rule says so; Money requires an explicit economic consequence.
- NPC/interpersonal outcomes may affect Reputation or Public Opinion only when an authored public/professional consequence exists; Threat Level requires an authored exposure/protection/risk consequence; Money requires an authored transaction/cost/reward consequence.
- Authored story/external events may affect any global variable when explicitly authored.
- Evidence/clue acquisition, semantic resolution, Claim Atom extraction, publication-support labels, and generated NPC text have no automatic global-variable delta.
- Exact ranges, deltas, balance, decay, cross-variable formulas, and ending thresholds remain deferred. A technical prototype may use clearly marked Experimental placeholder deltas only to exercise the interface.
- Legacy BTL formulas and thresholds remain historical evidence rather than Remake rules unless separately revalidated.

## DEC-021

**Status:** Confirmed  
**Date:** 2026-08-29  
**Decision:** The first real-model P0 baseline will reuse the Frozen VI01/VI02 validation fixtures through a versioned baseline manifest and will test Dialogue Semantic Parsing, Headline Analysis, and Grounded NPC Surface Generation as separate model boundaries. Model outputs must pass deterministic validators/gates; the baseline must also include deliberate invalid-output/fault-injection cases, record first-pass and retry/fallback outcomes, and capture model/prompt version, calls, token usage, latency, and estimated cost. Numerical acceptance thresholds will be set only after the first measured baseline.

**Rationale:** The project already has stable expected semantics and hard safety constraints. The next useful evidence is empirical model performance against those fixtures, not another abstract schema round or premature production orchestration.

**Consequences:**

- `tests/01A_DIALOGUE_NPC_VALIDATION_FIXTURE.md`, `tests/01B_HEADLINE_VALIDATION_FIXTURE.md`, and the relevant model-facing cases from `tests/02A_*` / `tests/02C_*` become the source cases for the baseline manifest.
- `tests/02B_EVIDENCE_CLAIM_RULES_FIXTURE.md` remains a deterministic downstream regression oracle; the LLM is not asked to judge evidence sufficiency or canonical truth.
- Hard Safety Gates remain categorical correctness requirements and are not averaged into a quality score.
- Model-invalid output that is caught by the validator is a model/retry quality failure; invalid output that is accepted, displayed, or allowed to mutate reality is a Hard Safety Gate breach.
- Baseline blockers include a Hard Safety Gate breach, validators unable to reject invalid IDs/enums/incomplete Claim Sets, retry/fallback changing the deterministic decision, or a requirement to alter Frozen Contract semantics/P0 scope merely to make the model path work.
- Dify remains a planned prototyping/orchestration layer, not a production dependency. Dify feasibility should be measured after a direct baseline harness exists so model quality can be separated from orchestration overhead.
- No Unity implementation is authorised by this decision.

## DEC-022

**Status:** Confirmed
**Date:** 2026-08-30
**Decision:** Separate deterministic runtime contract validity from semantic fidelity/completeness assurance. Runtime validators enforce observable schema, enum, current-catalogue, context, compatibility, visibility, Pending Interaction, structured single-action, Claim Atom legality, and authority-boundary conditions. Fidelity of arbitrary natural-language interpretation — including tactic omission, consequential Claim Atom omission, and catalogue-valid but source-text-unsupported extra Claim Atoms — is measured against reproducible authored ground truth during baseline evaluation.

**Rationale:** Technical Prototype 01 demonstrated that a candidate-only deterministic validator cannot independently re-derive the complete meaning of arbitrary free text without a second authoritative model judge, a deterministic full-natural-language parser, or a changed input/schema boundary. None of those changes is authorised or required by this clarification. Explicitly separating the assurance responsibilities preserves both deterministic runtime authority and measurable parser-quality requirements.

**Consequences:**

- Runtime contract PASS and semantic fidelity PASS are separate results and MUST NOT be conflated.
- Authored fixture ground-truth comparison is evaluation-only and is not a production runtime validator or retry signal.
- Candidate-only runtime inability to prove arbitrary natural-language completeness is not itself a prototype blocker once the two assurance responsibilities are explicit and the mandatory baseline measures fidelity.
- Progress remains blocked if the mandatory baseline cannot detect gameplay-relevant tactic omission, consequential Claim Atom omission, or catalogue-valid extra Claim Atoms; if runtime PASS is reported as fidelity PASS; if a Frozen Hard Safety Gate is breached; or if the model path requires changes to shared schemas, AI/Response Plan authority, semantic statuses, hard gates, or P0 scope.
- Dialogue and Headline schemas, semantic statuses, the AI authority boundary, NPC Response Plan authority, P0 scope, and the eight existing Hard Safety Gates remain unchanged.

## DEC-023

**Status:** Confirmed for scripted-chapter design v1.0; scripted implementation delivered in 04, player validation pending.

**Date:** 2026-10-25

**Decision:** Following the user's request to adjudicate and finalise the first case, adopt [the railyard chapter design v1.0](planning/2026-10-25-sol/FIRST_CASE_AUTHOR_DRAFT.md) as the authoring baseline for the next scripted chapter. This is case-specific content and deterministic relationship/event data under DEC-017, DEC-018 and DEC-020, not a change to shared semantic schemas, AI authority or P0 scope.

**Rationale:** Each optional investigation must yield a distinct reportable result and a concrete human consequence. Publication responsibility must distinguish a recorded assertion, the underlying event, and a later clarification already available to the journalist. Reader attention alone does not establish public approval.

**Consequences:**

- Adopt three investigation slots, the 600/500 transaction, the two optional investigations and five evidence items. The manuscript fixes complete dialogue, exits, mappings and outcomes; values are a production baseline for this sample, not measured long-term balance.
- E1 supports the witness's recorded fire-order assertion, not the underlying order. E2 supports the depicted order in this case; E4 supports the witness's own limited view; E3 supports the payment record; E3+E5 support the recorded expense categories. This is not a universal ranking of video, testimony or paid material.
- Preserve historical attribution when E4 arrives. Publishing the old assertion while omitting the known clarification creates an authored editorial follow-up consequence; it does not rewrite what the witness originally said. Complete attributed clarification is a valid reporting outcome.
- Reuse the existing fire-order, funding, ledger request/deal, evidence/source and Pending IDs. Adopt three new case targets and two new evidence IDs as specified in the manuscript's section 15, with current-view restrictions. They are now registered in independently versioned chapter data; implementation evidence is recorded in 06/07. No new act, commitment mode, status or Frozen output field is introduced.
- Fix one professional follow-up event at Reputation +1 or one editorial review event at -1; pressure events remain separate, once per actor, and the ledger purchase costs 500 once. Reader calls and company correspondence do not increase Public Opinion; it stays at zero for this sample. No implicit evidence-label-to-variable rule is authorised.
- Keep old fixtures, oracle rows, historical publication snapshots and measured baseline results unchanged. Implement the new chapter with distinct versioned authoring data; never silently replace the old experimental evidence policy.
- The manuscript defines this sample's authored reality only. Python remains Experimental, Unity remains the planned authoritative owner, and Frozen v0.1.1 / all eight Hard Safety Gates remain unchanged. This design checkpoint authorises no model calls, spending, Unity creation or runtime work.


## DEC-024

**Status:** Confirmed production direction and presentation design; implementation not authorised by this documentation request.

**Date:** 2026-10-25

**Decision:** Adopt Unity 2D with static pixel-art scenes and clear text UI for the first offline Unity release. Use the [production plan](planning/2026-10-25-sol/UNITY_2D_PRODUCTION_PLAN.md) to migrate the existing scripted chapter in U0–U5 order. The next proposed Sol batch is U0–U2 only, after an explicit instruction to create and implement Unity. Reorder I5 offline work ahead of deferred Python saves/memory and online integration; retain all original task IDs and unmet acceptance criteria.

**Rationale:** The chapter already contains authored branches, evidence relationships, publication rules and consequences. Reusing these semantics and data while rebuilding a small, shared UI avoids simultaneous engine migration, rule redesign and model integration. A bounded dramatic presentation and current-run recap can make choices legible without expanding the case into a cinematic campaign.

**Consequences:**

- Plan one Unity scene, UI Toolkit, three static backgrounds and three base portraits. Core C# state owns rules; presentation submits commands. This is an implementation choice within the existing authority boundary, not a shared schema/P0 change.
- Keep chapter.v1.0 and its four versions unchanged during equivalence migration. Import a traceable data copy; port Python logic rather than embedding Python. Old fixtures and measured evidence stay intact.
- Adopt [author manuscript section17](planning/2026-10-25-sol/FIRST_CASE_AUTHOR_DRAFT.md#chapter-presentation) as planned presentation v1.1: task, personal stakes, investigation tension, last-slot decision, publication/withholding, concrete responses and current-run recap. It adds no evidence, semantic target, numerical rule or automatic consequence. Runtime presentation data is not yet created.
- Static pixel art does not require pixelated Chinese text, character movement, QTEs or costly animation. Use original placeholders first; preserve reading, focus and input requirements.
- Saves, cross-run unlocks, second cases and online language services remain deferred. The scripted milestone does not satisfy arbitrary-language P0 or player validation.
- This checkpoint changes documentation only. No Unity creation, code changes, installations, live calls, spending or messages to another chat are authorised. The plan contains a future user-sendable implementation instruction, not an active delegation.
