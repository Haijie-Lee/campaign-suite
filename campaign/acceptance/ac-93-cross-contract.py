#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ac-93 cross-contract acceptance —— 跨插件引用 lint（C13 六 check）+ fixture 自证
三红态。对 campaign 仓文本中一切指向 caliber 组件的引用做静态闸。九态逐字：

  1. 组件名存在性：封闭枚举 = caliber 十 skill（TEN_SKILLS 硬编码）+ agents（自
     CALIBER_ROOT/agents/*.md 文件名派生，非硬编码清单）；扫描域 = campaign/skills/、
     campaign/hooks/ 全部 .md/.sh；枚举名（词边界）在扫描文本出现 → 断言
     CALIBER_ROOT/skills/<n>/SKILL.md 或 agents/<n>.md 存在。另含显式引用形捕获
     （Part B）：campaign/skills/ 域内「caliber <连字符名>」→ 名必须解析为 caliber
     组件件或 campaign 本地 skill 目录。红态 R1（nonexistent-skill）只能走 Part B
     证明——agent 名自文件派生使枚举命中方向恒真，判定方向写反只有未知组件引用能证
     FAIL。Part B 限定 skills 域且名含连字符：hooks 域同形命中是 .sh 文件指针
     （index-md.sh / learnings-wrapup.sh）、program-forge「caliber program.py」无
     连字符，均不在 skills/agents 存在性断言范围（2026-09-26 实测）。
  2. 锚点存在性：brief 正则（第 3 组改非捕获，匹配语义不变）抽「组件名 → 工序 N /
     Step N」引用 → 目标 CALIBER_ROOT/skills/<name>/SKILL.md 全文检索锚串（原文形
     或去空白形，防源/目标空格写法差异假悬空），缺席即 FAIL、逐条报名。
  3. 禁版本号共现：同一行 caliber skill 名（十枚举，不含 agent——泛词误报面大）与
     v\\d+\\.\\d+ 共现 → FAIL。预期现状 0 命中（spec-forge 化石行已由 T6 先于本批
     消除，任务序保证）。
  4. 双写 cmp：CALIBER_ROOT 的 ui-forge/SKILL.md 与 plan-forge/SKILL.md 各提取
     「UI 信号命中（」起、「进选材产物。」止句（两侧起止标记各恰 1 次），逐字一致。
  5. hook matcher 名单：spec-context.sh 的 case 行五件（plan-forge/spec-forge/
     ingest-forge/trans-forge/program-forge）逐一对应 SKILL.md 存在——campaign 侧
     四件查 scan_root/campaign/skills/<n>/SKILL.md，caliber 侧 plan-forge 查
     CALIBER_ROOT。
  6. 反向闭环：CALIBER_ROOT/skills/*/SKILL.md 中含「campaign」且含「消费点」或
     「gate」的行所属 skill → 桥文件（CALIBER_ROOT/campaign-bridge.json）entries
     必有该 skill 条目。现网预期仅 ui-forge 命中（caliber 十 SKILL.md 实测三行）；
     未来新命中 = 闸的本职（先补桥条目再写文本）。
  R3/R1/R2. fixture 自证红态：tmp 造 campaign/skills/fake-x/SKILL.md 假树（三行
     素材：plan-forge v9.9.9 共现行 / caliber nonexistent-skill 引用行 /
     plan-forge 工序 99 悬空行），每红态独立 tempfile.TemporaryDirectory()，以
     scan_root=<tmp> 分别调 check3/check1/check2 → 断言判 FAIL 且诊断含对应素材词
     （判定方向写反只有红态能证；真实仓扫描域不受影响）。

CALIBER_ROOT 解析序：CALIBER_PLUGIN_DIR 环境变量（须为既有目录）→
~/.zcode/cli/plugins/cache/caliber-suite/caliber/<版本>/ 按版本号降序取首；两路
皆无 → 首行 BLOCKED-ENV、exit 3。

编码纪律（G3，范式 = ac-91/ac-92）：所有 open() 显式 encoding='utf-8'；fixture
写文件 newline='\\n'；每态独立 tempfile.TemporaryDirectory()；REPO_ROOT 自
__file__ 推（脚本位于 campaign/acceptance/ 内，上三级 = 仓根），不依赖进程 cwd。
本脚本无 subprocess 调用（纯静态扫描，无 program.py/git 依赖，G3 的 subprocess
条款不触发）。

打印顺序：先收集九行结果（六 check + 三红态），首行总结行，随后明细
（ok <n> / BAD <n>）。任一 BAD → 首行 FAIL、exit 1；全过 → 首行
PASS ac-93 cross-contract (9 checks)、exit 0。
"""
import json
import os
import re
import sys
import tempfile

# 仓库根 = 脚本位置上三级，自 __file__ 推，不依赖进程 cwd（与 ac-90/91/92 同款）
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# caliber 十 skill 封闭枚举（brief 硬编码清单）；agents 不入此表——自 CALIBER_ROOT 派生
TEN_SKILLS = [
    "caliber", "coding-forge", "deep-probe", "exec-forge", "init-docs",
    "plan-drafting", "plan-forge", "plan-review-ritual", "ui-forge",
    "update-docs",
]

# check② 引用抽取正则：brief 逐字，仅把锚内层捕获组 (\.\d+)? 改 (?:\.\d+)?——
# 分组序（1=组件名 2=锚串）与匹配语义完全不变，只是不再多占一个组号
CHECK2_RX = re.compile(
    r"(plan-forge|deep-probe|plan-review-ritual|plan-drafting|coding-forge"
    r"|exec-forge|ui-forge)[^\n]{0,40}?(工序\s*\d+(?:\.\d+)?|Step\s*\d+)")

# check③ 版本号共现模式（brief 逐字）
VERSION_RX = re.compile(r"v\d+\.\d+")

# check① Part B 显式引用形：caliber 后隔「空格/的」接含连字符的小写名。连字符必需
# ——滤掉「caliber program.py」类无连字符工具指称；「caliber/skills/…」路径段因
# 分隔符 / 不在 [ 的] 类而不被捕获（2026-09-26 实测真实仓 skills 域恰 5 处全解析）
CALIBER_REF_RX = re.compile(r"caliber[ 的]+([a-z][a-z0-9]*(?:-[a-z0-9]+)+)(?![a-z0-9-])")

# check④ 双写句起止标记（T7 新契约句；提取两侧各恰 1 次后逐字 cmp）
UI_SENT_START = "UI 信号命中（"
UI_SENT_END = "进选材产物。"

# check⑤ case 行五件与侧别（side: caliber=查 CALIBER_ROOT，campaign=查本仓 skills）
MATCHER_FIVE = [
    ("plan-forge", "caliber"),
    ("spec-forge", "campaign"),
    ("ingest-forge", "campaign"),
    ("trans-forge", "campaign"),
    ("program-forge", "campaign"),
]
# spec-context.sh:20 逐字 case 行（ac-92 态 3 同源锚，此处作名单定位前提）
MATCHER_CASE_RX = re.compile(
    r"plan-forge\|spec-forge\|ingest-forge\|trans-forge\|program-forge\) ;;")

# fixture 假树三行素材：一行喂一红态，三行互不串扰（逐行核对见各 red 函数 docstring）
FAKE_TREE_LINES = [
    "fake-x 自证假树（仅存在于 tmp，check①②③ 红态共用素材）",
    "plan-forge v9.9.9 共现行（check③ 红态素材）",
    "指引回 caliber nonexistent-skill 补 plan（check① 红态素材）",
    "按 plan-forge 工序 99 执行（check② 红态素材）",
]


def resolve_caliber_root():
    """CALIBER_ROOT 解析序：CALIBER_PLUGIN_DIR（须既有目录）→ cache 最高版本目录；
    两路皆无返回 None。与 program.py find_bridge() 同序自写——ac 脚本独立性优先，
    不 import 工具模块（brief 明示可自写同款）。"""
    env = os.environ.get("CALIBER_PLUGIN_DIR", "")
    if env and os.path.isdir(env):
        return env
    cache = os.path.join(os.path.expanduser("~"), ".zcode", "cli", "plugins",
                         "cache", "caliber-suite", "caliber")
    if os.path.isdir(cache):
        vers = []
        for name in os.listdir(cache):
            p = os.path.join(cache, name)
            if os.path.isdir(p):
                # 版本号取目录名全部数字段为比较键；无数字目录垫 (0,) 沉底
                nums = tuple(int(x) for x in re.findall(r"\d+", name)) or (0,)
                vers.append((nums, name, p))
        if vers:
            # 按版本号降序取首；同名版本目录参与排序保证结果确定
            vers.sort(reverse=True)
            return vers[0][2]
    return None


CALIBER_ROOT = resolve_caliber_root()


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(path, text):
    # fixture 落盘固定 LF（G3）——Windows 默认 CRLF 会混入被扫文本扰动行判定
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def agent_names():
    """12 agent 自 CALIBER_ROOT/agents/*.md 文件名派生（非硬编码清单）。"""
    d = os.path.join(CALIBER_ROOT, "agents") if CALIBER_ROOT else ""
    if not os.path.isdir(d):
        return []
    return sorted(n[:-3] for n in os.listdir(d) if n.endswith(".md"))


def component_exists(name):
    """brief 断言形：CALIBER_ROOT/skills/<name>/SKILL.md 存在 或 agents 件存在。"""
    return (os.path.isfile(os.path.join(CALIBER_ROOT, "skills", name, "SKILL.md"))
            or os.path.isfile(os.path.join(CALIBER_ROOT, "agents", name + ".md")))


def scan_files(scan_root):
    """扫描域：campaign/skills/ 与 campaign/hooks/ 全部 .md/.sh。返回 (绝对路径,
    域名) 列表并排序——诊断行序确定，便于跨次运行对比。"""
    out = []
    for sub in ("skills", "hooks"):
        d = os.path.join(scan_root, "campaign", sub)
        if not os.path.isdir(d):
            continue
        for dirpath, _dirnames, filenames in os.walk(d):
            for fn in filenames:
                if fn.endswith((".md", ".sh")):
                    out.append((os.path.join(dirpath, fn), sub))
    return sorted(out)


def name_rx(name):
    # 词边界两侧禁 [a-z0-9-]：组件名自身含连字符，须防 xplan-forge / plan-forge2 /
    # caliber-suite 类粘连误命中（"architect" 不得匹配 "architecture" 同理）
    return re.compile(r"(?<![a-z0-9-])" + re.escape(name) + r"(?![a-z0-9-])")


def check1(scan_root=REPO_ROOT):
    """check① 组件名存在性：枚举名命中 → 组件件存在；skills 域显式
    「caliber <连字符名>」引用 → 必须解析（红态 R1 走此路径）。"""
    enum = TEN_SKILLS + agent_names()
    rxs = [(n, name_rx(n)) for n in enum]
    sk = os.path.join(scan_root, "campaign", "skills")
    # campaign 本地 skill 目录名作 Part B 豁免集——「caliber spec-forge」类列举句中
    # 本仓 skill 排在 caliber 之后是合法写法（trans-forge SKILL.md:87 实测）
    local = ({n for n in os.listdir(sk) if os.path.isdir(os.path.join(sk, n))}
             if os.path.isdir(sk) else set())
    bad = []
    hit_names = set()
    ref_count = 0
    for p, domain in scan_files(scan_root):
        rel = os.path.relpath(p, scan_root)
        for i, ln in enumerate(read_text(p).split("\n"), 1):
            for n, rx in rxs:
                if rx.search(ln):
                    hit_names.add(n)
                    if not component_exists(n):
                        bad.append("%s:%d 枚举名 %s 无对应组件件" % (rel, i, n))
            if domain == "skills":
                for m in CALIBER_REF_RX.finditer(ln):
                    ref_count += 1
                    ref = m.group(1)
                    if not (component_exists(ref) or ref in local):
                        bad.append("%s:%d 显式引用 caliber %s 无解析"
                                   "（非 caliber 组件件亦非本地 skill）" % (rel, i, ref))
    if bad:
        return False, "%d 处违约：%s" % (len(bad), "；".join(bad))
    return True, "枚举 %d 名（ten+agents）命中 %d 种全解析；skills 域显式 caliber 引用 %d 处全解析" % (
        len(enum), len(hit_names), ref_count)


def check2(scan_root=REPO_ROOT):
    """check② 锚点存在性：组件名→工序 N/Step N 引用逐条在目标 SKILL.md 检索锚串，
    缺席即 FAIL、逐条报名。"""
    bad = []
    total = 0
    for p, _domain in scan_files(scan_root):
        rel = os.path.relpath(p, scan_root)
        text = read_text(p)
        for m in CHECK2_RX.finditer(text):
            total += 1
            name, anchor = m.group(1), m.group(2)
            lineno = text.count("\n", 0, m.start()) + 1
            tp = os.path.join(CALIBER_ROOT, "skills", name, "SKILL.md")
            if not os.path.isfile(tp):
                bad.append("%s:%d 引用 %s 但目标缺失 %s" % (rel, lineno, name, tp))
                continue
            tgt = read_text(tp)
            # 锚串检索取双形：原文形命中即过；否则去空白形（防「工序 3」vs「工序3」
            # 空格写法差异判假悬空）。去空白后子串仍缺席才是真缺席
            if (anchor not in tgt
                    and re.sub(r"\s+", "", anchor) not in re.sub(r"\s+", "", tgt)):
                bad.append("%s:%d 悬空锚：%s SKILL.md 无「%s」" % (rel, lineno, name, anchor))
    if bad:
        return False, "%d/%d 处悬空：%s" % (len(bad), total, "；".join(bad))
    return True, "%d 处组件→锚引用全部命中目标 SKILL.md" % total


def check3(scan_root=REPO_ROOT):
    """check③ 禁版本号共现：同行 caliber skill 名（十枚举，不含 agent）与
    v\\d+\\.\\d+。任一共现行 → FAIL 并报名 file:line + 行片段。"""
    rxs = [(n, name_rx(n)) for n in TEN_SKILLS]
    bad = []
    for p, _domain in scan_files(scan_root):
        rel = os.path.relpath(p, scan_root)
        for i, ln in enumerate(read_text(p).split("\n"), 1):
            if not VERSION_RX.search(ln):
                continue
            for n, rx in rxs:
                if rx.search(ln):
                    # 行片段截 80 字：诊断含原文，红态素材词 v9.9.9 随片段可断言
                    bad.append("%s:%d %s 与版本号共现：%s" % (rel, i, n, ln.strip()[:80]))
                    break
    if bad:
        return False, "%d 处版本号共现：%s" % (len(bad), "；".join(bad))
    return True, "扫描域 0 处 caliber 组件名与 v\\d+\\.\\d+ 同行共现"


def _extract_ui_sentence(text):
    """提取 UI 信号句；起止标记各恰 1 次且止在起后，否则 (None, 原因)。"""
    cs, ce = text.count(UI_SENT_START), text.count(UI_SENT_END)
    if cs != 1 or ce != 1:
        return None, "起标记 %d 次 / 止标记 %d 次（应各恰 1）" % (cs, ce)
    i, j = text.index(UI_SENT_START), text.index(UI_SENT_END)
    if j < i:
        return None, "止标记位于起标记之前"
    return text[i:j + len(UI_SENT_END)], ""


def check4(scan_root=REPO_ROOT):
    """check④ 双写 cmp：ui-forge 与 plan-forge 的 UI 信号句逐字一致。
    scan_root 不涉本 check（纯 CALIBER_ROOT 侧），签名随六 check 统一。"""
    texts = {}
    for n in ("ui-forge", "plan-forge"):
        p = os.path.join(CALIBER_ROOT, "skills", n, "SKILL.md")
        if not os.path.isfile(p):
            return False, "%s SKILL.md 缺失：%s" % (n, p)
        texts[n] = read_text(p)
    s_ui, e_ui = _extract_ui_sentence(texts["ui-forge"])
    s_pf, e_pf = _extract_ui_sentence(texts["plan-forge"])
    if s_ui is None:
        return False, "ui-forge 提取失败：%s" % e_ui
    if s_pf is None:
        return False, "plan-forge 提取失败：%s" % e_pf
    if s_ui != s_pf:
        return False, "双写句不一致（len %d vs %d）ui=%r pf=%r" % (
            len(s_ui), len(s_pf), s_ui, s_pf)
    return True, "双写句两侧各恰 1 次且逐字一致（%d 字）" % len(s_ui)


def check5(scan_root=REPO_ROOT):
    """check⑤ hook matcher 名单：spec-context.sh case 行五件逐一对应 SKILL.md
    存在；caliber 侧组件（plan-forge）查 CALIBER_ROOT，余四查本仓。"""
    shp = os.path.join(scan_root, "campaign", "hooks", "spec-context.sh")
    if not os.path.isfile(shp):
        return False, "spec-context.sh 缺失：%s" % shp
    if not MATCHER_CASE_RX.search(read_text(shp)):
        return False, "spec-context.sh 缺五件 case 行"
    miss = []
    for n, side in MATCHER_FIVE:
        p = (os.path.join(CALIBER_ROOT, "skills", n, "SKILL.md")
             if side == "caliber"
             else os.path.join(scan_root, "campaign", "skills", n, "SKILL.md"))
        if not os.path.isfile(p):
            miss.append("%s（%s 侧）缺 %s" % (n, side, p))
    if miss:
        return False, "case 行五件存在性违约：%s" % "；".join(miss)
    return True, "case 行五件逐一存在（plan-forge 查 CALIBER_ROOT，余四查本仓 skills）"


def check6(scan_root=REPO_ROOT):
    """check⑥ 反向闭环：CALIBER skills/*/SKILL.md 提 campaign∧(gate|消费点) 行的
    skill → 桥 entries 必有该条目。scan_root 不涉本 check，签名随六 check 统一。"""
    sk = os.path.join(CALIBER_ROOT, "skills")
    if not os.path.isdir(sk):
        return False, "CALIBER_ROOT/skills 缺失：%s" % sk
    hits = {}
    for d in sorted(os.listdir(sk)):
        sp = os.path.join(sk, d, "SKILL.md")
        if not os.path.isfile(sp):
            continue
        for i, ln in enumerate(read_text(sp).split("\n"), 1):
            if "campaign" in ln and ("消费点" in ln or "gate" in ln):
                hits.setdefault(d, []).append(i)
    bp = os.path.join(CALIBER_ROOT, "campaign-bridge.json")
    if not os.path.isfile(bp):
        return False, "桥文件缺失：%s（命中 skill：%s）" % (bp, sorted(hits))
    with open(bp, "r", encoding="utf-8") as f:
        bridge = json.load(f)
    entries = sorted(str(e.get("skill")) for e in bridge.get("entries", []))
    orphans = sorted(d for d in hits if d not in entries)
    if orphans:
        return False, "反向闭环违约：%s 提 campaign 消费点/gate 但桥无条目（现桥=%s）" % (
            orphans, entries)
    return True, "闭环合（命中 %s → 桥条目 %s）" % (sorted(hits), entries)


def build_fake_tree(tmp):
    """tmp 下造 campaign/skills/fake-x/SKILL.md 假树（三行素材，newline='\\n'）。"""
    d = os.path.join(tmp, "campaign", "skills", "fake-x")
    os.makedirs(d)
    write_text(os.path.join(d, "SKILL.md"), "\n".join(FAKE_TREE_LINES) + "\n")


def red3():
    """R3 红态：check③ 判定方向自证——假树 v9.9.9 共现行必须判 FAIL 且诊断含
    素材词。行 2「plan-forge v9.9.9」同线共现；行 3/4 无版本号不串扰。"""
    with tempfile.TemporaryDirectory() as tmp:
        build_fake_tree(tmp)
        ok, diag = check3(scan_root=tmp)
    if ok:
        return False, "check③ 对假树竟 PASS（判定方向写反）"
    if "v9.9.9" not in diag:
        return False, "check③ 判 FAIL 但诊断缺素材词 v9.9.9：%s" % diag
    return True, "假树 plan-forge v9.9.9 同行 → check③ FAIL + 诊断含素材词"


def red1():
    """R1 红态：check① Part B 判定方向自证——假树显式引用 nonexistent-skill 必须
    判 FAIL 且诊断含素材词。行 3「caliber nonexistent-skill」走未知组件路径；
    行 2/4 的 plan-forge 为枚举内名且组件件存在，不串扰。"""
    with tempfile.TemporaryDirectory() as tmp:
        build_fake_tree(tmp)
        ok, diag = check1(scan_root=tmp)
    if ok:
        return False, "check① 对假树竟 PASS（判定方向写反）"
    if "nonexistent-skill" not in diag:
        return False, "check① 判 FAIL 但诊断缺素材词 nonexistent-skill：%s" % diag
    return True, "假树引用 caliber nonexistent-skill → check① FAIL + 诊断含素材词"


def red2():
    """R2 红态：check② 判定方向自证——假树悬空锚「工序 99」必须判 FAIL 且诊断含
    素材词。行 4 匹配 (plan-forge, 工序 99)，目标 SKILL.md 无该锚；行 2 无锚、
    行 3 名不在正则枚举，均不串扰。"""
    with tempfile.TemporaryDirectory() as tmp:
        build_fake_tree(tmp)
        ok, diag = check2(scan_root=tmp)
    if ok:
        return False, "check② 对假树竟 PASS（判定方向写反）"
    if "工序 99" not in diag:
        return False, "check② 判 FAIL 但诊断缺素材词 工序 99：%s" % diag
    return True, "假树 plan-forge 工序 99 悬空 → check② FAIL + 诊断含素材词"


def main():
    # BLOCKED-ENV 先于一切结果行：首行契约优先级最高（brief：两路皆无 → 首行
    # BLOCKED-ENV、exit 3）
    if CALIBER_ROOT is None:
        print("BLOCKED-ENV ac-93 cross-contract: CALIBER_ROOT 两路皆无"
              "（CALIBER_PLUGIN_DIR 未设或非目录，且 cache 无版本目录）")
        sys.exit(3)
    results = []
    results.append(("1",) + check1())
    results.append(("2",) + check2())
    results.append(("3",) + check3())
    results.append(("4",) + check4())
    results.append(("5",) + check5())
    results.append(("6",) + check6())
    results.append(("R3",) + red3())
    results.append(("R1",) + red1())
    results.append(("R2",) + red2())

    passed = sum(1 for _, ok, _ in results if ok)
    head = "PASS" if passed == len(results) else "FAIL"
    print("%s ac-93 cross-contract (%d checks)" % (head, len(results)))
    for n, ok, desc in results:
        print("%s %s %s" % ("ok" if ok else "BAD", n, desc))
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
