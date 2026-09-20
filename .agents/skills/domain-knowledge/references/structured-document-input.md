# 结构化文档输入边界

## 职责边界

`domain-knowledge` 从已经结构化、可追溯的文档内容开始工作。PDF、DOCX、扫描件、图片的 OCR（光学字符识别）、版面恢复、表格识别、阅读顺序恢复和跨页拼接属于上游文档结构化服务，不属于本技能的生产职责。

本技能不绑定 MinerU、OCR 引擎或其他具体解析器。任何上游实现只要能够稳定输出本技能的结构化文档合同，即可作为输入提供者。

## 合同组成

- `SourceRef.artifact`：原始来源文档的不可变字节引用，可视为 DocumentArtifact（文档资产）。
- `SourceUnit`：业务知识形成可以直接阅读和引用的最小结构化来源单元。
- `SourceLocator`：可选的机器可读定位信息；`locator` 保留面向人的可读定位。
- `SourceExtraction`：记录上游结构化结果的完整性、方法、限制和单元闭包。字段名沿用既有合同，但它描述的是上游产物证据，不表示本技能执行了解析。
- `ParserMetadata`：可选的解析器名称、版本、运行标识和输入原文摘要，用于增强重放与审计。

机器结构见 [structured-document.schema.json](../contracts/structured-document.schema.json)。

## 最小追溯链

结构化输入必须支持：

```text
SourceUnit
  -> SourceRef
  -> original ArtifactRef
```

后续知识资产必须继续支持：

```text
Statement / Rule / Case
  -> SourceUnit
  -> SourceRef
  -> original ArtifactRef
```

因此，上游解析结果不能只交付“纯文本”；必须保留来源身份、原始文档摘要、单元定位和单元文本摘要。

## 生产要求

新生产输入应优先填写：

- `source_locator`：结构化定位；
- `sequence`：稳定阅读顺序；
- `parent_unit_id`：存在层级结构时保留父级；
- `source_extractions[].structured_document_contract = "1.0.0"`；
- `source_extractions[].parser`：解析器名称、版本及 `input_digest`。

这些元数据用于加强证据链。历史输入缺少这些可选字段时仍可作为既有资产读取，但不应据此宣称具有完整的解析重放证据。

## 缺失与失败

上游无法可靠读取某页、表格或区域时，不允许静默删除。应通过 `PARTIAL/FAILED`、限制说明和对应 SourceUnit 缺口向下游传播。领域知识技能只能依据实际提供且可定位的内容形成知识，不负责猜测被解析器遗漏的原文。

## 非目标

本合同不定义：

- 业务概念、规则或结论；
- 文档解析算法；
- OCR 模型；
- 表格重建算法；
- 平台数据映射；
- ECP 资产。

它只定义“领域知识形成开始之前，文档内容必须以什么可追溯形态到达”。
