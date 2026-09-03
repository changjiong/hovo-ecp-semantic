# ECP Mapping JSON 编写指南

文档版本：Mapping Definition V1

## 用途与导入顺序

Mapping JSON 描述关系型数据如何生成本体实例、数据属性和对象关系。它不是任意 SQL，也不能包含数据库连接配置或凭据。

1. 先导入并保存对应的 Ontology TTL。
2. 取得该 TTL 草稿页面显示的 `ontologySourceDigest`。
3. 将此摘要原样写入 Mapping JSON。
4. 在“数据映射”页面选择“导入 JSON”，也可直接选择统一工作包 ZIP；页面只读取其中的 Mapping。系统会执行严格结构、当前 Hovo 表/字段和语义校验并自动保存新的 Draft Revision。

`ontologySourceDigest` 绑定的是 TTL 原始文本摘要。即使语义相同，修改空白、换行或注释也可能产生不同摘要。

## 顶层结构

根对象必须且只能包含下列字段，未知字段会被拒绝：

| 字段 | 要求 |
|---|---|
| `schemaVersion` | 固定为 `1` |
| `mappingId` | 稳定标识，只允许系统 ID 字符 |
| `version` | Mapping 自身版本文本 |
| `name` / `description` | 名称和说明 |
| `ontologySourceDigest` | `sha256:` 加 64 位小写十六进制字符 |
| `dataSources` | Hovo 数据源引用，不得包含连接信息 |
| `scans` | 被读取的表或视图及完整字段清单 |
| `joins` | 同一数据源内的受控等值关联 |
| `entities` | 从 Scan 构造本体类实例的实体映射 |
| `properties` | 字段到 Datatype Property 的映射 |
| `relationships` | Entity 到 Entity 的 Object Property 映射 |
| `filters` | 有限比较操作组成的过滤条件 |
| `coverage` | 完整快照与 UNKNOWN 传播策略 |

## 关键约束

- `dataSources[].ref` 在本文档内唯一；只写 `dataSourceCode` 和 `environment`。
- `scans[].columns` 应包含该 Scan 后续身份、属性、Join 和 Filter 所使用的全部字段。
- `recordKey` 非空且必须来自 `columns`，应能稳定标识源记录。
- Join 仅支持 `INNER`、`LEFT` 和等值字段组；两端必须属于同一 Hovo 数据源。
- `cardinality` 只能是 `ONE_TO_ONE`、`ONE_TO_MANY`、`MANY_TO_ONE`。
- Entity 的 `classIri` 必须是当前 Ontology 中已声明的 Class。
- `anchorScanId` 是 Entity 的主 Scan；`joinIds` 必须形成从主 Scan 可达的闭包。
- 身份模板中的每个 `{variable}` 必须有且只有一个 binding；编码固定为 `RFC3986_COMPONENT`，空值策略固定为 `REJECT`。
- Property 的 `predicateIri` 必须是 Datatype Property；`datatypeIri` 应与本体 Range 一致。
- Relationship 的 `predicateIri` 必须是 Object Property，其 subject/object Class 应与本体 domain/range 一致。
- Mapping 与同一候选 Release 的 SHACL 必须一致：`nullPolicy: OMIT` 不能对应 `sh:minCount > 0`；允许多值的 Cardinality 不能对应 `sh:maxCount <= 1`；`datatypeIri` 必须与 `sh:datatype` 相同。系统会在候选审查和正式发布时用完整 Draft Head 正文失败关闭这些矛盾。
- Filter 不允许 SQL 文本，只支持 `IS_NULL`、`IS_NOT_NULL`、`EQ`、`NE`、`LT`、`LE`、`GT`、`GE`、`IN`、`NOT_IN`。
- 每个 Entity 都应有一个 Coverage Requirement；源不可用、部分读取或拒绝行时均固定传播 `UNKNOWN`。

## 与对象局部 Scope 的联动

标准全量Run只需要Mapping，不要求额外Scope。需要围绕一个Root创建Investigation Case时，应在Mapping稳定后
单独编写`Scope Definition v1`：

- Scope的`mapping.mappingId`和`mapping.mappingVersion`必须精确等于同一候选Release中的Mapping；
- `root.scanId`必须引用一个稳定Scan，`root.keyColumns`必须与该Scan的`recordKey`完全相同；
- `requiredScanIds`和`joinIds`必须分别完整覆盖Mapping的全部Scan和Join，不能只列“看起来相关”的子集；
- 不能通过Join到达但可由Root列等值筛选的Scan使用`rootBindings`；它是作用于每一条已选Root行的双向
  等值边，包括由Join或Overlay后来选中的Root行，不是只为最初请求Root执行一次。确需完整读取的小型治理
  参考表才使用`fullScanIds`；
- Scan ID、Join ID和Record Key会进入Scope及Case身份，应保持稳定，不能用数据库临时名或日期后缀充当逻辑ID。

修改Mapping的ID/version、Scan/Join集合、Root Record Key、Join端点或可达性时，必须同步创建新的Scope
Revision并发布新Release。仅修改Entity/Property投影而没有改变上述选择拓扑时，仍需重新执行Release编译；
Scope正文是否需要新Revision由其绑定的Mapping version及实际闭包变化决定，不能跳过预检自行推断兼容。

## 可导入示例

导入前请把示例中的 `ontologySourceDigest` 替换为当前 TTL 的精确摘要，并确保 Hovo 中存在对应数据源、表和字段。包中的Schema快照不替代导入时的当前Hovo发现，也不替代运行期Snapshot漂移检查。

```json mapping-example
{
  "schemaVersion": 1,
  "mappingId": "customer_mapping",
  "version": "1.0.0",
  "name": "客户主数据映射",
  "description": "从客户主表构造 Customer 实例",
  "ontologySourceDigest": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
  "dataSources": [
    {
      "ref": "customer_source",
      "dataSourceCode": "customer_db",
      "environment": "generated"
    }
  ],
  "scans": [
    {
      "id": "customer_scan",
      "dataSourceRef": "customer_source",
      "schema": "customer",
      "table": "customer",
      "relationKind": "TABLE",
      "columns": ["customer_id", "customer_name"],
      "recordKey": ["customer_id"]
    }
  ],
  "joins": [],
  "entities": [
    {
      "id": "customer_entity",
      "classIri": "urn:example:ontology:Customer",
      "anchorScanId": "customer_scan",
      "joinIds": [],
      "identity": {
        "template": "urn:example:customer:{customer_id}",
        "encoding": "RFC3986_COMPONENT",
        "bindings": [
          {
            "variable": "customer_id",
            "source": { "scanId": "customer_scan", "column": "customer_id" }
          }
        ],
        "nullPolicy": "REJECT"
      }
    }
  ],
  "properties": [
    {
      "id": "customer_name_property",
      "entityId": "customer_entity",
      "predicateIri": "urn:example:ontology:customerName",
      "source": { "scanId": "customer_scan", "column": "customer_name" },
      "datatypeIri": "http://www.w3.org/2001/XMLSchema#string",
      "cardinality": "ONE",
      "nullPolicy": "OMIT"
    }
  ],
  "relationships": [],
  "filters": [],
  "coverage": {
    "mode": "FULL_SNAPSHOT",
    "requirements": [
      {
        "entityId": "customer_entity",
        "requiredScanIds": ["customer_scan"],
        "onSourceUnavailable": "UNKNOWN",
        "onPartialRead": "UNKNOWN",
        "onRejectedRow": "UNKNOWN"
      }
    ]
  }
}
```

## 常见失败

- `additionalProperties`：出现了 V1 未声明的字段。
- `Mapping 绑定的 Ontology 源摘要 ... 与当前 Ontology Draft 摘要 ... 不一致`：JSON 绑定了另一版 TTL 草稿；请使用与目标 Ontology Draft 配套的 Mapping，或在确认兼容性后重新生成 Mapping。
- 引用了不存在的 Scan、Join、Entity、Class 或 Property。
- Identity 模板变量与 bindings 不一致。
- Join 跨越不同 Hovo 数据源，或 Join 字段未包含在 Scan columns 中。
- Coverage 缺失、重复或未覆盖 Entity。
- Mapping 与 SHACL 的 Null、Cardinality 或 Datatype 要求互相矛盾；请根据真实业务语义修改两者之一，不能依赖运行时数据“恰好不触发”。
