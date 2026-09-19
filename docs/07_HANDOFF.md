# Handoff — recovery checkpoint 2026-09-19

**BTL-AI:** PC-first, 2D narrative journalism; target 20–30 minute vertical slice. AI controls language; deterministic systems control reality. Portfolio goals: game/system design and AI product/orchestration.

**Current:** 04 / Technical Prototype 01, in progress.  
**Active branch:** `prototype/technical-prototype-01`  
**Reviewed implementation anchor:** `38703c4368ae774ebc36b6cbdc27cd61dd1a8c87`  
**Stable historical baseline:** `main @ aa87d39959e6a4b2f6cad31883528cb8e8d1cc42`

This is a later documentation-only checkpoint. Resolve the current remote HEAD; do not reset to the anchor. Completed stages, historical test counts and remaining risks are in `06_CURRENT_STATE.md`.

## Read by task, not the entire archive

Resume with AGENTS, applicable Project Instructions, README, Current State and this handoff. Before significant changes also read Project Definition and relevant Decision Log entries. For AI semantics/implementation, read applicable Frozen Contract v0.1.1 sections and affected code/tests. Reports 09–11 and specialist fixtures are reference evidence, not a mandatory full reread for every patch.

## Immediate local task: reconcile and rerun offline tests

Use the existing BTL-AI checkout selected in GitHub Desktop/Codex. `F:\BTL-AI` is a historical location, not verified now; do not create another copy or assume a drive letter.

Read-only inventory from that repository:

```powershell
git rev-parse --show-toplevel
git remote get-url origin
git branch --show-current
git status --short --branch
git rev-parse HEAD
git log -5 --oneline
```

Confirm remote `BenCCCCCCCCC/BTL-AI`. Redact embedded credentials in URLs. Do not inspect/print/upload `.env`, API keys or credential stores.

Preserve local work first. On the correct branch with no conflicting changes, use GitHub Desktop **Fetch origin → Pull origin**, or:

```powershell
git fetch origin
git rev-list --left-right --count HEAD...origin/prototype/technical-prototype-01
git pull --ff-only origin prototype/technical-prototype-01
```

Dirty worktree, wrong branch or divergent local commits: stop before changing files and report the difference. No reset, force-push, auto-stash, deletion or unrelated merge. Fetch alone does not update the checkout. Record HEAD/status after a safe pull.

Inspect the tracked tests and use the existing verified Python environment:

```powershell
python -m pytest -q
```

No provider calls or silent dependency installation/upgrade. Report missing dependencies as a blocker, not a test pass. Preserve a sanitised test result with exact SHA/environment.

The optional OpenAI preflight is not a model test. Check JSON `preflight_passed`, not exit code alone: the reviewed CLI returns 0 on false. Make a narrow CLI fix/regression before automating it. It also briefly creates/removes a local write probe, so it is not strictly read-only.

## Continue 04 after reconciliation

Select one **free-first** candidate route only after checking current access, quotas/billing, data handling and compatibility. No free provider is integrated in the reviewed branch. Reuse the runner, manifest and schemas; no broad provider framework or silent paid fallback.

Live calls require separate execution authorisation. Their deliverable is reproducible three-component P0 evidence and a proceed/fix/defer decision, not just connectivity. Four smoke cases do not replace the full baseline. Preserve sanitised candidates and first-pass/final quality evidence; do not pass expected answers to the model.

Keep Frozen semantics, Response Plan authority and eight Hard Safety Gates unchanged. Runtime validity is not fidelity; fixture truth is evaluation-only. Dialogue failure invents no action; headline failure preserves draft/blocks publication; NPC fallback preserves the plan. The lexical gate and consequence stub remain Experimental.

The paid sheet stays `execution_authorized=false`. API-key configuration and old price estimates are not permission for model or token-count requests. Dify remains optional post-baseline feasibility. Do not create Unity, production backend, final canon/balance or P1/P2 here. The later product target is one separately authorised minimal playable loop.

## Smaller collaboration and completion loop

Use one active Master conversation and the existing local Codex implementation stream. Routine implementation stays in 04; 01-M2 handles only new shared Contract/schema/authority/P0 issues. Open another specialist thread only for a concrete need, not every sub-batch.

Each handback contains: exact branch/commit/files; what changed; what was actually tested and its limits; next smallest action; local sync and Project Sources status. Update 06/07 together at substantive checkpoints. Do not create a new report or copy the whole history for every patch.

## Required sync for this checkpoint

Changed files: `README.md`, `AGENTS.md`, `docs/00_PROJECT_OVERVIEW.md`, `docs/06_CURRENT_STATE.md`, `docs/07_HANDOFF.md`.

**Local sync: required, not performed here.** The current Windows path/branch/cleanliness remains unknown until inventory and safe pull.

**Project Sources refresh:** replace `00_PROJECT_OVERVIEW.md`, `06_CURRENT_STATE.md`, `07_HANDOFF.md` after local sync. Refresh README/AGENTS too if they are uploaded Sources. Project freshness could not be verified; Library management cannot substitute for updating Project Sources.

If no usable baseline Sources are present, restore the repository's existing Project Instructions, `01_PROJECT_DEFINITION.md`, `05_DECISION_LOG.md` and Frozen `08_AI_INTERACTION_CONTRACT.md` v0.1.1 too. The Instructions text file and the Project's instruction settings are separate surfaces.

Decision Log/Contract change: **No**. Current State/Handoff: **Yes**. New specialist/Contract review: **not needed for this docs-only checkpoint**. No runtime/test/schema/paid-setting change, merge to main or historical-branch deletion.

## Audit limit

GitHub was read directly. The user's disk and Project Sources were inaccessible. No full-suite rerun, live-model call, paid request, local pull or Project refresh occurred in the 2026-09-19 Chat audit. Never report all copies as synchronised without new evidence.
