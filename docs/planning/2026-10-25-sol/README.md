# 2026-10-25 规划与交付索引

2026-10-26最新交付：[U5a首案体验定型](ITERATION_PLAN.md#u5-long-task)已完成0.4.0本地Windows包、作者稿第18节、chapter1.1/presentation1.2、表达卡与人物余波。[实际证据](verification/u5a/README.md)记录定向检查和一条原生路线；[首次读者表](FIRST_READER_NOTES.md)尚无真人数据。GitHub已按授权设为public并由连接器回读；本地0.4.0尚未提交/推送。

最新实施结果与待办见[06](../../06_CURRENT_STATE.md)/[07](../../07_HANDOFF.md)：0.4.0为当前交付，0.3.0及旧fixture保留。环境历史见[Unity与MCP](UNITY_SETUP.md)。

- [Unity 2D制作与迁移计划](UNITY_2D_PRODUCTION_PLAN.md)：U0–U4与U5a已交付；当前为U5b观察与单独源码同步。
- [样章设计 v1.0](FIRST_CASE_AUTHOR_DRAFT.md)：20个节点、5份材料、12个选稿、7项目录登记、完整后果及20条纸面路径，是本案细节的唯一正文；第17节呈现v1.1已独立装配，不改v1.0规则。
- [主规划与首案结构](ITERATION_PLAN.md#full-case)：保留20–30分钟目标及6个迭代/30项原任务，记录脚本实现已交付与玩家观察待办的边界。旧工作量不能作为新设计的剩余排期，旧委派词仅供追溯。
- [本地设计板](design-board.html)：早期 6 张关键屏幕 + 作者流程图、色板 / 字体 / 交互说明；本次未更新，尚未表现第 11 节的新案件结构。双击可离线打开。
- [新章入口](../../../ai/prototype/chapter_desktop.py)与[独立作者数据](../../../ai/content/railyard_chapter.v1.0.json)：默认启动脚本样章；旧短篇仍可-Legacy启动。
- [Unity 工程与启动](../../../unity/README.md)：Main场景与Windows包已有完整首案；菜单提供显式导入、构建和新增呈现检查。
- [实际截图](verification/)：本轮[u5a](verification/u5a/)记录末段取舍、人物余波、实际原句回看和最终表达卡，旧u3-u4保留。

## 上一规划检查点：Unity制作与剧情呈现计划

已确定Unity 2D、静态像素场景、清晰文字界面；先迁移v1.0规则，再做戏剧转场/末段取舍/人物回声/本局路径回看。当时仅交付计划，未创建工程或改代码；后来环境准备及U1–U2均已完成。首次玩家观察仍未进行。

## 上一实施检查点：首案脚本可玩样章v1.0

设计定稿已装配为独立版本运行数据/会话/界面，复用既有采访确认与阅读组件；三时段、两主线/两支线、五份材料、十二标题、明确签发/暂缓、编辑/来源/公司余波、事件账与重开均已接通。旧fixture与-Legacy入口保留，新支持关系不覆盖历史结果。

该实施轮26个不同测试通过（当前文档轮未重跑）：16项新规则、2项新Tk集成/回归、8项受影响的既有采访测试；原生窗口资金深入路线走至N99/事件账，默认启动器实际打开新章。发现报价回应转页丢失和长材料焦点跳底部，修复后仅定向跑新回归。命令、文件与限制见[06](../../06_CURRENT_STATE.md)/[07](../../07_HANDOFF.md)。

该历史脚本实施轮没有新模型请求、Unity、依赖安装、无关旧成功案例重跑或新截图文件。首位玩家/20–30分钟/取舍吸引力仍待观察；工程跑通不等于这些已通过。当前Unity结果以上方最新检查点为准，下一步为U5。

## 运行当前试玩

在 `F:\BTL-AI` 的 PowerShell：

```powershell
& .\tools\play_story.ps1
# 等价入口
& .\.venv\Scripts\python.exe -m ai.prototype.chapter_desktop
```

采访先载入示例、编辑原句、查看理解，再明确确认或返回改写。只有已接通脚本产生候选，脚本外文字保留且不执行。Tab 可离开输入框；Enter 在输入框内只换行。Ctrl+E 在写作时开证据，E/数字在输入框内仍是文字。新章可分配三段调查并进入两条深入方向，标题从作者选稿载入后逐项复核再签发。关闭不存档，无需密钥、联网或新安装。旧版入口用 `& .\tools\play_story.ps1 -Legacy`。

## I1–I2 实施检查点（历史，未重跑）

[interview_flow.py](../../../ai/prototype/interview_flow.py) 已实现原句/未执行候选/明确确认/改写作废/一次执行，复用原 validator 与作者选择。四个可见脚本用于如实询问、施压、复合策略与含糊表达。没有 oracle、任意语言解析或生成 NPC。界面增加阶段区分、确认后原句/回应、调查取舍提示、证据册返回的草稿/页面位置/焦点保护，以及输入区快捷键隔离。

该实施检查点只运行新 `test_interview_flow.py`：**8 passed**。当时实际窗口完成脚本外改写保留→证据往返→普通理解→返回改写→复合语气全部三策略→明确确认→录像→归属标题→作者争议结局→重开。修正并定向复核一次载入示例的过期失败提示。本轮复用了当时的窗口/截图证据；这8项控制测试因共享钩子受影响实际复测通过，其他旧例未重跑；新调用仍为0，历史总计仍12。

[新截图](verification/i1-i2/)包含 [起草](verification/i1-i2/compose.png)、[失败保留](verification/i1-i2/draft-retained.png)、[三策略确认](verification/i1-i2/review-all-tactics.png)、[确认后](verification/i1-i2/executed.png)、[结局](verification/i1-i2/ending.png)。旧 SVG 仍是完整目标提案；当前只实现其离线确认子集。真人观察、任意语言/中文模型质量、真实 NPC 生成、字段级修订、完整光标/选择恢复及 IME 组合过程尚未验收。

## 最初图形交付账目（历史，未重跑）

| 类型 | 真实完成 | 不可外推的范围 |
| --- | --- | --- |
| D18 模型测量 | 新结果原件已读取；1 请求、runtime / fidelity PASS、三策略与 PHOTO_01 正确；913 input / 131 completion，1.192 秒；批次已关闭 | 仅这个英文案例、该模型/prompt/input 配置；没有中文或任意语言准确率 |
| 证据保存 | 27 个 fingerprint 文件均匹配；JSONL 逐字节保留；sources.zip 含匹配源文件与 fingerprint | 不覆盖、删除 ignored 原件；已完成批次没有“剩余可用调用” |
| 图形实现 | 进入、采访、一次调查取舍、可选交易、证据阅读、预写标题选择/修改、签发、五类作者结局与重开 | 固定选项 / 作者文字 / 实验故事；不是实时自由输入 AI 游戏 |
| 当时自动验证 | `tests/test_story_desktop.py` **2 passed**；PowerShell 启动器语法通过 | 只覆盖当时新增玩家投影边界；本轮未重跑 |
| 实际窗口 | 资金线完整操作一次：record → clerk → offer500 → accept → 证据册 → security → edit → funding → publish；再点击重新开始 | 只实际走这一条；未逐条点完其余结局，未验证其他 PC / 缩放 / 辅助技术 |
| 视觉检查 | 实际开始/证据/签发/结局画面已查看并留截图；7 份 SVG 用本地 Sharp 渲染并查看，HTML 的 25 个本地引用已检查 | 浏览器工具禁止 `file:`，未做 HTML 浏览器画面验收；设计稿不等于实现，没有真人玩家验证或实际 20–30 分钟时长数据 |

D18 原件 SHA-256：`8de084cbccea36fdfddea911e3a0fbab1b4c895df461ebd0c05e33a0c83c941d`。三批真实请求合计 **8 + 3 + 1 = 12**，本任务未另发实时请求。费用均受原批准的 Free tier / USD 0 边界限制；成功记录估计 0，不等于独立核对账单。

## 提案资产与再生成

| 文件 | 内容 |
| --- | --- |
| [00-flow.svg](screens/00-flow.svg) | 作者流程：已有分支与未来界面连接 |
| [01-interview.svg](screens/01-interview.svg) | 采访 / 自由输入提案 |
| [02-evidence.svg](screens/02-evidence.svg) | 已取得材料的双页阅读 |
| [03-confirm-meaning.svg](screens/03-confirm-meaning.svg) | 可读释义 / 玩家确认与返回改写 |
| [04-editor.svg](screens/04-editor.svg) | 自由标题 / 完整表达说明 |
| [05-signoff.svg](screens/05-signoff.svg) | 中立提醒 / 独立签发 |
| [06-ending.svg](screens/06-ending.svg) | 作者余波 / 刊发归档 |

所有 SVG 使用代码绘图与系统后备字体，没有外部美术资产或图像服务。要修改设计稿，编辑 [build_designs.py](build_designs.py) 再运行：

```powershell
& .\.venv\Scripts\python.exe docs/planning/2026-10-25-sol/build_designs.py
```

当前停在Unity制作与剧情呈现计划交付。细节维护作者稿，执行细目维护制作计划，进度维护主规划与06/07。Unity开始制作、新模型请求和费用仍需相应授权；原设计板和图形资产保持不变。
