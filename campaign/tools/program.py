#!/usr/bin/env python
"""campaign program 状态机（K19/K20 契约实现）：DAG 单元编排。
零第三方依赖，Python 3.10+。迷你 YAML parser 仅支持 K19 子集；
行级保留式写回（仅 start/gate/reconcile 写 status:/last_reconciled: 行）。
ledger 按程序隔离：默认 .campaign/program/<program名>-ledger.jsonl。"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime

STATUS_ENUM = ("pending", "in_progress", "complete", "blocked")
ID_RE = re.compile(r"(?<![A-Za-z0-9])(?:FR-\d+(?:\.\d+)?|NFR-\d+(?:\.\d+)?|R\d+|D\d+|C\d+|Q\d+|AC-\d+)(?![A-Za-z0-9])")


class YamlErr(Exception):
    pass


def _scalar(s):
    s = s.strip()
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        return s[1:-1]
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return s


def _inline_list(s):
    s = s.strip()
    if not (s.startswith("[") and s.endswith("]")):
        raise YamlErr("not inline list: %s" % s)
    body = s[1:-1].strip()
    if not body:
        return []
    return [_scalar(x) for x in body.split(",")]


class Program:
    """解析结果：meta（顶级键）、units（列表，每项含行号索引）、lines（原始行）。"""

    def __init__(self, path):
        self.path = path
        with open(path, encoding="utf-8") as f:
            self.lines = f.read().split("\n")
        if self.lines and self.lines[-1] == "":
            self.lines.pop()
        self.meta = {}
        self.meta_idx = {}
        self.units = []
        self._parse()

    def _parse(self):
        in_units = False
        cur = None
        for i, raw in enumerate(self.lines):
            if raw.strip() == "":
                continue
            if raw.startswith("#"):
                raise YamlErr("comment not supported: line %d" % (i + 1))
            if not raw.startswith(" ") and raw.rstrip().endswith(":") and raw.strip() == "units:":
                in_units = True
                continue
            if not in_units:
                m = re.match(r"^([A-Za-z_]+):\s*(.*)$", raw)
                if not m:
                    raise YamlErr("bad top-level line %d: %s" % (i + 1, raw))
                self.meta[m.group(1)] = _scalar(m.group(2))
                self.meta_idx[m.group(1)] = i
            else:
                m = re.match(r"^  - id:\s*(.+)$", raw)
                if m:
                    cur = {"id": _scalar(m.group(1)), "_idx": {"id": i}}
                    self.units.append(cur)
                    continue
                m = re.match(r"^    ([A-Za-z_]+):\s*(.*)$", raw)
                if m and cur is not None:
                    key, val = m.group(1), m.group(2)
                    if key in ("depends", "gate"):
                        cur[key] = _inline_list(val)
                    else:
                        cur[key] = _scalar(val)
                    cur["_idx"][key] = i
                    continue
                raise YamlErr("bad unit line %d: %s" % (i + 1, raw))
        if not self.units:
            raise YamlErr("no units")

    def unit(self, uid):
        for u in self.units:
            if u["id"] == uid:
                return u
        return None

    def write_scalar_line(self, key, value, unit=None):
        """行级保留式写回：按记录行号整行替换，其余行字节不变。"""
        if unit is not None:
            idx = unit["_idx"][key]
            self.lines[idx] = "    %s: %s" % (key, value)
        else:
            idx = self.meta_idx[key]
            self.lines[idx] = "%s: %s" % (key, value)

    def save(self):
        with open(self.path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(self.lines) + "\n")


def load(path):
    if not os.path.exists(path):
        sys.exit("program file not found: %s" % path)
    try:
        return Program(path)
    except YamlErr as e:
        sys.exit("YAML subset error: %s" % e)


def ledger_path(args, prog):
    if getattr(args, "ledger", None):
        return args.ledger
    name = str(prog.meta.get("program", "program"))
    return os.path.join(".campaign", "program", "%s-ledger.jsonl" % name)


def ledger_append(path, event, unit=None, verdict=None, elapsed_s=None, detail=None):
    rec = {"ts": datetime.now().astimezone().isoformat(timespec="seconds"), "event": event}
    if unit is not None:
        rec["unit"] = unit
    if verdict is not None:
        rec["verdict"] = verdict
    if elapsed_s is not None:
        rec["elapsed_s"] = elapsed_s
    if detail is not None:
        rec["detail"] = detail.replace("\n", "\\n").replace("\r", "")
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def ledger_load(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def _lint_cmd(prog):
    """lint_cmd 配置串；未配置/空值/'-' → None。"""
    lc = prog.meta.get("lint_cmd")
    if lc is None or str(lc).strip() == "" or lc == "-":
        return None
    return str(lc)


def lint(prog):
    """返回 (errors, warns)。"""
    errs, warns = [], []
    ids = [u["id"] for u in prog.units]
    if len(ids) != len(set(ids)):
        errs.append("duplicate unit id")
    for u in prog.units:
        if u.get("parallel", "-") != "-":
            errs.append("%s: parallel must be '-' (F6 v1 serial)" % u["id"])
        if u.get("status") not in STATUS_ENUM:
            errs.append("%s: bad status %r" % (u["id"], u.get("status")))
        for d in u.get("depends", []):
            if d not in ids:
                errs.append("%s: depends on unknown unit %s" % (u["id"], d))
        gates = u.get("gate", [])
        if not gates:
            warns.append("%s: empty gate list" % u["id"])
        for g in gates:
            if " " in str(g):
                warns.append("%s: gate looks like prose not path: %s" % (u["id"], g))
    # 环检测 DFS
    dep = {u["id"]: list(u.get("depends", [])) for u in prog.units}
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {i: WHITE for i in ids}

    def dfs(n, stack):
        color[n] = GRAY
        for m in dep.get(n, []):
            if color.get(m) == GRAY:
                errs.append("cycle: %s" % "->".join(stack + [n, m]))
                continue
            if color.get(m) == WHITE:
                dfs(m, stack + [n])
        color[n] = BLACK

    for i in ids:
        if color[i] == WHITE:
            dfs(i, [])
    # K6：约定文件缺席 且 未配置 lint_cmd → 机械覆盖缺失 WARN（M2）
    cpath = str(prog.meta.get("conventions") or "CONVENTIONS.md")
    if not os.path.exists(cpath) and _lint_cmd(prog) is None:
        warns.append("程序零工程约定机械覆盖——风格约束仅靠 agent 自律（约定文件 %s 缺席且无 lint_cmd）" % cpath)
    return errs, warns


def eligible(prog):
    done = {u["id"] for u in prog.units if u["status"] == "complete"}
    out = []
    for u in prog.units:
        if u["status"] == "pending" and all(d in done for d in u.get("depends", [])):
            out.append(u["id"])
    return out


def _sort_key(uid):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", uid)]


def cmd_validate(args):
    prog = load(args.program)
    errs, warns = lint(prog)
    for w in warns:
        print("WARN: %s" % w)
    if errs:
        for e in errs:
            print("FAIL: %s" % e)
        sys.exit(1)
    print("OK: %d units, schema+lint pass" % len(prog.units))


def cmd_status(args):
    prog = load(args.program)
    print("program: %s  (reconcile_every=%s last_reconciled=%s)" %
          (prog.meta.get("program"), prog.meta.get("reconcile_every", "-"),
           prog.meta.get("last_reconciled", "-")))
    for u in prog.units:
        print("%-10s %-11s depends=%-12s %s" %
              (u["id"], u.get("status"), ",".join(u.get("depends", [])) or "-", u.get("title", "")))
    nxt = eligible(prog)
    print("eligible: %s" % (", ".join(sorted(nxt, key=_sort_key)) if nxt else "none"))


def cmd_next(args):
    prog = load(args.program)
    nxt = sorted(eligible(prog), key=_sort_key)
    print(nxt[0] if nxt else "none")


def cmd_brief(args):
    prog = load(args.program)
    u = prog.unit(args.unit)
    if not u:
        sys.exit("no such unit: %s" % args.unit)
    ids = ID_RE.findall(str(u.get("title", "")))
    # doc_graph 定位（可得时；缺席降级为纯 ID 清单）
    loc = {}
    gpath = os.path.join(".campaign", "graph", "graph.json")
    if os.path.exists(gpath):
        try:
            g = json.load(open(gpath, encoding="utf-8"))
            nodes = g.get("nodes", [])
            if isinstance(nodes, dict):
                nodes = list(nodes.values())
            for n in nodes:
                if isinstance(n, dict) and n.get("id") in ids:
                    loc[n["id"]] = "%s:%s %s" % (n.get("file", "?"), n.get("line", "?"), n.get("section", ""))
        except Exception:
            pass
    deps = u.get("depends", [])
    # 工程约定注入（K1/K3）：cpath = meta conventions 或缺省 CONVENTIONS.md（cwd 相对）
    cpath = str(prog.meta.get("conventions") or "CONVENTIONS.md")
    if os.path.exists(cpath):
        conv_lines = open(cpath, encoding="utf-8").read().splitlines()
        if len(conv_lines) > 25:
            print("WARN: %s 超 25 行，已按 brief 注入上限截断" % cpath)
            conv_lines = conv_lines[:25] + ["…（约定文件超预算截断，全文见 %s）" % cpath]
    else:
        conv_lines = ["（未配置：%s 缺席）" % cpath]
    lines = ["# Unit Brief: %s %s" % (u["id"], u.get("title", "")),
             "<!-- 派生文件：program.py brief 重装配时整体重写；改内容请改源（program.yaml / %s），勿手改本文件 -->" % cpath, "",
             "## 单元目标", "", str(u.get("title", "")), "", "## SRS 锚点", ""]
    if ids:
        for i in ids:
            lines.append("- %s%s" % (i, (" — " + loc[i]) if i in loc else ""))
    else:
        lines.append("（无显式 ID）")
    lines += ["", "## 前序接口产物", ""]
    if deps:
        for d in deps:
            du = prog.unit(d)
            lines.append("- %s: %s" % (d, (du or {}).get("result", "(无 result 指针)")))
    else:
        lines.append("（无前置单元）")
    lines += ["", "## Global Constraints 候选", "",
              "- D1 事实源：状态只认落盘文件", "- D2 不实现：程序层只编排",
              "- D3 门：证据齐才迁移", "- D4 不稀释：不折叠 caliber 停止点",
              "", "## 工程约定", ""]
    lines += conv_lines
    lines += ["", "## 验收锚", ""]
    acs = [i for i in ids if i.startswith("AC-")]
    lines.append("、".join(acs) if acs else "无")
    lines.append("- 约束符合：产物不得违反「工程约定」节任一条目（审查时逐条引用核对）。")
    lc = _lint_cmd(prog)
    if lc is not None:
        lines.append("- 可执行检查：`%s` 须零告警通过（gate 复跑，失败即 MISSING）。" % lc)
    out = str(u.get("brief") or os.path.join(".campaign", "program", "%s-brief.md" % u["id"]))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    if len(lines) > 90:
        print("WARN: brief %d 行超预算 90（不阻断；瘦身顺序：先瘦约定文件）" % len(lines))
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(out)


def cmd_start(args):
    prog = load(args.program)
    u = prog.unit(args.unit)
    if not u:
        sys.exit("no such unit: %s" % args.unit)
    if u["status"] == "blocked":
        prog.write_scalar_line("status", "pending", unit=u)
        prog.save()
        print("%s: blocked -> pending (resumed)" % u["id"])
        return
    if u["status"] != "pending":
        sys.exit("%s: status %s not startable" % (u["id"], u["status"]))
    if u["id"] not in eligible(prog):
        sys.exit("%s: not eligible (depends incomplete)" % u["id"])
    prog.write_scalar_line("status", "in_progress", unit=u)
    prog.save()
    ledger_append(ledger_path(args, prog), "unit_start", unit=u["id"])
    print("%s: pending -> in_progress" % u["id"])


def cmd_gate(args):
    prog = load(args.program)
    u = prog.unit(args.unit)
    if not u:
        sys.exit("no such unit: %s" % args.unit)
    missing = []
    if u["status"] != "in_progress":
        missing.append("status!=in_progress(%s)" % u["status"])
    for g in u.get("gate", []):
        if not os.path.exists(str(g)) or os.path.getsize(str(g)) == 0:
            missing.append(str(g))
    res = str(u.get("result") or "")
    if not res or not os.path.exists(res):
        missing.append("result:%s" % (res or "(unset)"))
    lp = ledger_path(args, prog)
    # K7：lint_cmd 门（M4）——基本 missing 为空且配置了 lint_cmd 才执行
    lc = _lint_cmd(prog)
    if lc is not None and not missing:
        try:
            r = subprocess.run(lc, shell=True, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=300)
        except subprocess.TimeoutExpired as e:
            tail = ((e.stdout or "") + (e.stderr or ""))[-500:]
            missing.append("lint_cmd 失败(rc=timeout>300s): %s" % tail)
        else:
            if r.returncode != 0:
                tail = ((r.stdout or "") + (r.stderr or ""))[-500:]
                missing.append("lint_cmd 失败(rc=%d): %s" % (r.returncode, tail))
    if missing:
        ledger_append(lp, "gate", unit=u["id"], detail="MISSING: %s" % "; ".join(missing))
        print("MISSING: %s" % "; ".join(missing))
        sys.exit(1)
    prog.write_scalar_line("status", "complete", unit=u)
    prog.save()
    ledger_append(lp, "gate", unit=u["id"], detail="PASS")
    ledger_append(lp, "unit_end", unit=u["id"])
    print("%s: in_progress -> complete (gate PASS)" % u["id"])


def cmd_collect(args):
    prog = load(args.program)
    u = prog.unit(args.unit)
    if not u:
        sys.exit("no such unit: %s" % args.unit)
    ledger_append(ledger_path(args, prog), "note", unit=u["id"],
                  elapsed_s=args.elapsed, detail=args.detail or "collect")
    print("OK")


def _complete_count(prog):
    return sum(1 for u in prog.units if u["status"] == "complete")


def cmd_reconcile_check(args):
    prog = load(args.program)
    comp = _complete_count(prog)
    last = int(prog.meta.get("last_reconciled", 0) or 0)
    every = int(prog.meta.get("reconcile_every", 5) or 5)
    recs = ledger_load(ledger_path(args, prog))
    last_rec_pos = -1
    for i, r in enumerate(recs):
        if r.get("event") == "reconcile":
            last_rec_pos = i
    ruling = any(r.get("event") == "ruling" and "plan 修订" in str(r.get("detail", ""))
                 for r in recs[last_rec_pos + 1:])
    reasons = []
    if comp <= last:
        print("due:no (complete=%d <= last_reconciled=%d)" % (comp, last))
        return
    if every and comp % every == 0:
        reasons.append("complete=%d is multiple of %d" % (comp, every))
    if ruling:
        reasons.append("plan-revision ruling since last reconcile")
    if reasons:
        print("due:yes (%s)" % "; ".join(reasons))
    else:
        print("due:no (complete=%d not multiple of %d; no plan-revision ruling)" % (comp, every))


def cmd_reconcile(args):
    prog = load(args.program)
    comp = _complete_count(prog)
    ledger_append(ledger_path(args, prog), "reconcile",
                  detail=args.detail or "reconcile at complete=%d" % comp)
    if "last_reconciled" not in prog.meta_idx:
        sys.exit("program.yaml missing last_reconciled key")
    prog.write_scalar_line("last_reconciled", str(comp))
    prog.save()
    print("OK last_reconciled=%d" % comp)


def cmd_impact(args):
    """B6 反向互查（K23）：以 program.yaml 内非空 plan 字段为扫描池。"""
    from spec_impact import scan
    prog = load(args.program)
    plans = [str(u["plan"]) for u in prog.units if u.get("plan")]
    if not plans:
        print("no impact")
        return
    hits = scan(args.ids.split(","), plans)
    if not hits:
        print("no impact")
        return
    print("| ID | 命中 plan | 命中行号 | 行摘录 |")
    print("|---|---|---|---|")
    for i, p, n, ex in hits:
        print("| %s | %s | %d | %s |" % (i, p, n, ex.replace("|", "｜")))


def main():
    p = argparse.ArgumentParser(prog="program.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    def base(name):
        sp = sub.add_parser(name)
        sp.add_argument("--program", required=True)
        return sp

    base("validate").set_defaults(fn=cmd_validate)
    base("status").set_defaults(fn=cmd_status)
    base("next").set_defaults(fn=cmd_next)
    sp = base("brief"); sp.add_argument("--unit", required=True); sp.set_defaults(fn=cmd_brief)
    sp = base("start"); sp.add_argument("--unit", required=True)
    sp.add_argument("--ledger"); sp.set_defaults(fn=cmd_start)
    sp = base("gate"); sp.add_argument("--unit", required=True)
    sp.add_argument("--ledger"); sp.set_defaults(fn=cmd_gate)
    sp = base("collect"); sp.add_argument("--unit", required=True)
    sp.add_argument("--elapsed", type=int, default=None); sp.add_argument("--detail")
    sp.add_argument("--ledger"); sp.set_defaults(fn=cmd_collect)
    sp = base("reconcile-check"); sp.add_argument("--ledger")
    sp.set_defaults(fn=cmd_reconcile_check)
    sp = base("reconcile"); sp.add_argument("--detail"); sp.add_argument("--ledger")
    sp.set_defaults(fn=cmd_reconcile)
    sp = base("impact"); sp.add_argument("--ids", required=True)
    sp.set_defaults(fn=cmd_impact)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
