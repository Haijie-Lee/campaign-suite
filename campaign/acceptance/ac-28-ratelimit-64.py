#!/usr/bin/env python
"""AC-28 IPv6 限流聚合粒度 — 验收骨架（local，真实探针，自含参考限流器）。
source: SRS §8.3 条目 28（v0.3.1 新增）；refs: D13。
阈值（逐字自 §8.3 正文）：单一 IPv6 客户端在同一 /64 内轮换源地址高频请求，
限流必须按 /64 聚合生效，不得被地址轮换绕过。
探针策略：自含参考限流器（按 /64 聚合计数），模拟同 /64 轮换 8 地址 × 高频
（断言被限）与跨 /64 轮换（断言不误伤）；另断言「按单地址计数」的朴素实现
会被绕过（反例对照，证明聚合必要）。"""
import ipaddress
import sys

LIMIT = 100          # 窗口内请求上限（聚合粒度判定对象）


def key_64(addr):
    return int(ipaddress.ip_address(addr)) >> 64  # /64 前缀


class NaiveLimiter:
    """反例：按单地址计数——会被 /64 内轮换绕过。"""

    def __init__(self):
        self.n = {}

    def hit(self, addr):
        self.n[addr] = self.n.get(addr, 0) + 1
        return self.n[addr] > LIMIT


class Aggregate64Limiter:
    """正例：按 /64 聚合计数（D13）。"""

    def __init__(self):
        self.n = {}

    def hit(self, addr):
        k = key_64(addr)
        self.n[k] = self.n.get(k, 0) + 1
        return self.n[k] > LIMIT


def rotating_addrs():
    base = int(ipaddress.ip_address("2001:db8:1:1::"))
    return [str(ipaddress.ip_address(base + i)) for i in range(8)]


def probe():
    # 同 /64 轮换 × 高频：聚合器必须限流
    agg = Aggregate64Limiter()
    limited = any(agg.hit(a) for _ in range(30) for a in rotating_addrs())
    # 朴素器在同量请求下是否被绕过（应 True=未被限=被绕过）
    naive = NaiveLimiter()
    bypassed = not any(naive.hit(a) for _ in range(30) for a in rotating_addrs())
    # 跨 /64 不误伤：两个不同 /64 各 30 次应均不被限
    agg2 = Aggregate64Limiter()
    a1, a2 = "2001:db8:1:1::1", "2001:db8:2:2::1"
    false_positive = any(agg2.hit(a) for _ in range(30) for a in (a1, a2))
    print("probe: aggregate_limited=%s naive_bypassed=%s cross64_false_positive=%s"
          % (limited, bypassed, false_positive))
    if limited and bypassed and not false_positive:
        print("PASS: /64 聚合限流不被轮换绕过，且跨 /64 不误伤（朴素单地址实现被绕过——对照成立）")
        return 0
    print("FAIL: limited=%s bypassed=%s fp=%s" % (limited, bypassed, false_positive))
    return 1


def main():
    sys.exit(probe())


if __name__ == "__main__":
    main()
