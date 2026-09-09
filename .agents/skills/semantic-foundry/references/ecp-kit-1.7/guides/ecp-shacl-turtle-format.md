# ECP SHACL Turtle 编写指南

文档版本：ECP SHACL Core Profile V1

## 执行边界

SHACL 资产使用 Turtle，发布时由 `rdf-validate-shacl` Core Profile 校验，推理模式为 `none`。一个完整 Release 必须按系统要求绑定六个 SHACL Stage；使用完整规则集 ZIP 导入时，Stage 由 `manifest.json` 的 `shaclStage` 确定并写入当前 Draft，发布面板会自动带入并冻结该绑定，不写入 Shape 文本。

## 保证支持

- `sh:NodeShape` 与 `sh:PropertyShape`
- 显式目标：`sh:targetClass`、`sh:targetNode`、`sh:targetSubjectsOf`、`sh:targetObjectsOf`
- `sh:property` 引用具名或空白 Property Shape
- 每个 Property Shape 恰好一个 `sh:path`，且 path 必须是直接 IRI
- 13 个约束组件：`sh:minCount`、`sh:maxCount`、`sh:datatype`、`sh:nodeKind`、`sh:class`、`sh:minInclusive`、`sh:maxInclusive`、`sh:pattern`、`sh:in`、`sh:hasValue`、`sh:or`、`sh:and`、`sh:not`
- `sh:in`、`sh:or`、`sh:and` 使用有限、无环且结构正确的 RDF List
- 严重级别：`sh:Violation`、`sh:Warning`、`sh:Info`
- `sh:message`，推荐提供中文文本

`sh:Violation` 会阻止对应门禁；Warning 和 Info 会进入报告但不作为致命失败。

## 不支持

- SHACL-SPARQL：`sh:sparql`、`sh:select`、`sh:ask`
- SHACL-JS：`sh:js`、`sh:jsFunctionName`、`sh:jsLibrary`
- Sequence、Alternative、Inverse、Zero-or-more 等复杂 Property Path
- `sh:minLength`、`sh:maxLength`、`sh:flags` 及其他未列出的 Constraint Component
- `sh:name`、`sh:description` 及其他未登记的 `sh:` Predicate
- 没有任何受支持 target 的 Node Shape
- 循环或不完整 RDF List
- 从数据库加载 SQL、JavaScript 或外部回调

## 示例

```turtle shacl-example
@prefix ex: <urn:example:ontology:> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:CustomerShape a sh:NodeShape ;
    sh:targetClass ex:Customer ;
    sh:severity sh:Violation ;
    sh:property [
        sh:path ex:customerName ;
        sh:datatype xsd:string ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:pattern ".+" ;
        sh:message "客户名称必须存在且只能有一个值。"@zh-CN
    ] .
```

## 建议

- Shape IRI 和业务 Property IRI 保持稳定。
- 每条约束只表达一个清晰意图，避免一个巨大 Shape 承担所有校验。
- Shape 引用的 Class 和 Property 必须存在于同一候选 Release 的 Ontology 中。
- Shape 必须与同一候选 Release 的 Mapping 输出合同一致：Mapping 使用 `nullPolicy: OMIT` 时不能把同一 Predicate 设为 `sh:minCount > 0`；允许多值时不能设 `sh:maxCount <= 1`；`sh:datatype` 必须与 Mapping `datatypeIri` 相同。候选审查和正式发布会静态拒绝这些矛盾。
- 保存前使用“只预检”，发布前再通过整体候选编译确认导入的 Stage 完整性。对旧的未标注 SHACL Draft，应重新导入完整规则集 ZIP，而不是逐次发布时手工猜测阶段。
- 同一套六阶段Shape同时用于完整Run和Scoped Evaluation；Scope不会覆盖、放宽或替换SHACL约束。
- 局部事实闭包不完整时应由Fact Provider/Scope完整性门禁失败关闭，不能用Shape把缺失事实解释为通过。
