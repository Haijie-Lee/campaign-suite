---
name: campaign
description: Use when a task shows campaign-domain signals — orchestrating a multi-unit program (program.yaml, 多 plan, 跨会话), ingesting a non-conformant requirements document (巨石单文件 / 散乱笔记 / 旧 SRS / 聊天记录), transforming a mature plan/solution document into an ingestible SRS (成熟方案文档 → 需求规格文档), producing or revising an SRS, or resuming .campaign program state — the campaign entry router (域判定 → ingest-forge / trans-forge / spec-forge / program-forge). Not for ordinary single-plan engineering tasks — those go to caliber.
metadata:
  version: "0.2.0"
  source: campaign-w6
---

# campaign — campaign 域总入口：分诊，不治病

campaign 域任务的唯一入口。本 skill 只管三件事——域判定、路由、守停止点。「分诊」= 不治病，只决定你去哪个科。

## Step 0 — 依赖验证（每次入口必做，一行输出）

对照会话可用 skill 清单，查 `campaign:ingest-forge` / `campaign:trans-forge` / `campaign:spec-forge` / `campaign:program-forge` 四 forge 与 `caliber`：

- 缺 forge → 插件安装残缺，上报用户，不继续。
- 缺 caliber → 「非本域」出口改报（逐字）：`非 campaign 域，且 caliber 缺席——请用户直述处置。`

输出一行 `✓ 全配` 或 `⚠ 缺 X`（X = 缺席者名）。

## Step 1 — 域判定（顺序仲裁，命中即停）

按序过五条分支，首个命中者胜出，命中即停：

1. program 域：编排多单元程序——program.yaml 在途、多 plan、跨会话推进、恢复 .campaign 程序状态 → 进 `campaign:program-forge`。
2. ingest 域：收编存量非规范需求文档——巨石单文件 / 散乱笔记 / 旧 SRS / 聊天记录 → 进 `campaign:ingest-forge`。
3. trans 域：转化成熟方案文档为可收编规格文档——plan/方案文档在途（决策注册表与路线已裁定）且目标 = 产出需求规格文档 → 进 `campaign:trans-forge`。判别：与 ingest 域 = 产出新文档 vs 收编本文档不改写；与 spec 域 = 收编区外单篇 plan 驱动 vs 工件区内生产/修订。
4. spec 域：生产或修订 SRS——零到一生产 / 增量修订（工件区已收编完成才允许进）→ 进 `campaign:spec-forge`。
5. 非本域：以上皆不命中。

非本域分支条款（逐字执行）：皆不命中 → 非本域：输出「非 campaign 域，转 caliber」并结束本 skill 动作——只出不进，不与 caliber 往返仲裁。

辅助信号：工程根 `adr/` 或 `docs/spec/` 或 `.campaign/` 存在 = 工程处于 campaign 工件区拓扑内——仅在域信号弱命中或难裁时作倾向参考，不单独定域；不存在不否决（新工程可从 ingest 或 trans 起步）。机械支撑一行：

`ls -d adr docs/spec .campaign 2>/dev/null`

歧义：多信号命中且顺序规则不覆盖 → 歧义即停，上用户裁定（同 caliber 铁律 7）。「收编后接产 SRS」类复合任务 = 先 ingest 后 spec，顺序规则已覆盖，不算歧义。「转化后接收编」类复合任务 = 先 trans 后 ingest，顺序规则已覆盖，不算歧义。

## Step 2 — 路由（宣布 + 改道）

宣布格式（逐字）：`域判定 <域名>，理由：<命中的信号原文>`。用户可一句话改道，此后不再判。

然后经 Skill 工具按名调用 `campaign:<forge>`，本 skill 动作结束——forge 内部剂量（ML/L）与停止点归 forge 与 caliber 各自所有，入口不重复、不定级。

## 域地图

| forge | 一句话职责 |
|---|---|
| ingest-forge | 收编：存量非规范文档 → 规范工件区（收编先于生产） |
| trans-forge | 转化：成熟方案文档 → 可收编规格文档（转化先于收编） |
| spec-forge | 生产：SRS 从零生产与增量修订（收编完成的工件区才允许进） |
| program-forge | 编排：多单元 DAG 程序（读 DAG→派单元→收账→过门→对账） |

出口：非本域 → caliber（默认工程入口）。

## 停止点速查

- ① 域歧义（多信号命中且顺序不覆盖 / 信号皆弱）→ 停，上用户裁定。
- ② 不可逆操作（删 `.campaign/`、覆盖既有 `program.yaml`）→ 停，无论信号。

其余一律自动推进——该判的判，该转手的转手，不加闸。

## 与 caliber 的分工

caliber = 默认工程入口。campaign = campaign 域平级前置门户：命中域信号 → 本 skill 分诊；不命中 → 直走 caliber，本 skill 不加第二道工序。

AGENTS.md 全局路由规则的信号清单以本 skill 的 description 为权威。
