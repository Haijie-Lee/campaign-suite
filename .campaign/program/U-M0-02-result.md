verdict: pass
结论: API 契约 v1.0 定版——§6.5/§6.6 收编为规范源（REST 26 端点 + WS 30 事件 + 错误码 16 全量入契）；补两处 SRS 真实缺口（/diag/policy 表缺、/diag/* 有名无实），裁定后 REST 入口式落 §3.9
证据: .campaign/evidence/m0/u02-api-contract.md（契约文档）；.campaign/evidence/m0/u02-lint.txt（L1=0/L2=0 PASS）
实测: budget 14400s vs 实际约 2100s（文档单元 inline 执行）
ruling: G1 /diag/policy 补表（机械收编）；G2 /diag/* REST 入口式 + 错误码全量入契（用户裁定两问均推荐项）；R-CONTRACT-1 本契约为接口规范源
