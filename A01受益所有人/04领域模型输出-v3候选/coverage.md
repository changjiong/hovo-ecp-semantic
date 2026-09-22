# A01 受益所有人领域模型候选：知识承接与覆盖

> 上游知识：`03领域知识输出-v3候选/review.md` 3.1.0-draft  
> 模型候选：`model-candidate.yaml` 0.1.0  
> 状态：DRAFT；当前不声称 Domain DSL 2.0 合同校验通过。

# 1. 覆盖原则

本轮不再以“30个问题是否都有模型对象”作为主要完成条件，而是逐条检查上游 **69条 Rule（业务规则）**：

- 已被稳定对象/关系/判断/过程承接 → MODELED；
- 上游知识本身仍有 OPEN → 模型显式绑定，不补造；
- 业务语义明确但具体算法属于后续实现 → 模型保留输入、输出、未知处理和边界，不扩张成运行时。

# 2. 核心模型对象

| 分组 | 模型元素 |
| --- | --- |
| 现实对象 | M.Person, M.Organization, M.Branch, M.Trust, M.AssetManagementProduct |
| 统一任务角色 | M.IdentificationObject |
| 基础事实 | M.OwnershipHolding, M.EconomicRight, M.ControlRelation, M.ManagementResponsibility, M.TrustPartyRelation, M.ProductManagementRelation |
| 证据与核实 | M.Evidence, M.VerificationAssessment |
| 路由/措施 | M.BaseRuleDecision, M.IdentificationTreatment, M.RiskSignal |
| 专项判断 | M.StateOwnedNatureAssessment, M.UltimateOwnershipAssessment |
| UBO结果 | M.QualificationBasis, M.BeneficialOwnerStatus |
| 任务与变化 | M.IdentificationCase, M.ChangeEvent |
| 差异 | M.DifferenceAssessment |

# 3. Rule → Model 映射

| Knowledge Rule | Model refs | 状态 |
| --- | --- | --- |
| R-01 | M.IdentificationObject, M.BaseRuleDecision, P-01 | MODELED |
| R-02 | M.BaseRuleDecision, M.IdentificationTreatment, P-01, P-02 | MODELED |
| R-03 | M.IdentificationTreatment, P-02 | MODELED |
| R-04 | M.IdentificationTreatment, P-02 | MODELED |
| R-05 | M.IdentificationTreatment, P-02 | MODELED |
| R-06 | M.IdentificationTreatment | MODELED |
| R-07 | M.UltimateOwnershipAssessment, M.QualificationBasis, D-02, P-03 | MODELED |
| R-08 | M.OwnershipHolding, D-02 | MODELED |
| R-09 | M.OwnershipHolding, M.UltimateOwnershipAssessment, D-02 | MODELED |
| R-10 | M.UltimateOwnershipAssessment, D-02 | MODELED |
| R-11 | M.UltimateOwnershipAssessment, D-02 | MODELED |
| R-12 | M.BeneficialOwnerStatus, D-02 | MODELED |
| R-13 | D-02, D-03, D-04 | MODELED |
| R-14 | M.UltimateOwnershipAssessment.path_completeness, D-02 | MODELED |
| R-15 | M.RiskSignal, M.UltimateOwnershipAssessment, O-01, D-06 | MODELED |
| R-16 | D-03 | MODELED |
| R-17 | M.EconomicRight, D-03 | MODELED |
| R-18 | M.EconomicRight, D-03 | MODELED |
| R-19 | M.EconomicRight, D-03 | MODELED |
| R-20 | M.EconomicRight, M.Evidence, M.VerificationAssessment | MODELED |
| R-21 | M.BeneficialOwnerStatus, M.QualificationBasis | MODELED |
| R-22 | D-04 | MODELED |
| R-23 | M.ControlRelation, D-04 | MODELED |
| R-24 | M.ControlRelation | MODELED |
| R-25 | M.ControlRelation | MODELED |
| R-26 | M.ControlRelation | MODELED |
| R-27 | M.ControlRelation | MODELED |
| R-28 | M.ControlRelation | MODELED |
| R-29 | M.ControlRelation, M.Evidence | MODELED |
| R-30 | M.Evidence, M.ControlRelation | MODELED |
| R-31 | M.ControlRelation.verification_status, M.VerificationAssessment | MODELED |
| R-32 | M.ManagementResponsibility, D-05, P-03 | MODELED |
| R-33 | M.ManagementResponsibility | MODELED |
| R-34 | M.ManagementResponsibility, O-03 | MODELED |
| R-35 | M.Branch, D-08, P-04 | MODELED |
| R-36 | M.Branch, D-08, P-04 | MODELED |
| R-37 | M.Branch, D-09, P-04 | MODELED |
| R-38 | M.Trust, M.TrustPartyRelation, D-10, P-05 | MODELED |
| R-39 | M.TrustPartyRelation, D-10, P-05 | MODELED |
| R-40 | M.Trust, M.IdentificationTreatment, D-10, P-05 | MODELED |
| R-41 | M.AssetManagementProduct, D-11, P-06 | MODELED |
| R-42 | M.AssetManagementProduct, M.ProductManagementRelation, M.IdentificationTreatment, O-04, D-11 | MODELED |
| R-43 | M.Evidence, M.VerificationAssessment, D-11 | MODELED |
| R-44 | M.Organization, M.IdentificationTreatment, O-05 | MODELED |
| R-45 | M.Organization, M.IdentificationTreatment | MODELED |
| R-46 | M.StateOwnedNatureAssessment, P-07 | MODELED |
| R-47 | M.StateOwnedNatureAssessment | MODELED |
| R-48 | M.StateOwnedNatureAssessment, M.Evidence | MODELED |
| R-49 | M.StateOwnedNatureAssessment | MODELED |
| R-50 | M.StateOwnedNatureAssessment, M.Evidence | MODELED |
| R-51 | M.StateOwnedNatureAssessment, M.IdentificationTreatment, M.QualificationBasis, D-07 | MODELED |
| R-52 | M.StateOwnedNatureAssessment, M.IdentificationTreatment, D-07 | MODELED |
| R-53 | M.RiskSignal, M.IdentificationTreatment, D-06, D-07 | MODELED |
| R-54 | M.IdentificationCase, M.VerificationAssessment, P-08 | MODELED |
| R-55 | M.Evidence, M.VerificationAssessment, D-13 | MODELED |
| R-56 | M.QualificationBasis, M.BeneficialOwnerStatus, M.VerificationAssessment | MODELED |
| R-57 | M.QualificationBasis.valid_from, D-12 | MODELED |
| R-58 | M.QualificationBasis, M.BeneficialOwnerStatus, M.ChangeEvent, D-12, P-09 | MODELED |
| R-59 | M.ChangeEvent, P-09 | MODELED |
| R-60 | M.RiskSignal, M.IdentificationTreatment, D-06, P-02 | MODELED |
| R-61 | M.IdentificationTreatment, D-06, P-02 | MODELED |
| R-62 | M.IdentificationTreatment, D-06 | MODELED |
| R-63 | M.DifferenceAssessment, P-10 | MODELED |
| R-64 | M.DifferenceAssessment, D-14 | MODELED |
| R-65 | M.DifferenceAssessment, D-14 | MODELED |
| R-66 | M.DifferenceAssessment, P-10 | MODELED |
| R-67 | M.DifferenceAssessment, D-14 | MODELED |
| R-68 | M.DifferenceAssessment, P-10 | MODELED |
| R-69 | M.DifferenceAssessment, D-14, P-10 | MODELED |

# 4. 69条规则的模型承接结论

本轮没有把69条规则等价成69个模型 Rule。领域模型做的是**去重复结构化**：

- R-07～R-15 共同落在 OwnershipHolding / UltimateOwnershipAssessment / QualificationBasis；
- R-22～R-31 共同落在 ControlRelation / Evidence / VerificationAssessment；
- R-46～R-53 共同落在 StateOwnedNatureAssessment + IdentificationTreatment；
- R-54～R-59 共同落在 IdentificationCase / VerificationAssessment / QualificationBasis / ChangeEvent；
- R-63～R-69 共同落在 DifferenceAssessment。

这符合领域模型的职责：抽象稳定结构，而不是复制知识规则文本。

# 5. 30个业务问题的模型覆盖

| 问题范围 | 主要模型能力 |
| --- | --- |
| Q-01～Q-04 对象、免于、简化、备案免报 | BaseRuleDecision + IdentificationTreatment |
| Q-05～Q-10 最终所有权 | OwnershipHolding + UltimateOwnershipAssessment |
| Q-11～Q-12 收益权/表决权 | EconomicRight |
| Q-13～Q-14 实际控制 | ControlRelation + Evidence + VerificationAssessment |
| Q-15 管理人员兜底 | ManagementResponsibility + D-05 |
| Q-16～Q-17 分支机构 | Branch + D-08/D-09 |
| Q-18～Q-20 信托、资管、社会组织 | Trust / AssetManagementProduct / Treatment |
| Q-21～Q-23 国企 | StateOwnedNatureAssessment + Treatment |
| Q-24～Q-27 核实与时间 | VerificationAssessment + QualificationBasis + ChangeEvent |
| Q-28 加强措施 | RiskSignal + IdentificationTreatment |
| Q-29～Q-30 差异与闭环 | DifferenceAssessment |

# 6. 上游 OPEN → 模型处理

| OPEN | 模型处理 | 是否自行补答案 |
| --- | --- | --- |
| O-01 循环/交叉持股算法 | UltimateOwnershipAssessment.path_completeness=CYCLIC_OR_CROSS；不产出低于阈值确定结论 | 否 |
| O-02 外部实控证据充分性 | ControlRelation保持CANDIDATE/INSUFFICIENT | 否 |
| O-03 多名管理负责人选择 | ManagementResponsibility允许多人；最终兜底选择不自动做 | 否 |
| O-04 多人管理资管产品 | ProductManagementRelation允许多人；不自动生成简化Basis | 否 |
| O-05 社会组织简化具体人员 | Treatment只判断简化适用性，不内置统一人员映射 | 否 |
| O-06 国有控制向下传播 | StateOwnedNatureAssessment只表达已确认性质，不新增传播算法 | 否 |
| O-07 自动放行/转人工 | 视为机构作业政策，不进入公共模型规则 | 否 |
| O-08 标准二+标准三展示口径 | 可保存多个事实/候选Basis；统一展示保持未决 | 否 |

# 7. 与旧版模型相比的结构性修正

## 7.1 不再把信托和资管塞进“非自然人主体”

旧版 `M.Subject` 同时承载：

- 公司；
- 合伙企业；
- 分支机构；
- 信托；
- 资产管理产品。

v3候选拆开，因为这些对象的法定基础识别规则不同。

## 7.2 不再用一个识别制度枚举承载两个维度

改为：

```text
BaseRuleDecision
+
IdentificationTreatment
```

前者决定第8/9/12-14条，后者决定免于/简化/加强。

## 7.3 UBO结果不再只是一条“人—主体—标准”关系

改为：

```text
基础事实
  ↓
QualificationBasis（每项依据独立有效期）
  ↓
BeneficialOwnerStatus（某时点当前状态）
```

这样可以保留多依据、历史变化和未知。

# 8. 当前不是正式 Domain DSL 的原因

正式 DSL 2.0 要求：

- `knowledge_ref.contract_version=4.0.0`；
- 精确绑定上游知识 `output.json`；
- 使用SHA-256 digest；
- `rule_coverage` / `question_coverage` / issue binding 均从固定知识合同校验。

当前上游 v3 知识仍是候选 `review.md + coverage.md`，还没有正式 `output.json`。

因此本轮有意使用 `model-candidate.yaml`，而不是伪造一个看似合同有效的 `model.yaml`。

# 9. 正式化条件

当 PR #8 的领域知识经业务确认并在项目运行环境生成正式 `output.json` 后：

1. 固定知识 artifact/digest；
2. 将本候选对象转为正式 DSL 2.0 Type / Rule / Judgment / Process；
3. 自动生成69条 rule_coverage；
4. 自动生成30条 question_coverage；
5. 绑定8个 upstream issue；
6. 用6个来源案例做解释/有限验证；
7. 生成正式 `model.yaml + review.md + coverage.md + output.json`。

在此之前，本候选用于验证**业务抽象是否正确**，而不是验证 DSL 语法。
