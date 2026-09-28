# 模型评审与线下回路

review_mode 只管理模型评审组织方式；knowledge_basis 管理采用的领域知识依据，两者独立。

## 会话评审

IN_SESSION 时先展示 review.md：业务对象、业务关系、业务判断和外部上下文边界。

业务人员不需要审查 YAML 结构或技术 ID，而是确认：
- 对象是不是业务里真实存在的东西；
- 两个对象之间的关系方向和含义是否正确；
- 是否有过度抽象导致非法业务组合；
- 判断输入、结果、UNKNOWN、非充分事实和人工边界是否正确；
- 外部上下文是否越界。

## 线下评审

DEFERRED 时交付：
- model.yaml
- coverage.json
- review.md
- coverage.md
- output.json

业务人员主要评审 review.md。coverage.md 供建模和审计人员检查知识承接，不要求业务人员逐项编辑。

收回反馈后，若只是模型抽象错误，进入 REVISE（修订）；若反馈改变了业务规则本身，应退回 domain-knowledge（领域知识形成）产生新知识版本。

## 确认边界

作者自查、Schema（模式）校验、生成器 PASS、Case（案例）静态解释都不是业务确认。

正式确认应绑定当前：
- model.yaml
- coverage.json
- review.md
- coverage.md
- output.json

旧版本确认不自动继承。

## OPEN 与反馈

如果反馈补充的是核心业务定义、关系或判断，修正模型或上游知识。

如果反馈只涉及机构岗位、报告流程、数据接口或邻接风险治理，不应为了“解决反馈”把它们扩张进核心 Domain Model（领域模型）。

只有直接阻止核心业务模型确定的 OPEN 才进入 MODEL_GAP。
