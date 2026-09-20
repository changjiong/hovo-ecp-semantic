# Document Structure Contract v1

## 所有权

该合同属于语义工程仓库的共享基础合同，不属于 `domain-knowledge` 私有合同。

生产实现应位于本仓库之外的共享数据/基础设施服务，例如独立的 `document-structure` 服务。服务可以适配 MinerU、OCR 或其他 Parser（解析器），但本合同不绑定供应商。

## 推荐服务形态

推荐采用异步 Job（任务）：

```text
submit(original document)
  -> job id
  -> parser adapter
  -> normalizer
  -> immutable structured-document result
```

原始文件和结构化结果可存放在受治理对象存储中；API 返回稳定身份、摘要和结果引用。该服务不负责业务概念、规则或判断。

机器结构见 [structured-document.schema.json](structured-document.schema.json)。

## 血缘责任

该服务负责 Document Data Lineage（文档数据血缘）：

```text
Original Artifact
  -> Parser Run
  -> SourceUnit
```

从 SourceUnit 进入 Statement/Rule/Case 后，责任转入 Evidence Lineage（证据血缘）。
