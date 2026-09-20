# spec-wrapup.sh — spec 收尾提醒 hook（Stop）

> campaign-suite W2 产物。契约：W2 plan K0/K6/K7；镜像 caliber `learnings-wrapup.sh` 安全契约。

## 行为

1. `stopHookActive|stop_hook_active` 为真 → **一律静默**（防续跑循环）。
2. K7 激活判据（`adr/` 或 `docs/spec/` 或 `.campaign/` 存在）。
3. 门控：每会话至多 block 1 次（`/tmp/campaign-sg-<SID>-reminded` 标记，**仅在实际 block 时写入**）。
4. 读 `/tmp/campaign-sg-<SID>-touched.jsonl`（K6，由 spec-lint.sh 维护）：
   - 含 spec 路径记录（`*/SRS.md`、`*/docs/spec/*.md`、`*/docs/spec/*.markdown`）
   - 且不含 `CHANGELOG*` 与 `*/adr/` 路径记录
   - → 输出顶层 `{"decision":"block","reason":"..."}`（`ensure_ascii=False`），提示变更叙事外移。

## 与 caliber learnings-wrapup.sh 的明示差异

**不采用 ≥3 次编辑门槛**——caliber 的语义是「≥3 次实质编辑才值得收尾检查」，W2 的语义是「改了 spec 一次即须外移变更叙事」（修订协议无最小剂量）。保留的安全契约：stopHookActive 静默、每会话 1 次、exit 恒 0、异常静默。

## 依赖

K6 会话状态由 spec-lint.sh 写入（先写后判激活，故非 spec 编辑也在册——本 hook 自行按 spec 口径过滤）。会话态全程 bash 读写（K0-5）。
