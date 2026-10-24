# Current State｜BTL-AI

审阅：2026-10-25（Australia/Sydney）  
阶段：**04 — Technical Prototype 01，进行中**  
活动分支：`prototype/technical-prototype-01`  
本轮审阅起点：`e1e66556ae67aed32ef6e739bec4183d708c6b88`  
最新实现锚点：`38703c4368ae774ebc36b6cbdc27cd61dd1a8c87`  
历史设计基线：`main @ aa87d39959e6a4b2f6cad31883528cb8e8d1cc42`

## 当前结论

产品定义、VI01、VI02 与 Gate 03 已完成；Experimental Python 验证组件已实现。**尚未恢复可核验的真实模型基线，也未交付可玩的 Remake demo。**

远端审阅起点比 main 多 12 个提交、无落后提交；当时无 open PR。最新实现之后的 5 个提交仅更新文档。main 仍是历史设计基线，不能作为最新实现读取。当前 Contract 为 Frozen **v0.1.1**；报告 09–11 的历史 v0.1 内容不覆盖它。

## 进度与证据

| 阶段 | 已完成内容 | 证据与限制 |
| --- | --- | --- |
| 00 / VI01 / VI02 / Gate 03 | 产品范围、三条 P0 规则、catalogue、证据关系、NPC grounding、后果接口和基线协议 | 01、05、报告 09–11；设计/fixture 验证，非真实模型效果 |
| 04 / Batch 1、1.2 | manifest、schema、validator、oracle、词法 NPC gate、隔离后果 stub；v0.1.1 已接受 | 历史报告 48 / 61 tests passed |
| 04 / Batch 2A | scripted runner、retry/fallback、JSONL measurement | `5f14abf8`；历史报告 82 passed |
| 04 / Batch 2B.0 | Experimental OpenAI Responses adapter、prompt、transport schema、preflight | `e4412efa`；历史报告 104 passed、该检查点零模型请求 |
| 04 / Batch 2B.0.1 | 授权、发送前 input-token count、调用上限 guard | `38703c43`；本轮仅核实代码存在 |
| 真实模型 smoke / baseline | 未恢复可审阅的完成证据 | 已提交树无测量结果；本地 ignored outputs 未读取，不能据此断言从未运行 |
| Dify / Unity / 玩家验证 | 当前远端树无实现/验证证据 | Dify 与 production data 目录为占位；20–30 分钟可玩切片仍是目标 |

48 / 61 / 82 / 104 为历史报告，**不是本轮重跑结果、模型准确率或玩家样本数**。本轮文档审查不需要运行完整测试套件。

## 具体缺口与下一步依据

| 缺口 | 代码事实 | 下一步 |
| --- | --- | --- |
| 实测入口与上下文装配 | runner 接收外部 catalogue；adapter 原样序列化 model_input；远端树无独立 manifest 执行 CLI | 解析 catalogue 引用，映射 `npc` / `npc_surface`，复用已有 runner |
| 模型输入与评估数据分离 | NPC 案例 model_facing_input 含 `surface_candidate_example` | 排除示例答案/oracle，保留 Response Plan 授权事实 |
| 结果可复核性 | measurement 有指标与单一 fidelity 结果，没有每次候选和遗漏/多余项明细 | 扩展现有 JSONL，以 run/case/attempt 关联候选和评估 |
| 当前覆盖有限 | manifest 共 18 案例：5 real_model（Dialogue 1、Headline 3、NPC 1），13 fault_injection | 先取得代表性实测；按具体产品问题补覆盖 |
| preflight 退出码 | `main()` 在 `preflight_passed=false` 时仍 return 0 | 使用该 CLI 自动化时修复并测通过/失败；不阻塞无关免费路线 |

主要源码：[manifest](../ai/eval/p0_baseline_manifest.v0.1.1.json)、[runner](../ai/prototype/runner.py)、[adapter](../ai/prototype/openai_responses_adapter.py)、[measurement](../ai/prototype/measurement.py)、[preflight](../ai/prototype/openai_preflight.py)、[测试装配](../tests/conftest.py)。

## 保留的技术边界

运行时合法与语义忠实分别评估（DEC-022）。D19 tactics 遗漏、F04 claim 遗漏、F05 合法目录内多余 claim 可在运行时通过而在 oracle 对照失败；expected 仅用于评估，不进入模型输入或驱动 runtime retry。

NPC 词法 gate 与 consequence stub 仍为 Experimental；正则样例通过不证明任意语言安全，也不等于正式剧情或数值系统。Dialogue 失败不创造动作；Headline 失败保留草稿并阻止发布；NPC fallback 保持确定性 Response Plan。八项 Hard Safety Gates 保留。

已有测试大多对应不同失效行为，当前没有充分依据大批删除。优化重点是按影响选测、复用适用结果、达到完成标准后停止，而非继续扩展防护平台。

## 模型与费用

免费优先；当前审阅分支只集成 OpenAI 路径，尚未选定或接入可用免费 provider。免费额度和接口兼容性在选定具体路线时核实，不预先建立多模型框架。

现有 [paid sheet](../ai/eval/paid_smoke_authorization.experimental.v0.1.json) 仍为 `PROPOSED_NOT_AUTHORIZED` / `execution_authorized=false`。历史计划：4 案例、最多 8 次 generation；每次 input/output 8,192 / 1,024 tokens，合计 65,536 / 8,192；USD 0.25 仅为 model-generation 计划上限，token-count endpoint 计费尚未覆盖。它不自动授权任何请求，也不覆盖第 5 个 real-model 案例。

真实批次执行前一次性确定实际模型、案例、调用与费用范围；已授权范围内连续执行，不逐步重复确认。本轮没有更改调用授权、预算、Contract 或运行时代码。

## 下一成果与产品方向

近期成果是：**薄执行入口 + 一个可用免费优先路径 + 可复核小样本结果 + proceed / fix / defer**。具体步骤、测试范围及停止标准见 [Handoff](07_HANDOFF.md)，此处不重复操作清单。

随后用临时内容证明一次采访、证据获取、标题发布和确定性后果，再扩为 20–30 分钟切片并做玩家验证。Dify 只按实际编排价值决定；Unity 创建仍需已有规则要求的明确授权。尚未实施的步骤保持计划状态。

## 本轮核验和同步范围

GitHub 的分支、提交、相关实现与文档已直接核验；本次只更新工作方式和交接。Windows checkout、未跟踪/ignored 结果与 Project Sources 未同步或核验。下一执行环境先复用本地已有成果，再补缺口；不把未知状态写成未完成事实，也不把旧记录写成新测试。

README 是入口；06 维护进度与证据；07 维护下一步与验证范围；AGENTS 与 Project Instructions 采用同一套精简执行规则。Decision Log 和 Frozen Contract 未变，本轮无需另开 Contract 审批或新建报告。
