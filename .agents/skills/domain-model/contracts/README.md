
# Business Domain Model（业务领域模型）合同

当前：
- Skill（技能）版本：1.0.0
- Input / Output Handoff（输入/输出交接）合同：5.0.0
- Business Domain Model（业务领域模型）合同：1.0.0
- Coverage（覆盖审计）合同：1.0.0
- Domain Knowledge（领域知识）输入合同：5.0.0

## 正式产物

input.json

model.yaml
  → 纯业务模型

coverage.json
  → 知识覆盖与审计

review.md
  → 从 model.yaml 生成

coverage.md
  → 从 coverage.json 生成

output.json
  → 交接引用

model.yaml 使用 contracts/business-domain-model.schema.json。

coverage.json 使用 contracts/coverage.schema.json。

output.json 的 content 必须包含：
- model_ref：business-domain-model/1.0.0
- coverage_ref：domain-model-coverage/1.0.0
- request_ref：5.0.0

## Breaking Change（破坏性变更）

1.0.0 不兼容 Domain DSL 2.x。

以下构造从核心模型合同中删除：
- types
- rules
- judgments
- constraints
- state_machines
- processes
- question_coverage
- case_explanations
- upstream_issue_bindings
- issues
- rule_coverage
- expression / operator / evaluate

覆盖和审计语义迁移到 coverage.json；执行语义不再属于 domain-model 阶段。

不提供旧 DSL 迁移或兼容层。旧模型只作历史归档，新的业务模型必须从固定 Domain Knowledge 重新 PRODUCE（创建）。
