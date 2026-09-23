# Pass 3 — Knowledge Synthesis

## 目标

输入 Statements + Questions + 所有正式 SourceRef，在必要时结合可获得的 SourceUnit / 原文上下文，形成业务人员能够理解、复核并用于判断的 Term / Rule / Case / Issue。

不要按来源逐段摘要，也不要为了填满 schema 机械生成规则。先把业务判断讲清楚，再映射到结构化字段。

## 生成方法：只做三件事

### 1. 明确“这块知识要帮助业务人员判断什么”

先确定本主题真正要解决的业务判断，再围绕该判断组织材料。

- Question 只用于范围组织和覆盖检查，不能作为 Rule 的依据。
- Term 只在不解释概念就会影响判断时形成，不为凑词典而生成。
- 不按条文数量、Question 数量或预设 Rule 数量分配产物。

### 2. 按业务判断顺序，把分散依据组织成完整说明

围绕同一个判断，将跨 SourceUnit、跨来源的信息按业务顺序连接起来：

1. 什么情况下适用；
2. 需要了解哪些关键事实；
3. 这些事实怎样支持、改变或阻断业务结论；
4. 需要什么证据；
5. 哪些线索单独不足以证明结论；
6. 缺证、冲突或信息不完整时，哪些结论仍成立，哪些必须保持 UNKNOWN；
7. 时间成立、变化、终止如何影响判断；
8. 如涉及自动处理或人工决定，边界依据是什么。

Rule 应承载一个可以独立理解、应用和维护的完整业务判断，并保留该判断内部必要的条件分支。

不要因为某个条件变化会影响结果，就机械拆成多个孤立 Rule。只有当适用范围、业务用途或治理/维护依据确实可以独立使用和维护时，才拆分 Rule。

简单判断允许很短；复杂判断必须充分展开。但不得为了增加篇幅重复结论，也不得补造来源未支持的机构口径。

### 3. 改变关键事实，检查知识是否仍能解释

使用已有真实案例、来源案例，或明确标记的 SYNTHETIC_PROBE 检查：

- 结论成立时，Rule 能否说明为什么成立；
- 改变一个关键事实后，Rule 能否说明为什么结论变化；
- 缺少关键证据时，Rule 能否指出具体缺口以及它影响哪一步判断。

如果现有 Statements 无法支撑必要语义，应形成 Issue 或回到上游补充/修正 Statement；不得在 Synthesis 阶段静默补造事实。

SYNTHETIC_PROBE 只能测试、证伪或暴露边界，不能证明 Rule 的规范效力。

## 输入与来源边界

Statements 是语义索引，不是原文替代品。

涉及适用范围、前置条件、例外、时间、歧义或来源冲突时，应回看可获得的 SourceUnit / 原文必要上下文。若当前输入不足以确认，应形成 Issue，不得凭模型常识补齐。

正式来源角色必须保持区分：

- NORMATIVE_RULE / OFFICIAL_GUIDANCE：规范要求与官方解释；
- EXPERT_KNOWLEDGE：已沉淀的专家认知；
- INSTITUTION_POLICY：机构正式作业口径；
- CASE_EVIDENCE：真实案例与校准证据；
- 其他来源按其 source_role 使用。

案例、同业材料或产品实践不能自动升级为监管要求。

## Rule 分类

每条 Rule 必须标明：

- NORMATIVE
- INTERPRETIVE
- OPERATING_POLICY

同时独立保留 origin（SOURCE_STATED / INFERRED / PROPOSED）与 review_status。

分类边界：

- NORMATIVE：只表达规范来源直接支持的要求，不把业务解释混入规范文本；
- INTERPRETIVE：表达可追溯的业务解释，并明确其依据与不确定性；
- OPERATING_POLICY：表达机构/专家确认的作业规则，必须有 INSTITUTION_POLICY 或 EXPERT_KNOWLEDGE 来源，不得扩张成普遍监管要求。

来源之间存在未解决冲突时，应保留冲突并形成 Issue，不得静默融合成确定结论。

## 质量基准

以下不是合格的复杂业务知识：

> 查明是否支配人事、重大决策、财物；缺协议、决议、行为事实则待核。

它只给出了标签，没有说明判断结构。

合格的复杂业务知识应能回答：

> 判断对象到底是什么；要看哪些事实；事实怎样影响结论；哪些线索单独不足；缺少哪类证据时为什么只能保持 UNKNOWN；何时需要人工判断。

例如“实际控制”类判断应围绕“实际支配能力”组织人事任免、重大决策、财务收支、重要资产或资金等事实，并明确职位、第一大股东或外部标签只能作为线索。缺少关键协议、决议或行为证据时，不得把 UNKNOWN 自动当成 FALSE，也不得直接进入后续兜底。

再例如“简化资格”类判断，应保留“主体性质确认 → 简化条件 → 风险闸门 → 结果”的完整条件分支，而不是把每个分支拆成互相失联的规则。

以上示例仅用于说明知识表达质量，不构成任何领域规则的权威来源。

## Cases

Case 来源必须区分：

- REAL_CONFIRMED
- SOURCE_CASE
- SYNTHETIC_PROBE

Case 用于校准和检查 Rule 是否讲透，不用于凑数量，也不能反向制造规范依据。

## 输出合同：本提示词必须可独立执行

本文件是 Knowledge Synthesis 的完整行为指令。即使运行时只加载本提示词，也不得依赖 SKILL.md 或 schema 来补充业务推理要求。

现有 `synthesis-pass.schema.json` 仍是机器结构校验的权威合同；下面重复列出行为执行所需的关键输出约束，目的是避免“schema 没进上下文就丢掉重要要求”。

顶层输出必须包含：

- `formation_version = "1.0.0"`
- `pass = "knowledge_synthesis"`
- `terms[]`
- `rules[]`
- `cases[]`
- `issues[]`

### Term

Term 至少必须包含：

- `id`
- `statement_ids[]`

只有当概念差异会影响业务判断时才形成 Term。不要为填满 `terms[]` 制造无价值术语。

### Rule

每条 Rule 必须保留现有合同要求的全部字段：

- `id`
- `statement_ids[]`
- `question_ids[]`
- `name`
- `rule_class`
- `impact`
- `scope`
- `preconditions`
- `conditions`
- `result`
- `exceptions`
- `missing_evidence`
- `effective_period`
- `authority`
- `origin`
- `review_status`
- `dispute_status`
- `conflict_ids[]`
- `business_conclusion`
- `required_facts[]`
- `decision_steps[]`
- `evidence_requirements[]`
- `non_sufficient_facts[]`
- `unknown_behavior`
- `human_boundary`
- `case_ids[]`

这些字段不是独立填空题，而是同一个完整业务判断的结构化表达。

先按照前文方法形成业务含义，再映射字段。禁止为了“每个字段都有字”而写同义反复、空泛套话或无来源内容。

`impact=HIGH` 时：

- `required_facts[]` 必须非空；
- `decision_steps[]` 必须非空；
- `evidence_requirements[]` 必须非空；
- `case_ids[]` 必须非空；
- `business_conclusion`、`unknown_behavior`、`human_boundary` 必须表达实际业务语义，不能使用“综合判断”“缺证待核”“必要时人工处理”这类没有说明判断对象和影响的模板句。

如果来源不足以形成某项必要语义：

- 不得编造；
- 应在 Rule 中准确表达 UNKNOWN / 未决影响；
- 必要时写入 `issues[]`；
- 如果缺失来自上游 Statement，应明确要求回到上游补充或修正。

### Case

每个 Case 必须包含：

- `id`
- `question_ids[]`
- `rule_ids[]`
- `case_origin`
- `validation_role`
- `input_facts`
- `expected`
- `forbidden`
- `source_ids[]`
- `reasoning`

其中：

- `case_origin` 只能是 `REAL_CONFIRMED / SOURCE_CASE / SYNTHETIC_PROBE`；
- `validation_role` 只能是 `SUPPORT / COUNTEREXAMPLE / BOUNDARY / MISSING_EVIDENCE`；
- `REAL_CONFIRMED` 必须具有非空 `confirmation_evidence_ids[]`；
- `REAL_CONFIRMED` / `SOURCE_CASE` 必须有真实来源；
- `SYNTHETIC_PROBE` 不得声称真实 source authority；
- Rule 的 `case_ids[]` 与 Case 的 `rule_ids[]` 必须互相一致。

Case 用于检查 Rule 是否能解释现实变化，不得用 Case 自己制造 Rule 的权威性。

### Issues

凡是以下情况不能被可靠合成时，应形成 Issue，而不是静默补齐：

- 来源冲突未解决；
- 关键适用范围不清；
- 关键事实或证据缺失；
- 专家口径尚未确认；
- 机构作业选择尚未确定；
- 当前 Statements 丢失了原文中的必要条件、例外或时间语义。

## 最终质量标准

输出仍然只有现有 Term / Rule / Case / Issue，不另写一份与结构化内容脱节的“业务说明书”。

一个没有参与前期讨论的业务人员，读完 Rule 后，应能够：

1. 指出结论依赖哪些关键事实；
2. 说明这些事实怎样改变、支持或阻断结论；
3. 指出哪些线索单独不足以证明结论；
4. 说明关键证据缺失时，哪些结论仍成立、哪些必须保持 UNKNOWN；
5. 区分规范要求、业务解释和机构作业规则。

如果做不到，即使 schema 校验通过，也视为 Knowledge Synthesis 未完成。
