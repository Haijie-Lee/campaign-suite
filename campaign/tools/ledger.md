# ledger.jsonl — K1 schema

每行一个 JSON 对象，字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `ts` | string | 是 | ISO 8601 本地时间（秒精度），由 ledger.py 生成，禁传入 |
| `event` | string | 是 | `unit_start` / `unit_end` / `verdict` / `ruling` / `reconcile` / `gate` / `note` |
| `unit` | string | 否 | 单元 ID |
| `plan` | string | 否 | 关联 plan 文件路径 |
| `verdict` | string | 否 | `pass` / `fail` / `concerns` |
| `elapsed_s` | int | 否 | 仅 unit_end |
| `detail` | string | 否 | 单行（换行转 `\n` 字面） |

规则：只追加不改写；每条记录以 `\n` 结尾；无 `token` 字段。
默认路径 `./.campaign/ledger.jsonl`；`--file` 三子命令均可覆盖；目录不存在自动创建。

## 示例

```bash
python campaign/tools/ledger.py append --event unit_start --unit m1-server
python campaign/tools/ledger.py append --event verdict --unit m1-server --verdict pass
python campaign/tools/ledger.py append --event unit_end --unit m1-server --elapsed-s 3600
python campaign/tools/ledger.py summary --last 5
python campaign/tools/ledger.py current   # 无未闭合单元时输出 idle
```
