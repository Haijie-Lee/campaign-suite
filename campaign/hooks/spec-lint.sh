#!/usr/bin/env bash
# campaign 插件 PostToolUse(Write|Edit) hook：spec 棘轮 lint（campaign-suite W2）
# 契约 K0/K5/K6/K7：① 每次调用先记 touched（K6，bash 重定向——K0-5）；② K7 激活
# 判据（adr/ 或 docs/spec/ 或 .campaign/ 存在）；③ spec 路径命中时按 K5 棘轮语义
# lint（Edit=new_string / Write=content 限 10 条），命中即 additionalContext 注入。
# exit 恒 0；任何异常静默；禁 set -e。
INPUT=$(cat)
PY=$(command -v python 2>/dev/null || command -v python3 2>/dev/null || true)
[ -n "$PY" ] || exit 0

# stdin 解析：python 一次输出 4 行（SID / TOOL / FP / touched-JSON 行）
{ IFS= read -r SID; IFS= read -r TOOL; IFS= read -r FP; IFS= read -r TLINE; } < <(printf '%s' "$INPUT" | "$PY" -c '
import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    print("");print("");print("");print("");raise SystemExit
sid=d.get("session_id") or d.get("sessionId") or ""
tn=d.get("tool_name") or d.get("toolName") or ""
ti=d.get("tool_input") or d.get("toolInput") or {}
fp=ti.get("file_path","") if isinstance(ti,dict) else ""
if not isinstance(fp,str): fp=""
fp=fp.replace("\\","/")
print(sid if isinstance(sid,str) else "")
print(tn if isinstance(tn,str) else "")
print(fp)
print(json.dumps({"file":fp,"tool":tn},ensure_ascii=False) if fp and tn else "")
' 2>/dev/null | tr -d '\r')

# K6 先写 touched（先写后判激活；bash 重定向，python 只出字符串——K0-5）
[ -n "$SID" ] || SID="${CLAUDE_SESSION_ID:-}"
[ -n "$SID" ] || SID="nosid"
SID=$(printf '%s' "$SID" | tr -c 'A-Za-z0-9_-' '_')
M="/tmp/campaign-sg-$SID"
[ -n "$TLINE" ] && printf '%s\n' "$TLINE" >> "$M-touched.jsonl" 2>/dev/null

# K7 激活判据（声明即数据）
PROJ="${ZCODE_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}}"
[ -d "$PROJ/adr" ] || [ -d "$PROJ/docs/spec" ] || [ -d "$PROJ/.campaign" ] || exit 0

# K7 spec 路径模式（统一口径）
case "$FP" in
  */SRS.md|*/docs/spec/*.md|*/docs/spec/*.markdown) ;;
  *) exit 0 ;;
esac

# K5 棘轮 lint 引擎（cygpath 归一化工程根——K0-2）
PROJ_W=$(cygpath -w "$PROJ" 2>/dev/null || printf '%s' "$PROJ")
printf '%s' "$INPUT" | "$PY" -c '
import json,sys,re,os
tool=sys.argv[1]; proj=sys.argv[2]
try:
    d=json.load(sys.stdin)
except Exception:
    raise SystemExit
ti=d.get("tool_input") or d.get("toolInput") or {}
if not isinstance(ti,dict): raise SystemExit
fp=ti.get("file_path","") or ""
fp=fp.replace("\\","/")
text=""
if tool=="Edit": text=ti.get("new_string") or ""
elif tool=="Write": text=ti.get("content") or ""
if not text: raise SystemExit
fence=chr(96)*3
lines=[]; in_f=False
for no,ln in enumerate(text.split("\n"),1):
    if ln.strip().startswith(fence):
        in_f=not in_f; continue
    if not in_f: lines.append((no,ln))
words=["适当","尽量","必要时","按需","尽快","优化","友好"]
wf=os.path.join(proj,".campaign","lint-words.txt")
if os.path.isfile(wf):
    try:
        ws=[w.strip() for w in open(wf,encoding="utf-8") if w.strip()]
        if ws: words=ws
    except Exception: pass
scan=re.compile(r"(?<![\w/.-])(FR-\d+(?:\.\d+[a-z]?)?|NFR-\d+\.\d+|R\d+|D\d+|C\d+|Q\d+|AC-\d+)(?![\w.-])")
nfr_def=re.compile(r"(^\|\s*NFR-|NFR-\d+\.\d+\s*[:：])")
nodes=set(); graph_missing=False
try:
    g=json.load(open(os.path.join(proj,".campaign","graph","graph.json"),encoding="utf-8"))
    nodes={n.get("id","") for n in g.get("nodes",[])}
except Exception:
    graph_missing=True
hits=[]
for no,ln in lines:
    for w in words:
        if w in ln:
            hits.append("[spec-lint L1] %s:%d 命中「%s」→ 给出可验证的量化口径或删除" % (fp,no,w))
            break
    seen=set()
    for m in scan.finditer(ln):
        iid=m.group(1)
        if not graph_missing and iid not in nodes and iid not in seen:
            seen.add(iid)
            hits.append("[spec-lint L2] %s:%d 悬空引用 %s → 该 ID 未在 doc-graph 定义" % (fp,no,iid))
    if nfr_def.search(ln):
        if not re.search(r"\d",re.sub(r"NFR-\d+\.\d+","",ln)):
            hits.append("[spec-lint L3] %s:%d NFR 定义缺数值 → 补量词与阈值" % (fp,no))
if not hits: raise SystemExit
if tool=="Write" and len(hits)>10:
    n=len(hits); hits=hits[:10]+["…共 %d 条，仅示前 10" % n]
body=("[spec-lint] graph.json 缺失，L2 跳过\n" if graph_missing else "")+"\n".join(hits)
print(json.dumps({"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":body}},ensure_ascii=False))
' "$TOOL" "$PROJ_W" 2>/dev/null
exit 0
