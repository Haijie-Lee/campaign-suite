#!/usr/bin/env bash
# campaign 插件 Stop hook：spec 收尾提醒（campaign-suite W2，契约 K0/K6/K7）
# 镜像 caliber learnings-wrapup.sh 安全契约：stopHookActive 一律静默（防续跑循环）、
# 每会话至多 block 1 次（reminded 标记，仅在实际 block 时写入）。
# 明示差异：不采用 caliber 的 ≥3 次编辑门槛——W2 语义「改了 spec 一次即须外移叙事」。
# exit 恒 0；任何异常静默；禁 set -e。
INPUT=$(cat)
PY=$(command -v python 2>/dev/null || command -v python3 2>/dev/null || true)
[ -n "$PY" ] || exit 0

ACTIVE=$(printf '%s' "$INPUT" | "$PY" -c '
import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    print("");raise SystemExit
print("1" if (d.get("stopHookActive") or d.get("stop_hook_active")) else "")
' 2>/dev/null | tr -d '\r')
[ -n "$ACTIVE" ] && exit 0

SID=$(printf '%s' "$INPUT" | "$PY" -c '
import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    print("");raise SystemExit
v=d.get("session_id") or d.get("sessionId") or ""
print(v if isinstance(v,str) else "")
' 2>/dev/null | tr -d '\r')
[ -n "$SID" ] || SID="${CLAUDE_SESSION_ID:-}"
[ -n "$SID" ] || SID="nosid"
SID=$(printf '%s' "$SID" | tr -c 'A-Za-z0-9_-' '_')
M="/tmp/campaign-sg-$SID"

# K7 激活判据
PROJ="${ZCODE_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}}"
[ -d "$PROJ/adr" ] || [ -d "$PROJ/docs/spec" ] || [ -d "$PROJ/.campaign" ] || exit 0

# 门控：每会话至多 1 次
[ -f "$M-reminded" ] && exit 0
[ -f "$M-touched.jsonl" ] || exit 0

# 摸了 spec（K7 统一口径）且未摸 CHANGELOG/adr → block
grep -qE '"file":"[^"]*(/SRS\.md|/docs/spec/[^"]*\.md)' "$M-touched.jsonl" 2>/dev/null || exit 0
grep -qE '"file":"[^"]*(CHANGELOG|/adr/)' "$M-touched.jsonl" 2>/dev/null && exit 0

touch "$M-reminded" 2>/dev/null
"$PY" -c '
import json
reason="会话收尾检查：本会话改了 spec（SRS.md / docs/spec/）但未更新 CHANGELOG/ADR——修订协议要求变更叙事外移：① 变更理由与新证据落 CHANGELOG 或 adr/ 新条目；② 若本次改动只是笔误/格式，显式声明「零叙事变更」再收尾。"
print(json.dumps({"decision":"block","reason":reason},ensure_ascii=False,separators=(",",":")))
' 2>/dev/null
exit 0
