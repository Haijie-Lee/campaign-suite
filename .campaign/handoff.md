# handoff — campaign 生存包

> 更新人：编排者；更新时机：每个停止点与单元边界。hook 只读注入，不改写本文件。

- 当前单元：无（**W1/W2/W3 已闭合**；W4 编排波未开工）
- 已过门：w1/w2 出口全过@2026-09-21；w3-plan 锻造闭合（轮1 16项→轮2 10项→闸口① 3项→闸口② PASS→彩排 9 补全）；**w3 出口判据全过@2026-09-21**（①spec-forge 完成 v0.6 真实修订全流程，fixture profile 终态 C=9/Q=20/duplicates=3；②修订模式 delta 范围机械核验 V1–V3 PASS + REVISION 实战审计 V06-R1 两项 SINGLE 裁定留档）
- 待裁定：①附录B 分类基准修正（第二篇调研文档修订项，继续挂起）；②无其他（定名=campaign 已终裁、K18 保留已终裁、429 处置已终裁）
- 下一步：开工 W4 编排波——先按 caliber 流程锻造 W4 建造 plan（CONTEXT = 设计文档 §4.1 W4 行 + §4.3 W4 出口判据）；W4 范围 = C3 program-forge（编排循环 F1 执行体）/ C6 验收基座 / B6 消费链；W4 出口 = program-forge 编排 AeroFold M0 全程（DAG 状态机与门证据全程一致、对账检查点至少触发一次、成本账与实际偏差可解释）
- ledger：C:\WorkSpace\campaign-suite\.campaign\ledger.jsonl
- 关键路径：设计文档与调研 = C:\Users\Administrator\WorkBuddy\2026-09-20-21-39-26\（campaign插件设计文档.md、W1/W2/W3 plan 等 9 份）；fixture = C:\Users\Administrator\WorkBuddy\2026-09-20-19-14-14\AeroFold-需求规格与技术架构方案.md（**现 v0.6**：C9/Q20/M5 量化指针 + §0.4 计数修正；v0.5 快照=/tmp/campaign-w3/aerofold-v0.5.md，diff=/tmp/campaign-w3/v05-v06.diff）；caliber 源码 = C:\WorkSpace\caliber-suite（plan-review-ritual 已 v2.7.0 = REVISION 版本间模式）
- 环境实测坑：WorkBuddy shell 常设 CLAUDE_PROJECT_DIR（测 hook 需 env -u）；Git Bash /tmp = C:\Users\Administrator\AppData\Local\Temp；**bash 喂 Windows python 一律 cygpath -w（含 --out 类输出参数——W3 执行期实证 K0-2 对输出路径同样适用）**；Windows python print 输出 CRLF（bash 提取字段一律 tr -d '\r'）；python json.dumps 默认分隔符带空格（断言按紧凑写时需 separators=(",",":")）；grep 无 -E 时 `\|` 是 alternation（表行断言用 grep -F）
- 工具教训（累积）：①同一文件的多个 Edit 必须串行并逐个回读（并行 Edit 曾丢 2/4 处）②任何修复落盘后必须回读验证，不得仅信工具返回值 ③fresh 闸口发现数不收敛于零是机制属性——判读看衰减轨迹与设计本体是否被挑战（plan-forge v1.8.0）④子代理 429 = 配置类停止点，上报用户裁定，禁止静默降级
- 待办（后续波次）：staleness 检测（挂 doc_graph 增量更新）；「等」词带边界规则加回（触发器见 W2 plan R4）；附录B 分类基准修正；doc_graph 词法 v1.2（裸组 ID 加粗叙事误判 FR-8/9/10 假阳性）；**revision_scope v1.1 候选：区间记法展开（C1–C9 / NFR-2.12～2.14 的区间成员 ID 展开进 changed_ids——触发器：区间外成员出现真实漏检时）**
