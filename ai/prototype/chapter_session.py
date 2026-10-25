"""Experimental, independently versioned scripted chapter. No network or truth oracle."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path

from .consequence_stub import (
    AuthoredConsequenceEvent, DeterministicallyResolvedGameplayResult,
    ExperimentalAuthoritativeTestState, ExperimentalVariableEffect, GlobalVariable,
    apply_authored_consequence_event,
)
from .interview_flow import InterviewFlow, TACTIC_LABELS
from .validation import RuntimeCatalogue, TargetDefinition, validate_headline_candidate

CHAPTER = Path(__file__).resolve().parents[1] / "content/railyard_chapter.v1.0.json"
FIRE = "PROP_FIRE_FIRST"
FUNDING = "PROP_FUNDED_OPERATION"
VIEW = "PROP_WITNESS_FIRST_SHOT_VIEW"
USES = "PROP_R17_RECORDED_USES"
AUDIO, VIDEO, LEDGER, CLARIFICATION, CONTEXT = (
    "EV_AUDIO_A", "EV_VIDEO_A", "EV_LEDGER_A", "EV_WITNESS_CLARIFICATION_A", "EV_LEDGER_CONTEXT_A")
SOURCE = "SRC_WITNESS_A"
SCENES = {"A": "N30", "B": "N50", "S-A": "N40", "S-B": "N60"}
SCENE_LABELS = {"A": "核查现场影像", "B": "核对付款账页", "S-A": "核对目击者观察范围", "S-B": "核对账目记录语境"}


@dataclass(frozen=True)
class ChapterPublicationSnapshot:
    headline: str
    claims_json: str
    evidence_json: str
    source_ids: tuple[str, ...]
    evaluation_json: str
    versions_json: str
    prior_events_json: str
    cooperation_json: str

    @property
    def evidence_ids(self):
        return tuple(json.loads(self.evidence_json))


@dataclass(frozen=True)
class PreparedHeadline:
    original_text: str
    claims_json: str
    context_token: int
    basis_json: str


def evaluate_claims(data, claims, evidence):
    """Versioned authored evidence relationships; never consult hidden canonical truth."""
    results = []
    for claim in claims:
        rows = [r for r in data["relationships"] if set(r["requires_evidence"]) <= evidence
                and r["target_id"] == claim["target_id"] and r["value_id"] == claim["value_id"]]
        underlying = [r for r in rows if r["dimension"] == "UNDERLYING"]
        supporting = [r["id"] for r in underlying if r["polarity"] == claim["polarity"]]
        contradicting = [r["id"] for r in underlying if r["polarity"] != claim["polarity"]]
        attribution = [r["id"] for r in rows if r["dimension"] == "ATTRIBUTION"
                       and r["polarity"] == claim["polarity"]
                       and r["source_ref_id"] == claim.get("source_ref_id")]
        results.append({
            "underlying": "CONTRADICTED" if contradicting else "SUPPORTED" if supporting else "INSUFFICIENT",
            "attribution": "NOT_APPLICABLE" if not claim.get("source_ref_id") else "SUPPORTED" if attribution else "INSUFFICIENT",
            "supporting_relationships": supporting, "contradicting_relationships": contradicting,
            "attribution_relationships": attribution,
        })
    return results


class ChapterSession:
    def __init__(self, data=None):
        self.data = deepcopy(data) if data is not None else json.loads(CHAPTER.read_text(encoding="utf-8"))
        self.node = "N00"
        self.revision = 0
        self.slots = self.data["investigation_slots"]
        self.state = ExperimentalAuthoritativeTestState(money=self.data["initial_money"])
        self.evidence: dict[str, dict] = {}
        self.sources: set[str] = set()
        self.cooperation = {"witness": True, "clerk": True}
        self.visited: set[str] = set()
        self.active_scene = None
        self.entry_scene = None
        self.pending = None
        self.history: list[dict] = []
        self.events: list[dict] = []
        self.result_text = ""
        self.result_evidence: tuple[str, ...] = ()
        self.draft = ""
        self.headline_review: PreparedHeadline | None = None
        self.headline_message = ""
        self.publication: ChapterPublicationSnapshot | None = None
        self.ending = None
        self.outcome_text = ""
        self.people_text = ""
        self.issues: list[tuple[int, str]] = []

    @property
    def finished(self):
        return self.node == "N99"

    def _record(self, action, text=""):
        self.revision += 1
        self.history.append({"node": self.node, "action": action, "text": text})

    def _event(self, key):
        if any(e["id"] == key for e in self.events):
            return
        authored = self.data["events"][key]
        result_id = f"{self.data['version']}:{self.revision}:{key}"
        result = DeterministicallyResolvedGameplayResult(result_id)
        event = AuthoredConsequenceEvent(key, result_id, tuple(
            ExperimentalVariableEffect(GlobalVariable(k), v) for k, v in authored["effects"].items()))
        self.state = apply_authored_consequence_event(self.state, result, event)
        self.events.append({"id": key, "label": authored["label"], "effects": deepcopy(authored["effects"]), "result_id": result_id})

    def available_scenes(self):
        if self.node != "N20" or self.slots <= 0:
            return ()
        return tuple(s for s in SCENES if s not in self.visited
                     and (s != "S-A" or {AUDIO, VIDEO} <= self.evidence.keys() and self.cooperation["witness"])
                     and (s != "S-B" or LEDGER in self.evidence and self.cooperation["clerk"]))

    def available_scripts(self):
        return tuple(s for s in self.data["scripts"].get(self.node, ())
                     if s["id"] != "accept" or self.state.money >= 500)

    def dialogue_catalogue(self):
        targets = {}
        for key, item in self.data["targets"].items():
            if self.node in item["dialogue_nodes"]:
                targets[key] = TargetDefinition(allowed_acts=frozenset(item["acts"]),
                    allowed_tactics=frozenset() if item["acts"] == ["OFFER"] else frozenset(TACTIC_LABELS),
                    target_kind=item.get("kind", "PROPOSITION"))
        pending = frozenset({self.pending}) if self.node == "N51" and self.pending else frozenset()
        return RuntimeCatalogue(targets, frozenset(self.evidence), frozenset(self.sources), pending,
            {p: frozenset({"ACCEPT", "REFUSE"} if self.state.money >= 500 else {"REFUSE"}) for p in pending})

    def headline_catalogue(self):
        targets = {}
        for key, item in self.data["targets"].items():
            if item.get("headline") and set(item.get("headline_requires", ())) <= self.evidence.keys():
                targets[key] = TargetDefinition(allowed_values=frozenset(item["values"]),
                    headline_eligible=True, headline_value_required=True, headline_polarity_required=True)
        return RuntimeCatalogue(targets, frozenset(self.evidence), frozenset(self.sources))

    def visible_headlines(self, group=None):
        return {k: v for k, v in self.data["headlines"].items() if not v.get("boundary_only")
                and set(v.get("requires_evidence", ())) <= self.evidence.keys()
                and (group is None or v["group"] == group)}

    def _grant(self, eid, variant=None):
        material = deepcopy(self.data["evidence"][eid])
        material["text"] = material.get("variants", {}).get(variant, material["text"])
        material.pop("variants", None)
        self.evidence[eid] = material
        if eid == AUDIO:
            self.sources.add(SOURCE)

    def _pressure(self, role):
        self.cooperation[role] = False
        self._event("pressure_" + role)

    def _settle(self):
        if self.active_scene:
            if self.active_scene in self.visited or self.slots < 1:
                raise ValueError("scene already settled")
            scene = self.active_scene
            self.visited.add(scene)
            self.slots -= 1
            self.history.append({"node": self.node, "action": "settle", "scene": scene, "cost": 1})
            self.active_scene = None
        self.pending = None

    def _result(self, text, acquired=()):
        self.result_text = text
        self.result_evidence = tuple(acquired)
        self.node = "result"

    def execute_script(self, script_id, candidate):
        # Only the staged controller may call this after revalidating the current context.
        item = next((s for s in self.available_scripts() if s["id"] == script_id), None)
        if item is None or item["candidate"] != candidate or candidate["status"] != "RESOLVED":
            raise ValueError("script is unavailable or does not match reviewed candidate")
        if self.node == "N51" and self.pending != "PENDING_LEDGER_500":
            raise ValueError("no current ledger transaction")
        self._record(script_id, item["text"])
        text = item["response"]
        if item.get("event"):
            self._event(item["event"])
        if item.get("grant"):
            self._grant(item["grant"], item.get("variant"))
        if item.get("pressure"):
            self._pressure(item["pressure"])
            text += "\n\n" + self.data["copy"]["pressure_record"]
        if item.get("finish"):
            self._settle()
            self._result(text, [item["grant"]] if item.get("grant") else [])
        elif item.get("next"):
            self.pending = "PENDING_LEDGER_500"
            self.result_text = text
            self.node = item["next"]
        else:
            self.result_text = text
        return text

    def background(self, label):
        text = self.data["nodes"].get(self.node, {}).get("background", {}).get(label)
        if text is None:
            raise ValueError("background question not available")
        self._record("background", label)
        self.result_text = text
        return text

    def choices(self):
        if self.node == "N00": return [("begin", "去见目击者")]
        if self.node == "N20":
            return [("visit:" + s, SCENE_LABELS[s] + " · 一段") for s in self.available_scenes()] + [("desk", "结束调查，回编辑台")]
        if self.node == "entry": return [("cancel_entry", "返回安排 · 尚未进场"), ("enter", "确认进入 · 本场结束用一段")]
        if self.node == "desk_confirm": return [("cancel_desk", "返回调查安排"), ("finish_investigation", "确认结束调查")]
        if self.node == "N30": return [("save_video", "调出并保存这段记录"), ("leave", "结束现场核查 · 用一段，不取记录")]
        if self.node in {"N10", "N40", "N50", "N60"}: return [("leave", "不采用这次采访" if self.node == "N10" else "结束访问 · 用一段")]
        if self.node == "N51": return [("cancel_pending", "返回交涉 · 取消待确认交易")]
        if self.node == "result": return [("continue", "读完材料，继续")]
        if self.node == "N80": return [("edit", "返回改写 · 保留原句"), ("signoff", "继续到签发确认")]
        if self.node == "N81": return [("edit", "返回改写"), ("publish", "确认签发这一版")]
        if self.node == "N82": return [("edit", "回到标题"), ("hold", "确认本版暂缓")]
        if self.node == "N90": return [("continue", "看刊发后的回应")]
        if self.node in {"N91", "N92", "N93", "N94", "N95"}: return [("continue", "看人物回应")]
        if self.node in {"aftermath", "N96"}: return [("continue", "收束与回看")]
        return []

    def choose(self, choice):
        if choice == "hold_review" and self.node == "N70":
            self._record(choice); self.headline_review = None; self.node = "N82"; return ""
        if choice not in {c[0] for c in self.choices()}:
            raise ValueError(f"unavailable choice {choice!r} at {self.node}")
        if choice in {"signoff", "publish"}:
            self._validate_prepared_headline()
        self._record(choice)
        self.result_text = ""
        if choice == "begin": self.node = "N10"
        elif choice.startswith("visit:"):
            self.entry_scene = choice.split(":", 1)[1]; self.node = "entry"
        elif choice == "cancel_entry": self.entry_scene = None; self.node = "N20"
        elif choice == "enter":
            self.active_scene = self.entry_scene; self.entry_scene = None; self.node = SCENES[self.active_scene]
        elif choice == "desk": self.node = "desk_confirm"
        elif choice == "cancel_desk": self.node = "N20"
        elif choice == "finish_investigation": self.slots = 0; self.node = "N70"
        elif choice == "cancel_pending": self.pending = None; self.node = "N50"
        elif choice == "save_video":
            self._grant(VIDEO); self._settle()
            self._result("你把画面停在两边动作之间的那几秒。屏幕没有替你决定怎样写。", [VIDEO])
        elif choice == "leave":
            text = {"N10": "阿岑：那你查到以后再决定。别把没记下来的话写成采访。",
                    "N40": "阿岑：那就把你现在确实知道的写清楚。",
                    "N50": "许先生：好。你没有拿到这页，别把它写成你看过的记录。",
                    "N60": "许先生：那就写你手里有的。"}.get(self.node, "本次现场访问结束，未取得影像记录。")
            self._settle(); self._result(text)
        elif choice == "edit": self.headline_review = None; self.node = "N70"
        elif choice == "signoff":
            self._validate_prepared_headline(); self.node = "N81"
        elif choice == "publish": self._publish()
        elif choice == "hold":
            self.ending = "N96"; self.outcome_text = self.data["copy"]["held"]
            self.outcome_text += "\n\n" + ("你把本局材料按取得顺序收拢。它们还在，今天的调查机会已经结束。" if self.evidence else "桌上没有新的记录。工作单留下两个调查方向，今晚没有替它们填上答案。")
            self.node = "N96"
        elif choice == "continue":
            if self.node == "result": self.result_evidence = (); self.node = "N20" if self.slots else "N70"
            elif self.node == "N90": self.node = self.ending
            elif self.node in {"N91", "N92", "N93", "N94", "N95"}: self.node = "aftermath"
            else: self.node = "N99"
        return self.result_text

    def prepare_headline(self, text):
        if self.node != "N70": raise ValueError("not at editor")
        self.draft = text; self.headline_review = None; self.headline_message = ""
        authored = next((v for v in self.data["headlines"].values() if v["text"] == text.strip()), None)
        if authored is None or "claims" not in authored:
            self.headline_message = "原句已保留。当前脚本没有完整可执行的理解，请改写或明确选择另一版作者选稿。"; return False
        claims = authored["claims"]
        if not self._valid_headline(claims):
            self.headline_message = "原句已保留。完整标题中有当前尚未开放的含义或来源，整版尚不能签发。"; return False
        self._record("review_headline", text)
        self.headline_review = PreparedHeadline(text, json.dumps(claims, ensure_ascii=False), len(self.history), self._headline_basis())
        self.node = "N80"
        return True

    def _valid_headline(self, claims):
        validation = validate_headline_candidate({"status": "RESOLVED", "claims": claims}, self.headline_catalogue())
        if not validation.can_proceed: return False
        return all(not c.get("source_ref_id") or c["target_id"] in {FIRE, VIEW} and c["commitment_mode"] == "ASSERTED" for c in claims)

    def _validate_prepared_headline(self):
        review = self.headline_review
        # Only signoff navigation can occur after preparation; any gameplay mutation invalidates it.
        navigation = self.history[review.context_token:] if review else []
        if review is None or review.basis_json != self._headline_basis() or any(h["action"] not in {"signoff", "publish"} for h in navigation) or not self._valid_headline(json.loads(review.claims_json)):
            raise ValueError("headline review is stale or invalid")
        return json.loads(review.claims_json)

    def _headline_basis(self):
        return json.dumps({"evidence": self.evidence, "sources": sorted(self.sources),
            "cooperation": self.cooperation, "state": self.state.as_dict(),
            "versions": {k: self.data[k] for k in ("version", "catalogue_version", "support_version", "consequences_version")}},
            ensure_ascii=False, sort_keys=True)

    def _publish(self):
        claims = self._validate_prepared_headline()
        evaluations = evaluate_claims(self.data, claims, set(self.evidence))
        versions = {k: self.data[k] for k in ("version", "catalogue_version", "support_version", "consequences_version")}
        self.publication = ChapterPublicationSnapshot(self.headline_review.original_text, self.headline_review.claims_json,
            json.dumps(self.evidence, ensure_ascii=False, sort_keys=True), tuple(sorted(self.sources)),
            json.dumps(evaluations, sort_keys=True), json.dumps(versions, sort_keys=True),
            json.dumps(self.events, ensure_ascii=False, sort_keys=True), json.dumps(self.cooperation, sort_keys=True))
        self.ending, self.issues = self._outcome(claims, evaluations)
        self.outcome_text, self.people_text = self._consequences(claims, evaluations)
        if self.ending == "N91": self._event("professional_followup")
        elif self.ending == "N94": self._event("editorial_review")
        self.node = "N90"

    def _outcome(self, claims, evaluations):
        if not claims: return "N95", []
        qualifier = any(c["target_id"] == VIEW and c["polarity"] == "DENY"
                        and e["underlying"] == "SUPPORTED" for c, e in zip(claims, evaluations))
        issues = []
        for i, (c, e) in enumerate(zip(claims, evaluations)):
            if c.get("source_ref_id"):
                if e["attribution"] != "SUPPORTED": issues.append((i, "wrong_attribution"))
                elif c["target_id"] == FIRE and c["value_id"] == "SECURITY_FORCES" and c["polarity"] == "AFFIRM" and CLARIFICATION in self.evidence and not qualifier:
                    issues.append((i, "omitted_clarification"))
            elif e["underlying"] == "CONTRADICTED":
                issues.append((i, "contradicted_assertion" if c["commitment_mode"] == "ASSERTED" else "contradicted_question"))
            elif c["commitment_mode"] == "ASSERTED" and e["underlying"] == "INSUFFICIENT": issues.append((i, "insufficient_assertion"))
        if issues: return "N94", issues
        for c, e in zip(claims, evaluations):
            if c.get("source_ref_id") and e["underlying"] != "SUPPORTED":
                historical_with_context = c["target_id"] == FIRE and c["value_id"] == "SECURITY_FORCES" and c["polarity"] == "AFFIRM" and qualifier
                if not historical_with_context: return "N92", []
        if any(c["commitment_mode"] != "ASSERTED" for c in claims): return "N93", []
        return "N91", []

    def _consequences(self, claims, evaluations):
        copy = self.data["copy"]
        topics = {c["target_id"] for c in claims}
        fire = bool(topics & {FIRE, VIEW}); funding = bool(topics & {FUNDING, USES})
        parts = []; people = []
        supported = [(c, e) for c, e in zip(claims, evaluations) if e["underlying"] == "SUPPORTED" and c["commitment_mode"] == "ASSERTED" and e["attribution"] in {"SUPPORTED", "NOT_APPLICABLE"}]
        if self.ending == "N91":
            if any(c["target_id"] == FIRE and not c.get("source_ref_id") for c in claims): parts.append(copy["supported_fire"])
            if VIEW in topics:
                parts.append(copy["supported_view"])
                if any(c["target_id"] == FIRE and c.get("source_ref_id") for c in claims): parts.append(copy["historical_quote"])
            if FUNDING in topics: parts.append(copy["supported_payment"])
            if USES in topics: parts.append(copy["supported_uses"])
            if fire: parts.append(copy["reader_fire"])
            if funding: parts.append(copy["reader_payment"])
            parts.append(copy["professional_followup"])
        elif self.ending == "N92": parts.append(copy["contested_with_video" if VIDEO in self.evidence else "contested_without_video"])
        elif self.ending == "N93":
            questions = [(c, e) for c, e in zip(claims, evaluations) if c["commitment_mode"] != "ASSERTED"]
            parts.append(copy["question_without_record" if any(e["underlying"] == "INSUFFICIENT" for c, e in questions) else "question_with_record"])
            for c, e in questions:
                parts.append(describe_claim(c) + ("：这项尚未取得对应记录。" if e["underlying"] == "INSUFFICIENT" else "：这项已有对应记录。"))
        elif self.ending == "N94":
            parts.append(copy["review_open"])
            for i, issue in self.issues: parts.append(describe_claim(claims[i]) + "\n\n编辑：" + copy[issue])
            if supported: parts.append(copy["keep_supported"])
            if any(issue == "wrong_attribution" for i, issue in self.issues): parts.append(copy["source_correction"])
            if funding: parts.append(copy["funding_review"])
            if fire: parts.append(copy["fire_review"])
            parts.append(copy["review_close"])
        else: parts.append(copy["no_claim"])
        if self.ending in {"N92", "N93"} and supported:
            parts.append(copy["keep_other_claims"])
            parts.extend(describe_claim(c) + "；留存材料：" + "、".join(self.evidence[eid]["title"] for eid in basis_for(self.data, e) if eid in self.evidence) for c, e in supported)
        if fire:
            if any(issue == "wrong_attribution" for i, issue in self.issues): pass
            elif not self.cooperation["witness"]: people.append(copy["witness_closed"])
            elif any(issue == "omitted_clarification" for i, issue in self.issues): people.append(copy["witness_omitted"])
            elif CLARIFICATION in self.evidence:
                people.append(copy["witness_clarified" if any(c["target_id"] == VIEW and c["polarity"] == "DENY" for c, e in supported) else "witness_kept"])
            elif AUDIO in self.evidence: people.append(copy["witness_open"])
        funding_problem = any(claims[i]["target_id"] in {FUNDING, USES} for i, issue in self.issues)
        if funding and not funding_problem:
            if self.ending in {"N92", "N93"}: people.append(copy["company_question"])
            if not self.cooperation["clerk"]: people.append(copy["clerk_closed_with_ledger" if LEDGER in self.evidence else "clerk_closed_no_ledger"])
            elif CONTEXT in self.evidence: people.append(copy["uses_published" if USES in topics else "uses_known"])
            elif LEDGER in self.evidence: people.append(copy["uses_unknown"])
        return "\n\n".join(parts), "\n\n".join(people) or "没有新增来源回应；本版没有替你取得新的材料。"


def basis_for(data, evaluation):
    rows = set(evaluation["supporting_relationships"] + evaluation["contradicting_relationships"] + evaluation["attribution_relationships"])
    return sorted({eid for r in data["relationships"] if r["id"] in rows for eid in r["requires_evidence"]})


def describe_claim(claim):
    target, value = claim["target_id"], claim["value_id"]
    text = {FIRE: {"MILITIA": "民兵在主通道率先开火", "SECURITY_FORCES": "安保在主通道率先开火"},
            FUNDING: {"COMPANY_A": "Company A 为本次行动提供资金"},
            VIEW: {"FIRST_SHOT_VISIBLE": "阿岑在首枪发生时看见了开火来源"},
            USES: {"VEHICLES_LIGHTING_TEMP_LABOUR": "R17 行动账目列明车辆、照明与临时劳务"}}[target][value]
    if claim["polarity"] == "DENY": text = "否定“" + text + "”"
    if claim.get("source_ref_id"): text = "目击者说过：" + text
    return {"ASSERTED": "明确陈述：", "SPECULATIVE": "猜测：", "QUESTIONED": "提问："}[claim["commitment_mode"]] + text


class ChapterInterviewFlow(InterviewFlow):
    """Reuse staged review, immutable candidates, rewrite and current-context validation."""
    def __init__(self, session):
        super().__init__(session, self._scripted_source)
        self.draft = ""

    def _active(self): return self.session.node in self.session.data["scripts"] and not self.session.finished
    def _context_token(self): return self.session.revision
    def _catalogue(self): return self.session.dialogue_catalogue()

    def _scripted_source(self, text):
        item = next((s for s in self.session.available_scripts() if s["text"] == text.strip()), None)
        return deepcopy(item["candidate"]) if item else None

    def _choice(self, candidate, text):
        return next((s["id"] for s in self.session.available_scripts() if s["text"] == text.strip() and s["candidate"] == candidate), None)

    def _execute(self, review):
        return self.session.choose("leave") if review.choice_id == "leave" else self.session.execute_script(review.choice_id, review.candidate)

    def review_lines(self):
        if self.review.choice_id == "leave":
            return ("不发送保留的草稿。", "不采用初访，不取得录音。" if self.session.node == "N10" else "结束本次访问，用一段调查时间，不取得新材料。")
        candidate = self.review.candidate
        action = {FIRE: "询问本次冲突谁先开火", FUNDING: "询问本次行动谁付款", VIEW: "核对目击者首枪时的位置与可见范围",
                  USES: "询问 R17 科目代码的具体名称", "PROP_R17_RECORDS_FIRE_ORDER": "核对这份账是否能说明开火命令",
                  "REQ_HAND_OVER_LEDGER": "请求交付付款账页副本", "DEAL_LEDGER_FOR_500": "提出支付500换账页副本；还未成交"}
        lines = ["行动：" + ({"ACCEPT": "接受当前唯一交易，支付500并取得副本", "REFUSE": "拒绝当前交易并结束本次访问"}.get(candidate["act"]) or action[candidate["target_id"]])]
        lines.extend(TACTIC_LABELS[t] for t in candidate["tactics"])
        if not candidate["tactics"]: lines.append("策略：没有附加施压、指控或旁敲侧击。")
        lines.extend("提及材料：" + self.session.evidence[e]["title"] for e in candidate["evidence_ref_ids"])
        if not candidate["evidence_ref_ids"]: lines.append("提及材料：没有引用已知证据。")
        lines.append("确认才执行此项行动；不会承诺替来源刊发或保证其说法真实。")
        return tuple(lines)
