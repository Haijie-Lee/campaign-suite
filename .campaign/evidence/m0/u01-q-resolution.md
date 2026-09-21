# U-M0-01 需求冻结裁定记录（2026-09-21）

- 程序：aerofold-m0（`.campaign/program/aerofold-m0.yaml`）；单元：U-M0-01。
- GATE：AskUserQuestion 两问（Q18/Q19），用户两选均「按答案方向确认」。

## 裁定落账

| 待定项 | 裁定 | 新决策 | fixture 落点 |
|---|---|---|---|
| Q18 体检允许消耗中继流量吗 | 按答案方向确认 | **C10**（计量告知 + 蜂窝二次确认 + 仅测直连选项） | §3.4 Q18 行 ✅（C10）；§0.4 C10 行；D17 联动 |
| Q19 体检探针会触发限速吗 | 按答案方向确认 | **C11**（探针后轮换 UDP 端口 + 5 s 冷却 FR-9.12 + 文档明示偏保守） | §3.4 Q19 行 ✅（C11）；§0.4 C11 行；R21 联动 |

- 版本：fixture v0.6 → **v0.7**（版本行 + §0.4 计数 C1–C9 → C1–C11）。
- 流程：plan-review-ritual REVISION 模式（B4）+ spec-lint.sh（零告警，exit 0）；
  doc_graph 重建终态 `C=11 Q=20 AC=36`（C 9→11、Q 不变——Q 行保留仅状态列改）。
- 程序账本：`.campaign/program/aerofold-m0-ledger.jsonl` ruling 一条（裁定原文）。
- §3.4 其余待定行（Q3/Q4/Q5/Q6/Q9/Q10/Q12/Q15 等 9 行）不在本单元范围
  （K26 单元定义 = Q18/Q19），保持待定不越权。
