#!/usr/bin/env python
"""campaign doc-graph（K3 契约实现）：解析 markdown 中 FR/NFR/R/D/C/Q/AC/§ 的
定义与引用，产出 graph.json。零第三方依赖，Python 3.10+。"""
import argparse
import json
import os
import re
import sys
from datetime import datetime

LEX = {
    "FR": re.compile(r"^FR-\d+(\.\d+[a-z]?)?$"),
    "NFR": re.compile(r"^NFR-\d+\.\d+$"),
    "R": re.compile(r"^R\d+$"),
    "D": re.compile(r"^D\d+$"),
    "C": re.compile(r"^C\d+$"),
    "Q": re.compile(r"^Q\d+$"),
    "S": re.compile(r"^§\d+(\.\d+)*$"),
}
# 行内扫描用（非精确）：带边界，防止 FR-x 粘附在更长 token 上被误捕
SCAN = re.compile(
    r"(?<![\w/.-])(FR-\d+(?:\.\d+[a-z]?)?|NFR-\d+\.\d+|R\d+|D\d+|C\d+|Q\d+|§\d+(?:\.\d+)*)(?![\w.-])")
RANGE = re.compile(
    r"(FR-|NFR-|R|D|C|Q|§)(\d+(?:\.\d+)?)([a-z]?) ?[～–-] ?(\d+(?:\.\d+)?)([a-z]?)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
HEAD = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
HEADNUM = re.compile(r"^(\d+(?:\.\d+)*)\.?\s")
GROUP = re.compile(r"^(FR-\d+)\s")
AC_ITEM = re.compile(r"^(\d+)\.\s")
REGISTRY = {"C": "已确认的需求决策", "R": "风险与对策", "D": "待决策", "Q": "需求澄清与假设"}


def id_type(i):
    for t, r in LEX.items():
        if r.match(i):
            return t
    return None


def expand_range(m):
    prefix, b1, s1, b2, s2 = m.groups()
    out = []
    if b1 == b2 and s1 and s2 and s1 != s2:  # FR-3.6a–3.6d
        for c in range(ord(s1), ord(s2) + 1):
            out.append(prefix + b1 + chr(c))
    elif not s1 and not s2:  # NFR-2.8～2.11（同主版本前提）
        p1, p2 = b1.split("."), b2.split(".")
        if len(p1) == len(p2) and p1[:-1] == p2[:-1]:
            for n in range(int(p1[-1]), int(p2[-1]) + 1):
                out.append(prefix + ".".join(p1[:-1] + [str(n)]))
    return out


class Parser:
    def __init__(self):
        self.nodes = {}          # id -> node
        self.edges = []          # {from,to,file,line,section}
        self.duplicates = []
        self.section = ""        # 当前节标题
        self.section_id = None   # 当前节 S id
        self.registry_zone = None  # C/R/D/Q 注册区标记
        self.in_accept = False
        self.def_in_section = []  # 当前节内已定义 id（from 端解析用）

    def add_node(self, i, typ, file, line, status="defined"):
        if i in self.nodes:
            if self.nodes[i]["status"] == "defined" and status == "defined" \
                    and self.nodes[i]["type"] == typ:
                if i not in self.duplicates:
                    self.duplicates.append(i)
                return False
            return False
        self.nodes[i] = {"id": i, "type": typ, "file": file, "line": line,
                         "status": status}
        if typ != "S":
            self.def_in_section.append(i)
        return True

    def resolve_from(self):
        if self.def_in_section:
            return self.def_in_section[-1]
        if self.section_id:
            return self.section_id
        return "S0"

    def add_edge(self, to, file, line, frm=None):
        self.edges.append({"from": frm or self.resolve_from(), "to": to,
                           "file": file, "line": line, "section": self.section})

    def feed_heading(self, text, file, line):
        self.section = text
        self.def_in_section = []
        self.section_id = None
        m = HEADNUM.match(text)
        if m:
            sid = "§" + m.group(1)
            self.add_node(sid, "S", file, line)
            self.section_id = sid
        g = GROUP.match(text)
        if g:
            self.add_node(g.group(1), "FR", file, line)
        zone = None
        for k, marker in REGISTRY.items():
            if marker in text:
                zone = k
        self.registry_zone = zone
        self.in_accept = ("验收标准" in text)

    def parse(self, path):
        fname = os.path.basename(path)
        in_fence = False
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        for no, raw in enumerate(lines, 1):
            line = raw.rstrip("\n")
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            hm = HEAD.match(line)
            if hm:
                self.feed_heading(hm.group(2), fname, no)
                continue
            # 区间展开（前缀白名单；展开物按定义/引用规则处理）
            skip_spans = []
            for m in RANGE.finditer(line):
                # K10-1（v1.1）：§ 区间前 20 字符窗口含字面 RFC → 外部标准引用，跳过
                if m.group(1) == "§" and \
                        "RFC" in line[max(0, m.start() - 20):m.start()]:
                    continue
                for iid in expand_range(m):
                    self.handle_id(iid, fname, no, line, in_table_cell=False)
                skip_spans.append(m.span())
            # 表格单元格：定义侦测（整格精确匹配，剥离 **）
            if line.lstrip().startswith("|"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                for c in cells:
                    cc = c.replace("**", "").strip()
                    if id_type(cc):
                        self.handle_id(cc, fname, no, line, in_table_cell=True)
            # 加粗整段精确匹配 → 定义候选
            for b in BOLD.findall(line):
                bb = b.strip()
                if id_type(bb):
                    self.handle_id(bb, fname, no, line, in_table_cell=False)
            # 验收条目
            if self.in_accept:
                am = AC_ITEM.match(line)
                if am:
                    acid = "AC-" + am.group(1)
                    self.add_node(acid, "AC", fname, no)
            # 全文引用扫描（跳过区间跨度）
            masked = list(line)
            for s, e in skip_spans:
                masked[s:e] = " " * (e - s)
            clean = "".join(masked)
            cur_ac = None
            if self.in_accept:
                am = AC_ITEM.match(line)
                cur_ac = "AC-" + am.group(1) if am else None
            for m in SCAN.finditer(clean):
                iid = m.group(1)
                # K10-1（v1.1）：§ 引用前 20 字符窗口含字面 RFC → 外部标准
                # 章节引用（如 RFC 8445 §6.1.2.3），不产出节点/边
                if iid.startswith("§") and \
                        "RFC" in clean[max(0, m.start() - 20):m.start()]:
                    continue
                frm = cur_ac if (cur_ac and iid != cur_ac) else None
                self.handle_id(iid, fname, no, line,
                               in_table_cell=False, force_frm=frm)

    def handle_id(self, iid, fname, no, line, in_table_cell, force_frm=None):
        typ = id_type(iid)
        if not typ:
            return
        # C/R/D/Q 只在注册区可由表格/加粗定义；区外一律引用
        if typ in REGISTRY and self.registry_zone != typ and iid not in self.nodes:
            self.add_edge(iid, fname, no, frm=force_frm)
            return
        status = "defined"
        seg = line
        if ("废弃" in seg) or ("deprecated" in seg.lower()) or ("~~" in seg):
            status = "deprecated"
        if iid in self.nodes:
            # 已定义：本次出现 = 引用
            self.add_edge(iid, fname, no, frm=force_frm)
            return
        if in_table_cell or self.registry_zone == typ or typ in ("FR", "NFR", "AC"):
            self.add_node(iid, typ, fname, no, status)
        else:
            # 普通正文首次出现：FR/NFR 允许加粗定义（调用方已限定加粗），其余按引用
            self.add_edge(iid, fname, no, frm=force_frm)


def build(files, outdir):
    os.makedirs(outdir, exist_ok=True)
    p = Parser()
    for fp in files:
        p.parse(fp)
    nodes = list(p.nodes.values())
    to_ids = set()
    for e in p.edges:
        to_ids.add(e["to"])
    ref_undef = sorted({e["to"] for e in p.edges} - set(p.nodes.keys()))
    def_unref = sorted([n["id"] for n in nodes
                        if n["type"] not in ("S",) and n["id"] not in to_ids])
    coverage = []
    ac_edges = {}
    for e in p.edges:
        if e["from"].startswith("AC-") and e["to"].startswith("FR-"):
            ac_edges.setdefault(e["to"], []).append(e["from"])
    for n in sorted([x for x in nodes if x["type"] == "FR"],
                    key=lambda x: [int(re.sub(r"\D", "", p) or 0)
                                   for p in x["id"].split(".")]):
        acs = sorted(set(ac_edges.get(n["id"], [])))
        row = {"fr": n["id"], "acceptance": acs}
        if not acs:
            row["gap"] = True
        coverage.append(row)
    graph = {
        "built_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "sources": files,
        "nodes": nodes,
        "edges": p.edges,
        "reports": {
            "orphans_referenced_undefined": ref_undef,
            "orphans_defined_unreferenced": def_unref,
            "duplicates": p.duplicates,
            "coverage": coverage,
        },
    }
    out = os.path.join(outdir, "graph.json")
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    print("built: %s (nodes=%d edges=%d)" % (out, len(nodes), len(p.edges)))


def load_graph(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def cmd_orphans(args):
    g = load_graph(args.graph)
    rows = [("referenced_undefined", i, "-", "-")
            for i in g["reports"]["orphans_referenced_undefined"]]
    pos = {n["id"]: n for n in g["nodes"]}
    rows += [("defined_unreferenced", i,
              pos[i]["file"], str(pos[i]["line"]))
             for i in g["reports"]["orphans_defined_unreferenced"] if i in pos]
    if g["reports"]["duplicates"]:
        rows += [("duplicate_definition", i, "-", "-")
                 for i in g["reports"]["duplicates"]]
    text = "".join("%s\t%s\t%s:%s\n" % r for r in rows)
    sys.stdout.write(text)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8", newline="") as f:
            f.write(text)


def cmd_ripple(args):
    g = load_graph(args.graph)
    for e in g["edges"]:
        if e["from"] == args.id or e["to"] == args.id:
            print("%s:%s\t%s\t%s→%s" % (e["file"], e["line"], e["section"],
                                        e["from"], e["to"]))


def cmd_coverage(args):
    g = load_graph(args.graph)
    for row in g["reports"]["coverage"]:
        acs = ",".join(row["acceptance"]) if row["acceptance"] else "gap: true"
        print("%s\t%s" % (row["fr"], acs))


EVID = re.compile(r"\d+(\.\d+)?\s*(%|ms|s|GB|MB|KB|万|倍|行)")
WEAK7 = ["适当", "尽量", "必要时", "按需", "尽快", "优化", "友好"]


def cmd_profile(args):
    """K10-2（v1.1）：文档画像——ID 计数 / 证据密度 / 决策密度 / 歧义词命中，
    恰好 4 行输出。ids/decisions 复用 build 节点集；密度统计跳围栏与非空行。"""
    p = Parser()
    p.parse(args.file)
    counts = {t: 0 for t in ("FR", "NFR", "R", "D", "C", "Q", "AC")}
    for n in p.nodes.values():
        if n["type"] in counts:
            counts[n["type"]] += 1
    evid = 0
    total = 0
    weak = 0
    in_fence = False
    with open(args.file, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or not line.strip():
                continue
            total += 1
            if EVID.search(line):
                evid += 1
            for w in WEAK7:
                weak += line.count(w)
    pct = round(evid * 100 / total) if total else 0
    print("ids: FR=%d NFR=%d R=%d D=%d C=%d Q=%d AC=%d" % (
        counts["FR"], counts["NFR"], counts["R"], counts["D"],
        counts["C"], counts["Q"], counts["AC"]))
    print("evidence_lines: %d (%d%% of %d content lines)" % (evid, pct, total))
    print("decisions: C=%d D=%d Q=%d" % (counts["C"], counts["D"], counts["Q"]))
    print("weak_words: %d hits (7-word list)" % weak)


def main():
    p = argparse.ArgumentParser(prog="doc_graph.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    pb = sub.add_parser("build")
    pb.add_argument("files", nargs="+")
    pb.add_argument("--out", default=os.path.join(".campaign", "graph"))
    po = sub.add_parser("orphans")
    po.add_argument("--graph", default=os.path.join(".campaign", "graph", "graph.json"))
    po.add_argument("--out")
    pr = sub.add_parser("ripple")
    pr.add_argument("--id", required=True)
    pr.add_argument("--graph", default=os.path.join(".campaign", "graph", "graph.json"))
    pcv = sub.add_parser("coverage")
    pcv.add_argument("--graph", default=os.path.join(".campaign", "graph", "graph.json"))
    pp = sub.add_parser("profile")
    pp.add_argument("file")
    args = p.parse_args()
    if args.cmd == "build":
        build(args.files, args.out)
    elif args.cmd == "orphans":
        cmd_orphans(args)
    elif args.cmd == "ripple":
        cmd_ripple(args)
    elif args.cmd == "coverage":
        cmd_coverage(args)
    elif args.cmd == "profile":
        cmd_profile(args)


if __name__ == "__main__":
    main()
