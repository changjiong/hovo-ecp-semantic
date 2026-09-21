# Structured Document IR（结构化文档中间表示）

## 定位

Structured Document IR 是 `domain-knowledge` 内部中间表示，不是用户前置输入。

用户视角：

```text
PDF / DOCX / 扫描件
  -> domain-knowledge
  -> Domain Knowledge
```

技能内部：

```text
raw documents
  -> document-intake
  -> MinerU 4.x V1 / structured_content
  -> normalize
  -> Structured Document IR
  -> Knowledge Formation
```

文档解析算法由 MinerU 服务提供；`domain-knowledge` 负责调用 V1 API、消费 `structured_content`、规范化、检查解析状态并把缺口继续传给知识形成。`middle_json` 只用于人工调试/校准，不进入正常生产链路。技能本身不安装 OCR、PDF 或 DOCX 解析库。

## 内部合同

内部规范化输入仍使用：

- `SourceRef`：原始文档字节身份和来源元数据；
- `SourceUnit`：知识形成可直接读取和引用的最小来源单元；
- `SourceLocator`：页、块或章节定位；
- `SourceExtraction`：本次解析状态、方法、限制和单元闭包；
- `ParserMetadata`：实际解析器名称、版本、运行标识和原文摘要。

机器结构见 [structured-document.schema.json](../contracts/structured-document.schema.json)。完整内部输入见 [input.schema.json](../contracts/input.schema.json)。

## 追溯

内部 IR 必须保留：

```text
SourceUnit
  -> SourceRef
  -> original ArtifactRef
```

后续知识资产继续形成：

```text
Statement / Rule / Case
  -> SourceUnit
  -> SourceRef
  -> original ArtifactRef
```

因此 document-intake 不能只保留纯文本，也不能在 normalize 时删除页码、块标识、原文摘要和解析限制。

## 错误边界

如果外部解析服务返回 PARTIAL / FAILED、空块或不可读内容，document-intake 不猜正文，也不把缺失静默转成完整输入。缺口进入 SourceExtraction / SourceUnit，再由现有 ProvisionCoverage 和 Knowledge Gap 机制继续处理。

Structured Document IR 只证明“技能实际接收到了什么解析结果”，不能独立证明外部解析器已经正确理解所有版面、表格或扫描内容。
