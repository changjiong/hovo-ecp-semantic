# A01受益所有人领域模型：覆盖与审计

模型 A01.DomainModel / 2026-09-28.fresh-baseline.1；DSL 2.1.0；范围模式 FULL_BASELINE。

本表核对对应关系与实际证据，不以引用存在代替语义正确性。

## 问题覆盖

| 问题 | 状态 | 规则 | 流程 | 案例 | 模型 | 缺口 |
| --- | --- | --- | --- | --- | --- | --- |
| Q.A01.S01 | EXTERNAL_CONTEXT | RULE.A01.KF.SCOPE |  | CASE.A01.KF.SCOPE.B |  |  |
| Q.A01.S02 | DEFERRED | RULE.A01.KF.SCOPE |  | CASE.A01.KF.SCOPE.B |  | GAP.A01.FX_CONVERSION |
| Q.A01.S03 | EXTERNAL_CONTEXT | RULE.A01.KF.SCOPE |  | CASE.A01.KF.SCOPE.B |  |  |
| Q.A01.S04 | EXTERNAL_CONTEXT | RULE.A01.KF.SCOPE |  | CASE.A01.KF.SCOPE.B |  |  |
| Q.A01.S05 | EXTERNAL_CONTEXT | RULE.A01.KF.SCOPE |  | CASE.A01.KF.SCOPE.B |  |  |
| Q.A01.S07 | DEFERRED | RULE.A01.KF.FILING |  | CASE.A01.KF.FILING.B |  | GAP.A01.DATED_PUBLISHING |
| Q.A01.S08 | DEFERRED | RULE.A01.KF.FILING |  | CASE.A01.KF.FILING.B |  | GAP.A01.DATED_PUBLISHING |
| Q.A01.S09 | PARTIAL | RULE.A01.KF.IDENTITY |  | CASE.A01.KF.IDENTITY.B | T.Party, T.Evidence, T.PersonAssessment, R.NaturalPerson, J.Evidence | GAP.A01.PROPOSED_POLICY |
| Q.A01.S10 | PARTIAL | RULE.A01.KF.IDENTITY |  | CASE.A01.KF.IDENTITY.B | T.Party, T.Evidence, T.PersonAssessment, R.NaturalPerson, J.Evidence | GAP.A01.PROPOSED_POLICY |
| Q.A01.S12 | MODELED | RULE.A01.KF.PROFILE |  | CASE.A01.KF.PROFILE.B | T.PersonAssessment, T.IdentificationRoute, J.Route |  |
| Q.A01.S13 | PARTIAL | RULE.A01.KF.EQUITY |  | CASE.A01.KF.EQUITY.B, CASE.A01.KF.SRC06.01 | T.Party, T.Right, T.PersonAssessment, R.Equity25 | GAP.A01.PROPOSED_POLICY |
| Q.A01.S14 | MODELED | RULE.A01.KF.EQUITY |  | CASE.A01.KF.EQUITY.B, CASE.A01.KF.SRC06.01 | T.Party, T.Right, T.PersonAssessment, R.Equity25 |  |
| Q.A01.S16 | PARTIAL | RULE.A01.KF.NOMINEE |  | CASE.A01.KF.NOMINEE.B, CASE.A01.KF.SRC06.03 | T.Right, T.Arrangement, T.Evidence, J.RightAttribution | GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S17 | MODELED | RULE.A01.KF.RETURNS_VOTES |  | CASE.A01.KF.RETURNS_VOTES.B, CASE.A01.KF.SRC06.02, CASE.A01.KF.SRC06.07 | T.Right, T.PersonAssessment, R.BenefitVote25 |  |
| Q.A01.S18 | MODELED | RULE.A01.KF.RETURNS_VOTES |  | CASE.A01.KF.RETURNS_VOTES.B, CASE.A01.KF.SRC06.02, CASE.A01.KF.SRC06.07 | T.Right, T.PersonAssessment, R.BenefitVote25 |  |
| Q.A01.S20 | MODELED | RULE.A01.KF.RETURNS_VOTES |  | CASE.A01.KF.RETURNS_VOTES.B, CASE.A01.KF.SRC06.02, CASE.A01.KF.SRC06.07 | T.Right, T.PersonAssessment, R.BenefitVote25 |  |
| Q.A01.S21 | PARTIAL | RULE.A01.KF.NOMINEE, RULE.A01.KF.CONTROL |  | CASE.A01.KF.NOMINEE.B, CASE.A01.KF.CONTROL.B, CASE.A01.KF.SRC06.03, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | T.Right, T.Arrangement, T.Evidence, J.RightAttribution, T.PersonAssessment, J.ActualControl | GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S22 | PARTIAL | RULE.A01.KF.CONTROL |  | CASE.A01.KF.CONTROL.B, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | T.Arrangement, T.PersonAssessment, J.ActualControl | GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S23 | PARTIAL | RULE.A01.KF.CONTROL |  | CASE.A01.KF.CONTROL.B, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | T.Arrangement, T.PersonAssessment, J.ActualControl | GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S24 | PARTIAL | RULE.A01.KF.CONTROL |  | CASE.A01.KF.CONTROL.B, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | T.Arrangement, T.PersonAssessment, J.ActualControl | GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S25 | PARTIAL | RULE.A01.KF.CONTROL |  | CASE.A01.KF.CONTROL.B, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | T.Arrangement, T.PersonAssessment, J.ActualControl | GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S26 | PARTIAL | RULE.A01.KF.CONTROL |  | CASE.A01.KF.CONTROL.B, CASE.A01.KF.SRC06.04, CASE.A01.KF.SRC06.05 | T.Arrangement, T.PersonAssessment, J.ActualControl | GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S27 | PARTIAL | RULE.A01.KF.PROFILE |  | CASE.A01.KF.PROFILE.B | T.PersonAssessment, T.IdentificationRoute, J.Route | GAP.A01.PROPOSED_POLICY |
| Q.A01.S28 | MODELED | RULE.A01.KF.FALLBACK |  | CASE.A01.KF.FALLBACK.B | T.Role, T.PopulationAssessment, R.FallbackGate |  |
| Q.A01.S29 | MODELED | RULE.A01.KF.FALLBACK |  | CASE.A01.KF.FALLBACK.B | T.Role, T.PopulationAssessment, R.FallbackGate |  |
| Q.A01.S30 | PARTIAL | RULE.A01.KF.SOE |  | CASE.A01.KF.SOE.B, CASE.A01.KF.SRC06.06 | T.Party, T.Role, T.PersonAssessment, R.SoeFiling, J.Route | GAP.A01.PROPOSED_POLICY, GAP.A01.STATE_CONTROL_SCOPE |
| Q.A01.S31 | PARTIAL | RULE.A01.KF.SOE |  | CASE.A01.KF.SOE.B, CASE.A01.KF.SRC06.06 | T.Party, T.Role, T.PersonAssessment, R.SoeFiling, J.Route | GAP.A01.PROPOSED_POLICY, GAP.A01.STATE_CONTROL_SCOPE |
| Q.A01.S32 | PARTIAL | RULE.A01.KF.SOE |  | CASE.A01.KF.SOE.B, CASE.A01.KF.SRC06.06 | T.Party, T.Role, T.PersonAssessment, R.SoeFiling, J.Route | GAP.A01.PROPOSED_POLICY, GAP.A01.STATE_CONTROL_SCOPE |
| Q.A01.S33 | PARTIAL | RULE.A01.KF.BRANCHES |  | CASE.A01.KF.BRANCHES.B | T.Party, T.Role, T.PersonAssessment, T.BranchAssessment, J.BranchInclusion | GAP.A01.CROSS_BORDER, GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S34 | PARTIAL | RULE.A01.KF.BRANCHES |  | CASE.A01.KF.BRANCHES.B | T.Party, T.Role, T.PersonAssessment, T.BranchAssessment, J.BranchInclusion | GAP.A01.CROSS_BORDER, GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S35 | PARTIAL | RULE.A01.KF.BRANCHES |  | CASE.A01.KF.BRANCHES.B | T.Party, T.Role, T.PersonAssessment, T.BranchAssessment, J.BranchInclusion | GAP.A01.CROSS_BORDER, GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S36 | PARTIAL | RULE.A01.KF.BRANCHES |  | CASE.A01.KF.BRANCHES.B | T.Party, T.Role, T.PersonAssessment, T.BranchAssessment, J.BranchInclusion | GAP.A01.CROSS_BORDER, GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S37 | PARTIAL | RULE.A01.KF.TRUST |  | CASE.A01.KF.TRUST.B | T.Role, T.BeneficiaryScope, T.Arrangement, T.PersonAssessment, J.Trust | GAP.A01.CROSS_BORDER |
| Q.A01.S38 | PARTIAL | RULE.A01.KF.TRUST |  | CASE.A01.KF.TRUST.B | T.Role, T.BeneficiaryScope, T.Arrangement, T.PersonAssessment, J.Trust | GAP.A01.CROSS_BORDER |
| Q.A01.S39 | PARTIAL | RULE.A01.KF.TRUST |  | CASE.A01.KF.TRUST.B | T.Role, T.BeneficiaryScope, T.Arrangement, T.PersonAssessment, J.Trust | GAP.A01.CROSS_BORDER |
| Q.A01.S40 | PARTIAL | RULE.A01.KF.TRUST |  | CASE.A01.KF.TRUST.B | T.Role, T.BeneficiaryScope, T.Arrangement, T.PersonAssessment, J.Trust | GAP.A01.CROSS_BORDER |
| Q.A01.S41 | MODELED | RULE.A01.KF.TRUST_PRODUCTS |  | CASE.A01.KF.TRUST_PRODUCTS.B | T.IdentificationRoute, J.Route |  |
| Q.A01.S42 | MODELED | RULE.A01.KF.TRUST_RELIANCE |  | CASE.A01.KF.TRUST_PRODUCTS.B, CASE.A01.KF.TRUST_RELIANCE.B | T.Evidence, J.Evidence |  |
| Q.A01.S43 | MODELED | RULE.A01.KF.ASSET_PRODUCTS |  | CASE.A01.KF.TRUST_PRODUCTS.B, CASE.A01.KF.ASSET_PRODUCTS.B | T.IdentificationRoute, J.Route |  |
| Q.A01.S44 | MODELED | RULE.A01.KF.ASSET_PRODUCTS |  | CASE.A01.KF.TRUST_PRODUCTS.B, CASE.A01.KF.ASSET_PRODUCTS.B | T.IdentificationRoute, J.Route |  |
| Q.A01.S45 | MODELED | RULE.A01.KF.EXCEPTIONS |  | CASE.A01.KF.EXCEPTIONS.B | T.IdentificationRoute, J.Route |  |
| Q.A01.S47 | MODELED | RULE.A01.KF.EXCEPTIONS |  | CASE.A01.KF.EXCEPTIONS.B, CASE.A01.KF.EXCEPTIONS.QFI.B, CASE.A01.KF.EXCEPTIONS.REP.B | T.IdentificationRoute, J.Route |  |
| Q.A01.S49 | MODELED | RULE.A01.KF.EXCEPTIONS |  | CASE.A01.KF.EXCEPTIONS.B, CASE.A01.KF.EXCEPTIONS.QFI.B, CASE.A01.KF.EXCEPTIONS.REP.B | T.IdentificationRoute, J.Route |  |
| Q.A01.S50 | PARTIAL | RULE.A01.KF.RISK |  | CASE.A01.KF.RISK.B | T.IdentificationRoute, J.Route | GAP.A01.CROSS_BORDER |
| Q.A01.S52 | PARTIAL | RULE.A01.KF.RISK |  | CASE.A01.KF.RISK.B | T.IdentificationRoute, J.Route | GAP.A01.CROSS_BORDER |
| Q.A01.S53 | PARTIAL | RULE.A01.KF.RISK |  | CASE.A01.KF.RISK.B | T.IdentificationRoute, J.Route | GAP.A01.CROSS_BORDER |
| Q.A01.S54 | DEFERRED | RULE.A01.KF.RISK_ACCEPT, RULE.A01.KF.SUSPICIOUS |  | CASE.A01.KF.RISK_ACCEPT.B, CASE.A01.KF.SUSPICIOUS.B |  | GAP.A01.INSTITUTION_AUTHORITY |
| Q.A01.S56 | PARTIAL | RULE.A01.KF.IDENTITY |  | CASE.A01.KF.IDENTITY.B | T.Party, T.Evidence, T.PersonAssessment, R.NaturalPerson, J.Evidence | GAP.A01.PROPOSED_POLICY |
| Q.A01.S57 | PARTIAL | RULE.A01.KF.IDENTITY |  | CASE.A01.KF.IDENTITY.B | T.Party, T.Evidence, T.PersonAssessment, R.NaturalPerson, J.Evidence | GAP.A01.PROPOSED_POLICY |
| Q.A01.S58 | PARTIAL | RULE.A01.KF.IDENTITY |  | CASE.A01.KF.IDENTITY.B | T.Party, T.Evidence, T.PersonAssessment, R.NaturalPerson, J.Evidence | GAP.A01.PROPOSED_POLICY |
| Q.A01.S59 | DEFERRED | RULE.A01.KF.BOMIS |  | CASE.A01.KF.BOMIS.B |  | GAP.A01.SYSTEM_QUERY_STATE |
| Q.A01.S60 | PARTIAL | RULE.A01.KF.DATES |  | CASE.A01.KF.DATES.B | T.Right, T.Arrangement, T.Role, T.PersonAssessment, J.FormationDate | GAP.A01.DATED_PUBLISHING, GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S61 | PARTIAL | RULE.A01.KF.DATES |  | CASE.A01.KF.DATES.B | T.Right, T.Arrangement, T.Role, T.PersonAssessment, J.FormationDate | GAP.A01.DATED_PUBLISHING, GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S62 | PARTIAL | RULE.A01.KF.DATES |  | CASE.A01.KF.DATES.B | T.Right, T.Arrangement, T.Role, T.PersonAssessment, J.FormationDate | GAP.A01.DATED_PUBLISHING, GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S63 | PARTIAL | RULE.A01.KF.DATES, RULE.A01.KF.HISTORICAL |  | CASE.A01.KF.DATES.B, CASE.A01.KF.HISTORICAL.B | T.Right, T.Arrangement, T.Role, T.PersonAssessment, J.FormationDate | GAP.A01.DATED_PUBLISHING, GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.S65 | DEFERRED | RULE.A01.KF.BOMIS |  | CASE.A01.KF.BOMIS.B |  | GAP.A01.SYSTEM_QUERY_STATE |
| Q.A01.S67 | DEFERRED | RULE.A01.KF.DIFFERENCE |  | CASE.A01.KF.DIFFERENCE.B |  | GAP.A01.DIFFERENCE_CROSSMONTH, GAP.A01.REPORT_DETAILS |
| Q.A01.S68 | DEFERRED | RULE.A01.KF.DIFFERENCE |  | CASE.A01.KF.DIFFERENCE.B |  | GAP.A01.DIFFERENCE_CROSSMONTH, GAP.A01.REPORT_DETAILS |
| Q.A01.S69 | DEFERRED | RULE.A01.KF.DIFFERENCE |  | CASE.A01.KF.DIFFERENCE.B |  | GAP.A01.DIFFERENCE_CROSSMONTH, GAP.A01.REPORT_DETAILS |
| Q.A01.S70 | DEFERRED | RULE.A01.KF.DIFFERENCE |  | CASE.A01.KF.DIFFERENCE.B |  | GAP.A01.DIFFERENCE_CROSSMONTH, GAP.A01.REPORT_DETAILS |
| Q.A01.S71 | DEFERRED | RULE.A01.KF.DIFFERENCE |  | CASE.A01.KF.DIFFERENCE.B |  | GAP.A01.DIFFERENCE_CROSSMONTH, GAP.A01.REPORT_DETAILS |
| Q.A01.S72 | DEFERRED | RULE.A01.KF.DIFFERENCE |  | CASE.A01.KF.DIFFERENCE.B |  | GAP.A01.DIFFERENCE_CROSSMONTH, GAP.A01.REPORT_DETAILS |
| Q.A01.S74 | DEFERRED | RULE.A01.KF.FEEDBACK |  | CASE.A01.KF.FEEDBACK.B |  | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.REPORT_DETAILS, GAP.A01.SYSTEM_QUERY_STATE |
| Q.A01.S75 | DEFERRED | RULE.A01.KF.FEEDBACK |  | CASE.A01.KF.FEEDBACK.B |  | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.REPORT_DETAILS, GAP.A01.SYSTEM_QUERY_STATE |
| Q.A01.S76 | DEFERRED | RULE.A01.KF.FEEDBACK |  | CASE.A01.KF.FEEDBACK.B |  | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.REPORT_DETAILS, GAP.A01.SYSTEM_QUERY_STATE |
| Q.A01.S77 | DEFERRED | RULE.A01.KF.FEEDBACK |  | CASE.A01.KF.FEEDBACK.B |  | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.REPORT_DETAILS, GAP.A01.SYSTEM_QUERY_STATE |
| Q.A01.S78 | DEFERRED | RULE.A01.KF.FEEDBACK |  | CASE.A01.KF.FEEDBACK.B |  | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.REPORT_DETAILS, GAP.A01.SYSTEM_QUERY_STATE |
| Q.A01.S79 | EXTERNAL_CONTEXT | RULE.A01.KF.SUSPICIOUS |  | CASE.A01.KF.SUSPICIOUS.B |  |  |
| Q.A01.S80 | MODELED | RULE.A01.KF.CONTINUOUS |  | CASE.A01.KF.CONTINUOUS.B | T.Right, T.PersonAssessment, T.PopulationAssessment, J.ChangeImpact |  |
| Q.A01.S82 | PARTIAL | RULE.A01.KF.DIFFERENCE, RULE.A01.KF.CONTINUOUS |  | CASE.A01.KF.DIFFERENCE.B, CASE.A01.KF.CONTINUOUS.B | T.Right, T.PersonAssessment, T.PopulationAssessment, J.ChangeImpact | GAP.A01.DIFFERENCE_CROSSMONTH, GAP.A01.REPORT_DETAILS |
| Q.A01.S83 | PARTIAL | RULE.A01.KF.GOVERNANCE |  | CASE.A01.KF.GOVERNANCE.B | T.PersonAssessment, T.Evidence, J.Evidence | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.PROPOSED_POLICY |
| Q.A01.S86 | MODELED | RULE.A01.KF.HISTORICAL |  | CASE.A01.KF.HISTORICAL.B | T.Right, T.PersonAssessment, J.FormationDate |  |
| Q.A01.S87 | PARTIAL | RULE.A01.KF.PROFILE, RULE.A01.KF.EXISTING |  | CASE.A01.KF.PROFILE.B, CASE.A01.KF.EXISTING.B | T.PersonAssessment, T.IdentificationRoute, J.Route | GAP.A01.SOURCE_PRECEDENCE |
| Q.A01.P01 | MODELED | RULE.A01.KF.PROFILE |  | CASE.A01.KF.PROFILE.B | T.PersonAssessment, T.IdentificationRoute, J.Route |  |
| Q.A01.P03 | PARTIAL | RULE.A01.KF.EQUITY, RULE.A01.KF.GOVERNANCE |  | CASE.A01.KF.EQUITY.B, CASE.A01.KF.GOVERNANCE.B, CASE.A01.KF.SRC06.01 | T.Party, T.Right, T.PersonAssessment, R.Equity25, T.Evidence, J.Evidence | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.PROPOSED_POLICY |
| Q.A01.P05 | PARTIAL | RULE.A01.KF.NOMINEE, RULE.A01.KF.IDENTITY, RULE.A01.KF.GOVERNANCE |  | CASE.A01.KF.NOMINEE.B, CASE.A01.KF.IDENTITY.B, CASE.A01.KF.GOVERNANCE.B, CASE.A01.KF.SRC06.03 | T.Right, T.Arrangement, T.Evidence, J.RightAttribution, T.Party, T.PersonAssessment, R.NaturalPerson, J.Evidence | GAP.A01.EVIDENCE_CONFLICT, GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.PROPOSED_POLICY |
| Q.A01.P07 | PARTIAL | RULE.A01.KF.RISK, RULE.A01.KF.RISK_ACCEPT |  | CASE.A01.KF.RISK.B, CASE.A01.KF.RISK_ACCEPT.B | T.IdentificationRoute, J.Route | GAP.A01.CROSS_BORDER, GAP.A01.INSTITUTION_AUTHORITY |
| Q.A01.P12 | PARTIAL | RULE.A01.KF.IDENTITY, RULE.A01.KF.GOVERNANCE |  | CASE.A01.KF.IDENTITY.B, CASE.A01.KF.GOVERNANCE.B | T.Party, T.Evidence, T.PersonAssessment, R.NaturalPerson, J.Evidence | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.PROPOSED_POLICY |
| Q.A01.P13 | PARTIAL | RULE.A01.KF.DATES |  | CASE.A01.KF.DATES.B | T.Right, T.Arrangement, T.Role, T.PersonAssessment, J.FormationDate | GAP.A01.DATED_PUBLISHING, GAP.A01.EVIDENCE_CONFLICT |
| Q.A01.P18 | DEFERRED | RULE.A01.KF.BOMIS, RULE.A01.KF.FEEDBACK |  | CASE.A01.KF.BOMIS.B, CASE.A01.KF.FEEDBACK.B |  | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.REPORT_DETAILS, GAP.A01.SYSTEM_QUERY_STATE |
| Q.A01.P21 | PARTIAL | RULE.A01.KF.IDENTITY, RULE.A01.KF.HISTORICAL, RULE.A01.KF.GOVERNANCE |  | CASE.A01.KF.IDENTITY.B, CASE.A01.KF.HISTORICAL.B, CASE.A01.KF.GOVERNANCE.B | T.Party, T.Evidence, T.PersonAssessment, R.NaturalPerson, J.Evidence, T.Right, J.FormationDate | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.PROPOSED_POLICY |
| Q.A01.P22 | PARTIAL | RULE.A01.KF.FALLBACK, RULE.A01.KF.RISK_ACCEPT, RULE.A01.KF.GOVERNANCE |  | CASE.A01.KF.FALLBACK.B, CASE.A01.KF.RISK_ACCEPT.B, CASE.A01.KF.GOVERNANCE.B | T.Role, T.PopulationAssessment, R.FallbackGate, T.PersonAssessment, T.Evidence, J.Evidence | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.PROPOSED_POLICY |
| Q.A01.P25 | PARTIAL | RULE.A01.KF.FILING, RULE.A01.KF.CONTINUOUS, RULE.A01.KF.EXISTING |  | CASE.A01.KF.FILING.B, CASE.A01.KF.CONTINUOUS.B, CASE.A01.KF.EXISTING.B | T.Right, T.PersonAssessment, T.PopulationAssessment, J.ChangeImpact | GAP.A01.DATED_PUBLISHING |
| Q.A01.P26 | PARTIAL | RULE.A01.KF.GOVERNANCE |  | CASE.A01.KF.GOVERNANCE.B | T.PersonAssessment, T.Evidence, J.Evidence | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.PROPOSED_POLICY |
| Q.A01.P28 | PARTIAL | RULE.A01.KF.GOVERNANCE |  | CASE.A01.KF.GOVERNANCE.B | T.PersonAssessment, T.Evidence, J.Evidence | GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.PROPOSED_POLICY |

## 逐条规则要素

### RULE.A01.KF.SCOPE

建模分类：EXTERNAL_CONTEXT；状态：EXTERNAL_CONTEXT；问题：Q.A01.S01, Q.A01.S02, Q.A01.S03, Q.A01.S04, Q.A01.S05；缺口：

处理理由：备案主体类型、承诺免报和申报责任属于登记备案范围；核心识别只接收目标主体及适用时点，不建立备案业务模型。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 备案主体（公司、合伙企业、外国公司分支机构）及个体工商户 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 前提 | 目标在2024年11月1日之后的中国备案义务范围内；识别登记主体本人，而非股东、分支母公司或机构开户客户的混合概念。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 判断条件 | 先确认登记性质：个体工商户无备案义务；外国公司分支机构须备案且不适用承诺免报；只有适用承诺免报的境内公司或合伙企业同时满足注册资本/出资额≤1000万元（含等值外币）、股东/合伙人全为自然人、没有股东/合伙人以外自然人实际控制或获益且无通过权益以外方式控制或获益，完成承诺后才能免备案。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 结果 | 外国公司分支机构须备案且不适用承诺免报；境内公司或合伙企业的全套免报条件均证实并完成承诺时才免备案，任一项不成立仍须备案。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 例外 | 未能确认任一自然人股东背后的代持或协议控制，不认定免报成立；登记股东全为自然人不能独立证明无其他控制或收益。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 缺证处理 | 登记文件、完整股东/合伙人名册及出资额、章程和受益/表决/控制安排、主体关于条件的承诺；外币等值核对口径需有依据。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 时间要求 | 2024-11-01 起；免报资格变化之日触发30日备案义务。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |

### RULE.A01.KF.FILING

建模分类：NO_MODEL_CHANGE；状态：NO_MODEL_CHANGE；问题：Q.A01.S07, Q.A01.S08, Q.A01.P25；缺口：

处理理由：设立、变更和存量主体的备案期限是申报义务与操作时限；权利生效日已由通用时间结构表达，无需备案流程或期限状态机。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 依法须备案的主体；分别判新设、设立无法系统办理及实施前已登记 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 前提 | 辨明主体设立登记发生在办法施行前还是施行后，是否能通过登记系统设立及备案，以及是否先曾合法承诺免报。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 判断条件 | 新设登记时系统备案；无法系统设立登记可现场登记并自登记日起30日内系统备案；受益人信息变更或承诺免报条件消失自变化日起30日系统备案；实施前已登记主体按办法2025-11-01前完成。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 结果 | 按设立或变更类别从相应事实日起分别办理初始或更新备案；实施前存量主体遵循正式办法截止日。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 例外 | 指南第二版的‘及时补报’不可擅自消灭正式办法明确的存量期限；身份变动与免报条件变化起算事实不同。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 缺证处理 | 设立登记日、系统可办状态、历史登记档案、权利变更生效文件、原免报承诺与条件变化材料。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 时间要求 | 备案义务自2024-11-01起；存量截止点以正式办法文本为准；现在须检查是否迟报，不逆向假造按时备案。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |

### RULE.A01.KF.PROFILE

建模分类：EXTERNAL_CONTEXT + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S12, Q.A01.S27, Q.A01.S87, Q.A01.P01；缺口：

处理理由：备案和金融机构独立识别是不同责任与结论语境；模型仅区分结论用途和判断时点，不将备案姓名直接当自然人权利事实。 非充分事实：备案有自然人姓名不能证明金融机构已合理核实其权利。；股东公司被标为实际控制企业、第三方百分比均不是最终自然人识别结论。 UNKNOWN：客户法定主体或上层法律关系不清，仍可确认备案义务和机构义务的责任边界，但具体自然人和风险结论保持UNKNOWN，按对应机构补登记链与原件。 证据要求：客户登记/备案记录及备案时点、银行业务时间。；机构逐层股权、收益与控制原件和身份佐证、独立核实及风险判断记录。 人工边界：备案主体对申报负责，适用的金融机构有权岗位对独立识别和风险负责；跨法规语境是否一致需核适用日期和主管权威，供应商不取代。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 2026-01-20起金融机构非自然人客户尽调与2024-11-01起备案主体申报 | T.PersonAssessment | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 同一对象可能同时存在中国登记备案、机构开户识别及其他监管语境的实际控制标签；须先划清各义务主体与日期。 | T.PersonAssessment | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 先依主体类型及日期确定是否有备案义务；另依客户组织形式与风险判机构识别义务。备案人填报与机构核实属于两个主体、两个目的，备案记录是可查询佐证但不是机构结论。公司法/国资交易的企业实际控制人不自动等于自然人受益所有人。 | J.Route.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 分别形成备案主体的申报义务判断及金融机构对客户受益所有人的独立识别、风险使用结论。 | J.Route | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 只有备案姓名、公司法控股标签或当地系统页面时，不可推定金融机构已完成独立识别。 | J.Route.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 本次业务日期、客户法定形态、登记主体与总分关系、机构自行收集的结构和可靠佐证。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 备案办法2024-11-01、金融机构办法2026-01-20；旧235/164通知自后者施行时废止，历史按当时制度还原。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.EQUITY

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S13, Q.A01.S14, Q.A01.P03；缺口：

处理理由：有效股权或合伙权益边、持有人和目标主体构成稳定结构；互异路径连乘汇总及含本数25%是可复用判断，未证路径保留未知。 非充分事实：第三方图谱展示单一持股比例，不能证明完整自然人路径或生效时点。；自然人控制一家公司，不等于持有该公司100%权益；中间节点持股70%不能直接当自然人70%。 UNKNOWN：某上层比例、代持实际归属或循环去重依据缺失时，受影响路径金额及该人的最终合计保持UNKNOWN；仅其他独立完整路径可以确证，绝不能把未知路径按零处理。 证据要求：每层官方登记及股东名册、章程/合伙协议，逐条权益比例和对应生效/终止文件。；计算账表列出各边原始资料、连乘、同人路径去重、最终汇总及矛盾来源。 人工边界：机构有权尽调人员对有争议的权益性质、代持效力及路径是否重复签核；系统可提供乘积，不独立认定最终法律权益。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 一般备案标准一；机构法人/非法人组织普通识别的第八条第一项 | T.Party | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 备案标准一或金融机构第八条第一项；以一个目标主体、一个有效时点、一名最终自然人为计算对象。 | T.Party | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 识别每一实际自然人和有效股权/合伙权益路径；直接比例计入，间接逐层依有效权益比例连乘，同一自然人的互异路径汇总；最终持有≥25%即符合（25%含本数），不把中间公司控制权自动换成100%权益。 | R.Equity25.expression | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 同一自然人互异有效路径汇总的最终股权或合伙权益达到25%（含本数），按权益标准列入。 | R.Equity25.result_binding | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 缺上层登记、路径有重复计算/循环、协议改变实际权益归属时保持比例和身份 UNKNOWN，不将第三方直接比例当最终权益。 | R.Equity25.on_unknown | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 逐层、同一时点股东名册及章程/合伙协议、各边比例、生效材料、代持及受益转移约定；计算路径与去重过程。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 按交易/判断时点取有效路径；股权变更及终止按法律关系效力追踪。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.NOMINEE

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S16, Q.A01.S21, Q.A01.P05；缺口：GAP.A01.EVIDENCE_CONFLICT

处理理由：名义登记人与最终拥有、收益、表决和控制人可分离；协议安排、权利范围和效力证据决定归属，不能以亲属或登记线索直接认定。 非充分事实：单纯同姓或母子、亲戚关系不证明代持；登记名义70%也不能证明最终拥有70%。；只知有分红转账而不知该权利由何份额产生，不能推最终收益权比例。 UNKNOWN：双方对协议真实性或权利归属存在矛盾且无可靠独立证据，则名义登记可确认但最终权利人及比例UNKNOWN；风险标记代持触发，加强措施可要求具有法律效力的协议。 证据要求：代持/表决权/分红转让原件与补充协议、生效与终止条款。；分红、投票、任免和实际决策记录及各方声明，冲突时独立资料印证。 人工边界：协议效力与实际履行冲突由机构有权人员复核，受益人必须是证据支持的自然人；供应商不得仅因亲属关系替换名义人。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 存在代持、隐名收益或亲属安排的法人/非法人组织 | T.Right | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 登记股东、协议受让方、收益/表决权享有人或真正决定者可能不是同一自然人。 | T.Right | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 分开登记股东、股权最终所有人、收益权人、表决权人及实际控制人：核对代持协议的权利、履行和期间；若名义人不是最终拥有者，不能单凭工商份额认其为受益人；真实权利人按对应标准识别，不以亲属称谓自动转移权益。 | J.RightAttribution.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 依已证实的实际权益、收益、表决和控制分离关系分别给出自然人结论；名义人仅在自身另有最终权利时列入。 | J.RightAttribution | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 亲属关系、口头说法或单一登记均不能证明权利转移；未取得有效协议及履行证据时名义归属与最终归属保留冲突。 | J.RightAttribution.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 经核实的代持/收益/表决协议、权利生效和终止条款、分红及投票记录、相关方确认与独立资料。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 协议效力与实际履行须对应本次判断日；历史名义记录不能覆盖已转移权益。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.RETURNS_VOTES

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S17, Q.A01.S18, Q.A01.S20；缺口：

处理理由：收益权和表决权各有独立的持有人、比例和有效期；未符合权益标准一者任一权利达到25%才符合标准二，控制须另判。 非充分事实：单笔分红流水不能单独证明最终收益占比≥25%。；持有投票委托草案或名义股权比例不能证明生效的表决权、最终收益或实际控制。 UNKNOWN：权利委托范围或期限不明时只保留已证实的股权结论，标准二和相应控制UNKNOWN；要求补约定、决议或投票记录，不能把尚未生效授权合并计算。 证据要求：权益链及份额，分红和收益转让协议，投票委托、一致行动协议的表决范围与期限。；实际投票、分红、任免及重大决策行为证据，权利生效/终止时间。 人工边界：机构对协议效力、委托行使及与股权重叠范围复核，机器只辅助计算权利比例，不把一人重复算成两名受益人。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 一般标准二；仅针对未满足持有权益标准一的自然人 | T.Right | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 仅在同一自然人未满足最终权益≥25%的标准一前提下，进一步判断标准二与三的适用；权益满足标准一者不重复归类标准二。 | T.Right | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 先判是否已按最终权益≥25%符合标准一；未达者分别核对收益分配和表决权的有效来源、期限及比例，任何一项最终享有≥25%即按标准二；仅该人未满足标准一且同时有可证实实际控制时才须同时记录标准二和标准三关系，不将经济收益、表决委托和股权混为一谈。 | R.BenefitVote25.expression | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 未按权益标准入选但最终收益或表决权任一达到25%（含本数）的自然人，按标准二识别，控制关系另记。 | R.BenefitVote25.result_binding | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 只知股东原始比例、获利转账或委托意向不证明最终收益/表决比例；收益合同未生效或授权过期时不能按25%认定。 | R.BenefitVote25.on_unknown | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 收益分配/表决权协议、章程、可委托权种、有效期、分红凭证或决议/投票记录、受让人与对象对应。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 以各权利实际生效及终止日判断；既有标准一者不重复套仅限未达标准一的标准二。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.CONTROL

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S21, Q.A01.S22, Q.A01.S23, Q.A01.S24, Q.A01.S25, Q.A01.S26；缺口：GAP.A01.EVIDENCE_CONFLICT

处理理由：人事、重大决策、财务及重要资产的最终支配安排是稳定事实；是否构成实际控制取决于权限与实际行使证据，职务和签字仅是线索。 非充分事实：第一大股东、法定代表人、总经理、近亲属、共同签署付款单或第三方‘实控人’标签，都不能单独证明最终决定权。；孤立一次大额收付仅证明经办或签字，不证明长期支配重要资金。 UNKNOWN：关键控制协议或决策行为证据未得、只存在名义职位或相互矛盾的权限记录时，对该自然人实际控制保持UNKNOWN；不能把未知控制当作‘三标准均无人’进入备位。 证据要求：生效的协议/章程、股东会和董事会决议、实际任免记录、预算和资金审批链、重要资产持续使用与控制凭证。；自然人权力来源、生效终止日期、共同控制签字机制及与实际行为不一致时的解释。 人工边界：决定权的实际效力、共同控制是否成立及冲突证据权重必须由有权尽调人员基于法律文件和行为记录复核；自动标签只能提出候选。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 一般标准三，先分清自然人是否已按权益达到标准一 | T.Arrangement | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 对象是具体自然人而非公司、股东集团标签；需分别核对是否已达标准一及是否通过本人或联合机制实际支配目标。 | T.Arrangement | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 找出单独或联合对主体具有最终决定能力的自然人及协议/关系路径；分别核实其能否决定人事任免、重大经营管理决策、财务收支或长期支配重要资产/主要资金，判断的是对组织的实际控制能力，不是一次签字或职务名称；联合控制要说明每个人的权力与共同决策机制。 | J.ActualControl.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 经证实单独或联合最终实际决定主体人事、重大决策、财务或重要财物的自然人，按实际控制标准识别。 | J.ActualControl | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 第一大股东、法定代表人、普通执行人、朋友/亲属关系和一次付款签名仅是线索；缺生效协议、决议、持续履行记录时实际支配为 UNKNOWN，不得因未发现股权人立即认定无控制。 | J.ActualControl.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 协议和章程中的权限、董事及重大决策记录、任免与预算授权、银行账户/重要资产长期支配事实、联合行动及实际行使证据。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 实际控制形成及终止与协议生效和长期事实持续区间对应，不以后来的标签追溯历史。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.FALLBACK

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S28, Q.A01.S29, Q.A01.P22；缺口：

处理理由：实际负责日常经营的角色需可指向自然人；仅在前三项均被充分证否时适用备位，任一未知不能当作不存在。 非充分事实：未检索到≥25%工商持股不能证明收益、表决或协议控制均不存在。；登记法代或董事长职务本身不能证明该人真实负责日常经营管理。 UNKNOWN：存在未取得的上层结构、代持条款或控制协议时至少该项为UNKNOWN，因此‘三项均不存在’不能成立，暂停备位；须补该项证明而非猜出管理者。 证据要求：完整逐层权益名册和收益/表决协议、控制权及履行核实记录、三类候选排除证明。；当期任职文件、管理决议和实际日常管理记录，证明备位自然人并非仅挂名法代。 人工边界：有权机构人员确认每一自然人识别标准已充分核实且无符合者，再复核日常管理人选；不能触发自动‘零人即法代’填值。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 在按普通识别标准逐一核实之后确无满足三类自然人的主体 | T.Role | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 针对已取得完整所有权、收益/表决权与控制资料的同一主体及日期，原则上按一般三标准识别自然人。 | T.Role | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 逐项完成权益、收益/表决、实际控制的自然人查找；只有三项均确定不存在，才认定真实负责日常经营管理人员作为备位（指南要求至少一名最高层级日常管理人员）；备位是特定条件结果，不是实质自然人控制权的证明。 | R.FallbackGate.expression | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 经查三项一般标准确实没有符合者，才将真实负责日常经营管理的人员按备位识别。 | R.FallbackGate.result_binding | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 结构分支未追完、代持协议缺失或控制争议属 UNKNOWN 而不是三项 FALSE，不得因此直接填法定代表人兜底。 | R.FallbackGate.on_unknown | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 完整自然人候选及排除理由、章程/决议、经营管理职责、任职记录与实际履职证据。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 按判断日确认三项均不成立和管理者任职存续。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.SOE

建模分类：CORE_STRUCTURE + DOMAIN_DECISION + EXTERNAL_CONTEXT；状态：PARTIAL；问题：Q.A01.S30, Q.A01.S31, Q.A01.S32；缺口：GAP.A01.STATE_CONTROL_SCOPE

处理理由：国资股权与控制事实、法定代表人角色影响特例人选；国资监管类别只是适用上下文，备案应当视同与机构可以简化须分别判断。 非充分事实：注册名称含‘国’、国有出资为第一大股东或第三方标‘国资实际控制’，均不能独立证明属于独资或控股特例。；国有参股路径停止穿透不意味着可跳过其余股东与非股权控制。 UNKNOWN：无国资产权链或相对控股的决定权证据时国控特例资格UNKNOWN；不得先把法代确认为备案或机构受益人，仍应尽力完成可证实社会资本及控制路径。 证据要求：官方产权登记、逐层国有资本出资、章程与表决安排及实际支配文件、经核实的法代任职。；参股企业社会资本所有权及控制资料、机构风险分类依据及适用时点。 人工边界：国有控股与参股边界由审查人核官方材料、控制权协议及适用法规；有争议的第32号令类型需权威解释，不允许供应商代码自动改写UBO结论。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 备案的国有独资/国有控股公司；金融机构对相应国资组织及国有参股 | T.Party | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 备案国有独资/控股与机构对国有企业及国有参股的简化分别判断，且目标公司应先确证有效国资产权和控制。 | T.Party | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 先用产权、章程、协议和实际支配证据区分国有独资/控股与仅参股；确属独资或控股公司时，2024年备案办法第七条要求‘应当’将法定代表人视为受益所有人备案，而金融机构2025年第12号令第十一条仅规定对相应类别‘可以’认定法定代表人，需核客户组织事实及风险；仅国资参股按一般标准核社会资本和非股权控制，国有资本部分可以不再穿透。 | R.SoeFiling.expression, J.Route.criteria | MIXED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 国有独资/控股备案按第七条应当报法定代表人；机构对适格国企依第十一条可以选择对应认定，不能混写成备案与机构相同的义务；国资仅参股按一般标准核社会资本及控制。 | R.SoeFiling.result_binding | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 国资占比、企业名称或某国企为股东，单独不足证明国控；国有参股‘国资不穿透’不能免除社会资本和协议控制核实。 | R.SoeFiling.on_unknown | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 官方登记/国资出资链、股权及表决结构、章程和实际控制资料、法定代表人当前任职；机构简化资格及风险审查。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 按适用日国资及控制状态识别，任职更换触发相应更新核查。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.BRANCHES

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S33, Q.A01.S34, Q.A01.S35, Q.A01.S36；缺口：GAP.A01.CROSS_BORDER, GAP.A01.EVIDENCE_CONFLICT

处理理由：总分关系、存续期间和分支高管角色是稳定结构；国内承继及外国分支双路径依有效所属关系和总部权利证据判断。 非充分事实：同名称、旧总公司登记号码、分支独立营业执照，不足证明当前总分关系和总部自然人。；外国公司本国申报豁免或仅一名分支法代不能替代总部自然人穿透。 UNKNOWN：总公司存续/所属链断裂时，分支与总部自然人关系UNKNOWN；可独立核分支高管，但不能以其自动替代总部人选；补总分变更、恢复及境外登记材料。 证据要求：分支及总公司当前/历史登记、注销和恢复文件，总分关系证照及有效期。；总部章程和股权控制协议、原机构尽调材料及复用时间；外国分支高管任命与履职材料。 人工边界：总分状态异常与资料复用由机构有权人员判定，境外材料真实性和增补风险措施不能从执照字段自动完成。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 分支机构作为机构客户；外国公司分支另负备案义务 | T.Party | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 明确该营业执照属于境内组织的国内分支还是外国公司的中国分支，确认其所属主体在相关时点存续与总分关系。 | T.Party | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 先证明所属主体与分支的真实有效关系和时点；国内分支通常承继所属法人/非法人组织的受益人，所属主体已作合规尽调才可复用既有资料；外国公司分支识别所属外国公司按一般标准的自然人并额外至少一名该分支高级管理人员，备案亦需对应两部分。 | J.BranchInclusion.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 国内分支通常承继已核实所属主体的受益人；外国公司分支另须纳入至少一名自身高管及所属外国公司的合格自然人。 | J.BranchInclusion | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 分支执照、旧总公司名称或注销时旧股权表不能独立证明当前总分关系；境外母公司当地申报豁免不适用于中国备案。 | J.BranchInclusion.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 分支及所属主体登记及存续证明、历史/恢复登记记录、总部最新结构与协议、分支高级管理人员任命及有效期。 | T.BranchAssessment.evidence, T.BranchAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 总公司强制注销、恢复登记期间分别标注状态；旧识别仅在时点相符且已核实条件下复用。 | T.BranchAssessment.as_of, T.Role.effective_start, T.Role.effective_end_bounds | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.TRUST

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S37, Q.A01.S38, Q.A01.S39, Q.A01.S40；缺口：GAP.A01.CROSS_BORDER

处理理由：信托当事人角色、未指定受益范围和处分或指定权安排独立存在；自然人识别须穿透非自然人当事人且不能虚构潜在人名。 非充分事实：某金融受托人名称不等于四类自然人及其他最终控制人的完整名单。；受益人尚未具体指定，不等于无人受益也不得猜出潜在名单中固定自然人。 UNKNOWN：非自然人当事人上层证据不足则其最终控制自然人UNKNOWN；可如实记录潜在受益范围，却不能填具体已确认受益人；补信托合同条款与相应当事人链。 证据要求：信托合同、修订和公告登记，四类当事人名册与监察人设置、受益范围或指定权条款。；非自然人股权控制资料，财产处分/投资分配/受托人更替记录。 人工边界：对信托财产权和指定权效力的解释由有权尽调人员及必要法律支持复核，自动穿透不能代替控制权判断。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构信托受益所有人识别，第十二条 | T.Role | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 被识别对象是真正信托关系而非普通法人、证券份额或资管产品；先按第十二条识别信托当事人与其他控制者。 | T.Role | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 逐一确认委托人、受托人、受益人、监察人（若有）；非自然人当事人逐层追溯最终有效控制信托的自然人；另外找有权处分信托财产、决定投资/分配、变更信托/受益人/受托人的其他最终自然人；受益人未具体确定时记录类别或指定权范围内潜在受益人，不编造确定人名。 | J.Trust.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 按信托当事人、逐层追溯的非自然人当事人及其他最终有效控制人列完整自然人范围；未定受益人记潜在范围。 | J.Trust | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 某一受托人名称或仅有最终收益名单不足以覆盖其他权限；受益人尚未指定不等于信托无须识别。 | J.Trust.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 信托合同与修订、当事人及资格名单、财产处分和受益人指定权限、登记和分配记录、非自然人穿透路径。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 设立及存续期间的指定、资格丧失与替换均需分别核实。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.TRUST_PRODUCTS

建模分类：EXTERNAL_CONTEXT + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S41；缺口：

处理理由：信托服务类别、结构复杂度和风险是识别深度的必要输入；只表达简化资格判断，不建信托产品全域。 非充分事实：产品名称写‘信托’或‘资产服务’不证明满足简化类别和低风险。 UNKNOWN：服务类别、结构或风险不能证实，简化资格UNKNOWN；先按信托第十二条完整查找当事人和控制自然人。 证据要求：信托合同与当事人/受益范围资料，服务类型证明及法律效力期间。；信托结构图、风险评级依据与简化理由。 人工边界：有权尽调和风险人员确认信托类别与简化条件，不能由产品名称自动放行。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构识别财富管理、公益慈善、民事、外国及其他资产服务信托 | T.IdentificationRoute | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 核实信托服务类型；第十三条对财富管理、公益慈善、民事和外国信托实行第十二条完整识别，其他资产服务信托有特殊条件。 | T.IdentificationRoute | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 财富管理服务信托、公益慈善信托、民事与外国信托按第十二条逐一识别自然人当事人及其他最终有效控制人；仅财富管理服务信托以外的其他资产服务信托同时结构简单且洗钱恐怖融资风险较低，才可以简化。 | J.Route.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 前四类完整按第十二条识别；其他资产服务信托只有结构简单且低风险时可简化，不得仅凭信托名称概括全部信托。 | J.Route | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | ‘信托产品’或‘已备案资管’名称不等于一律简化；受托人自报且有明显疑点不能视作确认。 | J.Route.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 信托/产品合同及性质、登记募集证明、持有人或信托当事人资料、服务角色、产品风险和受托人体系有效性、疑点处理记录。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 按产品存续及当事人变化重新审查简化适格与所供资料。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.ASSET_PRODUCTS

建模分类：EXTERNAL_CONTEXT + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S43, Q.A01.S44；缺口：

处理理由：产品募集备案、金融机构管理或受托、托管服务与风险共同限定简化资格；只保留这些输入与人选结果。 非充分事实：‘公开产品’名称、某一备案编号或代销服务，单独不足证明存在金融机构管理/受托与托管服务。 UNKNOWN：管理受托身份或备案/募集资料缺失时公开产品简化资格UNKNOWN；先按产品真实所有权控制和风险作一般识别并补合同及登记。 证据要求：产品合同说明书、管理或受托机构身份、募集/发行及备案凭证、托管服务合同。；份额持有人名册与最终受益/表决控制材料、风险评估记录。 人工边界：机构有权尽调岗确认服务角色与产品形态、风险岗核简化，供应商资管分类不构成批准。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构对资产管理信托等资管产品及提供资金托管等服务的产品客户 | T.IdentificationRoute | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 产品合同和服务关系已确定；普通识别参照第八条，公开募集简化路径有产品管理/受托人与登记条件。 | T.IdentificationRoute | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 先按产品风险和具体所有权控制结构参照第八条识别；产品以金融机构为管理人或受托人、公开募集或发行且依法备案/登记，且本机构提供资金托管等服务时，可以简化认定管理产品的自然人为受益所有人。其他金融机构管理/受托产品由提供托管等服务机构充分评估风险，企业或职业年金等低风险产品可简化。 | J.Route.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 对不满足公开募集+金融机构管理/受托+依法备案登记+托管服务全部条件的产品，不能套用该条公开产品简化；其他产品应按结构和风险参照一般标准。 | J.Route | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | ‘信托产品’或‘已备案资管’名称不等于一律简化；受托人自报且有明显疑点不能视作确认。 | J.Route.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 信托/产品合同及性质、登记募集证明、持有人或信托当事人资料、服务角色、产品风险和受托人体系有效性、疑点处理记录。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 按产品存续及当事人变化重新审查简化适格与所供资料。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.TRUST_RELIANCE

建模分类：EXTERNAL_CONTEXT + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S42；缺口：

处理理由：跨机构资料采信是来源质量和机构履责判断；保留证据来源、疑点及采信结论，不建立合作办理流程。 非充分事实：受托人为金融机构、合作多年或提供一份名单，都不能证明体系健全及每个疑点已处理。 UNKNOWN：对合作体系可靠性或权利明显疑点尚未澄清，资料采信结论UNKNOWN；可要求受托人重核或自行核实，并保留本机构风险处理责任。 证据要求：信托受益人清单、权利材料、双方合作/托管合同与服务类别。；受托人体系评估与有效履责证明、疑点沟通与重核结果、拒绝提供或重大风险记录。 人工边界：有权机构判断是否可采信、要求重新识别和风险措施；不能由对方合同约定豁免本机构独立责任。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 受托信托公司与其他金融机构建立业务关系、存续合作、提供托管经纪等服务 | T.Evidence | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 有受托信托公司提交的信托受益人资料；识别合作类型是否属于第十五条采信范围。 | T.Evidence | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 信托公司须提供受益人信息和材料；对财富管理服务信托以外其他营业信托，提供托管/经纪服务的非信托机构确信受托人反洗钱体系健全且已有效履责，才可采信。资料明显疑点或核实明显瑕疵时可以要求重新识别；拒绝提供、重大风险或系统性缺陷时视情采取风险措施。 | J.Evidence.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 受托材料有条件采信；有明显瑕疵时可要求重核，拒不配合或体系缺陷时走风险措施；不得以合作关系自动免除本机构义务。 | J.Evidence | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | ‘信托产品’或‘已备案资管’名称不等于一律简化；受托人自报且有明显疑点不能视作确认。 | J.Evidence.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 信托/产品合同及性质、登记募集证明、持有人或信托当事人资料、服务角色、产品风险和受托人体系有效性、疑点处理记录。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 按产品存续及当事人变化重新审查简化适格与所供资料。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.EXCEPTIONS

建模分类：EXTERNAL_CONTEXT + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S45, Q.A01.S47, Q.A01.S49；缺口：

处理理由：法定客户类别与风险闸门决定免识别或简化资格；资格未知即不适用，但无需复制邻接机构客户分类体系。 非充分事实：名称中的‘政府’、‘协会’或‘国有’，不能独立证明具体法定豁免或简化类别。；仅凭客户口述低风险或供应商预分类，不能证明第十一条风险闸门已通过。 UNKNOWN：组织性质、负责人或风险事实不能准确判断，免识别/简化资格UNKNOWN且依法不得采用；继续取得法定组织文件和风险资料按一般标准识别，必要时加强。 证据要求：主体设立/登记、组织身份及相应负责人、投资人、法代、授权代表、业务负责人的官方证明、授权范围和有效时间；外国常驻代表机构还需所属外国企业及本机构高管资料。；客户风险评级依据、代持与结构检查、第二十条特定风险排查及简化/拒简化理由。 人工边界：由机构有权人员依据客户与交易风险决定是否适用、停止或恢复简化；自动登记类别映射不能代替机构风险评估。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构客户尽调，区别免识别和条件性简化 | T.IdentificationRoute | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 机构核实的是客户组织本身可否享受金融机构第十条免识别或第十一条简化，而非该客户是否免向BOMIS备案。 | T.IdentificationRoute | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 先以有效设立材料确认第十条机关法人及派出机构、事业单位、基层自治组织、农村集体、政府间国际组织、外国政府及其驻华机构等法定类别，匹配者可以免识别。非第十条主体仅在第十一条对应类别且风险闸门允许时简化：无法人资格的专业服务机构可认定机构负责人；合作经济组织先按第八条，若无较高风险可认定法定代表人；个人独资企业无较高风险可认定投资人；合格境外投资者无较高风险可在法定代表人、授权代表或业务负责人中按实际角色认定；外国企业常驻代表机构先参照外国分支第九条第二款，且无较高风险时才可按风险简化，并非直接固定为负责人；社会组织按风险状况简化但不能预设统一人选；国有企业另按专门规则判断法代路径。类别或风险无法准确判断，或发生第二十条特定风险时，不得沿用免识别或简化。 | J.Route.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 第十条确证类别可以免识别；第十一条仅在其自身类别、人选和风险条件成立时，采用该类别允许的简化结果。无法证明类别、候选人或风险闸门时，回到一般或加强识别。 | J.Route | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 主体名字含‘协会’或‘国企’、客户声明低风险不能证明法定类别和风险闸门；专业机构负责人、个人独资投资人不能横向代替其他类别。 | J.Route.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 机构设立及登记资格、组织方式、负责人/投资人官方材料、风险评估记录与第二十条触发事实。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 按办理时点组织形式和风险状态判断，客户变化后重评简化资格。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.IDENTITY

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S09, Q.A01.S10, Q.A01.S56, Q.A01.S57, Q.A01.S58, Q.A01.P05, Q.A01.P12, Q.A01.P21；缺口：GAP.A01.PROPOSED_POLICY

处理理由：自然人身份、权利事实、证据来源和适用时间须分开记录；可靠性与充分性影响能否形成已核实人选。 非充分事实：透明国企等仅凭第三方标签不能套用出生年月+照片例外。；单独工商出资比例或仅BOMIS身份字段完整，不证明最终权利及其时间已经合理核实。 UNKNOWN：自然人身份官方信息冲突或权利文件缺生效条款时，分别把身份同一性或关系时间维持UNKNOWN；不能因另一维度已证实便填全已核，须补官方核验/有效原件。 证据要求：官方登记/透明主体资格材料、身份官方查询结果或身份证件及补充文件。；章程、合伙/信托及产品权益资料、各关系生效文件、风险判断、交叉验证与资料取舍理由。 人工边界：官方透明客户身份资格、低风险采信理由及信息可靠性由机构有权人员复核；备案主体自行负责其地址联系方式申报。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 机构一般客户身份与权利状况、经官方验证高透明度客户身份字段例外；备案字段另按2024年第3号令第十一条。 | T.Party | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 一般非自然人客户的机构受益所有人识别与备案填报字段分开；机构透明客户具有第十八条特定较少身份字段例外，须先有官方透明性质核验证据。 | T.Party | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 区分识别谁、为何及何时有权：一般客户留存自然人姓名、性别、国籍、出生日期、身份证明类别号码与有效期限、权利类型、比例/控制方式和形成终止时间；仅对上市及经官方核实的特定高透明国企客户，可按第十八条至少留姓名、性别、国籍、出生年月及可识别身份照片；身份优先官方渠道，不能用时身份证件及补充材料；权利以客户资料为基础并按风险核对官方、公开、机构发现信息。确属低风险才可采信客户权利信息；部分佐证足够时记录取舍理由。另外，备案主体按照2024年第3号令第十一条逐人填报经常居住地或工作单位地址、联系方式，及证件有效期限；该备案字段不与机构一般识别留存字段混同。 | R.NaturalPerson.expression, J.Evidence.criteria | MIXED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 逐人留存机构要求的身份、权利类型、比例或控制方式及有效时间，以风险相称可靠来源完成合理核实；备案另按第3号令第十一条填字段。 | R.NaturalPerson.result_binding | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 仅客户自报、第三方股权比例或身份证复印件在可得官方独立渠道且有冲突时不足；信息字段齐全不代表权利已核实。 | R.NaturalPerson.on_unknown | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 登记章程/合伙协议、股东董事及管理名单、有效身份件与官方核验、权利文件、日期、交叉核实及风险取舍记录。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 资料与权利状态必须同一适用时点；缺生效日时不可自动填默认日。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.RISK

建模分类：EXTERNAL_CONTEXT + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S50, Q.A01.S52, Q.A01.S53, Q.A01.P07；缺口：GAP.A01.CROSS_BORDER

处理理由：洗钱风险与加强措施属于邻域，但会阻断简化并决定识别深度；仅引用风险等级及是否可简化，不建AML风险或措施模型。 非充分事实：仅属境外股东、仅有软件标签‘复杂’、仅遭客户拒绝，均不能无其他事实直接断言洗钱或代持确实发生。；统一把所有客户识别阈值改为10%或一律要求实地走访，不能证明个案措施与风险相称。 UNKNOWN：无法核实境外上层、代持归属或真正资金支配时保留对应人选/比例UNKNOWN，启动补证与风险评估；不得把未知自动变为低风险或直接替机构决策拒办。 证据要求：具体国家地区与风险来源资料、境外登记查询/认证日志、循环路径图和代持协议或拒绝提供记录。；客户变化时间表、交易异常证据、机构风险评级、选措施理由及加强后核实结果。 人工边界：机构有权风险岗选择并调整相称措施、批准/限制/拒办另依据自身权限及法定风险边界；自动化可预警但不可替代风险判断。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 机构客户风险管理及第八条普通阈值的边界 | T.IdentificationRoute | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 金融机构已识别到第十二号令第二十条对应特定事实，并区分一般识别标准与加强措施的自由裁量范围。 | T.IdentificationRoute | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 客户高风险国家地区、境外上层无法核验、循环交叉持股、代持协议、异常频繁换人、重大差异或洗钱嫌疑等，触发按事实选择一种或多种相称加强措施；可取得独立可靠信息、补法效代持协议、回访、加强监测、降低比例阈值（如10%，仅可选加强不是普通25%改法）或提高更新频率。自然人客户较高风险还应视情筛查其作为受益人的本机构非自然人客户。 | J.Route.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 特定风险事实触发与风险相称的一项或多项加强识别措施，效果不充分继续评估剩余风险；10%仅属可选加强示例。 | J.Route | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 发现触发事实而仅维持低风险客户自报、把10%改作所有客户法定阈值、或按同一清单一刀切，均不能证明相称。 | J.Route.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 风险地区及交易证据、境外登记失败记录、循环路径、代持原始协议、异常变化和关联客户清单、措施选用及效果。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 风险事实发生和消失均影响加强程度；不能用后来的无风险状态抹去触发时记录。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.RISK_ACCEPT

建模分类：EXTERNAL_CONTEXT；状态：EXTERNAL_CONTEXT；问题：Q.A01.S54, Q.A01.P07, Q.A01.P22；缺口：

处理理由：剩余风险接受、高管批准、交易限制和拒办属于机构客户关系治理；不建立审批或客户准入模型。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 机构已发现需要加强尽调或风险超出管理能力的客户 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 前提 | 已按第二十条风险事实采取必要相称加强措施，并能够评估客户剩余洗钱恐怖融资风险及机构承受能力。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 判断条件 | 在相称加强识别后仍有风险，按具体风险可在建立/维持关系或办理业务前取得高级管理层批准并合理限制交易方式、规模、频率或业务类别；风险确超机构管理能力应拒绝业务或终止关系，不因有疑点便一律拒绝，也不因管理层签名绕过必要核实。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 结果 | 增强核实后对可管风险按情形取得高管批准和适配交易限制；超出机构管理能力须拒办或终止。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 例外 | 未有风险等级、补证结果和风险能力判断时，不能自动批准、拒办或解除。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 缺证处理 | 风险评估与已采取措施、补件及客户回应、授权审批记录、剩余风险与交易限制适配材料。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 时间要求 | 决定针对实际业务关系时点，不追认未经必要审查的历史审批。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |

### RULE.A01.KF.DATES

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S60, Q.A01.S61, Q.A01.S62, Q.A01.S63, Q.A01.P13；缺口：GAP.A01.DATED_PUBLISHING, GAP.A01.EVIDENCE_CONFLICT

处理理由：每项权利和角色的法律生效、终止、首次达标及当前状态日期形成核心时间结构；缺证只能保留区间或未知，不能以披露日补精确日。 非充分事实：登记公示日、BOMIS备案日、机构最新查询日或最近增持日，均不能单独证明首次达标日。；同一人一直在名单内不代表其53%当前比例自最初28%时起已生效。 UNKNOWN：仅有月份/生效区间但无法得到具体日期时保留该精度和证据缺口，不把月首或年初作为‘推定日’；关系是否存在可以部分确定，具体形成日仍UNKNOWN。 证据要求：股权转让协议与交割/批准证明、章程及股东决议、合伙协议、控制权协议含生效/终止条款。；历史比例与控制状态变化清单，工商记录和实际关系生效依据的不一致说明。 人工边界：生效条件是否完成及交易历史还原涉及文件解释，应由有权人员判定或请求法律材料；自动系统只维持可审计多时点版本。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 备案及机构识别的有效受益所有权关系 | T.Right | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 明确具体自然人、权利种类和目标主体，并区分原入选、当前比例变动与权利终止事件。 | T.Right | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 分别记录首次跨入识别标准、当前权益比例或控制关系的形成、终止、登记披露、机构核实和备案日；法规要求的是法律关系生效的形成/终止时间；逐份看章程、转让、决议和控制权协议何时生效；未退出时增持可能改变当前比例的形成日，却不抹掉首次入选日；退出后重入需建立新的权利区间。 | J.FormationDate.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 区分首次达到识别标准的日期、当前权利状态生效日及权利终止日，并另外保留披露、核实与备案日期。 | J.FormationDate | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 工商变更登记日、客户查询日、最新增持日不必等于关系生效日；仅知月份不能系统自动补一日。 | J.FormationDate.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 附生效条款的股权转让/控制协议、章程决议、批准条件完成证明、比例历史和权利终止文件。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 保留有效区间、精度及冲突；对历史交易按交易发生时证据与当时规则还原，不将当前人选追责历史。 | T.Right.formation_bounds, T.Right.effective_end_bounds, T.Arrangement.formation_bounds, T.Arrangement.effective_end_bounds, T.Role.formation_bounds, T.Role.effective_end_bounds | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.BOMIS

建模分类：EXTERNAL_CONTEXT；状态：EXTERNAL_CONTEXT；问题：Q.A01.S59, Q.A01.S65, Q.A01.P18；缺口：

处理理由：BOMIS备案查询只是外部观察和核对材料，不替代机构对自然人身份与权利的独立核实；核心只保留来源及比较时点。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构在核实符合2024年第3号令第二条的非自然人客户 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 前提 | 金融机构核实的是依法须备案的非自然人客户；先根据备案办法第二条辨别目标是否属于中国备案范围。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 判断条件 | 先凭独立合理方式识别核实自然人，再查询核对BOMIS相应客户同一适用时点的备案身份、关系及时间；查询是对照和疑点发现，不替代机构结构核查及风险判断。对于不属备案主体的客户，不虚构必有BOMIS备案。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 结果 | 本办法适用的金融机构对符合备案办法第二条的非自然人客户自行核实后，须将识别结果与系统备案逐人逐权利逐时点核对并处理差异；并不限于银行。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 例外 | 查无记录或名单一致不等于无人、全部权利一致或核实完成；自动批量匹配只是辅助手段。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 缺证处理 | 机构独立识别材料、客户法定主体与备案义务证明、系统查询结果和时间戳、备案与机构识别字段逐项比较。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 时间要求 | 同一时点核对，备案更新滞后可形成差异或未备案路径，不能混合历史快照。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |

### RULE.A01.KF.DIFFERENCE

建模分类：EXTERNAL_CONTEXT；状态：EXTERNAL_CONTEXT；问题：Q.A01.S67, Q.A01.S68, Q.A01.S69, Q.A01.S70, Q.A01.S71, Q.A01.S72, Q.A01.S82；缺口：

处理理由：重大差异是备案与机构结果之间的监管反馈分类；本领域保留身份、关系类型和年月的可比较事实，不建立报告业务模型。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 对已查询核对且可比较的同一客户/同一受益人记录 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 前提 | 适用本办法的金融机构自行识别结果与BOMIS针对同一须备案客户及同一自然人形成可比快照；先排除单纯不同历史时点造成的伪差异。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 判断条件 | 先核准双方对象/时点；BOMIS多/漏人且影响识别、同人法定身份六项不一致、比例或控制方式/职务不一致且影响受益权关系类型、形成或终止时间的‘年月’不同及其他实质差异，归重大。非汉字名拼写缩写、比例/控制描述差别不影响关系类型、机构合理采用更严阈值使<25%额外入选或其他不影响识别的，归非重大；实际重大事实不可用二手‘跨月≤30日’覆盖法定年月标准。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 结果 | 在人选、身份关键要素、权利关系类型或形成终止年月达到法定重大标准时列重大；其余符合非重大条款者留痕处理。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 例外 | 同名不同证件未证实为同一人时先核身份；人数没变化不排除关系/日期重大变化；日期仅‘日’不同且同年月不能因此直接归重大。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 缺证处理 | 两套记录完整字段、身份证明及匹配依据、有效权益链与关系类型、带年月形成终止证据、机构更严阈值适用记录。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 时间要求 | 年月比较针对实际权利形成/终止；差异发现日起另算反馈期限，不混为备案变更起点。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |

### RULE.A01.KF.FEEDBACK

建模分类：NO_MODEL_CHANGE；状态：NO_MODEL_CHANGE；问题：Q.A01.S74, Q.A01.S75, Q.A01.S76, Q.A01.S77, Q.A01.S78, Q.A01.P18；缺口：

处理理由：沟通、更正、报告与30工作日是金融机构反馈操作与期限，不新增受益所有权事实或领域判断。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构查出备案错误、不一致、不完整或客户依法须备案但尚未备案 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 前提 | 适用金融机构已在合理核实中发现自身识别和系统备案差异，或确认依法须备案客户系统尚无记录。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 判断条件 | 发现差异先与客户必要核实；己方识别不准及时纠正己方；合理认为备案不准且重大，发现日起30个工作日内报告并留理由、确认过程、佐证；非重大无需报告但发现日起30工作日内记录核实、不报告理由和措施并提示客户。依法须备案但未备案先沟通提示，提示后仍未备案再提交差异报告；重大差异风险可控时可以先建/维持关系。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 结果 | 机构己方错误自行更正；重大备案差异自发现日起30工作日内报告，非重大同期留痕并提示；依法未备案先提示后仍不备案再报。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 例外 | 差异未归因不能直接给客户填备案更正；一旦超期才向客户提示不等于合规；备案主体变更30日与机构差异30工作日不能混。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 缺证处理 | 差异发现时间戳、与客户沟通记录、两侧证据、归因与重大性理由、报告回执/非重大不报告原因、风险可控措施。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 时间要求 | 重大/非重大从发现差异日起算30工作日；主体信息变化30自然日起算另见备案规则。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |

### RULE.A01.KF.SUSPICIOUS

建模分类：EXTERNAL_CONTEXT；状态：EXTERNAL_CONTEXT；问题：Q.A01.S79, Q.A01.S54；缺口：

处理理由：可疑交易判断、报告和保密属于反洗钱邻域；差异事实不能自动产生可疑结论，故不建立交易或可疑报告类型。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 差异分析同时发现可能涉及洗钱或恐怖融资的事实 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 前提 | 金融机构需分别判断：是否有依法报告的备案重大差异、是否有交易层面的洗钱或恐怖融资可疑事实；两个判断可同时或单独成立。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 判断条件 | 按可疑交易法定条件履行可疑交易报告；同时达到重大差异报告条件时分别提交，两报告分别记录各自事实、时限和去向；差异报告中不得提及可疑交易报告报送情况。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 结果 | 差异报告与可疑交易报告各按各自条件独立提交；差异报告不得披露可疑报告报送事实。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 例外 | 存在差异不自动等于可疑交易；已报差异不替代可疑报告。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 缺证处理 | 差异比对与证据、交易异常与嫌疑评估记录、分别的提交与保密权限。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |
| 时间要求 | 差异报告遵守自身发现日起30工作日；可疑报告时限须按其适用规定确认，不能从本材料推断。 |  | NOT_MODELED | 属于外部上下文；已覆盖知识原文，不为其创建核心对象或流程。 |

### RULE.A01.KF.CONTINUOUS

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S80, Q.A01.S82, Q.A01.P25；缺口：

处理理由：同数换人、权利类型和有效区间变化可改变自然人结论；复用前后版本关系及重新识别判断，不建监控工作流。 非充分事实：受益人总数或登记控股股东数量未变不能证明具体人、关系类型和形成日期没变化。；一次普通人事调动不必然改变受益所有人，需要核其是否能决定主体重大事务。 UNKNOWN：变化只有第三方传闻或生效日不明时，识别结果中受影响人选/日期标待核并取得原始决议及生效材料；不能直接删除旧人或断言无更新必要。 证据要求：历史识别/备案快照、当前章程及权利转让、任免决议、信托范围与指定权记录。；变化生效与发现日期、再核实说明、必要更新或不更新的业务理由。 人工边界：持续尽调岗位审查变化的实质性和必要更新，机构风控处理附加风险；仅比对人头数或自动推送不能形成结论。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 已建立金融机构客户关系及仍须备案的主体 | T.Right | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 业务关系仍存续；机构持续监测客户结构、权利、交易与风险，备案主体自身另承担受益人变化后的备案义务。 | T.Right | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 持续关注客户整体与交易；持股、收益、表决、控制、关键管理人或信托当事人/受益范围变化且可能影响受益所有权，须审核并必要更新；人数相同但人选替换、关系类型或有效时间变化也须逐人核查。备案主体受益人信息变动另从变化日起30日更新系统。 | J.ChangeImpact.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 可能改变自然人、权利关系或有效时间的变化应审核并按需要更新；备案变更另履行主体30日义务。 | J.ChangeImpact | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 名单人数没变或旧备案数据仍能查到不证明无变化；不对无影响的形式变更一刀切认定新受益人。 | J.ChangeImpact.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 旧新权益链和证据、变更协议/任命/信托指定、交易与风险监测信息、更新及核实记录。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 分开权利变化日、机构发现日和备案更新起算，保留前后有效区间。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.HISTORICAL

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：MODELED；问题：Q.A01.S63, Q.A01.S86, Q.A01.P21；缺口：

处理理由：历史时点有效的自然人权利关系属于核心可回放事实；交易时点仅作as-of输入，不建交易模型或推定历史责任。 非充分事实：仅当前工商图或当前共同受益人标签不能证明历史控制或责任。 UNKNOWN：若必要事实尚未证实：仅当前工商图或当前共同受益人标签不能证明历史控制或责任。；具体补证：交易时间、同期权利生效/终止文书与当时规则、历史客户档案、关联筛查与风险审查记录。 证据要求：交易时间、同期权利生效/终止文书与当时规则、历史客户档案、关联筛查与风险审查记录。 人工边界：风险用途、客户准入或授信决定依机构正式授权；业务范围材料未授予自动责任归属权。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 关联客户/历史交易风险分析，为业务讨论范围而非新法定责任推定 | T.Right | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 关联客户/历史交易风险分析，为业务讨论范围而非新法定责任推定 | T.Right | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 以历史交易当时已生效的自然人拥有、收益、表决及控制关系判断可能关联；保留入选/退出区间与来源可靠性，当前共同受益人仅为关联风险线索，不能推出过去由同一人负责或交易可疑。对现时较高风险自然人客户按办法视情筛查其在本机构关联客户。 | J.FormationDate.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 关联交易分析使用交易当时有证据的有效权利区间；当前共同受益人只能产生风险线索，不推出历史责任。 | J.FormationDate | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 仅当前工商图或当前共同受益人标签不能证明历史控制或责任。 | J.FormationDate.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 交易时间、同期权利生效/终止文书与当时规则、历史客户档案、关联筛查与风险审查记录。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 每一历史交易按交易时点快照；2026新机构办法不可自动追认施行前义务，但存量过渡规定需另核。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

### RULE.A01.KF.EXISTING

建模分类：NO_MODEL_CHANGE；状态：NO_MODEL_CHANGE；问题：Q.A01.P25, Q.A01.S87；缺口：

处理理由：旧客户六个月、两年和激活例外是过渡政策与办理时限，不产生长期稳定的受益所有权结构或状态机。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 2026-01-20前已建立业务关系或已开展交易、识别未达新办法标准的非自然人客户 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 前提 | 2026-01-20前已建立业务关系或已开展交易、识别未达新办法标准的非自然人客户 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 判断条件 | 确认客户关系/交易建立时间和旧识别缺口；较高风险及以上客户自2026-01-20起6个月内完成；其余所有该类存量客户自起2年完成；长期不动户或已严格限制交易的可延至申请激活或办理业务时。2017年235号和2018年164号通知同日废止。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 结果 | 存量未达新规标准的较高风险客户按6个月，其余按2年窗口补足；严格不动或限制交易可按激活事件触发。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 例外 | 只因开户早或账户不活跃不能自动不处理；‘严格限制’须查真实交易限制和激活事实。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 缺证处理 | 开户/交易日期、旧档案相对新规定的缺口、客户风险等级与评估日、限制/不动记录及激活申请。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |
| 时间要求 | 6个月、2年按正式规则起算；激活事件是例外触发而非永久豁免。 |  | NOT_MODELED | 属于无模型变化；已覆盖知识原文，不为其创建核心对象或流程。 |

### RULE.A01.KF.GOVERNANCE

建模分类：CORE_STRUCTURE + DOMAIN_DECISION；状态：PARTIAL；问题：Q.A01.S83, Q.A01.P03, Q.A01.P05, Q.A01.P12, Q.A01.P21, Q.A01.P22, Q.A01.P26, Q.A01.P28；缺口：GAP.A01.INSTITUTION_AUTHORITY, GAP.A01.PROPOSED_POLICY

处理理由：逐人结论必须绑定权利、证据、有效时间及未知或冲突；机构审批授权只是外部边界，不创建岗位审批流程。 非充分事实：供应商输出一个姓名和持股比例、部门口头声称批准，均不构成机构最终业务结论与岗位授权。；当前共同受益人标签不能直接判断历史可疑交易或对外责任。 UNKNOWN：人选证据或机构授权缺失分别标`insufficient_evidence`及`authorization_unknown`，附具体补件与受影响业务用途；交付可审核的已知部分而非虚构全量已确认名单。 证据要求：带版本时间的客户原始文书、独立核实凭证、BOMIS查询及差异归因记录。；机构正式的岗位授权、风险与客户准入/授信/差异报告制度；缺失作为待办而非凭空填写。 人工边界：金融机构依法负责识别核实及风险判断；机构正式制度确定不同用途有权岗位，输入缺制度时保持未决Issue而不是生成普遍OPERATING_POLICY。

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 机构以自然人受益所有人结果支持业务和差异报告 | T.PersonAssessment | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 前提 | 输出拟供客户准入、关联风险、差异报告等不同业务用途，当前输入仅有法规和A01讨论，没有金融机构正式授权制度。 | T.PersonAssessment | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 判断条件 | 交付需逐人注明权利标准/比例或控制方式、上层路径、法律关系形成终止区间、身份与证据来源、当前风险/冲突、BOMIS比对和未决补件；缺境外路径、代持原件或控制权限证据时仅输出可确认部分，未知维持不足证据/冲突，并具体指出待补原件及影响哪项判断。 | J.Evidence.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 结果 | 交付已证实的自然人、权利、路径、有效时间、证据及未决缺口；机构正式制度缺位时审批及对外报告权限维持待确认。 | J.Evidence | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 例外 | 有名字、有第三方计算或供应商分类并不等于身份及权利核实完成；业务讨论材料不足以规定哪些岗位能批准授信或差异报告。 | J.Evidence.criteria | MANUAL | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 缺证处理 | 经逐人逐关系绑定的原始文书、来源日期与真实性核查、机构风险记录、复核异议和差异报告记录。 | T.Evidence, T.PersonAssessment.unknown_reason | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |
| 时间要求 | 结论记录业务适用时点、证据形成及核实时间；不得以当前来源抹去历史。 | T.PersonAssessment.as_of, T.Right.effective_start | FORMALIZED | 仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。 |

## 模型目录与依据

| 标识 | 名称 | 依据 |
| --- | --- | --- |
| T.Party | 业务当事人 | TERM.A01.KF.02, RULE.A01.KF.EQUITY, RULE.A01.KF.TRUST |
| T.Right | 逐段权利关系 | TERM.A01.KF.03, TERM.A01.KF.04, RULE.A01.KF.EQUITY, RULE.A01.KF.DATES |
| T.Arrangement | 权利与控制安排 | TERM.A01.KF.04, TERM.A01.KF.05, RULE.A01.KF.NOMINEE, RULE.A01.KF.CONTROL, RULE.A01.KF.TRUST |
| T.Role | 业务角色 | TERM.A01.KF.06, TERM.A01.KF.07, TERM.A01.KF.08, RULE.A01.KF.BRANCHES |
| T.BeneficiaryScope | 信托受益范围 | TERM.A01.KF.08, RULE.A01.KF.TRUST |
| T.Evidence | 权利与身份依据 | TERM.A01.KF.10, TERM.A01.KF.13, RULE.A01.KF.IDENTITY |
| T.PersonAssessment | 逐人受益所有人判断 | TERM.A01.KF.02, TERM.A01.KF.06, RULE.A01.KF.EQUITY, RULE.A01.KF.GOVERNANCE |
| T.PopulationAssessment | 三标准穷尽与备位判断 | TERM.A01.KF.06, RULE.A01.KF.FALLBACK, RULE.A01.KF.CONTINUOUS |
| T.BranchAssessment | 分支受益人组合判断 | RULE.A01.KF.BRANCHES |
| T.IdentificationRoute | 识别方式资格 | TERM.A01.KF.09, RULE.A01.KF.PROFILE, RULE.A01.KF.EXCEPTIONS |
| R.NaturalPerson | 自然人身份门槛 | TERM.A01.KF.02, RULE.A01.KF.IDENTITY |
| R.Equity25 | 最终权益达到25% | RULE.A01.KF.EQUITY |
| R.BenefitVote25 | 收益或表决达到25% | RULE.A01.KF.RETURNS_VOTES |
| R.FallbackGate | 备位启用门槛 | RULE.A01.KF.FALLBACK |
| R.SoeFiling | 国控备案法代视同 | RULE.A01.KF.SOE |
| J.RightAttribution | 名义与真实权利归属 | RULE.A01.KF.NOMINEE |
| J.ActualControl | 自然人实际控制 | RULE.A01.KF.CONTROL |
| J.Evidence | 身份与权利证据充分性 | RULE.A01.KF.IDENTITY, RULE.A01.KF.TRUST_RELIANCE, RULE.A01.KF.GOVERNANCE |
| J.Route | 免识别与简化资格 | RULE.A01.KF.PROFILE, RULE.A01.KF.TRUST_PRODUCTS, RULE.A01.KF.ASSET_PRODUCTS, RULE.A01.KF.EXCEPTIONS, RULE.A01.KF.RISK |
| J.Trust | 信托自然人归属 | RULE.A01.KF.TRUST |
| J.BranchInclusion | 分支双部分人选核实 | RULE.A01.KF.BRANCHES |
| J.FormationDate | 权利、安排与角色有效时间 | RULE.A01.KF.DATES, RULE.A01.KF.HISTORICAL |
| J.ChangeImpact | 人选与权利变化影响 | RULE.A01.KF.CONTINUOUS |
| GAP.A01.DIFFERENCE_CROSSMONTH | 上游未决：第三方TXT048声称同年跨月、相差30自然日内可以不算重大；12号令第二十八条明确形成年月或终止年月不一致为重大。现有来源不支持该第三方豁免；不能视为规范冲突，也不能让其覆盖规范。 |  |
| GAP.A01.INSTITUTION_AUTHORITY | 上游未决：仅有业务问题讨论与法规，没有机构正式制度/专家口径：复核、准入、授信、差异报告签核、风险接受等岗位及分权无法实质回答。 |  |
| GAP.A01.EVIDENCE_CONFLICT | 上游未决：真实客户代持协议效力、总分异常登记链、跨境证据及控制安排尚无案件材料，不可能确认具体自然人、控制形成日及冲突来源。 |  |
| GAP.A01.STATE_CONTROL_SCOPE | 上游未决：国资交易监管办法第32号令对国有实际控制企业的范围服务国资产权交易监管；不能自动等同备案/金融机构规定的国有独资或控股公司。国有相对控股边界与具体公司控制证据须逐案核查。 |  |
| GAP.A01.REPORT_DETAILS | 上游未决：2025年第12号令第二十七条要求建立反馈制度，第二十七条后续所述报告要素格式和填报要求由人民银行另行规定；本次输入未确认有效配套操作版本。 |  |
| GAP.A01.CROSS_BORDER | 上游未决：现有规范仅列境外分支、外国信托及境外登记不可核的路径，并无客户跨境登记核验渠道和证据可靠性评估材料。 |  |
| GAP.A01.DATED_PUBLISHING | 上游未决：2024年第3号令明确存量备案截止2025-11-01，第二版备案指南转述存量‘及时补报’不能单凭指南视作修改正式办法；个案已逾期事实、系统办理状况尚无证据。 |  |
| GAP.A01.PROPOSED_POLICY | 上游未决：业务讨论要求保留日期精度、缺证状态、证据链与人工复核，但未提供机构或专家正式作业来源，不可把设计建议写成普遍强制细则。 |  |
| GAP.A01.SYSTEM_QUERY_STATE | 上游未决：系统接口V2.0的SRC.SRC07.U0133规定先核验备案主体才能查询且未备案主体不可查询，SRC.SRC07.U0142规定主体信息更新后待审核差异报告由接口终止。它们是该接口版本的业务状态，不是第十二号令另设的人选条件、普遍期限或法律上的报告撤销；尚无机构实时系统版本与回执。 |  |
| GAP.A01.UNREADABLE_UNITS | 上游未决：219 个来源单元在已有解析结果中不可读或为空；无法审查其业务含义。此处仅保留缺口，不重新调用 MinerU 或猜测原文。 |  |
| GAP.A01.SOURCE_PRECEDENCE | 上游未决：已有规则区分备案与金融机构义务，但尚未形成跨来源效力、地域及生效日冲突的完整判序。问题映射不等于已回答。 |  |
| GAP.A01.FX_CONVERSION | 上游未决：免备案资本门槛涉及等值外币，但当前材料未给出可据以确认的折算时点、汇率来源与计算口径。问题映射不等于已回答。 |  |
| GAP.A01.OPTION_CLASSIFICATION | 上游未决：免报或国企法代系统选项与客观资格不符时，正式差异分类及处置指引未进入本批权威材料。 |  |
| GAP.A01.CROSSMONTH_GUIDANCE | 上游未决：二手材料声称跨月三十日内非重大，但未提供能改变现行正式办法年月差异标准的权威依据。 |  |
| GAP.A01.UNREADABLE_FIGURE | 上游未决：外链图例未提供可读股权路径，匿名案例亦不能证实特定实名主体，当前无法完成归档证据核对。 |  |
| GAP.A01.DATE_AUTHORITY | 上游未决：形成日期只有范围或证据冲突时，材料未给出机构内部最终裁决和签核权限。 |  |
| GAP.A01.INSTITUTION_GOVERNANCE | 上游未决：有权岗位、特殊地区口径和业务使用授权尚无经确认的机构制度输入。 |  |
| GAP.A01.DISPUTE.ST.TXT021.U00031.01 | 上游未决：二次分类摘要列出草案/正式版存量期限、发布时间、30日/30工作日、国企查询未命中、记录保存期限、重大变化人数指标等二手材料间冲突；这些只是待核线索，不能独立确立规范结论。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT051.U00065.001 | 上游未决：文章宣称转引公示信息的产品展示具有法律效力；数据摘录或产品截图的证据效力不能仅由供应商主张确定。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT052.U00064.001 | 上游未决：供应商宣称其系统可完全代替人工识别特定情形并自动标记；与规范来源禁止自动化替代必要风险判断的要求存在潜在冲突，不得当作金融机构免责依据。 |  |
| GAP.A01.DISPUTE.STM.SRC.TXT058.U00014.S01 | 上游未决：厂商文章在标准一识别叙述中使用“最终穿透识别持股≥25%自然人”的表达。 |  |
| GAP.A01.DISPUTE.STM.SRC.TXT059.U00016.S01 | 上游未决：厂商自述其对“≥25%持股”建立多层校验机制。 |  |
| GAP.A01.DISPUTE.STM.SRC.TXT062.U00014.S01 | 上游未决：厂商文章将三项标准表达为“股权/合伙权益≥25%、收益权/表决权≥25%、实际控制”。 |  |
| GAP.A01.DISPUTE.STM.SRC.TXT062.U00022.S01 | 上游未决：厂商称其对加强识别客户把产品阈值从“≥25%”自动下调至“≥10%”，并支持风险标签配置。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT063.U00039.001 | 上游未决：供应商提议优先推荐公开披露文件中的实际控制人；披露人仅为候选，是否控制客户及披露期间须另核。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT063.U00041.001 | 上游未决：产品声称对第三标准结果中已有公开披露的实际控制人优先推荐；推荐不等于认定或优于其他可靠来源。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00016.001 | 上游未决：文章称客户异常变化触发加强识别时阈值从25%下调至10%；原第12号令第二十一条将10%作为可选的加强措施示例，并未规定每次异常必须下调。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00017.001 | 上游未决：文章声称简化或豁免条件丧失一律构成重大变化、必须按普通标准重识别；须区分条件变化、受益所有权是否受影响和第二十五条禁止继续简化的效果。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00028.001 | 上游未决：作者把受益所有人总人数净增加与新增自然人并用作变化判断；仅看净人数可能遗漏旧人退出、新人进入而总数不变的情况。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00040.001 | 上游未决：作者把名单中自然人退出且受益所有人总数净减少视为变化；净人数单独判断不足以处理多人替换与权利类型变更。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00052.001 | 上游未决：作者认为总人数不变但适用标准由持股、收益、控制或简化路径互转可能影响权利类型；文中“标准四”不是第12号令第八条列举的第四项，定义不明。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00063.001 | 上游未决：作者以名单具体人员、人数、识别理由三问总结变化影响；即使这三项没变化，比例或形成、终止年月变化仍可能影响备案信息与重大差异判断，不能用作不再核实的绝对豁免。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00073.001 | 上游未决：企查查称自动比较变更前后识别人数与关系类型以判重大变化、免人工逐案分析；该产品能力不能代替金融机构必要的风险判断及权利事实核实。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00076.001 | 上游未决：供应商称系统判定不影响受益所有权的变更仅归档、不触发业务复核；该自动豁免可能漏掉同数换人、形成时间和控制事实变化。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00080.001 | 上游未决：企查查宣称系统可代替逐案人工研判并准确分类重大变化；效果未经验证，风险决策责任仍由金融机构承担。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT065.U00015.001 | 上游未决：文章称国资委名单曾将脱敏名称为中建某成都公司列为第51号假冒央企，并称其下设各级子公司亦在公告范围；未核对原始名单、完整企业身份及公告适用范围。 |  |
| GAP.A01.DISPUTE.STM.SRC.TXT066.U00016.S01 | 上游未决：厂商文章自述其产品把受益所有权关系形成日期统一调整为“按受益所有人最新股权变化定位的形成日期”这一口径。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00006.001 | 上游未决：作者以图文速览概括备案主体、承诺免报、三类受益所有人、身份与权利信息、设立和变更时限；混入“部分省市延期”但未列明地区与批准文件。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00006.002 | 上游未决：文章提到2025年11月1日前存量主体补备及部分省市延期；延期范围、法律依据和截至时间未知，不能改写统一规范期限。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00015.001 | 上游未决：文章称新设主体设立时备案、实施前登记主体2025年11月1日前补备、信息变更或失去免报条件后30日内更新；另称存量期限“已延期”，却未提供地区、文件与有效期限，后者待核。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00019.001 | 上游未决：作者建议权利形成日期锚定当前最新权利状态及章程、转让协议的生效时间，每人分别核实，避免统一取认缴日期；“最新一次满足标准日”这一通用口径未经本材料给出权威条款，持续持有期间比例变动如何处理仍未决。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00021.001 | 上游未决：文章称金融机构可比对备案与自行识别结果，但把人员不匹配、关系类型错误、应备未备一概表述为必然重大差异且必然报告，忽略客户沟通、差异成因、条件和报告时间分支；应回核2025年第12号令。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT068.U00023.001 | 上游未决：企查查宣称总公司注销而无受益所有人可沿用时，自动将分支机构负责人归为“日常经营管理人员”；规范第九条并未直接规定该替代，且母公司注销不证明第八条前三类均不存在，不得作为已确立识别规则。 |  |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT068.U00025.001 | 上游未决：文章称工商资料缺少总公司关系时识别方法见下图，并输出依据；文字未写明具体识别路径，下图仅图片外链，故真实分支逻辑缺证。 |  |

## 全部业务字段

### T.Party / 业务当事人

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| id | 业务实例标识 | Text | 必须一项 | 同一现实对象或事实的稳定区分键，不代表缺证时可编造身份。 |
| name | 名称或姓名 | Text | 必须一项 | 经可靠资料核对的当事人名称；同名不证明同一人。 |
| kind | 当事人性质 | Enum | 必须一项 | 区分自然人和各类非自然人主体。 |
| legal_form | 登记组织形态 | Enum | 可有一项；缺失时保留未知 | 仅保留识别路径所需的登记形态，不复制工商登记域。 |
| parent | 所属主体 | Ref → T.Party | 可有一项；缺失时保留未知 | 分支所属主体须按判断时点和有效证据核实。 |
| state_controlled | 国有独资或控股已证实 | Boolean | 可有一项；缺失时保留未知 | 必须由产权、控制权和适用口径支持；国有参股不等于控股。 |
| registered_on | 设立登记日期 | Date | 可有一项；缺失时保留未知 | 仅用于判断适用时点；不替代权利形成日期。 |

### T.Right / 逐段权利关系

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| id | 业务实例标识 | Text | 必须一项 | 同一现实对象或事实的稳定区分键，不代表缺证时可编造身份。 |
| holder | 本段实际权利人 | Ref → T.Party | 可有一项；缺失时保留未知 | 可为自然人或中间组织；归属证据不足时保持未知，不能默认登记人。 |
| subject | 本段权利所及主体 | Ref → T.Party | 必须一项 | 该段权利直接对应的组织、信托或产品。 |
| kind | 权利类别 | Enum | 必须一项 | 股权、收益与表决分别判断。 |
| percent | 本段有效比例 | Decimal | 可有一项；缺失时保留未知 | 逐段由原始材料核实；最终比例由同日完整路径连乘、去重和汇总，未知段不得按零。 |
| nominal_holder | 名义登记人 | Ref → T.Party | 可有一项；缺失时保留未知 | 与最终权利人分开核证。 |
| arrangement | 影响归属的安排 | Ref → T.Arrangement | 可有一项；缺失时保留未知 | 代持、委托等可改变表面归属。 |
| effective_start | 法律关系生效日 | Date | 可有一项；缺失时保留未知 | 只有精确日期有证据时填写；不能以登记、核实或报送日代填。 |
| formation_bounds | 形成时间已知区间 | IntervalSet | 可有一项；缺失时保留未知 | 精确日未知时保留已证实上下界及精度。 |
| effective_end | 法律关系终止日 | Date | 可有一项；缺失时保留未知 | 若已知终止且有证据则填写。 |
| effective_end_bounds | 终止时间已知区间 | IntervalSet | 可有一项；缺失时保留未知 | 仅知终止月份或区间时保留上下界、精度与证据，不补造某日。 |
| end_status | 终止情况 | Enum | 可有一项；缺失时保留未知 | 未终止已证实与终止未知不能混同。 |
| evidence | 权利证据 | Ref → T.Evidence | 至少 0 项，不限最多数量 | 逐条绑定各边比例、协议及生效材料。 |

### T.Arrangement / 权利与控制安排

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| id | 业务实例标识 | Text | 必须一项 | 同一现实对象或事实的稳定区分键，不代表缺证时可编造身份。 |
| actor | 权能行使人 | Ref → T.Party | 可有一项；缺失时保留未知 | 联合控制时各自然人的具体作用须另核。 |
| subject | 受影响主体 | Ref → T.Party | 必须一项 | 安排的目标组织或信托。 |
| kind | 安排类别 | Enum | 必须一项 | 不把不同法律效力的安排合并。 |
| power | 实际权限 | Enum | 至少 0 项，不限最多数量 | 人事、经营、财务、资产及信托处分或指定权分别核实。 |
| effective_start | 安排生效日 | Date | 可有一项；缺失时保留未知 | 缺生效证据时保持未知。 |
| formation_bounds | 安排形成区间 | IntervalSet | 可有一项；缺失时保留未知 | 仅能确定期间时保留范围。 |
| effective_end | 安排终止日 | Date | 可有一项；缺失时保留未知 | 不可把过期委托计入判断日。 |
| effective_end_bounds | 安排终止已知区间 | IntervalSet | 可有一项；缺失时保留未知 | 终止日不精确时保留可信范围和精度。 |
| end_status | 终止情况 | Enum | 可有一项；缺失时保留未知 | OPEN须有持续有效依据；UNKNOWN不是OPEN。 |
| evidence | 安排证据 | Ref → T.Evidence | 至少 0 项，不限最多数量 | 协议原件与实际行使记录需要相互核对。 |

### T.Role / 业务角色

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| id | 业务实例标识 | Text | 必须一项 | 同一现实对象或事实的稳定区分键，不代表缺证时可编造身份。 |
| bearer | 角色承担者 | Ref → T.Party | 必须一项 | 角色承担者身份需独立核实。 |
| subject | 角色所在主体 | Ref → T.Party | 必须一项 | 所任职组织、分支、信托或产品。 |
| kind | 角色类别 | Enum | 必须一项 | 特定路径的人选资格依角色与有效期间判断。 |
| effective_start | 任职或角色生效日 | Date | 可有一项；缺失时保留未知 | 按任命或信托文件的法律效力核对。 |
| formation_bounds | 角色形成区间 | IntervalSet | 可有一项；缺失时保留未知 | 精确日期缺证时保留范围。 |
| effective_end | 角色终止日 | Date | 可有一项；缺失时保留未知 | 角色终止不自动推出其他权利终止。 |
| effective_end_bounds | 角色终止已知区间 | IntervalSet | 可有一项；缺失时保留未知 | 终止日只知月份或范围时不补造精确日。 |
| end_status | 角色终止情况 | Enum | 可有一项；缺失时保留未知 | 已证实仍在任、已终止与未知分开。 |
| evidence | 角色证据 | Ref → T.Evidence | 至少 0 项，不限最多数量 | 官方登记、任命、信托文件及实际职责记录。 |

### T.BeneficiaryScope / 信托受益范围

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| id | 业务实例标识 | Text | 必须一项 | 同一现实对象或事实的稳定区分键，不代表缺证时可编造身份。 |
| trust | 所属信托 | Ref → T.Party | 必须一项 | 对应的具体信托。 |
| description | 潜在受益范围 | Text | 必须一项 | 按信托文件原义保留类别或指定范围。 |
| designated_person | 已指定自然人 | Ref → T.Party | 可有一项；缺失时保留未知 | 只有指定已生效且身份获证才填写。 |
| designation_status | 指定情况 | Enum | 必须一项 | 潜在、已指定与未知分开。 |
| effective_on | 指定生效日 | Date | 可有一项；缺失时保留未知 | 不以信托设立日替代后续指定生效日。 |
| evidence | 信托证据 | Ref → T.Evidence | 至少 0 项，不限最多数量 | 信托文件、指定文件和有效时间资料。 |

### T.Evidence / 权利与身份依据

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| id | 业务实例标识 | Text | 必须一项 | 同一现实对象或事实的稳定区分键，不代表缺证时可编造身份。 |
| source | 来源 | Text | 必须一项 | 可定位的文件或机构来源。 |
| kind | 来源类别 | Enum | 必须一项 | 区分原件、官方、客户、机构与外部观察。 |
| issued_on | 资料形成日 | Date | 可有一项；缺失时保留未知 | 资料形成日不等于权利生效日。 |
| verified_on | 核实日 | Date | 可有一项；缺失时保留未知 | 核实行为发生的时间。 |
| reliability | 可信及冲突状态 | Enum | 可有一项；缺失时保留未知 | 由有权人员依来源与交叉印证判断。 |
| claim | 所支持的事实 | Text | 可有一项；缺失时保留未知 | 写明材料实际能证明的身份、比例、权能或时间。 |

### T.PersonAssessment / 逐人受益所有人判断

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| id | 业务实例标识 | Text | 必须一项 | 同一现实对象或事实的稳定区分键，不代表缺证时可编造身份。 |
| subject | 被识别主体 | Ref → T.Party | 必须一项 | 本次判断的具体目标。 |
| person | 候选自然人 | Ref → T.Party | 必须一项 | 须独立核实其自然人身份。 |
| purpose | 结论责任语境 | Enum | 必须一项 | 备案与机构独立识别不能互换。 |
| as_of | 判断时点 | Date | 必须一项 | 历史业务只引用该时点有效关系。 |
| criterion | 识别依据 | Enum | 必须一项 | 每项标准单独记录，避免同人重复计数。 |
| outcome | 判断结果 | Enum | 可有一项；缺失时保留未知 | UNKNOWN不等于不成立。 |
| is_natural | 自然人身份已证实 | Boolean | 可有一项；缺失时保留未知 | 非自然人只可作路径节点。 |
| equity_percent | 同人最终权益比例 | Decimal | 可有一项；缺失时保留未知 | 完整有效路径连乘、去重并汇总；未知路径不得按零。 |
| equity_met | 权益标准成立 | Boolean | 可有一项；缺失时保留未知 | 含本数25%阈值判断。 |
| benefit_percent | 最终收益比例 | Decimal | 可有一项；缺失时保留未知 | 与名义持股分别核实。 |
| vote_percent | 最终表决比例 | Decimal | 可有一项；缺失时保留未知 | 委托范围、期限和重叠部分均须核实。 |
| benefit_vote_met | 收益或表决标准成立 | Boolean | 可有一项；缺失时保留未知 | 仅在该人未符合权益标准一时使用。 |
| actual_control | 实际控制成立 | Boolean | 可有一项；缺失时保留未知 | 人事、重大决策、财务或重要资产支配须有权限与行使证据。 |
| is_legal_rep | 有效法定代表人角色 | Boolean | 可有一项；缺失时保留未知 | 依有效任职材料和判断时点确认。 |
| soe_filing_match | 国控备案法代视同成立 | Boolean | 可有一项；缺失时保留未知 | 仅备案路径为应当视同，机构简化另行判断。 |
| first_qualified_on | 首次符合标准日 | Date | 可有一项；缺失时保留未知 | 持续未退出时不被后来的增持日期覆盖。 |
| current_right_formed_on | 当前权利状态形成日 | Date | 可有一项；缺失时保留未知 | 与首次达标日和登记披露日区分。 |
| rights | 依据的权利关系 | Ref → T.Right | 至少 0 项，不限最多数量 | 可回指逐条权益、收益与表决事实。 |
| arrangements | 依据的控制安排 | Ref → T.Arrangement | 至少 0 项，不限最多数量 | 可回指代持、控制、信托权能等安排。 |
| evidence | 判断证据 | Ref → T.Evidence | 至少 0 项，不限最多数量 | 充分证据逐项绑定；无证部分保持未知。 |
| non_sufficient_facts | 非充分线索 | Text | 至少 0 项，不限最多数量 | 记录登记名义、亲属、头衔、单次签字或第三方标签不能单独证明什么。 |
| unknown_reason | 未知原因及需补材料 | Text | 可有一项；缺失时保留未知 | 明确受影响标准、关系及补证要求。 |
| human_boundary | 人工审查边界 | Text | 可有一项；缺失时保留未知 | 证据冲突、权利效力和风险判断须由有权人员承担。 |

### T.PopulationAssessment / 三标准穷尽与备位判断

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| id | 业务实例标识 | Text | 必须一项 | 同一现实对象或事实的稳定区分键，不代表缺证时可编造身份。 |
| subject | 目标主体 | Ref → T.Party | 必须一项 | 同一主体的全部候选路径。 |
| as_of | 整体判断时点 | Date | 必须一项 | 所有路径须在同一时点核对。 |
| equity_absent_proven | 权益人不存在已证实 | Boolean | 可有一项；缺失时保留未知 | 未知上层路径时保持UNKNOWN。 |
| benefit_vote_absent_proven | 收益表决人不存在已证实 | Boolean | 可有一项；缺失时保留未知 | 未取得协议时保持UNKNOWN。 |
| control_absent_proven | 实际控制人不存在已证实 | Boolean | 可有一项；缺失时保留未知 | 未找到材料不等于已证实不存在。 |
| fallback_eligible | 可启用备位 | Boolean | 可有一项；缺失时保留未知 | 三项全部为真才成立。 |
| rights_changed | 人选或关系实质变化 | Boolean | 可有一项；缺失时保留未知 | 逐人比较权利与时间，不按总人数净变化判断。 |
| evidence | 穷尽检查证据 | Ref → T.Evidence | 至少 0 项，不限最多数量 | 上层结构、非股权安排及管理职责材料。 |
| unknown_reason | 未完成路径 | Text | 可有一项；缺失时保留未知 | 指出哪一项仍是UNKNOWN及待补资料。 |

### T.BranchAssessment / 分支受益人组合判断

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| id | 业务实例标识 | Text | 必须一项 | 同一现实对象或事实的稳定区分键，不代表缺证时可编造身份。 |
| branch | 目标分支 | Ref → T.Party | 必须一项 | 区分国内分支与外国公司中国分支。 |
| parent | 同一时点所属主体 | Ref → T.Party | 可有一项；缺失时保留未知 | 注销、恢复或改隶期间须另有有效证据。 |
| as_of | 判断时点 | Date | 必须一项 | 总部人选和分支任职均以同一时点核对。 |
| headquarters_people | 所属主体合格自然人 | Ref → T.PersonAssessment | 至少 0 项，不限最多数量 | 按所属主体的一般标准或已核实尽调结果取得。 |
| senior_roles | 有效分支高级管理角色 | Ref → T.Role | 至少 0 项，不限最多数量 | 任命、职责与有效期逐人核实。 |
| additional_senior_people | 额外纳入的分支高管自然人 | Ref → T.Party | 至少 0 项，不限最多数量 | 外国分支至少一名；不得代替总部合格自然人。 |
| outcome | 双部分人选核实结果 | Enum | 可有一项；缺失时保留未知 | 缺总分关系、总部人选或分支高管证据时为UNKNOWN。 |
| evidence | 总分与人选证据 | Ref → T.Evidence | 至少 0 项，不限最多数量 | 总分关系、所属主体尽调及分支任命履职材料。 |
| non_sufficient_facts | 不充分事实 | Text | 至少 0 项，不限最多数量 | 分支营业执照、本地经理头衔或旧总部姓名不能单独证明当前双部分人选。 |
| unknown_reason | 未知原因 | Text | 可有一项；缺失时保留未知 | 明确尚未核实的所属链、总部穿透或分支任职。 |
| human_boundary | 人工核实边界 | Text | 可有一项；缺失时保留未知 | 异常登记、境外资料真实性和旧资料复用由有权人员裁定。 |

### T.IdentificationRoute / 识别方式资格

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| id | 业务实例标识 | Text | 必须一项 | 同一现实对象或事实的稳定区分键，不代表缺证时可编造身份。 |
| subject | 适用主体 | Ref → T.Party | 必须一项 | 识别方式涉及的客户、信托或产品。 |
| as_of | 适用时点 | Date | 必须一项 | 依当时有效类别与风险判断。 |
| purpose | 责任语境 | Enum | 必须一项 | 备案与机构规则的责任主体不同。 |
| subject_category | 必要主体类别 | Text | 可有一项；缺失时保留未知 | 仅引用可否适用识别例外的类别，不建立完整客户分类。 |
| service_facts | 必要服务关系 | Text | 可有一项；缺失时保留未知 | 只记管理、受托或托管等适用前提。 |
| risk_tier | 外部风险结论 | Enum | 可有一项；缺失时保留未知 | 由机构风险责任方提供；未知不得当低风险。 |
| route | 可采用识别方式 | Enum | 可有一项；缺失时保留未知 | 可以简化不等于已批准简化。 |
| evidence | 资格证据 | Ref → T.Evidence | 至少 0 项，不限最多数量 | 官方类别、服务合同和机构风险评估记录。 |
| non_sufficient_facts | 不充分条件 | Text | 至少 0 项，不限最多数量 | 如公募或持牌名称单独不足以简化。 |
| unknown_reason | 资格未知原因 | Text | 可有一项；缺失时保留未知 | 缺任一必要类别、合同或风险事实即不放行特殊方式。 |
| human_boundary | 人工选择及责任 | Text | 可有一项；缺失时保留未知 | 可选路径须由适用机构有权人员决定。 |


## 字段绑定与依赖

### R.NaturalPerson / 自然人身份门槛

前序规则：

输出字段：T.PersonAssessment.is_natural

表达式：(person_kind = "NATURAL_PERSON")

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| person_kind | 候选人的身份性质 | Enum | T.Party.kind |

### R.Equity25 / 最终权益达到25%

前序规则：

输出字段：T.PersonAssessment.equity_met

表达式：(equity_percent ≥ 25)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| equity_percent | 已核实最终权益比例 | Decimal | T.PersonAssessment.equity_percent |

### R.BenefitVote25 / 收益或表决达到25%

前序规则：R.Equity25

输出字段：T.PersonAssessment.benefit_vote_met

表达式：(非(equity_met) 且 ((benefit_percent ≥ 25) 或 (vote_percent ≥ 25)))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| equity_met | 权益标准一是否成立 | Boolean | T.PersonAssessment.equity_met |
| benefit_percent | 最终收益比例 | Decimal | T.PersonAssessment.benefit_percent |
| vote_percent | 最终表决比例 | Decimal | T.PersonAssessment.vote_percent |

### R.FallbackGate / 备位启用门槛

前序规则：

输出字段：T.PopulationAssessment.fallback_eligible

表达式：(no_equity 且 no_benefit_vote 且 no_control)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| no_equity | 权益人不存在已证实 | Boolean | T.PopulationAssessment.equity_absent_proven |
| no_benefit_vote | 收益表决人不存在已证实 | Boolean | T.PopulationAssessment.benefit_vote_absent_proven |
| no_control | 控制人不存在已证实 | Boolean | T.PopulationAssessment.control_absent_proven |

### R.SoeFiling / 国控备案法代视同

前序规则：R.NaturalPerson

输出字段：T.PersonAssessment.soe_filing_match

表达式：(natural 且 state_controlled 且 legal_rep)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| natural | 自然人身份已证实 | Boolean | T.PersonAssessment.is_natural |
| state_controlled | 国控资格已证实 | Boolean | T.Party.state_controlled |
| legal_rep | 法定代表人角色有效 | Boolean | T.PersonAssessment.is_legal_rep |

## 案例对应

| 案例 | 标题 | 模型 | 解释状态 | 执行状态 | 验证证据 |
| --- | --- | --- | --- | --- | --- |
| CASE.A01.KF.SCOPE.B | 备案主体、免报资格与责任 |  | CONTEXT_ONLY | NOT_EXECUTED |  |
| CASE.A01.KF.FILING.B | 备案初次与变化后的期限 |  | CONTEXT_ONLY | NOT_EXECUTED |  |
| CASE.A01.KF.PROFILE.B | 备案与机构识别两个判断和适用时点 | T.PersonAssessment, T.IdentificationRoute, J.Route | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.EQUITY.B | 直接及多路径间接最终权益 | T.Party, T.Right, T.PersonAssessment, R.Equity25 | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.NOMINEE.B | 名义持股与最终权益分离 | T.Right, T.Arrangement, T.Evidence, J.RightAttribution | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.RETURNS_VOTES.B | 最终收益权和表决权标准 | T.Right, T.PersonAssessment, R.BenefitVote25 | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.CONTROL.B | 实际控制的人事、决策、财务和资产支配 | T.Arrangement, T.PersonAssessment, J.ActualControl | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.FALLBACK.B | 无人满足标准的管理人备位 | T.Role, T.PopulationAssessment, R.FallbackGate | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.SOE.B | 国有控股认定与国有参股边界 | T.Party, T.Role, T.PersonAssessment, R.SoeFiling, J.Route | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.BRANCHES.B | 境内与外国分支不同受益人规则 | T.Party, T.Role, T.PersonAssessment, T.BranchAssessment, J.BranchInclusion | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.TRUST.B | 信托自然人、非自然人当事人及潜在受益人 | T.Role, T.BeneficiaryScope, T.Arrangement, T.PersonAssessment, J.Trust | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.TRUST_PRODUCTS.B | 信托服务类别与低风险简化 | T.IdentificationRoute, J.Route | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.EXCEPTIONS.B | 第十条免识别、第十一条简化与风险闸门 | T.IdentificationRoute, J.Route | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.EXCEPTIONS.QFI.B | 第十条免识别、第十一条简化与风险闸门 | T.IdentificationRoute, J.Route | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.EXCEPTIONS.REP.B | 第十条免识别、第十一条简化与风险闸门 | T.IdentificationRoute, J.Route | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.IDENTITY.B | 可信来源核实身份、权利和必要字段 | T.Party, T.Evidence, T.PersonAssessment, R.NaturalPerson, J.Evidence | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.RISK.B | 第二十条风险触发与相称加强措施 | T.IdentificationRoute, J.Route | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.RISK_ACCEPT.B | 加强后的管理层批准与拒办边界 |  | CONTEXT_ONLY | NOT_EXECUTED |  |
| CASE.A01.KF.DATES.B | 权利关系形成日及历史版本 | T.Right, T.Arrangement, T.Role, T.PersonAssessment, J.FormationDate | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.BOMIS.B | BOMIS适用客户核对及证据独立性 |  | CONTEXT_ONLY | NOT_EXECUTED |  |
| CASE.A01.KF.DIFFERENCE.B | 重大与非重大差异的全维分类 |  | CONTEXT_ONLY | NOT_EXECUTED |  |
| CASE.A01.KF.FEEDBACK.B | 差异核实、30工作日与未备案 |  | CONTEXT_ONLY | NOT_EXECUTED |  |
| CASE.A01.KF.SUSPICIOUS.B | 差异报告和可疑交易报告并行隔离 |  | CONTEXT_ONLY | NOT_EXECUTED |  |
| CASE.A01.KF.CONTINUOUS.B | 存续关注、同数换人和权利变化 | T.Right, T.PersonAssessment, T.PopulationAssessment, J.ChangeImpact | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.HISTORICAL.B | 历史交易关系还原与当前人选限制 | T.Right, T.PersonAssessment, J.FormationDate | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.EXISTING.B | 机构旧客户过渡时限 |  | CONTEXT_ONLY | NOT_EXECUTED |  |
| CASE.A01.KF.GOVERNANCE.B | 结论交付、缺证停止和机构岗位授权 | T.PersonAssessment, T.Evidence, J.Evidence | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.01 | 直接及多路径间接最终权益 | T.Party, T.Right, T.PersonAssessment, R.Equity25 | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.02 | 最终收益权和表决权标准 | T.Right, T.PersonAssessment, R.BenefitVote25 | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.03 | 名义持股与最终权益分离 | T.Right, T.Arrangement, T.Evidence, J.RightAttribution | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.04 | 实际控制的人事、决策、财务和资产支配 | T.Arrangement, T.PersonAssessment, J.ActualControl | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.05 | 实际控制的人事、决策、财务和资产支配 | T.Arrangement, T.PersonAssessment, J.ActualControl | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.06 | 国有控股认定与国有参股边界 | T.Party, T.Role, T.PersonAssessment, R.SoeFiling, J.Route | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.SRC06.07 | 最终收益权和表决权标准 | T.Right, T.PersonAssessment, R.BenefitVote25 | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.ASSET_PRODUCTS.B | 资产管理信托等资管产品识别及托管简化 | T.IdentificationRoute, J.Route | EXPLAINED | NOT_EXECUTED |  |
| CASE.A01.KF.TRUST_RELIANCE.B | 信托合作中的受托资料采信和瑕疵处置 | T.Evidence, J.Evidence | EXPLAINED | NOT_EXECUTED |  |

## 上游未决事项

| 知识事项 | 模型事项 | 处理 | 说明 |
| --- | --- | --- | --- |
| ISSUE.A01.KF.DIFFERENCE_CROSSMONTH | GAP.A01.DIFFERENCE_CROSSMONTH | MODEL_LIMITATION | 上游仍为OPEN；相关问题及核心判断保留缺口。 |
| ISSUE.A01.KF.INSTITUTION_AUTHORITY | GAP.A01.INSTITUTION_AUTHORITY | MODEL_LIMITATION | 上游仍为OPEN；相关问题及核心判断保留缺口。 |
| ISSUE.A01.KF.EVIDENCE_CONFLICT | GAP.A01.EVIDENCE_CONFLICT | MODEL_LIMITATION | 上游仍为OPEN；相关问题及核心判断保留缺口。 |
| ISSUE.A01.KF.STATE_CONTROL_SCOPE | GAP.A01.STATE_CONTROL_SCOPE | MODEL_LIMITATION | 上游仍为OPEN；相关问题及核心判断保留缺口。 |
| ISSUE.A01.KF.REPORT_DETAILS | GAP.A01.REPORT_DETAILS | MODEL_LIMITATION | 上游仍为OPEN；相关问题及核心判断保留缺口。 |
| ISSUE.A01.KF.CROSS_BORDER | GAP.A01.CROSS_BORDER | MODEL_LIMITATION | 上游仍为OPEN；相关问题及核心判断保留缺口。 |
| ISSUE.A01.KF.DATED_PUBLISHING | GAP.A01.DATED_PUBLISHING | MODEL_LIMITATION | 上游仍为OPEN；相关问题及核心判断保留缺口。 |
| ISSUE.A01.KF.PROPOSED_POLICY | GAP.A01.PROPOSED_POLICY | MODEL_LIMITATION | 上游仍为OPEN；相关问题及核心判断保留缺口。 |
| ISSUE.A01.KF.SYSTEM_QUERY_STATE | GAP.A01.SYSTEM_QUERY_STATE | MODEL_LIMITATION | 上游仍为OPEN；相关问题及核心判断保留缺口。 |
| ISSUE.A01.KF.UNREADABLE_UNITS | GAP.A01.UNREADABLE_UNITS | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.SOURCE_PRECEDENCE | GAP.A01.SOURCE_PRECEDENCE | MODEL_LIMITATION | 上游仍为OPEN；相关问题及核心判断保留缺口。 |
| ISSUE.A01.KF.FX_CONVERSION | GAP.A01.FX_CONVERSION | MODEL_LIMITATION | 上游仍为OPEN；相关问题及核心判断保留缺口。 |
| ISSUE.A01.KF.OPTION_CLASSIFICATION | GAP.A01.OPTION_CLASSIFICATION | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.CROSSMONTH_GUIDANCE | GAP.A01.CROSSMONTH_GUIDANCE | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.UNREADABLE_FIGURE | GAP.A01.UNREADABLE_FIGURE | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DATE_AUTHORITY | GAP.A01.DATE_AUTHORITY | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.INSTITUTION_GOVERNANCE | GAP.A01.INSTITUTION_GOVERNANCE | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.TXT021.U00031.01 | GAP.A01.DISPUTE.ST.TXT021.U00031.01 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT051.U00065.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT051.U00065.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT052.U00064.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT052.U00064.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT058.U00014.S01 | GAP.A01.DISPUTE.STM.SRC.TXT058.U00014.S01 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT059.U00016.S01 | GAP.A01.DISPUTE.STM.SRC.TXT059.U00016.S01 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT062.U00014.S01 | GAP.A01.DISPUTE.STM.SRC.TXT062.U00014.S01 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT062.U00022.S01 | GAP.A01.DISPUTE.STM.SRC.TXT062.U00022.S01 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT063.U00039.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT063.U00039.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT063.U00041.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT063.U00041.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00016.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00016.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00017.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00017.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00028.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00028.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00040.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00040.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00052.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00052.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00063.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00063.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00073.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00073.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00076.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00076.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00080.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00080.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT065.U00015.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT065.U00015.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.STM.SRC.TXT066.U00016.S01 | GAP.A01.DISPUTE.STM.SRC.TXT066.U00016.S01 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00006.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00006.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00006.002 | GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00006.002 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00015.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00015.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00019.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00019.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00021.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00021.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT068.U00023.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT068.U00023.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |
| ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT068.U00025.001 | GAP.A01.DISPUTE.ST.CONTEXT.TXT068.U00025.001 | DEFERRED | 上游仍为OPEN；本次无直接问题影响，保留待核而不升格为规范。 |

## 模型问题

| 标识 | 状态 | 问题 | 影响 | 责任 | 解决前处理 |
| --- | --- | --- | --- | --- | --- |
| GAP.A01.DIFFERENCE_CROSSMONTH | OPEN | 上游未决：第三方TXT048声称同年跨月、相差30自然日内可以不算重大；12号令第二十八条明确形成年月或终止年月不一致为重大。现有来源不支持该第三方豁免；不能视为规范冲突，也不能让其覆盖规范。 | ISSUE.A01.KF.DIFFERENCE_CROSSMONTH, Q.A01.S67, Q.A01.S68, Q.A01.S69, Q.A01.S70, Q.A01.S71, Q.A01.S72, Q.A01.S82 | 制度专家与法规维护人 | 按现行正式办法将跨月列重大；不使用30自然日产品豁免。 |
| GAP.A01.INSTITUTION_AUTHORITY | OPEN | 上游未决：仅有业务问题讨论与法规，没有机构正式制度/专家口径：复核、准入、授信、差异报告签核、风险接受等岗位及分权无法实质回答。 | ISSUE.A01.KF.INSTITUTION_AUTHORITY, RULE.A01.KF.GOVERNANCE, Q.A01.P03, Q.A01.P05, Q.A01.P07, Q.A01.P12, Q.A01.P18, Q.A01.P21, Q.A01.P22, Q.A01.P26, Q.A01.P28, Q.A01.S54, Q.A01.S74, Q.A01.S75, Q.A01.S76, Q.A01.S77, Q.A01.S78, Q.A01.S83 | 金融机构制度负责人 | 只表达法定机构责任，权限/审批人为待定，不造OPERATING_POLICY。 |
| GAP.A01.EVIDENCE_CONFLICT | OPEN | 上游未决：真实客户代持协议效力、总分异常登记链、跨境证据及控制安排尚无案件材料，不可能确认具体自然人、控制形成日及冲突来源。 | ISSUE.A01.KF.EVIDENCE_CONFLICT, RULE.A01.KF.BRANCHES, RULE.A01.KF.CONTROL, RULE.A01.KF.DATES, RULE.A01.KF.NOMINEE, Q.A01.P05, Q.A01.P13, Q.A01.S16, Q.A01.S21, Q.A01.S22, Q.A01.S23, Q.A01.S24, Q.A01.S25, Q.A01.S26, Q.A01.S33, Q.A01.S34, Q.A01.S35, Q.A01.S36, Q.A01.S60, Q.A01.S61, Q.A01.S62, Q.A01.S63 | 经办机构与客户 | 仅输出已证实部分，争议人选和时间标不足证据/冲突。 |
| GAP.A01.STATE_CONTROL_SCOPE | OPEN | 上游未决：国资交易监管办法第32号令对国有实际控制企业的范围服务国资产权交易监管；不能自动等同备案/金融机构规定的国有独资或控股公司。国有相对控股边界与具体公司控制证据须逐案核查。 | ISSUE.A01.KF.STATE_CONTROL_SCOPE, RULE.A01.KF.SOE, Q.A01.S30, Q.A01.S31, Q.A01.S32 | 国资制度专家与客户 | 不得将‘国有实际控制’企业直接按国有独资/控股法代视同。 |
| GAP.A01.REPORT_DETAILS | OPEN | 上游未决：2025年第12号令第二十七条要求建立反馈制度，第二十七条后续所述报告要素格式和填报要求由人民银行另行规定；本次输入未确认有效配套操作版本。 | ISSUE.A01.KF.REPORT_DETAILS, Q.A01.P18, Q.A01.S67, Q.A01.S68, Q.A01.S69, Q.A01.S70, Q.A01.S71, Q.A01.S72, Q.A01.S74, Q.A01.S75, Q.A01.S76, Q.A01.S77, Q.A01.S78, Q.A01.S82 | 金融机构差异反馈负责人 | 可确定分类与法定期限，具体接口报文、审批和填写模板不得猜测。 |
| GAP.A01.CROSS_BORDER | OPEN | 上游未决：现有规范仅列境外分支、外国信托及境外登记不可核的路径，并无客户跨境登记核验渠道和证据可靠性评估材料。 | ISSUE.A01.KF.CROSS_BORDER, RULE.A01.KF.BRANCHES, RULE.A01.KF.RISK, RULE.A01.KF.TRUST, Q.A01.P07, Q.A01.S33, Q.A01.S34, Q.A01.S35, Q.A01.S36, Q.A01.S37, Q.A01.S38, Q.A01.S39, Q.A01.S40, Q.A01.S50, Q.A01.S52, Q.A01.S53 | 经办金融机构风险合规部门 | 无境外权利证据时不假定自然人和权利比例；需要加强风险措施。 |
| GAP.A01.DATED_PUBLISHING | OPEN | 上游未决：2024年第3号令明确存量备案截止2025-11-01，第二版备案指南转述存量‘及时补报’不能单凭指南视作修改正式办法；个案已逾期事实、系统办理状况尚无证据。 | ISSUE.A01.KF.DATED_PUBLISHING, RULE.A01.KF.DATES, Q.A01.P13, Q.A01.P25, Q.A01.S07, Q.A01.S08, Q.A01.S60, Q.A01.S61, Q.A01.S62, Q.A01.S63 | 备案主体及法规维护人 | 保留第3号令明确期限及个案是否按时UNKNOWN，不凭二手材料删期限。 |
| GAP.A01.PROPOSED_POLICY | OPEN | 上游未决：业务讨论要求保留日期精度、缺证状态、证据链与人工复核，但未提供机构或专家正式作业来源，不可把设计建议写成普遍强制细则。 | ISSUE.A01.KF.PROPOSED_POLICY, RULE.A01.KF.GOVERNANCE, RULE.A01.KF.IDENTITY, Q.A01.P03, Q.A01.P05, Q.A01.P12, Q.A01.P21, Q.A01.P22, Q.A01.P26, Q.A01.P28, Q.A01.S09, Q.A01.S10, Q.A01.S13, Q.A01.S27, Q.A01.S30, Q.A01.S31, Q.A01.S32, Q.A01.S56, Q.A01.S57, Q.A01.S58, Q.A01.S83 | 业务负责人和机构授权制度负责人 | 仅保留法规义务与业务范围提示，设计建议不升格为作业政策。 |
| GAP.A01.SYSTEM_QUERY_STATE | OPEN | 上游未决：系统接口V2.0的SRC.SRC07.U0133规定先核验备案主体才能查询且未备案主体不可查询，SRC.SRC07.U0142规定主体信息更新后待审核差异报告由接口终止。它们是该接口版本的业务状态，不是第十二号令另设的人选条件、普遍期限或法律上的报告撤销；尚无机构实时系统版本与回执。 | ISSUE.A01.KF.SYSTEM_QUERY_STATE, Q.A01.P18, Q.A01.S59, Q.A01.S65, Q.A01.S74, Q.A01.S75, Q.A01.S76, Q.A01.S77, Q.A01.S78 | BOMIS接口实施负责人及金融机构差异反馈负责人 | 依法先独立核实客户、按差异法定分类与期限处理；系统拒查或终止待审报告只记录技术状态，不能据此宣称受益人不存在或报告义务当然消灭。 |
| GAP.A01.UNREADABLE_UNITS | OPEN | 上游未决：219 个来源单元在已有解析结果中不可读或为空；无法审查其业务含义。此处仅保留缺口，不重新调用 MinerU 或猜测原文。 | ISSUE.A01.KF.UNREADABLE_UNITS | 材料提供方与业务审阅人 | 对应单元维持 UNREADABLE / NOT_REVIEWED；不得当作已覆盖的业务含义。 |
| GAP.A01.SOURCE_PRECEDENCE | OPEN | 上游未决：已有规则区分备案与金融机构义务，但尚未形成跨来源效力、地域及生效日冲突的完整判序。问题映射不等于已回答。 | ISSUE.A01.KF.SOURCE_PRECEDENCE, Q.A01.S87 | 法规维护人与业务专家 | 不得以当前规则替代具体场景的来源效力判定。 |
| GAP.A01.FX_CONVERSION | OPEN | 上游未决：免备案资本门槛涉及等值外币，但当前材料未给出可据以确认的折算时点、汇率来源与计算口径。问题映射不等于已回答。 | ISSUE.A01.KF.FX_CONVERSION, Q.A01.S02 | 法规维护人与备案业务专家 | 外币资本接近门槛时维持 UNKNOWN，不自行指定汇率。 |
| GAP.A01.OPTION_CLASSIFICATION | OPEN | 上游未决：免报或国企法代系统选项与客观资格不符时，正式差异分类及处置指引未进入本批权威材料。 | ISSUE.A01.KF.OPTION_CLASSIFICATION | 法规维护人与系统业务负责人 | 不依据二手系统选项推断法定差异类别。 |
| GAP.A01.CROSSMONTH_GUIDANCE | OPEN | 上游未决：二手材料声称跨月三十日内非重大，但未提供能改变现行正式办法年月差异标准的权威依据。 | ISSUE.A01.KF.CROSSMONTH_GUIDANCE | 法规维护人与业务专家 | 按现行正式办法处理年月差异，不以供应商说法关闭。 |
| GAP.A01.UNREADABLE_FIGURE | OPEN | 上游未决：外链图例未提供可读股权路径，匿名案例亦不能证实特定实名主体，当前无法完成归档证据核对。 | ISSUE.A01.KF.UNREADABLE_FIGURE | 材料提供方与证据归档人员 | 不补画股权路径，不把匿名示例当作真实确认案例。 |
| GAP.A01.DATE_AUTHORITY | OPEN | 上游未决：形成日期只有范围或证据冲突时，材料未给出机构内部最终裁决和签核权限。 | ISSUE.A01.KF.DATE_AUTHORITY | 机构制度负责人 | 保留日期范围与冲突，不强行填唯一日期。 |
| GAP.A01.INSTITUTION_GOVERNANCE | OPEN | 上游未决：有权岗位、特殊地区口径和业务使用授权尚无经确认的机构制度输入。 | ISSUE.A01.KF.INSTITUTION_GOVERNANCE | 机构制度负责人 | 仅记录待确认事项，不把设计建议写成机构规则。 |
| GAP.A01.DISPUTE.ST.TXT021.U00031.01 | OPEN | 上游未决：二次分类摘要列出草案/正式版存量期限、发布时间、30日/30工作日、国企查询未命中、记录保存期限、重大变化人数指标等二手材料间冲突；这些只是待核线索，不能独立确立规范结论。 | ISSUE.A01.KF.DISPUTE.ST.TXT021.U00031.01 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT051.U00065.001 | OPEN | 上游未决：文章宣称转引公示信息的产品展示具有法律效力；数据摘录或产品截图的证据效力不能仅由供应商主张确定。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT051.U00065.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT052.U00064.001 | OPEN | 上游未决：供应商宣称其系统可完全代替人工识别特定情形并自动标记；与规范来源禁止自动化替代必要风险判断的要求存在潜在冲突，不得当作金融机构免责依据。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT052.U00064.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.STM.SRC.TXT058.U00014.S01 | OPEN | 上游未决：厂商文章在标准一识别叙述中使用“最终穿透识别持股≥25%自然人”的表达。 | ISSUE.A01.KF.DISPUTE.STM.SRC.TXT058.U00014.S01 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.STM.SRC.TXT059.U00016.S01 | OPEN | 上游未决：厂商自述其对“≥25%持股”建立多层校验机制。 | ISSUE.A01.KF.DISPUTE.STM.SRC.TXT059.U00016.S01 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.STM.SRC.TXT062.U00014.S01 | OPEN | 上游未决：厂商文章将三项标准表达为“股权/合伙权益≥25%、收益权/表决权≥25%、实际控制”。 | ISSUE.A01.KF.DISPUTE.STM.SRC.TXT062.U00014.S01 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.STM.SRC.TXT062.U00022.S01 | OPEN | 上游未决：厂商称其对加强识别客户把产品阈值从“≥25%”自动下调至“≥10%”，并支持风险标签配置。 | ISSUE.A01.KF.DISPUTE.STM.SRC.TXT062.U00022.S01 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT063.U00039.001 | OPEN | 上游未决：供应商提议优先推荐公开披露文件中的实际控制人；披露人仅为候选，是否控制客户及披露期间须另核。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT063.U00039.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT063.U00041.001 | OPEN | 上游未决：产品声称对第三标准结果中已有公开披露的实际控制人优先推荐；推荐不等于认定或优于其他可靠来源。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT063.U00041.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00016.001 | OPEN | 上游未决：文章称客户异常变化触发加强识别时阈值从25%下调至10%；原第12号令第二十一条将10%作为可选的加强措施示例，并未规定每次异常必须下调。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00016.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00017.001 | OPEN | 上游未决：文章声称简化或豁免条件丧失一律构成重大变化、必须按普通标准重识别；须区分条件变化、受益所有权是否受影响和第二十五条禁止继续简化的效果。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00017.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00028.001 | OPEN | 上游未决：作者把受益所有人总人数净增加与新增自然人并用作变化判断；仅看净人数可能遗漏旧人退出、新人进入而总数不变的情况。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00028.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00040.001 | OPEN | 上游未决：作者把名单中自然人退出且受益所有人总数净减少视为变化；净人数单独判断不足以处理多人替换与权利类型变更。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00040.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00052.001 | OPEN | 上游未决：作者认为总人数不变但适用标准由持股、收益、控制或简化路径互转可能影响权利类型；文中“标准四”不是第12号令第八条列举的第四项，定义不明。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00052.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00063.001 | OPEN | 上游未决：作者以名单具体人员、人数、识别理由三问总结变化影响；即使这三项没变化，比例或形成、终止年月变化仍可能影响备案信息与重大差异判断，不能用作不再核实的绝对豁免。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00063.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00073.001 | OPEN | 上游未决：企查查称自动比较变更前后识别人数与关系类型以判重大变化、免人工逐案分析；该产品能力不能代替金融机构必要的风险判断及权利事实核实。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00073.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00076.001 | OPEN | 上游未决：供应商称系统判定不影响受益所有权的变更仅归档、不触发业务复核；该自动豁免可能漏掉同数换人、形成时间和控制事实变化。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00076.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT064.U00080.001 | OPEN | 上游未决：企查查宣称系统可代替逐案人工研判并准确分类重大变化；效果未经验证，风险决策责任仍由金融机构承担。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT064.U00080.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT065.U00015.001 | OPEN | 上游未决：文章称国资委名单曾将脱敏名称为中建某成都公司列为第51号假冒央企，并称其下设各级子公司亦在公告范围；未核对原始名单、完整企业身份及公告适用范围。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT065.U00015.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.STM.SRC.TXT066.U00016.S01 | OPEN | 上游未决：厂商文章自述其产品把受益所有权关系形成日期统一调整为“按受益所有人最新股权变化定位的形成日期”这一口径。 | ISSUE.A01.KF.DISPUTE.STM.SRC.TXT066.U00016.S01 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00006.001 | OPEN | 上游未决：作者以图文速览概括备案主体、承诺免报、三类受益所有人、身份与权利信息、设立和变更时限；混入“部分省市延期”但未列明地区与批准文件。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00006.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00006.002 | OPEN | 上游未决：文章提到2025年11月1日前存量主体补备及部分省市延期；延期范围、法律依据和截至时间未知，不能改写统一规范期限。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00006.002 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00015.001 | OPEN | 上游未决：文章称新设主体设立时备案、实施前登记主体2025年11月1日前补备、信息变更或失去免报条件后30日内更新；另称存量期限“已延期”，却未提供地区、文件与有效期限，后者待核。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00015.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00019.001 | OPEN | 上游未决：作者建议权利形成日期锚定当前最新权利状态及章程、转让协议的生效时间，每人分别核实，避免统一取认缴日期；“最新一次满足标准日”这一通用口径未经本材料给出权威条款，持续持有期间比例变动如何处理仍未决。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00019.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT067.U00021.001 | OPEN | 上游未决：文章称金融机构可比对备案与自行识别结果，但把人员不匹配、关系类型错误、应备未备一概表述为必然重大差异且必然报告，忽略客户沟通、差异成因、条件和报告时间分支；应回核2025年第12号令。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT067.U00021.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT068.U00023.001 | OPEN | 上游未决：企查查宣称总公司注销而无受益所有人可沿用时，自动将分支机构负责人归为“日常经营管理人员”；规范第九条并未直接规定该替代，且母公司注销不证明第八条前三类均不存在，不得作为已确立识别规则。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT068.U00023.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
| GAP.A01.DISPUTE.ST.CONTEXT.TXT068.U00025.001 | OPEN | 上游未决：文章称工商资料缺少总公司关系时识别方法见下图，并输出依据；文字未写明具体识别路径，下图仅图片外链，故真实分支逻辑缺证。 | ISSUE.A01.KF.DISPUTE.ST.CONTEXT.TXT068.U00025.001 | 法规维护人与业务专家 | 保留来源陈述和争议标记，不把该断言提升为规范或机构规则。 |
