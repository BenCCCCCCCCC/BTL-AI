# Current State｜BTL-AI

## 最新 U5a首案体验定型版0.4.0

2026-10-26：按[主规划第13节](planning/2026-10-25-sol/ITERATION_PLAN.md#u5-long-task)完成U5a制作。作者稿第18节落实三人的个人牵挂与首尾回声；独立chapter.v1.1/presentation.v1.2装配，原v1.0内容/旧fixture保留。三段调查、五材料、500交易、十二选稿、N91–N96和证据支持政策延续；Company A在新内容中统一中文名“澄川实业”，主体ID不变。候选结构、执行权、Frozen及八项Hard Safety Gates未改。

表达卡显示完整原句，编辑入口按需展开；保留原句→完整意图→返回/明确确认→执行。最后一段列当前实际可选机会成本；新余波短场景由原始人物回应匹配，已知澄清省略仍收到质询，暂缓不制造刊发联系。余波合并阅读到归档，工作单/路径可展开；删去重复动作/教学及选卡后的旧正文，签发保留标题与可展开的已复核含义。复用三场景/三头像，补人物名片与字号对比度。

Windows入口：`Builds/BTL-Internal-0.4.0-Windows/BTL.exe`；分发包`Builds/BTL-Internal-0.4.0-Windows.zip`。0.3.0包保留。新包186文件、51,619,620字节，散列与实际检查见[U5a证据](planning/2026-10-25-sol/verification/u5a/README.md)。本轮U5定向检查通过，Windows实走初访→A→B付500→S-A→H11→签发→人物回应→N99回看；末次纯阅读修正后仅重建及定向界面核对，没有重复整案或无关旧测试。新增模型请求0，累计仍12。

U5b真人观察尚未执行，[记录表](planning/2026-10-25-sol/FIRST_READER_NOTES.md)已备好；实际时长、乐趣、IME组合和其他电脑仍待证。GitHub公开已完成：[BenCCCCCCCCC/BTL-AI](https://github.com/BenCCCCCCCCC/BTL-AI)，2026-10-26 03:12（Australia/Sydney；UTC 2026-10-25 16:12:43）连接器get_repo回读`visibility: public`。用户登录内置浏览器后，按已记录授权在Settings执行可见性修改，[页面凭据](planning/2026-10-25-sol/verification/u5a/github-public.jpg)已保存。没有公开失败遗留。

2026-10-26用户明确要求push，现已提交并推送到活动分支`prototype/technical-prototype-01`。源码交付提交为[`4cddf5f`](https://github.com/BenCCCCCCCCC/BTL-AI/commit/4cddf5fb1fbd6bc8b89b33d39b6d5d4156038e35)，209文件包含0.4.0与其此前未同步的脚本、作者数据、Unity底座、资源和文档依赖；远端由`10c969a`正常推进到该提交。此后文档提交记录同步回执，当前HEAD以Git为准。提交前核对209路径及3个来源归档，无所查高置信凭据签名；Builds、缓存、logs及本机配置未入库。未pull、合并main或刷新Project Sources；未新增运行测试或模型调用。下一步为U5b首次读者观察，已有工作副本按07同步。

## 上一规划：U5首案体验定型长任务（已进入实施）

2026-10-26：按游戏设计/制作评审更新[主规划第13节](planning/2026-10-25-sol/ITERATION_PLAN.md#u5-long-task)。下一轮U5a完整推进人物牵挂、主支线取舍、脚本采访确认、刊发余波、路径回看、中文阅读与Windows交付；U5b单列首次读者观察。计划目标版本0.4.0，当前实际交付仍为0.3.0。详细执行顺序只维护在主规划，制作计划与交接提供入口。

本轮仅修改规划/交接及入口文档，没有执行长任务、改代码/作者数据/资产、启动Unity、构建、运行测试或新增模型请求。检查限定为改动文档的事实、状态与链接一致性；历史12次模型请求及既有工程验证均无新增结果。仍无真人时长/乐趣结论。

用户已明确授权**下一轮长任务完成后**把本项目GitHub仓库设为公开；本轮未更改或核验远端可见性。下一轮按主规划13.6核对实际远端、公开内容和权限后执行并回读，不重复询问同一授权；具体凭据/隐私或权限阻碍另据事实处理。公开与代码同步分别报告。

未commit/push/pull、刷新Sources或重查此前受限的Git状态。活动分支/HEAD仍只引用历史记录 `prototype/technical-prototype-01` / `10c969a78bfbe889f5f8c15e923620e821c23ef2`，不作为本轮新核验。下一动作是收到执行指令后按主规划13.7启动长任务；复制范围见07。

## 上一 U3–U4 首案内部试玩版（当前可运行交付）

2026-10-25：U3–U4 合并交付内部版 **0.3.0**。复用既有 Unity 工程/MCP，完整首案接通初访、三段调查、A/B/S-A/S-B、五份材料、十二作者选稿、整句复核、签发/暂缓、人物余波、工作单、本局纵向回看与重开。Windows入口为 `Builds/BTL-Internal-Windows/BTL.exe`，分发包为 `Builds/BTL-Internal-Windows.zip`；[运行与重建说明](../unity/README.md)。

独立[呈现v1.1](../ai/content/railyard_presentation.v1.1.json)已装配：人物诉求、材料后的记者自问、最后机会、六类收束和已知未完成方向。只读 `ChapterPresentation` 用实际确认原句、作者回应、材料与事件生成回看，不泄露未开放支线。Core仅补历史记录及只读查询；v1.0支持政策、数值和后果规则不变，Python、旧fixture及Frozen未改。三张原创静态像素场景/三头像由本地绘图脚本生成，Noto中文字体及许可证随包；UI补三档字号、窗口缩放、正文选择、独立材料册、分组标题、折叠回看及退出说明。

实际验证：新增呈现检查通过 A→S-A→H12、B→S-B→H10 的原句/回应保存、材料笔记、只读回看与未开放内容不披露；修正null来源显示后只复核该呈现检查。Windows独立包实际走完初访→B报价/接受500→S-B查科目→提前回桌→H10两项复核→签发→编辑/公司回应→工作单/路径/事件→重开。看到600→100、回访不再收费、费用−500与声誉+1分列、重开后三段/600且材料清空。另定向检查中文粘贴、Enter换行、脚本外保稿、材料保稿、字号与缩放，修复实际发现的焦点和反馈问题。[实际截图](planning/2026-10-25-sol/verification/u3-u4/)与详细边界见07。最终Windows构建成功；未重跑U1规则套件、Python历史案例或模型，真实模型累计仍12次。

下一步是[U5首次读者观察](planning/2026-10-25-sol/UNITY_2D_PRODUCTION_PLAN.md)，不是追加系统。尚无真人时长/乐趣、IME组合、其他电脑或辅助技术结论，也未逐条原生点击六种结局；关闭/重开不保存。未commit/push/pull或刷新Sources；分支/HEAD沿用上一记录，按此前限制未重新查询Git。复制范围见07。

交付收尾：原句回看中的签发/暂缓可重新展开完整实际后果与人物回应，N94保留原编辑复核要求；受影响呈现检查通过。zip约49.2 MiB，包内有构建/源散列记录，详细校验值和编译提示处理见07。两份源/Generated数据一致，文档链接核对完成。

## 上一 U1–U2 Unity 离线可玩检查点（历史）

2026-10-25：复用 `F:\BTL-AI\unity\BTL`、Unity 6000.3.10f1 Universal 2D 和既有 MCP，完成[首条 Unity 可玩路径](../unity/README.md)。`Assets/BTL/Main.unity` 接入 C# `ChapterSession` / `ChapterInterview` 与中文 UI Toolkit。作者 JSON 以同散列副本导入；源 `ai/content/railyard_chapter.v1.0.json`、Python 代码、旧 fixture、Frozen 合约均未改。Unity 会话拥有本工程的权威状态；采访仅用精确脚本候选，原句→完整理解→改写或确认→执行，失败保稿、不预支行动。目录、证据、三时段、待确认付款、标题整体复核、支持判断、刊发快照、事件去重和作者后果已迁移到 C#。

实际验证：Unity 编译后控制台 0 错误/警告；`BTL/Run U1 Focused Checks` 通过，覆盖采访预览/过期、500 交易、H4/N91、快照防外改、标题拒绝、暂缓、澄清和零主张刊发。Play Mode 人工走通初访→B 报价/付款（600→100，E1/E3）→H4→签发→刊发记录→人物回应→N99；另走“不采用初访→暂缓→N96→重开”，看到三段/600归零复位。最后修正空原句与暂缓标题后再次编译，0 错误/警告。没有跑 Python、模型或无关历史案例，真实模型累计仍 12 次。未执行 Windows 构建或真人试玩；IME 组合、不同缩放/电脑、字体随包分发、完整 U3 剧情呈现与时长/乐趣仍待验。

改动集中于 `unity/BTL/Assets/BTL/` 的 C#、Main 场景/PanelSettings、作者 JSON 副本及 `.meta`，另更新 README、主规划、制作计划和 06/07。当前未 commit/push/pull，未刷新云端 Sources；沿用上次记录的 `prototype/technical-prototype-01` / `10c969a78bfbe889f5f8c15e923620e821c23ef2`，按用户此前限制未重新查询 Git。下一阶段按[制作计划 U3](planning/2026-10-25-sol/UNITY_2D_PRODUCTION_PLAN.md)做完整主支线呈现与本局路径回看，U4 再补字体/美术/本机包，U5 为玩家观察。

## 上一空工程与MCP检查点（历史）

2026-10-25：用户已授权“建立本地工程、MCP、Git ignore”。本轮已完成空工程与连接准备，游戏内容未开始；详情见[Unity准备记录](planning/2026-10-25-sol/UNITY_SETUP.md)。

工程`F:\BTL-AI\unity\BTL`已由6000.3.10f1 LTS从本地Universal 2D 6.1.2模板创建，创建批处理退出0。固定MCP桥接v10.0.0已装入包清单/锁文件，Git依赖hash为`d49ae2953580f3481beb1e084a1da2682f0b5610`。Unity解析URP17.3.0、Newtonsoft Json3.2.2；保留模板场景/资源，未导入Python案件。

MCP服务沿用`E:\AI\Tools\unity-mcp`的10.0.0与已有Codex URL。原生MCP工具已实际连通`BTL@9e2f981c2b142ed8`：工程路径正确、Editor idle/未编译/未更新、ready_for_tools=true，错误/警告读取返回0。Editor保持打开；许可证成功解析，Windows构建尚未执行。只新增Editor连接工具`Assets/Editor/BtlMcpConnection.cs`，菜单为BTL/Connect Local MCP，无游戏逻辑/模型调用。

根.gitignore追加BTL的IDE生成文件与本地MCP状态规则；49个源文件未忽略、8项缓存/IDE路径已忽略，无嵌套.git。保留Assets/.meta、Packages清单/锁文件和ProjectSettings，Visible Meta Files/Force Text已核实。只做check-ignore新检查，没有重试旧分支/HEAD/status查询，也未commit/push/pull。

Computer Use窗口读取授权曾超时，未操作Hub；改用官方Editor命令行完成创建，未核验Hub项目列表。首次临时Git检查脚本的CRLF尾字符问题已用NUL输入修正。实际验证仅安装/编译/MCP只读/忽略规则与文档链接（8份文档、118个本地链接/锚点通过）；没有运行Python旧测试、Unity测试套件、Play Mode或模型基线。历史26项及12次模型请求仍是历史证据。

同步新增unity/README.md、BTL Assets/Packages/ProjectSettings，修改.gitignore和README、06/07、主规划/索引/制作计划/UNITY_SETUP。Library/Temp等缓存和外部MCP服务环境不入Git；云端Sources未刷新。下一轮可从既有工程开始U1/U2，无需再创建；当前授权只到环境，中文UI/IME与规则迁移未实现。

## 上一文档规划检查点

以下记录保留当时事实；段内“本轮/下一轮/当前”均指该历史规划轮，环境现状以顶部最新检查点为准。


更新：2026-10-25（Australia/Sydney），Unity 2D制作与剧情呈现计划 / 文档 checkpoint。阶段：**04 — Technical Prototype 01，进行中；Unity未创建**。

沿用上一检查点记录的活动分支 `prototype/technical-prototype-01`、HEAD `10c969a78bfbe889f5f8c15e923620e821c23ef2`，本轮按用户要求没有重试此前被拒绝的 Git 查询，未重新核验 Git 状态。保留原有本地工作；本轮仅更新规划与交接文档，**没有 commit / push / pull**。`main @ aa87d39959e6a4b2f6cad31883528cb8e8d1cc42` 是历史设计基线。

### 上一规划的结果与停点（历史）

已按用户方向完成[Unity 2D首版制作与迁移计划](planning/2026-10-25-sol/UNITY_2D_PRODUCTION_PLAN.md)，由[DEC-024](05_DECISION_LOG.md#dec-024)记录：Unity 2D＋静态像素背景＋清晰文字界面；一个场景、三背景、三基础头像、共用UI Toolkit阅读/确认组件。复用现有chapter.v1.0作者数据与语义，C#重新实现权威规则，不嵌入Python。已有十二标题、五材料、三时段与支持/后果政策保持不变。

[作者稿第17节](planning/2026-10-25-sol/FIRST_CASE_AUTHOR_DRAFT.md#chapter-presentation)完成剧情呈现v1.1设计：任务与人物诉求→调查引出矛盾/边界→最后时段取舍→签发/暂缓→具体人物回应→本局工作单和因果回看。新增转场与回看不扣资源、不授予证据、不改结局；运行数据尚未增加该呈现版本。不扩成多主角、QTE、第二案件或全分支树。

迁移排序已并入原主规划：U0工程落位→U1规则迁移→U2首条可玩路径→U3全量支线及呈现→U4有限美术/本机包→U5玩家观察。下一轮Sol提示只覆盖U0–U2，保存在制作计划第8节，未发送到其他聊天、未切模型。当前明确限制仍是只做计划；下一轮获得创建/实现指令后才执行。I4存档/记忆、I5在线接口推迟，原30任务编号与未验收项保留，不先造Python存档。

本轮实际核对10份文档、135个有效本地链接/锚点，原30项任务编号保留；37个既有代码/数据/测试/工具文件前后散列一致，拟建Unity工程目录仍不存在。仅做文档事实/状态一致性与未变检查；未运行pytest、Unity、模型、图像生成或安装依赖。历史脚本26项通过和模型12次请求没有更新，不是新C#或真人证据。仍未知本机Editor/许可证/Windows构建支持、Unity字体/IME/焦点适配及20–30分钟实际体验；制作计划把早期中文输入检查和针对端口的新验证列为必要工作，不用旧Python通过代替。

交付范围10份文档：README、00、01、05、06、07、规划索引、ITERATION_PLAN、FIRST_CASE_AUTHOR_DRAFT，以及新增UNITY_2D_PRODUCTION_PLAN。没有代码/JSON/fixture/合约/资产改动，无commit/push/pull或云端同步；本轮复制清单见07。以下实现和测量均为历史检查点，段内“本轮”指相应历史轮次。

## 上一脚本实现检查点的结果与停点

**首案[脚本可玩样章v1.0](../ai/prototype/chapter_desktop.py)已接通。** 默认入口 `tools/play_story.ps1` 打开新章，`-Legacy`保留旧短篇；旧fixture/规则未覆盖。独立[作者数据](../ai/content/railyard_chapter.v1.0.json)与[样章会话](../ai/prototype/chapter_session.py)装配设计v1.0的三时段、两条主线/两条支线、五份完整材料、十二个标题和刊发/暂缓/人物余波/事件账/重开。I3脚本实现已交付，玩家判据未验收。

采访复用InterviewFlow和既有Tk阅读/键盘组件。共享处只增加默认兼容的上下文/目录/执行钩子与界面数据入口；当前场景目录复核、返回改写作废、确认一次执行继续有效。新章的五处交涉（含交易接受/拒绝）都走原句→完整理解→确认；普通背景问答和界面退出单独标识。精确脚本之外保留原文，不做关键词近似、任意自由文本理解或新模型调用。

A/B/S-A/S-B每场最多结算一段，进场前可取消；报价、取消Pending、拒绝并结束、付款交付分别处理。E1/E4按实际普通/施压/追问版本保留；E3/E5同号联结。取得支线材料后开放相应选稿；H10有付款预设和用途两原子，H12保留旧来源归属与相反底层材料关系。合法但依据不足/错误归属可刊发，目录外或未完整理解的标题整句不执行；省略已取得的澄清触发编辑复核。

刊发冻结原始标题、全部原子、实际材料正文、来源、合作状态、此前事件与四个版本。新支持关系不读取隐藏真相；旧fixture和历史快照继续沿原规则。付款/施压/专业跟进/编辑复核均经既有作者事件入口：钱600或100，风险每来源最多+1，声誉每篇+1或-1一次；读者/公司追问不加公众态度。样章仍为Experimental，不改变Unity权威或Frozen字段/八项Hard Safety Gates。

**本轮增量验证：26个不同测试通过。** `test_chapter_session.py`新增16项、`test_chapter_desktop.py`新增2项；`test_interview_flow.py`因共享钩子受影响实际重跑8项。先24 passed，再新Tk完整路线1 passed，发现窗口具体问题后只跑新回归1 passed，没有扩大回归。所有调用为离线，不是模型fidelity或真人测试。

真实窗口通过computer-use走完：初访记录→B报价→明确接受500（600→100）→S-B核对科目→提前回桌→H10→复核两项含义→签发→编辑/公司回应→N99事件账。Tk控制集成另覆盖A→S-A→B→H12→回看→重开，验证旧引语底层仍相反、四份材料和全部新局状态重置。PS启动器语法无错误，默认启动器实际打开更新后封面。窗口检查发现“报价回应转页丢失”和“长材料默认聚焦底部继续按钮”，均修正并针对验证；未保存新截图文件。

未重跑无关旧StorySession/player-view/model/baseline案例，模型总数仍12且授权关闭。没有新模型请求、Unity、依赖安装、存档或真人观察。下一步请首次读者体验两种深入方向，观察取舍价值、来源/事实理解、阅读密度与时长，再按具体问题修改；不能将脚本闭环当成20–30分钟和乐趣已验证。

文档/内容核对：8份文档、100个有效本地链接/锚点；12个运行标题与定稿一致，五份材料正文、7项目录与30项原任务编号齐全，新章作者数据不含oracle。

## I1–I2 离线实现检查点（历史，未重跑）

**“原句 → 系统理解 → 确认或改写 → 执行”的离线采访流程已实现，并接到既有调查和刊发结局。** 上一轮授权是只用脚本候选、不新增模型调用、不创建 Unity、不重跑成功案例。该范围内的本地实现已完成，玩家验收未完成。下文实施与验证叙述属于该历史检查点。

新增 [interview_flow.py](../ai/prototype/interview_flow.py) 管理尚未执行的草稿、不可变候选、返回改写、明确确认与执行收据。提供如实询问、施压追问、复合语气和含糊表达四条可见脚本；只有精确示例（允许首尾空白）产生预写候选，不做关键字猜测、任意改写理解或 oracle 对照。脚本外文字 / 含糊句保留原文，不执行；可重新载入示例。离开采访是单独复核的作者选项，不伪装为模型解析。

候选复用 Frozen 字段、现有 `PROP_FIRE_FIRST` 和原 `validate_dialogue_candidate`。确认卡列出行动、全部策略、提及的可见证据和采用采访的选择；内部 ID / hidden support 不给玩家看。返回改写立即作废旧候选；确认时再校验当前目录，然后只调用既有 StorySession 的 record / pressure / leave。预览不授予证据、不消耗调查机会、不改四变量；确认仅执行一次。NPC 显示现有作者原话/施压回应，本轮没有新增表层生成器、NPC gate 能力或语义 schema。

阅读和操作打磨：起草 / 复核 / 已执行分屏；复核默认焦点在返回改写；已执行页保留刚才确认的原句及作者回应；调查选项说明一次机会的取舍。输入框内 Enter 仅换行，Tab 可离开，E / 数字不触发快捷行动，Ctrl+E 可翻证据。证据册往返保留原句、页面滚动与焦点；载入新示例清掉旧失败提示。未实现文字光标/选择区的完整恢复、字号设置或屏幕阅读器认证。

该实施检查点实际验证：当时新 [test_interview_flow.py](../tests/test_interview_flow.py) **8 passed**；实际窗口操作脚本外改写保留、证据册往返、普通理解→返回改写→复合语气三策略→明确确认→录像→归属标题→签发→争议结局→重开。只有确认后取得录音；末尾风险 +1、资金仍 600，沿原作者事件。发现并修正“载入示例仍残留旧失败提示”，仅为该缺陷重启窗口并定向复核；没有扩大回归。[该批截图](planning/2026-10-25-sol/verification/i1-i2/)区分起草、失败保留、复核、执行与结局。

该实施检查点 **0 模型请求**，既有三批累计仍为 12，授权关闭。没有跑旧 2 项玩家视图测试、StorySession 测试、baseline、D18 或 Headline/NPC；未安装依赖、创建 Unity 或刷新云端 Sources。工程操作不是真人验证；未知中文输入质量、IME 组合输入、不同 PC/缩放与完整 I1/I2 玩家完成判据仍未验证。

上一检查点：用户在本机隐藏输入后产生第三批结果，当时直接读取现有文件并归档，没有重复运行启动器。D18 首次 runtime PASS、fidelity PASS：REQUEST / REVEAL_PAYMENT_PAYER，PHOTO_01，THREAT + ACCUSATION + INDIRECT_PROBE，缺失/多余均为空，无 retry / fallback / hard safety breach。该结果只证明这个英文输入在该配置下成功，不证明一般中文理解或自然语言安全。

随后实现 [story_desktop.py](../ai/prototype/story_desktop.py) 和 [启动器](../tools/play_story.ps1)，复用未修改的 StorySession、故事 fixture、发布快照与作者后果。完整流程为：进入 → 采访 → 一次调查取舍 → 可选账簿交易 → 查看已获证据 → 选择/返回修改预写标题 → 明确签发 → 作者结局 → 重新开始。纸张、墨色、暗红批注与 Canvas 货场剪影构成轻量桌面阅读界面。玩家界面不显示 oracle、技术字段或隐藏支持判断。

这是 **Experimental / Validation-only / Non-canonical 的本地脚本候选 + 预写分支试玩**，可以编辑原句但不解析任意文字，不含故事模型调用、持久存档、Unity 或生产 Dify；不能称为完成 Remake AI demo。关闭不保存。20–30 分钟仍是目标，当前短篇没有真人时长数据。

## 三批真实模型测量

三批合计 **12 次 HTTP 请求：8 + 3 + 1**。均为已批准的 Groq Free tier / `openai/gpt-oss-20b`、每次上限 2048 completion tokens（含 reasoning）、low reasoning、USD 0、无付费 fallback。三份授权单现均 **COMPLETED / execution_authorized=false**；未用次数不延续为新许可。

| 案例 | 首批 01：5 例 / 8 请求 | 复测 02：3 例 / 3 请求 | D18 单例 03：1 例 / 1 请求 |
| --- | --- | --- | --- |
| Dialogue D18 | 两次 HTTP 400，无候选，语义不可评 | runtime PASS，只有 THREAT，漏 ACCUSATION / INDIRECT_PROBE；fidelity FAIL | runtime / fidelity PASS，三项策略与 PHOTO_01 全部正确 |
| Headline T01 四主张 | 一次 runtime / fidelity PASS | 未重跑 | 未重跑 |
| Headline T02 零主张 | 两次归一化后缺 claims，保留草稿并阻止发布 | 一次 RESOLVED + claims=[]，runtime / fidelity PASS | 未重跑 |
| Headline T10 单主张 | 一次 runtime / fidelity PASS | 未重跑 | 未重跑 |
| NPC N01 | 两次原样输出 PAYER=COMPANY_A，被 gate 拒绝，最后使用作者 fallback | 一次自然对白 Company A paid me. 通过原 gate，无 fallback | 未重跑 |

首批首次成功 2/5；不能把含模板的最终 3/5 当准确率。复测 runtime 3/3 不等于 fidelity 全过。第三批只重测 D18，一次通过不构成通过率估计。三批均无已记录 hard safety breach，仅限此小样本。语义 FAIL 没有触发 retry，oracle 始终仅为离线评估。

| 批次 | 已记录 tokens：input / completion | 模型请求时延 | 请求/费用说明 |
| --- | --- | --- | --- |
| 01 | 3,911 / 716（六个有响应请求） | 0.399–0.946 秒，中位 0.640 秒 | 另两次 400 无 usage，不能当已知零 token |
| 02 | 2,027 / 203 | D18 1.494 秒；T02 0.416；N01 0.376 | 三个首次请求，无重试/fallback |
| 03 | 913 / 131 | 1.192 秒；端到端约 1.200 秒 | 只有一个首次请求，无重试/fallback |

已记录 usage 合计 6,851 input / 1,050 completion，另有两个错误请求 usage 未知。01/02 的约 30/60 秒案例耗时主要来自人为限速；03 没有等待第二次请求。成功记录 estimated_cost 均 0.0，费用边界为用户确认 Free tier / USD 0；未独立核对账单。

## 证据与修正边界

[evidence](../ai/eval/evidence/) 保留三份原始 JSONL 与各自 sources.zip。读取时，01 / 02 / 03 的 **21 / 26 / 27** 个 fingerprint 源文件 SHA-256 均匹配；03 的归档发生在新增图形代码之前，准确保留当次运行的源文件。原始 ignored 输出未覆盖/删除。归档中没有凭据；03 的 sanitise 比对未发现需要替换的字符串，证据副本逐字节一致。JSONL SHA-256：

- 01：`95a7e34fec0205e0127541f2caddbed70eaabf12f93b0d67d81c4c934217049b`
- 02：`01ac998c7bb16c3f5ff6782a10330eb524a0988a88c12e4717bc11484e0b6fc2`
- 03：`8de084cbccea36fdfddea911e3a0fbab1b4c895df461ebd0c05e33a0c83c941d`

此前修正仍保留：Groq v0.2 wire schemas 不向 provider 发送 uniqueItems，本地原 transport 仍校验重复项；Headline envelope 用 anyOf 保证 RESOLVED 的 claims 是数组，不把 null 自动补为 []；NPC v0.2 提供作者关系与自然第一人称上下文，没有塞 expected sentence / fallback / oracle。首批 400 的具体 schema 根因并未被单独证明。

第三批使用 [Dialogue prompt v0.3](../ai/prompts/dialogue_parser.groq.experimental.v0.3.txt) 和 [执行上下文 v0.3](../ai/eval/baseline_execution.experimental.v0.3.json) 中的三项通用策略描述及多策略保留规则；没有填入 D18 答案。它们原先未测，现在仅有本次单例成功。Headline T01/T10 仍是旧 prompt/wire 成功证据，未对新版重跑。NPC 词法 gate 仍不是任意自然语言的完整语义保证。

上述模型检查点未修改 Frozen、Decision Log、共享 runner/validator/NPC gate、OpenAI 专用 adapter、原 manifest、旧 prompts/schemas，以及 StorySession / 现有故事规则。当前设计检查点仅在 Decision Log 增加 DEC-023；LLM 输出没有接入 canonical state。

## 最初图形验证与规划交付（历史，未重跑）

| 类型 | 实际执行 | 限制 |
| --- | --- | --- |
| 新玩家视图测试 | `tests/test_story_desktop.py` **2 passed** | 只测已获材料/交易文案投影及快照读取，不复制旧故事分支测试 |
| 启动器 | `tools/play_story.ps1` PowerShell parser 通过；实际 Python 模块启动窗口成功 | 未改变执行策略或安装依赖 |
| 实际窗口路径 | record → clerk → offer500 → accept → 证据册 → security → edit → funding → publish → 重新开始 | 只走这一条；交易前 600、确认后 100；证据仅录音/账簿；结局 +1 声誉/+1 公众反应/-500 资金，重开恢复 600/空证据 |
| 画面 | 开始、证据册、签发、结局实际查看并保存 [截图](planning/2026-10-25-sol/verification/) | 非真人玩家研究；未逐条点全部结局/其他机器/缩放或屏幕阅读器 |
| 规划视觉 | 6 屏 SVG + 作者流程图，本地 Sharp 渲染并查看；HTML 本地引用检查 | 浏览器工具禁止 file:，未做设计板 HTML 浏览器画面验收；SVG 提案不等于已实现 |

历史证据复用而未重跑：此前本地入口/故事/mock **45 passed**，全 manifest **18 cases / 28 scripted attempts / 0 requests**；此前启动器授权 **1 passed** 与语法检查；修正 **17 个不同测试**（15 + 2，后续定向复跑 1 + 2，累计 20 次通过）。更早 48 / 61 / 82 / 104 passed 是历史报告。此次没有全库回归、旧故事重跑、依赖安装/升级或额外模型测试。继续使用 Python 3.12.10、pytest 8.4.2、Tk 8.6。

[主规划](planning/2026-10-25-sol/ITERATION_PLAN.md)包含玩家幻想、25 分钟目标节奏、现有证据/来源/后果、六屏流程、色板/字体/操作、Python→Unity 边界、grounding/有限记忆/存档/作者内容引入时机、费用与等待体验。后续被组织为 **6 个迭代 / 30 项任务**，含依赖、主要模块、完成条件、原始工作量区间与不确定性；旧中文实施委派词仅供历史追溯，不能再次照单执行。[设计板](planning/2026-10-25-sol/design-board.html)和[索引](planning/2026-10-25-sol/README.md)区分未来提案与既有运行截图。本轮没有新增或重生成设计资产。

## 未决与后续条件

最新下一实施步为获明确授权后的Sol U0–U2；创建与代码尚未执行。首次读者观察继续待办，可用现有样章进行：两条支线是否产生不同的报道意图，能否解释“说过/看见/事实”和刊发后果，三时段取舍是否有价值，实际时长与阅读负担如何。脚本样章已完成，不再把同一轮内容装配列成待办；I3玩家验收尚未完成，I4–I6代码仍未开始，I5离线部分已按最新计划前移。

任意自由文本理解、真实NPC生成、中文模型质量、IME组合过程、多PC/缩放/辅助技术、有限记忆/存档、真人验证和Unity仍未验收/实现。runtime PASS、脚本精确匹配或玩家确认不等于模型fidelity。新调用/费用与Unity仍另行授权；不重刷已通过样例。

## 上一实施检查点的同步记录

此前会话有 fetch + fast-forward pull `e1e6655 → 10c969a` 的记录，本轮未再 pull、commit 或 push。GitHub 与 ChatGPT Project Sources / Instructions 均未刷新；不把本地文档更新当云端已同步。

本轮同步16个文件：新增 `ai/content/railyard_chapter.v1.0.json`、`chapter_session.py`、`chapter_desktop.py`、两份 `test_chapter_*`；修改 `interview_flow.py`、`story_desktop.py`、`tools/play_story.ps1`；文档为README、00、05、06、07与规划目录的作者稿/主规划/索引。完整路径和命令见07。旧fixture、schemas/validators、模型配置/证据、设计板与截图未改。已有上一检查点的环境同步这16份；云端Sources未刷新，未提交或推送。


## 当前文档检查点的同步

最新10份文档清单见07；此前16份脚本交付文件仍是运行底座。已有上轮环境只补这次文档，无旧底座者还需上轮代码和数据。分支/HEAD沿用既有记录，未重试Git查询；本轮无commit/push/pull、无Project Sources/Instructions刷新。禁止把本地规划写成Unity已创建或把历史26项写成本轮测试。
