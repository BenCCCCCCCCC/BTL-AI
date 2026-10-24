# Between the Lines: AI Remake (BTL-AI)

A PC-first, 2D narrative journalism game: investigate, question NPCs in free text, write a headline, and face authored consequences.

**AI controls language. Deterministic game systems control reality.** The target is a polished **20–30 minute playable vertical slice**.

## Current status — reviewed 2026-10-25

**04 / Technical Prototype 01 is in progress.** Product scope, VI01/VI02, Gate 03 and the Experimental Python components are implemented. A measured real-model baseline and playable Remake demo are not yet evidenced as complete.

Active branch: `prototype/technical-prototype-01`. Reviewed source: `e1e66556ae67aed32ef6e739bec4183d708c6b88`; latest implementation: `38703c4368ae774ebc36b6cbdc27cd61dd1a8c87`. `main` remains the historical design baseline. Historical test counts are not a fresh rerun.

## Start here

- [Plain-Chinese game introduction](docs/00_PROJECT_OVERVIEW.md)
- [Current State: progress, evidence and concrete gaps](docs/06_CURRENT_STATE.md)
- [Handoff: next increment, targeted verification and completion rules](docs/07_HANDOFF.md)
- [Working agreement](AGENTS.md), [Product Definition](docs/01_PROJECT_DEFINITION.md), [Decision Log](docs/05_DECISION_LOG.md), [Frozen Contract v0.1.1](docs/08_AI_INTERACTION_CONTRACT.md)

## Next useful outcome

Complete a thin manifest execution entry point, assemble model context correctly, and retain reviewable candidates with the existing runner and JSONL. Select one accessible **free-first** route and obtain a representative real-model sample under a defined execution authorisation.

The manifest currently contains **5 real-model and 13 offline fault-injection cases**. Reuse applicable results; compatible smoke results count toward the same batch. Follow the Handoff's change-based verification table instead of rerunning the whole suite on every resumption or documentation edit.

Use the findings to decide the next minimal investigation → conversation → evidence → headline → consequence loop. Dify is optional after a concrete orchestration need emerges; Unity creation and live calls retain their existing authorisation boundaries.

## Repository map

`docs/` holds decisions and progress; `ai/` holds Experimental components, prompts, schemas and the manifest; `tests/` holds fixtures and automated tests. Dify and production data/tool directories remain placeholders.

The active Git branch is canonical. Local checkouts and ChatGPT Project Sources are separate copies; refresh them at meaningful handoffs.
