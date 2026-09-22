#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ac-91 brief-conventions acceptance —— program.py cmd_brief 工程约定注入（K1/K3）、
lint() K6 WARN、cmd_gate lint_cmd 门（K7）+ env 钩子契约、无 lint_cmd gate
逐字节守护（KI-13 关闭态）的永久回归保护。八态逐字：

  1. 注入态：tmp 根 CONVENTIONS.md 两行 → brief 含「## 工程约定」(恰 1)、两行约定、
     派生声明行(恰 1)、「约束符合：产物不得违反」、「- D1 事实源」(D1–D4 回归)；
     不含「可执行检查」（无 lint_cmd）。
  2. 缺席态：无 CONVENTIONS.md → brief 含逐字「（未配置：CONVENTIONS.md 缺席）」。
  3. 截断态：CONVENTIONS.md 30 行 → brief 含 - rule-25、不含 - rule-26、
     含「约定文件超预算截断，全文见 CONVENTIONS.md」；stdout 含逐字截断 WARN。
  4. 门通过态：lint_cmd `python -c "import sys; sys.exit(0)"` + evidence/result 就位
     → gate rc=0、stdout 含「U-1: in_progress -> complete (gate PASS)」、
     prog.yaml 含「    status: complete」。
  5. 门失败态：lint_cmd exit(3) → gate rc=1、stdout 含「MISSING」与
     「lint_cmd 失败(rc=3)」、prog.yaml 仍含「    status: in_progress」（状态未迁移）。
  6. validate WARN 态（K6 回归保护）：同态 2（无 CONVENTIONS.md、无 lint_cmd）
     → rc=0、stdout 含逐字 K6 WARN、末行 ==「OK: 1 units, schema+lint pass」。
  7. env 契约态：lint_cmd 子进程断言 CAMPAIGN_UNIT=='U-1'、CAMPAIGN_PROGRAM
     以 prog.yaml 结尾、CAMPAIGN_WS isdir（违约 exit 7）→ gate rc=0，
     且 env.out 三值逐字/路径规范化命中期望。
  8. 无 lint_cmd 逐字节守护态（KI-13 关闭）：同态 4 fixture 去掉 lint_cmd
     → gate rc=0、stdout == 「U-1: in_progress -> complete (gate PASS)」逐字、
     prog.yaml 与 fixture(status=complete) 逐字节一致、ledger 事件序列 ==
     [(gate,U-1,PASS), (unit_end,U-1)]（ts 字段除外）。

编码纪律：所有 open() 显式 encoding='utf-8'；subprocess 用 text=True,
encoding='utf-8', errors='replace' 且 try/except 包住；fixture yaml 写文件用
newline='\n'，yaml 字符串零注释（# 起始行）与零制表符。每态独立
tempfile.TemporaryDirectory()；调 program.py 一律
[sys.executable, PROGRAM_PY, <cmd>, "--program", "prog.yaml"] + 追加参数，cwd=tmp。

打印顺序：先收集八态结果，首行总结行，随后八态明细（ok <n> / BAD <n>）。
任一 BAD → 首行 FAIL、exit 1；全过 → 首行 PASS、exit 0（run_all.py 归类契约）。
"""
import json
import os
import subprocess
import sys
import tempfile

# 仓库根 = 脚本位置上三级（脚本位于 campaign/acceptance/ 内），用 os.path 从
# __file__ 推，不依赖进程 cwd，与 runner 以 cwd=acceptance/ 调起本脚本兼容。
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROGRAM_PY = os.path.join(REPO_ROOT, "campaign", "tools", "program.py")

# K6 WARN 逐字行（态 6 断言用）与 validate 末行（契约精确值，逐字）。
K6_WARN = ("WARN: 程序零工程约定机械覆盖——风格约束仅靠 agent 自律"
           "（约定文件 CONVENTIONS.md 缺席且无 lint_cmd）")
VALIDATE_LAST = "OK: 1 units, schema+lint pass"


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def fixture_yaml(meta_lint=None, status="pending", unit_extra=()):
    """prog.yaml fixture：meta 五键 program/context/created/reconcile_every/
    last_reconciled（态 4/5 加 lint_cmd），units 单条 U-1。零注释、零制表符；
    `parallel: "-"` 带引号（mini parser 契约）；inline list 仅 gate 用。"""
    lines = [
        "program: ac-91-fixture",
        "context: ac-91 brief conventions acceptance fixture",
        "created: 2026-09-22",
        "reconcile_every: 5",
        "last_reconciled: 0",
    ]
    if meta_lint is not None:
        lines.append("lint_cmd: %s" % meta_lint)
    lines += [
        "units:",
        "  - id: U-1",
        "    title: acceptance fixture unit",
        "    status: %s" % status,
        '    parallel: "-"',
    ]
    lines.extend(unit_extra)
    return "\n".join(lines) + "\n"


def write_fixture(tmp, **kw):
    write_text(os.path.join(tmp, "prog.yaml"), fixture_yaml(**kw))


def run_prog(cmd, tmp, *extra):
    """调 program.py：argv = [python, program.py, cmd, --program, prog.yaml, *extra]，
    cwd=tmp。异常 → (None, 诊断)；正常 → (CompletedProcess, "")。"""
    argv = [sys.executable, PROGRAM_PY, cmd, "--program", "prog.yaml"] + list(extra)
    try:
        r = subprocess.run(argv, cwd=tmp, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
    except Exception as e:
        return None, "%s: %s" % (type(e).__name__, e)
    return r, ""


def brief_text(tmp):
    """brief 落盘路径（fixture 无 brief 键 → 缺省 .campaign/program/U-1-brief.md）。"""
    return os.path.join(tmp, ".campaign", "program", "U-1-brief.md")


def _read_brief(tmp, r, err):
    """读 brief 落盘文本；r/err 来自 run_prog。含 rc=0 契约断言（态 1–3 共用）。返回 (ok, 文本|诊断)。"""
    if err:
        return False, "program.py 调用异常: %s" % err
    if r.returncode != 0:
        return False, "brief rc=%d（应 0）stdout=%r stderr=%r" % (
            r.returncode, r.stdout, r.stderr)
    bp = brief_text(tmp)
    if not os.path.isfile(bp):
        return False, "brief 未写出 %s (rc=%d stdout=%r stderr=%r)" % (
            bp, r.returncode, r.stdout, r.stderr)
    return True, read_text(bp)


def check1():
    """态 1 注入态：CONVENTIONS.md 两行 → brief 约定节逐字注入。"""
    with tempfile.TemporaryDirectory() as tmp:
        write_fixture(tmp)
        write_text(os.path.join(tmp, "CONVENTIONS.md"),
                   "- 命名一律蛇形\n- 禁全局可变状态\n")
        r, err = run_prog("brief", tmp, "--unit", "U-1")
        ok, text = _read_brief(tmp, r, err)
        if not ok:
            return False, text
        if text.count("## 工程约定") != 1:
            return False, "「## 工程约定」出现 %d 次（应恰 1）" % text.count("## 工程约定")
        for s in ("- 命名一律蛇形", "- 禁全局可变状态"):
            if s not in text:
                return False, "brief 缺约定行 %r" % s
        if text.count("派生文件：program.py brief 重装配时整体重写") != 1:
            return False, "派生声明行缺失或非恰 1 次（K8 派生声明回归）"
        for s in ("约束符合：产物不得违反", "- D1 事实源"):
            if s not in text:
                return False, "brief 缺子串 %r" % s
        if "可执行检查" in text:
            return False, "无 lint_cmd 却含「可执行检查」"
    return True, "约定注入 + 派生声明 + D1 事实源锚 + 无可执行检查 全过"


def check2():
    """态 2 缺席态：无 CONVENTIONS.md → brief 含逐字未配置行。"""
    with tempfile.TemporaryDirectory() as tmp:
        write_fixture(tmp)
        r, err = run_prog("brief", tmp, "--unit", "U-1")
        ok, text = _read_brief(tmp, r, err)
        if not ok:
            return False, text
        if "（未配置：CONVENTIONS.md 缺席）" not in text:
            return False, "brief 缺逐字「（未配置：CONVENTIONS.md 缺席）」"
    return True, "缺席态：brief 含逐字未配置行"


def check3():
    """态 3 截断态：CONVENTIONS.md 30 行 → 截断到 rule-25，WARN 上 stdout。"""
    with tempfile.TemporaryDirectory() as tmp:
        write_fixture(tmp)
        write_text(os.path.join(tmp, "CONVENTIONS.md"),
                   "".join("- rule-%02d\n" % i for i in range(1, 31)))
        r, err = run_prog("brief", tmp, "--unit", "U-1")
        ok, text = _read_brief(tmp, r, err)
        if not ok:
            return False, text
        if "- rule-25" not in text:
            return False, "截断后 brief 缺 - rule-25"
        if "- rule-26" in text:
            return False, "截断后 brief 竟含 - rule-26"
        if "约定文件超预算截断，全文见 CONVENTIONS.md" not in text:
            return False, "brief 缺截断提示「约定文件超预算截断，全文见 CONVENTIONS.md」"
        if "WARN: CONVENTIONS.md 超 25 行，已按 brief 注入上限截断" not in r.stdout:
            return False, "stdout 缺逐字截断 WARN: %r" % r.stdout
    return True, "30 行截断到 rule-25 + WARN 逐字 + 截断提示行"


def check4():
    """态 4 门通过态：lint_cmd exit(0) + evidence/result 就位 → complete。"""
    with tempfile.TemporaryDirectory() as tmp:
        write_fixture(tmp, meta_lint='python -c "import sys; sys.exit(0)"',
                      status="in_progress",
                      unit_extra=("    gate: [evidence.txt]", "    result: result.md"))
        write_text(os.path.join(tmp, "evidence.txt"), "evidence\n")
        write_text(os.path.join(tmp, "result.md"), "# result\n")
        r, err = run_prog("gate", tmp, "--unit", "U-1")
        if err:
            return False, "program.py 调用异常: %s" % err
        if r.returncode != 0:
            return False, "gate rc=%d（应 0）stdout=%r stderr=%r" % (r.returncode, r.stdout, r.stderr)
        if "U-1: in_progress -> complete (gate PASS)" not in r.stdout:
            return False, "stdout 缺「U-1: in_progress -> complete (gate PASS)」: %r" % r.stdout
        if "    status: complete" not in read_text(os.path.join(tmp, "prog.yaml")):
            return False, "prog.yaml 状态未迁移到 complete"
    return True, "gate PASS：rc=0 + 状态 complete + 迁移行逐字"


def check5():
    """态 5 门失败态：lint_cmd exit(3) → MISSING，状态不迁移。"""
    with tempfile.TemporaryDirectory() as tmp:
        write_fixture(tmp, meta_lint='python -c "import sys; sys.exit(3)"',
                      status="in_progress",
                      unit_extra=("    gate: [evidence.txt]", "    result: result.md"))
        write_text(os.path.join(tmp, "evidence.txt"), "evidence\n")
        write_text(os.path.join(tmp, "result.md"), "# result\n")
        r, err = run_prog("gate", tmp, "--unit", "U-1")
        if err:
            return False, "program.py 调用异常: %s" % err
        if r.returncode != 1:
            return False, "gate rc=%d（应 1）stdout=%r stderr=%r" % (r.returncode, r.stdout, r.stderr)
        if "MISSING" not in r.stdout or "lint_cmd 失败(rc=3)" not in r.stdout:
            return False, "stdout 缺 MISSING / lint_cmd 失败(rc=3): %r" % r.stdout
        if "    status: in_progress" not in read_text(os.path.join(tmp, "prog.yaml")):
            return False, "prog.yaml 状态竟已迁移（应保持 in_progress）"
    return True, "gate MISSING：rc=1 + lint_cmd 失败(rc=3) + 状态不迁移"


def check6():
    """态 6 validate WARN 态（K6 回归保护）：无 CONVENTIONS.md、无 lint_cmd。"""
    with tempfile.TemporaryDirectory() as tmp:
        write_fixture(tmp)
        r, err = run_prog("validate", tmp)
        if err:
            return False, "program.py 调用异常: %s" % err
        if r.returncode != 0:
            return False, "validate rc=%d（应 0）stdout=%r stderr=%r" % (r.returncode, r.stdout, r.stderr)
        if K6_WARN not in r.stdout:
            return False, "stdout 缺逐字 K6 WARN: %r" % r.stdout
        lines = r.stdout.strip().split("\n")
        if not lines or lines[-1] != VALIDATE_LAST:
            return False, "stdout 末行 %r（应 %r）" % (lines[-1] if lines else "(空)", VALIDATE_LAST)
    return True, "validate WARN：K6 逐字 + 末行 OK"


# 态 7 fixture 脚本：子进程自检 env 契约三键并落 env.out；违约 exit 7。
# 走脚本文件而非 python -c 单行——cmd.exe 引号/管道折叠会截断复杂 payload。
ENV_CHECK_PY = ("\n".join([
    "import os, sys",
    'u = os.environ.get("CAMPAIGN_UNIT", "")',
    'p = os.environ.get("CAMPAIGN_PROGRAM", "")',
    'w = os.environ.get("CAMPAIGN_WS", "")',
    'with open("env.out", "w", encoding="utf-8") as f:',
    '    f.write(u + "|" + p + "|" + w)',
    'sys.exit(0 if (u == "U-1" and p.endswith("prog.yaml") '
    'and os.path.isdir(w)) else 7)',
]) + "\n")


def check7():
    """态 7 env 契约态：gate 执行 lint_cmd 时注入 CAMPAIGN_UNIT/PROGRAM/WS。"""
    with tempfile.TemporaryDirectory() as tmp:
        write_fixture(tmp, meta_lint="python check_env.py", status="in_progress",
                      unit_extra=("    gate: [evidence.txt]", "    result: result.md"))
        write_text(os.path.join(tmp, "check_env.py"), ENV_CHECK_PY)
        write_text(os.path.join(tmp, "evidence.txt"), "evidence\n")
        write_text(os.path.join(tmp, "result.md"), "# result\n")
        r, err = run_prog("gate", tmp, "--unit", "U-1")
        if err:
            return False, "program.py 调用异常: %s" % err
        if r.returncode != 0:
            return False, "gate rc=%d（应 0；rc=7 = env 契约违约）stdout=%r stderr=%r" % (
                r.returncode, r.stdout, r.stderr)
        ep = os.path.join(tmp, "env.out")
        if not os.path.isfile(ep):
            return False, "env.out 未写出（lint_cmd 未跑？）"
        u, p, w = (read_text(ep).split("|") + ["", "", ""])[:3]
        if u != "U-1":
            return False, "CAMPAIGN_UNIT %r（应 'U-1'）" % u
        same = lambda a, b: os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))
        if not (p.endswith("prog.yaml") and same(p, os.path.join(tmp, "prog.yaml"))):
            return False, "CAMPAIGN_PROGRAM %r 未指向 %s" % (p, os.path.join(tmp, "prog.yaml"))
        if not same(w, tmp):
            return False, "CAMPAIGN_WS %r 未指向工程根 %s" % (w, tmp)
    return True, "env 契约：CAMPAIGN_UNIT 逐字 + PROGRAM/WS 路径规范化命中"


def check8():
    """态 8 无 lint_cmd 逐字节守护（KI-13 关闭态）：gate stdout/prog.yaml/
    ledger 事件序列与基线逐字节一致（ledger ts 字段除外）。"""
    with tempfile.TemporaryDirectory() as tmp:
        extras = ("    gate: [evidence.txt]", "    result: result.md")
        write_fixture(tmp, status="in_progress", unit_extra=extras)
        write_text(os.path.join(tmp, "evidence.txt"), "evidence\n")
        write_text(os.path.join(tmp, "result.md"), "# result\n")
        r, err = run_prog("gate", tmp, "--unit", "U-1")
        if err:
            return False, "program.py 调用异常: %s" % err
        if r.returncode != 0:
            return False, "gate rc=%d（应 0）stdout=%r stderr=%r" % (r.returncode, r.stdout, r.stderr)
        if r.stdout != "U-1: in_progress -> complete (gate PASS)\n":
            return False, "stdout 非逐字基线: %r" % r.stdout
        want_yaml = fixture_yaml(status="complete", unit_extra=extras)
        got_yaml = read_text(os.path.join(tmp, "prog.yaml"))
        if got_yaml != want_yaml:
            return False, "prog.yaml 非逐字基线: %r（应 %r）" % (got_yaml, want_yaml)
        lp = os.path.join(tmp, ".campaign", "program", "ac-91-fixture-ledger.jsonl")
        if not os.path.isfile(lp):
            return False, "ledger 未生成: %s" % lp
        seq = []
        for ln in read_text(lp).splitlines():
            rec = json.loads(ln)
            seq.append((rec.get("event"), rec.get("unit"), rec.get("detail")))
        if seq != [("gate", "U-1", "PASS"), ("unit_end", "U-1", None)]:
            return False, "ledger 事件序列非基线: %r" % (seq,)
    return True, "无 lint_cmd gate：stdout/prog.yaml/ledger 事件序列逐字节钉住"


def main():
    results = []
    results.append(("1",) + check1())
    results.append(("2",) + check2())
    results.append(("3",) + check3())
    results.append(("4",) + check4())
    results.append(("5",) + check5())
    results.append(("6",) + check6())
    results.append(("7",) + check7())
    results.append(("8",) + check8())

    passed = sum(1 for _, ok, _ in results if ok)
    if passed == len(results):
        print("PASS ac-91 brief-conventions acceptance (%d/8 states)" % passed)
    else:
        print("FAIL ac-91 brief-conventions acceptance (%d/8 states)" % passed)
    for n, ok, desc in results:
        print("%s %s %s" % ("ok" if ok else "BAD", n, desc))
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
