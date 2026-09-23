# Trans Forge — 检查清单（按工序读取）

仅在进入对应工序时读对应节。这里是对抗审查的**视角细目**；机制（双声部/三级裁定/收敛循环/闸口/彩排派遣形态）一律调 caliber plan-forge / plan-review-ritual / spec-forge 既有机制（指针引用，不复制）。

## 工序 1 — 选材检查清单

- [ ] **准入三判据逐条过**（缺一即拒绝并上报）：①决策注册表存在（plan 内有已裁定 D 条目）；②路线已裁定（现状论证 → 目标形态有明确选择）；③现状断言有实证密度（file:line 或实测数据可核）。指引回 caliber plan-forge / deep-probe 补 plan。
- [ ] plan 节级解析已跑：`python campaign/tools/doc_graph.py profile <plan>`（ids / evidence_lines / decisions / weak_words 四行）。
- [ ] **实证抽查回收**：plan 引用的 file:line 逐一复核，有漂移即上报——逐条记录「引用点 → 实测现状 → 是否漂移」。
- [ ] 缺口清单对照：读 `references/skeleton-aerofold.md` 完备性清单（10 项必备面），标已覆盖 / 待补面。
- [ ] Q 预选清单落盘（疑似模糊点：无量化判据 / 一义多读 / 注册表矛盾）。

## 工序 2 — 制坯检查清单

- [ ] **映射设计表 100% 覆盖**：每个源 plan `##` 节恰一行（含丢弃行），无遗漏；表头逐字 = `templates/mapping-design-template.md`。
- [ ] **出处标签三枚举齐**（每节标注其一）：照录源方案 §x / 扩写源方案 §x / 新写（spec 阶段新增，待评审）。
- [ ] **分章律自检**：`##` 节单一工件归属（七枚举：SRS.md / architecture.md / adr/ / research/ / plan.md / risks.md / DECISIONS.md）；混合节（§0/§2/§4/§6/§7/§8）显式 `子节归属声明` 行。
- [ ] **ID 规范自检**（指针 `references/id-grammar.md`）：七前缀白名单 FR/NFR/R/D/C/Q/AC；禁单字母 P 前缀；稳定编号只增不改；正文禁通配引用（`FR-3.x`），组引用用「FR-3 全组」；区间引用（`FR-2.1–2.4`）仅索引/锚点区；TODO token 一处值一 token。
- [ ] **两态标记自检**：新增/变更范围内数值断言未标记清单为空——`grep -nE '[0-9]+(\.[0-9]+)?[ ]*(%|ms|s|GB|MB|KB|万|倍|行)' <目标> | grep -vE '【(证据|假设·验证=)'` → 零行。标记形逐字 `【证据】` / `【假设·验证=<方法>】`（行尾）。
- [ ] **q-table 全角 `｜` 规则**：Q 表单元格禁裸 `|`，内容含竖线写全角 `｜`（C5——ingest-forge SKILL.md 全角规则优先；模板注释行 `\|` 与 SKILL.md 不一致是已知 KI-15，trans-forge 侧一律从全角）。
- [ ] **L1 歧义词表仅以指针引用**（spec-forge 工序 2 / spec-lint hook），禁在本文件与 SKILL.md 正文内联七词词表。

## 工序 3 — 锻打检查清单

### 溯源必填律检查

- [ ] 每条 FR/NFR 答得出源节 / D 条目 / 实证行；答不出 → 已标「spec 阶段新增，待评审」（禁伪装源方案内容）。
- [ ] 未知分类规则落实：形状级未知 → 进停点②；参数级未知 → TODO 注册 + 最可能假设落笔。
- [ ] 全文档无一处编造数值（无出处 → TODO 注册，禁正文常量）。

### 第六视角「可收编性」细目（trans-forge 特有，SRS 五视角之外）

- [ ] **一节一投**：每个 `##` 节判定时单一目标工件，混合节显式子节归属声明——禁「一节多投」（flow-builder 案例 9 处一节多投反模式）。
- [ ] **ID 规整**：七前缀白名单；无单字母 P 撞优先级/分位；无通配引用；组引用注记形态。
- [ ] **Q 收敛**：Q 表每条绑定 §10 D 号（源注册表沿用原编号，新发现从 Q100 起）；待决项唯一登记点（§10/DECISIONS.md），他处禁重复登记。
- [ ] **干跑预过**：可收编译演证的试映射先行自检——低置信 = 0？中置信行全带子节归属？spec-lint L1/L2/L3 离线复跑零命中？
- [ ] 对抗审查（SRS 五视角 + 双声部 + 三级裁定 + 收敛循环）机制摘要 + 指针 spec-forge 工序 3；B5 evidence-auditor（`campaign/agents/evidence-auditor.md`）审计全部新增定量断言。

## 工序 4 — 成型检查清单

### 彩排派遣 prompt 骨架（填槽 `{DELTA_PATH}` `{SCOPE}`）

- [ ] `{DELTA_PATH}` = 转化 spec 草稿路径（真实使用 = 本轮新增/变更的 FR 范围或定量断言行集）。
- [ ] `{SCOPE=FR/AC/契约节}`（裁剪制，D-4）。
- [ ] 派遣 prompt 骨架指针 spec-forge `checklists.md` 工序 4 节（`campaign/skills/spec-forge/checklists.md:74` 起）；ac-92 静态闸范式参照 `campaign/acceptance/ac-91-brief-conventions.py`。
- [ ] fresh 零背景 agent，read-only，不执行写操作。

### 回收检查（编排者逐条）

- [ ] 每条新增/变更 FR 都被复述（无遗漏——漏复述 = 漏测）。
- [ ] 歧义点与不可验证点全部回工序 2 补全（不是嘴上答「显然」）。
- [ ] 补全后复检：同一 fresh reader 对修订行重述，无新歧义。

## 工序 5 — 出口门检查清单（三证逐条操作化）

### 溯源完整证
- [ ] 映射设计表 100% 覆盖源节（含丢弃理由，丢弃行理由列非空）。
- [ ] plan 每条 D 在产物逐字可查（grep 逐条命中）且有落点指针（本 spec 落点列）。
- [ ] 实证索引附录（附录 B）落盘，证据行可回溯源 plan。

### 增量真实证
- [ ] `python campaign/tools/doc_graph.py profile <产物>` → FR ≥1 / NFR ≥1 / AC ≥1（计数非零）。
- [ ] NFR 过 L3 数值 lint：NFR 定义行剔除编号数字后行内无其他数字 → 补量词与阈值。
- [ ] 非全节照录（全节照录 = 换皮重排，打回）。

### 可收编译演证
- [ ] 试映射判据：低置信 = 0；中置信行全带显式子节归属（AeroFold 实测校准：高 9/中 4/低 0）。
- [ ] Q 表候选仅限源注册表沿用 + 停点②遗留（禁新造模糊点充数）。
- [ ] spec-lint L1/L2/L3 离线复跑零命中（L1 词表 / L2 ID 引用完整 / L3 NFR 数值）。
- [ ] `python campaign/tools/doc_graph.py build <产物>` 建图成功。

### 停点③
- [ ] 三证全过 → 落盘双产物（转化文档 + 收编预案五件套）；任一缺 → 状态不迁移，上报用户。

（数值锚 = 校准口径，见 `references/skeleton-aerofold.md` 收编校准数据；金样判据阈值首轮实测后由编排者固化进本节。）
