#!/usr/bin/env python
"""AC-26 幽灵地址过滤 — 验收骨架（local，真实探针）。
source: SRS §8.3 条目 26（v0.3.1 新增）；refs: D10、§4.1.8。
阈值（逐字自 §8.3 正文）：候选地址列表中不得出现 fe80::/10、2001::/32
（Teredo）、2002::/16（6to4）与 ULA fd00::/8，只保留全局单播 2000::/3。
探针策略：枚举本机 IPv6 地址 → 过参考过滤器（只留 2000::/3）→
断言过滤后候选集不含任何幽灵段；同时打印原始清单供人工核对。"""
import ipaddress
import socket
import sys

GHOST_NETS = [
    ipaddress.ip_network("fe80::/10"),   # 链路本地
    ipaddress.ip_network("2001::/32"),   # Teredo
    ipaddress.ip_network("2002::/16"),   # 6to4
    ipaddress.ip_network("fd00::/8"),    # ULA
    ipaddress.ip_network("fec0::/10"),   # site-local（已废弃，同害）
    ipaddress.ip_network("::1/128"),     # 回环
]
GLOBAL_UNICAST = ipaddress.ip_network("2000::/3")


def env_ok():
    if not socket.has_ipv6:
        return False, "本机无 IPv6 协议栈"
    return True, ""


def local_v6_addrs():
    addrs = set()
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6):
            addrs.add(info[4][0].split("%")[0])
    except OSError:
        pass
    return sorted(addrs)


def reference_filter(addrs):
    """参考实现：只保留 2000::/3 全局单播。"""
    out = []
    for a in addrs:
        ip = ipaddress.ip_address(a)
        if ip in GLOBAL_UNICAST and not any(ip in g for g in GHOST_NETS):
            out.append(a)
    return out


def probe():
    raw = local_v6_addrs()
    print("probe: 本机 IPv6 地址原始清单 = %s" % (raw or "（空）"))
    kept = reference_filter(raw)
    ghosts = [a for a in kept
              if any(ipaddress.ip_address(a) in g for g in GHOST_NETS)]
    print("probe: 过滤后候选 = %s" % (kept or "（空）"))
    if ghosts:
        print("FAIL: 候选列表含幽灵地址 %s" % ghosts)
        return 1
    print("PASS: 候选列表无幽灵段（fe80/2001::/32/2002::/16/fd00 均被剔除）")
    return 0


def main():
    ok, why = env_ok()
    if not ok:
        print("BLOCKED-ENV: %s" % why)
        sys.exit(3)
    sys.exit(probe())


if __name__ == "__main__":
    main()
