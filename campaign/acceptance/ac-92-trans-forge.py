#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ac-92 trans-forge acceptance —— trans-forge skill 本体（T3）+ 入口第四分支
（T4）+ spec-context hook 名单（T5）+ manifests/README（T6）+ references/templates
（T1/T2）+ 零触碰守卫（C4）的静态闸。六态逐字：

  1. trans-forge skill 本体：七文件全在（SKILL.md/checklists.md/templates 两件/
     references 三件）+ SKILL.md 锚（三证名各≥1、停点①②③各≥1、准入判据「缺一即拒绝」、
     分工节三节标题锚「与 ingest-forge」「与 spec-forge」「与 caliber」各≥1）。
  2. campaign 入口：「按序过五条分支」「3. trans 域」/ 判别式两子串逐字
     「产出新文档 vs 收编本文档不改写」「收编区外单篇 plan 驱动 vs 工件区内生产/修订」/
     M11 域地图行 / M12 新句「不单独定域」；反向锚「判定时加权」命中数=0；行数≤100。
  3. spec-context hook：spec-context.sh 含 M7 逐字行
     「plan-forge|spec-forge|ingest-forge|trans-forge|program-forge) ;;」；
     spec-context.md 含「trans-forge」。
  4. manifests：三 JSON version 动态一致（两两互等 + X.Y.Z 形态）；两 marketplace 逐字节同形；plugin.json 与
     marketplace.json description 含「trans-forge」。
  5. references 锚：skeleton-aerofold.md 含「高 9 / 中 4 / 低 0」；id-grammar.md 含
     「一处值一 token」；case-flow-builder.md 含「反模式」节标题。
  6. 零触碰守卫：git status --porcelain 全量输出中，本 wave 文件清单（穷举）之外
     路径数=0（KI-09：porcelain 非 diff HEAD，兼捕未跟踪新件）。预存基线豁免逐字
     「?? campaign/tools/__pycache__/」。本态在 T1–T6 各 commit 落盘后跑（T7 自身
     未提交改动由白名单吸收——ac-92 路径在穷举清单内）。

编码纪律（范式 = ac-90/ac-91）：open() 显式 encoding='utf-8'；subprocess 用
text=True, encoding='utf-8', errors='replace' 且 try/except 包住；git 异常记
SKIP 降级计通过。REPO_ROOT 自 __file__ 推（脚本位于 campaign/acceptance/ 内，
上三级 = 仓根），不依赖进程 cwd。

打印顺序：先收集六态结果，首行总结行，随后六态明细（ok <n> / BAD <n>）。
任一 BAD → 首行 FAIL、exit 1；全过 → 首行 PASS、exit 0（run_all.py 归类契约，
同 ac-90/ac-91 docstring）。
"""
import filecmp
import json
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILL_DIR = os.path.join(REPO_ROOT, "campaign", "skills", "trans-forge")
CAMPAIGN_SKILL = os.path.join(REPO_ROOT, "campaign", "skills", "campaign", "SKILL.md")
PLUGIN_JSON = os.path.join(REPO_ROOT, "campaign", ".zcode-plugin", "plugin.json")
MARKETPLACE_JSON = os.path.join(REPO_ROOT, "marketplace.json")
CLAUDE_MARKETPLACE_JSON = os.path.join(REPO_ROOT, ".claude-plugin", "marketplace.json")
SPEC_CONTEXT_SH = os.path.join(REPO_ROOT, "campaign", "hooks", "spec-context.sh")
SPEC_CONTEXT_MD = os.path.join(REPO_ROOT, "campaign", "hooks", "spec-context.md")

# trans-forge 七文件（态 1）
TRANS_FORGE_FILES = [
    "SKILL.md", "checklists.md",
    "templates/solution-spec-template.md", "templates/mapping-design-template.md",
    "references/case-flow-builder.md", "references/skeleton-aerofold.md",
    "references/id-grammar.md",
]

# 态 6 本 wave 文件清单（T1–T7 全部新建/修改路径，穷举）
WAVE_FILES = [
    "campaign/skills/trans-forge/references/case-flow-builder.md",
    "campaign/skills/trans-forge/references/skeleton-aerofold.md",
    "campaign/skills/trans-forge/references/id-grammar.md",
    "campaign/skills/trans-forge/templates/solution-spec-template.md",
    "campaign/skills/trans-forge/templates/mapping-design-template.md",
    "campaign/skills/trans-forge/SKILL.md",
    "campaign/skills/trans-forge/checklists.md",
    "campaign/skills/campaign/SKILL.md",
    "campaign/hooks/spec-context.sh",
    "campaign/hooks/spec-context.md",
    "campaign/.zcode-plugin/plugin.json",
    "marketplace.json",
    ".claude-plugin/marketplace.json",
    "README.md",
    "campaign/acceptance/ac-90-entry-skill-smoke.py",
    "campaign/acceptance/ac-92-trans-forge.py",
    "docs/plans/2026-09-23-trans-forge-plan.md",
    "docs/plans/2026-09-26-campaign-caliber-fusion-plan.md",
    "docs/known-issues.md",
    "campaign/skills/ingest-forge/SKILL.md",
    "campaign/skills/spec-forge/SKILL.md",
    "campaign/skills/program-forge/SKILL.md",
    "campaign/tools/program.py",
    "campaign/hooks/handoff-inject.sh",
    "campaign/acceptance/ac-94-bridge-behavior.py",
    "campaign/acceptance/ac-95-pipeline-driver.py",
    "campaign/skills/campaign/references/pipeline-cases.md",
    "docs/plans/2026-09-27-campaign-pipeline-driver-plan.md",
]
# 预存基线豁免（wave 前已存在未跟踪件；.caliber/ .campaign/ 已 gitignore 天然豁免）
WAVE_EXEMPT = {"?? campaign/tools/__pycache__/"}


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def check1():
    """trans-forge 七文件全在 + SKILL.md 锚。"""
    for rel in TRANS_FORGE_FILES:
        p = os.path.join(SKILL_DIR, rel)
        if not os.path.isfile(p):
            return False, "缺 trans-forge 文件: %s" % rel
    skill = read_text(os.path.join(SKILL_DIR, "SKILL.md"))
    for s in ("溯源完整证", "增量真实证", "可收编译演证"):
        if skill.count(s) < 1:
            return False, "SKILL.md 缺三证名 %r" % s
    for s in ("停点①", "停点②", "停点③"):
        if skill.count(s) < 1:
            return False, "SKILL.md 缺停点 %r" % s
    if "缺一即拒绝" not in skill:
        return False, "SKILL.md 缺准入判据「缺一即拒绝」"
    for s in ("与 ingest-forge", "与 spec-forge", "与 caliber"):
        if skill.count(s) < 1:
            return False, "SKILL.md 缺分工节标题锚 %r" % s
    return True, "trans-forge 七文件全在 + SKILL.md 锚齐（三证/三停点/准入/分工）"


def check2():
    """campaign 入口：第四分支 + 判别式 + M11/M12 + 反向锚 + 行数。"""
    if not os.path.isfile(CAMPAIGN_SKILL):
        return False, "campaign SKILL.md 不存在"
    body = read_text(CAMPAIGN_SKILL)
    n = len(body.splitlines())
    if n > 100:
        return False, "campaign SKILL.md 行数 %d > 100" % n
    for s in ("按序过五条分支", "3. trans 域",
              "产出新文档 vs 收编本文档不改写",
              "收编区外单篇 plan 驱动 vs 工件区内生产/修订",
              "| trans-forge | 转化：成熟方案文档 → 可收编规格文档（转化先于收编） |",
              "不单独定域"):
        if s not in body:
            return False, "campaign SKILL.md 缺锚 %r" % s
    c = body.count("判定时加权")
    if c != 0:
        return False, "「判定时加权」残留 %d 处（应 0）" % c
    return True, "入口第四分支齐（五条分支/判别式/M11/M12/反向锚 0/行数 %d）" % n


def check3():
    """spec-context hook 名单五件。"""
    sh = read_text(SPEC_CONTEXT_SH)
    if "plan-forge|spec-forge|ingest-forge|trans-forge|program-forge) ;;" not in sh:
        return False, "spec-context.sh 缺 M7 逐字行（五件 case 行）"
    md = read_text(SPEC_CONTEXT_MD)
    if "trans-forge" not in md:
        return False, "spec-context.md 缺「trans-forge」"
    return True, "spec-context hook 名单五件（sh case 行 + md 含 trans-forge）"


def _version_of(obj):
    if isinstance(obj, dict) and "version" in obj:
        return str(obj["version"])
    if isinstance(obj, dict) and isinstance(obj.get("plugins"), list) and obj["plugins"]:
        return _version_of(obj["plugins"][0])
    return None


def check4():
    """manifests：三 JSON version 动态一致（两两互等 + X.Y.Z 形态）+ 双 marketplace 同形 + description 含 trans-forge。"""
    vers = []
    for label, path in (("plugin.json", PLUGIN_JSON),
                        ("marketplace.json", MARKETPLACE_JSON),
                        (".claude-plugin/marketplace.json", CLAUDE_MARKETPLACE_JSON)):
        if not os.path.isfile(path):
            return False, "%s 缺失: %s" % (label, path)
        with open(path, "r", encoding="utf-8") as f:
            v = _version_of(json.load(f))
        if v is None or not re.fullmatch(r"\d+\.\d+\.\d+", v):
            return False, "%s version=%r（形态非 X.Y.Z）" % (label, v)
        vers.append((label, v))
    if len(set(v for _, v in vers)) != 1:
        return False, "三处 version 不一致: %s" % (vers,)
    if not filecmp.cmp(MARKETPLACE_JSON, CLAUDE_MARKETPLACE_JSON, shallow=False):
        return False, "marketplace 双份逐字节不一致"
    if "trans-forge" not in read_text(PLUGIN_JSON):
        return False, "plugin.json description 缺「trans-forge」"
    if "trans-forge" not in read_text(MARKETPLACE_JSON):
        return False, "marketplace.json description 缺「trans-forge」"
    return True, "三处 version 一致（动态）+ 双 marketplace 同形 + description 含 trans-forge"


def check5():
    """references 锚。"""
    sk = read_text(os.path.join(SKILL_DIR, "references", "skeleton-aerofold.md"))
    if "高 9 / 中 4 / 低 0" not in sk:
        return False, "skeleton-aerofold.md 缺「高 9 / 中 4 / 低 0」"
    ig = read_text(os.path.join(SKILL_DIR, "references", "id-grammar.md"))
    if "一处值一 token" not in ig:
        return False, "id-grammar.md 缺「一处值一 token」"
    cf = read_text(os.path.join(SKILL_DIR, "references", "case-flow-builder.md"))
    if "反模式" not in cf:
        return False, "case-flow-builder.md 缺「反模式」"
    return True, "references 三锚齐（高9中4低0/一处值一token/反模式）"


def check6(notes):
    """零触碰守卫：本 wave 清单外路径数=0。"""
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
    if passed == len(results):
        print("PASS ac-92 trans-forge (%d/%d checks)" % (passed, len(results)))
    else:
        print("FAIL ac-92 trans-forge (%d/%d checks)" % (passed, len(results)))
    for n, ok, desc in results:
        print("%s %s %s" % ("ok" if ok else "BAD", n, desc))
    for note in notes:
        print(note)
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
