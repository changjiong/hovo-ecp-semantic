# 设计期数据血缘

## 目标

本阶段的数据血缘回答：

> 一个已定义业务事实或业务身份，在设计上由哪个 Mapping、哪些 Scan/Column、哪些 Join 提供？

它不回答某次 Run 实际读取了哪一行。行级、断言级运行血缘属于 ECP Runtime。

共享机器合同见 [Design-time Data Lineage Contract](../../../../contracts/lineage/v1/README.md)。

## 事实血缘

每个 Binding 必须且只能有一条 FactLineage：

```text
required fact
  -> binding
  -> mapping artifact
  -> source field(s)
  -> join(s)
  -> schema snapshot
```

`source_fields[].locator` 必须与 Binding 的 `source_columns` 精确一致；同时提供结构化的 `scan_id` 与 `column`，使审计不依赖自由文本猜测。Mapping 资产集合、predicate、execution owner 与当前 output.json 保持一致。

## 身份血缘

每个 Identity Rule 必须且只能有一条 IdentityLineage：

```text
business identity
  -> identity rule
  -> mapping artifact
  -> record key field(s)
```

`record_key_fields[].locator` 必须精确覆盖当前 Identity 的 `record_key`。

## 设计期与运行期边界

设计期可以声明：

- 哪个业务事实由哪些字段提供；
- 哪个 Mapping/Join 参与；
- 哪些字段构成来源记录身份；
- 转换由 Mapping、治理来源还是 Authoring 负责。

设计期不能声明：

- 本次运行真实读取了某条记录；
- 某个 Snapshot 已经完整；
- 某个 Asserted/Derived Fact 已经在 Runtime 产生；
- 某个结果已经具有行级支持链。

运行期血缘目标由 ECP Runtime 负责：

```text
Run -> Snapshot -> source record -> asserted fact
    -> derived/entailed fact -> evaluation result
```

只有 Runtime 正式合同提供具体身份和字段后，才新增对应机器 Schema；本阶段不虚构它们。

## 交付

生成独立 `data-lineage.json`，以 ArtifactRef 登记在 `output.json.content.data_lineage`。它是工程审计资产，不是 ECP Mapping wire，不应因为存在血缘文件就声称平台已经导入或运行。
