# ECP 语义资产编写与选择手册

本文件只总结如何选择资产和保持跨资产一致性。正式边界仍以 `ecp-kit-1.7/` 原始规范为准。

## 1. 资产选择矩阵

| 需求 | 资产 | 何时不应生成 |
|---|---|---|
| 定义 Class、Property、继承、domain/range、inverse | `ONTOLOGY` | 仅仅是数据质量、计算或流程需求时 |
| 将 MySQL/OceanBase 表实例化为本体对象 | `MAPPING` | 没有可靠物理 Schema 或只是概念设计时 |
| 对 asserted/domain/feature/change/output/provenance 做封闭世界约束 | `SHACL` | 没有任何约束需求且当前 Release 仅用于编译审查时 |
| 从事实确定性地产生派生事实/Feature | `DERIVATION` | 只是概念关系，或需要 ECP 未登记任意函数时 |
| 对对象执行条件判断、产生 Candidate/结果和证据投影 | `EVALUATION` | 只是派生属性，不需要对象级求值时 |
| 已提交语义变化触发外部有限 Capability Intent | `ACTION_POLICY` | 普通工作流编排、直接写 HTTP、需要凭据时 |
| 从一个 Root 读取完整局部关系型事实闭包 | `SCOPE` | 全量 Run，或只是 Evaluation objectScope 时 |
| 原子替换全部规则 Draft Head | Rule Set Bundle | 只编辑一条规则时 |
| 跨页面交换完整语义工作目录 | Workspace Package | 单一 Ontology/Mapping/规则编辑时 |

## 2. Ontology

硬规则：

- 至少一个具名 `owl:Ontology`；
- Class/Property/Schema 两端都是具名绝对 IRI；
- 每个 Property 最多一个 domain、range、inverse；
- Datatype Property range 只用 Profile 列出的 7 种 XSD 类型；
- 中文 label/comment 推荐完整；
- IRI 不包含环境名、数据库物理地址或临时版本后缀；
- 不在 TTL 中写 Scope、表名、Scan ID、SQL、规则脚本或凭据。

明确拒绝：匿名 `owl:Restriction`；`owl:equivalentClass` / `owl:equivalentProperty` / `owl:sameAs`；union/intersection/complement；Property Chain、Transitive、Symmetric、Functional 等属性特征；OWL Cardinality、Key、Disjointness、Imports；任意未登记 Schema 构造。

## 3. Mapping

生成 Mapping 前必须拿到真实 Schema 或可靠 Schema 快照。

顺序：
1. Scan + columns + Record Key；
2. 同一数据源内受控 INNER/LEFT 等值 Join；
3. Entity + Class + IRI identity；
4. Datatype Property；
5. Object Property Relationship；
6. Filter；
7. Coverage。

硬规则：`ontologySourceDigest` 绑定最终 TTL 原始字节；不生成任意 SQL；复杂逻辑由上游治理 View 提供；Property datatype 必须与 Ontology Range 一致；Relationship domain/range 必须与 Ontology 一致；每个 Entity 必须有 Coverage Requirement；NULL、Cardinality、Datatype 不得与 SHACL 冲突。

## 4. SHACL

如果可执行 Release 含任意 SHACL，必须完整提供并唯一绑定：`asserted`、`domain`、`feature`、`change`、`output`、`provenance`。

只使用 Profile 保证的 `sh:NodeShape` / `sh:PropertyShape`、4 类 Target、直接 IRI `sh:path`、13 个 Constraint Component、`Violation/Warning/Info`。不使用 SHACL-SPARQL、SHACL-JS、复杂 Path、未登记 `sh:` Predicate。

## 5. Derivation

用途：把已提交事实转换为新的派生断言。

硬规则：`FeatureDefinition v2`；有限 Typed Operator；DAG 无环；所有 IRI 来自候选 Ontology 或允许的输出声明；缺失输入传播 Coverage/UNKNOWN，不制造默认事实；图上比例连乘使用版本化 `WeightedTransitiveClosure`，且必须设置单 Root 和跨 Root 预算；不把最终业务阈值和结论塞进 `WeightedTransitiveClosure`；不写 Root Record Key、Fact Provider、物理表或 Scope 预算。

## 6. Evaluation

用途：对象级条件与 Candidate 输出计划。

硬规则：有限 Typed Plan；`clockBasis`、Coverage、objectScope、identity、projection、evidence、trace 明确；`compilerContract.expect` 是 ECP 编译器权威结果，不得从自然语言猜测。

如果没有真实 ECP “只预检”或编译器输出：可以生成 Definition 设计草稿；文件名明确包含 `.draft`；报告状态为 `ECP_PREFLIGHT_REQUIRED`；不把该草稿登记进最终 Rule Set Manifest；不声称可导入、可发布。

## 7. Action Policy

只声明 Trigger、Capability IRI、Operation、`executorBindingRef`、有限 Argument Source。禁止 URL、Header、Token、密码、Bucket、本地路径、重试脚本、任意代码。

## 8. Scope

Scope 负责关系型局部事实选择，不属于 Ontology，也不能替代 Evaluation `objectScope`。

硬规则：精确绑定 Mapping ID/version；Root keyColumns 与 Scan recordKey 完全一致；requiredScanIds 覆盖全部 Mapping Scan；joinIds 覆盖全部 Mapping Join；Root Binding 是闭包内每条已选 Root 行上的双向等值边；Full Scan 只用于小型治理参考表；所有资源上限命中时失败关闭；Fact Provider 只使用逻辑引用，不写 Endpoint/Token。

## 9. Rule Set Bundle

Manifest 必须闭合；成员路径和 `sourceDigest` 与原始 UTF-8 字节完全一致；如果有 SHACL，六阶段各且仅一个；ZIP 中不得有 Manifest 未登记业务文件；Full Replacement 导入会让候选 Draft Head 中遗漏的旧规则退出当前候选集合，必须显式提醒。

## 10. Workspace Package

正式目录：

```text
manifest.json
ontology/<model>.ttl
mapping/<mapping>.json
rules/manifest.json
rules/shacl/<stage>.ttl
rules/derivation/<rule>.json
rules/evaluation/<rule>.json
rules/action-policy/<policy>.json
scopes/<scope>.json              # 仅 V2
data-sources/<source>/schema.json
```

- 无 Scope：V1；
- 有 Scope：V2；
- Manifest 摘要是字节完整性证明，不是语义正确性证明；
- 包中 Schema 快照只用于审阅，不能替代 Hovo 当前 Schema 发现和运行期 Snapshot 漂移检查。

## 11. 跨资产依赖顺序

```text
Ontology
  ↓
Mapping
  ↓
SHACL / Derivation / Evaluation
  ↓
Action Policy / Scope
  ↓
Rule Set Manifest
  ↓
Workspace Manifest
```

任何上游 IRI、Source Digest、Mapping ID/version、Scan/Join 拓扑变化，都必须检查全部下游引用；不要添加兼容 fallback。
