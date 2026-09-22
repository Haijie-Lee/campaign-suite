# campaign-suite

> 最后更新：2026-09-22 ｜ 平台形态出处：`caliber-suite`（同机已验证的本地目录 marketplace 模式）

ZCode **本地目录 marketplace**（名 `campaign-suite`），当前只含一个插件 **campaign v0.4.0**：超大规模开发任务的编排套件，layered on caliber——总入口 skill campaign + 三个 forge skills（ingest-forge / spec-forge / program-forge）+ 一个证据审计 agent（evidence-auditor）+ 四个 spec 守护 hook + 五个零第三方依赖契约工具，经本地 marketplace 一次安装、随插件自动加载。

## 核心定位

**把超大规模任务（多 plan、多单元、跨会话）的编排从对话即兴记忆中解放出来，落为文件系统上的状态机**——每条机制对应一个长程编排失效模式：

- **文件系统即真相**：graph.json / ledger.jsonl / program.yaml / handoff.md——状态不驻留上下文，跨压缩、跨会话可恢复；
- **证据门控状态迁移**：单元过门、里程碑推进、程序收官均以落盘证据为准；`evidence-auditor` 专审定量断言的口径（来源/日期/测量条件/口径四要素）；
- **编排与实现分席**：程序层只编排、永不亲手实现——编排原子单位 = 一个 caliber L 级运行；
- **spec 棘轮**：SRS 变更经 doc-graph 机械解析、修订范围可测（revision_scope）、消费链反向互查在途 plan 池（spec_impact）——防规范漂移。

## 组件表（按实物）

| 组件 | 类型 | 一句话职责 |
|---|---|---|
| `campaign` | skill | 总入口分诊：域判定（四信号+顺序仲裁）→ 路由三 forge 或转 caliber，只管三件事 |
| `ingest-forge` | skill | 文档初刷：非规范存量文档（巨石单文件/散乱笔记/旧 SRS）→ 规范工件区，产出映射表 + Q 表 + 证据登记 |
| `spec-forge` | skill | SRS 四道工序（选材→制坯→锻打→成型），零到一与增量修订双模式 |
| `program-forge` | skill | 编排循环执行体：读 DAG → 派单元 → 收账 → 过门 → 对账 |
| `evidence-auditor` | agent | 证据口径审计专责：定量断言的来源/日期/测量条件/口径四要素核对 |
| hook `handoff-inject.sh` | SessionStart（matcher `startup\|compact`） | 注入 `.campaign/handoff.md` 生存包——跨会话/压缩不失忆 |
| hook `spec-context.sh` | PreToolUse（matcher `Skill`） | 调 skill 前注入 spec 图摘要 |
| hook `spec-lint.sh` | PostToolUse（matcher `Write\|Edit`） | spec 棘轮 lint：写文档时守护契约 |
| hook `spec-wrapup.sh` | Stop（无 matcher） | 会话收尾提醒（spec 收尾检查单） |
| `tools/doc_graph.py` | 工具（K3） | 解析 markdown 中 FR/NFR/R/D/C/Q/AC/§ 的定义与引用 → graph.json |
| `tools/ledger.py` | 工具（K1） | run-ledger：append / summary / current，只追加不改写 |
| `tools/program.py` | 工具（K19/K20） | program 状态机：DAG 单元编排，行级保留式写回 |
| `tools/revision_scope.py` | 工具 | 修订范围清单计算器：统一 diff × 当前文档 × doc-graph → 修订范围清单 |
| `tools/spec_impact.py` | 工具（K23） | spec 消费链反向互查：SRS 变更 ID 集 × 在途 plan 池 → 受影响 plan 清单 |
| `conventions/` | 契约 | 结果落盘契约（K4）+ result 模板——dispatch 执行单元的落盘纪律 |
| `acceptance/` | 验收基座 | 通用 runner（run_all.py + README），机制与具体项目条目分离 |

五个工具均零第三方依赖，Python 3.10+。各 hook 的契约说明在同目录 `.md`（`hooks/handoff.md` 是 hook 只读注入的生存包本体）。

## 目录树（按实物）

```
campaign-suite/
├── marketplace.json            # 与 .claude-plugin/ 内逐字节一致（双份同形=平台约定）
├── .claude-plugin/
│   └── marketplace.json        # ZCode 实际读取的 manifest
├── campaign/                   # 插件目录（marketplace.json 的 plugins[0].source: "./campaign"）
│   ├── .zcode-plugin/
│   │   └── plugin.json         # {"name":"campaign","version":"0.4.0"}
│   ├── skills/
│   │   ├── campaign/           # SKILL.md（总入口：域判定→路由→守停止点）
│   │   ├── ingest-forge/       # SKILL.md + templates/（映射表、Q 表模板）
│   │   ├── program-forge/      # SKILL.md
│   │   └── spec-forge/         # SKILL.md + checklists.md + templates/srs-template.md
│   ├── agents/
│   │   └── evidence-auditor.md
│   ├── hooks/
│   │   ├── hooks.json          # SessionStart + PreToolUse + PostToolUse + Stop 四组，type 均 "process"
│   │   ├── handoff-inject.sh / spec-context.sh / spec-lint.sh / spec-wrapup.sh
│   │   ├── handoff.md          # 生存包本体（hook 只读注入）
│   │   └── spec-*.md           # 各 hook 契约说明
│   ├── tools/                  # 五契约工具（py + 同名 schema md）
│   ├── conventions/            # 结果落盘契约 + result 模板
│   └── acceptance/             # 通用验收 runner + 契约说明
├── .campaign/                  # 本仓库自身的工作区（程序状态/证据/台账）——非分发物
└── LICENSE
```

`.campaign/` 是本仓库用 campaign 自身管理自身开发的自举工作区（S1-S5 程序、W1-W4 波次证据），不属于插件分发物。

## 依赖

本插件是 **caliber 的上层**：program-forge 的编排原子单位 = 一个 caliber L 级运行。建议先安装 caliber-suite（marketplace 名 `caliber-suite`，插件 `caliber`，见 `F:\workspaces\caliber-suite`），再安装本插件。

## 安装

1. Settings → Plugin Management → Discover → **+** → 添加本地目录 `F:\workspaces\campaign-suite`
2. 安装插件 `campaign`

安装后：skills 以 `campaign:<name>` 命名空间出现且裸名别名可用；四个 hook 随插件自动注册。

**注意**：hooks.json 的 process 命令硬编码 `C:/Program Files/Git/bin/bash.exe`（Windows 下 command 型 hook 落 WSL bash 全灭，process 型 + Git bash 绝对路径是已验证可行模式）。Git 安装路径不同的机器需改 `campaign/hooks/hooks.json`。

## 更新语义（与直觉相反）

本地目录源**无更新检测**：改了 `campaign/` 源码后，已安装副本不会自动更新；重装 = 新事务（新 version 目录入 cache、旧 cache 删除）。迭代插件时递增 `plugin.json` 的 version 后重走安装流程。
