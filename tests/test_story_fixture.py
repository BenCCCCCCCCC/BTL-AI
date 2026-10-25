import json

import pytest

from ai.prototype.story_fixture import StorySession, evaluate_publication


@pytest.mark.parametrize("choices,ending,money,reputation", [
    (["record", "video", "militia", "publish"], "SUPPORTED_REPORT", 600, 1),
    (["record", "video", "attributed", "publish"], "CONTESTED_ATTRIBUTION", 600, 0),
    (["record", "clerk", "offer500", "accept", "funding", "publish"], "SUPPORTED_REPORT", 100, 1),
    (["record", "clerk", "request", "funding", "publish"], "UNSUPPORTED_REPORT", 600, -1),
    (["record", "desk", "security", "publish"], "SUPPORTED_REPORT", 600, 1),
    (["leave", "desk", "militia", "publish"], "UNSUPPORTED_REPORT", 600, -1),
    (["leave", "video", "neutral", "publish"], "NO_CLAIM", 600, 0),
    (["record", "clerk", "offer500", "refuse", "hold"], "HELD", 600, 0),
])
def test_distinct_authored_paths(choices, ending, money, reputation):
    session = StorySession()
    for choice in choices:
        session.choose(choice)
    assert session.ending == ending
    assert session.state.money == money and session.state.reputation == reputation
    with pytest.raises(ValueError):
        session.choose("publish")  # no repeated consequence from the same publication


def test_later_evidence_and_hidden_oracle_do_not_rewrite_publication_snapshot():
    session = StorySession()
    for choice in ["record", "desk", "security", "publish"]:
        session.choose(choice)
    snapshot = session.publication
    assert json.loads(snapshot.evaluation_json)[0]["underlying"] == "SUPPORTED"
    session.evidence.add("EV_VIDEO_A")
    session.story["author_only_oracle"]["PROP_FIRE_FIRST"] = "SECURITY_FORCES"
    now = evaluate_publication(session.story, json.loads(snapshot.claims_json), session.evidence)
    assert now[0]["underlying"] == "INSUFFICIENT"
    assert session.publication == snapshot
    assert snapshot.evidence_ids == ("EV_AUDIO_A",)


def test_pressure_and_headline_edit_have_only_authored_effects():
    session = StorySession()
    for choice in ["pressure", "video", "security", "edit", "militia"]:
        session.choose(choice)
    assert session.state.threat_level == 1
    assert session.state.reputation == 0 and session.publication is None
    session.choose("publish")
    assert session.state.reputation == 1
    assert session.publication.headline == "民兵在货场率先开火"
