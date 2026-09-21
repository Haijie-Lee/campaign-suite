# handoff — campaign 生存包

> 更新人：编排者；更新时机：每个停止点与单元边界。hook 只读注入，不改写本文件。

- 当前单元：无（W1–W4 四波全量建成；**aerofold-m0 程序 6/7 complete + 1 blocked 挂起收官@2026-09-21，该程序状态已随工程迁至 C:\WorkSpace\AeroFold\.campaign\program\**）
- 已过门：w1/w2/w3/w4 出口全过；**M0 单元门**：U-M0-01 需求冻结（Q18/Q19→C10/C11，fixture v0.7）/ U-M0-02 API 契约 v1.0 定版（REST 26+WS 30+错误码 16，补 /diag/* 缺口 G1/G2）/ U-M0-03 UI 原型三屏（C7/C8 四件全覆盖）/ U-M0-04 技术栈决策门①=**Rust+Tauri 2 确认**（PoC 实测吞吐 2043 vs 1372 MB/s、内存 13 vs 33 MB）/ U-M0-05 iroh 1.2.0 工程闭环五项实证（吞吐 225 MB/s），**决策门②挂起待国内实测**（用户更严证据标准）/ U-M0-06 Layer A 标定四条参数（超时 300ms/并行/UDP 三级/STUN 降级）/ U-M0-07 blocked
- M0 对账①：无漂移（计数路径 complete=5 触发，fresh agent）@2026-09-21
- 待裁定：①附录B 分类基准修正（继续挂起）；②无其他
- 下一步（重访触发器序）：**M1 服务端骨架**（境内 iroh-relay + 自建 STUN 部署）→ 同一验证窗口 resume 三件：决策门②国内实测 + U-M0-06 B/C 层标定 + U-M0-07 中继限速裁决；「M0 全程」出口判据回验义务 = 设计文档 §4.3 v1.2 注记（回验清单新增：决策门②挂起、U-M0-07 blocked）
- ledger：wave 账本 C:\WorkSpace\campaign-suite\.campaign\ledger.jsonl；程序账本 .campaign/program/smoke-w4-ledger.jsonl + aerofold-m0-ledger.jsonl（按程序隔离，K20）
- 关键路径：设计文档与调研 = C:\Users\Administrator\WorkBuddy\2026-09-20-21-39-26\（campaign插件设计文档.md v1.2、W1–W4 plan 等 10 份）
- **AeroFold 工程资产已迁出（2026-09-21）** → `C:\WorkSpace\AeroFold\`（docs/ SRS v0.7、poc/、acceptance/ 36 条 AC、.campaign/ 程序状态与 M0 证据 u01–u06）。本仓库仅保留插件本体 + W1–W4 出口证据（`campaign/acceptance/` 只留通用 runner 与契约说明）；AeroFold 侧续跑 M1 时工作目录切到该工程目录。
- 环境实测坑：WorkBuddy shell 常设 CLAUDE_PROJECT_DIR（测 hook 需 env -u）；Git Bash /tmp = C:\Users\Administrator\AppData\Local\Temp；bash 喂 Windows python 一律 cygpath -w；Windows python print CRLF；grep 表行断言用 grep -F
- 工具教训（累积）：①同文件 Edit 严格一条一消息 ②回读 grep 模式必须为目标位置独有 ③修复落盘必回读 ④fresh 闸口发现数不收敛于零是机制属性 ⑤子代理 429 = 配置类停止点上报裁定 ⑥彩排是抓真缺陷的 ⑦**iroh 1.2 工程三坑**：builder 必传 preset（禁 N0）/ crypto_provider 必挂 builder（全局 install_default 无效）/ ALPN 必双端配置
- 待办（后续波次）：staleness 检测；「等」词带边界规则；附录B 分类基准修正；doc_graph v1.2（FR-8/9/10 假阳性）；revision_scope v1.1 两项；**「M0 全程」判据回验（挂起）**；spec-lint 路径模式不覆盖 .campaign/evidence/（lint 需手动触发，M1 前考虑扩模式）
- 本会话新挂起（M0 程序层）：决策门②国内实测 / U-M0-06 B/C 标定 / U-M0-07 中继裁决（三合一验证窗口=M1 中继部署后）；macOS 复测+安装包体积+签名公证+杀软（M1 打包流水线期）；三档体检参数正式值（随 B/C 标定，联动 U03-A1）；Python 长稳性（仅当降级 Python 路径时）
