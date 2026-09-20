#!/usr/bin/env bash
# campaign 插件 PreToolUse(Skill) hook：spec 图摘要注入（campaign-suite W2）
# 契约 K0/K7（镜像 caliber index-md.sh）：skill ∈ {plan-forge, spec-forge,
# ingest-forge, program-forge} 且工程激活（adr/ 或 docs/spec/ 或 .campaign/）
# 且 .campaign/graph/graph.json 存在 → 注入图摘要三行。exit 恒 0；异常静默。
INPUT=$(cat)
PY=$(command -v python 2>/dev/null || command -v python3 2>/dev/null || true)
[ -n "$PY" ] || exit 0
SKILL=$(printf '%s' "$INPUT" | "$PY" -c '
import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    print("");raise SystemExit
ti=d.get("tool_input") or d.get("toolInput") or {}
print(ti.get("skill","") if isinstance(ti,dict) else "")
' 2>/dev/null)
SKILL="${SKILL##*:}"  # 剥插件前缀（镜像 index-md.sh：caliber:plan-forge→plan-forge）
case "$SKILL" in
  plan-forge|spec-forge|ingest-forge|program-forge) ;;
  *) exit 0 ;;
esac
PROJ="${ZCODE_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}}"
[ -d "$PROJ/adr" ] || [ -d "$PROJ/docs/spec" ] || [ -d "$PROJ/.campaign" ] || exit 0
[ -f "$PROJ/.campaign/graph/graph.json" ] || exit 0
PROJ_W=$(cygpath -w "$PROJ" 2>/dev/null || printf '%s' "$PROJ")
"$PY" -c '
import json,sys,os
proj=sys.argv[1]
try:
    g=json.load(open(os.path.join(proj,".campaign","graph","graph.json"),encoding="utf-8"))
except Exception:
    raise SystemExit
nodes=g.get("nodes",[]); edges=g.get("edges",[]); rep=g.get("reports",{})
orph=len(rep.get("orphans_defined_unreferenced",[]))+len(rep.get("orphans_referenced_undefined",[]))
counts={t:0 for t in ("FR","NFR","R","D","C","Q","AC")}
for n in nodes:
    t=n.get("type","")
    if t in counts: counts[t]+=1
body="doc-graph: nodes=%d edges=%d orphans=%d\nids: FR=%d NFR=%d R=%d D=%d C=%d Q=%d AC=%d\n定计划前先查引用：python campaign/tools/doc_graph.py ripple --id <ID>" % (
    len(nodes),len(edges),orph,
    counts["FR"],counts["NFR"],counts["R"],counts["D"],counts["C"],counts["Q"],counts["AC"])
print(json.dumps({"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":body}},ensure_ascii=False))
' "$PROJ_W" 2>/dev/null
exit 0
