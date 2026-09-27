# campaign 已知问题与体验 backlog

> 用途：登记 campaign 插件使用中确认的不顺手 / 缺陷，每条带证据与处置方向，供后续逐条立项解决。
> 建立：2026-09-22。来源 = campaign vs caliber 对比调查（两插件本体通读：campaign 三 skill + 四 hook 契约 + 工具 schema；caliber 主入口 v1.17 + hooks）。
> 消费：每条有「状态」字段；解决时在条目内记处置结果与证据指针。caliber 阶段 6 触发核查会消费本文件——重访触发命中的 open 项须显式处置（关闭记理由 / 带新触发再延 / 转 TODO）。

## KI-01 无统一入口，任务分拣负担在用户身上 【P0】

- **现象**：三个 skill（ingest-forge / spec-forge / program-forge）平级分立，description 全为否定式互踢（"Not for X, use Y"）；用户须先自行判对任务性质才进得对门；且无 ML/L 定级前置，剂量靠用户自己知道。
- **对比证据**：caliber 唯一入口，定级 / 路由 / 剂量是 skill 内部机械判断（Step 1 五维定级表 + Step 1.5 路由装配 + Step 2 六阶段 × 四档剂量表），用户只说"做什么"。
- **处置方向**：新增 campaign 总入口 skill——学 caliber 定级路由形态，三 skill 收编为内部路由目标；入口内补全景流程心智地图（顺带缓解 KI-02）。
- **状态**：**已关闭**（2026-09-22）。处置 = campaign 总入口 skill 落地（`campaign/skills/campaign/SKILL.md`：域判定→路由→守停止点三职，域地图/停止点速查/与 caliber 分工三节内联；description 信号清单为 AGENTS.md 全局路由权威，排除句配对指向 caliber）。证据：`docs/plans/2026-09-22-campaign-entry-skill-plan.md` + ac-90 验收四跑 PASS（`.campaign/evidence/ac-run-20260922.txt`）+ `C:\Users\Administrator\.zcode\AGENTS.md` 工程入口节新非对称路由。生效待插件卸载重装（v0.4.0）。定级前置未纳入——入口不定级系本案明确裁定（剂量归 forge 与 caliber 各自所有），KI-07 跟踪。

## KI-02 指针式写作，流程拼不完整

- **现象**：spec-forge 工序 3 实质内容仅"机制与 plan-forge 工序 3 全同，见 caliber plan-forge SKILL.md 工序 3/3.5 与 plan-review-ritual Step 0-4"；执行时须跨插件多文档跳读才能拼出完整流程。防双份纪律漂移的设计意图正确，代价是首用者没有心智地图。
- **对比证据**：caliber SKILL.md 自包含——铁律、停止点速查、阶段表全部内联，336 行一次读完即可执行。
- **处置方向**：总入口 skill 内嵌全景流程图（指针的索引层）；各 skill 关键指针处增补一两句"机制摘要 + 指针"两段式，让跳读前先有概念。
- **状态**：**部分消化**（2026-09-22，随 KI-01）。已落地 = 指针索引层：入口 skill 域地图表（三 forge 一句话职责 + 出口）+ 「只管三件事」开篇定位。未消化 = forge 正文「机制摘要 + 指针」两段式（转 plan 挂起项③，见 `docs/plans/2026-09-22-campaign-entry-skill-plan.md`）。重访触发 = 任一 forge 下次改版。

## KI-03 无 fallback，缺 caliber 即指针悬空

- **现象**：plugin.json 自述 "layered on caliber"，但 ZCode 插件无依赖声明机制，campaign 自身也无缺失兜底——caliber 不在时 spec-forge / program-forge 的指针引用全部悬空，静默失效。
- **对比证据**：caliber Step 0 依赖验证一行输出 + fallback.md 逐章兜底，"缺失不中断"。
- **处置方向**：总入口加依赖验证一行输出（镜像 caliber Step 0），缺 caliber 时给最低限度纪律兜底文本。
- **状态**：**部分消化**（2026-09-22，随 KI-01）。已落地 = 入口层：Step 0 依赖验证一行输出（`✓ 全配` / `⚠ 缺 X`）+ 缺 caliber 改报文本 + 缺 forge 上报不继续（`campaign/skills/campaign/SKILL.md` Step 0；运行时行为，ac-90 以锚文本静态闸覆盖）。未消化 = forge 层 fallback 兜底文本（超入口职责，裁定不消化）。重访触发 = 任一 forge 下次改版，或 caliber 缺席环境的实测失真报告。

- **现象**：program-forge 推一个单元 = 七步 LOOP × program.py 九子命令手工按序调用（status → next → brief → start → collect → gate → reconcile-check），顺序不能错、失败禁跳过。设计意图（查表机械劳动替代即兴记忆）正确，但查表劳动本身未封装。
- **处置方向**：封装"推进到下一停止点"单原语（如 `program.py advance`），LOOP 内机械查表步骤合并为一次调用；七步语义保留为内部实现。
- **状态**：待立项。

## KI-05 停止点无折叠机制，全部硬等

- **现象**：Q 表逐条停、出口三证不齐状态不迁移、三停止点硬等人工——无一例可折叠。
- **对比证据**：caliber 2026-09-15 裁定三条件全满足可折叠（① 用户消息含明确执行授权；② 无取舍待决；③ 无新增不可逆操作），折叠须一行展示依据 + ledger Ruling 记账。
- **处置方向**：从 caliber Step 1.5 第 5 步折叠条件移植，作用于 Q 表对齐（批量裁定形态）与门检查报告点。
- **状态**：待立项。

## KI-06 激活面窄 + 生存包手工维护

- **现象**：四个 hook 带 K7 激活判据（工程根存在 `adr/` | `docs/spec/` | `.campaign/` 任一才激活）——未初始化项目里整个插件静默，用户感知不到它存在；`handoff.md` 生存包 hook 只读不改写（"更新人：编排者"），靠纪律手工维护，遗忘即注入陈旧状态（2026-09-22 会话实测：注入的是前一日手工快照）。
- **对比证据**：caliber 的 docs 订阅检查在未订阅时也输出一行可发现性提示，不静默。
- **处置方向**：hook 未激活时输出一行可发现性提示（学 caliber docs 订阅检查）；handoff 维护挂到 program.py 门 / 收账事件上自动更新，替代纯人工纪律。
- **状态**：待立项。

## KI-07 剂量不缩放，无轻量路径

- **现象**：全插件为 mega-scale 固定全装备（graph / ledger / 门 / 对账），仅 ML/L 两档；中小任务无轻档，用上即高射炮打蚊子。
- **对比证据**：caliber 核心卖点"S 级也过六站，只是每站一分钟"，剂量随定级四档缩放。
- **处置方向**：总入口定级时定义轻档语义（如免对账周期、免 handoff、门检查降级为提醒）。
- **状态**：部分消化（2026-09-26 融合批）——声明定级制落地后单元剂量由 caliber 四档承载（文档单元声明 S），形态下限表封死向下余量为本批裁定形态。

## KI-08 入口 skill 辅助信号「加权」未操作化【已关闭，见下消化记】

- **现象**：`campaign/skills/campaign/SKILL.md` Step 1 辅助信号「工程根 adr/ 或 docs/spec/ 或 .campaign/ 存在 = …判定时加权」——「加权」无操作化定义：四信号皆弱或辅助信号单独在场时，执行者不知该加权到什么程度、能否单独定域。
- **来源**：plan 原文如此（计划强制，2026-09-22 终审评估 E2 裁定入册不升档——修法须发明 plan 未含的语义，属设计决策而非机械改动，且无实测误判实证）。
- **处置方向**：下次 SKILL.md 改版时改写为可操作语义，如「仅在四信号弱命中/难裁时作倾向参考，不单独定域」。
- **状态**：open。重访触发 = SKILL.md 下次改版，或出现「加权」引发实际误判/困惑的实证。

## KI-09 ac-90 检查 6 零触碰探针对未跟踪新文件不敏感

- **现象**：`campaign/acceptance/ac-90-entry-skill-smoke.py` 检查 6① 探针 `git diff --name-only HEAD -- <守卫路径>` 只看已跟踪文件——守卫路径（三 forge / hooks / tools）下新建未跟踪文件落入盲区，守卫强度低于零触碰意图。
- **来源**：plan 逐字规定的探针形态（计划强制，2026-09-22 终审评估 E6 裁定入册不升档——换探针偏离绑定权威，且与既有 SKIP 降级语义的交互需重新设计）。
- **处置方向**：升级为 `git status --porcelain -- <paths>` 或 diff-HEAD + `git ls-files --others --exclude-standard` 双段。
- **状态**：open。重访触发 = ac-90 下次修订 / 下一波 acceptance 整理窗（与 run_all docstring 事项同窗）/ 任何把 ac-90 启用为合并闸的流程上线前。

## KI-10 plan 文本「声明新建实已存在」类事实偏差无下游护栏

- **现象**：`docs/plans/2026-09-22-campaign-conventions-channel-plan.md` T1 注记「conventions/ 为新目录」，实际该目录在 BASE 已有 result-file-contract.md/result-template.md 两个 tracked 文件（彩排补写引入的事实错误）。本例产物路径正确、零实害，但同类偏差若落在路径/文件名上即有实害。
- **来源**：plan 锁定文本（计划强制，2026-09-22 终审评估 T1① 裁定入册不升档——plan 系未跟踪历史工件、无下游消费者，修文本不改变任何产物）。
- **处置方向**：plan 锻造/彩排工序对「新建目录/文件」类断言加一条实证核对（写 plan 前 `ls` 目标路径）；本 plan 文本不回改。
- **状态**：open。重访触发 = 该 plan 文本被复用/引用，或 plan 锻造再产出同类「声明新建实已存在」事实偏差时。

## KI-11 program.py 读文件未用 with（两处同形）

- **现象**：`campaign/tools/program.py` cmd_brief 读约定文件 `open(cpath)` 未 with 包裹（约 :275），与既有 :262 `json.load(open(gpath))` 同形；一次性 CLI 进程靠 CPython 引用回收关句柄，无泄漏实害，但与资源管理最佳实践不符。
- **来源**：plan 锁定代码逐字 + 仓内既有风格（计划强制，2026-09-22 终审评估 T2② 裁定入册不升档——修 = 偏离锁定代码且与仓内同形风格冲突）。
- **处置方向**：program.py 下次实质重构时两处一并 with 化；若仓库引入资源管理强制 lint 约定则提前处理。
- **状态**：open。重访触发 = program.py 下次实质重构，或仓库引入 open()/资源泄漏强制 lint 约定时（连同 :262 gpath 同形一并包裹）。

## KI-12 conventions 路径解析两处重复未提取 helper

- **现象**：program.py K6 行与 K1/K3 行各写一遍 `str(prog.meta.get("conventions") or "CONVENTIONS.md")`（约 :202 与 :273，逐字节相同）；今日无漂移，未来单侧编辑可静默分叉。
- **来源**：执行引入（2026-09-22 终审评估 T3① 裁定入册不升档——两处低于自设 DRY 阈值，T3 review「第三处出现才提取 helper」裁定在案）。
- **处置方向**：第三处出现时提取模块级 `_conv_path(prog)` helper（形态参照既有 `_lint_cmd`）。
- **状态**：open。重访触发 = program.py 出现第三处 conventions 路径解析（或新增约定文件消费者）时。

## KI-13 未配置 lint_cmd 的 gate 逐字节一致无 ac-91 回归态守护

- **现象**：ac-91 六态覆盖 cmd_brief 三态 + gate 通过/失败 + validate WARN，但「未配置 lint_cmd 的程序 gate 输出与改造前逐字节一致」这一 opt-in 约束的 gate 半侧无永久回归态（仅 T3 实现期手工验证一次留痕，validate 半侧有态 6）。
- **来源**：plan 锁定六态结构（计划强制，2026-09-22 终审评估 T4② 裁定入册不升档——加第 7 态 = 偏离绑定权威）。
- **处置方向**：ac-91 获 plan 级修订授权重开态结构时补第 7 态（同态 2 fixture、无 lint_cmd 跑 gate，断言 stdout/ledger 与基线逐字节一致）。
- **状态**：closed（2026-09-22）——重访触发命中（cmd_gate env 钩子契约改动 + ac-91 态结构经用户授权重开）；处置方向已落地：ac-91 补态 7（CAMPAIGN_UNIT/PROGRAM/WS env 契约回归）+ 态 8（无 lint_cmd gate 的 stdout/prog.yaml/ledger 事件序列逐字节守护，ledger ts 字段除外）。

## KI-14 ingest-forge SKILL.md 判别指引行 `。；` 标点瑕疵

- **现象**：`campaign/skills/ingest-forge/SKILL.md` 判别指引行末为 `…待决项 → DECISIONS.md。；编码/架构约定类内容…`——句号后接全角分号，纯排版瑕疵无语义危害。
- **来源**：plan 锁定追加句以 `；` 起首贴上既有行尾 `。` 的直接结果（计划强制，2026-09-22 终审评估 T6① 裁定入册不升档——修 = 偏离绑定权威）。
- **处置方向**：下次该行因他因编辑或该 skill 升版时顺手收敛为单标点。
- **状态**：open。重访触发 = ingest-forge SKILL.md 判别指引行下次因他因编辑，或该 skill 升版时。

## KI-08 消化记（2026-09-23，trans-forge 波次）

- **处置**：T4 落地 M12 新句——辅助信号改写为「仅在域信号弱命中或难裁时作倾向参考，不单独定域」（`campaign/skills/campaign/SKILL.md` 辅助信号行）；反向断言「判定时加权」命中数=0 由 ac-92 态 2 把守。
- **KI-08 原条状态**：closed（2026-09-23）。证据 = ac-92 态 2 反向锚 + T8 口试三例全对。

## KI-02/KI-03/KI-05 消化行（2026-09-23，trans-forge 波次）

- **KI-02（指针式写作）**：trans-forge SKILL.md 落地两段式（机制摘要一句 + 指针 spec-forge/caliber 工序），未复制实现——forge 层两段式由 trans-forge 首次兑现。
- **KI-03（无 fallback）**：trans-forge SKILL.md 开篇依赖验证（缺 doc_graph.py / ingest-forge 模板 / spec-forge 机制指针任一 → 上报不继续）+ ac-92 态 1 锚把守。
- **KI-05（停止点无折叠）**：trans-forge 三停点（映射设计表 / 自增 D+Q 表 / 出口门证不过不迁移）为首个全程硬停的 forge；M4 彩排豁免令（停点①②以「最可能假设落笔+全量登记」代替）仅限金样彩排，真实使用必停——非折叠，是显式豁免。

## KI-15 q-table 模板注释 `\|` 与 SKILL.md 全角 `｜` 不一致

- **现象**：ingest-forge `templates/q-table-template.md` 注释行写为 `\|`，与 `SKILL.md` 全角 `｜` 规则（W2-T6 实证）不一致——模板注释与正文规则双形态。
- **来源**：执行引入（模板注释行历史如此，非本波改动）。
- **处置方向**：ingest-forge 下次升版时模板注释行改全角 `｜`，与 SKILL.md 对齐。trans-forge 侧（C5）一律从 SKILL.md 全角规则，不受影响。
- **状态**：open。重访触发 = ingest-forge 下次升版。

## KI-16 ac-90/ac-92 版本字面值断言随升版批失同步致红

- **现象**：ac-90 check4 / ac-92 check4 以字面值（`v != "0.5.0"`）钉定三 manifest 版本、ac-90 check2 钉 skill 版本字面值 `0.2.0`——验收断言与版本号集互相咬死：每次升版必连带改断言，漏改即红。2026-09-26 融合批升版（campaign 0.5.1→0.6.0、skill 0.2.0→0.3.0）基线实证字面值断言即刻失同步。
- **来源**：计划强制（ac-90/ac-92 系各波 plan 逐字钉定的验收脚本，版本字面值随当时版本写入）。
- **处置方向**：check4 动态化——逐处 `re.fullmatch(r"\d+\.\d+\.\d+")` 形态校验 + 三处互等（`len(set(...)) != 1`），断言不再含版本字面值；check2 跟随升版同步。ac-90 check2 字面值（`0.3.0`）为同族残留——下次 campaign skill 升版批同款动态化（重访触发）。
- **状态**：closed（2026-09-26，融合批 T10 已落地）。同族残留（ac-90 check2 字面值 `0.3.0`）已于 2026-09-28 流水线驱动批 T5 同款动态化（`re.search` X.Y.Z 形态断言，断言面零版本字面值），残留清零。

## KI-17 ui-forge campaign gate 消费点声明后零消费（手工接线必败实证）

- **现象**：caliber ui-forge §消费点契约声明的 campaign gate 判据，2026-09-25 声明至 2026-09-26 零消费——AeroFold-ui 四单元 gate 无 fidelity-report、lint_cmd 仅 `npm run lint`：声明的消费点靠程序作者手工接线，必败实证。
- **来源**：2026-09-26 融合批设计期实证（双轨方案勘探对照中查实消费面为零）。
- **处置方向**：桥文件机制承接——caliber 仓导出 campaign-bridge.json（T1），program.py gate 机械合并桥判据（T2），消费不再依赖手工接线；本批已落地（ac-93/ac-94 双闸把守）。
- **状态**：closed（2026-09-26，融合批 T1/T2/T7）。（AeroFold-ui 仓侧 learnings 归 U-M2-08 汇合时消费，不入本批。）

## KI-18 handoff-inject.sh 相对 brief 键按 hook 进程 cwd 解析（静默丢注入）

- **现象**：程序 yaml 声明相对形态 `brief:` 键 + 单元 in_progress + hook 进程 cwd ≠ 工程根时，`os.path.isfile(bp)` 落空且相对键无默认路径回退——compact 后静默丢在途单元 brief 注入（恰是 A2 注入要根除的失忆形态）。实证：smoke-w4.yaml 五单元 brief 值恰为相对形态（现网全 complete 故休眠）。
- **来源**：计划强制（handoff-inject.sh 钉定代码按 hook 进程 cwd 解析相对 brief 键——2026-09-26 融合批终审评估 loop 自 deferred minor T4② 转入）。
- **处置方向**：`os.path.join(rnd, brief)` 或 rnd 优先解析；修复需动钉定代码 + ac-94 态 5 补分支，值得独立小批。
- **状态**：closed（2026-09-28，流水线驱动批 T4）。修复 = bp 相对键按程序目录（rnd）回退解析（`os.path.isabs` 守卫，空串视同缺键走缺省名）；ac-94 态 5 补 U-10 相对键分支（与 U-9 缺省分支并存，断言按修前必红设计）；头注释在途单元 brief 枚举与注入面（`.campaign/pipeline/*.md`）同批补齐。fixture 直跑实证：相对 brief 内容命中注入。

## KI-19 meta `anchor:` 键声明性落地，cmd_brief 消费端未接（文档-行为分叉）

- **现象**：program.yaml 声明 meta `anchor: <注册表路径>` 后，`program.py brief` 的锚点定位仍硬编码 `.campaign/graph/graph.json`（program.py grep "anchor" 零命中），静默走缺省源——声明者不被告知键未生效。
- **来源**：2026-09-28 流水线驱动批 T6 独立审查（code-review 位）发现；plan C3 自知「无码改」（parser 天然容纳新键），T6 文档规格与消费端缺口为 plan 内生分叉。
- **处置方向**：cmd_brief 注册表定位改读 `prog.meta.get("anchor")` 覆盖（缺省行为不变）+ ac-9x 补分支；小改，随下批。
- **状态**：open。重访触发 = 首个在程序中声明 `anchor:` 键的用户实证，或下次触碰 cmd_brief 时。缓解：program-forge SKILL.md schema 节 anchor 键定义点已标注「声明性键，本批未消费」。

## 附：工具层已登记毛刺（不重复立案）

- doc_graph 组 ID 叙事性加粗误报 duplicates 假阳性（fixture 实测 FR-8/9/10 三例，词法 v1.2 候选修法已登记）——见 `campaign/tools/doc_graph.md` 已知限制节。
- spec-lint 路径口径（`*/SRS.md`、`*/docs/spec/*.md`）不覆盖 `.campaign/` 下其他规范工件——如需扩面再单独立项。

## 根因一句话

caliber 把流程严谨度藏在"定级 + 六阶段表"后面（托管式：用户交任务，skill 出剂量）；campaign 把编排纪律显式化为文件系统状态机（自助式：用户自己当编排者，查表、跑命令、维护生存包），且未经 caliber 那样的多轮实战裁定打磨（v1.17 vs v0.1.0）。本 backlog 的收敛方向 = **补入口、补原语、补折叠、补兜底**。
