# ECP Semantic Profile 1.0

文档状态：当前规范说明

日期：2026-08-14

## 1. 目的与符合性声明

`ECP Semantic Profile 1.0`定义Enterprise Cognitive Platform当前保证的RDF、有限蕴含和SHACL执行边界。它是生产Runtime的版本化语义合同，不是第三方库能力清单，也不宣称ECP是通用RDF数据库、SPARQL引擎、完整RDFS实现或OWL 2推理器。

一个Runtime只有同时满足以下条件，才符合本Profile：

1. 接受并按本文语义执行所有受支持构造；
2. 在不可变Semantic Release发布前拒绝所有未支持的标准语义构造；
3. 对本文有限蕴含规则计算最小不动点；
4. 在相同Release、Snapshot与Execution Closure下产生逐字节确定的Graph、Report和身份；
5. 把Profile ID、Profile Digest、Runtime ABI、Runtime Artifact及依赖锁纳入可审计运行身份。

本文使用`MUST`、`MUST NOT`、`SHOULD`和`MAY`表达规范要求。实现中的机器可读权威是[`ECP_SEMANTIC_PROFILE_MANIFEST`](../packages/ontology-engine/src/semantic-profile.ts)。本文与Manifest发生漂移时质量门禁必须失败。

本文是ECP语义能力的总规范，不替代面向具体资产的编写指南。Ontology、Mapping、SHACL、Derivation、Evaluation和Action Policy的页面内指南负责给出可直接编写的格式与示例；Profile Manifest、JSON Schema和编译器断言负责机器校验。三层材料由管理端“文档中心”和“下载中心”统一分发。

## 2. Profile身份

| 层次 | 身份 |
|---|---|
| 组合Profile | `enterprise-cognitive/semantic-profile/1.0.0` |
| RDF Runtime | `enterprise-cognitive/rdf-runtime-profile/1.0.0` |
| 有限蕴含 | `enterprise-cognitive/rdfs-plus-entailment/1.0.0` |
| SHACL Core子集 | `enterprise-cognitive/shacl-core-profile/1.0.0` |

Profile Manifest使用`ecp-semantic-profile-manifest-v1`计算内容摘要。任何改变已接受输入、推理结果、验证结果或失败顺序的修改都MUST发布新Profile身份和新Runtime ABI，不能在既有身份下静默改变语义。

历史`er-entailment-v1`只用于冻结Golden与Archived Runtime重放，不是新运行的当前语义声明。

## 3. RDF Runtime Profile

### 3.1 输入和图

- Ontology和SHACL语义资产使用标准Turtle；
- Runtime Assertion的Subject和Predicate MUST是Named IRI；
- Runtime Object只能是Named IRI或第3.2节列出的Literal；
- Runtime Data MUST NOT包含Blank Node、Variable、Default Graph或RDF-star Term；
- Runtime只使用`asserted`、`entailed`、`derived`、`change`和`output`五个固定Named Graph；
- Ontology/Shape源中的Turtle Blank Node不自动成为Runtime Blank Node。Ontology Profile禁止Blank Node；SHACL仅在Shape结构和RDF List中受控使用Blank Node。

ECP的Canonical N-Quads是项目确定性投影，不是通用RDF Dataset Canonicalization实现。若未来允许Runtime Blank Node或RDF-star，必须发布新Profile和身份协议。

### 3.2 Runtime Object类型

| Object kind | RDF datatype或Term | ECP约束 |
|---|---|---|
| `iri` | Named IRI | 仅合法绝对HTTP、HTTPS或URN IRI |
| `string` | `xsd:string` | Unicode NFC |
| `date` | `xsd:date` | `YYYY-MM-DD`有效日期子集 |
| `dateTime` | `xsd:dateTime` | 最多6位小数秒；时区绝对值最大`14:00` |
| `yearMonth` | `xsd:gYearMonth` | `YYYY-MM`子集 |
| `decimal` | `xsd:decimal` | 进入RDF前按28位`ROUND_HALF_EVEN`业务Decimal Context量化 |
| `integer` | `xsd:integer` | 任意精度，输入不能经过JavaScript `number` |
| `boolean` | `xsd:boolean` | 规范输出`true`或`false` |
| `langString` | `rdf:langString` | `Intl.getCanonicalLocales`接受的结构化BCP 47标签，并转为小写 |

除明确记录的Decimal量化外，Runtime MUST NOT静默改变输入RDF值。超过6位的`dateTime`小数秒必须失败，不能截断。

### 3.3 IRI和兼容缩写

RDF身份始终使用展开后的绝对IRI。`er:`及历史实体缩写只是Wire兼容输入/显示形式，不是额外RDF Term类型。新领域语义SHOULD在Published Mapping中产生绝对IRI。

## 4. Ontology Profile

### 4.1 受支持声明

Ontology MUST声明至少一个Named `owl:Ontology`。Profile支持以下Named声明：

- `owl:Class`和`rdfs:Class`；
- `owl:ObjectProperty`；
- `owl:DatatypeProperty`；
- `owl:AnnotationProperty`，仅用于明确允许的无推理元数据；
- `owl:NamedIndividual`以及以已声明领域Class为`rdf:type`的Named Individual。

Ontology中的Subject、Schema Predicate参数和Class/Property引用MUST使用Named IRI。Ontology Blank Node一律拒绝，以避免把未实现的匿名OWL Class Expression误当作已支持语义。

### 4.2 受支持Schema谓词

| 谓词 | 语义 |
|---|---|
| `rdfs:subClassOf` | Named Class层级，可多继承和成环 |
| `rdfs:subPropertyOf` | 同种Object或Datatype Property层级，可多继承和成环 |
| `rdfs:domain` | Property Subject类型蕴含 |
| `rdfs:range` | Object Property Object类型蕴含；Datatype Property词法/Mapping检查 |
| `owl:inverseOf` | Object Property之间对称的逆属性关系 |

每个Property至多声明一个`rdfs:domain`、一个`rdfs:range`和一个`owl:inverseOf`。多Domain/Range/Inverse虽然可由更广标准表达，但不属于本Profile。多`subClassOf`和多`subPropertyOf`受支持。

Datatype Property的Range只能是：`xsd:string`、`xsd:date`、`xsd:dateTime`、`xsd:gYearMonth`、`xsd:decimal`、`xsd:integer`或`xsd:boolean`。

### 4.3 元数据

`rdfs:label`、`rdfs:comment`、`skos:prefLabel`、`owl:versionIRI`和`owl:versionInfo`可作为元数据使用，不产生蕴含。声明为`owl:AnnotationProperty`的项目属性也只能产生无执行效果的元数据。实现MUST区分“接受但无执行效果”和“支持语义”。

### 4.4 明确拒绝

本Profile拒绝但不限于：OWL匿名Restriction、交集、并集、补集和枚举Class Expression；`owl:equivalentClass`、`owl:equivalentProperty`、`owl:sameAs`和`owl:differentFrom`；Transitive、Symmetric、Functional、InverseFunctional和Property Chain公理；Cardinality、Key、Negative Property Assertion、Disjointness和Imports；`rdfs:Datatype`、Container语义、RDFS公理Triple和完整Datatype Entailment；未声明Term或不同Property Kind之间的`subPropertyOf`；任意未登记的OWL/RDFS语义构造。

## 5. 有限RDFS-Plus蕴含

### 5.1 规则

ECP只物化ABox结果，不输出推导后的Schema公理。`subClassOf*`和`subPropertyOf*`表示含自身的传递闭包。

```text
TYPE
  x rdf:type C, C subClassOf* D
  => x rdf:type D

SUBPROPERTY
  x p y, p subPropertyOf* q
  => x q y

DOMAIN
  x p y, p subPropertyOf* q, q rdfs:domain C, C subClassOf* D
  => x rdf:type C and x rdf:type D

RANGE
  x p y, p subPropertyOf* q, q is ObjectProperty,
  q rdfs:range C, C subClassOf* D
  => y rdf:type C and y rdf:type D

INVERSE
  x p y, p owl:inverseOf q
  => y q x
```

`owl:inverseOf`公理本身按对称关系解释。由INVERSE产生的Property Assertion必须继续参与SUBPROPERTY、DOMAIN、RANGE和INVERSE，直到没有新Triple为止。

### 5.2 闭包与支持

- Entailment读取`asserted`和`derived`来源Assertion；
- 结果写入`entailed`；
- 算法MUST计算有限最小不动点，并在Hierarchy或Inverse环中终止；
- 输入顺序、Ontology Triple顺序和重复推导路径不得改变结果；
- 每个结果绑定触发闭包的来源Assertion ID；Schema依据由Ontology Revision和Profile Digest绑定；
- 同一来源和同一结果只产生一个确定Entailed Assertion；
- Domain/Range是类型蕴含，不是必填字段验证或封闭世界约束。

本Profile不执行一致性、可满足性、OWL分类或Realization，也不声称符合OWL 2 EL、QL、RL或DL。

## 6. SHACL Core项目Profile

### 6.1 Target、Path和Constraint

支持Target：`sh:targetClass`、`sh:targetNode`、`sh:targetSubjectsOf`、`sh:targetObjectsOf`。

本Profile的四类Target参数都必须是Named IRI；不接受Literal或Blank Node作为显式Target参数。

Property Shape只能使用直接Named IRI `sh:path`。不支持Sequence、Alternative、Inverse、Zero/One/More等复杂Property Path。

正式保证以下13个SHACL Core Constraint Component：`sh:minCount`、`sh:maxCount`、`sh:datatype`、`sh:nodeKind`、`sh:class`、`sh:minInclusive`、`sh:maxInclusive`、`sh:pattern`、`sh:in`、`sh:hasValue`、`sh:or`、`sh:and`、`sh:not`。

`sh:nodeKind`当前只保证`sh:IRI`。`sh:datatype`只保证第4.2节列出的Datatype。`sh:pattern`按ECMAScript无Flags正则表达式执行；`sh:flags`不受支持。`sh:or`、`sh:and`、`sh:not`中的嵌套Shape必须继续满足本Profile。`sh:in`、`sh:or`和`sh:and`使用由Blank Node条目组成的完整无环RDF List。相同Constraint参数可重复出现并按合取执行；`sh:path`必须且只能有一个，`sh:severity`至多有一个。空Shape Graph允许作为显式无约束Stage。

### 6.2 六阶段数据视图

| Stage | SHACL看到的数据 |
|---|---|
| `asserted` | Asserted Graph |
| `domain` | Asserted + Entailed Graph |
| `feature` | Asserted + Entailed + Derived Graph |
| `change` | Change Graph |
| `output` | Output Graph |
| `provenance` | Committed Run PROV-O投影Dataset |

仅用于Ontology/Definition编译和审查的Release可以不含SHACL；进入Engine执行的Release MUST完整且唯一绑定六个Stage，不允许部分绑定。Validator自身使用`inference=none`；`domain`和`feature`看到的是ECP已物化的Entailed Graph，不允许Validator隐式选择其他推理模式。

### 6.3 Severity与报告

仅允许`sh:Violation`、`sh:Warning`和`sh:Info`。ECP Stage通过策略是“没有Violation”；Warning和Info保留在确定性Report中但不使Stage失败。

### 6.4 明确拒绝

SHACL-SPARQL及SPARQL Target；SHACL-JS；Meta-SHACL声明；复杂Property Path；本Profile未列出的SHACL Constraint Component；未登记的SHACL Predicate、Node Kind、Severity或Datatype；结构错误、参数类型错误、循环/超限RDF List和超限嵌套Shape。

## 7. 确定性资源边界

| 资源 | 上限 |
|---|---:|
| 单个Ontology Triple | 100,000 |
| 单Stage Shape Triple | 50,000 |
| 单个Shape RDF List项 | 4,096 |
| Shape嵌套深度 | 64 |
| `sh:minCount`或`sh:maxCount`参数 | 1,000,000 |
| 单来源Assertion蕴含结果 | 10,000 |

超过上限MUST以稳定错误失败，不能截断、抽样或产生部分语义结果。墙钟超时可以作为运维保护，但不得代替进入语义身份的结构化预算。

## 8. 发布、运行与历史兼容

1. Ontology与SHACL Draft保存即执行Profile静态检查并提供源码绑定诊断；
2. Published Release Preflight必须对精确Ontology和六个SHACL绑定执行完整Profile检查；
3. Base View和每个后续Stage重新核对Release内容、Profile Policy及Digest；
4. Evaluation Context记录Entailment Profile和Validation Policy；
5. Runtime Artifact记录组合Profile ID和Digest；
6. Execution Closure绑定Release、Runtime Artifact和Dependency Lock；
7. 历史Run按原Archived Runtime重放，不把新Profile应用于旧Run后声称相同执行身份。

读取既有Published Release时，Registry只复核其持久化Source、Canonical Content、Ontology Projection、Validation Report、Revision、Membership和Release摘要及跨资产绑定，不使用当前Profile重新生成历史Validation Report或改写历史身份。当前Runtime是否可以执行该Release，由版本化编译、Runtime ABI和Execution Closure兼容门禁另行判定；不能兼容时必须失败关闭或使用原Archived Runtime。

Profile 1.0的新运行使用Node Runtime ABI `enterprise-cognitive-node-runtime/2.0.0-alpha.13`和Runtime Artifact Boundary `enterprise-cognitive-node-runtime-artifact/2.0.0-alpha.3`。历史兼容入口只用于冻结Golden合同回归，不构成Execution Engine V1部署入口，也不构成Published Release的符合性入口。

## 9. 一致性门禁

Profile变更至少需要：每种RDF Term的合法、边界和拒绝Fixture；每条蕴含规则及组合、环、重复路径、顺序无关和幂等测试；13个SHACL组件各自的合规和违规Fixture；所有未支持OWL/RDFS/SHACL构造的发布前拒绝测试；独立标准实现比较Golden；Published Release只读兼容审计；文档、Manifest和可执行清单的漂移检查。

独立实现只作为Oracle或独立门禁，不进入生产Runtime。

## 10. 非目标

ECP Semantic Profile 1.0明确不提供：SPARQL Query、Update、Protocol、Service和Federation；通用RDF持久化或Endpoint；完整RDFS、OWL 2 EL/QL/RL/DL或SWRL；SHACL-SPARQL、SHACL-JS、Meta-SHACL和复杂Property Path；RDF-star、Runtime Blank Node和通用Dataset Canonicalization。

未来出现明确领域需求时，新能力必须通过新Profile版本加入。OWL 2 EL/DL推理或SPARQL应优先作为受控外部适配器评估，而不是扩大当前有限Runtime的隐式能力面。
