# 知识基线验收

首先审阅 [业务主交付物](business-delivery.md)，再检查结构化附件。参考 [审阅方法](review-guide.md) 记录每项目标的具体落点、发现和未决项；工具结果不能替代业务验收。

## 四项目标

1. **概念正确：** 关键概念有业务定义、范围、实例、反例及相邻非同义；来源记载、现实事实和判断结论清楚分开；重要陈述可定位原文。作者推断、建议和未确认内容明确标记，争议没有被静默合并。
2. **业务可理解：** 说明书开头先用业务语言给出领域认知速览，讲清业务目标、核心概念导航、业务主线和主要判断；第一次接触该领域的业务读者无需先阅读版本演进、来源单元统计、候选问题清洗、JSON、内部枚举、物理字段或平台知识，就能说出“这个业务是做什么的、主要涉及什么、事情怎样展开”。正文不是字段表、术语表和抽象口号的堆积。
3. **认知机理可审查：** 每个高影响 Rule（业务规则）除适用范围、前提、条件、结果、例外、缺证处理、时间和依据外，还必须明确 business_conclusion、required_facts、decision_steps、evidence_requirements、non_sufficient_facts、unknown_behavior、human_boundary，并至少绑定一个可检验案例；每个业务问题能指向足够的规则/概念或明确 OPEN（未决）。计算说明口径和单位，规则冲突说明尚未裁定的影响。案例能解释为何成立、何时不成立，不能由生成规则循环证明自身正确。
4. **可用于需求访谈及确认：** 未决事项有具体问题、原文位置、候选口径、建议依据或不推荐的原因、业务影响、相关案例和责任角色。清单能够直接提问并记录真实答复；确认范围具体，变化可回到相关概念、规则和案例。

## 完整性与一致性

5. 创建或修订交付业务正文 `review.md`、审计附件 `coverage.md` 和结构化 `output.json`，八项业务内容齐备；`review.md` 的业务认知入口先于知识工程过程，来源覆盖、问题归并和编号索引不得成为理解业务的前置条件；只有技术附件、空模板、章节标题或表格占位不构成完成。审查模式则交付范围明确、定位准确、业务可读的审查意见，无需制造完整知识基线。
6. PRODUCE/REVISE 的用户请求以原始 documents 为入口；document-intake 必须保留原始文档字节摘要和 SourceBlock，document-normalizer 必须在这些块上形成 SourceUnit。明确结构由确定性规则处理；模糊边界使用 Jev Choice 并保存 BoundaryDecision。SourceBlock / SourceUnit 文本摘要一致，parser.input_digest 与原始 ArtifactRef 一致；每个保留 SourceBlock 必须且只能归属一个 SourceUnit，每个 BoundaryDecision 必须绑定相邻块并保存 selected/applied、概率、置信度、阈值和模型；低于阈值或明确 UNRESOLVED 时 SourceExtraction 必须为 PARTIAL；每个 SourceUnit 恰好对应一条 ProvisionCoverage。外部解析返回 `PARTIAL/FAILED`、不可读块或空内容时必须形成显式缺口；本技能不得把“解析响应已规范化”表述成“解析器正确恢复了全部原文”，也不得把“语义单元已重建”表述成“业务含义已确认”。
7. 案例覆盖以“是否能新增、修正或证伪知识”为准，不按每个问题机械要求四类案例。经确认真实案例、来源案例和合成探针的地位必须可区分；每个已交付案例具有事实、依据、判断解释、预期及禁止结果，合成案例标记清楚且不能循环自证。
8. Term（业务概念）、Rule（业务规则）、未决事项在业务正文有主要可读落点；Question（业务问题）承担导航和覆盖检查。逐条单元、陈述、全量案例和问题发现记录在审计附件有可读落点，与结构化附件双向一致。前提、比例、时间、例外、预期及禁止结果、确认状态不因改写而变化。
9. 来源的身份、版本、日期、位置和权威范围明确；来源有这句话不等于已采信。数据字典只能帮助核实业务含义，不成为概念模板。
10. 引用指向正确类型，推断前提可定位且不循环自证；冲突关联具体说法，未解决前行为明确；覆盖缺口诚实登记，不为使检查通过而编造内容。候选问题逐项保留去向和理由，流程补查不能由已有问题列表倒推充数。每个问题具有业务主题；父子引用有意义且无环。

每条覆盖记录同时说明材料映射和业务含义审查；原文摘录不计为完整含义提取。**Document Coverage（文档覆盖）与 Knowledge Coverage（知识覆盖）分开验收：全量 SourceBlock（来源块）有且仅有一个 SourceUnit（来源单元）归属、所有模糊边界均有可审计 BoundaryDecision 且不存在未解决边界、全量 SourceUnit 有覆盖记录，只证明材料处理范围和语义分段闭包，不证明业务问题已有答案。**局部深度审查可以交付，但剩余范围必须明确为未审或部分审查。


## Knowledge Formation 门禁

13. Statement Pass 必须逐 SourceUnit 给出去向；EXTRACTED 单元至少形成一条 Statement，非 EXTRACTED 单元不得偷偷携带陈述。Statement 的 source_ids 与 source_unit_ids 必须严格一致。
14. Question Discovery 必须分别保留 SOURCE 与 PROCESS 两条发现路径；不能从最终问题列表倒填。Question 合并不能吞掉独立前提、结果、证据、缺证和时间分支。
15. Knowledge Synthesis 必须区分 NORMATIVE / INTERPRETIVE / OPERATING_POLICY。fresh run 可以丢弃旧生成物，但不能丢弃已经作为 EXPERT_KNOWLEDGE / INSTITUTION_POLICY / CASE_EVIDENCE 正式输入的企业认知。
16. Knowledge Audit 必须逐 Rule 检查 Impact Calibration、Semantic Depth、Granularity、Counterfactual 与 Contradiction；任一 HIGH Rule 失败即阻断 assemble。当前这类“适用范围一句、判断一句、缺证一句”的高影响规则应被判为 SEMANTIC_DEPTH_INSUFFICIENT，而不是因为七字段非空就视为完整。
17. Case 必须说明来源和验证角色。SYNTHETIC_PROBE 不得提供 source authority，也不得循环证明生成它的 Rule。
18. Schema Complete 不等于 Knowledge Complete。高影响规则只有在业务专家无需重新阅读原始制度即可据此解释正常案例、边界案例和缺证案例时，才达到 Decision-Ready。

## 完成声明

11. 作者自查逐项记录正文位置、依据及限制。没有实际业务读者复述，不宣称已证明可理解；没有领域责任人确认，不宣称业务含义已获批准。自查、读者验证、领域确认分别报告。
12. 确认绑定具体业务事项和固定版本；答复缺失写待确认，不能把脚本通过、作者审查或其他智能体判断登记为客户确认。变更后重新确认受影响内容，不复用旧摘要下的批准。

说明书可作为待审草案交付，但关键定义、判断依据或案例缺口必须显著呈现。最终完成判断以五件事为核心：问题有去向；核心概念/规则有依据；规范知识与机构/专家口径未混写；关键歧义获必要确认；相关案例未明显推翻规则。SourceUnit 数量、候选问题数量、规则数量和合成案例数量都不是完成指标。
