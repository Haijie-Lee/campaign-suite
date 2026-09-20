#!/usr/bin/env bash
# campaign 插件 SessionStart hook：工程有 .campaign/handoff.md 则注入（生存包）
# 契约：stdout=单行 JSON 或空输出；exit 恒 0；文件缺失/解析失败静默
# 工程根解析（短路顺序钉死）：ZCODE_PROJECT_DIR → CLAUDE_PROJECT_DIR → stdin(cwd/project_dir/projectDir) → PWD
PROJ="${ZCODE_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-}}"
PY=$(command -v python 2>/dev/null || command -v python3 2>/dev/null || true)
[ -n "$PY" ] || exit 0

if [ -z "$PROJ" ]; then
  # env 均空才读 stdin；解析失败静默 exit 0
  INPUT=$(cat 2>/dev/null || true)
  PROJ=$(printf '%s' "$INPUT" | "$PY" -c "
import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    print(''); raise SystemExit
for k in ('cwd','project_dir','projectDir'):
    v=d.get(k)
    if isinstance(v,str) and v:
        print(v); break
else:
    print('')
" 2>/dev/null | tr -d '\r')
fi
[ -n "$PROJ" ] || PROJ="$PWD"

HF="$PROJ/.campaign/handoff.md"
[ -f "$HF" ] || exit 0

# MSYS → Windows 路径归一化（bash 的 [ -f ] 认 /c/...，Windows python 的 open() 不认；
# cygpath 不可用时原样传递——Windows 形式输入自然兼容）
HF_WIN=$(cygpath -w "$HF" 2>/dev/null || printf '%s' "$HF")

"$PY" -c "
import json,sys
body=open(sys.argv[1],encoding='utf-8').read()
tail='\n\n> 以上来自 .campaign/handoff.md（campaign 生存包）'
print(json.dumps({'hookSpecificOutput':{'hookEventName':'SessionStart','additionalContext':body+tail}},ensure_ascii=False))
" "$HF_WIN" 2>/dev/null
exit 0
