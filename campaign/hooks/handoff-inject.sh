#!/usr/bin/env bash
# campaign 插件 SessionStart hook：工程有 .campaign/handoff.md 或
# .campaign/program/*-resume-note.md 或 .campaign/pipeline/*.md 则注入（生存包，K22）
# 契约：stdout=单行 JSON 或空输出；exit 恒 0；文件缺失/解析失败静默
# 工程根解析（短路顺序钉死）：ZCODE_PROJECT_DIR → CLAUDE_PROJECT_DIR → stdin(cwd/project_dir/projectDir) → PWD
# 相对 brief 键按程序目录解析（KI-18）；yaml 键写 MSYS 绝对形态（/f/...）时
# Windows ntpath isabs 判 True 但 open 可能失败——既有边缘输入，仅标注不处置
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
RND="$PROJ/.campaign/program"
PLD="$PROJ/.campaign/pipeline"
[ -f "$HF" ] || [ -d "$RND" ] || [ -d "$PLD" ] || exit 0

# MSYS → Windows 路径归一化（bash 的 [ -f ] 认 /c/...，Windows python 的 open() 不认；
# cygpath 不可用时原样传递——Windows 形式输入自然兼容）
HF_WIN=$(cygpath -w "$HF" 2>/dev/null || printf '%s' "$HF")
RND_WIN=$(cygpath -w "$RND" 2>/dev/null || printf '%s' "$RND")
PLD_WIN=$(cygpath -w "$PLD" 2>/dev/null || printf '%s' "$PLD")

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TOOLS_WIN=$(cygpath -w "$SCRIPT_DIR/../tools" 2>/dev/null || printf '%s' "$SCRIPT_DIR/../tools")

"$PY" -c "
import glob,json,os,sys
hf,rnd,tools,pld=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
parts=[]; names=[]
if os.path.isfile(hf):
    try:
        parts.append(open(hf,encoding='utf-8').read())
        names.append('.campaign/handoff.md')
    except Exception:
        pass
for f in sorted(glob.glob(os.path.join(rnd,'*-resume-note.md'))):
    try:
        parts.append('--- .campaign/program/'+os.path.basename(f)+' ---\n'+open(f,encoding='utf-8').read())
        names.append('.campaign/program/'+os.path.basename(f))
    except Exception:
        pass
for f in sorted(glob.glob(os.path.join(pld,'*.md'))):
    try:
        t=open(f,encoding='utf-8').read()
        lines=t.splitlines()
        if len(lines)>40:
            t='\n'.join(lines[:40])+'\n…（charter 超预算截断）'
        parts.append('--- .campaign/pipeline/'+os.path.basename(f)+'（流水线 charter） ---\n'+t)
        names.append('.campaign/pipeline/'+os.path.basename(f))
    except Exception:
        pass
# A2：在途单元 brief 注入（串行 v1：每程序至多 1 个 in_progress）
sys.path.insert(0, tools)
try:
    import program as _prog
except Exception:
    _prog = None
if _prog is not None:
    for y in sorted(glob.glob(os.path.join(rnd,'*.yaml'))):
        try:
            p = _prog.Program(y)
        except Exception:
            continue
        for u in p.units:
            if u.get('status') != 'in_progress':
                continue
            bp = str(u.get('brief') or '')
            bp = '' if bp == '-' else bp
            bp = bp if os.path.isabs(bp) else os.path.join(rnd, bp or (u['id']+'-brief.md'))
            if os.path.isfile(bp):
                try:
                    rel = '.campaign/program/'+os.path.basename(bp)
                    parts.append('--- '+rel+'（在途单元 brief，A2） ---\n'+open(bp,encoding='utf-8').read())
                    names.append(rel)
                except Exception:
                    pass
if not parts:
    raise SystemExit
tail='\n\n> 以上来自 '+ '、'.join(names) +'（campaign 生存包）'
print(json.dumps({'hookSpecificOutput':{'hookEventName':'SessionStart','additionalContext':'\n\n'.join(parts)+tail}},ensure_ascii=False))
" "$HF_WIN" "$RND_WIN" "$TOOLS_WIN" "$PLD_WIN" 2>/dev/null
exit 0
