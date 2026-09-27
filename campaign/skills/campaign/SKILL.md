---
name: campaign
description: Use when a task shows campaign-domain signals — orchestrating a multi-unit program (program.yaml, 多 plan, 跨会话), ingesting a non-conformant requirements document (巨石单文件 / 散乱笔记 / 旧 SRS / 聊天记录), transforming a mature plan/solution document into an ingestible SRS (成熟方案文档 → 需求规格文档), producing or revising an SRS, or resuming .campaign program state — the campaign entry router (域判定 → ingest-forge / trans-forge / spec-forge / program-forge). Not for ordinary single-plan engineering tasks — those go to caliber. 多环任务（≥2 forge 或含 program 环）进流水线驱动模式：先对齐、立 charter、按产物状态回路接力推进。
metadata:
  version: "0.4.0"
  source: campaign-w6
---

# campaign — campaign 域总入口：分诊，不治病

campaign 域任务的唯一入口。本 skill 只管三件事——域判定、路由、守停止点（「分诊」= 不治病，只决定你去哪个科）；多环任务追加第二重身份：流水线驱动者（对齐→立案→回路推进）。

## Step 0 — 依赖验证（每次入口必做，一行输出）

对照会话可用 skill 清单，查 `campaign:ingest-forge` / `campaign:trans-forge` / `campaign:spec-forge` / `campaign:program-forge` 四 forge 与 `caliber`：

- 缺 forge → 插件安装残缺，上报用户，不继续。
- 缺 caliber → 「非本域」出口改报（逐字）：`非 campaign 域，且 caliber 缺席——请用户直述处置。`

输出一行 `✓ 全配` 或 `⚠ 缺 X`（X = 缺席者名）。

桥版本核查（Q4 软警告，不新增停止点）：定位 caliber 仓 campaign-bridge.json（CALIBER_PLUGIN_DIR 环境变量 → 插件 cache 最高版本目录）；读到且本插件 version 低于其 min_campaign → 追加输出一行 `⚠ 桥版本越界（min_campaign=<值>，本插件=<值>）`；桥缺席或解析失败 → 静默跳过。

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

歧义：多信号命中且顺序规则不覆盖 → 歧义即停，上用户裁定（同 caliber 铁律 7）。「收编后接产 SRS」（先 ingest 后 spec）与「转化后接收编」（先 trans 后 ingest）两类复合任务顺序规则已覆盖，不算歧义。

## Step 1.5 — 环数门控

宣布域判定后判环数：命中单一 forge 且非复合任务 → 直走该 forge（Step 2 只宣布不回路）；复合任务（顺序规则已覆盖两类）或用户明示多环目标（≥2 forge 或含 program 环）→ 进 Step 1.6 流水线驱动模式。

## Step 1.6 — 前置对齐（一次一问带押注）

一句话重推目标 → 指出 1-2 个最大不确定性 → 押注提案藏问（「我猜你要 A 不是 B，因为 X——对吗？」）；事实查环境，决策问对方。产物 = 对齐快照（目标一句话/已确认取舍/开放决策点）；半成形方案入场 → 先切审计视角（列软肋与假设清单）。快照上用户裁定（停点③）。

## Step 1.7 — 流水线立案（charter）

按六节写 `.campaign/pipeline/<name>.md`（≤40 行）：`# Pipeline Charter: <name>` → `## 对齐快照指针` → `## 目标态`（产物集描述，不用流程语言）→ `## 前提清单`（每条包含/跳过理由 = 一条可攻击假设）→ `## 初始路径`（每环含进入或跳过理由）→ `## 弹性点`（预期复量处）→ `## 复量记录`。立案上用户裁定一次（停点④），此后回路自动推进不再逐环请示；`.campaign/` 首次创建时 `.gitignore` 追加 `.campaign/` 行（无 `.git` 则跳过并输出一行说明）。

## Step 2 — 状态回路

宣布格式（逐字）：`域判定 <域名>，理由：<命中的信号原文>`。用户可一句话改道，此后不再判。

单环任务：经 Skill 工具按名调用 `campaign:<forge>`，本 skill 动作结束——forge 内部剂量与停止点归 forge 与 caliber 各自所有。
多环任务（charter 已立案）LOOP 五步：
```
LOOP：1. 盘点（ls -d adr docs/spec .campaign 2>/dev/null + .campaign/ 工件清单）
 2. 对照 charter 目标态：产物齐 → 收口（更新 resume note）
 3. 选环：就绪条件匹配唯一 → 进；多环就绪或皆不就绪 → 推荐+依据，停，用户一句话
 4. 调用该 forge（Skill 工具按名），出口证齐 → 回步 1；5. 触发器命中 → 复量节
```

## 复量（charter 升/降级）

双机械触发器：①前提被证伪（跳过的环其实需要）；②就绪条件反复不满足（路径选错）。命中即宣布 charter 升/降级+理由+补差额（砍已裁定环 → 停，上用户裁定），记 charter `## 复量记录` 节。折叠三条件全满足（①用户消息含明确执行授权 ②无取舍待决 ③无新增不可逆操作）→ 可不停，一行依据+复量记录留痕；任一不满足 → 停点⑤。

## 判例回流

`references/pipeline-cases.md` 判例库五步：触发四类（跳过前提被证伪/就绪条件反复不满足/charter 误判致复量/折叠三条件误用致停点漏停）→ 即时登记 → 成文五要素（情境→错误→机制→规则→失效条件）→ 分辨率裁决（同构合并、异制新条）→ 库超 ~20 条压缩进本节并备份。无沉淀的使用是浪费。

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
- ③ 对齐快照裁定（多环任务）。
- ④ charter 立案裁定（一次，此后回路自动推进）。
- ⑤ 复量越界（折叠三条件任一不满足 / 砍已裁定环）。

其余一律自动推进——该判的判，该转手的转手，不加闸。

## 与 caliber 的分工

caliber = 默认工程入口。campaign = campaign 域平级前置门户：命中域信号 → 本 skill 分诊；不命中 → 直走 caliber，本 skill 不加第二道工序。流水线驱动模式下单元执行层 = caliber 辖区（每单元一次完整 caliber 运行，画像→组合→派遣由 §动态组合 现组），campaign 不造第二套执行引擎。

AGENTS.md 全局路由规则的信号清单以本 skill 的 description 为权威。
