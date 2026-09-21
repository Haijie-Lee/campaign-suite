#!/usr/bin/env python
r"""campaign spec 消费链反向互查（K23 契约实现）：
SRS 变更 ID 集 × 在途 plan 池 → 受影响 plan 清单。
零第三方依赖，Python 3.10+。
ID 词法自定义七类（doc_graph 七类第七类为 § 而非 AC，故自立）：
FR-\d+(\.\d+)? / NFR-\d+(\.\d+)? / R\d+ / D\d+ / C\d+ / Q\d+ / AC-\d+，
全部七类前后要求非字母数字边界（FR 防 NFR 内子串、AC 防 MAC 内子串）。"""
import argparse
import os
import re
import sys

LEX = {
    "FR": r"FR-\d+(?:\.\d+)?",
    "NFR": r"NFR-\d+(?:\.\d+)?",
    "R": r"R\d+",
    "D": r"D\d+",
    "C": r"C\d+",
    "Q": r"Q\d+",
    "AC": r"AC-\d+",
}
BOUNDARY = r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])"
ALL_RE = re.compile(BOUNDARY % "|".join(LEX.values()))


def valid_id(s):
    return re.fullmatch(BOUNDARY % "|".join(LEX.values()), s) is not None


def scan(ids, plans):
    """返回命中行列表 (id, plan, lineno, excerpt)。"""
    pats = {}
    for i in ids:
        i = i.strip()
        if not i:
            continue
        if not valid_id(i):
            sys.exit("bad ID (not in 7-class lexicon): %s" % i)
        pats[i] = re.compile(BOUNDARY % re.escape(i))
    hits = []
    for p in plans:
        if not os.path.exists(p):
            print("WARN: plan not found: %s" % p, file=sys.stderr)
            continue
        with open(p, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                for i, pat in pats.items():
                    if pat.search(line):
                        hits.append((i, p, n, line.strip()[:120]))
    return hits


def cmd_scan(args):
    ids = args.ids.split(",")
    plans = []
    for p in args.plans:
        plans.extend(p.split(","))
    hits = scan(ids, plans)
    if not hits:
        print("no impact")
        return
    print("| ID | 命中 plan | 命中行号 | 行摘录 |")
    print("|---|---|---|---|")
    for i, p, n, ex in hits:
        print("| %s | %s | %d | %s |" % (i, p, n, ex.replace("|", "｜")))


def main():
    ap = argparse.ArgumentParser(prog="spec_impact.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("scan")
    sp.add_argument("--ids", required=True, help="逗号分隔 ID 列表")
    sp.add_argument("--plans", required=True, nargs="+", help="plan 文件路径列表")
    sp.set_defaults(fn=cmd_scan)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
