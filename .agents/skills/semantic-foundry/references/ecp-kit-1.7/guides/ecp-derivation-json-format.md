# ECP 派生规则 JSON 编写指南

文档版本：Feature Definition V2

派生规则把已提交语义事实转换为新的派生断言。它使用版本化有限算子，不执行数据库中的 JavaScript、SQL 或任意回调。

## 必要结构

- `apiVersion`：固定为 `enterprise-risk/feature-definition/v2`
- `kind`：固定为 `FeatureDefinition`
- `metadata.id`：稳定规则 ID，应与 Rule Series ID 一致
- `metadata.version`：规则内容版本
- `coverage`：至少一个源覆盖要求；每项明确数据源、粒度、截止口径和回看周期
- `spec.kind`：固定为 `typedPlan`
- `spec.operators`：有序有限算子，算子 `id` 在规则内唯一
- `tests.contract`：非空的测试合同标识；数据库 Revision 不会从该路径加载可执行代码

可用算子和表达式以页面“插入模板”和保存前预检结果为准。不要自行构造未在 Runtime ABI 中登记的 `op`。

当前加权图场景可使用 `WeightedTransitiveClosure`。它要求根、边和终点三个前序数据集，边的 `from`、`to`
为资源，`weight`为 Decimal；`weightUnit`必须选择 `UNIT_INTERVAL` 或 `PERCENT`，并显式设置深度、路径数和
展开状态数的单根上限。新Definition还应在`limits`中显式设置跨全部Root的`maxPathRecordsTotal`和
`maxTraversalStatesTotal`；两者分别不能超过25000和250000。既有不可变Release省略时使用相同的有界兼容上限；
新Definition必须显式选择经过基数与RSS门禁验证的更小预算，默认等于上限并不代表推荐值。
单根限制产生可归属的不完整性诊断；全局预算命中时整个Feature失败关闭，不提交部分路径，也不会直接认定最终业务结论。

`EquiJoinRows`用于关联两个前序算子数据集。必须显式列出`matches`、完整的`rightVariables`、
`joinType`和`cardinality`；`LEFT` Join应使用`matchedBind`输出匹配布尔值。它只支持Typed Value等值连接，
不执行SQL、回调或模糊匹配。

`ProjectAssertions`的每个`assertions`成员可选提供`when`布尔表达式。条件为假时该断言不产生，
并且不求值它的`object`；这适合投影`LEFT` Join可选匹配的属性。

需要按自然日处理数据库`DATETIME`或语义`xsd:dateTime`时，先用`ReadProperty.valueType: "dateTime"`
读取，再使用有限表达式`DateFromDateTime`：

```json
{
  "op": "DateFromDateTime",
  "value": { "op": "Var", "name": "saleTime" }
}
```

该表达式返回`date`，提取`xsd:dateTime`词法值自身表达的日历日期。例如
`2026-08-17T23:30:00+08:00`得到`2026-08-17`；它不会把时刻换算到另一个时区。源字段若是无时区的
MySQL/OceanBase `DATETIME`，其日期部分按源本地时间保留。需要统一时区换算时，应先在受治理的数据生产边界
规范化时间语义，不能在Definition中嵌入SQL或JavaScript。

布尔表达式`Or`是受支持的有限表达式：`operands`必须是至少两个布尔表达式，并按顺序短路求值。它适合
表达同一规则内的有限并列条件；不能用它装载脚本、SQL或任意函数。

`Compare`除`EQ/NE/LT/LTE/GT/GTE`外，还支持字符串专用的`CONTAINS`和`STARTS_WITH`。两侧必须由
编译器静态判定为`string`；Runtime不会把IRI、数字、布尔值或NULL隐式转成字符串。匹配前只执行平台统一的
Unicode NFC规范化，随后按Unicode码点精确、区分大小写地比较，不Trim、不做Locale Case Folding，也不使用
正则表达式。`CONTAINS(left, "")`和`STARTS_WITH(left, "")`按标准精确字符串语义返回`true`。例如：

```json
{
  "op": "Compare",
  "operator": "CONTAINS",
  "left": { "op": "Var", "name": "caseTitle" },
  "right": { "op": "String", "value": "专利侵权" }
}
```

不同派生规则可以共同产出同一个Class或Property。运行时把它们作为保留各自`producerKey`和Support的确定性
并集，读取该语义项的后续规则会依赖全部生产者，不存在“后写覆盖前写”。同一规则内仍不得重复声明同一输出
谓词；如果多条规则可能为同一Subject/Property产生互相冲突的值，必须由候选Ontology的Range/Cardinality和
`feature`阶段SHACL明确约束，不能依赖规则执行顺序消解。

Feature DAG只连接前序规则**直接**产出的Class和Property。RDFS的Subclass、Subproperty、Domain、Range和
Inverse蕴含在全部Feature执行后统一计算；它们不能被误判为规则之间的即时依赖或用来打破/制造DAG环。

## 示例

```json derivation-example
{
  "apiVersion": "enterprise-risk/feature-definition/v2",
  "kind": "FeatureDefinition",
  "metadata": {
    "id": "customer_display_name",
    "version": "1.0.0",
    "name": "客户显示名称"
  },
  "coverage": [
    {
      "sourceId": "customer_master",
      "granularity": "DAY",
      "requiredThrough": "evaluationDate",
      "lookbackPeriods": 1
    }
  ],
  "spec": {
    "kind": "typedPlan",
    "operators": [
      {
        "id": "scan",
        "op": "ScanClass",
        "class": "urn:example:ontology:Customer",
        "bind": "customer"
      },
      {
        "id": "project",
        "op": "ProjectAssertions",
        "input": "scan",
        "subject": {
          "template": "derived:{customerId}",
          "fields": {
            "customerId": {
              "op": "CompactId",
              "value": { "op": "Var", "name": "customer" }
            }
          }
        },
        "assertions": [
          {
            "predicate": "urn:example:ontology:displayNameStatus",
            "object": { "op": "String", "value": "AVAILABLE" },
            "objectKind": "string",
            "cardinality": "one"
          }
        ]
      }
    ]
  },
  "tests": { "contract": "embedded-feature-contract.json" }
}
```

## 校验原则

- 所有 IRI 必须存在于候选 Ontology 或属于明确允许的输出声明。
- 算子输入必须引用前序有效算子，不能形成环。
- Decimal、日期和集合必须使用对应类型表达式，不能依赖 JavaScript 隐式转换。
- `CONTAINS/STARTS_WITH`只接受两个String表达式，并采用NFC、区分大小写的精确匹配。
- 修改算子集合可能改变 Runtime Identity；必须通过整体 Release 编译后发布。
- 同一Derivation会被完整Run和Scoped Evaluation复用。规则只声明语义事实/Feature依赖，不写Root Record
  Key、Fact Provider、数据库表或Scope资源上限；这些选择边界属于Mapping和独立`SCOPE`资产。
- 规则依赖新增事实时，先确认Mapping能物化该事实，再确认Published Scope闭包能完整取得其源记录；缺失或
  截断必须传播为Coverage/UNKNOWN或失败关闭，不能由规则补造默认事实。
