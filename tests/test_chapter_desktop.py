"""One new Tk integration route; does not repeat the old story's GUI cases."""
import json
import tkinter as tk

from ai.prototype.chapter_desktop import ChapterDesktop, chapter_evidence_entries
from ai.prototype.chapter_session import CLARIFICATION, LEDGER


def test_chapter_window_reuses_confirmation_reader_archive_and_restart():
    root = tk.Tk(); root.withdraw()
    try:
        app = ChapterDesktop(root)
        app.start(); app.choose("begin")
        app.draft_entry.delete("1.0", "end"); app.draft_entry.insert("1.0", "未接通的自写问题e1")
        app._prepare_interview()
        assert app.interview.review is None and not app.session.evidence
        original = app.draft_entry.get("1.0", "end-1c")
        app._toggle_evidence(); app._toggle_evidence()
        assert app.draft_entry.get("1.0", "end-1c") == original
        app._load_script("如实询问"); app._prepare_interview(); app._rewrite_interview()
        assert not app.session.evidence
        app._prepare_interview(); app._confirm_interview(); app.choose("continue")
        app.choose("visit:A"); app.choose("enter"); app.choose("save_video"); app.choose("continue")
        app.choose("visit:S-A"); app.choose("enter")
        app._load_script("指出矛盾"); app._prepare_interview(); app._confirm_interview()
        assert CLARIFICATION in app.session.evidence
        app.choose("continue"); app.choose("visit:B"); app.choose("enter")
        app._load_script("提出500交易"); app._prepare_interview(); app._confirm_interview()
        assert app.session.pending and app.session.state.money == 600
        app._prepare_interview(); app._confirm_interview()
        assert LEDGER in app.session.evidence and app.session.state.money == 100
        app.choose("continue")
        assert app.session.node == "N70"
        app._load_headline(app.session.data["headlines"]["H12"]["text"])
        app._toggle_evidence(); app._toggle_evidence()
        assert "后补充" in app.draft_entry.get("1.0", "end-1c")
        app._prepare_headline(); app.choose("signoff"); app.choose("publish")
        for _ in range(3): app.choose("continue")
        assert app.session.finished and app.session.ending == "N91"
        assert len(chapter_evidence_entries(app.session)) == 4
        assert json.loads(app.session.publication.evaluation_json)[0]["underlying"] == "CONTRADICTED"
        app._toggle_log(); root.update()
        app.restart()
        assert not app.started and app.session.slots == 3 and app.session.state.money == 600
        assert not app.session.evidence and not app.session.events and app.session.publication is None
        assert app.session.pending is None and all(app.session.cooperation.values())
    finally:
        root.destroy()


def test_transaction_acknowledgement_and_long_material_begin_at_first_line():
    root = tk.Tk()
    try:
        app = ChapterDesktop(root); app.start(); app.choose("begin")
        app._prepare_interview(); app._confirm_interview(); app.choose("continue")
        app.choose("visit:B"); app.choose("enter")
        app._load_script("提出500交易"); app._prepare_interview(); app._confirm_interview()
        assert "只交纸上已有的记录" in app._interview_text()
        app._prepare_interview(); app._confirm_interview(); app.choose("continue")
        app.choose("visit:S-B"); app.choose("enter")
        app._prepare_interview(); app._confirm_interview(); root.update()
        assert app.session.node == "result" and app.session.result_evidence
        assert app.content.winfo_height() > app.scroll.winfo_height()
        assert app.scroll.yview()[0] == 0
        assert app.session.state.money == 100 and app.session.slots == 1
    finally:
        root.destroy()
