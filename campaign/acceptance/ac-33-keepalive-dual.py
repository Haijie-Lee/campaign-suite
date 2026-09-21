#!/usr/bin/env python
"""AC-33 保活双阈值 — 验收骨架（三态结构）。
source: SRS §8.3 条目 33（v0.5 新增）；refs: FR-8.17、NFR-3.7。
阈值（逐字自 §8.3 正文，进代码常量）：静默 45 s 以上存活（15 s 探测 / 30 s 判死）；30 s 单阈值对照组应断连"""
import sys

ENV_NEED = "NAT 映射 30 s 回收构造环境"
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
    """探针 + 断言：环境与实现就绪后执行。阈值：静默 45 s 以上存活（15 s 探测 / 30 s 判死）；30 s 单阈值对照组应断连"""
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
