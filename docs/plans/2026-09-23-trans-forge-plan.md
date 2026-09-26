# trans-forge（campaign 第四 forge：plan→spec 转化锻造）实现 plan

> 版本：v1.0（2026-09-23 初稿）
> 定级：L｜引擎路径：caliber:exec-forge（任务性质分布：文档 4 / 配置 2 / 新增代码 1 / 操作 2 / 重构 1——代码不过半）
> 对齐快照：caliber L 级阶段 1 产物（双轨澄清已裁定「全部按押注」），工作材料全文 = `.caliber/trans-forge-stage1-snapshot.md`

## 对齐快照节

### 目标重推
把「成熟方案文档（plan 形态：现状论证+路线裁定+蓝图+里程碑+风险登记）→ 可收编、含完整需求规格与技术架构的可落地文档」的转化能力，固化为 campaign-suite 第四 forge（trans-forge）：五工序+三停点+出口三证，双产物（转化文档 + 收编预案），配套案例库与 genre 模板；使任意工程稳定复现 flow-builder 案例专家手工质量（FR/NFR/AC/契约/DDL/状态机完备、决策逐字追溯、TODO 零编造），且可收编性经机械预演实证（判据以 AeroFold 真实收编实测校准）。

### 道层条款（价值排序/不可妥协项/失败的形状）
- 价值排序：可收编性+可验证性 > 生产速度 > 自动化程度；宁可多停点，不可编造。
- 不可妥协项：①零编造数值（无出处 → TODO 注册+最可能假设落笔，禁正文常量）；②plan 已裁定决策逐字可追溯（溯源完整证机械把守）；③产物 `##` 节单一工件归属（可收编译演证把守，低置信=0）；④模糊点上 Q 表停点由用户裁定，不代答；⑤规格增量必须真实（增量真实证把守，换皮重排=打回）。
- 失败的形状：①可收编性只宣称未验证（flow-builder spec 剖析时点未真实收编=前车之鉴，2026-09-23 上午；同日 17:25 前已被并发会话完成首次真实收编——事实断言必带时间戳）；②换皮重排无规格增量=假转化；③纪律退化为模板+自由发挥=质量不可复现。

### 开放决策点+方案选定记录
方案选定：**方案 A（新 forge，trans-forge）**——主轨与挑战轨独立生成一致推荐。方案 B（spec-forge 扩转化模式：契约自相矛盾+模式分叉渗入头尾工序）与方案 C（轻资产三件套/few-shot 临摹：纪律经闸门传递不经样例）否决。
已裁定（2026-09-23 用户「全部按押注」）：
- D-1 命名 = **trans-forge**
- D-2 入口分支序位 = program > ingest > trans > spec；判别式（与 ingest：产出新文档 vs 收编本文档不改写；与 spec：门外单篇 plan vs 门内生产/修订）（判别式逐字形态以契约矩阵 M2 为准）
- D-3 收编预案落盘 `.campaign/ingest/<slug>/` 五件套，真实 ingest 降为 replay 验证
- D-4 fresh 读者理解性测试范围 = FR/AC/契约节（裁剪制）
- D-5 金样回归判据 = 先跑一轮再定阈值，不预造数值
- D-6 准入三判据缺一即拒绝进入并上报（回 caliber plan-forge / deep-probe 补 plan）
- D-7 路由表 14 条全采纳（6 条 visible:false 的 .claude 侧组件以 Read 注入消费，不安装）

### 挂起项（带触发器）
- artifact-native 直产七工件（2026-09-23 否决，四理由：删独立验证层/工件区非签收形态/第二入区通道失控/问题已被更便宜解决）——触发器：工件区 IDE 化成为主阅读面时复活
- 专用 trans-forge agent 定义文件（暂缓，YAGNI）——触发器：金样彩排中基线 agent 按 brief 执行反复失败
- doc_graph 增 ID 前缀冲突 lint 子命令（暂缓）——触发器：金样彩排出现 ID 前缀冲突漏检
- 出口三证 Stop hook 强制化（当前为 skill 内工序）——触发器：两次真实使用中出现跳过出口门

### 前提清单
1. genre（§0–§10+附录「需求规格与技术架构方案」体例）可泛化到第三工程——两实例佐证（AeroFold 2596 行 / flow-builder 1622 行，2026-09-23 实测；后者当日持续编辑中），但只有两例
2. plan 准入判据可机械判定——flow-builder plan 满足；其他工程 plan 形态未验证
3. ingest-forge 七类枚举与映射粒度稳定；caliber 机制指针稳定
4. 用户瓶颈是转化质量不可复现，而非生产速度
5. monolith 文档仍是用户想要的评审/签收形态
6. campaign 入口域判定可改（加第四分支=改既有 skill 行为——已获批准）

## Global Constraints

- **C1 机制指针引用不复制**（house 惯例，防双份纪律漂移）；trans-forge 正文关键指针处用「机制摘要一句 + 指针」两段式（KI-02 处置方向）。
- **C2 依赖兜底**（KI-03 处置方向）：trans-forge SKILL.md 开篇带依赖验证一行——缺 `campaign/tools/doc_graph.py` / ingest-forge 模板 / spec-forge 机制指针任一 → 上报不继续。
- **C3 新建路径已 ls 实证**（KI-10 教训，2026-09-23 选材实证）：`campaign/skills/trans-forge/` 及其 `templates/` `references/` 子目录当前不存在；`campaign/acceptance/ac-92-trans-forge.py` 不存在。
- **C4 零触碰面穷举**：本 plan 改动 = 各任务文件清单之并集，此外零改动；验收用 `git status --porcelain`（KI-09 教训：diff HEAD 探针对未跟踪新文件不敏感）。
- **C5 q-table 全角 `｜` 规则优先**：ingest-forge SKILL.md（W2-T6 实证：`\|` 转义会被 awk 按字面 `|` 切分）与 q-table-template.md 注释行（写为 `\|`）不一致——trans-forge 侧产物与模板一律从 SKILL.md 全角 `｜` 规则；模板注释行本 plan 不改（非本域），登记 KI-15（T10）。
- **C6 ac-90 既有锚为本 plan 硬约束**（ac-90-entry-skill-smoke.py docstring 逐字）：campaign SKILL.md 行数 ≤100；三处 JSON 同版本；marketplace 双份逐字节同形。
- **C7 数值全部有出处**：AeroFold mapping = 高 9 / 中 4 / 低 0（13 数据行，2026-09-23 直测，该件为历史冻结工件不再漂移）；q-table 25 行全 resolved（同日直测）；flow-builder spec = 1622 行、profile = FR=98 NFR=32 R=12 D=20 Q=16 AC=32、weak_words=3（2026-09-23 复测——**该文档当日在持续编辑，本组数值以测量时点为准，T9 执行时一律重测不引本行旧值**）；plan 468 行（同日实测）；AeroFold SRS 2596 行（同日实测）；campaign SKILL.md 基线 66 行（同日实测）。
- **C8 彩排写入穷举**：T9 对 flow-builder 工程仅新增契约矩阵第 10 行所列内容，全 additive；回滚 = 删除 M10 ①②③ 三件（文件/目录），④ 仅移除所追加的 `.campaign/` 一行（不删 `.gitignore` 文件本体，且④条件未触发时无需动作）（风险 R3）。
- **C9 波次标记**：本波 = campaign-w6（metadata source 字段沿用此值；w5 = 入口 skill 波）。
- **C10 提交纪律**（ac-90 check6① 前置 + 共享工作树纪律）：T1–T2 合并一次、T3 一次、T4–T6 合并一次、T7 一次、T10 一次，共五个 commit；每次 `git add <该次文件清单显式路径>`——禁 `git add -A` / `git add .` / `git add -u`（仓内有他线未跟踪件 `campaign/tools/__pycache__/`）；commit message 前缀 `campaign: trans-forge`。**T7 步骤 4 跑 run_all 前，T1–T6 全部改动必须已提交**——ac-90 check6① 对 hooks 等守卫路径做 diff-HEAD 零触碰检查，改动提交后 diff 归零、守卫自然通过。**修复环返工 commit 另计**（T8/T9 失败处置回改 T3/T4 等文件时）——前缀与显式路径暂存纪律不变；ac-92 态 6 白名单按路径不按 commit 计数，天然覆盖。
- **C11 路由消费契约**（D-7 落地）：本 plan 执行期技能消费以 `.caliber/routing.yaml`（14 条）为编排者选料单——dispatch 边界按任务文本与路由 keywords 匹配消费；6 条 `visible: false` 组件（spec-miner / architect / intent-driven-development / skill-comply / delivery-gate / gateguard）按路由表各自 `path` 字段以 **Read 注入正文**消费、**不安装**（caliber §动态组合 注入式激活）；预分配表 领域组件列 为候选非绑定，plan-forge 工序 4 Phase 2 彩排后经编排者裁定回写升级为预绑定（默认消费、偏离记 ledger Ruling、终审闭环核查）。

## Review Focus（≤5）

1. **域判定回归**：trans 分支插入后既有三域（program/ingest/spec）误判风险——钉 T4 锚文本断言 + T8 口试三例（覆盖 trans/ingest/program 三例，期望路由与判别式一致）。
2. **出口三证首轮未校准**：判据过严则金样彩排假红，过宽则失守——钉 T9 记录义务（实测值全量登记，D-5：阈值首轮跑完再定，本 plan 不预造）。
3. **彩排执行者扛不住 1500 行级写作**：基线 agent 长文产物质量是首次实测——钉 T9 处置链（不变量缺失 → 回 T3 补 brief 重跑一次；两轮不过 → 停，上用户裁定，并触发「专用 agent」挂起项评估）。
4. **spec-context.sh Windows Git Bash 行为**：hook 为 bash 脚本、5000ms 超时、exit 恒 0 契约下失效表现为静默无注入——钉 T5 逐字锚 + T8(b) 注入实测（不能只看 exit 0）。
5. **KI-08 语义改写既有 skill**：旧句「判定时加权」必须除净——钉 T4 反向断言 + T7 态 2 反向锚（grep 旧句命中数 = 0）。

## 契约矩阵

| # | 契约 | 逐字内容 / 形态 | 定义任务 | 消费任务 |
|---|---|---|---|---|
| M1 | forge 名 | `trans-forge`（逐字，全小写连字符） | T3 | T3/T4/T5/T6/T7/T8/T9 |
| M2 | 分支判别式 | 「与 ingest 域 = 产出新文档 vs 收编本文档不改写；与 spec 域 = 收编区外单篇 plan 驱动 vs 工件区内生产/修订」 | T4（入口 Step 1） | T3（分工节逐字一致）/T7 态 2 锚（锚子串逐字 = 「产出新文档 vs 收编本文档不改写」「收编区外单篇 plan 驱动 vs 工件区内生产/修订」两条，不含前导标点） |
| M3 | 出口三证名 | `溯源完整证` / `增量真实证` / `可收编译演证` | T3 | T7 态 1 锚/T9 判据 |
| M4 | 三停点 | 停点①=映射设计表上裁定；停点②=自增 D（待评审）+Q 表上裁定；停点③=出口门证不过不迁移（停点①不含形状级未知——那归停点②的未知分类规则） | T3 | T9（彩排以「最可能假设落笔+全量登记」代替①②人工裁定——彩排限定，真实使用必停） |
| M5 | 准入三判据 | ①决策注册表存在（D 条目）；②路线已裁定；③现状断言有实证密度（file:line 或实测数据可核）。缺一即拒绝进入并上报 | T3 | T9（flow-builder plan 通过性已证：§10 D0–D5 + §2 路线决策 + 附录 file:line 清单，2026-09-23 选材实证） |
| M6 | 收编预案路径 | `.campaign/ingest/<slug>/{profile.md, mapping.md, q-table.md, evidence-register.md, exit/{lint.txt, coverage.txt, q-check.txt}}`（文件名与 ingest-forge 出口逐字一致） | T3 | T9 |
| M7 | spec-context.sh case 行 | `  plan-forge\|spec-forge\|ingest-forge\|trans-forge\|program-forge) ;;`（两空格缩进，逐字；**单元格内 `\|` 仅为 markdown 表格转义——文件真实内容是裸 `|` 交替符，写入 hook 时禁带反斜杠**） | T5 | T7 态 3 锚/ac-90 适配锚 |
| M8 | 版本号 | `0.5.0` 三处：plugin.json + marketplace.json + .claude-plugin/marketplace.json；两 marketplace 逐字节同形 | T6 | T7 态 4/ac-90 check 4 适配 |
| M9 | ac-92 契约 | `campaign/acceptance/ac-92-trans-forge.py`；首行 PASS/FAIL、全过 exit 0 / 任一 BAD exit 1（run_all.py 归类契约，同 ac-90 docstring） | T7 | T7 验证 |
| M10 | 彩排写入清单（flow-builder 工程内，全 additive） | ① `docs/spec/<执行日>-multi-tenant-saas-rehearsal-需求规格与技术架构方案.md`；② `.campaign/ingest/multi-tenant-saas-rehearsal/` 五件套（M6）；③ `.campaign/ingest/multi-tenant-saas-rehearsal/graph/graph.json`（**build 的 `--out` 收目录**：`--out <…/multi-tenant-saas-rehearsal/graph>`，build 落 graph.json 于其内（doc_graph.py:233 实测）——禁把本行文件路径直接喂给 --out，会产出 `graph.json/graph.json` 套娃；既有 `.campaign/graph/graph.json` 为他线产物（2026-09-23 实测在案），禁覆写）；④ `.gitignore` 追加 `.campaign/` 一行（仅当该文件存在且缺此行） | T9 | 风险 R3 回滚依据 |
| M11 | 域地图新行 | `\| trans-forge \| 转化：成熟方案文档 → 可收编规格文档（转化先于收编） \|` | T4 | T7 态 2 锚 |
| M12 | KI-08 新句 | 「仅在域信号弱命中或难裁时作倾向参考，不单独定域」 | T4 | T7 态 2 锚（正向）+ 反向锚（旧句「判定时加权」命中数=0） |
| M13 | genre 模板节序 | §0 文档说明（读者/术语/需求复述/已确认决策注册表）→ §1 项目概述 → §2 现状调研与实证 → §3 需求规格（角色/FR/NFR/Q 注册表）→ §4 关键技术决策 → §5 总体架构 → §6 详细设计 → §7 部署与运维 → §8 实施计划（里程碑/AC）→ §9 风险与对策 → §10 待决策事项 → 附录 A 配置默认值 / B 实证索引 / C 引用来源（共 14 个 `##` 节：§0–§10 十一节 + 附录 A/B/C 各自成节；AeroFold 实例为 13 节，附录仅 A/B 两件，模板新增附录 C） | T2 | T3 工序 2 引用/T9 产物结构判据 |
| M14 | 映射设计表表头 | `\| 源节 \| 节标题 \| 处理法(照录/扩写/新写/归属调整/丢弃) \| 目标节 \| 理由（含丢弃理由） \|` | T2 | T3 工序 2/T9 产物判据 |
| M15 | 彩排报告路径 | `F:\workspaces\campaign-suite\.campaign\rehearsal\trans-forge-golden-2026-09-23.md`（.campaign/ 已 gitignore，2026-09-23 实证 .gitignore 含该行） | T9 | T10 复盘输入 |

## 任务块

### T1 references 案例库三件（新建）

画像: 性质=文档; 难度=集成; 领域词=[参考案例库, flow-builder 案例剖析, AeroFold 骨架, ID 规范]

步骤：
1. 新建 `campaign/skills/trans-forge/references/case-flow-builder.md`：flow-builder 案例剖析。素材源 = `F:\workspaces\campaign-suite\.caliber\case-flow-builder-analysis.md`（已落盘，含映射实例表/14 纪律/9 反模式/可收编性自白——行号指针以其「文档名+章节号为主锚、行号为辅锚」口径转写）；内容定型为四节：①plan§→spec§ 映射实例表（照录/扩写/新写/归属调整四类各 ≥2 例）；②14 条方法纪律**以表格行呈现（每条一表行）**（三类陈述分离/照录标注/D 逐字+落点列/决策三态注册/TODO 纪律/Q-D 绑定/AC 可证伪/稳定编号/证据分级复核/不推翻红线/选型诚实声明/结构与内容分离/注册式扩展/一节一需求），每条附案例原文例句指针（文档名+章节号为主锚；行号一律标注 `as-of spec 1514 行版，2026-09-23 剖析时点`——剖析时点全文 1514 行，复测时点已 1622 行（同日该文档持续编辑），故行号一律以章节号锚为主、行号为辅锚；③9 条反模式教训**以表格行呈现（每条一表行）**（§0 三路混投 / P 前缀撞 P0·P95·P256 / FR-3.x 通配引用 / R 表乱序 / TODO 同义异名两例 / file:line 路径前缀不统一 / 同文件行号区间两说不一致 / FR-8.8 与 FR-7.7 内容重复 / 附录 A TODO 重复登记）；④本案例可收编性时间线自白（带时间戳事实，反「只宣称未验证」一课）：剖析时点（2026-09-23 上午）工程无 .campaign/、从未真实收编；同日 17:25 前已由并发会话完成首次真实收编（`.campaign/ingest/multi-tenant-saas/` 五件套 + `.campaign/graph/graph.json` 在案；映射 15 数据行 = 高 10 / 中 5 / 低 0，q-table pending=0——2026-09-23 18:02 后实测）——案例的可收编性由此从「未验证」转为「已实测」，该实测分布同时成为 genre 可收编性的第二个校准点。**转写前必须先实测 `ls F:/workspaces/flow_builder/flow-builder/.campaign/ingest/` 复核本时间线仍成立**（活工程，事实可能再漂移；漂移则按实测重写本段）。三件落盘后按 C10 提交（与 T2 合并为一个 commit，显式路径暂存三件）。
2. 新建 `campaign/skills/trans-forge/references/skeleton-aerofold.md`：AeroFold 实例骨架与校准数据。四节：①AeroFold 13 节实例骨架清单（§0–§10 + 附录 A/B，逐节一句话内容概括；并一行注明与本模板 M13 的 14 节节序差异 = 模板新增附录 C 引用来源）；②七套 ID 注册表形态（FR/NFR/C/D/Q/R/AC 七前缀各一条真实例句）+ ADR 预登记形态；③消费链锚点形态（程序单元 brief 的 SRS 锚点区真实形态：FR 编号+文档相对路径+行号三级锚定，引 U-M1-02-brief 实例一段）；④收编校准数据（2026-09-23 直测：映射 13 数据行 = 高 9 / 中 4 / 低 0，13/13 节覆盖，q-table 25 行全 resolved→C）+ spec 完备性清单（转化产物的必备面：角色权限矩阵/FR 验收标准列/NFR 量化+测量方式/DDL/API 契约/状态机/威胁模型/AC 可证伪/配置默认值/实证索引——案例 architect 交付报告所列 15 项源缺口（清单在 `.caliber/case-flow-builder-analysis.md` 附录，出处可达）提炼为前列 10 项必备面）。
3. 新建 `campaign/skills/trans-forge/references/id-grammar.md`：ID 体系规范。内容：前缀白名单 = FR/NFR/R/D/C/Q/AC（七前缀，与 doc_graph 词法一致）；禁单字母 `P` 作前缀（撞 P0 优先级/P95 分位/P256 曲线——案例实证）；稳定编号只增不改；正文禁通配引用（`FR-3.x`），组引用用「FR-3 全组」注记形态；区间引用（`FR-2.1–2.4`）仅允许出现于索引/锚点区；TODO token 语法 = `TODO-<主题>:`（一处值一 token，禁斜杠复合，禁同义异名）；doc_graph 组 ID 叙事性加粗误报 duplicates 为已知限制（指针 `campaign/tools/doc_graph.md` 已知限制节）。

Interfaces:
- Consumes: `F:\workspaces\campaign-suite\.caliber\case-flow-builder-analysis.md`（案例剖析素材，已落盘）；`F:\workspaces\AeroFold\docs\AeroFold-需求规格与技术架构方案.md`（2596 行，2026-09-23 实测）；`F:\workspaces\AeroFold\.campaign\program\U-M1-02-brief.md`（消费链锚点实例）；`F:\workspaces\AeroFold\.campaign\ingest\aerofold-srs\mapping.md`（收编校准实例）；M13；C7 校准数值
- Produces: 三文件落盘；被 T3（references 使用说明节）与 T7 态 5 锚消费

验证：
- `ls campaign/skills/trans-forge/references/` → 逐字三文件：`case-flow-builder.md` `skeleton-aerofold.md` `id-grammar.md`
- `grep -c '^|' campaign/skills/trans-forge/references/case-flow-builder.md` ≥ 20（映射实例+纪律+反模式均为表行）
- `grep -cF '高 9 / 中 4 / 低 0' campaign/skills/trans-forge/references/skeleton-aerofold.md` → 1
- `grep -F 'TODO-' campaign/skills/trans-forge/references/id-grammar.md | grep -cF '一处值一 token'` → ≥ 1

### T2 templates 两件（新建）

画像: 性质=文档; 难度=集成; 领域词=[genre 模板, solution-spec 骨架, 映射设计表]

步骤：
1. 新建 `campaign/skills/trans-forge/templates/solution-spec-template.md`：genre 骨架模板，节序逐字按 M13。每节含三行机注：①`工件归属:`（SRS.md / architecture.md / adr/ / research/ / plan.md / risks.md / DECISIONS.md 七枚举其一，与 ingest-forge 判别指引逐字一致）；②`出处标签:`（照录源方案 §x / 扩写源方案 §x / 新写（spec 阶段新增，待评审） 三枚举占位）；③填写要点（≤3 行，含该节的反模式警告——§0 节注「决策注册表与待决项必须子节隔离并显式声明归属」；§3.4 注「Q 注册表每条绑定 §10 D 号」；§10 注「待决项唯一登记点，他处禁重复登记」）。混合节（§0/§2/§4/§6/§7/§8）头部加 `子节归属声明` 占位行。
2. 新建 `campaign/skills/trans-forge/templates/mapping-design-template.md`：映射设计表模板，表头逐字按 M14，附三行填写规则（每个源 plan `##` 节恰一行；处理法五枚举；丢弃必须给理由）+ 一行示例（照录 plan §10 决策表 → 目标 §0.4 已确认决策注册表，处理法=照录）。两模板落盘后按 C10 提交（与 T1 合并，显式路径暂存）。

Interfaces:
- Consumes: M13/M14；AeroFold genre 形态（references/skeleton-aerofold.md，T1 产出）
- Produces: 两文件落盘；被 T3 工序 2 引用、T7 态 1 锚、T9 产物结构判据消费

验证：
- `grep -F '工件归属:' campaign/skills/trans-forge/templates/solution-spec-template.md | wc -l` → ≥ 14（14 个 `##` 节每节一行，M13）
- `grep -F '子节归属声明' campaign/skills/trans-forge/templates/solution-spec-template.md | wc -l` → ≥ 6（六个混合节）
- `head -20 campaign/skills/trans-forge/templates/mapping-design-template.md | grep -F '处理法(照录/扩写/新写/归属调整/丢弃)'` → 命中 1 行

### T3 trans-forge SKILL.md + checklists.md（新建，核心设计件）

画像: 性质=文档; 难度=判断; 领域词=[trans-forge 五工序, 出口三证, 三停点, 分工节, 转化纪律]

步骤：
1. 新建 `campaign/skills/trans-forge/SKILL.md`，frontmatter：`name: trans-forge`；`description` 含触发信号（成熟方案/plan 文档 → 需求规格文档的转化）与两条排除句（非规范存量收编 → ingest-forge；从零生产/工件区修订 → spec-forge）；`metadata: version: "0.1.0"`、`source: campaign-w6`（C9）。正文节序：
   - 开篇定位：转化锻造——收编区外的上游生产者；流水线位置 trans「转」→ ingest「收」→ spec「写」→ program「编排」（数据流水线序，与 D-2 入口仲裁序 program→ingest→trans→spec 不同，二者勿混）；本 skill 形态 = 五工序 + 三停点 + 出口三证（速查行，与 M3/M4 逐字一致）。**三停点** = 停点①映射设计表上裁定 / 停点②自增 D（待评审）+Q 表上裁定 / 停点③出口门证不过不迁移——三处定义句须写全（验证对「停点」计数 ≥6，速查行以外的定义句不足会被后续 grep 计漏）。
   - 依赖验证（C2 一行）：缺 doc_graph.py / ingest-forge 模板 / spec-forge 机制指针任一 → 上报不继续。
   - 输入：成熟 plan 文档路径 + slug（默认从文件名派生）。
   - 工序 1 选材：准入三判据（M5，缺一即拒绝并上报，指引回 caliber plan-forge/deep-probe 补 plan）；plan 节级解析（机械支撑 `python campaign/tools/doc_graph.py profile <plan>`）；实证抽查（plan 引用的 file:line 逐一复核，有漂移即上报）；缺口清单对照（指针 references/skeleton-aerofold.md 完备性清单）；Q 预选。
   - 工序 2 制坯：填映射设计表（指针 templates/mapping-design-template.md）→ **停点①**（M4）；按 genre 骨架制坯（指针 templates/solution-spec-template.md）；三类陈述分离纪律（用户裁定逐字 / 源方案设计判断标注 / spec 阶段新增待评审）；七工件物理分章律（`##` 节单一工件归属，混合节显式子节归属声明）；ID 规范（指针 references/id-grammar.md）；两态标记与 TODO 纪律（机制摘要一句 + 指针 spec-forge 工序 2）。**L1 歧义词表仅以指针引用（spec-forge 工序 2 / spec-lint hook），禁在 SKILL.md 与 checklists.md 正文内联七词词表**——T3 验证对该两文件跑 L1 grep 期望 0 命中，内联词表 = 规则定义自嵌假阳性。
   - 工序 3 锻打：规格增量生成（溯源必填律：每条 FR/NFR 答得出源节/D 条目/实证行，答不出标「spec 阶段新增，待评审」；未知分类规则：形状级 → 停点②，参数级 → TODO 注册+最可能假设落笔）；对抗审查 = 机制摘要一句 + 指针 spec-forge 工序 3（SRS 五视角+双声部+B5 evidence-auditor 全套；B5 = 证据口径审计专责，`campaign/agents/evidence-auditor.md`，审计全部新增定量断言——as-of 2026-09-23 仅一份 agent 定义文件，未发现已注册 skill 版）+ 第六视角「可收编性」（细目在 checklists.md 工序 3 节）→ **停点②**（M4，Q→C 机制指针 ingest-forge 第三步）。
   - 工序 4 成型：fresh 读者理解性测试，范围 = FR/AC/契约节（D-4 裁剪制；机制摘要一句 + 派遣 prompt 骨架指针 spec-forge checklists.md 工序 4 节）。
   - 工序 5 出口门三证（M3）：**溯源完整证**（映射设计表 100% 覆盖源节含丢弃理由；plan 每条 D 在产物逐字可查且有落点指针；实证索引附录落盘）；**增量真实证**（`doc_graph.py profile` 判 FR/NFR/AC 计数非零、NFR 过 L3 数值 lint；全节照录=换皮重排打回）；**可收编译演证**（试映射判据：低置信=0、中置信行必须带显式子节归属——AeroFold 实测校准；Q 表候选仅限源注册表沿用+停点②遗留；spec-lint L1/L2/L3 离线复跑零命中；`doc_graph.py build` 建图成功）→ **停点③**（M4）。三证过 → 双产物落盘：转化文档 `docs/spec/<date>-<slug>-需求规格与技术架构方案.md` + 收编预案五件套（M6）。
   - 分工节三节：与 ingest-forge（判别式 M2 逐字 + 收编预案 replay 语义：预案=其产物预演，真实 ingest 验证 replay 非发现）；与 spec-forge（判别式 M2 逐字）；与 caliber（转化内对抗审查/彩排机制全指针调用，不复制）。
   - 参考案例库节：references/ 三件角色（参照骨架/方法纪律/反模式教训）+ 一句警示（案例是参照不是临摹对象——纪律经闸门传递，不经样例传递）。
   两文件落盘后按 C10 提交（显式路径暂存两文件，独立 commit）。
2. 新建 `campaign/skills/trans-forge/checklists.md`（「进到哪道工序读哪节」组织，与 spec-forge checklists.md 同构）：工序 1 节（准入判据操作化+实证抽查回收检查）；工序 2 节（映射设计表 100% 覆盖检查/出处标签/分章律/ID 规范自检——含 q-table 全角 `｜` 规则行，C5）；工序 3 节（溯源必填律检查 + 可收编性视角细目：一节一投/ID 规整/Q 收敛/干跑预过）；工序 4 节（彩排派遣 prompt 骨架指针 spec-forge `checklists.md` 工序 4 节——`campaign/skills/spec-forge/checklists.md:74` 起；ac-92 静态闸范式参照 `campaign/acceptance/ac-91-brief-conventions.py`）填槽 `{DELTA_PATH}`（= 彩排 spec 草稿路径；真实使用 = 本轮新增/变更的 FR 范围或定量断言行集） `{SCOPE=FR/AC/契约节}` + 回收检查三条）；工序 5 节（三证逐条操作化判据+机械命令+期望形态，数值锚 = C7 校准口径）。

Interfaces:
- Consumes: M1–M6/M13/M14 全矩阵；T1/T2 产物；C1/C2/C5/C9
- Produces: trans-forge skill 本体；M2/M3/M4/M5 的定义点；被 T4（入口信号）/T7 态 1 锚/T8/T9 消费

验证：
- `grep -cF '停点' campaign/skills/trans-forge/SKILL.md` → ≥ 6（三停点定义+引用+速查行）
- `grep -cF '五工序 + 三停点 + 出口三证' campaign/skills/trans-forge/SKILL.md` → ≥ 1（速查行逐字形态）
- `grep -F '溯源完整证' campaign/skills/trans-forge/SKILL.md && grep -F '增量真实证' campaign/skills/trans-forge/SKILL.md && grep -F '可收编译演证' campaign/skills/trans-forge/SKILL.md` → 三行各命中
- `grep -nE '适当|尽量|必要时|按需|尽快|优化|友好' campaign/skills/trans-forge/SKILL.md campaign/skills/trans-forge/checklists.md` → 0 命中（L1 自律）

### T4 campaign 入口 SKILL.md 修订（既有文件，66 行基线）

画像: 性质=重构; 难度=集成; 领域词=[campaign 入口域判定, 第四分支, KI-08 加权操作化, description 信号]

步骤（锚串均引自 2026-09-23 直读原文）：
1. frontmatter description（当前第 3 行）：在 `producing or revising an SRS` 前插入 `transforming a mature plan/solution document into an ingestible SRS (成熟方案文档 → 需求规格文档), `；路由链 `域判定 → ingest-forge / spec-forge / program-forge` 改为 `域判定 → ingest-forge / trans-forge / spec-forge / program-forge`。metadata version `0.1.0` → `0.2.0`；metadata source `campaign-w5` → `campaign-w6`（审查裁定档 .caliber/review-logs/2026-09-23-trans-forge-plan.md（R1-F28/Taste-3）——source 记最近实质改版波次，与 version 语义一致，C9）。
2. Step 0（第 15 行）：``查 `campaign:ingest-forge` / `campaign:spec-forge` / `campaign:program-forge` 三 forge``（含反引号）改为 ``查 `campaign:ingest-forge` / `campaign:trans-forge` / `campaign:spec-forge` / `campaign:program-forge` 四 forge``（反引号保留）。
3. Step 1 引言（第 24 行）：`按序过四条分支` → `按序过五条分支`。
4. Step 1 分支表（第 26–29 行）：在第 2 条（ingest 域）后插入新第 3 条：``3. trans 域：转化成熟方案文档为可收编规格文档——plan/方案文档在途（决策注册表与路线已裁定）且目标 = 产出需求规格文档 → 进 `campaign:trans-forge`。判别：与 ingest 域 = 产出新文档 vs 收编本文档不改写；与 spec 域 = 收编区外单篇 plan 驱动 vs 工件区内生产/修订。``（`campaign:trans-forge` 含反引号，与相邻分支行形态一致）；原第 3 条（spec 域）改编号 4；原第 4 条（非本域）改编号 5。
5. 歧义行（第 37 行）末尾追加：`「转化后接收编」类复合任务 = 先 trans 后 ingest，顺序规则已覆盖，不算歧义。`
6. 辅助信号行（第 33 行，KI-08）：`工程处于 campaign 工件区拓扑内，判定时加权；不存在不否决（新工程可从 ingest 起步）` 改为 `工程处于 campaign 工件区拓扑内——仅在域信号弱命中或难裁时作倾向参考，不单独定域；不存在不否决（新工程可从 ingest 或 trans 起步）`。
7. 域地图表（第 47–51 行）：ingest-forge 行后插入 M11 行（M11 域地图行逐字 = `| trans-forge | 转化：成熟方案文档 → 可收编规格文档（转化先于收编） |`——markdown 表格单元格内的 `\|` 仅为渲染转义，实文写入 SKILL.md 时须用裸 `|` 与两侧空格）。
8. 与 caliber 的分工（第 64 行）：`命中四信号` 改为 `命中域信号`（旧串逐字，锚引自 2026-09-23 直读原文）。落盘后按 C10 提交（与 T5/T6 合并，显式路径暂存 T4 改动件 `campaign/skills/campaign/SKILL.md`）。

Interfaces:
- Consumes: M1/M2/M11/M12；C6（≤100 行约束）
- Produces: 入口第四分支；被 T7 态 2 锚/T8 口试消费

验证：
- `wc -l campaign/skills/campaign/SKILL.md` → ≤ 100（C6；基线 66 行，预计 ≤80，以实测为准）
- `grep -F '按序过五条分支' campaign/skills/campaign/SKILL.md` → 命中 1 行
- `grep -F '3. trans 域' campaign/skills/campaign/SKILL.md` → 命中 1 行；`grep -F '4. spec 域' ...` 与 `grep -F '5. 非本域' ...` 各命中 1 行
- `grep -cF '判定时加权' campaign/skills/campaign/SKILL.md` → 0（KI-08 反向断言）；`grep -F '不单独定域' ...` → 命中 1 行
- `grep -F '| trans-forge | 转化：成熟方案文档 → 可收编规格文档（转化先于收编） |' campaign/skills/campaign/SKILL.md` → 命中 1 行（M11）
- `grep -F 'version: "0.2.0"' campaign/skills/campaign/SKILL.md` → 命中 1 行

### T5 spec-context hook 名单 + 契约文档同步

画像: 性质=配置; 难度=机械; 领域词=[spec-context.sh case 行, hooks 契约文档]

步骤：
1. `campaign/hooks/spec-context.sh` 第 20 行（当前逐字 `  plan-forge|spec-forge|ingest-forge|program-forge) ;;`）改为 M7 逐字形态。注释集合跨第 3–4 两行且第 4 行带行首 `# `（2026-09-23 实文：`…{plan-forge, spec-forge,` 换行 `# ingest-forge, program-forge}…`）——在第 4 行 `ingest-forge,` 后插入 `trans-forge, `，保持行首 `# ` 与换行形态（或把两行重排为一行注释，二选一，禁漏改）。第 18 行 `$SKILL="${SKILL##*:}"` 做 `campaign:` 插件前缀剥离（`campaign:trans-forge` → `trans-forge` 后入 case 匹配）——本 case 行因此**必须只写裸名、禁带 `campaign:` 前缀**。落盘后按 C10 提交（与 T4/T6 合并，显式路径暂存 T5 改动件 `campaign/hooks/spec-context.sh` 与 `campaign/hooks/spec-context.md`）。
2. `campaign/hooks/spec-context.md` 行为节第 2 条：skill 集合（实文逐项带反引号：`` skill ∈ {`plan-forge`, `spec-forge`, `ingest-forge`, `program-forge`} ``）改为含 `trans-forge` 的五件集合（逐项反引号形态保持）。

Interfaces:
- Consumes: M1/M7
- Produces: hook 对 trans-forge 注入能力；被 T7 态 3 锚/T8(b) 实测消费

验证：
- `grep -nF 'plan-forge|spec-forge|ingest-forge|trans-forge|program-forge) ;;' campaign/hooks/spec-context.sh` → 命中 1 行（注意 grep -F 逐字，管道符不转义）
- `grep -cF 'trans-forge' campaign/hooks/spec-context.md` → ≥ 1
- 运行时注入冒烟不在本任务验证范围——归 T8 步骤 2（图文件前置条件在 T8 处理）

### T6 版本与描述同步（manifests + README）

画像: 性质=配置; 难度=机械; 领域词=[plugin.json 0.5.0, marketplace 双份同形, description 信号]

步骤：
1. `.claude-plugin/marketplace.json` 存在（2026-09-23 实证，ac-90 docstring 三处契约成立）——本任务改三处。
2. `campaign/.zcode-plugin/plugin.json`：`"version": "0.4.0"` → `"0.5.0"`；description 在 `ingest-forge/spec-forge/program-forge` 处改为 `ingest-forge/trans-forge/spec-forge/program-forge`。
3. `marketplace.json` 与 `.claude-plugin/marketplace.json`：plugins[0] 的 `"version"` → `"0.5.0"`；description 逐字替换——旧串 `ingest-forge / spec-forge / program-forge 三 forge` → 新串 `ingest-forge / trans-forge / spec-forge / program-forge 四 forge`（2026-09-23 实文核对旧串逐字存在，含斜杠两侧空格）；保存后两份 marketplace 逐字节同形（C6——逐字节复制其中一份到另一份，不做手工对齐）。

4. `README.md` 同步「四处」（W5 先例 commit 33b5cca：README 随版本 bump 同 commit 更新——README 是本仓维护中的同步目标；锚串 2026-09-23 实证在案，执行时先 `grep -n` 复核实文，被他线编辑过则以实文为准。「四处」= 编号 ①②③ 三处正文改动 + ②内部嵌 version 字符串一次——第 48 行内嵌 plugin.json 引用块的 version 与第 5 行的 bump 是同一次 0.4.0→0.5.0 替换的第 ④ 个落点，合计四处改动）：① 第 5 行 `campaign v0.4.0` → `campaign v0.5.0`、`三个 forge skills（ingest-forge / spec-forge / program-forge）` → `四个 forge skills（ingest-forge / trans-forge / spec-forge / program-forge）`；② 第 20 行 `域判定（四信号+顺序仲裁）→ 路由三 forge` → `域判定（域信号+顺序仲裁）→ 路由四 forge`；③ 第 48 行内嵌 plugin.json 引用块 `"version":"0.4.0"` → `"version":"0.5.0"`。落盘后按 C10 提交（与 T4/T5 合并，显式路径暂存 T6 改动件 `campaign/.zcode-plugin/plugin.json` / `marketplace.json` / `.claude-plugin/marketplace.json` / `README.md`）。

Interfaces:
- Consumes: M1/M8
- Produces: 三处 0.5.0 + README 四处同步；被 T7 态 4/ac-90 check 4 适配消费（README.md 入 T1–T7 修改路径穷举，态 6 白名单天然覆盖）

验证：
- `python -c "import json,os; [print(json.load(open(p,encoding='utf-8'))['version'] if os.path.basename(p)=='plugin.json' else json.load(open(p,encoding='utf-8'))['plugins'][0]['version']) for p in ['campaign/.zcode-plugin/plugin.json','marketplace.json','.claude-plugin/marketplace.json']]"` → 三行均 `0.5.0`（判别按 basename：'.claude-plugin/marketplace.json' 路径含 'plugin' 子串，按子串判别会 KeyError）
- `cmp marketplace.json .claude-plugin/marketplace.json` → 零输出（逐字节同形；Git Bash 下 `fc` 是 shell 历史内建，不可用）
- `grep -cF 'trans-forge' marketplace.json campaign/.zcode-plugin/plugin.json` → 各 ≥ 1
- `grep -cF 'trans-forge' README.md` → ≥ 1；`grep -cF 'v0.5.0' README.md` → ≥ 1（README 同步锚）

### T7 acceptance 层：ac-90 适配 + ac-92 新建 + run_all 全量

画像: 性质=新增; 难度=集成; 领域词=[ac-92 静态闸, ac-90 版本适配, run_all PASS]

步骤：
1. 适配 `campaign/acceptance/ac-90-entry-skill-smoke.py`：check 4 版本期望 `0.4.0` → `0.5.0`（docstring 同步）；**check 2 两锚同步**：`0.1.0` → `0.2.0`、`campaign-w5` → `campaign-w6`（随 T4 步骤 1 的 source 字段改动，审查裁定档 .caliber/review-logs/2026-09-23-trans-forge-plan.md）**——含 check2 函数 docstring 内同名锚**（ac-90 docstring 是 C6 契约载体，漏改则契约自相矛盾）；check 5 若对 case 行做逐字串断言 → 更新为 M7 新行（实现时先读该检查实际断言串再改，禁凭猜测）；check 3 锚文本逐条核对 T4 后的 campaign SKILL.md 仍匹配，不匹配处同步锚文本。**check6① 去留裁定 = 保留不改**——T5 对 hooks 的改动经 C10 提交纪律落 commit 后 diff-HEAD 归零，守卫自然通过（前置条件 = C10，若 run_all 时仍有未提交改动则 check6① BAD 属设计内拦截，不是误红）。docstring 中「C8 六项检查」语义保持（本步为既有验收的基线适配，非新增检查；该「C8」是 ac-90 内部对六项检查集合的命名，与本 plan 契约矩阵 C8 同名异义，勿混）。
2. 新建 `campaign/acceptance/ac-92-trans-forge.py`（范式 = ac-90/ac-91：REPO_ROOT 自 `__file__` 推、utf-8 显式、subprocess text+encoding+errors、git 异常记 SKIP 降级、首行 PASS/FAIL + 明细 ok/BAD、exit 契约同 M9）。六态：
   - 态 1：trans-forge 七文件全在（SKILL.md/checklists.md/templates 两件/references 三件）+ SKILL.md 锚：三证名（M3）各 ≥1、停点①②③（M4 关键词）各 ≥1、准入判据行（M5 关键词「缺一即拒绝」）、分工节三节标题锚子串 = `与 ingest-forge` / `与 spec-forge` / `与 caliber` 各 ≥1。
   - 态 2：campaign SKILL.md 锚：`按序过五条分支`/`3. trans 域`/判别式两子串逐字 = `产出新文档 vs 收编本文档不改写` 与 `收编区外单篇 plan 驱动 vs 工件区内生产/修订`（M2，不含前导标点）/M11 域地图行/M12 新句；反向锚：`判定时加权` 命中数=0；行数 ≤100。
   - 态 3：spec-context.sh 含 M7 逐字行；spec-context.md 含 `trans-forge`。
   - 态 4：三 JSON version==0.5.0；两 marketplace 逐字节同形；plugin.json 与 marketplace.json description 含 `trans-forge`。
   - 态 5：references 锚：skeleton-aerofold.md 含 `高 9 / 中 4 / 低 0`；id-grammar.md 含 `一处值一 token`；case-flow-builder.md 含 `反模式` 节标题。
   - 态 6：零触碰守卫——`git status --porcelain` 全量输出中，本 wave 文件清单（穷举进脚本：T1–T7 全部新建/修改路径 + 本 plan 文件 `docs/plans/2026-09-23-trans-forge-plan.md` + `docs/known-issues.md`）之外的路径数 = 0（KI-09 教训：用 porcelain 不用 diff HEAD，兼捕未跟踪新文件）。预存基线豁免逐字登记进脚本：`?? campaign/tools/__pycache__/`（2026-09-23 git status 快照所载的 wave 前已存在未跟踪目录；`.caliber/` `.campaign/` 已 gitignore（.gitignore 第 1–2 行，2026-09-23 实证），porcelain 不可见、天然豁免，不入白名单）。本态在 T1–T6 各 commit 落盘后跑（T7 自身的未提交改动由白名单吸收——ac-92 路径在穷举清单内）；porcelain 同时覆盖未提交遗留与清单外新件。落盘后按 C10 提交（显式路径暂存 ac-90/ac-92 与 run_all 若有改动）。
3. 查 `campaign/acceptance/run_all.py` 的脚本发现机制（glob 或显式列表）：显式列表则登记 ac-92；glob 则零改动。
4. 跑全量：`python campaign/acceptance/run_all.py`。

Interfaces:
- Consumes: M7/M8/M9；T1–T6 全部产物；C4/C6
- Produces: ac-92 六态；ac-90 适配版；run_all 全 PASS 证据

验证：
- `python campaign/acceptance/ac-92-trans-forge.py` → 首行 `PASS`，exit 0
- `python campaign/acceptance/ac-90-entry-skill-smoke.py` → 首行 `PASS`，exit 0（适配后）
- `python campaign/acceptance/run_all.py` → 汇总表格 AC 行全为 PASS（run_all 自身退出码恒 0，不承载判定——以汇总表为准，不看 exit 码）

### T8 插件卸载重装 + 冒烟（操作）

画像: 性质=操作; 难度=集成; 领域词=[插件卸载重装, 本地源无更新检测, spec-context 注入冒烟, 域判定口试]

步骤：
1. 卸载 campaign 插件并重装（本地 marketplace 源；机制事实：本地源无更新检测，重装=新事务+旧 cache 删除——AGENTS.md 插件实证事实）。**卸载/重装的确切命令形态本 plan 不预写**——执行时 Read 路由组件 plugin-creator 与 zcode-configuration-guide 正文取当前平台真实命令（候选组件，T8 注入档=指令化），禁凭记忆拼命令。重装后查会话 skill 清单出现 `campaign:trans-forge`。
2. 冒烟 (b) 注入/静默两行为实测。前置：工作目录 = 含 `.campaign/graph/graph.json` 的工程根（campaign-suite 仓有则直接用；缺则先 `python campaign/tools/doc_graph.py build campaign/skills/spec-forge/templates/srs-template.md` 建图——build 默认输出 `.campaign/graph/`，2026-09-23 实证）。逐字两条：
   - 注入态：`echo '{"tool_input":{"skill":"campaign:trans-forge"}}' | bash campaign/hooks/spec-context.sh` → 期望 stdout 为单行 JSON 信封，含子串 `doc-graph: nodes=`；
   - 静默态：`echo '{"tool_input":{"skill":"foo"}}' | bash campaign/hooks/spec-context.sh` → 期望零输出（stdout 为空）。
3. 冒烟 (c) 域判定口试三例，操作形态（审查裁定档 .caliber/review-logs/2026-09-23-trans-forge-plan.md，2026-09-23）：**经 Skill 工具按名调用 campaign 入口、每次仅投一句触发语、记录其 Step 2 宣布行原文**（`域判定 <域名>，理由：…`）——禁以阅读入口 SKILL.md 文本推断代替真实调用（纸上自证不算数）：①「把这份改造方案 plan 转成需求规格文档」→ 期望宣布路由 `campaign:trans-forge`；②「收编这篇旧格式 SRS」→ 期望 `campaign:ingest-forge`；③「编排多单元程序推进 program.yaml」→ 期望 `campaign:program-forge`。三例全对 = 过；任何误判 = 回 T4 修判别式，重跑本步 + T7 态 2 + ac-92（改动按 C10 修复环纪律另计 commit）。**卸载/重装任一失败处置链**：M7 case 行已落盘 → `git revert` 该 commit（spec-context.sh 回滚）→ 已重装成功则重装恢复 wave 前基线；重装仍失败 → 按 R4 全量回滚 + 报用户，T8 本步与 T9 暂停。**热刷新兜底**：重装后若当前会话 skill 清单未出现 `campaign:trans-forge`，记台账断点（事件+已验证项），切新会话继续本步与 T9——不凭旧清单强行口试。

Interfaces:
- Consumes: T1–T7 全部；M1
- Produces: 安装态生效证据（口试三例结果进 T9 彩排报告附录）

验证：
- 会话 skill 清单含 `campaign:trans-forge`（重装后新会话首屏核对）
- 冒烟 (b) 两行为实测记录（注入信封 JSON 一行 / 静默零输出）
- 口试三例路由全对（记录判定原文行）

### T9 金样回归彩排（flow-builder 真实跑 + 三证 + 不变量 + 既有收编复核与对拍实测）

画像: 性质=操作; 难度=判断; 领域词=[金样回归彩排, 出口三证实测, 不变量对拍, flow-builder 收编复核]

步骤：
1. 前置：**盘点既有 `.campaign/` 产物**（`ls -la F:/workspaces/flow_builder/flow-builder/.campaign/ingest/` 记录各件时间戳与来源——2026-09-23 已有并发会话收编产物 `multi-tenant-saas/` 在案；彩排与其共存规则 = 只写 rehearsal slug 路径、禁读改他线产物）；**记录素材 plan 基线**（`wc -l` + mtime——R7 假红防护；重锻时点实测 468 行 / mtime 10:09）；查 `.gitignore` 是否含 `.campaign/` 行（决定 M10④动作）；实证 flow-builder plan 过准入三判据（M5 通过性已在选材证实，此处落一行核对记录）。**工具路径纪律（全 T9 适用）**：doc_graph/spec-lint 命令一律以 campaign-suite 仓根为 cwd、目标文件传 flow-builder 绝对路径（或工具写绝对路径 `F:/workspaces/campaign-suite/campaign/tools/doc_graph.py`）——flow-builder 仓无 `campaign/tools/`（2026-09-23 实测），`cd` 到 flow-builder 后跑相对路径工具必挂。
2. 派遣转化执行（主线程编排，多派遣串行）：派遣 A = 工序 1-2（选材+映射设计表+制坯骨架）；派遣 B = 工序 3 增量生成（最重）；**派遣 B′ = 工序 3 对抗审查**（主线程在派遣 B 返回草稿后追加派遣，按 trans-forge 工序 3 全量编排：SRS 五视角+双声部+B5 evidence-auditor 审计全部新增定量断言，输入 = 彩排 spec 草稿路径——嵌套派遣不可用，审查由主线程编排骨葆独立性，金样彩排须测全过程链）；派遣 C = 工序 4（fresh 读者理解性测试，范围 FR/AC/契约节，D-4）。派遣均为 fresh 零背景 agent（派遣工具 = ZCode Agent，subagent_type `general-purpose`——K2.8 当前 dispatch 界面无 model 选择字段，用平台默认；dispatch 界面也不传文件，正文注入 = prompt 内给绝对路径 + 指令「先 Read 再动手」），输入 = trans-forge SKILL.md 与 checklists.md 全文（Read 注入）+ **references/ 三件正文或路径**（case-flow-builder/skeleton-aerofold/id-grammar——纪律与 ID 规范的执行依据）+ **被转化素材 plan 文档路径**（flow-builder plan，绝对路径 `F:\workspaces\flow_builder\flow-builder\docs\plans\2026-09-23-multi-tenant-saas-transformation-plan.md`——「plan」在此不指本 trans-forge plan 自身）+ slug=`multi-tenant-saas-rehearsal` + 彩排豁免令（M4：停点①②以「最可能假设落笔+全量登记」代替人工裁定——彩排限定）。产物路径按 M10①。**派遣 A 的报告必须全文带回映射设计表**（M14 形态），主线程将其落入 M15 彩排报告附录——溯源完整证的复核对象由此持久化（审查裁定档 .caliber/review-logs/2026-09-23-trans-forge-plan.md，2026-09-23）。
3. 主线程跑出口三证（M3 操作化判据 = checklists.md 工序 5 节）：溯源完整证（映射表 100% 覆盖 + plan D0–D5 六条逐字 grep 命中 6/6 + 落点指针）；增量真实证（profile 计数 FR/NFR/AC 非零、L3 过）；可收编译演证（试映射低置信=0、中置信带子节归属、lint 零命中、`doc_graph.py build <彩排spec> --out F:/workspaces/flow_builder/flow-builder/.campaign/ingest/multi-tenant-saas-rehearsal/graph` 建图成功——**--out 必须绝对路径**：相对 --out 按 cwd 解析会落进 campaign-suite 仓（doc_graph.py build 落点行为实测），与 M10③「flow-builder 工程内」逐字对齐；cwd 纪律见步骤 1）。**三证过后由主线程按工序 5 落盘双产物**：M10①转化文档（派遣 B′ 处置后的定稿）+ M10②收编预案五件套（试映射表/Q 表/证据登记/profile/exit 三件），③图已随建图命令落位。
4. 不变量对拍（彩排 spec vs 人工 spec）：I1 = D0–D5 六条逐字命中 6/6；I2 = TODO 纪律（数值断言无来源且无 TODO/两态标记的行数 = 0，机械 grep——spec-forge checklists.md 工序 2「两态标记自检」同款命令：`grep -nE '[0-9]+(\.[0-9]+)?[ ]*(%|ms|s|GB|MB|KB|万|倍|行)' <彩排spec路径> | grep -vE '【(证据|假设·验证=)'` → 期望零行；有行即 BAD 逐条登记）；I3 = 映射置信分布与 FR 组数/NFR 条数/TODO  token 数实测登记（D-5：记录不预断）。
5. 人工 spec 收编实测复核（「首次真实收编」已由并发会话于同日 17:25 前完成——本步改为**复核既有产物 + 对拍实测**，不再自跑收编，避免与在途工作互踩）：**人工 spec = monolith 绝对路径 `F:\workspaces\flow_builder\flow-builder\docs\spec\2026-09-23-multi-tenant-saas-需求规格与技术架构方案.md`**（`docs/spec/` 现有并发收编拆出的 SRS.md/architecture.md 等多件——profile 对象仅此 monolith，先 `ls` 该目录实测为准，禁凭猜测）；读既有 `.campaign/ingest/multi-tenant-saas/mapping.md` 与 `q-table.md`，记录置信分布（2026-09-23 18:02 后实测 = 高 10 / 中 5 / 低 0，15 数据行，q-table pending=0）与案例剖析 9 处一节多投预测的对拍结果（预测命中/被修复各几处——spec 当日持续编辑，部分缺陷可能已被并发会话修掉）；对人工 spec 复跑 `doc_graph.py profile`（cwd 纪律见步骤 1）记录 ids 行；结论（genre 第二校准点 + 案例库反哺素材）进报告。
6. 彩排报告落盘 M15：三证结果逐项 / I1–I3 实测 / 既有收编复核实测 / FR 组数等阈值原始数据 / **映射设计表附录（派遣 A 全文带回，审查裁定档 .caliber/review-logs/2026-09-23-trans-forge-plan.md）** / 对抗审查（派遣 B′）发现与处置记 / 口试三例（T8）附录 / 失败处置记录（若有）。
7. 失败处置链（Review Focus 3）：I1 或三证不过 → 回 T3 补 brief（明确缺口点）后重跑一次；两轮不过 → **停**，上用户裁定（贴两轮报告），并评估「专用 agent」挂起项触发。

Interfaces:
- Consumes: T1–T8 全部（重装后的 live trans-forge）；M3–M6/M10/M15；D-4/D-5
- Produces: 金样彩排证据链（三证+不变量+既有收编复核实测）；阈值原始数据（T10 消费）；flow-builder 彩排写入（M10 清单，additive）

验证：
- 彩排 spec 存在且 `python campaign/tools/doc_graph.py profile <彩排spec>` 输出 ids 行 FR≥1 / NFR≥1 / AC≥1
- D0–D5 逐字 grep（六条，子串取自 plan §10 原文）→ 命中 6/6
- 试映射表低置信行数 = 0；中置信行全带子节归属声明
- M15 报告存在且含三证三节 + I1–I3 + 既有收编复核实测节

### T10 收尾：登记表处置 + handoff 更新 + L 级首次全流程复盘

画像: 性质=文档; 难度=机械; 领域词=[known-issues 处置, handoff 更新, L 级复盘, learnings 固化]

步骤：
1. `docs/known-issues.md`：KI-08 状态 → closed（处置 = T4 落地 M12 句，证据 = ac-92 态 2 反向锚）；KI-02/KI-03/KI-05 各记一行消化行（trans-forge 落地两段式/依赖兜底/Q 表停点形态，证据指针 SKILL.md）；新增 KI 条目（q-table-template.md 注释 `\|` 与 SKILL.md 全角 `｜` 不一致，处置方向 = 模板注释行改全角，重访触发 = ingest-forge 下次升版）——**编号取当前最大 +1**（2026-09-23 重锻时点最大 = KI-14 → 用 KI-15；执行时先 `grep -oE 'KI-[0-9]+' docs/known-issues.md | sort -u | tail -1` 实测，若已被并发会话占用则顺延并记一行说明）。
2. `.campaign/handoff.md` 更新：当前单元行（trans-forge 建成 + 版本 0.5.0）、已过门行、待办行（D-5 阈值已首轮固化（步骤 5）、二轮真实使用时复核校准（触发器）/挂起项四条）、环境实测坑行追加本波新坑（若有）。
3. L 级首次真实全流程复盘（AGENTS.md 三 skill 锻造流水线义务）：对照四道工序（定级/澄清/锻造/审查）实际产出 vs 设计预期，失效/冗余环节成文报告用户并提议调整——落 `.caliber/trans-forge-L1-retro.md`。
4. learnings 固化评估：本波新型陷阱（若工序 3/彩排抓到平台级可复用陷阱）按三级回写规则处置（项目级 → 本仓 learnings；平台级 → caliber-suite checklists；流程级 → skill 本体升版）。
5. **D-5 阈值首轮固化**（R6① 触发器兑现——「先跑一轮再定阈值」）：读 M15 彩排报告首轮实测数据（FR 组数/NFR 条数/映射置信分布/TODO token 数），把金样判据阈值写入 `campaign/skills/trans-forge/checklists.md` 工序 5 节（每值标注「首轮实测固化 + 2026-09-23 + 数据源 M15」；本步之前 checklists.md 不含预造阈值——T3 工序 5 节只给判据形态不给数值）。

Interfaces:
- Consumes: T9 彩排报告（M15）/T1–T9 全部
- Produces: known-issues 处置记录；handoff 新生存包；L 级复盘报告；固化候选

验证：
- `grep -A6 '^## KI-08' docs/known-issues.md | grep -F 'closed'` → 命中（KI-08 状态行含 closed；标题行与状态行不同行，双 grep 管道直连会零命中）
- `grep -cF 'q-table-template' docs/known-issues.md` → ≥ 1（新 KI 条目落文——编号顺延条款下不钉死 KI-15）
- `grep -F 'trans-forge' .campaign/handoff.md` → 命中
- `grep -cF '首轮实测固化' campaign/skills/trans-forge/checklists.md` → ≥ 1（D-5 阈值固化锚，R6① 兑现证据）
- `ls .caliber/trans-forge-L1-retro.md` → 存在

## 执行编排预分配表

| 任务 | 性质 | 难度 | 形态 | 执行者 | 审查者 | 注入档 | 领域组件（预绑定） |
|---|---|---|---|---|---|---|---|
| T1 | 文档 | 集成 | dispatch | doc-writer → general-purpose | fresh 独立（general-purpose） | 指令化 | 无 |
| T2 | 文档 | 集成 | dispatch | doc-writer → general-purpose | fresh 独立（general-purpose） | 指令化 | [ingest-forge] |
| T3 | 文档 | 判断 | inline | 主线程 | fresh 独立（general-purpose） | N/A | [writing-great-skills, spec-forge, ingest-forge] |
| T4 | 重构 | 集成 | dispatch | coder → general-purpose | fresh 独立（general-purpose） | 指令化 | [writing-great-skills] |
| T5 | 配置 | 机械 | dispatch | coder → general-purpose | fresh 独立（general-purpose） | 无 | 无 |
| T6 | 配置 | 机械 | dispatch | coder → general-purpose | fresh 独立（general-purpose） | 无 | [plugin-creator] |
| T7 | 新增 | 集成 | dispatch | coder → general-purpose | fresh 独立（general-purpose） | 指令化 | 无 |
| T8 | 操作 | 集成 | dispatch | ops-operator → general-purpose | fresh 独立（general-purpose） | 指令化 | [plugin-creator, zcode-configuration-guide] |
| T9 | 操作 | 判断 | inline | 主线程 | fresh 独立（general-purpose） | N/A | [spec-forge, ingest-forge]（被测件本体除外） |
| T10 | 文档 | 机械 | dispatch | general-purpose | fresh 独立（general-purpose） | 无 | 无 |

注：本表 领域组件列 = 工序 4 Phase 2 彩排后经编排者裁定升级的**预绑定**（默认消费、偏离记 ledger Ruling、终审闭环核查）；候选判定依据 = 路由表（`.caliber/routing.yaml`，14 条，D-7）keywords × 任务画像领域词交集，消费契约见 C11（visible:false 组件按 `path` 字段 Read 注入、不安装）。

## 风险登记

| # | 触发条件 | 爆炸半径 | 可逆性 | 处置 |
|---|---|---|---|---|
| R1 | T4 判别式改动致既有三域误判 | 入口路由层 | git revert 可回 | T7 态 2 锚 + T8 口试三例拦截；误判实例进 known-issues |
| R2 | T9 彩排不变量/三证不过 | skill 设计返工 | 迭代可回 | 处置链：回 T3 补 brief 重跑一次；两轮不过 → 停上裁定 + 评估专用 agent 挂起项 |
| R3 | T9 写入 flow-builder（M10 清单） | 新增内容 ≤ 清单上限，全 additive（既有他线产物——并发会话的 `.campaign/graph/` 与 `.campaign/ingest/multi-tenant-saas/`——禁触碰，2026-09-23 实测在案） | 回滚 = 删 M10①文件 + 删 `.campaign/ingest/multi-tenant-saas-rehearsal/` 目录整体（②③同在其下）；④ 仅移除所追加的 `.campaign/` 一行，**不删 `.gitignore` 文件本体** | 清单穷举进彩排报告 |
| R4 | T8 重装失败或 cache 异常 | campaign 插件不可用 | `git revert` 本波 commit（C10 清单中**截至 T8 已入库的四个**：T1–T2/T3/T4–T6/T7——T10 commit 在 T8 后发生，按「C10 清单」找五个会扑空；`git stash` 对 clean 工作树是 no-op 且不收未跟踪新件，不可用）+ 按显式路径删除未跟踪新件（`campaign/skills/trans-forge/`、`campaign/acceptance/ac-92-trans-forge.py`——若尚未提交）+ 重装 | 回滚后重装验证：会话 skill 清单恢复 wave 前基线四行——`campaign:campaign` / `campaign:ingest-forge` / `campaign:spec-forge` / `campaign:program-forge`（无 `campaign:trans-forge`） |
| R5 | spec-context.sh 在 Windows Git Bash 静默失效 | hook 无注入（exit 恒 0 契约掩盖） | 单行 revert | T5 逐字锚 grep（T5 验证第 1 条）+ T8(b) 注入/静默两行为实测（T8 步骤 2 两条逐字命令），不只看 exit 0 |
| R6 | 延期决策 | — | — | ①金样判据阈值：触发器 = T9 首轮数据落地后 T10 固化；②ac-92 纳入 run_all 之外的合并闸：触发器 = 下一波 acceptance 整理窗（与 KI-09 同窗）；③ingest-forge/spec-forge SKILL.md 双侧分工指针补写（本 plan 单指针写法，trans-forge 侧承载全部分工节）：触发器 = 两 skill 下次升版时 |
| R7 | 素材 plan 在 T9 执行期被并发编辑（D0–D5 原文变动） | I1 六条逐字 grep 假红、彩排报告误判 | 复测即回 | T9 步骤 1 记录素材 plan 基线（`wc -l` + mtime——2026-09-23 重锻时点实测 468 行 / mtime 10:09 稳定）；I1 未命中时先比对基线再判：基线漂移 → 按新版 §10 原文重取六条子串并记台账，不直接判彩排失败 |

## 技能消费裁定

（plan-forge 工序 4 Phase 2 彩排回写，编排者逐条裁定；回收检查五条全过——Phase 1 纯度成立、建议表 10/10 覆盖、弃用逐条有理由、全局清单无来源建议、本裁定全留痕。）

| 任务 | 彩排建议 | 裁定 | 理由 |
|---|---|---|---|
| T1 | 无 | 无 | 素材已落盘（`.caliber/case-flow-builder-analysis.md`），转写自含，不需外部组件 |
| T2 | ingest-forge；弃 spec-forge | **采纳**（绑定 ingest-forge；弃用 spec-forge） | 模板表头/工件归属枚举须与 ingest-forge 判别指引逐字一致（实读其模板对齐）；spec-forge 弃用理由成立——其 genre 为 ISO 29148 九节 SRS 模板，与 M13 十四节 genre 不同构，参照会引入节序污染 |
| T3 | [writing-great-skills, spec-forge, ingest-forge] | **采纳** | SKILL.md 本体写作纪律 + 两指针所指的机制源（spec-forge 工序 2/3/4、ingest-forge Q→C 与五件套） |
| T4 | writing-great-skills | **采纳** | 入口 SKILL.md 修订属 skill 文本编辑，写作纪律组件 |
| T5 | 无 | 无 | 锚串逐字修订自含（M7 已注转义陷阱） |
| T6 | plugin-creator | **采纳（补入）** | manifest 版本/description 字段变更形态参照插件清单规范；补入后 T6 非空 |
| T7 | 无 | 无 | ac 范式可直读 ac-90/ac-91 在仓源文件，无需外部组件 |
| T8 | [plugin-creator, zcode-configuration-guide] | **采纳** | 卸载/重装命令形态实读两组件正文取（T8 步骤 1 已指令化），禁凭记忆拼 |
| T9 | [spec-forge, ingest-forge] | **采纳** | 彩排本身即测 spec-forge 机制（工序 2/3/4 指针）+ ingest-forge 收编五件套形态；被测件本体（trans-forge）除外 |
| T10 | 无 | 无 | 登记表/handoff 更新为自含文档操作 |
| visible:false 六件 | 不消费（spec-miner/architect/intent-driven-development/skill-comply/delivery-gate/gateguard） | **采纳（不消费、保留为资源）** | 本 plan 十任务无一命中其职责面（spec 挖掘/架构设计/意图驱动/技能合规/交付闸/门守卫）；D-7 已裁定按 path Read 注入消费、不安装，本波无落点 |

**彩排总结**：困惑点发现四类 A1–A4（外部数据缺口/未定义标识符/未写明显步骤/无法定位引用），分任务 T1–T10 全覆盖 + 顶层 7 条——全部 15 处可修项已回工序 2 落修进本 plan（含 M7 转义陷阱、态 6 白名单穷举、T8 前缀剥离与失败处置链、T9 I2 机械命令、C10 commit 落点句等）；技能消费裁定 10 条全决（采纳 7/无 3/弃用 1/补入 1/visible:false 不消费 1）。**未决项：NO UNRESOLVED**。审查决策审计全档 = `.caliber/review-logs/2026-09-23-trans-forge-plan.md`（轮 1–3 + Taste + 闸口 + 工序 4 回写）。
