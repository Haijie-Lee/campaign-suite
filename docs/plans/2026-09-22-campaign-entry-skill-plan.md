# campaign 总入口 skill 建造 plan（L 级）

> plan-forge 工序 2 初稿 v1（2026-09-22）｜引擎路由：exec-forge（文档+配置主导，无源码任务，仓库有 git）
> 审计文件：`.caliber/review-logs/2026-09-22-campaign-entry-skill-plan.md`（工序 3 起写入，plan 末尾只留指针）

## 对齐快照节

**目标重推**：为 campaign 插件造总入口 skill `campaign`（`campaign/skills/campaign/SKILL.md`），把「任务该进 ingest-forge / spec-forge / program-forge 哪个门」的分拣从用户心智负担变成入口机械判定：域判定（四信号 + 顺序仲裁 + 「非本域转 caliber 只出不进」）→ 路由（宣布 + 一句话改道 + 歧义即停）→ 守停止点。配套最小改动：plugin.json 0.3.0→0.4.0、marketplace.json 双份同升、AGENTS.md 工程入口条款改写为非对称路由规则、README 组件表联动。三 forge / 四 hooks / 五工具 / caliber 仓库零触碰。（2026-09-22 工序 3.5 闸口补记：配套改动面扩记——description 整行改写（C5/C6）与 README 门面五处联动（日期头/首段/组件表行/目录树插入行/目录树注释版本）属新增第四个 skill 的 manifest/门面真实性维护：旧 description「三个 skills」自述在 T1 交付后即成错误陈述，不改 = 交付虚假 manifest，方向唯一无取舍；经用户全权授权折叠，台账记 Ruling。）

**道层条款（价值排序/不可妥协项/失败的形状）**：价值排序 = 解不顺手（分拣进机制）> 改动面保守；不可妥协 = 与 caliber 触发面边界干净不抢活；失败的形状 = ①双入口打架 ②入口自身变重流程 ③改 forge 引回归。

**开放决策点+方案选定记录**：双轨对照（主轨方案 1 vs 挑战者方案 A）高度收敛，用户 2026-09-22 裁定采纳合并方案——薄路由三段式 + AGENTS.md 非对称分叉（caliber 保默认位）+ 命名 `campaign`（调用形 `campaign:campaign`，与 `caliber:caliber` 同构）+ Step 0 一行依赖验证 + hooks 零改动（采纳挑战者）。否决：目录模式（赘肉删除测试未过，能力地图由路由表自身呈现）；caliber Step 0 反向开门（层倒置 + 跨仓库永久耦合）；caliber 路由表注册式（分拣仍过 caliber，不顺手只解一半，且被道层裁定排除）。

**挂起项（带触发器）**：① spec-context.sh 过滤集合加 campaign——触发器：实测入口判定确需图摘要辅助时；② caliber description 尾加指向 campaign 一行——触发器：用户认为 caliber 侧需要指路时；③ KI-02 的 forge 正文「机制摘要+指针」两段式增补——触发器：KI-02 单独立项时（本 plan 只消化其索引层，见 T1 域地图表，forge 正文零触碰不动）。

**前提清单**：①按名调用 + AGENTS.md 纪律足以承载优先级仲裁（现行「一切走 caliber」机制实证有效）；②ZCode 注入清单不含 description（2026-09-14 实证），触发第一承载 = AGENTS.md 路由规则 + skill 名，description 是第二承载；③forge 集稳定为三，加第四门时需同步改入口 + AGENTS.md（漂移面已登记）；④AGENTS.md 对未装 campaign 的环境留一段规则，经自消解句「未安装 campaign 插件的环境忽略本分支」化解（见契约 C3）。

**选材消化记录**（工序 1 第 5 条，docs/known-issues.md 同域项，2026-09-22 读）：KI-01 = 本 plan 主体；KI-02 消化其「指针索引层」（T1 域地图表），forge 正文两段式转挂起项③；KI-03 消化其入口层（T1 Step 0 依赖验证一行 + 缺 caliber 改报文本），forge 层 fallback 不消化（超出入口职责）；KI-04/05/06/07 非本 plan 域，不处理。docs/TODO.md 不存在。

## Global Constraints

1. **零触碰清单**：`campaign/skills/ingest-forge/`、`campaign/skills/spec-forge/`、`campaign/skills/program-forge/`、`campaign/hooks/`、`campaign/tools/`（本仓库五路径——执行完成后 `git diff --name-only HEAD -- <五路径>` 必须为空，与 ac-90 检查 6① 同口径）+ `F:\workspaces\caliber-suite` 的 `caliber/` 插件本体目录（不含其 `.caliber/` 工作产物；探针形态见 ac-90 检查 6②——caliber-suite 当前非 git 仓库（2026-09-22 实测），该探针本机恒 SKIP 属预期，caliber 零触碰实际靠本条纪律 + 任务块无任何 caliber 路径写入兜底，其 git 化后探针自动生效）。
2. 入口 SKILL.md ≤ 100 行（对齐三 forge 实测规模 67/97/99 行，2026-09-22 `wc -l`）。
3. description 双向界定：触发分支 + 排除句，且排除句必须配对指向 caliber（writing-great-skills negation 条款：否定只作硬护栏并配「去做什么」）。
4. 入口不定级（ML/L 剂量归 forge 与 caliber 各自所有）、不复述 forge 正文机制（防双份漂移）。
5. marketplace.json 双份（根级 + `.claude-plugin/`）改后逐字节一致（平台约定，README 目录树注记）。
6. 文档语言中文；frontmatter 的 name/description 以 C1/C2 逐字文本为准（中英混合形态、中文域词允许保留——ingest-forge 纯英文、program-forge 纯中文，三 forge 本无统一风格，约束以契约矩阵为权威）。
7. `campaign/hooks/hooks.json` 硬编码 bash 路径不动；本 plan 不重装插件、不改插件 cache（本地源无更新检测，改 cache 禁——安装生效属用户操作，见交接节）。
8. AGENTS.md 改写只动「## 工程任务入口（全局）」一节，其余节（Plan review 例行流程 / 三 skill 锻造流水线 / Memory Index）一字不动。

## Review Focus（≤5 条，最可能伤真实用户者在前）

1. **双入口字面重叠**：「修订 SRS」既是 engineering task（caliber 广谱 description 命中）又是 campaign 域——优先级规则必须存在于 AGENTS.md 且排除句必须存在于 description。钉 T4 验证 + T1 验证 V2。
2. **「非本域」出口被跳过**（入口变成什么活都接 = 打架复发）——「只出不进」条款逐字存在性。钉 T1 验证 V3 + 工序 4 彩排非域文本实测。
3. **marketplace 双份改一漏一**（平台读 `.claude-plugin/` 份，根级份成陈旧门面）——钉 T2 验证 V5（diff 零输出）。
4. **AGENTS.md 死规则段**：未装 campaign 的机器读到路由规则后找不存在的 skill——契约 C3 含自消解句「未安装 campaign 插件的环境忽略本分支」。钉 T4 验证 V10。
5. **入口长成第二个 gstack preamble**（602 行反例，2026-09-22 实测）——约束 2 行数硬门。钉 T1 验证 V1。

## 契约矩阵

| # | 契约 | 逐字内容 / 值 | 消费任务 |
|---|---|---|---|
| C1 | 入口 frontmatter description（触发面，权威信号清单） | `Use when a task shows campaign-domain signals — orchestrating a multi-unit program (program.yaml, 多 plan, 跨会话), ingesting a non-conformant requirements document (巨石单文件 / 散乱笔记 / 旧 SRS / 聊天记录), producing or revising an SRS, or resuming .campaign program state — the campaign entry router (域判定 → ingest-forge / spec-forge / program-forge). Not for ordinary single-plan engineering tasks — those go to caliber.` | T1, T5 |
| C2 | 入口 frontmatter 全量 | `name: campaign` / `description: <C1>` / metadata 嵌套形（镜像三 forge frontmatter 实形；禁平铺——`metadata: version: "0.1.0"` 单行双冒号是非法 YAML）：`metadata:` 行下两缩进行 `  version: "0.1.0"`、`  source: campaign-w5` | T1 |
| C3 | AGENTS.md 工程入口节新条款（替换文本，逐字） | 见 T4 任务块内「新文本」 | T4 |
| C4 | 版本号 | `0.4.0`（三处：`campaign/.zcode-plugin/plugin.json`、`marketplace.json`、`.claude-plugin/marketplace.json`；实测旧值 `0.3.0`，2026-09-22） | T2 |
| C5 | plugin.json 新 description（英文，整行替换） | `Mega-scale development task orchestration suite layered on caliber: campaign entry router (域判定 → ingest-forge/spec-forge/program-forge) + doc-graph/run-ledger/handoff/spec-guard hooks/evidence-auditor — file-system-as-truth, evidence-gated state transitions` | T2 |
| C6 | marketplace 双份新 description（中文，整行替换） | `超大规模开发任务编排套件（layered on caliber）：campaign 总入口（域判定→路由）+ ingest-forge / spec-forge / program-forge 三 forge + evidence-auditor agent + 四个 spec 守护 hook + 五个零依赖契约工具——文件系统即真相、证据门控状态迁移` | T2 |
| C7 | 判定顺序仲裁 | program 域 > ingest 域 > spec 域 > 非本域（首个命中者胜出；复合任务「收编后接产 SRS」= 先 ingest 后 spec，不算歧义） | T1, T5 |
| C8 | ac-90 冒烟检查项（6 项，钉死） | 见 T5 任务块检查清单 | T5 |
| C9 | 域地图表（KI-02 索引层，SKILL.md 内一节，三行） | 写入 SKILL.md 时用未转义管道符的三行表：`\| ingest-forge \| 收编：存量非规范文档 → 规范工件区（收编先于生产） \|` / `\| spec-forge \| 生产：SRS 从零生产与增量修订（收编完成的工件区才允许进） \|` / `\| program-forge \| 编排：多单元 DAG 程序（读 DAG→派单元→收账→过门→对账） \|`（此处 `\|` 仅为本 plan 表格内转义呈现） | T1 |

## 任务块

### T1 — 新增入口 skill 本体

画像: 性质=文档; 难度=判断; 领域词=[skill 编写, 路由, frontmatter, description 触发面, 分诊]

**步骤**：

1. 创建目录 `campaign/skills/campaign/`。
2. 写入 `campaign/skills/campaign/SKILL.md`，内容 = C2 frontmatter（前后加 `---` 围栏行，V2 正则锚）+ 下文「正文骨架」规格成稿（正文 prose 由执行者按骨架撰写，骨架中「逐字」标记的句子一字不得改）；两条形态约束：description 单行书写（V2 正则只匹配单行）；Step 1 四分支之外禁用 `^[0-9]+\. ` 数字行首（V4 断言锚保护）：
   - 标题段：`# campaign — campaign 域总入口：分诊，不治病` + 一段定位（≤3 行）：唯一入口，本 skill 只管三件事——域判定、路由、守停止点；「分诊」= 不治病，只决定你去哪个科。
   - `## Step 0 — 依赖验证（每次入口必做，一行输出）`：对照会话可用 skill 清单查 `campaign:ingest-forge` / `campaign:spec-forge` / `campaign:program-forge` 三 forge 与 `caliber`。缺 forge → 插件安装残缺，上报用户不继续；缺 caliber → 「非本域」出口改报（逐字）：`非 campaign 域，且 caliber 缺席——请用户直述处置。`输出一行 `✓ 全配` 或 `⚠ 缺 X`。
   - `## Step 1 — 域判定（顺序仲裁，命中即停）`：按 C7 顺序四条分支，**行首格式钉死**（V4 断言锚）：`1. program 域：…` / `2. ingest 域：…` / `3. spec 域：…` / `4. 非本域：…`——每条分支一行触发信号描述（信号词与 C1 对齐）。非本域分支条款（逐字）：`皆不命中 → 非本域：输出「非 campaign 域，转 caliber」并结束本 skill 动作——只出不进，不与 caliber 往返仲裁。` 节后附「辅助信号」段：工程根 `adr/` 或 `docs/spec/` 或 `.campaign/` 存在 = 工程处于 campaign 工件区拓扑内，判定时加权；不存在不否决（新工程可从 ingest 起步）；机械支撑一行 bash（逐字）：``ls -d adr docs/spec .campaign 2>/dev/null``。节后附「歧义」段（逐字要点）：多信号命中且 C7 顺序规则不覆盖 → 歧义即停，上用户裁定（同 caliber 铁律 7）。
   - `## Step 2 — 路由（宣布 + 改道）`：宣布格式（逐字）：`域判定 <域名>，理由：<命中的信号原文>`；用户可一句话改道，此后不再判；然后经 Skill 工具按名调用 `campaign:<forge>`，本 skill 动作结束——forge 内部剂量（ML/L）与停止点归 forge 与 caliber 各自所有，入口不重复、不定级。
   - `## 域地图`：C9 三行表 + 一行出口说明（非本域 → caliber）。本节是 KI-02 的指针索引层，三行各一句话，不复述 forge 机制。
   - `## 停止点速查`：两条——①域歧义（多信号命中且顺序不覆盖 / 信号皆弱）停，上裁定；②不可逆操作（删 `.campaign/`、覆盖既有 `program.yaml`）停，无论信号。末行（逐字要点）：其余一律自动推进——该判的判，该转手的转手，不加闸。
   - `## 与 caliber 的分工`：caliber = 默认工程入口；campaign = campaign 域平级前置门户，命中四信号 → 本 skill 分诊，不命中 → 直走 caliber；末行（逐字）：`AGENTS.md 全局路由规则的信号清单以本 skill 的 description 为权威。`
3. 回读成稿，对照本任务验证 V1–V4 与 V13 逐条过。

**Interfaces**：Consumes = C1, C2, C7, C9；Produces = `campaign/skills/campaign/SKILL.md`（≤100 行）。

**验证期望**（在仓库根执行，Git Bash）：

- V1 行数门：`wc -l campaign/skills/campaign/SKILL.md` 输出 ≤ 100。
- V2 触发面契约：`python -c "import re; t=open('campaign/skills/campaign/SKILL.md',encoding='utf-8').read(); fm=re.match(r'\s*---\s*\n(.*?)\n---',t,re.S).group(1); print('name ok' if 'name: campaign' in fm else 'name BAD'); d=re.search(r'description:\s*(.+)',fm).group(1); print('signals ok' if all(k in d for k in ['program','ingest','SRS','.campaign']) else 'signals BAD'); print('guard ok' if ('Not for' in d and 'caliber' in d) else 'guard BAD'); print('meta ok' if all(k in fm for k in ['version:','0.1.0','campaign-w5']) else 'meta BAD')"` → 四行依次 `name ok` / `signals ok` / `guard ok` / `meta ok`。
- V3 只出不进条款：`grep -c '只出不进' campaign/skills/campaign/SKILL.md` → ≥1；`grep -c '不与 caliber 往返仲裁' campaign/skills/campaign/SKILL.md` → `1`（后句更独特，钉唯一权威；「只出不进」允许正文他处引用）。
- V4 顺序仲裁：`grep -nE '^[0-9]+\. (program|ingest|spec) 域' campaign/skills/campaign/SKILL.md | head -3` → 三行，行内依次含 `program 域`、`ingest 域`、`spec 域`，且行号严格递增。
- V13 骨架完备（KI-02/KI-03 与三段式交付物机械闸；V 编号全局唯一、按任务块追加不重排，本断言属 T1）：`grep -cF '## Step 0' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF '## Step 2' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF '## 域地图' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF '## 停止点速查' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF '## 与 caliber 的分工' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF '分诊，不治病' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF 'AGENTS.md 全局路由规则的信号清单以本 skill 的 description 为权威。' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF '✓ 全配' campaign/skills/campaign/SKILL.md` → ≥1；`grep -cF '⚠ 缺' campaign/skills/campaign/SKILL.md` → ≥1；`grep -cF '非 campaign 域，且 caliber 缺席' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF '域判定 <域名>，理由：' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF '此后不再判' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF '歧义即停' campaign/skills/campaign/SKILL.md` → ≥1；`grep -cF '| ingest-forge | 收编：' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF '| spec-forge | 生产：' campaign/skills/campaign/SKILL.md` → `1`；`grep -cF '| program-forge | 编排：' campaign/skills/campaign/SKILL.md` → `1`。

### T2 — 版本号与 description 三处联动

画像: 性质=配置; 难度=机械; 领域词=[plugin.json, marketplace.json, 版本号]

**步骤**（三文件各自：锚定串唯一性确认 → Edit 替换 → 下一文件；同文件多处替换分多次 Edit，一次一处）：

1. `campaign/.zcode-plugin/plugin.json`：① `"version": "0.3.0"` → `"version": "0.4.0"`；② description 整行（旧行逐字锚定：`"description": "Mega-scale development task orchestration suite layered on caliber: doc-graph/run-ledger/handoff/spec-guard hooks/ingest-forge/spec-forge/evidence-auditor — file-system-as-truth, evidence-gated state transitions"`）→ `"description": "<C5>"`。
2. `marketplace.json`：① `"version": "0.3.0"` → `"version": "0.4.0"`；② description 整行（旧行逐字锚定：`"description": "超大规模开发任务编排套件（layered on caliber）：ingest-forge / spec-forge / program-forge 三 skills + evidence-auditor agent + 四个 spec 守护 hook + 五个零依赖契约工具——文件系统即真相、证据门控状态迁移"`）→ `"description": "<C6>"`。
3. `.claude-plugin/marketplace.json`：同第 2 步两处替换（锚定串与第 2 步逐字相同）。

中断续跑：三文件互相独立——中断后逐文件重跑「锚定确认 → 替换」即可（已改文件旧锚消失，二次 Edit 报锚不存在即知已做），V5–V7 为终态判据。任一锚定串未命中（Edit 报 not found 且非已完成态）→ 停止上报，不强行替换。

**Interfaces**：Consumes = C4, C5, C6；Produces = 三文件更新。

**验证期望**：

- V5 双份同形：`diff marketplace.json .claude-plugin/marketplace.json` → 零输出。
- V6 版本就位：`grep -c '"version": "0.4.0"' campaign/.zcode-plugin/plugin.json marketplace.json .claude-plugin/marketplace.json` → 三行各 `1`；`grep -rc '"version": "0.3.0"' campaign/.zcode-plugin/plugin.json marketplace.json .claude-plugin/marketplace.json` → 三行各 `0`；description 就位：`grep -cF 'campaign entry router' campaign/.zcode-plugin/plugin.json` → `1`、`grep -cF '总入口（域判定→路由）' marketplace.json` → `1`；旧串反向断言：`grep -c 'ingest-forge/spec-forge/evidence-auditor' campaign/.zcode-plugin/plugin.json` → `0`。
- V7 JSON 合法：`python -c "import json; [print(p,'ok') for p in ['campaign/.zcode-plugin/plugin.json','marketplace.json','.claude-plugin/marketplace.json'] if json.load(open(p,encoding='utf-8'))]"` → 三行各 `<path> ok`。

### T3 — README 联动

画像: 性质=文档; 难度=机械; 领域词=[README, 组件表, 目录树]

**步骤**（同文件多处编辑，一次一处，严格按序）：

1. 头行：`> 最后更新：2026-09-21 ｜` → `> 最后更新：2026-09-22 ｜`（锚定串 `> 最后更新：2026-09-21`，唯一）。
2. 首段：`**campaign v0.3.0**` → `**campaign v0.4.0**`；同句 `三个 skills（ingest-forge / spec-forge / program-forge）` → `总入口 skill campaign + 三个 forge skills（ingest-forge / spec-forge / program-forge）`。
3. 组件表：在 `` | `ingest-forge` | skill | `` 行**前**插入一行（写入 README 的实际文本，逐字）：`` | `campaign` | skill | 总入口分诊：域判定（四信号+顺序仲裁）→ 路由三 forge 或转 caliber，只管三件事 | ``
4. 目录树 skills 块：在 `│   │   ├── ingest-forge/       # SKILL.md + templates/（映射表、Q 表模板）` 行**前**插入一行（逐字）：`│   │   ├── campaign/           # SKILL.md（总入口：域判定→路由→守停止点）`
5. 目录树 plugin.json 注释行：`│   │   └── plugin.json         # {"name":"campaign","version":"0.3.0"}` → 注释内版本号改 `"0.4.0"`（锚定串 `"version":"0.3.0"`——注意此行无空格形态，与 T2 的 JSON 正文锚 `"version": "0.3.0"` 有空格形态不同，互不冲突）。

**Interfaces**：Consumes = C4；Produces = README.md 更新。

**验证期望**：

- V8 门面更新：`grep -c 'campaign v0.4.0' README.md` → `1`；`grep -cF '0.3.0' README.md` → `0`（无 v 前缀形态，同时覆盖 L5 与 L47 注释两形态）。
- V9 组件表行：`grep -cF '总入口分诊' README.md` → `1`；目录树插入行：`grep -cF '├── campaign/           # SKILL.md' README.md` → `1`（含注释全串——README L45 根层既有 `├── campaign/` 行无此注释，计数恰 1；注意 `#` 前为 11 个空格，与插入行逐字一致）；目录树注释版本：`grep -cF '"version":"0.4.0"' README.md` → `1`。

### T4 — AGENTS.md 工程入口节改写（用户级文件）

画像: 性质=文档; 难度=判断; 领域词=[AGENTS.md, 路由规则, 全局指令]

**步骤**：

1. 备份：`cp /c/Users/Administrator/.zcode/AGENTS.md /c/Users/Administrator/.zcode/AGENTS.md.bak-20260922`（`/c/` 路径形，与步骤 4 的 rm 同形；Windows cmd 下才用反斜杠形）。
2. Edit 替换「## 工程任务入口（全局）」节内的加粗条款段。**旧文本**（逐字锚定，两行）：

```
**任何 feature / bugfix / refactor / 改动请求，先走 skill `caliber`（caliber-suite 插件，经 Skill 工具按名调用）定级再执行**，不要直接动手。
原因：流程严谨度随任务复杂度缩放（S/MS 轻、ML 标准、L 全剂量）；定级、六阶段骨架、停止点（不可逆操作/歧义/延期决策）规则均在 caliber skill 内，任何级别不省略。
```

   **新文本**（C3，逐字替换为）：

```
**任何 feature / bugfix / refactor / 改动请求，先做域判定再执行**，不要直接动手：
- 任务命中 campaign 域信号（编排多单元程序 / 收编存量非规范文档 / 生产或修订 SRS / 恢复 .campaign 程序状态）→ 先走 skill `campaign`（campaign-suite 插件，经 Skill 工具按名调用）分诊路由；信号清单权威 = campaign skill 的 description；未安装 campaign 插件的环境忽略本分支。
- 不命中 → 先走 skill `caliber`（caliber-suite 插件，经 Skill 工具按名调用）定级再执行。
- campaign 判「非本域」即转 caliber，不往返仲裁。
原因：流程严谨度随任务复杂度缩放（S/MS 轻、ML 标准、L 全剂量）；定级、六阶段骨架、停止点（不可逆操作/歧义/延期决策）规则均在 caliber skill 内，任何级别不省略。campaign 域任务的分诊、路由、门控规则均在 campaign skill 内。
```

3. 回读全节核对；确认「## Plan review 例行流程（全局）」「## 三 skill 锻造流水线（要点）」「# Memory Index (Global)」三节标题仍在且内容未动。
4. V10–V12 全过后删除备份：`rm /c/Users/Administrator/.zcode/AGENTS.md.bak-20260922`（`/c/` 路径形，与步骤 1 注记同形）；任一不过 → 用备份恢复并停止上报。

**Interfaces**：Consumes = C3；Produces = AGENTS.md 工程入口节更新。

**验证期望**：

- V10 新条款就位：`grep -cF '先做域判定再执行' /c/Users/Administrator/.zcode/AGENTS.md` → `1`；`grep -cF '未安装 campaign 插件的环境忽略本分支' /c/Users/Administrator/.zcode/AGENTS.md` → `1`。
- V11 既有节完好：`grep -cE '^## (Plan review 例行流程|三 skill 锻造流水线)' /c/Users/Administrator/.zcode/AGENTS.md` → `2`；`grep -cF '# Memory Index (Global)' /c/Users/Administrator/.zcode/AGENTS.md` → `1`。
- V12 旧条款唯一处替换：`grep -cF "先走 skill \`caliber\`（caliber-suite 插件，经 Skill 工具按名调用）定级再执行" /c/Users/Administrator/.zcode/AGENTS.md` → `1`（出现于新文本「不命中」分支行，属预期；注意 grep 模式含反引号，shell 用双引号包裹——转义反引号 + 双引号形态 2026-09-22 已实跑验证输出 1）。

### T5 — ac-90 冒烟脚本与首跑

画像: 性质=操作; 难度=集成; 领域词=[冒烟, ac runner, frontmatter 解析, 零触碰守卫]

**步骤**：

1. 写入 `campaign/acceptance/ac-90-entry-skill-smoke.py`（编号 90+ 段 = 插件自留验收段，避开 AeroFold 1-36 实例段——写入脚本 docstring）。脚本规格：Python 3.10+ 零第三方依赖；仓库根 = 脚本位置上两级（`acceptance/` 的父级的父级）；六项检查（C8，逐字）：
   - 检查 1（存在与行数门）：`campaign/skills/campaign/SKILL.md` 存在且行数 ≤ 100。
   - 检查 2（触发面契约）：frontmatter 含 `name: campaign`，且 metadata 含 `version:`、`0.1.0`、`campaign-w5` 三子串；description 同时含子串 `program`、`ingest`、`SRS`、`.campaign`、`Not for`、`caliber`。
   - 检查 3（只出不进 + 顺序仲裁 + 骨架完备）：正文含 `只出不进` ≥1 处且 `不与 caliber 往返仲裁` 恰 1 处；`^[0-9]+\. (program|ingest|spec) 域` 三行顺序为 program → ingest → spec；骨架闸（KI-02/KI-03 + 三段式）：`## Step 0`、`## Step 2`、`## 域地图`、`## 停止点速查`、`## 与 caliber 的分工`、`域判定 <域名>，理由：`、`此后不再判`、`非 campaign 域，且 caliber 缺席`、`分诊，不治病`、`AGENTS.md 全局路由规则的信号清单以本 skill 的 description 为权威。`、`| ingest-forge | 收编：`、`| spec-forge | 生产：`、`| program-forge | 编排：` 各恰 1 处，`✓ 全配`、`⚠ 缺`、`歧义即停` 各 ≥1 处。
   - 检查 4（版本三处 + 双份同形 + description 就位）：三处 JSON 的 `version` 均为 `0.4.0`；`marketplace.json` 与 `.claude-plugin/marketplace.json` 逐字节一致（`filecmp.cmp(shallow=False)`）；`campaign/.zcode-plugin/plugin.json` 含子串 `campaign entry router` 且不含 `ingest-forge/spec-forge/evidence-auditor`（旧串反向断言）；`marketplace.json` 含子串 `总入口（域判定→路由）`。
   - 检查 5（hooks 零改动守卫）：`campaign/hooks/spec-context.sh` 含 `plan-forge|spec-forge|ingest-forge|program-forge` 的 case 模式行，且该行不含 `campaign`。
   - 检查 6（forge/tools 零触碰守卫，两段）：① subprocess 跑 `git -C <repo_root> diff --name-only HEAD -- campaign/skills/ingest-forge campaign/skills/spec-forge campaign/skills/program-forge campaign/hooks campaign/tools`（repo_root = 脚本位置上两级，与 runner 以 `cwd=acceptance/` 调起本脚本兼容——不依赖进程 cwd），输出为空；② subprocess 跑 `git -C F:\workspaces\caliber-suite diff --name-only HEAD -- caliber/`（native Windows 路径直传 subprocess，不经 POSIX 转换；caliber 插件本体目录，不含其 `.caliber/` 工作产物），输出为空。降级放宽：任一段 git 返回非零退出码或 stderr 含 `fatal` → 该段记 SKIP 并计数为通过，打印一行降级说明；subprocess 调用须 try/except 包住，抛异常（如 git 不在 PATH 的 FileNotFoundError）同按 SKIP 计通过。注记：caliber-suite 当前非 git 仓库（2026-09-22 实测），② 在本机恒 SKIP 属预期；其 git 化后探针自动生效。
   - 脚本编码纪律：所有 `open()` 显式 `encoding='utf-8'`（Windows python 默认 locale 编码陷阱，handoff 实证）；读 subprocess 输出同理（`text=True, encoding='utf-8', errors='replace'`）。
   - 打印顺序：先收集六项结果，首行总结行，随后六项明细——每项一行 `ok <n> <说明>` 或 `BAD <n> <说明>`；任一 BAD → 首行 `FAIL ac-90 ...`、exit 1；全过 → 首行 `PASS ac-90 entry-skill smoke (6/6 checks)`、exit 0（run_all.py 归类契约：exit 0=PASS / 1=FAIL）。
2. 首跑：`python campaign/acceptance/ac-90-entry-skill-smoke.py` → 首行输出逐字 `PASS ac-90 entry-skill smoke (6/6 checks)`。
3. runner 联跑：`python campaign/acceptance/run_all.py --out .campaign/evidence/ac-run-20260922.txt` → 汇总表含 `| AC-90 | PASS |` 行（断言：`grep -cF '| AC-90 | PASS |' .campaign/evidence/ac-run-20260922.txt` → `1`；runner 经 glob `ac-*.py` 自动发现新脚本、自建输出目录——run_all.py L35/L55，无需前置建目录）。
4. cache 残留检查（R3 联动，只读）：`ls "/c/Users/Administrator/.zcode/cli/plugins/cache/campaign-suite/campaign/"` → 记录现存版本目录，供交接节比对；0.4.0 安装后是否多版本并存由用户安装后自查（执行时点 0.4.0 尚未安装；本地源无更新检测，2026-09-16 memory 实证）。

**Interfaces**：Consumes = C4, C7, C8, T1–T4 全部产物；Produces = ac-90 脚本 + `.campaign/evidence/ac-run-20260922.txt`。

**验证期望**：步骤 2/3 的输出即验证（首行 PASS 逐字 + runner 表行 PASS）。

## 执行编排预分配表（exec-forge 路径必产）

| 任务 | 性质 | 难度 | 形态 | 执行者 | 审查者 | 注入档 | 领域组件 |
|---|---|---|---|---|---|---|---|
| T1 | 文档 | 判断 | inline | 主线程 | 独立 reviewer（code-reviewer → general-purpose 链） | N/A | [writing-skills, writing-great-skills]（预绑定） |
| T2 | 配置 | 机械 | dispatch | coder → general-purpose | 独立 reviewer | 指令化 | [plugin-creator]（预绑定） |
| T3 | 文档 | 机械 | dispatch | general-purpose | 独立 reviewer | 指令化 | 无（彩排确认） |
| T4 | 文档 | 判断 | inline | 主线程 | 独立 reviewer | N/A | 无（彩排确认） |
| T5 | 操作 | 集成 | dispatch | general-purpose | 独立 reviewer | 指令化 | 无（原候选弃用，见裁定节） |

## 风险登记

| # | 触发条件 | 爆炸半径 | 可逆性 | 处置 |
|---|---|---|---|---|
| R1 | description 触发面过宽，普通单 plan 任务被路由进 campaign | 双入口打架复发，用户对 campaign 信任崩 | git revert + 重装 | 修：排除句（C1）+ AGENTS.md 优先级（C3）+ T5 检查 2 静态守卫 + 工序 4 彩排非域文本实测 |
| R2 | AGENTS.md 替换引入歧义或误伤既有节 | 所有项目的工程任务入口 | 备份秒回（T4 步骤 1/4） | 修：C3 逐字文本 + 备份 + 回读验证 + 独立审查；约束 8 限定只动一节 |
| R3 | 0.4.0 重装后 0.3.0 cache 目录残留并存 | skill 列表重复、调用歧义 | 卸载重装 | 兜底：T5 步骤 4 只读检查 + 交接节提示（触发器：见多版本并存即卸载重装） |
| R4 | run_all.py docstring「恒 36 行」与新增 ac-90 语义冲突 | 未来读者误解 runner 契约 | 改 docstring 可逆 | 接受+登记：本 plan 不改 runner（零触碰原则）；重访触发器 = 下一波 acceptance 整理时改 docstring |
| R5 | AGENTS.md 新条款与「三 skill 锻造流水线」节语义重叠致全局指令自相矛盾 | 全局指令可信度 | 备份秒回 | 修：新文本保留 caliber 定级语义（「不命中 → caliber 定级」原句形态），V11 验证既有节完好 |

## 技能消费裁定节

工序 4 彩排 Phase 2（2026-09-22，fresh 零背景基线）建议 + 编排者逐条裁定：

| 任务 | 建议 | 裁定 | 理由 |
|---|---|---|---|
| T1 | writing-skills + writing-great-skills（路由表命中） | 采用 | SDO（description 只写触发条件）约束 C1 排除句写法；router skill 范式正是本入口形态；与原候选一致 |
| T1 | skill-reviewer（路由表命中，自检补充） | 弃用 | V1–V13 机械闸已覆盖其 checklist 机械部分，第三人称/触发条件约束已由 writing-skills SDO 承载，叠加收益低 |
| T2 | plugin-creator（路由表命中） | 采用 | 「增量迭代 = 改文件+递增语义版本、不重脚手架」「marketplace 保留无关条目」纪律正对 T2；与原候选一致 |
| T3 | 无 | 无（确认） | 彩排显式答无——纯机械 README 五处锚定替换，无组件能力交集 |
| T4 | zcode-configuration-guide（全局清单，附 description 摘录）+ gstack（路由表命中，参考） | 弃用 | T4 为 inline 判断类，主线程已持全部上下文；目标文件是用户级单文件单节逐字替换，无 scope 合并问题；gstack 路由形态在 plan 阶段已消费完毕 |
| T5 | 弃用 zcode-configuration-guide（彩排弃用建议） | 采纳弃用，T5 = 无 | T5 主体为自写零依赖 Python 验收脚本 + git diff 守卫，组件能力域无交集；步骤 4 cache 只读 ls 所需发现顺序知识已由 R3/交接节承载 |

预绑定语义：预绑定 = 默认消费——dispatch 边界偏离须记台账 Ruling，终审闭环核查；未绑定任务的组合决定由编排层在 dispatch 边界做出。

## 交接节（plan 完成后消费）

- 执行引擎：caliber:exec-forge（非代码主导）；阶段 4 入口批量确认停止点确认上表（含彩排后预绑定回写）。
- 生效路径（用户操作，不进任务块）：插件改源后本地源无更新检测——递增版本已就位（C4），用户在 Plugin Management 卸载重装后，新会话生效（hooks 注册表会话启动时快照，config 无热加载，2026-09-12/13 实证）。
- cache 多版本触发器（R3 联动）：用户卸载重装后，若 `ls "/c/Users/Administrator/.zcode/cli/plugins/cache/campaign-suite/campaign/"` 见多版本目录并存 → 再次卸载重装（残留旧版会致 skill 列表重复、调用歧义）。
- known-issues 联动（阶段 6 触发核查）：KI-01 关闭（证据 = 本 plan + ac-90 PASS）；KI-02/KI-03 更新为「部分消化」并留指针（域地图表 / Step 0 依赖验证）；KI-04/05/06/07 不触动。

---

**plan 锻造总结行**（plan-forge 四工序全过，审计指针 = `.caliber/review-logs/2026-09-22-campaign-entry-skill-plan.md`）：发现数 = 工序 3 轮 1 十七项（自审 4 + 双声部 13：P1×1、P2×4、P3×8）+ 轮 2 三项（P3）+ 工序 3.5 闸口六项（G1×4、G2×1、G3×1，均 P2）+ 工序 4 困惑补全五处；分类分布 = 全 Mechanical（R2-F1 Taste 与 G1-F2 范围确认各一，全权授权折叠记台账）；收敛轮次 = 工序 3 两轮收敛、工序 3.5 四闸口终局 PASS；技能消费裁定 = 六条（采用 2 / 弃用 3 / 无确认 1，预绑定 T1、T2）；未决项 = NO UNRESOLVED（挂起项 ①②③ 为显式挂起带触发器，非未决）。
