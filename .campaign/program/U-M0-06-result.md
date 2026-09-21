verdict: pass
结论: Layer A 时间窗标定完成——FR-9.4「<1s」成立（边界=单点超时≤300ms+多 STUN 并行）；实测参数集四条（超时 300ms/并行/UDP 三级分层/STUN 降级语义）+ 本机画像发现（IPv4 虚拟接口稀释、公共 STUN 全不可达）；B/C 层挂起待 M1 环境
证据: .campaign/evidence/m0/u06-probe-calibration.md；/tmp/u04-poc/layer-a-calib.txt（原始数据）
实测: budget 100800s vs 实际约 1500s（部分执行裁定：Layer A 本地标定，B/C 挂起带触发器）
ruling: 部分执行闭合（用户显式）；三档正式参数回验挂 M1（联动 U03-A1）
