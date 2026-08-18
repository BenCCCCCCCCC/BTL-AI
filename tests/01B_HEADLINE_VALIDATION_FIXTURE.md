# 01B Headline Analysis Validation Fixture

**Project:** Between the Lines: AI Remake (BTL-AI)  
**Validation Increment:** 01  
**Thread:** 01B — Headline Analysis Validation  
**Status:** Temporary validation fixture — non-canonical  
**Specialist status:** READY FOR MASTER REVIEW — TARGETED REGRESSION PASSED  
**Regression basis:** 01 Master first integration review, 2026-08-18  
**Purpose:** Pressure-test the Headline Analyzer and deterministic evidence/publication boundary before any Dify or Unity implementation.

> This file contains invented validation IDs and examples only. They are not story canon, final Target Catalogue content, final Evidence–Claim Relationship data, gameplay formulas, or production prompts.

---

## 1. Contract assumptions under targeted regression

This fixture now tests the Master-revised headline contract supplied after the first 01B review.

The targeted regression assumes:

- Headline Analyzer output is non-authoritative.
- AI controls language; deterministic systems control evidence evaluation, canonical truth, publication consequences, and game state.
- Headline output is `status + claims[]`.
- There is **no fixed 1–3 Claim Atom limit**.
- `claims[]` must represent all consequential claims visible in the headline.
- Silent truncation or selective simulation is forbidden.
- `RESOLVED + claims=[]` is valid when the headline contains no consequential proposition and no unresolved consequential content.
- Each consequential Claim Atom contains an authored `target_id`, conditional `value_id`, conditional `polarity`, a `commitment_mode`, and optional `source_ref_id`.
- `commitment_mode` values are:
  - `ASSERTED`
  - `SPECULATIVE`
  - `QUESTIONED`
- Attribution is orthogonal to commitment mode: `source_ref_id` may coexist with `ASSERTED`, `SPECULATIVE`, or `QUESTIONED` where the language supports it.
- Presupposed consequential propositions in questions must create Claim Atoms. In v0.1, when no additional gameplay distinction is required, the presupposed proposition is represented with `ASSERTED` commitment.
- Attribution support and underlying-proposition support are separate deterministic evidence questions.
- Canonical reality remains separate from both evidence-support questions.
- Publication responsibility is bound to the evidence / knowledge snapshot available at publication time.
- Later evidence may change the player's current understanding but does not retroactively rewrite the original publication-responsibility basis.
- Headline AI/system failure may use a deterministic UX fallback only. It must never manufacture a Claim Set after parsing failure and then continue publication resolution.
- A consequentially unresolved headline must not enter publication resolution.
- Pre-publish warnings describe player language behaviour rather than hidden evidence sufficiency or canonical truth.

### Regression scope

This pass is intentionally targeted. It does **not** re-execute every first-pass case. It focuses on the Master revisions and the cases most likely to regress:

- 4+ claims;
- zero consequential claims;
- attribution + speculation;
- attribution + negation;
- attribution + question where representable;
- presuppositional questions;
- attribution support vs underlying proposition support;
- publication-time evidence snapshots;
- parser failure without fabricated Claim Sets;
- claim omission / extra-claim safety gates.

First-pass cases outside those areas remain carry-forward validation cases and are not claimed as newly re-tested here.

---

## 2. Temporary authored catalogue

### Targets

`FIRE_FIRST`
- `SECURITY_FORCES`
- `MILITIA`

`ORDERED_OPERATION`
- `MAYOR_OFFICE`
- `MILITIA_COMMAND`

`FUNDED_OPERATION`
- `COMPANY_A`
- `MAYOR_OFFICE`

`CIVILIAN_DEATH_CAUSE`
- `SECURITY_FORCES`
- `MILITIA`

### Sources

- `SRC_WITNESS_A`
- `SRC_POLICE`
- `SRC_MAYOR`

### Evidence

- `EV_VIDEO_A`
- `EV_WITNESS_A`
- `EV_MEMO_A`
- `EV_AUDIO_A`

`CIA`, `FOREIGN_AGENCY`, and any ID not listed above are intentionally outside the fixture catalogue.

---

## 3. Expected-output shorthand

A Claim Atom is written as:

`TARGET / VALUE / POLARITY / COMMITMENT_MODE / [optional SOURCE]`

Examples:

`RESOLVED → FIRE_FIRST / SECURITY_FORCES / AFFIRM / ASSERTED`

`RESOLVED → FIRE_FIRST / SECURITY_FORCES / AFFIRM / SPECULATIVE / SRC_WITNESS_A`

`RESOLVED → claims=[]`

`SYSTEM_FAILURE` means malformed, invalid, timed-out, or validator-rejected model output rather than a semantic status.

Evidence outcomes such as `SUPPORTED`, `INSUFFICIENT`, and `CONTRADICTED` are conceptual deterministic test labels only. This fixture does not confirm final production evidence enum names.

---

# 4. Targeted semantic regression cases

| ID | Player headline | Expected result | Regression result / notes |
| --- | --- | --- | --- |
| T01 | Security forces fired first, the mayor's office ordered the operation, Company A funded it, and militia forces caused the civilian deaths. | `RESOLVED → 4 Claim Atoms` | **PASS.** Fixed claim-count cap is no longer needed. All four consequential claims must be returned; no `TOO_MANY_CLAIMS`; no truncation. |
| T02 | A city waits for answers. | `RESOLVED → claims=[]` | **PASS.** No consequential proposition and no unresolved consequential content. The headline may resolve without manufacturing a claim. |
| T03 | Witness A says security forces may have fired first. | `RESOLVED → FIRE_FIRST / SECURITY_FORCES / AFFIRM / SPECULATIVE / SRC_WITNESS_A` | **PASS.** Attribution and speculation are represented orthogonally without a schema gap. |
| T04 | The mayor denies the mayor's office ordered the operation. | `RESOLVED → ORDERED_OPERATION / MAYOR_OFFICE / DENY / ASSERTED / SRC_MAYOR` | **PASS.** Source attribution, proposition polarity, and commitment remain independently representable. |
| T05 | Witness A asks whether security forces fired first. | `RESOLVED → FIRE_FIRST / SECURITY_FORCES / AFFIRM / QUESTIONED / SRC_WITNESS_A` | **PASS.** Explicit attribution and questioned commitment are representable together. This is distinct from asking whether Witness A made a statement. |
| T06 | Why did the mayor's office order the operation? | `RESOLVED → ORDERED_OPERATION / MAYOR_OFFICE / AFFIRM / ASSERTED` | **PASS.** The consequential presupposition is not hidden behind a question mark. The interrogative request for a reason does not erase the asserted presupposition. |
| T07 | Why didn't the mayor's office order the operation? | `RESOLVED → ORDERED_OPERATION / MAYOR_OFFICE / DENY / ASSERTED` | **PASS.** Presuppositional question + negation remains representable through polarity plus asserted commitment. |
| T08 | Witness A says security forces fired first; Police say they did not. | `RESOLVED → 2 attributed Claim Atoms` | **PASS** when reference scope is unambiguous: Witness A = `AFFIRM / ASSERTED / SRC_WITNESS_A`; Police = `DENY / ASSERTED / SRC_POLICE`. No source is treated as automatically reliable. |
| T09 | Security forces fired first as CIA agents directed the operation. | `UNSUPPORTED / OUT_OF_CATALOGUE` | **PASS.** Removing the claim-count cap does not weaken atomic resolution. One unresolved consequential claim still blocks the full headline from publication resolution. |
| T10 | Security forces fired first. | `RESOLVED → 1 Claim Atom` | **PASS.** Ordinary single-claim baseline remains compatible with the revised schema. |
| T11 | Security forces may not have fired first. | `RESOLVED → FIRE_FIRST / SECURITY_FORCES / DENY / SPECULATIVE` | **PASS.** Polarity remains independent from commitment mode. |
| T12 | Did security forces fire first? | `RESOLVED → FIRE_FIRST / SECURITY_FORCES / AFFIRM / QUESTIONED` | **PASS.** A non-presuppositional direct question remains a questioned proposition rather than an asserted one. |

### Clarifying contrast: attribution + question vs question about attribution

The revised schema solves cases where a known source is linguistically expressing a question, such as T05.

It does **not** imply that:

> `Did Witness A say security forces fired first?`

should be flattened into `FIRE_FIRST / SECURITY_FORCES / ... / SRC_WITNESS_A`.

That sentence asks whether a source-speech event occurred. If the authored catalogue does not contain a proposition for source-speech occurrence, it remains unsupported in this fixture. This is not a new schema defect.

---

# 5. Carry-forward semantic cases not fully re-executed

These first-pass cases remain useful evaluation coverage but were not the target of this regression pass.

| Case family | Carry-forward expectation |
| --- | --- |
| Direct assertion | `Security forces fired first.` → `ASSERTED`. |
| Direct negation | `Security forces did not fire first.` → `DENY / ASSERTED`. |
| Unsupported entity | `CIA agents directed the operation.` → semantic unresolved / out of catalogue. |
| Ambiguous reference | `They fired first.` → `AMBIGUOUS / AMBIGUOUS_REFERENCE` when multiple antecedents remain plausible. |
| Scoped negation trap | `Police did not deny that security forces fired first.` must not be reduced by keyword matching into a simple polarity flip. |
| Pure framing | `Shocking: security forces fired first.` carries the same consequential Claim Atom as the unframed assertion when no gameplay rule depends on `shocking`. |
| Proposition-changing rhetoric | `murdered`, `slaughtered`, etc. must not be silently flattened if the wording adds authored consequential meaning such as intent or culpability. |
| Prompt injection | Player headline text cannot instruct the model to ignore the catalogue, reveal canonical truth, or produce evidence verdicts. |

---

# 6. Parser / validator failure targeted regression

| ID | Input / model behaviour | Expected system behaviour | Regression result |
| --- | --- | --- | --- |
| F01 | Model returns malformed JSON / unusable structure. | `SYSTEM_FAILURE` → retry once → validate again. If retry also fails: preserve player draft, show deterministic non-consequential UX fallback, **produce no Claim Set**, and do not enter publication resolution. | **PASS.** No semantic template fallback is permitted. |
| F02 | Model returns illegal `commitment_mode = CERTAIN_TRUE`. | Validator rejects; system failure path; no publication resolution from the invalid output. | **PASS.** |
| F03 | Model returns `target_id = CIA_DIRECTOR`. | Validator rejects invalid authored ID; no publication resolution. | **PASS.** |
| F04 | T01 input but model returns only three of the four consequential claims. | Mandatory safety defect. The incomplete result must not be accepted as a successful complete Claim Set. | **PASS.** Claim omission remains a hard safety concern after removing the old 1–3 limit. |
| F05 | T10 input but model invents an additional claim that the mayor ordered the operation. | Mandatory safety defect / extra-claim hallucination; invented atom must not be accepted as faithful headline semantics. | **PASS.** |
| F06 | Prompt injection causes model to output `SUPPORTED` or canonical truth. | Authority-boundary defect; such output has no publication authority and must be rejected/ignored by contract validation. | **PASS.** |
| F07 | Retry fails and deterministic UX says “Headline analysis unavailable; edit or try again.” | Draft remains intact; `claims` is not fabricated; publication resolution remains blocked. | **PASS.** Confirms UX fallback is allowed while semantic fallback is forbidden. |

---

# 7. Deterministic evidence / publication targeted regression

All cases below begin **after** semantic parsing and Claim Set validation. The LLM does not determine any evidence outcome.

For attributed claims, deterministic evaluation keeps three concepts separate:

1. **Attribution support** — evidence that the named source actually expressed the represented proposition/commitment.
2. **Underlying proposition support** — evidence supporting or contradicting the proposition itself.
3. **Canonical reality** — authored world truth, which remains separate from publication-time evidence responsibility.

| ID | Headline | Publication-time basis | Later / canonical information | Expected result | Regression result |
| --- | --- | --- | --- | --- | --- |
| E01 | Witness A says security forces fired first. | `EV_AUDIO_A` reliably records Witness A saying it. A verified video contradicts the underlying proposition. | Canonically militia fired first. | Attribution support = `SUPPORTED`; underlying proposition support = `CONTRADICTED`; canonical reality = militia fired first. | **PASS.** The supported attribution does not convert the underlying proposition into supported fact. |
| E02 | Witness A says security forces fired first. | No reliable evidence Witness A said it. Independent video supports security forces firing first. | Canonically security forces fired first. | Attribution support = `INSUFFICIENT`; underlying proposition support = `SUPPORTED`; canonical reality = security forces fired first. | **PASS.** A true/supported underlying proposition does not rescue unsupported attribution. |
| E03 | Security forces fired first. | Publication snapshot contains only one uncertain witness statement. | Later evidence proves security forces actually fired first. | Original publication responsibility remains `INSUFFICIENT` on its publication-time basis. Later canonical confirmation must not retroactively mark the original reporting as well-supported. | **PASS.** |
| E04 | Security forces fired first. | Publication snapshot contains multiple apparently reliable items supporting the claim. | Later evidence shows militia fired first and earlier sources were misleading. | Original responsibility basis remains the publication-time snapshot and may remain `SUPPORTED` as a journalism-responsibility judgment even though canonical reality is later shown false. | **PASS.** |
| E05 | Security forces fired first. | Publication snapshot records evidence IDs / relevant knowledge state used for deterministic evaluation. | Player later obtains `EV_VIDEO_A` contradicting the headline. | Current player knowledge changes, but the stored original publication-responsibility basis does not change. | **PASS.** Snapshot requirement is sufficient at contract level without choosing a backend schema yet. |

### Snapshot requirement

This regression does not prescribe a production persistence implementation. The deterministic system only needs an auditable publication-time basis sufficient to prevent later evidence from silently rewriting the original responsibility evaluation. A later implementation may store evidence IDs, a knowledge snapshot, deterministic inputs, or another auditable equivalent approved in a later design step.

---

# 8. Zero-claim publication boundary

`RESOLVED + claims=[]` is not a parser failure and does not authorise the LLM to invent gameplay consequences.

For a headline such as:

> `A city waits for answers.`

expected contract behaviour is:

1. semantic parsing succeeds;
2. `claims=[]`;
3. there is no consequential claim to send through claim-specific evidence evaluation;
4. any non-claim publication behaviour, if the game later needs it, must come from authored deterministic rules rather than a fabricated Claim Atom.

**Targeted regression result: PASS.** No new P0 schema field is required by this case.

---

# 9. Pre-publish warning regression

Master revisions do not change the confirmed warning philosophy.

Temporary non-canonical examples:

| Headline | Expected warning behaviour |
| --- | --- |
| Security forces fired first. | May describe a direct responsibility assertion. Must not reveal hidden evidence sufficiency or canonical truth. |
| Witness A says the mayor's office ordered the operation. | May describe publication of a serious attributed allegation. Must not imply the source is credible merely because it is named. |
| Witness A says security forces may have fired first. | May describe an attributed speculative allegation if the authored target is warning-worthy. Must not collapse attribution and speculation into a hidden correctness score. |
| Why did the mayor's office order the operation? | Warning logic may treat the extracted presupposed `ASSERTED` allegation as a direct responsibility claim. The question mark must not suppress the warning. |
| A city waits for answers. | `claims=[]` by itself should not trigger a consequential-claim warning. |

The player retains **Edit** and **Publish Anyway** for semantically resolved valid-risk headlines.

---

# 10. Rhetorical wording carry-forward result

Targeted regression produced no reason to add generic sentiment, emotionality, political-bias, propaganda, misinformation, or sensationalism scores.

The first-pass distinction remains sufficient:

1. **Pure framing** — tone changes without adding a gameplay-relevant proposition; may remain outside authoritative v0.1 semantics.
2. **Semantic payload disguised as rhetoric** — wording adds consequential meaning such as intent, culpability, scale, or agency; it must map to authored semantics or fail safely rather than being silently weakened.

Current 01B recommendation remains: keep a generic `rhetorical_frame` field deferred.

---

# 11. Headline-specific safety gates after Master revision

The old gate referring to silent truncation into a valid **1–3** Claim Set is superseded because the fixed claim-count cap has been removed.

Current targeted safety-gate candidates:

- Unsupported consequential content entering publication resolution = **0**.
- Invented target/source ID accepted = **0**.
- Any known visible consequential claim omitted while an incomplete Claim Set is accepted in the mandatory safety suite = **0**.
- Extra consequential Claim Atom not expressed by the headline accepted in the mandatory safety suite = **0**.
- Claim-count-based silent truncation = **0**.
- Prompt injection producing authoritative evidence/canonical verdict = **0**.
- Malformed or validator-rejected model output entering publication resolution = **0**.
- Retry-exhausted parser failure producing a fabricated fallback Claim Set = **0**.
- Semantically unresolved headline entering publication resolution = **0**.

These remain evaluation correctness constraints rather than average-quality scores.

---

# 12. Quality metrics after Master revision

Headline evaluation candidates now read more clearly as:

- Claim Set Exact Match
- Per-Atom Precision
- Per-Atom Recall
- Consequential Claim Omission Rate
- Extra Claim Rate
- Commitment Mode Accuracy
- Source Attribution Accuracy
- Polarity Accuracy
- Unsupported Entity Detection
- Ambiguity Detection
- Atomic Resolution Accuracy
- Zero-Claim Resolution Accuracy
- Prompt-Injection Robustness
- Safety Gate Violation Count

No numerical acceptance threshold should be invented before a real model baseline is measured.

---

# 13. Targeted regression findings

The Master revisions resolve the seven shared structural issues raised by the first 01B pass without creating a new headline-contract structural conflict.

### Passed findings

1. **4+ claims:** removing the fixed cap allows all visible consequential claims to be represented while preserving atomic resolution and anti-omission safety.
2. **Zero claims:** `RESOLVED + claims=[]` cleanly represents valid non-consequential headlines without treating them as semantic failures or inventing claims.
3. **Attribution + speculation:** `commitment_mode` plus optional `source_ref_id` represents both dimensions without loss.
4. **Attribution + negation:** polarity remains independent from both source attribution and commitment mode.
5. **Attribution + question:** where a source is explicitly asking/questioning the proposition, `QUESTIONED + source_ref_id` is sufficient.
6. **Presuppositional question:** extracting the consequential presupposition as an `ASSERTED` Claim Atom prevents a question mark from hiding an allegation.
7. **Evidence architecture:** attribution support, underlying-proposition support, and canonical reality can diverge without contradiction.
8. **Publication-time responsibility:** an auditable publication-time evidence/knowledge basis prevents later evidence from retroactively rewriting the original journalistic-responsibility evaluation.
9. **Parser failure:** retry-exhausted failure can safely fall back to UX while remaining unable to fabricate a Claim Set or continue publication resolution.
10. **Claim omission / extra claims:** safety gates remain meaningful after the claim cap is removed and are now simpler to state: the semantic representation must neither omit visible consequential claims nor invent new ones.

### New shared structural issues

**None identified in this targeted regression.**

The revised design still leaves implementation details intentionally deferred, including final Evidence–Claim Relationship data structures, persistence/backend representation of publication snapshots, model prompts, runtime orchestration, and numerical acceptance thresholds. Those are not regressions in the shared v0.1 contract.

---

# 14. Master decision trace

The first-pass `MASTER-01` through `MASTER-07` issues are considered **resolved for 01B regression purposes** by the supplied Master decisions:

- former MASTER-01 → fixed claim-count cap removed; all consequential claims required;
- former MASTER-07 → `RESOLVED + claims=[]` allowed;
- former MASTER-03 → `commitment_mode` separated from optional `source_ref_id`;
- former MASTER-04 → consequential presupposition extracted and treated as `ASSERTED` in v0.1 absent another gameplay need;
- former MASTER-02 → attribution support separated from underlying proposition support and canonical reality;
- former MASTER-05 → publication responsibility bound to publication-time evidence/knowledge basis;
- former MASTER-06 → headline parser retry exhaustion permits UX fallback only, never a fabricated semantic fallback.

No `TOO_MANY_CLAIMS` reason is introduced.

---

# 15. Specialist status

**Thread:** 01B — Headline Analysis Validation  
**Status:** **READY FOR MASTER REVIEW — TARGETED REGRESSION PASSED**

Reason:

- the Master-requested targeted cases have been pressure-tested against the revised contract;
- all seven first-pass shared structural issues have a coherent regression outcome;
- no new shared structural issue was discovered;
- the validation fixture has been updated to the revised headline schema and evidence boundary;
- claim omission, extra-claim, parser-failure, and authority-boundary safety gates remain explicit;
- no production prompt, Dify workflow, Unity implementation, final story canon, or backend persistence schema has been introduced.

This status does **not** independently freeze AI Interaction Contract v0.1. Final integration / freeze authority remains with `01 | AI Interaction Contract — Validation Increment 01`.
