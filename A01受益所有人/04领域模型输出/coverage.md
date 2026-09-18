# 受益所有人识别、备案核对与差异处置：覆盖与审计

模型 A01.DomainModel / 0.3.0；DSL 2.0.0；范围模式 FULL_BASELINE。

本表核对对应关系与实际证据，不以引用存在代替语义正确性。

## 问题覆盖

| 问题 | 状态 | 规则 | 流程 | 案例 | 模型 | 缺口 |
| --- | --- | --- | --- | --- | --- | --- |
| K.Q.07 | PARTIAL | K.R.07, K.R.07.NATURE, K.R.07.APPLY, K.R.07.RISK | M.Process.G2 | K.C.PILOT.01, K.C.PILOT.02, K.C.PILOT.03, K.C.PILOT.04, K.C.PILOT.15 | M.Judgment.Risk, M.Judgment.StateNature, M.Process.G2, M.Rule.Article44, M.Rule.RelativeHolding, M.Rule.StateApplicability, M.Rule.StateSimplification | M.Gap.SEMANTIC_REVIEW, M.Gap.CURRENT_TARGET_RISK |
| K.Q.07.NATURE | PARTIAL | K.R.07.NATURE | M.Process.G2 | K.C.PILOT.01, K.C.PILOT.02 | M.Judgment.StateNature, M.Process.G2, M.Rule.Article44, M.Rule.RelativeHolding | M.Gap.SEMANTIC_REVIEW |
| K.Q.07.APPLY | PARTIAL | K.R.07.APPLY | M.Process.G2 | K.C.PILOT.03, K.C.PILOT.15 | M.Judgment.StateNature, M.Process.G2, M.Rule.RelativeHolding, M.Rule.StateApplicability | M.Gap.SEMANTIC_REVIEW, M.Gap.CURRENT_TARGET_RISK |
| K.Q.07.RISK | PARTIAL | K.R.07.RISK | M.Process.G2 | K.C.PILOT.04, K.C.PILOT.15 | M.Judgment.Risk, M.Process.G2, M.Rule.StateSimplification | M.Gap.SEMANTIC_REVIEW, M.Gap.CURRENT_TARGET_RISK |
| K.Q.11 | PARTIAL | K.R.11, K.R.11.START, K.R.11.HISTORY | M.Process.G4 | K.C.PILOT.05, K.C.PILOT.06, K.C.PILOT.07, K.C.PILOT.08, K.C.REVIEW.TYPE_CONTINUITY | M.Constraint.BeneficialOwnershipInterval, M.Constraint.ControlInterval, M.Constraint.RightInterval, M.Judgment.Continuity, M.Judgment.EffectiveDate, M.Process.G4, M.Rule.Formation | M.Gap.SEMANTIC_REVIEW |
| K.Q.11.START | PARTIAL | K.R.11.START | M.Process.G4 | K.C.PILOT.05, K.C.PILOT.06 | M.Judgment.EffectiveDate, M.Process.G4 | M.Gap.SEMANTIC_REVIEW |
| K.Q.11.HISTORY | PARTIAL | K.R.11.HISTORY | M.Process.G4 | K.C.PILOT.07, K.C.PILOT.08, K.C.REVIEW.TYPE_CONTINUITY | M.Constraint.BeneficialOwnershipInterval, M.Judgment.Continuity, M.Process.G4, M.Rule.Formation | M.Gap.SEMANTIC_REVIEW |
| K.Q.18 | PARTIAL | K.R.18, K.R.18.DATES, K.R.18.PENDING | M.Process.G6 | K.C.PILOT.09, K.C.PILOT.10, K.C.PILOT.11 | M.Judgment.DifferenceCause, M.Process.G6, M.Rule.DateYearMonth, M.Rule.MaterialDifference, M.Rule.TimingPending, M.Rule.UpdateDue | M.Gap.02, M.Gap.SEMANTIC_REVIEW, M.Gap.INTERFACE_REPORT_DUTY |
| K.Q.18.DATES | PARTIAL | K.R.18.DATES | M.Process.G6 | K.C.PILOT.09, K.C.PILOT.10 | M.Process.G6, M.Rule.DateYearMonth, M.Rule.MaterialDifference | M.Gap.02, M.Gap.SEMANTIC_REVIEW |
| K.Q.18.PENDING | PARTIAL | K.R.18.PENDING | M.Process.G6 | K.C.PILOT.11 | M.Process.G6, M.Rule.TimingPending, M.Rule.UpdateDue | M.Gap.02, M.Gap.SEMANTIC_REVIEW |
| K.Q.19 | PARTIAL | K.R.19, K.R.19.CORRECT, K.R.19.CLOSE | M.Process.G6 | K.C.PILOT.12, K.C.PILOT.13, K.C.PILOT.14 | M.Judgment.DifferenceCause, M.Machine.Difference, M.Process.G6, M.Rule.CloseDifference, M.Rule.CorrectionAction, M.Rule.ReportRequired | M.Gap.02, M.Gap.SEMANTIC_REVIEW |
| K.Q.19.CORRECT | PARTIAL | K.R.19.CORRECT | M.Process.G6 | K.C.PILOT.12 | M.Judgment.DifferenceCause, M.Process.G6, M.Rule.CorrectionAction, M.Rule.ReportRequired | M.Gap.02, M.Gap.SEMANTIC_REVIEW |
| K.Q.19.CLOSE | PARTIAL | K.R.19.CLOSE | M.Process.G6 | K.C.PILOT.13, K.C.PILOT.14 | M.Judgment.DifferenceCause, M.Machine.Difference, M.Process.G6, M.Rule.CloseDifference | M.Gap.SEMANTIC_REVIEW |
| K.Q.01 | PARTIAL | K.R.01 | M.Process.G1 | K.C.IDENT.Q01.01, K.C.IDENT.Q01.02, K.C.IDENT.Q01.03 | M.Judgment.Authority, M.Process.G1, M.Rule.CddScope, M.Rule.FilingScope | M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.MISSING_ORDER11 |
| K.Q.02 | PARTIAL | K.R.02 | M.Process.G1 | K.C.IDENT.Q02.01, K.C.IDENT.Q02.02, K.C.IDENT.Q02.03, K.C.IDENT.Q02.04 | M.Process.G1, M.Rule.FilingExemption | M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.FX_EQUIV |
| K.Q.03 | PARTIAL | K.R.03 | M.Process.G1 | K.C.IDENT.Q03.01, K.C.IDENT.Q03.02, K.C.IDENT.Q03.03, K.C.IDENT.Q03.04 | M.Constraint.RightHolder, M.Constraint.RightParty, M.Constraint.RightRatio, M.Constraint.RightTarget, M.Process.G1, M.Rule.EquityPaths, M.Rule.EquityTotal, M.Rule.KnownEquityLowerBound, M.Rule.KnownEquityPaths, M.Rule.KnownStandard1Candidate, M.Rule.PersonQualified, M.Rule.Standard1, M.Rule.UseStandard2, M.Rule.UseStandard3 | M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.CIRCULAR_CALC, M.Gap.INTERFACE_THRESHOLD |
| K.Q.04 | PARTIAL | K.R.04 | M.Process.G1 | K.C.IDENT.Q04.01, K.C.IDENT.Q04.02, K.C.IDENT.Q04.03, K.C.IDENT.Q04.04 | M.Constraint.RightParty, M.Constraint.RightRatio, M.Process.G1, M.Rule.IncomePaths, M.Rule.IncomeTotal, M.Rule.PersonQualified, M.Rule.Standard2, M.Rule.UseStandard2, M.Rule.VotingPaths, M.Rule.VotingTotal | M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.CIRCULAR_CALC |
| K.Q.05 | PARTIAL | K.R.05 | M.Process.G1 | K.C.IDENT.Q04.04, K.C.IDENT.Q05.01, K.C.IDENT.Q05.02, K.C.IDENT.Q05.03, K.C.IDENT.Q05.04 | M.Judgment.Control, M.Process.G1, M.Rule.PersonQualified, M.Rule.Standard3, M.Rule.UseStandard3 | M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.CIRCULAR_CALC |
| K.Q.06 | PARTIAL | K.R.06 | M.Process.G1 | K.C.IDENT.Q06.01, K.C.IDENT.Q06.02, K.C.IDENT.Q06.03 | M.Constraint.AppointmentInterval, M.Process.G1, M.Rule.Fallback | M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.TIED_MANAGERS |
| K.Q.08 | PARTIAL | K.R.08 | M.Process.G1 | K.C.IDENT.Q08.01, K.C.IDENT.Q08.02, K.C.IDENT.Q08.03, K.C.IDENT.Q08.04, K.C.IDENT.Q08.05 | M.Constraint.AppointmentInterval, M.Process.G1, M.Rule.BranchRoute | M.Gap.SEMANTIC_REVIEW |
| K.Q.09 | PARTIAL | K.R.09, K.R.09.TYPE, K.R.09.ASSET, K.R.09.RELIANCE | M.Process.G3 | K.C.IDENT.Q09.01, K.C.IDENT.Q09.02, K.C.IDENT.Q09.03, K.C.IDENT.Q09.04, K.C.IDENT.Q09.05, K.C.IDENT.Q09.06, K.C.IDENT.Q09.07 | M.Judgment.Products, M.Process.G3, M.Rule.AssetSimplification, M.Rule.ManagerReliance, M.Rule.TrustFull, M.Rule.TrustSimplification | M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.AM_MANAGER |
| K.Q.10 | PARTIAL | K.R.10, K.R.EXT.GOV.10.FORMATION | M.Process.G1, M.Process.G4 | K.C.EXT.GOV.10.01, K.C.EXT.GOV.10.02 | M.Judgment.EffectiveDate, M.Judgment.IdentityRights, M.Judgment.RecordContents, M.Process.G1, M.Process.G4 | M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS |
| K.Q.12 | PARTIAL | K.R.12, K.R.EXT.GOV.12.FILING, K.R.EXT.GOV.12.LEGACY_CDD | M.Process.G4 | K.C.EXT.GOV.12.01, K.C.EXT.GOV.12.02 | M.Process.G4, M.Rule.FilingDue, M.Rule.LegacyDeferral, M.Rule.LegacyDue | M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS |
| K.Q.13 | PARTIAL | K.R.13, K.R.EXT.GOV.13.IDENTIFY, K.R.EXT.GOV.13.VERIFY | M.Process.G5 | K.C.EXT.GOV.13.01, K.C.EXT.GOV.13.02 | M.Judgment.IdentityRights, M.Process.G5, M.Rule.QueryAfterIdentification | M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS |
| K.Q.14 | PARTIAL | K.R.14, K.R.EXT.GOV.14.STOP | M.Process.G5 | K.C.EXT.GOV.14.01, K.C.EXT.GOV.14.02 | M.Judgment.RemainingRisk, M.Judgment.Risk, M.Process.G5, M.Rule.RefuseOrEnd | M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS |
| K.Q.15 | PARTIAL | K.R.15, K.R.EXT.GOV.15.STATE, K.R.EXT.GOV.15.EXEMPT, K.R.EXT.GOV.15.SIMPLIFY, K.R.EXT.GOV.15.FILING_EXEMPT | M.Process.G2, M.Process.G5 | K.C.EXT.GOV.15.01, K.C.EXT.GOV.15.02 | M.Judgment.Authority, M.Judgment.Risk, M.Judgment.StateNature, M.Process.G2, M.Process.G5, M.Rule.CddExemption, M.Rule.FilingExemption, M.Rule.SimplificationMeasure, M.Rule.StateApplicability, M.Rule.StateSimplification | M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.FX_EQUIV, M.Gap.EXT.GOV.BROAD_UNITS, M.Gap.CURRENT_TARGET_RISK |
| K.Q.16 | PARTIAL | K.R.16, K.R.EXT.GOV.16.FREQUENCY | M.Process.G4 | K.C.EXT.GOV.16.01, K.C.EXT.GOV.16.02 | M.Process.G4, M.Rule.ReviewTrigger | M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.REVIEW_FREQUENCY, M.Gap.EXT.GOV.BROAD_UNITS |
| K.Q.17 | PARTIAL | K.R.17 | M.Process.G6 | K.C.EXT.OPS.17.A, K.C.EXT.OPS.17.B | M.Judgment.DifferenceCause, M.Process.G6, M.Rule.QueryAfterIdentification | M.Gap.SEMANTIC_REVIEW |
| K.Q.20 | PARTIAL | K.R.20, K.R.EXT.GOV.20.ACCESS, K.R.EXT.GOV.20.TRANSPORT | M.Process.G7 | K.C.EXT.GOV.20.01, K.C.EXT.GOV.20.02 | M.Judgment.Authority, M.Process.G7, M.Rule.Access, M.Rule.ReturnMode, M.Rule.Transport | M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.RETENTION, M.Gap.EXT.GOV.BROAD_UNITS |
| K.Q.21 | PARTIAL | K.R.21, K.R.EXT.GOV.21.TRANSITION, K.R.EXT.GOV.21.LIABILITY | M.Process.G7 | K.C.EXT.GOV.21.01, K.C.EXT.GOV.21.02 | M.Judgment.Authority, M.Judgment.Liability, M.Process.G7, M.Rule.Regime | M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.PENALTY_BASIS, M.Gap.EXT.GOV.BROAD_UNITS |
| K.Q.22 | PARTIAL | K.R.22 | M.Process.G8 | K.C.EXT.OPS.22.A, K.C.EXT.OPS.22.B | M.Judgment.FilingRoute, M.Process.G8, M.Rule.FilingSubmit | M.Gap.SEMANTIC_REVIEW |
| K.Q.23 | PARTIAL | K.R.23 | M.Process.G9 | K.C.EXT.OPS.23.A, K.C.EXT.OPS.23.B, K.C.EXT.OPS.23.C, K.C.EXT.OPS.23.D, K.C.EXT.OPS.23.E, K.C.EXT.OPS.23.F | M.Machine.Query, M.Process.G9, M.Rule.QueryAllowed, M.Rule.QueryMatch, M.Rule.QueryUsable | M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.RETENTION |
| K.Q.23.VERIFY | PARTIAL | K.R.23.VERIFY | M.Process.G9 | K.C.EXT.OPS.23.A, K.C.EXT.OPS.23.B | M.Machine.Query, M.Process.G9, M.Rule.DailyStop, M.Rule.QueryAllowed, M.Rule.QueryUsable | M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.RETENTION |
| K.Q.23.CURRENT | PARTIAL | K.R.23.CURRENT | M.Process.G9 | K.C.EXT.OPS.23.C, K.C.EXT.OPS.23.D | M.Machine.Query, M.Process.G9, M.Rule.CurrentQuery, M.Rule.QueryMatch, M.Rule.QueryUsable, M.Rule.Reverification | M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.RETENTION |
| K.Q.23.HISTORY | PARTIAL | K.R.23.HISTORY | M.Process.G9 | K.C.EXT.OPS.23.E, K.C.EXT.OPS.23.F | M.Judgment.Continuity, M.Process.G9, M.Rule.QueryMatch | M.Gap.SEMANTIC_REVIEW |
| K.Q.24 | PARTIAL | K.R.24 | M.Process.G9 | K.C.EXT.OPS.24.R1, K.C.EXT.OPS.24.R2, K.C.EXT.OPS.24.S1, K.C.EXT.OPS.24.S2, K.C.EXT.OPS.24.C1, K.C.EXT.OPS.24.C2, K.C.EXT.OPS.24.P1, K.C.EXT.OPS.24.P2, K.C.EXT.OPS.24.F1, K.C.EXT.OPS.24.F2 | M.Machine.Report, M.Process.G9, M.Rule.ReportContent, M.Rule.ReportSubmit | M.Gap.SEMANTIC_REVIEW |
| K.Q.24.REPORT | PARTIAL | K.R.24.REPORT | M.Process.G9 | K.C.EXT.OPS.24.R1, K.C.EXT.OPS.24.R2 | M.Process.G9, M.Rule.ReportContent, M.Rule.ReportSubmit | M.Gap.SEMANTIC_REVIEW, M.Gap.INTERFACE_REPORT_DUTY, M.Gap.INTERFACE_THRESHOLD, M.Gap.INTERFACE_IDENTITY |
| K.Q.24.STATUS | PARTIAL | K.R.24.STATUS | M.Process.G9 | K.C.EXT.OPS.24.S1, K.C.EXT.OPS.24.S2 | M.Constraint.ReportFeedback, M.Machine.Report, M.Process.G9 | M.Gap.SEMANTIC_REVIEW |
| K.Q.24.CASE | PARTIAL | K.R.24.CASE | M.Process.G9 | K.C.EXT.OPS.24.C1, K.C.EXT.OPS.24.C2 | M.Constraint.BomisCaseDuplicate, M.Machine.Case, M.Process.G9, M.Rule.CaseQuery | M.Gap.SEMANTIC_REVIEW |
| K.Q.24.PARAM | PARTIAL | K.R.24.PARAM | M.Process.G9 | K.C.EXT.OPS.24.P1, K.C.EXT.OPS.24.P2 | M.Process.G9, M.Rule.ParameterContinuity, M.Rule.ParameterResend, M.Rule.ParameterSend | M.Gap.SEMANTIC_REVIEW |
| K.Q.24.FILE | PARTIAL | K.R.24.FILE | M.Process.G9 | K.C.EXT.OPS.24.F1, K.C.EXT.OPS.24.F2 | M.Constraint.FileFeedback, M.Constraint.FileTransferDuplicate, M.Machine.File, M.Process.G9, M.Rule.FileUsable | M.Gap.SEMANTIC_REVIEW, M.Gap.INTERFACE_IDENTITY |

## 逐条规则要素

### K.R.01

状态：PARTIAL；问题：K.Q.01；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.MISSING_ORDER11

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 截至2026-09-15的中国境内受益所有人备案办理，以及12号令下金融机构对非自然人客户的受益所有人识别核实。 | M.Process.G1.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 取得主体登记身份和组织形式、业务关系、承办机构是否属于客户尽调义务机构、适用时点。 | M.Access.purpose, M.Identification.as_of, M.Identification.business_relation, M.Identification.evidence, M.Identification.institution_in_scope, M.Identification.subject, M.Subject.kind | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 分别判断3号令备案主体范围和12号令非自然人客户识别范围；公司、合伙企业、外国公司分支机构进入备案判断，金融机构对非自然人客户进入识别核实，个体工商户从两项本专项要求中排除。 | M.Judgment.Authority.criteria, M.Rule.CddScope.expression, M.Rule.FilingScope.expression | MIXED | 由判断备案适用范围、判断金融机构识别适用范围、主体分类、用途授权和责任适用核查共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 输出备案适用、金融机构识别适用、两者均适用或本专项均不适用四类结果，并注明责任主体；当前暂无需备案的其他非自然人客户仍可进入金融机构识别。 | M.Access.institution_authorized, M.Access.lawful_purpose, M.Access.operator_authorized, M.Identification.category_verified, M.Identification.cdd_applicable, M.Identification.filing_applicable | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 第二版指南所述“暂无需备案”属于当前办理范围说明；信托、资管、分支和12号令第十、十一条主体另走专门分支。 | M.Judgment.Authority.criteria, M.Rule.CddScope.expression, M.Rule.FilingScope.expression | FORMALIZED | 第二版指南所述“暂无需备案”属于当前办理范围说明；信托、资管、分支和12号令第十、十一条主体另走专门分支。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 组织形式或业务关系未知时不分流；缺2025年第11号令时不能穷举义务机构，补充该令后再封闭机构清单。 | M.Judgment.Authority.on_missing, M.Rule.CddScope.on_unknown, M.Rule.FilingScope.on_unknown | FORMALIZED | 组织形式或业务关系未知时不分流；缺2025年第11号令时不能穷举义务机构，补充该令后再封闭机构清单。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版备案指南日期为2026-01。本规则按2026-09-15在限定材料内整理。 | M.Identification.as_of | FORMALIZED | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版备案指南日期为2026-01。本规则按2026-09-15在限定材料内整理。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.02

状态：PARTIAL；问题：K.Q.02；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.FX_EQUIV

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 3号令备案主体中的公司、合伙企业承诺免报判断；不包括金融机构是否免于识别。 | M.Process.G1.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 取得注册资本或出资额及币种、全体股东合伙人名册、代持和协议安排、控制与收益事实，并确认不是外国公司分支机构。 | M.Filing.all_natural_holders, M.Filing.as_of, M.Filing.capital_cny, M.Filing.no_external_beneficiary, M.Filing.no_other_control_benefit, M.Filing.promise_truthful, M.Subject.kind | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 资本或出资额不超过1000万元等值、股东合伙人全为自然人、无股东合伙人外自然人控制或获益、无股权合伙权益外控制或获益，四项同时成立且主体作出真实承诺。 | M.Rule.FilingExemption.expression | FORMALIZED | 由承诺免报条件共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 可承诺免于提交具体备案信息；任一条件不成立则自行填报；后来失去条件时自失效之日起30日内备案。 | M.Filing.promise_exempt | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 外国公司及其分支机构不适用；承诺免报不免除金融机构按12号令识别核实，也不同于12号令第十条免于识别。 | M.Rule.FilingExemption.expression | FORMALIZED | 外国公司及其分支机构不适用；承诺免报不免除金融机构按12号令识别核实，也不同于12号令第十条免于识别。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 任一事实缺失即不得承诺；外币接近边界且缺折算依据时暂停结论并补充主管认可的折算时点和汇率。 | M.Rule.FilingExemption.on_unknown | FORMALIZED | 任一事实缺失即不得承诺；外币接近边界且缺折算依据时暂停结论并补充主管认可的折算时点和汇率。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01施行；第二版备案指南按2026-01版本用于解释。本规则按2026-09-15整理。 | M.Filing.as_of | FORMALIZED | 3号令自2024-11-01施行；第二版备案指南按2026-01版本用于解释。本规则按2026-09-15整理。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.03

状态：PARTIAL；问题：K.Q.03；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.CIRCULAR_CALC, M.Gap.INTERFACE_THRESHOLD

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 公司、合伙企业、法人及非法人组织的直接和间接股权、股份或合伙权益；外国公司分支按所属外国公司计算。 | M.Process.G1.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 固定判断时点，取得完整持有链、每层比例和权益类型，穿透到自然人，并确认比例可归属于同一自然人。 | M.Identification.acyclic, M.Identification.rights, M.Identification.structure_complete, M.Identification.subject, M.PersonAssessment.as_of, M.PersonAssessment.equity_ratio, M.PersonAssessment.known_equity_lower_bound, M.PersonAssessment.known_equity_paths, M.PersonAssessment.path_products, M.PersonAssessment.person, M.PersonAssessment.standard1, M.PersonAssessment.standard2, M.PersonAssessment.standard3 | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 逐路径相乘，同一自然人多路径相加；最终拥有比例达到或超过25%即达标，25%包含在内。逐人判断并保留全部达标者。 | M.Constraint.RightHolder.expression, M.Constraint.RightParty.expression, M.Constraint.RightRatio.expression, M.Constraint.RightTarget.expression, M.Rule.EquityPaths.expression, M.Rule.EquityTotal.expression, M.Rule.KnownEquityLowerBound.expression, M.Rule.KnownEquityPaths.expression, M.Rule.KnownStandard1Candidate.expression, M.Rule.PersonQualified.expression, M.Rule.Standard1.expression, M.Rule.UseStandard2.expression, M.Rule.UseStandard3.expression | FORMALIZED | 由股权或合伙权益路径逐条乘算、股权或合伙权益多路径合计、按股权或合伙权益标准认定、汇总该自然人的达标情况、本人优先采用标准一后的标准二、本人优先采用标准一后的标准三、保留已证明的股权路径、已知股权路径形成下界、不完整结构中的已知达标候选、一项持有权益只对应一种权利人、权益目标身份与主体一致、权益持有人身份与对应实体一致、权益比例以0至1表示共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 按标准一识别自然人并记录比例、路径及证据；对该人不再重复归为标准二、三，但继续识别其他自然人。 | M.PersonAssessment.equity_ratio, M.PersonAssessment.known_equity_lower_bound, M.PersonAssessment.known_equity_paths, M.PersonAssessment.ownership_qualified, M.PersonAssessment.path_products, M.PersonAssessment.standard1, M.PersonAssessment.standard1_candidate, M.PersonAssessment.uses_standard2, M.PersonAssessment.uses_standard3 | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 12号令特定风险下金融机构可采取更严格阈值，例如10%；该阈值不改变一般备案25%以上基准。 | M.Constraint.RightHolder.expression, M.Constraint.RightParty.expression, M.Constraint.RightRatio.expression, M.Constraint.RightTarget.expression, M.Rule.EquityPaths.expression, M.Rule.EquityTotal.expression, M.Rule.KnownEquityLowerBound.expression, M.Rule.KnownEquityPaths.expression, M.Rule.KnownStandard1Candidate.expression, M.Rule.PersonQualified.expression, M.Rule.Standard1.expression, M.Rule.UseStandard2.expression, M.Rule.UseStandard3.expression | FORMALIZED | 12号令特定风险下金融机构可采取更严格阈值，例如10%；该阈值不改变一般备案25%以上基准。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 缺层、缺比例、代持未知或终点不是自然人时返回证据不足；循环、交叉持股没有本语料认可算法时停止精确比例结论。 | M.Constraint.RightHolder.on_unknown, M.Constraint.RightParty.on_unknown, M.Constraint.RightRatio.on_unknown, M.Constraint.RightTarget.on_unknown, M.Rule.EquityPaths.on_unknown, M.Rule.EquityTotal.on_unknown, M.Rule.KnownEquityLowerBound.on_unknown, M.Rule.KnownEquityPaths.on_unknown, M.Rule.KnownStandard1Candidate.on_unknown, M.Rule.PersonQualified.on_unknown, M.Rule.Standard1.on_unknown, M.Rule.UseStandard2.on_unknown, M.Rule.UseStandard3.on_unknown | FORMALIZED | 缺层、缺比例、代持未知或终点不是自然人时返回证据不足；循环、交叉持股没有本语料认可算法时停止精确比例结论。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版指南为2026-01版本。 | M.PersonAssessment.as_of | FORMALIZED | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版指南为2026-01版本。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.04

状态：PARTIAL；问题：K.Q.04；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.CIRCULAR_CALC

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 未满足标准一、但可能通过收益权或表决权达到阈值的自然人。 | M.Process.G1.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 先完成该自然人的标准一判断，再取得收益转让、代持、投票委托和其他协议及其效力、比例、期限。 | M.Identification.acyclic, M.Identification.rights, M.Identification.structure_complete, M.Identification.subject, M.PersonAssessment.as_of, M.PersonAssessment.income_path_products, M.PersonAssessment.income_ratio, M.PersonAssessment.person, M.PersonAssessment.standard1, M.PersonAssessment.standard2, M.PersonAssessment.standard3, M.PersonAssessment.voting_path_products, M.PersonAssessment.voting_ratio | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 最终收益权或表决权任一项达到或超过25%即达标；两类权利分别计算和记录。 | M.Constraint.RightParty.expression, M.Constraint.RightRatio.expression, M.Rule.IncomePaths.expression, M.Rule.IncomeTotal.expression, M.Rule.PersonQualified.expression, M.Rule.Standard2.expression, M.Rule.UseStandard2.expression, M.Rule.VotingPaths.expression, M.Rule.VotingTotal.expression | FORMALIZED | 由收益权路径逐条乘算、收益权多路径合计、表决权路径逐条乘算、表决权多路径合计、按收益权或表决权标准认定、汇总该自然人的达标情况、本人优先采用标准一后的标准二、一项持有权益只对应一种权利人、权益比例以0至1表示共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 按标准二识别自然人，记录收益权、表决权比例；若同时实际控制，则同时记录标准三。 | M.PersonAssessment.income_path_products, M.PersonAssessment.income_ratio, M.PersonAssessment.ownership_qualified, M.PersonAssessment.standard2, M.PersonAssessment.uses_standard2, M.PersonAssessment.voting_path_products, M.PersonAssessment.voting_ratio | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 已经满足标准一的同一自然人按标准一备案，不再把其重复归为标准二；普通工资、顾问费、交易收入不是股权合伙权益收益权。 | M.Constraint.RightParty.expression, M.Constraint.RightRatio.expression, M.Rule.IncomePaths.expression, M.Rule.IncomeTotal.expression, M.Rule.PersonQualified.expression, M.Rule.Standard2.expression, M.Rule.UseStandard2.expression, M.Rule.VotingPaths.expression, M.Rule.VotingTotal.expression | FORMALIZED | 已经满足标准一的同一自然人按标准一备案，不再把其重复归为标准二；普通工资、顾问费、交易收入不是股权合伙权益收益权。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 协议主体、比例、效力或最终归属无法核实时返回证据不足，不以名义持股或口头说明替代。 | M.Constraint.RightParty.on_unknown, M.Constraint.RightRatio.on_unknown, M.Rule.IncomePaths.on_unknown, M.Rule.IncomeTotal.on_unknown, M.Rule.PersonQualified.on_unknown, M.Rule.Standard2.on_unknown, M.Rule.UseStandard2.on_unknown, M.Rule.VotingPaths.on_unknown, M.Rule.VotingTotal.on_unknown | FORMALIZED | 协议主体、比例、效力或最终归属无法核实时返回证据不足，不以名义持股或口头说明替代。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版指南为2026-01版本。 | M.PersonAssessment.as_of | FORMALIZED | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版指南为2026-01版本。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.05

状态：PARTIAL；问题：K.Q.05；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.CIRCULAR_CALC

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 未满足标准一但可能单独或联合实际控制公司、合伙企业、法人或非法人组织的自然人。 | M.Process.G1.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 取得权力来源和实际行使证据，包括有效协议、章程、投票安排、任免和重大决策记录、财务授权及资产资金支配记录。 | M.Control.arrangement, M.Control.evidence, M.Control.exercise, M.Control.matters, M.PersonAssessment.control_verified, M.PersonAssessment.standard1, M.PersonAssessment.standard2, M.PersonAssessment.standard3 | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 判断自然人是否单独或与他人共同持续、实质支配人事、重大经营管理、财务收支、重要资产或主要资金；不设固定持股比例。 | M.Judgment.Control.criteria, M.Rule.PersonQualified.expression, M.Rule.Standard3.expression, M.Rule.UseStandard3.expression | MIXED | 由按实际控制标准认定、汇总该自然人的达标情况、本人优先采用标准一后的标准三、实际控制证据判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 按标准三识别自然人并记录单独或联合方式、具体控制内容和证据；与标准二同时成立时保留两类关系。 | M.Control.sustained, M.PersonAssessment.control_verified, M.PersonAssessment.ownership_qualified, M.PersonAssessment.standard3, M.PersonAssessment.uses_standard3 | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 关系密切、法定代表人、董事、顾问或第三方实际控制人标签不单独构成结论；实际控制人概念不得与受益所有人合并。 | M.Judgment.Control.criteria, M.Rule.PersonQualified.expression, M.Rule.Standard3.expression, M.Rule.UseStandard3.expression | FORMALIZED | 关系密切、法定代表人、董事、顾问或第三方实际控制人标签不单独构成结论；实际控制人概念不得与受益所有人合并。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 只有关系或职位线索、没有权力或行为证据时返回证据不足；联合控制还须说明共同安排及各方作用。 | M.Judgment.Control.on_missing, M.Rule.PersonQualified.on_unknown, M.Rule.Standard3.on_unknown, M.Rule.UseStandard3.on_unknown | FORMALIZED | 只有关系或职位线索、没有权力或行为证据时返回证据不足；联合控制还须说明共同安排及各方作用。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版指南为2026-01版本。 | M.Process.G1.trigger | FORMALIZED | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版指南为2026-01版本。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.06

状态：PARTIAL；问题：K.Q.06；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.TIED_MANAGERS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 经充分核实确实不存在标准一、二、三人员的法人、非法人组织或备案主体。 | M.Process.G1.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 三项标准均已用完整、可靠材料检查并得出无人满足，而非因材料缺失无法判断。 | M.Identification.all_standards_checked, M.Identification.any_standard_positive, M.Identification.structure_complete | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 从负责日常经营管理的人员中确定至少一名最高层级人员；公司和合伙企业按其治理与实际履职识别相应候选。 | M.Constraint.AppointmentInterval.expression, M.Rule.Fallback.expression | FORMALIZED | 由是否可以采用管理人员兜底、已知终止须晚于开始，未知终止不得冒充持续共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 将选定人员作为兜底受益所有人并记录职位和使用兜底的原因，不把其因此称为实际控制人。 | M.Identification.fallback_allowed | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 任一自然人达到标准一、二或三时不得以管理人员替代；外国公司分支另有叠加高管规则。 | M.Constraint.AppointmentInterval.expression, M.Rule.Fallback.expression | FORMALIZED | 任一自然人达到标准一、二或三时不得以管理人员替代；外国公司分支另有叠加高管规则。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 前三项任一缺证时不进入兜底；多名同层最高人员如何选择在限定材料中无优先级，须补充业务口径和选择理由。 | M.Constraint.AppointmentInterval.on_unknown, M.Rule.Fallback.on_unknown | FORMALIZED | 前三项任一缺证时不进入兜底；多名同层最高人员如何选择在限定材料中无优先级，须补充业务口径和选择理由。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版指南为2026-01版本。 | M.Process.G1.trigger | FORMALIZED | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版指南为2026-01版本。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.07

状态：PARTIAL；问题：K.Q.07；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.CURRENT_TARGET_RISK

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 拟主张国有独资、国有控股、国有实际控制、国有参股等性质的客户。 | M.Process.G2.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 取得股东结构、第一大股东及实际支配证据，依法核实国企性质。其他官方材料作为补件相互印证，不作为独立替代路径。 | M.Identification.data_doubt, M.Identification.matched_risk_measure, M.Identification.risk20_triggered, M.Identification.risk_assessment_complete, M.StateNature.cdd_branch_applicable, M.StateNature.evidence, M.StateNature.nature, M.StateNature.officially_verified, M.StateNature.relative_holding, M.StateNature.state_investor, M.StateNature.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 先按32号令等适用依据形成性质判断，再分别检查备案规则与金融机构12号令的适用分支，最后完成风险评估和禁用条件判断。 | M.Judgment.StateNature.criteria, M.Rule.StateApplicability.expression, M.Rule.StateSimplification.expression | MIXED | 由金融机构国企简化主体范围、国企简化风险门控、国有性质与实际支配证据判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 性质、适用性和风险均具备依据时选择相应简化措施；只符合国有参股的按该部分规则处理。 | M.Identification.simplification_allowed, M.StateNature.actual_dominance, M.StateNature.cdd_branch_applicable, M.StateNature.largest_shareholder, M.StateNature.nature, M.StateNature.officially_verified, M.StateNature.qualified_investor | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 性质标签不直接触发简化。现行操作一般直接简化、三类例外会核实的描述单独保留；是否已经满足全部制度风险要求仍待合规裁定。 | M.Judgment.StateNature.criteria, M.Rule.StateApplicability.expression, M.Rule.StateSimplification.expression | FORMALIZED | 性质标签不直接触发简化。现行操作一般直接简化、三类例外会核实的描述单独保留；是否已经满足全部制度风险要求仍待合规裁定。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 无法证明第一大股东、实际支配、官方国企性质或风险评估时，按一般或加强流程处理。 | M.Judgment.StateNature.on_missing, M.Rule.StateApplicability.on_unknown, M.Rule.StateSimplification.on_unknown | FORMALIZED | 无法证明第一大股东、实际支配、官方国企性质或风险评估时，按一般或加强流程处理。 缺证不得用默认值补足。 |
| 时间要求 | 按所引制度文件的生效和过渡条款；业务建议在确认后自确认版本生效。 | M.Process.G2.trigger | FORMALIZED | 按所引制度文件的生效和过渡条款；业务建议在确认后自确认版本生效。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.08

状态：PARTIAL；问题：K.Q.08；缺口：M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 国内法人、非法人组织分支机构和在中国登记的外国公司分支机构。 | M.Process.G1.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 确认所属主体类别、备案场景或金融机构客户关系、所属主体在本机构的尽调状态，以及外国公司和分支高管资料。 | M.Identification.branch_reuse_verified, M.Subject.kind | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 国内分支在金融机构识别中一般沿用所属主体受益所有人，仅在所属主体已是本机构客户且已完成尽调时复用既有信息；外国分支识别所属外国公司受益所有人并叠加分支高级管理人员。 | M.Constraint.AppointmentInterval.expression, M.Rule.BranchRoute.expression | FORMALIZED | 由分支机构识别路径、已知终止须晚于开始，未知终止不得冒充持续共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 国内分支形成与所属主体一致且说明是否复用的清单；外国分支形成所属公司受益所有人加至少一名分支高管的清单。 | M.Identification.branch_result | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 境内公司、合伙企业分支当前暂无需单独备案；外国公司本国申报豁免不适用于中国，分支高管不能替代所属公司穿透。 | M.Constraint.AppointmentInterval.expression, M.Rule.BranchRoute.expression | FORMALIZED | 境内公司、合伙企业分支当前暂无需单独备案；外国公司本国申报豁免不适用于中国，分支高管不能替代所属公司穿透。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 所属主体、既有尽调、外国公司结构或高管资料缺失时分别返回证据不足并补件。 | M.Constraint.AppointmentInterval.on_unknown, M.Rule.BranchRoute.on_unknown | FORMALIZED | 所属主体、既有尽调、外国公司结构或高管资料缺失时分别返回证据不足并补件。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版指南为2026-01版本。 | M.Process.G1.trigger | FORMALIZED | 3号令自2024-11-01施行；12号令自2026-01-20施行；第二版指南为2026-01版本。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.09

状态：PARTIAL；问题：K.Q.09；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.AM_MANAGER

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构为信托提供服务时的受益所有人识别。 | M.Process.G3.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 取得信托合同与登记、委托人受托人受益人监察人清单、控制条款；确认每个当事人是否为自然人。 | M.ProductAssessment.evidence, M.ProductAssessment.manager, M.ProductAssessment.product, M.ProductAssessment.trust_lookthrough_complete, M.ProductAssessment.trust_parties, M.ProductAssessment.trust_party_scope_complete | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 列入全部信托当事人和其他最终有效控制自然人；非自然人当事人逐一逐层追溯；未列明具体受益人时识别并记录受益人范围。 | M.Judgment.Products.criteria, M.Rule.TrustFull.expression | MIXED | 由完整信托当事人识别、信托与资管条件及受托机构履职判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成信托当事人、穿透自然人、其他最终控制人及未确定受益人范围的可审计记录。 | M.ProductAssessment.doubts, M.ProductAssessment.full_trust_identification, M.ProductAssessment.low_risk, M.ProductAssessment.manager_duties_effective, M.ProductAssessment.manager_people_identified, M.ProductAssessment.manager_system_sound, M.ProductAssessment.risk_assessment_complete, M.ProductAssessment.simple_structure, M.ProductAssessment.trust_lookthrough_complete, M.ProductAssessment.trust_party_scope_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 仅受聘的投资顾问、律师、会计师应留存基本信息，不因受聘身份自动成为受益所有人。 | M.Judgment.Products.criteria, M.Rule.TrustFull.expression | FORMALIZED | 仅受聘的投资顾问、律师、会计师应留存基本信息，不因受聘身份自动成为受益所有人。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 合同、登记、当事人名单、受益权登记或控制条款缺失时返回证据不足，不虚构具体受益人或以法人当事人为终点。 | M.Judgment.Products.on_missing, M.Rule.TrustFull.on_unknown | FORMALIZED | 合同、登记、当事人名单、受益权登记或控制条款缺失时返回证据不足，不虚构具体受益人或以法人当事人为终点。 缺证不得用默认值补足。 |
| 时间要求 | 12号令自2026-01-20施行；本规则按2026-09-15整理。 | M.Process.G3.trigger | FORMALIZED | 12号令自2026-01-20施行；本规则按2026-09-15整理。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.10

状态：PARTIAL；问题：K.Q.10；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 备案主体填报与金融机构识别留存两个场景。 | M.Process.G1.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已识别候选自然人、适用场景、受益所有权关系类型及证据。 | M.Identification.evidence, M.Identification.purpose, M.Identification.rights, M.Identification.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 分别套用备案信息集合或金融机构识别留存集合，并按关系类型补比例或控制方式，按法律关系生效和终止证据记录时间。 | M.Judgment.IdentityRights.criteria, M.Judgment.RecordContents.criteria | MANUAL | 由核实身份、权利及结构证据、场景所需信息集合核对共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成能够支持备案、核实、差异比较和持续复核的受益所有人信息记录。 | M.Identification.identity_verified, M.Identification.records_complete, M.Identification.rights_verified, M.Identification.structure_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 12号令第十八条对透明度较高且信息披露充分的特定客户允许较少身份要素，仅适用于金融机构场景。 | M.Judgment.IdentityRights.criteria, M.Judgment.RecordContents.criteria | FORMALIZED | 12号令第十八条对透明度较高且信息披露充分的特定客户允许较少身份要素，仅适用于金融机构场景。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 关系类型、比例、控制方式或生效依据不全时返回缺项并补证，不宣称信息完整。 | M.Judgment.IdentityRights.on_missing, M.Judgment.RecordContents.on_missing | FORMALIZED | 关系类型、比例、控制方式或生效依据不全时返回缺项并补证，不宣称信息完整。 缺证不得用默认值补足。 |
| 时间要求 | 备案规则自2024-11-01施行；金融机构规则自2026-01-20施行。 | M.Process.G1.trigger | FORMALIZED | 备案规则自2024-11-01施行；金融机构规则自2026-01-20施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.11

状态：PARTIAL；问题：K.Q.11；缺口：M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 每一自然人与主体之间的每一种受益所有权关系。 | M.Process.G4.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 取得章程、协议、决议、转让或控制安排的生效日及历史权益变化。 | M.Identification.subject, M.PersonAssessment.as_of, M.PersonAssessment.basis_evidence, M.PersonAssessment.continuity_verified, M.PersonAssessment.history, M.PersonAssessment.history_complete, M.PersonAssessment.person | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 按原文核实法律关系实际生效与终止；按已答业务口径取最近连续达标区间起点。跨类型且总体资格连续时不重置，分关系类型留存日期。 | M.Constraint.ControlInterval.expression, M.Constraint.RightInterval.expression, M.Judgment.Continuity.criteria, M.Judgment.EffectiveDate.criteria, M.Rule.Formation.expression | MIXED | 由当前总体形成日期、法律关系实际生效日期判断、历史完整性和总体资格连续判断、已知终止须晚于开始，未知终止不得冒充持续、已知终止须晚于开始，未知终止不得冒充持续共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 按每种关系保留形成、变化、终止及证据；整体资格连续则保留原总体日期，中断后取最新连续达标起点。 | M.PersonAssessment.continuity_verified, M.PersonAssessment.date_reason, M.PersonAssessment.formation_date, M.PersonAssessment.history_complete, M.PersonAssessment.legal_start | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 用户已答：权利类型切换但整体资格连续时，总体形成日期不重置，各关系类型分别留存事件日期。若整体资格实际中断，则重新达标按最新连续区间开始日期记录。连续性和生效日期仍须证据支持。 | M.Constraint.ControlInterval.expression, M.Constraint.RightInterval.expression, M.Judgment.Continuity.criteria, M.Judgment.EffectiveDate.criteria, M.Rule.Formation.expression | FORMALIZED | 用户已答：权利类型切换但整体资格连续时，总体形成日期不重置，各关系类型分别留存事件日期。若整体资格实际中断，则重新达标按最新连续区间开始日期记录。连续性和生效日期仍须证据支持。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 无法证明生效时间或中断区间时，形成日期保持待确认。 | M.Constraint.ControlInterval.on_unknown, M.Constraint.RightInterval.on_unknown, M.Judgment.Continuity.on_missing, M.Judgment.EffectiveDate.on_missing, M.Rule.Formation.on_unknown | FORMALIZED | 无法证明生效时间或中断区间时，形成日期保持待确认。 缺证不得用默认值补足。 |
| 时间要求 | 按所引制度文件的生效和过渡条款；业务建议在确认后自确认版本生效。 | M.PersonAssessment.as_of, M.PersonAssessment.formation_date, M.PersonAssessment.legal_start | FORMALIZED | 按所引制度文件的生效和过渡条款；业务建议在确认后自确认版本生效。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.12

状态：PARTIAL；问题：K.Q.12；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 备案设立和变化、存量备案主体、金融机构存量客户。 | M.Process.G4.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 确认义务主体、事件类型、事件日、风险等级和是否属于长期不动或严格限制客户。 | M.Filing.trigger, M.Filing.trigger_date, M.Followup.activated, M.Followup.higher_risk, M.Followup.inactive_or_restricted, M.Followup.legacy_customer, M.Followup.trigger_date | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 在线设立同步备案；现场设立或信息变化按30日；存量备案按2025-11-01；金融机构存量客户按6个月、2年或激活办理时例外。 | M.Rule.FilingDue.expression, M.Rule.LegacyDue.expression | FORMALIZED | 由备案及更新期限、存量客户补齐期限共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 得到明确起算点、截止要求和适用例外。 | M.Filing.due_date, M.Followup.due_date | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 长期不动户或严格限制客户仅延后金融机构存量识别核实，不消除激活办理时义务。 | M.Rule.FilingDue.expression, M.Rule.LegacyDue.expression | FORMALIZED | 长期不动户或严格限制客户仅延后金融机构存量识别核实，不消除激活办理时义务。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 事件日不明时不得从发现日倒推；30日不得当作日期差异容差。 | M.Rule.FilingDue.on_unknown, M.Rule.LegacyDue.on_unknown | FORMALIZED | 事件日不明时不得从发现日倒推；30日不得当作日期差异容差。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01；12号令自2026-01-20。 | M.Filing.due_date, M.Filing.trigger_date, M.Followup.due_date, M.Followup.trigger_date | FORMALIZED | 3号令自2024-11-01；12号令自2026-01-20。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.13

状态：PARTIAL；问题：K.Q.13；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构对非自然人客户的识别、核实和BOMIS核对。 | M.Process.G5.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 取得客户信息，并明确客户组织形式、结构、风险和是否属于备案主体。 | M.Identification.evidence, M.Identification.filing_applicable, M.Identification.identity_verified, M.Identification.rights, M.Identification.rights_verified, M.Identification.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 先用类型相符材料解释结构并识别自然人，再分别核实身份与权利；对备案主体查询核对BOMIS，多来源相互印证。 | M.Judgment.IdentityRights.criteria, M.Rule.QueryAfterIdentification.expression | MIXED | 由备案主体查询核对前提、核实身份、权利及结构证据共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成材料、识别路径、核实动作、BOMIS核对和风险判断完整的证据链。 | M.Identification.identity_verified, M.Identification.records_complete, M.Identification.refresh_query_required, M.Identification.rights_verified, M.Identification.structure_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 明显低风险或适用简化时可少取足够材料，但要记录过程和理由。 | M.Judgment.IdentityRights.criteria, M.Rule.QueryAfterIdentification.expression | FORMALIZED | 明显低风险或适用简化时可少取足够材料，但要记录过程和理由。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 仅客户声明、仅BOMIS或仅自动化结果均不足以宣称核实完成。 | M.Judgment.IdentityRights.on_missing, M.Rule.QueryAfterIdentification.on_unknown | FORMALIZED | 仅客户声明、仅BOMIS或仅自动化结果均不足以宣称核实完成。 缺证不得用默认值补足。 |
| 时间要求 | 自2026-01-20施行。 | M.Process.G5.trigger | FORMALIZED | 自2026-01-20施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.14

状态：PARTIAL；问题：K.Q.14；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 存在12号令第二十条特定情形的客户。 | M.Process.G5.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已有可描述的风险触发事实，而非仅有未解释的风险标签。 | M.Identification.enhanced_measures, M.Identification.enhanced_measures_completed, M.Identification.enhanced_reasons, M.Identification.evidence, M.Identification.residual_risk_manageable | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 将触发原因映射到一种或多种相匹配加强措施，实施后再评估剩余风险。 | M.Judgment.RemainingRisk.criteria, M.Judgment.Risk.criteria, M.Rule.RefuseOrEnd.expression | MIXED | 由加强后是否可拒绝或终止、风险及措施匹配判断、加强措施后的剩余风险判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成加强识别、合理限制、继续、拒绝或终止的分层决定及记录。 | M.Identification.data_doubt, M.Identification.enhanced_measures, M.Identification.enhanced_measures_completed, M.Identification.higher_risk, M.Identification.matched_risk_measure, M.Identification.refuse_or_end, M.Identification.residual_risk_manageable, M.Identification.restrict_needed, M.Identification.risk20_triggered, M.Identification.risk_assessment_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 风险触发不自动终止；措施不得明显超过必要限度或一刀切。 | M.Judgment.RemainingRisk.criteria, M.Judgment.Risk.criteria, M.Rule.RefuseOrEnd.expression | FORMALIZED | 风险触发不自动终止；措施不得明显超过必要限度或一刀切。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 触发事实、措施结果或风险能力边界不能证明时保持加强调查状态。 | M.Judgment.RemainingRisk.on_missing, M.Judgment.Risk.on_missing, M.Rule.RefuseOrEnd.on_unknown | FORMALIZED | 触发事实、措施结果或风险能力边界不能证明时保持加强调查状态。 缺证不得用默认值补足。 |
| 时间要求 | 自2026-01-20施行。 | M.Process.G5.trigger | FORMALIZED | 自2026-01-20施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.15

状态：PARTIAL；问题：K.Q.15；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.FX_EQUIV, M.Gap.EXT.GOV.BROAD_UNITS, M.Gap.CURRENT_TARGET_RISK

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构免识别和简化识别，以及备案承诺免报的边界。 | M.Process.G5.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已准确确定主体或产品类型、官方或可靠性质证据及当前风险。 | M.Identification.category_verified, M.Identification.data_doubt, M.Identification.enhanced_reasons, M.Identification.evidence, M.Identification.exemption_category, M.Identification.higher_risk, M.Identification.matched_risk_measure, M.Identification.risk20_triggered, M.Identification.risk_assessment_complete, M.Identification.simplification_category | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 先判断金融机构免识别封闭清单，再判断具体简化分支；无法准确判断或出现第二十条情形即阻断；备案免报单独判断。 | M.Judgment.Risk.criteria, M.Rule.CddExemption.expression, M.Rule.SimplificationMeasure.expression | MIXED | 由列明主体免识别条件、按具体主体分支选择措施、风险及措施匹配判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 记录免识别、简化识别、一般识别或备案免报的不同结论与依据。 | M.Identification.data_doubt, M.Identification.enhanced_measures, M.Identification.exemption_allowed, M.Identification.higher_risk, M.Identification.matched_risk_measure, M.Identification.risk20_triggered, M.Identification.risk_assessment_complete, M.Identification.simplification_measure | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 国有参股只免穿透国有资本部分；备案免报不免金融机构识别。 | M.Judgment.Risk.criteria, M.Rule.CddExemption.expression, M.Rule.SimplificationMeasure.expression | FORMALIZED | 国有参股只免穿透国有资本部分；备案免报不免金融机构识别。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 性质或风险证据不足时按一般识别，不以名称、法定代表人或系统勾选推定。 | M.Judgment.Risk.on_missing, M.Rule.CddExemption.on_unknown, M.Rule.SimplificationMeasure.on_unknown | FORMALIZED | 性质或风险证据不足时按一般识别，不以名称、法定代表人或系统勾选推定。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01；12号令自2026-01-20。 | M.Process.G5.trigger | FORMALIZED | 3号令自2024-11-01；12号令自2026-01-20。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.16

状态：PARTIAL；问题：K.Q.16；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.REVIEW_FREQUENCY, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构已建立业务关系的非自然人客户。 | M.Process.G4.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 存在既有识别基线、持续关注信息和变化事件。 | M.Followup.may_affect_ownership | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 出现可能影响受益所有权的事件即审核，审核后必要时更新；加强情形可提高频率。 | M.Rule.ReviewTrigger.expression | FORMALIZED | 由变更事件触发复核共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 保留新旧事实、影响判断、审核结果、更新内容和依据。 | M.Followup.review_required | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 人员变化只有在可能影响受益所有权时触发；本次来源未规定统一固定周期。 | M.Rule.ReviewTrigger.expression | FORMALIZED | 人员变化只有在可能影响受益所有权时触发；本次来源未规定统一固定周期。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 变化影响不清时保持审核待补证，不覆盖旧记录。 | M.Rule.ReviewTrigger.on_unknown | FORMALIZED | 变化影响不清时保持审核待补证，不覆盖旧记录。 缺证不得用默认值补足。 |
| 时间要求 | 自2026-01-20施行。 | M.Process.G4.trigger | FORMALIZED | 自2026-01-20施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.17

状态：PARTIAL；问题：K.Q.17；缺口：M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构核实属于备案范围的客户。 | M.Process.G6.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 确定组织形式、备案义务及本机构识别结果，保存查询时点。 | M.Difference.correction_evidence, M.Difference.filing_value, M.Difference.institution_value, M.Difference.recheck_evidence, M.Identification.filing_applicable, M.Identification.identity_verified, M.Identification.rights_verified | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 自行识别→查询核对→分辨错误、不一致、不完整、应备案未备案或查询故障；对确实应备案未备案者先提示，仍未备案则报告。 | M.Judgment.DifferenceCause.criteria, M.Rule.QueryAfterIdentification.expression | MIXED | 由备案主体查询核对前提、差异原因和更正后复核共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成可解释的比对结果及后续核实/提示/报告事项。 | M.Difference.affects_ubo, M.Difference.cause, M.Difference.customer_corrected, M.Difference.reason, M.Difference.recheck_consistent, M.Identification.refresh_query_required | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 承诺免报不是系统故障；未返回记录不自动证明应备案未备案。 | M.Judgment.DifferenceCause.criteria, M.Rule.QueryAfterIdentification.expression | FORMALIZED | 承诺免报不是系统故障；未返回记录不自动证明应备案未备案。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 主体类型、免报条件或查询结果不清时先补证；保持机构识别责任。 | M.Judgment.DifferenceCause.on_missing, M.Rule.QueryAfterIdentification.on_unknown | FORMALIZED | 主体类型、免报条件或查询结果不清时先补证；保持机构识别责任。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G6.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.18

状态：PARTIAL；问题：K.Q.18；缺口：M.Gap.02, M.Gap.SEMANTIC_REVIEW, M.Gap.INTERFACE_REPORT_DUTY

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 金融机构识别结果与BOMIS备案信息之间的差异。 | M.Process.G6.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已完成客户沟通、同一自然人匹配、差异字段和权利关系影响分析。 | M.Difference.actual_change_date, M.Difference.affects_ubo, M.Difference.as_of, M.Difference.correction_evidence, M.Difference.customer_corrected, M.Difference.filing_date, M.Difference.filing_value, M.Difference.institution_date, M.Difference.institution_value, M.Difference.key_rights_mismatch, M.Difference.other_major_branch, M.Difference.people_mismatch, M.Difference.recheck_evidence, M.Difference.update_due, M.Difference.year_month_mismatch | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 先辨同一人、关键身份和权利信息，再分别检查年月差异与是否影响受益所有人/关系类型认定；按第二十八、二十九条对应分支判断重大性。近期真实变化尚在更新期的另记时点性待更新，不覆盖重大性结论。 | M.Judgment.DifferenceCause.criteria, M.Rule.DateYearMonth.expression, M.Rule.MaterialDifference.expression, M.Rule.TimingPending.expression | MIXED | 由关系日期年月比较、差异重大性判断、时点性待更新标记、差异原因和更正后复核共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成重大或非重大差异判断及依据；近期待更新作为独立跟踪标记保留。 | M.Difference.affects_ubo, M.Difference.cause, M.Difference.customer_corrected, M.Difference.material, M.Difference.reason, M.Difference.recheck_consistent, M.Difference.timing_pending, M.Difference.year_month_mismatch | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 年月差异是独立的重大分支，不要求同时改变人员认定；30日更新期限不是日期容差或重大性豁免。 | M.Judgment.DifferenceCause.criteria, M.Rule.DateYearMonth.expression, M.Rule.MaterialDifference.expression, M.Rule.TimingPending.expression | FORMALIZED | 年月差异是独立的重大分支，不要求同时改变人员认定；30日更新期限不是日期容差或重大性豁免。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 先补齐人员对应、日期年月和权利变化证据；两个判断维度分别检查，不仅比较相差天数。 | M.Judgment.DifferenceCause.on_missing, M.Rule.DateYearMonth.on_unknown, M.Rule.MaterialDifference.on_unknown, M.Rule.TimingPending.on_unknown | FORMALIZED | 先补齐人员对应、日期年月和权利变化证据；两个判断维度分别检查，不仅比较相差天数。 缺证不得用默认值补足。 |
| 时间要求 | 按所引制度文件的生效和过渡条款；业务建议在确认后自确认版本生效。 | M.Difference.actual_change_date, M.Difference.as_of, M.Difference.filing_date, M.Difference.institution_date, M.Difference.update_due | FORMALIZED | 按所引制度文件的生效和过渡条款；业务建议在确认后自确认版本生效。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.19

状态：PARTIAL；问题：K.Q.19；缺口：M.Gap.02, M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 查询核对发现差异或应备案未备案的客户。 | M.Process.G6.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已取得差异明细、机构识别证据、客户说明和备案状态。 | M.Difference.cause, M.Difference.correction_evidence, M.Difference.customer_corrected, M.Difference.filing_value, M.Difference.institution_value, M.Difference.material, M.Difference.recheck_consistent, M.Difference.recheck_evidence | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 先沟通核实成因：机构识别有误则更正；备案有误且重大则按规定报告；非重大则记录和提示。客户实际更正后重新查询复核，结果一致才按用户口径关闭业务差异。 | M.Judgment.DifferenceCause.criteria, M.Rule.CloseDifference.expression, M.Rule.CorrectionAction.expression, M.Rule.ReportRequired.expression, M.Transition.DifferenceCorrected.guard, M.Transition.DifferenceInvestigate.guard, M.Transition.DifferenceResolve.guard | MIXED | 由差异报告义务判断、按原因采取差异处置、实际更正且复核一致后闭环、差异原因和更正后复核、差异实质处置共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成更正、报告或记录提示的处置链，分别保留系统报告结果和差异实质闭环证据。 | M.Difference.affects_ubo, M.Difference.cause, M.Difference.closure_allowed, M.Difference.correction_action, M.Difference.customer_corrected, M.Difference.reason, M.Difference.recheck_consistent, M.Difference.report_required, M.Difference.state | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 重大差异在风险可控时可以建立或维持关系；应报可疑交易报告的独立办理，不能以差异报告替代；接口反馈成功不自动闭环。 | M.Judgment.DifferenceCause.criteria, M.Rule.CloseDifference.expression, M.Rule.CorrectionAction.expression, M.Rule.ReportRequired.expression, M.Transition.DifferenceCorrected.guard, M.Transition.DifferenceInvestigate.guard, M.Transition.DifferenceResolve.guard | FORMALIZED | 重大差异在风险可控时可以建立或维持关系；应报可疑交易报告的独立办理，不能以差异报告替代；接口反馈成功不自动闭环。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 客户口头承诺或已提交更新但系统未复核一致时，不得标记已解决。 | M.Judgment.DifferenceCause.on_missing, M.Rule.CloseDifference.on_unknown, M.Rule.CorrectionAction.on_unknown, M.Rule.ReportRequired.on_unknown, M.Transition.DifferenceCorrected.guard, M.Transition.DifferenceInvestigate.guard, M.Transition.DifferenceResolve.guard | FORMALIZED | 客户口头承诺或已提交更新但系统未复核一致时，不得标记已解决。 缺证不得用默认值补足。 |
| 时间要求 | 按所引制度文件的生效和过渡条款；业务建议在确认后自确认版本生效。 | M.Process.G6.trigger | FORMALIZED | 按所引制度文件的生效和过渡条款；业务建议在确认后自确认版本生效。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.20

状态：PARTIAL；问题：K.Q.20；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.RETENTION, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 备案、查询、识别核实和后续使用中的受益所有人信息。 | M.Process.G7.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 确认查询者身份、法定职责或反洗钱目的、权限、代报关系和接收方。 | M.Access.institution_authorized, M.Access.lawful_purpose, M.Access.operator_authorized, M.Access.purpose, M.Identification.evidence, M.Identification.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 仅在合法目的和权限内查询使用；按查询声明返回加密非掩码或掩码信息；传输采用认证、加密、签名验签并对所得信息保密。 | M.Judgment.Authority.criteria, M.Rule.Access.expression | MIXED | 由查询用途及授权、主体分类、用途授权和责任适用核查共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成用途、权限、访问、传输和后续使用可追溯的保密链。 | M.Access.allowed, M.Access.institution_authorized, M.Access.lawful_purpose, M.Access.operator_authorized, M.Identification.category_verified | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 技术成功不扩大法定用途；公开来源也不解除对识别核实过程中信息的保密义务。 | M.Judgment.Authority.criteria, M.Rule.Access.expression | FORMALIZED | 技术成功不扩大法定用途；公开来源也不解除对识别核实过程中信息的保密义务。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 用途、权限或接收方不明时拒绝查询披露；10年保存期限及起算在本次来源中证据不足。 | M.Judgment.Authority.on_missing, M.Rule.Access.on_unknown | FORMALIZED | 用途、权限或接收方不明时拒绝查询披露；10年保存期限及起算在本次来源中证据不足。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01；12号令自2026-01-20；BOMIS接口规范版本2026-03。 | M.Process.G7.trigger | FORMALIZED | 3号令自2024-11-01；12号令自2026-01-20；BOMIS接口规范版本2026-03。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.21

状态：PARTIAL；问题：K.Q.21；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.PENALTY_BASIS, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 备案主体与金融机构在制度生效、过渡及履职期间的行为。 | M.Process.G7.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 确定行为发生时间、义务主体、具体义务、违法事实和履职记录。 | M.Access.purpose, M.ComplianceReview.as_of, M.ComplianceReview.duty_kind, M.ComplianceReview.evidence, M.Identification.evidence, M.Identification.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 先按生效和过渡条款选版本，再把事实映射到备案、一般识别、严重识别、风险管理、差异反馈或内控缺陷责任，并单独考虑从轻减轻因素。 | M.Judgment.Authority.criteria, M.Judgment.Liability.criteria, M.Rule.Regime.expression | MIXED | 由按时点选择制度、主体分类、用途授权和责任适用核查、责任类型及从轻减轻因素核查共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成适用版本、整改要求、责任类型和法务复核材料。 | M.Access.institution_authorized, M.Access.lawful_purpose, M.Access.operator_authorized, M.ComplianceReview.applicable_regime, M.ComplianceReview.legal_sources_complete, M.ComplianceReview.mitigation, M.ComplianceReview.rectification, M.ComplianceReview.violation_type, M.Identification.category_verified | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 从轻减轻因素不免除基础义务；处罚决定还依被引用法律和行政法规。 | M.Judgment.Authority.criteria, M.Judgment.Liability.criteria, M.Rule.Regime.expression | FORMALIZED | 从轻减轻因素不免除基础义务；处罚决定还依被引用法律和行政法规。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 被引用反洗钱法及企业登记行政法规全文未在7份输入中，具体处罚适用保留法务核验。 | M.Judgment.Authority.on_missing, M.Judgment.Liability.on_missing, M.Rule.Regime.on_unknown | FORMALIZED | 被引用反洗钱法及企业登记行政法规全文未在7份输入中，具体处罚适用保留法务核验。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01；12号令自2026-01-20。 | M.ComplianceReview.as_of | FORMALIZED | 3号令自2024-11-01；12号令自2026-01-20。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.22

状态：PARTIAL；问题：K.Q.22；缺口：M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 依据本地北京、深圳备案指引开展对应地区办理。 | M.Process.G8.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 确定地区、主体类别、办理事项、登录身份及已核实人员资料。 | M.Filing.all_people_recorded, M.Filing.all_relations_recorded, M.Filing.evidence, M.Filing.method, M.Filing.subject, M.Filing.submission_checked, M.Identification.local_routing | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 准备资料→选择所在地入口→按主体分类和真实条件选填报方式→录入全部人员/关系→检查并确认提交→保存结果。 | M.Judgment.FilingRoute.criteria, M.Rule.FilingSubmit.expression | MIXED | 由备案资料和人员关系完整后提交、地方办理方式和入口核对共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成对应事项的备案办理记录；资料变更继续按法定期限更新。 | M.Filing.can_submit, M.Identification.local_routing | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 国企备案勾选不替代金融机构风险门控；地方页面完成不证明银行已尽调。 | M.Judgment.FilingRoute.criteria, M.Rule.FilingSubmit.expression | FORMALIZED | 国企备案勾选不替代金融机构风险门控；地方页面完成不证明银行已尽调。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 无账号资格、关系依据或办理回执时注明具体待补项；界面已变化应核对当前官方办理指引。 | M.Judgment.FilingRoute.on_missing, M.Rule.FilingSubmit.on_unknown | FORMALIZED | 无账号资格、关系依据或办理回执时注明具体待补项；界面已变化应核对当前官方办理指引。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G8.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.23

状态：PARTIAL；问题：K.Q.23；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.RETENTION

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 使用BOMIS进行核验与查询的义务机构。 | M.Process.G9.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 具备机构身份、主体标识、识别资料及必要核验流水。 | M.Access.allowed, M.Query.batch, M.Query.business_feedback_success, M.Query.daily_used_before, M.Query.feedback_matched, M.Query.feedback_received, M.Query.parameters_current, M.Query.per_subject_complete, M.Query.quota, M.Query.request_reference, M.Query.response_reference, M.Query.subject_count | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 区分核验、当前查询、历史查询；核对参数与额度；关联请求和异步反馈；逐主体检查结果。 | M.Rule.QueryAllowed.expression, M.Rule.QueryMatch.expression, M.Rule.QueryUsable.expression, M.Transition.QueryFail.guard, M.Transition.QueryIncomplete.guard, M.Transition.QueryReceive.guard, M.Transition.QuerySend.guard | FORMALIZED | 由核验报文允许发送、反馈关联原请求、逐主体业务结果可用、查询异步反馈共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 取得相应系统信息以支持机构独立核实及差异分析。 | M.Query.feedback_matched, M.Query.query_allowed, M.Query.result_usable, M.Query.state | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 历史系统信息不替代法律关系生效证据。 | M.Rule.QueryAllowed.expression, M.Rule.QueryMatch.expression, M.Rule.QueryUsable.expression, M.Transition.QueryFail.guard, M.Transition.QueryIncomplete.guard, M.Transition.QueryReceive.guard, M.Transition.QuerySend.guard | FORMALIZED | 历史系统信息不替代法律关系生效证据。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 超额、过期、校验失败或反馈未到时保留待完成；不伪造空结果。 | M.Rule.QueryAllowed.on_unknown, M.Rule.QueryMatch.on_unknown, M.Rule.QueryUsable.on_unknown, M.Transition.QueryFail.guard, M.Transition.QueryIncomplete.guard, M.Transition.QueryReceive.guard, M.Transition.QuerySend.guard | FORMALIZED | 超额、过期、校验失败或反馈未到时保留待完成；不伪造空结果。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G9.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.24

状态：PARTIAL；问题：K.Q.24；缺口：M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | BOMIS报告及配套办理。 | M.Process.G9.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 明确业务结论、主体、报告、文件与请求身份，核对最新可用事实和参数。 | M.DifferenceReport.analysis_present, M.DifferenceReport.attachments_usable, M.DifferenceReport.new_person_name_present, M.DifferenceReport.new_person_present, M.DifferenceReport.nonmajor_policy_confirmed, M.DifferenceReport.old_person_present, M.DifferenceReport.operation, M.DifferenceReport.organization_change, M.DifferenceReport.person_change, M.DifferenceReport.promise_or_state_condition, M.DifferenceReport.required_content_complete, M.DifferenceReport.subject_code_present, M.DifferenceReport.subject_in_system, M.DifferenceReport.subtype, M.DifferenceReport.support_present, M.DifferenceReport.system_people_empty, M.DifferenceReport.type_supported, M.DifferenceReport.verification_consistent | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 报告类型选择→文件关联→提交→分别处理补充、审批、撤销和终止→需要时申请案例→保存回执与处置。 | M.Rule.ReportContent.expression, M.Rule.ReportSubmit.expression, M.Transition.ReportDone.guard, M.Transition.ReportProcessing.guard, M.Transition.ReportSubmit.guard, M.Transition.ReportSupplement.guard, M.Transition.ReportTerminate.guard, M.Transition.ReportWithdrawFeedback.guard, M.Transition.ReportWithdrawRequest.guard | FORMALIZED | 由按报告类别检查内容和操作、差异报告提交前提、差异报告办理共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 获得对应系统业务状态及下一步任务，而非统一的“成功”。 | M.DifferenceReport.required_content_complete, M.DifferenceReport.state, M.DifferenceReport.submit_allowed | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 法定报告、可疑交易报告与系统报备功能各有条件。 | M.Rule.ReportContent.expression, M.Rule.ReportSubmit.expression, M.Transition.ReportDone.guard, M.Transition.ReportProcessing.guard, M.Transition.ReportSubmit.guard, M.Transition.ReportSupplement.guard, M.Transition.ReportTerminate.guard, M.Transition.ReportWithdrawFeedback.guard, M.Transition.ReportWithdrawRequest.guard | FORMALIZED | 法定报告、可疑交易报告与系统报备功能各有条件。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 缺事实、回执、参数或附件时保留具体缺口，不强行闭环。 | M.Rule.ReportContent.on_unknown, M.Rule.ReportSubmit.on_unknown, M.Transition.ReportDone.guard, M.Transition.ReportProcessing.guard, M.Transition.ReportSubmit.guard, M.Transition.ReportSupplement.guard, M.Transition.ReportTerminate.guard, M.Transition.ReportWithdrawFeedback.guard, M.Transition.ReportWithdrawRequest.guard | FORMALIZED | 缺事实、回执、参数或附件时保留具体缺口，不强行闭环。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G9.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.07.NATURE

状态：PARTIAL；问题：K.Q.07, K.Q.07.NATURE；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.CURRENT_TARGET_RISK

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 国有企业何时可进入法定代表人简化识别？ | M.Process.G2.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 先固定主体、核对时点及所述事实的证据；区分制度原文与明确的用户业务口径。 | M.StateNature.actual_dominance, M.StateNature.article4_4, M.StateNature.evidence, M.StateNature.largest_shareholder, M.StateNature.qualified_investor, M.StateNature.state_investor, M.StateNature.state_ratio, M.StateNature.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 第四条第（四）项的主体资格、未超过50%、第一大股东、实际支配安排同时具备；其中实际支配须以协议、章程、决议等具体内容支持。 | M.Judgment.StateNature.criteria, M.Rule.Article44.expression, M.Rule.RelativeHolding.expression | MIXED | 由第四条第四项性质条件、衔接国有相对控股口径、国有性质与实际支配证据判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成有证据的企业性质判断，供下一步判断国有控股适用范围使用。 | M.StateNature.actual_dominance, M.StateNature.article4_4, M.StateNature.largest_shareholder, M.StateNature.nature, M.StateNature.officially_verified, M.StateNature.qualified_investor, M.StateNature.relative_holding | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 超过50%的结构应另核对第（二）、（三）项；国资参股但不能实际支配，不凭名称认定实际控制。 | M.Judgment.StateNature.criteria, M.Rule.Article44.expression, M.Rule.RelativeHolding.expression | FORMALIZED | 超过50%的结构应另核对第（二）、（三）项；国资参股但不能实际支配，不凭名称认定实际控制。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 补件可来自国资监管名单/公示、产权登记/工商档案、官方公示及其他正式文件（集团出资证明、红头文件、审计报告等）。逐件核对主体、时点、证明事项和可靠性；补件能证明第一大股东及实际支配后才完成性质认定。仅有名录或标签仍待核实，补件不是独立替代路径。 | M.Judgment.StateNature.on_missing, M.Rule.Article44.on_unknown, M.Rule.RelativeHolding.on_unknown | FORMALIZED | 补件可来自国资监管名单/公示、产权登记/工商档案、官方公示及其他正式文件（集团出资证明、红头文件、审计报告等）。逐件核对主体、时点、证明事项和可靠性；补件能证明第一大股东及实际支配后才完成性质认定。仅有名录或标签仍待核实，补件不是独立替代路径。 缺证不得用默认值补足。 |
| 时间要求 | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 | M.Process.G2.trigger | FORMALIZED | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.07.APPLY

状态：PARTIAL；问题：K.Q.07, K.Q.07.APPLY；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.CURRENT_TARGET_RISK

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 国有企业何时可进入法定代表人简化识别？ | M.Process.G2.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 先固定主体、核对时点及所述事实的证据；区分制度原文与明确的用户业务口径。 | M.StateNature.article4_4, M.StateNature.evidence, M.StateNature.nature, M.StateNature.officially_verified, M.StateNature.relative_holding, M.StateNature.state_investor, M.StateNature.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 先确认性质，再按所处备案或金融机构业务判断适用条款；金融机构分支还必须进入风险判断。 | M.Judgment.StateNature.criteria, M.Rule.RelativeHolding.expression, M.Rule.StateApplicability.expression | MIXED | 由衔接国有相对控股口径、金融机构国企简化主体范围、国有性质与实际支配证据判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 输出适用的备案或识别分支，不直接完成简化识别。 | M.StateNature.actual_dominance, M.StateNature.cdd_branch_applicable, M.StateNature.largest_shareholder, M.StateNature.nature, M.StateNature.officially_verified, M.StateNature.qualified_investor, M.StateNature.relative_holding | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 国有参股公司只可按相应条款不再识别国有资本部分；不能因此对全部公司按法定代表人简化。 | M.Judgment.StateNature.criteria, M.Rule.RelativeHolding.expression, M.Rule.StateApplicability.expression | FORMALIZED | 国有参股公司只可按相应条款不再识别国有资本部分；不能因此对全部公司按法定代表人简化。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 性质或适用业务关系不清时，不进入简化分支。 | M.Judgment.StateNature.on_missing, M.Rule.RelativeHolding.on_unknown, M.Rule.StateApplicability.on_unknown | FORMALIZED | 性质或适用业务关系不清时，不进入简化分支。 缺证不得用默认值补足。 |
| 时间要求 | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 | M.Process.G2.trigger | FORMALIZED | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.07.RISK

状态：PARTIAL；问题：K.Q.07, K.Q.07.RISK；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.CURRENT_TARGET_RISK

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 国有企业何时可进入法定代表人简化识别？ | M.Process.G2.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 先固定主体、核对时点及所述事实的证据；区分制度原文与明确的用户业务口径。 | M.Identification.data_doubt, M.Identification.enhanced_reasons, M.Identification.evidence, M.Identification.matched_risk_measure, M.Identification.risk20_triggered, M.Identification.risk_assessment_complete, M.StateNature.cdd_branch_applicable | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 性质与条款适用成立后再充分评估风险；遇第二十条适用情形，依据具体风险采取加强措施。 | M.Judgment.Risk.criteria, M.Rule.StateSimplification.expression | MIXED | 由国企简化风险门控、风险及措施匹配判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 记录是否可以使用所选简化措施及其理由；风险证据未澄清时不自动简化。 | M.Identification.data_doubt, M.Identification.enhanced_measures, M.Identification.higher_risk, M.Identification.matched_risk_measure, M.Identification.risk20_triggered, M.Identification.risk_assessment_complete, M.Identification.simplification_allowed | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 具体加强措施仍须依第二十一条等对应范围核对，本样章不把若干风险例子当作穷尽清单。 现行操作（2026-09-15用户答复）：一般直接简化；遇复杂/境外结构、资料可靠性存疑或人员异常频繁变更会停下来核实。该现状不替代12号令制度要求，差异由合规责任人裁定。 | M.Judgment.Risk.criteria, M.Rule.StateSimplification.expression | FORMALIZED | 具体加强措施仍须依第二十一条等对应范围核对，本样章不把若干风险例子当作穷尽清单。 现行操作（2026-09-15用户答复）：一般直接简化；遇复杂/境外结构、资料可靠性存疑或人员异常频繁变更会停下来核实。该现状不替代12号令制度要求，差异由合规责任人裁定。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 风险资料缺失或真实性存疑时补查，不能以未发现风险等同已完成风险评估。 | M.Judgment.Risk.on_missing, M.Rule.StateSimplification.on_unknown | FORMALIZED | 风险资料缺失或真实性存疑时补查，不能以未发现风险等同已完成风险评估。 缺证不得用默认值补足。 |
| 时间要求 | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 | M.Process.G2.trigger | FORMALIZED | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.11.START

状态：PARTIAL；问题：K.Q.11, K.Q.11.START；缺口：M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 受益所有权关系形成和终止日期如何确定？ | M.Process.G4.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 先固定主体、核对时点及所述事实的证据；区分制度原文与明确的用户业务口径。 | M.PersonAssessment.basis_evidence | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 核对章程、协议、决议等文件的生效约定及所需条件，并判断该关系在何时满足识别标准。 | M.Judgment.EffectiveDate.criteria | MANUAL | 由法律关系实际生效日期判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成有证据支持的形成日期，或明确因缺证暂不能确定。 | M.PersonAssessment.date_reason, M.PersonAssessment.legal_start | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 文件生效日期只是应结合实质判断的依据；不能在附条件尚未满足时直接取签署日。 | M.Judgment.EffectiveDate.criteria | FORMALIZED | 文件生效日期只是应结合实质判断的依据；不能在附条件尚未满足时直接取签署日。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 分别检查并补充：生效条件何时满足的记录；协议/章程是否明确生效约定；历史权益变化是否留痕；控制协议生效时间证据。缺失哪类就标明哪类，不能用签署日、备案日或录入日自动填充。 | M.Judgment.EffectiveDate.on_missing | FORMALIZED | 分别检查并补充：生效条件何时满足的记录；协议/章程是否明确生效约定；历史权益变化是否留痕；控制协议生效时间证据。缺失哪类就标明哪类，不能用签署日、备案日或录入日自动填充。 缺证不得用默认值补足。 |
| 时间要求 | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 | M.PersonAssessment.legal_start | FORMALIZED | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.11.HISTORY

状态：PARTIAL；问题：K.Q.11, K.Q.11.HISTORY；缺口：M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 受益所有权关系形成和终止日期如何确定？ | M.Process.G4.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 先固定主体、核对时点及所述事实的证据；区分制度原文与明确的用户业务口径。 | M.Identification.subject, M.PersonAssessment.as_of, M.PersonAssessment.basis_evidence, M.PersonAssessment.continuity_verified, M.PersonAssessment.history, M.PersonAssessment.history_complete, M.PersonAssessment.person | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 按已生效的关系变化重建达标与不达标区间，取当前连续达标区间的起点，并展示之前中断。 | M.Constraint.BeneficialOwnershipInterval.expression, M.Judgment.Continuity.criteria, M.Rule.Formation.expression | MIXED | 由当前总体形成日期、历史完整性和总体资格连续判断、已知终止须晚于开始，未知终止不得冒充持续共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 当前日期反映最近重新达标，回访可以解释为何不同于历史最早形成日期。 | M.PersonAssessment.continuity_verified, M.PersonAssessment.date_reason, M.PersonAssessment.formation_date, M.PersonAssessment.history_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 用户已答：权利类型切换但整体资格连续时，总体形成日期不重置，各关系类型分别留存事件日期。若整体资格实际中断，则重新达标按最新连续区间开始日期记录。连续性和生效日期仍须证据支持。 | M.Constraint.BeneficialOwnershipInterval.expression, M.Judgment.Continuity.criteria, M.Rule.Formation.expression | FORMALIZED | 用户已答：权利类型切换但整体资格连续时，总体形成日期不重置，各关系类型分别留存事件日期。若整体资格实际中断，则重新达标按最新连续区间开始日期记录。连续性和生效日期仍须证据支持。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 缺历史权益变化记录时无法证明中断及持续区间；缺控制协议生效日期或附条件生效记录时无法证明跨类型无缝接续，先补相应证据，不以未知视为中断。 | M.Constraint.BeneficialOwnershipInterval.on_unknown, M.Judgment.Continuity.on_missing, M.Rule.Formation.on_unknown | FORMALIZED | 缺历史权益变化记录时无法证明中断及持续区间；缺控制协议生效日期或附条件生效记录时无法证明跨类型无缝接续，先补相应证据，不以未知视为中断。 缺证不得用默认值补足。 |
| 时间要求 | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 | M.PersonAssessment.as_of, M.PersonAssessment.formation_date | FORMALIZED | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.18.DATES

状态：PARTIAL；问题：K.Q.18, K.Q.18.DATES；缺口：M.Gap.02, M.Gap.SEMANTIC_REVIEW, M.Gap.INTERFACE_REPORT_DUTY

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 差异如何区分重大、非重大和时点性待更新？ | M.Process.G6.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 先固定主体、核对时点及所述事实的证据；区分制度原文与明确的用户业务口径。 | M.Difference.affects_ubo, M.Difference.filing_date, M.Difference.institution_date, M.Difference.key_rights_mismatch, M.Difference.other_major_branch, M.Difference.people_mismatch, M.Difference.year_month_mismatch | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 分别核对人员匹配、关键身份信息、权利类型、形成终止年月及其他实质影响；列明的重大情形成立即进入相应分支。 | M.Rule.DateYearMonth.expression, M.Rule.MaterialDifference.expression | FORMALIZED | 由关系日期年月比较、差异重大性判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成有原文依据的重大或非重大判断，保留比对事实和理由。 | M.Difference.material, M.Difference.year_month_mismatch | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 同月日差且不影响识别、也不存在其他重大情形时，可按其他非实质差异讨论非重大；不能把这一结论推广到年月差异。 | M.Rule.DateYearMonth.expression, M.Rule.MaterialDifference.expression | FORMALIZED | 同月日差且不影响识别、也不存在其他重大情形时，可按其他非实质差异讨论非重大；不能把这一结论推广到年月差异。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 无法判断影响或两边日期缺证时，先核实，不能默认非重大。 | M.Rule.DateYearMonth.on_unknown, M.Rule.MaterialDifference.on_unknown | FORMALIZED | 无法判断影响或两边日期缺证时，先核实，不能默认非重大。 缺证不得用默认值补足。 |
| 时间要求 | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 | M.Difference.filing_date, M.Difference.institution_date | FORMALIZED | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.18.PENDING

状态：PARTIAL；问题：K.Q.18, K.Q.18.PENDING；缺口：M.Gap.02, M.Gap.SEMANTIC_REVIEW, M.Gap.INTERFACE_REPORT_DUTY

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 差异如何区分重大、非重大和时点性待更新？ | M.Process.G6.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 先固定主体、核对时点及所述事实的证据；区分制度原文与明确的用户业务口径。 | M.Difference.actual_change_date, M.Difference.as_of, M.Difference.customer_corrected, M.Difference.update_due | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 确认真实变更时点及适用更新期限，再检查差异成因与重大性，并登记后续复核。 | M.Rule.TimingPending.expression, M.Rule.UpdateDue.expression | FORMALIZED | 由近期变化的法定更新截止、时点性待更新标记共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 记录时点性待更新及相应跟踪事项，保留重大性和报告义务的独立判断。 | M.Difference.timing_pending, M.Difference.update_due | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 差异报告或非重大记录的30个工作日，分别按12号令要求计算，不能被备案的30日替代或自动顺延。 | M.Rule.TimingPending.expression, M.Rule.UpdateDue.expression | FORMALIZED | 差异报告或非重大记录的30个工作日，分别按12号令要求计算，不能被备案的30日替代或自动顺延。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 缺实际变更日期或更新证据时不臆算到期日；复核责任和超期升级方式仍待业务补充。 | M.Rule.TimingPending.on_unknown, M.Rule.UpdateDue.on_unknown | FORMALIZED | 缺实际变更日期或更新证据时不臆算到期日；复核责任和超期升级方式仍待业务补充。 缺证不得用默认值补足。 |
| 时间要求 | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 | M.Difference.actual_change_date, M.Difference.as_of, M.Difference.update_due | FORMALIZED | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.19.CORRECT

状态：PARTIAL；问题：K.Q.19, K.Q.19.CORRECT；缺口：M.Gap.02, M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 发现差异后如何沟通、报告和闭环？ | M.Process.G6.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 先固定主体、核对时点及所述事实的证据；区分制度原文与明确的用户业务口径。 | M.Difference.cause, M.Difference.correction_evidence, M.Difference.filing_value, M.Difference.institution_value, M.Difference.material, M.Difference.recheck_evidence | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 自身识别不准确则更正本机构信息；合理判断备案不准确且差异重大则按规定期限报告并留存理由、过程和佐证；非重大按规定记录并提示客户。 | M.Judgment.DifferenceCause.criteria, M.Rule.CorrectionAction.expression, M.Rule.ReportRequired.expression | MIXED | 由差异报告义务判断、按原因采取差异处置、差异原因和更正后复核共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 选择有成因依据的更正、报告或记录提示分支。 | M.Difference.affects_ubo, M.Difference.cause, M.Difference.correction_action, M.Difference.customer_corrected, M.Difference.reason, M.Difference.recheck_consistent, M.Difference.report_required | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 是否建立或维持业务关系还须单独判断风险可控，不能仅因有报告义务就自动决定业务关系。 | M.Judgment.DifferenceCause.criteria, M.Rule.CorrectionAction.expression, M.Rule.ReportRequired.expression | FORMALIZED | 是否建立或维持业务关系还须单独判断风险可控，不能仅因有报告义务就自动决定业务关系。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 成因或重大性尚不清楚时继续核实，不能伪造确定的报告理由。 | M.Judgment.DifferenceCause.on_missing, M.Rule.CorrectionAction.on_unknown, M.Rule.ReportRequired.on_unknown | FORMALIZED | 成因或重大性尚不清楚时继续核实，不能伪造确定的报告理由。 缺证不得用默认值补足。 |
| 时间要求 | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 | M.Process.G6.trigger | FORMALIZED | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.19.CLOSE

状态：PARTIAL；问题：K.Q.19, K.Q.19.CLOSE；缺口：M.Gap.02, M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 发现差异后如何沟通、报告和闭环？ | M.Process.G6.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 先固定主体、核对时点及所述事实的证据；区分制度原文与明确的用户业务口径。 | M.Difference.correction_evidence, M.Difference.customer_corrected, M.Difference.filing_value, M.Difference.institution_value, M.Difference.recheck_consistent, M.Difference.recheck_evidence | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 记录实际更正及重新查询比对结果，两项均成立后将该差异标记为已解决。 | M.Judgment.DifferenceCause.criteria, M.Rule.CloseDifference.expression, M.Transition.DifferenceCorrected.guard, M.Transition.DifferenceInvestigate.guard, M.Transition.DifferenceResolve.guard | MIXED | 由实际更正且复核一致后闭环、差异原因和更正后复核、差异实质处置共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 差异状态闭环，并保留更正、复核及历史处置证据。 | M.Difference.affects_ubo, M.Difference.cause, M.Difference.closure_allowed, M.Difference.customer_corrected, M.Difference.reason, M.Difference.recheck_consistent, M.Difference.state | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | “已解决”是用户明确的处置口径，不等于制度中所有既有报告或留存义务自动消失。 | M.Judgment.DifferenceCause.criteria, M.Rule.CloseDifference.expression, M.Transition.DifferenceCorrected.guard, M.Transition.DifferenceInvestigate.guard, M.Transition.DifferenceResolve.guard | FORMALIZED | “已解决”是用户明确的处置口径，不等于制度中所有既有报告或留存义务自动消失。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 未重新查询、人员或关系仍不一致时，保留待核实或待处理。 | M.Judgment.DifferenceCause.on_missing, M.Rule.CloseDifference.on_unknown, M.Transition.DifferenceCorrected.guard, M.Transition.DifferenceInvestigate.guard, M.Transition.DifferenceResolve.guard | FORMALIZED | 未重新查询、人员或关系仍不一致时，保留待核实或待处理。 缺证不得用默认值补足。 |
| 时间要求 | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 | M.Process.G6.trigger | FORMALIZED | 适用所引文件及具体业务时点；用户口径不改变原制度生效时间。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.09.TYPE

状态：PARTIAL；问题：K.Q.09；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.AM_MANAGER

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 财富管理服务、公益慈善、其他资产服务、民事及外国信托的识别程度。 | M.Process.G3.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 确定信托法律与业务类型、所有权控制结构复杂度以及洗钱和恐怖融资风险。 | M.Identification.data_doubt, M.Identification.risk20_triggered, M.ProductAssessment.evidence, M.ProductAssessment.low_risk, M.ProductAssessment.manager, M.ProductAssessment.product, M.ProductAssessment.risk_assessment_complete, M.ProductAssessment.simple_structure, M.ProductAssessment.trust_parties, M.Subject.trust_kind | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 财富管理服务、公益慈善、民事和外国信托按第十二条完整识别；其他资产服务信托仅在结构简单且风险较低时可简化。 | M.Judgment.Products.criteria, M.Rule.TrustSimplification.expression | MIXED | 由信托类型和风险分支、信托与资管条件及受托机构履职判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 输出完整识别或简化识别路径，并留存类型和风险理由。 | M.ProductAssessment.doubts, M.ProductAssessment.low_risk, M.ProductAssessment.manager_duties_effective, M.ProductAssessment.manager_people_identified, M.ProductAssessment.manager_system_sound, M.ProductAssessment.risk_assessment_complete, M.ProductAssessment.simple_structure, M.ProductAssessment.simplify_allowed, M.ProductAssessment.trust_lookthrough_complete, M.ProductAssessment.trust_party_scope_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 专业服务人员基本信息留存义务不等于把其识别为受益所有人。 | M.Judgment.Products.criteria, M.Rule.TrustSimplification.expression | FORMALIZED | 专业服务人员基本信息留存义务不等于把其识别为受益所有人。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 信托类型、结构或风险不足以判断时不得简化，补充分类依据和风险评估。 | M.Judgment.Products.on_missing, M.Rule.TrustSimplification.on_unknown | FORMALIZED | 信托类型、结构或风险不足以判断时不得简化，补充分类依据和风险评估。 缺证不得用默认值补足。 |
| 时间要求 | 12号令自2026-01-20施行；本规则按2026-09-15整理。 | M.Process.G3.trigger | FORMALIZED | 12号令自2026-01-20施行；本规则按2026-09-15整理。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.09.ASSET

状态：PARTIAL；问题：K.Q.09；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.AM_MANAGER

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 资产管理信托等资产管理产品及金融机构提供托管等服务的场景。 | M.Process.G3.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 取得产品类型、合同说明书、募集发行方式、备案登记、管理人或受托人身份、份额名册、实际管理自然人和风险评估。 | M.Identification.data_doubt, M.Identification.risk20_triggered, M.ProductAssessment.evidence, M.ProductAssessment.financial_manager, M.ProductAssessment.low_risk, M.ProductAssessment.manager, M.ProductAssessment.manager_people_identified, M.ProductAssessment.product, M.ProductAssessment.public_offering, M.ProductAssessment.registered, M.ProductAssessment.risk_assessment_complete, M.ProductAssessment.service_in_scope, M.ProductAssessment.trust_parties | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 一般基于风险参照第八条；金融机构管理或受托、公开募集或发行且依法备案登记、处于托管等服务时可简化；其他产品按风险确定程度，低风险年金类产品可简化。 | M.Judgment.Products.criteria, M.Rule.AssetSimplification.expression | MIXED | 由资管产品简化条件、信托与资管条件及受托机构履职判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 输出一般识别或简化识别路径；简化时认定管理产品的自然人并记录依据、材料和理由。 | M.ProductAssessment.doubts, M.ProductAssessment.low_risk, M.ProductAssessment.manager_duties_effective, M.ProductAssessment.manager_people_identified, M.ProductAssessment.manager_system_sound, M.ProductAssessment.risk_assessment_complete, M.ProductAssessment.simple_structure, M.ProductAssessment.simplify_allowed, M.ProductAssessment.trust_lookthrough_complete, M.ProductAssessment.trust_party_scope_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 产品名称、公募宣传、管理公司法定代表人身份均不能单独证明简化前提或具体管理自然人。 | M.Judgment.Products.criteria, M.Rule.AssetSimplification.expression | FORMALIZED | 产品名称、公募宣传、管理公司法定代表人身份均不能单独证明简化前提或具体管理自然人。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 任一募集、登记、管理、风险或实际管理自然人事实缺失时不自动简化；多人治理下具体自然人选择需业务补充。 | M.Judgment.Products.on_missing, M.Rule.AssetSimplification.on_unknown | FORMALIZED | 任一募集、登记、管理、风险或实际管理自然人事实缺失时不自动简化；多人治理下具体自然人选择需业务补充。 缺证不得用默认值补足。 |
| 时间要求 | 12号令自2026-01-20施行；本规则按2026-09-15整理。 | M.Process.G3.trigger | FORMALIZED | 12号令自2026-01-20施行；本规则按2026-09-15整理。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.09.RELIANCE

状态：PARTIAL；问题：K.Q.09；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.AM_MANAGER

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 信托公司、非信托金融机构、资管管理人与其他机构合作时的信息提供和采信。 | M.Process.G3.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 取得提供方受益所有人材料、反洗钱体系与履责有效性评估，以及疑点、瑕疵、违法和风险事实。 | M.ProductAssessment.doubts, M.ProductAssessment.evidence, M.ProductAssessment.major_risk, M.ProductAssessment.manager, M.ProductAssessment.manager_duties_effective, M.ProductAssessment.manager_system_sound, M.ProductAssessment.product, M.ProductAssessment.serious_violation, M.ProductAssessment.trust_parties, M.ProductAssessment.uncooperative | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 仅在能够确信体系健全且有效履责时采信；有明显疑点或识别瑕疵要求重新识别；不配合、严重违法、重大风险或体系性缺陷时采取必要风险管理措施。 | M.Judgment.Products.criteria, M.Rule.ManagerReliance.expression | MIXED | 由是否可采信管理受托机构结果、信托与资管条件及受托机构履职判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 输出可采信、要求重识别或采取风险管理措施，并保留评估和沟通证据。 | M.ProductAssessment.doubts, M.ProductAssessment.low_risk, M.ProductAssessment.manager_duties_effective, M.ProductAssessment.manager_people_identified, M.ProductAssessment.manager_system_sound, M.ProductAssessment.reliance_allowed, M.ProductAssessment.risk_assessment_complete, M.ProductAssessment.simple_structure, M.ProductAssessment.trust_lookthrough_complete, M.ProductAssessment.trust_party_scope_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 信托公司提供材料不产生无条件采信，合作关系也不转移接收机构责任。 | M.Judgment.Products.criteria, M.Rule.ManagerReliance.expression | FORMALIZED | 信托公司提供材料不产生无条件采信，合作关系也不转移接收机构责任。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 无法评估提供方体系和材料质量时不得声称可采信，补充制度、执行证据、抽查和疑点处置记录。 | M.Judgment.Products.on_missing, M.Rule.ManagerReliance.on_unknown | FORMALIZED | 无法评估提供方体系和材料质量时不得声称可采信，补充制度、执行证据、抽查和疑点处置记录。 缺证不得用默认值补足。 |
| 时间要求 | 12号令自2026-01-20施行；本规则按2026-09-15整理。 | M.Process.G3.trigger | FORMALIZED | 12号令自2026-01-20施行；本规则按2026-09-15整理。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.10.FORMATION

状态：PARTIAL；问题：K.Q.10；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 受益所有权关系形成日期。 | M.Process.G4.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已取得导致最终拥有、实际控制或最终获益的法律文件及生效条件。 | M.PersonAssessment.basis_evidence | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 核对法律关系实际生效时间，不以发现、录入或提交时间替代。 | M.Judgment.EffectiveDate.criteria | MANUAL | 由法律关系实际生效日期判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成可审计的形成日期及其文件依据。 | M.PersonAssessment.date_reason, M.PersonAssessment.legal_start | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 文件需满足条件或批准后生效的，以实际满足生效条件的时间为准；材料未说明时不推定。 | M.Judgment.EffectiveDate.criteria | FORMALIZED | 文件需满足条件或批准后生效的，以实际满足生效条件的时间为准；材料未说明时不推定。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 缺生效条款或生效事实时登记日期不明并请求补充原始文件。 | M.Judgment.EffectiveDate.on_missing | FORMALIZED | 缺生效条款或生效事实时登记日期不明并请求补充原始文件。 缺证不得用默认值补足。 |
| 时间要求 | 备案指南第二版2026-01。 | M.PersonAssessment.legal_start | FORMALIZED | 备案指南第二版2026-01。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.14.STOP

状态：PARTIAL；问题：K.Q.14；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 采取加强措施后的剩余洗钱恐怖融资风险。 | M.Process.G5.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已实际采取与触发情形相匹配的加强措施并记录结果。 | M.Identification.enhanced_measures, M.Identification.enhanced_measures_completed, M.Identification.enhanced_reasons, M.Identification.evidence, M.Identification.residual_risk_manageable | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 仍需管理时可合理限制；只有经评估风险超出机构风险管理能力才拒绝或终止。 | M.Judgment.RemainingRisk.criteria, M.Judgment.Risk.criteria, M.Rule.RefuseOrEnd.expression | MIXED | 由加强后是否可拒绝或终止、风险及措施匹配判断、加强措施后的剩余风险判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 避免把风险触发与退出结论合并，保留风险能力判断依据。 | M.Identification.data_doubt, M.Identification.enhanced_measures, M.Identification.enhanced_measures_completed, M.Identification.higher_risk, M.Identification.matched_risk_measure, M.Identification.refuse_or_end, M.Identification.residual_risk_manageable, M.Identification.restrict_needed, M.Identification.risk20_triggered, M.Identification.risk_assessment_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 不得跳过加强措施和剩余风险评估直接一律终止。 | M.Judgment.RemainingRisk.criteria, M.Judgment.Risk.criteria, M.Rule.RefuseOrEnd.expression | FORMALIZED | 不得跳过加强措施和剩余风险评估直接一律终止。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 机构风险能力边界或措施结果缺失时不得宣称达到法定终止条件。 | M.Judgment.RemainingRisk.on_missing, M.Judgment.Risk.on_missing, M.Rule.RefuseOrEnd.on_unknown | FORMALIZED | 机构风险能力边界或措施结果缺失时不得宣称达到法定终止条件。 缺证不得用默认值补足。 |
| 时间要求 | 自2026-01-20施行。 | M.Process.G5.trigger | FORMALIZED | 自2026-01-20施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.15.STATE

状态：PARTIAL；问题：K.Q.15；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.FX_EQUIV, M.Gap.EXT.GOV.BROAD_UNITS, M.Gap.CURRENT_TARGET_RISK

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 国有独资、国有控股、全民所有制、国有参股等客户的金融机构简化识别。 | M.Process.G2.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 有官方信息或适用依据确认企业性质，并完成风险评估。 | M.Identification.data_doubt, M.Identification.matched_risk_measure, M.Identification.risk20_triggered, M.Identification.risk_assessment_complete, M.StateNature.cdd_branch_applicable, M.StateNature.evidence, M.StateNature.nature, M.StateNature.officially_verified, M.StateNature.relative_holding, M.StateNature.state_investor, M.StateNature.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 国有独资、国有控股、全民所有制等可按条文将法定代表人认定为受益所有人；国有参股仍按一般标准识别非国有部分。 | M.Judgment.StateNature.criteria, M.Rule.StateApplicability.expression, M.Rule.StateSimplification.expression | MIXED | 由金融机构国企简化主体范围、国企简化风险门控、国有性质与实际支配证据判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成有性质证据、风险门控和处理范围的简化结论。 | M.Identification.simplification_allowed, M.StateNature.actual_dominance, M.StateNature.cdd_branch_applicable, M.StateNature.largest_shareholder, M.StateNature.nature, M.StateNature.officially_verified, M.StateNature.qualified_investor | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 出现第二十条情形不得简化；单有国资股东或企业名称不足以证明性质。 | M.Judgment.StateNature.criteria, M.Rule.StateApplicability.expression, M.Rule.StateSimplification.expression | FORMALIZED | 出现第二十条情形不得简化；单有国资股东或企业名称不足以证明性质。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 缺持股、第一大股东、协议或官方性质信息时请求补证，不直接简化。 | M.Judgment.StateNature.on_missing, M.Rule.StateApplicability.on_unknown, M.Rule.StateSimplification.on_unknown | FORMALIZED | 缺持股、第一大股东、协议或官方性质信息时请求补证，不直接简化。 缺证不得用默认值补足。 |
| 时间要求 | 自2026-01-20施行。 | M.Process.G2.trigger | FORMALIZED | 自2026-01-20施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.12.FILING

状态：PARTIAL；问题：K.Q.12；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 3号令备案主体的设立、信息变化、免报条件失效和存量备案。 | M.Process.G4.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已确定设立方式、变化或失效实际发生日，以及是否为2024-11-01前登记。 | M.Filing.trigger, M.Filing.trigger_date | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 在线设立同步备案；现场设立自设立日起30日；变化或免报失效自事件日起30日；存量主体截至2025-11-01。 | M.Rule.FilingDue.expression | FORMALIZED | 由备案及更新期限共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成备案义务的准确起算和期限记录。 | M.Filing.due_date | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 30日是备案义务期限，不是日期差异容差，也不是30个工作日。 | M.Rule.FilingDue.expression | FORMALIZED | 30日是备案义务期限，不是日期差异容差，也不是30个工作日。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 无法证明事件日时请求登记、协议或条件变化材料。 | M.Rule.FilingDue.on_unknown | FORMALIZED | 无法证明事件日时请求登记、协议或条件变化材料。 缺证不得用默认值补足。 |
| 时间要求 | 自2024-11-01施行。 | M.Filing.due_date, M.Filing.trigger_date | FORMALIZED | 自2024-11-01施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.12.LEGACY_CDD

状态：PARTIAL；问题：K.Q.12；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 12号令实施前已建立关系或交易且未满足新标准的存量非自然人客户。 | M.Process.G4.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已确定存量身份、当前风险等级及账户是否长期不动或已严格限制。 | M.Followup.activated, M.Followup.higher_risk, M.Followup.inactive_or_restricted, M.Followup.legacy_customer, M.Followup.trigger_date | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 较高风险以上6个月内；全部存量2年内；符合不动或严格限制条件可延至激活或办理业务时。 | M.Rule.LegacyDeferral.expression, M.Rule.LegacyDue.expression | FORMALIZED | 由存量客户激活例外、存量客户补齐期限共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成分层补齐计划和延期触发点。 | M.Followup.deferral_allowed, M.Followup.due_date | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 延期不是永久豁免，激活或办理业务时恢复义务。 | M.Rule.LegacyDeferral.expression, M.Rule.LegacyDue.expression | FORMALIZED | 延期不是永久豁免，激活或办理业务时恢复义务。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 风险等级或限制状态不明时不得使用较长期限或延期例外。 | M.Rule.LegacyDeferral.on_unknown, M.Rule.LegacyDue.on_unknown | FORMALIZED | 风险等级或限制状态不明时不得使用较长期限或延期例外。 缺证不得用默认值补足。 |
| 时间要求 | 自2026-01-20起算。 | M.Followup.due_date, M.Followup.trigger_date | FORMALIZED | 自2026-01-20起算。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.13.IDENTIFY

状态：PARTIAL；问题：K.Q.13；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 从客户组织形式和所有权控制权结构识别候选受益所有人。 | M.Process.G5.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 取得客户信息并确定法人、合伙、分支机构、信托或资管产品类型。 | M.Identification.evidence, M.Identification.rights, M.Identification.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 使用与类型相符的章程、协议、名单、权益和管理材料解释结构到自然人，多来源相互印证。 | M.Judgment.IdentityRights.criteria | MANUAL | 由核实身份、权利及结构证据共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成候选自然人、识别路径和证据来源。 | M.Identification.identity_verified, M.Identification.records_complete, M.Identification.rights_verified, M.Identification.structure_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 低风险少取材料只在现有部分已足够识别且过程理由有记录时适用。 | M.Judgment.IdentityRights.criteria | FORMALIZED | 低风险少取材料只在现有部分已足够识别且过程理由有记录时适用。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 结构不能闭合或来源可靠性不足时停止在候选，不进入核实完成。 | M.Judgment.IdentityRights.on_missing | FORMALIZED | 结构不能闭合或来源可靠性不足时停止在候选，不进入核实完成。 缺证不得用默认值补足。 |
| 时间要求 | 自2026-01-20施行。 | M.Process.G5.trigger | FORMALIZED | 自2026-01-20施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.13.VERIFY

状态：PARTIAL；问题：K.Q.13；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 对已识别候选人的身份真实性、权利状况和备案信息进行核实。 | M.Process.G5.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 识别阶段已有候选自然人及其权利关系解释。 | M.Identification.evidence, M.Identification.filing_applicable, M.Identification.identity_verified, M.Identification.rights, M.Identification.rights_verified, M.Identification.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 身份优先用官方信息，无法时用证件及补充材料；权利以客户佐证为基础并按需多渠道验证；备案主体查询核对BOMIS。 | M.Judgment.IdentityRights.criteria, M.Rule.QueryAfterIdentification.expression | MIXED | 由备案主体查询核对前提、核实身份、权利及结构证据共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成身份、权利及备案核对相互区分的核实记录。 | M.Identification.identity_verified, M.Identification.records_complete, M.Identification.refresh_query_required, M.Identification.rights_verified, M.Identification.structure_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 确属低风险可直接采信客户权利状况信息，但不解除身份核实和必要查询核对。 | M.Judgment.IdentityRights.criteria, M.Rule.QueryAfterIdentification.expression | FORMALIZED | 确属低风险可直接采信客户权利状况信息，但不解除身份核实和必要查询核对。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 任何一层缺证均指出未完成部分，不用BOMIS一致替代全部核实。 | M.Judgment.IdentityRights.on_missing, M.Rule.QueryAfterIdentification.on_unknown | FORMALIZED | 任何一层缺证均指出未完成部分，不用BOMIS一致替代全部核实。 缺证不得用默认值补足。 |
| 时间要求 | 自2026-01-20施行。 | M.Process.G5.trigger | FORMALIZED | 自2026-01-20施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.15.EXEMPT

状态：PARTIAL；问题：K.Q.15；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.FX_EQUIV, M.Gap.EXT.GOV.BROAD_UNITS, M.Gap.CURRENT_TARGET_RISK

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 12号令第十条列明的金融机构免识别主体。 | M.Process.G5.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 可靠确认客户属于条文列明的具体主体类别且未出现第二十条阻断情形。 | M.Access.purpose, M.Identification.category_verified, M.Identification.data_doubt, M.Identification.enhanced_reasons, M.Identification.evidence, M.Identification.exemption_category, M.Identification.risk20_triggered, M.Identification.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 按封闭清单逐项核对，不从相似名称或备案状态扩张。 | M.Judgment.Authority.criteria, M.Judgment.Risk.criteria, M.Rule.CddExemption.expression | MIXED | 由列明主体免识别条件、风险及措施匹配判断、主体分类、用途授权和责任适用核查共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 可免于识别受益所有人并保存主体性质依据。 | M.Access.institution_authorized, M.Access.lawful_purpose, M.Access.operator_authorized, M.Identification.category_verified, M.Identification.data_doubt, M.Identification.enhanced_measures, M.Identification.exemption_allowed, M.Identification.higher_risk, M.Identification.matched_risk_measure, M.Identification.risk20_triggered, M.Identification.risk_assessment_complete | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 无法准确判断或出现第二十条情形时不得豁免。 | M.Judgment.Authority.criteria, M.Judgment.Risk.criteria, M.Rule.CddExemption.expression | FORMALIZED | 无法准确判断或出现第二十条情形时不得豁免。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 主体资格证据不足即按一般识别。 | M.Judgment.Authority.on_missing, M.Judgment.Risk.on_missing, M.Rule.CddExemption.on_unknown | FORMALIZED | 主体资格证据不足即按一般识别。 缺证不得用默认值补足。 |
| 时间要求 | 自2026-01-20施行。 | M.Process.G5.trigger | FORMALIZED | 自2026-01-20施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.15.SIMPLIFY

状态：PARTIAL；问题：K.Q.15；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.FX_EQUIV, M.Gap.EXT.GOV.BROAD_UNITS, M.Gap.CURRENT_TARGET_RISK

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 12号令第十一、十三、十四条的主体和产品简化分支。 | M.Process.G5.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 准确确认主体或产品类型，并完成条文要求的风险和结构评估。 | M.Access.purpose, M.Identification.category_verified, M.Identification.data_doubt, M.Identification.enhanced_reasons, M.Identification.evidence, M.Identification.higher_risk, M.Identification.matched_risk_measure, M.Identification.risk20_triggered, M.Identification.risk_assessment_complete, M.Identification.simplification_category, M.Identification.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 按具体分支选择负责人、法定代表人、管理产品自然人或较低程度识别，不跨分支概括。 | M.Judgment.Authority.criteria, M.Judgment.Risk.criteria, M.Rule.SimplificationMeasure.expression | MIXED | 由按具体主体分支选择措施、风险及措施匹配判断、主体分类、用途授权和责任适用核查共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成与主体、产品和风险匹配的简化措施及理由。 | M.Access.institution_authorized, M.Access.lawful_purpose, M.Access.operator_authorized, M.Identification.category_verified, M.Identification.data_doubt, M.Identification.enhanced_measures, M.Identification.higher_risk, M.Identification.matched_risk_measure, M.Identification.risk20_triggered, M.Identification.risk_assessment_complete, M.Identification.simplification_measure | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 出现第二十条情形或无法准确判断条件时禁止简化。 | M.Judgment.Authority.criteria, M.Judgment.Risk.criteria, M.Rule.SimplificationMeasure.expression | FORMALIZED | 出现第二十条情形或无法准确判断条件时禁止简化。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 产品备案、公开募集、结构简单或低风险条件缺一即不适用对应分支。 | M.Judgment.Authority.on_missing, M.Judgment.Risk.on_missing, M.Rule.SimplificationMeasure.on_unknown | FORMALIZED | 产品备案、公开募集、结构简单或低风险条件缺一即不适用对应分支。 缺证不得用默认值补足。 |
| 时间要求 | 自2026-01-20施行。 | M.Process.G5.trigger | FORMALIZED | 自2026-01-20施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.15.FILING_EXEMPT

状态：PARTIAL；问题：K.Q.15；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.REV.IDENTITY.FX_EQUIV, M.Gap.EXT.GOV.BROAD_UNITS, M.Gap.CURRENT_TARGET_RISK

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 3号令备案承诺免报与金融机构识别边界。 | M.Process.G5.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 备案主体全部满足1000万元门槛、自然人股东合伙人、无外部自然人和无其他方式控制获益。 | M.Filing.all_natural_holders, M.Filing.as_of, M.Filing.capital_cny, M.Filing.no_external_beneficiary, M.Filing.no_other_control_benefit, M.Filing.promise_truthful, M.Subject.kind | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 符合时只免登记系统报送；金融机构另按12号令识别、核实、简化或豁免规则判断。 | M.Rule.FilingExemption.expression | FORMALIZED | 由承诺免报条件共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 备案免报与金融机构客户尽调分别形成结论。 | M.Filing.promise_exempt | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 任一承诺条件失效即在30日内更新备案。 | M.Rule.FilingExemption.expression | FORMALIZED | 任一承诺条件失效即在30日内更新备案。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 控制获益安排不明时不能承诺免报，也不能作为银行免识别依据。 | M.Rule.FilingExemption.on_unknown | FORMALIZED | 控制获益安排不明时不能承诺免报，也不能作为银行免识别依据。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01；12号令自2026-01-20。 | M.Filing.as_of | FORMALIZED | 3号令自2024-11-01；12号令自2026-01-20。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.16.FREQUENCY

状态：PARTIAL；问题：K.Q.16；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.REVIEW_FREQUENCY, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 持续关注下的复核触发和加强情形的复核频率。 | M.Process.G4.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已有客户识别基线、变化监测和风险状态。 | M.Followup.may_affect_ownership | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 发生可能影响受益所有权事件时审核；第二十条加强情形可提高频率。 | M.Rule.ReviewTrigger.expression | FORMALIZED | 由变更事件触发复核共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成事件驱动复核并对高风险加密频率。 | M.Followup.review_required | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 本次来源未规定所有客户统一固定周期，内部周期须另标机构政策。 | M.Rule.ReviewTrigger.expression | FORMALIZED | 本次来源未规定所有客户统一固定周期，内部周期须另标机构政策。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 无适用规范或确认政策时不填造季度、年度频率。 | M.Rule.ReviewTrigger.on_unknown | FORMALIZED | 无适用规范或确认政策时不填造季度、年度频率。 缺证不得用默认值补足。 |
| 时间要求 | 自2026-01-20施行。 | M.Process.G4.trigger | FORMALIZED | 自2026-01-20施行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.20.ACCESS

状态：PARTIAL；问题：K.Q.20；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.RETENTION, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 国家机关、金融机构和特定非金融机构对BOMIS受益所有人信息的获取和使用。 | M.Process.G7.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 能够证明法定职责或反洗钱反恐怖融资义务及具体查询者权限。 | M.Access.allowed, M.Access.declaration_verified, M.Access.institution_authorized, M.Access.lawful_purpose, M.Access.operator_authorized, M.Access.purpose, M.Identification.evidence, M.Identification.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 目的成立才查询；反洗钱声明决定非掩码加密或掩码返回；所得信息仅在目的范围使用并保密。 | M.Judgment.Authority.criteria, M.Rule.Access.expression, M.Rule.ReturnMode.expression | MIXED | 由查询用途及授权、查询返回方式、主体分类、用途授权和责任适用核查共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成合法目的、返回方式和后续用途相连的访问记录。 | M.Access.allowed, M.Access.institution_authorized, M.Access.lawful_purpose, M.Access.operator_authorized, M.Access.return_mode, M.Identification.category_verified | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 非掩码返回不扩大内部用途。 | M.Judgment.Authority.criteria, M.Rule.Access.expression, M.Rule.ReturnMode.expression | FORMALIZED | 非掩码返回不扩大内部用途。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 目的或授权不能证明即拒绝访问披露。 | M.Judgment.Authority.on_missing, M.Rule.Access.on_unknown, M.Rule.ReturnMode.on_unknown | FORMALIZED | 目的或授权不能证明即拒绝访问披露。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01；BOMIS接口规范版本2026-03。 | M.Process.G7.trigger | FORMALIZED | 3号令自2024-11-01；BOMIS接口规范版本2026-03。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.20.TRANSPORT

状态：PARTIAL；问题：K.Q.20；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.RETENTION, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | BOMIS与参与机构之间的系统传输。 | M.Process.G7.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 参与机构、用户、业务权限、代报关系及证书有效。 | M.Access.authenticated, M.Access.document_envelope, M.Access.encrypted_transport, M.Access.signature_valid | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 经DEMP和HTTPS传输，报文签名验签，证件编号数字信封加密，并执行认证权限检查。 | M.Rule.Transport.expression | FORMALIZED | 由传输保护条件共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 技术层面保护传输机密性、完整性和访问资格。 | M.Access.transport_allowed | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 技术控制不替代业务用途合法性、最小必要使用和后续保密。 | M.Rule.Transport.expression | FORMALIZED | 技术控制不替代业务用途合法性、最小必要使用和后续保密。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 认证、权限、代报或证书失败时不得绕过。 | M.Rule.Transport.on_unknown | FORMALIZED | 认证、权限、代报或证书失败时不得绕过。 缺证不得用默认值补足。 |
| 时间要求 | BOMIS接口规范V2.0，2026-03。 | M.Process.G7.trigger | FORMALIZED | BOMIS接口规范V2.0，2026-03。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.21.TRANSITION

状态：PARTIAL；问题：K.Q.21；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.PENALTY_BASIS, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 3号令和12号令的生效、旧文件废止及存量过渡。 | M.Process.G7.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已确定行为和客户关系时点。 | M.ComplianceReview.as_of, M.ComplianceReview.duty_kind | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 3号令自2024-11-01、存量备案至2025-11-01；12号令自2026-01-20，旧235/164号废止，存量客户按6个月、2年或延期例外。 | M.Rule.Regime.expression | FORMALIZED | 由按时点选择制度共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成正确适用版本和过渡计划。 | M.ComplianceReview.applicable_regime | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 网页抓取时间不构成生效时间。 | M.Rule.Regime.expression | FORMALIZED | 网页抓取时间不构成生效时间。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 行为日或存量关系证明缺失时不作版本结论。 | M.Rule.Regime.on_unknown | FORMALIZED | 行为日或存量关系证明缺失时不作版本结论。 缺证不得用默认值补足。 |
| 时间要求 | 按各条明示日期。 | M.ComplianceReview.as_of | FORMALIZED | 按各条明示日期。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.EXT.GOV.21.LIABILITY

状态：PARTIAL；问题：K.Q.21；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.PENALTY_BASIS, M.Gap.EXT.GOV.BROAD_UNITS

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 备案不履行及金融机构一般、严重、风险管理、差异和内控违法。 | M.Process.G7.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 已固定具体行为、义务主体、发生时点、危害和整改事实。 | M.Access.purpose, M.ComplianceReview.as_of, M.ComplianceReview.duty_kind, M.ComplianceReview.evidence, M.Identification.evidence, M.Identification.subject | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 按条文分流违法类型和处罚档位，再单独评估从轻减轻因素及上位法适用。 | M.Judgment.Authority.criteria, M.Judgment.Liability.criteria | MANUAL | 由主体分类、用途授权和责任适用核查、责任类型及从轻减轻因素核查共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成责任风险和法务复核清单。 | M.Access.institution_authorized, M.Access.lawful_purpose, M.Access.operator_authorized, M.ComplianceReview.legal_sources_complete, M.ComplianceReview.mitigation, M.ComplianceReview.rectification, M.ComplianceReview.violation_type, M.Identification.category_verified | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 从轻减轻不免责，罚款上限不等于必然处罚额。 | M.Judgment.Authority.criteria, M.Judgment.Liability.criteria | FORMALIZED | 从轻减轻不免责，罚款上限不等于必然处罚额。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 上位法或企业登记行政法规未补齐时不作具体案件最终处罚判断。 | M.Judgment.Authority.on_missing, M.Judgment.Liability.on_missing | FORMALIZED | 上位法或企业登记行政法规未补齐时不作具体案件最终处罚判断。 缺证不得用默认值补足。 |
| 时间要求 | 3号令自2024-11-01；12号令自2026-01-20。 | M.ComplianceReview.as_of | FORMALIZED | 3号令自2024-11-01；12号令自2026-01-20。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.23.VERIFY

状态：PARTIAL；问题：K.Q.23.VERIFY；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.RETENTION

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 单笔与批量核验。 | M.Process.G9.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 核对每日额度；批量不超过单报文100家。 | M.Access.allowed, M.Query.batch, M.Query.business_feedback_success, M.Query.daily_used_before, M.Query.feedback_matched, M.Query.feedback_received, M.Query.parameters_current, M.Query.per_subject_complete, M.Query.quota, M.Query.subject_count | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 同步初步校验→对应核验业务反馈；批量另核对夜间批处理结果，按各主体与流水关联。 | M.Rule.DailyStop.expression, M.Rule.QueryAllowed.expression, M.Rule.QueryUsable.expression, M.Transition.QueryFail.guard, M.Transition.QueryIncomplete.guard, M.Transition.QueryReceive.guard, M.Transition.QuerySend.guard | FORMALIZED | 由核验报文允许发送、本批次后是否停止后续核验、逐主体业务结果可用、查询异步反馈共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 区分接收、格式/逻辑失败、业务核验结论。 | M.Query.query_allowed, M.Query.result_usable, M.Query.state, M.Query.triggers_daily_stop | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 临界批次全部核验、后续不处理的规则按原文，不拆改为只处理额度内部分。 | M.Rule.DailyStop.expression, M.Rule.QueryAllowed.expression, M.Rule.QueryUsable.expression, M.Transition.QueryFail.guard, M.Transition.QueryIncomplete.guard, M.Transition.QueryReceive.guard, M.Transition.QuerySend.guard | FORMALIZED | 临界批次全部核验、后续不处理的规则按原文，不拆改为只处理额度内部分。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 没有逐户业务反馈就保留待结果。 | M.Rule.DailyStop.on_unknown, M.Rule.QueryAllowed.on_unknown, M.Rule.QueryUsable.on_unknown, M.Transition.QueryFail.guard, M.Transition.QueryIncomplete.guard, M.Transition.QueryReceive.guard, M.Transition.QuerySend.guard | FORMALIZED | 没有逐户业务反馈就保留待结果。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G9.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.23.CURRENT

状态：PARTIAL；问题：K.Q.23.CURRENT；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.EXT.GOV.RETENTION

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 备案主体当前详情查询。 | M.Process.G9.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 先取得核验流水并核对当前有效期，主体处于可查询状态。 | M.Access.allowed, M.Query.business_feedback_success, M.Query.feedback_matched, M.Query.feedback_received, M.Query.independent_identification_complete, M.Query.per_subject_complete, M.Query.request_reference, M.Query.response_reference, M.Query.verification_reference, M.Query.verification_valid | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 校验前提→请求→等待详情反馈→核对人员、身份、权利状况。 | M.Rule.CurrentQuery.expression, M.Rule.QueryMatch.expression, M.Rule.QueryUsable.expression, M.Rule.Reverification.expression, M.Transition.QueryFail.guard, M.Transition.QueryIncomplete.guard, M.Transition.QueryReceive.guard, M.Transition.QuerySend.guard | FORMALIZED | 由反馈关联原请求、逐主体业务结果可用、当前详情查询的核验流水前提、失效流水重新核验、查询异步反馈共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 使用取得的当前备案信息进行比对。 | M.Query.feedback_matched, M.Query.query_allowed, M.Query.result_usable, M.Query.reverification_required, M.Query.state | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 180天仅初始值；业务通知可能调整；未备案主体不可查。 | M.Rule.CurrentQuery.expression, M.Rule.QueryMatch.expression, M.Rule.QueryUsable.expression, M.Rule.Reverification.expression, M.Transition.QueryFail.guard, M.Transition.QueryIncomplete.guard, M.Transition.QueryReceive.guard, M.Transition.QuerySend.guard | FORMALIZED | 180天仅初始值；业务通知可能调整；未备案主体不可查。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 重新核验或处理错误后查询；仍保留本机构独立识别。 | M.Rule.CurrentQuery.on_unknown, M.Rule.QueryMatch.on_unknown, M.Rule.QueryUsable.on_unknown, M.Rule.Reverification.on_unknown, M.Transition.QueryFail.guard, M.Transition.QueryIncomplete.guard, M.Transition.QueryReceive.guard, M.Transition.QuerySend.guard | FORMALIZED | 重新核验或处理错误后查询；仍保留本机构独立识别。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G9.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.23.HISTORY

状态：PARTIAL；问题：K.Q.23.HISTORY；缺口：M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 备案历史信息回访。 | M.Process.G9.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 明确待回溯主体和时点，取得实际历史反馈。 | M.PersonAssessment.basis_evidence, M.PersonAssessment.history, M.Query.request_reference, M.Query.response_reference | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 将历史备案信息与权益变更、生效时间证据逐项对照，分别解释关系日期及备案时点。 | M.Judgment.Continuity.criteria, M.Rule.QueryMatch.expression | MIXED | 由反馈关联原请求、历史完整性和总体资格连续判断共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成历史变化与中断说明；未记录历史保留证据缺口。 | M.PersonAssessment.continuity_verified, M.PersonAssessment.date_reason, M.PersonAssessment.history_complete, M.Query.feedback_matched | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 用户已答总体资格连续不重置日期，关系类型分别记时；这不是接口规则。 | M.Judgment.Continuity.criteria, M.Rule.QueryMatch.expression | FORMALIZED | 用户已答总体资格连续不重置日期，关系类型分别记时；这不是接口规则。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 缺实际生效或历史权益记录时不得用本次查询日补齐。 | M.Judgment.Continuity.on_missing, M.Rule.QueryMatch.on_unknown | FORMALIZED | 缺实际生效或历史权益记录时不得用本次查询日补齐。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G9.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.24.REPORT

状态：PARTIAL；问题：K.Q.24.REPORT；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.INTERFACE_REPORT_DUTY, M.Gap.INTERFACE_THRESHOLD, M.Gap.INTERFACE_IDENTITY

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 核实后选择报告类型。 | M.Process.G9.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 核对主体是否在库、填报类型、人员是否为空、资料是否完整及核验结果。 | M.DifferenceReport.analysis_present, M.DifferenceReport.attachments_usable, M.DifferenceReport.new_person_name_present, M.DifferenceReport.new_person_present, M.DifferenceReport.nonmajor_policy_confirmed, M.DifferenceReport.old_person_present, M.DifferenceReport.operation, M.DifferenceReport.organization_change, M.DifferenceReport.person_change, M.DifferenceReport.promise_or_state_condition, M.DifferenceReport.required_content_complete, M.DifferenceReport.subject_code_present, M.DifferenceReport.subject_in_system, M.DifferenceReport.subtype, M.DifferenceReport.support_present, M.DifferenceReport.system_people_empty, M.DifferenceReport.type_supported, M.DifferenceReport.verification_consistent | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 按报备四类、补充两类、审批三类、确认无差异分别判断；遵守各自新增/修改/删除边界与证据要求。 | M.Rule.ReportContent.expression, M.Rule.ReportSubmit.expression | FORMALIZED | 由按报告类别检查内容和操作、差异报告提交前提共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 得到可报送类型及应准备的业务内容；仍不足者保留待补。 | M.DifferenceReport.required_content_complete, M.DifferenceReport.submit_allowed | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 非重大差异接口报备是否实施仍待合规确认；25%以上与个别接口行>25%差异留待澄清。 | M.Rule.ReportContent.expression, M.Rule.ReportSubmit.expression | FORMALIZED | 非重大差异接口报备是否实施仍待合规确认；25%以上与个别接口行>25%差异留待澄清。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 身份存疑或部分缺失按对应分支，不填造缺失身份；类型不适用先核实。 | M.Rule.ReportContent.on_unknown, M.Rule.ReportSubmit.on_unknown | FORMALIZED | 身份存疑或部分缺失按对应分支，不填造缺失身份；类型不适用先核实。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G9.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.24.STATUS

状态：PARTIAL；问题：K.Q.24.STATUS；缺口：M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 已提交报告的后续处理。 | M.Process.G9.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 关联原报告、最新主体事实及反馈内容。 | M.Constraint.ReportFeedback, M.Machine.Report | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 待补充则补件；申请撤销先核对允许状态并等待反馈；终止后重新查询，独立判断差异是否消除。 | M.Constraint.ReportFeedback.expression, M.Transition.ReportDone.guard, M.Transition.ReportProcessing.guard, M.Transition.ReportSubmit.guard, M.Transition.ReportSupplement.guard, M.Transition.ReportTerminate.guard, M.Transition.ReportWithdrawFeedback.guard, M.Transition.ReportWithdrawRequest.guard | FORMALIZED | 由报告业务反馈关联原报告、差异报告办理共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 报告状态与差异业务处置分别记录。 | M.DifferenceReport.state | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 报告办结或终止不直接等同已解决；客户实际更正加机构复核一致才按用户口径闭环。 | M.Constraint.ReportFeedback.expression, M.Transition.ReportDone.guard, M.Transition.ReportProcessing.guard, M.Transition.ReportSubmit.guard, M.Transition.ReportSupplement.guard, M.Transition.ReportTerminate.guard, M.Transition.ReportWithdrawFeedback.guard, M.Transition.ReportWithdrawRequest.guard | FORMALIZED | 报告办结或终止不直接等同已解决；客户实际更正加机构复核一致才按用户口径闭环。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 未取得结果或复核不一致时不关闭差异。 | M.Constraint.ReportFeedback.on_unknown, M.Transition.ReportDone.guard, M.Transition.ReportProcessing.guard, M.Transition.ReportSubmit.guard, M.Transition.ReportSupplement.guard, M.Transition.ReportTerminate.guard, M.Transition.ReportWithdrawFeedback.guard, M.Transition.ReportWithdrawRequest.guard | FORMALIZED | 未取得结果或复核不一致时不关闭差异。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G9.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.24.CASE

状态：PARTIAL；问题：K.Q.24.CASE；缺口：M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 差异案例申请。 | M.Process.G9.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 核对差异报告状态以及是否已有进行中或已批准案例。 | M.BomisCase.conditions_met, M.BomisCase.initial_feedback, M.BomisCase.number_received | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 符合条件才申请；首条反馈收编号；后续反馈查审批结果、日期和意见。 | M.Constraint.BomisCaseDuplicate.expression, M.Rule.CaseQuery.expression, M.Transition.CaseApply.guard, M.Transition.CaseApproval.guard, M.Transition.CaseNumber.guard, M.Transition.CaseWaitApproval.guard | FORMALIZED | 由案例编号取得后查询审批、重复反馈保持原业务关联、案例申请和审批共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 区分已受理申请与已批准案例。 | M.BomisCase.may_query_approval, M.BomisCase.state | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 未办结、已终止或持续关注等状态不可申报；相同报告禁止规定情形下重复申请。 | M.Constraint.BomisCaseDuplicate.expression, M.Rule.CaseQuery.expression, M.Transition.CaseApply.guard, M.Transition.CaseApproval.guard, M.Transition.CaseNumber.guard, M.Transition.CaseWaitApproval.guard | FORMALIZED | 未办结、已终止或持续关注等状态不可申报；相同报告禁止规定情形下重复申请。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 缺最终反馈保持待审批。 | M.Constraint.BomisCaseDuplicate.on_unknown, M.Rule.CaseQuery.on_unknown, M.Transition.CaseApply.guard, M.Transition.CaseApproval.guard, M.Transition.CaseNumber.guard, M.Transition.CaseWaitApproval.guard | FORMALIZED | 缺最终反馈保持待审批。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G9.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.24.PARAM

状态：PARTIAL；问题：K.Q.24.PARAM；缺口：M.Gap.SEMANTIC_REVIEW

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 业务通知、参数与系统状态。 | M.Process.G9.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 掌握通知类型、参数期数及当前系统状态。 | M.Parameters.business_accepting, M.Parameters.initial_snapshot_verified, M.Parameters.previous_sequence, M.Parameters.sequence, M.Parameters.sequence_continuous | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 按通知更新适用参数；缺失期数请求补发；只在受理状态下办理。 | M.Rule.ParameterContinuity.expression, M.Rule.ParameterResend.expression, M.Rule.ParameterSend.expression | FORMALIZED | 由参数通知连续性、参数缺期请求补发、参数完整且业务受理才发送共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 形成参数可用性和当下是否可以发送的判断。 | M.Parameters.resend_needed, M.Parameters.send_allowed, M.Parameters.sequence_continuous | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 初始180天、文件个数和额度不能固化为永久限制。 | M.Rule.ParameterContinuity.expression, M.Rule.ParameterResend.expression, M.Rule.ParameterSend.expression | FORMALIZED | 初始180天、文件个数和额度不能固化为永久限制。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 缺期或内容不明先补参数；不自行编造枚举含义。 | M.Rule.ParameterContinuity.on_unknown, M.Rule.ParameterResend.on_unknown, M.Rule.ParameterSend.on_unknown | FORMALIZED | 缺期或内容不明先补参数；不自行编造枚举含义。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G9.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

### K.R.24.FILE

状态：PARTIAL；问题：K.Q.24.FILE；缺口：M.Gap.SEMANTIC_REVIEW, M.Gap.INTERFACE_IDENTITY

| 要素 | 知识原文 | 模型引用 | 表达方式 | 对应解释 |
| --- | --- | --- | --- | --- |
| 适用范围 | 报告附件和失败请求。 | M.Process.G9.trigger | FORMALIZED | 流程固定主体、用途和判断时点，并按该规则的适用对象选择对应机制。 |
| 前提 | 核对文件用途大小、原请求身份及已有回执。 | M.FileTransfer.file_id_received, M.FileTransfer.response_matched, M.FileTransfer.response_received | FORMALIZED | 这些输入逐项承载前提事实；未核实资料保持未知，由所列机制暂停依赖判断。 |
| 判断条件 | 等待文件上传实际应答并取得ID再关联；按同步/异步错误定位原因；保留原报文和补交关系。 | M.Constraint.FileFeedback.expression, M.Constraint.FileTransferDuplicate.expression, M.Rule.FileUsable.expression, M.Transition.FileFailed.guard, M.Transition.FileUpload.guard, M.Transition.FileUsable.guard | FORMALIZED | 由附件取得实际应答后可用、重复反馈保持原业务关联、附件业务反馈关联原传输、附件上传与关联共同表达条件，人工证据准则与可计算判断分开。 |
| 结果 | 明确附件是否可用、请求失败或待返回；可以追溯已报内容。 | M.FileTransfer.state, M.FileTransfer.usable | FORMALIZED | 判断结果落到这些业务字段；流程和状态仍区分请求、反馈与实质业务结论。 |
| 例外 | 重复报文被拒不代表第一次成功；文件上传成功不代表差异报告通过。 | M.Constraint.FileFeedback.expression, M.Constraint.FileTransferDuplicate.expression, M.Rule.FileUsable.expression, M.Transition.FileFailed.guard, M.Transition.FileUpload.guard, M.Transition.FileUsable.guard | FORMALIZED | 重复报文被拒不代表第一次成功；文件上传成功不代表差异报告通过。 对应规则分支、证据准则和未决事项共同限制可得结论。 |
| 缺证处理 | 无文件ID、反馈或原因未查明时保留未完成，内部重试/超时策略另行确定。 | M.Constraint.FileFeedback.on_unknown, M.Constraint.FileTransferDuplicate.on_unknown, M.Rule.FileUsable.on_unknown, M.Transition.FileFailed.guard, M.Transition.FileUpload.guard, M.Transition.FileUsable.guard | FORMALIZED | 无文件ID、反馈或原因未查明时保留未完成，内部重试/超时策略另行确定。 缺证不得用默认值补足。 |
| 时间要求 | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 | M.Process.G9.trigger | FORMALIZED | 按所引本地制度版本及业务时点使用；接口参数以适用通知为准，未核验在线运行。 先固定业务时点和适用版本，不把请求或记录时间替代实际生效。 |

## 模型目录与依据

| 标识 | 名称 | 依据 |
| --- | --- | --- |
| M.Person | 自然人 | K.R.03, K.R.10, K.R.EXT.GOV.13.VERIFY |
| M.Subject | 非自然人主体 | K.R.01, K.R.08, K.R.09, K.R.09.ASSET |
| M.Evidence | 业务证据 | K.R.13, K.R.11.START |
| M.Right | 持有权益 | K.R.03, K.R.04, K.R.11 |
| M.Control | 实际控制关系 | K.R.05, K.R.11 |
| M.Appointment | 任职关系 | K.R.06, K.R.08, K.R.09.ASSET, K.R.20 |
| M.Identification | 受益所有人识别 | K.R.01, K.R.03, K.R.04, K.R.05, K.R.06, K.R.13, K.R.14, K.R.15, K.R.11.HISTORY |
| M.BeneficialOwnership | 受益所有权关系 | K.R.03, K.R.04, K.R.05, K.R.06, K.R.11.HISTORY |
| M.PersonAssessment | 个人认定结果 | K.R.03, K.R.04, K.R.05, K.R.11.HISTORY |
| M.StateNature | 国企性质认定 | K.R.07.NATURE, K.R.07.APPLY, K.R.EXT.GOV.15.STATE |
| M.Filing | 受益所有人备案 | K.R.02, K.R.12, K.R.EXT.GOV.12.FILING, K.R.22 |
| M.TrustParty | 信托当事人 | K.R.09, K.R.09.TYPE |
| M.ProductAssessment | 产品识别判断 | K.R.09.TYPE, K.R.09.ASSET, K.R.09.RELIANCE |
| M.Difference | 受益所有人信息差异 | K.R.17, K.R.18, K.R.18.DATES, K.R.18.PENDING, K.R.19.CORRECT, K.R.19.CLOSE |
| M.Access | 信息查询授权 | K.R.20, K.R.EXT.GOV.20.ACCESS, K.R.EXT.GOV.20.TRANSPORT |
| M.Query | 备案信息查询 | K.R.23, K.R.23.VERIFY, K.R.23.CURRENT, K.R.23.HISTORY |
| M.DifferenceReport | 差异报告 | K.R.24, K.R.24.REPORT, K.R.24.STATUS |
| M.BomisCase | 案例申请 | K.R.24.CASE |
| M.FileTransfer | 附件传输 | K.R.24.FILE |
| M.Parameters | 业务参数接收 | K.R.24.PARAM |
| M.Followup | 复核与补充任务 | K.R.16, K.R.18.PENDING, K.R.EXT.GOV.12.LEGACY_CDD, K.R.EXT.GOV.16.FREQUENCY |
| M.ComplianceReview | 适用制度与责任核查 | K.R.21, K.R.EXT.GOV.21.TRANSITION, K.R.EXT.GOV.21.LIABILITY |
| M.RightTime |  | K.R.11 |
| M.ControlTime |  | K.R.11 |
| M.AppointmentTime |  | K.R.06, K.R.08 |
| M.BeneficialOwnershipTime |  | K.R.11.HISTORY |
| M.Rule.FilingScope | 判断备案适用范围 | K.R.01 |
| M.Rule.CddScope | 判断金融机构识别适用范围 | K.R.01 |
| M.Rule.FilingExemption | 承诺免报条件 | K.R.02, K.R.EXT.GOV.15.FILING_EXEMPT |
| M.Rule.EquityPaths | 股权或合伙权益路径逐条乘算 | K.R.03 |
| M.Rule.EquityTotal | 股权或合伙权益多路径合计 | K.R.03 |
| M.Rule.IncomePaths | 收益权路径逐条乘算 | K.R.04 |
| M.Rule.IncomeTotal | 收益权多路径合计 | K.R.04 |
| M.Rule.VotingPaths | 表决权路径逐条乘算 | K.R.04 |
| M.Rule.VotingTotal | 表决权多路径合计 | K.R.04 |
| M.Rule.Standard1 | 按股权或合伙权益标准认定 | K.R.03 |
| M.Rule.Standard2 | 按收益权或表决权标准认定 | K.R.04 |
| M.Rule.Standard3 | 按实际控制标准认定 | K.R.05 |
| M.Rule.PersonQualified | 汇总该自然人的达标情况 | K.R.03, K.R.04, K.R.05 |
| M.Rule.UseStandard2 | 本人优先采用标准一后的标准二 | K.R.03, K.R.04 |
| M.Rule.UseStandard3 | 本人优先采用标准一后的标准三 | K.R.03, K.R.05 |
| M.Rule.Fallback | 是否可以采用管理人员兜底 | K.R.06 |
| M.Rule.Article44 | 第四条第四项性质条件 | K.R.07.NATURE |
| M.Rule.RelativeHolding | 衔接国有相对控股口径 | K.R.07.NATURE, K.R.07.APPLY |
| M.Rule.StateApplicability | 金融机构国企简化主体范围 | K.R.07, K.R.07.APPLY, K.R.EXT.GOV.15.STATE |
| M.Rule.StateSimplification | 国企简化风险门控 | K.R.07, K.R.07.RISK, K.R.EXT.GOV.15.STATE |
| M.Rule.BranchRoute | 分支机构识别路径 | K.R.08 |
| M.Rule.TrustFull | 完整信托当事人识别 | K.R.09 |
| M.Rule.TrustSimplification | 信托类型和风险分支 | K.R.09.TYPE |
| M.Rule.AssetSimplification | 资管产品简化条件 | K.R.09.ASSET |
| M.Rule.ManagerReliance | 是否可采信管理受托机构结果 | K.R.09.RELIANCE |
| M.Rule.Formation | 当前总体形成日期 | K.R.11, K.R.11.HISTORY |
| M.Rule.FilingDue | 备案及更新期限 | K.R.12, K.R.EXT.GOV.12.FILING |
| M.Rule.LegacyDeferral | 存量客户激活例外 | K.R.EXT.GOV.12.LEGACY_CDD |
| M.Rule.LegacyDue | 存量客户补齐期限 | K.R.12, K.R.EXT.GOV.12.LEGACY_CDD |
| M.Rule.RefuseOrEnd | 加强后是否可拒绝或终止 | K.R.14, K.R.EXT.GOV.14.STOP |
| M.Rule.CddExemption | 列明主体免识别条件 | K.R.15, K.R.EXT.GOV.15.EXEMPT |
| M.Rule.SimplificationMeasure | 按具体主体分支选择措施 | K.R.15, K.R.EXT.GOV.15.SIMPLIFY |
| M.Rule.ReviewTrigger | 变更事件触发复核 | K.R.16, K.R.EXT.GOV.16.FREQUENCY |
| M.Rule.QueryAfterIdentification | 备案主体查询核对前提 | K.R.13, K.R.17, K.R.EXT.GOV.13.VERIFY |
| M.Rule.DateYearMonth | 关系日期年月比较 | K.R.18, K.R.18.DATES |
| M.Rule.MaterialDifference | 差异重大性判断 | K.R.18, K.R.18.DATES |
| M.Rule.UpdateDue | 近期变化的法定更新截止 | K.R.18.PENDING |
| M.Rule.TimingPending | 时点性待更新标记 | K.R.18, K.R.18.PENDING |
| M.Rule.ReportRequired | 差异报告义务判断 | K.R.19, K.R.19.CORRECT |
| M.Rule.CorrectionAction | 按原因采取差异处置 | K.R.19, K.R.19.CORRECT |
| M.Rule.CloseDifference | 实际更正且复核一致后闭环 | K.R.19, K.R.19.CLOSE |
| M.Rule.Access | 查询用途及授权 | K.R.20, K.R.EXT.GOV.20.ACCESS |
| M.Rule.ReturnMode | 查询返回方式 | K.R.EXT.GOV.20.ACCESS |
| M.Rule.Transport | 传输保护条件 | K.R.EXT.GOV.20.TRANSPORT |
| M.Rule.Regime | 按时点选择制度 | K.R.21, K.R.EXT.GOV.21.TRANSITION |
| M.Rule.FilingSubmit | 备案资料和人员关系完整后提交 | K.R.22 |
| M.Rule.QueryAllowed | 核验报文允许发送 | K.R.23, K.R.23.VERIFY |
| M.Rule.DailyStop | 本批次后是否停止后续核验 | K.R.23.VERIFY |
| M.Rule.QueryMatch | 反馈关联原请求 | K.R.23, K.R.23.CURRENT, K.R.23.HISTORY |
| M.Rule.QueryUsable | 逐主体业务结果可用 | K.R.23, K.R.23.VERIFY, K.R.23.CURRENT |
| M.Rule.CurrentQuery | 当前详情查询的核验流水前提 | K.R.23.CURRENT |
| M.Rule.ReportContent | 按报告类别检查内容和操作 | K.R.24, K.R.24.REPORT |
| M.Rule.ReportSubmit | 差异报告提交前提 | K.R.24, K.R.24.REPORT |
| M.Rule.CaseQuery | 案例编号取得后查询审批 | K.R.24.CASE |
| M.Rule.ParameterContinuity | 参数通知连续性 | K.R.24.PARAM |
| M.Rule.ParameterResend | 参数缺期请求补发 | K.R.24.PARAM |
| M.Rule.ParameterSend | 参数完整且业务受理才发送 | K.R.24.PARAM |
| M.Rule.FileUsable | 附件取得实际应答后可用 | K.R.24.FILE |
| M.Rule.KnownEquityPaths | 保留已证明的股权路径 | K.R.03 |
| M.Rule.KnownEquityLowerBound | 已知股权路径形成下界 | K.R.03 |
| M.Rule.KnownStandard1Candidate | 不完整结构中的已知达标候选 | K.R.03 |
| M.Rule.Reverification | 失效流水重新核验 | K.R.23.CURRENT |
| M.Machine.Difference | 差异实质处置 | K.R.19, K.R.19.CLOSE |
| M.Machine.Query | 查询异步反馈 | K.R.23, K.R.23.VERIFY, K.R.23.CURRENT |
| M.Machine.Report | 差异报告办理 | K.R.24, K.R.24.STATUS |
| M.Machine.Case | 案例申请和审批 | K.R.24.CASE |
| M.Machine.File | 附件上传与关联 | K.R.24.FILE |
| M.Judgment.IdentityRights | 核实身份、权利及结构证据 | K.R.10, K.R.13, K.R.EXT.GOV.13.IDENTIFY, K.R.EXT.GOV.13.VERIFY |
| M.Judgment.Control | 实际控制证据判断 | K.R.05 |
| M.Judgment.StateNature | 国有性质与实际支配证据判断 | K.R.07, K.R.07.NATURE, K.R.07.APPLY, K.R.EXT.GOV.15.STATE |
| M.Judgment.EffectiveDate | 法律关系实际生效日期判断 | K.R.11, K.R.11.START, K.R.EXT.GOV.10.FORMATION |
| M.Judgment.Continuity | 历史完整性和总体资格连续判断 | K.R.11, K.R.11.HISTORY, K.R.23.HISTORY |
| M.Judgment.Risk | 风险及措施匹配判断 | K.R.07.RISK, K.R.14, K.R.15, K.R.EXT.GOV.14.STOP, K.R.EXT.GOV.15.SIMPLIFY, K.R.EXT.GOV.15.EXEMPT |
| M.Judgment.RemainingRisk | 加强措施后的剩余风险判断 | K.R.14, K.R.EXT.GOV.14.STOP |
| M.Judgment.Products | 信托与资管条件及受托机构履职判断 | K.R.09, K.R.09.TYPE, K.R.09.ASSET, K.R.09.RELIANCE |
| M.Judgment.DifferenceCause | 差异原因和更正后复核 | K.R.17, K.R.18, K.R.19, K.R.19.CORRECT, K.R.19.CLOSE |
| M.Judgment.Authority | 主体分类、用途授权和责任适用核查 | K.R.01, K.R.20, K.R.21, K.R.EXT.GOV.20.ACCESS, K.R.EXT.GOV.21.LIABILITY, K.R.EXT.GOV.15.EXEMPT, K.R.EXT.GOV.15.SIMPLIFY |
| M.Judgment.RecordContents | 场景所需信息集合核对 | K.R.10 |
| M.Judgment.FilingRoute | 地方办理方式和入口核对 | K.R.22 |
| M.Judgment.Liability | 责任类型及从轻减轻因素核查 | K.R.21, K.R.EXT.GOV.21.LIABILITY |
| M.Constraint.RightParty | 一项持有权益只对应一种权利人 | K.R.03, K.R.04 |
| M.Constraint.RightTarget | 权益目标身份与主体一致 | K.R.03 |
| M.Constraint.RightHolder | 权益持有人身份与对应实体一致 | K.R.03 |
| M.Constraint.RightRatio | 权益比例以0至1表示 | K.R.03, K.R.04 |
| M.Constraint.RightInterval | 已知终止须晚于开始，未知终止不得冒充持续 | K.R.11 |
| M.Constraint.ControlInterval | 已知终止须晚于开始，未知终止不得冒充持续 | K.R.11 |
| M.Constraint.AppointmentInterval | 已知终止须晚于开始，未知终止不得冒充持续 | K.R.06, K.R.08 |
| M.Constraint.BeneficialOwnershipInterval | 已知终止须晚于开始，未知终止不得冒充持续 | K.R.11.HISTORY |
| M.Constraint.BomisCaseDuplicate | 重复反馈保持原业务关联 | K.R.24.CASE |
| M.Constraint.FileTransferDuplicate | 重复反馈保持原业务关联 | K.R.24.FILE |
| M.Constraint.ReportFeedback | 报告业务反馈关联原报告 | K.R.24.STATUS |
| M.Constraint.FileFeedback | 附件业务反馈关联原传输 | K.R.24.FILE |
| M.Process.G1 | 适用性、备案与身份识别 | K.R.01, K.R.02, K.R.03, K.R.04, K.R.05, K.R.06, K.R.08, K.R.10 |
| M.Process.G2 | 国企性质与简化 | K.R.07, K.R.07.NATURE, K.R.07.APPLY, K.R.07.RISK, K.R.EXT.GOV.15.STATE |
| M.Process.G3 | 信托与资产管理产品 | K.R.09, K.R.09.TYPE, K.R.09.ASSET, K.R.09.RELIANCE |
| M.Process.G4 | 时间、期限与持续复核 | K.R.11, K.R.11.START, K.R.11.HISTORY, K.R.12, K.R.16, K.R.EXT.GOV.10.FORMATION, K.R.EXT.GOV.12.FILING, K.R.EXT.GOV.12.LEGACY_CDD, K.R.EXT.GOV.16.FREQUENCY |
| M.Process.G5 | 证据、风险与措施 | K.R.13, K.R.14, K.R.15, K.R.EXT.GOV.13.IDENTIFY, K.R.EXT.GOV.13.VERIFY, K.R.EXT.GOV.14.STOP, K.R.EXT.GOV.15.EXEMPT, K.R.EXT.GOV.15.SIMPLIFY, K.R.EXT.GOV.15.FILING_EXEMPT |
| M.Process.G6 | 查询、差异与闭环 | K.R.17, K.R.18, K.R.18.DATES, K.R.18.PENDING, K.R.19, K.R.19.CORRECT, K.R.19.CLOSE |
| M.Process.G7 | 访问、保密、过渡与责任 | K.R.20, K.R.21, K.R.EXT.GOV.20.ACCESS, K.R.EXT.GOV.20.TRANSPORT, K.R.EXT.GOV.21.TRANSITION, K.R.EXT.GOV.21.LIABILITY |
| M.Process.G8 | 地方备案办理 | K.R.22 |
| M.Process.G9 | BOMIS核验、查询与办理 | K.R.23, K.R.23.VERIFY, K.R.23.CURRENT, K.R.23.HISTORY, K.R.24, K.R.24.REPORT, K.R.24.STATUS, K.R.24.CASE, K.R.24.PARAM, K.R.24.FILE |
| M.Gap.02 | 近期变更处于法定30日更新期时，应标记时点性待更新，这一选择已有用户答复；后续复核责任、复核时点和超期升级操作尚需明确。 |  |
| M.Gap.SEMANTIC_REVIEW | 20个既有问题已按本轮方法补成具体业务解释、判断和案例；全量输入单元仍有未审或仅部分拆解，不能声明知识全量完整。 |  |
| M.Gap.REV.IDENTITY.MISSING_ORDER11 | 12号令第二条把适用机构范围交由2025年第11号令规定，但该令不在用户限定的七份制度原文中，因此当前不能列出完整义务机构清单。 |  |
| M.Gap.REV.IDENTITY.FX_EQUIV | 3号令第三条允许以等值外币判断1000万元免报边界，但限定材料没有规定折算日期、汇率来源或舍入方法。 |  |
| M.Gap.REV.IDENTITY.CIRCULAR_CALC | 第二版备案指南说明普通多层路径乘算和同一自然人多路径合计，12号令把循环嵌套、交叉持股列为需加强的复杂结构，但限定材料没有给出循环或交叉持股的封闭比例算法。 |  |
| M.Gap.REV.IDENTITY.TIED_MANAGERS | 第二版备案指南规定兜底时至少备案一名最高层级日常经营管理人员，但未规定同一最高层级有多名人员时的选择或全量纳入标准。 |  |
| M.Gap.REV.IDENTITY.AM_MANAGER | 12号令第十四、十七条要求简化时认定并取得‘管理资产管理产品的自然人’信息，但没有界定多人团队、投资决策委员会或管理职责分散时应选择哪些自然人。 |  |
| M.Gap.EXT.GOV.RETENTION | 本次唯一权威输入要求金融机构识别留存并依法保密，但未载明保存10年，也未说明从业务关系终止、交易完成或其他事件起算。 |  |
| M.Gap.EXT.GOV.REVIEW_FREQUENCY | 12号令规定事件触发审核，并允许加强情形提高审核更新频率，但本次来源未给全部客户统一固定复核周期。 |  |
| M.Gap.EXT.GOV.PENALTY_BASIS | 3号令和12号令的责任条款继续引用企业登记管理行政法规及反洗钱法第五十二至五十四条，本次7份来源未包含这些全文。 |  |
| M.Gap.EXT.GOV.BROAD_UNITS | 本轮仅对8个问题直接相关的原文条款和BOMIS安全查询单元做深度回读；地方操作手册全部界面图、BOMIS其余千余报文字段及8题以外业务含义未宣称完成。 |  |
| M.Gap.INTERFACE_REPORT_DUTY | 非重大差异无需法定差异报告，与接口“非重大差异报备”功能如何在本机构衔接？ |  |
| M.Gap.INTERFACE_THRESHOLD | BOMIS补充类个别说明写比例>25%，与制度“25%以上”及25%边界如何一致？ |  |
| M.Gap.INTERFACE_IDENTITY | V2.0修订说明与附录旧错误码对人员匹配和必填项存在不一致，使用哪套字段规则？ |  |
| M.Gap.CURRENT_TARGET_RISK | 国企简化的现行操作已经澄清，但“通常直接简化”的做法与制度要求的充分风险评估之间仍需合规裁定。 |  |
| M.Transition.DifferenceInvestigate | 开始查因 | K.R.19, K.R.19.CLOSE |
| M.Transition.DifferenceCorrected | 实际更正后等待复核 | K.R.19, K.R.19.CLOSE |
| M.Transition.DifferenceResolve | 复核一致后解决 | K.R.19, K.R.19.CLOSE |
| M.Transition.QuerySend | 按准入发起请求 | K.R.23, K.R.23.VERIFY, K.R.23.CURRENT |
| M.Transition.QueryReceive | 逐主体反馈齐备 | K.R.23, K.R.23.VERIFY, K.R.23.CURRENT |
| M.Transition.QueryIncomplete | 已反馈但逐主体结果不完整 | K.R.23, K.R.23.VERIFY, K.R.23.CURRENT |
| M.Transition.QueryFail | 收到明确业务失败 | K.R.23, K.R.23.VERIFY, K.R.23.CURRENT |
| M.Transition.ReportSubmit | 提交报告后等待反馈 | K.R.24, K.R.24.STATUS |
| M.Transition.ReportSupplement | 收到待补充反馈 | K.R.24, K.R.24.STATUS |
| M.Transition.ReportProcessing | 收到办理中反馈 | K.R.24, K.R.24.STATUS |
| M.Transition.ReportDone | 收到办结反馈 | K.R.24, K.R.24.STATUS |
| M.Transition.ReportWithdrawRequest | 当前状态允许申请撤销 | K.R.24, K.R.24.STATUS |
| M.Transition.ReportWithdrawFeedback | 收到真实撤销反馈 | K.R.24, K.R.24.STATUS |
| M.Transition.ReportTerminate | 收到终止业务反馈 | K.R.24, K.R.24.STATUS |
| M.Transition.CaseApply | 符合条件后提出申请 | K.R.24.CASE |
| M.Transition.CaseNumber | 首反馈取得编号 | K.R.24.CASE |
| M.Transition.CaseWaitApproval | 按编号查询审批 | K.R.24.CASE |
| M.Transition.CaseApproval | 收到实际审批结果 | K.R.24.CASE |
| M.Transition.FileUpload | 发送上传请求 | K.R.24.FILE |
| M.Transition.FileUsable | 上传应答确认可用 | K.R.24.FILE |
| M.Transition.FileFailed | 收到同步或异步错误 | K.R.24.FILE |
| M.Step.G1.FilingScope | 判断备案适用范围 | K.R.01 |
| M.Step.G1.CddScope | 判断金融机构识别适用范围 | K.R.01 |
| M.Step.G1.FilingExemption | 承诺免报条件 | K.R.02, K.R.EXT.GOV.15.FILING_EXEMPT |
| M.Step.G1.EquityPaths | 股权或合伙权益路径逐条乘算 | K.R.03 |
| M.Step.G1.EquityTotal | 股权或合伙权益多路径合计 | K.R.03 |
| M.Step.G1.IncomePaths | 收益权路径逐条乘算 | K.R.04 |
| M.Step.G1.IncomeTotal | 收益权多路径合计 | K.R.04 |
| M.Step.G1.VotingPaths | 表决权路径逐条乘算 | K.R.04 |
| M.Step.G1.VotingTotal | 表决权多路径合计 | K.R.04 |
| M.Step.G1.Standard1 | 按股权或合伙权益标准认定 | K.R.03 |
| M.Step.G1.Standard2 | 按收益权或表决权标准认定 | K.R.04 |
| M.Step.G1.Standard3 | 按实际控制标准认定 | K.R.05 |
| M.Step.G1.PersonQualified | 汇总该自然人的达标情况 | K.R.03, K.R.04, K.R.05 |
| M.Step.G1.UseStandard2 | 本人优先采用标准一后的标准二 | K.R.03, K.R.04 |
| M.Step.G1.UseStandard3 | 本人优先采用标准一后的标准三 | K.R.03, K.R.05 |
| M.Step.G1.Fallback | 是否可以采用管理人员兜底 | K.R.06 |
| M.Step.G1.BranchRoute | 分支机构识别路径 | K.R.08 |
| M.Step.G1.KnownEquityPaths | 保留已证明的股权路径 | K.R.03 |
| M.Step.G1.KnownEquityLowerBound | 已知股权路径形成下界 | K.R.03 |
| M.Step.G1.KnownStandard1Candidate | 不完整结构中的已知达标候选 | K.R.03 |
| M.Step.G1.IdentityRights | 核实身份、权利及结构证据 | K.R.10, K.R.13, K.R.EXT.GOV.13.IDENTIFY, K.R.EXT.GOV.13.VERIFY |
| M.Step.G1.Control | 实际控制证据判断 | K.R.05 |
| M.Step.G1.Authority | 主体分类、用途授权和责任适用核查 | K.R.01, K.R.20, K.R.21, K.R.EXT.GOV.20.ACCESS, K.R.EXT.GOV.21.LIABILITY, K.R.EXT.GOV.15.EXEMPT, K.R.EXT.GOV.15.SIMPLIFY |
| M.Step.G1.RecordContents | 场景所需信息集合核对 | K.R.10 |
| M.Step.G2.Article44 | 第四条第四项性质条件 | K.R.07.NATURE |
| M.Step.G2.RelativeHolding | 衔接国有相对控股口径 | K.R.07.NATURE, K.R.07.APPLY |
| M.Step.G2.StateApplicability | 金融机构国企简化主体范围 | K.R.07, K.R.07.APPLY, K.R.EXT.GOV.15.STATE |
| M.Step.G2.StateSimplification | 国企简化风险门控 | K.R.07, K.R.07.RISK, K.R.EXT.GOV.15.STATE |
| M.Step.G2.StateNature | 国有性质与实际支配证据判断 | K.R.07, K.R.07.NATURE, K.R.07.APPLY, K.R.EXT.GOV.15.STATE |
| M.Step.G2.Risk | 风险及措施匹配判断 | K.R.07.RISK, K.R.14, K.R.15, K.R.EXT.GOV.14.STOP, K.R.EXT.GOV.15.SIMPLIFY, K.R.EXT.GOV.15.EXEMPT |
| M.Step.G3.TrustFull | 完整信托当事人识别 | K.R.09 |
| M.Step.G3.TrustSimplification | 信托类型和风险分支 | K.R.09.TYPE |
| M.Step.G3.AssetSimplification | 资管产品简化条件 | K.R.09.ASSET |
| M.Step.G3.ManagerReliance | 是否可采信管理受托机构结果 | K.R.09.RELIANCE |
| M.Step.G3.Products | 信托与资管条件及受托机构履职判断 | K.R.09, K.R.09.TYPE, K.R.09.ASSET, K.R.09.RELIANCE |
| M.Step.G4.Formation | 当前总体形成日期 | K.R.11, K.R.11.HISTORY |
| M.Step.G4.FilingDue | 备案及更新期限 | K.R.12, K.R.EXT.GOV.12.FILING |
| M.Step.G4.LegacyDeferral | 存量客户激活例外 | K.R.EXT.GOV.12.LEGACY_CDD |
| M.Step.G4.LegacyDue | 存量客户补齐期限 | K.R.12, K.R.EXT.GOV.12.LEGACY_CDD |
| M.Step.G4.ReviewTrigger | 变更事件触发复核 | K.R.16, K.R.EXT.GOV.16.FREQUENCY |
| M.Step.G4.EffectiveDate | 法律关系实际生效日期判断 | K.R.11, K.R.11.START, K.R.EXT.GOV.10.FORMATION |
| M.Step.G4.Continuity | 历史完整性和总体资格连续判断 | K.R.11, K.R.11.HISTORY, K.R.23.HISTORY |
| M.Step.G5.FilingExemption | 承诺免报条件 | K.R.02, K.R.EXT.GOV.15.FILING_EXEMPT |
| M.Step.G5.RefuseOrEnd | 加强后是否可拒绝或终止 | K.R.14, K.R.EXT.GOV.14.STOP |
| M.Step.G5.CddExemption | 列明主体免识别条件 | K.R.15, K.R.EXT.GOV.15.EXEMPT |
| M.Step.G5.SimplificationMeasure | 按具体主体分支选择措施 | K.R.15, K.R.EXT.GOV.15.SIMPLIFY |
| M.Step.G5.QueryAfterIdentification | 备案主体查询核对前提 | K.R.13, K.R.17, K.R.EXT.GOV.13.VERIFY |
| M.Step.G5.IdentityRights | 核实身份、权利及结构证据 | K.R.10, K.R.13, K.R.EXT.GOV.13.IDENTIFY, K.R.EXT.GOV.13.VERIFY |
| M.Step.G5.Risk | 风险及措施匹配判断 | K.R.07.RISK, K.R.14, K.R.15, K.R.EXT.GOV.14.STOP, K.R.EXT.GOV.15.SIMPLIFY, K.R.EXT.GOV.15.EXEMPT |
| M.Step.G5.RemainingRisk | 加强措施后的剩余风险判断 | K.R.14, K.R.EXT.GOV.14.STOP |
| M.Step.G5.Authority | 主体分类、用途授权和责任适用核查 | K.R.01, K.R.20, K.R.21, K.R.EXT.GOV.20.ACCESS, K.R.EXT.GOV.21.LIABILITY, K.R.EXT.GOV.15.EXEMPT, K.R.EXT.GOV.15.SIMPLIFY |
| M.Step.G6.QueryAfterIdentification | 备案主体查询核对前提 | K.R.13, K.R.17, K.R.EXT.GOV.13.VERIFY |
| M.Step.G6.DateYearMonth | 关系日期年月比较 | K.R.18, K.R.18.DATES |
| M.Step.G6.MaterialDifference | 差异重大性判断 | K.R.18, K.R.18.DATES |
| M.Step.G6.UpdateDue | 近期变化的法定更新截止 | K.R.18.PENDING |
| M.Step.G6.TimingPending | 时点性待更新标记 | K.R.18, K.R.18.PENDING |
| M.Step.G6.ReportRequired | 差异报告义务判断 | K.R.19, K.R.19.CORRECT |
| M.Step.G6.CorrectionAction | 按原因采取差异处置 | K.R.19, K.R.19.CORRECT |
| M.Step.G6.CloseDifference | 实际更正且复核一致后闭环 | K.R.19, K.R.19.CLOSE |
| M.Step.G6.DifferenceCause | 差异原因和更正后复核 | K.R.17, K.R.18, K.R.19, K.R.19.CORRECT, K.R.19.CLOSE |
| M.Step.G6.Difference | 差异实质处置 | K.R.19, K.R.19.CLOSE |
| M.Step.G7.Access | 查询用途及授权 | K.R.20, K.R.EXT.GOV.20.ACCESS |
| M.Step.G7.ReturnMode | 查询返回方式 | K.R.EXT.GOV.20.ACCESS |
| M.Step.G7.Transport | 传输保护条件 | K.R.EXT.GOV.20.TRANSPORT |
| M.Step.G7.Regime | 按时点选择制度 | K.R.21, K.R.EXT.GOV.21.TRANSITION |
| M.Step.G7.Authority | 主体分类、用途授权和责任适用核查 | K.R.01, K.R.20, K.R.21, K.R.EXT.GOV.20.ACCESS, K.R.EXT.GOV.21.LIABILITY, K.R.EXT.GOV.15.EXEMPT, K.R.EXT.GOV.15.SIMPLIFY |
| M.Step.G7.Liability | 责任类型及从轻减轻因素核查 | K.R.21, K.R.EXT.GOV.21.LIABILITY |
| M.Step.G8.FilingSubmit | 备案资料和人员关系完整后提交 | K.R.22 |
| M.Step.G8.FilingRoute | 地方办理方式和入口核对 | K.R.22 |
| M.Step.G9.QueryAllowed | 核验报文允许发送 | K.R.23, K.R.23.VERIFY |
| M.Step.G9.DailyStop | 本批次后是否停止后续核验 | K.R.23.VERIFY |
| M.Step.G9.QueryMatch | 反馈关联原请求 | K.R.23, K.R.23.CURRENT, K.R.23.HISTORY |
| M.Step.G9.QueryUsable | 逐主体业务结果可用 | K.R.23, K.R.23.VERIFY, K.R.23.CURRENT |
| M.Step.G9.CurrentQuery | 当前详情查询的核验流水前提 | K.R.23.CURRENT |
| M.Step.G9.ReportContent | 按报告类别检查内容和操作 | K.R.24, K.R.24.REPORT |
| M.Step.G9.ReportSubmit | 差异报告提交前提 | K.R.24, K.R.24.REPORT |
| M.Step.G9.CaseQuery | 案例编号取得后查询审批 | K.R.24.CASE |
| M.Step.G9.ParameterContinuity | 参数通知连续性 | K.R.24.PARAM |
| M.Step.G9.ParameterResend | 参数缺期请求补发 | K.R.24.PARAM |
| M.Step.G9.ParameterSend | 参数完整且业务受理才发送 | K.R.24.PARAM |
| M.Step.G9.FileUsable | 附件取得实际应答后可用 | K.R.24.FILE |
| M.Step.G9.Reverification | 失效流水重新核验 | K.R.23.CURRENT |
| M.Step.G9.Continuity | 历史完整性和总体资格连续判断 | K.R.11, K.R.11.HISTORY, K.R.23.HISTORY |
| M.Step.G9.Query | 查询异步反馈 | K.R.23, K.R.23.VERIFY, K.R.23.CURRENT |
| M.Step.G9.Report | 差异报告办理 | K.R.24, K.R.24.STATUS |
| M.Step.G9.Case | 案例申请和审批 | K.R.24.CASE |
| M.Step.G9.File | 附件上传与关联 | K.R.24.FILE |

## 全部业务字段

### M.Person / 自然人

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| document_kind | 证件种类 | Text | 必须一项 | 证件种类；资料不足时保留未知，不用默认值代替。 |
| document_number | 证件号码 | Text | 必须一项 | 证件号码；资料不足时保留未知，不用默认值代替。 |
| issuer | 证件签发国家或地区 | Text | 必须一项 | 证件签发国家或地区；资料不足时保留未知，不用默认值代替。 |
| name | 姓名 | Text | 可有一项；缺失时保留未知 | 姓名；资料不足时保留未知，不用默认值代替。 |
| nationality | 国籍或地区 | Text | 可有一项；缺失时保留未知 | 国籍或地区；资料不足时保留未知，不用默认值代替。 |
| birth_date | 出生日期 | Date | 可有一项；缺失时保留未知 | 出生日期；资料不足时保留未知，不用默认值代替。 |
| document_expiry | 证件有效期限 | Date | 可有一项；缺失时保留未知 | 证件有效期限；资料不足时保留未知，不用默认值代替。 |
| residence | 住所或经常居住地 | Text | 可有一项；缺失时保留未知 | 住所或经常居住地；资料不足时保留未知，不用默认值代替。 |
| contact | 联系方式 | Text | 可有一项；缺失时保留未知 | 联系方式；资料不足时保留未知，不用默认值代替。 |

### M.Subject / 非自然人主体

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| identifier_scheme | 登记或产品标识体系 | Text | 必须一项 | 登记或产品标识体系；资料不足时保留未知，不用默认值代替。 |
| identifier | 登记或产品标识 | Text | 必须一项 | 登记或产品标识；资料不足时保留未知，不用默认值代替。 |
| name | 主体名称 | Text | 可有一项；缺失时保留未知 | 主体名称；资料不足时保留未知，不用默认值代替。 |
| kind | 主体类型 | Enum | 可有一项；缺失时保留未知 | 主体类型；资料不足时保留未知，不用默认值代替。 |
| jurisdiction | 登记国家或地区 | Text | 可有一项；缺失时保留未知 | 登记国家或地区；资料不足时保留未知，不用默认值代替。 |
| locality | 办理地区 | Text | 可有一项；缺失时保留未知 | 办理地区；资料不足时保留未知，不用默认值代替。 |
| parent | 所属主体 | Ref → M.Subject | 可有一项；缺失时保留未知 | 所属主体；资料不足时保留未知，不用默认值代替。 |
| established_on | 设立日期 | Date | 可有一项；缺失时保留未知 | 设立日期；资料不足时保留未知，不用默认值代替。 |
| capital | 注册资本或出资额 | Decimal | 可有一项；缺失时保留未知 | 原币种金额；不得未确认折算口径就与人民币阈值比较。 |
| currency | 币种 | Text | 可有一项；缺失时保留未知 | 币种；资料不足时保留未知，不用默认值代替。 |
| capital_cny | 有依据折算的人民币出资额 | Decimal | 可有一项；缺失时保留未知 | 有依据折算的人民币出资额；资料不足时保留未知，不用默认值代替。 |
| trust_kind | 信托业务类别 | Enum | 可有一项；缺失时保留未知 | 信托业务类别；资料不足时保留未知，不用默认值代替。 |
| financial_category | 机构或组织性质 | Text | 可有一项；缺失时保留未知 | 机构或组织性质；资料不足时保留未知，不用默认值代替。 |
| product_kind | 产品类别 | Text | 可有一项；缺失时保留未知 | 产品类别；资料不足时保留未知，不用默认值代替。 |
| current_status | 登记状态 | Text | 可有一项；缺失时保留未知 | 登记状态；资料不足时保留未知，不用默认值代替。 |

### M.Evidence / 业务证据

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| source | 证据提供方或来源 | Text | 必须一项 | 证据提供方或来源；资料不足时保留未知，不用默认值代替。 |
| reference | 来源中的文档或记录标识 | Text | 必须一项 | 来源中的文档或记录标识；资料不足时保留未知，不用默认值代替。 |
| version | 证据版本或取得批次 | Text | 必须一项 | 证据版本或取得批次；资料不足时保留未知，不用默认值代替。 |
| kind | 证据类别 | Text | 可有一项；缺失时保留未知 | 证据类别；资料不足时保留未知，不用默认值代替。 |
| observed_at | 取得或观察时点 | DateTime | 可有一项；缺失时保留未知 | 取得或观察时点；资料不足时保留未知，不用默认值代替。 |
| effective_on | 证据所载业务生效日 | Date | 可有一项；缺失时保留未知 | 证据所载业务生效日；资料不足时保留未知，不用默认值代替。 |
| locator | 原文位置 | Text | 可有一项；缺失时保留未知 | 原文位置；资料不足时保留未知，不用默认值代替。 |
| supports | 支持的具体事实 | Text | 可有一项；缺失时保留未知 | 支持的具体事实；资料不足时保留未知，不用默认值代替。 |
| limitations | 证据局限 | Text | 可有一项；缺失时保留未知 | 证据局限；资料不足时保留未知，不用默认值代替。 |
| verified | 真实性与适用性已核验 | Boolean | 可有一项；缺失时保留未知 | 真实性与适用性已核验；资料不足时保留未知，不用默认值代替。 |

### M.Right / 持有权益

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| holder_key | 经核验的权利主体标识 | Text | 必须一项 | 与自然人或组织身份一致的权利人标识；两者只能选择一个，缺证时不能生成已确认持有关系。 |
| person | 自然人权利人 | Ref → M.Person | 可有一项；缺失时保留未知 | 自然人权利人；资料不足时保留未知，不用默认值代替。 |
| organization | 组织权利人 | Ref → M.Subject | 可有一项；缺失时保留未知 | 组织权利人；资料不足时保留未知，不用默认值代替。 |
| subject | 权益所指主体 | Ref → M.Subject | 必须一项 | 权益所指主体；资料不足时保留未知，不用默认值代替。 |
| right_kind | 权利类型 | Enum | 必须一项 | 权利类型；资料不足时保留未知，不用默认值代替。 |
| ratio | 权益比例 | Decimal | 可有一项；缺失时保留未知 | 以0到1的小数表示同一权利维度的直接比例；未知不作0，25%记0.25。 |
| denominator | 比例分母及权利范围 | Text | 可有一项；缺失时保留未知 | 比例分母及权利范围；资料不足时保留未知，不用默认值代替。 |
| start | 实际形成日期 | Date | 必须一项 | 实际形成日期；资料不足时保留未知，不用默认值代替。 |
| end | 实际终止日期 | Date | 可有一项；缺失时保留未知 | 实际终止日期；资料不足时保留未知，不用默认值代替。 |
| end_status | 终止信息情况 | Enum | 必须一项 | 尚未终止须有核实依据；未取得终止信息保留未知。 |
| evidence | 权利及生效证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 权利及生效证据；资料不足时保留未知，不用默认值代替。 |
| target_key | 权益目标业务身份键 | Text | 可有一项；缺失时保留未知 | 按目标主体的登记标识体系及标识确定的身份键；仅用于路径计算，须与subject的业务身份一致。 |

### M.Control / 实际控制关系

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| person | 控制自然人 | Ref → M.Person | 必须一项 | 控制自然人；资料不足时保留未知，不用默认值代替。 |
| subject | 被控制主体 | Ref → M.Subject | 必须一项 | 被控制主体；资料不足时保留未知，不用默认值代替。 |
| mode | 单独或联合控制 | Enum | 可有一项；缺失时保留未知 | 单独或联合控制；资料不足时保留未知，不用默认值代替。 |
| matters | 实际支配事项 | Text | 至少 0 项，不限最多数量 | 实际支配事项；资料不足时保留未知，不用默认值代替。 |
| arrangement | 控制安排及权利基础 | Text | 可有一项；缺失时保留未知 | 控制安排及权利基础；资料不足时保留未知，不用默认值代替。 |
| exercise | 实际行使事实 | Text | 可有一项；缺失时保留未知 | 实际行使事实；资料不足时保留未知，不用默认值代替。 |
| sustained | 持续和实质支配已核实 | Boolean | 可有一项；缺失时保留未知 | 持续和实质支配已核实；资料不足时保留未知，不用默认值代替。 |
| start | 实际形成日期 | Date | 必须一项 | 实际形成日期；资料不足时保留未知，不用默认值代替。 |
| end | 实际终止日期 | Date | 可有一项；缺失时保留未知 | 实际终止日期；资料不足时保留未知，不用默认值代替。 |
| end_status | 终止信息情况 | Enum | 必须一项 | 尚未终止须有核实依据；未取得终止信息保留未知。 |
| evidence | 控制证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 控制证据；资料不足时保留未知，不用默认值代替。 |

### M.Appointment / 任职关系

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| person | 任职自然人 | Ref → M.Person | 必须一项 | 任职自然人；资料不足时保留未知，不用默认值代替。 |
| subject | 任职主体 | Ref → M.Subject | 必须一项 | 任职主体；资料不足时保留未知，不用默认值代替。 |
| position | 职务或责任 | Enum | 必须一项 | 职务或责任；资料不足时保留未知，不用默认值代替。 |
| start | 实际形成日期 | Date | 必须一项 | 实际形成日期；资料不足时保留未知，不用默认值代替。 |
| end | 实际终止日期 | Date | 可有一项；缺失时保留未知 | 实际终止日期；资料不足时保留未知，不用默认值代替。 |
| end_status | 终止信息情况 | Enum | 必须一项 | 尚未终止须有核实依据；未取得终止信息保留未知。 |
| evidence | 任职或授权证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 任职或授权证据；资料不足时保留未知，不用默认值代替。 |

### M.Identification / 受益所有人识别

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| institution | 承担识别的机构 | Ref → M.Subject | 必须一项 | 承担识别的机构；资料不足时保留未知，不用默认值代替。 |
| reference | 本机构识别业务编号 | Text | 必须一项 | 本机构识别业务编号；资料不足时保留未知，不用默认值代替。 |
| subject | 被识别主体 | Ref → M.Subject | 必须一项 | 被识别主体；资料不足时保留未知，不用默认值代替。 |
| purpose | 识别用途 | Enum | 可有一项；缺失时保留未知 | 识别用途；资料不足时保留未知，不用默认值代替。 |
| as_of | 业务判断日期 | Date | 可有一项；缺失时保留未知 | 业务判断日期；资料不足时保留未知，不用默认值代替。 |
| known_at | 所用信息截止时点 | DateTime | 可有一项；缺失时保留未知 | 所用信息截止时点；资料不足时保留未知，不用默认值代替。 |
| reviewer | 复核责任人 | Ref → M.Appointment | 可有一项；缺失时保留未知 | 复核责任人；资料不足时保留未知，不用默认值代替。 |
| evidence | 采用证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 采用证据；资料不足时保留未知，不用默认值代替。 |
| state | 识别办理状态 | Enum | 必须一项 | 识别办理状态；资料不足时保留未知，不用默认值代替。 |
| institution_in_scope | 机构适用范围已核实 | Boolean | 可有一项；缺失时保留未知 | 机构适用范围已核实；资料不足时保留未知，不用默认值代替。 |
| business_relation | 已建立或拟建立客户业务关系 | Boolean | 可有一项；缺失时保留未知 | 已建立或拟建立客户业务关系；资料不足时保留未知，不用默认值代替。 |
| filing_applicable | 属于备案范围 | Boolean | 可有一项；缺失时保留未知 | 属于备案范围；资料不足时保留未知，不用默认值代替。 |
| cdd_applicable | 属于金融机构识别范围 | Boolean | 可有一项；缺失时保留未知 | 属于金融机构识别范围；资料不足时保留未知，不用默认值代替。 |
| structure_complete | 权利结构已完整核实 | Boolean | 可有一项；缺失时保留未知 | 权利结构已完整核实；资料不足时保留未知，不用默认值代替。 |
| acyclic | 结构无循环已核实 | Boolean | 可有一项；缺失时保留未知 | 结构无循环已核实；资料不足时保留未知，不用默认值代替。 |
| identity_verified | 个人身份已核实 | Boolean | 可有一项；缺失时保留未知 | 个人身份已核实；资料不足时保留未知，不用默认值代替。 |
| rights_verified | 权利状况已核实 | Boolean | 可有一项；缺失时保留未知 | 权利状况已核实；资料不足时保留未知，不用默认值代替。 |
| all_standards_checked | 前三项标准已全部核验 | Boolean | 可有一项；缺失时保留未知 | 前三项标准已全部核验；资料不足时保留未知，不用默认值代替。 |
| any_standard_positive | 存在按前三项标准认定的自然人 | Boolean | 可有一项；缺失时保留未知 | 存在按前三项标准认定的自然人；资料不足时保留未知，不用默认值代替。 |
| fallback_allowed | 可进入管理人员兜底 | Boolean | 可有一项；缺失时保留未知 | 可进入管理人员兜底；资料不足时保留未知，不用默认值代替。 |
| simple_structure | 结构简单已核实 | Boolean | 可有一项；缺失时保留未知 | 结构简单已核实；资料不足时保留未知，不用默认值代替。 |
| low_risk | 低风险已充分评估 | Boolean | 可有一项；缺失时保留未知 | 低风险已充分评估；资料不足时保留未知，不用默认值代替。 |
| risk20_triggered | 存在加强识别触发情形 | Boolean | 可有一项；缺失时保留未知 | 存在加强识别触发情形；资料不足时保留未知，不用默认值代替。 |
| data_doubt | 信息准确性或完整性存疑 | Boolean | 可有一项；缺失时保留未知 | 信息准确性或完整性存疑；资料不足时保留未知，不用默认值代替。 |
| risk_assessment_complete | 风险评估已完成 | Boolean | 可有一项；缺失时保留未知 | 风险评估已完成；资料不足时保留未知，不用默认值代替。 |
| exemption_allowed | 可免识别 | Boolean | 可有一项；缺失时保留未知 | 可免识别；资料不足时保留未知，不用默认值代替。 |
| simplification_allowed | 可简化识别 | Boolean | 可有一项；缺失时保留未知 | 可简化识别；资料不足时保留未知，不用默认值代替。 |
| higher_risk | 属于较高及以上风险 | Boolean | 可有一项；缺失时保留未知 | 属于较高及以上风险；资料不足时保留未知，不用默认值代替。 |
| enhanced_measures_completed | 加强措施已实施 | Boolean | 可有一项；缺失时保留未知 | 加强措施已实施；资料不足时保留未知，不用默认值代替。 |
| residual_risk_manageable | 剩余风险在管理能力内 | Boolean | 可有一项；缺失时保留未知 | 剩余风险在管理能力内；资料不足时保留未知，不用默认值代替。 |
| restrict_needed | 需要合理限制业务 | Boolean | 可有一项；缺失时保留未知 | 需要合理限制业务；资料不足时保留未知，不用默认值代替。 |
| refuse_or_end | 可拒绝或终止业务 | Boolean | 可有一项；缺失时保留未知 | 可拒绝或终止业务；资料不足时保留未知，不用默认值代替。 |
| history_complete | 历史材料完整已核实 | Boolean | 可有一项；缺失时保留未知 | 历史材料完整已核实；资料不足时保留未知，不用默认值代替。 |
| continuity_verified | 总体资格连续性已核实 | Boolean | 可有一项；缺失时保留未知 | 总体资格连续性已核实；资料不足时保留未知，不用默认值代替。 |
| decision_reason | 识别判断理由 | Text | 可有一项；缺失时保留未知 | 识别判断理由；资料不足时保留未知，不用默认值代替。 |
| branch | 识别分支 | Text | 可有一项；缺失时保留未知 | 识别分支；资料不足时保留未知，不用默认值代替。 |
| review_due | 补齐或复核期限 | Date | 可有一项；缺失时保留未知 | 补齐或复核期限；资料不足时保留未知，不用默认值代替。 |
| rights | 同一时点核实的直接权益集合 | Ref → M.Right | 至少 0 项，不限最多数量 | 同一时点核实的直接权益集合；未取得充分依据时保持未知。 |
| branch_reuse_verified | 本机构已对所属主体完成尽调 | Boolean | 可有一项；缺失时保留未知 | 本机构已对所属主体完成尽调；未取得充分依据时保持未知。 |
| branch_result | 分支机构识别路径 | Text | 可有一项；缺失时保留未知 | 分支机构识别路径；未取得充分依据时保持未知。 |
| exemption_category | 经可靠核实的免识别类别 | Enum | 可有一项；缺失时保留未知 | 经可靠核实的免识别类别；未取得充分依据时保持未知。 |
| category_verified | 主体类别及适用依据已可靠核实 | Boolean | 可有一项；缺失时保留未知 | 主体类别及适用依据已可靠核实；未取得充分依据时保持未知。 |
| simplification_category | 对应的简化分支 | Enum | 可有一项；缺失时保留未知 | 对应的简化分支；未取得充分依据时保持未知。 |
| simplification_measure | 对应的具体简化措施 | Text | 可有一项；缺失时保留未知 | 对应的具体简化措施；未取得充分依据时保持未知。 |
| matched_risk_measure | 所选简化措施与风险相匹配 | Boolean | 可有一项；缺失时保留未知 | 所选简化措施与风险相匹配；未取得充分依据时保持未知。 |
| enhanced_reasons | 已核实的加强识别触发原因 | Text | 至少 0 项，不限最多数量 | 已核实的加强识别触发原因；未取得充分依据时保持未知。 |
| enhanced_measures | 与具体风险相匹配的加强措施 | Text | 至少 0 项，不限最多数量 | 与具体风险相匹配的加强措施；未取得充分依据时保持未知。 |
| records_complete | 适用业务场景所需身份及权利信息齐备 | Boolean | 可有一项；缺失时保留未知 | 适用业务场景所需身份及权利信息齐备；未取得充分依据时保持未知。 |
| refresh_query_required | 备案主体需要查询核对 | Boolean | 可有一项；缺失时保留未知 | 备案主体需要查询核对；未取得充分依据时保持未知。 |
| local_routing | 备案办理入口已按实际所在地选定 | Boolean | 可有一项；缺失时保留未知 | 备案办理入口已按实际所在地选定；未取得充分依据时保持未知。 |

### M.BeneficialOwnership / 受益所有权关系

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| person | 受益所有人 | Ref → M.Person | 必须一项 | 受益所有人；资料不足时保留未知，不用默认值代替。 |
| subject | 关系所指主体 | Ref → M.Subject | 必须一项 | 关系所指主体；资料不足时保留未知，不用默认值代替。 |
| standard | 认定标准 | Enum | 必须一项 | 认定标准；资料不足时保留未知，不用默认值代替。 |
| identification | 形成判断的识别记录 | Ref → M.Identification | 必须一项 | 形成判断的识别记录；资料不足时保留未知，不用默认值代替。 |
| right_kind | 对应权利类型 | Text | 可有一项；缺失时保留未知 | 对应权利类型；资料不足时保留未知，不用默认值代替。 |
| start | 实际形成日期 | Date | 必须一项 | 实际形成日期；资料不足时保留未知，不用默认值代替。 |
| end | 实际终止日期 | Date | 可有一项；缺失时保留未知 | 实际终止日期；资料不足时保留未知，不用默认值代替。 |
| end_status | 终止信息情况 | Enum | 必须一项 | 尚未终止须有核实依据；未取得终止信息保留未知。 |
| evidence | 认定及日期证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 认定及日期证据；资料不足时保留未知，不用默认值代替。 |

### M.PersonAssessment / 个人认定结果

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| person | 本项判断所涉自然人 | Ref → M.Person | 必须一项 | 本项判断所涉自然人；资料不足时保留未知，不用默认值代替。 |
| standard1 | 标准一成立 | Boolean | 可有一项；缺失时保留未知 | 标准一成立；资料不足时保留未知，不用默认值代替。 |
| standard2 | 标准二成立 | Boolean | 可有一项；缺失时保留未知 | 标准二成立；资料不足时保留未知，不用默认值代替。 |
| standard3 | 标准三成立 | Boolean | 可有一项；缺失时保留未知 | 标准三成立；资料不足时保留未知，不用默认值代替。 |
| equity_ratio | 同一自然人最终股权或合伙权益比例 | Decimal | 可有一项；缺失时保留未知 | 同一自然人最终股权或合伙权益比例；资料不足时保留未知，不用默认值代替。 |
| income_ratio | 最终收益权比例 | Decimal | 可有一项；缺失时保留未知 | 最终收益权比例；资料不足时保留未知，不用默认值代替。 |
| voting_ratio | 最终表决权比例 | Decimal | 可有一项；缺失时保留未知 | 最终表决权比例；资料不足时保留未知，不用默认值代替。 |
| formation_date | 当前总体形成日期 | Date | 可有一项；缺失时保留未知 | 当前总体形成日期；资料不足时保留未知，不用默认值代替。 |
| recognized_standards | 采用的认定标准 | Text | 至少 0 项，不限最多数量 | 采用的认定标准；资料不足时保留未知，不用默认值代替。 |
| identification | 所属识别工作 | Ref → M.Identification | 必须一项 | 所属识别工作；资料不足时保留未知，不用默认值代替。 |
| as_of | 本项判断日期 | Date | 可有一项；缺失时保留未知 | 本项判断日期；资料不足时保留未知，不用默认值代替。 |
| control_verified | 实际控制已核实 | Boolean | 可有一项；缺失时保留未知 | 实际控制已核实；资料不足时保留未知，不用默认值代替。 |
| ownership_qualified | 按前三项标准达标 | Boolean | 可有一项；缺失时保留未知 | 按前三项标准达标；资料不足时保留未知，不用默认值代替。 |
| history_complete | 本人的历史关系已完整核实 | Boolean | 可有一项；缺失时保留未知 | 本人的历史关系已完整核实；资料不足时保留未知，不用默认值代替。 |
| continuity_verified | 本人的总体资格连续性已核实 | Boolean | 可有一项；缺失时保留未知 | 本人的总体资格连续性已核实；资料不足时保留未知，不用默认值代替。 |
| history | 已核实的历史受益所有权关系 | Ref → M.BeneficialOwnership | 至少 0 项，不限最多数量 | 已核实的历史受益所有权关系；资料不足时保留未知，不用默认值代替。 |
| reason | 本人的认定理由 | Text | 可有一项；缺失时保留未知 | 本人的认定理由；资料不足时保留未知，不用默认值代替。 |
| path_products | 有效无环路径比例乘积 | Decimal | 至少 0 项，不限最多数量 | 有效无环路径比例乘积；未取得充分依据时保持未知。 |
| income_path_products | 收益权路径比例乘积 | Decimal | 至少 0 项，不限最多数量 | 收益权路径比例乘积；未取得充分依据时保持未知。 |
| voting_path_products | 表决权路径比例乘积 | Decimal | 至少 0 项，不限最多数量 | 表决权路径比例乘积；未取得充分依据时保持未知。 |
| legal_start | 经证据核实的法律关系实际生效日期 | Date | 可有一项；缺失时保留未知 | 经证据核实的法律关系实际生效日期；未取得充分依据时保持未知。 |
| date_reason | 生效或连续日期的认定理由 | Text | 可有一项；缺失时保留未知 | 生效或连续日期的认定理由；未取得充分依据时保持未知。 |
| basis_evidence | 个人认定的支撑证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 个人认定的支撑证据；未取得充分依据时保持未知。 |
| uses_standard2 | 本人的认定采用标准二 | Boolean | 可有一项；缺失时保留未知 | 本人的认定采用标准二；未取得充分依据时保持未知。 |
| uses_standard3 | 本人的认定采用标准三 | Boolean | 可有一项；缺失时保留未知 | 本人的认定采用标准三；未取得充分依据时保持未知。 |
| known_equity_paths | 已证明有效的股权路径乘积 | Decimal | 至少 0 项，不限最多数量 | 已证明有效的股权路径乘积；未取得充分依据时保持未知。 |
| known_equity_lower_bound | 已证明股权比例下界 | Decimal | 可有一项；缺失时保留未知 | 已证明股权比例下界；未取得充分依据时保持未知。 |
| standard1_candidate | 已有证据支持的标准一候选 | Boolean | 可有一项；缺失时保留未知 | 已有证据支持的标准一候选；未取得充分依据时保持未知。 |

### M.StateNature / 国企性质认定

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| subject | 认定主体 | Ref → M.Subject | 必须一项 | 认定主体；资料不足时保留未知，不用默认值代替。 |
| as_of | 性质判断日期 | Date | 必须一项 | 性质判断日期；资料不足时保留未知，不用默认值代替。 |
| state_investor | 国有出资人 | Ref → M.Subject | 可有一项；缺失时保留未知 | 国有出资人；资料不足时保留未知，不用默认值代替。 |
| state_ratio | 国有持股比例 | Decimal | 可有一项；缺失时保留未知 | 国有持股比例；资料不足时保留未知，不用默认值代替。 |
| qualified_investor | 出资人身份符合相应条款 | Boolean | 可有一项；缺失时保留未知 | 出资人身份符合相应条款；资料不足时保留未知，不用默认值代替。 |
| largest_shareholder | 属于第一大股东 | Boolean | 可有一项；缺失时保留未知 | 属于第一大股东；资料不足时保留未知，不用默认值代替。 |
| actual_dominance | 国有主体实际支配已核实 | Boolean | 可有一项；缺失时保留未知 | 国有主体实际支配已核实；资料不足时保留未知，不用默认值代替。 |
| officially_verified | 企业性质已有可靠官方依据 | Boolean | 可有一项；缺失时保留未知 | 企业性质已有可靠官方依据；资料不足时保留未知，不用默认值代替。 |
| article4_4 | 第四条第四项条件成立 | Boolean | 可有一项；缺失时保留未知 | 第四条第四项条件成立；资料不足时保留未知，不用默认值代替。 |
| relative_holding | 按已确认口径属于国有相对控股 | Boolean | 可有一项；缺失时保留未知 | 按已确认口径属于国有相对控股；资料不足时保留未知，不用默认值代替。 |
| cdd_branch_applicable | 符合金融机构简化的主体范围 | Boolean | 可有一项；缺失时保留未知 | 符合金融机构简化的主体范围；资料不足时保留未知，不用默认值代替。 |
| filing_branch_applicable | 符合备案简化的主体范围 | Boolean | 可有一项；缺失时保留未知 | 符合备案简化的主体范围；资料不足时保留未知，不用默认值代替。 |
| nature | 认定的企业性质 | Text | 可有一项；缺失时保留未知 | 认定的企业性质；资料不足时保留未知，不用默认值代替。 |
| reason | 性质认定理由 | Text | 可有一项；缺失时保留未知 | 性质认定理由；资料不足时保留未知，不用默认值代替。 |
| evidence | 性质及实际支配证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 性质及实际支配证据；资料不足时保留未知，不用默认值代替。 |

### M.Filing / 受益所有人备案

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| subject | 备案主体 | Ref → M.Subject | 必须一项 | 备案主体；资料不足时保留未知，不用默认值代替。 |
| reference | 备案办理编号 | Text | 必须一项 | 备案办理编号；资料不足时保留未知，不用默认值代替。 |
| method | 办理方式 | Enum | 可有一项；缺失时保留未知 | 办理方式；资料不足时保留未知，不用默认值代替。 |
| trigger | 备案触发 | Enum | 可有一项；缺失时保留未知 | 备案触发；资料不足时保留未知，不用默认值代替。 |
| trigger_date | 起算事件实际日期 | Date | 可有一项；缺失时保留未知 | 起算事件实际日期；资料不足时保留未知，不用默认值代替。 |
| due_date | 备案或更新截止日期 | Date | 可有一项；缺失时保留未知 | 备案或更新截止日期；资料不足时保留未知，不用默认值代替。 |
| filing_date | 实际提交日期 | Date | 可有一项；缺失时保留未知 | 实际提交日期；资料不足时保留未知，不用默认值代替。 |
| receipt | 登记系统结果回执 | Text | 可有一项；缺失时保留未知 | 登记系统结果回执；资料不足时保留未知，不用默认值代替。 |
| capital_cny | 有依据核实的人民币注册资本或出资额 | Decimal | 可有一项；缺失时保留未知 | 有依据核实的人民币注册资本或出资额；资料不足时保留未知，不用默认值代替。 |
| all_natural_holders | 全部股东或合伙人均为自然人 | Boolean | 可有一项；缺失时保留未知 | 全部股东或合伙人均为自然人；资料不足时保留未知，不用默认值代替。 |
| no_external_beneficiary | 不存在股东合伙人以外自然人控制或获益 | Boolean | 可有一项；缺失时保留未知 | 不存在股东合伙人以外自然人控制或获益；资料不足时保留未知，不用默认值代替。 |
| no_other_control_benefit | 不存在股权合伙权益以外控制或获益方式 | Boolean | 可有一项；缺失时保留未知 | 不存在股权合伙权益以外控制或获益方式；资料不足时保留未知，不用默认值代替。 |
| promise_truthful | 承诺真实且条件已核验 | Boolean | 可有一项；缺失时保留未知 | 承诺真实且条件已核验；资料不足时保留未知，不用默认值代替。 |
| promise_exempt | 符合承诺免报 | Boolean | 可有一项；缺失时保留未知 | 符合承诺免报；资料不足时保留未知，不用默认值代替。 |
| online_synchronous | 线上设立已同步办理 | Boolean | 可有一项；缺失时保留未知 | 线上设立已同步办理；资料不足时保留未知，不用默认值代替。 |
| all_people_recorded | 全部应报自然人已录入 | Boolean | 可有一项；缺失时保留未知 | 全部应报自然人已录入；资料不足时保留未知，不用默认值代替。 |
| all_relations_recorded | 应报关系类别和日期已录入 | Boolean | 可有一项；缺失时保留未知 | 应报关系类别和日期已录入；资料不足时保留未知，不用默认值代替。 |
| submission_checked | 填报检查已完成 | Boolean | 可有一项；缺失时保留未知 | 填报检查已完成；资料不足时保留未知，不用默认值代替。 |
| state | 备案办理状态 | Enum | 必须一项 | 备案办理状态；资料不足时保留未知，不用默认值代替。 |
| evidence | 备案材料和回执依据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 备案材料和回执依据；资料不足时保留未知，不用默认值代替。 |
| as_of | 备案判断日期 | Date | 可有一项；缺失时保留未知 | 备案判断日期；未取得充分依据时保持未知。 |
| can_submit | 可提交备案 | Boolean | 可有一项；缺失时保留未知 | 可提交备案；未取得充分依据时保持未知。 |

### M.TrustParty / 信托当事人

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| trust | 信托 | Ref → M.Subject | 必须一项 | 信托；资料不足时保留未知，不用默认值代替。 |
| party_key | 当事人或已确定受益范围标识 | Text | 必须一项 | 当事人或已确定受益范围标识；资料不足时保留未知，不用默认值代替。 |
| role | 当事人类别 | Enum | 必须一项 | 当事人类别；资料不足时保留未知，不用默认值代替。 |
| person | 自然人当事人 | Ref → M.Person | 可有一项；缺失时保留未知 | 自然人当事人；资料不足时保留未知，不用默认值代替。 |
| organization | 组织当事人 | Ref → M.Subject | 可有一项；缺失时保留未知 | 组织当事人；资料不足时保留未知，不用默认值代替。 |
| beneficiary_scope | 尚未确定受益人时的受益范围 | Text | 可有一项；缺失时保留未知 | 尚未确定受益人时的受益范围；资料不足时保留未知，不用默认值代替。 |
| person_identified | 具体自然人已确定 | Boolean | 可有一项；缺失时保留未知 | 具体自然人已确定；资料不足时保留未知，不用默认值代替。 |
| lookthrough_complete | 组织当事人穿透已完成 | Boolean | 可有一项；缺失时保留未知 | 组织当事人穿透已完成；资料不足时保留未知，不用默认值代替。 |
| evidence | 信托及当事人证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 信托及当事人证据；资料不足时保留未知，不用默认值代替。 |

### M.ProductAssessment / 产品识别判断

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| identification | 产品识别工作 | Ref → M.Identification | 必须一项 | 产品识别工作；资料不足时保留未知，不用默认值代替。 |
| product | 产品或信托 | Ref → M.Subject | 必须一项 | 产品或信托；资料不足时保留未知，不用默认值代替。 |
| manager | 管理或受托机构 | Ref → M.Subject | 可有一项；缺失时保留未知 | 管理或受托机构；资料不足时保留未知，不用默认值代替。 |
| managing_people | 实际管理产品的自然人 | Ref → M.Person | 至少 0 项，不限最多数量 | 实际管理产品的自然人；资料不足时保留未知，不用默认值代替。 |
| financial_manager | 管理或受托方属于适用金融机构 | Boolean | 可有一项；缺失时保留未知 | 管理或受托方属于适用金融机构；资料不足时保留未知，不用默认值代替。 |
| public_offering | 公开募集或发行条件成立 | Boolean | 可有一项；缺失时保留未知 | 公开募集或发行条件成立；资料不足时保留未知，不用默认值代替。 |
| registered | 依法备案条件成立 | Boolean | 可有一项；缺失时保留未知 | 依法备案条件成立；资料不足时保留未知，不用默认值代替。 |
| service_in_scope | 服务场景属于适用范围 | Boolean | 可有一项；缺失时保留未知 | 服务场景属于适用范围；资料不足时保留未知，不用默认值代替。 |
| simple_structure | 信托结构简单 | Boolean | 可有一项；缺失时保留未知 | 信托结构简单；资料不足时保留未知，不用默认值代替。 |
| low_risk | 风险已充分评估为低 | Boolean | 可有一项；缺失时保留未知 | 风险已充分评估为低；资料不足时保留未知，不用默认值代替。 |
| simplify_allowed | 可按对应条款简化 | Boolean | 可有一项；缺失时保留未知 | 可按对应条款简化；资料不足时保留未知，不用默认值代替。 |
| manager_system_sound | 管理受托机构制度健全 | Boolean | 可有一项；缺失时保留未知 | 管理受托机构制度健全；资料不足时保留未知，不用默认值代替。 |
| manager_duties_effective | 已有效履行识别义务 | Boolean | 可有一项；缺失时保留未知 | 已有效履行识别义务；资料不足时保留未知，不用默认值代替。 |
| doubts | 所得信息存在疑点 | Boolean | 可有一项；缺失时保留未知 | 所得信息存在疑点；资料不足时保留未知，不用默认值代替。 |
| uncooperative | 管理方不配合 | Boolean | 可有一项；缺失时保留未知 | 管理方不配合；资料不足时保留未知，不用默认值代替。 |
| serious_violation | 存在严重违法情形 | Boolean | 可有一项；缺失时保留未知 | 存在严重违法情形；资料不足时保留未知，不用默认值代替。 |
| major_risk | 存在重大风险 | Boolean | 可有一项；缺失时保留未知 | 存在重大风险；资料不足时保留未知，不用默认值代替。 |
| reliance_allowed | 可采信管理方识别结果 | Boolean | 可有一项；缺失时保留未知 | 可采信管理方识别结果；资料不足时保留未知，不用默认值代替。 |
| branch | 所选一般或简化分支 | Text | 可有一项；缺失时保留未知 | 所选一般或简化分支；资料不足时保留未知，不用默认值代替。 |
| reason | 适用和采信理由 | Text | 可有一项；缺失时保留未知 | 适用和采信理由；资料不足时保留未知，不用默认值代替。 |
| evidence | 评估及沟通证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 评估及沟通证据；资料不足时保留未知，不用默认值代替。 |
| risk_assessment_complete | 产品风险已充分评估 | Boolean | 可有一项；缺失时保留未知 | 产品风险已充分评估；未取得充分依据时保持未知。 |
| manager_people_identified | 实际管理自然人已具体识别 | Boolean | 可有一项；缺失时保留未知 | 实际管理自然人已具体识别；未取得充分依据时保持未知。 |
| professional_info_retained | 专业服务人员基本信息已留存 | Boolean | 可有一项；缺失时保留未知 | 专业服务人员基本信息已留存；未取得充分依据时保持未知。 |
| trust_parties | 已核实的信托当事人关系 | Ref → M.TrustParty | 至少 0 项，不限最多数量 | 已核实的信托当事人关系；未取得充分依据时保持未知。 |
| trust_party_scope_complete | 信托各类当事人和其他控制人范围完整 | Boolean | 可有一项；缺失时保留未知 | 信托各类当事人和其他控制人范围完整；未取得充分依据时保持未知。 |
| trust_lookthrough_complete | 组织当事人穿透完整 | Boolean | 可有一项；缺失时保留未知 | 组织当事人穿透完整；未取得充分依据时保持未知。 |
| full_trust_identification | 完整信托识别条件满足 | Boolean | 可有一项；缺失时保留未知 | 完整信托识别条件满足；未取得充分依据时保持未知。 |

### M.Difference / 受益所有人信息差异

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| identification | 产生差异的识别工作 | Ref → M.Identification | 必须一项 | 产生差异的识别工作；资料不足时保留未知，不用默认值代替。 |
| reference | 本次差异编号 | Text | 必须一项 | 本次差异编号；资料不足时保留未知，不用默认值代替。 |
| field_name | 差异字段 | Text | 可有一项；缺失时保留未知 | 差异字段；资料不足时保留未知，不用默认值代替。 |
| institution_value | 机构经核实的信息 | Text | 可有一项；缺失时保留未知 | 机构经核实的信息；资料不足时保留未知，不用默认值代替。 |
| filing_value | 备案信息 | Text | 可有一项；缺失时保留未知 | 备案信息；资料不足时保留未知，不用默认值代替。 |
| institution_date | 机构认定的关系日期 | Date | 可有一项；缺失时保留未知 | 机构认定的关系日期；资料不足时保留未知，不用默认值代替。 |
| filing_date | 备案记载的关系日期 | Date | 可有一项；缺失时保留未知 | 备案记载的关系日期；资料不足时保留未知，不用默认值代替。 |
| actual_change_date | 实际变化日期 | Date | 可有一项；缺失时保留未知 | 实际变化日期；资料不足时保留未知，不用默认值代替。 |
| as_of | 差异核对日期 | Date | 可有一项；缺失时保留未知 | 差异核对日期；资料不足时保留未知，不用默认值代替。 |
| update_due | 法定更新期限届满日 | Date | 可有一项；缺失时保留未知 | 法定更新期限届满日；资料不足时保留未知，不用默认值代替。 |
| cause | 差异成因 | Enum | 可有一项；缺失时保留未知 | 差异成因；资料不足时保留未知，不用默认值代替。 |
| people_mismatch | 人员存在差异 | Boolean | 可有一项；缺失时保留未知 | 人员存在差异；资料不足时保留未知，不用默认值代替。 |
| key_rights_mismatch | 关键权利状况存在差异 | Boolean | 可有一项；缺失时保留未知 | 关键权利状况存在差异；资料不足时保留未知，不用默认值代替。 |
| year_month_mismatch | 关系日期年月存在差异 | Boolean | 可有一项；缺失时保留未知 | 关系日期年月存在差异；资料不足时保留未知，不用默认值代替。 |
| affects_ubo | 差异影响受益所有人认定 | Boolean | 可有一项；缺失时保留未知 | 差异影响受益所有人认定；资料不足时保留未知，不用默认值代替。 |
| other_major_branch | 其他列明重大差异条件成立 | Boolean | 可有一项；缺失时保留未知 | 其他列明重大差异条件成立；资料不足时保留未知，不用默认值代替。 |
| material | 属于重大差异 | Boolean | 可有一项；缺失时保留未知 | 属于重大差异；资料不足时保留未知，不用默认值代替。 |
| timing_pending | 仍处法定期限的时点性待更新 | Boolean | 可有一项；缺失时保留未知 | 仍处法定期限的时点性待更新；资料不足时保留未知，不用默认值代替。 |
| customer_corrected | 客户已实际更正 | Boolean | 可有一项；缺失时保留未知 | 客户已实际更正；资料不足时保留未知，不用默认值代替。 |
| recheck_consistent | 再次核验或查询比对一致 | Boolean | 可有一项；缺失时保留未知 | 再次核验或查询比对一致；资料不足时保留未知，不用默认值代替。 |
| closure_allowed | 符合已解决差异条件 | Boolean | 可有一项；缺失时保留未知 | 符合已解决差异条件；资料不足时保留未知，不用默认值代替。 |
| report_required | 需要差异报告 | Boolean | 可有一项；缺失时保留未知 | 需要差异报告；资料不足时保留未知，不用默认值代替。 |
| correction_evidence | 实际更正证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 实际更正证据；资料不足时保留未知，不用默认值代替。 |
| recheck_evidence | 复核一致证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 复核一致证据；资料不足时保留未知，不用默认值代替。 |
| reason | 重大性和处置理由 | Text | 可有一项；缺失时保留未知 | 重大性和处置理由；资料不足时保留未知，不用默认值代替。 |
| state | 实质处置状态 | Enum | 必须一项 | 实质处置状态；资料不足时保留未知，不用默认值代替。 |
| correction_action | 应采取的差异处置 | Text | 可有一项；缺失时保留未知 | 应采取的差异处置；未取得充分依据时保持未知。 |
| matched_query | 复核对应的查询 | Ref → M.Query | 可有一项；缺失时保留未知 | 复核对应的查询；未取得充分依据时保持未知。 |

### M.Access / 信息查询授权

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| institution | 使用机构 | Ref → M.Subject | 必须一项 | 使用机构；资料不足时保留未知，不用默认值代替。 |
| authorization_reference | 授权依据标识 | Text | 必须一项 | 授权依据标识；资料不足时保留未知，不用默认值代替。 |
| operator | 授权经办人 | Ref → M.Appointment | 可有一项；缺失时保留未知 | 授权经办人；资料不足时保留未知，不用默认值代替。 |
| purpose | 具体查询用途 | Text | 可有一项；缺失时保留未知 | 具体查询用途；资料不足时保留未知，不用默认值代替。 |
| lawful_purpose | 用途属于法定职责或反洗钱义务 | Boolean | 可有一项；缺失时保留未知 | 用途属于法定职责或反洗钱义务；资料不足时保留未知，不用默认值代替。 |
| institution_authorized | 机构具有查询权限 | Boolean | 可有一项；缺失时保留未知 | 机构具有查询权限；资料不足时保留未知，不用默认值代替。 |
| operator_authorized | 经办授权有效 | Boolean | 可有一项；缺失时保留未知 | 经办授权有效；资料不足时保留未知，不用默认值代替。 |
| declaration_verified | 非掩码查询声明条件已核实 | Boolean | 可有一项；缺失时保留未知 | 非掩码查询声明条件已核实；资料不足时保留未知，不用默认值代替。 |
| allowed | 允许该次查询 | Boolean | 可有一项；缺失时保留未知 | 允许该次查询；资料不足时保留未知，不用默认值代替。 |
| authenticated | 通信及访问身份认证通过 | Boolean | 可有一项；缺失时保留未知 | 通信及访问身份认证通过；资料不足时保留未知，不用默认值代替。 |
| signature_valid | 签名验签通过 | Boolean | 可有一项；缺失时保留未知 | 签名验签通过；资料不足时保留未知，不用默认值代替。 |
| encrypted_transport | 按接口要求加密传输 | Boolean | 可有一项；缺失时保留未知 | 按接口要求加密传输；资料不足时保留未知，不用默认值代替。 |
| document_envelope | 证件号按要求使用数字信封 | Boolean | 可有一项；缺失时保留未知 | 证件号按要求使用数字信封；资料不足时保留未知，不用默认值代替。 |
| transport_allowed | 本次传输保护条件满足 | Boolean | 可有一项；缺失时保留未知 | 本次传输保护条件满足；资料不足时保留未知，不用默认值代替。 |
| allowed_scope | 授权数据及后续使用范围 | Text | 可有一项；缺失时保留未知 | 授权数据及后续使用范围；资料不足时保留未知，不用默认值代替。 |
| return_mode | 允许的返回方式 | Enum | 可有一项；缺失时保留未知 | 允许的返回方式；资料不足时保留未知，不用默认值代替。 |
| evidence | 授权和法定用途依据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 授权和法定用途依据；资料不足时保留未知，不用默认值代替。 |

### M.Query / 备案信息查询

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| institution | 请求机构 | Ref → M.Subject | 必须一项 | 请求机构；资料不足时保留未知，不用默认值代替。 |
| request_reference | 请求业务流水 | Text | 必须一项 | 请求业务流水；资料不足时保留未知，不用默认值代替。 |
| authorization | 本次查询授权 | Ref → M.Access | 可有一项；缺失时保留未知 | 本次查询授权；资料不足时保留未知，不用默认值代替。 |
| subjects | 请求主体 | Ref → M.Subject | 至少 0 项，不限最多数量 | 请求主体；资料不足时保留未知，不用默认值代替。 |
| kind | 查询种类 | Enum | 可有一项；缺失时保留未知 | 查询种类；资料不足时保留未知，不用默认值代替。 |
| subject_count | 请求主体数量 | Integer | 可有一项；缺失时保留未知 | 请求主体数量；资料不足时保留未知，不用默认值代替。 |
| quota | 有效参数规定的额度 | Integer | 可有一项；缺失时保留未知 | 有效参数规定的额度；资料不足时保留未知，不用默认值代替。 |
| response_reference | 反馈关联的请求流水 | Text | 可有一项；缺失时保留未知 | 反馈关联的请求流水；资料不足时保留未知，不用默认值代替。 |
| verification_reference | 有效核验流水 | Text | 可有一项；缺失时保留未知 | 有效核验流水；资料不足时保留未知，不用默认值代替。 |
| feedback_business_id | 业务反馈标识 | Text | 可有一项；缺失时保留未知 | 业务反馈标识；资料不足时保留未知，不用默认值代替。 |
| sent_at | 请求发出时点 | DateTime | 可有一项；缺失时保留未知 | 请求发出时点；资料不足时保留未知，不用默认值代替。 |
| received_at | 业务反馈收到时点 | DateTime | 可有一项；缺失时保留未知 | 业务反馈收到时点；资料不足时保留未知，不用默认值代替。 |
| filing_status | 逐主体备案状态 | Text | 可有一项；缺失时保留未知 | 逐主体备案状态；资料不足时保留未知，不用默认值代替。 |
| current_information | 逐主体返回信息说明 | Text | 可有一项；缺失时保留未知 | 逐主体返回信息说明；资料不足时保留未知，不用默认值代替。 |
| historical_period | 请求历史范围 | Text | 可有一项；缺失时保留未知 | 请求历史范围；资料不足时保留未知，不用默认值代替。 |
| parameters_current | 参数版本完整有效 | Boolean | 可有一项；缺失时保留未知 | 参数版本完整有效；资料不足时保留未知，不用默认值代替。 |
| accepted | 报文已被接收 | Boolean | 可有一项；缺失时保留未知 | 报文已被接收；资料不足时保留未知，不用默认值代替。 |
| feedback_received | 业务反馈已收到 | Boolean | 可有一项；缺失时保留未知 | 业务反馈已收到；资料不足时保留未知，不用默认值代替。 |
| feedback_matched | 反馈与原请求一致 | Boolean | 可有一项；缺失时保留未知 | 反馈与原请求一致；资料不足时保留未知，不用默认值代替。 |
| per_subject_complete | 逐主体结果已完整收到 | Boolean | 可有一项；缺失时保留未知 | 逐主体结果已完整收到；资料不足时保留未知，不用默认值代替。 |
| query_allowed | 允许发出该查询 | Boolean | 可有一项；缺失时保留未知 | 允许发出该查询；资料不足时保留未知，不用默认值代替。 |
| result_usable | 结果可用于后续核对 | Boolean | 可有一项；缺失时保留未知 | 结果可用于后续核对；资料不足时保留未知，不用默认值代替。 |
| filing_present | 已明确存在备案 | Boolean | 可有一项；缺失时保留未知 | 已明确存在备案；资料不足时保留未知，不用默认值代替。 |
| history_reconciled | 备案历史与实际生效证据已对照 | Boolean | 可有一项；缺失时保留未知 | 备案历史与实际生效证据已对照；资料不足时保留未知，不用默认值代替。 |
| state | 查询办理状态 | Enum | 必须一项 | 查询办理状态；资料不足时保留未知，不用默认值代替。 |
| evidence | 请求及反馈原文 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 请求及反馈原文；资料不足时保留未知，不用默认值代替。 |
| daily_used_before | 本次请求前当日已核验主体数 | Integer | 可有一项；缺失时保留未知 | 本次请求前当日已核验主体数；未取得充分依据时保持未知。 |
| batch | 采用批量核验 | Boolean | 可有一项；缺失时保留未知 | 采用批量核验；未取得充分依据时保持未知。 |
| triggers_daily_stop | 本批次后达到或超过当日额度 | Boolean | 可有一项；缺失时保留未知 | 本批次后达到或超过当日额度；未取得充分依据时保持未知。 |
| format_logic_valid | 格式及逻辑校验通过 | Boolean | 可有一项；缺失时保留未知 | 格式及逻辑校验通过；未取得充分依据时保持未知。 |
| business_feedback_success | 逐主体业务反馈有效 | Boolean | 可有一项；缺失时保留未知 | 逐主体业务反馈有效；未取得充分依据时保持未知。 |
| independent_identification_complete | 本机构独立识别已完成 | Boolean | 可有一项；缺失时保留未知 | 本机构独立识别已完成；未取得充分依据时保持未知。 |
| verification_valid | 核验流水在本次查询时仍有效 | Boolean | 可有一项；缺失时保留未知 | 核验流水在本次查询时仍有效；未取得充分依据时保持未知。 |
| reverification_required | 需要重新核验以取得有效流水 | Boolean | 可有一项；缺失时保留未知 | 需要重新核验以取得有效流水；未取得充分依据时保持未知。 |

### M.DifferenceReport / 差异报告

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| institution | 报告机构 | Ref → M.Subject | 必须一项 | 报告机构；资料不足时保留未知，不用默认值代替。 |
| reference | 报告业务标识 | Text | 必须一项 | 报告业务标识；资料不足时保留未知，不用默认值代替。 |
| difference | 关联差异 | Ref → M.Difference | 可有一项；缺失时保留未知 | 关联差异；资料不足时保留未知，不用默认值代替。 |
| kind | 报告业务类别 | Enum | 可有一项；缺失时保留未知 | 报告业务类别；资料不足时保留未知，不用默认值代替。 |
| operation | 本次报文操作 | Enum | 可有一项；缺失时保留未知 | 本次报文操作；资料不足时保留未知，不用默认值代替。 |
| subtype | 接口具体报告类型 | Enum | 可有一项；缺失时保留未知 | 接口具体报告类型；资料不足时保留未知，不用默认值代替。 |
| feedback_reference | 反馈关联报告标识 | Text | 可有一项；缺失时保留未知 | 反馈关联报告标识；资料不足时保留未知，不用默认值代替。 |
| feedback_status | 系统业务反馈状态 | Text | 可有一项；缺失时保留未知 | 系统业务反馈状态；资料不足时保留未知，不用默认值代替。 |
| type_supported | 具体类型与当前接口允许范围一致 | Boolean | 可有一项；缺失时保留未知 | 具体类型与当前接口允许范围一致；资料不足时保留未知，不用默认值代替。 |
| required_content_complete | 具体类型所需内容齐备 | Boolean | 可有一项；缺失时保留未知 | 具体类型所需内容齐备；资料不足时保留未知，不用默认值代替。 |
| attachments_usable | 应附文件已取得可用标识 | Boolean | 可有一项；缺失时保留未知 | 应附文件已取得可用标识；资料不足时保留未知，不用默认值代替。 |
| submit_allowed | 可提交当前报告 | Boolean | 可有一项；缺失时保留未知 | 可提交当前报告；资料不足时保留未知，不用默认值代替。 |
| withdraw_allowed | 当前状态允许撤销 | Boolean | 可有一项；缺失时保留未知 | 当前状态允许撤销；资料不足时保留未知，不用默认值代替。 |
| withdraw_feedback | 已收到撤销业务反馈 | Boolean | 可有一项；缺失时保留未知 | 已收到撤销业务反馈；资料不足时保留未知，不用默认值代替。 |
| termination_feedback | 已收到终止业务反馈 | Boolean | 可有一项；缺失时保留未知 | 已收到终止业务反馈；资料不足时保留未知，不用默认值代替。 |
| next_action | 反馈要求的下一步 | Text | 可有一项；缺失时保留未知 | 反馈要求的下一步；资料不足时保留未知，不用默认值代替。 |
| state | 报告办理状态 | Enum | 必须一项 | 报告办理状态；资料不足时保留未知，不用默认值代替。 |
| evidence | 报告与反馈证据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 报告与反馈证据；资料不足时保留未知，不用默认值代替。 |
| subject_in_system | 主体在系统中 | Boolean | 可有一项；缺失时保留未知 | 主体在系统中；未取得充分依据时保持未知。 |
| system_people_empty | 系统中人员为空 | Boolean | 可有一项；缺失时保留未知 | 系统中人员为空；未取得充分依据时保持未知。 |
| promise_or_state_condition | 承诺免报或国有公司对应条件成立 | Boolean | 可有一项；缺失时保留未知 | 承诺免报或国有公司对应条件成立；未取得充分依据时保持未知。 |
| subject_code_present | 主体代码齐备 | Boolean | 可有一项；缺失时保留未知 | 主体代码齐备；未取得充分依据时保持未知。 |
| analysis_present | 分析报告齐备 | Boolean | 可有一项；缺失时保留未知 | 分析报告齐备；未取得充分依据时保持未知。 |
| support_present | 佐证材料齐备 | Boolean | 可有一项；缺失时保留未知 | 佐证材料齐备；未取得充分依据时保持未知。 |
| old_person_present | 原人员信息齐备 | Boolean | 可有一项；缺失时保留未知 | 原人员信息齐备；未取得充分依据时保持未知。 |
| new_person_present | 新人员信息齐备 | Boolean | 可有一项；缺失时保留未知 | 新人员信息齐备；未取得充分依据时保持未知。 |
| new_person_name_present | 新增人员姓名齐备 | Boolean | 可有一项；缺失时保留未知 | 新增人员姓名齐备；未取得充分依据时保持未知。 |
| organization_change | 提交企业信息变更 | Boolean | 可有一项；缺失时保留未知 | 提交企业信息变更；未取得充分依据时保持未知。 |
| person_change | 提交人员变更 | Boolean | 可有一项；缺失时保留未知 | 提交人员变更；未取得充分依据时保持未知。 |
| verification_consistent | 核验结果一致 | Boolean | 可有一项；缺失时保留未知 | 核验结果一致；未取得充分依据时保持未知。 |
| nonmajor_policy_confirmed | 非重大接口报备实施口径已确认 | Boolean | 可有一项；缺失时保留未知 | 非重大接口报备实施口径已确认；未取得充分依据时保持未知。 |

### M.BomisCase / 案例申请

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| institution | 申请机构 | Ref → M.Subject | 必须一项 | 申请机构；资料不足时保留未知，不用默认值代替。 |
| request_reference | 申请请求标识 | Text | 必须一项 | 申请请求标识；资料不足时保留未知，不用默认值代替。 |
| report | 相关差异报告 | Ref → M.DifferenceReport | 可有一项；缺失时保留未知 | 相关差异报告；资料不足时保留未知，不用默认值代替。 |
| case_number | 系统返回案例编号 | Text | 可有一项；缺失时保留未知 | 系统返回案例编号；资料不足时保留未知，不用默认值代替。 |
| approval_result | 实际审批结果 | Text | 可有一项；缺失时保留未知 | 实际审批结果；资料不足时保留未知，不用默认值代替。 |
| conditions_met | 申请条件已核实符合 | Boolean | 可有一项；缺失时保留未知 | 申请条件已核实符合；资料不足时保留未知，不用默认值代替。 |
| initial_feedback | 首个反馈已收到 | Boolean | 可有一项；缺失时保留未知 | 首个反馈已收到；资料不足时保留未知，不用默认值代替。 |
| number_received | 案例编号已收到 | Boolean | 可有一项；缺失时保留未知 | 案例编号已收到；资料不足时保留未知，不用默认值代替。 |
| approval_feedback | 审批反馈已收到 | Boolean | 可有一项；缺失时保留未知 | 审批反馈已收到；资料不足时保留未知，不用默认值代替。 |
| may_query_approval | 可继续查询审批 | Boolean | 可有一项；缺失时保留未知 | 可继续查询审批；资料不足时保留未知，不用默认值代替。 |
| state | 案例办理状态 | Enum | 必须一项 | 案例办理状态；资料不足时保留未知，不用默认值代替。 |
| evidence | 申请和审批反馈 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 申请和审批反馈；资料不足时保留未知，不用默认值代替。 |
| original_request_reference | 重复申请所关联的原请求标识 | Text | 可有一项；缺失时保留未知 | 重复申请所关联的原请求标识；未取得充分依据时保持未知。 |
| duplicate_rejected | 系统明确拒绝重复申请 | Boolean | 可有一项；缺失时保留未知 | 系统明确拒绝重复申请；未取得充分依据时保持未知。 |

### M.FileTransfer / 附件传输

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| institution | 传输机构 | Ref → M.Subject | 必须一项 | 传输机构；资料不足时保留未知，不用默认值代替。 |
| transfer_reference | 文件传输请求标识 | Text | 必须一项 | 文件传输请求标识；资料不足时保留未知，不用默认值代替。 |
| file_digest | 实际文件内容摘要 | Text | 可有一项；缺失时保留未知 | 实际文件内容摘要；资料不足时保留未知，不用默认值代替。 |
| file_identifier | 上传应答返回的文件标识 | Text | 可有一项；缺失时保留未知 | 上传应答返回的文件标识；资料不足时保留未知，不用默认值代替。 |
| response_reference | 应答关联传输标识 | Text | 可有一项；缺失时保留未知 | 应答关联传输标识；资料不足时保留未知，不用默认值代替。 |
| synchronous_error | 同步错误信息 | Text | 可有一项；缺失时保留未知 | 同步错误信息；资料不足时保留未知，不用默认值代替。 |
| asynchronous_error | 异步错误信息 | Text | 可有一项；缺失时保留未知 | 异步错误信息；资料不足时保留未知，不用默认值代替。 |
| response_received | 实际上传业务应答已收到 | Boolean | 可有一项；缺失时保留未知 | 实际上传业务应答已收到；资料不足时保留未知，不用默认值代替。 |
| response_matched | 应答对应本次传输 | Boolean | 可有一项；缺失时保留未知 | 应答对应本次传输；资料不足时保留未知，不用默认值代替。 |
| file_id_received | 已取得真实文件标识 | Boolean | 可有一项；缺失时保留未知 | 已取得真实文件标识；资料不足时保留未知，不用默认值代替。 |
| usable | 附件可关联业务 | Boolean | 可有一项；缺失时保留未知 | 附件可关联业务；资料不足时保留未知，不用默认值代替。 |
| state | 附件办理状态 | Enum | 必须一项 | 附件办理状态；资料不足时保留未知，不用默认值代替。 |
| evidence | 原始报文与应答 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 原始报文与应答；资料不足时保留未知，不用默认值代替。 |
| original_transfer_reference | 重复上传所关联的首次传输标识 | Text | 可有一项；缺失时保留未知 | 重复上传所关联的首次传输标识；未取得充分依据时保持未知。 |
| duplicate_rejected | 系统明确反馈重复传输 | Boolean | 可有一项；缺失时保留未知 | 系统明确反馈重复传输；未取得充分依据时保持未知。 |

### M.Parameters / 业务参数接收

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| institution | 接收机构 | Ref → M.Subject | 必须一项 | 接收机构；资料不足时保留未知，不用默认值代替。 |
| sequence | 本次通知序号 | Integer | 必须一项 | 本次通知序号；资料不足时保留未知，不用默认值代替。 |
| previous_sequence | 已采用的前次通知序号 | Integer | 可有一项；缺失时保留未知 | 已采用的前次通知序号；资料不足时保留未知，不用默认值代替。 |
| received_at | 接收时点 | DateTime | 可有一项；缺失时保留未知 | 接收时点；资料不足时保留未知，不用默认值代替。 |
| business_accepting | 业务处于受理状态 | Boolean | 可有一项；缺失时保留未知 | 业务处于受理状态；资料不足时保留未知，不用默认值代替。 |
| sequence_continuous | 通知序号连续 | Boolean | 可有一项；缺失时保留未知 | 通知序号连续；资料不足时保留未知，不用默认值代替。 |
| resend_needed | 需要申请补发 | Boolean | 可有一项；缺失时保留未知 | 需要申请补发；资料不足时保留未知，不用默认值代替。 |
| send_allowed | 允许发送业务 | Boolean | 可有一项；缺失时保留未知 | 允许发送业务；资料不足时保留未知，不用默认值代替。 |
| quota | 通知给定业务额度 | Integer | 可有一项；缺失时保留未知 | 通知给定业务额度；资料不足时保留未知，不用默认值代替。 |
| evidence | 通知及补发应答 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 通知及补发应答；资料不足时保留未知，不用默认值代替。 |
| initial_snapshot_verified | 首次完整参数快照已核实 | Boolean | 可有一项；缺失时保留未知 | 首次完整参数快照已核实；未取得充分依据时保持未知。 |

### M.Followup / 复核与补充任务

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| institution | 承担任务的机构 | Ref → M.Subject | 必须一项 | 承担任务的机构；资料不足时保留未知，不用默认值代替。 |
| reference | 机构内任务编号 | Text | 必须一项 | 机构内任务编号；资料不足时保留未知，不用默认值代替。 |
| subject | 任务主体 | Ref → M.Subject | 可有一项；缺失时保留未知 | 任务主体；资料不足时保留未知，不用默认值代替。 |
| identification | 相关识别工作 | Ref → M.Identification | 可有一项；缺失时保留未知 | 相关识别工作；资料不足时保留未知，不用默认值代替。 |
| difference | 相关差异 | Ref → M.Difference | 可有一项；缺失时保留未知 | 相关差异；资料不足时保留未知，不用默认值代替。 |
| kind | 任务类型 | Enum | 可有一项；缺失时保留未知 | 任务类型；资料不足时保留未知，不用默认值代替。 |
| trigger | 触发事件 | Text | 可有一项；缺失时保留未知 | 触发事件；资料不足时保留未知，不用默认值代替。 |
| trigger_date | 触发日期 | Date | 可有一项；缺失时保留未知 | 触发日期；资料不足时保留未知，不用默认值代替。 |
| due_date | 有明确依据的截止日期 | Date | 可有一项；缺失时保留未知 | 有明确依据的截止日期；资料不足时保留未知，不用默认值代替。 |
| review_date | 已确定的复核日期 | Date | 可有一项；缺失时保留未知 | 已确定的复核日期；资料不足时保留未知，不用默认值代替。 |
| owner | 已落实责任人 | Ref → M.Appointment | 可有一项；缺失时保留未知 | 已落实责任人；资料不足时保留未知，不用默认值代替。 |
| may_affect_ownership | 事件可能影响受益所有权 | Boolean | 可有一项；缺失时保留未知 | 事件可能影响受益所有权；资料不足时保留未知，不用默认值代替。 |
| review_required | 需要启动复核 | Boolean | 可有一项；缺失时保留未知 | 需要启动复核；资料不足时保留未知，不用默认值代替。 |
| update_required | 核实后需要更新 | Boolean | 可有一项；缺失时保留未知 | 核实后需要更新；资料不足时保留未知，不用默认值代替。 |
| legacy_customer | 属于存量客户 | Boolean | 可有一项；缺失时保留未知 | 属于存量客户；资料不足时保留未知，不用默认值代替。 |
| higher_risk | 属于较高及以上风险 | Boolean | 可有一项；缺失时保留未知 | 属于较高及以上风险；资料不足时保留未知，不用默认值代替。 |
| inactive_or_restricted | 账户不动或严格限制 | Boolean | 可有一项；缺失时保留未知 | 账户不动或严格限制；资料不足时保留未知，不用默认值代替。 |
| activated | 账户已激活或发生办理 | Boolean | 可有一项；缺失时保留未知 | 账户已激活或发生办理；资料不足时保留未知，不用默认值代替。 |
| deferral_allowed | 可适用激活时补齐例外 | Boolean | 可有一项；缺失时保留未知 | 可适用激活时补齐例外；资料不足时保留未知，不用默认值代替。 |
| missing_items | 待补内容 | Text | 至少 0 项，不限最多数量 | 待补内容；资料不足时保留未知，不用默认值代替。 |
| unresolved_policy | 尚未确定的内部跟踪口径 | Text | 可有一项；缺失时保留未知 | 尚未确定的内部跟踪口径；资料不足时保留未知，不用默认值代替。 |
| state | 任务状态 | Enum | 必须一项 | 任务状态；资料不足时保留未知，不用默认值代替。 |
| evidence | 事件、期限及完成依据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 事件、期限及完成依据；资料不足时保留未知，不用默认值代替。 |
| regime_start | 制度施行起算日 | Date | 可有一项；缺失时保留未知 | 制度施行起算日；未取得充分依据时保持未知。 |

### M.ComplianceReview / 适用制度与责任核查

| 字段 | 业务名称 | 类型与目标 | 基数 | 含义 |
| --- | --- | --- | --- | --- |
| subject | 核查主体 | Ref → M.Subject | 必须一项 | 核查主体；资料不足时保留未知，不用默认值代替。 |
| reference | 核查记录标识 | Text | 必须一项 | 核查记录标识；资料不足时保留未知，不用默认值代替。 |
| as_of | 适用业务日期 | Date | 可有一项；缺失时保留未知 | 适用业务日期；资料不足时保留未知，不用默认值代替。 |
| regime | 适用制度版本 | Text | 可有一项；缺失时保留未知 | 适用制度版本；资料不足时保留未知，不用默认值代替。 |
| duty_kind | 相关义务类型 | Enum | 可有一项；缺失时保留未知 | 相关义务类型；资料不足时保留未知，不用默认值代替。 |
| violation_type | 发现的责任风险类型 | Text | 可有一项；缺失时保留未知 | 发现的责任风险类型；资料不足时保留未知，不用默认值代替。 |
| mitigation | 从轻或减轻因素 | Text | 可有一项；缺失时保留未知 | 从轻或减轻因素；资料不足时保留未知，不用默认值代替。 |
| rectification | 整改要求 | Text | 可有一项；缺失时保留未知 | 整改要求；资料不足时保留未知，不用默认值代替。 |
| legal_sources_complete | 处罚适用所需法律材料齐备 | Boolean | 可有一项；缺失时保留未知 | 处罚适用所需法律材料齐备；资料不足时保留未知，不用默认值代替。 |
| review_complete | 责任适用核查已完成 | Boolean | 可有一项；缺失时保留未知 | 责任适用核查已完成；资料不足时保留未知，不用默认值代替。 |
| evidence | 适用制度与事实依据 | Ref → M.Evidence | 至少 0 项，不限最多数量 | 适用制度与事实依据；资料不足时保留未知，不用默认值代替。 |
| applicable_regime | 按时点选择的适用制度 | Text | 可有一项；缺失时保留未知 | 按时点选择的适用制度；未取得充分依据时保持未知。 |


## 字段绑定与依赖

### M.Rule.FilingScope / 判断备案适用范围

前序规则：

输出字段：M.Identification.filing_applicable

表达式：((date ≥ "2024-11-01") 且 包含(列表("公司"，"合伙企业"，"外国公司分支机构")，kind))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| kind | 主体类型 | Enum | M.Subject.kind |
| date | 业务判断日期 | Date | M.Identification.as_of |

### M.Rule.CddScope / 判断金融机构识别适用范围

前序规则：

输出字段：M.Identification.cdd_applicable

表达式：((date ≥ "2026-01-20") 且 非((kind = "个体工商户")) 且 institution 且 relation)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| kind | 主体类型 | Enum | M.Subject.kind |
| date | 业务判断日期 | Date | M.Identification.as_of |
| institution | 机构适用范围已核实 | Boolean | M.Identification.institution_in_scope |
| relation | 已建立或拟建立客户业务关系 | Boolean | M.Identification.business_relation |

### M.Rule.FilingExemption / 承诺免报条件

前序规则：

输出字段：M.Filing.promise_exempt

表达式：(包含(列表("公司"，"合伙企业")，kind) 且 (date ≥ "2024-11-01") 且 (capital ≤ 10000000.0) 且 all_natural 且 no_external 且 no_other 且 truthful)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| kind | 主体类型 | Enum | M.Subject.kind |
| date | 备案判断日期 | Date | M.Filing.as_of |
| capital | 有依据核实的人民币注册资本或出资额 | Decimal | M.Filing.capital_cny |
| all_natural | 全部股东或合伙人均为自然人 | Boolean | M.Filing.all_natural_holders |
| no_external | 不存在股东合伙人以外自然人控制或获益 | Boolean | M.Filing.no_external_beneficiary |
| no_other | 不存在股权合伙权益以外控制或获益方式 | Boolean | M.Filing.no_other_control_benefit |
| truthful | 承诺真实且条件已核验 | Boolean | M.Filing.promise_truthful |

### M.Rule.EquityPaths / 股权或合伙权益路径逐条乘算

前序规则：

输出字段：M.PersonAssessment.path_products

表达式：无环路径逐条连乘(从 rights 中逐项取 edge，满足 (包含(列表("股权"，"合伙权益")，edge.right_kind) 且 若 (edge.end_status = "UNKNOWN")，则 null，否则 ((edge.start ≤ date) 且 ((edge.end_status = "OPEN") 或 (edge.end > date))))，得到 edge，业务身份键(person)，业务身份键(subject)，"holder_key"，"target_key"，"ratio")

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| rights | 同一时点核实的直接权益集合 | Ref | M.Identification.rights |
| date | 本项判断日期 | Date | M.PersonAssessment.as_of |
| person | 本项判断所涉自然人 | Ref | M.PersonAssessment.person |
| subject | 被识别主体 | Ref | M.Identification.subject |

### M.Rule.EquityTotal / 股权或合伙权益多路径合计

前序规则：M.Rule.EquityPaths

输出字段：M.PersonAssessment.equity_ratio

表达式：若 (complete 且 acyclic)，则 求和(paths)，否则 null

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| paths | 有效无环路径比例乘积 | Decimal | M.PersonAssessment.path_products |
| complete | 权利结构已完整核实 | Boolean | M.Identification.structure_complete |
| acyclic | 结构无循环已核实 | Boolean | M.Identification.acyclic |

### M.Rule.IncomePaths / 收益权路径逐条乘算

前序规则：

输出字段：M.PersonAssessment.income_path_products

表达式：无环路径逐条连乘(从 rights 中逐项取 edge，满足 (包含(列表("收益权")，edge.right_kind) 且 若 (edge.end_status = "UNKNOWN")，则 null，否则 ((edge.start ≤ date) 且 ((edge.end_status = "OPEN") 或 (edge.end > date))))，得到 edge，业务身份键(person)，业务身份键(subject)，"holder_key"，"target_key"，"ratio")

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| rights | 同一时点核实的直接权益集合 | Ref | M.Identification.rights |
| date | 本项判断日期 | Date | M.PersonAssessment.as_of |
| person | 本项判断所涉自然人 | Ref | M.PersonAssessment.person |
| subject | 被识别主体 | Ref | M.Identification.subject |

### M.Rule.IncomeTotal / 收益权多路径合计

前序规则：M.Rule.IncomePaths

输出字段：M.PersonAssessment.income_ratio

表达式：若 (complete 且 acyclic)，则 求和(paths)，否则 null

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| paths | 收益权路径比例乘积 | Decimal | M.PersonAssessment.income_path_products |
| complete | 权利结构已完整核实 | Boolean | M.Identification.structure_complete |
| acyclic | 结构无循环已核实 | Boolean | M.Identification.acyclic |

### M.Rule.VotingPaths / 表决权路径逐条乘算

前序规则：

输出字段：M.PersonAssessment.voting_path_products

表达式：无环路径逐条连乘(从 rights 中逐项取 edge，满足 (包含(列表("表决权")，edge.right_kind) 且 若 (edge.end_status = "UNKNOWN")，则 null，否则 ((edge.start ≤ date) 且 ((edge.end_status = "OPEN") 或 (edge.end > date))))，得到 edge，业务身份键(person)，业务身份键(subject)，"holder_key"，"target_key"，"ratio")

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| rights | 同一时点核实的直接权益集合 | Ref | M.Identification.rights |
| date | 本项判断日期 | Date | M.PersonAssessment.as_of |
| person | 本项判断所涉自然人 | Ref | M.PersonAssessment.person |
| subject | 被识别主体 | Ref | M.Identification.subject |

### M.Rule.VotingTotal / 表决权多路径合计

前序规则：M.Rule.VotingPaths

输出字段：M.PersonAssessment.voting_ratio

表达式：若 (complete 且 acyclic)，则 求和(paths)，否则 null

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| paths | 表决权路径比例乘积 | Decimal | M.PersonAssessment.voting_path_products |
| complete | 权利结构已完整核实 | Boolean | M.Identification.structure_complete |
| acyclic | 结构无循环已核实 | Boolean | M.Identification.acyclic |

### M.Rule.Standard1 / 按股权或合伙权益标准认定

前序规则：M.Rule.EquityTotal

输出字段：M.PersonAssessment.standard1

表达式：(ratio ≥ 0.25)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| ratio | 同一自然人最终股权或合伙权益比例 | Decimal | M.PersonAssessment.equity_ratio |

### M.Rule.Standard2 / 按收益权或表决权标准认定

前序规则：M.Rule.IncomeTotal, M.Rule.VotingTotal

输出字段：M.PersonAssessment.standard2

表达式：((income ≥ 0.25) 或 (vote ≥ 0.25))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| income | 最终收益权比例 | Decimal | M.PersonAssessment.income_ratio |
| vote | 最终表决权比例 | Decimal | M.PersonAssessment.voting_ratio |

### M.Rule.Standard3 / 按实际控制标准认定

前序规则：

输出字段：M.PersonAssessment.standard3

表达式：control

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| control | 实际控制已核实 | Boolean | M.PersonAssessment.control_verified |

### M.Rule.PersonQualified / 汇总该自然人的达标情况

前序规则：M.Rule.Standard1, M.Rule.Standard2, M.Rule.Standard3

输出字段：M.PersonAssessment.ownership_qualified

表达式：(one 或 two 或 three)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| one | 标准一成立 | Boolean | M.PersonAssessment.standard1 |
| two | 标准二成立 | Boolean | M.PersonAssessment.standard2 |
| three | 标准三成立 | Boolean | M.PersonAssessment.standard3 |

### M.Rule.UseStandard2 / 本人优先采用标准一后的标准二

前序规则：M.Rule.Standard1, M.Rule.Standard2

输出字段：M.PersonAssessment.uses_standard2

表达式：(非(one) 且 two)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| one | 标准一成立 | Boolean | M.PersonAssessment.standard1 |
| two | 标准二成立 | Boolean | M.PersonAssessment.standard2 |

### M.Rule.UseStandard3 / 本人优先采用标准一后的标准三

前序规则：M.Rule.Standard1, M.Rule.Standard3

输出字段：M.PersonAssessment.uses_standard3

表达式：(非(one) 且 three)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| one | 标准一成立 | Boolean | M.PersonAssessment.standard1 |
| three | 标准三成立 | Boolean | M.PersonAssessment.standard3 |

### M.Rule.Fallback / 是否可以采用管理人员兜底

前序规则：

输出字段：M.Identification.fallback_allowed

表达式：(checked 且 complete 且 非(positive))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| checked | 前三项标准已全部核验 | Boolean | M.Identification.all_standards_checked |
| complete | 权利结构已完整核实 | Boolean | M.Identification.structure_complete |
| positive | 存在按前三项标准认定的自然人 | Boolean | M.Identification.any_standard_positive |

### M.Rule.Article44 / 第四条第四项性质条件

前序规则：

输出字段：M.StateNature.article4_4

表达式：(investor 且 (ratio ≤ 0.5) 且 largest 且 dominance)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| investor | 出资人身份符合相应条款 | Boolean | M.StateNature.qualified_investor |
| ratio | 国有持股比例 | Decimal | M.StateNature.state_ratio |
| largest | 属于第一大股东 | Boolean | M.StateNature.largest_shareholder |
| dominance | 国有主体实际支配已核实 | Boolean | M.StateNature.actual_dominance |

### M.Rule.RelativeHolding / 衔接国有相对控股口径

前序规则：M.Rule.Article44

输出字段：M.StateNature.relative_holding

表达式：nature

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| nature | 第四条第四项条件成立 | Boolean | M.StateNature.article4_4 |

### M.Rule.StateApplicability / 金融机构国企简化主体范围

前序规则：M.Rule.RelativeHolding

输出字段：M.StateNature.cdd_branch_applicable

表达式：(official 且 (relative 或 包含(列表("国有独资公司"，"国有控股公司"，"全民所有制企业"，"集体所有制企业"，"联营企业")，nature)))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| relative | 按已确认口径属于国有相对控股 | Boolean | M.StateNature.relative_holding |
| nature | 认定的企业性质 | Text | M.StateNature.nature |
| official | 企业性质已有可靠官方依据 | Boolean | M.StateNature.officially_verified |

### M.Rule.StateSimplification / 国企简化风险门控

前序规则：M.Rule.StateApplicability

输出字段：M.Identification.simplification_allowed

表达式：(applicable 且 risk_complete 且 非(trigger) 且 非(doubt) 且 matched)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| applicable | 符合金融机构简化的主体范围 | Boolean | M.StateNature.cdd_branch_applicable |
| risk_complete | 风险评估已完成 | Boolean | M.Identification.risk_assessment_complete |
| trigger | 存在加强识别触发情形 | Boolean | M.Identification.risk20_triggered |
| doubt | 信息准确性或完整性存疑 | Boolean | M.Identification.data_doubt |
| matched | 所选简化措施与风险相匹配 | Boolean | M.Identification.matched_risk_measure |

### M.Rule.BranchRoute / 分支机构识别路径

前序规则：

输出字段：M.Identification.branch_result

表达式：若 (kind = "国内分支机构")，则 若 reused，则 "沿用本机构已完成尽调的所属主体结果"，否则 "先对所属主体完成识别核实"，否则 若 (kind = "外国公司分支机构")，则 "穿透所属外国公司并加入分支机构高级管理人员"，否则 "非本规则分支"

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| kind | 主体类型 | Enum | M.Subject.kind |
| reused | 本机构已对所属主体完成尽调 | Boolean | M.Identification.branch_reuse_verified |

### M.Rule.TrustFull / 完整信托当事人识别

前序规则：

输出字段：M.ProductAssessment.full_trust_identification

表达式：(scope 且 lookthrough)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| scope | 信托各类当事人和其他控制人范围完整 | Boolean | M.ProductAssessment.trust_party_scope_complete |
| lookthrough | 组织当事人穿透完整 | Boolean | M.ProductAssessment.trust_lookthrough_complete |

### M.Rule.TrustSimplification / 信托类型和风险分支

前序规则：

输出字段：M.ProductAssessment.simplify_allowed

表达式：(((kind = "其他资产服务信托") 且 simple 且 low 且 risk) 且 非(risk_block) 且 非(data_doubt))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| kind | 信托业务类别 | Enum | M.Subject.trust_kind |
| simple | 信托结构简单 | Boolean | M.ProductAssessment.simple_structure |
| low | 风险已充分评估为低 | Boolean | M.ProductAssessment.low_risk |
| risk | 产品风险已充分评估 | Boolean | M.ProductAssessment.risk_assessment_complete |
| risk_block | 存在加强识别触发情形 | Boolean | M.Identification.risk20_triggered |
| data_doubt | 信息准确性或完整性存疑 | Boolean | M.Identification.data_doubt |

### M.Rule.AssetSimplification / 资管产品简化条件

前序规则：

输出字段：M.ProductAssessment.simplify_allowed

表达式：((manager 且 service 且 risk 且 people 且 ((public 且 registered) 或 low)) 且 非(risk_block) 且 非(data_doubt))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| manager | 管理或受托方属于适用金融机构 | Boolean | M.ProductAssessment.financial_manager |
| public | 公开募集或发行条件成立 | Boolean | M.ProductAssessment.public_offering |
| registered | 依法备案条件成立 | Boolean | M.ProductAssessment.registered |
| service | 服务场景属于适用范围 | Boolean | M.ProductAssessment.service_in_scope |
| risk | 产品风险已充分评估 | Boolean | M.ProductAssessment.risk_assessment_complete |
| low | 风险已充分评估为低 | Boolean | M.ProductAssessment.low_risk |
| people | 实际管理自然人已具体识别 | Boolean | M.ProductAssessment.manager_people_identified |
| risk_block | 存在加强识别触发情形 | Boolean | M.Identification.risk20_triggered |
| data_doubt | 信息准确性或完整性存疑 | Boolean | M.Identification.data_doubt |

### M.Rule.ManagerReliance / 是否可采信管理受托机构结果

前序规则：

输出字段：M.ProductAssessment.reliance_allowed

表达式：(sound 且 effective 且 非(doubt) 且 非(uncooperative) 且 非(violation) 且 非(major))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| sound | 管理受托机构制度健全 | Boolean | M.ProductAssessment.manager_system_sound |
| effective | 已有效履行识别义务 | Boolean | M.ProductAssessment.manager_duties_effective |
| doubt | 所得信息存在疑点 | Boolean | M.ProductAssessment.doubts |
| uncooperative | 管理方不配合 | Boolean | M.ProductAssessment.uncooperative |
| violation | 存在严重违法情形 | Boolean | M.ProductAssessment.serious_violation |
| major | 存在重大风险 | Boolean | M.ProductAssessment.major_risk |

### M.Rule.Formation / 当前总体形成日期

前序规则：

输出字段：M.PersonAssessment.formation_date

表达式：当前连续区间起点(形成时间区间(从 history 中逐项取 relation，满足 ((业务身份键(relation.person) = 业务身份键(person)) 且 (业务身份键(relation.subject) = 业务身份键(subject)))，得到 relation，"start"，"end"，"end_status")，date，complete，continuity)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| history | 已核实的历史受益所有权关系 | Ref | M.PersonAssessment.history |
| date | 本项判断日期 | Date | M.PersonAssessment.as_of |
| complete | 本人的历史关系已完整核实 | Boolean | M.PersonAssessment.history_complete |
| continuity | 本人的总体资格连续性已核实 | Boolean | M.PersonAssessment.continuity_verified |
| person | 本项判断所涉自然人 | Ref | M.PersonAssessment.person |
| subject | 被识别主体 | Ref | M.Identification.subject |

### M.Rule.FilingDue / 备案及更新期限

前序规则：

输出字段：M.Filing.due_date

表达式：若 (trigger = "线上设立")，则 date，否则 若 (trigger = "存量备案")，则 "2025-11-01"，否则 日期加天数(date，30)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| trigger | 备案触发 | Enum | M.Filing.trigger |
| date | 起算事件实际日期 | Date | M.Filing.trigger_date |

### M.Rule.LegacyDeferral / 存量客户激活例外

前序规则：

输出字段：M.Followup.deferral_allowed

表达式：若 已取得值(higher)，则 (legacy 且 inactive 且 非(activated))，否则 null

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| legacy | 属于存量客户 | Boolean | M.Followup.legacy_customer |
| inactive | 账户不动或严格限制 | Boolean | M.Followup.inactive_or_restricted |
| activated | 账户已激活或发生办理 | Boolean | M.Followup.activated |
| higher | 属于较高及以上风险 | Boolean | M.Followup.higher_risk |

### M.Rule.LegacyDue / 存量客户补齐期限

前序规则：

输出字段：M.Followup.due_date

表达式：若 legacy，则 若 inactive，则 若 activated，则 activation_date，否则 null，否则 日期加月数("2026-01-20"，若 high，则 6，否则 24)，否则 null

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| legacy | 属于存量客户 | Boolean | M.Followup.legacy_customer |
| inactive | 账户不动或严格限制 | Boolean | M.Followup.inactive_or_restricted |
| activated | 账户已激活或发生办理 | Boolean | M.Followup.activated |
| high | 属于较高及以上风险 | Boolean | M.Followup.higher_risk |
| activation_date | 触发日期 | Date | M.Followup.trigger_date |

### M.Rule.RefuseOrEnd / 加强后是否可拒绝或终止

前序规则：

输出字段：M.Identification.refuse_or_end

表达式：(done 且 非(manageable))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| done | 加强措施已实施 | Boolean | M.Identification.enhanced_measures_completed |
| manageable | 剩余风险在管理能力内 | Boolean | M.Identification.residual_risk_manageable |

### M.Rule.CddExemption / 列明主体免识别条件

前序规则：

输出字段：M.Identification.exemption_allowed

表达式：(非((category = "不属于列明类别")) 且 verified 且 非(trigger) 且 非(doubt))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| category | 经可靠核实的免识别类别 | Enum | M.Identification.exemption_category |
| verified | 主体类别及适用依据已可靠核实 | Boolean | M.Identification.category_verified |
| trigger | 存在加强识别触发情形 | Boolean | M.Identification.risk20_triggered |
| doubt | 信息准确性或完整性存疑 | Boolean | M.Identification.data_doubt |

### M.Rule.SimplificationMeasure / 按具体主体分支选择措施

前序规则：

输出字段：M.Identification.simplification_measure

表达式：若 (verified 且 risk 且 matched 且 非(trigger) 且 非(doubt) 且 非((category = "不属于列明类别")) 且 (包含(列表("国有独资或国有控股等列明企业"，"国有参股公司"，"人民银行另行规定且已有依据")，category) 或 非(higher)))，则 若 (category = "非法人专业服务机构")，则 "可以认定机构负责人"，否则 若 (category = "合作经济组织法人")，则 "参照一般标准后可以认定法定代表人"，否则 若 (category = "个人独资企业")，则 "可以认定投资人"，否则 若 (category = "合格境外投资者")，则 "可以认定法定代表人、授权代表或相关业务负责人"，否则 若 (category = "国有独资或国有控股等列明企业")，则 "另经国企性质及风险链条后可以认定法定代表人"，否则 若 (category = "国有参股公司")，则 "一般识别中仅可不再识别国有资本部分"，否则 "按具体条款及风险确定识别措施"，否则 "不得采用该简化分支"

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| category | 对应的简化分支 | Enum | M.Identification.simplification_category |
| verified | 主体类别及适用依据已可靠核实 | Boolean | M.Identification.category_verified |
| risk | 风险评估已完成 | Boolean | M.Identification.risk_assessment_complete |
| higher | 属于较高及以上风险 | Boolean | M.Identification.higher_risk |
| trigger | 存在加强识别触发情形 | Boolean | M.Identification.risk20_triggered |
| doubt | 信息准确性或完整性存疑 | Boolean | M.Identification.data_doubt |
| matched | 所选简化措施与风险相匹配 | Boolean | M.Identification.matched_risk_measure |

### M.Rule.ReviewTrigger / 变更事件触发复核

前序规则：

输出字段：M.Followup.review_required

表达式：impact

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| impact | 事件可能影响受益所有权 | Boolean | M.Followup.may_affect_ownership |

### M.Rule.QueryAfterIdentification / 备案主体查询核对前提

前序规则：

输出字段：M.Identification.refresh_query_required

表达式：(applicable 且 identity 且 rights)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| applicable | 属于备案范围 | Boolean | M.Identification.filing_applicable |
| identity | 个人身份已核实 | Boolean | M.Identification.identity_verified |
| rights | 权利状况已核实 | Boolean | M.Identification.rights_verified |

### M.Rule.DateYearMonth / 关系日期年月比较

前序规则：

输出字段：M.Difference.year_month_mismatch

表达式：((日期年份(ours) ≠ 日期年份(filing)) 或 (日期月份(ours) ≠ 日期月份(filing)))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| ours | 机构认定的关系日期 | Date | M.Difference.institution_date |
| filing | 备案记载的关系日期 | Date | M.Difference.filing_date |

### M.Rule.MaterialDifference / 差异重大性判断

前序规则：M.Rule.DateYearMonth

输出字段：M.Difference.material

表达式：(people 或 rights 或 year_month 或 impact 或 other)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| people | 人员存在差异 | Boolean | M.Difference.people_mismatch |
| rights | 关键权利状况存在差异 | Boolean | M.Difference.key_rights_mismatch |
| year_month | 关系日期年月存在差异 | Boolean | M.Difference.year_month_mismatch |
| impact | 差异影响受益所有人认定 | Boolean | M.Difference.affects_ubo |
| other | 其他列明重大差异条件成立 | Boolean | M.Difference.other_major_branch |

### M.Rule.UpdateDue / 近期变化的法定更新截止

前序规则：

输出字段：M.Difference.update_due

表达式：日期加天数(change，30)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| change | 实际变化日期 | Date | M.Difference.actual_change_date |

### M.Rule.TimingPending / 时点性待更新标记

前序规则：M.Rule.UpdateDue

输出字段：M.Difference.timing_pending

表达式：((as_of ≥ change) 且 (as_of ≤ due) 且 非(corrected))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| change | 实际变化日期 | Date | M.Difference.actual_change_date |
| as_of | 差异核对日期 | Date | M.Difference.as_of |
| due | 法定更新期限届满日 | Date | M.Difference.update_due |
| corrected | 客户已实际更正 | Boolean | M.Difference.customer_corrected |

### M.Rule.ReportRequired / 差异报告义务判断

前序规则：M.Rule.MaterialDifference

输出字段：M.Difference.report_required

表达式：((cause = "备案信息错误") 且 material)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| cause | 差异成因 | Enum | M.Difference.cause |
| material | 属于重大差异 | Boolean | M.Difference.material |

### M.Rule.CorrectionAction / 按原因采取差异处置

前序规则：M.Rule.MaterialDifference

输出字段：M.Difference.correction_action

表达式：若 (cause = "机构识别错误")，则 "更正机构识别信息并保留复核"，否则 若 (cause = "备案信息错误")，则 若 material，则 "报告重大差异并跟踪"，否则 "记录差异并提示客户"，否则 "继续核实或跟踪，重大性及报告义务不豁免"

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| cause | 差异成因 | Enum | M.Difference.cause |
| material | 属于重大差异 | Boolean | M.Difference.material |

### M.Rule.CloseDifference / 实际更正且复核一致后闭环

前序规则：

输出字段：M.Difference.closure_allowed

表达式：(corrected 且 consistent)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| corrected | 客户已实际更正 | Boolean | M.Difference.customer_corrected |
| consistent | 再次核验或查询比对一致 | Boolean | M.Difference.recheck_consistent |

### M.Rule.Access / 查询用途及授权

前序规则：

输出字段：M.Access.allowed

表达式：(purpose 且 institution 且 operator)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| purpose | 用途属于法定职责或反洗钱义务 | Boolean | M.Access.lawful_purpose |
| institution | 机构具有查询权限 | Boolean | M.Access.institution_authorized |
| operator | 经办授权有效 | Boolean | M.Access.operator_authorized |

### M.Rule.ReturnMode / 查询返回方式

前序规则：M.Rule.Access

输出字段：M.Access.return_mode

表达式：若 allowed，则 若 declaration，则 "非掩码"，否则 "掩码"，否则 null

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| allowed | 允许该次查询 | Boolean | M.Access.allowed |
| declaration | 非掩码查询声明条件已核实 | Boolean | M.Access.declaration_verified |

### M.Rule.Transport / 传输保护条件

前序规则：

输出字段：M.Access.transport_allowed

表达式：(auth 且 signature 且 encryption 且 envelope)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| auth | 通信及访问身份认证通过 | Boolean | M.Access.authenticated |
| signature | 签名验签通过 | Boolean | M.Access.signature_valid |
| encryption | 按接口要求加密传输 | Boolean | M.Access.encrypted_transport |
| envelope | 证件号按要求使用数字信封 | Boolean | M.Access.document_envelope |

### M.Rule.Regime / 按时点选择制度

前序规则：

输出字段：M.ComplianceReview.applicable_regime

表达式：若 (duty = "备案")，则 若 (date ≥ "2024-11-01")，则 "3号令及对应办理指引；另核存量过渡"，否则 "本知识未封闭该历史时点备案口径"，否则 若 (date ≥ "2026-01-20")，则 "12号令；存量客户另核第三十九条"，否则 "使用适用历史制度，当前基线不足以封闭历史判断"

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| date | 适用业务日期 | Date | M.ComplianceReview.as_of |
| duty | 相关义务类型 | Enum | M.ComplianceReview.duty_kind |

### M.Rule.FilingSubmit / 备案资料和人员关系完整后提交

前序规则：

输出字段：M.Filing.can_submit

表达式：(people 且 relations 且 checked 且 routing)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| people | 全部应报自然人已录入 | Boolean | M.Filing.all_people_recorded |
| relations | 应报关系类别和日期已录入 | Boolean | M.Filing.all_relations_recorded |
| checked | 填报检查已完成 | Boolean | M.Filing.submission_checked |
| routing | 备案办理入口已按实际所在地选定 | Boolean | M.Identification.local_routing |

### M.Rule.QueryAllowed / 核验报文允许发送

前序规则：M.Rule.Access

输出字段：M.Query.query_allowed

表达式：(parameters 且 authorization 且 (count > 0) 且 若 batch，则 (count ≤ 100)，否则 (count = 1) 且 (used < quota))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| parameters | 参数版本完整有效 | Boolean | M.Query.parameters_current |
| count | 请求主体数量 | Integer | M.Query.subject_count |
| used | 本次请求前当日已核验主体数 | Integer | M.Query.daily_used_before |
| quota | 有效参数规定的额度 | Integer | M.Query.quota |
| authorization | 允许该次查询 | Boolean | M.Access.allowed |
| batch | 采用批量核验 | Boolean | M.Query.batch |

### M.Rule.DailyStop / 本批次后是否停止后续核验

前序规则：

输出字段：M.Query.triggers_daily_stop

表达式：((used + count) ≥ quota)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| used | 本次请求前当日已核验主体数 | Integer | M.Query.daily_used_before |
| count | 请求主体数量 | Integer | M.Query.subject_count |
| quota | 有效参数规定的额度 | Integer | M.Query.quota |

### M.Rule.QueryMatch / 反馈关联原请求

前序规则：

输出字段：M.Query.feedback_matched

表达式：(request = response)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| request | 请求业务流水 | Text | M.Query.request_reference |
| response | 反馈关联的请求流水 | Text | M.Query.response_reference |

### M.Rule.QueryUsable / 逐主体业务结果可用

前序规则：M.Rule.QueryMatch

输出字段：M.Query.result_usable

表达式：(received 且 matched 且 complete 且 valid)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| received | 业务反馈已收到 | Boolean | M.Query.feedback_received |
| matched | 反馈与原请求一致 | Boolean | M.Query.feedback_matched |
| complete | 逐主体结果已完整收到 | Boolean | M.Query.per_subject_complete |
| valid | 逐主体业务反馈有效 | Boolean | M.Query.business_feedback_success |

### M.Rule.CurrentQuery / 当前详情查询的核验流水前提

前序规则：M.Rule.Access

输出字段：M.Query.query_allowed

表达式：((已取得值(verification) 且 identified 且 auth) 且 valid)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| verification | 有效核验流水 | Text | M.Query.verification_reference |
| identified | 本机构独立识别已完成 | Boolean | M.Query.independent_identification_complete |
| auth | 允许该次查询 | Boolean | M.Access.allowed |
| valid | 核验流水在本次查询时仍有效 | Boolean | M.Query.verification_valid |

### M.Rule.ReportContent / 按报告类别检查内容和操作

前序规则：

输出字段：M.DifferenceReport.required_content_complete

表达式：若 (subtype = "客户身份存疑")，则 ((code 且 analysis 且 support) 且 非(org_change) 且 非(person_change))，否则 若 (subtype = "部分信息缺失")，则 ((code 且 analysis 且 support) 且 (operation = "新增人员") 且 new_name 且 非(org_change))，否则 若 (subtype = "信息获取完整")，则 ((code 且 analysis 且 support) 且 (((operation = "新增人员") 且 new) 或 ((operation = "修改人员") 且 old 且 new) 或 ((operation = "删除人员") 且 old 且 非(new)) 或 (operation = "主体填报类型")))，否则 若 包含(列表("机构自行更正"，"主体自行备案"，"主体自行更正")，subtype)，则 (code 且 非(org_change) 且 非(person_change))，否则 若 (subtype = "非重大差异报备")，则 (code 且 analysis 且 nonmajor_policy)，否则 若 (subtype = "确认无差异")，则 (code 且 consistent 且 非(org_change) 且 非(person_change))，否则 若 (subtype = "主体信息补充")，则 (in_system 且 empty 且 promise_state 且 code 且 new 且 (operation = "新增人员"))，否则 (非(in_system) 且 code 且 new 且 (operation = "新增人员"))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| subtype | 接口具体报告类型 | Enum | M.DifferenceReport.subtype |
| operation | 本次报文操作 | Enum | M.DifferenceReport.operation |
| code | 主体代码齐备 | Boolean | M.DifferenceReport.subject_code_present |
| analysis | 分析报告齐备 | Boolean | M.DifferenceReport.analysis_present |
| support | 佐证材料齐备 | Boolean | M.DifferenceReport.support_present |
| old | 原人员信息齐备 | Boolean | M.DifferenceReport.old_person_present |
| new | 新人员信息齐备 | Boolean | M.DifferenceReport.new_person_present |
| new_name | 新增人员姓名齐备 | Boolean | M.DifferenceReport.new_person_name_present |
| org_change | 提交企业信息变更 | Boolean | M.DifferenceReport.organization_change |
| person_change | 提交人员变更 | Boolean | M.DifferenceReport.person_change |
| nonmajor_policy | 非重大接口报备实施口径已确认 | Boolean | M.DifferenceReport.nonmajor_policy_confirmed |
| consistent | 核验结果一致 | Boolean | M.DifferenceReport.verification_consistent |
| in_system | 主体在系统中 | Boolean | M.DifferenceReport.subject_in_system |
| empty | 系统中人员为空 | Boolean | M.DifferenceReport.system_people_empty |
| promise_state | 承诺免报或国有公司对应条件成立 | Boolean | M.DifferenceReport.promise_or_state_condition |

### M.Rule.ReportSubmit / 差异报告提交前提

前序规则：M.Rule.ReportContent

输出字段：M.DifferenceReport.submit_allowed

表达式：(supported 且 content 且 (包含(列表("机构自行更正"，"主体自行备案"，"主体自行更正"，"确认无差异")，subtype) 或 attachments))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| supported | 具体类型与当前接口允许范围一致 | Boolean | M.DifferenceReport.type_supported |
| content | 具体类型所需内容齐备 | Boolean | M.DifferenceReport.required_content_complete |
| attachments | 应附文件已取得可用标识 | Boolean | M.DifferenceReport.attachments_usable |
| subtype | 接口具体报告类型 | Enum | M.DifferenceReport.subtype |

### M.Rule.CaseQuery / 案例编号取得后查询审批

前序规则：

输出字段：M.BomisCase.may_query_approval

表达式：(condition 且 first 且 number)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| condition | 申请条件已核实符合 | Boolean | M.BomisCase.conditions_met |
| first | 首个反馈已收到 | Boolean | M.BomisCase.initial_feedback |
| number | 案例编号已收到 | Boolean | M.BomisCase.number_received |

### M.Rule.ParameterContinuity / 参数通知连续性

前序规则：

输出字段：M.Parameters.sequence_continuous

表达式：(initial 或 (current = (previous + 1)))

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| current | 本次通知序号 | Integer | M.Parameters.sequence |
| previous | 已采用的前次通知序号 | Integer | M.Parameters.previous_sequence |
| initial | 首次完整参数快照已核实 | Boolean | M.Parameters.initial_snapshot_verified |

### M.Rule.ParameterResend / 参数缺期请求补发

前序规则：M.Rule.ParameterContinuity

输出字段：M.Parameters.resend_needed

表达式：非(continuous)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| continuous | 通知序号连续 | Boolean | M.Parameters.sequence_continuous |

### M.Rule.ParameterSend / 参数完整且业务受理才发送

前序规则：M.Rule.ParameterContinuity

输出字段：M.Parameters.send_allowed

表达式：(continuous 且 accepting)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| continuous | 通知序号连续 | Boolean | M.Parameters.sequence_continuous |
| accepting | 业务处于受理状态 | Boolean | M.Parameters.business_accepting |

### M.Rule.FileUsable / 附件取得实际应答后可用

前序规则：

输出字段：M.FileTransfer.usable

表达式：(received 且 matched 且 id)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| received | 实际上传业务应答已收到 | Boolean | M.FileTransfer.response_received |
| matched | 应答对应本次传输 | Boolean | M.FileTransfer.response_matched |
| id | 已取得真实文件标识 | Boolean | M.FileTransfer.file_id_received |

### M.Rule.KnownEquityPaths / 保留已证明的股权路径

前序规则：

输出字段：M.PersonAssessment.known_equity_paths

表达式：无环路径逐条连乘(从 rights 中逐项取 known_edge，满足 (已取得值(known_edge) 且 已取得值(known_edge.holder_key) 且 已取得值(known_edge.target_key) 且 已取得值(known_edge.ratio) 且 包含(列表("股权"，"合伙权益")，known_edge.right_kind) 且 ((known_edge.start ≤ date) 且 ((known_edge.end_status = "OPEN") 或 ((known_edge.end_status = "KNOWN") 且 已取得值(known_edge.end) 且 (known_edge.end > date)))))，得到 known_edge，业务身份键(person)，业务身份键(subject)，"holder_key"，"target_key"，"ratio")

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| rights | 同一时点核实的直接权益集合 | Ref | M.Identification.rights |
| date | 本项判断日期 | Date | M.PersonAssessment.as_of |
| person | 本项判断所涉自然人 | Ref | M.PersonAssessment.person |
| subject | 被识别主体 | Ref | M.Identification.subject |

### M.Rule.KnownEquityLowerBound / 已知股权路径形成下界

前序规则：M.Rule.KnownEquityPaths

输出字段：M.PersonAssessment.known_equity_lower_bound

表达式：求和(paths)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| paths | 已证明有效的股权路径乘积 | Decimal | M.PersonAssessment.known_equity_paths |

### M.Rule.KnownStandard1Candidate / 不完整结构中的已知达标候选

前序规则：M.Rule.KnownEquityLowerBound

输出字段：M.PersonAssessment.standard1_candidate

表达式：(lower ≥ 0.25)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| lower | 已证明股权比例下界 | Decimal | M.PersonAssessment.known_equity_lower_bound |

### M.Rule.Reverification / 失效流水重新核验

前序规则：

输出字段：M.Query.reverification_required

表达式：非(valid)

| 输入 | 业务名称 | 类型 | 字段 |
| --- | --- | --- | --- |
| valid | 核验流水在本次查询时仍有效 | Boolean | M.Query.verification_valid |

## 案例对应

| 案例 | 标题 | 模型 | 解释状态 | 执行状态 | 验证证据 |
| --- | --- | --- | --- | --- | --- |
| K.C.PILOT.01 | 性质判断成立后仍只进入适用与风险判断。 | M.Judgment.Risk, M.Judgment.StateNature, M.Rule.Article44, M.Rule.RelativeHolding, M.Rule.StateApplicability, M.Rule.StateSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.02 | 第一大股东但缺支配证据时性质判断为UNKNOWN。 | M.Judgment.Risk, M.Judgment.StateNature, M.Rule.Article44, M.Rule.RelativeHolding, M.Rule.StateApplicability, M.Rule.StateSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.03 | 国有参股路由到一般识别且仅处理国有资本部分。 | M.Judgment.Risk, M.Judgment.StateNature, M.Rule.Article44, M.Rule.RelativeHolding, M.Rule.StateApplicability, M.Rule.StateSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.04 | 风险触发阻断简化并创建加强识别决定。 | M.Judgment.Risk, M.Judgment.StateNature, M.Rule.Article44, M.Rule.RelativeHolding, M.Rule.StateApplicability, M.Rule.StateSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.05 | 从签署、条件满足、录入三日期选择实际生效日。 | M.Constraint.BeneficialOwnershipInterval, M.Constraint.ControlInterval, M.Constraint.RightInterval, M.Judgment.Continuity, M.Judgment.EffectiveDate, M.Rule.Formation | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.06 | 缺生效约定和条件证据时形成日UNKNOWN并生成补证任务。 | M.Constraint.BeneficialOwnershipInterval, M.Constraint.ControlInterval, M.Constraint.RightInterval, M.Judgment.Continuity, M.Judgment.EffectiveDate, M.Rule.Formation | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.07 | 历史中断后当前区间起点与历史事件同时保留。 | M.Constraint.BeneficialOwnershipInterval, M.Constraint.ControlInterval, M.Constraint.RightInterval, M.Judgment.Continuity, M.Judgment.EffectiveDate, M.Rule.Formation | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.08 | 跨关系类型切换先核连续性和控制协议生效。 | M.Constraint.BeneficialOwnershipInterval, M.Constraint.ControlInterval, M.Constraint.RightInterval, M.Judgment.Continuity, M.Judgment.EffectiveDate, M.Rule.Formation | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.09 | 年月差异独立命中重大分支。 | M.Judgment.DifferenceCause, M.Rule.DateYearMonth, M.Rule.MaterialDifference, M.Rule.TimingPending, M.Rule.UpdateDue | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.10 | 非重大结论仍保留理由、比对、措施与提示。 | M.Judgment.DifferenceCause, M.Rule.DateYearMonth, M.Rule.MaterialDifference, M.Rule.TimingPending, M.Rule.UpdateDue | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.11 | 待更新任务和重大性判断并存。 | M.Judgment.DifferenceCause, M.Rule.DateYearMonth, M.Rule.MaterialDifference, M.Rule.TimingPending, M.Rule.UpdateDue | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.12 | 机构识别错误走本机构更正分支并保留成因证据。 | M.Judgment.DifferenceCause, M.Machine.Difference, M.Rule.CloseDifference, M.Rule.CorrectionAction, M.Rule.ReportRequired | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.13 | 实际更正AND复核一致后迁移到RESOLVED且保留历史。 | M.Judgment.DifferenceCause, M.Machine.Difference, M.Rule.CloseDifference, M.Rule.CorrectionAction, M.Rule.ReportRequired | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.14 | 缺实际更正或复核一致时闭环guard阻断。 | M.Judgment.DifferenceCause, M.Machine.Difference, M.Rule.CloseDifference, M.Rule.CorrectionAction, M.Rule.ReportRequired | EXPLAINED | NOT_EXECUTED |  |
| K.C.PILOT.15 | 全链成立时输出MAY_SIMPLIFY并保存理由，不输出MUST。 | M.Judgment.Risk, M.Judgment.StateNature, M.Rule.Article44, M.Rule.RelativeHolding, M.Rule.StateApplicability, M.Rule.StateSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q01.01 | 备案义务与银行独立识别同时适用。 | M.Judgment.Authority, M.Rule.CddScope, M.Rule.FilingScope | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q01.02 | 本专项不适用不外推其他尽调义务。 | M.Judgment.Authority, M.Rule.CddScope, M.Rule.FilingScope | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q01.03 | 暂无需备案与仍需金融机构识别并列。 | M.Judgment.Authority, M.Rule.CddScope, M.Rule.FilingScope | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q02.01 | 人民币恰1000万元命中<=边界，银行识别不受影响。 | M.Rule.FilingExemption | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q02.02 | 外部控制或获益事实使免报四项条件失败。 | M.Rule.FilingExemption | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q02.03 | 资本超限严格失败，无容差。 | M.Rule.FilingExemption | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q02.04 | 未知控制/获益保持UNKNOWN，不转false。 | M.Rule.FilingExemption | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q03.01 | >=25包含25.00。 | M.Constraint.RightHolder, M.Constraint.RightParty, M.Constraint.RightRatio, M.Constraint.RightTarget, M.Rule.EquityPaths, M.Rule.EquityTotal, M.Rule.KnownEquityLowerBound, M.Rule.KnownEquityPaths, M.Rule.KnownStandard1Candidate, M.Rule.PersonQualified, M.Rule.Standard1, M.Rule.UseStandard2, M.Rule.UseStandard3 | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q03.02 | 两条可归属路径合计24%+2%=26%。 | M.Constraint.RightHolder, M.Constraint.RightParty, M.Constraint.RightRatio, M.Constraint.RightTarget, M.Rule.EquityPaths, M.Rule.EquityTotal, M.Rule.KnownEquityLowerBound, M.Rule.KnownEquityPaths, M.Rule.KnownStandard1Candidate, M.Rule.PersonQualified, M.Rule.Standard1, M.Rule.UseStandard2, M.Rule.UseStandard3 | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q03.03 | 24.99不四舍五入且只否定标准一。 | M.Constraint.RightHolder, M.Constraint.RightParty, M.Constraint.RightRatio, M.Constraint.RightTarget, M.Rule.EquityPaths, M.Rule.EquityTotal, M.Rule.KnownEquityLowerBound, M.Rule.KnownEquityPaths, M.Rule.KnownStandard1Candidate, M.Rule.PersonQualified, M.Rule.Standard1, M.Rule.UseStandard2, M.Rule.UseStandard3 | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q03.04 | 已知达标候选可保留，但未知境外层阻断完整名单。 | M.Constraint.RightHolder, M.Constraint.RightParty, M.Constraint.RightRatio, M.Constraint.RightTarget, M.Rule.EquityPaths, M.Rule.EquityTotal, M.Rule.KnownEquityLowerBound, M.Rule.KnownEquityPaths, M.Rule.KnownStandard1Candidate, M.Rule.PersonQualified, M.Rule.Standard1, M.Rule.UseStandard2, M.Rule.UseStandard3 | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q04.01 | 收益权30%独立于名义股权10%。 | M.Constraint.RightParty, M.Constraint.RightRatio, M.Rule.IncomePaths, M.Rule.IncomeTotal, M.Rule.PersonQualified, M.Rule.Standard2, M.Rule.UseStandard2, M.Rule.VotingPaths, M.Rule.VotingTotal | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q04.02 | 低于阈值且无控制事实不命中标准二三。 | M.Constraint.RightParty, M.Constraint.RightRatio, M.Rule.IncomePaths, M.Rule.IncomeTotal, M.Rule.PersonQualified, M.Rule.Standard2, M.Rule.UseStandard2, M.Rule.VotingPaths, M.Rule.VotingTotal | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q04.03 | 标准一优先分类但收益安排事实保留。 | M.Constraint.RightParty, M.Constraint.RightRatio, M.Rule.IncomePaths, M.Rule.IncomeTotal, M.Rule.PersonQualified, M.Rule.Standard2, M.Rule.UseStandard2, M.Rule.VotingPaths, M.Rule.VotingTotal | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q04.04 | 表决权和实际控制两类关系并存但只形成一人。 | M.Constraint.RightParty, M.Constraint.RightRatio, M.Judgment.Control, M.Rule.IncomePaths, M.Rule.IncomeTotal, M.Rule.PersonQualified, M.Rule.Standard2, M.Rule.Standard3, M.Rule.UseStandard2, M.Rule.UseStandard3, M.Rule.VotingPaths, M.Rule.VotingTotal | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q05.01 | 低持股不阻断有证据联合控制。 | M.Judgment.Control, M.Rule.PersonQualified, M.Rule.Standard3, M.Rule.UseStandard3 | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q05.02 | 亲属/候选/5%仅为线索，控制判断缺证阻断。 | M.Judgment.Control, M.Rule.PersonQualified, M.Rule.Standard3, M.Rule.UseStandard3 | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q05.03 | 普通合伙人需协议和履职证据，1%不否定控制。 | M.Judgment.Control, M.Rule.PersonQualified, M.Rule.Standard3, M.Rule.UseStandard3 | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q05.04 | 专业影响和参会不满足控制事实。 | M.Judgment.Control, M.Rule.PersonQualified, M.Rule.Standard3, M.Rule.UseStandard3 | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q06.01 | 前三项明确无人后至少一名最高层级经理兜底且actual_controller=false。 | M.Constraint.AppointmentInterval, M.Rule.Fallback | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q06.02 | 标准一命中阻断兜底替代。 | M.Constraint.AppointmentInterval, M.Rule.Fallback | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q06.03 | 前三项因缺证未知时兜底入口BLOCK。 | M.Constraint.AppointmentInterval, M.Rule.Fallback | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q08.01 | 国内分支沿用且复用记录来源和有效性。 | M.Constraint.AppointmentInterval, M.Rule.BranchRoute | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q08.02 | 所属主体非本机构已尽调客户时不声称复用完成。 | M.Constraint.AppointmentInterval, M.Rule.BranchRoute | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q08.03 | 外国分支=所属公司穿透自然人+分支高管双路径。 | M.Constraint.AppointmentInterval, M.Rule.BranchRoute | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q08.04 | 境外本国豁免不终止中国识别。 | M.Constraint.AppointmentInterval, M.Rule.BranchRoute | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q08.05 | 只得一名分支高管时清单状态PARTIAL。 | M.Constraint.AppointmentInterval, M.Rule.BranchRoute | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q09.01 | 全部信托当事人和其他控制人进入记录并区分路径。 | M.Judgment.Products, M.Rule.AssetSimplification, M.Rule.ManagerReliance, M.Rule.TrustFull, M.Rule.TrustSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q09.02 | 组织当事人本身记录但穿透未知保持证据不足。 | M.Judgment.Products, M.Rule.AssetSimplification, M.Rule.ManagerReliance, M.Rule.TrustFull, M.Rule.TrustSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q09.03 | 受益人未具体确定时保存可核实范围。 | M.Judgment.Products, M.Rule.AssetSimplification, M.Rule.ManagerReliance, M.Rule.TrustFull, M.Rule.TrustSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q09.04 | 产品简化成立仍必须识别具体管理自然人。 | M.Judgment.Products, M.Rule.AssetSimplification, M.Rule.ManagerReliance, M.Rule.TrustFull, M.Rule.TrustSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q09.05 | 产品条件不足走一般风险识别并补登记管理资料。 | M.Judgment.Products, M.Rule.AssetSimplification, M.Rule.ManagerReliance, M.Rule.TrustFull, M.Rule.TrustSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q09.06 | 采信决定绑定体系评估、材料审查和理由。 | M.Judgment.Products, M.Rule.AssetSimplification, M.Rule.ManagerReliance, M.Rule.TrustFull, M.Rule.TrustSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.IDENT.Q09.07 | 疑点/拒补触发重识别和风险措施。 | M.Judgment.Products, M.Rule.AssetSimplification, M.Rule.ManagerReliance, M.Rule.TrustFull, M.Rule.TrustSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.10.01 | 备案场景完整信息集合且形成日取实际生效。 | M.Judgment.EffectiveDate, M.Judgment.IdentityRights, M.Judgment.RecordContents | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.10.02 | 金融机构较少要素分支不反向缩减备案信息。 | M.Judgment.EffectiveDate, M.Judgment.IdentityRights, M.Judgment.RecordContents | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.12.01 | 现场设立30日期限从设立日起算。 | M.Rule.FilingDue, M.Rule.LegacyDeferral, M.Rule.LegacyDue | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.12.02 | 高风险6月与睡眠/限制客户激活例外分开。 | M.Rule.FilingDue, M.Rule.LegacyDeferral, M.Rule.LegacyDue | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.13.01 | 单一名单/BOMIS观察不足以宣称完整核实。 | M.Judgment.IdentityRights, M.Rule.QueryAfterIdentification | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.13.02 | 低风险少取材料需有条件完成且仍核BOMIS。 | M.Judgment.IdentityRights, M.Rule.QueryAfterIdentification | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.14.01 | 风险触发、三项措施、剩余风险和继续决定分层。 | M.Judgment.RemainingRisk, M.Judgment.Risk, M.Rule.RefuseOrEnd | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.14.02 | 实施措施后风险超能力方可拒绝/终止并保存依据。 | M.Judgment.RemainingRisk, M.Judgment.Risk, M.Rule.RefuseOrEnd | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.15.01 | 封闭类别证据成立后免识别且留性质依据。 | M.Judgment.Authority, M.Judgment.Risk, M.Judgment.StateNature, M.Rule.CddExemption, M.Rule.FilingExemption, M.Rule.SimplificationMeasure, M.Rule.StateApplicability, M.Rule.StateSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.15.02 | 备案免报状态不触发银行免识别。 | M.Judgment.Authority, M.Judgment.Risk, M.Judgment.StateNature, M.Rule.CddExemption, M.Rule.FilingExemption, M.Rule.SimplificationMeasure, M.Rule.StateApplicability, M.Rule.StateSimplification | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.16.01 | 控制终止事件触发复核，旧事实不删除。 | M.Rule.ReviewTrigger | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.16.02 | 董事变化经影响判断为不影响时可不更新正式UBO。 | M.Rule.ReviewTrigger | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.20.01 | 授权目的内访问且用途受限并留审计。 | M.Judgment.Authority, M.Rule.Access, M.Rule.ReturnMode, M.Rule.Transport | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.20.02 | 权限不成立时访问guard拒绝。 | M.Judgment.Authority, M.Rule.Access, M.Rule.ReturnMode, M.Rule.Transport | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.21.01 | 责任规则输出风险档位而非必然罚款数额。 | M.Judgment.Authority, M.Judgment.Liability, M.Rule.Regime | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.GOV.21.02 | 严重违法与从轻材料分别记录。 | M.Judgment.Authority, M.Judgment.Liability, M.Rule.Regime | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.17.A | 确认应备案未备案后形成差异报告事项并与STR分开。 | M.Judgment.DifferenceCause, M.Rule.QueryAfterIdentification | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.17.B | 查询故障/待完成不生成无UBO、未备案或一致结论。 | M.Judgment.DifferenceCause, M.Rule.QueryAfterIdentification | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.22.A | 地方填报保留全部人员而非只保留系统带入首人。 | M.Judgment.FilingRoute, M.Rule.FilingSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.22.B | 登录失败保留待办理，不输出完成或免报。 | M.Judgment.FilingRoute, M.Rule.FilingSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.23.A | 临界批次全体处理、后续拒绝且等待批处理结果。 | M.Machine.Query, M.Rule.DailyStop, M.Rule.QueryAllowed, M.Rule.QueryMatch, M.Rule.QueryUsable | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.23.B | 缺逐户反馈时批量状态待返回。 | M.Machine.Query, M.Rule.DailyStop, M.Rule.QueryAllowed, M.Rule.QueryMatch, M.Rule.QueryUsable | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.23.C | 流水过期记录失效并重新核验。 | M.Machine.Query, M.Rule.CurrentQuery, M.Rule.QueryAllowed, M.Rule.QueryMatch, M.Rule.QueryUsable, M.Rule.Reverification | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.23.D | 详情反馈成功只产生观察，另做一致性判断。 | M.Machine.Query, M.Rule.CurrentQuery, M.Rule.QueryAllowed, M.Rule.QueryMatch, M.Rule.QueryUsable, M.Rule.Reverification | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.23.E | 仅两次备案日期不足以生成业务关系中断。 | M.Judgment.Continuity, M.Machine.Query, M.Rule.QueryAllowed, M.Rule.QueryMatch, M.Rule.QueryUsable | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.23.F | 有证据时展示旧区间、终止和新形成且来源分开。 | M.Judgment.Continuity, M.Machine.Query, M.Rule.QueryAllowed, M.Rule.QueryMatch, M.Rule.QueryUsable | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.24.R1 | 非重大法定处理完成，但接口采用依据保留未决。 | M.Machine.Report, M.Rule.ReportContent, M.Rule.ReportSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.24.R2 | 部分身份缺失选相应分支且不伪造，新增事实不允许借机删除他人。 | M.Machine.Report, M.Rule.ReportContent, M.Rule.ReportSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.24.S1 | 终止回执保留但差异仍按最新事实处理。 | M.Constraint.ReportFeedback, M.Machine.Report, M.Rule.ReportContent, M.Rule.ReportSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.24.S2 | 报告办结历史保留，新事实另走后续处理。 | M.Constraint.ReportFeedback, M.Machine.Report, M.Rule.ReportContent, M.Rule.ReportSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.24.C1 | 首反馈仅迁移到待审批并关联原报告。 | M.Constraint.BomisCaseDuplicate, M.Machine.Case, M.Machine.Report, M.Rule.CaseQuery, M.Rule.ReportContent, M.Rule.ReportSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.24.C2 | 重复申请拒绝后继续原申请，无第二成功记录。 | M.Constraint.BomisCaseDuplicate, M.Machine.Case, M.Machine.Report, M.Rule.CaseQuery, M.Rule.ReportContent, M.Rule.ReportSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.24.P1 | 参数期数缺口先补发再使用。 | M.Machine.Report, M.Rule.ParameterContinuity, M.Rule.ParameterResend, M.Rule.ParameterSend, M.Rule.ReportContent, M.Rule.ReportSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.24.P2 | 非营业受理时间保持待发送。 | M.Machine.Report, M.Rule.ParameterContinuity, M.Rule.ParameterResend, M.Rule.ParameterSend, M.Rule.ReportContent, M.Rule.ReportSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.24.F1 | 初步响应后保持上传待结果，文件ID未知。 | M.Constraint.FileFeedback, M.Constraint.FileTransferDuplicate, M.Machine.File, M.Machine.Report, M.Rule.FileUsable, M.Rule.ReportContent, M.Rule.ReportSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.EXT.OPS.24.F2 | 重复报文拒绝与首次请求结果分别保留并关联。 | M.Constraint.FileFeedback, M.Constraint.FileTransferDuplicate, M.Machine.File, M.Machine.Report, M.Rule.FileUsable, M.Rule.ReportContent, M.Rule.ReportSubmit | EXPLAINED | NOT_EXECUTED |  |
| K.C.REVIEW.TYPE_CONTINUITY | 总体资格连续时总体日期不重置，分类型事件分别记。 | M.Constraint.BeneficialOwnershipInterval, M.Constraint.ControlInterval, M.Constraint.RightInterval, M.Judgment.Continuity, M.Judgment.EffectiveDate, M.Rule.Formation | EXPLAINED | NOT_EXECUTED |  |

## 上游未决事项

| 知识事项 | 模型事项 | 处理 | 说明 |
| --- | --- | --- | --- |
| K.ISSUE.02 | M.Gap.02 | MODEL_LIMITATION | 不能声称已给出完整内部跟踪SLA或自动升级流程。 |
| K.ISSUE.SEMANTIC_REVIEW | M.Gap.SEMANTIC_REVIEW | MODEL_LIMITATION | 不能把41题、59规则、86案例数量等同全量制度无遗漏。 |
| K.ISSUE.REV.IDENTITY.MISSING_ORDER11 | M.Gap.REV.IDENTITY.MISSING_ORDER11 | MODEL_LIMITATION | 不能列出完整识别义务机构清单。 |
| K.ISSUE.REV.IDENTITY.FX_EQUIV | M.Gap.REV.IDENTITY.FX_EQUIV | MODEL_LIMITATION | 不能自定汇率、时点、舍入或容差。 |
| K.ISSUE.REV.IDENTITY.CIRCULAR_CALC | M.Gap.REV.IDENTITY.CIRCULAR_CALC | MODEL_LIMITATION | 不能对循环交叉结构输出精确比例或完整UBO名单。 |
| K.ISSUE.REV.IDENTITY.TIED_MANAGERS | M.Gap.REV.IDENTITY.TIED_MANAGERS | MODEL_LIMITATION | 不能自动选法定代表人、总经理或职位排序第一者。 |
| K.ISSUE.REV.IDENTITY.AM_MANAGER | M.Gap.REV.IDENTITY.AM_MANAGER | MODEL_LIMITATION | 不能默认管理机构法定代表人、产品经理或任一经办人。 |
| K.ISSUE.EXT.GOV.RETENTION | M.Gap.EXT.GOV.RETENTION | MODEL_LIMITATION | 不能输出确定保存年限和截止日。 |
| K.ISSUE.EXT.GOV.REVIEW_FREQUENCY | M.Gap.EXT.GOV.REVIEW_FREQUENCY | MODEL_LIMITATION | 不能填造季度、年度等统一周期。 |
| K.ISSUE.EXT.GOV.PENALTY_BASIS | M.Gap.EXT.GOV.PENALTY_BASIS | MODEL_LIMITATION | 不能宣称必然处罚、具体数额或最终竞合结论。 |
| K.ISSUE.EXT.GOV.BROAD_UNITS | M.Gap.EXT.GOV.BROAD_UNITS | MODEL_LIMITATION | 不能称七份文件全部业务语义审查完成。 |
| K.ISSUE.INTERFACE_REPORT_DUTY | M.Gap.INTERFACE_REPORT_DUTY | MODEL_LIMITATION | 不能把全部非重大差异强制上报。 |
| K.ISSUE.INTERFACE_THRESHOLD | M.Gap.INTERFACE_THRESHOLD | MODEL_LIMITATION | 不能为迁就接口把25.00%排除。 |
| K.ISSUE.INTERFACE_IDENTITY | M.Gap.INTERFACE_IDENTITY | MODEL_LIMITATION | 不能声称字段匹配和必填规则已统一。 |
| K.ISSUE.CURRENT_TARGET_RISK | M.Gap.CURRENT_TARGET_RISK | MODEL_LIMITATION | 不能把现行三类例外描述成已满足第二十条全部情形。 |

## 模型问题

| 标识 | 状态 | 问题 | 影响 | 责任 | 解决前处理 |
| --- | --- | --- | --- | --- | --- |
| M.Gap.02 | OPEN | 近期变更处于法定30日更新期时，应标记时点性待更新，这一选择已有用户答复；后续复核责任、复核时点和超期升级操作尚需明确。 | K.ISSUE.02, K.Q.18, K.Q.18.DATES, K.Q.18.PENDING, K.Q.19, K.Q.19.CORRECT, K.R.18, K.R.18.PENDING | 差异管理与反洗钱合规责任人 | 标记待更新并保留跟踪，不能把30日作为日期容差或差异豁免；不臆定内部处置时限。 |
| M.Gap.SEMANTIC_REVIEW | OPEN | 20个既有问题已按本轮方法补成具体业务解释、判断和案例；全量输入单元仍有未审或仅部分拆解，不能声明知识全量完整。 | K.ISSUE.SEMANTIC_REVIEW, K.Q.01, K.Q.02, K.Q.03, K.Q.04, K.Q.05, K.Q.06, K.Q.07, K.Q.07.APPLY, K.Q.07.NATURE, K.Q.07.RISK, K.Q.08, K.Q.09, K.Q.10, K.Q.11, K.Q.11.HISTORY, K.Q.11.START, K.Q.12, K.Q.13, K.Q.14, K.Q.15, K.Q.16, K.Q.17, K.Q.18, K.Q.18.DATES, K.Q.18.PENDING, K.Q.19, K.Q.19.CLOSE, K.Q.19.CORRECT, K.Q.20, K.Q.21, K.Q.22, K.Q.23, K.Q.23.CURRENT, K.Q.23.HISTORY, K.Q.23.VERIFY, K.Q.24, K.Q.24.CASE, K.Q.24.FILE, K.Q.24.PARAM, K.Q.24.REPORT, K.Q.24.STATUS | 领域知识整理者与相关业务角色 | 本版可供按主题业务评审；不作为全量制度无遗漏或接口实现完备的保证。 |
| M.Gap.REV.IDENTITY.MISSING_ORDER11 | OPEN | 12号令第二条把适用机构范围交由2025年第11号令规定，但该令不在用户限定的七份制度原文中，因此当前不能列出完整义务机构清单。 | K.ISSUE.REV.IDENTITY.MISSING_ORDER11, K.Q.01, K.R.01 | 反洗钱制度与客户尽调责任人 | 仅表述为‘第11号令规定的客户尽调义务机构’，不按常识、机构名称或历史清单穷举。 |
| M.Gap.REV.IDENTITY.FX_EQUIV | OPEN | 3号令第三条允许以等值外币判断1000万元免报边界，但限定材料没有规定折算日期、汇率来源或舍入方法。 | K.ISSUE.REV.IDENTITY.FX_EQUIV, K.Q.02, K.Q.15, K.R.02 | 备案业务与合规责任人 | 外币注册资本接近边界时返回证据不足，不自定汇率或容差；人民币案例按小于等于1000万元执行。 |
| M.Gap.REV.IDENTITY.CIRCULAR_CALC | OPEN | 第二版备案指南说明普通多层路径乘算和同一自然人多路径合计，12号令把循环嵌套、交叉持股列为需加强的复杂结构，但限定材料没有给出循环或交叉持股的封闭比例算法。 | K.ISSUE.REV.IDENTITY.CIRCULAR_CALC, K.Q.03, K.Q.04, K.Q.05, K.R.03 | 受益所有人计算口径与反洗钱合规责任人 | 普通无环结构按逐路径相乘和同一自然人合计；循环、交叉结构停止精确比例与完整清单结论并加强核实。 |
| M.Gap.REV.IDENTITY.TIED_MANAGERS | OPEN | 第二版备案指南规定兜底时至少备案一名最高层级日常经营管理人员，但未规定同一最高层级有多名人员时的选择或全量纳入标准。 | K.ISSUE.REV.IDENTITY.TIED_MANAGERS, K.Q.06, K.R.06 | 备案业务与反洗钱识别责任人 | 确认前三项均无人满足后可遵守‘至少一名最高层级’最低要求，但不宣称限定材料已规定同层优先顺序。 |
| M.Gap.REV.IDENTITY.AM_MANAGER | OPEN | 12号令第十四、十七条要求简化时认定并取得‘管理资产管理产品的自然人’信息，但没有界定多人团队、投资决策委员会或管理职责分散时应选择哪些自然人。 | K.ISSUE.REV.IDENTITY.AM_MANAGER, K.Q.09, K.R.09.ASSET | 资产管理业务与反洗钱合规责任人 | 不得默认选择管理机构法定代表人、产品经理或任一经办人；事实不足时保持证据不足。 |
| M.Gap.EXT.GOV.RETENTION | OPEN | 本次唯一权威输入要求金融机构识别留存并依法保密，但未载明保存10年，也未说明从业务关系终止、交易完成或其他事件起算。 | K.ISSUE.EXT.GOV.RETENTION, K.Q.20, K.Q.23, K.Q.23.CURRENT, K.Q.23.VERIFY, K.R.20 | 反洗钱制度与档案管理责任人 | 只陈述现有留存义务，不写10年、不自定起算日。 |
| M.Gap.EXT.GOV.REVIEW_FREQUENCY | OPEN | 12号令规定事件触发审核，并允许加强情形提高审核更新频率，但本次来源未给全部客户统一固定复核周期。 | K.ISSUE.EXT.GOV.REVIEW_FREQUENCY, K.Q.16, K.R.16 | 持续尽调与客户风险管理责任人 | 执行事件触发复核；加强情形提高频率，但不填造季度、年度等统一周期。 |
| M.Gap.EXT.GOV.PENALTY_BASIS | OPEN | 3号令和12号令的责任条款继续引用企业登记管理行政法规及反洗钱法第五十二至五十四条，本次7份来源未包含这些全文。 | K.ISSUE.EXT.GOV.PENALTY_BASIS, K.Q.21, K.R.21 | 法务与反洗钱制度责任人 | 可识别规章内违法类型和档位，不作具体案件必然处罚结论。 |
| M.Gap.EXT.GOV.BROAD_UNITS | OPEN | 本轮仅对8个问题直接相关的原文条款和BOMIS安全查询单元做深度回读；地方操作手册全部界面图、BOMIS其余千余报文字段及8题以外业务含义未宣称完成。 | K.ISSUE.EXT.GOV.BROAD_UNITS, K.Q.10, K.Q.12, K.Q.13, K.Q.14, K.Q.15, K.Q.16, K.Q.20, K.Q.21 | 领域知识整理者 | 不得将本补丁描述为7份文件全部业务语义审查完成。 |
| M.Gap.INTERFACE_REPORT_DUTY | OPEN | 非重大差异无需法定差异报告，与接口“非重大差异报备”功能如何在本机构衔接？ | K.ISSUE.INTERFACE_REPORT_DUTY, K.Q.18, K.Q.24.REPORT | 差异管理与反洗钱合规责任人 | 可完成差异识别和非重大差异记录；不将接口可报备自动变成必须报送。 |
| M.Gap.INTERFACE_THRESHOLD | OPEN | BOMIS补充类个别说明写比例>25%，与制度“25%以上”及25%边界如何一致？ | K.ISSUE.INTERFACE_THRESHOLD, K.Q.03, K.Q.24.REPORT | BOMIS接口规范维护方、反洗钱合规责任人 | 业务识别依制度边界；该报送边界未经明确前不能声称已完成接口适配。 |
| M.Gap.INTERFACE_IDENTITY | OPEN | V2.0修订说明与附录旧错误码对人员匹配和必填项存在不一致，使用哪套字段规则？ | K.ISSUE.INTERFACE_IDENTITY, K.Q.24.FILE, K.Q.24.REPORT | BOMIS接口规范维护方 | 可继续业务判断与材料整理；不将未经澄清的字段匹配顺序作为已核验运行事实。 |
| M.Gap.CURRENT_TARGET_RISK | OPEN | 国企简化的现行操作已经澄清，但“通常直接简化”的做法与制度要求的充分风险评估之间仍需合规裁定。 | K.ISSUE.CURRENT_TARGET_RISK, K.Q.07, K.Q.07.APPLY, K.Q.07.RISK, K.Q.15, K.R.07, K.R.07.RISK | 反洗钱合规责任人及国企业务负责人 | 制度链条继续作为应遵守的判断依据；现状单列。不得把评审记录“冲突解除”解释为合规差异已经裁定。 |
