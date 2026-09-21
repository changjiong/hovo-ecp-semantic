# 领域知识交付合同

本技能独立交付业务知识，不依赖其他技能或平台。完整输出由 [业务交付要求](../references/business-delivery.md) 和结构化资产合同 4.0.0 共同约束；JSON Schema 约束条款输入清单与结构化附件，本地校验器另行核对来源闭包、逐条覆盖、问题发现记录、业务文档存在、跨文档链接与定位覆盖。4.0.0 不兼容 3.0.0。

## 输入与工作模式

用户提供业务目标、使用者以及按 [结构化文档输入合同](structured-document.schema.json) 提供的来源内容。`domain-knowledge` 不负责把 PDF、DOCX、扫描件或图片解析成文本；上游负责形成 SourceRef、SourceUnit 与 SourceExtraction，本技能只验证其闭包、摘要与引用。每份输入以 `request_id` 和 `contract_version: "4.0.0"` 标识；输出的唯一 `input_ref` 必须回指相同版本的输入。

- PRODUCE：先校验上游结构化来源单元清单，再形成业务知识草案。
- REVIEW：审查指定文件，交付业务可读的审查意见及结构化问题报告；不要求已有确认，也不制造占位知识基线。
- REVISE：按明确请求和依据更新已有成果，列明发生变化的业务含义、受影响案例和需要重新确认的事项。

REVIEW 的结构化结果使用 `content.subjects`、`assessment`、`limitations` 和顶层 `issues`，不输出 `confirmation`，也不生成 `coverage.md` 占位件。其余模式使用来源、条款单元、陈述、概念、问题、规则、案例、条款覆盖、案例覆盖、问题发现记录与确认范围。字段定义见 input.schema.json 与 output.schema.json。

## 主成果与附件

`review.md` 是《领域业务知识说明书》，审查模式下是《领域业务知识审查意见》。`output.json` 是技术附件。说明书涵盖正文、访谈确认清单及来源索引；业务人员可以独立阅读，不需要核对 JSON 字段。

PRODUCE 与 REVISE 必须登记唯一的 `review.md` 和 `coverage.md`，两者与 `output.json` 使用相同 `content_version`。`review.md` 解释范围、问题、术语、规则、开放事项和来源，并以相对链接指向 `coverage.md`；它不承担全部陈述、案例和条款覆盖台账。`coverage.md` 承接完整的陈述、案例、ProvisionCoverage、候选问题和流程核对记录及逐条台账。REVIEW 只登记唯一的 `review.md`，不得以 `coverage.md` 占位。可以登记其他明确附件；它们不取代两份规定业务文档。

所有登记文档使用独立的 `ArtifactRef`，有各自真实字节摘要；Markdown 文档的 `contract_version` 为 `text/markdown`，不等于领域知识合同版本。`output.json` 不登记或引用自身。文档在相应业务内容处使用有可读邻近文字的 HTML 锚点关联对象标识，业务链接显示名称。校验器检查定位与内部相对链接，不以锚点通过声称正文含义已经验证。章节与锚点约定见业务交付要求。

ArtifactRef 使用稳定 artifact_id、content_version、contract_version、相对任务项目根目录的 path 和原始字节 SHA-256 digest。禁止路径越界、符号链接和凭据。说明书或来源变动后重新计算引用摘要，不把旧检查报告当成新字节的证明。

## 来源、状态与确认

SourceRef 定位原始材料、来源主体、时间、版本、原文位置及来源角色。SourceUnit 是上游结构化文档服务提供的可核对来源单元；SourceExtraction 记录该上游结构化结果的状态、方法、限制和完整单元集合。字段名保留 “extraction” 仅表示来源产物证据，不表示本技能执行了解析。可选的 source_locator、sequence、parent_unit_id 与 parser 元数据用于增强定位和重放。SOURCE_STATED 陈述必须同时指向来源和具体条款单元，Term/Rule.statement_ids 指向陈述，Case.question_ids 指向业务问题。`Question` 以 `topic` 归组，可用 `parent_question_id` 表示无环父子关系；`explanation`、Term 的 `example`/`counterexample` 与 Case 的 `reasoning` 为独立业务解释的结构化载体。PRODUCE 或 REVISE 新增的判断和样章必须填写适用解释；未重审的既有范围可以缺省，不得用空白补造解释。

ProvisionCoverage 的 `status` 只记录来源单元是否已被登记处理（COVERED、PARTIAL、UNREADABLE、OUT_OF_SCOPE）；`meaning_status` 独立记录业务含义审查（REVIEWED、PARTIAL、NOT_REVIEWED、NOT_APPLICABLE），并以 `meaning_note` 说明状态。PARTIAL 或 NOT_REVIEWED 必须关联开放的 KNOWLEDGE_GAP；OUT_OF_SCOPE 必须对应 NOT_APPLICABLE 和具体理由；REVIEWED 必须关联当前单元的非 SOURCE_EXCERPT 业务陈述。`meaning_kind` 区分原文摘录、定义、义务、许可、禁止、判断标准、流程、证据、时间、例外与背景，不能把原文摘录本身当作业务含义审查。

`question_discovery` 明确本轮 `scope_question_ids`，并登记候选问题及流程核对。候选问题有 SOURCE/PROCESS 来源和 RETAINED、MERGED、OUT_OF_SCOPE 或 OPEN 去向；RETAINED/MERGED 必须指向声明范围内的问题，OPEN 必须关联开放缺口。流程核对记录角色、阶段、关注点、来源单元、范围内问题及 COVERED、GAP 或 NOT_APPLICABLE 状态；GAP 必须关联开放缺口。本轮范围内的问题必须能回指候选去向或开放缺口，流程补查为空时不能通过；若不适用则保留理由。合同不要求臆造范围外候选，也不允许合并去向静默丢失。问题发现检查只对显式声明的范围负责，报告同时列出范围外问题。

issues 记录分歧或缺口、影响范围、建议、责任和解决前行为。案例仍标记正例、反例、边界或缺证类型；每个问题的案例覆盖可使用实际案例、明确不适用说明或开放缺口，不要求凑齐四类样板。

内部 origin、review_status、dispute_status 分别保存形成性质、确认状态和争议状态。业务正文使用“材料记载”“分析推断”“建议口径”“待确认”“存在分歧”等完整中文，并说明具体依据。确认不能抹掉推断来源，原文记载不能自动变成已采信事实。

states 只记录结构检查与业务内容审查。未执行写 NOT_EXECUTED，已执行结果应有真实 evidence；业务内容审查的 claim 必须说明是作者自查、智能体审阅还是业务读者审阅，不能把前两者写成人类验收。说明书分别呈现四项目标的自查、实际读者答复和领域确认。

业务确认使用独立 ConfirmationRecord，包含真实答复、责任角色、时间、业务事项范围和固定版本的 subjects。技能维护技术绑定，业务人员按可读标题答复。没有答复就保留待确认；确认对象摘要不能写入被确认文件自身。确认不会回写已签认字节，后续使用携带该成果及外部确认记录。输出内声明 CONFIRMED/REJECTED 时，关联证据必须是满足 ConfirmationRecord 的记录，结论和事项范围一致，并精确绑定本内容版本的业务文档与审计附件；其他结构检查证据不能代替。已签认文档不由生成器原地重写，修订应产生新的草案版本和路径。

## 完成与检查边界

先按四项目标审阅主文档，再核对附件。两者的事实、前提、阈值、时间、例外、案例预期、禁止结果与确认状态必须一致；自然语言改写不得改变业务含义。缺口可随待审草案交付，但不能将受影响范围称为确定实施需求。

本地入口为 scripts/validate_contract.py --check-schemas 和 validate input|output FILE --project-root ROOT。Registry 按随包 Schema 的标识离线解析，不访问网络，不读取其他技能合同。

检查工具核对结构、精确字节引用、来源与单元闭包、逐条覆盖、标识类别、问题发现记录、覆盖一致性、文档定位和规定的跨文档链接。`sourceCoverage=COMPLETE` 只表示每个已提供输入单元恰好有一条 ProvisionCoverage，即来源登记映射闭包；它不表示原始文件解析完整、业务含义已审查或知识完整。上游结构化完整性由 SourceExtraction 状态与解析证据单独说明。`sourceExtraction` 单独报告来源与条款抽取是否完整，`meaningReview` 单独报告范围内含义审查是否仍有 PARTIAL/NOT_REVIEWED，`questionDiscovery` 单独报告是否有 OPEN 候选或 GAP 流程核对，并输出开放 KNOWLEDGE_GAP、OPEN 候选和流程 GAP 的数量及标识。

只有来源抽取、业务含义审查与问题发现均无未决项，且不存在任何开放 KNOWLEDGE_GAP 时，`knowledgeExtraction=COMPLETE`；否则为 PARTIAL。该状态仍不是业务语义验证、来源真实性验证、实际读者理解或确认人身份验证。工具不能证明锚点附近内容正确、正文与附件语义一致、业务逻辑正确或客户确认。
