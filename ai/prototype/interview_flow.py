"""Experimental player-confirmed interview, using exact scripted lines, never NLP.

Candidates use Frozen Dialogue fields and the existing validator. This local
controller stages a player's confirmation; only StorySession applies effects.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from typing import Callable

from .story_fixture import StorySession
from .validation import RuntimeCatalogue, TargetDefinition, validate_dialogue_candidate


@dataclass(frozen=True)
class ScriptedLine:
    label: str
    text: str
    tactics: tuple[str, ...] = ()
    ambiguous: bool = False


SCRIPTED_LINES = (
    ScriptedLine("如实询问", "我会记录你的原话。你看到的是谁先开火？"),
    ScriptedLine("施压追问", "你最好说清楚是谁先开火，否则我会把你的名字写出来。", ("THREAT",)),
    ScriptedLine("复合语气", "你似乎在隐瞒，你在误导我。是谁先开火？不说清楚我就公开你的名字。",
                 ("INDIRECT_PROBE", "ACCUSATION", "THREAT")),
    ScriptedLine("含糊表达", "他说的那个呢？", ambiguous=True),
)
TACTIC_LABELS = {"THREAT": "施压：以公开名字作为不配合的后果。",
                 "ACCUSATION": "指控：指责对方在误导你。",
                 "INDIRECT_PROBE": "旁敲侧击：暗示对方隐瞒，试图引出回答。"}


def scripted_candidate(text: str) -> dict | None:
    """Exact sample lookup only. Edited unknown text is not guessed or classified."""
    script = next((s for s in SCRIPTED_LINES if s.text == text.strip()), None)
    if script is None:
        return None
    if script.ambiguous:
        return {"status": "AMBIGUOUS", "reason": "AMBIGUOUS_REFERENCE"}
    return {"status": "RESOLVED", "act": "QUESTION", "target_id": "PROP_FIRE_FIRST",
            "tactics": list(script.tactics), "evidence_ref_ids": []}


def interview_catalogue(session: StorySession) -> RuntimeCatalogue:
    # Existing shared meaning, locally exposed for this one authored interview.
    targets = {} if session.node != "interview" or session.ending else {
        "PROP_FIRE_FIRST": TargetDefinition(allowed_acts=frozenset({"QUESTION"}),
            allowed_tactics=frozenset(TACTIC_LABELS))}
    return RuntimeCatalogue(targets=targets, visible_evidence_ids=frozenset(session.evidence),
                            visible_source_ids=frozenset(session.sources))


def authored_choice(candidate: dict) -> str | None:
    """Translate only the two supported authored routes; never discard extra fields."""
    if (candidate.get("status"), candidate.get("act"), candidate.get("target_id")) != (
            "RESOLVED", "QUESTION", "PROP_FIRE_FIRST"):
        return None
    if "value_id" in candidate or "polarity" in candidate:
        return None
    tactics = set(candidate.get("tactics", ()))
    if not tactics:
        return "record"
    return "pressure" if "THREAT" in tactics else None


@dataclass(frozen=True)
class PreparedInterview:
    original_text: str
    candidate_json: str | None
    choice_id: str
    context_token: object = None

    @property
    def candidate(self) -> dict | None:
        return json.loads(self.candidate_json) if self.candidate_json is not None else None


@dataclass(frozen=True)
class InterviewReceipt:
    original_text: str
    choice_id: str
    response: str


class InterviewFlow:
    def __init__(self, session: StorySession,
                 source: Callable[[str], dict | None] = scripted_candidate):
        self.session = session
        self.source = source
        self.draft = SCRIPTED_LINES[0].text
        self.review: PreparedInterview | None = None
        self.message = ""
        self.receipt: InterviewReceipt | None = None

    def _active(self) -> bool:
        return self.session.node == "interview" and not self.session.ending

    def _catalogue(self):
        return interview_catalogue(self.session)

    def _choice(self, candidate, text):
        return authored_choice(candidate)

    def _context_token(self):
        return None

    def _execute(self, review):
        response = self.session.choose(review.choice_id)
        if review.choice_id == "record":
            response = "目击者 A：『" + self.session.story["characters"]["NPC_WITNESS_A"]["authorised_statement"] + "』"
        return response

    def edit(self, text: str | None = None):
        if text is not None:
            self.draft = text
        self.review = None
        self.message = ""

    def prepare(self, text: str) -> bool:
        self.edit(text)
        if not self._active():
            raise ValueError("interview is no longer available")
        if not text.strip():
            self.message = "先写一句你想说的话，或载入一条离线示例。"
            return False
        candidate = self.source(text)
        if candidate is None:
            self.message = "原句已保留。这段文字不在离线脚本中，当前没有系统理解可供确认。请载入示例体验流程。"
            return False
        result = validate_dialogue_candidate(candidate, self._catalogue())
        if not result.can_proceed:
            self.message = ("还不能确定“那个”指什么。原句已保留，请返回改写或载入另一条示例。"
                            if candidate.get("status") == "AMBIGUOUS" else
                            "这次没有可执行的系统理解。原句已保留，采访尚未发生。")
            return False
        choice = self._choice(candidate, text)
        if choice is None:
            self.message = "这层含义目前还不能执行。原句已保留，采访尚未发生。"
            return False
        self.review = PreparedInterview(text, json.dumps(deepcopy(candidate)), choice, self._context_token())
        return True

    def prepare_leave(self):
        if not self._active():
            raise ValueError("interview is no longer available")
        self.review = PreparedInterview(self.draft, None, "leave", self._context_token())
        self.message = ""

    def confirm(self) -> InterviewReceipt:
        review = self.review
        if review is None or not self._active():
            raise ValueError("no current interview to confirm")
        if review.context_token != self._context_token():
            self.review = None
            self.message = "采访条件已经变化。原句已保留，请重新复核。"
            raise ValueError("review context is stale")
        candidate = review.candidate
        if candidate is not None:
            result = validate_dialogue_candidate(candidate, self._catalogue())
            if not result.can_proceed or self._choice(candidate, review.original_text) != review.choice_id:
                self.review = None
                self.message = "采访条件已经变化。原句已保留，请重新复核。"
                raise ValueError("review is no longer valid")
        response = self._execute(review)
        self.receipt = InterviewReceipt(review.original_text, review.choice_id, response)
        self.review = None
        return self.receipt


def review_lines(review: PreparedInterview, evidence_names: dict[str, str]) -> tuple[str, ...]:
    if review.choice_id == "leave":
        return ("不发送这段草稿，不采用这次采访。", "直接转入最后一次调查；不会取得采访录音。")
    candidate = review.candidate
    result = ["行动：向目击者询问货场冲突中，谁先开火。"]
    tactics = candidate.get("tactics", ())
    result.extend(TACTIC_LABELS[t] for t in tactics)
    if not tactics:
        result.append("策略：没有附加施压、指控或旁敲侧击。")
    evidence = candidate.get("evidence_ref_ids", ())
    result.extend("提及材料：" + evidence_names[e] for e in evidence)
    if not evidence:
        result.append("提及材料：没有引用证据。")
    result.append("你的选择：采用这次采访，记录对方原话；没有承诺替他刊发。")
    return tuple(result)
