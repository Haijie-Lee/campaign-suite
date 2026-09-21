# 审查决策审计（plan-review-ritual v2.7.0 REVISION 模式）

> PLAN = AeroFold-需求规格与技术架构方案.md（v0.6）；REVISION 四件：PREV=/tmp/campaign-w3/aerofold-v0.5.md、DIFF=/tmp/campaign-w3/v05-v06.diff、CHANGE_SUMMARY=版本行（v0.6 摘要）、SCOPE=/tmp/campaign-w3/scope-v06.md。
> 声部A = Agent(general-purpose) 逐 hunk 验尸 + 涟漪节冲突猎手（仓库交叉核对）；声部B = 第二 Agent(general-purpose) 纯文本一致性。对抗价值稀释留痕（同家族，ritual v2.6 条款）。

<!-- REVIEW DECISION LOG -->
| ID | 来源 | 发现 | 分类 | 裁定 | 理由 | 修复位置 | 涟漪 |
|---|---|---|---|---|---|---|---|
| V06-R1-F1 | 声部B | C9 影响列仅 NFR-2.1/2.5/2.6，与 Q20 全指针集（含 2.11/2.12～2.14）不对齐 | Mechanical（SINGLE，P2 边界） | **不修** | C9「主要影响章节」列精确描述决策直接影响面（M5 量化指针三件套）；NFR-2.11/2.12～2.14 是 Q20 的沿用上下文而非 C9 的改动面；C9→Q20 引用链完整闭合，读者一跳可达全集 | — | 否 |
| V06-R1-F2 | 声部B | scope changed_ids 仅含 C1/C6/C7/C8/C9，「C1–C9」区间记法未展开 C2–C5 | Mechanical（SINGLE，P3） | **不修** | changed_ids 按 diff 字面 token 词法提取（设计内行为）；「C1–C9」是计数修正记法，C2–C5 内容未被触碰、无需进涟漪；区间展开（～/– 记法）登记为 revision_scope v1.1 候选（触发器：区间端点外的成员 ID 出现真实漏检时） | — | 否 |

零发现记录：
- 声部A 逐 hunk 验尸：5 hunk 意图-实际-摘要三方一致（版本行声明集合 = diff 实际集合）；NFR-2.1/2.5/2.6 指针与 §3.3 逐字核对精准；涟漪节（§4.1.10/§8.1/§10）零冲突；抽查节（## 附录 A）零冲突（确认）。**PASS，零发现**。
- 声部B 任务 1（新旧文本对/误删猎手）：PASS——3 处替换同位置、2 处纯插入、无内容丢失；任务 3 changed_sections/counts 自洽：PASS。
- 共识表：零 CONFIRMED（无双声部命中）；V06-R1-F1/F2 均 SINGLE，经编排者裁定留档。

总结行：V06-R1 发现 2 项（0 P1 / 1 P2 / 1 P3，全 SINGLE，裁定均不修带理由）；NO UNRESOLVED。
