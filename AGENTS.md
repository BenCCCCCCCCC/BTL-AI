# Working Agreement

## Before significant changes

Read `README.md`, `docs/01_PROJECT_DEFINITION.md`, `docs/05_DECISION_LOG.md`, and `docs/06_CURRENT_STATE.md`. Read `docs/07_HANDOFF.md` when taking over from another environment/tool.

Check the actual repository root, remote, branch, HEAD and worktree. Use the active branch in Current State, not an assumed-latest `main`. Resolve differences before writes; preserve local work. Project Sources are separate snapshots.

## Architecture invariants

- AI controls language; deterministic game systems control reality.
- Unity is the planned authoritative state/rule owner; the Python prototype is not an implemented Unity client.
- LLM output must never directly modify canonical state.
- NPC output is grounded by authored character cards, knowledge, canon and dynamic state.
- Follow Frozen Contract v0.1.1 on the active branch. Runtime validity and semantic fidelity are separate; fixture truth is evaluation-only. The lexical NPC gate is Experimental, not a general safety guarantee.

## Do not

- Create Unity unless explicitly requested.
- Implement Dify/production runtime integration before validation and authorisation. Existing Experimental harness work follows Current State/Handoff.
- Replace authored branches with fully generated plot; invent unresolved story canon or architecture.
- Commit/push unrelated work without approval, reset/force-push, delete historical branches or auto-stash local work.
- Treat a configured API key as permission for live model/token-count requests, credential access or spending. Preserve execution gates.

## Smallest useful increment

Prefer a bounded testable change, state assumptions and keep scope narrow. Free-first is the user's experimentation preference: verify access/billing; never silently substitute paid execution. Reuse schemas and authority boundaries across provider experiments.

Use the current Master/local implementation stream. Reopen historical validation or add a specialist only for a concrete issue. Dify is a planned feasibility choice, not a compulsory delay before a minimal playable loop.

## Evidence and handback

Add appropriate tests for behaviour changes. Distinguish implemented code, historical reported tests, actual reruns, measured model results and player validation. Preflight, test counts and key configuration are not proof of a working game.

Update Current State and Handoff together at substantial checkpoints. README is the entry; Overview explains the project; Decision Log records confirmed product/architecture decisions; Contract changes require the appropriate approval. Avoid duplicate histories and a new report for every patch.

Done means the requested change is implemented, appropriately verified and documented, with AI/state boundaries intact. Report exact commit/files, actual tests/limits, next action, local sync needs and Source refresh files. Never claim a pull or Project refresh without evidence it occurred.
