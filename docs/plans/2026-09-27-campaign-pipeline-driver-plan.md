# campaign 流水线驱动者改造 plan（L 级，目标版本 0.6.5）

> 审计与轮次记录：`.caliber/review-logs/2026-09-27-campaign-pipeline-driver.md`（锻打期装配）。

## 对齐快照

**目标重推**：把 campaign 从「分诊后断链的路由器」改造为「流水线驱动者」——多环任务先对齐、立 charter、按产物状态回路接力推进；program-forge 以 rolling DAG 承接开放性任务的渐进细化；单元执行层原样委托 caliber。刚性只留目标态/不可逆/已裁定项，路径与剂量全程可复量、可折叠。

**道层条款**（四轮裁定，逐条可溯）：
1. 先对齐（deep-probe 式）后立案，charter 从对齐快照起建，不重复审讯已确认项；
2. 不加人格层；
3. 判例回流进流水线层（`pipeline-cases.md`，五要素 + 四类触发 + 压缩阈值 ~20 条）；
4. 单环任务免立案直走 forge；
5. 折叠三条件适用于两处：charter 复量 / rolling DAG 细化（program.py 三子命令 `--ruling` 参数承载）；「单元批量派遣」不折叠——该停止点归 caliber 阶段 4 入口既有机制，campaign 不复制（D4 边界）；
6. 锚点泛化（meta 声明 anchor source，立项门 = 锚点可解析 ≠ 必须 SRS）；
7. 复量双机械触发器：前提被证伪 / 就绪条件反复不满足；
8. 单元执行形态全权委托 caliber §动态组合，campaign 不造第二套引擎；
9. 不搬 caliber 两机制：routing.yaml 装配表、双声部对抗审查；
10. resume note 复用既有形态，只加「charter 道状态」一节。

**开放决策点 + 选定记录**：
- charter schema 节数 → **选定六节**（对齐快照指针 / 目标态 / 前提清单 / 初始路径 / 弹性点 / 复量记录），见契约 C2；
- `planning: rolling` × `fold_grant` 交互 → **选定：允许共存但默认不声明**——fold_grant 是单元级方案确认停折叠、rolling 是 DAG 级细化折叠，两者正交不互斥；rolling 程序声明 fold_grant 合法但 lint 输出 WARN 一行提醒（双重折叠需程序作者自知），见契约 C5/T3；
- 下游三 forge 加「出口证齐 → 回调 campaign」一行 → **选定：加**（用户 2026-09-27 裁定），行内注明「经 campaign 入口进入时」。

**挂起项（带触发器）**：
- KI-04（advance 单原语）不消化——状态回路是文本层纪律；触发 = 状态回路实测后证明文本纪律失效；
- KI-06 半侧（hook 未激活可发现性提示）不消化；触发 = 用户报告「不知道插件没激活」实证。

**前提清单**（每条 = 可攻击假设）：
- P1：状态回路用文本纪律（SKILL.md 指令）即可闭环，不需要 program.py 新子命令承载；
- P2：迷你 YAML parser 子集（键名 [A-Za-z_]、inline list 仅 depends/gate、禁注释）可容纳 rolling 全部新键，无需扩 parser 语法；
- P3：bridge 与 rolling 零耦合（bridge 只消费单元 title/gate_artifacts，不碰 status 枚举）；
- P4：下游 forge 一行回调条款足以闭环，不需要 forge 侧状态机；
- P5：版本号集动态化后 ac-90/92 不再随升版失同步（KI-16 同族根因拔除）。

## Global Constraints

- C-D1：状态只认落盘文件；C-D2：程序层只编排不实现；C-D3：门证据齐才迁移；C-D4：不折叠 caliber 停止点（编排层不得自建折叠规则——本 plan 的折叠三条件全部落在 campaign 编排层停止点上，不碰 caliber 内部停止点）；
- C-K21：brief/result 契约行数预算不动（90/15 行）；
- C-向后兼容：非 rolling 程序（无 `planning:` 键）行为逐字节不变（ac-91 态 8 守护面延伸）；
- C-parser：新键全部落迷你 YAML 子集，parser 语法零扩展；
- C-行数顶：campaign 主 SKILL.md 重写后全文 ≤100 行（ac-90 check1 / ac-92 check2 双守卫钉死，实测 ac-90 check1 断言「行数 <= 100」、ac-92 check2 同顶）——T1 新增五节（Step 1.5/1.6/1.7/复量/判例指针）必须在这个预算内写完，写不进就压缩措辞，不许调守卫；
- C-验收守卫预处置（碰撞预扫，声部 A 轮 1 P1#2）：本批全部改动撞三重零触碰守卫——① ac-90 check6 对三 forge/hooks/tools 跑 `git diff HEAD`（脏树即 BAD）；② ac-92 check6 / ac-94 check6 用 `git status --porcelain` + WAVE_FILES 白名单（本批新件 ac-95、pipeline-cases.md、plan 文档本体均不在列）。处置 = **先提后验**：T1~T8 全部任务执行期间不跑 ac-90/92/94 单件（验证锚中涉及这三件的条目统一推迟到 T9 终验）；T9 先更新 ac-92/ac-94 的 WAVE_FILES 白名单收编本批清单，再 commit 全部改动（含 plan 文档与台账），porcelain 干净后跑 run_all 全量。

## Review Focus

1. **rolling 的 status 写回路径**：sketch→pending 细化若走 `write_scalar_line` 会改 yaml 文件——必须确认该写回与「行级保留式写回（仅 status:/last_reconciled: 行）」既有契约不冲突，且 sketch 单元**新增/删除**（不止改 status）时的文件完整性（→ T3 验证锚）；
2. **eligible 对 sketch 的排除**：`eligible()` 只认 `status=="pending"`——sketch 天然被排除（无码改），但 `cmd_start` 对 sketch 单元的拒绝路径必须显式报错文案而非静默（→ T3）；
3. **handoff-inject.sh 注入体积**：charter 注入追加后 SessionStart additionalContext 膨胀——单 charter ≤40 行硬顶（对齐 resume note 体积纪律），超限截断（→ T4）；
4. **description 信号清单漂移**：campaign 主 skill description 是 AGENTS.md 全局权威——路由语义从「分诊」变「驱动」后 description 必须重写，且 ac-90 check2 六子串断言可能失同步（→ T1/T5 双向核对）。

## 契约矩阵

| ID | 契约 | 定义点 | 消费点 |
|---|---|---|---|
| C1 | unit.status 枚举五态：`pending / sketch / in_progress / complete / blocked`（sketch 插入第二位）；**sketch 单元显式声明 `status: sketch`**——四键形态（id/title/status: sketch/depends，depends 可 `[]`），不存在「无 status 键的 sketch」（parser 缺键三路径全炸：cmd_status 打 None / cmd_start KeyError / lint bad status None——2026-09-28 闸口实测） | program.py `STATUS_ENUM` 元组（块：文件顶部常量区） | T3 改；ac-91/ac-94 fixture 引用（兼容：四旧态不变）；program-forge SKILL.md schema 节 |
| C2 | charter 文件六节序（固定）：`# Pipeline Charter: <name>` → `## 对齐快照指针` → `## 目标态` → `## 前提清单` → `## 初始路径` → `## 弹性点` → `## 复量记录`；路径 `.campaign/pipeline/<name>.md`；全文 ≤40 行 | campaign SKILL.md 新「流水线驱动」节 | T1 写；T4 hook 注入面；pipeline-cases.md 判例引用 |
| C3 | meta 新键二枚：`planning: rolling`（缺省 = 非 rolling）、`anchor: <注册表路径>`（缺省 = SRS/doc_graph 现状）；均落 parser 顶级键 regex `^([A-Za-z_]+):\s*(.*)$` | program.py `_parse`（无码改——regex 天然容纳新键，lint 不校验未知 meta 键，实证：`_parse` 对顶级键无白名单） | T3 消费（`prog.meta.get("planning")`）；program-forge SKILL.md schema 节 |
| C4 | sketch 细化写回形态：refine = 合并语义（现有键为底、fields 覆盖、status 强制 pending；title/gate/result 缺一即报错清单；depends 缺省继承；brief 缺省写占位 `-`），整块重写七键序，不走 `write_scalar_line`；新增 sketch 单元 = 文件尾 append 块；删除 sketch 单元 = 整块剔除。三操作均原子落盘（tmp + os.replace）且记 ledger `ruling` 事件，detail 含折叠三条件核对文本 | program.py 新函数 `refine_unit(prog, uid, fields)` / `add_sketch(prog, fields)` / `drop_sketch(prog, uid)` + `_atomic_save(prog)`（块：`cmd_reconcile` 后插入） | T3 实现；program-forge SKILL.md rolling 节；ac-95 验收 |
| C5 | rolling × fold_grant 交互：lint 增加一条 WARN——`planning==rolling and fold_grant in meta` → `WARN: rolling 程序声明 fold_grant，双重折叠叠加需程序作者自知`；不阻断 | program.py `lint()`（块：K6 WARN 段后追加） | T3 实现；ac-95 态 |
| C6 | 下游 forge 回调行（三 forge 各一行，逐字）：`经 campaign 入口进入时：出口证齐后经 Skill 工具调用 campaign 推进流水线回路；独立使用忽略本行。` 落点 = 各 forge 出口门节末尾 | ingest-forge「第五步：出口门」节末 / trans-forge「工序 5 — 出口门三证」节末 / spec-forge 出口节末 | T2 写三件；ac-95 静态锚 |
| C7 | hook 注入面扩展：handoff-inject.sh 在 resume-note 枚举段后追加 `.campaign/pipeline/*.md` 枚举（同 `sorted(glob.glob(...))` 形态），单件 >40 行截断（末行 `…（charter 超预算截断）`）；parts 前缀 `--- .campaign/pipeline/<base>（流水线 charter） ---`；names 记 `.campaign/pipeline/<base>`，**`<base>` = `os.path.basename(f)` 含 .md 扩展名**（与 resume-note 段同形） | handoff-inject.sh（块：resume-note glob 段后、A2 段前） | T4 实现；ac-95 态（注入行为由 ac-95 补态或 T4 验证锚直验，见 T4） |
| C8 | KI-18 修复：handoff-inject.sh A2 段 brief 路径解析 `bp = str(u.get('brief') or os.path.join(rnd, u['id']+'-brief.md'))` → 相对形态先 `os.path.join(rnd, bp)` 再 isfile（rnd 优先回退） | handoff-inject.sh A2 段 | T4 实现；ac-94 态 5 补分支 |
| C9 | 版本号集：插件版四件 = `marketplace.json` / `.claude-plugin/marketplace.json` / `campaign/.zcode-plugin/plugin.json` + `README.md`（L5/L26/L49 三锚）→ `0.6.5`；skill 版五件 = campaign `0.3.0→0.4.0`、program-forge `0.2.0→0.3.0`、ingest-forge `0.1.0→0.1.1`、trans-forge `0.1.1→0.1.2`、spec-forge `0.1.1→0.1.2`（实测现值 2026-09-27） | 九件文件 | T5 实现；ac-90/92 check4 动态断言守护（已动态化，实证 L163/L160） |
| C10 | ac-90 check2 动态化：`_metadata_block` 内字面值 `0.3.0` → `re.search(r'version:\s*"(\d+\.\d+\.\d+)"', md)` 形态断言（与 check4 同款）；`campaign-w6` source 锚保留字面值 | ac-90-entry-skill-smoke.py `check2()` | T5 实现 |

## 任务块

### T1 — campaign 主 skill 重写：前置对齐 + charter + 状态回路
画像: 性质=文档; 难度=判断; 领域词=[SKILL.md, 状态回路, pipeline charter, 前置对齐]

步骤：
1. 读 `campaign/skills/campaign/SKILL.md` 全文（70 行现状）。
2. frontmatter：`version: "0.3.0"` → `"0.4.0"`；`source: campaign-w6` 保留；description **除尾部追加一句外逐字不动**（五域信号清单与「Not for…caliber」尾句原文保留——ac-90 check2 六子串守护，实测六子串为 program/ingest/SRS/.campaign/Not for/caliber）；尾部追加：`多环任务（≥2 forge 或含 program 环）进流水线驱动模式：先对齐、立 charter、按产物状态回路接力推进。`
3. 正文结构改造（**全文 ≤100 行硬顶**，C-行数顶；现 70 行 → 净增预算 30 行，**节间空行与 Step 2 保留两行（宣布格式行+「此后不再判」句）计入预算**——Step 2 的 ≤8 行额度含该两行；各节预算含标题行与节前后空行，顶格时压缩优先级：措辞 > 例子 > 空行。保留：**H1 标题行**（含「分诊，不治病」——ac-90 _ONCE 锚）、Step 0 依赖验证原样、Step 1 域判定五分支原文、辅助信号段、歧义段、宣布格式行「域判定 <域名>，理由：<命中的信号原文>」与「此后不再判」句（ac-90 check3 三锚）、域地图表、停止点速查、与 caliber 分工节、**文末「AGENTS.md 全局路由规则的信号清单以本 skill 的 description 为权威。」行**（ac-90 _ONCE 锚）——未声明改写处逐节保留）：
   - **新增节标题级别钉死**：Step 1.5/1.6/1.7/复量节/判例指针节均为 `## ` 二级标题（计入 `grep -c "^## "` ≥8 锚）；
   - Step 1 后新增 **Step 1.5 — 环数门控**（≤4 行）：宣布域判定后判环数——命中单一 forge 且非复合任务 → 直走 forge（现状路由路径）；复合任务（顺序规则已覆盖两类 = Step 1 歧义段既有两类：「收编后接产 SRS」与「转化后接收编」）或用户明示多环目标 → 进 Step 1.6；
   - 新增 **Step 1.6 — 前置对齐**（≤5 行；deep-probe 式行为参照，**注意行内不得出现 `Step N`/`工序 N`/`vX.Y` 字样与组件名近距共现**——ac-93 check②③ 扫描域为 campaign/skills/** 全部 .md，写作约束：提 deep-probe 时单独成行或不与编号字样同行）：一句话重推目标 → 指出 1-2 个最大不确定性 → 押注提案藏问；产物 = 对齐快照（目标一句话/已确认取舍/开放决策点）；半成形方案入场 → 先审计视角；快照上用户裁定（停点）；
   - 新增 **Step 1.7 — 流水线立案**（≤5 行）：按 C2 六节写 `.campaign/pipeline/<name>.md`（≤40 行），前提清单每条 = 可攻击假设；立案上用户裁定一次（停点，此后回路自动推进不再逐环请示）；`.campaign/` 首次创建 gitignore 条款复用 program-forge 输入节同款；
   - Step 2 标题改为逐字 `## Step 2 — 状态回路`（双兼容：ac-90 check3 的 `## Step 2` 前缀 + ac-95 态 5 的「状态回路」子串），内容改写为 LOOP 五步（≤8 行）：盘点产物（机械：`ls -d adr docs/spec .campaign 2>/dev/null` + `.campaign/` 下工件清单）→ 对照 charter 目标态：满足 → 收口 → 选下一 forge（就绪条件匹配；多环就绪或皆不就绪 → 推荐+依据，停，用户一句话）→ 经 Skill 工具调用 forge → 出口证齐回圈；**保留**宣布格式行与「此后不再判」句于 LOOP 前；
   - 新增 **复量节**（≤5 行）：双触发器（前提被证伪 / 就绪条件反复不满足）→ 宣布 charter 升/降级 + 补差额 + 记 charter `## 复量记录` 节；折叠三条件（①用户消息含明确执行授权 ②无取舍待决 ③无新增不可逆操作）全满足 → 可不停，一行依据 + 复量记录节留痕；
   - 新增 **判例回流指针节**（≤3 行）：`references/pipeline-cases.md` 五步（触发四类/即时登记/成文五要素/分辨率裁决/压缩 ~20 条），无沉淀的使用是浪费。
4. 停止点速查追加三枚：③ 对齐快照裁定 ④ charter 立案裁定 ⑤ 复量越界（折叠条件不满足时）。

验证期望：
- `wc -l campaign/skills/campaign/SKILL.md` ≤ 100（C-行数顶硬锚）；
- `grep -c "^## " campaign/skills/campaign/SKILL.md` 输出 ≥ 8；
- `grep -c "pipeline-cases.md" campaign/skills/campaign/SKILL.md` = 1（指针式引用，防自嵌）；
- `grep -c "0.4.0" campaign/skills/campaign/SKILL.md` = 1；
- `grep -c "^## Step 2 — 状态回路" campaign/skills/campaign/SKILL.md` = 1；
- `grep -c "此后不再判" campaign/skills/campaign/SKILL.md` = 1；
- description 六子串复核：`python -c "import re; fm=open('campaign/skills/campaign/SKILL.md',encoding='utf-8').read().split('---')[1]; d=[l for l in fm.split(chr(10)) if l.strip().startswith('description:')][0]; print(all(s in d for s in ('program','ingest','SRS','.campaign','Not for','caliber')))"` 输出 `True`（独立调用，不链管道）。

### T2 — 下游三 forge 回调行 + 微升版
画像: 性质=文档; 难度=机械; 领域词=[ingest-forge, trans-forge, spec-forge, 回调行, C6]

步骤：
1. 三件各在出口门节末尾追加 C6 逐字行：
   - `campaign/skills/ingest-forge/SKILL.md`：「第五步：出口门」节（锚：`## 第五步：出口门` 标题行起至下一同级标题前）末尾追加；
   - `campaign/skills/trans-forge/SKILL.md`：「工序 5 — 出口门三证」节（锚同上形态）末尾追加；
   - `campaign/skills/spec-forge/SKILL.md`：无独立出口节——落点 = 「## 工序 4 — 成型」节（最末工艺节，锚：该标题行起至 `## 与 ingest-forge 的分工` 前）末尾追加；
2. 三件 frontmatter version 各 +0.0.1（实测现值 2026-09-27：ingest-forge `0.1.0→0.1.1`、trans-forge `0.1.1→0.1.2`、spec-forge `0.1.1→0.1.2`；均位于各件 metadata 块 version 行）。

验证期望：
- 三件各 `grep -c "经 campaign 入口进入时" <path>` = 1；
- 三件 `grep -n 'version: "0\.' <path> | wc -l` = 1 且数值为原值 +0.0.1。

### T3 — program.py rolling 支持 + ac-91/94 兼容核查
画像: 性质=新增; 难度=集成; 领域词=[program.py, STATUS_ENUM, sketch, refine_unit, lint WARN]

步骤：
0. **基线固化（先于一切码改动）**：工序两段式——(i) 先落 ac-95 全部 fixture（态 1-4 的 rolling/非 rolling yaml + gate/result 证据占位文件：status 四旧态与 sketch 按 C1、title 自定、gate/result 路径自定，占位文件以非空内容创建）；(ii) 用批前 commit 的 program.py 对 fixture 跑基线——`git show HEAD:campaign/tools/program.py > .caliber/tmp-program-baseline.py`（执行时 HEAD 即批前 commit；若执行顺序调整致 HEAD 已含本批改动，则用首个不含本批的祖先 commit），对 ac-95 兼容守护态 fixture（fixture 由本任务态 1-4 创建时先行落盘）跑 `validate`/`status`/`next`，输出串写入 `campaign/acceptance/ac-95-pipeline-driver.py` 顶部常量 `BASELINE_VALIDATE` / `BASELINE_STATUS` / `BASELINE_NEXT`（ledger ts 字段不参与比对——ac-91 态 8 同例）。**ac-95 文件与态 1-4/兼容守护态断言由本任务创建**（先测后码：先写断言跑出红，再实现）；T8 仅补态 5 静态锚与终验集成。

   **ac-95 态规格（本任务创建态 1-4 + 兼容守护态，T8 补态 5）**：
   - 态 1（rolling 排除）：fixture = `planning: rolling` + 1 sketch 单元（u-sketch，id/title/status: sketch/depends 四键）+ 1 pending 无依赖单元（u-a）→ `status` stdout 含 u-sketch 行且其 status 列 = sketch；`next` stdout = `u-a`（≠ u-sketch）；`start --unit u-sketch` exit≠0 且输出含「须先细化」；
   - 态 2（refine 合并语义）：`refine --unit u-sketch --field title:<新标题> --field gate:[<g1路径>] --field result:<r路径> --ruling "三条件核对:授权✓无待决✓无不可逆✓"` → exit 0 且 stdout 含 `refine: u-sketch sketch -> pending`；yaml 该单元七键齐、status=pending、title/gate/result 为新值、depends 继承；**ledger 含 ruling 事件且 detail 含核对文本**（C4 消费点兜底）；随后 `start --unit u-sketch` exit 0（cmd_start 只验 status/eligible 不查 gate 证据——gate 证据归 cmd_gate；断言仅 start 的状态迁移与 ledger unit_start）；
   - 态 3（add/drop 往返）：`add-sketch --field id:u-b --field title:<标题> --ruling "<核对文本>"` → exit 0 含 `add-sketch: u-b`，`status` 含 u-b sketch 行；`drop-sketch --unit u-b --ruling "<核对文本>"` → exit 0 含 `drop-sketch: u-b`，`status` 不再含 u-b；`drop-sketch --unit u-a`（pending 非 sketch）→ exit≠0 含「非 sketch」；
   - 态 4（C5 WARN 双向）：rolling + fold_grant fixture → `validate` stdout 含「双重折叠」WARN 且 exit 0；非 rolling + fold_grant fixture → `validate` stdout 无「双重折叠」WARN；
   - 兼容守护态：非 rolling fixture 的 `validate`/`status`/`next` 输出 == BASELINE 三常量（逐字节，ledger ts 除外）。
1. `STATUS_ENUM = ("pending", "in_progress", "complete", "blocked")` → `("pending", "sketch", "in_progress", "complete", "blocked")`；
2. `cmd_start` 在 `if u["status"] != "pending":` 拒绝分支前加显式 sketch 文案：status==sketch → `sys.exit("%s: sketch 单元须先细化（refine）为 pending 才可 start" % u["id"])`；
3. 新增三函数（插入点：`cmd_reconcile` 函数定义结束后、`cmd_impact` 前）。**原子落盘**：三函数写文件一律走「tmp 文件 + `os.replace`」（`save()` 现状为整文件覆盖写，进程中途被杀会截断 program.yaml 且 `.campaign/` 通常 gitignore 无 git 兜底——实现一个 `_atomic_save(prog)`：写到 `path + ".tmp"` 后 `os.replace(tmp, prog.path)`；不改既有 `save()` 调用点的行为面，仅三新函数消费）；**每函数末尾重新解析**：函数末 `prog2 = load(prog.path)` 并在 docstring 注明「调用方在写后须重新 load，`_idx` 行号已失效」：
   - `refine_unit(prog, uid, fields)`：**合并语义**——以单元现有键为底、fields 覆盖、status 强制 pending；合并后七键（id/title/status/depends/gate/brief/result）中 title/gate/result 缺一即 exit 报错清单（`refine: <uid> 缺键: <列表>`；**`--field` 切分后 v 为空串视同缺键**，`--field gate:` 不得绕过必填），depends 缺省继承现值或 `[]`，brief 缺省写 `-`（占位标量，语义 = 未声明——**与 lint_cmd 的 `-` 同款**；消费侧联动见步 3.5）；定位 units 块行区间（`_idx` 记录的首行到下一 `- id:` 前或文件尾），整块重写为七键序（id/title/status/depends/gate/brief/result），`_atomic_save`；ledger_append `ruling` detail=`refine <uid>: sketch->pending, 折叠三条件核对=<ruling 参数文本>`；
   - `add_sketch(prog, fields)`：必填 id/title，缺即报错；文件尾 append `  - id:` 起 sketch 块（status: sketch；depends/gate 缺省 `[]`；brief/result 缺省 `-`）；`_atomic_save`；ledger 同形态；
   - `drop_sketch(prog, uid)`：status!=sketch → exit 报错（`drop-sketch: <uid> status=<值> 非 sketch`）；整块剔除（行区间同 refine 定位）；`_atomic_save`；ledger 同形态；
3.5. **cmd_brief/result 占位联动**（防 `-` 劫持，2026-09-28 彩排实证：`out = str(u.get("brief") or …)` 对 `brief: -` 会写到名为 `-` 的文件）：`cmd_brief` 的 out 行改为「bp = u.get('brief')；bp 为 None/空串/`-` → out = .campaign/program/<id>-brief.md 缺省路径，否则 out = str(bp)」；`_result_path(u)` 同款联动（`-` → 返回空串，gate 的 result 检查与身份节还账行按未声明处理）；ac-95 态 2 补一断言：refine 未传 brief（缺省 `-`）后跑 `brief --unit <uid>` 落盘路径为 `.campaign/program/<uid>-brief.md` 而非 `-`；
   - 三函数各挂子命令 `refine` / `add-sketch` / `drop-sketch`（`main()` 内 base() 形态）：参数 `--unit`（refine/drop 必填；add-sketch 用 `--field id:...` 不带 --unit）、`--field` 可重复 `k:v` 串（按首个 `:` 切分键与值；depends/gate 两键的值按 inline list 解析——去方括号后按 `,` 切分逐项 strip，空串 `[]` → 空 list；其余键按标量）、`--ruling` 必填折叠核对文本、`--ledger`（与 start 同形态 `sp.add_argument("--ledger")`）；
4. `lint()` K6 WARN 段后追加 C5 WARN（`str(prog.meta.get("planning")) == "rolling"` 且 `"fold_grant" in prog.meta` → `WARN: rolling 程序声明 fold_grant，双重折叠叠加需程序作者自知`）；
5. 兼容核查：`grep -n "status" campaign/acceptance/ac-91-brief-conventions.py campaign/acceptance/ac-94-bridge-behavior.py`——fixture yaml 的 status 值清单与四旧态比对，确认无 sketch 引用（有则该 fixture 不动、新行为由 ac-95 覆盖）。**ac-94 单件在本任务后不跑**（脏树必红，统一推迟 T9）；ac-91 无 git 守卫、可跑可不跑，随批保守推迟。

Interfaces：
- Consumes：C1/C3/C4/C5；
- Produces：program.py 五态枚举 + 三子命令 + C5 WARN；子命令 stdout 形态：`refine: <uid> sketch -> pending` / `add-sketch: <uid>` / `drop-sketch: <uid>`（单行；ac-95 态 2/态 3 断言这三串子串）。

验证期望：
- ac-95 兼容守护态：`python campaign/acceptance/ac-95-pipeline-driver.py` 该态断言新代码输出 == BASELINE 常量（逐字节，ledger ts 除外）；
- `python campaign/tools/program.py status --program <rolling fixture>` 含 sketch 单元行且 eligible 不含 sketch id；
- `python campaign/tools/program.py start --program <rolling fixture> --unit <sketch id>` exit≠0 且输出含「须先细化」。

### T4 — handoff-inject.sh：charter 注入 + KI-18 修复
画像: 性质=新增; 难度=集成; 领域词=[handoff-inject.sh, charter 注入, KI-18, SessionStart]

步骤：
1. KI-18 修复（C8）：A2 段 `bp = str(u.get('brief') or os.path.join(rnd, u['id']+'-brief.md'))` 行改为：`bp = str(u.get('brief') or ''); bp = bp if os.path.isabs(bp) else os.path.join(rnd, bp or (u['id']+'-brief.md'))`——相对键一律 rnd 回退（注释行同步改写：头注释补一句「相对 brief 键按程序目录解析（KI-18）」；注：yaml 键写 MSYS 绝对形态 `/f/...` 时 Windows ntpath 的 isabs 判 True 但 open 可能失败——该形态属既有边缘输入，非本批新回归，仅注释标注不处置）；
2. charter 注入（C7）：HF/RND 变量定义处同款追加两行——`PLD="$PROJ/.campaign/pipeline"` 与（MSYS 归一化段内）`PLD_WIN=$(cygpath -w "$PLD" 2>/dev/null || printf '%s' "$PLD")`；激活条件行整行现状为 `[ -f "$HF" ] || [ -d "$RND" ] || exit 0`（注意保尾 `|| exit 0` 契约），改为 `[ -f "$HF" ] || [ -d "$RND" ] || [ -d "$PLD" ] || exit 0`；python 段 `for f in sorted(glob.glob(os.path.join(rnd,'*-resume-note.md'))):` 块后追加同形态 pipeline 块：`for f in sorted(glob.glob(os.path.join(pld,'*.md'))):`——读入 splitlines()，>40 行 → 取前 40 行 + 追加一行 `…（charter 超预算截断）`；parts 追加 `'--- .campaign/pipeline/'+os.path.basename(f)+'（流水线 charter） ---\n'+内容`；names 追加 `'.campaign/pipeline/'+os.path.basename(f)`；python 段签名 `hf,rnd,tools=sys.argv[1],sys.argv[2],sys.argv[3]` → `hf,rnd,tools,pld=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]`，调用行尾追加 `"$PLD_WIN"` 第四参；
3. `docs/known-issues.md` KI-18 条目状态改 closed（处置 = 本批 C8 修复 + ac-94 态 5 分支守护；证据指针留 T9 commit）；
4. ac-94 态 5 补 KI-18 分支：fixture **新增一单元** brief 键写相对形态 + 子进程 cwd 设非工程根 → 断言注入输出含该单元 brief 内容（**断言按修前必红设计，不实测红态**——C-验收守卫预处置下脏树跑 ac-94 必然 check6 BAD，红态由逻辑必然性背书；**既有 U-9 无 brief 键缺省回退分支保留不动**，新单元与 U-9 并存覆盖两路径；PASS 输出位置为**首行**，ac-94 骨架实证 L51-52/L452-456）。

Interfaces：Consumes C7/C8；Produces hook 输出 JSON names 数组新增 `.campaign/pipeline/*.md` 形态（basename 含扩展名）。

验证期望：
- fixture 工程（含 `.campaign/pipeline/x.md`）跑 `ZCODE_PROJECT_DIR=<fixture> bash campaign/hooks/handoff-inject.sh` → 单行 JSON 且含 `pipeline/x.md`；
- 42 行 charter fixture → 输出含 `charter 超预算截断`；
- ac-94 推迟 T9 统一跑（C-验收守卫预处置），届时首行 `PASS ac-94 bridge-behavior (6/6 states)`、exit 0。

### T6 — program-forge SKILL.md：rolling DAG + 锚点泛化 + 升版
画像: 性质=文档; 难度=判断; 领域词=[program-forge, rolling DAG, sketch, 锚点泛化, explore 单元]

步骤：
1. frontmatter `version: "0.2.0"` → `"0.3.0"`；
2. schema 节（K19 块）追加：`status` 枚举五态（C1 逐字）；meta 新键 `planning: rolling`（缺省 = 非 rolling，v1 串行不变）与 `anchor: <注册表路径>`（缺省 = SRS/doc_graph 现状）两枚说明行；
3. 新增 **rolling DAG 节**（插入点：「F1 编排循环」节后、「接口包契约」节前）：
   - sketch 语义：远景单元四键形态（id/title/status: sketch/depends），不进 eligible、不可 start（program.py 显式报错）；
   - 细化三操作：`refine`（sketch→pending 七键补齐）/ `add-sketch` / `drop-sketch`——折叠三条件全满足 → rulings not stalls（program.py `--ruling` 参数落账）；改动 in_progress/complete 单元或其依赖边 → 停点①原样触发；
   - explore 单元：画像性质=调研的单元可声明开创性信号 → 该单元的 caliber 运行走 deep-probe 全剂量档；产出 = DAG 修订提案（refine/add-sketch/drop-sketch 建议清单），对账点批量上裁定；
   - 折叠三条件与 fold_grant 正交说明（C5：共存合法但 lint WARN 提醒）；
4. 锚点泛化（K21 brief「SRS 锚点」节说明行改写）：节名保留（兼容），说明改为「锚点源 = meta `anchor:` 声明的注册表（缺省 SRS/doc_graph）；brief 该节列单元 title 中提取的 ID + 注册表定位」；
5. resume note 节追加一行：「内容五件追加第六件可选——`charter 道状态`（流水线驱动模式下：charter 路径 + 当前复量计数）」。

验证期望：
- `grep -c "sketch" campaign/skills/program-forge/SKILL.md` ≥ 4（心算代入：schema 枚举行 + rolling 节语义行 + 细化三操作行 + explore 单元行 ≈ 4~5 行，阈值按内容实产校准）；
- `grep -c "anchor:" campaign/skills/program-forge/SKILL.md` ≥ 2；
- `grep -c "0.3.0" campaign/skills/program-forge/SKILL.md` = 1；
- ac-93 写作约束自查：新增行内 caliber 组件名（deep-probe/plan-forge 等）不与 `Step N`/`工序 N`/`vX.Y` 字样同行近距共现（T1 同款约束，ac-93 check②③ 扫描域）——`grep -nE "(deep-probe|plan-forge|plan-review-ritual|plan-drafting|coding-forge|exec-forge|ui-forge).*(Step [0-9]|工序 [0-9]|v[0-9]+\.[0-9])" campaign/skills/program-forge/SKILL.md` 零命中（名单与 ac-93 CHECK2_RX 七名全量同步；独立调用）。

### T5 — 版本号集 0.6.5 + ac-90 check2 动态化
画像: 性质=配置; 难度=机械; 领域词=[版本号, 0.6.5, ac-90, 动态化, KI-16]

步骤：
1. 插件版三处（C9）：`marketplace.json` / `.claude-plugin/marketplace.json` / `campaign/.zcode-plugin/plugin.json` 的 `"version": "0.6.0"` → `"0.6.5"`；
2. `README.md` 三处（**自文件尾向上改，防行号漂移**——先 L49 后 L26 再 L5）：L49 注释 `# {"name":"campaign","version":"0.6.0"}` → `0.6.5`；L26 表行 `0.6.0 起兼注在途单元 brief` 保留不动，在其表格下追加一行 `0.6.5 起兼注 .campaign/pipeline/*.md 流水线 charter（KI-18 相对 brief 键解析同步修复）`；L5 `campaign v0.6.0` → `v0.6.5`；
3. skill 版核对（**本步只核对不改动**——campaign `0.4.0` 由 T1 承载、program-forge `0.3.0` 由 T6 承载、三 forge 微升由 T2 承载；执行顺序 T6 必须先于本任务）：`grep -n 'version: "0\.' campaign/skills/*/SKILL.md` 五件各恰 1 行且值为 C9 目标值；
4. ac-90 check2 动态化（C10）：`for s in ("version:", "0.3.0", "campaign-w6"):` → 拆为 `for s in ("version:", "campaign-w6"):` + 其后 `m = re.search(r'version:\s*"(\d+\.\d+\.\d+)"', md); if not m: return False, "metadata version 非 X.Y.Z 形态"`；check2 docstring 同步（`含 name/version/0.3.0/campaign-w6` → `含 name/version(X.Y.Z 形态)/campaign-w6`）；
5. ac-92 check4 核查（仅读不改）：确认 `re.fullmatch(r"\d+\.\d+\.\d+", v)` 动态断言在 0.6.5 下天然通过。

验证期望：
- `grep -rn '"0.6.0"' marketplace.json .claude-plugin/marketplace.json campaign/.zcode-plugin/plugin.json | wc -l` = 0；
- `grep -c '0\.6\.0' README.md` = 1（仅 L26 历史行）；
- ac-90 推迟 T9 统一跑（C-验收守卫预处置），届时 exit 0。

### T7 — pipeline-cases.md 判例库建库
画像: 性质=文档; 难度=机械; 领域词=[pipeline-cases, 判例库, 五要素]

步骤：
1. 新建 `campaign/skills/campaign/references/pipeline-cases.md`，内容 = 库头（用途/判例五要素格式（情境→错误→机制→规则→失效条件）/**四类触发信号（逐字 = ①跳过前提被证伪 ②就绪条件反复不满足 ③charter 误判致复量 ④折叠三条件误用致停点漏停）**/即时登记义务/分辨率裁决（情境与机制同构合并、机制不同新条目）/压缩阈值 ~20 条——与 campaign SKILL.md 判例节五步指针同源，词表只存本件）+ 首条判例（种子判例：本批缘起——「分诊后断链：program 首命中短路全链路」情境→错误→机制→规则→失效条件五要素，证据 = 2026-09-27 用户专利案截图实证）；
2. 目录不存在则创建（`references/` 为新目录，实证：`ls campaign/skills/campaign/` 无此目录）。

验证期望：
- `test -f campaign/skills/campaign/references/pipeline-cases.md && grep -c "失效条件" campaign/skills/campaign/references/pipeline-cases.md` ≥ 2（库头规则行 + 种子判例行）。

### T8 — ac-95 态 5 静态锚补全 + 集成
画像: 性质=新增; 难度=集成; 领域词=[ac-95, 验收, 静态锚, 回调行]

步骤：
1. ac-95 文件与态 1-4 + 兼容守护态**已由 T3 创建**（先测后码）；本任务补 **态 5 静态锚**（三类共 5 项断言）——三 forge 各 `经 campaign 入口进入时` 计数=1（3 项）；campaign SKILL.md 含子串 `## Step 2 — 状态回路` 计数=1；program-forge SKILL.md 含子串 `rolling` 计数 ≥1（grep -c 数命中行数，一行多命中只计 1——断言语义照此写）；含 stdout 子串断言补齐：态 2 断 `refine: <uid> sketch -> pending`、态 3 断 `add-sketch:`/`drop-sketch:` 前缀（T3 Produces 契约消费点）；PASS 输出为**首行**（对齐 ac-94 骨架形态）；
2. run_all.py 免登记确认（glob `ac-*.py` 自动收编，实证 L35）；**run_all 全量推迟 T9 统一跑**（C-验收守卫预处置）。

验证期望：
- `python campaign/acceptance/ac-95-pipeline-driver.py` 首行 `PASS ac-95 pipeline-driver (6/6 states)`、exit 0。

### T9 — 验收守卫收编 + 终验（先提后验）
画像: 性质=操作; 难度=集成; 领域词=[WAVE_FILES, commit, run_all, 终验]

步骤：
0. **前置环境修复（ac-93 批前基线即红，2026-09-28 实测 `BAD 6 桥文件缺失：…cache\caliber-suite\caliber\1.6.1\campaign-bridge.json` exit 1——与本批改动无关，但 T9 终验锚不可达必须先处置）**：源仓 `F:\workspaces\caliber-suite\caliber\campaign-bridge.json` 存在，cache 1.6.1 缺件。**处置已裁定 = (c) 重装 caliber 插件**（2026-09-28 用户裁定：根治 cache 与源仓失同步；本地源无更新检测，重装=新事务）。**工序**：ZCode Settings → Plugins → caliber-suite 卸载 → 重装 → 验证 `ls` cache 目录（`C:\Users\Administrator\.zcode\cli\plugins\cache\caliber-suite\caliber\`）下出现版本目录且内含 campaign-bridge.json（装后状态如实标注 unverified，直至 ac-93 单跑 PASS）；与本批结束后 campaign 0.6.5 重装同窗口。**单跑 `python campaign/acceptance/ac-93-cross-contract.py` 确认首行 PASS 再进步 1**。
1. 读 ac-92/ac-94 的 WAVE_FILES/WAVE_EXEMPT 清单块（`grep -n "WAVE" campaign/acceptance/ac-92-trans-forge.py campaign/acceptance/ac-94-bridge-behavior.py` 定位），把本批改动文件按两件守卫各自扫描域补入——**ac-92 WAVE_FILES 补 9 件**：`campaign/skills/ingest-forge/SKILL.md`、`campaign/skills/spec-forge/SKILL.md`、`campaign/skills/program-forge/SKILL.md`、`campaign/tools/program.py`、`campaign/hooks/handoff-inject.sh`、`campaign/acceptance/ac-94-bridge-behavior.py`、`campaign/acceptance/ac-95-pipeline-driver.py`、`campaign/skills/campaign/references/pipeline-cases.md`、`docs/plans/2026-09-27-campaign-pipeline-driver-plan.md`；**ac-94 WAVE_FILES 补 5 件**：`campaign/skills/ingest-forge/SKILL.md`、`campaign/skills/trans-forge/SKILL.md`、`campaign/acceptance/ac-95-pipeline-driver.py`、`campaign/skills/campaign/references/pipeline-cases.md`、`docs/plans/2026-09-27-campaign-pipeline-driver-plan.md`（两份清单以执行时各件 WAVE_FILES 块现状为基追加，重名不重复；ac-90 check6 无白名单机制、靠 commit 后 diff 为空天然满足；`.caliber/` 两件 gitignore 豁免无需入列；ac-90-entry-skill-smoke.py 自身改动属 ac-90 扫描域外，其 check6 守护对象为 forge/hooks/tools 不含 acceptance 自身——若实测该件在任一 WAVE_FILES 域内则同步补入）；
2. commit 全部改动（显式路径暂存，禁 `git add -A`——共享工作树纪律；**台账与 routing.yaml 经 `.gitignore` 豁免本就不入 commit**，T9 步 1 白名单中该两件为死条目无需操作；commit message 遵循仓内「campaign: …」前缀惯例）；
3. `git status --porcelain` 输出至多一行 `?? campaign/tools/__pycache__/`（该件为解释器副产物，不入 commit 也不挡终验；若裁定 .gitignore 追加 `__pycache__/` 则此行亦消）后跑 `python campaign/acceptance/run_all.py`，期望全绿（ac-90~95 六件；各件 exit 0=PASS，run_all 汇总形态以其 stdout 为准）；
4. 任一红 → 按输出定位修复，重跑至全绿；**修复仍须显式路径暂存 + 追加 commit**。

验证期望：
- `python campaign/acceptance/run_all.py` exit 0 且汇总行六件全 PASS；
- `git status --porcelain` 输出为空或仅 `?? campaign/tools/__pycache__/` 一行（独立调用）。

## 执行编排预分配表

（coding-forge 路径免产——引擎自带角色分配；本表仅留任务画像汇总供阶段 4 入口批量确认）

**执行顺序（显式依赖）**：T1 → T2 → T3（含 ac-95 态 1-4/兼容态创建与基线固化）→ T4 → T6 → T5（步 3 核对依赖 T6/T2/T1 已升版）→ T7 → T8（态 5 静态锚）→ T9（守卫收编+commit+run_all 终验）。T3 步 0 依赖 T8 步 1 的 fixture——实际由 T3 先落 fixture（态 1-4 创建时自带），T8 仅补态 5，无环。

| 任务 | 性质 | 难度 | 形态建议 |
|---|---|---|---|
| T1 | 文档 | 判断 | inline + 独立审查 |
| T2 | 文档 | 机械 | dispatch |
| T3 | 新增 | 集成 | dispatch + 注入 |
| T4 | 新增 | 集成 | dispatch + 注入 |
| T6 | 文档 | 判断 | inline + 独立审查 |
| T5 | 配置 | 机械 | dispatch |
| T7 | 文档 | 机械 | dispatch |
| T8 | 新增 | 集成 | dispatch + 注入 |
| T9 | 操作 | 集成 | inline + 独立审查（commit 纪律+终验，不可 dispatch 盲跑） |

## 风险登记

| 风险 | 触发条件 | 爆炸半径 | 可逆性 | 处置 |
|---|---|---|---|---|
| ac-94 fixture 碰 STATUS_ENUM 后行为漂移 | ac-94 内嵌 fixture yaml 用四旧态，五态枚举下 lint 校验路径不变（`in STATUS_ENUM` 对旧值仍真） | ac-94 红 | git revert | T3 步 5 兼容核查先手跑一遍；真红 → 逐字节比对定位 |
| refine 整块重写破坏行级保留式契约 + 非原子写截断 | sketch 单元 `_idx` 行号块重写后失效；`save()` 整文件覆盖写，进程中途被杀 → program.yaml 截断且 `.campaign/` 通常 gitignore 无 git 兜底 | 程序状态文件损坏 | tmp+os.replace 可回（旧文件在 replace 前不受损） | T3 实现：`_atomic_save`（tmp + os.replace）+ 函数末 reload 提示写 docstring；ac-95 态 2 连续 refine+start 覆盖 |
| charter 注入体积膨胀 | 多 charter 程序并存时 SessionStart additionalContext 超模型舒适区 | 注入噪声 | 删文件可回 | C7 ≤40 行截断硬顶；T4 验证锚含 42 行截断态 |
| cache bridge 缺席（实证 ABSENT）致 ac-93 基线批前即红（check⑥ 反向闭环消费桥定位，2026-09-28 实测 `BAD 6 桥文件缺失` exit 1）——ac-94 不受影响（全部用 fixture 桥，实证 L166-171），ac-93 影响 T9 终验可达性 | T9 run_all 必红 | 前置修复后绿（方向见 T9 步 0，处置待用户裁定） | T9 步 0 前置环境修复 + 单跑 ac-93 确认绿再进终验 |
| description 重写后 AGENTS.md 全局路由漂移 | 用户环境 AGENTS.md 引用 description 信号清单 | 全局路由误判 | 文本可回 | T1 步 2 description 除尾句追加外逐字不动 + T1 验证锚六子串内联复核；ac-90 check2 由 T9 终验 |

## 技能消费裁定节

（工序 4 彩排后回写，2026-09-28。预绑定语义 = 默认消费——dispatch 边界偏离须记 ledger Ruling，终审闭环核查）

| 任务 | 建议 | 裁定 | 理由 |
|---|---|---|---|
| T1 | code-review（独立审查位） | 采用为预绑定 | 双轴真实匹配：Spec 轴 = T1 七锚+保留清单逐字对 diff；Standards 轴 = 仓内 skill 惯例+ac-90 _ONCE 面 |
| T1 | grilling（routing 参照位） | 弃用（采纳彩排弃用建议） | plan 本身即四轮对齐产物，执行期无对齐对象；Step 1.6 是写入 SKILL.md 的未来行为文本，非本批执行动作 |
| T1/T6/T7 | writing-skills | 弃用（采纳） | 其 skill 基线测试 Iron Law 与 C-预处置「先提后验」直接冲突；验证由 ac-90/ac-93 机械守卫承担 |
| T1/T6 | skill-reviewer | 弃用（采纳） | 英文「Use when」标准形态与本仓中文自定骨架错位，误报率高；自动化维度已被 ac-90/ac-93 定制覆盖 |
| T2 | 无 | 无（采纳） | 一次性逐字追加，无组件交集 |
| T3 | test-driven-development | 采用为预绑定（限缩：红绿循环只落 ac-95 新件） | plan 自带先红后绿工序与其 Iron Law 同构 |
| T3 | subagent-driven-development | 采用为预绑定（dispatch 形态时） | dispatch+注入形态的执行引擎纪律 |
| T3 | campaign:program-forge 正文参照 | 采用（参照非 Skill 调用） | C1/C5 语义与 K19 schema/fold_grant 权威表述对齐 |
| T3 | python-patterns / python-testing（visible:false） | 弃用（采纳） | 仓内零依赖风格 + 自研 ac-*.py 骨架（非 pytest），引入破坏风格一致与 run_all 收编 |
| T3/T4/T9 | systematic-debugging（条件性：验证锚跑红时） | 采用为预绑定（条件触发） | 根因先行防盲改重跑；SessionStart 注入失灵是其点名场景 |
| T4 | TDD（若类推） | 弃用（采纳） | plan 裁定「不实测红态」——红态由逻辑必然性背书，实测反撞零触碰守卫 |
| T5 | plugin-creator | 采用为预绑定（工序参照） | manifest 递增+双 marketplace 同步纪律同构 |
| T6 | code-review（独立审查位） | 采用为预绑定 | 同 T1；Standards 轴补 ac-93 check③ 十枚举面 |
| T7 | 无 | 无（采纳） | 判例内容只能自产，无组件可替代 |
| T8 | verification-before-completion（完成判定门） | 采用为预绑定 | 「见到 PASS+exit 0 才算完」= 其门函数直接实例 |
| T8 | subagent-driven-development | 采用为预绑定（dispatch 形态时） | 同 T3 |
| T9 | verification-before-completion（终验声称门） | 采用为预绑定 | 两验证锚均「跑命令→读全输出→才声称」形态 |
| T9 | plugin-creator（步 0 重装工序参照） | 采用为预绑定 | 卸载+重装工序、unverified 如实标注、版本同步指导 |
| T9 | code-review（commit 前整批 diff 独立审查） | 采用为预绑定 | 形态建议明言不可 dispatch 盲跑；Spec 轴 = C1-C10 逐条对 diff |
| 全局 | campaign:campaign / campaign:program-forge（被改造对象） | 不作执行组件（维持路由表微调裁定） | 改造对象不能自我消费；仅作核对基准 |

未决项：NO UNRESOLVED。

---
> 锻造总结：工序 3 两轮（发现 47 条：P1×4/P2×13/P3×30，全部修复）+ 工序 3.5 闸口（P1×1/P3×6，sketch 四键裁定）+ 工序 4 彩排（Phase 1 点位 12 项全部回写；Phase 2 技能裁定 22 行：采用预绑定 12、弃用 7、无 3）。审计：.caliber/review-logs/2026-09-27-campaign-pipeline-driver.md。NO UNRESOLVED。
