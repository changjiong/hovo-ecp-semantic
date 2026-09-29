# 05 ECP V3 语义资产编制输出

本目录由 `ecp-semantic-authoring 0.3.0` 按合同 `2.0.0` 生成，输入为：

- `A01受益所有人/04领域模型输出/output.json`
- `A01受益所有人/04领域模型输出/model.yaml`
- `A01受益所有人/02数据源与表结构/ubo_mvp_standardized.md`
- Semantic Authoring Kit 1.8（语义编制工具包 1.8）/ ECP V3（第三版）参考边界

正式技术语义资产：

- `ontology.ttl`：Business Domain Model（业务领域模型）对象、关系及本次源事实词汇；
- 六个 SHACL（形状约束）检查点：asserted、domain、feature、change、output、provenance；
- `mapping.json`：ECP V3 Mapping（第三版映射），12 个 Scan（扫描）、13 个 Projection（投影）、12 个 FULL_SNAPSHOT Coverage（全量快照覆盖）；
- `derivation.json`：仅包含当前数据可以安全确定的 6 个 Derivation（派生）阶段；
- `input.json`、`output.json`、`review.md`：阶段合同、交接闭包与人工审阅视图。

本版**不生成** Evaluation（求值）、Lifecycle（生命周期）和 Action Policy（动作策略）资产。原因不是遗漏，而是当前源结构不足以安全形成最终 UBO（最终受益所有人）结论，业务模型也没有授权任何自动外部动作。

当前 `candidate_closure`（候选闭包）保持 `BLOCKED`：本地技术资产可以生成，但尚未取得目标 Workspace（工作空间）的真实 deployment boundary（部署能力回执），不得进入 release（发布）阶段。
