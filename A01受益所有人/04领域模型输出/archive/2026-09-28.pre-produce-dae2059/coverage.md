# 受益所有人识别核心领域模型：覆盖与审计

模型 A01.DomainModel / 2026-09-24.practical-ubo-core.2；DSL 2.1.0；范围模式 EXPLICIT_SUBSET。

本表核对对应关系与实际证据，不以引用存在代替语义正确性。

## 问题覆盖

| 问题 | 状态 | 规则 | 流程 | 案例 | 模型 | 缺口 |
| --- | --- | --- | --- | --- | --- | --- |
| Q.A01.S13 | MODELED | RULE.A01.KF.EQUITY |  | CASE.A01.KF.EQUITY.B, CASE.A01.KF.SRC06.01 | M.OwnershipLink, M.EquityPath, M.CandidateAssessment, M.AssessOwnershipPaths, M.SumEquityPaths, M.MeetsEquityThreshold |  |
| Q.A01.S14 | MODELED | RULE.A01.KF.EQUITY |  | CASE.A01.KF.EQUITY.B, CASE.A01.KF.SRC06.01 | M.OwnershipLink, M.EquityPath, M.EquityPathStep, M.CandidateAssessment, M.AssessOwnershipPaths, M.SumEquityPaths, M.MeetsEquityThreshold |  |
| Q.A01.S16 | PARTIAL | RULE.A01.KF.NOMINEE |  | CASE.A01.KF.NOMINEE.B, CASE.A01.KF.SRC06.03 | M.OwnershipLink, M.OtherRight, M.ReviewCandidateEvidence | M.Gap.EvidenceConflict |
| Q.A01.S17 | MODELED | RULE.A01.KF.RETURNS_VOTES |  | CASE.A01.KF.RETURNS_VOTES.B, CASE.A01.KF.SRC06.02, CASE.A01.KF.SRC06.07 | M.OtherRight, M.CandidateAssessment, M.MeetsBenefitVoteThreshold |  |
| Q.A01.S18 | MODELED | RULE.A01.KF.RETURNS_VOTES |  | CASE.A01.KF.RETURNS_VOTES.B, CASE.A01.KF.SRC06.02, CASE.A01.KF.SRC06.07 | M.OtherRight, M.CandidateAssessment, M.MeetsBenefitVoteThreshold |  |
| Q.A01.S20 | MODELED | RULE.A01.KF.RETURNS_VOTES |  | CASE.A01.KF.RETURNS_VOTES.B, CASE.A01.KF.SRC06.02, CASE.A01.KF.SRC06.07 | M.CandidateAssessment, M.MeetsBenefitVoteThreshold, M.AssessActualControl |  |
| Q.A01.S21 | PARTIAL | RULE.A01.KF.CONTROL, RULE.A01.KF.NOMINEE |  | CASE.A01.KF.CONTROL.B, CASE.A01.KF.NOMINEE.B, CASE.A01.KF.SRC06.03, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | M.OtherRight, M.ControlArrangement, M.ReviewCandidateEvidence, M.AssessActualControl | M.Gap.EvidenceConflict |
| Q.A01.S22 | PARTIAL | RULE.A01.KF.CONTROL |  | CASE.A01.KF.CONTROL.B, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | M.ControlArrangement, M.AssessActualControl | M.Gap.EvidenceConflict |
| Q.A01.S23 | PARTIAL | RULE.A01.KF.CONTROL |  | CASE.A01.KF.CONTROL.B, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | M.ControlArrangement, M.AssessActualControl | M.Gap.EvidenceConflict |
| Q.A01.S24 | PARTIAL | RULE.A01.KF.CONTROL |  | CASE.A01.KF.CONTROL.B, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | M.ControlArrangement, M.AssessActualControl | M.Gap.EvidenceConflict |
| Q.A01.S25 | PARTIAL | RULE.A01.KF.CONTROL |  | CASE.A01.KF.CONTROL.B, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | M.ControlArrangement, M.AssessActualControl | M.Gap.EvidenceConflict |
| Q.A01.S26 | PARTIAL | RULE.A01.KF.CONTROL |  | CASE.A01.KF.CONTROL.B, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | M.ControlArrangement, M.AssessActualControl | M.Gap.EvidenceConflict |
| Q.A01.S28 | MODELED | RULE.A01.KF.FALLBACK |  | CASE.A01.KF.FALLBACK.B | M.CandidateAssessment, M.CandidatePopulationAssessment, M.ReviewCandidatePopulation, M.FallbackAvailable |  |
| Q.A01.S29 | MODELED | RULE.A01.KF.FALLBACK |  | CASE.A01.KF.FALLBACK.B | M.CandidatePopulationAssessment, M.ReviewCandidatePopulation, M.FallbackAvailable, M.SelectFallbackManager |  |
| Q.A01.S56 | PARTIAL | RULE.A01.KF.IDENTITY |  | CASE.A01.KF.IDENTITY.B | M.NaturalPerson, M.Evidence, M.ReviewCandidateEvidence | M.Gap.ProposedPolicy |
| Q.A01.S57 | PARTIAL | RULE.A01.KF.IDENTITY |  | CASE.A01.KF.IDENTITY.B | M.Evidence, M.CandidateAssessment, M.ReviewCandidateEvidence | M.Gap.ProposedPolicy |
| Q.A01.S60 | PARTIAL | RULE.A01.KF.DATES |  | CASE.A01.KF.DATES.B | M.CandidateAssessment, M.UBOQualification, M.OwnershipLink, M.OtherRight, M.ControlArrangement | M.Gap.DatedPublishing, M.Gap.EvidenceConflict |
| Q.A01.S61 | PARTIAL | RULE.A01.KF.DATES |  | CASE.A01.KF.DATES.B | M.CandidateAssessment, M.UBOQualification, M.OwnershipLink, M.OtherRight, M.ControlArrangement | M.Gap.DatedPublishing, M.Gap.EvidenceConflict |
| Q.A01.S62 | PARTIAL | RULE.A01.KF.DATES |  | CASE.A01.KF.DATES.B | M.CandidateAssessment, M.UBOQualification | M.Gap.DatedPublishing, M.Gap.EvidenceConflict |

## 逐条规则要素

### RULE.A01.KF.EQUITY

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S13, Q.A01.S14；缺口：

处理理由：权益边、穿透路径及判断时点是可复用结构；完整路径的最终比例和25%达标是稳定领域判断。路径完整性须由证据确认，不能由计算式自证。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 一般备案标准一；机构法人/非法人组织普通识别的第八条第一项 | M.OwnershipLink, M.EquityPath, M.CandidateAssessment | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 前提 | 备案标准一或金融机构第八条第一项；以一个目标主体、一个有效时点、一名最终自然人为计算对象。 | M.CandidateAssessment.as_of, M.CandidateAssessment.equity_path_status | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 判断条件 | 识别每一实际自然人和有效股权/合伙权益路径；直接比例计入，间接逐层依有效权益比例连乘，同一自然人的互异路径汇总；最终持有≥25%即符合（25%含本数），不把中间公司控制权自动换成100%权益。 | M.AssessOwnershipPaths.criteria, M.SumEquityPaths.expression, M.MeetsEquityThreshold.expression, M.ReviewCandidateEvidence.criteria | MIXED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 结果 | 同一自然人互异有效路径汇总的最终股权或合伙权益达到25%（含本数），按权益标准列入。 | M.CandidateAssessment.final_equity_percentage, M.CandidateAssessment.meets_standard1 | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 例外 | 缺上层登记、路径有重复计算/循环、协议改变实际权益归属时保持比例和身份 UNKNOWN，不将第三方直接比例当最终权益。 | M.CandidateAssessment.equity_path_status, M.ReviewCandidateEvidence.criteria | MANUAL | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 缺证处理 | 逐层、同一时点股东名册及章程/合伙协议、各边比例、生效材料、代持及受益转移约定；计算路径与去重过程。 | M.OwnershipLink.evidence, M.EquityPath.evidence, M.CandidateAssessment.evidence | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 时间要求 | 按交易/判断时点取有效路径；股权变更及终止按法律关系效力追踪。 | M.OwnershipLink.effective_from, M.OwnershipLink.end_status | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |

### RULE.A01.KF.NOMINEE

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S16, Q.A01.S21；缺口：M.Gap.EvidenceConflict

处理理由：名义持有和最终收益、表决、控制可指向不同自然人；须分别保留安排与证据，最终归属依协议效力和实际履行裁定。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 存在代持、隐名收益或亲属安排的法人/非法人组织 | M.OwnershipLink, M.OtherRight, M.ControlArrangement | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 前提 | 登记股东、协议受让方、收益/表决权享有人或真正决定者可能不是同一自然人。 | M.CandidateAssessment.as_of, M.Evidence.verification_state | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 判断条件 | 分开登记股东、股权最终所有人、收益权人、表决权人及实际控制人：核对代持协议的权利、履行和期间；若名义人不是最终拥有者，不能单凭工商份额认其为受益人；真实权利人按对应标准识别，不以亲属称谓自动转移权益。 | M.ReviewCandidateEvidence.criteria, M.AssessActualControl.criteria | MANUAL | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 结果 | 依已证实的实际权益、收益、表决和控制分离关系分别给出自然人结论；名义人仅在自身另有最终权利时列入。 | M.UBOQualification | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 例外 | 亲属关系、口头说法或单一登记均不能证明权利转移；未取得有效协议及履行证据时名义归属与最终归属保留冲突。 | M.Evidence.verification_state, M.ReviewCandidateEvidence.criteria | MANUAL | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 缺证处理 | 经核实的代持/收益/表决协议、权利生效和终止条款、分红及投票记录、相关方确认与独立资料。 | M.Evidence, M.ReviewCandidateEvidence.required_evidence | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 时间要求 | 协议效力与实际履行须对应本次判断日；历史名义记录不能覆盖已转移权益。 | M.OwnershipLink.effective_from, M.OtherRight.effective_from, M.ControlArrangement.effective_from | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |

### RULE.A01.KF.RETURNS_VOTES

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S17, Q.A01.S18, Q.A01.S20；缺口：

处理理由：最终收益权和表决权是独立的权利事实；在标准一未入选时，任一权利达到25%构成稳定判断，重复归类不能增加人数。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 一般标准二；仅针对未满足持有权益标准一的自然人 | M.OtherRight, M.CandidateAssessment | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 前提 | 仅在同一自然人未满足最终权益≥25%的标准一前提下，进一步判断标准二与三的适用；权益满足标准一者不重复归类标准二。 | M.CandidateAssessment.meets_standard1 | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 判断条件 | 先判是否已按最终权益≥25%符合标准一；未达者分别核对收益分配和表决权的有效来源、期限及比例，任何一项最终享有≥25%即按标准二；仅该人未满足标准一且同时有可证实实际控制时才须同时记录标准二和标准三关系，不将经济收益、表决委托和股权混为一谈。 | M.MeetsBenefitVoteThreshold.expression, M.ReviewCandidateEvidence.criteria | MIXED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 结果 | 未按权益标准入选但最终收益或表决权任一达到25%（含本数）的自然人，按标准二识别，控制关系另记。 | M.CandidateAssessment.meets_standard2, M.UBOQualification.qualification_basis | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 例外 | 只知股东原始比例、获利转账或委托意向不证明最终收益/表决比例；收益合同未生效或授权过期时不能按25%认定。 | M.OtherRight.right_kind, M.OtherRight.end_status, M.ReviewCandidateEvidence.criteria | MANUAL | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 缺证处理 | 收益分配/表决权协议、章程、可委托权种、有效期、分红凭证或决议/投票记录、受让人与对象对应。 | M.OtherRight.evidence, M.ReviewCandidateEvidence.criteria | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 时间要求 | 以各权利实际生效及终止日判断；既有标准一者不重复套仅限未达标准一的标准二。 | M.OtherRight.effective_from, M.OtherRight.end_status | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |

### RULE.A01.KF.CONTROL

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S21, Q.A01.S22, Q.A01.S23, Q.A01.S24, Q.A01.S25, Q.A01.S26；缺口：M.Gap.EvidenceConflict

处理理由：控制安排的权限、作用、共同机制和有效期间是稳定事实；是否构成实际控制属于需要证据裁定的领域判断。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 一般标准三，先分清自然人是否已按权益达到标准一 | M.ControlArrangement, M.CandidateAssessment | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 前提 | 对象是具体自然人而非公司、股东集团标签；需分别核对是否已达标准一及是否通过本人或联合机制实际支配目标。 | M.CandidateAssessment.as_of | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 判断条件 | 找出单独或联合对主体具有最终决定能力的自然人及协议/关系路径；分别核实其能否决定人事任免、重大经营管理决策、财务收支或长期支配重要资产/主要资金，判断的是对组织的实际控制能力，不是一次签字或职务名称；联合控制要说明每个人的权力与共同决策机制。 | M.AssessActualControl.criteria | MANUAL | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 结果 | 经证实单独或联合最终实际决定主体人事、重大决策、财务或重要财物的自然人，按实际控制标准识别。 | M.CandidateAssessment.meets_standard3, M.UBOQualification | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 例外 | 第一大股东、法定代表人、普通执行人、朋友/亲属关系和一次付款签名仅是线索；缺生效协议、决议、持续履行记录时实际支配为 UNKNOWN，不得因未发现股权人立即认定无控制。 | M.ControlArrangement.actual_exercise, M.CandidateAssessment.assessment_state, M.AssessActualControl.criteria | MANUAL | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 缺证处理 | 协议和章程中的权限、董事及重大决策记录、任免与预算授权、银行账户/重要资产长期支配事实、联合行动及实际行使证据。 | M.ControlArrangement.evidence, M.AssessActualControl.required_evidence | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 时间要求 | 实际控制形成及终止与协议生效和长期事实持续区间对应，不以后来的标签追溯历史。 | M.ControlArrangement.effective_from, M.ControlArrangement.end_status | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |

### RULE.A01.KF.FALLBACK

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S28, Q.A01.S29；缺口：

处理理由：候选全集完整性和前三项标准均无人符合是组织级事实；仅当前提明确成立，才能判断备位资格和实际管理人选。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 在按普通识别标准逐一核实之后确无满足三类自然人的主体 | M.CandidatePopulationAssessment, M.UBOQualification | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 前提 | 针对已取得完整所有权、收益/表决权与控制资料的同一主体及日期，原则上按一般三标准识别自然人。 | M.CandidatePopulationAssessment.search_complete, M.CandidatePopulationAssessment.any_qualifying_candidate | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 判断条件 | 逐项完成权益、收益/表决、实际控制的自然人查找；只有三项均确定不存在，才认定真实负责日常经营管理人员作为备位（指南要求至少一名最高层级日常管理人员）；备位是特定条件结果，不是实质自然人控制权的证明。 | M.FallbackAvailable.expression, M.SelectFallbackManager.criteria | MIXED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 结果 | 经查三项一般标准确实没有符合者，才将真实负责日常经营管理的人员按备位识别。 | M.SelectFallbackManager.criteria, M.UBOQualification.qualification_basis | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 例外 | 结构分支未追完、代持协议缺失或控制争议属 UNKNOWN 而不是三项 FALSE，不得因此直接填法定代表人兜底。 | M.CandidatePopulationAssessment.fallback_available, M.SelectFallbackManager.criteria | MANUAL | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 缺证处理 | 完整自然人候选及排除理由、章程/决议、经营管理职责、任职记录与实际履职证据。 | M.SelectFallbackManager.required_evidence, M.ReviewCandidatePopulation.required_evidence | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 时间要求 | 按判断日确认三项均不成立和管理者任职存续。 | M.CandidatePopulationAssessment.as_of, M.UBOQualification.effective_from | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |

### RULE.A01.KF.IDENTITY

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S56, Q.A01.S57；缺口：M.Gap.ProposedPolicy

处理理由：现实自然人身份、权利事实和各自证据必须分离；身份同一性及证据可靠性决定候选结论能否成立，字段齐全并不充分。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 机构一般客户身份与权利状况、经官方验证高透明度客户身份字段例外；备案字段另按2024年第3号令第十一条。 | M.NaturalPerson, M.CandidateAssessment | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 前提 | 一般非自然人客户的机构受益所有人识别与备案填报字段分开；机构透明客户具有第十八条特定较少身份字段例外，须先有官方透明性质核验证据。 | M.CandidateAssessment.target_organization, M.CandidateAssessment.as_of | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 判断条件 | 区分识别谁、为何及何时有权：一般客户留存自然人姓名、性别、国籍、出生日期、身份证明类别号码与有效期限、权利类型、比例/控制方式和形成终止时间；仅对上市及经官方核实的特定高透明国企客户，可按第十八条至少留姓名、性别、国籍、出生年月及可识别身份照片；身份优先官方渠道，不能用时身份证件及补充材料；权利以客户资料为基础并按风险核对官方、公开、机构发现信息。确属低风险才可采信客户权利信息；部分佐证足够时记录取舍理由。另外，备案主体按照2024年第3号令第十一条逐人填报经常居住地或工作单位地址、联系方式，及证件有效期限；该备案字段不与机构一般识别留存字段混同。 | M.ReviewCandidateEvidence.criteria | MANUAL | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 结果 | 逐人留存机构要求的身份、权利类型、比例或控制方式及有效时间，以风险相称可靠来源完成合理核实；备案另按第3号令第十一条填字段。 | M.CandidateAssessment.assessment_state, M.IdentificationConclusion | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 例外 | 仅客户自报、第三方股权比例或身份证复印件在可得官方独立渠道且有冲突时不足；信息字段齐全不代表权利已核实。 | M.Evidence.verification_state, M.ReviewCandidateEvidence.criteria | MANUAL | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 缺证处理 | 登记章程/合伙协议、股东董事及管理名单、有效身份件与官方核验、权利文件、日期、交叉核实及风险取舍记录。 | M.Evidence, M.ReviewCandidateEvidence.required_evidence | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 时间要求 | 资料与权利状态必须同一适用时点；缺生效日时不可自动填默认日。 | M.CandidateAssessment.as_of, M.OwnershipLink.effective_from | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |

### RULE.A01.KF.DATES

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S60, Q.A01.S61, Q.A01.S62；缺口：M.Gap.EvidenceConflict, M.Gap.DatedPublishing

处理理由：权利形成、变化、终止和判断时点属于关系本身的时间事实；首次达标与当前状态不可互相覆盖，未知精度不得补成具体日期。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 备案及机构识别的有效受益所有权关系 | M.CandidateAssessment, M.UBOQualification | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 前提 | 明确具体自然人、权利种类和目标主体，并区分原入选、当前比例变动与权利终止事件。 | M.CandidateAssessment.as_of, M.UBOQualification.first_qualified_precision | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 判断条件 | 分别记录首次跨入识别标准、当前权益比例或控制关系的形成、终止、登记披露、机构核实和备案日；法规要求的是法律关系生效的形成/终止时间；逐份看章程、转让、决议和控制权协议何时生效；未退出时增持可能改变当前比例的形成日，却不抹掉首次入选日；退出后重入需建立新的权利区间。 | M.AssessOwnershipPaths.criteria | MANUAL | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 结果 | 区分首次达到识别标准的日期、当前权利状态生效日及权利终止日，并另外保留披露、核实与备案日期。 | M.CandidateAssessment.first_qualified_on, M.UBOQualification.first_qualified_on, M.UBOQualification.effective_from | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 例外 | 工商变更登记日、客户查询日、最新增持日不必等于关系生效日；仅知月份不能系统自动补一日。 | M.UBOQualification.first_qualified_precision, M.UBOQualification.effective_from_precision, M.AssessOwnershipPaths.criteria | MANUAL | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 缺证处理 | 附生效条款的股权转让/控制协议、章程决议、批准条件完成证明、比例历史和权利终止文件。 | M.AssessOwnershipPaths.required_evidence | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |
| 时间要求 | 保留有效区间、精度及冲突；对历史交易按交易发生时证据与当时规则还原，不将当前人选追责历史。 | M.OwnershipLink.effective_from, M.OtherRight.effective_from, M.ControlArrangement.effective_from | FORMALIZED | 仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。 |

## 模型目录与依据

| 标识 | 名称 | 依据 |
| --- | --- | --- |
| M.Organization | 组织主体 | TERM.A01.KF.02, RULE.A01.KF.EQUITY |
| M.NaturalPerson | 自然人 | TERM.A01.KF.02, TERM.A01.KF.04, RULE.A01.KF.IDENTITY, RULE.A01.KF.CONTROL |
| M.Evidence | 识别证据 | RULE.A01.KF.EQUITY, RULE.A01.KF.NOMINEE, RULE.A01.KF.IDENTITY |
| M.OwnershipLink | 权益持有关系 | TERM.A01.KF.03, TERM.A01.KF.04, RULE.A01.KF.EQUITY, RULE.A01.KF.NOMINEE |
| M.EquityPath | 权益穿透路径 | RULE.A01.KF.EQUITY, RULE.A01.KF.DATES |
| M.EquityPathStep | 权益路径步骤 | RULE.A01.KF.EQUITY |
| M.OtherRight | 收益或表决权安排 | TERM.A01.KF.04, RULE.A01.KF.RETURNS_VOTES, RULE.A01.KF.NOMINEE |
| M.ControlArrangement | 实际控制安排 | TERM.A01.KF.05, RULE.A01.KF.CONTROL, RULE.A01.KF.NOMINEE |
| M.CandidateAssessment | 自然人识别评估 | TERM.A01.KF.02, TERM.A01.KF.03, TERM.A01.KF.04, TERM.A01.KF.05, TERM.A01.KF.06, RULE.A01.KF.EQUITY, RULE.A01.KF.RETURNS_VOTES, RULE.A01.KF.FALLBACK |
| M.CandidatePopulationAssessment | 组织级候选全集核查 | RULE.A01.KF.FALLBACK |
| M.IdentificationReviewer | 金融机构识别责任角色 | RULE.A01.KF.PROFILE, RULE.A01.KF.IDENTITY, RULE.A01.KF.RISK |
| M.UBOQualification | 受益所有权关系角色 | TERM.A01.KF.02, TERM.A01.KF.03, TERM.A01.KF.04, TERM.A01.KF.05, TERM.A01.KF.06, RULE.A01.KF.EQUITY, RULE.A01.KF.RETURNS_VOTES, RULE.A01.KF.CONTROL, RULE.A01.KF.FALLBACK |
| M.IdentificationConclusion | 受益所有人识别结论 | RULE.A01.KF.PROFILE, RULE.A01.KF.FALLBACK, RULE.A01.KF.IDENTITY, RULE.A01.KF.RISK |
| M.SumEquityPaths | 汇总同一自然人有效权益路径 | RULE.A01.KF.EQUITY |
| M.MeetsEquityThreshold | 权益比例达到25% | RULE.A01.KF.EQUITY |
| M.MeetsBenefitVoteThreshold | 收益/表决权标准达到25% | RULE.A01.KF.RETURNS_VOTES |
| M.FallbackAvailable | 三项一般标准均确定不成立 | RULE.A01.KF.FALLBACK |
| M.AssessOwnershipPaths | 核验并计算权益穿透路径 | TERM.A01.KF.02, TERM.A01.KF.03, TERM.A01.KF.04, TERM.A01.KF.05, TERM.A01.KF.06, TERM.A01.KF.07, TERM.A01.KF.09, TERM.A01.KF.10, TERM.A01.KF.13, RULE.A01.KF.EQUITY, RULE.A01.KF.DATES |
| M.ReviewCandidateEvidence | 核实自然人身份与权利证据 | TERM.A01.KF.02, TERM.A01.KF.03, TERM.A01.KF.04, TERM.A01.KF.05, TERM.A01.KF.06, TERM.A01.KF.07, TERM.A01.KF.09, TERM.A01.KF.10, TERM.A01.KF.13, RULE.A01.KF.IDENTITY, RULE.A01.KF.NOMINEE |
| M.ReviewCandidatePopulation | 核定组织级候选全集及备位前提 | TERM.A01.KF.02, TERM.A01.KF.03, TERM.A01.KF.04, TERM.A01.KF.05, TERM.A01.KF.06, TERM.A01.KF.07, TERM.A01.KF.09, TERM.A01.KF.10, TERM.A01.KF.13, RULE.A01.KF.FALLBACK |
| M.AssessActualControl | 裁定实际控制 | TERM.A01.KF.02, TERM.A01.KF.03, TERM.A01.KF.04, TERM.A01.KF.05, TERM.A01.KF.06, TERM.A01.KF.07, TERM.A01.KF.09, TERM.A01.KF.10, TERM.A01.KF.13, RULE.A01.KF.CONTROL |
| M.SelectFallbackManager | 选择备位日常管理人员 | TERM.A01.KF.02, TERM.A01.KF.03, TERM.A01.KF.04, TERM.A01.KF.05, TERM.A01.KF.06, TERM.A01.KF.07, TERM.A01.KF.09, TERM.A01.KF.10, TERM.A01.KF.13, RULE.A01.KF.FALLBACK |
| M.Constraint.OwnershipHolderMatchesKind | 权益持有人类别与引用一致 | RULE.A01.KF.EQUITY |
| M.Constraint.OwnershipDatePrecision | 权利生效日期精度与日期值一致 | RULE.A01.KF.DATES |
| M.Constraint.OtherRightDatePrecision | 权利生效日期精度与日期值一致 | RULE.A01.KF.DATES |
| M.Constraint.ControlDatePrecision | 权利生效日期精度与日期值一致 | RULE.A01.KF.DATES |
| M.Constraint.CandidateEquityConsistent | 权益阈值输入必须等于完整有效路径之和 | RULE.A01.KF.EQUITY |
| M.Gap.EvidenceConflict | 具体客户的代持效力、最终权利归属或实际控制证据可能冲突；未取得并核对案件材料前，不确认受影响自然人及关系形成时点。 |  |
| M.Gap.DatedPublishing | 上游备案期限事项与权利形成日规则共享来源陈述，合同要求继续追溯；备案期限本身不进入本模型，也不改变权利生效日的判断。 |  |
| M.Gap.ProposedPolicy | 业务讨论要求保留日期精度、缺证状态、证据链与人工复核，但未提供机构或专家正式作业来源，不可把设计建议写成普遍强制细则。 |  |
| M.Gap.OutOfSubsetKnowledgeIssues | 其余上游OPEN事项已逐项登记，但只影响本次明确排除的备案办理、信托/资管产品、BOMIS、差异报告或其他范围，不在本模型内解决。 |  |

## 全部业务字段

### M.Organization / 组织主体

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| registration_identifier | 登记识别号 | Text | 必须一项 | 官方登记或设立文件中的稳定主体识别号。缺失时不能虚构组织身份。 |
| jurisdiction | 登记/设立法域 | Text | 必须一项 | 该组织登记或依法设立的法域，用于解释组织身份及证据适用范围。 |
| official_name | 法定名称 | Text | 必须一项 | 与判断时点相符的登记或设立文件名称。 |
| supporting_evidence | 组织身份依据 | Ref → M.Evidence | 至少 1 项，不限最多数量 | 登记、设立、产权、章程或治理依据。 |

### M.NaturalPerson / 自然人

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| document_kind | 身份证明类别 | Text | 必须一项 | 官方核验或有效身份证明所载类别。 |
| document_number | 身份证明号码 | Text | 必须一项 | 与签发法域共同用于识别个人的号码。 |
| issuer | 签发国家或地区 | Text | 必须一项 | 身份证明签发国家或地区。 |
| name | 姓名 | Text | 必须一项 | 自然人姓名；同名不能作为合并身份的依据。 |
| gender | 性别 | Text | 可有一项；缺失时保留未知 | 金融机构一般客户识别所需身份信息。 |
| nationality | 国籍/地区 | Text | 可有一项；缺失时保留未知 | 金融机构一般客户识别所需身份信息。 |
| birth_date | 出生日期 | Date | 可有一项；缺失时保留未知 | 金融机构一般客户识别所需身份信息。 |
| document_expiry | 证件有效期限 | Date | 可有一项；缺失时保留未知 | 所用身份证明的有效期限；过期不自动抹除历史身份。 |

### M.Evidence / 识别证据

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| source_reference | 来源记录标识 | Text | 必须一项 | 来源文件、官方查询或客户原始材料的可回溯标识。 |
| locator | 材料位置 | Text | 必须一项 | 页码、条款、登记记录或查询结果位置。 |
| claim | 支持的事实 | Text | 必须一项 | 该材料实际支持的身份、权利、时间或风险事实，不超出来源内容。 |
| source_authority | 来源性质 | Enum | 可有一项；缺失时保留未知 | 来源类型不是可靠性结论。 |
| verification_state | 核实状态 | Enum | 可有一项；缺失时保留未知 | 记录材料核实结果；UNVERIFIED不得视作已证实。 |
| issued_on | 材料出具日 | Date | 可有一项；缺失时保留未知 | 来源材料被出具的日期，不自动视为权利生效日。 |
| obtained_on | 材料取得日 | Date | 可有一项；缺失时保留未知 | 金融机构取得该材料的日期。 |
| verified_on | 机构核实日 | Date | 可有一项；缺失时保留未知 | 机构完成该材料核实的日期；不替代权利形成日。 |
| disclosed_on | 对外披露日 | Date | 可有一项；缺失时保留未知 | 来源事实对外披露的日期；不替代法律关系生效日。 |
| applicable_period | 材料适用期间 | Text | 可有一项；缺失时保留未知 | 描述材料所支持事实的时点或期间；不得把材料日期直接替代权利生效日。 |

### M.OwnershipLink / 权益持有关系

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| target_organization | 被投资/持有权益的组织 | Ref → M.Organization | 必须一项 | 路径中接受该段权益的组织。 |
| holder_kind | 持有人类别 | Enum | 必须一项 | 每条关系边只有一个持有人类别。 |
| holder_organization | 持有人组织 | Ref → M.Organization | 可有一项；缺失时保留未知 | 当 holder_kind 为 ORGANIZATION 时填写。 |
| holder_person | 持有人自然人 | Ref → M.NaturalPerson | 可有一项；缺失时保留未知 | 当 holder_kind 为 NATURAL_PERSON 时填写。 |
| share_class | 权益类别 | Text | 必须一项 | 能够区分同一双方之间不同权益安排的业务类别。 |
| relationship_reference | 权益关系依据标识 | Text | 必须一项 | 来源文件/登记权利关系中的稳定引用；无依据不构造事实边。 |
| percentage | 本段权益比例 | Decimal | 必须一项 | 以百分比数值表示，例如25表示25%；缺失不得按零处理。 |
| effective_from | 本段关系精确生效日 | Date | 可有一项；缺失时保留未知 | 仅在可证实精确法律生效日时填写；登记或查询日期不能代替。 |
| effective_from_precision | 生效时点精度 | Enum | 必须一项 | 按来源保留精度；非EXACT不得伪造具体日。 |
| effective_from_period_note | 生效期间说明 | Text | 可有一项；缺失时保留未知 | 仅知月份/年份/区间时记录对应来源描述。 |
| effective_to | 本段关系终止日 | Date | 可有一项；缺失时保留未知 | 有证据时记录终止日；未知或未终止与OPEN状态分别处理。 |
| end_status | 关系终止状态 | Enum | 必须一项 | OPEN表示有依据确认仍持续；UNKNOWN表示无法判断是否终止。 |
| evidence | 持有关系证据 | Ref → M.Evidence | 至少 1 项，不限最多数量 | 支持持有人、比例和期间的材料。 |

### M.EquityPath / 权益穿透路径

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| target_organization | 目标组织 | Ref → M.Organization | 必须一项 | 路径终点组织。 |
| person | 最终自然人 | Ref → M.NaturalPerson | 必须一项 | 路径起点自然人。 |
| as_of | 路径判断时点 | Date | 必须一项 | 所有路径边按同一时点筛选。 |
| path_key | 路径标识 | Text | 必须一项 | 区分同一人到同一组织的不同关系路径。 |
| steps | 有序路径步骤 | Ref → M.EquityPathStep | 至少 1 项，不限最多数量 | 按 step_order 排序，每步引用一条权益边。 |
| path_percentage | 单路径权益贡献 | Decimal | 可有一项；缺失时保留未知 | 路径边逐段相乘后的比例贡献，例如30表示30%。 |
| path_status | 路径状态 | Enum | 必须一项 | 不完整、循环或冲突路径不按零计入。 |
| evidence | 路径核验证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 支持路径中各边及期间的来源材料。 |

### M.EquityPathStep / 权益路径步骤

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| path | 所属路径 | Ref → M.EquityPath | 必须一项 | 对应的单条权益路径。 |
| ownership_link | 权益关系边 | Ref → M.OwnershipLink | 必须一项 | 该步骤采用的已核权益边。 |
| step_order | 路径顺序 | Integer | 必须一项 | 从自然人一侧到目标组织一侧的正整数顺序。 |

### M.OtherRight / 收益或表决权安排

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| target_organization | 目标组织 | Ref → M.Organization | 必须一项 | 发生收益或表决权关系的组织。 |
| person | 权利自然人 | Ref → M.NaturalPerson | 必须一项 | 收益或表决权最终归属/行使的自然人。 |
| right_kind | 权利类型 | Enum | 必须一项 | 收益与表决是不同权利，不得混同。 |
| arrangement_reference | 权利安排依据标识 | Text | 必须一项 | 协议、章程或权利来源中的稳定引用。 |
| percentage | 最终权利比例 | Decimal | 必须一项 | 按最终权利计算的百分比，25含本数；缺失保持UNKNOWN。 |
| effective_from | 权利精确生效日 | Date | 可有一项；缺失时保留未知 | 仅在证据支持精确法律生效日时填写。 |
| effective_from_precision | 生效时点精度 | Enum | 必须一项 | 按来源保留精度，不能自动补月首或年初。 |
| effective_from_period_note | 生效期间说明 | Text | 可有一项；缺失时保留未知 | 记录非精确生效期间及其来源。 |
| effective_to | 权利终止日 | Date | 可有一项；缺失时保留未知 | 有证据时填写，不能以材料更新时间替代。 |
| end_status | 权利终止状态 | Enum | 必须一项 | 区分仍有效与终止状态未知。 |
| evidence | 权利安排证据 | Ref → M.Evidence | 至少 1 项，不限最多数量 | 协议、章程、实际分配/投票记录及核验材料。 |

### M.ControlArrangement / 实际控制安排

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| target_organization | 目标组织 | Ref → M.Organization | 必须一项 | 被支配或共同控制的组织。 |
| person | 控制候选人 | Ref → M.NaturalPerson | 必须一项 | 被评估是否实际控制的自然人。 |
| control_domain | 支配领域 | Enum | 必须一项 | 分别记录人事、重大决策、财务、重要资产/主要资金或联合控制。 |
| arrangement_reference | 控制安排依据标识 | Text | 必须一项 | 有效协议、章程或治理决议中的稳定关系引用。 |
| decision_power | 具体支配能力 | Text | 必须一项 | 具体事项、权限来源和该人如何影响组织决定。 |
| actual_exercise | 实际作用证据摘要 | Text | 可有一项；缺失时保留未知 | 区分有效权限与持续/真实行使；仅职位或签字不充分。 |
| joint_group | 联合机制说明 | Text | 可有一项；缺失时保留未知 | 仅共同控制时说明共同机制和该自然人自身权限。 |
| effective_from | 安排精确生效日 | Date | 可有一项；缺失时保留未知 | 仅在证据支持精确法律生效日时填写。 |
| effective_from_precision | 生效时点精度 | Enum | 必须一项 | 非精确日保留原有精度，不以披露/核实日替代。 |
| effective_from_period_note | 生效期间说明 | Text | 可有一项；缺失时保留未知 | 记录来源支持的月份、年份或区间。 |
| effective_to | 安排终止日 | Date | 可有一项；缺失时保留未知 | 有证据时填写。 |
| end_status | 安排终止状态 | Enum | 必须一项 | 未知不得表示为已经结束。 |
| evidence | 控制安排证据 | Ref → M.Evidence | 至少 1 项，不限最多数量 | 协议、任免、决策、预算、资产支配和长期实际行使证据。 |

### M.CandidateAssessment / 自然人识别评估

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| target_organization | 目标组织 | Ref → M.Organization | 必须一项 | 本次识别对象。 |
| person | 被评估自然人 | Ref → M.NaturalPerson | 必须一项 | 身份已核实或作为待核候选的自然人。 |
| as_of | 判断时点 | Date | 必须一项 | 所有权益和控制事实均对应的同一判断时点。 |
| first_qualified_on | 首次达标法律生效日 | Date | 可有一项；缺失时保留未知 | 该自然人首次达到任一一般识别标准的法律关系生效日；具体依据仍以受益所有权关系区分。 |
| first_qualified_precision | 首次达标日期精度 | Enum | 必须一项 | 只保留来源支持的精度，不用月首或年初补造具体日。 |
| first_qualified_period_note | 首次达标期间说明 | Text | 可有一项；缺失时保留未知 | 日期非精确时记录来源支持的月份、年份或区间。 |
| final_equity_percentage | 最终权益比例 | Decimal | 可有一项；缺失时保留未知 | 直接及有效间接路径在同一人层面的合计百分比；路径不完整或有循环争议时必须为UNKNOWN。 |
| final_benefit_percentage | 最终收益权比例 | Decimal | 可有一项；缺失时保留未知 | 最终收益权比例；不能从单笔分配金额臆算。 |
| final_voting_percentage | 最终表决权比例 | Decimal | 可有一项；缺失时保留未知 | 生效授权范围对应的最终表决权比例。 |
| equity_path_status | 权益路径状态 | Enum | 必须一项 | 路径完整性及循环/交叉关系状态。 |
| equity_paths | 权益穿透路径 | Ref → M.EquityPath | 至少 0 项，不限最多数量 | 逐条说明路径边、乘积和贡献，作为最终比例的审计依据。 |
| meets_standard1 | 符合权益标准 | Boolean | 可有一项；缺失时保留未知 | 由最终权益比例与25%含本数规则得出；缺失比例按UNKNOWN传播。 |
| meets_standard2 | 符合收益/表决标准 | Boolean | 可有一项；缺失时保留未知 | 仅在不符合标准一时，依据最终收益权或表决权任一达到25%判断。 |
| meets_standard3 | 符合实际控制标准 | Boolean | 可有一项；缺失时保留未知 | 由人工依据具体支配能力、实际作用和证据形成；未知不能记为否。 |
| ownership_links | 权益关系边 | Ref → M.OwnershipLink | 至少 0 项，不限最多数量 | 用于解释直接及间接路径，不代表已经完成图遍历。 |
| other_rights | 收益/表决关系 | Ref → M.OtherRight | 至少 0 项，不限最多数量 | 按权利类型和有效期间分别引用。 |
| control_arrangements | 控制安排 | Ref → M.ControlArrangement | 至少 0 项，不限最多数量 | 支持实际控制人工评估的事实。 |
| evidence | 候选评估证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 支持身份、权益、收益/表决及控制事实的来源材料。 |
| assessment_state | 评估状态 | Enum | 必须一项 | 区分评估进度与业务结论；有缺口不得标为SUPPORTED。 |

### M.CandidatePopulationAssessment / 组织级候选全集核查

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| target_organization | 目标组织 | Ref → M.Organization | 必须一项 | 候选全集对应的客户组织。 |
| as_of | 判断时点 | Date | 必须一项 | 候选全集和权利状态所对应的日期。 |
| candidate_assessments | 逐人评估 | Ref → M.CandidateAssessment | 至少 0 项，不限最多数量 | 包括所有入选、排除和待核候选。 |
| search_complete | 候选与路径核查是否穷尽 | Boolean | 可有一项；缺失时保留未知 | 只有全部相关权益、收益/表决和控制路径均已核对才为TRUE。 |
| any_qualifying_candidate | 是否存在满足一般标准者 | Boolean | 可有一项；缺失时保留未知 | 全部候选均评估后判定；全集不完整时保持UNKNOWN。 |
| fallback_available | 组织级备位前提 | Boolean | 可有一项；缺失时保留未知 | 只有全集穷尽且不存在任何符合一般标准者时才为TRUE。 |
| evidence | 全集与排除依据 | Ref → M.Evidence | 至少 1 项，不限最多数量 | 证明候选搜索完整性和逐人入选/排除结论。 |
| reviewer | 责任人员 | Ref → M.IdentificationReviewer | 必须一项 | 由金融机构责任人员核定候选全集完整性。 |

### M.IdentificationReviewer / 金融机构识别责任角色

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| person | 承担职责的自然人 | Ref → M.NaturalPerson | 必须一项 | 具体人员须在业务记录中有真实身份。 |
| institution | 金融机构 | Ref → M.Organization | 必须一项 | 该人员承担识别职责的机构。 |
| assigned_function | 职责范围 | Text | 必须一项 | 记录经办/复核职责来源；本模型不规定机构岗位名称或内部审批权限。 |

### M.UBOQualification / 受益所有权关系角色

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| person | 受益所有人自然人 | Ref → M.NaturalPerson | 必须一项 | 角色承担者必须是自然人。 |
| target_organization | 目标组织 | Ref → M.Organization | 必须一项 | 受益所有权所指向的组织。 |
| qualification_basis | 识别依据 | Enum | 必须一项 | 同一自然人可以有多个有证据支持的识别依据；备位仅在三项标准均确定不成立时使用。 |
| first_qualified_on | 首次达标法律生效日 | Date | 可有一项；缺失时保留未知 | 保留第一次达到标准的时点，不因比例变更而覆盖。 |
| first_qualified_precision | 首次达标日期精度 | Enum | 必须一项 | 按证据保留精度，不推定具体日。 |
| first_qualified_period_note | 首次达标期间说明 | Text | 可有一项；缺失时保留未知 | 精度不是EXACT时描述来源支持的期间。 |
| effective_from | 当前权利状态生效日 | Date | 可有一项；缺失时保留未知 | 当前比例/控制方式对应的法律生效日；不能用登记日替代。 |
| effective_from_precision | 当前权利日期精度 | Enum | 必须一项 | 仅使用来源支持的日期精度。 |
| effective_period_note | 当前权利期间说明 | Text | 可有一项；缺失时保留未知 | 说明当前权利状态的期间或日期证据缺口。 |
| effective_to | 关系终止日 | Date | 可有一项；缺失时保留未知 | 有证据时记录。 |
| end_status | 关系终止状态 | Enum | 必须一项 | 未知不等于持续，也不等于终止。 |
| candidate_assessment | 自然人评估 | Ref → M.CandidateAssessment | 必须一项 | 连接比例、控制判断和判断时点。 |
| evidence | 关系证据 | Ref → M.Evidence | 至少 1 项，不限最多数量 | 支持身份、权利和期间的来源材料。 |

### M.IdentificationConclusion / 受益所有人识别结论

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| target_organization | 识别对象 | Ref → M.Organization | 必须一项 | 受益所有人识别的目标组织。 |
| as_of | 判断时点 | Date | 必须一项 | 本结论覆盖的客户关系时点。 |
| result_state | 结果完整性 | Enum | 必须一项 | COMPLETE仅表示本范围内人选及必要关系均有足够依据，不表示业务批准。 |
| qualifications | 已支持的受益所有权关系 | Ref → M.UBOQualification | 至少 0 项，不限最多数量 | 逐人列明权利标准与有效区间。 |
| candidate_assessments | 候选评估 | Ref → M.CandidateAssessment | 至少 0 项，不限最多数量 | 包含已入选和未能排除的候选。 |
| candidate_population | 组织级候选全集 | Ref → M.CandidatePopulationAssessment | 可有一项；缺失时保留未知 | 是否穷尽候选及可否启用备位的组织级依据。 |
| unresolved_items | 未决事项 | Text | 至少 0 项，不限最多数量 | 逐项说明缺证、冲突或未确定的路由，并注明受影响结论。 |
| reviewer | 识别责任角色 | Ref → M.IdentificationReviewer | 必须一项 | 金融机构有权尽调人员；本模型不规定准入/授信/报告审批岗位。 |


## 字段绑定与依赖

### M.SumEquityPaths / 汇总同一自然人有效权益路径

前序规则：

输出字段：M.CandidateAssessment.final_equity_percentage

表达式：若 ((path_status = "COMPLETE") 且 全部为真(从 去重(paths) 中逐项取 path，满足 true，得到 (path.path_status = "VALID")))，则 求和(从 去重(paths) 中逐项取 path，满足 true，得到 path.path_percentage)，否则 null

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| paths | 互异权益路径 | Ref | M.CandidateAssessment.equity_paths |
| path_status | 整体路径状态 | Enum | M.CandidateAssessment.equity_path_status |

### M.MeetsEquityThreshold / 权益比例达到25%

前序规则：M.SumEquityPaths

输出字段：M.CandidateAssessment.meets_standard1

表达式：若 (path_status = "COMPLETE")，则 (equity_percentage ≥ 25)，否则 null

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| equity_percentage | 最终权益比例（百分比） | Decimal | M.CandidateAssessment.final_equity_percentage |
| path_status | 整体路径状态 | Enum | M.CandidateAssessment.equity_path_status |

### M.MeetsBenefitVoteThreshold / 收益/表决权标准达到25%

前序规则：M.MeetsEquityThreshold

输出字段：M.CandidateAssessment.meets_standard2

表达式：若 meets_standard1，则 false，否则 ((benefit_percentage ≥ 25) 或 (voting_percentage ≥ 25))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| meets_standard1 | 已符合权益标准 | Boolean | M.CandidateAssessment.meets_standard1 |
| benefit_percentage | 最终收益权比例 | Decimal | M.CandidateAssessment.final_benefit_percentage |
| voting_percentage | 最终表决权比例 | Decimal | M.CandidateAssessment.final_voting_percentage |

### M.FallbackAvailable / 三项一般标准均确定不成立

前序规则：

输出字段：M.CandidatePopulationAssessment.fallback_available

表达式：((search_complete = true) 且 (any_qualifying = false))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| search_complete | 组织级候选及路径已穷尽 | Boolean | M.CandidatePopulationAssessment.search_complete |
| any_qualifying | 存在满足一般标准者 | Boolean | M.CandidatePopulationAssessment.any_qualifying_candidate |

## 案例对应

| 案例 | 标题 | 模型 | 解释状态 | 执行状态 | 验证证据 |
| --- | --- | --- | --- | --- | --- |
| CASE.A01.KF.EQUITY.B | 路径法律效力与受益人本人相同才可相加；改变一条路径的有效期间让标准一结论反转。 | M.AssessOwnershipPaths, M.CandidateAssessment, M.EquityPath, M.EquityPathStep, M.MeetsEquityThreshold, M.OwnershipLink, M.SumEquityPaths | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.NOMINEE.B | 本案改变的是权利让渡真实性和效力证据；名义产权与最终权利的认定分别独立。 | M.AssessActualControl, M.CandidateAssessment, M.ControlArrangement, M.OtherRight, M.OwnershipLink, M.ReviewCandidateEvidence | BLOCKED | NOT_EXECUTED |  |
| CASE.A01.KF.RETURNS_VOTES.B | 权益资格先于标准二；委托效力改变表决权结果，重大事项支配缺失阻断标准三。 | M.CandidateAssessment, M.MeetsBenefitVoteThreshold, M.OtherRight | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.CONTROL.B | 决定权及可见行使是控制的核心事实；仅操作执行而不能决定结果不满足同一标准。 | M.AssessActualControl, M.CandidateAssessment, M.ControlArrangement, M.OtherRight, M.OwnershipLink, M.ReviewCandidateEvidence | BLOCKED | NOT_EXECUTED |  |
| CASE.A01.KF.FALLBACK.B | 决定备位的必要前提是三个标准全部为FALSE，而非有UNKNOWN；补证把未知转成否定才进入备位。 | M.CandidateAssessment, M.CandidatePopulationAssessment, M.FallbackAvailable, M.ReviewCandidatePopulation, M.SelectFallbackManager | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.IDENTITY.B | 证实法定透明客户身份会改变可留存的身份信息最小范围，不改变权利合理核实义务。 | M.CandidateAssessment, M.Evidence, M.NaturalPerson, M.ReviewCandidateEvidence | BLOCKED | NOT_EXECUTED |  |
| CASE.A01.KF.DATES.B | 是否中途退出决定原入选区间是否连续；登记公示是另一类日期。 | M.AssessOwnershipPaths, M.CandidateAssessment, M.ControlArrangement, M.OtherRight, M.OwnershipLink, M.UBOQualification | BLOCKED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.01 | 指南示例4分别展示甲30%、乙21%、丙两路径31.5%和丁17.5%；先乘每段有效权益，再把同一自然人丙的14%与17.5%相加，不能将中间公司持股70%整体归丙。本例仅校准标准一，不排除其他标准。 原始定位：SRC.SRC06.U0067、SRC.SRC06.U0069、SRC.SRC06.U0070、SRC.SRC06.U0071。 | M.AssessOwnershipPaths, M.CandidateAssessment, M.EquityPath, M.EquityPathStep, M.MeetsEquityThreshold, M.OwnershipLink, M.SumEquityPaths | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.02 | 指南图2把四个自然人置于不同权利来源：甲乙按直接股权、丙按最终收益、丁按实际控制；即使前两人的名单完整，也不能遗漏无股权的丙丁。该示例假设事实不证明任何现实客户。 原始定位：SRC.SRC06.U0051、SRC.SRC06.U0052。 | M.CandidateAssessment, M.MeetsBenefitVoteThreshold, M.OtherRight | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.03 | 指南示例9在‘甲名义持有、丙经亲属实际获益控制’明确前提下，区分乙30%股权、丙控制和甲名义70%；现实必须另证明名义与实质分离，不能单凭亲子关系复制结论。 原始定位：SRC.SRC06.U0098、SRC.SRC06.U0099。 | M.AssessActualControl, M.CandidateAssessment, M.ControlArrangement, M.OtherRight, M.OwnershipLink, M.ReviewCandidateEvidence | BLOCKED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.04 | 指南示例7给了甲5%持股以及有效协议共同决定任免和重大经营决策的事实，两者联合支持实际控制；若只剩5%股权而协议和支配事实不存在，不再能从该示例推出控制。 原始定位：SRC.SRC06.U0094。 | M.AssessActualControl, M.CandidateAssessment, M.ControlArrangement, M.OtherRight, M.OwnershipLink, M.ReviewCandidateEvidence | BLOCKED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.05 | 指南示例12重心并非普通合伙人甲只出资1%，而是其对人事、财务和投资具有实际决定能力；删除决定能力只保留GP头衔时，标准三结论不再有支撑。 原始定位：SRC.SRC06.U0114。 | M.AssessActualControl, M.CandidateAssessment, M.ControlArrangement, M.OtherRight, M.OwnershipLink, M.ReviewCandidateEvidence | BLOCKED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.07 | 指南示例10中甲股权不满足标准一、51%表决协议有效且能决定任免和重大决策，因两种独立权利同时满足标准二和标准三；如仅有51%表决而无实际决定能力，只支持标准二。 原始定位：SRC.SRC06.U0104、SRC.SRC06.U0105。 | M.CandidateAssessment, M.MeetsBenefitVoteThreshold, M.OtherRight | EXPLAINED | NOT_EXECUTED |  |

## 上游未决事项

| 知识事项 | 模型事项 | 处理 | 说明 |
| --- | --- | --- | --- |
| ISSUE.A01.KF.EVIDENCE_CONFLICT | M.Gap.EvidenceConflict | DEFERRED | 该未决事项直接影响本次显式子集的识别规则/问题，按原状态保留，不在模型阶段关闭。 |
| ISSUE.A01.KF.DATED_PUBLISHING | M.Gap.DatedPublishing | DEFERRED | 该未决事项直接影响本次显式子集的识别规则/问题，按原状态保留，不在模型阶段关闭。 |
| ISSUE.A01.KF.PROPOSED_POLICY | M.Gap.ProposedPolicy | DEFERRED | 该未决事项直接影响本次显式子集的识别规则/问题，按原状态保留，不在模型阶段关闭。 |
| ISSUE.A01.KF.CROSSMONTH_GUIDANCE | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.CROSS_BORDER | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DATE_AUTHORITY | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DIFFERENCE_CROSSMONTH | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT051.U00065.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT052.U00064.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT063.U00039.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT063.U00041.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00016.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00017.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00028.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00040.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00052.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00063.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00073.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00076.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00080.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT065.U00015.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00006.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00006.002 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00015.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00019.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00021.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT068.U00023.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT068.U00025.001 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.ST.TXT021.U00031.01 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT058.U00014.S01 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT059.U00016.S01 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT062.U00014.S01 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT062.U00022.S01 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT066.U00016.S01 | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.FX_CONVERSION | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.INSTITUTION_AUTHORITY | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.INSTITUTION_GOVERNANCE | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.OPTION_CLASSIFICATION | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.REPORT_DETAILS | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.SOURCE_PRECEDENCE | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.STATE_CONTROL_SCOPE | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.SYSTEM_QUERY_STATE | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.UNREADABLE_FIGURE | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |
| ISSUE.A01.KF.UNREADABLE_UNITS | M.Gap.OutOfSubsetKnowledgeIssues | NOT_APPLICABLE | 经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。 |

## 模型问题

| 标识 | 状态 | 问题 | 影响 | 责任 | 解决前处理 |
| --- | --- | --- | --- | --- | --- |
| M.Gap.EvidenceConflict | OPEN | 具体客户的代持效力、最终权利归属或实际控制证据可能冲突；未取得并核对案件材料前，不确认受影响自然人及关系形成时点。 | ISSUE.A01.KF.EVIDENCE_CONFLICT, RULE.A01.KF.NOMINEE, RULE.A01.KF.CONTROL, RULE.A01.KF.DATES, Q.A01.S16, Q.A01.S21, Q.A01.S22, Q.A01.S23, Q.A01.S24, Q.A01.S25, Q.A01.S26, Q.A01.S60, Q.A01.S61, Q.A01.S62 | 经办机构与客户 | 仅输出已证实部分，争议人选和时间标不足证据/冲突。 |
| M.Gap.DatedPublishing | OPEN | 上游备案期限事项与权利形成日规则共享来源陈述，合同要求继续追溯；备案期限本身不进入本模型，也不改变权利生效日的判断。 | ISSUE.A01.KF.DATED_PUBLISHING, RULE.A01.KF.DATES, Q.A01.S60, Q.A01.S61, Q.A01.S62 | 备案主体及法规维护人 | 备案期限保持上游OPEN；不得把登记、披露或备案日替代权利形成日。 |
| M.Gap.ProposedPolicy | OPEN | 业务讨论要求保留日期精度、缺证状态、证据链与人工复核，但未提供机构或专家正式作业来源，不可把设计建议写成普遍强制细则。 | ISSUE.A01.KF.PROPOSED_POLICY, RULE.A01.KF.IDENTITY, Q.A01.S56, Q.A01.S57 | 业务负责人和机构授权制度负责人 | 仅保留法规义务与业务范围提示，设计建议不升格为作业政策。 |
| M.Gap.OutOfSubsetKnowledgeIssues | OPEN | 其余上游OPEN事项已逐项登记，但只影响本次明确排除的备案办理、信托/资管产品、BOMIS、差异报告或其他范围，不在本模型内解决。 | ISSUE.A01.KF.CROSSMONTH_GUIDANCE, ISSUE.A01.KF.CROSS_BORDER, ISSUE.A01.KF.DATE_AUTHORITY, ISSUE.A01.KF.DIFFERENCE_CROSSMONTH, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT051.U00065.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT052.U00064.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT063.U00039.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT063.U00041.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00016.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00017.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00028.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00040.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00052.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00063.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00073.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00076.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00080.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT065.U00015.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00006.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00006.002, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00015.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00019.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00021.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT068.U00023.001, ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT068.U00025.001, ISSUE.A01.KF.DISPUTE.ST.TXT021.U00031.01, ISSUE.A01.KF.DISPUTE.STM.SRC.TXT058.U00014.S01, ISSUE.A01.KF.DISPUTE.STM.SRC.TXT059.U00016.S01, ISSUE.A01.KF.DISPUTE.STM.SRC.TXT062.U00014.S01, ISSUE.A01.KF.DISPUTE.STM.SRC.TXT062.U00022.S01, ISSUE.A01.KF.DISPUTE.STM.SRC.TXT066.U00016.S01, ISSUE.A01.KF.FX_CONVERSION, ISSUE.A01.KF.INSTITUTION_AUTHORITY, ISSUE.A01.KF.INSTITUTION_GOVERNANCE, ISSUE.A01.KF.OPTION_CLASSIFICATION, ISSUE.A01.KF.REPORT_DETAILS, ISSUE.A01.KF.SOURCE_PRECEDENCE, ISSUE.A01.KF.STATE_CONTROL_SCOPE, ISSUE.A01.KF.SYSTEM_QUERY_STATE, ISSUE.A01.KF.UNREADABLE_FIGURE, ISSUE.A01.KF.UNREADABLE_UNITS | 领域知识阶段责任人 | 这些事项继续在领域知识版本中保持OPEN；本模型不引用其结论。 |
