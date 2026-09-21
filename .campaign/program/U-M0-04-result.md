verdict: pass
结论: 技术栈决策门闭合——主选 Rust + Tauri 2 确认（用户裁定）；PoC 实测 2/5 项（吞吐 Rust 2043 vs Python 1372 MB/s、内存 13 vs 33 MB，哈希逐字节一致）未推翻 SRS 推荐；3 项环境不可达 + macOS 全部显式挂 M1 流水线期
证据: .campaign/evidence/m0/u04-techstack-decision.md（决策记录+实测数据+挂起项触发器）；/tmp/u04-poc/（Rust 工程+Python 脚本+bench.txt）
实测: budget 201600s vs 实际约 2700s（PoC 范围按会话可达性收缩，收缩项全部挂起带触发器）
ruling: M0 决策门①=Rust + Tauri 2 确认（用户显式）；开发规范硬条目=Tauri 原生拖拽 API 禁用 HTML5 drop
