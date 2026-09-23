# document-normalizer

`document-normalizer` 是 `domain-knowledge` 内部的确定性文档规范化模块。它位于 MinerU（文档解析工具）与 Knowledge Formation（知识形成）之间，解决“解析块边界不等于业务语义边界”的问题。

调用链：

```text
MinerU structured_content
  -> SourceBlock（原始解析块，逐块保真）
  -> structure-aware reconstruction（结构感知重建）
  -> SourceUnit（语义来源单元）
  -> context / reference binding（上下文与引用绑定）
  -> Knowledge Formation
```

原则：

- MinerU block（块）只表示解析器恢复出的物理/版面片段，不直接作为知识抽取边界；
- 每个保留的 SourceBlock（来源块）必须且只能归属一个 SourceUnit（来源单元），保证可审计；
- 条、款等明确结构节点作为语义边界；其后被 MinerU 拆开的普通正文块合并回当前条/款；
- 没有条款结构的普通文档，只在上一正文块明显未结束时合并，避免把整个章节粗暴拼成一个大块；
- SourceUnit 保存父级、标题路径、前后单元和交叉引用；上下文只用于理解，知识归属仍绑定当前 SourceUnit；
- 不以固定 token（词元）大小或 overlap（重叠）定义语义单元；
- 该模块不判断业务概念、业务规则或机构口径，也不调用大模型修正文义。

当前实现首先覆盖确定性结构重建。解析器无法可靠恢复的复杂表格、版式或扫描缺口仍按 `PARTIAL` / limitations（限制）进入后续审计，不在此层猜测原文。
