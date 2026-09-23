# Pass 3 — Knowledge Synthesis

输入 Statements + Questions + 所有正式 SourceRef，包括专家认知、机构政策和真实案例；跨 SourceUnit、跨来源形成稳定的 Term / Rule / Case / Issue。

## Rule 分类

每条 Rule 必须标明：

- NORMATIVE
- INTERPRETIVE
- OPERATING_POLICY

同时独立保留 origin（SOURCE_STATED / INFERRED / PROPOSED）与 review_status。

## Rule 粒度

不要把多个可独立改变结论的判断塞进一个 Rule。以下任一变化会独立改变业务结论时，通常应拆 Rule：

- 适用对象不同；
- 前置条件不同；
- 证据要求不同；
- 阈值或计算方式不同；
- 缺证行为不同；
- 时间成立/失效条件不同；
- 自动/人工边界不同。

## 高影响 Rule

impact=HIGH 时，必须形成：

- business_conclusion
- required_facts
- decision_steps
- evidence_requirements
- non_sufficient_facts
- unknown_behavior
- human_boundary
- case_ids

Rule 不能只写“查明事实”“缺证待核”这种模板句。

## Cases

Case 来源必须区分：

- REAL_CONFIRMED
- SOURCE_CASE
- SYNTHETIC_PROBE

合成探针只能测试/证伪/暴露边界，不能证明本次生成 Rule 的权威性。
