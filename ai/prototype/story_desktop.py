"""Local scripted interview confirmation and authored story. No model calls or NLP."""

from __future__ import annotations

from dataclasses import dataclass
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

from .interview_flow import InterviewFlow, SCRIPTED_LINES, review_lines
from .story_fixture import StorySession


INK = "#202724"
PAPER = "#F1E8D5"
SHEET = "#FBF5E8"
MUTED = "#66675B"
RULE = "#C8BCA6"
RED = "#8B302B"
DESK = "#28342F"

NODE_TITLES = {
    "interview": ("01 / 采访", "货场边的目击者"),
    "followup": ("02 / 调查", "最后一段调查时间"),
    "clerk": ("02 / 资金线", "账簿压在他的手下"),
    "deal": ("02 / 交易确认", "一份账簿，500 的代价"),
    "publication": ("03 / 编辑台", "你准备怎样写这条新闻？"),
    "confirm": ("04 / 签发", "让这句话进入晚报"),
}
EVIDENCE_TITLES = {"EV_AUDIO_A": "采访录音", "EV_VIDEO_A": "现场录像", "EV_LEDGER_A": "付款账簿"}
EVIDENCE_ORIGINS = {"EV_AUDIO_A": "来源：目击者 A · 现场采访", "EV_VIDEO_A": "出处：本次追加调查取得的现场录像", "EV_LEDGER_A": "出处：本次交易取得的付款账簿"}
ENDING_TITLES = {
    "SUPPORTED_REPORT": "这一版，有材料可循",
    "UNSUPPORTED_REPORT": "刊发之后，还要回答依据",
    "CONTESTED_ATTRIBUTION": "他说过，事实仍有争议",
    "NO_CLAIM": "城市仍在等待答案",
    "HELD": "这一版，暂不刊发",
}


@dataclass(frozen=True)
class Page:
    kicker: str
    title: str
    body: str
    choices: tuple[tuple[str, str], ...]
    headline: str = ""


def page_for(session: StorySession) -> Page:
    """Explicit player copy; never stringify nodes, oracle, rules, or internal evaluation."""
    if session.ending:
        body = session.story["endings"][session.ending]
        if session.ending == "HELD":
            body = "你错过这一版的刊发，但保留了调查空间。"
        return Page("05 / 余波" if session.publication else "05 / 暂缓", ENDING_TITLES[session.ending],
                    body, (), session.publication.headline if session.publication else "")
    kicker, title = NODE_TITLES[session.node]
    body = session.story["nodes"][session.node]["text"]
    if session.node == "deal":
        body = f"他同意交出账簿，条件是支付 500。\n你现在有 {session.state.money}，付款后余下 {session.state.money - 500}。\n只有确认付款，交易才会发生。"
    elif session.node == "publication":
        body = "材料已经摊在桌上。选择一版预写标题，或暂缓这一版。\n你可以先翻证据册；进入签发页后仍能返回修改。"
    labels = {"offer500": "提出交易：支付 500，取得账簿。", "accept": "确认支付 500，取得账簿。", "publish": "确认签发这版标题", "edit": "返回修改标题"}
    choices = tuple((c["id"], labels.get(c["id"], c["label"])) for c in session.choices())
    headline = session.story["headlines"][session.draft]["text"] if session.node == "confirm" else ""
    return Page(kicker, title, body, choices, headline)


def evidence_entries(session: StorySession, *, published: bool = False) -> tuple[tuple[str, str, str], ...]:
    """Only acquired, readable evidence; a publication view uses the frozen snapshot."""
    ids = session.publication.evidence_ids if published and session.publication else session.evidence
    return tuple((EVIDENCE_TITLES[e], EVIDENCE_ORIGINS[e], session.story["evidence"][e])
                 for e in EVIDENCE_TITLES if e in ids)


class StoryDesktop:
    def __init__(self, root: tk.Tk, *, session=None, interview_factory=InterviewFlow):
        self.root = root
        self.session = session if session is not None else StorySession()
        self.interview = interview_factory(self.session)
        self.started = False
        self.reading_evidence = False
        self.last_response = ""
        self.choice_buttons: list[tk.Button] = []
        self.draft_entry: tk.Text | None = None
        self.reader_bookmark = (0.0, "")
        self.root.title("截稿前的货场 | 离线采访确认")
        self.root.geometry("1180x820")
        self.root.minsize(1060, 740)
        self.root.configure(bg=DESK)
        families = set(tkfont.families(root))
        self.sans = "Microsoft YaHei UI" if "Microsoft YaHei UI" in families else "TkDefaultFont"
        self.serif = "SimSun" if "SimSun" in families else self.sans
        self.root.option_add("*Font", (self.sans, 12))
        self.root.bind("<Escape>", self._escape)
        self.root.bind("<Key-e>", self._toggle_evidence)
        self.root.bind("<Key-E>", self._toggle_evidence)
        self.root.bind("<Control-e>", lambda e: self._toggle_evidence())
        self.root.bind("<MouseWheel>", self._wheel)
        self.root.bind("<Prior>", lambda e: self._page_scroll(-1))
        self.root.bind("<Next>", lambda e: self._page_scroll(1))
        for n in range(1, 7):
            self.root.bind(str(n), lambda e, index=n - 1: self._number_choice(index))
        self._build_shell()
        self.render()

    def _build_shell(self):
        header = tk.Frame(self.root, bg=DESK, padx=30, pady=15)
        header.pack(fill="x")
        tk.Label(header, text="BETWEEN THE LINES", fg=PAPER, bg=DESK,
                 font=("Georgia", 17)).pack(side="left")
        tk.Label(header, text="晚报 / 货场调查", fg="#C9CEBE", bg=DESK,
                 font=(self.sans, 11)).pack(side="right")
        self.shell = tk.Frame(self.root, bg=PAPER)
        self.shell.pack(fill="both", expand=True, padx=22, pady=(0, 18))
        self.shell.columnconfigure(1, weight=1)
        self.shell.rowconfigure(0, weight=1)
        self.side = tk.Frame(self.shell, bg=INK, width=265)
        self.side.grid(row=0, column=0, sticky="nsew")
        self.side.grid_propagate(False)
        self.art = tk.Canvas(self.side, bg=INK, height=290, width=265, highlightthickness=0)
        self.art.pack(fill="x")
        self._draw_yard()
        self.location = tk.Label(self.side, text="货场 / 截稿之前", bg=INK, fg=PAPER,
                                 font=(self.serif, 18), anchor="w")
        self.location.pack(fill="x", padx=25, pady=(8, 12))
        self.side_note = tk.Label(self.side, text="", bg=INK, fg="#C8CBBE", justify="left",
                                  anchor="nw", wraplength=215, font=(self.sans, 11))
        self.side_note.pack(fill="x", padx=25)
        self.money = tk.Label(self.side, bg=INK, fg=PAPER, anchor="w", font=(self.sans, 12))
        self.money.pack(fill="x", padx=25, pady=(25, 8))
        self.evidence_button = self._button(self.side, "证据册  [E]", self._toggle_evidence, dark=True)
        self.evidence_button.pack(fill="x", padx=22, pady=(0, 10))
        tk.Label(self.side, text="Tab 选择 · Enter / 空格确认\n输入框内 Enter 换行\nCtrl+E 证据册 · Esc 返回",
                 bg=INK, fg="#C8CBBE", justify="left", font=(self.sans, 9)).pack(side="bottom", anchor="w", padx=25, pady=20)
        reader = tk.Frame(self.shell, bg=PAPER)
        reader.grid(row=0, column=1, sticky="nsew")
        self.scroll = tk.Canvas(reader, bg=PAPER, highlightthickness=0, takefocus=False)
        bar = tk.Scrollbar(reader, command=self.scroll.yview)
        self.scroll.configure(yscrollcommand=bar.set)
        bar.pack(side="right", fill="y")
        self.scroll.pack(side="left", fill="both", expand=True)
        self.content = tk.Frame(self.scroll, bg=PAPER, padx=36, pady=28)
        self.content_window = self.scroll.create_window((0, 0), anchor="nw", window=self.content)
        self.content.bind("<Configure>", lambda e: self.scroll.configure(scrollregion=self.scroll.bbox("all")))
        self.scroll.bind("<Configure>", self._resize_reader)

    def _draw_yard(self):
        c = self.art
        c.create_rectangle(0, 0, 265, 290, fill=INK, outline="")
        c.create_oval(180, 32, 214, 66, fill="#D9D0B7", outline="")
        for x, y, w, h in [(14, 161, 83, 67), (99, 180, 90, 48), (171, 146, 76, 82)]:
            c.create_rectangle(x, y, x+w, y+h, fill="#3C4840", outline="#667062")
            for xx in range(x+8, x+w, 12):
                c.create_line(xx, y+4, xx, y+h-4, fill="#536052")
        c.create_line(39, 154, 39, 82, 131, 82, fill="#A59F89", width=2)
        c.create_line(124, 82, 124, 102, fill="#A59F89", width=2)
        c.create_polygon(114, 104, 134, 104, 158, 224, 82, 224, fill="#303C34", outline="")
        for x in (-85, -25, 35, 95, 155, 215, 275):
            c.create_line(x, 290, 127, 230, fill="#5D695A", width=2)
        for y in (245, 260, 280):
            c.create_line(0, y, 265, y, fill="#414D41", width=2)
        c.create_text(24, 28, anchor="nw", text="THE LAST EDITION", font=("Georgia", 10), fill="#B5BAAA")
        c.create_line(24, 52, 103, 52, fill=RED, width=3)

    def _resize_reader(self, event):
        self.scroll.itemconfigure(self.content_window, width=event.width)
        width = max(400, event.width - 78)
        for widget in self.content.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button)):
                widget.configure(wraplength=width)

    def _label(self, text, *, size=13, color=INK, serif=False, pady=(0, 12)):
        label = tk.Label(self.content, text=text, bg=PAPER, fg=color, anchor="w", justify="left",
                         wraplength=max(400, self.scroll.winfo_width()-78),
                         font=(self.serif if serif else self.sans, size))
        label.pack(fill="x", pady=pady)
        return label

    def _button(self, parent, text, command, *, primary=False, dark=False):
        bg = RED if primary else INK if dark else SHEET
        fg = SHEET if primary or dark else INK
        button = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                           activebackground=RED if primary else RULE, activeforeground=SHEET if primary else INK,
                           relief="flat", borderwidth=0, highlightthickness=2, highlightcolor=RED,
                           highlightbackground=RULE if not dark else "#667062", padx=16, pady=10,
                           cursor="hand2", anchor="w", justify="left", takefocus=True, font=(self.sans, 12))
        button.bind("<Return>", lambda e: button.invoke())
        button.bind("<FocusIn>", lambda e: self._reveal(button) if not dark else None)
        return button

    def _reveal(self, widget):
        self.content.update_idletasks()
        height = max(1, self.content.winfo_height())
        top = self.scroll.canvasy(0)
        bottom = top + self.scroll.winfo_height()
        y = widget.winfo_rooty() - self.content.winfo_rooty()
        if y < top:
            self.scroll.yview_moveto(max(0, y - 20) / height)
        elif y + widget.winfo_height() > bottom:
            self.scroll.yview_moveto(max(0, y + widget.winfo_height() - self.scroll.winfo_height() + 20) / height)

    def _rule(self):
        tk.Frame(self.content, bg=RULE, height=1).pack(fill="x", pady=(5, 18))

    def render(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self.draft_entry = None
        self.choice_buttons = []
        self.scroll.yview_moveto(0)
        self.money.configure(text=f"随身资金  {self.session.state.money}")
        self.evidence_button.configure(text=f"证据册  {len(self.session.evidence)}  [E]",
                                       state="normal" if self.started else "disabled")
        self.side_note.configure(text="问清楚。留下出处。\n决定怎样刊发。" if not self.started else
                                 "浏览材料不会消耗调查机会。\n未取得的材料，不在你的手中。")
        if self.reading_evidence:
            self._render_evidence()
        elif not self.started:
            self._render_cover()
        elif self.session.node == "interview" and not self.session.ending:
            self._render_interview()
        else:
            self._render_story()
        self.root.update_idletasks()
        self.scroll.configure(scrollregion=self.scroll.bbox("all"))
        self.scroll.yview_moveto(0)

    def _render_cover(self):
        self._label("作者实验短篇 / 离线采访确认", size=11, color=RED, pady=(8, 28))
        self._label("截稿前\n的货场", size=36, serif=True, pady=(0, 24))
        self._rule()
        self._label("货场冲突之后，晚报还缺一个标题。", size=18, serif=True)
        self._label("你是一名记者。先听目击者怎么说，再决定最后一段调查时间用在哪里。回到编辑台时，你必须选择怎样报道。", size=13, pady=(8, 22))
        self._label("写下原句 → 复核理解 → 确认采访 → 调查与刊发", size=11, color=MUTED, pady=(0, 25))
        start = self._button(self.content, "进入故事  →", self.start, primary=True)
        start.pack(fill="x", pady=(0, 22))
        self._label("采访理解来自标明的脚本示例，不调用 AI，不分析任意文字。\n调查与标题仍用预写选项；关闭后不保存进度。", size=10, color=MUTED)
        start.focus_set()

    def _render_interview(self):
        review = self.interview.review
        self._label("01 / 采访 · " + ("复核理解" if review else "写下原句"), size=11, color=RED)
        self._label("先看清，再说出口" if review else self._interview_title(), size=26, serif=True, pady=(0, 18))
        if review:
            self._render_review()
            return
        self._label(self._interview_text(), size=14, pady=(0, 18))
        self._label("脚本候选演示 · 仅接通下列示例，不会理解任意改写。", size=10, color=MUTED)
        samples = tk.Frame(self.content, bg=PAPER)
        samples.pack(fill="x", pady=(0, 12))
        scripts = self._script_samples()
        selected = tk.StringVar(value=next((s.label for s in scripts if s.text == self.interview.draft.strip()), scripts[0].label))
        selector = ttk.Combobox(samples, values=[s.label for s in scripts],
                                textvariable=selected, state="readonly", width=12, font=(self.sans, 11))
        selector.pack(side="left", padx=(0, 12), pady=4)
        load = self._button(samples, "载入示例", lambda: self._load_script(selected.get()))
        load.pack(side="left")
        self._label("你想说的原句", size=11, color=MUTED, pady=(0, 6))
        self.draft_entry = tk.Text(self.content, height=4, wrap="word", undo=True, bg=SHEET, fg=INK,
                                   insertbackground=RED, selectbackground=RULE, relief="flat", padx=14, pady=10,
                                   highlightthickness=2, highlightbackground=RULE, highlightcolor=RED,
                                   font=(self.sans, 13), spacing1=3, spacing3=5)
        self.draft_entry.pack(fill="x", pady=(0, 12))
        self.draft_entry.insert("1.0", self.interview.draft)
        self.draft_entry.bind("<Tab>", lambda e: self._tab_from_text(1))
        self.draft_entry.bind("<Shift-Tab>", lambda e: self._tab_from_text(-1))
        self.draft_entry.bind("<FocusIn>", lambda e: self._reveal(self.draft_entry))
        if self.interview.message:
            self._label(self.interview.message, size=11, color=RED)
        submit = self._button(self.content, "查看系统理解  →", self._prepare_interview, primary=True)
        submit.pack(fill="x", pady=(0, 8))
        if self._leave_label():
            leave = self._button(self.content, self._leave_label(), self._prepare_leave)
            leave.pack(fill="x", pady=(0, 8))
        self._label("现在还没有发送、记录采访或消耗调查机会。\nEnter 在输入框内只换行；Tab 离开输入框后可激活按钮。", size=10, color=MUTED)
        self.draft_entry.focus_set()

    def _render_review(self):
        review = self.interview.review
        self._label("作者选项 · 尚未离开" if review.choice_id == "leave" else "脚本候选 · 尚未执行采访", size=11, color=RED)
        self._label("你的原句" if review.choice_id != "leave" else "保留的草稿（不会发送）", size=10, color=MUTED)
        self._label("「" + review.original_text + "」", size=15, serif=True, pady=(0, 22))
        self._rule()
        self._label("系统理解" if review.choice_id != "leave" else "准备采取的选择", size=12, color=RED)
        for item in self._review_copy():
            self._label(item, size=12, pady=(0, 9))
        self._rule()
        edit = self._button(self.content, "返回改写 · 保留原句", self._rewrite_interview)
        edit.pack(fill="x", pady=(0, 10))
        confirm = self._button(self.content, "确认离开采访" if review.choice_id == "leave" else "照此表达并执行采访", self._confirm_interview, primary=True)
        confirm.pack(fill="x", pady=(0, 10))
        self._label("请对照原句检查；如果不是你的意思，请返回改写。", size=10, color=MUTED)
        edit.focus_set()

    def _capture_draft(self):
        if self.draft_entry is not None:
            text = self.draft_entry.get("1.0", "end-1c")
            if text != self.interview.draft:
                self.interview.edit(text)

    def _load_script(self, label):
        self.interview.edit(next(s.text for s in self._script_samples() if s.label == label))
        self.render()

    def _script_samples(self):
        return SCRIPTED_LINES

    def _interview_title(self):
        return "货场边的目击者"

    def _interview_text(self):
        return self.session.story["nodes"]["interview"]["text"]

    def _review_copy(self):
        return review_lines(self.interview.review, EVIDENCE_TITLES)

    def _leave_label(self):
        return "不采用采访，准备离开"

    def _prepare_interview(self):
        self._capture_draft()
        self.interview.prepare(self.interview.draft)
        self.render()

    def _prepare_leave(self):
        self._capture_draft()
        self.interview.prepare_leave()
        self.render()

    def _rewrite_interview(self):
        self.interview.edit()
        self.render()

    def _confirm_interview(self):
        try:
            receipt = self.interview.confirm()
        except ValueError:
            self.render()
            return
        self.last_response = receipt.response
        self.render()

    def _tab_from_text(self, direction):
        target = self.draft_entry.tk_focusNext() if direction > 0 else self.draft_entry.tk_focusPrev()
        target.focus_set()
        return "break"

    def _render_story(self):
        page = page_for(self.session)
        self._label(page.kicker, size=11, color=RED, pady=(0, 14))
        self._label(page.title, size=27, serif=True, pady=(0, 20))
        self._rule()
        if self.session.node == "followup" and self.interview.receipt:
            receipt = self.interview.receipt
            self._label("已确认的采访" if receipt.choice_id != "leave" else "已选择不采用采访", size=10, color=MUTED)
            if receipt.choice_id != "leave":
                self._label("你：" + receipt.original_text, size=12, pady=(0, 12))
        if self.last_response and not self.session.ending:
            self._label(self.last_response, size=12, color=RED, pady=(0, 20))
        if page.headline:
            self._label("本版标题" if self.session.publication else "待签发标题", size=10, color=MUTED)
            self._label("「" + page.headline + "」", size=22, serif=True, pady=(0, 22))
        self._label(page.body, size=14, pady=(0, 22))
        if self.session.ending:
            self._render_ending()
            return
        if self.session.node == "followup":
            self._label("只能追加一项调查：核查开火顺序，或追查资金；选定后回编辑台。", size=11, color=RED)
        if self.session.node == "publication":
            self._label("预写标题 / 可在下一页返回修改", size=10, color=MUTED)
        hints = {"video": "把最后一次调查机会用来核查开火顺序。", "clerk": "把最后一次调查机会用来追查行动资金。", "desk": "不追加调查，直接带着已有材料写标题。"}
        for index, (choice_id, label) in enumerate(page.choices):
            primary = self.session.node in {"confirm", "deal"} and choice_id in {"publish", "accept"}
            button = self._button(self.content, f"{index+1}   {label}", lambda cid=choice_id: self.choose(cid), primary=primary)
            button.pack(fill="x", pady=(0, 8))
            self.choice_buttons.append(button)
            if self.session.node == "followup":
                self._label(hints[choice_id], size=10, color=MUTED, pady=(0, 10))
        # Signing / payment always needs an explicit action; focus the reversible choice.
        focus_index = 1 if self.session.node == "deal" else 0
        if self.choice_buttons:
            self.choice_buttons[focus_index].focus_set()

    def _render_ending(self):
        self._label("已刊发 · 本版材料已归档" if self.session.publication else "本版未刊发", size=12, color=RED)
        self._rule()
        labels = {"Reputation": "声誉", "Public Opinion": "公众反应", "Threat Level": "风险", "Money": "资金"}
        initial = {"Reputation": 0, "Public Opinion": 0, "Threat Level": 0, "Money": self.session.story["initial_money"]}
        changes = [f"{labels[k]}  {v-initial[k]:+d}" for k, v in self.session.state.as_dict().items() if v != initial[k]]
        self._label("这次的变化：" + ("  /  ".join(changes) if changes else "没有数值变化"), size=11, color=MUTED)
        self._label("数值是本篇的实验设定。结局来自你的调查、交易与刊发选择。", size=10, color=MUTED)
        review = self._button(self.content, "回看刊发时的材料" if self.session.publication else "回看手上的材料", self._toggle_evidence)
        review.pack(fill="x", pady=(8, 10))
        restart = self._button(self.content, "重新开始 · 选择另一条调查线", self.restart, primary=True)
        restart.pack(fill="x", pady=(0, 12))
        review.focus_set()

    def _render_evidence(self):
        published = self.session.publication is not None
        self._label("随身笔记 / 刊发归档" if published else "随身笔记 / 当前材料", size=11, color=RED)
        self._label("证据册", size=30, serif=True, pady=(0, 18))
        self._label("这里只收录你已经取得的材料。" + ("以下为刊发当时留存的版本。" if published else "先读原文，再决定怎样报道。"), size=12, color=MUTED)
        self._rule()
        entries = evidence_entries(self.session, published=published)
        if not entries:
            self._label("笔记本还是空的。\n回到故事里，决定下一步要调查什么。", size=15, serif=True, pady=(20, 40))
        for title, origin, text in entries:
            self._label(title, size=20, serif=True)
            self._label(origin, size=10, color=MUTED)
            self._label(text, size=13, pady=(0, 22))
            self._rule()
        button = self._button(self.content, "返回故事  [Esc]", self._toggle_evidence, primary=True)
        button.pack(fill="x", pady=(8, 10))
        button.focus_set()

    def start(self):
        self.started = True
        self.render()

    def restart(self):
        self.session = StorySession()
        self.interview = InterviewFlow(self.session)
        self.last_response = ""
        self.reading_evidence = False
        self.started = False
        self.render()

    def choose(self, choice_id):
        if self.session.node == "interview":
            raise ValueError("interview requires explicit review and confirmation")
        self.last_response = self.session.choose(choice_id)
        self.render()

    def _toggle_evidence(self, event=None):
        if event is not None and self._typing():
            return
        if self.started:
            if not self.reading_evidence:
                self._capture_draft()
                focused = self.root.focus_get()
                focus_key = "draft" if focused == self.draft_entry else focused.cget("text") if isinstance(focused, tk.Button) else ""
                self.reader_bookmark = (self.scroll.yview()[0], focus_key)
            self.reading_evidence = not self.reading_evidence
            self.render()
            if not self.reading_evidence:
                position, focus_key = self.reader_bookmark
                if focus_key == "draft" and self.draft_entry is not None:
                    self.draft_entry.focus_set()
                else:
                    for widget in self.content.winfo_children():
                        if isinstance(widget, tk.Button) and widget.cget("text") == focus_key:
                            widget.focus_set()
                            break
                self.root.update_idletasks()
                self.scroll.yview_moveto(position)

    def _escape(self, event=None):
        if self.reading_evidence:
            self._toggle_evidence()
        elif self.started and self.session.node == "interview" and self.interview.review:
            self._rewrite_interview()
        elif self.started and not self.session.ending and self.session.node == "confirm":
            self.choose("edit")

    def _number_choice(self, index):
        if not self._typing() and not self.reading_evidence and index < len(self.choice_buttons):
            self.choice_buttons[index].invoke()

    def _typing(self):
        focused = self.root.focus_get()
        return focused is not None and focused.winfo_class() in {"Text", "Entry", "TEntry", "TCombobox"}

    def _page_scroll(self, direction):
        if not self._typing():
            self.scroll.yview_scroll(direction, "pages")

    def _wheel(self, event):
        if event.widget != self.draft_entry and self.scroll.winfo_height() < self.content.winfo_height():
            self.scroll.yview_scroll(-int(event.delta / 120), "units")


def main():
    root = tk.Tk()
    StoryDesktop(root)
    root.mainloop()


if __name__ == "__main__":
    main()
