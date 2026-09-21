#!/usr/bin/env python
"""C6 run_all（K22 runner 契约）：顺序跑全部 36 骨架，归类表钉死：
exit 0=PASS / 1=FAIL / 3=BLOCKED-ENV / 4=BLOCKED-IMPL / 2 及其余=FAIL。
每脚本恒记一行，汇总恒 36 行；runner 自身退出码恒 0。
--out <路径> 指定汇总输出；--registry <路径> 回写 status。"""
import argparse
import glob
import os
import re
import subprocess
import sys
from datetime import datetime

STATE = {0: "PASS", 1: "FAIL", 3: "BLOCKED-ENV", 4: "BLOCKED-IMPL"}


def classify(rc, first_line):
    if rc in STATE:
        return STATE[rc]
    # 输出首行已带态（如探针内部判 FAIL 但以 exit 1 返回之外的形态）
    for s in ("PASS", "FAIL", "BLOCKED-ENV", "BLOCKED-IMPL"):
        if first_line.startswith(s):
            return s
    return "FAIL"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--registry", default=None)
    ap.add_argument("--dir", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()
    out = args.out or os.path.join(".campaign", "evidence",
                                   "ac-run-%s.txt" % datetime.now().strftime("%Y%m%d"))
    scripts = sorted(glob.glob(os.path.join(args.dir, "ac-*.py")))
    rows = []
    for sp in scripts:
        m = re.match(r"(ac-\d+)-", os.path.basename(sp))
        aid = m.group(1).upper() if m else os.path.basename(sp)
        try:
            r = subprocess.run([sys.executable, sp], capture_output=True, text=True,
                               timeout=120, cwd=args.dir)
            rc = r.returncode
            first = (r.stdout.strip().splitlines() or [""])[0]
            summary = (r.stdout.strip().splitlines() or ["(no output)"])[-1][:100]
        except subprocess.TimeoutExpired:
            rc, first, summary = 1, "", "TIMEOUT>120s"
        except Exception as e:  # 兜底：任何异常记 FAIL 行，runner 不崩
            rc, first, summary = 1, "", "runner-error: %s" % e
        rows.append((aid, classify(rc, first), summary))
    lines = ["# C6 验收基座首跑汇总  %s" % datetime.now().isoformat(timespec="seconds"),
             "| AC | 退出态 | 摘要 |", "|---|---|---|"]
    for aid, st, sm in rows:
        lines.append("| %s | %s | %s |" % (aid, st, sm.replace("|", "｜")))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    if args.registry:
        with open(args.registry, encoding="utf-8") as f:
            reg = f.read().split("\n")
        stmap = {aid: st.lower() for aid, st, _ in rows}
        cur = None
        for i, ln in enumerate(reg):
            m = re.match(r"- id: (AC-\d+)", ln)
            if m:
                cur = m.group(1)
            elif cur and ln.strip().startswith("status:"):
                indent = ln[: len(ln) - len(ln.lstrip())]
                reg[i] = "%sstatus: %s" % (indent, stmap.get(cur, "not-run"))
        with open(args.registry, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(reg))
    sys.exit(0)


if __name__ == "__main__":
    main()
