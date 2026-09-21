# handoff — campaign 生存包

> 更新人：编排者；更新时机：每个停止点与单元边界。hook 只读注入，不改写本文件。

- 当前单元：无（**W1/W2/W3/W4 已闭合——四波全量建成**）；aerofold-m0 程序进行中（U-M0-01 complete，U-M0-02/03/04/05 eligible）
- 已过门：w1/w2/w3 出口全过@2026-09-21；**w4 出口判据（裁定后形态）全过@2026-09-21**（①C3/C6/B6 建成：program.py 九+一子命令 V1–V7、program-forge skill、36 骨架首跑 4PASS/21env/11impl、spec_impact + caliber plan-forge v1.9.0；②冒烟全程闭环：负向门实证 D3、对账双路径各触发一次、成本账 −63% 可解释、A1–A6 全成立；③M0 初始化 + U-M0-01 闭环：Q18/Q19→C10/C11，fixture v0.7；④设计文档 v1.2 挂起注记）
- 待裁定：①附录B 分类基准修正（继续挂起）；②无其他
- 下一步：**AeroFold M0 程序续跑**（U-M0-02 API 契约 / U-M0-03 UI 原型 / U-M0-04 技术栈 PoC / U-M0-05 P2P 引擎 PoC eligible；M0 全程判据挂起中，跑完由 program 账本回验补闭合）；「M0 全程」出口判据回验义务在设计文档 §4.3 v1.2 注记
- ledger：wave 账本 C:\WorkSpace\campaign-suite\.campaign\ledger.jsonl；程序账本 .campaign/program/smoke-w4-ledger.jsonl + aerofold-m0-ledger.jsonl（按程序隔离，K20）
- 关键路径：设计文档与调研 = C:\Users\Administrator\WorkBuddy\2026-09-20-21-39-26\（campaign插件设计文档.md **v1.2**、W1–W4 plan 等 10 份）；fixture = C:\Users\Administrator\WorkBuddy\2026-09-20-19-14-14\AeroFold-需求规格与技术架构方案.md（**现 v0.7**：C10/C11 落账、Q18/Q19 冻结；profile C=11/Q=20/AC=36）；caliber = C:\WorkSpace\caliber-suite（ritual v2.7.0 + **plan-forge v1.9.0** = B6 正向）
- 环境实测坑：WorkBuddy shell 常设 CLAUDE_PROJECT_DIR（测 hook 需 env -u）；Git Bash /tmp = C:\Users\Administrator\AppData\Local\Temp；bash 喂 Windows python 一律 cygpath -w；Windows python print CRLF（tr -d '\r'）；json.dumps 紧凑断言 separators=(",",":")；grep 表行断言用 grep -F
- 工具教训（累积）：①同文件 Edit 严格一条一消息（同消息双 Edit 实测丢第一处 ×2）②回读 grep 模式必须为目标位置独有（误中版本叙事造成过一次假绿）③修复落盘必回读 ④fresh 闸口发现数不收敛于零是机制属性（plan-forge v1.8.0）⑤子代理 429 = 配置类停止点上报裁定 ⑥彩排是抓真缺陷的（S2 彩排抓出 2001::/32 ⊂ 2000::/3 白名单逻辑矛盾）
- 待办（后续波次）：staleness 检测；「等」词带边界规则；附录B 分类基准修正；doc_graph v1.2（FR-8/9/10 假阳性）；revision_scope v1.1 两项（区间记法展开 + sample 计数疑似未向上取整/基数含「（无节）」——SMK-R1-B1）；**「M0 全程」判据回验（挂起，设计文档 §4.3）**
