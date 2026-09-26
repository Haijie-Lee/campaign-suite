# campaign × caliber 融合与共同生长机制 — plan（锻造中）

> 状态：锻造完毕（2026-09-26：工序 1 选材 → 工序 2 制坯 → 工序 3 三轮收敛 → 工序 3.5 闸口 → 工序 4 彩排全过），待阶段 4 实施（用户定格：阶段 4 开始前暂停）。方案确认停止点已过（2026-09-26，deep-probe ML 轻量档双轨：主轨 + 挑战者 architect 信息隔离独立生成，对照表见本文件末附录）。

## 对齐快照

### 目标重推

设计并落地 campaign×caliber 的融合机制，根治「campaign 冻结 caliber 旧管线快照、升级不传导」：F1 步 4 去枚举化（声明定级制委派 caliber 真入口，brief 为 CONTEXT）+ brief 身份还账节（A1）+ compact 注入在途单元 brief（A2）+ ac-93 派生式跨插件 lint（A3，含禁版本号规则）+ campaign-bridge.json 桥文件（A4，ui-forge 条目为首个金样；格式定为 JSON——G2 零第三方依赖约束，program.py 标准库 json 直读）+ 迁移姿态（程序收口后切换）。使：①caliber 升级自动传导进单元执行；②委派/compact 后单元不忘 campaign 层纪律；③跨插件契约机器可发现、可校验。

### 道层条款（价值排序/不可妥协项/失败的形状）

- D1：状态只认落盘文件，会话记忆不可信。
- D4：剂量不折叠——折叠权只在用户，通道 = caliber 原生折叠条件 + 程序级预授权 Ruling（用户已裁定，见 Q2）；campaign 编排层永不得自建折叠规则。
- 不可妥协：K21 文件契约形状（brief 进、result 出）不动；caliber 零改动优先（桥文件是唯一例外，且属 caliber 仓的自描述导出物）；在途程序规则不中途变更。
- 价值排序：机制正确性 > 用户裁定带宽 > token 成本。
- 失败的形状：①campaign 用户跑过时/缩水流程而不自知；②融合机制自身成为第三份需手工同步的文档，制造新漂移源。

### 开放决策点+方案选定记录

- **Q1 单元定级权 = 声明定级制**（用户裁定 2026-09-26）：单元形态→声明级别（判断/集成→声明 ML、文档→声明 S；修订单元例外——直调 plan-review-ritual REVISION 模式（B4），不经六阶段、无声明定级），caliber 五维只升不降；借 Step 1「用户一句话改级」通道，caliber 零改动。双轨独立收敛。
- **Q2 单元级阶段 1 剂量 = 原生折叠 + 程序级预授权**（用户裁定 2026-09-26）：挑战者照跑、对照表进账本；程序启动时一次性 Ruling 预授权「SRS 锚点已冻结方案空间的单元」按 caliber 原生折叠条件折叠方案确认停，逐次记 ledger。主轨原押注（campaign 侧自建「锚点冲突才停」规则）被挑战者证伪（违 D4），已否决。
- **Q3 在途迁移 = 程序收口后切换**（用户裁定 2026-09-26，取保守档）：aerofold-m2 全程旧语义跑完（U-M2-08 不动），新语义自下一程序起生效；AeroFold-ui 已收口不追改，其 gate 空转作 A4 反例夹具进 learnings。挑战者的「单元边界切换」建议被用户覆盖。
- **Q4 版本耦合 = 派生 lint + 软警告**（用户裁定 2026-09-26）：ac-93 查跨插件引用（封闭枚举 + 锚点存在 + 禁版本号规则 + 双写 cmp + 反向闭环）挂发布闸；campaign Step 0 读桥文件版本字段出一行 WARN，不新增停止点、不做硬门。
- 对照表（收敛 5 / 分歧 3 / 借鉴 1）与被否决路线（两插件合并 / 接口反转 / 版本钉死 / gate 指纹方案 B 本体）见附录，各带理由。

### 挂起项（带触发器）

- 单元级停止点带宽实测定价——触发器：首个新语义程序跑完，回填用户裁定带宽体感（模式文 §9.1 第七问同族）。
- A2 多 in_progress 注入策略——触发器：B2 parallel 语义重议时。
- 补丁 2（resume note 挂 program.py 事件自动写）——被 A2 吸收降级；触发器：A2 落地后编排者回接仍出困惑实证。
- deep-probe 判例成文（押注被证伪：「campaign 侧自建折叠规则」违 D4——道层条款优先于带宽优化直觉）——触发器：本设计案落地批执行时，写入 caliber-suite **源仓** `caliber/skills/deep-probe/references/probe-cases.md`（禁改 cache）。

### 前提清单

1. caliber 入口对「声明定级 + 外部 CONTEXT」调用健壮（文本已核实：接续任务条款 + 改级通道；首日实跑待验证）。
2. hook additionalContext 在 compact 后可见（2026-09-12 冒烟已实证）。
3. 桥文件与其描述的机制同仓同批落地（caliber 仓非 git 仓库——2026-09-26 闸口实证，「同提交」无指涉；纪律 = 同仓 + ac-93 check⑥ 机器兜底）。
4. acceptance 发布闸（run_all.py）必跑的纪律存续——A3 挂此闸。
5. program v1 串行成立（B2 挂起中）——A2「至多 1 个 in_progress 单元」假设依此。
6. Q3 裁定的代价：aerofold-m2 剩余单元（含 U-M2-08）不享受新机制——用户已知情裁定。

## Global Constraints

- **G1 双仓纪律**：campaign 改动只落 `F:\workspaces\campaign-suite`，caliber 改动只落 `F:\workspaces\caliber-suite`；**禁改** `C:\Users\Administrator\.zcode\cli\plugins\cache\` 下任何已安装副本（本地源无更新检测，改源后须卸载+重装生效——实证：memory zcode-plugin-system-facts）。
- **G2 零第三方依赖**：program.py / ac-9x / hooks 只用 Python 3.10+ 标准库与 Bash；桥文件解析用 `json`（标准库现成），禁止引入 YAML 解析器。
- **G3 ac 编码契约**（ac-91 docstring 逐字继承）：所有 `open()` 显式 `encoding='utf-8'`；subprocess 用 `text=True, encoding='utf-8', errors='replace'` 且 try/except 包住；fixture 写文件用 `newline='\n'`；fixture yaml 零注释零制表符；每态独立 `tempfile.TemporaryDirectory()`；REPO_ROOT 自 `__file__` 推（上三级），不依赖进程 cwd。
- **G4 run_all 归类契约**：ac 脚本首行 `PASS …` / `FAIL …`，退出码 0=PASS / 1=FAIL / 3=BLOCKED-ENV / 4=BLOCKED-IMPL；run_all.py 经 `glob("ac-*.py")` 自动发现（实证：run_all.py 第 35 行），**新 ac 文件落 `campaign/acceptance/` 即被收编，无需注册**。
- **G5 mini YAML 子集约束**（实证：program.py `_parse`）：program.yaml 顶级键名仅 `[A-Za-z_]+`；不支持注释行；inline list 仅 `depends`/`gate` 两键；本批唯一新增 meta 键 = `fold_grant`（合法键名）。
- **G6 hook 契约**：hooks.json 四组事件已注册（SessionStart matcher `startup|compact` / PreToolUse `Skill` / PostToolUse `Write|Edit` / Stop）；type 均 `"process"` + `C:/Program Files/Git/bin/bash.exe` 绝对路径（Windows 实证可行模式）；timeoutMs 5000；hook stdout = 单行 JSON（`hookSpecificOutput.additionalContext`）或空输出；exit 恒 0、异常静默。A2 只改 `handoff-inject.sh` 脚本体，**hooks.json 不动**。
- **G7 过程停折叠预授权**：用户 2026-09-26 明示「路由表以及后续过程除非致命性问题否则无需等确认，自主推进」——本 plan 的路由表确认停与阶段 4 入口批量确认停按 caliber 原生折叠条件折叠——三条件全满足才折叠：①用户消息含明确执行授权 ②无取舍待决 ③无新增不可逆操作（逐次记台账 Ruling）；与快照 / Q1–Q4 裁定冲突的发现、不可逆操作仍必停。
- **G8 KI-10 纪律**：plan 内「新建」断言全部经 2026-09-26 实测 `ls` 验证（`caliber/campaign-bridge.json` 不存在、`campaign/acceptance/ac-93*` / `ac-94*` 不存在——均为真新建）。
- **G9 KI-11 消化**：本批实质修改 `cmd_brief`/`cmd_gate`（重访触发命中）——两处未 with 化的 `open()`（program.py :262 `json.load(open(gpath, encoding="utf-8"))` 与 :275 `open(cpath, encoding="utf-8").read()`，行号 2026-09-26 实测）一并 with 化，零行为变化（ac-91 态 8 逐字节守护把守）。

## Review Focus

1. **桥信号误判面（宁漏勿错）**：信号 = paths 任一存在 **AND** keywords 任一命中（AND 收敛）；误报形态 = 单元被误拦（gate MISSING）烧裁定带宽；漏报形态 = 现状（无桥行为）。AND 语义的验证锚在 ac-94 态 2/3。
2. **A2 注入体积与 5s 超时**：`.campaign/program/*.yaml` 多程序（双线模式实证 = 2 程序）各至多 1 个 in_progress 单元（v1 串行硬拒 `parallel != "-"`，program.py lint 实证）→ 注入 ≤ N×90 行；hook 超时或异常 = 静默无注入，不阻塞会话（现状契约保持）。
3. **桥 locator 版本选择**：`CALIBER_PLUGIN_DIR` 环境变量 > `~/.zcode/cli/plugins/cache/caliber-suite/caliber/*/campaign-bridge.json` 取最高版本号 > 缺席跳过。ac-93/ac-94 用环境变量指 fixture，不触碰真实 cache。
4. **双写 cmp 提取规则脆弱性**：UI 信号句在 ui-forge §消费点契约与 plan-forge 工序 1 第 6 条各出现一次，ac-93 以固定起止子串提取后逐字比对；起止界标漂移 → ac-93 报 FAIL（fail-closed，宁可误报不可漏报）。
5. **ac-90/ac-92 版本断言动态化的守卫强度变化**：字面值钉（每次升版须手工同步三处 ac 文件，2026-09-25 0.5.1 批实证未同步致红）→ 动态一致性断言（三 JSON version 互等 + 形如 `X.Y.Z`）。代价：「忘记升版」不再有闸——由 T10 任务步骤的逐字文件清单兜底。

## 契约矩阵

| # | 契约 | 定义（逐字/精确值） | 产出任务 | 消费任务 |
|---|---|---|---|---|
| C1 | 桥文件路径 | `<caliber 插件根>/campaign-bridge.json`（源仓 = `F:\workspaces\caliber-suite\caliber\campaign-bridge.json`） | T1 | T2/T8/T9 |
| C2 | 桥 schema v1 | 顶级三键：`bridge_version: 1`（int）、`min_campaign: "0.6.0"`（str）、`entries: [...]`；entry 键：`skill`（str）/ `signal: {paths: [str], keywords: [str]}` / `gate_artifacts: [str]`（支持 `**/` 前缀 glob）/ `brief_obligations: [str]` | T1 | T2/T8/T9 |
| C3 | 桥定位序 | `os.environ["CALIBER_PLUGIN_DIR"]`（若指向含 campaign-bridge.json 的目录）→ `glob(~/.zcode/cli/plugins/cache/caliber-suite/caliber/*/campaign-bridge.json)` 按版本号降序取首 → 返回 `None`（缺席） | T2 | T9（ac-94 态 4） |
| C4 | program.py 新函数签名（共五个） | `def find_bridge():` → `str | None`；`def load_bridge():` → `dict | None`（JSON 损坏 → print WARN 一行 + 返回 None）；`def _unit_seed_text(u):` → `str`（信号匹配种子 = title 原文）；`def bridge_hits(bridge, unit, ws):` → `list[dict]`（signal = paths 任一存在——相对 ws——AND keywords 任一在 `_unit_seed_text(unit)`）；`def _result_path(u):` → `str`（`u.get("result")` 或 `""`） | T2 | T9 |
| C5 | brief 八节序 | `# Unit Brief` → 派生声明注释行 → `## 编排身份`（新增）→ `## 单元目标` → `## SRS 锚点` → `## 前序接口产物` → `## Global Constraints 候选` → `## 工程约定` → `## 验收锚`；总预算 90 行不变 | T2/T3 | T9（ac-94 态 1） |
| C6 | 编排身份节逐字模板 | 见 T2 步骤 ② 代码块（四固定行 + 桥义务行动态追加） | T2 | T3/T9 |
| C7 | gate 桥合并语义 | cmd_gate 内联 gate 循环之后追加：对 `bridge_hits` 命中条目的每个 `gate_artifacts` 路径做 `glob.glob(pattern, recursive=True)`，无命中文件或全空 → `missing.append("bridge:<pattern>")`；桥缺席/损坏 → 跳过不新增 missing（fail-open 对桥、fail-closed 对 artifact） | T2 | T9（ac-94 态 3/4） |
| C8 | F1 步 4 委派文本 | 见 T3 步骤 ② 逐字替换块 | T3 | —（文本契约） |
| C9 | fold_grant meta 键 | `fold_grant: srs_frozen`（可缺省）；编排者仅在「单元 SRS 锚点冻结方案空间 + caliber 原生折叠条件三条件全满足」时折叠方案确认停，逐次记 ledger Ruling | T3 | —（编排纪律） |
| C10 | 版本号集 | campaign plugin = **0.6.0**（plugin.json + marketplace.json + .claude-plugin/marketplace.json + README 两处）；campaign skill metadata = **0.3.0**；program-forge skill = **0.2.0**；spec-forge skill = **0.1.1**；caliber plugin = **1.7.0**（plugin.json + marketplace.json + .claude-plugin/marketplace.json + README 两处 + docs/skills-changelog.md 条目；双 marketplace 逐字节同形）；ui-forge skill = **0.3.0** | T3/T5/T6/T7/T10 | T8/T9（锚引用） |
| C11 | A2 注入格式 | parts 顺序 = handoff.md → `*-resume-note.md` → 在途单元 brief（每份前缀与 T4① 实码逐字同形：`--- .campaign/program/<brief 文件名>（在途单元 brief，A2） ---`——括注为格式后缀，非文件名部分）；尾注 names 行追加对应文件名 | T4 | T9（ac-94 态 5） |
| C12 | ui-forge 契约新句 | 见 T7 步骤 ① 逐字替换块 | T7 | T8（ac-93 check⑥ 源） |
| C13 | ac-93 六 check | ①组件名存在性 ②锚点（工序 N/Step N）存在性 ③禁版本号共现 ④双写句 cmp ⑤hook matcher 名单 ⑥反向闭环（caliber 文本提 campaign 消费点 → 桥必有条目） | T8 | T11（run_all） |
| C14 | ac-94 六态 | 态 1 身份节注入 / 态 2 桥义务注入（信号命中+未命中两分支）/ 态 3 gate 桥合并 fail-closed / 态 4 桥缺席与损坏降级 / 态 5 A2 hook 注入（bash 缺席 → BLOCKED-ENV）/ 态 6 零触碰守卫（本 wave 清单穷举） | T9 | T11（run_all） |
| C15 | ac-90/ac-92 版本断言新形态 | 三 JSON version **两两互等 + 形如 `\d+\.\d+\.\d+`**（不钉字面值）；ac-90 态 2 的 `"0.2.0"` 字面值 → `"0.3.0"` | T10 | T11（run_all） |

## 任务块

### T1 桥文件落盘（caliber 仓）

画像: 性质=配置; 难度=机械; 领域词=[桥文件, campaign-bridge, 跨插件契约, JSON schema]

步骤：
① 新建 `F:\workspaces\caliber-suite\caliber\campaign-bridge.json`，内容逐字：

```json
{
  "bridge_version": 1,
  "min_campaign": "0.6.0",
  "entries": [
    {
      "skill": "ui-forge",
      "signal": {
        "paths": ["docs/designs"],
        "keywords": ["页面", "组件", "视觉还原", "mockup", "hifi", "设计稿"]
      },
      "gate_artifacts": ["**/fidelity-report.md"],
      "brief_obligations": [
        "样式值只能来自 baseline 映射表/token 差集映射表；表内无档时禁止就近取整或自造值——记 FIDELITY-LOG（或并入该仓 DRIFT-LOG）一行待清算，按最近档占位并标注。"
      ]
    }
  ]
}
```

Interfaces：Produces C1/C2。
验证期望：`python -c "import json; d=json.load(open(r'F:\workspaces\caliber-suite\caliber\campaign-bridge.json',encoding='utf-8')); assert d['bridge_version']==1 and d['min_campaign']=='0.6.0' and d['entries'][0]['skill']=='ui-forge' and d['entries'][0]['gate_artifacts']==['**/fidelity-report.md']; print('bridge OK')"` → stdout 逐字 `bridge OK`。

### T2 program.py 桥解释器 + brief 身份节 + KI-11（campaign 仓）

画像: 性质=新增; 难度=集成; 领域词=[program.py, brief 装配, gate 判据合并, 桥解释器, 身份节]

步骤：
① 在 `_lint_cmd` 函数定义之后插入五个函数（C3/C4），代码逐字：

```python
def find_bridge():
    """桥文件定位序（C3）：CALIBER_PLUGIN_DIR → cache 最高版本 → None。"""
    env = os.environ.get("CALIBER_PLUGIN_DIR")
    if env:
        p = os.path.join(env, "campaign-bridge.json")
        if os.path.isfile(p):
            return p
    import glob as _glob
    cands = _glob.glob(os.path.join(os.path.expanduser("~"),
        ".zcode", "cli", "plugins", "cache", "caliber-suite", "caliber",
        "*", "campaign-bridge.json"))
    if not cands:
        return None
    def _ver(p):
        name = os.path.basename(os.path.dirname(p))
        try:
            return tuple(int(x) for x in name.split("."))
        except ValueError:
            return (0,)
    return sorted(cands, key=_ver, reverse=True)[0]


def load_bridge():
    """读桥文件；缺席 → None（静默）；损坏 → WARN 一行 + None（C4）。"""
    p = find_bridge()
    if p is None:
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("WARN: campaign-bridge.json 解析失败，按无桥降级（%s）" % p)
        return None


def _unit_seed_text(u):
    """信号匹配的单元文本种：title 原文（brief 在装配中，种子不含它）。"""
    return str(u.get("title", ""))


def bridge_hits(bridge, unit, ws):
    """命中条目清单：paths 任一存在（ws 相对）AND keywords 任一在种子文本（宁漏勿错）。"""
    if not bridge:
        return []
    out = []
    for e in bridge.get("entries", []):
        sig = e.get("signal", {})
        paths = sig.get("paths", [])
        kws = sig.get("keywords", [])
        p_hit = any(os.path.exists(os.path.join(ws, p)) for p in paths) if paths else False
        k_hit = any(k in _unit_seed_text(unit) for k in kws) if kws else False
        if p_hit and k_hit:
            out.append(e)
    return out


def _result_path(u):
    return str(u.get("result") or "")
```

② cmd_brief 身份节（`prog`/`u` 变量名实证：cmd_brief 首行 `prog = load(args.program)`、次行 `u = prog.unit(args.unit)`，2026-09-26 直读 program.py）：把

```python
    lines = ["# Unit Brief: %s %s" % (u["id"], u.get("title", "")),
             "<!-- 派生文件：program.py brief 重装配时整体重写；改内容请改源（program.yaml / %s），勿手改本文件 -->" % cpath, "",
             "## 单元目标", "", str(u.get("title", "")), "", "## SRS 锚点", ""]
```

替换为（C5/C6；身份节四固定行 + 桥义务行动态追加）：

```python
    gate_list = [str(g) for g in u.get("gate", [])]
    res_disp = _result_path(u) or "（unit 未声明 result 键——gate 必红，先补 program.yaml）"
    lines = ["# Unit Brief: %s %s" % (u["id"], u.get("title", "")),
             "<!-- 派生文件：program.py brief 重装配时整体重写；改内容请改源（program.yaml / %s），勿手改本文件 -->" % cpath, "",
             "## 编排身份", "",
             "- 你在 campaign 程序 %s 的单元 %s 执行中（unit_start 已落账）。" % (prog.meta.get("program", "?"), u["id"]),
             "- 完工还账：写 %s 五行（verdict/结论/证据/实测/ruling），落盘即停手——收账与门由编排者执行。" % res_disp,
             "- 门证据：%s 须存在且非空。" % ("、".join(gate_list) if gate_list else "（本单元 gate 清单为空）"),
             "- 生存包：.campaign/program/%s-resume-note.md（跨会话与 compact 后回接读它）。" % prog.meta.get("program", "program"),
             "", "## 单元目标", "", str(u.get("title", "")), "", "## SRS 锚点", ""]
```

③ cmd_brief 验收锚节追加还账行：在 `lines.append("- 约束符合：产物不得违反「工程约定」节任一条目（审查时逐条引用核对）。")` 之后插入：

```python
    if _result_path(u):
        lines.append("- 还账：产出 %s 五行契约（verdict/结论/证据/实测/ruling）。" % _result_path(u))
```

④ cmd_brief 桥义务注入：② 的 lines 装配代码块之后、写文件之前，插入以下代码（逐字）：

```python
    for e in bridge_hits(load_bridge(), u, os.getcwd()):
        for ob in e.get("brief_obligations", []):
            idx = lines.index("## 单元目标")
            lines.insert(idx - 1, "- 机制义务（桥 %s）：%s" % (e.get("skill", "?"), ob))
```

（`lines.index("## 单元目标")` 定位节界，`idx - 1` = 其前空行位——义务行落在身份节末尾、单元目标节之前，C5 节序不变；多条义务行按序堆叠。）

⑤ cmd_gate 桥合并（C7）：在 `for g in u.get("gate", []):` 循环块之后、`res = ...` 行之前插入：

```python
    _bridge = load_bridge()
    for e in bridge_hits(_bridge, u, os.getcwd()):
        import glob as _glob
        for pat in e.get("gate_artifacts", []):
            found = [p for p in _glob.glob(pat, recursive=True)
                     if os.path.isfile(p) and os.path.getsize(p) > 0]
            if not found:
                missing.append("bridge:%s" % pat)
```

（cwd 契约：桥 glob 相对进程 cwd——编排者自工程根跑 program.py 为既有契约，gate 注入的 CAMPAIGN_WS=os.path.abspath(os.getcwd()) 同源（program.py 实文实证）；ac-94 态 3 以 cwd=tmp 把守。）

⑥ KI-11 消化（G9）：`json.load(open(gpath, encoding="utf-8"))`（cmd_brief doc_graph 段）与 `open(cpath, encoding="utf-8").read()`（约定注入段）两处改 `with open(...) as f:` 形态，行为零变化。

Interfaces：Consumes C1/C2；Produces C3/C4/C5/C6/C7。
验证期望：`python campaign/acceptance/ac-91-brief-conventions.py` → 首行逐字 `PASS ac-91 brief-conventions acceptance (8/8 states)`（身份节不破坏既有八态：态 1-3 无 brief 行数断言、态 8 断言 prog.yaml/stdout/ledger 非 brief）；`python -c "import ast; ast.parse(open(r'campaign/tools/program.py',encoding='utf-8').read()); print('syntax OK')"` → 逐字 `syntax OK`。

### T3 program-forge SKILL.md 委派化重写（campaign 仓）

画像: 性质=文档; 难度=判断; 领域词=[F1 编排循环, K21 契约, 声明定级, fold_grant, SKILL.md 修订]

步骤：
① frontmatter `version: "0.1.1"` → `version: "0.2.0"`。
② F1 步 4 逐字替换（C8）——旧块（逐字，含前导单空格）：

```
 3. 装配        program.py brief --program <p> --unit <id>
                → 输入包 <id>-brief.md（K21 七节），即 caliber 阶段 1 的 CONTEXT
 4. 调 caliber  program.py start --program <p> --unit <id>（落 unit_start）
                按单元形态执行完整 caliber 运行：
                - 判断/集成单元 = ML/L 级（plan-forge 制坯 + 工序 4 彩排 → 执行 → 验证）
                - 修订单元 = plan-review-ritual REVISION 模式（B4）
                - 文档单元 = 主线程 inline 执行 + 独立审查
                caliber 的停止点按 D4 原样触发——编排不得替用户回答
```

新块（逐字）：

```
 3. 装配        program.py brief --program <p> --unit <id>
                → 输入包 <id>-brief.md（K21 八节，含编排身份节）
 4. 调 caliber  program.py start --program <p> --unit <id>（落 unit_start）
                经 Skill 工具按名调用 caliber，任务输入 = 上一步装配的
                <id>-brief.md 全文 + 声明定级（程序作者代理人语义，借
                caliber Step 1「用户一句话改级」通道，caliber 零改动）：
                - 判断/集成单元 → 声明 ML；修订单元 → 直调 plan-review-ritual
                  REVISION 模式（B4，不经六阶段）；文档单元 → 声明 S
                - caliber 按五维复量，只升不降
                此后单元执行 = 一次完整 caliber 运行（Step 0 起全骨架：依赖
                验证、定级、路由装配、六阶段），方案挑战者（阶段 1 双轨）、
                ui-forge 等装备库消费点随 caliber 现行版本自动触发——本
                skill 不持有管线枚举（枚举即化石，2026-09-26 实证）。
                方案确认停的折叠：仅当程序 meta 声明 fold_grant 且 caliber
                原生折叠条件三条件全满足时折叠，逐次记 ledger Ruling——
                编排层不得自建折叠规则（D4）。
                完成判定 = <id>-result.md 五行契约落盘（K21），随后回本
                循环步 5 收账。
```

③ 「输入」节 meta schema 追加 fold_grant：定位锚 = 「多项检查用 wrapper」（实文唯一命中，2026-09-26 复核——注意实文跨行，「wrapper」与「脚本收口」间是换行非空格，勿用长串）——插入点 = 该说明段「脚本收口）。」行之后，追加一行：「可选 `fold_grant: srs_frozen` = 方案确认停折叠预授权（见 F1 步 4）；缺省 = 不折叠。」
④ K21 输入包段三处编辑（锚均实文唯一子串，2026-09-26 复核）：
   a. 「固定七节序」→「固定八节序」；
   b. 节序枚举接缝：实文为跨行连续枚举「…约定文件）→ `## 单元目标` → `## SRS 锚点`…」——在「约定文件）→」与「 `## 单元目标`」之间插入「 `## 编排身份`（程序名/单元 id/还账契约/门证据清单/生存包指针 + 桥机制义务行——全部由 program.py 机械装配）→ 」；插入后该接缝逐字形态为：「约定文件）→ `## 编排身份`（程序名/单元 id/还账契约/门证据清单/生存包指针 + 桥机制义务行——全部由 program.py 机械装配）→ `## 单元目标`」（注意：「约定文件）」是派生声明注释行的行尾括号，与「## 工程约定」节无关——勿误读为节级插入）；
   c. 「## 验收锚」描述句末（「时追加『可执行检查』行）。」行尾）追加「+ 还账行（产出 result 五行契约）」。
⑤ 「与 caliber 的分工」节追加一行：「- 桥消费：cmd_brief/cmd_gate 读 caliber 仓 campaign-bridge.json（定位序 = CALIBER_PLUGIN_DIR 环境变量 → 插件 cache 最高版本目录），命中信号单元的机制义务行进 brief 编排身份节、gate_artifacts 并入门判据；桥缺席/损坏静默降级不阻断（向后兼容）。」

⑥ 宣言句消矛盾（与 F1 步 4 新文本对齐）：文件首部「编排原子单位 = 一个 caliber L 级运行；」→「编排原子单位 = 一次完整 caliber 运行（声明定级与升级规则见 F1 步 4）；」。

Interfaces：Consumes C5/C6/C8/C9/C10。
验证期望：写 `.caliber/tmp-verify-t3.py`（Git Bash 下中文断言落临时脚本，避开 -c 引号陷阱），内容逐字：

```python
t = open(r"campaign/skills/program-forge/SKILL.md", encoding="utf-8").read()
assert 'version: "0.2.0"' in t
assert "固定八节序" in t
assert "## 编排身份" in t
assert "fold_grant" in t
assert "campaign-bridge.json" in t
assert "按单元形态执行完整 caliber 运行" not in t
assert "一个 caliber L 级运行" not in t
assert "编排原子单位 = 一次完整 caliber 运行" in t
assert t.index("## 编排身份") < t.index("## 单元目标", t.index("固定八节序"))
print("T3 OK")
```

跑 `python .caliber/tmp-verify-t3.py` → stdout 逐字 `T3 OK`；脚本留置 .caliber/（gitignored）免清理。

### T4 handoff-inject.sh A2 在途 brief 注入（campaign 仓）

画像: 性质=新增; 难度=集成; 领域词=[SessionStart hook, compact 注入, 在途单元, brief 注入, handoff-inject]

步骤：
① `campaign/hooks/handoff-inject.sh`：把末尾 python 块（`'$PY' -c "..." "$HF_WIN" "$RND_WIN"` 段）整体替换为（C11；插件根自脚本目录推，不依赖环境变量；替换范围 = 自 `"$PY" -c "` 行起至 `"$HF_WIN" "$RND_WIN" 2>/dev/null` 行止，**末行 `exit 0` 保留不动**——G6 契约 exit 恒 0）：

```bash
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOOLS_WIN=$(cygpath -w "$SCRIPT_DIR/../tools" 2>/dev/null || printf '%s' "$SCRIPT_DIR/../tools")

"$PY" -c "
import glob,json,os,sys
hf,rnd,tools=sys.argv[1],sys.argv[2],sys.argv[3]
parts=[]; names=[]
if os.path.isfile(hf):
    try:
        parts.append(open(hf,encoding='utf-8').read())
        names.append('.campaign/handoff.md')
    except Exception:
        pass
for f in sorted(glob.glob(os.path.join(rnd,'*-resume-note.md'))):
    try:
        parts.append('--- .campaign/program/'+os.path.basename(f)+' ---\n'+open(f,encoding='utf-8').read())
        names.append('.campaign/program/'+os.path.basename(f))
    except Exception:
        pass
# A2：在途单元 brief 注入（串行 v1：每程序至多 1 个 in_progress）
sys.path.insert(0, tools)
try:
    import program as _prog
except Exception:
    _prog = None
if _prog is not None:
    for y in sorted(glob.glob(os.path.join(rnd,'*.yaml'))):
        try:
            p = _prog.Program(y)
        except Exception:
            continue
        for u in p.units:
            if u.get('status') != 'in_progress':
                continue
            bp = str(u.get('brief') or os.path.join(rnd, u['id']+'-brief.md'))
            if os.path.isfile(bp):
                try:
                    rel = '.campaign/program/'+os.path.basename(bp)
                    parts.append('--- '+rel+'（在途单元 brief，A2） ---\n'+open(bp,encoding='utf-8').read())
                    names.append(rel)
                except Exception:
                    pass
if not parts:
    raise SystemExit
tail='\n\n> 以上来自 '+ '、'.join(names) +'（campaign 生存包）'
print(json.dumps({'hookSpecificOutput':{'hookEventName':'SessionStart','additionalContext':'\n\n'.join(parts)+tail}},ensure_ascii=False))
" "$HF_WIN" "$RND_WIN" "$TOOLS_WIN" 2>/dev/null
```

（替换要点：argv 由两参变三参；`import program` 复用插件自带解析器，Program 类构造只读解析无副作用——实证：program.py Program.__init__ 仅读文件+_parse。）
② `campaign/hooks/handoff.md` 在注记行「> 更新人：编排者；更新时机：每个停止点与单元边界。hook 只读注入，不改写本文件。」整行之后插入新行（逐字）：`> A2（0.6.0）：SessionStart 同时注入在途单元 brief 全文（status=in_progress 单元），每程序至多 1 个。`
③ `README.md` 第 26 行 hook 表行末「跨会话/压缩不失忆」改为「跨会话/压缩不失忆；0.6.0 起兼注在途单元 brief」。

Interfaces：Consumes C11。验证期望：`"C:/Program Files/Git/bin/bash.exe" -n campaign/hooks/handoff-inject.sh && echo "bash syntax OK"` → 逐字 `bash syntax OK`；`grep -c "在途单元 brief" campaign/hooks/handoff-inject.sh campaign/hooks/handoff.md README.md` → 三行计数 `2:1:1`（依序；handoff-inject.sh 内注释行与代码行各命中一次）；`grep -A1 -F "> 更新人：编排者" campaign/hooks/handoff.md` → 次行逐字 `> A2（0.6.0）：SessionStart 同时注入在途单元 brief 全文（status=in_progress 单元），每程序至多 1 个。`（计数证存在、本锚证位置）。

### T5 campaign SKILL.md Step 0 桥版本软警告（campaign 仓）

画像: 性质=文档; 难度=机械; 领域词=[Step 0 依赖验证, 桥版本核查, min_campaign, SKILL.md 修订]

步骤：
① frontmatter `version: "0.2.0"` → `version: "0.3.0"`。
② 在「输出一行 `✓ 全配` 或 `⚠ 缺 X`（X = 缺席者名）。」行之后插入一段（逐字）：

```
桥版本核查（Q4 软警告，不新增停止点）：定位 caliber 仓 campaign-bridge.json（CALIBER_PLUGIN_DIR 环境变量 → 插件 cache 最高版本目录）；读到且其 min_campaign 与本插件 version 不符 → 追加输出一行 `⚠ 桥版本越界（min_campaign=<值>，本插件=<值>）`；桥缺席或解析失败 → 静默跳过。
```

Interfaces：Consumes C10。验证期望：`python -c "t=open(r'campaign/skills/campaign/SKILL.md',encoding='utf-8').read(); assert '桥版本核查' in t and 'version: \"0.3.0\"' in t and len(t.split(chr(10)))<=100; print('T5 OK')"` → 逐字 `T5 OK`（行数锚 = ac-90 态 1 的 ≤100 行守护；余量实测：现 68 行 +本段 3 行 ≈ 71，2026-09-26 实测）。

### T6 spec-forge 版本化石修复（campaign 仓）

画像: 性质=文档; 难度=机械; 领域词=[版本化石, 禁版本号, spec-forge, 指针浮动]

步骤：
① 第 12 行旧句「骨架与\nplan-forge v1.8.0 四工序同构，替换三个配置件（差异替换表见下）。」（注意原文跨行：「骨架与」在行 11 末）——把子串 `plan-forge v1.8.0 四工序同构` 替换为 `plan-forge 四工序同构（机制指针随 caliber 现行版本浮动，禁钉版本号——化石实证 2026-09-26）`。
② frontmatter `version: "0.1.0"` → `version: "0.1.1"`。

Interfaces：Consumes C10。验证期望：`grep -c "v1\.8\.0" campaign/skills/spec-forge/SKILL.md` → `0`；`grep -c 'version: "0.1.1"' campaign/skills/spec-forge/SKILL.md` → `1`。

### T7 ui-forge 契约改写 + 双写 cmp 验证（caliber 仓）

画像: 性质=文档; 难度=判断; 领域词=[消费点契约, campaign gate, 桥承载, 双写 cmp, ui-forge]

步骤：
① `F:\workspaces\caliber-suite\caliber\skills\ui-forge\SKILL.md` §消费点契约的 campaign gate 定义句逐字替换（C12）——旧句（逐字）：

```
campaign gate 消费点定义：campaign 单元 gate 两判据 = ①`fidelity-report.md` 文件存在且非空 ②单元 lint_cmd 复跑串联 visual-gate.mjs，退出码 1 = gate 红。
```

新句（逐字）：

```
campaign gate 消费点定义：campaign 单元 gate 两判据 = ①`fidelity-report.md` 文件存在且非空（由 caliber 仓 campaign-bridge.json 的 ui-forge 条目经 program.py gate 机械合并承载，信号 = docs/designs 存在 ∧ 单元文本命中 UI 关键词）②单元 lint_cmd 复跑串联 visual-gate.mjs，退出码 1 = gate 红（程序作者通道：lint_cmd wrapper 串联，参数契约见 scripts/visual-gate.mjs 的 USAGE）。
```

② 「与既有 skill 的关系」表 campaign 行替换为：`| campaign | 单元 gate 消费 fidelity-report（两判据见 §消费点契约；判据①经 campaign-bridge.json 机械合并，本 skill 条目为桥首个金样）；本 skill 不进 campaign 编排 |`
③ frontmatter `version: "0.2.0"` → `version: "0.3.0"`。
④ 双写 cmp 验证（不改文本，只验）：UI 信号双写句两侧仍逐字一致（sig 两侧各恰一次逐字同形——2026-09-26 闸口复核：ui-forge §消费点契约 ↔ plan-forge 工序 1 第 6 条）；若验证红（漂移实况）→ 停，上报编排者——双写纪律违规属既有债，不在本批改动面。

Interfaces：Consumes C12/C10。验证期望：写 `.caliber/tmp-verify-t7.py`（Git Bash 双引号内反引号会触发命令替换——sig 含反引号对，禁 -c 单行），内容逐字：

```python
u = open(r"F:\workspaces\caliber-suite\caliber\skills\ui-forge\SKILL.md", encoding="utf-8").read()
p = open(r"F:\workspaces\caliber-suite\caliber\skills\plan-forge\SKILL.md", encoding="utf-8").read()
sig = "UI 信号命中（`docs/designs/` 视觉稿交付物存在 + 任务含页面/组件/视觉还原实现动词）时：选材加跑 ui-forge 视觉基线协议"
assert sig in u and sig in p, "double-write drift"
assert "campaign-bridge.json" in u and 'version: "0.3.0"' in u
print("T7 OK")
```

跑 `python .caliber/tmp-verify-t7.py` → stdout 逐字 `T7 OK`；脚本留置 .caliber/ 免清理。

### T8 ac-93 跨插件引用 lint 新建（campaign 仓）

画像: 性质=新增; 难度=集成; 领域词=[ac-93, 跨插件 lint, 禁版本号, 锚点存在性, 双写 cmp, 静态闸]

步骤：
① 新建 `campaign/acceptance/ac-93-cross-contract.py`，实现 C13 六 check（编码契约 G3/G4；六 check 各实现为带 `scan_root=REPO_ROOT` 缺省参数的函数——fixture 自证态以 `scan_root=<tmp 假树>` 调用，不触碰真实仓）：
- check① 组件名存在性：封闭枚举 = caliber 十 skill（caliber/coding-forge/deep-probe/exec-forge/init-docs/plan-drafting/plan-forge/plan-review-ritual/ui-forge/update-docs）+ 12 agent（自 `CALIBER_ROOT/agents/*.md` 文件名派生，非硬编码清单）；扫描域 = `campaign/skills/`、`campaign/hooks/` 全部 .md/.sh；对扫描文本中出现的每个枚举名，断言 `<CALIBER_ROOT>/skills/<name>/SKILL.md` 或 agents 件存在。CALIBER_ROOT 解析序 = `CALIBER_PLUGIN_DIR` 环境变量 → cache 最高版本目录（`~/.zcode/cli/plugins/cache/caliber-suite/caliber/*/` 按版本号降序取首）；两路皆无 → 首行 `BLOCKED-ENV …`、exit 3。
- check② 锚点存在性：正则 `(plan-forge|deep-probe|plan-review-ritual|plan-drafting|coding-forge|exec-forge|ui-forge)[^\n]{0,40}?(工序\s*\d+(\.\d+)?|Step\s*\d+)` 抽取引用 → 在目标 SKILL.md 全文检索对应「工序 N」「Step N」标题串，缺席即 FAIL（逐条报名。2026-09-26 预扫实证：现网 8 处命中全部锚点存在、零悬空）。
- check③ 禁版本号共现：同一行内 caliber 组件名（= 十 skill 枚举，不含 agent 名——泛词误报面大）与 `v\d+\.\d+` 共现 → FAIL（扫描域同①；预期现状 0 命中——2026-09-26 预扫实证：现网唯一命中 = spec-forge 化石行，T6 先于 T8 消除，任务序保证）。
- check④ 双写 cmp：自 CALIBER_ROOT 读 ui-forge/SKILL.md 与 plan-forge/SKILL.md，提取 UI 信号句（以「UI 信号命中（」起、「进选材产物。」止），两侧各恰 1 次且逐字一致。
- check⑤ hook matcher 名单：spec-context.sh 的 case 行五件（plan-forge/spec-forge/ingest-forge/trans-forge/program-forge）逐一对应 `campaign/skills/<name>/SKILL.md` 存在；caliber 侧组件（plan-forge）查 CALIBER_ROOT。
- check⑥ 反向闭环：CALIBER_ROOT 下全部 skills/*/SKILL.md grep「campaign」命中行含「消费点」或「gate」→ 桥文件 entries 必有该 skill 条目。落地预期：现网仅 ui-forge 命中（2026-09-26 预扫实证：caliber 十 SKILL.md 中 campaign∧(gate|消费点) 命中行仅 ui-forge 三行），桥有条目即绿；未来新命中 = 闸的本职（先补桥条目再写文本），误报处置 = 修正引用文本或补桥条目。
- fixture 自证态：tmp 造 `campaign/skills/fake-x/SKILL.md` 假树（内含 `plan-forge v9.9.9` 共现行）+ 以 `scan_root=<tmp>` 调 check③ → 断言判 FAIL；同假树追加两态——check① 红态（假树引用不存在组件 `nonexistent-skill` → 判 FAIL）、check② 红态（假树引用「工序 99」→ 判 FAIL）（判定方向写反只有红态能证；真实仓扫描域不受影响）。
② 首行总结契约（G4）：全绿 `PASS ac-93 cross-contract (N checks)`。

Interfaces：Consumes C1/C2/C10/C12/C13。验证期望：`CALIBER_PLUGIN_DIR="F:/workspaces/caliber-suite/caliber" python campaign/acceptance/ac-93-cross-contract.py` → 首行前缀 `PASS ac-93 cross-contract`、exit 0（引号 + 正斜杠——Git Bash 未加引号的 env 赋值会吃反斜杠，2026-09-26 实测；开发态显式指源仓——caliber 1.7.0 重装后 cache 有桥，环境变量可免）；`python -c "import ast; ast.parse(open(r'campaign/acceptance/ac-93-cross-contract.py',encoding='utf-8').read()); print('syntax OK')"` → 逐字 `syntax OK`。

### T9 ac-94 桥行为验收新建（campaign 仓）

画像: 性质=新增; 难度=集成; 领域词=[ac-94, 桥合并, 身份节, A2 注入, fail-closed, 零触碰守卫]

步骤：
① 新建 `campaign/acceptance/ac-94-bridge-behavior.py`，实现 C14 六态（编码契约 G3/G4；调 program.py 范式照 ac-91 的 `run_prog`——其无 env 参数，本脚本内自写变体：`env = os.environ.copy(); env.update(逐态覆盖)` 后传入 subprocess，cwd 参数照 ac-91）：
- 态 1 身份节注入：fixture 程序（单单元 U-1，无 lint_cmd）跑 brief → brief 含 `## 编排身份` 恰 1 次、含「你在 campaign 程序 ac-94-fixture 的单元 U-1 执行中」、含「完工还账」、节序 = 编排身份在 单元目标 之前（`text.index("## 编排身份") < text.index("## 单元目标")`）。
- 态 2 桥义务注入两分支：CALIBER_PLUGIN_DIR 指 fixture 桥（ui-forge 条目照 C2 schema 四键齐备：paths=[docs/designs]、keywords=[页面]、brief_obligations 非空、gate_artifacts 非空）；tmp 建 docs/designs/ 且单元 title 含「页面」→ brief 含「机制义务（桥 ui-forge）」且 `text.index("机制义务") < text.index("## 单元目标")`（位置断言：义务行必落在身份节内）；删 docs/designs 后重跑 brief → 不含「机制义务」。
- 态 3 gate 桥合并 fail-closed：信号命中 fixture 下 gate_artifacts=[`**/fidelity-report.md`]；artifact 缺席 → gate exit 1 且 stdout 含 `MISSING` 与 `bridge:**/fidelity-report.md`；落 fidelity-report.md 非空后再跑 → exit 0。
- 态 4 降级两分支：分支 a（无桥）= 子进程 env 设 `CALIBER_PLUGIN_DIR=<tmp 空目录>` 且 `USERPROFILE=<tmp 空 home>`（Windows 实测 2026-09-26：`os.path.expanduser("~")` 跟随 USERPROFILE、不读 HOME；同时写 HOME 兼容 POSIX）→ cache glob 落空，brief/gate 行为同无桥（brief 无「机制义务」、gate 不新增 missing）；分支 b（坏桥）= CALIBER_PLUGIN_DIR 指含坏 JSON 的目录 → stdout 含「WARN: campaign-bridge.json 解析失败」且 gate 不因此 MISSING。
- 态 5 A2 hook 注入：tmp 造 `.campaign/program/prog.yaml`（单元 U-9 status=in_progress、brief 键缺席 → 缺省路径）+ 对应 brief 文件（内容含标记串 `A2-MARKER-9941`）；subprocess 调 `"C:/Program Files/Git/bin/bash.exe" <hook 绝对路径>`（hook 路径自 REPO_ROOT 拼：`os.path.join(REPO_ROOT, "campaign", "hooks", "handoff-inject.sh")`——run_all 以 cwd=acceptance/ 调起，相对路径必炸），stdin 喂 `{"cwd":"<tmp>"}`，env 清掉 ZCODE_PROJECT_DIR/CLAUDE_PROJECT_DIR → 断言 stdout 为单行 JSON 且 additionalContext 含 `A2-MARKER-9941` 与「在途单元 brief，A2」；bash 不存在 → 首行 `BLOCKED-ENV`、exit 3。
- 态 6 零触碰守卫：本态只对 campaign 仓跑 git status --porcelain（caliber 仓改动——T1/T7/T10④/T11⑤——不在守卫范围，ac-92 check6 同款单仓语义）；WAVE_FILES 之外路径数 = 0。事实前提：`.caliber/` 与 `.campaign/` 已在 .gitignore（2026-09-26 实测 .gitignore 前两行），其下产物（tmp-verify 脚本、evidence 文件）不破守卫。WAVE_FILES 逐字清单：`campaign/tools/program.py`、`campaign/skills/program-forge/SKILL.md`、`campaign/skills/campaign/SKILL.md`、`campaign/skills/spec-forge/SKILL.md`、`campaign/hooks/handoff-inject.sh`、`campaign/hooks/handoff.md`、`campaign/acceptance/ac-90-entry-skill-smoke.py`、`campaign/acceptance/ac-92-trans-forge.py`、`campaign/acceptance/ac-93-cross-contract.py`、`campaign/acceptance/ac-94-bridge-behavior.py`、`campaign/.zcode-plugin/plugin.json`、`marketplace.json`、`.claude-plugin/marketplace.json`、`README.md`、`docs/known-issues.md`、`docs/plans/2026-09-26-campaign-caliber-fusion-plan.md`；预存豁免逐字两条：`?? campaign/tools/__pycache__/`、`?? docs/plans/2026-09-23-trans-forge-plan.md`；git 异常/非零退出 → 本态 SKIP 计通过并附降级说明行（同 ac-92 check6 既有语义）。
Interfaces：Consumes C3/C4/C5/C6/C7/C11/C14。验证期望：`python campaign/acceptance/ac-94-bridge-behavior.py` → 首行 `PASS ac-94 bridge-behavior (6/6 states)`、exit 0；syntax OK 锚同 T8。

### T10 版本同步批 + ac 版本断言动态化（双仓）

画像: 性质=配置; 难度=集成; 领域词=[版本同步, plugin.json, marketplace, changelog, ac 断言动态化]

步骤（逐文件，C10/C15）：
① campaign 仓：前置预检（2026-09-26 实测值先行核对，漂移则停并回报）：`grep -c "0\.5\.1" README.md` 现值 = 2（行 5 与行 49，恰为本次两处目标）。然后：`campaign/.zcode-plugin/plugin.json` version → `0.6.0`；`marketplace.json` 与 `.claude-plugin/marketplace.json` version → `0.6.0`（双份一致性以 tmp-verify-t10.py 的 filecmp 断言为权威——Git Bash 无 `fc` 内建，勿用）；`README.md` 行 5「campaign v0.5.1」→「campaign v0.6.0」、行 49 注释 `"version":"0.5.1"` → `"version":"0.6.0"`。tmp-verify-t10.py 以 `F:\workspaces\campaign-suite` 为 cwd 跑（脚本内含相对路径，T11③ 重跑同此 cwd）。
② ac-90：态 2 的 `"0.2.0"` → `"0.3.0"`（docstring 同步）；check4 的 `if v != "0.5.0":` 块改为三 JSON version 两两互等 + `re.fullmatch(r"\d+\.\d+\.\d+", v)`，返回串「三处 version 一致（动态）+ 双份同形 + description 就位」；docstring 第 9 行同步。
③ ac-92：check4 同款动态化（返回串同步），docstring 态 4 描述同步；态 6 的 WAVE_FILES 清单追加逐字一条 `docs/plans/2026-09-26-campaign-caliber-fusion-plan.md`（该清单按路径名匹配、tracked/untracked 均豁免——ac-92 check6 实文语义）。
④ caliber 仓：`caliber/.zcode-plugin/plugin.json` version → `1.7.0`；`marketplace.json` 与 `.claude-plugin/marketplace.json` version → `1.7.0`（双份改完逐字节一致——caliber 仓两 marketplace 同形纪律与 campaign 仓同款，2026-09-26 实测两文件现均 1.6.1）；`README.md` 行 5「caliber v1.6.1」→「caliber v1.7.0」、行 54 注释同步；`docs/skills-changelog.md` 末尾追加两条（caliber 1.7.0：新增 campaign-bridge.json 桥导出物；ui-forge 0.3.0：§消费点契约 campaign gate 判据①改桥承载）。campaign 仓无 skills-changelog.md（2026-09-26 实测缺席）——本批不新建，commit message 承载。
Interfaces：Consumes C10/C15。验证期望：写 `.caliber/tmp-verify-t10.py`，内容逐字：

```python
import json, filecmp
def ver(p):
    d = json.load(open(p, encoding="utf-8"))
    return str(d.get("version") or d["plugins"][0]["version"])
assert ver(r"campaign/.zcode-plugin/plugin.json") == "0.6.0"
assert ver(r"marketplace.json") == "0.6.0"
assert ver(r".claude-plugin/marketplace.json") == "0.6.0"
assert filecmp.cmp(r"marketplace.json", r".claude-plugin/marketplace.json", shallow=False)
cr = open(r"README.md", encoding="utf-8").read()
assert "campaign v0.6.0" in cr and "campaign v0.5.1" not in cr
assert '"version":"0.6.0"' in cr
assert ver(r"F:\workspaces\caliber-suite\caliber\.zcode-plugin\plugin.json") == "1.7.0"
assert ver(r"F:\workspaces\caliber-suite\marketplace.json") == "1.7.0"
assert ver(r"F:\workspaces\caliber-suite\.claude-plugin\marketplace.json") == "1.7.0"
assert filecmp.cmp(r"F:\workspaces\caliber-suite\marketplace.json", r"F:\workspaces\caliber-suite\.claude-plugin\marketplace.json", shallow=False)
kr = open(r"F:\workspaces\caliber-suite\README.md", encoding="utf-8").read()
assert "caliber v1.7.0" in kr and "caliber v1.6.1" not in kr
assert '"version":"1.7.0"' in kr and '"version":"1.6.1"' not in kr
print("versions OK")
```

跑 `python .caliber/tmp-verify-t10.py` → stdout 逐字 `versions OK`；脚本留置 .caliber/ 免清理。

### T11 收口：known-issues + 全量回归 + 终审

画像: 性质=操作; 难度=集成; 领域词=[known-issues, KI-07, run_all 回归, 终审, learnings 登记]

步骤：
① `docs/known-issues.md`：KI-07 状态改「部分消化（2026-09-26 融合批）」——处置记一行「声明定级制落地后单元剂量由 caliber 四档承载（文档单元声明 S），形态下限表封死向下余量为本批裁定形态」；新建 `## KI-16` 节（现档最大编号 KI-15，顺延；形态照既有 KI 条目：现象/来源/处置方向/状态）：「ac-90/ac-92 版本字面值断言 0.5.1 批失同步致红（2026-09-26 基线实证）→ T10 动态化处置」，状态 closed；新建 `## KI-17` 节（closed 消化记，尾注括注为条目正文一部分）：「ui-forge campaign gate 消费点 2026-09-25 声明至 2026-09-26 零消费（AeroFold-ui 四单元 gate 无 fidelity-report、lint_cmd 仅 npm run lint——手工接线必败实证）→ 桥文件机制（T1/T2）承接，本批落地（AeroFold-ui 仓侧 learnings 归 U-M2-08 汇合时消费，不入本批）」。
② deep-probe 判例成文（快照挂起项触发器 = 本批；**次序在 ③ 全量回归之前**——③ 的 caliber 侧产物锚含本步产物）：在 `F:\workspaces\caliber-suite\caliber\skills\deep-probe\references\probe-cases.md` 照既有条目格式追加一判——情境 = 2026-09-26 campaign×caliber 融合设计双轨；错误 = 主轨押注「campaign 侧自建折叠规则（与 SRS 锚点冲突才停）」；机制 = 挑战者以道层 D4（编排层不得折叠停止点）证伪；规则 = 停止点折叠类设计先问折叠权归属——在用户与原生机制，不在新造规则；失效条件 = caliber 原生折叠机制改版。
③ 全量回归：前置确认——T1–T10 全部改动 + 本任务 ①② 的改动已逐任务 commit（**逐任务 commit 节奏：每个任务验证锚转绿后即 commit**；campaign 仓 `git status --porcelain` 输出除两条预存豁免与本 plan 路径外为零；ac-92 态 6 只对已落账世界绿，未 commit 即跑必红）。caliber 仓侧确认（该仓**非 git 仓库**——2026-09-26 闸口实证 `.git` 缺席，git 命令会 fatal，勿跑）：产物锚复跑——以 `F:\workspaces\campaign-suite` 为 cwd 重跑 tmp-verify-t7.py 与 tmp-verify-t10.py 全绿 + probe-cases.md 新条目存在（`grep -c "campaign×caliber 融合设计" F:/workspaces/caliber-suite/caliber/skills/deep-probe/references/probe-cases.md` → ≥1）。然后 `CALIBER_PLUGIN_DIR="F:/workspaces/caliber-suite/caliber" python campaign/acceptance/run_all.py --out .campaign/evidence/ac-run-20260926.txt`（env 随子进程继承，ac-93 定位用；引号 + 正斜杠——Git Bash 未加引号的 env 赋值会吃反斜杠，2026-09-26 实测；重装后免设。附带：env 继承使 ac-91 亦加载真桥——零影响实证：ac-91 fixture 无 docs/designs 且 title「acceptance fixture unit」无 UI 关键词，AND 双条件均不满足）→ 汇总表数据行恰五行（AC-90/91/92/93/94），退出态列全 PASS（另有 3 行表头属正常——run_all.py 输出形态实测；`.campaign/evidence/` 目录由 run_all 自建——os.makedirs exist_ok 实证）。
④ 终审：派 exec-reviewer 对双仓改动做终审（Spec 轴 = 本 plan 与快照四裁定；Standards 轴 = G3/G4 编码契约；两适配：caliber 仓非 git → 以 tmp-verify 产物锚清单替代 diff 基线；spec 源 = 本 plan 文件路径直传——预绑定裁定见技能消费裁定节）。
⑤ 给用户的三行简报 + 重装安排：**两插件的卸载重装排在 aerofold-m2 程序收口之后执行**（Q3「程序收口后切换」裁定的机制落点——重装后 program.py 与 SKILL 新语义全局生效，在途 m2 单元的下一次 brief/gate 会吃到身份节与桥合并；m2 收口前不重装 = 切换点）。若用户要提前享受新机制于其他工程：身份节与桥合并为纯加法变更（不撤除任何既有判据），桥合并仅在 docs/designs ∧ UI 关键词双命中时加判据——此为 Q3 宽松读法，须用户一句话裁定后方可提前重装。
Interfaces：Consumes 全部。验证期望：run_all 输出中 AC-90/91/92/93/94 五行的退出态列全为 `PASS`；终审报告落 `.caliber/exec/2026-09-26-campaign-caliber-fusion-plan/final-review.md`。

## 执行编排预分配表（exec-forge 路径——非代码主导：代码任务 4/11，仓库有 git）

| 任务 | 性质 | 难度 | 形态 | 执行者 | 审查者 | 注入档 | 领域组件（预绑定，工序 4 彩排后裁定回写） |
|---|---|---|---|---|---|---|---|
| T1 | 配置 | 机械 | dispatch | executor → general-purpose | exec-reviewer → general-purpose | 无 | 无（弃用 plugin-creator 候选：无 manifest 动作） |
| T2 | 新增 | 集成 | dispatch | coder → general-purpose | exec-reviewer → general-purpose | 指令化 | 无（弃用 program-forge 候选：cache 副本含待修订旧文，注入即干扰） |
| T3 | 文档 | 判断 | inline | 主线程 | exec-reviewer → general-purpose | N/A | 无（弃用 program-forge/writing-great-skills/campaign 候选：逐字钉死+断言把守，原则性注入只给偏离许可） |
| T4 | 新增 | 集成 | dispatch | coder → general-purpose | exec-reviewer → general-purpose | 指令化 | **diagnosing-hooks**（预绑定，限排障/验证态） |
| T5 | 文档 | 机械 | dispatch | executor → general-purpose | exec-reviewer → general-purpose | 无 | 无（弃用 campaign 候选） |
| T6 | 文档 | 机械 | dispatch | executor → general-purpose | exec-reviewer → general-purpose | 无 | 无 |
| T7 | 文档 | 判断 | inline | 主线程 | exec-reviewer → general-purpose | N/A | 无（弃用 ui-forge/writing-great-skills 候选：修订对象正文在场反而是旧文） |
| T8 | 新增 | 集成 | dispatch | coder → general-purpose | exec-reviewer → general-purpose | 指令化 | 无（弃用 campaign 候选） |
| T9 | 新增 | 集成 | dispatch | coder → general-purpose | exec-reviewer → general-purpose | 指令化 | **diagnosing-hooks**（预绑定，限态 5 注入测试编写与排障） |
| T10 | 配置 | 集成 | dispatch | executor → general-purpose | exec-reviewer → general-purpose | 指令化 | **plugin-creator**（预绑定，限步骤①④：manifest 版本递增 + marketplace 双份同形纪律；不取脚手架/安装流程） |
| T11 | 操作 | 集成 | inline | 主线程 | exec-reviewer → general-purpose | N/A | **code-review**（预绑定，限步骤③终审；两适配：caliber 仓非 git → 以 tmp-verify 产物锚清单替代 diff 基线；spec 源 = 本 plan 文件路径直传） |

## 风险登记

| # | 触发条件 | 爆炸半径 | 可逆性 | 处置 |
|---|---|---|---|---|
| R1 | program.py 改坏（身份节/桥合并回归） | 全部在途程序 brief/gate | git revert 可回 | ac-91 八态 + ac-94 六态双闸；T2 验证锚把守 |
| R2 | hook 5s 超时（多程序 × 慢盘 × Program 解析） | compact 后无注入（静默） | 不阻塞会话 | 现状契约保持（异常静默 exit 0）；双线实证规模 = 2 程序 × ≤90 行，解析为纯文件读，实测远低于 5s；重访触发 = 出现注入缺失实证 |
| R3 | 桥 JSON 损坏 / caliber 未装 | 桥功能整体缺席 | 降级不崩 | ac-94 态 4 两分支把守（WARN + 行为同无桥） |
| R4 | ac-93 引用抽取正则误报（自然语言「工序」类） | 静态闸误红 | 改正则即修 | 模式须组件名共现 + 扫描域限 skills/hooks（排除 docs/acceptance）；误报逐条修模式 |
| R5 | 版本断言动态化后「忘升版」无闸 | 版本描述与用户感知漂移 | — | 接受（字面值闸实证每次升版都失同步；T10 步骤①④为逐字五件清单）；重访触发 = 再出现版本失同步实证 |
| R6 | caliber 1.7.0 未重装而 campaign 0.6.0 先装 | 桥消费静默降级 | 天然向后兼容 | locator 缺席即跳过（C3 末段）；T11 ④ 重装提醒 |
| R7 | 用户环境 Git Bash 路径不同 | ac-94 态 5 BLOCKED-ENV | 降级 | exit 3 归类，不误红（README 行 83 已声明同形态约束） |
| R8 | 本批改动使 ac-92 态 6 在 wave 中途见红 | 回归噪音 | commit 后自绿 | ac-92 态 6 语义 = 「wave 清单外零触碰」，中途红为既有语义（T1–T10 各 commit 后复跑转绿）；T11 ② 为最终判据 |
| R9 | 用户在 m2 收口前重装插件 | 在途 m2 单元吃到新语义（Q3 裁定被架空） | 可逆（卸装回旧版目录） | T11④ 把重装排在 m2 收口后；提前重装须用户显式裁定（Q3 宽松读法） |

## 技能消费裁定节（工序 4 彩排后回写，2026-09-26）

| 任务 | 建议 | 裁定 | 理由 |
|---|---|---|---|
| T1 | 无（弃 plugin-creator 候选） | 采用 | 无 manifest/marketplace/版本动作，能力交集为空 |
| T2 | 无（弃 program-forge 候选） | 采用 | cache 副本含待修订旧文，注入即干扰；双 ac 闸自足 |
| T3 | 无（弃 program-forge/writing-great-skills/campaign 候选） | 采用 | 修订对象正文在场即旧文；原则已固化进逐字新块 |
| T4 | diagnosing-hooks（限排障/验证态） | 采用 | hook 输出严格 schema/timeout 毫秒/手喂样例流程直接覆盖排障面 |
| T5 | 无（弃 campaign 候选） | 采用 | 两处机械编辑 + 锚行已逐字给出 |
| T6 | 无 | 采用 | 本就无候选，全 plan 最干净机械任务 |
| T7 | 无（弃 ui-forge/writing-great-skills 候选） | 采用 | 双写义务已三重机械化（C12+T7④+ac-93 check④） |
| T8 | 无（弃 campaign 候选） | 采用 | 实现参照物全部仓内文件，领域词零命中路由 |
| T9 | diagnosing-hooks（限态 5） | 采用 | stdin JSON 构造/严格 schema 断言/env 清洗的直接依据 |
| T10 | plugin-creator（限①④） | 采用 | 版本递增 + marketplace 双份同形纪律出处；不取脚手架流程 |
| T11 | code-review（限③终审，双适配） | 采用 | 双轴 = plan 终审条款原生形态；适配：caliber 仓非 git 以 tmp-verify 产物锚替代 diff 基线、spec 源 = 本 plan 直传 |

附带修正：routing.yaml 的 campaign-bridge.yaml→json 形态漂移三处已回改（2026-09-26）。

## 停止点与折叠授权记录

- 2026-09-26 用户预授权：路由表确认停 + 后续过程停（除致命性问题外）折叠自主推进——已折叠：Step 1.5 路由表确认停（依据：①授权 ②9 条 route 均为辅料无取舍 ③零不可逆）。
- 阶段 4 入口批量确认停：待阶段 4 开场按同一授权折叠 + 台账 Ruling。
- 剩余必停：与快照/Q1–Q4 裁定冲突的发现；不可逆操作（本批无）。

## 附录：双轨对照表（2026-09-26）

| 类 | 点位 | 挑战案 | 主案 | 裁定 |
|---|---|---|---|---|
| 收敛 | 单元执行去枚举化、委派 caliber 真入口 | A-core | Layer 1 | 采纳（双轨一致，强信号） |
| 收敛 | brief 身份/还账节 | A1（身份+还账+gate 路径+生存包指针） | 补丁 1（另含还账进验收锚） | 收敛，细节合并 |
| 分歧 | compact 重注入粒度 | A2：hook 找 in_progress 单元注入其 brief 全文（覆盖 pre-K22 程序） | 补丁 2：resume note 挂事件自动写 | 采纳 A2；补丁 2 删除测试不过（F1 位置可从文件派生），降级挂起 |
| 分歧 | 消费点接线形态 | A4：caliber 仓机器可读桥文件 + program.py 通用解释（同仓同提交，lint 闭环） | Layer 2①：campaign 侧手工双写消费点节 | 采纳 A4——手工双写即 AeroFold-ui gate 空转的失败模式本身 |
| 收敛 | 跨插件 lint | A3（封闭枚举+锚点存在+禁版本号+双写 cmp+反向闭环，挂发布闸） | ac-93（同形态，粒度粗） | 收敛，以挑战案细目为准 |
| 分歧 | 单元级阶段 1 剂量 | C4：campaign 不得自建折叠规则 | Q2 原押注：锚点冲突才停 | 主案被证伪（违 D4）；用户裁定原生折叠+预授权 |
| 分歧→用户覆盖 | 在途迁移姿态 | C6：约定钉创建时、机制浮新作，单元边界切换 | Q3 押注：单元边界 | 用户裁定**程序收口后切换**（保守档） |
| 借鉴 | 「不信任编排者」兜底 | 方案 B 内核 → A4 gate 判据合并吸收 | 主案无此件 | 借鉴；B 本体否决（事后把关 + 无落盘产物的机制够不着） |
| 借鉴 | 版本 WARN | A5 删除测试 → 折进 A3/Step 0 一行 | Q4 押注（软 lint+警告） | 收敛且更简，采纳折叠形态 |

**挑战者实证（仓库直读）**：①spec-forge 第 12 行声称「与 plan-forge v1.8.0 同构」而 plan-forge 已 1.9.1——文本漂移现形；②aerofold-ui.yaml 的 lint_cmd 仅 `npm run lint`、四单元 gate 无 fidelity-report、全仓无 baseline.json——ui-forge campaign 消费点从未被消费；③program-forge 第 11 行宣言与步 4 枚举句同文件自相矛盾；④aerofold-m2 为 pre-K22 程序（无 resume-note），U-M2-08 brief 系手写。

**被否决路线**：两插件合并（入口触发面污染 / 成熟度错配 1.6.1 vs 0.5.1 / 不治本只缩半径 / 存在只要引擎的用户场景）；接口反转（caliber 直读 program.yaml——依赖方向倒置）；版本钉死 caliber_pin（把冻结从 bug 升格为 feature，与目标①正面相反）。

---

总结行（2026-09-26 工序 4 收口）：发现数 = 轮 1（自审 3 + 声部A 13 + 声部B 11）+ 轮 2（A 5 + B 7）+ 轮 3（A 3 + B 4）+ 闸口 3 + 彩排 Phase 1 困惑点位 6 大类（全部回工序 2 补全）；分类分布 = 全量 Mechanical（零 Taste 上门、零 User Challenge）；收敛轮次 = 3（轮 3 收敛；生产文本层涟漪 = R1 两件 [C4 签名/C10 常量集]、R2 一件 [C11 措辞]，轮 3/闸口/彩排修复零涟漪）；技能消费裁定数 = 11（预绑定 3：T4/T9→diagnosing-hooks 限域、T10→plugin-creator 限①④、T11→code-review 限③带双适配；其余弃用候选全留痕）；未决项 = NO UNRESOLVED。审计文件 = .caliber/review-logs/2026-09-26-campaign-caliber-fusion-plan.md。
