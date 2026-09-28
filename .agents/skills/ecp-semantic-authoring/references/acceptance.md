# ECP V3 技术语义模型验收

## 1. 业务忠实性

每个 Business Domain Model（业务领域模型）的 business_object、business_relation、business_decision 必须在 implementation_map 中出现。无法表达时明确 EXTERNAL 或 UNSUPPORTED，并建立 Capability Gap；不得删掉业务承诺来通过平台合同。

PROFESSIONAL_JUDGMENT（专业判断）不得自动化伪装；MIXED（混合判断）必须显式区分机器可判部分和人工边界。unknown_behavior（未知处理）必须被保留。

## 2. 同一模型闭包

当前 V3（第三版）按同一不可变 Draft Revision（草稿修订版本）组装 Ontology、SHACL、Mapping、Derivation、Evaluation、Lifecycle 和 Action Policy。Mapping 的 ontologySourceDigest 必须匹配所选 Ontology 原始字节。修改 Ontology 后必须同步重算并重新检查 Mapping。

独立 Scope（范围）不是当前 V3 原生候选成员，不生成、不迁移、不用旧 Scope Definition V1 伪装。

## 3. 数据绑定

Mapping 只能基于真实 DDL、数据字典或经授权的实时发现。必须核对数据源、表、列类型、Record Key、实体身份、Join、Filter、Projection、NULL 和时间语义。不得根据业务模型猜表字段，也不得因真实数据缺失反向修改业务定义。

FULL_SNAPSHOT coverage（全量快照覆盖）声明缺源、部分读取和拒绝行如何进入对象级 UNKNOWN；它不是完整捕获证明。缺失事实不能归约为 false。

## 4. 平台版本边界

新模型只使用 Semantic Authoring Kit 1.8 和当前 V3 原生格式。旧 Mapping Definition V1、Feature Definition V2、Evaluation Asset V1、Scope Definition V1 不能作为新 V3 候选输入。

随包目标边界与开发能力快照不代表目标 Workspace 已部署同样能力。必须读取目标 Workspace 的真实 deployment_boundary（部署能力回执）。

## 5. 静态检查与原生编译

本技能可做 JSON Schema、RDF/Turtle、标准 SHACL、摘要和跨资产引用的有限静态检查。单项 Draft VALID（有效）不等于整包候选可编译。

authoring 阶段完成条件：
- implementation_map 无遗漏；
- fact_bindings 对所有运行所需事实给出 MAPPED、PARTIAL 或 UNAVAILABLE；
- PARTIAL/UNAVAILABLE 均有 Data Gap；
- Ontology 与 Mapping 摘要一致；
- SHACL 检查点身份明确；
- 资产依赖闭包无悬空；
- 案例 expected/forbidden 未因实现而改写；
- candidate_closure 为 READY，或 BLOCKED 并列明 Gap；
- 语义实现审查与数据绑定审查仍待真实责任人分别确认。

只有 ecp-semantic-release 在目标环境取得的 V3 原生候选编译回执，才能把 platform_compiled 标为 PASS。
