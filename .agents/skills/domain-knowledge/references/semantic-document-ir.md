# Semantic Document IR（语义文档中间表示）

## 定位

Semantic Document IR 是 `domain-knowledge` 内部中间表示，不是用户前置输入。它明确区分 parser block（解析器块）与 semantic unit（语义单元）。

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
  -> SourceBlock
  -> document-normalizer
  -> SourceUnit
  -> Knowledge Formation
```

## 两层对象

### SourceBlock（来源块）

SourceBlock 是 MinerU 输出经最小清洗后的物理解析事实，保留：

- 原始阅读顺序；
- page（页码）与 parser block（解析器块）定位；
- block_type（块类型）与 bbox（边界框，若存在）；
- 规范化文本及 SHA-256（摘要）。

SourceBlock 不承担知识归属。一个 block 被解析器切在哪里，不代表业务语义就应该切在哪里。

### SourceUnit（来源单元）

SourceUnit 是 Knowledge Formation（知识形成）的最小来源归属单元，由 document-normalizer 在 SourceBlock 上确定性重建。当前规则优先识别章节、条、款、表格与连续正文；条/款后的普通文本块归并到其所属单元，普通文档只在明显续文时合并。

每个 SourceUnit 必须列出 `source_block_ids`。所有保留 SourceBlock 在一份来源内满足：

```text
exactly one SourceUnit owner
```

即不允许遗漏，也不允许重复归属。

## Context（上下文）与 Ownership（归属）

SourceUnit 可携带：

- `heading_path`：标题路径；
- `ancestor_unit_ids`：结构祖先；
- `previous_unit_id` / `next_unit_id`：邻接单元；
- `references`：可解析的条文交叉引用。

这些字段用于构造 processing window（处理窗口）。模型可以读取父级、前后文或引用条款以避免断义，但知识抽取必须遵守：

```text
可读上下文 != 当前知识归属
```

Statement / Term / Rule（陈述/概念/规则）只有在语义所有权属于当前 SourceUnit 时才绑定当前单元。不能因为处理窗口看到了邻接条款，就把邻接条款知识重复抽取到当前单元。

固定 token（词元）长度和 overlap（重叠）可以用于控制模型输入长度，但不得定义 SourceUnit。

## 追溯

完整追溯链：

```text
Statement / Rule / Case
  -> SourceUnit
  -> SourceBlock
  -> SourceRef
  -> original ArtifactRef
```

因此规范化不能只保留拼接后的纯文本。即使多个 SourceBlock 合并成一个 SourceUnit，原始页码、块顺序、块摘要和解析限制仍必须保留。

## 错误边界

MinerU 返回 PARTIAL / FAILED、空块、不可读内容或复杂版式时，不猜正文。解析缺口进入 SourceExtraction / limitations（限制）和后续 Knowledge Gap（知识缺口）。

Semantic Document IR 证明的是：

1. 技能实际收到了哪些解析块；
2. 哪些块被重建为哪些语义单元；
3. 有没有块被遗漏或重复归属。

它不能独立证明 MinerU 已正确恢复全部原文，也不能证明 document-normalizer 的结构判断已被业务专家确认。
