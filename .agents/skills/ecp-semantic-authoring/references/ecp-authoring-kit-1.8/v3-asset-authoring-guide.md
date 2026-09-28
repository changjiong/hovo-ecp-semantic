# ECP V3 语义资产编写指南

文档状态：当前 V3 建模入口
最后核验日期：2026-09-28

本指南只说明 ECP 宿主如何向独立 `semantic-execution-engine` 提交资产。语义含义以工具包内从引擎原文同步的 `engine/docs/standards/semantic-profile.md` 为准；`contracts/deployed-v3-semantic-boundary.json` 是下载时从当前 Workspace 的真实 V3 Service 读取的能力回执。目标边界、开发仓库能力和当前部署能力不可混为一谈。编译通过只证明这个候选被该原生制品接受，不证明源数据完整、运行质量或发布许可。

## 建模与验证顺序

1. 先读引擎语义规范和当前部署能力回执，选择已实现的有限构造；不要从目标合同推断可执行能力。
2. 编写 Ontology Turtle 与 SHACL Turtle。SHACL 的 `asserted`、`domain`、`feature`、`change`、`output`、`provenance` 是不同检查点，随资产会员身份明确声明。
3. 编写 V3 Mapping；`ontologySourceDigest` 必须匹配选定 Ontology 原始字节。按 `contracts/v3-mapping-definition.schema.json` 检查顶层结构，并核对 Hovo 的真实 Scan、列类型及 Record Key。
4. 编写有限 Derivation；需要求值时再添加 V3 Evaluation Module。Lifecycle 和 Action Policy 按各自 V3 Schema 与发布上下文编写。
5. 保存不可变 Draft Revision，选择精确 Revision 执行“V3 编译候选”。逐资产拒绝和跨资产拒绝必须处理完毕，再审查和发布。单项 Draft 的 `VALID` 不代表整包编译成功。

工具包内 `examples/business-context-v1/` 是从独立引擎原样同步的通用参考模型：Ontology、Mapping、Derivation 和两个 SHACL 检查点已由引擎真实进程测试使用。例中的 `test` 数据源、IRI 和摘要属于示例；改动 Ontology 字节后要重算 Mapping 的 `ontologySourceDigest`，并用目标部署原生编译重新验证。示例不是 ECP 内置业务模型。

## V3 JSON 资产格式

| 资产 | 当前 V3 原生编译入口 | 不应当作 V3 输入的旧格式 |
| --- | --- | --- |
| Mapping | `schemaVersion: 1`、`kind: ECP_V3_MAPPING`，包含 `dataSources`、`scans`、`projections`；可声明有限 `joins`、`filters` 与 `coverage` | Mapping Definition V1 的 `entities`、独立 `properties`／`relationships` 根数组 |
| Derivation | `schemaVersion: 1`、`profileId: ecp-declarative-derivation/1.0.0` 的单一 Profile，或显式排序的 `ECP_V3_DERIVATION_MODULE`，其中 `profile` 使用同一 Profile | `enterprise-cognitive/feature-definition/v2` |
| Evaluation | `schemaVersion: 1`、`kind: ECP_V3_EVALUATION_MODULE`，`profile.profileId: ecp-scoped-evaluation/1.0.0`；每个阶段的操作必须是 `SCOPED_DECISION` | `enterprise-cognitive/evaluation-asset/v1` 和旧 Definition V1 |
| Lifecycle | `kind: ECP_V3_LIFECYCLE_BINDING`；使用工具包内 V3 Schema | 旧生命周期定义 |
| Action Policy | `kind: ECP_V3_ACTION_POLICY`；使用工具包内 V3 Schema。引擎将它绑定进模型身份，意图与投递由宿主负责 | 过渡期 Action Policy V1 |
| Scope | 当前原生模型组装不接受独立 `SCOPE` 资产 | `enterprise-cognitive/scope-definition/v1` 即使单项预检为 `VALID` 也不能发布为 V3 候选 |

Derivation Profile 的阶段使用 `query.bindings`、`query.patterns` 和有限 `operation`；列序号按该查询的绑定顺序解释。多个 Derivation Module 的 `after` 必须形成唯一顺序；资产列表顺序或名称不能代替依赖声明。Evaluation Module 与派生阶段共用有限表达式与 RDF Term 结构，但只允许 `SCOPED_DECISION`，必须明确 `scope`、键列、`emptyInput` 和 MATCH／NO_MATCH／UNKNOWN 三类输出。没有命中的结果不能自动解释为 false。工具包中的 `examples/v3-evaluation-module.json` 给出可用的完整包络和阶段结构。

Mapping 的 `coverage` 声明缺源、部分读取及拒绝行如何变为对象级 UNKNOWN；它不是完整捕获证明。数据源只写 Hovo 逻辑引用，不写连接参数、SQL、密钥或回调。有限算子、精确数值和输入资源边界以引擎 Profile、实际能力回执和当前原生编译结果为准。

## 旧 Admin 材料的适用边界

下载中心仍单独提供旧 Mapping、Feature、Evaluation、Scope、Rule Set ZIP、Workspace Package 与完整替换指南，供既有 Draft 导入和审查。这些格式不自动转换为 V3 资产，也不因为旧 JSON Schema 校验通过就可发布。AI 建立新的 V3 模型时，应先使用本指南、随包的 V3 Schema／通用示例和目标部署能力回执；不要将旧版 `ecp-semantic-profile-1.0.json` 当作运行时语义标准。
