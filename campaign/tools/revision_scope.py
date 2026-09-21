#!/usr/bin/env python3
"""revision_scope.py — 修订范围清单计算器（campaign B4 的机械可测核心）

输入 = 统一 diff + 当前文档 + doc-graph 图；输出 = 修订范围清单（changed_ids /
changed_sections / ripple_sections / sample_sections / counts），供
plan-review-ritual REVISION 模式作为 SCOPE_PATH 消费。

stdlib-only；ensure_ascii=False；降级不炸（graph 缺席 / diff 无 hunk 均 exit 0
并在 manifest 内留警告行）。

契约：campaign-W3建造plan.md K16-B（changed_sections 边界映射三边界规则：
半开区间 [c, c+d)；跨节逐行归属取最近上方 `## ` 节；首个 `## ` 之前记（无节）；
纯删除 hunk（d=0）以新侧起始行 c 的最近上方 `## ` 节为归属）。
"""
import argparse
import json
import math
import random
import re
import sys

ID_PATTERNS = [
    r"FR-\d+(?:\.\d+)?[a-z]?",
    r"NFR-\d+(?:\.\d+)?",
    r"R\d+",
    r"D\d+",
    r"C\d+",
    r"Q\d+",
    r"AC-\d+",
]
ID_RE = re.compile("|".join("(?:" + p + ")" for p in ID_PATTERNS))
HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
SECTION_RE = re.compile(r"^## ")
NO_SECTION = "（无节）"


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()


def parse_sections(doc_lines):
    """返回 [(lineno_1based, title_line), ...]，仅 `## ` 级。"""
    out = []
    for i, line in enumerate(doc_lines, 1):
        if SECTION_RE.match(line):
            out.append((i, line.strip()))
    return out


def section_of(sections, lineno):
    """lineno 行号所属 `## ` 节 = 最近上方；无则（无节）。"""
    best = None
    for ln, title in sections:
        if ln <= lineno:
            best = title
        else:
            break
    return best if best is not None else NO_SECTION


def parse_diff_hunks(diff_lines):
    """解析 unified diff，返回 (changed_id_lines, hunks)。
    changed_id_lines = 增删行文本列表（排除 +++/--- 头行）；
    hunks = [(new_start_c, new_len_d), ...]。"""
    id_lines = []
    hunks = []
    for line in diff_lines:
        m = HUNK_RE.match(line)
        if m:
            c = int(m.group(3))
            d = int(m.group(4)) if m.group(4) is not None else 1
            hunks.append((c, d))
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+") or line.startswith("-"):
            id_lines.append(line[1:])
    return id_lines, hunks


def extract_ids(lines):
    found = set()
    for line in lines:
        for m in ID_RE.finditer(line):
            found.add(m.group(0))
    return sorted(found)


def cmd_build(args):
    warnings = []
    doc_lines = read_lines(args.doc)
    sections = parse_sections(doc_lines)
    diff_lines = read_lines(args.diff)
    id_lines, hunks = parse_diff_hunks(diff_lines)

    changed_ids = extract_ids(id_lines)

    changed_sections = []
    for c, d in hunks:
        if d == 0:
            # 纯删除 hunk：以新侧起始行 c 的最近上方 `## ` 节为归属
            cand = {section_of(sections, c)} if c > 0 else {NO_SECTION}
        else:
            cand = {section_of(sections, ln) for ln in range(c, c + d)}
        for t in cand:
            if t not in changed_sections:
                changed_sections.append(t)

    if not hunks:
        warnings.append("diff 未解析到 hunk，counts 全 0")

    # ripple_sections：changed_ids 的 1-hop 邻居边（edge.from/to 命中）→
    # edge.line 经同一边界映射到 `## ` 节。
    ripple_sections = []
    graph_loaded = False
    if args.graph:
        try:
            with open(args.graph, encoding="utf-8") as f:
                graph = json.load(f)
            graph_loaded = True
        except (OSError, json.JSONDecodeError):
            graph_loaded = False
    if not graph_loaded:
        warnings.append("graph 缺失，涟漪计算跳过")
    else:
        id_set = set(changed_ids)
        for e in graph.get("edges", []):
            if e.get("from") in id_set or e.get("to") in id_set:
                t = section_of(sections, e.get("line", 0))
                if t not in ripple_sections:
                    ripple_sections.append(t)

    # sample_sections：未触及节 = 全部 `## ` 节 − changed ∪ ripple；
    # ceil(未触及 × rate)，random.Random(seed) 可复现。
    all_titles = [t for _, t in sections]
    touched = set(changed_sections) | set(ripple_sections)
    untouched = [t for t in all_titles if t not in touched]
    k = math.ceil(len(untouched) * args.rate)
    rng = random.Random(args.seed)
    sample_sections = rng.sample(untouched, k) if k > 0 else []

    counts = {
        "ids": len(changed_ids),
        "sections": len(changed_sections),
        "ripple": len(ripple_sections),
        "sample": len(sample_sections),
    }

    meta = {
        "diff": args.diff.replace("\\", "/"),
        "doc": args.doc.replace("\\", "/"),
        "seed": args.seed,
        "rate": args.rate,
    }

    # manifest（节标题逐字锁定，契约 K16-B）
    out = []
    out.append("# 修订范围清单")
    out.append("")
    out.append(f"- diff: {meta['diff']}")
    out.append(f"- doc: {meta['doc']}")
    out.append(f"- seed: {args.seed}")
    out.append(f"- rate: {args.rate}")
    for w in warnings:
        out.append(f"- 警告: {w}")
    out.append("")
    out.append("## changed_ids")
    out.append("")
    out.extend(f"- {x}" for x in changed_ids)
    out.append("")
    out.append("## changed_sections")
    out.append("")
    out.extend(f"- {x}" for x in changed_sections)
    out.append("")
    out.append("## ripple_sections")
    out.append("")
    out.extend(f"- {x}" for x in ripple_sections)
    out.append("")
    out.append(f"## sample_sections(seed={args.seed}, rate={args.rate})")
    out.append("")
    out.extend(f"- {x}" for x in sample_sections)
    out.append("")
    out.append("## counts")
    out.append("")
    out.append(
        "ids={ids} sections={sections} ripple={ripple} sample={sample}".format(**counts)
    )
    out.append("")
    text = "\n".join(out)

    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    else:
        sys.stdout.write(text)

    if args.json:
        payload = {
            "meta": meta,
            "warnings": warnings,
            "changed_ids": changed_ids,
            "changed_sections": changed_sections,
            "ripple_sections": ripple_sections,
            "sample_sections": sample_sections,
            "counts": counts,
        }
        with open(args.json, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return 0


def main():
    ap = argparse.ArgumentParser(prog="revision_scope.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="计算修订范围清单")
    b.add_argument("--diff", required=True, help="统一 diff 文件路径")
    b.add_argument("--doc", required=True, help="当前（新侧）文档路径")
    b.add_argument("--graph", default=None, help="doc-graph graph.json 路径（可缺）")
    b.add_argument("--rate", type=float, default=0.1, help="未触及节抽查比例")
    b.add_argument("--seed", type=int, default=42, help="抽查随机种子")
    b.add_argument("--out", default=None, help="范围清单 md 输出路径（缺省 stdout）")
    b.add_argument("--json", default=None, help="范围清单 json 输出路径（可选）")
    b.set_defaults(func=cmd_build)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
