"""New staged-interview boundaries; not a rerun of model or story baselines."""
import pytest

from ai.prototype.interview_flow import InterviewFlow, SCRIPTED_LINES, review_lines, scripted_candidate
from ai.prototype.story_fixture import StorySession


def state_of(session):
    return (session.node, frozenset(session.evidence), frozenset(session.sources),
            session.state, tuple(session.history), session.publication, session.ending)


def test_preview_and_return_to_rewrite_preserve_original_without_executing():
    session = StorySession()
    flow = InterviewFlow(session)
    before = state_of(session)
    original = "  " + SCRIPTED_LINES[1].text + "\n"
    assert flow.prepare(original)
    assert flow.review.original_text == original
    assert state_of(session) == before
    flow.edit()
    assert flow.review is None and flow.draft == original
    with pytest.raises(ValueError):
        flow.confirm()  # returning to edit invalidates the old confirmation
    assert state_of(session) == before


def test_explicit_confirmation_executes_pressure_only_once():
    session = StorySession()
    flow = InterviewFlow(session)
    assert flow.prepare(SCRIPTED_LINES[1].text)
    assert session.state.threat_level == 0 and not session.evidence
    receipt = flow.confirm()
    assert receipt.original_text == SCRIPTED_LINES[1].text
    assert session.node == "followup" and session.history == ["pressure"]
    assert session.state.threat_level == 1 and session.evidence == {"EV_AUDIO_A"}
    after = state_of(session)
    with pytest.raises(ValueError):
        flow.confirm()
    assert state_of(session) == after


@pytest.mark.parametrize("text,source", [
    ("e1 我想问另一件事", scripted_candidate),
    (SCRIPTED_LINES[3].text, scripted_candidate),
    ("保留这句", lambda text: {"status": "RESOLVED", "act": "QUESTION", "target_id": "MISSING"}),
])
def test_unresolved_or_invalid_script_preserves_draft_and_cannot_confirm(text, source):
    session = StorySession()
    before = state_of(session)
    flow = InterviewFlow(session, source)
    assert not flow.prepare(text)
    assert flow.draft == text and flow.message and flow.review is None
    with pytest.raises(ValueError):
        flow.confirm()
    assert state_of(session) == before


def test_confirmation_copy_keeps_all_tactics_and_known_evidence_visible():
    session = StorySession()
    session.evidence.add("EV_AUDIO_A")  # controlled known-evidence context for the projection
    candidate = scripted_candidate(SCRIPTED_LINES[2].text)
    candidate["evidence_ref_ids"] = ["EV_AUDIO_A"]
    flow = InterviewFlow(session, lambda text: candidate)
    assert flow.prepare(SCRIPTED_LINES[2].text)
    copy = "\n".join(review_lines(flow.review, {"EV_AUDIO_A": "采访录音"}))
    assert all(label in copy for label in ["施压", "指控", "旁敲侧击", "采访录音", "谁先开火"])
    assert not any(internal in copy for internal in ["PROP_", "EV_", "THREAT", "author_only_oracle"])
    # An immutable review retains the candidate actually shown, not a later source mutation.
    candidate["tactics"].clear()
    assert len(flow.review.candidate["tactics"]) == 3


def test_leaving_is_an_explicit_authored_choice_and_does_not_send_the_draft():
    session = StorySession()
    flow = InterviewFlow(session)
    flow.edit("尚未发送的自写草稿")
    before = state_of(session)
    flow.prepare_leave()
    assert state_of(session) == before and flow.draft == "尚未发送的自写草稿"
    assert "不发送" in review_lines(flow.review, {})[0]
    flow.confirm()
    assert session.node == "followup" and not session.evidence and session.history == ["leave"]


def test_confirmation_revalidates_current_visible_evidence():
    session = StorySession()
    session.evidence.add("EV_AUDIO_A")
    candidate = scripted_candidate(SCRIPTED_LINES[0].text)
    candidate["evidence_ref_ids"] = ["EV_AUDIO_A"]
    flow = InterviewFlow(session, lambda text: candidate)
    flow.prepare(SCRIPTED_LINES[0].text)
    session.evidence.clear()
    before = state_of(session)
    with pytest.raises(ValueError):
        flow.confirm()
    assert state_of(session) == before and flow.review is None and flow.draft
