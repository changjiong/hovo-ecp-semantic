# Scope Definition JSON 编写指南

`SCOPE` 是 Published Semantic Release 中的正式资产，用来声明“从一个根对象出发，哪些 Mapping Scan 必须被完整读取，如何沿 Mapping Join 闭包扩展，以及局部求值的硬限制”。它不包含 SQL、数据源地址、凭证或对象存储坐标。

Scope不是Ontology构造，也不是Evaluation中的`objectScope`。Ontology定义Class/Property及推理语义；
Evaluation `objectScope`定义求值对象和结果身份；Release `SCOPE`只负责关系型局部事实的完整选择边界。
新增Scope本身不要求修改Ontology Turtle。

## 推荐编写顺序

1. 先稳定Ontology业务概念和IRI；
2. 完成Mapping的Scan、Join、Record Key、Entity、Property、Relationship及Coverage；
3. 完成SHACL、Derivation和Evaluation，让它们只依赖已映射的语义事实；
4. 选择一个Mapping Root Scan，列出全部Scan/Join并补齐Root Binding或必要Full Scan；
5. 按目标数据量设置硬上限，执行Scope源码预检和完整Release编译；
6. 将Ontology、Mapping、六阶段SHACL、规则和Scope的精确Revision一起发布。

## 固定协议

- `apiVersion`: `enterprise-cognitive/scope-definition/v1`
- `kind`: `ScopeDefinition`
- `metadata.status`: `ACTIVE` 或 `RETIRED`
- `selection.strategy`: `MAPPING_JOIN_CLOSURE_V1`
- `selection.direction`: `BOTH`

## 关键字段

- `mapping` 必须绑定同一候选/Published Release 中唯一 Mapping 的 `mappingId` 与 `version`。
- `root.scanId` 是入口 Scan，`root.keyColumns` 必须与该 Scan 的 `recordKey` 完全相同。
- `requiredScanIds` 必须覆盖 Release Mapping 的全部 Scan；`joinIds` 必须覆盖全部 Mapping Join。
- `rootBindings` 把Root Scan列与另一个Scan列声明为受治理的双向等值边，用于取得无法仅靠Mapping Join
  连通的辅助事实。它作用于闭包中每一条已选Root Scan行，包括后来由Join或Overlay选中的Root行，而不是
  只对创建Case时请求的Root执行一次；左右列数量必须相等，关系型类型必须兼容。
- `fullScanIds` 仅用于确实属于局部语义闭包、且不参与 Join 的小型完整参考表。
- `limits` 是发布时固化的行数、前沿键和补丁操作上限，任何截断都必须失败关闭。
- `factProviderRef` 只引用服务端已部署的有限事实提供器；Endpoint 和 Token 由服务端环境配置，不进入资产。

## 跨资产变更规则

| 发生的变化 | Scope动作 |
|---|---|
| 只增加或修改Ontology label/comment，Mapping拓扑不变 | Scope语义通常不变；仍须重绑Mapping的Ontology摘要并重新编译Release |
| 新增Class/Property，但Mapping和规则尚未使用 | 不自动修改Scope；在完整候选中复核 |
| Mapping ID/version、Scan/Join集合、Root Record Key或Join端点变化 | 必须审查并通常创建新Scope Revision |
| 新规则依赖新的已映射事实 | 复核该事实所在Scan从Root可达；必要时增加Root Binding/Full Scan并创建新Revision |
| 只调整Fact Provider URL、Token或超时 | 只改部署配置，不创建Scope Revision或Release |
| Scope资源上限或`factProviderRef`变化 | 创建新Scope Revision和新Release |

Scope发布后不可原地修改。任何正文变化都通过新Draft Revision和新Published Release表达；历史Case继续绑定
原Release、Scope Revision与Execution Binding。

## 禁止内容

- 任意 SQL、JavaScript、回调或动态操作符；
- Hovo/MySQL/OceanBase 连接参数和密钥；
- S3 Endpoint、Bucket、Object Key、ETag 或本地暂存路径；
- 未在 Mapping 中声明的 Scan、Join 或列。

保存前预检会进行严格 JSON Schema 校验；候选 Release 编译还会验证 Scope 与该 Release 的 Mapping 是否形成完整、可达、未截断的选择策略。

## 最小完整示例

下例与Mapping指南中的单表`customer_scan(customer_id)`配套。真实多表Mapping必须把全部Scan和Join列入
`requiredScanIds`及`joinIds`，不能照抄空数组。

```json scope-example
{
  "apiVersion": "enterprise-cognitive/scope-definition/v1",
  "kind": "ScopeDefinition",
  "metadata": {
    "scopeId": "customer_investigation",
    "scopeVersion": "1.0.0",
    "name": "客户局部调查范围",
    "description": "读取一个客户及其完整映射事实",
    "status": "ACTIVE"
  },
  "mapping": {
    "mappingId": "customer_mapping",
    "mappingVersion": "1.0.0"
  },
  "factProviderRef": "customer_scoped_facts_v1",
  "root": {
    "scanId": "customer_scan",
    "keyColumns": ["customer_id"]
  },
  "selection": {
    "strategy": "MAPPING_JOIN_CLOSURE_V1",
    "direction": "BOTH",
    "joinIds": [],
    "rootBindings": [],
    "fullScanIds": [],
    "requiredScanIds": ["customer_scan"],
    "maximumDepth": 10
  },
  "limits": {
    "maximumRowsPerScan": 10000,
    "maximumTotalRows": 50000,
    "maximumFrontierKeys": 100000,
    "maximumPatchOperations": 1000,
    "maximumOverlayOperations": 10000,
    "maximumFactBundleBytes": 67108864,
    "maximumResultAssertions": 1000000,
    "maximumResultEvaluations": 100000,
    "maximumResultBytes": 67108864
  }
}
```

## 发布前检查

- Root Key与Mapping `recordKey`逐列相同；
- Required Scan和Join分别与Mapping全集一致；
- 每个非Full Scan都能从Root、Root Binding或Join闭包到达；
- 每个Root Binding都按双向等值关系应用于全部已选Root行；测试数据必须覆盖“Join先选中第二条Root，
  再由Root Binding带入其辅助事实”的情形；
- Full Scan确实是有治理的小型参考/完成证明，不是绕过闭包的便利开关；
- 上限按真实数据量压测后设置，任何命中上限都失败关闭而不是静默截断；
- 服务端存在与`factProviderRef`匹配的Provider，并且Endpoint/Token没有进入任何语义文件；
- 候选Release包含唯一Mapping、完整六阶段SHACL以及规则所需的全部精确Revision。
