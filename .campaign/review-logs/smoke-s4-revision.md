# SMK-R1 — S4 版本间修订审计（plan-review-ritual v2.7.0 REVISION 模式，冒烟）

- REVISION 输入：上一版 = smoke/s2-plan.md（v1.0，彩排修复后）；diff = smoke/s2-plan.diff（1 hunk）；变更摘要 = 「探针超时常数 0.2s 硬编码 → CLI `--timeout` 可配置，默认 0.2 不变」。
- 范围产物：smoke/s4-scope.md（revision_scope.py，graph 缺席降级——警告在档，ripple=0）。
- AUDIT_PATH = 本文件（K25 指定）。

## SMK-R1-A（声部A 逐 hunk 验尸，编排者代行——冒烟单元深度声明见 s5 报告）

- hunk 内容：T1-3 功能行改写（`probe <addr>` → `probe <addr> [--timeout <秒>]`，超时常数可配置化 + 默认值不变声明）+ 版本行 v1.0→v2 + V4 新增 + R2 新增。
- 意图 vs 实际 vs 摘要三者一致：✓（diff 仅触碰 probe 行与验证/风险节，未夹带）。
- 冲突猎手：changed_sections（任务/验证/风险）内无与修订矛盾的残留表述；「默认 0.2 s」与 R2「默认行为不变」互洽。✓
- SINGLE 裁定（冒烟深度声明：双声部剂量在真实程序保留，冒烟单元以编排者单声部 + 范围机械核验替代——已入 s2-plan-v2 风险节与 s5 报告）。

## SMK-R1-B（范围机械核验）

- changed_ids = {R2}：diff 中实际变更行号语义属于「探针超时可配置」——R2 正是该变更的风险登记行；T1-3 功能行无 ID 词法命中（plan 文档无 FR/NFR 引用），故 ids=1 正确。✓
- ripple=0：graph 缺席降级路径按 K16-B 契约触发警告，未静默。✓
- 抽查节：sample=0（4 节 × 0.1 向上取整 = 1？——实算：changed=4 节（含「（无节）」版本行区），未触及 = 全文 4 个 `##` 节 − 3 个 changed（任务/验证/风险）= 1；ceil(1×0.1)=1——**工具报 sample=0**。

### SMK-R1-B1（偏差记录 → revision_scope v1.1 候选）

sample_sections 实算应为 1（未触及节 1 × 0.1 向上取整），工具输出 0。
疑似 sample 基数把「（无节）」计入 changed 致未触及=0，或未触及×rate 后未向上取整。
处置：冒烟不阻塞（S4 范围=diff 全文已覆盖），登记为 revision_scope v1.1 候选第二项
（首项 = W3 登记的区间记法展开），触发器 = 真实 SRS 修订中 sample 漏抽造成实质漏审时。

## 结论

PASS（含 SINGLE 裁定 1 条 + 偏差登记 1 条）。s2-plan-v2.md 放行。
