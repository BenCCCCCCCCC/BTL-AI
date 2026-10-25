"""Only the new chapter's rules and integration boundaries; no model requests."""
from copy import deepcopy
from dataclasses import FrozenInstanceError
import json

import pytest

from ai.prototype.chapter_session import (
    ChapterSession, ChapterInterviewFlow, AUDIO, VIDEO, LEDGER, CLARIFICATION, CONTEXT,
    FIRE, FUNDING, VIEW, SOURCE, evaluate_claims,
)


def act(session, script_id, *, read=True):
    flow = ChapterInterviewFlow(session)
    script = next(s for s in session.available_scripts() if s["id"] == script_id)
    assert flow.prepare(script["text"])
    receipt = flow.confirm()
    if read and session.node == "result": session.choose("continue")
    return receipt


def start(record=True):
    s = ChapterSession(); s.choose("begin")
    if record: act(s, "record")
    else: s.choose("leave"); s.choose("continue")
    return s


def visit(s, scene):
    s.choose("visit:" + scene); s.choose("enter")


def video(s):
    visit(s, "A"); s.choose("save_video"); s.choose("continue")


def ledger(s):
    visit(s, "B"); act(s, "offer500"); act(s, "accept")


def desk(s):
    if s.node == "N20": s.choose("desk"); s.choose("finish_investigation")
    assert s.node == "N70"


def publish(s, title):
    desk(s)
    assert s.prepare_headline(s.data["headlines"][title]["text"])
    s.choose("signoff"); s.choose("publish")
    assert s.node == "N90"
    for _ in range(3): s.choose("continue")
    assert s.finished


def test_two_main_lines_and_funding_branch_publish_two_complete_atoms_once():
    s = start(); ledger(s); visit(s, "S-B"); act(s, "codes"); video(s)
    assert s.slots == 0 and s.node == "N70" and len(s.evidence) == 4
    publish(s, "H10")
    assert s.state.money == 100 and s.state.reputation == 1 and s.state.public_opinion == 0
    assert len(json.loads(s.publication.claims_json)) == 2
    assert "R17" in s.outcome_text and "编辑向 Company A 回复" in s.people_text
    assert [e["id"] for e in s.events] == ["ledger_purchase", "professional_followup"]
    with pytest.raises(ValueError): s.choose("publish")
    assert s.state.money == 100 and s.state.reputation == 1


@pytest.mark.parametrize("title", ["H9", "H11", "H12"])
def test_witness_branch_makes_distinct_reportable_clarification(title):
    s = start(); video(s); visit(s, "S-A"); act(s, "contradiction")
    assert s.slots == 1
    assert "我不能拿看不见的那一边作保证" in s.evidence[CLARIFICATION]["text"]
    assert "就在这里" not in s.evidence[CLARIFICATION]["text"]
    original = s.evidence[AUDIO]["text"]
    publish(s, title)
    assert s.ending == "N91" and s.state.reputation == 1
    assert s.evidence[AUDIO]["text"] == original
    assert "看不到的也写清楚" in s.people_text
    if title == "H12":
        e = json.loads(s.publication.evaluation_json)
        assert e[0]["attribution"] == "SUPPORTED" and e[0]["underlying"] == "CONTRADICTED"
        assert e[1]["attribution"] == e[1]["underlying"] == "SUPPORTED"


@pytest.mark.parametrize("clarify,expected,delta", [(False, "N92", 0), (True, "N94", -1)])
def test_old_quote_and_known_clarification_have_separate_responsibility(clarify, expected, delta):
    s = start(); video(s)
    if clarify: visit(s, "S-A"); act(s, "position")
    publish(s, "H3")
    assert s.ending == expected and s.state.reputation == delta
    assert json.loads(s.publication.evaluation_json)[0]["attribution"] == "SUPPORTED"
    assert ("省掉了它" in s.outcome_text) == clarify


def test_request_offer_cancel_refuse_costs_only_one_scene_and_no_money():
    s = start(); visit(s, "B"); act(s, "request")
    assert s.node == "N50" and s.slots == 3 and LEDGER not in s.evidence
    act(s, "offer500"); assert s.pending and s.state.money == 600
    stale = ChapterInterviewFlow(s)
    assert stale.prepare(s.available_scripts()[0]["text"])
    s.choose("cancel_pending")
    with pytest.raises(ValueError): stale.confirm()
    act(s, "offer500"); act(s, "refuse")
    assert s.slots == 2 and s.pending is None and s.state.money == 600 and LEDGER not in s.evidence
    assert "B" not in s.available_scenes()


def test_entry_cancel_mid_branch_exit_and_deadline_are_not_refundable():
    s = start(); s.choose("visit:A"); s.choose("cancel_entry")
    assert s.slots == 3 and not s.visited
    video(s); visit(s, "S-A"); s.choose("leave"); s.choose("continue")
    assert s.slots == 1 and CLARIFICATION not in s.evidence and "S-A" not in s.available_scenes()
    ledger(s)
    assert s.node == "N70" and s.slots == 0 and s.publication is None
    with pytest.raises(ValueError): s.choose("visit:S-B")


def test_two_pressures_close_sources_preserve_original_and_have_independent_events():
    s = ChapterSession(); s.choose("begin"); act(s, "compound")
    assert "别再来问我" in s.evidence[AUDIO]["text"]
    assert "我看见他们举枪" not in s.evidence[AUDIO]["text"]
    visit(s, "B"); act(s, "pressure"); video(s)
    assert not any(s.cooperation.values()) and s.state.threat_level == 2
    assert "S-A" not in s.available_scenes()
    publish(s, "H1")
    assert s.state.reputation == 1 and s.state.threat_level == 2
    assert s.state.money == 600 and s.state.public_opinion == 0
    assert "不会再接受你的采访" in s.people_text


def test_script_failure_and_rewrite_cannot_grant_material_or_consume_time():
    s = start(); visit(s, "S-B") if "S-B" in s.available_scenes() else visit(s, "B")
    before = (s.revision, s.slots, deepcopy(s.evidence), s.state, deepcopy(s.history))
    flow = ChapterInterviewFlow(s)
    for text in ["我付300，拿到账页", "他说的那个呢？", "给我账页并告诉我谁下令"]:
        assert not flow.prepare(text) and flow.draft == text
        with pytest.raises(ValueError): flow.confirm()
    assert before == (s.revision, s.slots, s.evidence, s.state, s.history)
    assert flow.prepare(s.available_scripts()[0]["text"])
    flow.edit()
    with pytest.raises(ValueError): flow.confirm()
    assert before == (s.revision, s.slots, s.evidence, s.state, s.history)


def test_headline_current_catalogue_failure_and_unsupported_extra_clause_are_atomic():
    s = start(); ledger(s); desk(s)
    for text in [s.data["headlines"]["H10"]["text"], s.data["headlines"]["UNSUPPORTED_ORDER"]["text"], "自己写的未接通标题"]:
        assert not s.prepare_headline(text)
        assert s.draft == text and s.node == "N70" and s.publication is None
    assert s.state.money == 100 and s.state.reputation == 0
    s.choose("hold_review"); s.choose("hold"); s.choose("continue")
    assert s.finished and s.ending == "N96" and s.publication is None
    assert "Company A 来信" not in s.outcome_text


def test_zero_claim_is_actual_publication_and_archive_freezes_text_versions_and_costs():
    s = start(); publish(s, "H8")
    snap = s.publication
    assert s.ending == "N95" and json.loads(snap.claims_json) == []
    assert len(json.loads(snap.versions_json)) == 4
    text = snap.evidence_json
    s._grant(VIDEO); s.evidence[AUDIO]["text"] = "later change"
    s.data["support_version"] = "later"
    assert snap.evidence_json == text and VIDEO not in snap.evidence_ids
    assert "later" not in snap.versions_json and not s.events
    with pytest.raises(FrozenInstanceError): snap.headline = "changed"


def test_source_error_is_catalogue_legal_but_not_repaired_by_world_evidence():
    s = start(); video(s); publish(s, "SOURCE_ERROR")
    e = json.loads(s.publication.evaluation_json)[0]
    assert e["underlying"] == "SUPPORTED" and e["attribution"] == "INSUFFICIENT"
    assert s.ending == "N94" and "那句话不是我说的" in s.outcome_text


def test_mixed_claim_issue_cannot_be_hidden_by_supported_or_questioned_atom():
    s = start(); video(s); desk(s)
    h = deepcopy(s.data["headlines"]["H5"])
    s.data["headlines"]["MIXED"] = h
    h["text"] = "民兵在货场率先开火，Company A 为行动提供资金"
    assert s.prepare_headline(h["text"])
    s.choose("signoff"); s.choose("publish")
    assert s.ending == "N94" and len(json.loads(s.publication.claims_json)) == 2
    assert "另一项已经取得的材料照常保留" in s.outcome_text
    assert s.state.reputation == -1


def test_negation_and_modes_use_same_evidence_and_unsupported_testimony_is_not_truth():
    s = start()
    sec = s.data["headlines"]["H2"]["claims"][0]
    assert evaluate_claims(s.data, [sec], set(s.evidence))[0]["underlying"] == "INSUFFICIENT"
    denied = dict(sec, polarity="DENY", commitment_mode="QUESTIONED")
    assert evaluate_claims(s.data, [denied], {VIDEO})[0]["underlying"] == "SUPPORTED"
    publish(s, "H6")
    assert s.ending == "N93" and s.state.reputation == 0 and "尚未取得对应记录" in s.outcome_text


def test_prepared_headline_is_invalidated_by_edit_and_basis_change():
    s = start(); video(s); desk(s)
    assert s.prepare_headline(s.data["headlines"]["H1"]["text"])
    s.choose("edit")
    with pytest.raises(ValueError): s.choose("publish")
    assert s.prepare_headline(s.draft); s.choose("signoff")
    s.evidence.pop(VIDEO)
    before = (s.revision, deepcopy(s.history), s.state)
    with pytest.raises(ValueError): s.choose("publish")
    assert s.publication is None and before == (s.revision, s.history, s.state)
