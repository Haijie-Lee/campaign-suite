---
name: trans-forge
description: "Use when transforming a mature plan/solution document (现状论证+路线裁定+蓝图+里程碑+风险登记，含已裁定决策注册表) into an ingestible SRS-with-architecture deliverable (需求规格与技术架构方案). Not for ingesting non-conformant existing documents (use ingest-forge); not for producing an SRS zero-to-one or revising an ingested workspace (use spec-forge)."
metadata:
  version: "0.1.0"
  source: campaign-w6
---

# Trans Forge — 转化锻造：成熟 plan → 可收编规格文档

把「成熟方案文档（plan 形态）→ 可收编、含完整需求规格与技术架构的可落地文档」的转化能力固化为五道工序。本 skill 是**收编区外的上游生产者**——产出的转化文档连同收编预案，是 ingest-forge 的下游输入。

## 流水线位置与形态

数据流水线序（产物流向）：**trans「转」→ ingest「收」→ spec「写」→ program「编排」**。
（勿与入口仲裁序 program→ingest→trans→spec 混——那是 campaign 域判定分支先后，本行是产物加工先后。）

本 skill 形态 = **五工序 + 三停点 + 出口三证**（速查行，逐字）。

**三停点**：停点① = 映射设计表上裁定；停点② = 自增 D（待评审）+ Q 表上裁定；停点③ = 出口门证不过不迁移。

对抗审查 / fresh 读者彩排 / 收敛循环机制一律调 caliber 与 spec-forge 既有机制（指针引用，不复制实现——防双份纪律漂移）。检查细目在 `checklists.md`——用到哪道工序读哪节，不预读。

## 依赖验证（每次入口必做，一行输出）

对照本插件仓，查 `campaign/tools/doc_graph.py` / ingest-forge 模板（`campaign/skills/ingest-forge/templates/`）/ spec-forge 机制指针（`campaign/skills/spec-forge/SKILL.md`）任一缺席 → 上报用户不继续。输出一行 `✓ 全配` 或 `⚠ 缺 X`。

## 输入

成熟 plan 文档路径 + slug（默认从文件名派生，作收编预案目录名）。

## 工序 1 — 选材（准入 + 实证备料）

**准入三判据**（缺一即拒绝进入并上报，指引回 caliber plan-forge / deep-probe 补 plan）：
1. 决策注册表存在（plan 内有已裁定 D 条目）；
2. 路线已裁定（现状论证 → 目标形态有明确选择，非开放罗列）；
3. 现状断言有实证密度（plan 引用的 file:line 或实测数据可核）。

通过 → 继续；缺一 → 拒绝并上报。

- **plan 节级解析**：机械支撑 `python campaign/tools/doc_graph.py profile <plan>`（ids / evidence_lines / decisions / weak_words 四行）。
- **实证抽查**：plan 引用的 file:line 逐一复核，有漂移即上报（不照搬过时断言）。
- **缺口清单对照**：读 `references/skeleton-aerofold.md` 完备性清单（10 项必备面），标出本 plan 已覆盖 / 待补面。
- **Q 预选**：通读标出疑似模糊点（无量化判据 / 一义多读 / 注册表矛盾），进工序 3 Q 表。

## 工序 2 — 制坯（映射设计 + genre 骨架）

1. **填映射设计表**：读 `templates/mapping-design-template.md`，逐字用其表头；每个源 plan `##` 节恰一行，处理法五枚举（照录/扩写/新写/归属调整/丢弃），丢弃必须给理由 → **停点①**（映射设计表上裁定）。
2. **按 genre 骨架制坯**：读 `templates/solution-spec-template.md`（§0–§10 + 附录 A/B/C 共 14 `##` 节）；`##` 节单一工件归属，混合节显式 `子节归属声明`。
3. **三类陈述分离纪律**（硬性）：① 用户裁定——逐字引用源 plan 决策注册表，不加料；② 源方案设计判断——标注「源方案 §x」；③ 本转化新增——标注「spec 阶段新增，待评审」。三者禁混。
4. **ID 规范**：读 `references/id-grammar.md`（七前缀白名单 FR/NFR/R/D/C/Q/AC；禁单字母 P；稳定编号只增不改；TODO token 一处值一 token）。
5. **两态标记与 TODO 纪律**：每条含数值/实测形态的新增断言，行尾标 `【证据】`（来源可引）或 `【假设·验证=<方法>】`（无来源给验证法）；无来源数值禁写正文常量，注册 `TODO-<主题>:` 并落最可能假设。（机制摘要一句 + 指针 spec-forge 工序 2 的 L1/L2/L3 lint 与两态标记；L1 歧义词表仅以指针引用，不内联。）

## 工序 3 — 锻打（规格增量 + 对抗审查）

1. **规格增量生成**——**溯源必填律**：每条 FR/NFR 答得出源节 / D 条目 / 实证行；答不出 → 标「spec 阶段新增，待评审」，禁伪装成源方案内容。
   - **未知分类规则**：形状级未知（影响结构 / 需求语义方向）→ 进停点②；参数级未知（具体数值 / 阈值）→ TODO 注册 + 最可能假设落笔。
2. **对抗审查**：机制摘要一句 + 指针 spec-forge 工序 3（SRS 五视角 = 歧义性/可验证性/一致性/完备性/可行性 + 双声部 + 三级裁定 + 收敛循环 + 工序 3.5 闸口）+ B5 evidence-auditor（`campaign/agents/evidence-auditor.md`，审计全部新增定量断言——as-of 2026-09-23 仅一份 agent 定义文件，未发现已注册 skill 版）+ **第六视角「可收编性」**（细目读 `checklists.md` 工序 3 节：一节一投 / ID 规整 / Q 收敛 / 干跑预过）。
3. **Q 表落盘 → 停点②**（自增 D（待评审）+ Q 表上裁定）：模糊点进 Q 表（编号规则与全角 `｜` 纪律指针 ingest-forge 第三步），对齐产物作为 C 决策条目。

## 工序 4 — 成型（fresh 读者理解性测试）

fresh 零背景 agent，read-only。范围 = FR / AC / 契约节（裁剪制，对齐可验证性）。逐条新增/变更 FR 复述「我会如何实现它、如何验证它」，报告歧义点与不可验证点。（机制摘要一句 + 派遣 prompt 骨架指针 spec-forge `checklists.md` 工序 4 节——`campaign/skills/spec-forge/checklists.md:74` 起；填槽 `{DELTA_PATH}` = 转化 spec 草稿路径，`{SCOPE=FR/AC/契约节}`。）困惑点位回工序 2 补全——不是嘴上答「显然」。

## 工序 5 — 出口门三证

三证齐全才允许落盘双产物；缺证 = 状态不迁移，上报用户。（逐条操作化判据 + 机械命令读 `checklists.md` 工序 5 节。）

| 证 | 内容 |
|---|---|
| **溯源完整证** | 映射设计表 100% 覆盖源节（含丢弃理由）；plan 每条 D 在产物逐字可查且有落点指针；实证索引附录落盘 |
| **增量真实证** | `doc_graph.py profile` 判 FR/NFR/AC 计数非零、NFR 过 L3 数值 lint；全节照录 = 换皮重排打回 |
| **可收编译演证** | 试映射判据：低置信 = 0、中置信行必须带显式子节归属（AeroFold 实测校准）；Q 表候选仅限源注册表沿用 + 停点②遗留；spec-lint L1/L2/L3 离线复跑零命中；`doc_graph.py build` 建图成功 |

→ **停点③**（出口门证不过不迁移）。

三证过 → 双产物落盘：
- 转化文档 `docs/spec/<date>-<slug>-需求规格与技术架构方案.md`
- 收编预案五件套 `.campaign/ingest/<slug>/{profile.md, mapping.md, q-table.md, evidence-register.md, exit/{lint.txt, coverage.txt, q-check.txt}}`（文件名与 ingest-forge 出口逐字一致）

## 分工节

**与 ingest-forge**：判别 = 产出新文档 vs 收编本文档不改写。trans-forge 产出新规格文档 + 收编预案；ingest-forge 收编既有非规范文档、不改写其语义。收编预案的 replay 语义：预案 = ingest-forge 产物的预演，真实 ingest 验证的是 replay（机械把预案当 ingest 产物复核），不是新发现。

**与 spec-forge**：判别 = 收编区外单篇 plan 驱动 vs 工件区内生产/修订。trans-forge 由区外单篇 plan 驱动转化；spec-forge 在收编完成的工件区内从零生产或增量修订 SRS。

**与 caliber**：转化内的对抗审查 / 彩排 / 收敛循环机制全指针调用 caliber plan-forge / plan-review-ritual / spec-forge 既有机制，不复制。

## 参考案例库

`references/` 三件角色：
- `case-flow-builder.md` — flow-builder 案例剖析：映射实例表（四类处理法各 ≥2 例）+ 14 条方法纪律 + 9 条反模式教训 + 可收编性时间线自白。
- `skeleton-aerofold.md` — AeroFold 实例骨架与校准数据：13 节实例骨架 + 七套 ID 注册表形态 + 消费链锚点形态 + 收编校准数据 + spec 完备性清单。
- `id-grammar.md` — ID 体系规范：七前缀白名单 / 禁 P 前缀 / 稳定编号 / 通配与组引用 / TODO token。

警示：**案例是参照不是临摹对象——纪律经闸门传递，不经样例传递。** 三件供理解方法与判断口径，不逐字套用。
