---
name: semantic-foundry
description: 编排从业务材料到领域知识、业务领域模型、ECP V3 技术语义模型闭包和平台发布的四阶段工程。用于跨阶段任务、入口判定、合同检查、责任人确认、依赖追踪和变更退回；单阶段任务交给对应技能，不自行生成或改写阶段资产，不执行未授权平台动作。
metadata:
  author: Hovo
  version: "0.6.0"
---

# Semantic Foundry 语义工程编排

本技能只负责编排，不生产领域知识、业务领域模型或 ECP 技术语义资产。

## 四阶段责任

| 阶段 | 技能 | 核心产物 | 治理闸门 |
| --- | --- | --- | --- |
| 1 | domain-knowledge | 可追溯领域知识、规则、案例、开放问题 | 领域负责人确认知识基线 |
| 2 | domain-model | Business Domain Model：业务对象、关系、判断、外部上下文 | 领域负责人确认业务模型 |
| 3 | ecp-semantic-authoring | Ontology、SHACL、V3 Mapping、Derivation、Evaluation、Lifecycle、Action Policy 与完整闭包 | 语义实现负责人和数据负责人分别确认同一输出 |
| 4 | ecp-semantic-release | 不可变 Revision、V3 候选编译、Release、回读与 Run 证据 | 平台动作需明确授权；业务验收独立 |

原 ecp-data-mapping 已并入第三阶段，不再作为独立生产技能。

## 路由原则

1. 业务材料、法规、案例和专家材料进入 domain-knowledge。
2. 已确认知识进入 domain-model；数据库表、DDL、ECP 算子不得进入该阶段。
3. 已确认业务模型进入 ecp-semantic-authoring；从这一阶段开始允许真实 Schema、数据源身份、目标 ECP Profile 和部署能力回执。
4. authoring 同时完成平台表达和真实数据绑定。语义确认与数据确认是同一阶段的两个责任闸门，不是两个串行模型版本。
5. 双确认后的完整 authoring 闭包进入 ecp-semantic-release。编译失败返回 authoring；若诊断揭示业务含义缺口，再由 authoring 提 CHANGE_REQUEST 返回 domain-model 或 domain-knowledge。
6. 编译、发布、运行和业务验收始终分开取证。

## 上下文隔离

domain-model 只允许业务上下文。ECP 平台能力、物理 Schema 和字段只能从 authoring 开始进入。不得因为数据现状反向改写业务模型。

## 校验

`scripts/validate_pipeline.py --check-schemas` 检查四阶段当前合同；单阶段输入输出仍由对应技能自己的 validate_contract.py 验证。结构检查不等于业务确认、V3 原生编译、发布或运行。
