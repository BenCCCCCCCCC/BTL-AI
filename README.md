# Between the Lines: AI Remake (BTL-AI)

A PC-first, 2D narrative journalism game: investigate, question NPCs in free text, write a headline, and face authored consequences.

**AI controls language. Deterministic game systems control reality.** The target is a polished **20–30 minute playable vertical slice**.

## Current status — 2026-10-26

**Unity U5a experience build 0.4.0 is delivered locally:** [Play and rebuild](unity/README.md). Character stakes now carry from first meetings to publication aftermath; the final investigation slot shows the actual opportunity cost. Full scripted expression cards, complete intent review, concrete character scenes and a shorter reading flow connect to the current-run recap. Independent chapter1.1/presentation1.2 preserve the old content and deterministic evidence rules. [Actual checks and screenshots](docs/planning/2026-10-25-sol/verification/u5a/README.md) distinguish the full native route from final focused UI inspection. No model calls or unrelated historical suites were added.

The Windows package is `Builds/BTL-Internal-0.4.0-Windows.zip`; 0.3.0 remains available locally. U5b first-reader observation is pending; use the [reader notes](docs/planning/2026-10-25-sol/FIRST_READER_NOTES.md). The [GitHub repository](https://github.com/BenCCCCCCCCC/BTL-AI) is **public**. The complete 0.4.0 source delivery was committed and pushed to `prototype/technical-prototype-01` on 2026-10-26; see [handoff](docs/07_HANDOFF.md) for the sync scope. Windows packages remain local and are not included in Git.

**Unity U3–U4 internal playtest 0.3.0 is available:** [Unity project and Windows launch instructions](unity/README.md) connect the complete first case, both main investigations and follow-ups, Chinese interview confirmation, five evidence items, 12 authored headlines, publication/withholding, character consequences and a current-run recap. Three original pixel scenes, three portraits and a licensed Chinese font ship in `Builds/BTL-Internal-Windows/`. A standalone B→S-B→H10 route was played through publication, recap and restart; new presentation checks passed. No new model calls or unrelated historical suites were run. See [current state](docs/06_CURRENT_STATE.md) and [handoff](docs/07_HANDOFF.md).

The [Unity 2D production plan](docs/planning/2026-10-25-sol/UNITY_2D_PRODUCTION_PLAN.md) records U5a as delivered and U5b first-reader observation pending. Current authoring uses [manuscript section18](docs/planning/2026-10-25-sol/FIRST_CASE_AUTHOR_DRAFT.md), chapter1.1 and presentation1.2; previous content remains in place. Play length, enjoyment, IME composition and other PCs remain unmeasured; there are no saves or live language services.

**04 / Technical Prototype 01 is in progress.** D18 now passes runtime and semantic fidelity with all three tactics: one request in the third authorised batch. The three batches used **12 real requests total (8 + 3 + 1)** and are closed. This is small-sample evidence, not general language reliability.

A **scripted playable first chapter v1.0** now connects the existing original utterance → system understanding → confirm/rewrite → execute flow to three investigation slots, two main investigations, two optional follow-ups, five complete evidence items, 12 authored headlines, explicit publication/withholding and concrete character/editorial consequences. Authored examples are matched exactly; other edits are preserved without guessing. There are no model requests or saves.

Current Unity authoring uses [chapter1.1](ai/content/railyard_chapter.v1.1.json) and [presentation1.2](ai/content/railyard_presentation.v1.2.json). The [prior chapter](ai/content/railyard_chapter.v1.0.json), [old fixture](tests/fixtures/railyard_story.experimental.v0.1.json) and their rules are retained. Python remains Experimental; Unity owns its runtime state and Frozen v0.1.1 is unchanged.

Active branch: `prototype/technical-prototype-01`. Source delivery commit: [`4cddf5f`](https://github.com/BenCCCCCCCCC/BTL-AI/commit/4cddf5fb1fbd6bc8b89b33d39b6d5d4156038e35); subsequent documentation records the sync receipt. No pull or main-branch merge was performed.

## Play the local story

From `F:\BTL-AI` in PowerShell:

```powershell
& .\tools\play_story.ps1
# Equivalent direct entry
& .\.venv\Scripts\python.exe -m ai.prototype.chapter_desktop
```

Load an interview example, edit the original, click **查看系统理解**, then return to rewrite or explicitly confirm. Reading, rewriting and evidence browsing are free. Each completed or explicitly terminated investigation uses one slot; the ledger costs 500 only after accepting the pending transaction. At the editor, selecting a title fills the draft; review every claim and confirm publication separately. Withholding also has its own confirmation.

Enter inserts a newline in text inputs; Tab leaves them. Ctrl+E opens evidence and preserves the draft/page position; single E and number shortcuts do not execute actions while typing. The ending offers publication-time materials, an event ledger and restart. Closing does not save.

Use `& .\tools\play_story.ps1 -Legacy` or `-m ai.prototype.story_desktop` for the previous one-investigation prototype. Its terminal entry remains `-m ai.prototype.story_fixture`. The unchanged scripted/model baselines are historical evidence and do not need rerunning.

## Read the next development plan

- [First-case chapter design v1.0](docs/planning/2026-10-25-sol/FIRST_CASE_AUTHOR_DRAFT.md): dialogue, actions, five readable evidence items, costs, failure/exit paths and concrete publication consequences.
- [Main plan and case structure](docs/planning/2026-10-25-sol/ITERATION_PLAN.md#full-case): progress within the existing six-iteration plan. The old implementation prompt is retained for history only.
- [Local design board](docs/planning/2026-10-25-sol/design-board.html): earlier screen/flow proposals and separate actual window screenshots. It has not been updated to depict the new case structure. Open the HTML locally; no account or publishing is required.
- [Delivery index and actual verification](docs/planning/2026-10-25-sol/README.md).

The chapter implements [design v1.0](docs/planning/2026-10-25-sol/FIRST_CASE_AUTHOR_DRAFT.md) / [DEC-023](docs/05_DECISION_LOG.md#dec-023) with separate content/catalogue/support/consequence versions. It distinguishes recorded attribution, underlying evidence and a known later clarification. Publication snapshots freeze the actual material text and all claims; reader calls do not increase Public Opinion.

Historical scripted-chapter incremental verification: **26 distinct tests passed** — 16 new chapter-rule tests, 2 new Tk integration/regression tests, and the 8 existing interview tests affected by the shared flow hooks. One native-window funding/follow-up/publication route and the default launcher were checked. The native check found a missing offer acknowledgement and long pages jumping to Continue; both were corrected with a focused Tk regression. No unrelated old story/model cases were rerun.

Next is U5b first-reader observation and a separate scoped source sync. The 20–30 minute target, enjoyment, arbitrary Chinese interpretation and IME/accessibility remain unvalidated. Live calls and spending still require separate authorisation.

## Project entry points

- [Game introduction](docs/00_PROJECT_OVERVIEW.md)
- [Current State: implementation, three model batches, evidence and limits](docs/06_CURRENT_STATE.md)
- [Handoff: commands, verification policy and continuation](docs/07_HANDOFF.md)
- [Working agreement](AGENTS.md), [Product Definition](docs/01_PROJECT_DEFINITION.md), [Decision Log](docs/05_DECISION_LOG.md), [Frozen Contract v0.1.1](docs/08_AI_INTERACTION_CONTRACT.md)
- [Original model records and matching sources](ai/eval/evidence/)

The three model batches still total 12 requests; no new model-quality evidence is claimed. U5a evidence includes compilation, focused C# checks, a native Windows A+B+S-A/H11 route and final focused reading inspection. Historical Python cases were not rerun; no player study occurred. Project Sources have not been refreshed. See the Handoff for limits and copy lists.
