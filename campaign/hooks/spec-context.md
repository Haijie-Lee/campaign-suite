# spec-context.sh — spec 图摘要注入 hook（PreToolUse(Skill)）

> campaign-suite W2 产物。契约：W2 plan K0/K7；镜像 caliber `index-md.sh` 的「skill 调用前注入索引」模式。

## 行为

1. stdin 取 `tool_input.skill`，剥插件前缀 `${SKILL##*:}`（全限定名调用同样命中）。
2. skill ∈ {`plan-forge`, `spec-forge`, `ingest-forge`, `program-forge`} 才继续，否则静默。
3. **激活判据（K7）**：工程根存在 `adr/` 或 `docs/spec/` 或 `.campaign/` 任一，且 `.campaign/graph/graph.json` 存在——否则静默。
4. **注入图摘要**（信封 `{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":...}}`，`ensure_ascii=False`），摘要逐字三行：

```
doc-graph: nodes=<n> edges=<n> orphans=<n>
ids: FR=<n> NFR=<n> R=<n> D=<n> C=<n> Q=<n> AC=<n>
定计划前先查引用：python campaign/tools/doc_graph.py ripple --id <ID>
```

计数口径：`nodes`/`edges` = graph.json 两数组长度；`orphans` = reports 内 `orphans_defined_unreferenced` 与 `orphans_referenced_undefined` 两列表长度之和；ids 行 = 按节点 type 分类计数。

## 硬性规则（K0）

exit 恒 0、异常静默；stdout JSON 信封 python 编码（`ensure_ascii=False`）；读图前工程根 `cygpath -w`。
