"""Playable railyard chapter v1.0 using the existing Tk reader and interview flow."""
from __future__ import annotations

import json
from types import SimpleNamespace
import tkinter as tk
from tkinter import ttk

from .chapter_session import ChapterSession, ChapterInterviewFlow, SCENE_LABELS, AUDIO, VIDEO, LEDGER, CLARIFICATION, CONTEXT, describe_claim
from .story_desktop import StoryDesktop, PAPER, SHEET, INK, RED, RULE, MUTED


def chapter_evidence_entries(session):
    materials = json.loads(session.publication.evidence_json) if session.publication else session.evidence
    return tuple((m["title"], m["origin"], m["text"]) for m in materials.values())


class ChapterDesktop(StoryDesktop):
    def __init__(self, root):
        self.interview_node = None
        self.scene_drafts = {}
        self.menu = None
        self.show_log = False
        self.background_open = False
        super().__init__(root, session=ChapterSession(), interview_factory=ChapterInterviewFlow)
        root.title("截稿前的货场 | 脚本样章 v1.0")

    def _script_samples(self):
        return tuple(SimpleNamespace(label=s["label"], text=s["text"]) for s in self.session.available_scripts())

    def _interview_title(self):
        return self.session.data["nodes"][self.session.node]["title"]

    def _interview_text(self):
        text = self.scene_text()
        if self.session.result_text:
            text += "\n\n刚才的回应\n" + self.session.result_text
        return text

    def _review_copy(self):
        return self.interview.review_lines()

    def _leave_label(self):
        return "不采用初访，准备离开" if self.session.node == "N10" else "结束访问 · 用一段，不取新材料" if self.session.node != "N51" else ""

    def _capture_draft(self):
        if self.draft_entry is not None:
            text = self.draft_entry.get("1.0", "end-1c")
            if self.session.node == "N70": self.session.draft = text
            else:
                if text != self.interview.draft: self.interview.edit(text)
                self.scene_drafts[self.session.node] = text

    def render(self):
        for widget in self.content.winfo_children(): widget.destroy()
        self.draft_entry = None
        self.choice_buttons = []
        self.scroll.yview_moveto(0)
        self.money.configure(text=f"随身资金  {self.session.state.money}\n剩余调查  {self.session.slots} 段")
        self.evidence_button.configure(text=f"证据册  {len(self.session.evidence)}  [E]", state="normal" if self.started else "disabled")
        self.side_note.configure(text="先听原话，再决定怎样写。\n阅读、改写、复核不计时。\n每场调查结算一段。" if self.started else "三段调查，两条深入方向。\n为这一版标题负责。")
        if self.reading_evidence: self._render_evidence()
        elif not self.started: self._render_cover()
        elif self.session.node in self.session.data["scripts"]:
            if self.interview_node != self.session.node:
                self.interview_node = self.session.node
                self.interview.edit(self.scene_drafts.get(self.session.node, self._script_samples()[0].text))
            self._render_interview()
            if not self.interview.review:
                self._render_background()
                if self.session.node == "N51": self._choices(self.session.choices())
        elif self.session.node == "N70": self._render_editor()
        else: self._render_chapter()
        self.root.update_idletasks()
        self.scroll.configure(scrollregion=self.scroll.bbox("all"))
        self.scroll.yview_moveto(0)

    def _render_cover(self):
        self._label("首案 / 脚本可玩样章 v1.0", size=11, color=RED)
        self._label("截稿前\n的货场", size=36, serif=True, pady=(12, 24))
        self._rule()
        self._label("有限的调查时间，一句要承担后果的标题。", size=18, serif=True)
        self._label("先采访，再分配三段调查。核查现场，追查资金，或把时间用来说明已经发现的疑点。你可以刊发，也可以暂缓。", size=14)
        self._choices([("start", "进入案件 →")])
        self._label("采访与标题使用标明的离线脚本；脚本外文字保留，不猜测执行。\n无模型请求；关闭不保存。20–30分钟为目标，实际体验时长尚未验证。", size=10, color=MUTED)

    def scene_text(self):
        node = self.session.node
        text = self.session.data["nodes"].get(node, {}).get("text", "")
        text = text.format(slots=self.session.slots, money=self.session.state.money, after_money=self.session.state.money-500)
        if node == "N70":
            e = self.session.evidence
            if VIDEO in e and LEDGER in e: extra = "你拿到了两个方向的记录。放在同一句里，就得分别为两句话负责。"
            elif VIDEO in e: extra = "这一版可以围绕经过来写。另一个方向没拿到记录，就在工作笔记里留着。"
            elif LEDGER in e: extra = "你带回的是付款记录。别让标题比这张纸走得更远。"
            elif AUDIO in e: extra = "你有一位受访者的原话。写之前，想清楚是在引用他，还是由报纸作判断。"
            else: extra = "这次没有取得可用记录。你可以改写这一版的表达，也可以暂缓。"
            text += "\n\n编辑：" + extra
        return text

    def _render_background(self):
        questions = self.session.data["nodes"].get(self.session.node, {}).get("background", {})
        if not questions: return
        self._rule()
        self._button(self.content, "背景询问 · 不取材料，不计时" if not self.background_open else "收起背景询问", self._toggle_background).pack(fill="x", pady=(0, 8))
        if self.background_open:
            for label in questions:
                self._button(self.content, label, lambda key=label: self._background(key)).pack(fill="x", pady=(0, 7))

    def _toggle_background(self):
        self._capture_draft(); self.background_open = not self.background_open; self.render()

    def _background(self, label):
        self._capture_draft(); self.interview.edit()
        self.session.background(label); self.render()

    def _choices(self, choices):
        for cid, label in choices:
            button = self._button(self.content, label, lambda c=cid: self.choose(c), primary=cid in {"start", "begin", "save_video", "publish", "hold"})
            button.pack(fill="x", pady=(0, 10)); self.choice_buttons.append(button)
        if self.choice_buttons:
            # A new reading page begins at its first line, even when Continue is below the fold.
            if self.session.node in {"result", "N91", "N92", "N93", "N94", "N95", "N96", "aftermath"}:
                self.scroll.focus_set()
            else:
                self.choice_buttons[0].focus_set()

    def _render_chapter(self):
        s = self.session; n = s.node
        special = {"entry": "确认本次调查", "desk_confirm": "结束这一版的调查？", "result": "已执行 · 留下这份记录", "aftermath": "人物与这版报道", "N91": "这一版，有材料可循", "N92": "他说过，事实仍待核查", "N93": "一个问题留下的责任", "N94": "刊发之后，开始补救", "N95": "城市仍在等待答案", "N96": "这一版没有刊发"}
        title = special.get(n, s.data["nodes"].get(n, {}).get("title", "货场调查"))
        self._label("首案 / " + ("余波" if s.ending else "进行中"), size=11, color=RED)
        self._label(title, size=26, serif=True); self._rule()
        if n == "entry":
            body = SCENE_LABELS[s.entry_scene] + "\n\n进入前可免费返回。进场后，取得材料或确认结束访问会用一段；读材料和改写不逐句耗时。"
        elif n == "desk_confirm": body = f"还有 {s.slots} 段。确认后结束剩余调查机会，回到编辑台；不会自动刊发。"
        elif n == "result": body = s.result_text
        elif n in {"N91", "N92", "N93", "N94", "N95", "N96"}: body = s.outcome_text
        elif n == "aftermath": body = s.people_text
        else: body = self.scene_text()
        if n in {"N80", "N81", "N90", "N99"} and (s.headline_review or s.publication):
            self._label("已刊标题" if s.publication else "待签发原句", size=10, color=MUTED)
            self._label(s.publication.headline if s.publication else s.headline_review.original_text, size=21, serif=True)
        self._label(body, size=14)
        if n == "result":
            if self.interview.receipt and self.interview.receipt.response == s.result_text:
                self._label("刚才确认的原句：" + self.interview.receipt.original_text, size=11, color=MUTED)
            for eid in s.result_evidence: self._material(s.evidence[eid])
        if n in {"N80", "N81"}:
            claims = json.loads(s.headline_review.claims_json)
            if n == "N80":
                self._label("系统理解 · 全部含义", size=12, color=RED)
                for c in claims: self._label(describe_claim(c), size=13)
                if not claims: self._label("没有本章的具体责任主张；这仍是一次真实刊发。", size=13)
                self._label("本局材料：" + ("、".join(m["title"] for m in s.evidence.values()) or "尚无记录"), size=11, color=MUTED)
            else:
                if any(c.get("source_ref_id") for c in claims): self._label("这句话把主张归于目击者。归属表达并不自动说明事情已得到证实。", size=12)
                if any(c["commitment_mode"] != "ASSERTED" for c in claims): self._label("这句话提出一种需要读者考虑的可能。请确认它表达的是你的意思。", size=12)
                if any(c["commitment_mode"] == "ASSERTED" and not c.get("source_ref_id") for c in claims): self._label("这句话把责任或经过写作事实。你可以返回修改，也可以照此刊发。", size=12)
        if n == "N20": self._hub_choices()
        elif n == "N99": self._render_recap()
        else: self._choices(s.choices())
        if n == "N00":
            if s.result_text: self._label(s.result_text, size=13, color=RED)
            self._render_background()

    def _hub_choices(self):
        choices = self.session.choices()
        if self.menu:
            wanted = {"A", "B"} if self.menu == "main" else {"S-A", "S-B"}
            self._choices([(cid, label) for cid, label in choices if cid.startswith("visit:") and cid.split(":", 1)[1] in wanted] + [("menu:back", "返回调查安排")])
        else:
            options = []
            available = set(self.session.available_scenes())
            if available & {"A", "B"}: options.append(("menu:main", "选择现场或资金调查"))
            if available & {"S-A", "S-B"}: options.append(("menu:side", "深入已经发现的问题"))
            self._choices(options + [("desk", "结束调查，回编辑台")])
        if AUDIO in self.session.evidence and VIDEO in self.session.evidence and not self.session.cooperation["witness"]:
            self._label("阿岑已拒绝继续采访，不能开展观察范围追问。", size=11, color=MUTED)
        if LEDGER in self.session.evidence and not self.session.cooperation["clerk"]:
            self._label("许先生已拒绝继续解释，不能开展记账语境核对。", size=11, color=MUTED)

    def _material(self, material):
        self._rule(); self._label(material["title"], size=19, serif=True)
        self._label(material["origin"], size=10, color=MUTED)
        self._label(material["text"], size=13)

    def _render_editor(self):
        s = self.session
        self._label("编辑台 / 本版调查已经结束", size=11, color=RED)
        self._label("你准备怎样写这一版？", size=26, serif=True)
        self._label(self.scene_text(), size=13); self._rule()
        self._label("选稿只替换输入文字；仍须查看完整理解并明确签发。", size=10, color=MUTED)
        titles = s.visible_headlines()
        preset = tk.StringVar(value="选择一版作者标题")
        selector = ttk.Combobox(self.content, values=[h["text"] for h in titles.values()], textvariable=preset, state="readonly", font=(self.sans, 11))
        selector.pack(fill="x", pady=(0, 10))
        selector.bind("<<ComboboxSelected>>", lambda e: self._load_headline(preset.get()))
        self.draft_entry = tk.Text(self.content, height=3, wrap="word", undo=True, bg=SHEET, fg=INK, insertbackground=RED,
            selectbackground=RULE, relief="flat", padx=14, pady=10, highlightthickness=2, highlightbackground=RULE, highlightcolor=RED, font=(self.sans, 13))
        self.draft_entry.pack(fill="x", pady=(0, 12)); self.draft_entry.insert("1.0", s.draft)
        self.draft_entry.bind("<Tab>", lambda e: self._tab_from_text(1)); self.draft_entry.bind("<Shift-Tab>", lambda e: self._tab_from_text(-1))
        self.draft_entry.bind("<FocusIn>", lambda e: self._reveal(self.draft_entry))
        if s.headline_message: self._label(s.headline_message, size=11, color=RED)
        self._button(self.content, "查看标题的完整理解", self._prepare_headline, primary=True).pack(fill="x", pady=(0, 10))
        self._button(self.content, "本版暂缓 · 先复核决定", lambda: self.choose("hold_review")).pack(fill="x", pady=(0, 10))
        self._label("任意改写暂不解析；脚本外原句保留，不自动换成作者稿。Ctrl+E可翻材料，返回后草稿与页面位置保留。", size=10, color=MUTED)
        self.draft_entry.focus_set()

    def _load_headline(self, text):
        self.session.draft = text; self.session.headline_message = ""; self.render()

    def _prepare_headline(self):
        self._capture_draft(); self.session.prepare_headline(self.session.draft); self.render()

    def _render_evidence(self):
        self._label("刊发时留存材料" if self.session.publication else "当前取得的材料", size=25, serif=True)
        self._label("这里只显示你已经取得的版本；回看不消耗时间。", size=11, color=MUTED)
        entries = chapter_evidence_entries(self.session)
        if not entries: self._label("目前没有取得记录。", size=14)
        for title, origin, text in entries: self._material({"title": title, "origin": origin, "text": text})
        self._button(self.content, "返回原页面 [Esc]", self._toggle_evidence).pack(fill="x", pady=(8, 10))

    def _render_recap(self):
        self._label("本版已刊发，按当时材料留存。" if self.session.publication else "本版未刊发，保留本案工作记录。", size=12, color=RED)
        self._button(self.content, "收起事件账" if self.show_log else "查看本次选择与代价", self._toggle_log).pack(fill="x", pady=(0, 10))
        if self.show_log:
            for h in self.session.history:
                if h.get("scene"): self._label(SCENE_LABELS[h["scene"]] + "：调查时间 -1", size=11)
                elif h.get("text"): self._label(h["text"], size=11, color=MUTED)
            for event in self.session.events:
                deltas = "、".join({"Money": "资金", "Threat Level": "风险", "Reputation": "声誉", "Public Opinion": "公众态度"}[key] + f" {value:+d}" for key, value in event["effects"].items())
                self._label(event["label"] + "：" + deltas, size=12)
            self._label("读者来电和公司询问不改变公众态度；本章没有自动退款或合作恢复。", size=10, color=MUTED)
        self._button(self.content, "回看本版材料", self._toggle_evidence).pack(fill="x", pady=(0, 10))
        self._button(self.content, "重新开始本案", self.restart, primary=True).pack(fill="x", pady=(0, 10))
        self._label("关闭不保存；本案没有可进入的第二天关卡。", size=10, color=MUTED)

    def _toggle_log(self): self.show_log = not self.show_log; self.render()

    def choose(self, choice_id):
        if choice_id == "start": self.start(); return
        if choice_id.startswith("menu:"):
            value = choice_id.split(":", 1)[1]; self.menu = None if value == "back" else value; self.render(); return
        self._capture_draft()
        self.interview.edit()
        self.session.choose(choice_id)
        self.menu = None; self.background_open = False; self.render()

    def _escape(self, event=None):
        if self.reading_evidence: self._toggle_evidence()
        elif self.interview.review: self._rewrite_interview()
        elif self.session.node in {"N80", "N81", "N82"}: self.choose("edit")
        elif self.session.node == "entry": self.choose("cancel_entry")
        elif self.session.node == "desk_confirm": self.choose("cancel_desk")
        elif self.menu: self.choose("menu:back")

    def restart(self):
        self.session = ChapterSession(); self.interview = ChapterInterviewFlow(self.session)
        self.interview_node = None; self.scene_drafts = {}; self.menu = None; self.show_log = False
        self.last_response = ""; self.reading_evidence = False; self.background_open = False; self.started = False
        self.render()


def main():
    root = tk.Tk(); ChapterDesktop(root); root.mainloop()


if __name__ == "__main__": main()
