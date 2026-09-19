# Between the Lines: AI Remake (BTL-AI)

A PC-first, 2D narrative journalism game: investigate, question NPCs in free text, write a headline, and face authored consequences.

**AI controls language. Deterministic game systems control reality.** The target is a polished **20–30 minute playable vertical slice**, not a full 14-day game or an unconstrained AI-generated plot.

## Current status — reviewed 2026-09-19

**04 / Technical Prototype 01 is in progress. No playable Remake demo yet.**

Completed: product scope, VI01/VI02 design validation, Gate 03, and the Experimental Python harness with scripted retry/fallback, measurement and a guarded OpenAI adapter. Latest implementation reviewed: `38703c4368ae774ebc36b6cbdc27cd61dd1a8c87` (Batch 2B.0.1).

Not evidenced as complete: real-model baseline, measured model quality/latency/cost, Dify feasibility, Unity integration or player testing. Historical test counts are not a fresh rerun.

**Active branch:** `prototype/technical-prototype-01`. **Stable historical baseline:** `main` (VI01 + VI02 + Gate 03). Do not mistake `main` for the latest implementation.

## Start here

- [Plain-Chinese game introduction and stage history](docs/00_PROJECT_OVERVIEW.md)
- [Current State: evidence, limits and next outcome](docs/06_CURRENT_STATE.md)
- [Handoff: resume work and reconcile local/Project copies](docs/07_HANDOFF.md)
- [Product Definition](docs/01_PROJECT_DEFINITION.md), [Decision Log](docs/05_DECISION_LOG.md), [Frozen Contract v0.1.1](docs/08_AI_INTERACTION_CONTRACT.md)

## Next useful outcome

Reconcile the local checkout, rerun offline tests, then prepare one **free-first** real-model baseline using the existing fixtures and runner. No free provider is yet selected or integrated. Paid execution stays **not authorised**; historical model/SDK/price settings need reverification before live use.

After measured evidence: one minimal playable investigation → conversation → evidence → headline → consequence loop. Dify is an optional post-baseline feasibility experiment. Unity creation still requires explicit authorisation.

## Repository map

`docs/` holds decisions and progress; `ai/` holds the Experimental harness, prompts, schemas and manifest; `tests/` holds fixtures and automated tests. `ai/dify/`, production `data/` and `tools/` are placeholders, not completed systems.

Git is canonical. GitHub edits do not automatically update the Windows checkout or ChatGPT Project Sources.
