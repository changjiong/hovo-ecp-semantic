# Pass 1 — Statement Extraction

只回答：**当前 SourceUnit 实际表达了哪些业务含义？**

禁止在本轮生成 Rule、Term、Case 或最终 Question。

## 输入

每次读取一个 SourceUnit，以及仅用于理解的 heading_path、ancestor、previous/next 和已解析引用。Statement 的 provenance 仍只能绑定真正表达该含义的 SourceUnit；不能把邻接上下文静默记到当前单元。

## 输出要求

一个 SourceUnit 可以产生 0、1 或多个 Statement。0 个时必须标注原因。

Statement 按业务语义拆分，不按句号机械拆分。例如“实际控制”条款中，人事任免、重大经营决策、财务收支、重要资产/资金支配应在业务含义彼此独立时拆为不同 Statement。

meaning_kind 使用：
DEFINITION / OBLIGATION / PERMISSION / PROHIBITION / CRITERION / PROCEDURE / EVIDENCE / TIME / EXCEPTION / CONTEXT / SOURCE_EXCERPT。

## 禁止

- 不要把原文标题直接改写成一条“万能规则”。
- 不要把推测写成 SOURCE_STATED。
- 不要因为后续想得到某条 Rule 而选择性遗漏 Statement。
- 不要把“缺少证据”解释成“事实不存在”。
