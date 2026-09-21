#!/usr/bin/env python
"""AC-25 Windows 10 双栈 socket — 验收骨架（local，真实探针）。
source: SRS §8.3 条目 25（v0.3.1 新增）；refs: R19、§8.1 M0。
阈值（逐字自 §8.3 正文）：双栈监听时 IPv4 与 IPv6 客户端均可成功连接
（验证 IPV6_V6ONLY=0 已被显式设置）。
探针策略：按 R19 对策用 socket 显式构造 AF_INET6 监听并 set only_v6=False，
再从 ::1（v6）与 127.0.0.1（v4）各连一次，两端都通 = PASS。"""
import socket
import sys

IPV6_V6ONLY = 27  # Windows/Linux 常量值一致


def env_ok():
    if not socket.has_ipv6:
        return False, "本机无 IPv6 协议栈"
    return True, ""


def _try_connect(family, addr, port):
    s = socket.socket(family, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect((addr, port))
        return True
    except OSError:
        return False
    finally:
        s.close()


def probe():
    srv = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    srv.setsockopt(socket.IPPROTO_IPV6, IPV6_V6ONLY, 0)  # set_only_v6(False)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        srv.bind(("::", 0))
    except OSError as e:
        print("BLOCKED-ENV: 无法绑定 [::]:0（%s）" % e)
        return 3
    srv.listen(2)
    port = srv.getsockname()[1]
    import threading

    def acceptor():
        try:
            srv.settimeout(3.0)
            for _ in range(2):
                c, _ = srv.accept()
                c.close()
        except OSError:
            pass

    t = threading.Thread(target=acceptor, daemon=True)
    t.start()
    v6 = _try_connect(socket.AF_INET6, "::1", port)
    v4 = _try_connect(socket.AF_INET, "127.0.0.1", port)
    srv.close()
    print("probe: ipv4_connect=%s ipv6_connect=%s (IPV6_V6ONLY=0)" % (v4, v6))
    if v4 and v6:
        print("PASS: 双栈监听 v4/v6 均可连接（only_v6=False 显式设置生效）")
        return 0
    print("FAIL: v4=%s v6=%s —— 双栈语义不符（R19 陷阱复现）" % (v4, v6))
    return 1


def main():
    ok, why = env_ok()
    if not ok:
        print("BLOCKED-ENV: %s" % why)
        sys.exit(3)
    sys.exit(probe())


if __name__ == "__main__":
    main()
