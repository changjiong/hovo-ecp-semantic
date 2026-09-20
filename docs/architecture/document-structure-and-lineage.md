# 文档结构服务与血缘边界

## 1. 前置数据处理服务

语义工程五阶段保持不变。前置的 Document Structure Gateway（文档结构化网关）属于共享基础设施，不是第六个 Skill，也不放在 `.agents/skills` 中。

```text
[基础设施]
Original Document
  -> Document Structure Gateway
  -> Structured Document

[语义工程]
domain-knowledge
  -> domain-model
  -> ecp-semantic-authoring
  -> ecp-data-mapping
  -> ecp-semantic-release
```

本仓库只拥有共享合同：`/contracts/document-structure/v1`。实际服务代码应放在独立数据/基础设施服务仓库或现有数据服务平台，由其适配 MinerU、OCR 或其他解析服务。

## 2. 四类血缘

| 血缘 | 回答的问题 | 主要责任方 |
| --- | --- | --- |
| Document Data Lineage（文档数据血缘） | SourceUnit 从哪个原始文件、哪次解析产生？ | Document Structure Gateway |
| Evidence Lineage（证据血缘） | 为什么存在这条知识、规则或业务判断？ | domain-knowledge → domain-model → authoring |
| Data Lineage（数据血缘） | 一个业务事实从什么数据字段产生；一次运行具体用了什么记录？ | ecp-data-mapping（设计期）+ ECP Runtime（运行期） |
| Asset Lineage（资产血缘） | 哪一版知识、模型、语义资产、Mapping、Release 和 Runtime 产生结果？ | authoring → release → Runtime |

四种血缘互补，不能互相代替。

## 3. Evidence Lineage 与 Data Lineage 的区别

```text
制度条款 -> Business Rule -> Domain Rule -> ECP Evaluation
```

回答“为什么这么判”，属于 Evidence Lineage。

```text
source table/column -> Mapping -> Asserted Fact -> Derived Fact -> Evaluation
```

回答“这个值从哪里来”，属于 Data Lineage。

一个可复核业务结果至少应能同时回答：为什么、用了什么数据、哪一版资产。

## 4. 数据血缘分层

### 设计期

由 `ecp-data-mapping` 负责，使用 `/contracts/lineage/v1/design-time-data-lineage.schema.json`。

最小闭包：

```text
Required Fact
  -> Binding
  -> Mapping Artifact
  -> Scan / Column
  -> Join
  -> Schema Snapshot
```

设计期血缘不得声称某条源记录已经在 Runtime 中被实际读取。

### 运行期

由 ECP Runtime 负责。目标闭包：

```text
Run
  -> Snapshot
  -> source record identity
  -> asserted fact
  -> derived / entailed fact
  -> evaluation result
```

现有 ECP Semantic Profile 已包含 provenance stage 与来源 Assertion 支持。只有目标 Runtime 对具体字段和身份作出正式合同后，才应在本仓库增加对应 Runtime lineage schema。

## 5. 资产血缘

Release 必须继续绑定精确 ArtifactRef / Digest / Membership。数据血缘文件属于工程审计资产，不自动成为 ECP Mapping wire 或 Release package 成员；Release 只保留其精确引用并核对版本闭包。

## 6. 原则

- 不建立通用血缘数据库作为本轮前提；
- 不把 Evidence 与 Data provenance 混为一个字段；
- 不根据设计期映射虚构运行期行级血缘；
- 不把外部文档 Parser 纳入五个生产 Skill；
- 所有血缘以稳定 ID、版本、摘要和不可变引用为基础。
