#!/usr/bin/env python
"""campaign run-ledger（K1 契约实现）：append / summary / current。
零第三方依赖，Python 3.10+。只追加不改写；每条记录以 \\n 结尾。"""
import argparse
import json
import os
import sys
from datetime import datetime

EVENTS = ["unit_start", "unit_end", "verdict", "ruling", "reconcile", "gate", "note"]
VERDICTS = ["pass", "fail", "concerns"]
DEFAULT_FILE = os.path.join(".campaign", "ledger.jsonl")


def cmd_append(args):
    rec = {"ts": datetime.now().astimezone().isoformat(timespec="seconds"),
           "event": args.event}
    if args.unit is not None:
        rec["unit"] = args.unit
    if args.plan is not None:
        rec["plan"] = args.plan
    if args.verdict is not None:
        rec["verdict"] = args.verdict
    if args.elapsed_s is not None:
        rec["elapsed_s"] = args.elapsed_s
    if args.detail is not None:
        rec["detail"] = args.detail.replace("\n", "\\n").replace("\r", "")
    d = os.path.dirname(os.path.abspath(args.file))
    os.makedirs(d, exist_ok=True)
    with open(args.file, "a", encoding="utf-8", newline="") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _load(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def cmd_summary(args):
    recs = _load(args.file)
    units = {}
    for r in recs:
        u = r.get("unit", "(global)")
        e = units.setdefault(u, {"events": 0, "elapsed_s": 0})
        e["events"] += 1
        e["elapsed_s"] += int(r.get("elapsed_s", 0) or 0)
    for u in sorted(units):
        e = units[u]
        print("%s\t%d\t%d" % (u, e["events"], e["elapsed_s"]))
    for r in recs[-args.last:]:
        print("%s %s %s %s" % (r.get("ts", "-"), r.get("event", "-"),
                               r.get("unit", "-"), r.get("detail", "-")))


def cmd_current(args):
    recs = _load(args.file)
    last_start = None
    for r in recs:
        if r.get("event") == "unit_start":
            last_start = r.get("unit")
        elif r.get("event") == "unit_end" and last_start is not None \
                and r.get("unit") == last_start:
            last_start = None
    print(last_start if last_start else "idle")


def main():
    p = argparse.ArgumentParser(prog="ledger.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    pa = sub.add_parser("append")
    pa.add_argument("--event", required=True, choices=EVENTS)
    pa.add_argument("--unit")
    pa.add_argument("--plan")
    pa.add_argument("--verdict", choices=VERDICTS)
    pa.add_argument("--elapsed-s", type=int, default=None, dest="elapsed_s")
    pa.add_argument("--detail")
    pa.add_argument("--file", default=DEFAULT_FILE)
    pa.set_defaults(fn=cmd_append)
    ps = sub.add_parser("summary")
    ps.add_argument("--last", type=int, default=5)
    ps.add_argument("--file", default=DEFAULT_FILE)
    ps.set_defaults(fn=cmd_summary)
    pc = sub.add_parser("current")
    pc.add_argument("--file", default=DEFAULT_FILE)
    pc.set_defaults(fn=cmd_current)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
