
# domain-model

从固定 Domain Knowledge（领域知识）生成纯业务视角 Domain Model（领域模型）。

Hovo 1.0.0 · Business Domain Model contract（业务领域模型合同）1.0.0 · Coverage contract（覆盖合同）1.0.0 · 上游知识合同 5.0.0。

## 核心变化

Domain Knowledge（领域知识）
    ↓
Business Domain Model（业务领域模型）
    ├─ 业务对象
    ├─ 业务关系
    ├─ 业务判断
    └─ 外部上下文
    ↓
ECP Semantic Authoring（ECP语义资产编制）

model.yaml 不再是 DSL（领域专用语言），不包含 Process（流程）、StateMachine（状态机）、Expression（表达式）、Coverage（覆盖）或审计信息。

覆盖与审计独立放在 coverage.json。

## 使用

先读：
1. SKILL.md
2. prompts/01-knowledge-to-domain-model.md
3. references/business-modeling.md
4. references/business-model-contract.md

验证命令：

    python scripts/self_test.py
    python scripts/domain_model.py validate /project/domain-model/model.yaml
    python scripts/domain_model.py validate-coverage /project/domain-model/coverage.json
    python scripts/validate_contract.py --check-schemas
    python scripts/deliver_model.py /project/domain-model/model.yaml       --coverage /project/domain-model/coverage.json       --request /project/domain-model/input.json       --output-dir /project/domain-model       --project-root /project

1.0.0 是破坏性版本，不兼容旧 Domain DSL 2.x，不提供迁移层。旧模型归档后必须从固定 Domain Knowledge 重新 PRODUCE（创建）。
