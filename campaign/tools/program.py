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

STATUS_ENUM = ("pending", "sketch", "in_progress", "complete", "blocked")
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


def find_bridge():
    """桥文件定位序（C3）：CALIBER_PLUGIN_DIR → cache 最高版本 → None。"""
    env = os.environ.get("CALIBER_PLUGIN_DIR")
    if env:
        p = os.path.join(env, "campaign-bridge.json")
        if os.path.isfile(p):
            return p
    import glob as _glob
    cands = _glob.glob(os.path.join(os.path.expanduser("~"),
        ".zcode", "cli", "plugins", "cache", "caliber-suite", "caliber",
        "*", "campaign-bridge.json"))
    if not cands:
        return None
    def _ver(p):
        name = os.path.basename(os.path.dirname(p))
        try:
            return tuple(int(x) for x in name.split("."))
        except ValueError:
            return (0,)
    return sorted(cands, key=_ver, reverse=True)[0]


def load_bridge():
    """读桥文件；缺席 → None（静默）；损坏 → WARN 一行 + None（C4）。"""
    p = find_bridge()
    if p is None:
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("WARN: campaign-bridge.json 解析失败，按无桥降级（%s）" % p)
        return None


def _unit_seed_text(u):
    """信号匹配的单元文本种：title 原文（brief 在装配中，种子不含它）。"""
    return str(u.get("title", ""))


def bridge_hits(bridge, unit, ws):
    """命中条目清单：paths 任一存在（ws 相对）AND keywords 任一在种子文本（宁漏勿错）。"""
    if not bridge:
        return []
    out = []
    for e in bridge.get("entries", []):
        sig = e.get("signal", {})
        paths = sig.get("paths", [])
        kws = sig.get("keywords", [])
        p_hit = any(os.path.exists(os.path.join(ws, p)) for p in paths) if paths else False
        k_hit = any(k in _unit_seed_text(unit) for k in kws) if kws else False
        if p_hit and k_hit:
            out.append(e)
    return out


def _result_path(u):
    """result 键消费口径：缺键 / 空串 / 占位 `-`（rolling 缺省）一律视为未声明。"""
    v = str(u.get("result") or "")
    return "" if v in ("", "-") else v


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
    # C5：rolling × fold_grant 双重折叠提醒（不阻断）
    if str(prog.meta.get("planning")) == "rolling" and "fold_grant" in prog.meta:
        warns.append("rolling 程序声明 fold_grant，双重折叠叠加需程序作者自知")
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
            with open(gpath, encoding="utf-8") as f:
                g = json.load(f)
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
        with open(cpath, encoding="utf-8") as f:
            conv_lines = f.read().splitlines()
        if len(conv_lines) > 25:
            print("WARN: %s 超 25 行，已按 brief 注入上限截断" % cpath)
            conv_lines = conv_lines[:25] + ["…（约定文件超预算截断，全文见 %s）" % cpath]
    else:
        conv_lines = ["（未配置：%s 缺席）" % cpath]
    gate_list = [str(g) for g in u.get("gate", [])]
    res_disp = _result_path(u) or "（unit 未声明 result 键——gate 必红，先补 program.yaml）"
    lines = ["# Unit Brief: %s %s" % (u["id"], u.get("title", "")),
             "<!-- 派生文件：program.py brief 重装配时整体重写；改内容请改源（program.yaml / %s），勿手改本文件 -->" % cpath, "",
             "## 编排身份", "",
             "- 你在 campaign 程序 %s 的单元 %s 执行中（unit_start 已落账）。" % (prog.meta.get("program", "?"), u["id"]),
             "- 完工还账：写 %s 五行（verdict/结论/证据/实测/ruling），落盘即停手——收账与门由编排者执行。" % res_disp,
             "- 门证据：%s 须存在且非空。" % ("、".join(gate_list) if gate_list else "（本单元 gate 清单为空）"),
             "- 生存包：.campaign/program/%s-resume-note.md（跨会话与 compact 后回接读它）。" % prog.meta.get("program", "program"),
             "", "## 单元目标", "", str(u.get("title", "")), "", "## SRS 锚点", ""]
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
    if _result_path(u):
        lines.append("- 还账：产出 %s 五行契约（verdict/结论/证据/实测/ruling）。" % _result_path(u))
    lc = _lint_cmd(prog)
    if lc is not None:
        lines.append("- 可执行检查：`%s` 须零告警通过（gate 复跑，失败即 MISSING）。" % lc)
    for e in bridge_hits(load_bridge(), u, os.getcwd()):
        for ob in e.get("brief_obligations", []):
            idx = lines.index("## 单元目标")
            lines.insert(idx - 1, "- 机制义务（桥 %s）：%s" % (e.get("skill", "?"), ob))
    out_bp = u.get("brief")
    out = (str(out_bp) if out_bp not in (None, "", "-")
           else os.path.join(".campaign", "program", "%s-brief.md" % u["id"]))
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
    if u["status"] == "sketch":
        sys.exit("%s: sketch 单元须先细化（refine）为 pending 才可 start" % u["id"])
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
    _bridge = load_bridge()
    for e in bridge_hits(_bridge, u, os.getcwd()):
        import glob as _glob
        for pat in e.get("gate_artifacts", []):
            found = [p for p in _glob.glob(pat, recursive=True)
                     if os.path.isfile(p) and os.path.getsize(p) > 0]
            if not found:
                missing.append("bridge:%s" % pat)
    res = str(u.get("result") or "")
    if not res or not os.path.exists(res):
        missing.append("result:%s" % (res or "(unset)"))
    lp = ledger_path(args, prog)
    # K7：lint_cmd 门（M4）——基本 missing 为空且配置了 lint_cmd 才执行
    lc = _lint_cmd(prog)
    if lc is not None and not missing:
        # 钩子契约：检查脚本凭 CAMPAIGN_UNIT/PROGRAM/WS 定位当前单元、
        # 程序文件与工程根，免反向解析程序状态文件
        env = dict(os.environ)
        env["CAMPAIGN_UNIT"] = u["id"]
        env["CAMPAIGN_PROGRAM"] = os.path.abspath(args.program)
        env["CAMPAIGN_WS"] = os.path.abspath(os.getcwd())
        try:
            r = subprocess.run(lc, shell=True, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=300,
                               env=env)
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


# ---------- rolling DAG：sketch 细化三操作（C4） ----------


def _atomic_save(prog):
    """原子落盘：tmp 文件 + os.replace——save() 整文件覆盖写进程中途被杀会
    截断 program.yaml，而 .campaign/ 通常 gitignore 无 git 兜底。仅 rolling
    三函数消费；既有 save() 调用点行为面不变。"""
    tmp = prog.path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(prog.lines) + "\n")
    os.replace(tmp, prog.path)


def _unit_span(prog, uid):
    """单元块行区间 [首行, 末行后)：`_idx["id"]` 行起，至下一 `  - id:` 前或
    units 末（文件尾/下一个非缩进行）。"""
    u = prog.unit(uid)
    if not u:
        sys.exit("no such unit: %s" % uid)
    start = u["_idx"]["id"]
    end = len(prog.lines)
    for i in range(start + 1, len(prog.lines)):
        if prog.lines[i].startswith("  - id:") or (prog.lines[i] and not prog.lines[i].startswith(" ")):
            end = i
            break
    return u, start, end


def _unit_block(fields):
    """七键序序列化（id/title/status/depends/gate/brief/result）。"""
    def lv(v):
        return "[%s]" % ", ".join(str(x) for x in v) if isinstance(v, list) else str(v)
    return ["  - id: %s" % fields["id"],
            "    title: %s" % fields["title"],
            "    status: %s" % fields["status"],
            "    depends: %s" % lv(fields["depends"]),
            "    gate: %s" % lv(fields["gate"]),
            "    brief: %s" % fields["brief"],
            "    result: %s" % fields["result"]]


def _parse_fields(args):
    """--field k:v 重复项 → dict；按首个 `:` 切分；depends/gate 两键值按
    inline list 解析（去方括号按 `,` 切分逐项 strip，空串 `[]` → 空 list）。"""
    out = {}
    for kv in (args.field or []):
        if ":" not in kv:
            sys.exit("--field 缺冒号: %r" % kv)
        k, v = kv.split(":", 1)
        if k in ("depends", "gate"):
            s = v.strip()
            if s.startswith("[") and s.endswith("]"):
                body = s[1:-1].strip()
                out[k] = [x.strip() for x in body.split(",") if x.strip()] if body else []
            else:
                sys.exit("--field %s 值须为 inline list [a, b]: %r" % (k, v))
        else:
            out[k] = v
    return out


def refine_unit(prog, uid, fields):
    """sketch → pending 合并语义：以单元现有键为底、fields 覆盖、status 强制
    pending；title/gate/result 缺一（或 --field v 为空串视同缺）即报错清单。
    非 sketch 单元拒绝（整块重写会静默丢七键外的键——plan/budget_s/parallel
    等）；--field 键限 title/depends/gate/brief/result 五键（id 锚定、status
    强制 pending，plan/budget_s 等非七键不入块）。写后调用方须重新 load
    （`_idx` 行号已失效）。"""
    u, start, end = _unit_span(prog, uid)
    if u.get("status") != "sketch":
        sys.exit("refine: %s status=%s 非 sketch" % (uid, u.get("status")))
    merged = {"id": uid,
              "title": u.get("title", ""),
              "status": "pending",
              "depends": u.get("depends", []),
              "gate": u.get("gate", []),
              "brief": u.get("brief", "-"),
              "result": u.get("result", "-")}
    for k, v in fields.items():
        if v == "":
            continue
        if k not in ("title", "depends", "gate", "brief", "result"):
            sys.exit("refine: --field 键 %r 不在可细化集（title/depends/gate/brief/result）" % k)
        merged[k] = v
    missing = [k for k in ("title", "gate", "result")
               if merged.get(k) in (None, "", "-") or merged.get(k) == []]
    if missing:
        sys.exit("refine: %s 缺键: %s" % (uid, ", ".join(missing)))
    if merged["brief"] in (None, ""):
        merged["brief"] = "-"
    prog.lines[start:end] = _unit_block(merged)
    _atomic_save(prog)
    return load(prog.path)


def add_sketch(prog, fields):
    """文件尾 append sketch 单元（status: sketch；depends/gate 缺省 []；
    brief/result 缺省 `-`）。必填 id/title。"""
    if not fields.get("id") or not fields.get("title"):
        sys.exit("add-sketch: 必填 id 与 title（--field id:... --field title:...）")
    if prog.unit(fields["id"]):
        sys.exit("add-sketch: %s 已存在" % fields["id"])
    blk = {"id": fields["id"], "title": fields["title"], "status": "sketch",
           "depends": fields.get("depends", []), "gate": fields.get("gate", []),
           "brief": fields.get("brief") or "-", "result": fields.get("result") or "-"}
    prog.lines.extend(_unit_block(blk))
    _atomic_save(prog)
    return load(prog.path)


def drop_sketch(prog, uid):
    """整块剔除 sketch 单元；非 sketch 拒绝。"""
    u, start, end = _unit_span(prog, uid)
    if u.get("status") != "sketch":
        sys.exit("drop-sketch: %s status=%s 非 sketch" % (uid, u.get("status")))
    del prog.lines[start:end]
    _atomic_save(prog)
    return load(prog.path)


def cmd_refine(args):
    prog = load(args.program)
    prog = refine_unit(prog, args.unit, _parse_fields(args))
    ledger_append(ledger_path(args, prog), "ruling", unit=args.unit,
                  detail="refine %s: sketch->pending, 折叠三条件核对=%s" % (args.unit, args.ruling))
    print("refine: %s sketch -> pending" % args.unit)


def cmd_add_sketch(args):
    prog = load(args.program)
    fields = _parse_fields(args)
    uid = fields.get("id", "?")
    prog = add_sketch(prog, fields)
    ledger_append(ledger_path(args, prog), "ruling", unit=uid,
                  detail="add-sketch %s, 折叠三条件核对=%s" % (uid, args.ruling))
    print("add-sketch: %s" % uid)


def cmd_drop_sketch(args):
    prog = load(args.program)
    prog = drop_sketch(prog, args.unit)
    ledger_append(ledger_path(args, prog), "ruling", unit=args.unit,
                  detail="drop-sketch %s, 折叠三条件核对=%s" % (args.unit, args.ruling))
    print("drop-sketch: %s" % args.unit)


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
    sp = base("refine"); sp.add_argument("--unit", required=True)
    sp.add_argument("--field", action="append"); sp.add_argument("--ruling", required=True)
    sp.add_argument("--ledger"); sp.set_defaults(fn=cmd_refine)
    sp = base("add-sketch"); sp.add_argument("--field", action="append")
    sp.add_argument("--ruling", required=True)
    sp.add_argument("--ledger"); sp.set_defaults(fn=cmd_add_sketch)
    sp = base("drop-sketch"); sp.add_argument("--unit", required=True)
    sp.add_argument("--ruling", required=True)
    sp.add_argument("--ledger"); sp.set_defaults(fn=cmd_drop_sketch)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
