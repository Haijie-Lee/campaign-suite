---
name: ingest-forge
description: "Use when receiving a non-conformant requirements/architecture document (monolith, scattered notes, legacy SRS) that must be ingested into the campaign workspace topology before any downstream flow. Not for writing new specs from scratch."
metadata:
  version: "0.1.0"
  source: campaign-w2
---

# ingest-forge — 文档初刷：非规范存量文档 → 规范工件区

程序层前门。触发：输入文档不符合工件区拓扑（巨石单文件 / 散乱笔记 / 旧格式 SRS / 聊天记录）。
出口：映射表 + Q 表 + 证据登记 + 出口三证，全部落 `.campaign/ingest/<doc-slug>/`。

## 边界：收编，不是改写

**收编，不是改写**——本 skill 只做「探测 → 切片归类 → 标记 → 对齐」，**不代写需求语义**（道层 D2 不实现条款）。
- 不修改源文档（自验证与真实 ingest 都不动原件）；
- 不把「看起来合理」的内容补进需求——模糊需求的裁定权在用户（第三步的 Q 表对齐停点）；
- 拆分存储是后续治理步骤的事，本 skill 的产出是**映射与标记**，不是拆分后的文件。

## 第一步：探测

- **输入**：源文档路径。
- **动作**：跑机械画像 + 通读全文形成质量印象（哪些章节需求密集、哪些是证据、哪些是决策叙事）。
- **产出**：`.campaign/ingest/<slug>/profile.md`。
- **首次创建 `.campaign/` 时**：项目根存在 `.git` 目录且 `.gitignore` 无 `.campaign/` 行 → 追加一行 `.campaign/`；无 `.git` → 跳过并输出一行说明（运行工件不入 git）。
- **机械支撑**：
  ```bash
  python campaign/tools/doc_graph.py profile <源文档> > .campaign/ingest/<slug>/profile.md
  echo "sections: $(grep -c '^## ' <源文档>)" >> .campaign/ingest/<slug>/profile.md
  ```
  profile 四行：ids（FR/NFR/R/D/C/Q/AC 计数）/ evidence_lines（数值+单位行密度）/ decisions（C/D/Q 计数）/ weak_words（7 词歧义词命中数）。

## 第二步：映射拆解

- **输入**：源文档 `##` 级节清单 + 第一步画像。
- **动作**：对每个 `##` 级节判定目标工件。**每 `##` 节恰一行**；子节归属并入所属节行的理由列。目标工件枚举（工件区七类）：`SRS.md / architecture.md / adr/ / research/ / plan.md / risks.md / DECISIONS.md`。
  判别指引：需求与术语 → SRS.md；选型论证/架构/详细设计 → architecture.md；已确认的决策（含推翻链）→ adr/（只增）；实测数据/调研证据 → research/（dated 不可变）；里程碑计划 → plan.md；风险登记 → risks.md；待决项 → DECISIONS.md。；编码/架构约定类内容（命名/注释/分层规范）→ 指向工程根 CONVENTIONS.md（约定通道见 program-forge 输入节；文件不存在则登记为程序初始化期待办，不代写）
- **产出**：`.campaign/ingest/<slug>/mapping.md`（模板 `templates/mapping-template.md`，表头逐字：`| 源节 | 节标题 | 目标工件 | 置信度(高/中/低) | 理由 |`）。**判定是 agent 的判断，不机械代劳；低置信度行 = 第三步 Q 表的候选。**

## 第三步：模糊点对齐（核心停点）

- **输入**：源文档全文 + 机械歧义词扫描 + 第二步低置信度行。
- **动作**：识别真实模糊点（歧义词命中、一义多读、无量化判据、注册表矛盾），生成 Q 表。**模糊需求不代写、不猜测**——Q 表落盘后**停**，与用户逐条对齐；对齐产物作为 C 决策条目落 DECISIONS/ADR（复用 Q→C 机制）。
- **产出**：`.campaign/ingest/<slug>/q-table.md`（模板 `templates/q-table-template.md`，表头逐字：`| Q-ID | 源位置 | 原文引用 | 模糊点类型 | 建议选项 | 状态 |`）。
- **编号规则**：源注册表已有项沿用原编号；新发现项从 Q100 起；全新 ingest 从 Q1 起。状态枚举：`pending` / `resolved(→C-ID)` / `deferred(触发器)`。单元格禁裸 `|`，内容含竖线时写**全角 `｜`**（W2-T6 实证：`\|` 转义会被 awk 等机器校验按字面 `|` 切分，全角字符渲染等效且数据自洽）。
- **机械支撑**：`grep -nE '适当|尽量|必要时|按需|尽快|优化|友好' <源文档>`（命中行逐条人工裁定是否真模糊点——机械扫描只负责不遗漏，裁定是判断）。

## 第四步：证据标记

- **输入**：源文档中含数值/实测形态的断言。
- **动作**：抽取关键断言，逐条标两态——**证据**（有来源/测量条件，在原文引用）或 **假设**（无来源，标注验证方法）。假设条目进 evidence-auditor（B5）待审计队列。
- **产出**：`.campaign/ingest/<slug>/evidence-register.md`（表头：`| 断言 | 源位置 | 态(证据/假设) | 验证方法 |`）。
- **机械支撑**：`grep -nE '[0-9]+(\.[0-9]+)?[ ]*(%|ms|s|GB|MB|KB|万|倍|行)' <源文档>` 取候选行。

## 第五步：出口门（D3 门条款）

三证齐全才允许进入后续流程；缺证 = 状态不迁移，上报用户。

| 证 | 内容 | 机械支撑 |
|---|---|---|
| lint.txt | 引用图建成功 + 孤儿报告落盘 | `python campaign/tools/doc_graph.py build <源文档>` → `orphans --graph .campaign/graph/graph.json --out .campaign/ingest/<slug>/exit/lint.txt` |
| coverage.txt | 追溯矩阵初始版 | `python campaign/tools/doc_graph.py coverage --graph .campaign/graph/graph.json > .campaign/ingest/<slug>/exit/coverage.txt` |
| q-check.txt | **真实 ingest = Q 表清零**（无 pending）；**自验证限定 = 格式合规**（表头正确 + 每表格行 `awk -F'|' NF=8`）——豁免仅限无人裁定的自验证场景，真实 ingest 不免 | `grep '^|' q-table.md \| awk -F'|' 'NF!=8' \| wc -l` → 0 |

## 与 spec-forge 的分工

spec-forge 是从零/增量**生产**规格（W3）；ingest-forge 是把存量**收编**进规范（本 skill）。一个写，一个收。收编完成的工件区才允许进入 spec-forge 的修订流程。
