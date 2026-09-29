# A01 ECP V3 技术语义资产编制审阅

版本：`2026-09-29.v3-draft.1`

## 1. 本次完成了什么

本次从 Business Domain Model（业务领域模型）1.0.0 和 `ubo_mvp_standardized` 数据源结构建立一个 ECP V3（第三版）技术语义模型候选：

- 7 个业务对象、23 个业务关系全部进入 Ontology（本体）；
- 22 个业务判断全部进入 `implementation_map`（实现映射），但不强行全部自动化；
- 12 张具有稳定 Record Key（记录键）的源表进入 V3 Mapping（第三版映射）；
- `std_control_third_party` 因没有主键或唯一键，明确不进入 Mapping（映射）；
- 六个 SHACL（形状约束）检查点齐备；
- 6 个安全确定的 Derivation（派生）阶段已经生成；
- 36 个业务案例继续保留原始 expected / forbidden（预期结果 / 禁止结果），没有为适配技术实现而改写。

## 2. 当前 Mapping（映射）能够稳定形成的事实

当前源可以较稳定表达：

- 组织主体登记基础事实；
- 分支机构及总分隶属；
- 股权/股份关系的目标主体、比例、时效和来源；
- 收益权关系；
- 表决权关系；
- 控制关系及已采信标志；
- 合伙权益及执行事务合伙人委派代表；
- 人员任职的职位文本、权限描述和有效期间；
- AML/KYC（反洗钱/客户尽调）风险等级；
- 历史变更记录；
- UBO（最终受益所有人）参数及监管政策文档。

所有 12 个 Scan（扫描）均有 FULL_SNAPSHOT Coverage（全量快照覆盖）。源不可用、部分读取或拒绝行均要求传播为 `UNKNOWN`（未知），不得静默解释为不存在。

## 3. 为什么当前不能直接生成完整 UBO 结论

### 3.1 自然人身份主数据缺失

当前 13 张表中没有自然人身份主表，缺少身份证明号码、签发法域等稳定身份信息。因此不能完成 `UBO.Decision.IdentityVerification`（自然人身份核实），也不能把姓名直接作为自然人唯一身份。

### 3.2 股权持有人没有稳定 ID

`std_ownership_relation` 只有 `participant_name` 和 `owner_party_type_code`，没有 `owner_party_id`。因此可以计算“某一股权观察行比例是否达到 25%”，但不能安全地把该行绑定到唯一自然人/组织，更不能完成多层路径聚合。

### 3.3 任职关系只有姓名

`std_person_role_relation` 没有 `person_id`，因此法定代表人、日常经营管理人等角色不能安全绑定到 `UBO.NaturalPerson`（自然人）身份。

### 3.4 信托和资管产品源缺失

当前没有 Trust（信托）和 Asset Product（资产管理产品）的结构化源表，因此相关对象、关系和判断只能保留为 Ontology（本体）定义 + `UNSUPPORTED/EXTERNAL`（不支持/外部判断）。

### 3.5 外部上下文不完整

已有 `aml_risk_level_code`，但缺：

- `specific_risk_triggers`（具体风险触发事实）；
- `suspicious_flag`（可疑标志）；
- `IdentificationPurpose.purpose/as_of`（识别责任语境/判断时点）；
- `HistoricalTransaction.transaction_time`（历史业务时点）；
- `TrustInstitutionCooperation`（信托合作与受托机构履责）上下文。

这些缺口必须保持 `UNKNOWN`，不能自动当作低风险或不适用。

## 4. 本次真正自动化了什么

本次 Derivation（派生）严格限制在可以从当前源确定计算的事实：

1. 已采信且控制方类型明确为 PERSON（自然人）的控制记录 → 形成“控制候选”；
2. 单条直接股权比例 ≥25% → 形成阈值特征，但因持有人 ID 缺失，不形成自然人人选；
3. 单条收益权比例 ≥25% → 形成原始阈值特征；
4. 单条表决权比例 ≥25% → 形成原始阈值特征；
5. 单条合伙权益比例 ≥25% → 形成原始阈值特征；
6. 明确的执行事务合伙人委派代表自然人 ID → 可形成自然人类型事实。

**没有**自动实现：

- 最终间接持股穿透与多路径聚合；
- 实际控制专业判断；
- 国企特殊路径最终认定；
- 日常经营管理人兜底；
- 信托/资管产品识别；
- 最终 `IdentificationResult`（识别结果）和 `ResultIncludesPerson`（结果包含自然人）。

因此本版不会“为了跑通”而制造正式 UBO 人选。

## 5. ECP V3 边界

Mapping（映射）的 `ontologySourceDigest` 已绑定当前 `ontology.ttl` 精确字节。

本次使用技能内固定的 Kit 1.8（工具包 1.8）/ V3（第三版）参考能力快照作为作者依据，但它不是目标 Workspace（工作空间）实时能力回执。因此形成 `CAPABILITY_GAP.A01.TargetWorkspaceBoundary`（目标工作空间能力缺口），`candidate_closure`（候选闭包）保持 `BLOCKED`。

在取得真实 Workspace deployment boundary（工作空间部署能力回执）前：

- `platform_compiled = NOT_EXECUTED`（平台编译未执行）
- `released = NOT_EXECUTED`（发布未执行）
- `runtime_validated = NOT_EXECUTED`（运行验证未执行）

## 6. 下一步真正需要补的不是更多规则

当前最有价值的数据改造顺序是：

1. 给股权持有人补稳定 `owner_party_id`；
2. 给任职人员补稳定 `person_id`，并接自然人身份主表；
3. 补主体类型/法律形式/组织性质/所有制性质代码集；
4. 补信托与资管产品源；
5. 补 AML/KYC（反洗钱/客户尽调）具体风险触发事实；
6. 最后再考虑把更多 MIXED / PROFESSIONAL_JUDGMENT（混合判断/专业判断）拆成可执行规则。

当前版本的价值在于：已经把“业务模型哪些部分能由现有数据安全执行、哪些不能”精确暴露出来，而不是把数据缺口藏进算法。
