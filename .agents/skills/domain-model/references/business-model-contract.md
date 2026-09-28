
# model.yaml：业务模型结构

## 顶层

model_version: 1.0.0
artifact_id: ...
content_version: ...
name: ...
domain_name: ...
domain_purpose: ...
knowledge_ref: ...
knowledge_basis: DRAFT | CONFIRMED
scope_mode: FULL_BASELINE | EXPLICIT_SUBSET
question_scope_ids: [...]

business_objects: [...]
business_relations: [...]
business_decisions: [...]
external_contexts: [...]

## business_objects（业务对象）

业务对象必须有：
- 业务名称与定义
- 身份说明
- 参与身份识别的属性
- 例子与反例

属性只能是对象自身标量事实，不允许用 Ref（引用）字段偷偷表达业务关系。对象之间的关联统一放在 business_relations。Knowledge Rule（知识规则）到模型元素的逐项依据不写入 model.yaml，而由 coverage.json 保存。

## business_relations（业务关系）

关系由参与方及其业务角色描述。例如：

participants:
  - role: holder
    label: 权利人
    object_id: NaturalPerson
  - role: subject
    label: 权利所及主体
    object_id: Organization

一个关系可以有多个参与角色。

## business_decisions（业务判断）

不保存可执行 expression（表达式）。

判断只保留：
- business_question
- decision_mode
- inputs
- outcomes
- criteria
- non_sufficient_facts
- unknown_behavior
- evidence_requirements
- human_boundary
- external_context_ids

## external_contexts（外部上下文）

只描述当前领域需要什么外部事实以及由哪个邻接领域提供。

不得在这里复制邻接领域对象、流程或规则。
