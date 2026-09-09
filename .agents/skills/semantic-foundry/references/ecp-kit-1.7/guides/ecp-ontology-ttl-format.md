# ECP Ontology Turtle 编写指南

文档版本：ECP 有限本体配置 Profile V1

## 权威与范围

导入的 Turtle 原文会保存为不可变 Draft Revision，并在发布后成为 Semantic Release 的语义权威。本系统使用标准 Turtle 解析器，但运行时只承诺支持下面列出的有限 RDFS/OWL 子集。

至少声明一个具名 `owl:Ontology`。Class、Property、domain、range、继承和 inverse 的两端都应使用具名绝对 IRI。

## 保证支持的声明

- `owl:Ontology`、`owl:Class`、`rdfs:Class`
- `owl:ObjectProperty`、`owl:DatatypeProperty`、`owl:AnnotationProperty`
- `rdfs:subClassOf`、`rdfs:subPropertyOf`
- `rdfs:domain`、`rdfs:range`
- `owl:inverseOf`，仅用于两个 Object Property
- `rdfs:label`、`rdfs:comment`、`skos:prefLabel`
- `owl:versionIRI`、`owl:versionInfo`
- `owl:NamedIndividual`

每个 Property 最多声明一个 domain、一个 range 和一个 inverse。Object Property 的 range 必须是已声明 Class；Datatype Property 的 range 只能是 `xsd:string`、`xsd:date`、`xsd:dateTime`、`xsd:gYearMonth`、`xsd:decimal`、`xsd:integer` 或 `xsd:boolean`。同一 `subPropertyOf` 链中的属性类型必须一致。

## 不要使用

下列 OWL/RDFS 特性不属于可保证支持的 Profile：

- `owl:Restriction`、`someValuesFrom`、`allValuesFrom`、基数 Restriction
- `owl:unionOf`、`intersectionOf`、`complementOf`、复杂 Class Expression
- `owl:equivalentClass`、`equivalentProperty`、`sameAs`
- Functional、InverseFunctional、Transitive、Symmetric 等 Property 特征声明
- 裸 `rdf:Property`、`rdfs:Datatype` 和未登记的 OWL/RDFS Schema 构造
- 以空白节点作为 Class、Property、domain、range 或继承端点
- 在 TTL 中嵌入规则脚本、JavaScript、SQL 或 SPARQL

需要必填、数量、数据类型或取值范围约束时，请使用“规则与约束”中的 SHACL 资产。

## 推荐命名与注释

- 使用稳定命名空间，不要把环境名或数据库物理地址写入 IRI。
- 每个 Class 和 Property 都提供中文 `rdfs:label` 与 `rdfs:comment`。
- IRI 是稳定身份；修改 label/comment 不应通过创建新 IRI 完成。
- Mapping 依赖 TTL 原始文本摘要。TTL 保存后应再导入与该摘要绑定的 Mapping JSON。

## 与 Mapping、规则和 Scope 的关系

Ontology只定义业务概念及其可执行语义，不定义“调查哪一个对象、读取哪些表”。对象局部调查使用独立的
`SCOPE` JSON资产；不要在Turtle中增加物理表名、Scan ID、Fact Provider、数据源地址或所谓的“Scope
Class”。新增Scope本身不要求修改Ontology；仅仅启用Scoped Semantic Evaluation也不要求修改现有TTL。

只有业务概念发生变化时才修改Ontology，例如新增Class/Property、调整domain/range、继承或inverse。随后应：

1. 更新引用这些Term的Mapping、SHACL、Derivation和Evaluation；
2. 任何Turtle原文字节变化都重新绑定Mapping的`ontologySourceDigest`，即使只改注释或格式；
3. 仅当Mapping的Scan、Join、Record Key或可达闭包随之变化时，才另建Scope Revision；
4. 通过Release Composer发布新的精确Revision集合，不原地改写既有Published Release。

## 完整示例

```turtle ontology-example
@prefix ex: <urn:example:ontology:> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:customerOntology a owl:Ontology ;
    owl:versionIRI <urn:example:ontology:version:1.0.0> ;
    owl:versionInfo "1.0.0" ;
    rdfs:label "客户本体"@zh-CN ;
    rdfs:comment "客户和负责人的最小示例本体。"@zh-CN .

ex:Party a owl:Class ;
    rdfs:label "参与方"@zh-CN .

ex:Customer a owl:Class ;
    rdfs:subClassOf ex:Party ;
    rdfs:label "客户"@zh-CN ;
    rdfs:comment "接受服务的客户主体。"@zh-CN .

ex:Person a owl:Class ;
    rdfs:subClassOf ex:Party ;
    rdfs:label "自然人"@zh-CN .

ex:customerName a owl:DatatypeProperty ;
    rdfs:domain ex:Customer ;
    rdfs:range xsd:string ;
    rdfs:label "客户名称"@zh-CN ;
    rdfs:comment "客户的标准显示名称。"@zh-CN .

ex:owner a owl:ObjectProperty ;
    rdfs:domain ex:Customer ;
    rdfs:range ex:Person ;
    owl:inverseOf ex:ownsCustomer ;
    rdfs:label "负责人"@zh-CN .

ex:ownsCustomer a owl:ObjectProperty ;
    rdfs:domain ex:Person ;
    rdfs:range ex:Customer ;
    owl:inverseOf ex:owner ;
    rdfs:label "负责客户"@zh-CN .
```

## 导入检查

系统会依次执行 Turtle 语法解析、Projection 编译、有限语义 Profile 校验以及与 Mapping/规则候选的兼容性检查。语法可解析不代表一定属于受支持的运行 Profile。
