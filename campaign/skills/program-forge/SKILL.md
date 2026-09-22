---
name: program-forge
description: 编排多单元程序（读 DAG → 派单元 → 收账 → 过门 → 对账）。当任务被分解为 program.yaml 中的多个有依赖关系的单元、需要跨 plan/跨会话编排时使用。不用于：单 plan 任务（caliber 直跑）、SRS 生产（spec-forge）、文档收编（ingest-forge）。
metadata:
  version: "0.1.0"
  source: campaign-w4
---

# program-forge — 编排循环 F1 的执行体

程序层只编排、永不亲手实现（D2）。编排原子单位 = 一个 caliber L 级运行；
里程碑是状态聚合层，不是执行单位。本 skill 把「编排」从主线程的即兴记忆
劳动变成查表执行的机械劳动 + 停止点处的人工裁定。

## 输入

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
- 首次创建 `.campaign/` 时：项目根存在 `.git` 目录且 `.gitignore` 无 `.campaign/` 行 → 追加一行 `.campaign/`；无 `.git` → 跳过并输出一行说明（程序状态与证据不入 git）。
- 工具：`campaign/tools/program.py`（状态机，九子命令 + impact）、
  `campaign/tools/ledger.py`（wave 账本）、`campaign/tools/doc_graph.py`（SRS 定位）、
  `campaign/tools/spec_impact.py`（B6 反向互查）。

约定通道（何时裁定 / 写什么）：
- 制宪时刻：首个编码单元启动前，由该单元产出 CONVENTIONS.md 并经用户
  裁定；模板 = campaign/conventions/engineering-conventions-template.md。
- 里程碑边界：新语言/新框架入场 → 补生态层裁定（lint 配置入库 + lint_cmd）。
- 首次复触：单元首次改动他单元产出的包 → 对应组件边界行进「组件边界」节。
- 并行启动：parallel 放开前 → 组件边界与数据所有权先就位。

## F1 编排循环（七步，逐步机械动作）

```
LOOP：
 1. 读状态      program.py status --program <p>     （不读会话记忆，D1）
 2. 选单元      program.py next --program <p>       （eligible = pending ∧ 依赖全 complete；v1 串行取最小 ID）
 3. 装配        program.py brief --program <p> --unit <id>
                → 输入包 <id>-brief.md（K21 七节），即 caliber 阶段 1 的 CONTEXT
 4. 调 caliber  program.py start --program <p> --unit <id>（落 unit_start）
                按单元形态执行完整 caliber 运行：
                - 判断/集成单元 = ML/L 级（plan-forge 制坯 + 工序 4 彩排 → 执行 → 验证）
                - 修订单元 = plan-review-ritual REVISION 模式（B4）
                - 文档单元 = 主线程 inline 执行 + 独立审查
                caliber 的停止点按 D4 原样触发——编排不得替用户回答
 5. 收账        写 <id>-result.md（K21 五行输出包）
                program.py collect --program <p> --unit <id> --elapsed <秒>
 6. 门检查      program.py gate --program <p> --unit <id>
                证据齐 → complete + unit_end；不齐 → MISSING + 状态不变 + 上报（D3）
 7. 对账        program.py reconcile-check --program <p>
                due:yes → 派 fresh agent 对账 → program.py reconcile --program <p>
```

任何一步失败 = 停止或回退到上一步，禁止跳过。每 5 单元或 plan 修订类
ruling 入账时必到对账点（reconcile-check 判定式承载）。

## 接口包契约（K21）

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

**输出包** `<id>-result.md`（caliber → program，≤ 15 行，C4 契约程序级版本），
固定五行：

```
verdict: pass|fail|concerns
结论: ≤3 行
证据: <文件指针清单>
实测: <预测 vs 实际，可空>
ruling: <新增 ruling 清单，可空>
```

收账时约定回流（M6）：result 的 `ruling:` 行含工程约定条款 → 编排者把
该条款追加进 CONVENTIONS.md（此后所有 brief 自动携带）；制宪时把禁则
清单镜像进工程 `CONTEXT.md` 铁律段（该工程订阅 docs 治理体系时）。

## 停止点（F5，少而重）

1. 单元 DAG 变更（加/删/改依赖）——停，上裁定；
2. 对账发现目标漂移（漂移清单非空）——停，上裁定；
3. 门证据伪造嫌疑（证据文件与实测不符，含手工编辑 status=complete）——停，上裁定。

其余 rulings not stalls：Ruling 进程序账本，不阻塞循环。

## 对账（F1 步 7 展开）

- 判定：`reconcile-check` 输出 `due:yes` 才派遣，不凭感觉。
- 派遣：编排者用 Agent 工具 dispatch `general-purpose` 零背景 subagent。
- prompt 骨架：

```
You are a fresh goal-reconciliation agent with ZERO context. 报告用中文。
INPUTS: ① 原始 CONTEXT = <program.yaml 的 context 字段所指文件/节>；
② 当前全部产物 = <已 complete 单元的 result 文件清单 + 关键工件路径>。
任务：对照 ①②，回答：产物是否仍服务于原始目标？
输出二选一：「无漂移」+ 一句依据；或「漂移清单」= | 漂移点 | 证据 | 建议处置 |。
附查（有界）：上次对账以来 complete 的单元的产物之间，是否存在互斥的
实现约定（命名/分层/错误处理范式两两矛盾）？只报互斥级矛盾，不报品味、
不评质量；每条引用 文件:行。
Rules: read-only；只报目标级漂移（不是质量问题）；每条引用原文。
```

- 输出落 `.campaign/review-logs/<program>-reconcile.md`（追加），然后
  `program.py reconcile` 落账（ledger reconcile 事件 + last_reconciled 写回）。
- 漂移清单非空 = 停止点 ②，上报用户裁定。

## 与 caliber 的分工

- campaign = 程序层：程序状态、工件治理、编排循环、门、账本。
- caliber = 任务级引擎：每个单元是一次完整 caliber 运行，其内部纪律
  （plan 收敛循环、双 verdict 审查门、TDD 证据）原样保留，剂量不折叠（D4）。
- 接口零 caliber 改动：文件约定（brief 进、result 出）。
- spec 变更时跑 `program.py impact --program <p> --ids <变更 ID 集>`（B6
  反向互查）→ 受影响在途 plan 清单，触发重审或修订。
