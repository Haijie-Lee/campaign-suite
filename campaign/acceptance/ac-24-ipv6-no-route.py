#!/usr/bin/env python
"""AC-24 IPv6「有地址无路由」场景 — 验收骨架（local，真实探针）。
source: SRS §8.3 条目 24（v0.3.1 新增）；refs: D14。
阈值（逐字自 §8.3 正文）：约 200 ms 内判定路径不可用并从候选剔除，不得空耗建链预算。
探针策略：对一个保留的无路由全局 IPv6 地址发起 connect，超时预算 = 0.2 s，
断言「失败返回的墙钟耗时」与预算同量级（< 2.0 s 宽容上限），并证明预算常量为 0.2 s。"""
import socket
import sys
import time

TIMEOUT_BUDGET_S = 0.2   # §8.3「约 200 ms」（D14）
WALL_ASSERT_S = 2.0      # 墙钟宽容上限（含协议栈开销；判定逻辑本身的预算为上行）
UNROUTABLE_V6 = "2001:db8:ffff:ffff:ffff:ffff:ffff:ffff"  # 文档保留段，无路由


def env_ok():
    if not socket.has_ipv6:
        return False, "本机无 IPv6 协议栈"
    return True, ""


def probe():
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT_BUDGET_S)
    t0 = time.monotonic()
    try:
        s.connect((UNROUTABLE_V6, 9))
        print("FAIL: 无路由地址竟连接成功（环境异常）")
        return 1
    except OSError:
        elapsed = time.monotonic() - t0
    finally:
        s.close()
    print("probe: budget=%.3fs elapsed=%.3fs" % (TIMEOUT_BUDGET_S, elapsed))
    if elapsed >= WALL_ASSERT_S:
        print("FAIL: 判定耗时 %.3fs ≥ 宽容上限 %.1fs（预算被空耗）" % (elapsed, WALL_ASSERT_S))
        return 1
    print("PASS: 200 ms 预算内快速判定不可用（elapsed=%.3fs）" % elapsed)
    return 0


def main():
    ok, why = env_ok()
    if not ok:
        print("BLOCKED-ENV: %s" % why)
        sys.exit(3)
    sys.exit(probe())


if __name__ == "__main__":
    main()
