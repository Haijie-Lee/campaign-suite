# U-M0-05 P2P 引擎 PoC 报告（iroh 1.2.0）

> 2026-09-21 · 环境：Windows 10.0.26220 x64 / Rust 1.95 / iroh 1.2.0（与 SRS §4.7 所述版本一致）
> 范围声明：单元三子项中两项复用 W4 验收基座实测（双栈 socket / 幽灵过滤），iroh 子项本会话完成**工程可行性闭环**；「国内实测」（真实 NAT 打洞率 + 境内自建中继）环境不可达，显式挂起带触发器，非缺席。

## 1. iroh 工程可行性闭环（本会话实测）

**方法**：同进程双 Endpoint 全闭环——各自生成 Ed25519 密钥对（公钥即身份），`presets::Empty`（纯直连、无海外发现/中继，即生产配置形态），按公钥身份 + 直连地址拨号（ALPN `aerofold/poc/0`），QUIC+TLS 1.3 端到端加密通道上传输 256 MB。工程：`/tmp/u04-poc/iroh-poc/`。

**实测结果（×3）**：

| 验证点 | 结果 |
|---|---|
| crate 可构建（iroh 1.2.0 + tokio，约 400 依赖） | ✅ 通过 |
| 公钥即身份拨号 + 对端身份验证 | ✅ `remote_id` 与对端 EndpointId 逐字节一致（双向 Ed25519 认证内生于握手） |
| 端到端加密通道建立（QUIC/TLS 1.3） | ✅ 3/3 成功 |
| 流传输吞吐（loopback） | **218.7 / 225.6 / 225.4 MB/s**（中位 225.4） |
| 直连地址枚举 | ✅ 自动枚举本机全部接口地址（含双栈接口） |

**对 SRS 论断的验证**：①「公钥即身份与设备身份模型可合并为同一套」（§4.7 理由 3）——**实证成立**，`EndpointId` 即 Ed25519 公钥，白名单指纹可直接复用；②「端到端加密天然具备」——**实证成立**；③ 吞吐远超产品需求（NFR-2.1 目标 ≈10.6 MB/s，loopback 实测 21× 余量，局域网路径不构成瓶颈）。

**iroh 1.2.0 工程注意项（PoC 踩坑记录，入开发规范）**：
1. `Endpoint::builder(preset)` 必须传 preset（`Empty/Minimal/N0/N0DisableRelay`）；生产禁用 `N0`（海外公共基础设施），应基于 `Empty`/`Minimal` 自建配置；
2. crypto provider 必须**显式挂在 builder**（`.crypto_provider(ring)`），全局 `install_default` 无效；
3. ALPN 必须两端配置（`.alpns(...)`），否则握手报 `no_application_protocol`；
4. 1.2 已含多路径模型（`conn.paths()` / `rtt(PathId)`），与 C8 路径切换设计同向。

## 2. 双栈 socket（复用 W4 实测）

AC-25 骨架实测 **PASS**（W4 首跑，`.campaign/evidence/w4-exit/ac-run-first.txt`）：Windows 10 双栈 socket `socket(AF_INET6)+IPV6_V6ONLY=0` 建通、IPv4 映射地址可连接、ipv4_connect=True 实测数据在档。

## 3. Teredo/6to4 幽灵地址过滤（复用 W4 实测）

AC-26 骨架实测 **PASS**（同上证据档）：fe80/Teredo(2001::/32)/6to4(2002::/16)/ULA 全部剔除，且 2001::/32 ⊂ 2000::/3 白名单形态含反例对照。S1 冒烟另实证本机「有 IPv6 协议栈、无全局地址、Teredo=disabled」画像。

## 4. 环境不可达项（显式挂起，带重访触发器）

| 项 | 缺口 | 重访触发器 |
|---|---|---|
| iroh 国内真实打洞率实测（对标官方 90% 口径 vs NFR-2.5 ≥85%） | 需双端真实 NAT 环境（多运营商） | M1 中段：境内中继部署完成后，用 U-M0-05 工程改造为双端实测版 |
| 自建 `iroh-relay` 境内云主机部署 + HTTPS(443) 兜底验证 | 需云主机 + 域名 + 证书 | M1 服务端骨架单元（M1 行已含「STUN 与中继部署」） |
| UDP 全封场景下中继（TCP/443）兜底实测 | 同上 | 随中继部署一并验证 |

## 5. 结论

工程可行性全部验证通过，未发现推翻 SRS「主选 iroh」的证据；国内实测缺口以挂起项承载并已有明确验证路径（PoC 工程可直接改造复用）。决策记录见 `u05-engine-decision.md`。
