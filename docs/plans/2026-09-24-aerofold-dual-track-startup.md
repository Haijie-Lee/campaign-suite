# AeroFold 双线并行启动包（deep-probe 双轨收口 · 已裁定）

- 日期：2026-09-24
- 流程：caliber deep-probe 双轨（主轨 + 方案挑战者信息隔离独立生成 → 对照表 → 方案确认停止点）
- 裁定：用户在方案确认停止点批准「默认全按推荐」
- 通用化：本启动包是 [多线并行编排模式 v0.1](../patterns/multi-line-parallel-orchestration.md) 的首例实例化（映射见该文 §7）；后续工程启用双线时以模式文为准、本包为参照案例。

## 对齐快照（五段）

**目标重推**：在不破坏 campaign 状态纪律的前提下，为 AeroFold 新增第二条并行开发线——SRS M2 发送端 MVP 的 UI 切片（Tauri 壳 + Web UI 三屏 + 拖拽 + 进度展示 + 降级确认 UI），对冻结的 API 契约 v1.0 + Mock 服务端开发，由第二个 ZCode session 独立编排推进，在 aerofold-m2 收口（U-M2-07 三网验收）后汇合做真链路集成（U-M2-08），用双份算力换墙钟时间。

**道层条款**：价值排序 = 墙钟时间 > 算力/token 成本；演示闭环优先于客户端全量。不可妥协项：①campaign 状态完整性（不得撞车丢账）；②组件所有权两线不得交叉写；③汇合点必须预置 DAG，不得事后硬拼；④M2 线节奏不得因二线启动变慢。失败形状 = 状态双写撞车 / Mock 与契约漂移失控 / 汇合集成变大坑 / 用户裁定带宽过载 / 并行无净收益。

**开放决策点+方案选定记录**：方案确认停止点已裁定（2026-09-24）＝ 挑战案 A 全骨架（双 worktree 物理隔离 + 双 campaign 程序）+ 主案 B（插件机制改造）降挂起。对照表要点：收敛 5 项（双程序双 worktree / 不动引擎起步 / 组件所有权硬切 / 汇合双侧预置 / 删除测试三案交叉印证）；分歧 1 项（状态拓扑——挑战案「双 .campaign 物理隔离」胜主案「单 .campaign + cd 纪律」，理由：物理「写不到」> 纪律「约定不写」，program.py 484 行仅一处 getcwd 已核实）；借鉴 6 项（契约出仓 / Mock 对账门 / 中期 smoke / 裁定包预算化 / ADR-0001 复活条件追溯 / 单屏压缩扳机）；未采纳 3 项（主 session 代账制——违反④；零 campaign 野跑——恢复力归零，洞察已吸收；主案状态单源——以汇合归档补偿）。

**挂起项（带触发器）**：①插件机制改造（parallel 语义——program.py:170-171 validate 硬拒 `parallel != "-"`，已核实，本案不依赖 / handoff 分件 / 显式工程根）——触发器 = 双线实测撞车或对账负担现形；v2 若放开 parallel，双程序可无损回并。②跨程序统一对账视图——触发器 = 汇合对账负担实测过重或第三次启用双线。③macOS 公证预研（SRS §8 建议 M2 阶段启动）——挂 UI 线后续程序立项。

**前提清单**：①启动裁定包一次批准（已发生）；②UI 线全程不写 `server/`、`crates/`、`wire/`（出现则写 DRIFT-LOG 转 M2 线）；③第二 session cwd 锁定第二 worktree；④契约快照按当前态出仓、不等 U-M2 在途单元收账；若快照时 U-M2-03 未收账，candidates/WS 信令段标注「在途扩展」，M2 线收账后更新契约文件；⑤Mock 服务端沿用 Go 零新增依赖约定；⑥双线 token ≈ 两倍已被价值排序覆盖。

## 启动裁定包（已批准默认配置）

| 项 | 值 |
|---|---|
| 第二 worktree | `F:\workspaces\AeroFold-ui` |
| UI 线组件 | `client/`（Tauri 壳 + Web UI）+ `client-mock/`（Mock 服务端） |
| 契约出仓 | `docs/api/contract-v1.md`（M2 线独写，UI 线只读） |
| 漂移登记 | `docs/api/DRIFT-LOG.md`（append-only，UI 线写） |
| M2 侧 DAG 追加 | U-M2-08「真链路集成与演示闭环」，depends [U-M2-07]，外部门 = UI 线交付 tag |
| UI 程序 | aerofold-ui，4 轻单元（见下） |
| 启动合法性追溯 | ADR-0001 被否方案 3 复活条件 =「M2 里程碑启动且 API 契约 v1.0 冻结」——两条件 2026-09-24 同时满足（docs/adr/ADR-0001-ui-contract-alignment.md:50） |

## 主线侧三步（归 M2 线 session 执行，写权决定不可外派）

时机：**尽早，无需等 U-M2-03 收账**（U-UI-02 的契约前置要求它先于二线第二单元完成；与在途单元不冲突——产物全为新文件/新目录 + 一条 `.campaign` 内 yaml 追加）。git 纪律：单独小提交，显式路径暂存，禁 `git add -A`（G8 = AeroFold CONVENTIONS.md:27）；**提交直接落 main 并立即 `git push origin main`**——二线 rebase 参照系 = origin/main，不 push 则二线静默吸收不到契约文件（切 main 前未跟踪文件随动不受影响，提交后切回原单元分支继续）。

1. **契约出仓**：先 `mkdir docs/api`（目录当前不存在）；`.campaign/evidence/m0/u02-api-contract.md` 当前态固化为 `docs/api/contract-v1.md`，头部加派生声明（源指针 + 权威随快照移交注明 + **条件标注**：执行时若 U-M2-03 未收账 → candidates/WS 信令段标注「在途扩展，以 M2 线后续更新为准」；若已收账 → 核对原件，已含扩展终版则不加在途标注，并在 ADR 补记中记录快照基线 = 03 收账后态）。同建 `docs/api/DRIFT-LOG.md` 初始文件（表头：日期/发现线/契约锚点/漂移描述/处置状态）。
2. **ADR 补记**：`docs/adr/` 新增 **ADR-0002-contract-export.md**（下一可用编号，已核 docs/adr/ 仅存 ADR-0001）记录契约出仓——援引 ADR-0001 重审条件 3（:56，契约进入实测校验须同步复核）与 R-CONTRACT-1（:20）；注明 `.campaign` 原件不动、权威身份随快照移交、UI 线只读。
3. **追加 U-M2-08**：`aerofold-m2.yaml` 尾部追加（DAG 变更 = 停止点①，本次已由用户在双轨方案确认中裁定，记录出处即可）：
   （粘贴时缩进对齐既有单元：`- id:` 前恰两个空格，字段四空格——上块因处于列表项内带了额外前导空格，照抄会破坏 YAML 结构）
   ```yaml
   - id: U-M2-08
     title: 真链路集成与演示闭环（消化 UI 线交付 tag + 契约 delta + Mock 假设清算）
     status: pending
     depends: [U-M2-07]
     parallel: "-"
     gate: [.campaign/evidence/m2/u08-integration.md]
     brief: .campaign/program/U-M2-08-brief.md
     result: .campaign/program/U-M2-08-result.md
     budget_s: 100800
   ```

## 二线侧启动（用户开新 ZCode session，归该 session 的 program-forge 流程）

1. **建 worktree**：`cd F:\workspaces\AeroFold && git worktree add F:\workspaces\AeroFold-ui -b line/ui-slice main`（**末尾 `main` 不可省**——省略则锚当前 HEAD = 在途的 u-m2-03 单元分支，会把未完成工作带进二线；单元分支照旧日期式，单元完成合回 line/ui-slice 并定期 rebase origin/main）。session 启动目录 = `F:\workspaces\AeroFold-ui`，全程锁定。
2. **锻造 aerofold-ui 程序**（草案→用户裁定→落盘，走既有 program-forge；`.campaign/` 由引擎在 worktree 内新建，与主树物理隔离）：
   - U-UI-01 Tauri 壳与三屏骨架（depends []；消费 `docs/designs/web-ui/` 六件（含 design-tokens.css/json，清单以 ADR-0001 收编表为准）；门 = 壳启动 + 三屏静态渲染实录）
   - U-UI-02 Mock 服务端与契约对账门（depends [U-UI-01]；`client-mock/` 实现发送端所需 REST/WS 子集，吃 `wire/vectors/*.json` 同向量；门 = Mock 端点表 vs `docs/api/contract-v1.md` 端点表行级对账输出——**前置条件：契约文件已在 origin/main（二线 rebase 吸收）**）
   - U-UI-03 拖拽/进度/降级确认全链路（depends [U-UI-02]；门 = 交互闭环演示录屏 + 对账门复跑；**前置条件：自查 git log，若 U-M2-03 已合 main → rebase 后跑中期握手级 smoke**（非三网验收），结果记证据）
   - U-UI-04 集成就绪交付（depends [U-UI-03]；门 = Mock 对账终版 + 演示录屏 + DRIFT-LOG 全量清单 + 集成 checklist + 交付 tag——tag 即 U-M2-08 外部门）
3. **纪律**：CONVENTIONS.md 只读（rebase 吸收 M2 线更新，UI 线约定需求记单元 brief）；契约漂移只写 DRIFT-LOG，不反攻契约文件；契约漂移以外的跨线需求一律挂起等汇合，不私拉通道。
4. **范围删除扳机**（已批准留作选项）：需压缩时三屏砍为「发送屏单屏闭环先行」（拖拽→进度→完成一页流，另两屏静态壳），与「演示闭环优先于客户端全量」对齐。

## 回滚

方案整体可逆：`git worktree remove F:\workspaces\AeroFold-ui`（若二线已有提交或未跟踪文件 → 需 `git worktree remove --force`；分支 `line/ui-slice` 另需 `git branch -D line/ui-slice`）+ 移除 aerofold-m2.yaml 的 U-M2-08 追加即回现状，M2 线无残留；契约出仓为新增文件，撤销 = 删文件 + ADR 标注撤回。

## 证据与出处

- 挑战者（方案挑战者，信息隔离独立生成）报告：状态物理隔离设计 / 契约出仓必要性与位置陷阱 / Mock 对账门 / 中期 smoke / 代账制与野跑否决理由 / 影响评估（爆炸半径 Medium）。
- 事实核验：`program.py:170-171`（parallel 硬拒，已核实）；ADR-0001:50（复活条件原文，已核实）；ADR-0001:20（契约权威源 = `.campaign/evidence/m0/u02-api-contract.md`，R-CONTRACT-1）；账本实测单元墙钟 4.8–12.5h（瓶颈在串行执行）。
- 关键风险对价：跨程序无统一账本视图（以 git log + 双 handoff + 汇合归档吸收）；第二 worktree Rust target/ 双份磁盘开销；契约快照段含在途标注（U-M2-03 扩展段落定后 M2 线须更新契约文件——已写入前提④）。

<!-- REVIEW DECISION LOG -->
## 审查决策审计（plan-review-ritual v2.6.4，ROUND=1）

- 审查对象：本启动包 + [../patterns/multi-line-parallel-orchestration.md](../patterns/multi-line-parallel-orchestration.md)（两文档同一审查，审计单点落盘于此）。
- 声部A = plan-reviewer（仓库交叉核对 + 四视角）；声部B = voice-b-reviewer（override: K2.8 Preview，跨家族分化在场；纯文本内部一致性）。
- 剂量说明：设计本体同日已过 deep-probe 双轨挑战（独立第二生成源）；本轮专责文档层可执行性（fresh session 逐字执行视角）。

### 共识表

| 发现 | 声部A | 声部B | 共识 |
|---|---|---|---|
| 主线三步时机与契约标注互斥/「建议」歧义 | ✓(A-F2) | ✓(B-B3) | **CONFIRMED** |
| push origin 缺失 + rebase 参照系不统一 | ✓(A-F1) | — | SINGLE-P2 |
| 「重审条件 3」对两文档读者为悬空锚 | —（A 已核原文属实） | ✓(B-B1) | SINGLE-P2 |
| ADR 未给编号 / docs/api 目录不存在 / 六件双算 / worktree remove 缺 --force | ✓(A-F3/F4/F5/F7) | — | SINGLE-P3×4 |
| 模式文 M2 缺「docs/ 入 git 主体系」前提 | ✓(A-F6) | — | SINGLE-P3 |
| 挂起④无触发器且与①重叠 / 双斜杠路径歧义 / G8 悬空引用 | — | ✓(B-B2/B4/B5) | SINGLE-P3×3 |

### 决策行

| ID | 来源 | 发现 | 分类 | 裁定 | 理由 | 修复位置 | 涟漪 |
|---|---|---|---|---|---|---|---|
| R1-S1 | 作者自审(Step1) | worktree 命令缺 `main` 锚（省略则锚在途单元分支 HEAD） | Mechanical | 修 | 字面执行即带错在途状态 | 二线侧步 1 | 否 |
| R1-S2 | 作者自审(Step1) | YAML 块在列表项内带额外前导空格，照抄破坏结构 | Mechanical | 修 | 引擎解析器正则要求恰两/四空格（A 复核确认） | 主线侧步 3 | 否 |
| R1-F1 | A-F2+B-B3 | 时机「建议 U-M2-03 收账后」与已批准前提④（立即快照）互斥；「建议」产生两种合法解读 | Mechanical | 修（CONFIRMED 无条件） | 对齐用户已裁定前提④；条件标注规则消除双重错误 | 时机行 + 步 1 条件标注 + 前提④措辞 | 否 |
| R1-F2 | A-F1 | push origin main 未写明；二线参照系「已上 main」≠「origin/main」 | Mechanical | 修 | 不 push 则二线静默缺契约，U-UI-02 卡死或更糟无感继续 | 时机行 + U-UI-02 前置 | 否 |
| R1-F3 | B-B1 | 「重审条件 3」编号对持两文档读者不可解（A 核实 ADR-0001:56 原文属实） | Mechanical | 修 | 补行号锚 + 内容摘要，术语与「复活条件 :50」并立不混 | 主线侧步 2 | 否 |
| R1-F4 | A-F3 | ADR 未给编号/文件名（实测下一可用 = ADR-0002） | Mechanical | 修 | 逐字执行者需字面量 | 主线侧步 2 | 否 |
| R1-F5 | A-F4 | docs/api/ 不存在，未写建目录步骤 | Mechanical | 修 | shell 重定向写法会失败 | 主线侧步 1 | 否 |
| R1-F6 | A-F5 | 「六件 + design-tokens」双算（tokens 属六件之二） | Mechanical | 修 | 防找不存在的第七件 | U-UI-01 行 | 否 |
| R1-F7 | A-F6 | 模式文 M2 隐含前提「docs/ 入 git 为主体系」未声明 | Mechanical | 修 | 前提不成立时 C3 与 M2 无法互检 | 模式文 §3 M2 行 | 是——波及模式文（已同修）；启动包所在工程前提成立，无需联动 |
| R1-F8 | A-F7 | worktree remove 遇提交/未跟踪文件会被 git 拒绝 | Mechanical | 修 | 补 --force 与 branch -D | 回滚段 | 否 |
| R1-F9 | B-B2 | 挂起④无触发器且与①实质重叠 | Mechanical | 修 | 并入①并保留 parallel 子项的硬拒证据 | 挂起项段 | 否 |
| R1-F10 | B-B4 | 「server//crates//wire/」双斜杠未定义 | Mechanical | 修 | 显式枚举三顶层目录 | 前提② | 否 |
| R1-F11 | B-B5 | G8 引用两文档内无出处 | Mechanical | 修 | 注出处 AeroFold CONVENTIONS.md:27 | 时机行 | 否 |

### 零发现记录（查了什么）

- 声部A 视角1（事实核查）：YAML 块 vs program.py 解析器正则逐位比对通过；evidence 命名惯例、web-ui 六件俱在、.gitignore 含 .campaign/ 行、契约源文件存在、wire/vectors 可消费、CONVENTIONS G8/30 行硬顶引用可解析、origin/main 与 worktree 实况与文档断言吻合——除入表各行外零发现。
- 声部A 视角3（跨文档一致性）：§7 映射表七行逐对、互链相对路径实测有效、§4 六步与启动包结构同构——零发现。
- 声部A 视角4（通用性）：模式文正文无未标注专属值残留；C/M 依赖无环——除 R1-F7 外零发现。
- 声部B CHECK2（交叉引用）：映射表/计数（收敛5/分歧1/借鉴6/未采纳3）/段名互引全部逐字相符——零发现；CHECK5（通用性残留）零发现；CHECK3 逃逸词扫描「必要时/视情况/类似/尽量」零命中。

### 总结

发现 13（自审 2 + 声部 11：CONFIRMED 1、SINGLE-P2 2、SINGLE-P3 8）；分类：Mechanical 13 / Taste 0 / User Challenge 0——全部直接修，无用户裁定项。未决项 = 0；设计内延期项（非审查发现）：U-M2-08 详细 plan 归汇合时代锻造、二线 .campaign 归档机制见模式文 §5。litmus 已复走：主线三步与二线四步逐字可执行，字面值（编号/路径/命令/锚点）全部给出。
