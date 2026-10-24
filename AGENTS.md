# Working Agreement

## Start with the current task

Read README, Current State and Handoff; for significant product or architecture changes also read Project Definition and the relevant Decision Log / Frozen Contract sections. Read affected code and fixtures as needed, not the entire archive.

Check the actual repository, active branch, HEAD and relevant local changes once when taking over. Use the active branch in Current State. Preserve local work; unrelated dirty files do not block independent work. Resolve overlapping edits or actual divergence before touching those paths.

## Architecture invariants

- AI controls language; deterministic systems control reality.
- Unity is the planned authoritative state/rule owner; Python components are Experimental.
- LLM output never directly changes canonical state.
- Frozen Contract v0.1.1 and the eight Hard Safety Gates remain in force.
- Runtime validity and semantic fidelity are separate. Fixture truth is evaluation-only; the lexical NPC gate is not a general natural-language guarantee.

## Progress without repeated gates

Within an authorised task, proceed with routine reversible implementation, document fixes and repository-scoped environment setup using existing requirements. Do not repeatedly request the same approval or add checks without a concrete defect, input boundary or contractual requirement.

Reuse existing components and evidence. Choose one suitable free-first route; stop provider comparison when it meets the immediate need. Never silently substitute paid execution. A configured key is not live-call or spending permission.

Use the existing Master/implementation stream. Escalate new shared semantic/schema/authority/P0 decisions; ordinary fixes need no specialist thread. Dify is optional when it solves an observed orchestration need. Unity creation, live calls and spending retain their recorded authorisation requirements.

Preserve user changes. No unrelated commits, destructive reset/force-push, branch deletion or automatic disposal/stashing of local work.

## Verification and completion

Use the change-based verification table in `docs/07_HANDOFF.md`:
- Documentation-only changes: factual/link/consistency review, no runtime suite.
- Behaviour changes: the smallest affected existing tests plus a focused regression for a concrete new behaviour.
- Full offline regression: a new execution environment with no applicable results, material shared-path changes, or a justified integration checkpoint.
- Reuse unchanged smoke/baseline evidence under matching code, model, prompt, schema, inputs and run conditions. Do not repeat identical calls to satisfy separate labels.

Stop when the agreed acceptance criteria are met. Broaden verification only to answer a named unresolved issue. Keep useful existing boundary tests; reducing redundant execution is preferable to a separate mass-deletion project.

Report implementation, historical tests, actual reruns, measured model quality and player validation distinctly. At substantive checkpoints update 06/07 together. Handback needs outcome/commit/files, actual verification and limits, unresolved issues, next action and copy-sync needs. Avoid duplicate reports, repeated Yes/No checklists and unnecessary mode/model switches.

Done means the requested result is implemented, proportionately verified and documented. Never claim local pull, Project refresh, runtime repair or live-model results without evidence.
