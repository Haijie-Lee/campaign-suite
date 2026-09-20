# handoff — campaign 生存包

> 更新人：编排者；更新时机：每个停止点与单元边界。hook 只读注入，不改写本文件。

- 当前单元：无（W1/W2 已闭合，W3 未开工）
- 已过门：w1: 出口四判据全过@2026-09-21；w1-plan: 五轮闸口后按用户裁定转执行@2026-09-21；w2: 出口判据全过（hooks 双向用例 + ingest fixture 自验证 覆盖率100%/一致率92.3%）@2026-09-21
- 待裁定：①插件正式定名（campaign/program-forge/ingest-forge 均为占位）②plan-forge 元观察是否回写本体（闸口循环严重度衰减退出条款 / 残余 P2 用户验收出口，证据=W1 plan §5 + W2 四轮轨迹）
- 下一步：开工 W3 生产波——先按 caliber 流程锻造 W3 建造 plan（CONTEXT = campaign插件设计文档.md v1.1 §4.1 W3 行 + §4.3 W3 出口判据）；W3 范围 = B3 spec-forge（五视角+理解性彩排+澄清-grounding 交织）/ B4 ritual 修订模式 / B5 evidence-auditor；W3 出口 = spec-forge 完成一次真实 SRS 修订（v0.6）全流程 + 修订模式给出正确 delta 审查范围
- ledger：C:\WorkSpace\campaign-suite\.campaign\ledger.jsonl
- 关键路径：设计文档与调研 = C:\Users\Administrator\WorkBuddy\2026-09-20-21-39-26\（campaign插件设计文档.md、W1/W2 plan 等 8 份）；fixture = C:\Users\Administrator\WorkBuddy\2026-09-20-19-14-14\AeroFold-需求规格与技术架构方案.md；caliber 源码 = C:\WorkSpace\caliber-suite
- 环境实测坑：WorkBuddy shell 常设 CLAUDE_PROJECT_DIR（测 hook 需 env -u）；Git Bash /tmp = C:\Users\Administrator\AppData\Local\Temp；Windows python 需 C:/ 形式路径；Windows python print 输出 CRLF（bash 提取字段一律 tr -d '\r'）；python json.dumps 默认分隔符带空格（断言按紧凑写时需 separators=(",",":")）
- 工具教训（W2 新增）：①同一文件的多个 Edit 必须串行并逐个回读（并行 Edit 曾丢 2/4 处）②任何修复落盘后必须回读验证，不得仅信工具返回值
- 待办（后续波次）：staleness 检测（挂 doc_graph 增量更新）；「等」词带边界规则加回（触发器见 W2 plan R4）；附录B 分类基准修正（第二篇调研文档修订项）；Q16/Q17 注册表矛盾（fixture 文档自身缺陷，待用户裁定处置）
