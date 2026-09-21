# Structured Document IR 与来源覆盖

## 输入单元

每份 `SourceRef` 必须对应一条 `source_extractions`。这些对象由 `domain-knowledge` 内部 document-intake 根据外部解析服务响应规范化形成。状态为 `COMPLETE` 或 `PARTIAL` 时，列出的 `unit_ids` 必须与该来源实际 `source_units` 完全一致；状态为 `FAILED` 时不得伪造单元。

每份来源同时标明 `source_role`：`NORMATIVE_RULE` 支撑实体规则，`PROCEDURAL_GUIDANCE` 说明办理过程，`SYSTEM_INTERFACE` 说明报文与状态，`EXPERT_EXPLANATION` 和 `SECONDARY_CONTEXT` 只作解释、案例线索或冲突输入。来源角色不能被统一的 `PRIMARY` 权威标签替代。

`source_units` 保存可复核的最小结构化输入单元：条款、款项、章节、表格、附录、前言或页块。每个单元记录来源、显示标签、可读定位、规范化文本和文本 SHA-256；上游可额外提供机器可读 `source_locator`、父级和阅读顺序。扫描页、无法提取的内容和跨页续接问题必须由外部解析响应或 document-intake 状态显式保留；Knowledge Formation 不能因解析结果缺失而补写、推测或静默跳过。

## 输出覆盖

每个输入单元在 `provision_coverage` 中恰好出现一次：

- `COVERED`：该单元已有材料映射，并至少关联一个陈述、概念、问题、规则或案例；此状态不单独证明含义已审查。
- `PARTIAL`：仅完成部分材料映射，必须关联开放的 `KNOWLEDGE_GAP`。
- `UNREADABLE`：无法可靠读取，必须关联开放的 `KNOWLEDGE_GAP` 和恢复材料。
- `OUT_OF_SCOPE`：已阅读但不属于本次业务范围，必须说明范围依据和业务主题。

覆盖记录说明业务主题、业务含义、适用范围和关联对象。不能用空锚点、笼统的“全文已覆盖”或一个规则覆盖整份文件来绕过逐单元判断。

`SOURCE_STATED` 陈述必须直接列出 `source_unit_ids`；其 `source_ids` 必须与这些单元所属来源完全一致。覆盖记录关联某个陈述时，该陈述必须真实引用当前条款单元。

## 业务含义审查

每条覆盖记录另记 `meaning_status` 和具体的 `meaning_note`：

- `NOT_REVIEWED`：未按本版本方法回读业务含义。原文已读、已摘录或旧映射齐全也不能自动升级。
- `PARTIAL`：只审查了部分义务、条件、例外或用途，说明已审及剩余内容。
- `REVIEWED`：本单元全部范围内的业务含义已回读并形成具体陈述；必须至少关联一条真实引用本单元、非 `SOURCE_EXCERPT` 的陈述。这是作者审查声明，不等于责任人批准。
- `NOT_APPLICABLE`：仅用于有明确排除理由的 `OUT_OF_SCOPE`。

前两种状态必须关联开放的 `KNOWLEDGE_GAP`，该事项的 `affects` 包含对应覆盖记录；同一整体重审缺口可覆盖多条未审单元。部分审查不能只记录一句“待确认”。不能以用户尚未批准为由把已经完成的作者回读改成未审；两者是独立状态。

陈述的 `meaning_kind` 区分原文摘录、定义、义务、权限、禁止、条件、过程、证据、时间、例外及背景。长原文加标题前缀仍是 `SOURCE_EXCERPT`。一条原文可能包含多条陈述，多条依据也可共同解释一个业务问题。详见 [问题发现与归并](question-discovery.md)。

## 完成声明

SourceExtraction 声明 COMPLETE、每个已提供单元唯一映射且均 `COVERED` 或有依据的 `OUT_OF_SCOPE`，只能声明“本次解析响应形成的来源单元已完整处理”。这不是对外部解析器正确恢复原始文件内容的独立证明。`PARTIAL`、`UNREADABLE` 或 `FAILED` 必须报告材料缺口。

业务含义审查另按范围统计，存在 `NOT_REVIEWED` 或 `PARTIAL` 时，整体语义审查只能为部分完成或未开展。三个主题样章不能使其他主题自动变为已审。候选问题是否有去向、流程是否补查也独立记录。

台账在 `coverage.md` 完整展示；正文仅概览和说明影响。结构检查可以验证状态、数量和引用，不能验证阅读确实发生或独立断定制度已被正确理解。
