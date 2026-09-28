# A01.DomainModel.Coverage：覆盖与审计

覆盖版本：2026-09-28.business-v1.0.0.draft.1；范围模式：FULL_BASELINE。

## 规则覆盖

| 知识规则 | 建模分类 | 状态 | 模型引用 | MODEL_GAP | 理由 |
| --- | --- | --- | --- | --- | --- |
| RULE.A01.KF.SCOPE | EXTERNAL_CONTEXT | EXTERNAL_CONTEXT |  |  | 备案主体、承诺免报及申报责任属于备案邻域；UBO核心模型不建立备案主体流程。 |
| RULE.A01.KF.FILING | NO_MODEL_CHANGE | NO_MODEL_CHANGE |  |  | 设立、变更和存量备案期限属于申报义务与操作时限，不产生稳定UBO对象、关系或判断。 |
| RULE.A01.KF.PROFILE | EXTERNAL_CONTEXT | EXTERNAL_CONTEXT |  |  | 备案与金融机构独立识别的责任边界属于识别语境；核心模型在业务判断的人选语义中区分，不建立备案业务模型。 |
| RULE.A01.KF.EQUITY | CORE_STRUCTURE + DOMAIN_DECISION | MODELED | UBO.NaturalPerson, UBO.Organization, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Decision.EquityStandard |  | 自然人与组织的逐段权益关系是稳定业务结构；最终路径汇总及25%标准是稳定领域判断。 |
| RULE.A01.KF.NOMINEE | CORE_STRUCTURE + DOMAIN_DECISION | MODELED | UBO.Rel.RightsControlArrangement, UBO.Decision.RightAttribution |  | 代持、委托等安排会使名义人与真实权利人分离，是稳定业务关系；真实归属需要独立业务判断。 |
| RULE.A01.KF.RETURNS_VOTES | CORE_STRUCTURE + DOMAIN_DECISION | MODELED | UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Decision.BenefitVoteStandard |  | 收益权和表决权是独立业务关系，25%阈值及与标准一的顺序是稳定领域判断。 |
| RULE.A01.KF.CONTROL | CORE_STRUCTURE + DOMAIN_DECISION | MODELED | UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Decision.ActualControlStandard |  | 最终支配关系和控制安排属于核心业务结构；是否构成实际控制属于专业领域判断。 |
| RULE.A01.KF.FALLBACK | CORE_STRUCTURE + DOMAIN_DECISION | MODELED | UBO.Rel.OrganizationRole, UBO.Decision.FallbackManager |  | 真实日常经营管理角色是业务关系；只有前三项均明确不成立才能启用备位，是稳定判断。 |
| RULE.A01.KF.SOE | CORE_STRUCTURE + DOMAIN_DECISION + EXTERNAL_CONTEXT | PARTIAL | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Decision.StateOwnership, UBO.Decision.SOEPath, UBO.Context.AMLRisk | GAP.A01.StateControlScope | 国资产权/控制事实和法定代表人角色进入核心结构；国资分类及特殊人选是领域判断，机构风险是外部输入。 |
| RULE.A01.KF.BRANCHES | CORE_STRUCTURE + DOMAIN_DECISION | MODELED | UBO.Branch, UBO.Rel.BranchAffiliation, UBO.Rel.BranchRole, UBO.Decision.BranchIdentification |  | 分支、总分隶属及分支高管角色是稳定结构；境内承继与外国分支双部分人选是稳定判断。 |
| RULE.A01.KF.TRUST | CORE_STRUCTURE + DOMAIN_DECISION | MODELED | UBO.Trust, UBO.Rel.TrustPersonRole, UBO.Rel.TrustOrganizationRole, UBO.Rel.TrustBeneficiaryScope, UBO.Rel.TrustControlPower, UBO.Decision.TrustIdentification |  | 信托、信托当事人角色、受益范围及最终控制权均为核心业务结构；自然人范围需专业判断。 |
| RULE.A01.KF.TRUST_PRODUCTS | CORE_STRUCTURE + DOMAIN_DECISION + EXTERNAL_CONTEXT | PARTIAL | UBO.Trust, UBO.Decision.TrustServiceRoute, UBO.Context.AMLRisk | GAP.A01.TrustSimplifiedPersonSemantics | 信托类别是业务对象事实，完整/简化资格是领域判断，低风险结论来自AML邻域。 |
| RULE.A01.KF.ASSET_PRODUCTS | CORE_STRUCTURE + DOMAIN_DECISION + EXTERNAL_CONTEXT | PARTIAL | UBO.AssetProduct, UBO.Rel.ProductServiceRole, UBO.Rel.ProductPersonRole, UBO.Rel.ProductNaturalInterest, UBO.Rel.ProductOrganizationInterest, UBO.Rel.ProductControl, UBO.Decision.ProductGeneralIdentification, UBO.Decision.PublicProductSimplification, UBO.Decision.OtherProductSimplification, UBO.Context.AMLRisk | GAP.A01.OtherProductSimplifiedPersonSemantics | 资管产品、产品权利、服务和自然人管理角色属于核心结构；一般识别及简化路径是领域判断，风险为外部输入。 |
| RULE.A01.KF.TRUST_RELIANCE | DOMAIN_DECISION + EXTERNAL_CONTEXT | MODELED | UBO.Evidence, UBO.Decision.TrustEvidenceReliance, UBO.Context.TrustInstitutionCooperation |  | 是否采信受托资料是证据采用判断；受托机构AML体系及合作角色属于外部机构责任上下文。 |
| RULE.A01.KF.EXCEPTIONS | CORE_STRUCTURE + DOMAIN_DECISION + EXTERNAL_CONTEXT | MODELED | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Branch, UBO.Decision.ExemptEligibility, UBO.Decision.SimplifiedEligibility, UBO.Context.AMLRisk |  | 主体形态和真实业务角色影响法定免识别/简化人选，属于核心结构与判断；风险闸门来自AML邻域。 |
| RULE.A01.KF.IDENTITY | CORE_STRUCTURE + DOMAIN_DECISION | MODELED | UBO.NaturalPerson, UBO.Evidence, UBO.Decision.IdentityVerification, UBO.Decision.ConclusionFormation |  | 自然人和证据是核心对象；身份是否可靠核实以及最终结论完整性是稳定业务判断。 |
| RULE.A01.KF.RISK | DOMAIN_DECISION + EXTERNAL_CONTEXT | MODELED | UBO.Decision.RiskImpact, UBO.Context.AMLRisk |  | AML风险模型不属于UBO核心，但风险如何停止简化或加强识别是UBO识别边界判断。 |
| RULE.A01.KF.RISK_ACCEPT | EXTERNAL_CONTEXT | EXTERNAL_CONTEXT |  |  | 风险接受、高管批准、交易限制、拒办和终止属于金融机构客户关系/风险治理邻域。 |
| RULE.A01.KF.DATES | CORE_STRUCTURE + DOMAIN_DECISION | MODELED | UBO.Decision.EffectivePeriod, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Rel.OrganizationRole |  | 所有权利、控制和角色都具有独立有效期间；形成/终止日期精度是稳定领域判断。 |
| RULE.A01.KF.BOMIS | EXTERNAL_CONTEXT | EXTERNAL_CONTEXT |  |  | BOMIS查询是外部备案观察和核对上下文，不构成机构独立UBO关系事实。 |
| RULE.A01.KF.DIFFERENCE | EXTERNAL_CONTEXT | EXTERNAL_CONTEXT |  |  | 重大差异属于备案结果与机构结果之间的监管差异管理邻域，不进入UBO核心模型。 |
| RULE.A01.KF.FEEDBACK | NO_MODEL_CHANGE | NO_MODEL_CHANGE |  |  | 差异沟通、更正、报告及30工作日是反馈流程和期限，不改变UBO业务领域模型。 |
| RULE.A01.KF.SUSPICIOUS | EXTERNAL_CONTEXT | EXTERNAL_CONTEXT |  |  | 可疑交易判断、报告和保密属于AML邻域；差异不能自动产生UBO核心关系或人选。 |
| RULE.A01.KF.CONTINUOUS | CORE_STRUCTURE + DOMAIN_DECISION | MODELED | UBO.Decision.ChangeImpact, UBO.Rel.NaturalPersonEquity, UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Rel.ActualControl, UBO.Rel.TrustPersonRole, UBO.Rel.TrustBeneficiaryScope |  | 受益所有权关系具有历史版本；同数换人、关系类型和期间变化是否需要重识别是稳定领域判断。 |
| RULE.A01.KF.HISTORICAL | CORE_STRUCTURE + DOMAIN_DECISION + EXTERNAL_CONTEXT | MODELED | UBO.Decision.HistoricalAsOf, UBO.Context.HistoricalTransaction, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Rel.ActualControl |  | 历史有效权利关系属于核心时间语义；交易本身仅提供as-of时点，不扩建交易模型。 |
| RULE.A01.KF.EXISTING | NO_MODEL_CHANGE | NO_MODEL_CHANGE |  |  | 旧客户六个月、两年及激活例外是过渡政策与办理时限，不构成长期稳定领域结构。 |
| RULE.A01.KF.GOVERNANCE | DOMAIN_DECISION + EXTERNAL_CONTEXT | MODELED | UBO.Evidence, UBO.Decision.ConclusionFormation |  | 结论必须绑定身份、权利、时间、证据和UNKNOWN，是领域判断；具体机构岗位授权属于外部治理。 |

## 问题覆盖

| 问题 | 状态 | 模型引用 | 缺口 | 说明 |
| --- | --- | --- | --- | --- |
| 当前组织属于须备案主体、暂无备案要求的主体，还是个体工商户，依据哪个适用时点和主体类型判断？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 注册资本或出资额恰为1000万元、折算为等值外币时，承诺免报的金额条件如何核对？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 全部股东或合伙人都是自然人，且名义自然人与真实控制、获益者一致的证据是否充分？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 是否存在股东或合伙人以外的自然人实际控制、取得收益，从而使承诺免报失效？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 是否存在通过股权或合伙权益以外方式实施控制或获取收益，从而不能承诺免报？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 新设登记、无法通过系统设立登记、实施前存量主体，各自何时完成备案？ | NO_MODEL_CHANGE |  |  | 该问题属于流程、期限或过渡政策，不改变UBO核心业务模型。 |
| 受益所有人信息变动与承诺免报条件丧失，各自从何事实日期起计算30日更新？ | NO_MODEL_CHANGE |  |  | 该问题属于流程、期限或过渡政策，不改变UBO核心业务模型。 |
| 备案的自然人身份字段及地址、联系方式、证件有效期如何逐人核对？ | MODELED | UBO.NaturalPerson, UBO.Evidence, UBO.Decision.IdentityVerification, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |
| 受益所有权关系类型、形成及终止日期应如何逐项记载？ | MODELED | UBO.NaturalPerson, UBO.Evidence, UBO.Decision.IdentityVerification, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |
| 备案主体识别与金融机构客户识别是否面对同一对象、作同一个判断、由谁承担各自核实责任？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 自然人直接持有多少股权、股份或合伙权益才达到标准，恰为25%是否包括？ | MODELED | UBO.NaturalPerson, UBO.Organization, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Decision.EquityStandard |  | 由纯业务对象、关系和领域判断承接。 |
| 间接持股经过哪些有效上层主体和路径，如何逐路径计算同一自然人最终拥有比例并汇总？ | MODELED | UBO.NaturalPerson, UBO.Organization, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Decision.EquityStandard |  | 由纯业务对象、关系和领域判断承接。 |
| 登记持股与代持、受益权转移不一致时，登记股东是否仍为最终拥有者、实际权益归属谁？ | MODELED | UBO.Rel.RightsControlArrangement, UBO.Decision.RightAttribution |  | 由纯业务对象、关系和领域判断承接。 |
| 自然人未满足持有权益标准，却最终享有多少收益权，是否达到25%，收益权从何而来？ | MODELED | UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Decision.BenefitVoteStandard |  | 由纯业务对象、关系和领域判断承接。 |
| 自然人未满足持有权益标准，却最终享有多少表决权，委托或一致行动的范围、期限是否支持25%以上？ | MODELED | UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Decision.BenefitVoteStandard |  | 由纯业务对象、关系和领域判断承接。 |
| 同一自然人已满足持股标准时，另有收益、表决或控制事实应如何处理，何时仍须同时标注标准二与三？ | MODELED | UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Decision.BenefitVoteStandard |  | 由纯业务对象、关系和领域判断承接。 |
| 控制权来自哪份协议、代持、一致行动、亲密关系或其他安排，其法律权限及实际行使是否足以控制客户？ | MODELED | UBO.Rel.RightsControlArrangement, UBO.Decision.RightAttribution, UBO.Rel.ActualControl, UBO.Decision.ActualControlStandard |  | 由纯业务对象、关系和领域判断承接。 |
| 谁能够决定法定代表人、董事、监事、高管或执行事务合伙人任免，实际决定权和普通任职如何区分？ | MODELED | UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Decision.ActualControlStandard |  | 由纯业务对象、关系和领域判断承接。 |
| 谁决定重大经营管理决策的制定或执行，决议权、否决权及实际决策记录是否支持结论？ | MODELED | UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Decision.ActualControlStandard |  | 由纯业务对象、关系和领域判断承接。 |
| 谁实际决定财务收支，与仅经办、签字或授权付款的人员有何区别？ | MODELED | UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Decision.ActualControlStandard |  | 由纯业务对象、关系和领域判断承接。 |
| 谁长期实际支配重要资产或主要资金，资产重要性、支配持续性和受益所有权之间如何核实？ | MODELED | UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Decision.ActualControlStandard |  | 由纯业务对象、关系和领域判断承接。 |
| 多个自然人是否通过同一协议或行为联合实施实际控制，每人控制权限和共同作用是什么？ | MODELED | UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Decision.ActualControlStandard |  | 由纯业务对象、关系和领域判断承接。 |
| 公司法或国资交易语境的实际控制企业、披露的实际控制人，与本次须识别的自然人受益所有人如何区分？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 何时可以证实三项自然人识别标准均不存在，才能启用负责日常经营管理人员的备位识别？ | MODELED | UBO.Rel.OrganizationRole, UBO.Decision.FallbackManager |  | 由纯业务对象、关系和领域判断承接。 |
| 启用备位后谁实际负责日常经营管理，法定代表人、董事长、经理中应如何选择并核对任职？ | MODELED | UBO.Rel.OrganizationRole, UBO.Decision.FallbackManager |  | 由纯业务对象、关系和领域判断承接。 |
| 国有独资、国有控股与仅国有参股如何以官方登记及实际股权/控制资料区分？ | PARTIAL | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Decision.StateOwnership, UBO.Decision.SOEPath, UBO.Context.AMLRisk | GAP.A01.StateControlScope | 核心业务结构/判断已承接，但存在直接影响该问题的MODEL_GAP。 |
| 备案中国有独资或控股公司法定代表人视同，金融机构识别中相应简化路径，各自是否可采用且需要哪些风险前提？ | PARTIAL | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Decision.StateOwnership, UBO.Decision.SOEPath, UBO.Context.AMLRisk | GAP.A01.StateControlScope | 核心业务结构/判断已承接，但存在直接影响该问题的MODEL_GAP。 |
| 国有参股公司国有资本路径能否停止向自然人穿透，其余社会资本及非股权控制是否仍须识别？ | PARTIAL | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Decision.StateOwnership, UBO.Decision.SOEPath, UBO.Context.AMLRisk | GAP.A01.StateControlScope | 核心业务结构/判断已承接，但存在直接影响该问题的MODEL_GAP。 |
| 国内法人或非法人组织分支机构如何识别所属主体，何时通常承继其受益所有人，既有尽调资料何时可复用？ | MODELED | UBO.Branch, UBO.Rel.BranchAffiliation, UBO.Rel.BranchRole, UBO.Decision.BranchIdentification |  | 由纯业务对象、关系和领域判断承接。 |
| 外国公司分支机构需如何同时识别所属外国公司自然人受益所有人与至少一名分支高管，并区别备案和机构识别？ | MODELED | UBO.Branch, UBO.Rel.BranchAffiliation, UBO.Rel.BranchRole, UBO.Decision.BranchIdentification |  | 由纯业务对象、关系和领域判断承接。 |
| 所属总公司注销或工商资料缺失总分关系时，能否认定某人代替受益所有人，应补哪些存续和控制证据？ | MODELED | UBO.Branch, UBO.Rel.BranchAffiliation, UBO.Rel.BranchRole, UBO.Decision.BranchIdentification |  | 由纯业务对象、关系和领域判断承接。 |
| 总公司强制注销、恢复登记与分支机构仍登记存续的不同时间状态下，能否沿用原所属关系和受益所有人？ | MODELED | UBO.Branch, UBO.Rel.BranchAffiliation, UBO.Rel.BranchRole, UBO.Decision.BranchIdentification |  | 由纯业务对象、关系和领域判断承接。 |
| 信托委托人、受托人、受益人、监察人及其他最终有效控制自然人分别是谁？ | MODELED | UBO.Trust, UBO.Rel.TrustPersonRole, UBO.Rel.TrustOrganizationRole, UBO.Rel.TrustBeneficiaryScope, UBO.Rel.TrustControlPower, UBO.Decision.TrustIdentification |  | 由纯业务对象、关系和领域判断承接。 |
| 某信托当事人为非自然人时，如何逐一逐层追溯到最终有效控制该信托的自然人？ | MODELED | UBO.Trust, UBO.Rel.TrustPersonRole, UBO.Rel.TrustOrganizationRole, UBO.Rel.TrustBeneficiaryScope, UBO.Rel.TrustControlPower, UBO.Decision.TrustIdentification |  | 由纯业务对象、关系和领域判断承接。 |
| 处分信托财产、决定投资分配、变更受益人或受托人等不同权限谁最终行使，如何识别其他最终有效控制人？ | MODELED | UBO.Trust, UBO.Rel.TrustPersonRole, UBO.Rel.TrustOrganizationRole, UBO.Rel.TrustBeneficiaryScope, UBO.Rel.TrustControlPower, UBO.Decision.TrustIdentification |  | 由纯业务对象、关系和领域判断承接。 |
| 信托设立时或存续期间没有明确具体受益人时，受益人范围如何识别记录，后来被指定时如何更新？ | MODELED | UBO.Trust, UBO.Rel.TrustPersonRole, UBO.Rel.TrustOrganizationRole, UBO.Rel.TrustBeneficiaryScope, UBO.Rel.TrustControlPower, UBO.Decision.TrustIdentification |  | 由纯业务对象、关系和领域判断承接。 |
| 财富管理、公益慈善、其他资产服务、民事与外国信托分别适用何种识别深度和简化条件？ | PARTIAL | UBO.Trust, UBO.Decision.TrustServiceRoute, UBO.Context.AMLRisk | GAP.A01.TrustSimplifiedPersonSemantics | 核心业务结构/判断已承接，但存在直接影响该问题的MODEL_GAP。 |
| 受托信托公司提供受益所有人资料时，合作机构何时可以采信，发现疑点、拒不配合或系统性缺陷如何升级？ | MODELED | UBO.Evidence, UBO.Decision.TrustEvidenceReliance, UBO.Context.TrustInstitutionCooperation |  | 由纯业务对象、关系和领域判断承接。 |
| 资产管理信托与其他资管产品如何按所有权控制结构和风险参照法人标准识别？ | PARTIAL | UBO.AssetProduct, UBO.Rel.ProductServiceRole, UBO.Rel.ProductPersonRole, UBO.Rel.ProductNaturalInterest, UBO.Rel.ProductOrganizationInterest, UBO.Rel.ProductControl, UBO.Decision.ProductGeneralIdentification, UBO.Decision.PublicProductSimplification, UBO.Decision.OtherProductSimplification, UBO.Context.AMLRisk | GAP.A01.OtherProductSimplifiedPersonSemantics | 核心业务结构/判断已承接，但存在直接影响该问题的MODEL_GAP。 |
| 公开募集且依法备案或登记的资管产品、低风险非公开产品，分别何时可简化认定管理产品的自然人？ | PARTIAL | UBO.AssetProduct, UBO.Rel.ProductServiceRole, UBO.Rel.ProductPersonRole, UBO.Rel.ProductNaturalInterest, UBO.Rel.ProductOrganizationInterest, UBO.Rel.ProductControl, UBO.Decision.ProductGeneralIdentification, UBO.Decision.PublicProductSimplification, UBO.Decision.OtherProductSimplification, UBO.Context.AMLRisk | GAP.A01.OtherProductSimplifiedPersonSemantics | 核心业务结构/判断已承接，但存在直接影响该问题的MODEL_GAP。 |
| 机关法人、事业单位、基层自治、农村集体等客户是否属于第十条可免识别类别，有何确证材料？ | MODELED | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Branch, UBO.Decision.ExemptEligibility, UBO.Decision.SimplifiedEligibility, UBO.Context.AMLRisk |  | 由纯业务对象、关系和领域判断承接。 |
| 无较高风险的不具有法人资格专业服务机构、个人独资企业、合作经济组织，各自可认定谁及何时先按一般标准？ | MODELED | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Branch, UBO.Decision.ExemptEligibility, UBO.Decision.SimplifiedEligibility, UBO.Context.AMLRisk |  | 由纯业务对象、关系和领域判断承接。 |
| 无法准确判断简化或豁免资格，或者存在第二十条特定风险时，如何回到完整识别核实并保留判断理由？ | MODELED | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Branch, UBO.Decision.ExemptEligibility, UBO.Decision.SimplifiedEligibility, UBO.Context.AMLRisk |  | 由纯业务对象、关系和领域判断承接。 |
| 高风险国家或地区、境外登记无法核实、循环交叉持股及代持协议分别是什么加强措施触发事实？ | MODELED | UBO.Decision.RiskImpact, UBO.Context.AMLRisk |  | 由纯业务对象、关系和领域判断承接。 |
| 有理由怀疑洗钱或恐怖融资以及自然人客户高风险关联时，谁评估受影响的全部非自然人客户？ | MODELED | UBO.Decision.RiskImpact, UBO.Context.AMLRisk |  | 由纯业务对象、关系和领域判断承接。 |
| 出现特定风险时，何时选择补全身份、独立验证、索取代持协议、回访、交易监测、降低阈值或提高更新频次中的哪些措施？ | MODELED | UBO.Decision.RiskImpact, UBO.Context.AMLRisk |  | 由纯业务对象、关系和领域判断承接。 |
| 何时需高级管理层批准、交易限制，或因风险超出管理能力拒办及终止关系？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 自然人身份真实性能否通过官方渠道核实，不能时哪些证件与客户补充材料足以替代？ | MODELED | UBO.NaturalPerson, UBO.Evidence, UBO.Decision.IdentityVerification, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |
| 权利状况所依客户材料、官方公开信息、金融机构发现资料如何交叉印证并与结构及风险相符？ | MODELED | UBO.NaturalPerson, UBO.Evidence, UBO.Decision.IdentityVerification, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |
| 何时可仅采部分佐证或直接采信低风险客户提供的权利信息，识别过程及理由应如何留痕？ | MODELED | UBO.NaturalPerson, UBO.Evidence, UBO.Decision.IdentityVerification, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |
| 仅BOMIS查询、第三方百分比或自动化识别输出是否足以代替独立识别、核实和机构风险判断？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 首次满足标准日、当前权利状态形成日、权利终止日、登记披露日、核实日和备案日如何分开记录？ | MODELED | UBO.Decision.EffectivePeriod, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Rel.OrganizationRole |  | 由纯业务对象、关系和领域判断承接。 |
| 股权转让、章程、合伙协议、股东决议与控制权协议分别何时生效，对自然人关系形成日期有何影响？ | MODELED | UBO.Decision.EffectivePeriod, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Rel.OrganizationRole |  | 由纯业务对象、关系和领域判断承接。 |
| 多次增持减持但未退出受益所有人名单时，首次符合标准和当前比例/控制方式的形成日期各应如何记录？ | MODELED | UBO.Decision.EffectivePeriod, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Rel.OrganizationRole |  | 由纯业务对象、关系和领域判断承接。 |
| 客户处于办理业务、历史交易及当前三个时点时，按哪一时点权利及证据还原自然人归属？ | MODELED | UBO.Decision.EffectivePeriod, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Rel.OrganizationRole, UBO.Decision.HistoricalAsOf, UBO.Context.HistoricalTransaction, UBO.Rel.BenefitRight, UBO.Rel.VotingRight |  | 由纯业务对象、关系和领域判断承接。 |
| 哪些依法须备案的非自然人客户必须将机构识别结果与BOMIS备案资料查询核对，查询在哪一核实阶段进行？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| BOMIS多出、遗漏或身份不匹配的自然人是否改变了应识别的人选，证据能否说明多出的原因？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 同一自然人姓名、性别、国籍、出生日期、身份证件种类或同一证件号码哪项不一致，是否涉及身份关键要素？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 同一人股权、合伙权益、收益或表决比例差异，何时改变受益所有权关系类型最终认定？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 实际控制方式、内容或担任职务不同，是否改变权利关系类型，抑或仅是非重大描述差异？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 受益所有权形成或终止时间在年月上不一致时如何定性，二次材料所谓30自然日同年跨月豁免是否成立？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 机构使用更严格的识别阈值导致额外识别人选时，这种不一致能否归为非重大及应如何留痕？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 客户依法应备案但未在系统备案时，如何沟通提示，以及客户提示后仍未备案何时报告？ | NO_MODEL_CHANGE |  |  | 该问题属于流程、期限或过渡政策，不改变UBO核心业务模型。 |
| 发现差异后与客户如何核实，是机构识别错误还是备案记录不准，各自谁更正或报告？ | NO_MODEL_CHANGE |  |  | 该问题属于流程、期限或过渡政策，不改变UBO核心业务模型。 |
| 重大差异报告的30工作日从何时起算，需保留哪些理由、确认过程与佐证材料？ | NO_MODEL_CHANGE |  |  | 该问题属于流程、期限或过渡政策，不改变UBO核心业务模型。 |
| 判为非重大差异后30工作日内应记哪些比较、核实和不报告理由，如何提醒客户？ | NO_MODEL_CHANGE |  |  | 该问题属于流程、期限或过渡政策，不改变UBO核心业务模型。 |
| 重大差异核实未完成时，何时仍可在风险可控条件下先建立或维持业务关系？ | NO_MODEL_CHANGE |  |  | 该问题属于流程、期限或过渡政策，不改变UBO核心业务模型。 |
| 差异分析涉及洗钱或恐怖融资嫌疑时，差异报告与可疑交易报告如何分别履行且隔离披露？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 客户所有权、收益、表决、控制或关键管理人员变化时，何种可能影响受益所有权的变化需审核和必要更新？ | MODELED | UBO.Decision.ChangeImpact, UBO.Rel.NaturalPersonEquity, UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Rel.ActualControl, UBO.Rel.TrustPersonRole, UBO.Rel.TrustBeneficiaryScope |  | 由纯业务对象、关系和领域判断承接。 |
| 同数换人、受益所有人总人数不变但权利类型或形成日期变化，能否仍需更新或报差异？ | MODELED | UBO.Decision.ChangeImpact, UBO.Rel.NaturalPersonEquity, UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Rel.ActualControl, UBO.Rel.TrustPersonRole, UBO.Rel.TrustBeneficiaryScope |  | 由纯业务对象、关系和领域判断承接。 |
| 识别完成时谁有权限复核自然人身份、权利、时点、冲突和结论，哪些决策不能交由供应商或自动系统？ | MODELED | UBO.Evidence, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |
| 受益所有人信息如何用于关联客户与历史交易风险分析，同时避免把同一受益人等同可疑或历史责任？ | MODELED | UBO.Decision.HistoricalAsOf, UBO.Context.HistoricalTransaction, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Rel.ActualControl |  | 由纯业务对象、关系和领域判断承接。 |
| 法规与官方指南、地方填报页面、机构作业口径及第三方产品解释互相不一致时，应以哪个适用对象、效力与生效日判断？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 谁提出本次客户识别或备案事项、目标客户与所属法人主体怎样确认、案件应记哪个办理时点？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 谁建立直接股东、合伙人、信托当事人和资管份额持有人清单，如何防漏上层分支？ | MODELED | UBO.NaturalPerson, UBO.Organization, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Decision.EquityStandard, UBO.Evidence, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |
| 发现工商登记与章程、协议、客户声明冲突时，应先向谁取什么原始文件并记录各材料适用期间？ | MODELED | UBO.Rel.RightsControlArrangement, UBO.Decision.RightAttribution, UBO.NaturalPerson, UBO.Evidence, UBO.Decision.IdentityVerification, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |
| 境外上层主体无法取得可靠登记或协议时，需要哪些跨境补证、谁判断风险加强及可否继续业务？ | MODELED | UBO.Decision.RiskImpact, UBO.Context.AMLRisk |  | 由纯业务对象、关系和领域判断承接。 |
| 谁对每项受益所有权关系的材料真实性、来源独立性与形成日期作判断并留下不同意见？ | MODELED | UBO.NaturalPerson, UBO.Evidence, UBO.Decision.IdentityVerification, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |
| 形成日期只能落在某时间区间但未知具体日时，如何保留日期精度而不由系统填默认日？ | MODELED | UBO.Decision.EffectivePeriod, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Rel.OrganizationRole |  | 由纯业务对象、关系和领域判断承接。 |
| 如何向有权岗位提交重大与非重大差异分类、期限、佐证及异议，谁签核提交或不报告？ | EXTERNAL_CONTEXT |  |  | 该问题属于备案、差异、AML或其他邻接领域，只保留边界，不扩建UBO核心模型。 |
| 交付识别结果时须包括哪些人、权利、路径、时间、原始材料及未决问题，谁确认已具业务可用性？ | MODELED | UBO.NaturalPerson, UBO.Evidence, UBO.Decision.IdentityVerification, UBO.Decision.ConclusionFormation, UBO.Decision.HistoricalAsOf, UBO.Context.HistoricalTransaction, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Rel.ActualControl |  | 由纯业务对象、关系和领域判断承接。 |
| 若最终无人可确认、存在控制权争议或来源互相矛盾，谁发补件清单、何时结束当前审查？ | MODELED | UBO.Rel.OrganizationRole, UBO.Decision.FallbackManager, UBO.Evidence, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |
| 存量较高风险客户及长期不动账户分别何时启动识别，适用起始日、完成时点和激活触发如何证明？ | MODELED | UBO.Decision.ChangeImpact, UBO.Rel.NaturalPersonEquity, UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Rel.ActualControl, UBO.Rel.TrustPersonRole, UBO.Rel.TrustBeneficiaryScope |  | 由纯业务对象、关系和领域判断承接。 |
| 机构对受益所有人识别、报告、备案比对及证据留存的有权岗位、复核人和权限从何制度获得？ | MODELED | UBO.Evidence, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |
| 生成的受益所有人结果谁有权限批准用于客户准入、授信、关联风险及差异报告，各用途是否分别复核？ | MODELED | UBO.Evidence, UBO.Decision.ConclusionFormation |  | 由纯业务对象、关系和领域判断承接。 |

## 案例覆盖

| 案例 | 状态 | 模型引用 | 解释 |
| --- | --- | --- | --- |
| CASE.A01.KF.SCOPE.B | CONTEXT_ONLY |  | 案例只验证外部责任、流程或时限边界，不为此创建UBO核心模型元素。 |
| CASE.A01.KF.FILING.B | CONTEXT_ONLY |  | 案例只验证外部责任、流程或时限边界，不为此创建UBO核心模型元素。 |
| CASE.A01.KF.PROFILE.B | CONTEXT_ONLY |  | 案例只验证外部责任、流程或时限边界，不为此创建UBO核心模型元素。 |
| CASE.A01.KF.EQUITY.B | EXPLAINED | UBO.NaturalPerson, UBO.Organization, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Decision.EquityStandard | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.NOMINEE.B | EXPLAINED | UBO.Rel.RightsControlArrangement, UBO.Decision.RightAttribution | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.RETURNS_VOTES.B | EXPLAINED | UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Decision.BenefitVoteStandard | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.CONTROL.B | EXPLAINED | UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Decision.ActualControlStandard | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.FALLBACK.B | EXPLAINED | UBO.Rel.OrganizationRole, UBO.Decision.FallbackManager | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.SOE.B | BLOCKED | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Decision.StateOwnership, UBO.Decision.SOEPath, UBO.Context.AMLRisk | 案例涉及尚未解决的核心人选/边界语义缺口；保持上游真值，不由模型补造结论。 |
| CASE.A01.KF.BRANCHES.B | EXPLAINED | UBO.Branch, UBO.Rel.BranchAffiliation, UBO.Rel.BranchRole, UBO.Decision.BranchIdentification | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.TRUST.B | EXPLAINED | UBO.Trust, UBO.Rel.TrustPersonRole, UBO.Rel.TrustOrganizationRole, UBO.Rel.TrustBeneficiaryScope, UBO.Rel.TrustControlPower, UBO.Decision.TrustIdentification | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.TRUST_PRODUCTS.B | BLOCKED | UBO.Trust, UBO.Decision.TrustServiceRoute, UBO.Context.AMLRisk | 案例涉及尚未解决的核心人选/边界语义缺口；保持上游真值，不由模型补造结论。 |
| CASE.A01.KF.EXCEPTIONS.B | EXPLAINED | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Branch, UBO.Decision.ExemptEligibility, UBO.Decision.SimplifiedEligibility, UBO.Context.AMLRisk | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.EXCEPTIONS.QFI.B | EXPLAINED | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Branch, UBO.Decision.ExemptEligibility, UBO.Decision.SimplifiedEligibility, UBO.Context.AMLRisk | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.EXCEPTIONS.REP.B | EXPLAINED | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Branch, UBO.Decision.ExemptEligibility, UBO.Decision.SimplifiedEligibility, UBO.Context.AMLRisk | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.IDENTITY.B | EXPLAINED | UBO.NaturalPerson, UBO.Evidence, UBO.Decision.IdentityVerification, UBO.Decision.ConclusionFormation | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.RISK.B | EXPLAINED | UBO.Decision.RiskImpact, UBO.Context.AMLRisk | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.RISK_ACCEPT.B | CONTEXT_ONLY |  | 案例只验证外部责任、流程或时限边界，不为此创建UBO核心模型元素。 |
| CASE.A01.KF.DATES.B | EXPLAINED | UBO.Decision.EffectivePeriod, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Rel.OrganizationRole | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.BOMIS.B | CONTEXT_ONLY |  | 案例只验证外部责任、流程或时限边界，不为此创建UBO核心模型元素。 |
| CASE.A01.KF.DIFFERENCE.B | CONTEXT_ONLY |  | 案例只验证外部责任、流程或时限边界，不为此创建UBO核心模型元素。 |
| CASE.A01.KF.FEEDBACK.B | CONTEXT_ONLY |  | 案例只验证外部责任、流程或时限边界，不为此创建UBO核心模型元素。 |
| CASE.A01.KF.SUSPICIOUS.B | CONTEXT_ONLY |  | 案例只验证外部责任、流程或时限边界，不为此创建UBO核心模型元素。 |
| CASE.A01.KF.CONTINUOUS.B | EXPLAINED | UBO.Decision.ChangeImpact, UBO.Rel.NaturalPersonEquity, UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Rel.ActualControl, UBO.Rel.TrustPersonRole, UBO.Rel.TrustBeneficiaryScope | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.HISTORICAL.B | EXPLAINED | UBO.Decision.HistoricalAsOf, UBO.Context.HistoricalTransaction, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Rel.ActualControl | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.EXISTING.B | CONTEXT_ONLY |  | 案例只验证外部责任、流程或时限边界，不为此创建UBO核心模型元素。 |
| CASE.A01.KF.GOVERNANCE.B | EXPLAINED | UBO.Evidence, UBO.Decision.ConclusionFormation | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.SRC06.01 | EXPLAINED | UBO.NaturalPerson, UBO.Organization, UBO.Rel.NaturalPersonEquity, UBO.Rel.OrganizationEquity, UBO.Decision.EquityStandard | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.SRC06.02 | EXPLAINED | UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Decision.BenefitVoteStandard | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.SRC06.03 | EXPLAINED | UBO.Rel.RightsControlArrangement, UBO.Decision.RightAttribution | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.SRC06.04 | EXPLAINED | UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Decision.ActualControlStandard | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.SRC06.05 | EXPLAINED | UBO.Rel.RightsControlArrangement, UBO.Rel.ActualControl, UBO.Decision.ActualControlStandard | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.SRC06.06 | BLOCKED | UBO.Organization, UBO.Rel.OrganizationRole, UBO.Decision.StateOwnership, UBO.Decision.SOEPath, UBO.Context.AMLRisk | 案例涉及尚未解决的核心人选/边界语义缺口；保持上游真值，不由模型补造结论。 |
| CASE.A01.KF.SRC06.07 | EXPLAINED | UBO.Rel.BenefitRight, UBO.Rel.VotingRight, UBO.Decision.BenefitVoteStandard | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |
| CASE.A01.KF.ASSET_PRODUCTS.B | BLOCKED | UBO.AssetProduct, UBO.Rel.ProductServiceRole, UBO.Rel.ProductPersonRole, UBO.Rel.ProductNaturalInterest, UBO.Rel.ProductOrganizationInterest, UBO.Rel.ProductControl, UBO.Decision.ProductGeneralIdentification, UBO.Decision.PublicProductSimplification, UBO.Decision.OtherProductSimplification, UBO.Context.AMLRisk | 案例涉及尚未解决的核心人选/边界语义缺口；保持上游真值，不由模型补造结论。 |
| CASE.A01.KF.TRUST_RELIANCE.B | EXPLAINED | UBO.Evidence, UBO.Decision.TrustEvidenceReliance, UBO.Context.TrustInstitutionCooperation | 案例可由当前业务对象、关系、判断和UNKNOWN边界解释；未改写上游 expected / forbidden。 |

## 上游 OPEN 去向

| 上游事项 | 处理 | MODEL_GAP | 说明 |
| --- | --- | --- | --- |
| ISSUE.A01.KF.DIFFERENCE_CROSSMONTH | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.INSTITUTION_AUTHORITY | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.EVIDENCE_CONFLICT | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.STATE_CONTROL_SCOPE | CORE_MODEL_GAP | GAP.A01.StateControlScope | 该未决直接影响国资性质分类和国资特殊人选边界，因此升级为核心MODEL_GAP。 |
| ISSUE.A01.KF.REPORT_DETAILS | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.CROSS_BORDER | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.DATED_PUBLISHING | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.PROPOSED_POLICY | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.SYSTEM_QUERY_STATE | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.UNREADABLE_UNITS | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.SOURCE_PRECEDENCE | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.FX_CONVERSION | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.OPTION_CLASSIFICATION | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.CROSSMONTH_GUIDANCE | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.UNREADABLE_FIGURE | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DATE_AUTHORITY | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.INSTITUTION_GOVERNANCE | EXTERNAL_CONTEXT_OPEN |  | 该未决影响备案、BOMIS、AML/风险治理、机构授权、跨境证据渠道或其他邻接业务；核心模型通过外部上下文/UNKNOWN处理，不升级MODEL_GAP。 |
| ISSUE.A01.KF.DISPUTE.ST.TXT021.U00031.01 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT051.U00065.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT052.U00064.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT058.U00014.S01 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT059.U00016.S01 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT062.U00014.S01 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT062.U00022.S01 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT063.U00039.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT063.U00041.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00016.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00017.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00028.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00040.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00052.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00063.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00073.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00076.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00080.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT065.U00015.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT066.U00016.S01 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00006.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00006.002 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00015.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00019.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00021.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT068.U00023.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT068.U00025.001 | NO_MODEL_IMPACT |  | 该未决属于个案证据、不可读材料或二手/厂商主张争议；固定领域知识已经给出不采信或UNKNOWN边界，不改变当前业务模型定义。 |

## 真正的核心模型缺口

| 缺口 | 影响 | 责任 | 解决前处理 |
| --- | --- | --- | --- |
| 国资交易监管中的“国有实际控制企业”不能自动等同备案/金融机构规则的国有独资或控股公司；国有相对控股边界仍需权威口径和个案控制证据。 | UBO.Decision.StateOwnership, UBO.Decision.SOEPath, RULE.A01.KF.SOE | 国资制度专家与客户 | 国资性质无法确认时特殊法定代表人路径保持 UNKNOWN，不自动套用。 |
| 固定领域知识明确部分其他资产服务信托在结构简单且低风险时“可以简化”，但没有给出统一的简化后替代自然人人选。 | UBO.Decision.TrustServiceRoute, RULE.A01.KF.TRUST_PRODUCTS | 领域知识责任人与信托业务专家 | 只输出简化资格，不从该资格直接生成具体受益所有人人选。 |
| 固定领域知识说明企业/职业年金等其他低风险产品“可简化”，但没有给出所有此类产品统一的简化后自然人人选。 | UBO.Decision.OtherProductSimplification, RULE.A01.KF.ASSET_PRODUCTS | 领域知识责任人与资管产品业务专家 | 只输出简化资格，不能由系统擅自套用产品管理人或其他固定自然人。 |
