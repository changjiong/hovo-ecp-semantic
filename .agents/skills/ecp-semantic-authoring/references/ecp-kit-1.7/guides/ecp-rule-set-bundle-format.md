# ECP 完整规则集 ZIP 编写指南

文档版本：Rule Set Bundle V1

## 用途

完整规则集 ZIP 用于一次性替换当前 Workspace 中全部活动的 `SHACL`、`DERIVATION`、`EVALUATION` 和 `ACTION_POLICY` Draft Head。ZIP 中未登记的旧规则会从当前 Draft 候选移除；不可变 Revision、Published Release 和运行记录不会删除。

单个 Turtle 或 JSON 文件只用于单项编辑，不能表示完整规则集。空 ZIP 也不表示清空；清空必须使用页面中的独立危险操作。

## 目录结构

ZIP 根目录只能包含一个 `manifest.json` 和 Manifest 精确登记的成员文件。目录条目可以存在，但不得包含额外文件。

```text
manifest.json
rules/asserted-shapes.ttl
rules/domain-shapes.ttl
rules/feature-shapes.ttl
rules/change-shapes.ttl
rules/output-shapes.ttl
rules/provenance-shapes.ttl
rules/customer-features.json
rules/customer-evaluations.json
rules/notification-policy.json
```

路径必须使用 NFC、正斜杠和相对路径，不能包含 `..`、反斜杠、空路径或未登记文件。所有正文必须是严格 UTF-8。

若已有完整工作目录（包含`ontology/`、`mapping/`、`data-sources/`和`rules/`），可直接把该目录压缩为ZIP并在“规则、约束与求值范围”页面导入。系统会忽略macOS的`__MACOSX/`、`.DS_Store`和`._*`元数据，只从根规则Manifest中抽取登记规则；普通规则ZIP仍不允许额外业务文件。新的跨页面正式布局请使用下载中心的`Semantic Workspace Package Manifest v1/v2 JSON Schema`和《ECP Semantic Workspace Package 1.0 / 2.0》。V2中的Scope仍作为独立Series保存，不属于规则集原子替换成员。

## Manifest

`manifest.json` 是闭合 JSON 合同，不接受未知字段。

```json rule-set-bundle-example
{
  "schemaVersion": 1,
  "kind": "ECP_RULE_SET_BUNDLE",
  "bundleFormat": "enterprise-cognitive/rule-set-bundle/1.0.0",
  "semanticProfileId": "enterprise-cognitive/semantic-profile/1.0.0",
  "semanticProfileDigest": "sha256:<从 ecp-semantic-profile-1.0.json 读取的 64 位小写摘要>",
  "members": [
    {
      "assetSeriesId": "asserted_shapes",
      "assetType": "SHACL",
      "name": "Asserted Shapes",
      "description": "约束关系型映射产生的断言",
      "path": "rules/asserted-shapes.ttl",
      "mediaType": "text/turtle",
      "sourceDigest": "sha256:<成员 UTF-8 正文字节的 64 位小写摘要>",
      "shaclStage": "asserted"
    },
    {
      "assetSeriesId": "customer_features",
      "assetType": "DERIVATION",
      "name": "Customer Features",
      "description": "客户派生事实",
      "path": "rules/customer-features.json",
      "mediaType": "application/json",
      "sourceDigest": "sha256:<成员 UTF-8 正文字节的 64 位小写摘要>",
      "shaclStage": null
    }
  ]
}
```

`sourceDigest` 对文件原始 UTF-8 字节计算 SHA-256。空白、换行和 JSON 格式化变化都会改变摘要。`semanticProfileDigest` 必须与下载中心当前 `ECP Semantic Profile Manifest` 中的 `profileDigest` 完全相同。

## 成员规则

| Asset Type | 扩展名 | `mediaType` | `shaclStage` |
|---|---|---|---|
| `SHACL` | `.ttl` | `text/turtle` | 六个 Stage 之一 |
| `DERIVATION` | `.json` | `application/json` | `null` |
| `EVALUATION` | `.json` | `application/json` | `null` |
| `ACTION_POLICY` | `.json` | `application/json` | `null` |

如果包含任意 SHACL 成员，就必须为 `asserted`、`domain`、`feature`、`change`、`output` 和 `provenance` 各提供且只提供一个成员。规则集可以暂时不含 SHACL，用于 Draft 开发；进入可执行 Release 时仍须满足 Release 的六阶段要求。

每个 `assetSeriesId` 和成员路径都必须唯一。若 Workspace 已存在同 ID Series，其 Asset Type、名称和说明必须与 Manifest 一致；Series 元数据不能通过导入偷偷改名或改类型。

## 预检与提交

1. 在“规则、约束与求值范围”页面选择“导入完整规则集”。
2. 选择 ZIP，等待服务端校验 Archive、Manifest、Profile、源码及可用的完整编译上下文。
3. 审查新增、修改、移除和不变项；整体编译为 `INVALID` 时不能提交。
4. 显式确认后提交。服务端使用预览得到的 Draft Set Digest 执行 CAS 和单事务替换。
5. 并发修改导致 CAS 冲突时，重新选择 ZIP 并生成新预览，不要重用旧 Candidate Digest。

当前上限为 4,000,000 字节 ZIP、20,000,000 字节解压正文、128 个 ZIP 条目、96 个规则成员及单文件 5,242,880 字节。超过上限会整体失败，不会截断或部分导入。

## 安全边界

- 不写数据库连接、密码、Token、Endpoint、Bucket 或本地路径。
- 不加载任意 JavaScript、SQL、SPARQL 回调或外部脚本。
- JSON 成员分别遵循派生、评估和动作策略编写指南；Turtle 成员遵循 SHACL 编写指南。
- ZIP 预检不代替 Release Composer 的最终发布门禁。
