#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ac-94 bridge-behavior acceptance —— campaign×caliber 桥行为六态（C14）的永久
回归保护。被测对象：program.py 五桥函数（find_bridge/load_bridge/_unit_seed_text/
bridge_hits/_result_path）+ cmd_brief 身份节 + cmd_gate 桥合并（T2）、
handoff-inject.sh A2 三参形态（T4）。各态用 fixture 桥 + CALIBER_PLUGIN_DIR 指向，
不依赖真桥。六态逐字：

  1. 身份节注入：fixture 程序（单单元 U-1，无 lint_cmd）跑 brief → brief 含
     「## 编排身份」恰 1 次、含「你在 campaign 程序 ac-94-fixture 的单元 U-1
     执行中」、含「完工还账」、节序 = 编排身份在 单元目标 之前（index 断言）。
  2. 桥义务注入两分支：CALIBER_PLUGIN_DIR 指 fixture 桥（ui-forge 条目照 C2
     schema 四键齐备：paths=[docs/designs]、keywords=[页面]、brief_obligations
     非空、gate_artifacts 非空）；tmp 建 docs/designs/ 且单元 title 含「页面」
     → brief 含「机制义务（桥 ui-forge）」且 机制义务 index < 单元目标 index
     （位置断言：义务行必落在身份节内）；删 docs/designs 后重跑 brief →
     不含「机制义务」（paths 半边缺席即不命中，证明 AND 语义）。
  3. gate 桥合并 fail-closed：信号命中 fixture 下 gate_artifacts=
     [**/fidelity-report.md]；artifact 缺席 → gate exit 1 且 stdout 含 MISSING
     与 bridge:**/fidelity-report.md；落 fidelity-report.md 非空后再跑 → exit 0。
  4. 降级两分支：分支 a（无桥）= 子进程 env 设 CALIBER_PLUGIN_DIR=<tmp 空目录>
     且 USERPROFILE=<tmp 空 home>（Windows 实测 2026-09-26：expanduser("~")
     跟随 USERPROFILE、不读 HOME；同时写 HOME 兼容 POSIX）→ cache glob 落空，
     brief/gate 行为同无桥（brief 无「机制义务」、gate 不新增 missing）；分支 b
     （坏桥）= CALIBER_PLUGIN_DIR 指含坏 JSON 的目录 → stdout 含「WARN:
     campaign-bridge.json 解析失败」且 gate 不因此 MISSING（rc=0 走 PASS）。
  5. A2 hook 注入：tmp 造 .campaign/program/prog.yaml（单元 U-9
     status=in_progress、brief 键缺席 → 缺省路径）+ 对应 brief 文件（内容含
     标记串 A2-MARKER-9941）；subprocess 调 "C:/Program Files/Git/bin/bash.exe"
     <hook 绝对路径>（hook 路径自 REPO_ROOT 拼——run_all 以 cwd=acceptance/ 调
     起，相对路径必炸），stdin 喂 {"cwd":"<tmp>"}，env 清 ZCODE_PROJECT_DIR/
     CLAUDE_PROJECT_DIR（测 hook 内 PROJ 回退链的 stdin 分支）→ 断言 stdout 为
     单行 JSON 且 additionalContext 含 A2-MARKER-9941 与「在途单元 brief，A2」；
     bash 不存在 → 首行 BLOCKED-ENV、exit 3（先于一切结果行，ac-93 同款优先级）。
  6. 零触碰守卫：本态只对 campaign 仓跑 git status --porcelain（caliber 仓改动
     ——T1/T7/T10④/T11⑤——不在守卫范围，ac-92 check6 同款单仓语义）；
     WAVE_FILES 之外路径数 = 0；预存豁免逐字两条。事实前提：.caliber/ 与
     .campaign/ 已 gitignore（2026-09-26 实测 .gitignore 前两行），其下产物
     （tmp-verify 脚本、evidence 文件）不破守卫；git 异常/非零退出 → 本态 SKIP
     计通过并附降级说明行。

编码纪律（G3/G4）：所有 open() 显式 encoding='utf-8'；subprocess 用 text=True,
encoding='utf-8', errors='replace' 且 try/except 包住；fixture 写文件用
newline='\n'，fixture yaml 零注释与零制表符。每态独立
tempfile.TemporaryDirectory()。REPO_ROOT 自 __file__ 推（脚本位于
campaign/acceptance/ 内，上三级 = 仓根），不依赖进程 cwd。调 program.py 范式照
ac-91 的 run_prog，但其无 env 参数——本脚本内自写变体：env = os.environ.copy()
后 env_pop/env_update 逐态覆盖再传 subprocess，cwd 参数照 ac-91。

打印顺序：先收集六态结果，首行总结行，随后六态明细（ok <n> / BAD <n>）+
态 6 降级说明行（如有）。任一 BAD → 首行 FAIL、exit 1；全过 → 首行
PASS ac-94 bridge-behavior (6/6 states)、exit 0；bash 缺席 → 首行
BLOCKED-ENV、exit 3。
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

# 仓库根 = 脚本位置上三级（脚本位于 campaign/acceptance/ 内），用 os.path 从
# __file__ 推，不依赖进程 cwd，与 runner 以 cwd=acceptance/ 调起本脚本兼容。
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROGRAM_PY = os.path.join(REPO_ROOT, "campaign", "tools", "program.py")
# hook 路径必须绝对：run_all.py 以 cwd=acceptance/ 调起，相对路径必炸
HOOK_SH = os.path.join(REPO_ROOT, "campaign", "hooks", "handoff-inject.sh")
BASH_EXE = "C:/Program Files/Git/bin/bash.exe"

# 态 6 本 wave 文件清单（T1–T11 落于 campaign 仓的全部路径，穷举，brief 逐字）
WAVE_FILES = [
    "campaign/tools/program.py",
    "campaign/skills/program-forge/SKILL.md",
    "campaign/skills/campaign/SKILL.md",
    "campaign/skills/spec-forge/SKILL.md",
    "campaign/hooks/handoff-inject.sh",
    "campaign/hooks/handoff.md",
    "campaign/acceptance/ac-90-entry-skill-smoke.py",
    "campaign/acceptance/ac-92-trans-forge.py",
    "campaign/acceptance/ac-93-cross-contract.py",
    "campaign/acceptance/ac-94-bridge-behavior.py",
    "campaign/.zcode-plugin/plugin.json",
    "marketplace.json",
    ".claude-plugin/marketplace.json",
    "README.md",
    "docs/known-issues.md",
    "docs/plans/2026-09-26-campaign-caliber-fusion-plan.md",
    "campaign/skills/ingest-forge/SKILL.md",
    "campaign/skills/trans-forge/SKILL.md",
    "campaign/acceptance/ac-95-pipeline-driver.py",
    "campaign/skills/campaign/references/pipeline-cases.md",
    "docs/plans/2026-09-27-campaign-pipeline-driver-plan.md",
]
# 预存豁免（wave 前已存在的未跟踪件，brief 逐字；.caliber/ .campaign/ 已
# gitignore 天然豁免）
WAVE_EXEMPT = {
    "?? campaign/tools/__pycache__/",
    "?? docs/plans/2026-09-23-trans-forge-plan.md",
}

# 态 2/3 fixture 桥：ui-forge 条目照 C2 schema 四键齐备（paths/keywords/
# brief_obligations/gate_artifacts），结构与真桥（caliber/campaign-bridge.json）
# 同形；keywords 只留「页面」收窄命中面，义务行文案带 fixture 标记防与真桥串扰
BRIDGE_JSON = json.dumps({
    "bridge_version": 1,
    "min_campaign": "0.6.0",
    "entries": [{
        "skill": "ui-forge",
        "signal": {"paths": ["docs/designs"], "keywords": ["页面"]},
        "brief_obligations": ["页面实现须先跑 ui-forge 选材并落 fidelity-report"
                              "（ac-94 fixture 义务行）"],
        "gate_artifacts": ["**/fidelity-report.md"],
    }],
}, ensure_ascii=False, indent=2) + "\n"


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path, text):
    # fixture 落盘固定 LF（G3）——Windows 默认 CRLF 会混入被扫/被测文本
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def run_prog(cmd, tmp, *extra, env_over=None, env_pop=()):
    """调 program.py：argv = [python, program.py, cmd, --program, prog.yaml, *extra]，
    cwd=tmp（照 ac-91）。ac-91 的 run_prog 无 env 参数——本变体先 copy
    os.environ，env_pop 逐键剔除、env_over 逐键覆盖后传入（态 2–4 的桥定位与
    态 5 的 hook env 清洗都靠它；不传即继承外层 env）。异常 → (None, 诊断)。"""
    argv = [sys.executable, PROGRAM_PY, cmd, "--program", "prog.yaml"] + list(extra)
    env = os.environ.copy()
    for k in env_pop:
        env.pop(k, None)
    if env_over:
        env.update(env_over)
    try:
        r = subprocess.run(argv, cwd=tmp, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60, env=env)
    except Exception as e:
        return None, "%s: %s" % (type(e).__name__, e)
    return r, ""


def fixture_yaml(title="acceptance fixture unit", status="pending", unit_extra=()):
    """ws 侧 prog.yaml fixture：meta 五键 + 单单元 U-1。零注释、零制表符；
    `parallel: "-"` 带引号（mini parser 契约）。title 默认不含任何 ui-forge
    关键词，态 2/3/4 经 _write_signal_ws 覆写为含「页面」。"""
    lines = [
        "program: ac-94-fixture",
        "context: ac-94 bridge behavior acceptance fixture",
        "created: 2026-09-26",
        "reconcile_every: 5",
        "last_reconciled: 0",
        "units:",
        "  - id: U-1",
        "    title: %s" % title,
        "    status: %s" % status,
        '    parallel: "-"',
    ]
    lines.extend(unit_extra)
    return "\n".join(lines) + "\n"


def write_fixture(tmp, **kw):
    write_text(os.path.join(tmp, "prog.yaml"), fixture_yaml(**kw))


def write_bridge(tmp):
    """tmp/bridge/ 落 fixture 桥并返回桥目录（CALIBER_PLUGIN_DIR 指向它——
    find_bridge 只认 <dir>/campaign-bridge.json，目录名不限）。"""
    bdir = os.path.join(tmp, "bridge")
    os.makedirs(bdir)
    write_text(os.path.join(bdir, "campaign-bridge.json"), BRIDGE_JSON)
    return bdir


def _write_signal_ws(tmp, **kw):
    """信号可命中的 ws：title 含「页面」+ docs/designs 目录（桥 ui-forge 条目
    signal 两半齐）。供态 2/3/4——降级态也保留信号，为的是证明降级源于桥缺席
    而非信号不命中。"""
    write_fixture(tmp, title="落地页面交互细节", **kw)
    os.makedirs(os.path.join(tmp, "docs", "designs"))


def brief_path(tmp):
    """brief 落盘路径（fixture 无 brief 键 → 缺省 .campaign/program/U-1-brief.md）。"""
    return os.path.join(tmp, ".campaign", "program", "U-1-brief.md")


def _read_brief(tmp, r, err):
    """读 brief 落盘文本；r/err 来自 run_prog。含 rc=0 契约断言。返回 (ok, 文本|诊断)。"""
    if err:
        return False, "program.py 调用异常: %s" % err
    if r.returncode != 0:
        return False, "brief rc=%d（应 0）stdout=%r stderr=%r" % (
            r.returncode, r.stdout, r.stderr)
    bp = brief_path(tmp)
    if not os.path.isfile(bp):
        return False, "brief 未写出 %s (rc=%d stdout=%r stderr=%r)" % (
            bp, r.returncode, r.stdout, r.stderr)
    return True, read_text(bp)


def check1():
    """态 1 身份节注入：fixture 单单元 U-1 无 lint_cmd → brief 身份节四断言。
    身份行/完工还账/节序均与桥无关（桥命中只会在身份节内追加义务行），故此态
    不做 env 覆写。"""
    with tempfile.TemporaryDirectory() as tmp:
        write_fixture(tmp)
        r, err = run_prog("brief", tmp, "--unit", "U-1")
        ok, text = _read_brief(tmp, r, err)
        if not ok:
            return False, text
        if text.count("## 编排身份") != 1:
            return False, "「## 编排身份」出现 %d 次（应恰 1）" % text.count("## 编排身份")
        if "你在 campaign 程序 ac-94-fixture 的单元 U-1 执行中" not in text:
            return False, "brief 缺身份行逐字「你在 campaign 程序 ac-94-fixture 的单元 U-1 执行中」"
        if "完工还账" not in text:
            return False, "brief 缺「完工还账」"
        if not text.index("## 编排身份") < text.index("## 单元目标"):
            return False, "节序错：编排身份未落在单元目标之前"
    return True, "身份节：编排身份恰 1 + 身份行逐字 + 完工还账 + 节序（身份<目标）"


def check2():
    """态 2 桥义务注入两分支：信号双半齐 → 义务行入身份节；删 docs/designs
    （paths 半边缺席）→ 义务行消失。"""
    with tempfile.TemporaryDirectory() as tmp:
        bdir = write_bridge(tmp)
        _write_signal_ws(tmp)
        r, err = run_prog("brief", tmp, "--unit", "U-1",
                          env_over={"CALIBER_PLUGIN_DIR": bdir})
        ok, text = _read_brief(tmp, r, err)
        if not ok:
            return False, text
        if "机制义务（桥 ui-forge）" not in text:
            return False, "信号双半齐但 brief 缺「机制义务（桥 ui-forge）」：%r" % text
        if not text.index("机制义务") < text.index("## 单元目标"):
            return False, "义务行位置错：未落在身份节内（应先于「## 单元目标」）"
        shutil.rmtree(os.path.join(tmp, "docs", "designs"))
        r, err = run_prog("brief", tmp, "--unit", "U-1",
                          env_over={"CALIBER_PLUGIN_DIR": bdir})
        ok, text = _read_brief(tmp, r, err)
        if not ok:
            return False, text
        if "机制义务" in text:
            return False, "删 docs/designs 后 brief 竟仍含「机制义务」（AND 语义破）"
    return True, "桥义务：双半齐注入身份节（位置断言）+ 删 paths 后消失"


def check3():
    """态 3 gate 桥合并 fail-closed：bridge artifact 缺席 → rc=1 + MISSING +
    bridge:<pattern>；artifact 落盘非空 → rc=0（status/result 均就位，使唯一
    missing 恰为桥 artifact——首跑 stdout 可精确断言）。"""
    with tempfile.TemporaryDirectory() as tmp:
        bdir = write_bridge(tmp)
        _write_signal_ws(tmp, status="in_progress",
                         unit_extra=("    result: report.md",))
        write_text(os.path.join(tmp, "report.md"), "# result\n")
        r, err = run_prog("gate", tmp, "--unit", "U-1",
                          env_over={"CALIBER_PLUGIN_DIR": bdir})
        if err:
            return False, "program.py 调用异常: %s" % err
        if r.returncode != 1:
            return False, "gate rc=%d（应 1）stdout=%r stderr=%r" % (
                r.returncode, r.stdout, r.stderr)
        if "MISSING" not in r.stdout or "bridge:**/fidelity-report.md" not in r.stdout:
            return False, "stdout 缺 MISSING / bridge:**/fidelity-report.md: %r" % r.stdout
        # glob "**/fidelity-report.md" recursive=True 的零目录层命中已实测
        # （2026-09-26，Python 3.14）——artifact 落 tmp 根即可
        write_text(os.path.join(tmp, "fidelity-report.md"), "fidelity: pass\n")
        r, err = run_prog("gate", tmp, "--unit", "U-1",
                          env_over={"CALIBER_PLUGIN_DIR": bdir})
        if err:
            return False, "program.py 调用异常: %s" % err
        if r.returncode != 0:
            return False, "artifact 落盘后 gate rc=%d（应 0）stdout=%r stderr=%r" % (
                r.returncode, r.stdout, r.stderr)
    return True, "gate 桥合并 fail-closed：缺席 rc=1+MISSING+bridge:pattern，落盘非空后 rc=0"


def check4():
    """态 4 降级两分支：a 无桥（cache glob 落空）/ b 坏桥（WARN 一行 + None）。
    两分支各自独立 tmp；ws 均保留信号（页面 + docs/designs），证明行为差异只
    来自桥缺席/损坏。"""
    # 分支 a：CALIBER_PLUGIN_DIR=<空目录> + USERPROFILE=HOME=<空 home>——
    # find_bridge 的 env 路无桥文件、cache 路在空 home 下 glob 落空 → None。
    # Windows expanduser 跟随 USERPROFILE，HOME 同写为 POSIX 兼容（brief 逐字）
    with tempfile.TemporaryDirectory() as tmp:
        home = os.path.join(tmp, "empty-home")
        plug = os.path.join(tmp, "empty-plugin")
        os.makedirs(home)
        os.makedirs(plug)
        _write_signal_ws(tmp, status="in_progress",
                         unit_extra=("    result: report.md",))
        write_text(os.path.join(tmp, "report.md"), "# report\n")
        env_over = {"CALIBER_PLUGIN_DIR": plug, "USERPROFILE": home, "HOME": home}
        r, err = run_prog("brief", tmp, "--unit", "U-1", env_over=env_over)
        ok, text = _read_brief(tmp, r, err)
        if not ok:
            return False, "分支 a brief: %s" % text
        if "机制义务" in text:
            return False, "分支 a brief 竟含「机制义务」（cache glob 未落空？）"
        r, err = run_prog("gate", tmp, "--unit", "U-1", env_over=env_over)
        if err:
            return False, "分支 a gate 调用异常: %s" % err
        if r.returncode != 0 or "MISSING" in r.stdout:
            return False, "分支 a gate rc=%d stdout=%r（应 rc=0 且无新增 missing）" % (
                r.returncode, r.stdout)
    # 分支 b：坏 JSON 桥 → load_bridge 打 WARN 一行 + None，brief/gate 均按
    # 无桥走且不 crash
    with tempfile.TemporaryDirectory() as tmp:
        bdir = os.path.join(tmp, "bridge")
        os.makedirs(bdir)
        write_text(os.path.join(bdir, "campaign-bridge.json"), "{不是 JSON")
        _write_signal_ws(tmp, status="in_progress",
                         unit_extra=("    result: report.md",))
        write_text(os.path.join(tmp, "report.md"), "# report\n")
        r, err = run_prog("brief", tmp, "--unit", "U-1",
                          env_over={"CALIBER_PLUGIN_DIR": bdir})
        ok, text = _read_brief(tmp, r, err)
        if not ok:
            return False, "分支 b brief: %s" % text
        if "WARN: campaign-bridge.json 解析失败" not in r.stdout:
            return False, "分支 b brief stdout 缺解析失败 WARN: %r" % r.stdout
        if "机制义务" in text:
            return False, "分支 b brief 竟含「机制义务」（坏桥未降级为 None）"
        r, err = run_prog("gate", tmp, "--unit", "U-1",
                          env_over={"CALIBER_PLUGIN_DIR": bdir})
        if err:
            return False, "分支 b gate 调用异常: %s" % err
        if r.returncode != 0 or "gate PASS" not in r.stdout:
            return False, "分支 b gate rc=%d stdout=%r（坏桥不得产生 MISSING）" % (
                r.returncode, r.stdout)
    return True, "降级：无桥（brief 无义务 + gate rc=0）+ 坏桥（WARN 逐字 + gate 不 MISSING）"


def hook_fixture_yaml():
    """态 5 hook 侧 prog.yaml：U-9 in_progress 无 brief 键（缺省路径分支）+
    U-10 in_progress 相对 brief 键（KI-18 修复分支：相对键按程序目录解析；
    断言按修前必红设计）+ U-11 in_progress `brief: -` 占位（视同缺键走缺省路径，
    T3 步 3.5 占位语义 hook 侧联动）。零注释、零制表符。"""
    lines = [
        "program: ac-94-hook-fixture",
        "context: ac-94 state5 hook fixture",
        "created: 2026-09-26",
        "reconcile_every: 5",
        "last_reconciled: 0",
        "units:",
        "  - id: U-9",
        "    title: hook fixture unit",
        "    status: in_progress",
        '    parallel: "-"',
        "  - id: U-11",
        "    title: hook fixture dash brief unit",
        "    status: in_progress",
        '    brief: "-"',
        '    parallel: "-"',
        "  - id: U-10",
        "    title: hook fixture relative brief unit",
        "    status: in_progress",
        "    brief: U-10-brief.md",
        '    parallel: "-"',
    ]
    return "\n".join(lines) + "\n"


def check5():
    """态 5 A2 hook 注入：bash 手喂 stdin 单行 JSON（diagnosing-hooks §5 步 5
    方法）；env 清 ZCODE_PROJECT_DIR/CLAUDE_PROJECT_DIR 逼 PROJ 走 stdin cwd
    分支；断言 strict schema（顶层恰 1 键 + 内层恰 2 键）+ marker + A2 标记。"""
    with tempfile.TemporaryDirectory() as tmp:
        progdir = os.path.join(tmp, ".campaign", "program")
        os.makedirs(progdir)
        write_text(os.path.join(progdir, "prog.yaml"), hook_fixture_yaml())
        write_text(os.path.join(progdir, "U-9-brief.md"),
                   "# Unit Brief: U-9\n\nA2-MARKER-9941 在途 brief 正文。\n")
        write_text(os.path.join(progdir, "U-10-brief.md"),
                   "# Unit Brief: U-10\n\nA2-REL-MARKER-4410 相对键 brief 正文。\n")
        write_text(os.path.join(progdir, "U-11-brief.md"),
                   "# Unit Brief: U-11\n\nA2-DASH-MARKER-1100 占位键 brief 正文。\n")
        env = os.environ.copy()
        env.pop("ZCODE_PROJECT_DIR", None)
        env.pop("CLAUDE_PROJECT_DIR", None)
        try:
            r = subprocess.run(
                [BASH_EXE, HOOK_SH],
                input=json.dumps({"cwd": tmp}),
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=60, env=env, cwd=tmp)
        except Exception as e:
            return False, "hook 调用异常: %s: %s" % (type(e).__name__, e)
        if r.returncode != 0:
            return False, "hook rc=%d（契约恒 0）stdout=%r stderr=%r" % (
                r.returncode, r.stdout, r.stderr)
        out = r.stdout.strip()
        if not out:
            return False, "hook stdout 空（A2 未注入——parts 为空走了静默语义）"
        if "\n" in out:
            return False, "hook stdout 非单行: %r" % r.stdout
        try:
            obj = json.loads(out)
        except Exception as e:
            return False, "hook stdout 非合法 JSON（%s）: %r" % (e, out)
        # strict schema：多余键即验证失败（diagnosing-hooks 输出契约）
        if set(obj) != {"hookSpecificOutput"}:
            return False, "hook 输出顶层键 %r（应恰 {'hookSpecificOutput'}）" % sorted(obj)
        hso = obj["hookSpecificOutput"]
        if not isinstance(hso, dict) or set(hso) != {"hookEventName", "additionalContext"}:
            return False, "hookSpecificOutput 键 %r（应恰 event+context 两键）" % (
                sorted(hso) if isinstance(hso, dict) else hso)
        if hso.get("hookEventName") != "SessionStart":
            return False, "hookEventName=%r（应 SessionStart）" % hso.get("hookEventName")
        ctx = hso.get("additionalContext", "")
        if "A2-MARKER-9941" not in ctx:
            return False, "additionalContext 缺标记串 A2-MARKER-9941: %r" % ctx[:200]
        if "在途单元 brief，A2" not in ctx:
            return False, "additionalContext 缺「在途单元 brief，A2」标记: %r" % ctx[:200]
        # KI-18 分支：相对 brief 键（U-10）须按程序目录解析命中——修前 isfile 落空
        # 静默丢注入，本断言修前必红（不实测红态，T9 统一跑）
        if "A2-REL-MARKER-4410" not in ctx:
            return False, "additionalContext 缺相对键标记 A2-REL-MARKER-4410（KI-18 未修复？）: %r" % ctx[:200]
        # brief: - 占位分支（U-11）：`-` 视同缺键走缺省路径——rolling refine 缺省
        # 即写 brief: -，缺该回退则 rolling 标准流 A2 注入整条落空（MEDIUM 守卫）
        if "A2-DASH-MARKER-1100" not in ctx:
            return False, "additionalContext 缺占位键标记 A2-DASH-MARKER-1100（brief: - 未回退缺省路径？）: %r" % ctx[:200]
    return True, "A2 hook：strict JSON + marker×2 + 相对键/占位键 marker（KI-18 + brief:- 联动）"


def check6(notes):
    """零触碰守卫（单仓语义 = ac-92 check6）：只对 campaign 仓跑 porcelain；
    WAVE_FILES 穷举清单与两条预存豁免之外路径数=0。git 异常/非零退出 → SKIP
    计通过并附降级说明行（notes 由 main 在明细后打印）。"""
    try:
        r = subprocess.run(
            ["git", "-C", REPO_ROOT, "status", "--porcelain"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=60)
    except Exception as e:
        notes.append("note 6 降级: git 调用异常（%s: %s）" % (type(e).__name__, e))
        return True, "SKIP"
    if r.returncode != 0 or "fatal" in r.stderr:
        notes.append("note 6 降级: git rc=%d stderr=%s" % (r.returncode, r.stderr.strip()))
        return True, "SKIP"
    lines = [ln for ln in r.stdout.split("\n") if ln.strip()]
    unexpected = []
    for ln in lines:
        path = ln[3:].strip()
        if path in WAVE_FILES:
            continue
        if ln in WAVE_EXEMPT:
            continue
        unexpected.append(ln)
    if unexpected:
        return False, "wave 清单外路径 %d 个: %s" % (
            len(unexpected), " | ".join(unexpected[:5]))
    return True, "零触碰（porcelain 清单外路径=0）"


def main():
    # BLOCKED-ENV 先于一切结果行（ac-93 同款优先级）：bash 缺席则态 5 无从执行
    if not os.path.isfile(BASH_EXE):
        print("BLOCKED-ENV ac-94 bridge-behavior: bash 缺席（%s 不存在）——态 5 无法执行" % BASH_EXE)
        sys.exit(3)

    results = []
    results.append(("1",) + check1())
    results.append(("2",) + check2())
    results.append(("3",) + check3())
    results.append(("4",) + check4())
    results.append(("5",) + check5())
    notes = []
    ok6, desc6 = check6(notes)
    results.append(("6", ok6, desc6))

    passed = sum(1 for _, ok, _ in results if ok)
    head = "PASS" if passed == len(results) else "FAIL"
    print("%s ac-94 bridge-behavior (%d/%d states)" % (head, passed, len(results)))
    for n, ok, desc in results:
        print("%s %s %s" % ("ok" if ok else "BAD", n, desc))
    for note in notes:
        print(note)
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
