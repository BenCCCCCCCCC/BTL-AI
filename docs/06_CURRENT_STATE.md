# Current State

**Reviewed:** 2026-09-19  
**Current phase:** **04 — Technical Prototype 01, IN PROGRESS**  
**Active branch:** `prototype/technical-prototype-01`  
**Reviewed implementation:** `38703c4368ae774ebc36b6cbdc27cd61dd1a8c87`  
**Stable historical baseline:** `main @ aa87d39959e6a4b2f6cad31883528cb8e8d1cc42`

This is a documentation-only recovery checkpoint. The implementation SHA is an audit anchor, not the moving documentation HEAD; resolve the current branch tip before work.

## Actual position

Product definition, VI01, VI02 and Gate 03 are complete. An Experimental Python test harness is implemented. **A measured real-model baseline, playable Remake demo and player validation are not evidenced as complete.**

Frozen Contract **v0.1.1** is current on the active branch. Historical reports 09–11 retain v0.1 context; they do not supersede v0.1.1. `main` is the earlier stable design baseline, not the latest implementation.

## Stage and evidence ledger

| Increment | Result | Evidence / limitation |
| --- | --- | --- |
| 00 / repository baseline | Complete | Product scope and working agreement |
| VI01 | Complete: three P0 AI boundaries | Report 09; design/fixture validation, not real-model results |
| VI02 | Complete: catalogue, Evidence–Claim rules and NPC grounding | Report 10; railyard sample remains Experimental / non-canonical |
| Gate 03 | Complete; integrated into main | Report 11; DEC-020 consequence interface and DEC-021 model-baseline protocol |
| 04 / Batch 1 and 1.2 | Implemented; Contract v0.1.1 accepted | Manifest, schemas, validators, fixture oracle, lexical NPC gate and isolated consequence stub; historical reports: 48 then 61 tests passed |
| 04 / Batch 2A | Complete; accepted by 04 Master | `5f14abf8ddd759f9dcefd864cf9d7de213150ae7`; scripted runner, retry/fallback and JSONL measurement; historical report: 82 passed |
| 04 / Batch 2B.0 | Implemented; zero-call checkpoint recorded | `e4412efa27ff41a77ca3f3cc7e777c12cf222be5`; Experimental Responses adapter, prompts, transport schemas and preflight; historical report: 104 passed, zero model requests at that checkpoint |
| 04 / Batch 2B.0.1 | Implementation present; omitted handoff entry repaired here | `38703c4368ae774ebc36b6cbdc27cd61dd1a8c87`; authorisation, pre-send input-token count and call-limit guards. No fresh full-suite result established by this audit |
| Live smoke / Batch 2B.1 / measured baseline | Not evidenced as complete | No reviewed committed measurement proves completion; ignored local output files were inaccessible |
| Dify / Unity / playable loop / player testing | Not started in reviewed repository | Future direction/placeholders, not delivered functionality |

These test counts are **historical reported results**, not tests rerun on 2026-09-19, player counts or model accuracy. The implementation HEAD's combined-status lookup returned no statuses; that is not a CI pass.

## Invariants and known limits

- **Runtime PASS is not fidelity PASS.** D19 tactic omission, F04 missing claims and F05 extra catalogue-valid claims can pass candidate/context validation and fail the authored oracle. DEC-022 and v0.1.1 preserve this separation. Fixture truth is evaluation-only, never a production runtime judge or retry signal.
- **The lexical NPC gate is fixture-scoped, not production safety.** Known regex checks do not prove arbitrary free-text response-plan fidelity. The eight Hard Safety Gates remain unchanged.
- Dialogue retries system failure once, but not valid AMBIGUOUS/UNSUPPORTED. Exhaustion invents no validated action. Headline exhaustion preserves the draft and blocks publication, not `RESOLVED + claims=[]`. NPC fallback must preserve the deterministic plan and pass the gate.
- The consequence stub is isolated and uses Experimental effects, not final balance or a complete game rule engine. AI never creates authoritative state deltas.
- Measurement infrastructure exists; a complete Frozen quality-metric report does not. Retain sanitised candidates and distinguish first-pass/final quality, runtime safety, omissions/extras, latency, retries, tokens and cost. Never include expected answers in model inputs.
- **Static-review operational caveat:** `openai_preflight.py::main()` returns 0 even when JSON `preflight_passed` is false. Until a focused CLI fix/regression is made, check that Boolean explicitly. No runtime fix or test rerun is claimed here.

## Cost and execution

The user's preference is **suitable free models first; minimise spending**. No free provider is evidenced as integrated; scripted tests are not free real-model tests.

The paid sheet remains `PROPOSED_NOT_AUTHORIZED`, `execution_authorized=false`. This audit authorises no live model/token-count requests, new accounts, credentials or spending. A previous conversation reported an API key configured; its current existence/validity is unverified and is not execution permission.

The historical paid plan covered four cases, up to eight generation calls, 8,192/1,024 input/output tokens per call, aggregate 65,536/8,192 and a USD 0.25 **model-generation-only planning ceiling**. Token-count endpoint billing is explicitly unknown. Reverify model, SDK, pricing and full billing coverage before any separately authorised live run; never silently substitute paid execution.

## Next smallest outcome

1. Reconcile the actual local checkout and rerun offline tests using `07_HANDOFF.md`. Record exact SHA/environment/results. Address the preflight CLI caveat with a focused regression before relying on exit codes.
2. Check **one** currently accessible free route; reuse the existing runner/manifest/schemas rather than building a multi-provider platform. Verify access, billing, data handling and compatibility. Report a specific blocker if no suitable free route works.
3. After separate live-execution authorisation, run a smoke and then the fixture-derived three-component P0 baseline. Four smoke cases alone are not the full quality baseline. Preserve safety boundaries and first/final evidence; set numerical acceptance thresholds after initial measurements as DEC-021 requires.
4. Return **proceed / fix / defer**, aimed at a minimal playable loop. Escalate only new shared Contract/schema/authority/P0 issues to Contract Master; ordinary implementation stays in 04.

Future route: **technical evidence → one minimal playable investigation/conversation/evidence/headline/consequence loop → polished 20–30 minute vertical slice → player evaluation and portfolio evidence**. Future stages are not started or authorised by this audit. Dify remains optional post-baseline feasibility; Unity creation, final canon/balance, production tooling, backend and P1/P2 remain separately gated.

## Source reconciliation

| Surface | Verified status |
| --- | --- |
| GitHub | Read directly. Before this docs checkpoint the active branch was 7 commits ahead of main, 0 behind |
| Windows checkout | Inaccessible here; historical `F:\BTL-AI` is not a verified current path. Branch, local changes, ignored outputs and sync remain unknown |
| Project Sources | Project-scoped search returned no files; freshness/existence could not be verified. This does not prove deletion |
| Library | No authoritative current source bundle recovered; resumes/unrelated results do not substitute for project evidence |

No local pull, Project Sources refresh, full-suite rerun or live-model request occurred in this Chat audit. GitHub changes do not update the other copies automatically.

## Workflow repair applied

The user's 2026-09-19 audit/optimisation request is implemented as: corrected stage labels; restored Batch 2B.0.1 history; explicit evidence limits/free-first preference; one Master plus local Codex for routine work; a compact task-specific handoff.

README = entry; Overview = plain-language history; Current State = live evidence; Handoff = action/sync; Decision Log = confirmed decisions; Contract = frozen semantics. Existing reports and Git history preserve earlier evidence. No new report or product/architecture decision is introduced. Code, tests, schemas, prompts, authorisation settings, historical reports and branch history are unchanged.
