# Pass 4 — Knowledge Audit

这是独立语义审查，不重新生成一套知识。

## 必查维度

1. Source → Knowledge Coverage：重要定义、义务、条件、例外、证据、时间是否有落点。
2. Knowledge → Source Support：Rule 是否有足够 Statement / Source 支撑。
3. Rule Granularity：是否把多个独立判断压成一条。
4. Semantic Depth：高影响 Rule 是否真正足以指导业务判断。
5. Counterfactual：改变关键事实后，是否能解释结果为何变化。
6. Contradiction：规范、官方解释、机构政策、专家认知、案例之间是否被错误融合。
7. Case Independence：SYNTHETIC_PROBE 是否被循环用于证明生成它的 Rule。

## Blocking codes

- SEMANTIC_DEPTH_INSUFFICIENT
- RULE_SPLIT_REQUIRED
- COUNTERFACTUAL_FAILED
- UNRESOLVED_CONTRADICTION
- SYNTHETIC_CASE_CIRCULAR_SUPPORT

只要存在 BLOCK finding，audit_status=BLOCKED，确定性 assembler 必须拒绝生成正式 output.json。
