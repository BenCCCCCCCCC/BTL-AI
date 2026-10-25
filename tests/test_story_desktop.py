"""Player projection boundaries introduced by the desktop view; no duplicate rules tests."""
from ai.prototype.story_desktop import evidence_entries, page_for
from ai.prototype.story_fixture import StorySession


def test_player_view_hides_unacquired_materials_and_internal_deal_fields():
    session = StorySession()
    assert evidence_entries(session) == ()
    session.choose("record")
    assert [entry[0] for entry in evidence_entries(session)] == ["采访录音"]
    session.choose("clerk")
    session.choose("offer500")
    page = page_for(session)
    assert "PENDING_" not in page.body and "300" not in page.body
    assert "付款后余下 100" in page.body
    assert session.state.money == 600  # merely reading the offer cannot execute it


def test_player_archive_reads_publication_snapshot_not_later_knowledge():
    session = StorySession()
    for choice in ["record", "desk", "security", "publish"]:
        session.choose(choice)
    session.evidence.add("EV_VIDEO_A")
    assert [entry[0] for entry in evidence_entries(session, published=True)] == ["采访录音"]
    page = page_for(session)
    assert page.headline == session.publication.headline
    assert page.choices == ()
