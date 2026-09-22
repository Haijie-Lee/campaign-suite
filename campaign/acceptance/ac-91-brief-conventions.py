#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ac-91 brief-conventions acceptance —— program.py cmd_brief 工程约定注入（K1/K3）、
lint() K6 WARN、cmd_gate lint_cmd 门（K7）的永久回归保护。六态逐字：

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

编码纪律：所有 open() 显式 encoding='utf-8'；subprocess 用 text=True,
encoding='utf-8', errors='replace' 且 try/except 包住；fixture yaml 写文件用
newline='\n'，yaml 字符串零注释（# 起始行）与零制表符。每态独立
tempfile.TemporaryDirectory()；调 program.py 一律
[sys.executable, PROGRAM_PY, <cmd>, "--program", "prog.yaml"] + 追加参数，cwd=tmp。

打印顺序：先收集六态结果，首行总结行，随后六态明细（ok <n> / BAD <n>）。
任一 BAD → 首行 FAIL、exit 1；全过 → 首行 PASS、exit 0（run_all.py 归类契约）。
"""
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
    """读 brief 落盘文本；r/err 来自 run_prog。返回 (ok, 文本|诊断)。"""
    if err:
        return False, "program.py 调用异常: %s" % err
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
    return True, "约定注入 + 派生声明 + D1-D4 + 无可执行检查 全过"


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


def main():
    results = []
    results.append(("1",) + check1())
    results.append(("2",) + check2())
    results.append(("3",) + check3())
    results.append(("4",) + check4())
    results.append(("5",) + check5())
    results.append(("6",) + check6())

    passed = sum(1 for _, ok, _ in results if ok)
    if passed == len(results):
        print("PASS ac-91 brief-conventions acceptance (%d/6 states)" % passed)
    else:
        print("FAIL ac-91 brief-conventions acceptance (%d/6 states)" % passed)
    for n, ok, desc in results:
        print("%s %s %s" % ("ok" if ok else "BAD", n, desc))
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
