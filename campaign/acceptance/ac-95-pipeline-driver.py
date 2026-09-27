#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ac-95 pipeline-driver acceptance —— campaign 流水线驱动行为六态的永久回归
保护。被测对象：program.py rolling（STATUS_ENUM 五态 / cmd_start sketch 拒绝 /
refine / add-sketch / drop-sketch / lint C5 WARN / _atomic_save / cmd_brief 占位
联动）+ 三 forge 回调行 + 主/副 SKILL.md 静态锚。六态逐字：

  1. rolling 排除：fixture（planning: rolling + u-sketch 四键 + u-a pending）→
     status 输出 u-sketch 行且 status 列 = sketch；next 输出 u-a；start u-sketch
     exit≠0 且输出含「须先细化」。
  2. refine 合并语义：refine u-sketch（title/gate/result 三 field + --ruling）
     → exit 0 含「refine: u-sketch sketch -> pending」；yaml 七键齐、status=
     pending、depends 继承；ledger 含 ruling 事件且 detail 含核对文本；未传
     brief（缺省 -）后 brief --unit → 落盘 .campaign/program/u-sketch-brief.md
     而非名为 - 的文件；start u-sketch → exit 0。
  3. add/drop 往返：add-sketch u-b → exit 0 含「add-sketch: u-b」，status 含
     u-b sketch 行；drop-sketch u-b → exit 0 含「drop-sketch: u-b」，status 不
     再含 u-b；drop-sketch u-a（pending）→ exit≠0 含「非 sketch」；refine
     u-a（pending）→ exit≠0 含「非 sketch」（整块重写丢键守卫）。
  4. C5 WARN 双向：rolling+fold_grant fixture → validate 含「双重折叠」WARN
     且 exit 0；非 rolling+fold_grant fixture → validate 无该 WARN。
  5. 静态锚：三 forge 各「经 campaign 入口进入时」计数=1；campaign
     SKILL.md 含「## Step 2 — 状态回路」计数=1；program-forge SKILL.md 含
     「rolling」计数≥1。
  6. 兼容守护：非 rolling fixture 的 validate/status/next 输出 == BASELINE
     三常量（批前 program.py 固化，逐字节）。

任一 BAD → 首行 FAIL、exit 1；全过 → 首行
PASS ac-95 pipeline-driver (6/6 states)、exit 0。
"""
import json
import os
import re
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROGRAM_PY = os.path.join(REPO_ROOT, "campaign", "tools", "program.py")
SKILLS_DIR = os.path.join(REPO_ROOT, "campaign", "skills")

# 兼容守护态基线（T3 步 0 由批前 program.py 对同一 fixture 实跑固化；
# 态 6 就位前以 None 占位——占位时态 6 跳过并计 PASS 的语义禁止：见 check6）
BASELINE_VALIDATE = 'WARN: 程序零工程约定机械覆盖——风格约束仅靠 agent 自律（约定文件 CONVENTIONS.md 缺席且无 lint_cmd）\nOK: 1 units, schema+lint pass\n'
BASELINE_STATUS = 'program: ac-95-plain  (reconcile_every=5 last_reconciled=0)\nu-a        pending     depends=-            单元 FR-1\neligible: u-a\n'
BASELINE_NEXT = 'u-a\n'

ROLLING_YAML = """program: ac-95-rolling
context: ac-95 pipeline driver fixture
created: 2026-09-28
reconcile_every: 5
last_reconciled: 0
planning: rolling
units:
  - id: u-sketch
    title: 远景占位单元
    status: sketch
    depends: []
  - id: u-a
    title: 近景单元 FR-1
    status: pending
    depends: []
    gate: [u-a-result.md]
    brief: u-a-brief.md
    result: u-a-result.md
"""

FOLD_YAML = """program: ac-95-fold
context: ac-95 C5 WARN fixture
created: 2026-09-28
reconcile_every: 5
last_reconciled: 0
fold_grant: srs_frozen
units:
  - id: u-a
    title: 单元 FR-1
    status: pending
    depends: []
    gate: [u-a-result.md]
    result: u-a-result.md
"""

PLAIN_YAML = """program: ac-95-plain
context: ac-95 baseline fixture
created: 2026-09-28
reconcile_every: 5
last_reconciled: 0
units:
  - id: u-a
    title: 单元 FR-1
    status: pending
    depends: []
    gate: [u-a-result.md]
    result: u-a-result.md
"""

RULING_TEXT = "三条件核对:授权✓无待决✓无不可逆✓"


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def run_prog(cmd, tmp, prog_file, *extra):
    """调 program.py，cwd=tmp，program 文件名可变。返回 CompletedProcess。"""
    argv = [sys.executable, PROGRAM_PY, cmd, "--program", prog_file] + list(extra)
    return subprocess.run(argv, cwd=tmp, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def ledger_rows(tmp):
    """读 tmp 下 .campaign/program/<program>-ledger.jsonl 全部事件行。"""
    d = os.path.join(tmp, ".campaign", "program")
    if not os.path.isdir(d):
        return []
    out = []
    for f in os.listdir(d):
        if f.endswith("-ledger.jsonl"):
            for line in read_text(os.path.join(d, f)).splitlines():
                line = line.strip()
                if line:
                    out.append(json.loads(line))
    return out


def check1():
    """rolling 排除三断言。"""
    tmp = tempfile.mkdtemp(prefix="ac95-s1-")
    write_text(os.path.join(tmp, "prog.yaml"), ROLLING_YAML)
    r = run_prog("status", tmp, "prog.yaml")
    if r.returncode != 0:
        return False, "status exit=%d: %s" % (r.returncode, (r.stderr or r.stdout)[-200:])
    line = next((ln for ln in r.stdout.splitlines() if ln.startswith("u-sketch")), None)
    if line is None:
        return False, "status 输出无 u-sketch 行"
    cols = line.split()
    if len(cols) < 2 or cols[1] != "sketch":
        return False, "u-sketch status 列 != sketch: %r" % line
    r = run_prog("next", tmp, "prog.yaml")
    if r.returncode != 0 or r.stdout.strip() != "u-a":
        return False, "next != u-a: %r" % r.stdout.strip()
    r = run_prog("start", tmp, "prog.yaml", "--unit", "u-sketch")
    if r.returncode == 0:
        return False, "start u-sketch 竟然 exit 0"
    if "须先细化" not in (r.stdout + r.stderr):
        return False, "start u-sketch 拒绝输出无「须先细化」: %r" % (r.stdout + r.stderr)[-200:]
    return True, "sketch 行/next=u-a/start 拒绝三断言全过"


def check2():
    """refine 合并语义 + ledger ruling + brief 占位联动 + start。"""
    tmp = tempfile.mkdtemp(prefix="ac95-s2-")
    write_text(os.path.join(tmp, "prog.yaml"), ROLLING_YAML)
    r = run_prog("refine", tmp, "prog.yaml", "--unit", "u-sketch",
                 "--field", "title:细化后的近景单元 FR-9",
                 "--field", "gate:[u-sketch-result.md]",
                 "--field", "result:u-sketch-result.md",
                 "--ruling", RULING_TEXT)
    if r.returncode != 0:
        return False, "refine exit=%d: %s" % (r.returncode, (r.stdout + r.stderr)[-300:])
    if "refine: u-sketch sketch -> pending" not in r.stdout:
        return False, "refine stdout 缺契约串: %r" % r.stdout[-200:]
    body = read_text(os.path.join(tmp, "prog.yaml"))
    for key in ("id:", "title:", "status: pending", "depends:", "gate:", "brief:", "result:"):
        if key not in body:
            return False, "refine 后 yaml 缺键 %r" % key
    if "细化后的近景单元 FR-9" not in body:
        return False, "refine 后 title 未更新"
    if "gate: [u-sketch-result.md]" not in body or "result: u-sketch-result.md" not in body:
        return False, "refine 后 gate/result 新值未落盘"
    rows = ledger_rows(tmp)
    if not any(row.get("event") == "ruling" and RULING_TEXT in str(row.get("detail", ""))
               for row in rows):
        return False, "ledger 无 ruling 事件或 detail 缺核对文本"
    # brief 占位联动：refine 未传 brief（缺省 -）→ brief 落缺省路径
    r = run_prog("brief", tmp, "prog.yaml", "--unit", "u-sketch")
    if r.returncode != 0:
        return False, "brief exit=%d: %s" % (r.returncode, (r.stdout + r.stderr)[-200:])
    expect = os.path.join(".campaign", "program", "u-sketch-brief.md")
    if expect not in r.stdout.replace("/", os.sep) and expect not in r.stdout:
        return False, "brief 输出路径非缺省形态: %r" % r.stdout[-200:]
    if os.path.exists(os.path.join(tmp, "-")):
        return False, "出现了名为 - 的劫持文件"
    # start（cmd_start 只验 status/eligible，不查 gate 证据——gate 归 cmd_gate）
    r = run_prog("start", tmp, "prog.yaml", "--unit", "u-sketch")
    if r.returncode != 0:
        return False, "refine 后 start exit=%d: %s" % (r.returncode, (r.stdout + r.stderr)[-200:])
    return True, "refine 七键/ledger ruling/brief 占位/start 全过"


def check3():
    """add-sketch / drop-sketch 往返 + 非 sketch 拒绝。"""
    tmp = tempfile.mkdtemp(prefix="ac95-s3-")
    write_text(os.path.join(tmp, "prog.yaml"), ROLLING_YAML)
    r = run_prog("add-sketch", tmp, "prog.yaml",
                 "--field", "id:u-b", "--field", "title:新增远景单元",
                 "--ruling", RULING_TEXT)
    if r.returncode != 0 or "add-sketch: u-b" not in r.stdout:
        return False, "add-sketch 失败: exit=%s %r" % (r.returncode, (r.stdout + r.stderr)[-200:])
    r = run_prog("status", tmp, "prog.yaml")
    if not any(ln.startswith("u-b") and "sketch" in ln for ln in r.stdout.splitlines()):
        return False, "add 后 status 无 u-b sketch 行"
    r = run_prog("drop-sketch", tmp, "prog.yaml", "--unit", "u-b",
                 "--ruling", RULING_TEXT)
    if r.returncode != 0 or "drop-sketch: u-b" not in r.stdout:
        return False, "drop-sketch 失败: exit=%s %r" % (r.returncode, (r.stdout + r.stderr)[-200:])
    r = run_prog("status", tmp, "prog.yaml")
    if any(ln.startswith("u-b") for ln in r.stdout.splitlines()):
        return False, "drop 后 status 仍含 u-b"
    r = run_prog("drop-sketch", tmp, "prog.yaml", "--unit", "u-a",
                 "--ruling", RULING_TEXT)
    if r.returncode == 0:
        return False, "drop 非 sketch 竟然 exit 0"
    if "非 sketch" not in (r.stdout + r.stderr):
        return False, "drop 非 sketch 拒绝文案缺失: %r" % (r.stdout + r.stderr)[-200:]
    r = run_prog("refine", tmp, "prog.yaml", "--unit", "u-a",
                 "--field", "title:改标题", "--field", "gate:[x.md]",
                 "--field", "result:x.md", "--ruling", RULING_TEXT)
    if r.returncode == 0:
        return False, "refine 非 sketch 竟然 exit 0（整块重写静默丢键风险，HIGH 守卫）"
    if "非 sketch" not in (r.stdout + r.stderr):
        return False, "refine 非 sketch 拒绝文案缺失: %r" % (r.stdout + r.stderr)[-200:]
    return True, "add/drop 往返 + drop/refine 非 sketch 双拒绝全过"


def check4():
    """C5 WARN 双向。"""
    tmp = tempfile.mkdtemp(prefix="ac95-s4-")
    write_text(os.path.join(tmp, "rolling.yaml"), ROLLING_YAML.replace(
        "last_reconciled: 0", "last_reconciled: 0\nfold_grant: srs_frozen"))
    r = run_prog("validate", tmp, "rolling.yaml")
    if r.returncode != 0:
        return False, "rolling+fold validate exit=%d: %s" % (r.returncode, (r.stdout + r.stderr)[-200:])
    if "双重折叠" not in r.stdout:
        return False, "rolling+fold_grant 无「双重折叠」WARN: %r" % r.stdout[-300:]
    write_text(os.path.join(tmp, "fold.yaml"), FOLD_YAML)
    r = run_prog("validate", tmp, "fold.yaml")
    if r.returncode != 0:
        return False, "fold-only validate exit=%d" % r.returncode
    if "双重折叠" in r.stdout:
        return False, "非 rolling 出现「双重折叠」WARN（反向断言炸）"
    return True, "rolling+fold 有 WARN / 非 rolling 无 WARN 双向过"


def check5():
    """静态锚五断言：三 forge 回调行各计数=1；campaign 状态回路节标题=1；
    program-forge rolling 命中行≥1（grep -c 语义：一行多命中只计 1）。"""
    for name in ("ingest-forge", "trans-forge", "spec-forge"):
        p = os.path.join(SKILLS_DIR, name, "SKILL.md")
        if not os.path.isfile(p):
            return False, "%s SKILL.md 不存在: %s" % (name, p)
        n = read_text(p).count("经 campaign 入口进入时")
        if n != 1:
            return False, "%s 回调行计数=%d（应恰 1）" % (name, n)
    n = read_text(os.path.join(SKILLS_DIR, "campaign", "SKILL.md")).count(
        "## Step 2 — 状态回路")
    if n != 1:
        return False, "campaign SKILL.md 状态回路节标题计数=%d（应恰 1）" % n
    hits = sum(1 for ln in read_text(os.path.join(
        SKILLS_DIR, "program-forge", "SKILL.md")).splitlines() if "rolling" in ln)
    if hits < 1:
        return False, "program-forge SKILL.md 无 rolling 命中行"
    return True, "三 forge 回调行/状态回路节标题/rolling 命中行五断言全过"


def check6():
    """兼容守护：非 rolling fixture 三命令输出 == BASELINE 常量。"""
    if BASELINE_VALIDATE is None or BASELINE_STATUS is None or BASELINE_NEXT is None:
        return False, "BASELINE 常量未固化（T3 步 0(ii) 未回填）"
    tmp = tempfile.mkdtemp(prefix="ac95-s6-")
    write_text(os.path.join(tmp, "prog.yaml"), PLAIN_YAML)
    r = run_prog("validate", tmp, "prog.yaml")
    if r.stdout != BASELINE_VALIDATE:
        return False, "validate 输出 != 基线: %r vs %r" % (r.stdout[-200:], BASELINE_VALIDATE[-200:])
    r = run_prog("status", tmp, "prog.yaml")
    if r.stdout != BASELINE_STATUS:
        return False, "status 输出 != 基线"
    r = run_prog("next", tmp, "prog.yaml")
    if r.stdout != BASELINE_NEXT:
        return False, "next 输出 != 基线"
    return True, "validate/status/next 与批前基线逐字节一致"


def main():
    results = []
    results.append(("1",) + check1())
    results.append(("2",) + check2())
    results.append(("3",) + check3())
    results.append(("4",) + check4())
    results.append(("5",) + check5())
    results.append(("6",) + check6())
    passed = sum(1 for _, ok, _ in results if ok)
    head = "PASS" if passed == len(results) else "FAIL"
    print("%s ac-95 pipeline-driver (%d/%d states)" % (head, passed, len(results)))
    for n, ok, desc in results:
        print("%s %s %s" % ("ok" if ok else "BAD", n, desc))
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
