# plan：campaign 插件工程约定通道（长程一致性机制）

> 2026-09-22 ｜ caliber ML 级 ｜ 引擎路由 = coding-forge（代码主导 + git）
> 方案来源 = 双轨收敛（主轨分析 + 挑战者 caliber:architect 独立生成报告），用户三项拍板在案

## 对齐快照

### 目标重推

给 campaign 插件补上「工程约定 → 执行单元」的机械通道：program.py 装配 brief 时
把工程约定文件全文注入（替代手工补、消灭记性方差与重装配冲刷），validate 对
零覆盖程序告警，gate 支持 opt-in lint 复跑门，对账加互斥矛盾附查，收账 ruling
回流约定文件；顺带把悬空引用的 K19 yaml schema 落盘，ingest-forge 映射指引加
约定指向。新增文件恰 2 个：conventions 模板 + ac-91 验收脚本。

### 道层条款

- **价值排序**：机械通道 > 指引文本；零新增 hook/skill/工具 > 新组件；
  context 预算纪律 > 表达完整。
- **不可妥协项**：① 约定到达执行单元必须走装配机械注入，不靠人记得；
  ② lint_cmd opt-in——缺席时 cmd_gate 行为与现状逐字节一致；cmd_validate
  唯一新增 = K6 WARN 行（M2 设计本意，exit code 与 OK 行不变）；
  ③ brief = 纯派生工件（重装配幂等，禁手改，内容只改源）。
- **失败的形状**：机制装好但约定文件静默空转无人知（M2 WARN 的存在理由）；
  约定文件膨胀致死（30 行 cap 的存在理由）；lint_cmd 假失败卡死程序
  （opt-in + 「必须是开发者日常同一命令行」文档条款的存在理由）。

### 开放决策点 + 方案选定记录（2026-09-22 拍板）

| 决策点 | 选定 | 备选（未选理由） |
|---|---|---|
| 范围 | 合并方案全量（M1–M6 + K19 落盘 + ingest 指引行 + 模板 + ac-91） | 砍 M4（lint 门价值对 AeroFold 即时可用，保留）；最小刀（留三洞，否决） |
| 约定文件缺省路径 | 工程根 `CONVENTIONS.md`（meta `conventions:` 可覆盖） | docs/engineering-conventions.md（发现性次于根级，否决） |
| 子档 | ML | MS（契约变更 + 新验收脚本，轻量 plan 兜底不足） |
| 组件卡/touches | **否决**（采纳挑战者否决 #1：行内路径标签 + 模板「组件边界」节替代） | 做（防文档膨胀/匹配靠猜/平台日后或原生支持嵌套 AGENTS.md 成双份事实源） |
| K21 预算 | 总 90 行 / 约定节 ≤28 行 / 源文件 ≤30 行 cap | 宪章瘦身保 60（截断+WARN 机制更机械，采纳挑战者数字） |
| 版本号 | 不动（plugin.json/manifests 全留 0.4.0） | 升版（publish 属用户决策点，不在本任务边界） |

### 挂起项（带触发器）

1. touches/组件卡选读通道——触发器：AeroFold M2 客户端开工前，或对账/审查
   首次发现跨单元组件边界矛盾。
2. lint 配置起草能力（帮仓库起草 lint 配置，spec/ingest 域新增能力）——
   触发器：首个无 lint 工具链的工程进入 program 域。
3. 插件版本号升级与卸载重装发布——触发器：本任务验证全过后的用户 publish
   决策。
4. KI-09 探针升级——触发器原样（ac-90 修订窗）；ac-91 用行为断言，天然无
   未跟踪文件盲区，不继承该病。

### 前提清单（全部实测 2026-09-22）

- 仓库 F:\workspaces\campaign-suite，git 工作树干净；Python 3.14.3 在 PATH。
- program.py 434 行（cmd_brief L238-283 / lint L154-192 / cmd_validate
  L208-217 / cmd_gate L306-329 / main L402-433；imports 无 subprocess）。
- ac-90 251 行；program-forge SKILL.md 100 行；ingest-forge SKILL.md 68 行。
- docs/TODO.md 缺席（选材第 5 条登记）；known-issues.md 同域核查 = KI-04..09
  均不消化（KI-08 不命中——本任务不改 campaign/SKILL.md；KI-09 登记为
  ac-91 避同类盲区，见挂起项 4）。
- 执行者从**工程根**运行 program.py（其 `.campaign/` 等路径全为 cwd 相对，
  CONVENTIONS.md 解析同此语义）。
- `campaign/acceptance/run_all.py` 按 `ac-*.py` glob 自动发现验收脚本
  （零注册，已读核实）——ac-91 落位即被 T7 步骤 4 覆盖。

## Global Constraints

- 零新增 hook / skill / 工具文件；新增常驻文件恰 2 个
  （`campaign/conventions/engineering-conventions-template.md` +
  `campaign/acceptance/ac-91-brief-conventions.py`）。
- program.py 零第三方依赖纪律不破（subprocess 为 stdlib）。
- lint_cmd 缺席（无 meta 键或值 `-`）时 cmd_gate 输出与行为逐字节一致；
  cmd_validate 唯一新增 = K6 WARN 行（M2 设计本意，exit code 与 OK 行不变）。
- `## Global Constraints 候选` 节 D1–D4 四行原样不动；ac-90 check5 锚
  （spec-context.sh case 模式行）不触碰；hooks/ 目录整目录不动。
- brief 消费方仅执行 agent 人读（全仓 grep 无代码解析 brief 文件）——
  加节零解析风险。
- 禁改插件 cache；不改 hooks.json 硬编码 bash 路径；不碰
  F:\workspaces\caliber-suite 的 caliber/ 本体；版本号全部不动。
- 双 marketplace.json 同形守卫：本任务不触碰两 manifest（无联动改）。

## Review Focus（≤5 条）

1. **mini parser 不支持注释行**（program.py L60-61：`#` 开头行 raise
   YamlErr）——ac-91 fixture yaml 带注释即炸。钉 T4：fixture 零注释；
   六态全 PASS 覆盖。
2. **Windows shell=True 走 cmd.exe**——lint_cmd 引号语义差异可致假失败。
   钉 T3/T4：ac-91 门态 lint_cmd 用 `python -c "..."` 双引号形态
   （cmd/sh 双兼容，且与文档条款「开发者日常同一命令行」一致）。
3. **截断静默丢尾部禁则**——约定文件尾部规则截断后不在 brief。
   钉 T2：截断标记行必须含「全文见 <path>」指针；T4 态 3 断言标记行在。
4. **cwd 依赖**——从非工程根调用时 CONVENTIONS.md 解析错位。钉 T2：行为与
   `.campaign/` 既有 cwd 语义一致（skill 文档写明从工程根运行）；T4
   fixture subprocess 显式 `cwd=tmp` 验证。
5. **lint_cmd 执行顺序**——基本证据不齐时跑 lint 是浪费且 MISSING 语义
   混乱。钉 T3：lint_cmd 仅在基本 missing 为空后执行；T4 态 5 fixture
   证据齐备验证失败进 MISSING。

## 契约矩阵

跨任务契约（各任务 Interfaces 块与本表逐字一致）：

- **K1 路径契约**：约定文件路径 = program.yaml meta `conventions:` 值，
  缺省 `CONVENTIONS.md`；cwd 相对（与 `.campaign/` 同语义）。meta 键名
  `conventions` / `lint_cmd` 均合 parser 键名规则 `[A-Za-z_]+`
  （program.py L66/L77 实测）。
- **K2 brief 七节固定节序（K21 v2）**：
  `# Unit Brief: <id> <title>` → 派生声明注释行（K8）→ `## 单元目标` →
  `## SRS 锚点` → `## 前序接口产物` → `## Global Constraints 候选`
  （D1–D4 原样）→ `## 工程约定`（K3）→ `## 验收锚`（K4）。
- **K3 `## 工程约定` 节三态**（「内容行」= 文件行，不剥离空行/标题）：
  存在且 ≤25 行 → 全文注入（0 行 = 节内仅标题与空行，归本态）；
  存在且 >25 行 → 注入前 25 行 + 追加标记行
  `…（约定文件超预算截断，全文见 <path>）` + stdout 逐字
  `WARN: <path> 超 25 行，已按 brief 注入上限截断`；缺席 → 节内一行
  `（未配置：<path> 缺席）`。
- **K4 `## 验收锚` 追加**（AC 行之后；AC 行恒为单行——现码
  `"、".join(acs)` 或 `无`）：固定行
  `- 约束符合：产物不得违反「工程约定」节任一条目（审查时逐条引用核对）。`；
  条件行（仅 lint_cmd 已配置 = meta 值非空且 ≠ `-`；空值视同缺席——
  执行期 Ruling 2026-09-22）
  `- 可执行检查：`<lint_cmd>` 须零告警通过（gate 复跑，失败即 MISSING）。`
  （反引号包命令原文）。
- **K5 预算 WARN**：brief 总行数 >90 → stdout 逐字
  `WARN: brief <n> 行超预算 90（不阻断；瘦身顺序：先瘦约定文件）`，不硬失败。
- **K6 validate WARN（M2）**：约定文件缺席 且 lint_cmd 未配置（meta 缺席、
  空值或为 `-`）→
  lint() warns 追加逐字
  `程序零工程约定机械覆盖——风格约束仅靠 agent 自律（约定文件 <path> 缺席且无 lint_cmd）`
  （cmd_validate 既有 `WARN: %s` 打印前缀自然成形）。
- **K7 gate lint_cmd 门（M4）**：lint_cmd 已配置（meta 值非空且 ≠ `-`；
  空值视同缺席），且基本 missing
  （status / gate 文件 / result）为空后 →
  `subprocess.run(lint_cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)`；
  非零退出或 TimeoutExpired → missing 追加
  `lint_cmd 失败(rc=<n>): <stdout+stderr 合并尾部 500 字符>`
  （超时记 `rc=timeout>300s`），走既有 MISSING 路径（ledger + print +
  exit 1 + 状态不迁移）；零退出 → 原 PASS 路径。lint_cmd 进程 cwd 继承
  program.py 进程 cwd（= 工程根，与模板「开发者日常同一命令行」条款互证）。
- **K8 派生声明行**（brief 第 2 行，逐字，`<path>` 为 K1 resolve 值）：
  `<!-- 派生文件：program.py brief 重装配时整体重写；改内容请改源（program.yaml / <path>），勿手改本文件 -->`
- **K9 模板文件**：`campaign/conventions/engineering-conventions-template.md`，
  七节（命名 / 注释与文件头 / 分层边界 / 错误处理 / 禁则清单 / 组件边界 /
  可执行检查）≤30 行，全文见 T1 步骤。
- **K10 ac-91 六态**：注入态 / 缺席态 / 截断态 / 门通过态 / 门失败态 /
  validate WARN 态（K6 回归保护），断言逐字见 T4 步骤；exit 0=PASS /
  1=FAIL，首行总结（run_all 归类契约，与 ac-90 同）。
- **K11 program-forge 修订五处**：输入节 K19 schema 块 + 约定通道段 /
  LOOP 步 3「K21 六节」→「K21 七节」/ K21 节改写 v2 /
  对账 prompt 骨架加 M5 附查行 / 输出包后加 M6 回流段。
- **K12 ingest-forge 修订一处**：第二步判别指引加约定指向一句（T6 逐字）。

## 任务块

### T1 conventions 模板文件

画像: 性质=文档; 难度=机械; 领域词=[conventions 模板, 工程约定, 插件资源文件]
技能消费: 无

步骤：新建 `campaign/conventions/engineering-conventions-template.md`
（`conventions/` 为新目录，随建文件一并创建），全文逐字：

```markdown
# <工程名> 工程约定（CONVENTIONS.md）

> 每条约定合法性三选一：生态标准采纳（注明出处）/ 裁定记录（ADR 或 ruling ID）/
> 现有代码范例（文件:行）。全文 ≤30 行硬顶——brief 注入上限 25 行，超线被截断。

## 命名
（例：类型大驼峰 / 函数与变量蛇形 / 常量全大写；模块前缀 <例：af_>）

## 注释与文件头
（例：包注释首行 = 职责一句 + 约束出处；文件头横幅仅 <枚举文件> 保留）

## 分层边界
（例：<上层> 不直连 <下层>；依赖方向不反——下层不 include 上层）

## 错误处理
（例：错误信封形状以 <契约文件> 为唯一源，禁造表外字面值）

## 禁则清单
（每条一行 + grep 配方，例：禁 <模式> —— `grep -rn '<模式>' <路径>` 应零命中）

## 组件边界
（每行 = <路径前缀>: 一句话职责/边界/不变量；单条约定可用行内路径标签限定
作用面，例：`- [仅 server/internal/ws/] 帧处理不得触碰业务状态`）

## 可执行检查
（lint_cmd 建议值 = 开发者日常在仓库根运行的同一命令行，例 `golangci-lint run`）
```

Interfaces: Produces K9。
验证期望：`wc -l campaign/conventions/engineering-conventions-template.md`
输出 ≤ 30；`grep -c '^## ' <文件>` = 7（七节标题）。

### T2 cmd_brief 改造（M1 注入 + M3 声明 + K4 验收锚 + K5 预算）

画像: 性质=新增; 难度=集成; 领域词=[program.py, cmd_brief, 约定注入, K21 七节]
技能消费: [program-forge]

步骤（对 `campaign/tools/program.py` 的 cmd_brief 函数，L238-283）：

1. 函数首部（组装 `lines` 列表之前的任意位置）解析约定路径与内容：
   `cpath = str(prog.meta.get("conventions") or "CONVENTIONS.md")`；
   读文件（`os.path.exists(cpath)` 时
   `open(cpath, encoding="utf-8").read().splitlines()`——splitlines 无
   尾换行幻影行；空行/标题照数，合 K3「内容行」定义），
   按 K3 三态得到 `conv_lines`（注入行列表）与可选截断 WARN。
2. 标题行后插入 K8 派生声明行（`<path>` 填 cpath）。
3. `## Global Constraints 候选` 块（D1–D4 四行原样）后、`## 验收锚` 前，
   插入 `## 工程约定` 节：标题 + 空行 + conv_lines。
4. `## 验收锚` 的 AC 行后追加 K4 固定行；meta `lint_cmd` 存在且 ≠ `-` 时
   再追加 K4 条件行（反引号包 lint_cmd 原文）。
5. 写文件前按 K5 检查总行数，超 90 打印 WARN（不阻断）。截断 WARN 在
   步骤 1 判定发生时即打印。写文件调用沿用既有
   `open(out, "w", encoding="utf-8", newline="\n")`（不动）。

Interfaces: Consumes K1/K2；Produces K3/K4/K5/K8。
验证期望（Git Bash，仓库根）：

```bash
tmp=$(mktemp -d) && cd "$tmp" && mkdir -p .campaign/program
printf '%s\n' 'program: t' 'context: -' 'created: t' 'reconcile_every: 5' 'last_reconciled: 0' 'units:' '  - id: U-1' '    title: 冒烟' '    status: pending' '    depends: []' '    parallel: "-"' '    gate: []' > prog.yaml
python "F:/workspaces/campaign-suite/campaign/tools/program.py" brief --program prog.yaml --unit U-1
grep -c '^## 工程约定$' .campaign/program/U-1-brief.md   # 期望 1
grep -c '（未配置：CONVENTIONS.md 缺席）' .campaign/program/U-1-brief.md   # 期望 1
grep -c '派生文件：program.py brief 重装配时整体重写' .campaign/program/U-1-brief.md   # 期望 1
grep -c '约束符合：产物不得违反' .campaign/program/U-1-brief.md   # 期望 1
grep -c '^- D1 事实源' .campaign/program/U-1-brief.md   # 期望 1（D1–D4 回归锚）
grep -c '可执行检查' .campaign/program/U-1-brief.md   # 期望 0（无 lint_cmd）
python "F:/workspaces/campaign-suite/campaign/tools/program.py" brief --program prog.yaml --unit U-1   # 重跑（重装配幂等）
grep -c '派生文件：program.py brief 重装配时整体重写' .campaign/program/U-1-brief.md   # 期望仍 1（不重影）
```

（fixture yaml 零注释——mini parser 遇 `#` 行报错，Review Focus #1。）

### T3 cmd_validate WARN（M2）+ cmd_gate lint_cmd 门（M4）

画像: 性质=新增; 难度=集成; 领域词=[program.py, cmd_validate, cmd_gate, lint_cmd 门]
技能消费: [program-forge]

步骤（同文件，接 T2 后）：

1. `lint(prog)`（L154-192）尾部追加 K6 判定：`cpath` 同 K1 解析，
   `os.path.exists(cpath)` 为假 且 `prog.meta.get("lint_cmd")` 缺席或为 `-`
   → warns 追加 K6 逐字文案（`<path>` 填 cpath）。
2. 文件头 import 区加 `import subprocess`。
3. `cmd_gate`（L306-329）：在 `if missing:` 分支**之前**插入 lint_cmd 段——
   仅当 `not missing` 且 meta lint_cmd 存在且 ≠ `-` 时执行 K7 调用；
   非零退出/超时 → missing 追加 K7 文案（随后自然落入既有 MISSING 分支）。

Interfaces: Consumes K1；Produces K6/K7。
验证期望（独立自含——shell 变量不跨调用续存，不承接 T2 的 $tmp）：

```bash
tmp=$(mktemp -d) && cd "$tmp" && mkdir -p .campaign/program
printf '%s\n' 'program: t' 'context: -' 'created: t' 'reconcile_every: 5' 'last_reconciled: 0' 'units:' '  - id: U-1' '    title: 冒烟' '    status: pending' '    depends: []' '    parallel: "-"' '    gate: []' > prog.yaml
python "F:/workspaces/campaign-suite/campaign/tools/program.py" validate --program prog.yaml
# 期望输出含逐字一行：WARN: 程序零工程约定机械覆盖——风格约束仅靠 agent 自律（约定文件 CONVENTIONS.md 缺席且无 lint_cmd）
# （其前另有既有行 WARN: U-1: empty gate list，不干扰）
# 且末行仍为：OK: 1 units, schema+lint pass
```

### T4 ac-91 验收脚本（六态）

画像: 性质=新增; 难度=集成; 领域词=[ac-91, 验收脚本, 六态 fixture, acceptance]
技能消费: [verification-before-completion]

步骤：新建 `campaign/acceptance/ac-91-brief-conventions.py`：

1. 骨架仿 ac-90：`REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))`；
   `PROGRAM_PY = os.path.join(REPO_ROOT, "campaign", "tools", "program.py")`；
   编码纪律照 ac-90 docstring（open 显式 utf-8；subprocess
   `text=True, encoding="utf-8", errors="replace"` + try/except）。
2. 每态独立 `tempfile.TemporaryDirectory()`；fixture prog.yaml 零注释，
   meta 含 program/context/created/reconcile_every/last_reconciled（+
   态 4/5 加 `lint_cmd`），units 单条 U-1。调 program.py 一律
   `[sys.executable, PROGRAM_PY, <cmd>, "--program", "prog.yaml"]` +
   `cwd=tmp`：态 1/2/3 <cmd>=`brief` 追加 `"--unit", "U-1"`；态 4/5
   <cmd>=`gate` 追加 `"--unit", "U-1"`；态 6 <cmd>=`validate`（无
   --unit）。fixture unit 无需 brief/plan 键（cmd_brief/cmd_gate 均不
   读取，已抽核）。
3. 六态（check 函数返 (bool, str)，main 收集首行总结，exit 0/1）：
   - **态 1 注入态**：tmp 根写 CONVENTIONS.md，两行内容
     `- 命名一律蛇形` / `- 禁全局可变状态`。跑 brief。断言 brief 文本：
     含 `## 工程约定`（计数 1）、含 `- 命名一律蛇形`、含 `- 禁全局可变状态`、
     含派生声明行（计数 1）、含 `约束符合：产物不得违反`、含 `- D1 事实源`
     （D1–D4 回归）、**不含** `可执行检查`（无 lint_cmd）。
   - **态 2 缺席态**：无 CONVENTIONS.md。跑 brief。断言含逐字
     `（未配置：CONVENTIONS.md 缺席）`。
   - **态 3 截断态**：CONVENTIONS.md 写 30 行（`- rule-01` … `- rule-30`）。
     跑 brief。断言：brief 含 `- rule-25`、**不含** `- rule-26`、含
     `约定文件超预算截断，全文见 CONVENTIONS.md`；stdout 含逐字
     `WARN: CONVENTIONS.md 超 25 行，已按 brief 注入上限截断`。
   - **态 4 门通过态**：meta 加 `lint_cmd: python -c "import sys; sys.exit(0)"`；
     U-1 `status: in_progress`、`gate: [evidence.txt]`、`result: result.md`，
     tmp 造非空 evidence.txt 与 result.md。跑 gate。断言：rc=0，
     stdout 含 `U-1: in_progress -> complete (gate PASS)`；
     prog.yaml 文本含 `    status: complete`。
   - **态 5 门失败态**：同态 4，lint_cmd 改 `python -c "import sys; sys.exit(3)"`。
     跑 gate。断言：rc=1，stdout 含 `MISSING` 且含 `lint_cmd 失败(rc=3)`；
     prog.yaml 文本仍含 `    status: in_progress`（状态未迁移）。
   - **态 6 validate WARN 态**（K6 回归保护）：fixture 同态 2（无
     CONVENTIONS.md、无 lint_cmd）。跑 validate。断言：rc=0；stdout 含
     逐字
     `WARN: 程序零工程约定机械覆盖——风格约束仅靠 agent 自律（约定文件 CONVENTIONS.md 缺席且无 lint_cmd）`；
     stdout 末行 == `OK: 1 units, schema+lint pass`。
4. 各态 fixture 的 yaml 写文件用 `newline="\n"`；yaml 字符串内不得出现
   `#` 起始行（Review Focus #1）与制表符。

Interfaces: Consumes K1/K3/K4/K6/K7/K8/K10；Produces K10。
验证期望：`python campaign/acceptance/ac-91-brief-conventions.py` 首行
`PASS`、exit 0；随后故意破坏验证（执行者自选其一：把 T2 注入行注释掉，
或将态 3 的 `- rule-26` 断言改为存在断言）→ 首行 `FAIL`、exit 1；
验证后恢复，恢复后再跑一次 → 首行 `PASS`、exit 0（复核归位）。

### T5 program-forge SKILL.md 五处修订

画像: 性质=文档; 难度=判断; 领域词=[program-forge SKILL.md, K21 v2, K19 schema, 对账附查, ruling 回流]
技能消费: [program-forge, writing-great-skills]

步骤（对 `campaign/skills/program-forge/SKILL.md`；契约文字必须与 T2/T3
代码行为逐字一致）：

1. **输入节**（现 L17 行）：「schema 见契约 K19」悬空引用改写为自带定义——
   该行替换为：
   ```
   - `.campaign/program/<name>.yaml`：程序定义（DAG），schema（K19）：
     - meta 顶级键：`program` / `context` / `created` / `reconcile_every` /
       `last_reconciled`；可选 `conventions:` = 约定文件路径覆盖（缺省
       `CONVENTIONS.md`，工程根）；可选 `lint_cmd:` = gate 复跑的 lint
       命令行（缺席、空值或 `-` = 不跑）。
     - unit 键：`id` / `title` / `status`（pending/in_progress/complete/blocked）/
       `depends` `gate`（inline list）/ `parallel`（v1 恒 `-`）/ `brief` /
       `result` / `plan` / `budget_s`。
     - parser 限制（program.py 迷你 YAML 子集）：键名仅 [A-Za-z_]；
       不支持注释行；inline list 仅 `depends`/`gate` 两键。
   ```
   并在输入节追加约定通道段：
   ```
   约定通道（何时裁定 / 写什么）：
   - 制宪时刻：首个编码单元启动前，由该单元产出 CONVENTIONS.md 并经用户
     裁定；模板 = campaign/conventions/engineering-conventions-template.md。
   - 里程碑边界：新语言/新框架入场 → 补生态层裁定（lint 配置入库 + lint_cmd）。
   - 首次复触：单元首次改动他单元产出的包 → 对应组件边界行进「组件边界」节。
   - 并行启动：parallel 放开前 → 组件边界与数据所有权先就位。
   ```
2. **K21 节**（现 L48-53 输入包段）改写为：
   ```
   **输入包** `<id>-brief.md`（program → caliber，骨架 ≤60 行 + 工程约定节
   ≤28 行，总预算 90 行——超线 stdout WARN 不硬失败，固定七节序）：
   `# Unit Brief` → 派生声明注释行（brief 是纯派生工件，禁手改——改内容
   请改源 program.yaml / 约定文件）→ `## 单元目标` → `## SRS 锚点`
   （FR/NFR/C/Q/AC ID + doc_graph 定位 file:line）→ `## 前序接口产物`
   （depends 单元 result 指针）→ `## Global Constraints 候选`（D1–D4
   编排纪律）→ `## 工程约定`（约定文件全文注入；缺席 = 占位行；超 25
   内容行截断 + 截断标记 + WARN）→ `## 验收锚`（关联 AC + 固定行
   「约束符合：产物不得违反『工程约定』节任一条目」+ meta 有 lint_cmd
   时追加「可执行检查」行）。
   约定文件自身 ≤30 行硬顶（cap 是防膨胀免疫系统）；制宪时点见输入节
   约定通道段。
   ```
   输出包段（L55-64）不动。F1 LOOP 步 3 行（现 L30）「（K21 六节）」
   改写为「（K21 七节）」（行内替换，其余不动）。
3. **对账节 prompt 骨架**（现 L80-87 代码块内，`Rules:` 行之前）插入逐字行：
   ```
   附查（有界）：上次对账以来 complete 的单元的产物之间，是否存在互斥的
   实现约定（命名/分层/错误处理范式两两矛盾）？只报互斥级矛盾，不报品味、
   不评质量；每条引用 文件:行。
   ```
4. **输出包契约代码块后**追加 M6 段：
   ```
   收账时约定回流（M6）：result 的 `ruling:` 行含工程约定条款 → 编排者把
   该条款追加进 CONVENTIONS.md（此后所有 brief 自动携带）；制宪时把禁则
   清单镜像进工程 `CONTEXT.md` 铁律段（该工程订阅 docs 治理体系时）。
   ```
5. 改后通读全文一遍：节序连贯、无残句、无重复段（writing-great-skills
   消费动作——single source of truth 与防 sprawl 视角）。

Interfaces: Consumes K2/K3/K4/K5/K6/K7/K8；Produces K11。
验证期望：
`grep -c '## 工程约定' campaign/skills/program-forge/SKILL.md` ≥ 1；
`grep -c '附查（有界）' <同上>` = 1；`grep -c '约定回流（M6）' <同上>` = 1；
`grep -c 'schema（K19）' <同上>` = 1；`grep -c 'schema 见契约 K19' <同上>` = 0；
`grep -c 'K21 六节' <同上>` = 0；
`wc -l <同上>` ≤ 135（预期 ≈131 = 现 100 + K19 块 +10 + 通道段 ≤7 +
K21 节 +7 + M5 +3 + M6 ≤4；LOOP 行改写 ±0）。

### T6 ingest-forge SKILL.md 指引行

画像: 性质=文档; 难度=机械; 领域词=[ingest-forge SKILL.md, 映射判别指引]
技能消费: [ingest-forge]

步骤：`campaign/skills/ingest-forge/SKILL.md` 第二步「判别指引」行
（现 L38）末尾追加一句（与前行同段）：
`；编码/架构约定类内容（命名/注释/分层规范）→ 指向工程根 CONVENTIONS.md（约定通道见 program-forge 输入节；文件不存在则登记为程序初始化期待办，不代写）`

Interfaces: Produces K12。
验证期望：`grep -c 'CONVENTIONS.md' campaign/skills/ingest-forge/SKILL.md`
= 1（现文件零命中，追加句恰含一次）；`wc -l <同上>` ≤ 70（现 68 行，
行内追加不增行）。

### T7 验证与收尾（全量归绿 + finishing 移交）

画像: 性质=操作; 难度=机械; 领域词=[run_all 回归, ac-90 归绿, commit 后验证]
技能消费: [verification-before-completion]

步骤（顺序不可换；commit 已在任务环完成——coding-forge git 语义节 = 每
任务至少一 commit、审查门区间锚承重，故为六 commit 而非原文三划分，
message 逐字如下）：
0. `git log --oneline <BASE>..HEAD` = 六行（T1–T6 各一；BASE =
   33b5cca2，见 coding ledger Setup 行）：
   T1 `campaign: conventions 工程约定模板（T1，工程约定通道）`
   T2 `campaign: program.py cmd_brief 约定注入 + K4 验收锚 + K5 预算（T2，工程约定通道）`
   T3 `campaign: program.py validate K6 WARN + gate lint_cmd 门（T3，工程约定通道）`
   T4 `campaign: ac-91 验收脚本（brief 约定通道六态）（T4）`
   T5 `campaign: program-forge 约定通道契约同步（K19 落盘 + K21 v2 七节 + M5/M6）（T5）`
   T6 `campaign: ingest-forge 映射判别指引约定指向（T6）`
   分支 = 新 branch `2026-09-22-campaign-conventions-channel-plan`
   （coding-forge §Setup「never on main/master without consent」闸——
   未获明确同意不上 master；finishing 菜单 merge/PR/keep/discard 由
   用户裁定，merge 即达仓库惯例终态）；**不 push**（publish 属挂起项 3）。
1. `python campaign/acceptance/ac-91-brief-conventions.py` → 首行 PASS
   exit 0（六态全过）。
2. `python campaign/acceptance/ac-90-entry-skill-smoke.py` → 6/6 PASS
   exit 0（全提交后 6① 归绿；6① 之外任何 BAD = 停）。
3. `python campaign/acceptance/run_all.py` → 汇总表 AC-90 = PASS 且
   AC-91 = PASS。
4. finishing 移交（caliber 阶段 6）：分支处置菜单 + known-issues
   触发核查 + 三行简报。

Interfaces: Consumes K10。
验证期望：步骤 1 输出首行 PASS；步骤 2 输出首行 PASS；步骤 3 汇总表
无 FAIL 行。

## 风险登记

| # | 触发条件 | 爆炸半径 | 可逆性 | 处置 |
|---|---|---|---|---|
| 1 | lint_cmd 平台差异（cmd/sh 引号）假失败 | 单程序 gate 卡死 | 可逆（去掉 meta 键即恢复） | opt-in + 文档「开发者日常同一命令行」+ T4 双态验证 |
| 2 | 约定文件膨胀 → brief 冗长 → agent 略读 | 全程序遵从率崩 | 可逆 | 30 行 cap + 截断 WARN + 模板指引行（T1） |
| 3 | 截断静默丢尾部禁则 | 尾部规则不达执行单元 | 可逆 | 截断标记行含全文指针（Review Focus #3）+ T4 态 3 |
| 4 | K5 预算 WARN 无行为断言覆盖（构造 90 行 fixture 成本高于价值） | WARN 回归失灵 | — | 接受：T5 契约文字 + 代码审查核对 |
| 5 | 在途程序旧 brief 仍为六节 | 执行单元读旧形态 | 可逆 | 重装配即升级（派生工件幂等）；T5 文档写明 |
| 6 | M6 回流被遗忘（全方案唯一非纯机械环节） | 涌现约定到不了后续 brief | 可逆（一行追加） | M5 对账附查兜底发现；接受残余 |
| 7 | ac-91 tmpdir 泄漏污染仓库 | 脏文件入库 | 可逆 | TemporaryDirectory 上下文管理器自动清理；T4 步骤 2 |
| 8 | 约定与代码现实脱节（aspirational conventions）→ 约定失信 | 全程序 | 可逆 | 模板指引：每条约定须指出现有代码范例或裁定出处（T1） |
| 9 | mini parser 注释行限制被 fixture 踩 | ac-91 自身炸 | 可逆 | Review Focus #1 + T4 步骤 4 禁令 |

## 技能消费裁定（工序 4 彩排后回写 · 2026-09-22）

预绑定语义：预绑定 = 默认消费——dispatch 边界偏离须记 ledger Ruling，
终审闭环核查。预绑定不是锁死，改变的是缺省（消费为默认、跳过须显式）。

| 任务 | 建议 | 裁定 | 理由 |
|---|---|---|---|
| T1 | 无 | 采用（无） | 逐字建文件 + wc/grep 验证，无组件增量；领域词命中 plugin-creator 但不推荐成立——publish 工序整体出边界（Global Constraints 版本号不动 + 挂起项 3） |
| T2 | program-forge | 采用 | 关键词命中 cmd_brief 输入包 / K21 / K19；F1 步 3 即被改路径，契约权威在此 |
| T3 | program-forge | 采用 | 关键词命中 cmd_validate WARN / cmd_gate 门检查；K6/K7 即其行为契约 |
| T4 | verification-before-completion | 采用 | 故意破坏红绿验证即其 Regression tests 形态；「证据先于断言」对齐 |
| T4 | code-review（路由表 review 段） | 弃用 | coding-forge 引擎内建实现/审查分席逐任务门已覆盖，独立双轴评审与引擎重复 |
| T5 | program-forge + writing-great-skills | 采用（两者） | 改自身 SKILL.md，契约文字须与代码逐字一致（program-forge）；结构改写质量纪律——single source of truth / 防 sprawl（writing-great-skills），消费动作 = 步骤 5 通读 |
| T5 | skill-reviewer（路由表 review 段） | 弃用 | frontmatter 触发面零改动，变更面已由 grep/wc 锚逐条钉死，通用启发式无增量 |
| T6 | ingest-forge | 采用 | 改自身 SKILL.md 判别指引；writing-great-skills 不作主推成立（单行逐字追加机械改动） |
| T7 | verification-before-completion | 采用 | 「无新鲜验证证据不得宣称完成」即 T7 全部动作 |
| T7 | code-review（路由表 review 段） | 弃用 | 同 T4 行理由 |
| 全任务 | plugin-creator（路由表 implement 段） | 弃用 | marketplace / 安装更新 / 本地分发工序整体在任务边界外（publish = 用户决策点） |
| T2/T5 | contract-first（plan 段，visible:false） | 已消费（非执行工序） | K21 六→七节契约治理已在 plan 阶段完成（K2 拍板在案），执行期无新增工序 |
| 全任务 | campaign（plan 段） | 弃用（无执行工序） | 分诊不治病；plan 阶段「不破坏分诊路由」核对已由路由层消费 |

<!-- REVIEW DECISION LOG -->
## 审查决策审计（plan-review-ritual v2.6.3 · ML 级 Step 1 自审 · 2026-09-22）

声部构成：ML 级 = Step 1 作者执行追踪式自审单声部（ritual 收尾节
「caliber ML 级仅用 Step 1 自审」）；后续的 plan-forge 工序 4 彩排
（confusion-hunt fresh subagent）是独立工序，非 ritual 声部 A，故本轮
无双声部共识表义务。

| ID | 来源 | 发现 | 分类 | 裁定 | 理由 | 修复位置 | 涟漪 |
|---|---|---|---|---|---|---|---|
| R1-F1 | Step1-④ 全局约束对照 | Global Constraints「lint_cmd 缺席时 validate/gate 输出与现状逐字节一致」与 K6 矛盾——M2 设计本意即双缺席时 validate 新增 WARN 行；不可妥协项 ② 同病 | Mechanical | 修 | 约束写宽了；K6/T3 验证期望才是拍板在案的设计本意 | 道层条款 ② + Global Constraints 行 | 否 |
| R1-F2 | Step1-③ 跨位置一致性 | F1 LOOP 步 3（现 SKILL.md L30）「（K21 六节）」未列入 T5 修订面，v2 七节序下变陈旧；全仓 grep 证实六节引用仅此一处 | Mechanical | 修 | 交叉引用漏改 | K11（四处→五处）+ T5 步骤 2 + 验证期望加 grep 'K21 六节'=0 | 否 |
| R1-F3 | Step1-① 心算断言 | T5 验证期望 `wc -l ≤ 115` 算错：plan 自带逐字块实际增量 ≈+31（K19 +10 / 通道段 ≤7 / K21 +7 / M5 +3 / M6 ≤4），预期 ≈131 > 115 必 FAIL | Mechanical | 修 | 断言值算错（增量估算偏离自带文本实测行数） | T5 验证期望 wc 行 | 否 |
| R1-F4 | Step1-⑤ 平台/语言事实 | T2 读约定文件方式未钉：`f.read().split("\n")` 对恰 25 行带尾换行文件数出 26 行 → 边界误截断 | Mechanical | 修 | 钉 `splitlines()`（无尾幻影行；空行/标题照数，合 K3「内容行」定义） | T2 步骤 1 | 否 |
| R1-F5 | Step1-⑤ 平台/语言事实 | K7 lint_cmd 进程 cwd 未写明（继承 program.py 进程 cwd = 工程根）——按所引 subprocess 调用形态实现自然继承，但契约层值得一句 | Mechanical | 修 | 澄清，零行为变化 | K7 文末补一句 | 否 |

### 零发现检查项留痕（查了什么、为什么没有）

- **心算断言（F3 之外）**：T2 六条 grep 逐条代入现 program.py L259-283
  结构 + 计划插入点（K8 第 2 行 / 工程约定节位置 / K4 位置 / D1 锚行首 /
  「可执行检查」零命中）全过；T3 validate WARN 逐字 = K6 文案 + 既有
  `WARN: %s` 前缀，empty-gate warn 在先不干扰末行 OK；T4 五态全链路对
  L323 `MISSING: %s` 与 L329 `%s: in_progress -> complete (gate PASS)`
  格式串逐字一致；态 5「仍含 status: in_progress」判别力核过（行级写回
  整行替换，误迁移即灭失该串）；T1 模板 26 行 ≤30、`^## ` 恰 7 个；
  T6 行内追加 68 行不变 ≤70。
- **模块级 import**：T3 唯一新增 `import subprocess`（stdlib，不破零依赖
  纪律）；ac-91 模块级仅 REPO_ROOT/PROGRAM_PY 路径推导，无 re.compile 类
  import 时执行语句。
- **跨任务一致性（F2 之外）**：K1 cpath 解析 T2/T3 同形；K3 截断 WARN
  文本 = 态 3 stdout 断言逐字；K4 条件行 `python -c "..."` 双引号形态
  cmd/sh 双兼容；K8「第 2 行」= T2 步骤 2「标题行后」；预算链
  骨架 ≤60 + 工程约定节 ≤28 ≤ 总 90 自洽；T2/T4 fixture yaml 逐行进
  parser（meta 键 `[A-Za-z_]+` / depends·gate inline list /
  `parallel: "-"` / 零注释 / 4 空格缩进）全过。
- **Global Constraints 其余各条**：恰 2 个新增常驻文件（T1 模板 + T4
  ac-91）；D1–D4 原样（断言锚 `^- D1 事实源` 行首在位）；hooks/ 整目录
  不动；cache / caliber 本体 / 版本号 / 双 marketplace 无任何任务触碰；
  ac-90 check5 锚（spec-context.sh case 行）不动。
- **平台事实（F4/F5 之外）**：shell=True→cmd.exe 引号形态 Review Focus
  #2 已钉且与态 4/5 lint_cmd 形态一致；grep UTF-8 中文按字节定串可行
  （ac-90 同法在先）；`newline="\n"` 写出 → `^…$` 锚无 \r 干扰；
  run_all 120s 超时 vs 五态数次 python 启停裕量充足；ac-90 6① 预红 /
  提交归绿与 KI-09 盲区交互核过——program.py 已跟踪故预红成立，ac-91
  全行为断言不依赖 git 追踪态。
- **User Challenge**：零——双轨拍板方向未被动摇，全部发现均为笔误 /
  漏改级。

总结：发现 5 ｜ Mechanical 5 / Taste 0 / User Challenge 0 ｜ NO UNRESOLVED。

### 工序 4 彩排回写记录（2026-09-22，单派遣两阶段）

派遣：fresh 零背景 general-purpose subagent；Phase 1 confusion-hunt（仅读
plan）→ Phase 2 技能消费映射（plan + routing.yaml + 命中组件正文）。
回收检查：Phase 1 报告混入组件名一处（「writing-great-skills 视角」括注）——
根源 = 派遣骨架内嵌 VISIBLE_MAP，该困惑点本体（T5 改后通读可预测性）成立
且与组件知识无关，时序隔离实质未破，留痕；建议表覆盖 T1–T7 含显式「无」；
无全局清单来源建议（全部路由表命中）；弃用建议逐条有理由；编排者裁定
逐条留痕（见「技能消费裁定」节）+ 任务块 `技能消费:` 行 ×7 + 本节三处
回写完成。

困惑点位裁定（修复 = 已回写 plan；容忍 = 附理由）：

| ID | 困惑点 | 裁定 | 落点/理由 |
|---|---|---|---|
| P4-F1 | T5 标题「四处修订」漏改残留（K11 已五处） | 修复 | T5 标题改五处 |
| P4-F2 | T3 验证「承接 T2 的 $tmp」跨 bash 调用不续存 | 修复 | T3 验证期望改独立自含块（自建 fixture） |
| P4-F3 | K6 validate WARN 无 ac-91 自动化覆盖（不可妥协项 ② 核心仅手工验证） | 修复 | T4 增态 6；K10 五态→六态；T4 Interfaces/领域词同步（涟漪：K10 文本，无跨任务引用波及） |
| P4-F4 | T7 commit message 未给 + add 范围未列 + 分支/push 未写 | 修复 | T7 步骤 2 补三条逐字 message + 逐文件 add 范围 + master 直提惯例 + 不 push |
| P4-F5 | run_all 发现机制未确认（ac-91 是否被覆盖） | 修复 | 前提清单补 glob 零注册已核实行 |
| P4-F6 | T2 写侧编码未钉 + 「loc 计算」未解释 | 修复 | 步骤 5 钉沿用既有 utf-8 写调用；步骤 1 措辞改「组装 lines 之前」 |
| P4-F7 | K4「AC 行之后」——AC 行单/多条未定 | 修复 | K4 补「AC 行恒为单行」注 |
| P4-F8 | 空约定文件（0 行）归属未定义 | 修复 | K3 补 0 行归全文注入态注 |
| P4-F9 | T4「跑 brief/gate」argv 形态未给 | 修复 | T4 步骤 2 钉 argv 逐字形态 + unit 无需 brief/plan 键（已抽核） |
| P4-F10 | 故意破坏「验证后恢复」无复核 | 修复 | T4 验证期望补恢复后再跑 PASS 归位 |
| P4-F11 | T1 新目录创建未写 | 修复 | T1 步骤补「conventions/ 为新目录」 |
| P4-F12 | T6 验证 `≥ 1` 弱（现文件零命中时可能原本成立） | 修复 | 改 `= 1`（现文件零命中已 grep 实证） |
| P4-F13 | T2 重装配幂等（不可妥协项 ③）无验证 | 修复 | T2 验证块补重跑 + 派生声明行计数仍 1 |
| P4-F14 | T5 改后无通读工序（可预测性视角） | 修复 | T5 增步骤 5 通读（writing-great-skills 消费动作） |
| P4-T1 | 「先读目标源文件定位锚点」类（D1–D4 全文 / ac-90 骨架 / L323·L329 格式串） | 容忍 | 执行者读码定位是 plan 执行标准前提（工序 1 纪律：代码块边界匹配）；plan 职责 = 钉锚点与契约，非复制现码 |
| P4-T2 | prog.meta / warns / missing 类型未定义 | 容忍 | 现码即权威，plan 引用属性名与现码一致（已抽核 L49/L311/L156） |
| P4-T3 | K19 `budget_s` 键无消费者 | 容忍 | parser 透传任意合法键，schema 记录 W4 设计意图；文档级零运行时风险 |
| P4-T4 | M6 引用 CONTEXT.md 未定义 | 容忍 | 逐字插入文本，指向目标工程的 caliber docs 治理概念，执行零理解需求 |
| P4-T5 | shell=True 引号 cmd 实际行为未预证 | 容忍 | 态 4/5 即在目标平台实证断言，炸则 ac-91 FAIL 显性暴露——正是验收职责 |
| P4-T6 | 彩排 agent 指「K19 块净增应 +9」 | 驳回 | 11 新行 − 1 原行 = +10，plan 算术无误（agent 自算错；≤135 帽有裕量） |

总结（工序 4 后）：ritual Step 1 发现 5（Mechanical 5，全修复）+
彩排困惑点修复 14 / 容忍 5 / 驳回 1 ｜ 技能消费裁定 13 行（采用 7 /
弃用 5 / 已消费 1）｜ 收敛轮次 N/A（ML 级无工序 3）｜ NO UNRESOLVED。
