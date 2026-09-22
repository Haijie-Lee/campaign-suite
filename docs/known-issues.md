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
- **状态**：待立项（依赖 KI-01 的定级机制先行）。

## KI-08 入口 skill 辅助信号「加权」未操作化

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
- **状态**：open。重访触发 = program.py cmd_gate（或 gate 账本路径）行为下次被触碰，或 ac-91 获 plan 级修订授权时。注意：本触发不因消息/rc 级修整（如 2026-09-22 final fix）而点火。

## KI-14 ingest-forge SKILL.md 判别指引行 `。；` 标点瑕疵

- **现象**：`campaign/skills/ingest-forge/SKILL.md` 判别指引行末为 `…待决项 → DECISIONS.md。；编码/架构约定类内容…`——句号后接全角分号，纯排版瑕疵无语义危害。
- **来源**：plan 锁定追加句以 `；` 起首贴上既有行尾 `。` 的直接结果（计划强制，2026-09-22 终审评估 T6① 裁定入册不升档——修 = 偏离绑定权威）。
- **处置方向**：下次该行因他因编辑或该 skill 升版时顺手收敛为单标点。
- **状态**：open。重访触发 = ingest-forge SKILL.md 判别指引行下次因他因编辑，或该 skill 升版时。

## 附：工具层已登记毛刺（不重复立案）

- doc_graph 组 ID 叙事性加粗误报 duplicates 假阳性（fixture 实测 FR-8/9/10 三例，词法 v1.2 候选修法已登记）——见 `campaign/tools/doc_graph.md` 已知限制节。
- spec-lint 路径口径（`*/SRS.md`、`*/docs/spec/*.md`）不覆盖 `.campaign/` 下其他规范工件——如需扩面再单独立项。

## 根因一句话

caliber 把流程严谨度藏在"定级 + 六阶段表"后面（托管式：用户交任务，skill 出剂量）；campaign 把编排纪律显式化为文件系统状态机（自助式：用户自己当编排者，查表、跑命令、维护生存包），且未经 caliber 那样的多轮实战裁定打磨（v1.17 vs v0.1.0）。本 backlog 的收敛方向 = **补入口、补原语、补折叠、补兜底**。
