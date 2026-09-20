# graph.json — K3 schema 与 ID 词法

## 结构

```json
{
  "built_at": "ISO8601",
  "sources": ["相对 CWD 的被解析文件路径"],
  "nodes": [{"id": "FR-8.13", "type": "FR|NFR|R|D|C|Q|AC|S", "file": "...", "line": 123, "status": "defined|deprecated"}],
  "edges": [{"from": "AC-29", "to": "FR-10.2", "file": "...", "line": 2335, "section": "所在节标题"}],
  "reports": {
    "orphans_referenced_undefined": ["..."],
    "orphans_defined_unreferenced": ["..."],
    "duplicates": ["..."],
    "coverage": [{"fr": "FR-9.1", "acceptance": ["AC-9"]}, {"fr": "FR-9.2", "acceptance": [], "gap": true}]
  }
}
```

## ID 词法

`FR-\d+(\.\d+[a-z]?)?`、`NFR-\d+\.\d+`、`R\d+`、`D\d+`、`C\d+`、`Q\d+`、`§\d+(\.\d+)*`（S 型节点 id 含 § 字面）；AC 编号 = 验收标准节内条目印刷编号。

## 解析规则要点（实现 = doc_graph.py）

- 定义：表格行整格精确匹配词法的首个单元格（FR 首列、NFR 第二列「编号」均覆盖）；整段加粗精确匹配；组标题（`#### FR-9 …`）产组节点；C/R/D/Q 限注册表（§0.4/§9/§10/§3.4）并按 ID 去重（重复入 duplicates）；AC 限「验收标准」节。同 ID 全文首现为定义。
- 引用：非定义出现 → edge；from = 同节内最近定义 → 当前节 S 节点 → S0。coverage 仅统计 from=AC 的边。
- 区间展开：前缀白名单（FR-/NFR-/R/D/C/Q/§）× 连符（～/–/-），数字或字母末段递增。
- 代码围栏不提取；行内 code 与表格管道符内提取。
- ~~已知限制（词法 v2 候选）~~ **已修复（v1.1，2026-09-21，W2-T1）**：§ 词法 RFC 排除——`§x.y` 匹配位置前 20 字符窗口内含字面大写 `RFC` 时不产出节点/边（W1 fixture 误报实例「RFC 8445 §6.1.2.3」实测消除，edges 744→742）。
- **已知限制（词法 v1.2 候选，2026-09-21 登记）**：组 ID（FR-8/9/10 等无子号的裸组号）在叙事性加粗提及（如文档头修订叙事 `**FR-9 链路体检…**`、C 决策表行内加粗）处被规则②判为定义，与组标题定义双重计数 → duplicates 假阳性（fixture 实测 FR-8/9/10 三例，W2 出口 lint 已证为既有、非文档缺陷）。候选修法：裸组号已有组标题定义形态时，其加粗出现一律判引用；触发器 = 下一波解析规则修订或该假阳性干扰真实重复检测时。

## 子命令

```bash
python campaign/tools/doc_graph.py build <file...> [--out ./.campaign/graph/]
python campaign/tools/doc_graph.py orphans [--graph ./.campaign/graph/graph.json] [--out <file>]
python campaign/tools/doc_graph.py ripple --id <ID> [--graph ...]   # 双向
python campaign/tools/doc_graph.py coverage [--graph ...]
python campaign/tools/doc_graph.py profile <file>                   # v1.1：文档画像 4 行
```

## v1.1 profile 子命令（K10-2，供 ingest-forge 探测阶段）

输出恰好 4 行：`ids`（七类节点计数，复用 build 节点集）/ `evidence_lines`（含数值+单位行的密度，跳围栏与非空行）/ `decisions`（C/D/Q 计数）/ `weak_words`（7 词表 `适当|尽量|必要时|按需|尽快|优化|友好` 命中总数）。fixture 首份画像实测：FR=124 NFR=33 R=22 D=20 C=8 Q=17 AC=36、evidence 274 行（19% of 1449）、weak 10 hits。
