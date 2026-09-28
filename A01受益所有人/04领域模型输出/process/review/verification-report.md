# A01 Business Domain Model 1.0.0 交付审阅记录

模型版本：`2026-09-28.business-v1.0.0.draft.1`  
知识版本：`A01.DomainKnowledge / 2026-09-24.draft.1 / 5.0.0`  
生成模式：`PRODUCE + FULL_BASELINE + DRAFT`

本版按 `domain-model 1.0.0` 从固定 Domain Knowledge（领域知识）全量重新抽象。旧 0.9.x model / coverage / builder 已归档，不作为本次语义来源。

## 业务模型规模

| 项目 | 数量 |
| --- | ---: |
| 业务对象 | 7 |
| 业务关系 | 23 |
| 业务判断 | 22 |
| 外部上下文 | 4 |
| Knowledge Rule | 27 |
| Question | 85 |
| Case | 36 |
| 上游 OPEN | 44 |
| 核心 MODEL_GAP | 3 |

业务对象为：自然人、组织主体、分支机构、信托、资产管理产品、识别证据、受益所有人识别结果。

## 规则处理

27 条 Knowledge Rule 均进入建模范围审计：

- MODELED：15
- PARTIAL：3
- EXTERNAL_CONTEXT：6
- NO_MODEL_CHANGE：3

建模分类允许组合，统计为：

- CORE_STRUCTURE：15
- DOMAIN_DECISION：18
- EXTERNAL_CONTEXT：14
- NO_MODEL_CHANGE：3

## 上游 OPEN 去向

44 个上游 OPEN 未被机械升级为 MODEL_GAP：

- CORE_MODEL_GAP：1
- EXTERNAL_CONTEXT_OPEN：13
- NO_MODEL_IMPACT：30

当前 3 个真正核心语义缺口：

1. `GAP.A01.StateControlScope`：国资相对控股/“国有实际控制企业”与 UBO 特例边界仍需权威口径和个案证据。
2. `GAP.A01.TrustSimplifiedPersonSemantics`：部分其他资产服务信托“可以简化”，但固定知识未给统一的简化后替代自然人人选。
3. `GAP.A01.OtherProductSimplifiedPersonSemantics`：部分低风险年金/其他产品“可以简化”，但固定知识未给所有类别统一的简化后自然人人选。

后两项是本次业务建模主动发现的知识语义缺口；模型没有自行猜测人选。

## 本次静态审计

已对当前分支字节执行结构/引用/覆盖/摘要一致性审计，结果 PASS：

- 业务对象、关系、判断、外部上下文 ID 全局唯一；
- 对象 identity_attributes 均存在；
- 关系参与对象均已定义，关系角色/属性无重复；
- 22 个业务判断的全部输入引用均可解析；
- 外部上下文引用的业务判断均存在；
- 业务判断依赖图无循环；
- 27 条 Rule 覆盖与固定知识精确一致；
- 85 个 Question 覆盖与固定知识精确一致；
- 36 个 Case 覆盖与固定知识精确一致；
- Case 的 expected / forbidden 未被改写；
- 44 个上游 OPEN 均有且只有一个去向；
- 非核心 OPEN 没有绑定 MODEL_GAP；
- Rule / Question / Case 的模型引用均无悬空；
- Rule 七要素 source_text 与固定知识原文一致；
- input / model / coverage / review / coverage view 的 SHA-256 与 output.json 引用一致；
- output.json 中的 MODEL_GAP 与 coverage.json 精确一致。

## 验证边界

当前会话未实际运行仓库 Python 命令，因此不把 `self_test.py`、JSON Schema 或 handoff validator 标为已执行。

合并前建议本地运行：

```bash
python .agents/skills/domain-model/scripts/self_test.py

python .agents/skills/domain-model/scripts/validate_contract.py --check-schemas

python .agents/skills/domain-model/scripts/domain_model.py validate   A01受益所有人/04领域模型输出/model.yaml

python .agents/skills/domain-model/scripts/domain_model.py validate-coverage   A01受益所有人/04领域模型输出/coverage.json   --model A01受益所有人/04领域模型输出/model.yaml

python .agents/skills/domain-model/scripts/validate_contract.py validate input   A01受益所有人/04领域模型输出/input.json   --project-root .

python .agents/skills/domain-model/scripts/validate_contract.py validate output   A01受益所有人/04领域模型输出/output.json   --project-root .
```

结构一致性 PASS 不等于业务专家已确认。当前 `business_reviewed=NOT_EXECUTED`、`confirmation=PENDING`。
