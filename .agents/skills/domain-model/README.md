# domain-model

把固定版本 Domain Knowledge（领域知识）抽象为平台无关的 Domain Model（领域模型）：**稳定业务结构 + 稳定领域判断**。

Hovo 0.9.0 开发候选包 · 模型合同 5.0.0 · DSL 2.1.0 · 上游知识合同 5.0.0。

核心边界：

```text
Domain Knowledge（领域知识）
业务是什么、怎么判断
        ↓
Domain Model（领域模型）
稳定对象/关系/事实/时间 + 稳定领域判断
        ↓
ECP Semantic Authoring（ECP语义资产编制）
平台可计算/执行资产
```

本技能不重新读取原始制度，不设计数据库，不复制全部知识规则，不强迫每条 Rule（规则）产生模型元素，也不以 Process（流程）、StateMachine（状态机）或本地可执行性证明模型完整。

## 使用

先读：

1. [SKILL.md](SKILL.md)
2. [Knowledge → Domain Model 提示词](prompts/01-knowledge-to-domain-model.md)
3. [业务建模方法](references/business-modeling.md)
4. [Domain DSL](references/domain-dsl.md)

验证：

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python scripts/validate_contract.py --check-schemas
.venv/bin/python scripts/domain_dsl.py validate /project/domain-model/model.yaml
.venv/bin/python scripts/deliver_model.py /project/domain-model/model.yaml \
  --request /project/domain-model/input.json \
  --output-dir /project/domain-model \
  --project-root /project
```

`evaluate（求值）` 仅用于有限验证，不是领域模型完成条件。

## 0.9.0 收敛

- Rule Coverage（规则覆盖）先分类为 CORE_STRUCTURE / DOMAIN_DECISION / EXTERNAL_CONTEXT / NO_MODEL_CHANGE；
- 正确的“无模型变化”成为合法结果；
- Process（流程）由必选变为可选；
- 领域规则保留为 Domain Decision（领域判断），不扩张成生产执行规则；
- review.md 优先展示业务结构与领域判断。
