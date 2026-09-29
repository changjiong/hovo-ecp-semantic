# A01 ECP V3 技术语义资产编制审阅

版本：`2026-09-29.v3-authoring.1`

## 结论

本次已从固定 Business Domain Model（业务领域模型）与 `ubo_mvp_standardized` 真实结构生成一个 ECP V3（第三版）技术语义模型候选闭包。候选严格区分“平台可直接表达/计算的源内事实”与“仍需身份核实、路径完备性、法律效力或专业判断的业务结论”。

本次没有把任何原子阈值结果冒充最终 UBO（受益所有人）结论。

## 数据结构落地

- 数据源：`ubo_mvp_standardized / UNKNOWN`（结构快照未声明运行环境）
- 文档声明表：13 张
- 可形成稳定 V3 Scan（扫描）的表：12 张
- 排除：`std_control_third_party` 无声明主键，不能构造稳定 Record Key（记录键）
- Mapping Projection（映射投影）：34
- Mapping Filter（映射过滤）：12
- Coverage（覆盖声明）：FULL_SNAPSHOT（全量快照），缺源/部分读取/拒绝行均传播为 UNKNOWN（未知）

## 已生成资产

- Ontology（本体）1 份
- SHACL（形状约束）6 个检查点：asserted（声明）、domain（领域）、feature（特征）、change（变化）、output（输出）、provenance（证据）
- V3 Mapping（第三版映射）1 份
- Derivation（派生）1 份，6 个原子阶段
- Evaluation（求值）1 份，3 个 SCOPED_DECISION（限定范围判断）阶段
- Lifecycle（生命周期）与 Action Policy（动作策略）：当前 Business Domain Model（业务领域模型）没有平台动作或状态迁移承诺，本版不生成空资产

## 自动化边界

当前自动化仅覆盖可由已给结构安全推出的原语，例如：
- 合伙关系中的 PERSON/SUBJECT（自然人/主体）分类转为权益关系候选；
- 已给单段比例的 25% 阈值比较；
- 收益权、表决权单段比例的 25% 阈值比较。

以下仍不是自动结论：
- 间接股权穿透及同一自然人多路径聚合；
- 自然人真实身份同一性；
- 实际控制的法律与事实认定；
- 日常经营管理人备位；
- 国资特殊路径最终资格；
- 信托、资管产品人选；
- 完整历史时点 UBO（受益所有人）还原；
- 最终 IdentificationResult（识别结果）形成。

## 关键数据缺口

1. 缺自然人身份主表，无法落实证件号、签发法域等身份同一性。
2. `std_ownership_relation` 缺 `owner_party_id`，无法建立稳定股东节点和可靠的间接权益图。
3. `std_person_role_relation` 只有姓名、无稳定自然人 ID。
4. 无信托对象与信托角色表。
5. 无资管产品对象与产品角色/权利表。
6. 无统一 Evidence（证据）主表，仅关系记录中散落来源/文档引用。
7. 缺识别责任语境 purpose/as_of。
8. AML/KYC（反洗钱/客户尽调）仅有风险等级，缺 specific_risk_triggers（具体风险触发）与 suspicious_flag（可疑标志）。
9. 缺 HistoricalTransaction.transaction_time（历史业务时点）。
10. 缺 TrustInstitutionCooperation（信托合作履责上下文）。
11. 无最终识别结果持久化结构。
12. `std_control_third_party` 无主键。
13. 主体 ID 在 `std_subject` 为 bigint（大整数），多个关系表为 varchar（字符串），需要数据负责人确认规范身份一致性。

## 模型开放问题

上游三个 MODEL_GAP（模型缺口）原样保留：`GAP.A01.StateControlScope`、`GAP.A01.TrustSimplifiedPersonSemantics`、`GAP.A01.OtherProductSimplifiedPersonSemantics`。技术层不得自行补口径。

## 验证状态

有限静态闭包检查：PASS（通过）。

目标 Workspace（工作空间）原生 Candidate Compile（候选编译）：NOT_EXECUTED（未执行）。当前仓库只携带 Kit 1.8（工具包 1.8）能力快照，不冒充目标 Workspace 的实时部署回执。
