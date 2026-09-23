# A01 受益所有人领域模型审阅稿（v3候选）

> 模型候选版本：0.1.0  
> 上游知识：`03领域知识输出-v3候选/review.md` 3.1.0-draft  
> 状态：DRAFT（草案），用于业务模型审阅。  
> 注意：当前上游知识尚未生成固定的 Contract 4.0.0 `output.json`，因此本目录暂不声称 `model-candidate.yaml` 已通过 Domain DSL 2.0 合同校验。

# 1. 这版模型解决的核心问题

上一版 A01 领域模型把“公司、合伙企业、分支机构、信托、资产管理产品”都放进了一个“非自然人主体”对象中，并把后续大量规则围绕这个统一主体展开。

新的领域知识已经证明这种抽象过早：

- 第8条针对法人、非法人组织；
- 第9条单独规定分支机构；
- 第12、13条单独规定信托；
- 第14条单独规定资产管理产品，而且只是“参照第8条”；
- 第10、11、13、14、20、21、25条又在基础规则之上规定免于、简化和加强措施。

因此本版模型最重要的修正是：

> **“识别对象适用哪套基础规则”与“是否采取免于、简化、加强措施”分开建模。**

不再把它们压成一个“一般 / 简化 / 免于 / 加强”枚举，也不再把信托、资管错误放进第8条所谓“一般识别”的子类。

# 2. 领域模型总览

## 2.1 现实业务对象

本版不再用一个 `M.Subject（非自然人主体）` 吞并所有对象，而是拆为：

| 模型对象 | 现实业务含义 |
| --- | --- |
| `M.Person` | 最终被识别、核实的自然人 |
| `M.Organization` | 法人、非法人组织，第8条的主要对象 |
| `M.Branch` | 国内/外国公司分支机构，第9条对象 |
| `M.Trust` | 信托，第12、13条对象 |
| `M.AssetManagementProduct` | 资产管理产品，第14条对象 |
| `M.IdentificationObject` | “本次识别针对谁”的抽象角色；只用于统一任务引用，不改变上述法律性质 |

`M.IdentificationObject` 不是说“信托也是组织”。它只是一次识别任务引用目标的业务抽象，并通过 `object_kind` 保证实际对象仍然是 Organization / Branch / Trust / AssetManagementProduct 中的一种。

## 2.2 基础事实

真正驱动 UBO（最终受益所有人）判断的基础事实包括：

| 模型对象 | 业务事实 |
| --- | --- |
| `M.OwnershipHolding` | 直接股权、股份、合伙权益 |
| `M.EconomicRight` | 收益权或表决权 |
| `M.ControlRelation` | 经证据支持的实际控制关系 |
| `M.ManagementResponsibility` | 负责日常经营管理的事实 |
| `M.TrustPartyRelation` | 委托人、受托人、受益人、监察人关系 |
| `M.ProductManagementRelation` | 自然人与资产管理产品之间的实际管理关系 |
| `M.Evidence` | 支撑身份、权利、控制、时间、主体性质的证据 |

这些事实与 UBO 结论分开。比如“法定代表人”“董事长”“第一大股东”“第三方平台实控人标签”只是可能进入事实/证据层，不直接等同 UBO。

# 3. 最关键的两个判断层

## 3.1 第一层：基础识别规则判断

`M.BaseRuleDecision` 回答：

> **当前对象适用12号令哪一组基础规则？**

~~~text
Organization
  → ARTICLE_8_ORG

Domestic Branch
  → ARTICLE_9_DOMESTIC_BRANCH

Foreign Company Branch
  → ARTICLE_9_FOREIGN_BRANCH

Trust
  → ARTICLE_12_13_TRUST

Asset Management Product
  → ARTICLE_14_ASSET_PRODUCT
~~~

这一步把上一轮讨论中的混维问题彻底切开。

资产管理产品虽然第14条要求“参照第8条”，模型仍然记录为 `ARTICLE_14_ASSET_PRODUCT`，而不是把产品强行转成 `ARTICLE_8_ORG`。

## 3.2 第二层：识别措施判断

`M.IdentificationTreatment` 回答：

> **基础规则确定以后，是否免于识别、可以简化，或者因风险必须加强？**

模型不是一个四选一枚举，而是：

~~~text
relief:
  NONE
  EXEMPT
  SIMPLIFIED
  UNKNOWN

enhanced_required:
  true / false / unknown
~~~

这样可以表达：

- 第10条：`relief=EXEMPT`
- 第11/13/14条：`relief=SIMPLIFIED`
- 第20/21条：`enhanced_required=true`
- 第25条：一旦加强情形成立，不得同时保持 EXEMPT / SIMPLIFIED

因此“加强识别”是风险增强层，不是和第8/9/12/14条互相替代的对象分类。

# 4. 第8条法人、非法人组织模型

## 4.1 标准一：最终所有权

模型将“直接持有事实”和“最终所有权结果”分开：

~~~text
OwnershipHolding
      ↓
同一自然人的有效路径计算/汇总
      ↓
UltimateOwnershipAssessment
      ↓
>=25%
      ↓
QualificationBasis
STANDARD_1_OWNERSHIP
~~~

关键边界：

- `OwnershipHolding` 只表达直接关系；
- `UltimateOwnershipAssessment` 才表达派生的最终比例；
- 多路径可以汇总，但必须避免重复经济权益；
- 路径不完整时不能把未知按0处理；
- 循环/交叉持股标为 `CYCLIC_OR_CROSS`，领域模型不自行发明精确图算法。

## 4.2 标准二：收益权 / 表决权

`M.EconomicRight` 分开记录：

- BENEFIT_RIGHT；
- VOTING_RIGHT。

标准二只对**同一自然人未满足标准一**时生效。

这解决了旧模型里“同一人的多个权利事实”和“最终认定标准”可能混为一谈的问题。

## 4.3 标准三：实际控制

`M.ControlRelation` 不是一个简单布尔值，而是承载：

- controller；
- target；
- control_modes；
- 有效时间；
- 证据；
- verification_status。

`control_modes` 包括：

- 人事任免；
- 重大经营管理决策；
- 财务收支；
- 重要资产/主要资金；
- 协议控制；
- 联合控制。

职位、第一大股东或第三方“实控人”标签不直接创建 `ControlRelation(CONFIRMED)`。

## 4.4 日常经营管理人员兜底

`M.ManagementResponsibility` 独立于任职头衔。

进入管理人员兜底必须同时满足：

~~~text
标准一：已完成判断且不存在
标准二：已完成判断且不存在
标准三：已完成判断且不存在
~~~

而不是：

~~~text
标准一/二/三资料不全
→ 为了完成流程
→ 直接找总经理/董事长兜底
~~~

# 5. UBO结果为什么拆成两层

## 5.1 QualificationBasis：认定依据

每一项依据独立记录：

- person；
- target；
- basis_type；
- valid_from / valid_to；
- evidence；
- source_fact_refs；
- verification_status。

例如：

~~~text
甲
→ A公司
→ STANDARD_1_OWNERSHIP
→ 2025-01-01起
~~~

和：

~~~text
甲
→ A公司
→ STANDARD_3_CONTROL
→ 2026-03-01起
~~~

在业务上是两项不同依据。

## 5.2 BeneficialOwnerStatus：当前是否为UBO

`M.BeneficialOwnerStatus` 是时点判断：

~~~text
person + target + as_of
        ↓
当前有哪些有效且已核实的QualificationBasis？
        ↓
ACTIVE / INACTIVE / UNKNOWN
~~~

这样能够正确表达：

> 某一项认定依据失效，并不意味着这个自然人一定退出 UBO；只有相关依据全部失效且事实完整时，才能确定 INACTIVE。

同时避免过早强行给“多依据情况下的唯一总体形成日期”下结论。只有历史完整、连续性已验证时才生成 `overall_active_since`。

# 6. 分支机构、信托、资管的专门结构

## 6.1 境内分支机构

~~~text
Branch
→ parent Organization
→ 获取所属主体当前UBO
→ 满足第9条复用前提时复用既有尽调
→ DOMESTIC_BRANCH_INHERITANCE
~~~

“继承”是结果形成机制，不是把分支机构自身当普通公司重新穿透。

## 6.2 外国公司分支机构

~~~text
Foreign Company Branch
├─ 所属外国公司按第8条识别的UBO
└─ 至少一名分支机构高级管理人员
~~~

上层存在境外股东 ≠ 目标对象是外国公司分支机构。

## 6.3 信托

~~~text
Trust
├─ 信托当事人
│   ├─ 委托人
│   ├─ 受托人
│   ├─ 受益人
│   └─ 监察人（如有）
├─ 非自然人当事人继续追溯
└─ 其他最终有效控制自然人
~~~

未明确具体受益人时，模型记录受益人范围，不虚构 Person。

## 6.4 资产管理产品

~~~text
AssetManagementProduct
        ↓
第14条基础规则
        ↓
根据产品情况和风险参照第8条
        ↓
若满足公开募集/发行 + 依法备案登记等条件
        ↓
可简化识别管理产品的自然人
~~~

多人团队/委员会下究竟选谁，仍保持 `O-04`，不由领域模型擅自选择。

# 7. 国企性质与简化识别

国企模型拆成两个判断：

~~~text
StateOwnedNatureAssessment
        ↓
IdentificationTreatment / QualificationBasis
~~~

也就是说：

> **“这是不是国有控股公司”**  
> 和  
> **“是否可以按第11条第七项把法定代表人识别为UBO”**

绝不是同一个布尔值。

`M.StateOwnedNatureAssessment` 可以表达：

- 国有独资；
- 国有控股；
- 国有实际控制；
- 国有参股；
- 非国有；
- UNKNOWN。

≤50%且第一大股东时仍要单独核实实际支配。

第三方平台标签进入 `Evidence`，不能直接写入 `nature=STATE_CONTROLLED`。

# 8. 时间模型

这版时间不再只挂在最终 UBO 结果上。

以下事实都具有自己的有效时间：

- OwnershipHolding；
- EconomicRight；
- ControlRelation；
- ManagementResponsibility；
- TrustPartyRelation；
- ProductManagementRelation；
- QualificationBasis。

时间推导原则：

~~~text
基础事实生效
      ↓
认定所需全部前提同时满足
      ↓
QualificationBasis.valid_from
~~~

当必要前提失效：

~~~text
对应QualificationBasis终止
~~~

然后再判断该人是否还有其他有效依据。

`ChangeEvent` 用于记录会触发重新审核的事实变化，不把当前状态覆盖到历史。

# 9. 识别与核实

模型显式分出：

- `IdentificationCase`：一次识别任务；
- 候选事实/依据；
- `VerificationAssessment`：身份、权利、控制、时间、对象性质分别核实。

因此：

~~~text
BOMIS返回一个人
≠
已核实UBO

第三方平台推荐一个人
≠
已核实UBO

模型算法计算出一个候选人
≠
已核实UBO
~~~

这些都只能成为识别或证据输入。

# 10. 风险加强与差异

## 10.1 风险

`M.RiskSignal` 保存第20条触发事实，而不是只有“高风险=true”。

`M.IdentificationTreatment.enhanced_required` 决定是否进入加强措施。

加强后：

- 可以补充信息、独立验证、补协议、回访、实地走访；
- 可以将权益阈值收紧到如10%；
- 可以提高更新频率；
- 可以要求高级管理层批准。

但不会直接把客户状态写成“拒绝”。

## 10.2 差异

`M.DifferenceAssessment` 区分：

- UBO不匹配；
- 关键身份重大差异；
- 权利类型重大差异；
- 形成/终止时间年月差异；
- 非重大权利差异；
- 机构采用更严格标准造成的差异；
- 应备案未备案。

并单独记录差异原因：

- 机构识别错误；
- 备案错误；
- 近期真实变化；
- UNKNOWN。

差异报告与可疑交易报告保持独立。

# 11. 十个核心业务过程

模型候选包含：

1. `P-01` 识别对象与基础规则选择；
2. `P-02` 识别措施判断；
3. `P-03` 法人/非法人组织第8条识别；
4. `P-04` 分支机构识别；
5. `P-05` 信托识别；
6. `P-06` 资产管理产品识别；
7. `P-07` 国企性质与简化；
8. `P-08` 结果核实与形成；
9. `P-09` 持续审核和历史维护；
10. `P-10` BOMIS差异反馈。

这些 Process（业务过程）用于说明业务依赖，不是生产工作流引擎。

# 12. 仍未进入模型硬规则的8个问题

模型完整保留上游 O-01～O-08：

- 循环/交叉持股算法；
- 缺治理文件时实控证据充分性；
- 多名日常经营管理负责人选择；
- 多人团队管理资管产品时具体选谁；
- 社会组织简化具体识别人员；
- 国有实际控制关系向下传播；
- 自动放行/转人工阈值；
- 同一人标准二+标准三时统一展示口径。

这些 OPEN 不是“模型没做完”，而是**上游业务知识尚无确定答案**。领域模型的责任是准确保留缺口，不能自己补政策。

# 13. 与旧版模型相比最重要的收敛

| 旧版倾向 | v3候选 |
| --- | --- |
| 一个“非自然人主体”覆盖公司、分支、信托、资管 | Organization / Branch / Trust / AssetManagementProduct 分开 |
| “一般/简化/免于/加强”容易平铺 | 基础规则 + 措施调整两维 |
| UBO关系携带一个认定标准 | QualificationBasis 独立，BeneficialOwnerStatus汇总当前状态 |
| 直接持有和最终持有容易混 | OwnershipHolding 与 UltimateOwnershipAssessment 分开 |
| 职位可能靠近兜底结果 | ManagementResponsibility 独立于职位 |
| 国企性质与简化容易耦合 | StateOwnedNatureAssessment 与 Treatment/Basis 分开 |
| 当前结果容易压掉历史 | 基础事实和依据均有独立有效期 |
| DSL求值能力容易主导模型 | 复杂算法保留业务语义，具体实现留后续阶段 |

# 14. 建议你重点审的五个问题

1. **对象拆分是否正确**：Organization / Branch / Trust / AssetManagementProduct 是否已经符合12号令的真实业务分类？
2. **两个判断维度是否正确**：基础规则 vs 免于/简化/加强措施，是否比“四种识别制度”更符合业务？
3. **QualificationBasis + BeneficialOwnerStatus 是否符合你实际记录UBO的方式？**
4. **时间是否应该挂在每项认定依据上，而不是只给一个UBO形成日期？**
5. **O-01～O-08 中哪些其实你作为业务专家已经可以直接给出明确答案？**
