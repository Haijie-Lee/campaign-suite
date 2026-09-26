# handoff — campaign 生存包

> 更新人：编排者；更新时机：每个停止点与单元边界。hook 只读注入，不改写本文件。
> A2（0.6.0）：SessionStart 同时注入在途单元 brief 全文（status=in_progress 单元），每程序至多 1 个。

- 当前单元：<unit-id 或 "无">
- 已过门：<最近 3 条门记录，格式 "unit: 门名@日期">
- 待裁定：<停止点描述 或 "无">
- 下一步：<一句话>
- ledger：<.campaign/ledger.jsonl 的绝对路径>
