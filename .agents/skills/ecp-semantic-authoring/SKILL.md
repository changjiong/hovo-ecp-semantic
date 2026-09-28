---
name: ecp-semantic-authoring
description: 将已确认的业务领域模型与真实数据结构共同编制为一个 ECP V3 技术语义模型闭包，覆盖 Ontology、SHACL、V3 Mapping、Derivation、Evaluation、Lifecycle 和 Action Policy，并交付业务模型实现映射、事实绑定、覆盖缺口和候选闭包。用于 ECP 技术语义建模；不重定义业务含义，不把缺失事实当 false，不执行编译、发布或运行。
metadata:
  author: Hovo
  version: "0.3.0"
---

# ECP 语义资产编制

本技能是平台相关建模的唯一入口。原 ecp-data-mapping 的职责并入本技能，不再存在独立 Mapping 阶段。

## 为什么合并

ECP V3 的当前建模顺序是：Ontology/SHACL → Mapping → Derivation/Evaluation/Lifecycle/Action Policy → 不可变 Draft Revision → 跨资产候选编译。V3 Mapping 还通过 ontologySourceDigest 绑定 Ontology 的精确字节，因此 Mapping 不是领域模型之后的独立业务阶段，而是同一技术语义模型闭包的一部分。

合并不取消职责分离。语义实现与数据绑定仍分别审查；只是两者在一个技能、一个版本闭包内迭代，避免用人工阶段边界制造循环交接。

## 输入合同

读取 contracts/input.schema.json、contracts/output.schema.json、references/acceptance.md 和 references/ecp-authoring-kit-1.8/ 下的当前 V3 快照。

必需输入包括：
- 已确认的 domain-model 5.0.0 交付，其中 model_ref 必须指向 business-domain-model/1.0.0；
- Semantic Authoring Kit 1.8 对应的语义 Profile 与目标 Workspace 部署能力回执；
- 真实 Schema 快照、数据源身份和 Schema 依据；
- 业务案例。

没有真实数据结构时，不得虚构 Mapping；没有当前部署能力回执时，不得从目标规范推断目标环境已经实现。

## 执行顺序

1. 固定业务模型版本、模型确认、Kit 1.8、Semantic Profile、目标部署能力回执和案例。
2. 从 business_objects、business_relations 建立 Ontology 与必要 SHACL；稳定 IRI、身份、类型、基数、时间和 UNKNOWN 语义。
3. 立即绑定真实数据结构，生成 ECP_V3_MAPPING。Mapping 必须引用真实数据源、表、列、Record Key、Join、Filter、Projection 与 Coverage；ontologySourceDigest 必须等于当前 Ontology 原始字节摘要。
4. 按 business_decisions 编制有限 Derivation、Evaluation、Lifecycle、Action Policy 或标记 EXTERNAL/UNSUPPORTED。PROFESSIONAL_JUDGMENT 不得伪装成自动规则；MIXED 必须保留人工边界。
5. 将数据缺失、部分读取、拒绝行与上游不确定性显式传播为 UNKNOWN。不得用空结果替代 false。
6. 建立 implementation_map 和 fact_bindings，保证每个业务对象、关系、判断都有实现对应或明确 Gap；数据现状不得反向修改业务模型。
7. 做跨资产静态闭包检查：Ontology/Mapping 字节绑定、六类 SHACL 检查点、依赖顺序、事实覆盖和案例绑定。当前 V3 不生成独立 Scope 资产。
8. 生成 output.json、review.md 和实际技术语义资产。完成后结束；平台原生候选编译、发布、回读和运行由 ecp-semantic-release 负责。

## 审查边界

语义实现负责人确认业务模型被忠实表达；数据负责人确认真实源绑定、身份、Join、空值、时间、覆盖和 UNKNOWN 传播。两份确认都绑定同一 authoring 输出字节，发布阶段缺一不可。

本地 Schema、RDF 或 SHACL 检查只证明有限静态条件。只有目标 Workspace 的 V3 原生候选编译回执才能证明该精确候选被当前部署接受。
