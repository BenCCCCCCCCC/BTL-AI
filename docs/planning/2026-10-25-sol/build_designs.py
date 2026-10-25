"""Rebuild local vector proposals, without external assets or image/model services."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "screens"
OUT.mkdir(exist_ok=True)
INK, PAPER, SHEET, MUTED, RULE, RED, DESK = "#202724", "#F1E8D5", "#FBF5E8", "#66675B", "#C8BCA6", "#8B302B", "#28342F"


def rect(x, y, w, h, fill, stroke="none", r=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'


def text(x, y, content, size=22, fill=INK, family="sans", weight="400", spacing=0):
    font = "SimSun,Songti SC,serif" if family == "serif" else "Microsoft YaHei UI,Microsoft YaHei,Noto Sans CJK SC,sans-serif"
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" fill="{fill}">{escape(content)}</text>'


def lines(x, y, content, size=22, fill=INK, leading=36, family="sans"):
    return "".join(text(x, y+i*leading, s, size, fill, family) for i, s in enumerate(content.split("\n")))


def line(x1, y1, x2, y2, fill=RULE, width=1):
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{fill}" stroke-width="{width}"/>'


def button(x, y, w, label, primary=False):
    return rect(x, y, w, 56, RED if primary else SHEET, RED if primary else RULE) + text(x+22, y+36, label, 20, SHEET if primary else INK)


def top(section, number):
    return (rect(0, 0, 1440, 900, DESK) + text(48, 50, "BETWEEN THE LINES", 24, PAPER, "serif", spacing=2)
            + text(990, 49, "晚报 / 截稿前的货场", 19, PAPER)
            + rect(46, 78, 1348, 762, PAPER) + text(80, 115, section, 16, RED)
            + text(80, 871, "设计提案 · 非运行截图 · 非正式剧情设定", 16, "#C9CEBE")
            + text(1290, 871, "AUTHOR" if number == "F" else f"S{number} / 06", 16, "#C9CEBE"))


def yard(x, y, w=350, h=570):
    a = f'<defs><clipPath id="yard-clip"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs><g clip-path="url(#yard-clip)">'
    a += rect(x, y, w, h, INK)
    a += f'<circle cx="{x+w-75}" cy="{y+68}" r="24" fill="#D9D0B7"/>'
    for bx, by, bw, bh in [(20, 290, 140, 100), (165, 320, 160, 70), (230, 235, 95, 80)]:
        a += rect(x+bx, y+by, bw, bh, "#3C4840", "#667062")
        for dx in range(12, bw, 16):
            a += line(x+bx+dx, y+by+5, x+bx+dx, y+by+bh-5, "#536052")
    for dx in (-100, -20, 60, 140, 220, 300, 380, 460):
        a += line(x+dx, y+h, x+170, y+405, "#5D695A", 2)
    for dy in (430, 460, 500, 550):
        a += line(x, y+dy, x+w, y+dy, "#414D41", 2)
    a += line(x+45, y+288, x+45, y+155, "#A59F89", 2)
    a += line(x+45, y+155, x+176, y+155, "#A59F89", 2)
    a += text(x+24, y+38, "货场 / 夜班手记", 17, PAPER)
    return a + '</g>'


def save(name, title, content, desc):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="900" viewBox="0 0 1440 900" role="img"><title>{escape(title)}</title><desc>{escape(desc)}</desc>{content}</svg>'
    (OUT / name).write_text(svg, encoding="utf-8")


# S1: a conversation with one environmental column; no omniscient dossier.
s = top("01 / 采访 · 先听他说", 1) + yard(80, 140, 350, 650)
s += text(472, 178, "货场边的目击者", 40, family="serif")
s += text(475, 218, "目击者 A / 你的采访对象", 18, MUTED)
s += line(474, 246, 1356, 246)
s += lines(500, 310, "“我看到安保先开火。\n你们会把我的话登出来吗？”", 30, leading=50, family="serif")
s += text(476, 432, "你想问他什么？", 19, MUTED)
s += rect(474, 460, 880, 142, SHEET, RULE)
s += lines(498, 501, "你看到的是谁先开火？\n请按你看到的经过说。", 23)
s += button(474, 628, 310, "整理这句话的含义  →", True)
s += button(806, 628, 226, "查看随身笔记")
s += lines(476, 735, "发送后先复核系统理解，再执行采访行动。\n自由输入与确认流程是后续提案；当前试玩使用预写选项。", 18, MUTED, 30)
save("01-interview.svg", "S1 采访提案", s, "环境剪影与大段人物原话；问题输入后进入玩家确认。")

# S2: an open notebook; only acquired evidence is on the paper.
s = top("02 / 证据册 · 读材料，也读出处", 2)
s += text(83, 175, "两份材料，都在你的手上", 36, family="serif")
s += text(83, 214, "示例状态：录音 → 核查录像。页面不会列出未取得的材料。", 19, MUTED)
s += rect(82, 250, 618, 425, SHEET, RULE) + rect(720, 250, 636, 425, SHEET, RULE)
s += text(112, 295, "01  采访录音", 27, family="serif") + text(750, 295, "02  现场录像", 27, family="serif")
s += text(112, 334, "来源：目击者 A · 本次采访", 18, MUTED) + text(750, 334, "出处：本次追加调查取得", 18, MUTED)
s += line(112, 360, 670, 360) + line(750, 360, 1326, 360)
s += lines(112, 408, "“安保先开火。”\n\n录音记录的是他的说法。", 24, leading=38, family="serif")
s += lines(750, 408, "画面呈现民兵先开火。\n\n这份材料与录音中的说法不同。", 24, leading=38, family="serif")
s += rect(110, 549, 552, 82, PAPER) + lines(130, 580, "我的笔记\n比较材料，不等于替来源作保证。", 18, MUTED, 28)
s += text(752, 582, "选中原文 → 留下自己的标记", 18, RED)
s += text(84, 718, "材料没有真伪分数。你要决定，标题究竟承担哪一种说法。", 21)
s += button(82, 752, 245, "返回正在写的内容", True) + button(348, 752, 222, "收起对照阅读")
save("02-evidence.svg", "S2 证据册提案", s, "两张相对的纸展示已经取得的材料和来源，不显示隐藏支持判断。")

# S3: the player owns the confirmation; copy does not mimic technical enums.
s = top("03 / 语义确认 · 执行前，把意思说清楚", 3)
s += rect(250, 142, 940, 645, SHEET, RULE)
s += text(292, 195, "这句话，将这样表达", 38, family="serif")
s += text(292, 237, "还没有执行采访行动。你可以照此表达，也可以返回修改。", 19, MUTED)
s += line(292, 263, 1146, 263)
s += text(292, 305, "你的原句", 17, MUTED)
s += lines(292, 346, "“你看到的是谁先开火？”", 25, family="serif", leading=40)
s += rect(292, 419, 854, 180, PAPER)
s += text(316, 459, "准备执行的行动", 18, RED)
s += lines(316, 499, "向目击者询问货场的开火顺序。\n没有使用已取得的材料，也没有附加施压策略。\n这一步不会承诺替他刊发。", 22, leading=36)
s += button(292, 637, 310, "照此表达  →", True) + button(622, 637, 245, "返回改写")
s += text(292, 738, "若原句含多项策略，必须全部呈现；不能只显示最显著的一项。", 18, MUTED)
save("03-confirm-meaning.svg", "S3 语义确认提案", s, "原句和将执行的可读释义并列；只有玩家确认才执行，没有隐藏 oracle。")

# S4: editorial composition, never a truth gauge.
s = top("04 / 编辑台 · 你愿意把责任写到哪一步", 4)
s += text(82, 178, "给今晚留下一句话", 40, family="serif")
s += text(83, 218, "标题草稿 / 你可以写，也可以修改", 19, MUTED)
s += rect(82, 254, 850, 225, SHEET, RULE)
s += text(110, 294, "本版标题", 17, MUTED)
s += lines(110, 356, "目击者称安保\n率先开火", 44, leading=64, family="serif")
s += line(112, 457, 901, 457, RED, 2)
s += text(83, 527, "系统整理的表达", 18, RED)
s += lines(83, 571, "你引用了目击者关于开火顺序的说法。\n这句话把说法归于目击者，而不是把它写成你的直接断言。", 23, leading=39)
s += button(82, 697, 300, "复核这一版标题  →", True) + button(404, 697, 240, "继续修改")
s += rect(962, 254, 394, 414, "#E6DCC6")
s += text(987, 295, "摊开的材料", 24, family="serif")
s += line(987, 319, 1329, 319)
s += lines(987, 363, "采访录音\n“安保先开火。”\n\n现场录像\n画面呈现民兵先开火。", 21, leading=36)
s += lines(987, 592, "只显示已取得材料。\n不提供“可安全刊发”评分。", 17, MUTED, 29)
s += text(84, 795, "完整列出所有主张；修改文字后，旧解析不再用于签发。", 18, MUTED)
save("04-editor.svg", "S4 编辑台提案", s, "标题纸占据阅读中心，侧边仅放玩家已打开的材料，不展示支持度。")

# S5: neutral wording and deliberate commitment.
s = top("05 / 签发 · 最后一次复核", 5)
s += rect(225, 143, 990, 643, SHEET, RULE)
s += text(267, 193, "晚报 / 本版签发单", 18, RED)
s += text(267, 259, "目击者称安保率先开火", 43, family="serif")
s += line(267, 290, 1170, 290, INK, 2)
s += lines(267, 339, "你把这句话写成目击者的说法。\n引用他人的话，同样需要对表述负责。", 25, family="serif", leading=44)
s += text(267, 465, "刊发时手上的材料", 18, MUTED)
s += text(267, 506, "采访录音    /    现场录像", 24)
s += lines(267, 570, "签发后，这一版会保留当时的标题和材料。\n你可以返回修改，也可以照此刊发。", 21, leading=35)
s += button(267, 666, 260, "返回修改标题") + button(551, 666, 320, "确认签发这一版", True)
s += text(267, 757, "焦点默认在“返回修改” · Enter 只激活当前按钮", 17, MUTED)
save("05-signoff.svg", "S5 签发提案", s, "中立措辞提醒与明确刊发动作，不泄露证据充分性，不显示结局预告。")

# S6: consequences read as an authored story, not a score screen.
s = top("06 / 余波 · 一张已经离开编辑台的纸", 6)
s += rect(145, 145, 1150, 625, SHEET, RULE)
s += text(184, 191, "THE LAST EDITION", 24, family="serif", spacing=3)
s += text(1082, 189, "本版已刊发", 18, RED)
s += line(184, 215, 1255, 215, INK, 3)
s += text(184, 283, "目击者称安保率先开火", 46, family="serif")
s += line(184, 314, 1255, 314)
s += text(184, 374, "他说过，事实仍有争议", 32, family="serif")
s += lines(184, 428, "你准确记录了目击者的说法，但录像提出相反证据。\n编辑要求后续报道说明争议；来源说过，不等于事实成立。", 24, leading=44, family="serif")
s += rect(184, 536, 658, 133, PAPER)
s += text(208, 573, "刊发时的材料", 18, MUTED) + text(208, 616, "采访录音 / 现场录像", 23)
s += lines(887, 569, "你的取舍\n你核查了开火顺序，\n没有继续资金线。", 21, leading=35)
s += button(184, 692, 270, "回看刊发归档") + button(478, 692, 335, "重新开始另一条调查线", True)
save("06-ending.svg", "S6 结局提案", s, "先呈现已刊标题与作者后果，再回看当时材料，不用真相分数结算。")

# Author-facing flow board. This is not a screen exposed to players.
s = top("作者规划 / 当前分支与未来界面衔接", "F")
s += '<defs><marker id="flow-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#8B302B"/></marker></defs>'
def arrow(d):
    return f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="3" marker-end="url(#flow-arrow)"/>'
def box(x, y, w, h, heading, body, dark=False):
    return rect(x,y,w,h,INK if dark else SHEET,RULE) + text(x+18,y+33,heading,22,PAPER if dark else INK,"serif") + lines(x+18,y+65,body,17,"#CCD0C0" if dark else MUTED,27)
s += box(80,153,270,130,"采访目击者","记录 / 施压 → 录音 + 来源\n不采用 → 不获得材料")
s += box(410,153,335,130,"最后一次追加调查","三选一：录像 / 账房 / 回桌\n界面先说明互斥代价")
s += box(810,153,540,130,"账房与交易","请求被拒 / 放弃 → 回桌\n提出 500 → 独立确认 → 账簿 + 作者扣费")
s += arrow('M350 214 L410 214') + arrow('M745 214 L810 214')
s += box(80,346,270,143,"证据册","随时打开，返回原页面\n只读已取得材料\n刊发归档用冻结快照")
s += box(410,346,335,143,"编辑台 ↔ 修改","预写标题（本轮）\n自由标题 + 完整确认（后续）\n不展示隐藏支持判断")
s += box(810,346,540,143,"明确签发 / 暂缓","签发 → 冻结当时证据与来源 → 作者结果\n暂缓 → 本版未刊发\n之后材料不倒改旧评估")
s += arrow('M577 283 L577 346') + arrow('M1080 283 L1080 314 L660 314 L660 346')
s += line(350,419,410,419,RULE,2) + arrow('M745 419 L810 419')
s += box(80,562,1270,111,"五类作者结果","支持报道 / 依据不足 / 归属成立但事实争议 / 无具体主张 / 暂缓；变量变化只来自已写作者事件。",True)
s += arrow('M1080 489 L1080 562')
s += text(84,724,"后续：输入 → 解析候选 → 玩家确认 / 改写 → 规则执行；NPC 只表述已授权的 Response Plan。",20)
s += text(84,765,"本图只描述已有实验结构与界面建议，不新增正史、schema 或模型权限。",18,MUTED)
save("00-flow.svg", "作者流程提案", s, "现有调查分支、证据阅读、编辑与签发的关系，明确区分本轮固定选择和后续自由输入。")
print(f"Wrote {len(list(OUT.glob('*.svg')))} SVG files to {OUT}")
