#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ac-90 entry-skill smoke —— campaign 插件自留验收段（编号 90+ 段 = 插件自留验收段，
避开 AeroFold 1-36 实例段）。C8 六项检查，逐字：

  1. campaign/skills/campaign/SKILL.md 存在且行数 <= 100。
  2. frontmatter 触发面契约：name/version/metadata/description 六子串。
  3. 只出不进 + 顺序仲裁 + 骨架完备（KI-02/KI-03 + 三段式）。
  4. 三处 JSON version=0.4.0 + marketplace 双份逐字节同形 + description 就位。
  5. hooks/spec-context.sh 的 case 模式行零改动（该行不含 campaign）。
  6. forge/tools 零触碰守卫：① campaign-suite 守卫路径 diff 为空；
     ② caliber-suite 插件本体 caliber/ diff 为空（非 git 仓库 → 恒 SKIP 属预期）。

编码纪律：所有 open() 显式 encoding='utf-8'；subprocess 用 text=True,
encoding='utf-8', errors='replace' 且 try/except 包住；git 非零退出码 /
stderr 含 fatal / 抛异常 → 该段记 SKIP 并计数为通过，打印一行降级说明。

打印顺序：先收集六项结果，首行总结行，随后六项明细（ok <n> / BAD <n>）。
任一 BAD → 首行 FAIL、exit 1；全过 → 首行 PASS、exit 0（run_all.py 归类契约）。
"""
import filecmp
import json
import os
import re
import subprocess
import sys

# 仓库根 = 脚本位置上两级（脚本位于 acceptance/ 内，acceptance/ 的父级的父级
# = 仓库根），用 os.path 从 __file__ 推，不依赖进程 cwd，与 runner 以
# cwd=acceptance/ 调起本脚本兼容。
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILL_PATH = os.path.join(REPO_ROOT, "campaign", "skills", "campaign", "SKILL.md")
PLUGIN_JSON = os.path.join(REPO_ROOT, "campaign", ".zcode-plugin", "plugin.json")
MARKETPLACE_JSON = os.path.join(REPO_ROOT, "marketplace.json")
CLAUDE_MARKETPLACE_JSON = os.path.join(REPO_ROOT, ".claude-plugin", "marketplace.json")
SPEC_CONTEXT_SH = os.path.join(REPO_ROOT, "campaign", "hooks", "spec-context.sh")
# 检查 6②：caliber 插件本体目录，native Windows 路径直传 subprocess（不经 POSIX 转换）。
CALIBER_SUITE = r"F:\workspaces\caliber-suite"


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_frontmatter(text):
    """拆 frontmatter，返回 (frontmatter_text, body_text)；解析失败返回 (None, None)。"""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return None, None


def _metadata_block(fm):
    """提取 frontmatter 中 metadata: 行起、到下一个顶格（无缩进）键或末尾为止的行段。"""
    lines = fm.split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.rstrip() == "metadata:"), None)
    if start is None:
        return ""
    end = len(lines)
    for j in range(start + 1, len(lines)):
        # 顶格非空行 = 下一顶级键即块边界（收尾 --- 已由 split_frontmatter 剥离，不在此列）
        if lines[j] and not lines[j][0].isspace():
            end = j
            break
    return "\n".join(lines[start:end])


def check1():
    """存在与行数门：SKILL.md 存在且行数 <= 100。"""
    if not os.path.isfile(SKILL_PATH):
        return False, "SKILL.md 不存在: %s" % SKILL_PATH
    with open(SKILL_PATH, "r", encoding="utf-8") as f:
        n = sum(1 for _ in f)
    if n > 100:
        return False, "SKILL.md 行数 %d > 100" % n
    return True, "SKILL.md 存在且 %d 行 <= 100" % n


def check2():
    """触发面契约：frontmatter 含 name/version/0.1.0/campaign-w5，description 含六子串。"""
    if not os.path.isfile(SKILL_PATH):
        return False, "SKILL.md 不存在: %s" % SKILL_PATH
    fm, _ = split_frontmatter(read_text(SKILL_PATH))
    if fm is None:
        return False, "SKILL.md 无 frontmatter"
    if "name: campaign" not in fm:
        return False, "frontmatter 缺「name: campaign」"
    md = _metadata_block(fm)
    for s in ("version:", "0.1.0", "campaign-w5"):
        if s not in md:
            return False, "metadata 块缺子串 %r" % s
    desc_line = next((ln for ln in fm.split("\n")
                      if ln.strip().startswith("description:")), None)
    if desc_line is None:
        return False, "frontmatter 缺 description 行"
    for s in ("program", "ingest", "SRS", ".campaign", "Not for", "caliber"):
        if s not in desc_line:
            return False, "description 缺子串 %r" % s
    return True, "frontmatter name/version/metadata + description 六子串全命中"


# 检查 3：各恰 1 处的骨架闸（KI-02/KI-03 + 三段式）。
_ONCE = [
    "## Step 0", "## Step 2", "## 域地图", "## 停止点速查",
    "## 与 caliber 的分工",
    "域判定 <域名>，理由：", "此后不再判",
    "非 campaign 域，且 caliber 缺席", "分诊，不治病",
    "AGENTS.md 全局路由规则的信号清单以本 skill 的 description 为权威。",
    "| ingest-forge | 收编：", "| spec-forge | 生产：", "| program-forge | 编排：",
]
_AT_LEAST = ["✓ 全配", "⚠ 缺", "歧义即停"]


def check3():
    """只出不进 + 顺序仲裁 + 骨架完备。"""
    if not os.path.isfile(SKILL_PATH):
        return False, "SKILL.md 不存在: %s" % SKILL_PATH
    _, body = split_frontmatter(read_text(SKILL_PATH))
    if body is None:
        return False, "SKILL.md 无正文"
    if body.count("只出不进") < 1:
        return False, "正文缺「只出不进」"
    c = body.count("不与 caliber 往返仲裁")
    if c != 1:
        return False, "「不与 caliber 往返仲裁」出现 %d 次（应恰 1）" % c
    order = re.findall(r"^[0-9]+\. (program|ingest|spec) 域", body, re.M)
    if order != ["program", "ingest", "spec"]:
        return False, "域顺序行 = %r（应 ['program', 'ingest', 'spec']）" % order
    for s in _ONCE:
        c = body.count(s)
        if c != 1:
            return False, "「%s」出现 %d 次（应恰 1）" % (s, c)
    for s in _AT_LEAST:
        if body.count(s) < 1:
            return False, "正文缺「%s」" % s
    return True, "只出不进 + program→ingest→spec 顺序 + 骨架闸全过"


def _version_of(obj):
    if isinstance(obj, dict) and "version" in obj:
        return str(obj["version"])
    if isinstance(obj, dict) and isinstance(obj.get("plugins"), list) and obj["plugins"]:
        return _version_of(obj["plugins"][0])
    return None


def check4():
    """版本三处 + 双份同形 + description 就位。"""
    for label, path in (("plugin.json", PLUGIN_JSON),
                        ("marketplace.json", MARKETPLACE_JSON),
                        (".claude-plugin/marketplace.json", CLAUDE_MARKETPLACE_JSON)):
        if not os.path.isfile(path):
            return False, "%s 缺失: %s" % (label, path)
        with open(path, "r", encoding="utf-8") as f:
            v = _version_of(json.load(f))
        if v != "0.4.0":
            return False, "%s version=%r（应 0.4.0）" % (label, v)
    if not filecmp.cmp(MARKETPLACE_JSON, CLAUDE_MARKETPLACE_JSON, shallow=False):
        return False, "marketplace 双份逐字节不一致"
    pj = read_text(PLUGIN_JSON)
    if "campaign entry router" not in pj:
        return False, "plugin.json 缺子串「campaign entry router」"
    if "ingest-forge/spec-forge/evidence-auditor" in pj:
        return False, "plugin.json 含旧串「ingest-forge/spec-forge/evidence-auditor」"
    if "总入口（域判定→路由）" not in read_text(MARKETPLACE_JSON):
        return False, "marketplace.json 缺子串「总入口（域判定→路由）」"
    return True, "三处 version=0.4.0 + 双份同形 + description 就位"


def check5():
    """hooks 零改动守卫：case 模式行在，且该行不含 campaign。"""
    if not os.path.isfile(SPEC_CONTEXT_SH):
        return False, "spec-context.sh 不存在: %s" % SPEC_CONTEXT_SH
    hits = [ln for ln in read_text(SPEC_CONTEXT_SH).split("\n")
            if "plan-forge|spec-forge|ingest-forge|program-forge" in ln]
    if not hits:
        return False, "spec-context.sh 缺 case 模式行（plan-forge|spec-forge|ingest-forge|program-forge）"
    if any("campaign" in ln for ln in hits):
        return False, "case 模式行含 campaign: %r" % hits
    return True, "spec-context.sh case 模式行在且不含 campaign"


def git_diff_untouched(repo, *paths):
    """跑 git -C <repo> diff --name-only HEAD -- <paths>。
    返回 (状态, 说明)；状态 ∈ OK / SKIP / BAD。"""
    try:
        r = subprocess.run(
            ["git", "-C", repo, "diff", "--name-only", "HEAD", "--", *paths],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=60)
    except Exception as e:  # 如 git 不在 PATH 的 FileNotFoundError → SKIP 计通过
        return "SKIP", "git 调用异常（%s: %s）" % (type(e).__name__, e)
    if r.returncode != 0:
        return "SKIP", "git rc=%d stderr=%s" % (r.returncode, r.stderr.strip())
    if "fatal" in r.stderr:
        return "SKIP", "git fatal: %s" % r.stderr.strip()
    out = r.stdout.strip()
    if out:
        return "BAD", "守卫路径有改动: %s" % out.replace("\n", " | ")
    return "OK", "diff 为空"


def check6(notes):
    """forge/tools 零触碰守卫（两段）。SKIP 计数为通过，附降级说明行。"""
    s1, n1 = git_diff_untouched(REPO_ROOT,
                                "campaign/skills/ingest-forge",
                                "campaign/skills/spec-forge",
                                "campaign/skills/program-forge",
                                "campaign/hooks",
                                "campaign/tools")
    if s1 == "BAD":
        return False, "① campaign 守卫路径被改动（%s）" % n1
    if s1 == "SKIP":
        notes.append("note 6① 降级: %s" % n1)
    s2, n2 = git_diff_untouched(CALIBER_SUITE, "caliber/")
    if s2 == "BAD":
        return False, "② caliber/ 被改动（%s）" % n2
    if s2 == "SKIP":
        notes.append("note 6② 降级: %s" % n2)
    return True, "①%s ②%s" % (s1, s2)


def main():
    results = []  # (编号, ok, 说明)
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
        print("PASS ac-90 entry-skill smoke (%d/%d checks)" % (passed, len(results)))
    else:
        print("FAIL ac-90 entry-skill smoke (%d/%d checks)" % (passed, len(results)))
    for n, ok, desc in results:
        print("%s %s %s" % ("ok" if ok else "BAD", n, desc))
    for note in notes:
        print(note)
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
