---
name: spec-forge
description: "Use when producing or revising an SRS (zero-to-one or increment), L-level routed alongside plan-forge. Not for ingesting non-conformant documents (use ingest-forge); not for task implementation plans (use plan-forge)."
metadata:
  version: "0.1.0"
  source: campaign-w3
---

# Spec Forge — SRS 选材、制坯、锻打、成型

把「写出一份可验证、单一解释的 SRS（或其增量修订）」固化为四道工序。骨架与
plan-forge v1.8.0 四工序同构，替换三个配置件（差异替换表见下）。本 skill 是
**锻造工艺**；对抗审查机制（双声部/三级裁定/收敛循环/准出闸口/彩排派遣形态）
一律调 caliber 既有机制，正文以指针引用，**不复制实现**（防双份纪律漂移）。
检查细目在 `checklists.md`——用到哪道工序读哪节，不预读。

## 与 plan-forge 的差异替换表

| 工序 | plan-forge 原版 | spec-forge 变体 |
|---|---|---|
| 工序 1 选材 | 事实有出处（5 条） | 原样保留 + spec 增补 3 条：①现有 SRS 节与 ADR 经 doc_graph 解析引用状态（孤儿/悬空先入选材）；②Q 表与待决项进选材输入；③澄清-grounding 交织提问结构（FOUNDATION → GROUNDING → DEEP DIVE → GROUNDING → DECISIONS，每组提问后 GATE 停等） |
| 工序 2 制坯 | plan 模板 + 契约矩阵 | ISO 29148 结构模板（templates/srs-template.md）+ 需求歧义 lint（L1/L2/L3 离线复跑）+ 证据两态标记 |
| 工序 3 锻打 | 五视角（执行者/契约/环境/风险/测试） | **SRS 五视角：歧义性/可验证性/一致性/完备性/可行性**；双声部、三级裁定、收敛循环、工序 3.5 闸口机制原样调 plan-review-ritual |
| 工序 4 彩排 | 零背景执行者 confusion-hunt | **fresh 读者理解性测试**：逐条新增/变更 FR 复述「我会如何实现它、如何验证它」，报告歧义点与不可验证点 |

## 何时使用 / 不使用

- **用**：从零生产 SRS，或对既有 SRS 做增量修订。L 级路由至此，与 plan-forge
  平级；ML 级 = 工序 1-2 + 工序 4，L 级 = 工序 1-4。
- **不用**：非规范存量文档收编（ingest-forge 的领域）；任务实现 plan
  （plan-forge 的领域）。

## 工序 1 — 选材（实证备料 + 澄清-grounding 交织）

plan-forge 工序 1 五条原样保留（读真实代码 / 测真实环境 / 真实数据当 fixture /
查陷阱档案 / 查执行期登记表——见 caliber plan-forge SKILL.md 工序 1），增补三条：

1. **引用状态解析**：现有 SRS 节与 ADR 经 doc_graph 解析（build/orphans），
   孤儿与悬空引用先进选材清单。
2. **Q 表进选材**：未决 Q 条目（注册表 / ingest Q 表）逐条列出，每条 = 本次
   修订的候选触发项。
3. **澄清-grounding 交织**：提问不是一次问完——FOUNDATION（目的/用户/范围/
   约束/成功形态）→ **GROUNDING**（拿事实校准：调研证据/实测数据/引用图）→
   DEEP DIVE（场景/失效模式/非目标）→ **GROUNDING**（技术可行性探测）→
   DECISIONS（做/不做/假设）。每组提问后 GATE 停等用户裁定；每组建立在
   前一轮 grounding 的事实上。依据：把「证据到达」从修订期前移到澄清期。

零出处的值禁止进 SRS；实在拿不到 → 按工序 2 两态标记为假设，不许写成正文常量。

## 工序 2 — 制坯（ISO 29148 模板 + 需求歧义 lint + 两态标记）

1. **结构**：`templates/srs-template.md` 九节骨干（0 文档说明 / 1 概述 /
   2 术语 / 3 FR / 4 NFR / 5 约束与假设 / 6 AC / 7 追溯指针 / 8 Q 表与待决）。
   找不到内容填 N/A，不删模板节。
2. **需求歧义 lint**（写作期离线复跑，规则与 spec-lint hook 同源）：
   - L1 歧义词表 7 词：`适当|尽量|必要时|按需|尽快|优化|友好` 子串匹配——
     命中 → 给可验证的量化口径或删除；
   - L2 ID 引用完整性：引用 ID 须在 graph.json 节点集存在（图缺失整体跳过）；
   - L3 NFR 定义形态缺数值：NFR 定义行剔除编号数字后无其他数字 → 补量词与阈值。
   （检查细目读 `checklists.md` 工序 2 节。）
3. **证据两态标记**：每条含数值/实测形态的**新增/变更**断言句，行尾标
   `【证据】`（来源 + 测量条件在原文可引）或 `【假设·验证=<方法>】`
   （无来源，给验证方法）。棘轮语义：存量不追溯。机械支撑：
   `grep -nE '[0-9]+(\.[0-9]+)?[ ]*(%|ms|s|GB|MB|KB|万|倍|行)' <目标> | grep -vE '【(证据|假设·验证=)'`
   → 未标记清单进 Q 表或补标。假设条目进 evidence-auditor 待审计队列
   （evidence-register 表头：`| 断言 | 源位置 | 态(证据/假设) | 验证方法 |`）。

## 工序 3 — 锻打（SRS 五视角收敛循环）

机制与 plan-forge 工序 3 全同——L 级收敛循环、双声部、三级裁定、轮次化、
成本封顶、工序 3.5 准出闸口（见 caliber plan-forge SKILL.md 工序 3/3.5 与
plan-review-ritual Step 0-4）。替换的只是注入的 CHECKLIST：
**SRS 五视角 = 歧义性 / 可验证性 / 一致性 / 完备性 / 可行性**
（细目读 `checklists.md` 工序 3 节）。

**B5 派遣点**：L 级工序 3 轮 1 与修订模式实战，均派遣 evidence-auditor；
输入 = 本次新增/变更节的全部定量断言（机械 pre-pass 提取）。

## 工序 4 — 成型（fresh 读者理解性测试）

派遣形态与 plan-forge 工序 4 同（fresh 零背景基线 agent，read-only，不执行
写操作），测试内容替换为**理解性测试**：fresh 读者逐条新增/变更 FR 复述
「我会如何实现它、如何验证它」，报告歧义点与不可验证点（测单解释性，对齐
ISO 29148 的 unambiguous + verifiable）。困惑点位回工序 2 补全——不是嘴上
答「显然」。派遣 prompt 骨架与回收检查读 `checklists.md` 工序 4 节。

## 与 ingest-forge 的分工

spec-forge 是从零/增量**生产**规格；ingest-forge 是把存量**收编**进规范。
收编完成的工件区才允许进入 spec-forge 的修订流程。

## 与修订模式的关系

版本间修订（vN → vN+1）的审查走 plan-review-ritual REVISION 模式——范围 =
diff 全文 + doc-graph 涟漪节 + 未触及节 10% 抽查，范围清单由
campaign/tools/revision_scope.py 预算。本 skill 负责产出内容，修订模式负责
版本间对抗审查。
