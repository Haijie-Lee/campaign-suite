# spec-lint.sh — spec 棘轮 lint hook（PostToolUse(Write|Edit)）

> campaign-suite W2 产物。契约：W2 plan K0/K5/K6/K7（《campaign-W2建造plan.md》v1.3）。

## 行为

1. **先记 touched（K6）**：每次调用向 `/tmp/campaign-sg-<SID>-touched.jsonl` 追加一行 `{"file","tool"}`（bash 重定向；python 仅出字符串——K0-5，Windows python 的 `/tmp` 与 Git Bash 错位，禁 `python open('/tmp/...')`）。先写后判激活。
2. **激活判据（K7，声明即数据）**：工程根存在 `adr/` 或 `docs/spec/` 或 `.campaign/` 任一 → 激活，否则静默。
3. **spec 路径模式（K7 统一口径）**：`*/SRS.md`、`*/docs/spec/*.md`、`*/docs/spec/*.markdown`。
4. **棘轮 lint（K5）**：Edit → 只 lint `new_string`；Write → lint 全部 `content` 但最多输出 10 条。lint 前剥 ``` 围栏段。
   - **L1 歧义词**：默认 7 词 `适当|尽量|必要时|按需|尽快|优化|友好` 子串匹配（每行首词命中报一次）；`.campaign/lint-words.txt` 存在则替换默认。
   - **L2 ID 引用完整性**：行内 ID（FR/NFR/R/D/C/Q/AC 词法）必须在 `.campaign/graph/graph.json` 节点集中；图缺失则 L2 整体跳过（提示行仅随有命中的信封输出）。同 ID 同行去重。
   - **L3 NFR 定义缺数值**：行以 `| NFR-` 开头或含 `NFR-x.y：`/`：` 形态，且剔除编号后无数字 → 告警。
5. **输出**：零命中零输出；有命中输出单行 JSON 信封 `{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"..."}}`（`ensure_ascii=False`）。

## 输出格式（逐字）

```
[spec-lint L1] <file>:<内容行号> 命中「<词>」→ 给出可验证的量化口径或删除
[spec-lint L2] <file>:<内容行号> 悬空引用 <ID> → 该 ID 未在 doc-graph 定义
[spec-lint L3] <file>:<内容行号> NFR 定义缺数值 → 补量词与阈值
```

## 硬性规则（K0）

exit 恒 0、异常静默、禁 `set -e`；stdout JSON 信封 python 编码（`ensure_ascii=False`）；bash→python 传路径一律 `cygpath -w`；file_path 归一化 `tr '\\' '/'`；SID 清洗 `tr -c 'A-Za-z0-9_-' '_'`（fallback：`session_id` → `$CLAUDE_SESSION_ID` → `nosid`）。
