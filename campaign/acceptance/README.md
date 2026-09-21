# C6 验收基座（K22 runner 契约）

本目录只保留**机制**，不含任何具体项目的验收条目。

- `run_all.py` —— 通用执行器，与项目无关。

## 契约

**骨架三态结构**：每个验收脚本实现三段，按序短路。

| 段 | 职责 | 不成立时 |
|---|---|---|
| `env_ok()` | 环境探测：外部网络 / 多机 / 运营商条件 | `BLOCKED-ENV`，exit 3 |
| `impl_ok()` | 实现探测：被测产品是否已构建 | `BLOCKED-IMPL`，exit 4 |
| `probe()` | 真实探针 + 断言，阈值写进常量 | PASS exit 0 / FAIL exit 1 |

**退出码归类**：`0=PASS / 1=FAIL / 3=BLOCKED-ENV / 4=BLOCKED-IMPL`，其余与超时、异常一律记 `FAIL`。

**原则**：没跑通过 ≠ 通过，也不许静默跳过 —— 必须显式归类为「缺环境」或「缺实现」，并说明缺什么。

**注册表 schema**（`ac-registry.yaml`，由使用方在本目录或工程目录自建）：

```yaml
- id: AC-01
  title: "<逐字取自 SRS 验收章节>"
  source: "§8.3 条目 01"
  refs: "FR-1"
  env_class: local|network|product
  skeleton: acceptance/ac-01-xxx.py
  status: pass|fail|blocked-env|blocked-impl|not-run
```

`title` 必须逐字引用需求文档的验收条目，不得改写；`env_class` 决定 `env_ok()` 的探测口径。

## 用法

```bash
python run_all.py --out <汇总路径> --registry <ac-registry.yaml>   # 后者会把 status 回写注册表
python run_all.py --dir <其他骨架目录>                              # 默认为本文件所在目录
```

runner 顺序执行、逐条捕获，**汇总恒 N 行、自身退出码恒 0**，单条失败不中断整轮。

## 归处

具体验收条目属**工程资产**，不属插件。AeroFold 的 36 条 AC 实例已迁至 `C:\WorkSpace\AeroFold\acceptance\`（2026-09-21）。
