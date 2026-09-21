#!/usr/bin/env python
"""AC-30 中继速率验收必做性 — 验收骨架（三态结构）。
source: SRS §8.3 条目 30（v0.5 新增）；refs: FR-10.2、C8。
阈值（逐字自 §8.3 正文，进代码常量）：首分片前必有一次独立中继速率探针（默认 5 s）；移除探针用例必须失败"""
import sys

ENV_NEED = "同 AC-29 环境 + 抓包"
IMPL_NEED = "AeroFold 产品（M1–M3 交付物）"
ENV_CLASS = "network"


def env_ok():
    """环境探测：外部网络/多机/运营商条件。"""
    if ENV_CLASS == "network":
        return False, ENV_NEED
    return True, ""


def impl_ok():
    """实现探测：被测产品是否存在。"""
    return False, IMPL_NEED + " 未构建"


def probe():
    """探针 + 断言：环境与实现就绪后执行。阈值：首分片前必有一次独立中继速率探针（默认 5 s）；移除探针用例必须失败"""
    raise NotImplementedError("pending product build")


def main():
    ok, why = env_ok()
    if not ok:
        print("BLOCKED-ENV: %s" % why)
        sys.exit(3)
    ok, why = impl_ok()
    if not ok:
        print("BLOCKED-IMPL: %s" % why)
        sys.exit(4)
    try:
        probe()
    except NotImplementedError as e:
        print("BLOCKED-IMPL: %s" % e)
        sys.exit(4)


if __name__ == "__main__":
    main()
