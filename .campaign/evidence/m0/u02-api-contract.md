# AeroFold API 契约 v1.0（定版）

> 版本：v1.0（2026-09-21 定版，M0 单元 U-M0-02 产出）
> 基线：AeroFold SRS v0.7 §6.5 / §6.6 / §6.1 / §8.2；本文档为接口**规范源**，SRS §6.5/§6.6 降级为摘要——冲突以本契约为准（裁决 R-CONTRACT-1）。
> 两态标记：直接来自 SRS 的条目不带标记；本契约新增/补全的条目带【新增·G2】（用户裁定 2026-09-21）或【假设·验证=待】。
> 追溯：端点 → SRS ID 的映射见 §6 追溯矩阵。

## 0. 版本与兼容性策略

| 项 | 约定 |
|---|---|
| 契约版本 | 独立于产品版本，SemVer：`MAJOR.MINOR`。MAJOR = 不兼容变更（删字段/改语义/改错误码含义）；MINOR = 兼容增量（加端点/加可选字段/加事件） |
| 路径版本 | URL 前缀 `/api/v1`；MAJOR 升级时升 `/api/v2`，v1 至少并行维护一个 MINOR 周期 |
| 客户端兼容 | 服务端必须忽略未知请求字段；客户端必须忽略未知响应字段与未知 WS 事件类型（健壮性原则） |
| 变更流程 | 契约修订走 campaign REVISION 模式（B4）：diff + revision_scope 涟漪 + 双声部审计后落账 |

## 1. 传输与鉴权

| 项 | 约定 | 来源 |
|---|---|---|
| 控制面传输 | HTTP/2 + TLS 1.3（后续可平滑升级 HTTP/3） | SRS §4.4 行 1338 |
| 实时通道 | `wss://<host>/api/v1/ws` | SRS §6.6 |
| 鉴权豁免 | 仅 `GET /health` 与 `POST /devices/register` 免鉴权 | SRS §6.5 |
| 设备鉴权 | **设备签名（Ed25519 挑战-响应）**：客户端对服务端下发的 nonce 签名，换取访问令牌；REST 携带 `Authorization: Bearer <device_token>` | SRS §6.1.3（票据换取） |
| 会话票据 | JWT（EdDSA 签名），有效期 10 分钟，绑定 `session_id` + `device_id`；仅对所属会话资源有访问权；过期后凭设备签名换新 | SRS §6.1.3 |
| WS 鉴权 | 连接首帧发送设备签名（同挑战-响应），鉴权失败即关闭（close code `4401`）【新增·G2 补 close code】 | SRS §6.6 |
| 密钥（业务） | 接收密钥（固定/临时）**仅用于配对握手**，不作 API 鉴权凭证；握手成功后会话票据接管 | SRS §6.1 |

## 2. 通用约定

### 2.1 错误信封（全接口统一）

```json
{
  "error": "MACHINE_READABLE_CODE",
  "message": "面向用户的可读描述",
  "details": { "任意补充字段": "可选" },
  "request_id": "srv-生成的请求 ID，排障用"
}
```

### 2.2 错误码表（全量入契，用户裁定 2026-09-21）

| 错误码 | HTTP | 语义 | 来源 |
|---|---|---|---|
| `RECEIVER_OFFLINE` | 409 | 接收端离线（竞态拦截），附 `last_seen_at` | SRS §6.5 |
| `KEY_INVALID` | 403 | 密钥错误或已吊销 | SRS §6.1 推全 |
| `KEY_EXPIRED` | 403 | 临时密钥过期（含宽限期外） | SRS §6.1.2 |
| `KEY_ALREADY_USED` | 409 | 临时密钥单次使用已消耗 | SRS §6.1.2 |
| `NOT_IN_ALLOWLIST` | 403 | 固定密钥流程：发送端设备不在白名单（降级为需人工确认时以 `need_confirm` 表达，非本错误） | SRS §6.1.1 |
| `CONFIRM_TIMEOUT` | 409 | 临时密钥确认超时 | SRS §6.5 `confirm_timeout_seconds` |
| `SESSION_NOT_FOUND` | 404 | 会话不存在或不属于本设备 | 通用 |
| `SESSION_STATE_CONFLICT` | 409 | 当前会话状态不允许该操作（如已 completed 再 accept） | 通用 |
| `TICKET_EXPIRED` | 401 | 会话票据过期，需凭设备签名换新 | SRS §6.1.3 |
| `DEVICE_AUTH_FAILED` | 401 | 设备签名校验失败 | §1 |
| `RATE_LIMITED` | 429 | 触发限流（见 §2.3），附 `retry_after_seconds` | SRS §6.1.2 限流 |
| `QUOTA_EXCEEDED` | 429 | 体检中继流量配额超限（D17/C10 计量告知） | SRS §8.2 |
| `UPLOAD_OFFSET_MISMATCH` | 409 | tus 续传偏移与服务端记录不一致 | SRS §6.5 tus |
| `PAYLOAD_TOO_LARGE` | 413 | 超出接口声明的大小上限 | 通用 |
| `VALIDATION_FAILED` | 400 | 请求字段校验失败，`details.fields` 指明字段 | 通用 |
| `INTERNAL_ERROR` | 500 | 服务端内部错误，附 `request_id` | 通用 |

### 2.3 限流（配对/密钥域，SRS §6.1.2 原值）

| 维度 | 限额 |
|---|---|
| 单设备失败（密钥校验） | 60 s 内 ≤ 5 次，超出锁定 15 分钟 |
| 单 IP | 60 s 内 ≤ 20 次尝试 |
| 单接收端 `device_id` | 60 s 内 ≤ 10 次 |
| 连续失败退避 | 0 s → 2 s → 5 s → 15 s → 60 s |

超限一律返回 `RATE_LIMITED` + `retry_after_seconds`。

### 2.4 其他约定

| 项 | 约定 |
|---|---|
| 时间 | RFC 3339 UTC（`2026-09-20T11:32:04Z`） |
| 字节数 | 整数，单位 byte |
| 速率 | `mbps` = 十进制兆比特每秒（10⁶ bit/s） |
| 幂等 | 变更类 POST 支持 `Idempotency-Key` 头（24 h 内重放返回首次结果）；`/pair`、`/sessions/{id}/candidates`、`/diag/checks` 强制支持【新增·G2】 |
| 分页 | 列表接口（`/history`、`/receive/keys`、`/allowlist`）支持 `cursor` + `limit`（默认 50，上限 200）【新增·G2】 |

## 3. REST 接口（前缀 `/api/v1`）

### 3.1 健康与能力

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/health` | 免鉴权。返回 `{version, time, capabilities:[...]}`；`capabilities` 枚举：`pair / fixed_key / temp_key / tus_fallback / diag / stun / relay`【新增·G2 枚举值】 |

### 3.2 设备

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/devices/register` | 免鉴权。提交 `{public_key(ed25519), platform, name}` → `{device_id, server_nonce}`；后续以设备签名换访问令牌 |
| `GET` | `/devices/me` | 本设备信息与在线状态 |
| `GET` | `/devices/{id}/presence` | 目标设备在线状态（发送端解锁/置灰「发送」按钮，FR-4.6b）→ `{device_id, online, last_seen_at}` |

### 3.3 接收密钥

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/receive/keys` | 生成密钥：`{type:"fixed"\|"temp", ttl?}`（temp 默认 600 s，60–3600 s 可配） |
| `GET` | `/receive/keys` | 列出本设备密钥（仅前缀与元信息，不回明文/哈希） |
| `POST` | `/receive/keys/{id}/rotate` | 轮换：`{immediate:true}` = 手动刷新（旧密钥立即失效）；否则旧密钥进 `grace`（默认 120 s） |
| `DELETE` | `/receive/keys/{id}` | 吊销，即时生效，不影响进行中会话 |

### 3.4 白名单（C2 强制）

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/allowlist` | 列出发送端设备公钥指纹（Ed25519 SHA-256） |
| `POST` | `/allowlist` | 新增：`{sender_device_id, public_key_fingerprint}` |
| `DELETE` | `/allowlist/{sender_device_id}` | 移除；不影响进行中会话 |

### 3.5 配对

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/pair/prepare` | 发送前预检：提交密钥 → 目标信息/在线状态/是否需人工确认；**不下发凭证、不消耗密钥次数**。响应 schema 见 SRS §6.5 示例（定版照收） |
| `POST` | `/pair` | 提交密钥 + 文件清单；服务端二次校验在线状态 → `{session_id}` 或 `{state:"pending", expires_at, confirm_timeout_seconds:120}`。请求 schema 见 SRS §6.5 示例（定版照收，字段含 `path_preference / strict_direct / ipv6_enabled / health_check_profile`） |

### 3.6 会话与打洞

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/sessions/{id}` | 会话状态与进度 |
| `POST` | `/sessions/{id}/accept` | 接收端接受（临时密钥流程） |
| `POST` | `/sessions/{id}/reject` | 接收端拒绝：`{reason}` |
| `POST` | `/sessions/{id}/candidates` | 上报本端候选列表（C5）：`{candidates:[{type, ip, port, priority}]}`，`type ∈ lan\|ipv4_srflx\|ipv6\|relay`；**仅地址，不含密钥材料**（§4.1.3 安全约束）；`ipv6_enabled=false` 时不得含 `ipv6` 项（C6） |
| `GET` | `/sessions/{id}/candidates` | 拉取对端候选列表 |
| `POST` | `/sessions/{id}/path` | 建链结果上报（C5）：`{path_type, measured_mbps, rtt_ms}`，`path_type ∈ lan\|ipv6\|udp_punch\|tcp_punch\|relay`；用于成本归因/排障/配额 |
| `POST` | `/sessions/{id}/resume-state` | 接收端上报续传状态：`{file_id, contiguous_offset, bitmap_ranges, verified_ok}`，云端转发发送端 |
| `POST` | `/sessions/{id}/files` | 声明文件元数据 `{rel_path, size, hash}`；直连路径仅控制面登记，数据不经此接口 |
| `GET` | `/stun/credentials` | （可选）自建 STUN 临时凭据；STUN 本身走标准协议不经业务网关 |

### 3.7 降级上传/下载（tus 兼容，仅降级路径）

| 方法 | 路径 | 说明 |
|---|---|---|
| `PATCH` | `/uploads/{upload_id}` | tus 写分片：`Upload-Offset` 头 |
| `HEAD` | `/uploads/{upload_id}` | tus 查偏移（**非权威**，`Upload-Offset-Authority: receiver-reported`） |
| `DELETE` | `/uploads/{upload_id}` | 取消上传并清理会话缓冲 |
| `GET` | `/downloads/{file_id}` | 接收端拉取分片流，`offset` 参数续收 |

> **直连路径下本组接口完全不参与数据传输**（C5 接口层变化，SRS §6.5 注记定版照收）。

### 3.8 历史

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/history` | 传输历史，`cursor`/`limit` 分页 |

### 3.9 体检（/diag/*，【新增·G2】用户裁定 2026-09-21）

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/diag/checks` | 发起体检：`{profile:"quick"\|"standard"\|"deep", include_relay_baseline?:bool}`（`include_relay_baseline` 默认 `false`，用户显式开启，D17）→ `{check_id, est_bytes, est_seconds}`；深度档且蜂窝网络 → 服务端标记 `need_confirm:true`（FR-9.11/C10），客户端须二次确认后 WS 才会推 `diag.started` |
| `GET` | `/diag/checks/{id}` | 查询体检结果快照：`{check_id, status, recommended_path, bottleneck, uplink_mbps, downlink_mbps, est_seconds, probe_bytes:{up,down,via_relay}}`（与 `diag.completed` 载荷同构） |
| `GET` | `/diag/policy` | 服务端下发体检默认档位与单设备中继流量配额（SRS §8.2）：`{default_profile, relay_quota_bytes, cellular_confirm_required}` |

> 体检分层进度、单路径结果与失败归因走 WS `diag.*` 事件（§4），REST 只做发起与查询——与 SRS「WS 以事件推送为主」形态一致。

## 4. WebSocket 协议

### 4.1 连接与生命周期

| 项 | 约定 | 来源 |
|---|---|---|
| 地址 | `wss://<host>/api/v1/ws` | SRS §6.6 |
| 鉴权 | 首帧设备签名（挑战-响应），失败关闭 `4401` | SRS §6.6 |
| 心跳 | 15 s 双向心跳；服务端连续 45 s 未收到判定离线，触发对端 `device.presence` 推送 | SRS §6.6 |
| 事件信封 | `{type, seq, ts, payload}`；`seq` 服务端单调递增，重连后客户端可带 `last_seq` 请求补发（窗口 ≤ 500 条）【新增·G2 补发窗】 | 信封字段为定版补全 |

### 4.2 事件表（定版照收 SRS §6.6 全量 30 事件）

方向记号：C=云端，S=发送端，R=接收端，UI=本地界面。

| 事件 | 方向 | 载荷要点 |
|---|---|---|
| `device.online` | S/R→C | 设备上线刷新状态 |
| `device.presence` | C→S | `{device_id, online, last_seen_at}` |
| `pair.request` | C→R | 发送方设备名/IP/文件清单/总大小 |
| `pair.accepted` | C→S | `{session_id, candidates}` |
| `pair.rejected` | C→S | `{reason}` |
| `pair.timeout` | C→S/R | 确认超时 |
| `connect.candidates` | 双向（经 C 转发） | `{session_id, candidates:[{type,ip,port,priority}]}` |
| `connect.progress` | 本地→UI | `{step, label}` |
| `connect.established` | 本地→C（可选） | `{session_id, path_type, measured_mbps, rtt_ms, selected_reason}` |
| `connect.failed` | 本地→UI | `{reason: all_direct_failed\|strict_mode_blocked\|udp_blocked}` |
| `path.changed` | 双向（经 C 转发） | `{session_id, from, to, reason: degraded\|throttled\|nat_expired\|profile_stale}` |
| `fallback.pool_probed` | 本地→UI | `{session_id, candidates:[{region,rtt_ms,coarse_mbps,ranking}], chosen}` |
| `fallback.verifying` | 本地→UI | `{session_id, relay_region, probe_seconds}` |
| `fallback.verdict` | 本地→UI | `{session_id, relay_region, measured_mbps, verdict: accepted\|below_floor\|unusable}`（`below_floor` 触发前置确认弹窗，FR-10） |
| `fallback.node_switched` | 本地→C（可选） | `{session_id, from_region, to_region, reason}` |
| `path.failback` | 本地→C（可选） | `{session_id, from_relay, to_direct, measured_mbps, ratio}` |
| `degrade.narrative` | 本地→UI | `{session_id, steps:[{stage,outcome,detail}], eta_seconds, server_bytes_est}`（FR-10.10 因果链直渲） |
| `diag.started` | 本地→UI | `{check_id, profile, est_bytes, est_seconds}`（蜂窝必确认，FR-9.11/C10） |
| `diag.layer` | 本地→UI | `{check_id, layer:"A"\|"B"\|"C", status, progress, detail}` |
| `diag.path_result` | 本地→UI | `{check_id, path, reachable, rtt_ms, punch_ms, mbps, via_server}` |
| `diag.completed` | 本地→UI/C | `{check_id, recommended_path, bottleneck, uplink_mbps, downlink_mbps, est_seconds, probe_bytes:{up,down,via_relay}}` |
| `diag.failed` | 本地→UI | `{check_id, layer, reason: udp_outbound_blocked\|peer_offline\|probe_aborted}` |
| `diag.profile_invalidated` | 本地→UI | `{reason: network_changed\|ip_changed\|resume_from_sleep\|ttl_expired\|deviation_exceeded}` |
| `transfer.incoming` | C→R | 固定密钥免确认投递通知 |
| `transfer.progress` | 双向 | 会话/文件级进度（节流 500 ms） |
| `transfer.paused` | 双向 | 必须带 `reason: user\|network\|peer_offline\|receiver_disk_full` |
| `resume.state` | R→C→S | `{file_id, contiguous_offset, bitmap_ranges, verified_ok}` |
| `transfer.completed` | C→S/R | 完成 |
| `transfer.failed` | C→S/R | 失败，附错误码（§2.2 表内值） |
| `key.revoked` | C→R | 多端同步 |
| `key.rotated` | C→R | `{old_id, new_id, new_prefix, expires_at, grace_expires_at}` |

## 5. 定版裁决记录

| 编号 | 裁决 | 依据 |
|---|---|---|
| R-CONTRACT-1 | 本文档为接口规范源，SRS §6.5/§6.6 降级为摘要 | 单元目标「定版」的语义落实 |
| G1 | `/diag/policy` 补入 REST 表（SRS §8.2 行 2239 有引用而 §6.5 表缺失） | 机械收编，用户裁定 2026-09-21 |
| G2 | `/diag/*` 接口族定版为 REST 入口式（`POST /diag/checks` + `GET /diag/checks/{id}` + `GET /diag/policy`），进度走 WS；错误码表全量入契 | 用户裁定 2026-09-21（两问均推荐项） |
| 【假设·验证=待】 | 事件信封 `seq`/补发窗口 ≤ 500 条、WS close code `4401`、`capabilities` 枚举值、分页 `cursor/limit` 默认值——四项为契约工程补全，无 SRS 直接出处，M1 服务端骨架实现期回验 | spec-forge K14 两态纪律 |

## 6. 追溯矩阵

| 契约条目 | SRS 锚点 |
|---|---|
| 密钥生成/轮换/吊销（§3.3） | FR-3.x、C1、§6.1.1/6.1.2 |
| 白名单（§3.4） | C2、§6.1.1 |
| 配对预检与配对（§3.5） | FR-4.x、FR-4.6b、Q5（已决） |
| 候选交换/路径上报（§3.6） | C5、C6、FR-8.2、FR-8.19、§4.1.3 安全约束 |
| 会话票据（§1） | §6.1.3、NFR-4.x |
| tus 降级（§3.7） | C8、FR-10.x、§6.5 注记 |
| 体检族（§3.9 + `diag.*`） | C7、C10、D17、FR-9.4、FR-9.11、§8.2 |
| 降级叙事/前置确认（§4.2） | C8、FR-10.10、NFR-2.12～2.14 |
| 限流（§2.3） | §6.1.2、NFR-4.3 |
| 错误码 `QUOTA_EXCEEDED` | C10、§8.2 配额 |

---
*U-M0-02 产出。修订走 campaign REVISION 模式（§0 变更流程）。*
