# document-normalizer

`document-normalizer` 是 `domain-knowledge` 内部的语义结构恢复模块。它位于 MinerU（文档解析工具）与 Knowledge Formation（知识形成）之间，解决“解析块边界不等于业务语义边界”的问题。

```text
MinerU structured_content
  -> SourceBlock（原始解析块）
  -> L1 deterministic reconstruction（确定性结构重建）
  -> ambiguous boundary（模糊边界）
  -> L2 Jev boundary-repair（Jev 边界修复）
  -> deterministic assembler（确定性组装）
  -> SourceUnit（语义来源单元）
  -> Knowledge Formation
```

## L1：确定性结构重建

以下情况不调用模型：

- 章、条、款等显式结构；
- paragraph_title（段落标题）；
- table（表格）和 image（图片）；
- 明显被硬切断且上一块未结束的连续正文；
- 明确已经结束的独立普通正文。

显式条/款后的普通文本仍归属对应条/款；MinerU block（块）只表示解析器物理边界，不直接成为知识边界。

## L2：Jev 边界修复

只有局部结构存在真实歧义时才调用 [boundary-repair](../boundary-repair/README.md)。当前触发点保持窄范围：

- 前一普通块以冒号结束，后续可能是续文、并列新单元或子项；
- 当前普通块具有未被显式条款规则识别的列表/子项形态。

Jev 只返回 `CONTINUE_PREVIOUS / START_NEW_UNIT / CHILD_OF_PREVIOUS / UNRESOLVED` 及概率和置信度。模型没有文本修改权限；SourceUnit 始终由代码组装。

## 不变量

- 每个保留 SourceBlock 必须且只能归属一个 SourceUnit；
- Jev 的局部 context（上下文）不改变知识 ownership（归属）；
- 低于置信度阈值的结果不自动应用；
- 未解决边界必须显式留下 BoundaryDecision，并使 SourceExtraction 为 PARTIAL；
- 不以固定 token（词元）大小或 overlap（重叠）定义语义单元；
- 本层不形成业务概念、业务规则或机构口径。
