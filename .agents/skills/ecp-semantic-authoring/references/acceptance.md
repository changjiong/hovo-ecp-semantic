# 忠实转译与 ECP 验收

以固定 Domain Model 2.0.0 及当前目标 Profile 为输入。模型的概念、属性、关系、语义政策、判断机理及步骤都应进入实现对应或明确能力缺口，不能只接收新结构而漏掉新增业务承诺。方法见本地手册 02 §5-6；ECP 表达从 [Kit README](ecp-kit-1.7/README.md)、[Profile](ecp-kit-1.7/standards/ecp-semantic-profile-1.0.md)、[平台适配](ecp-adaptation.md) 路由到具体指南。随包 Kit 1.7 只证明参考版本，不证明目标环境已安装同版能力。

1. 每个模型概念、业务属性、关系及机理都有实现对应或明确 Gap。固定 IRI、类型、domain/range 与语义身份；不得用字段缩写命名业务概念。
2. 逐条检查直接表达、SHACL 检查、Derivation 计算、Evaluation 判断、Action Policy 或外部责任的分工。不要让 OWL 承担闭世界判定，也不要让 SHACL 代替监管决策树。
3. 保留原有单位、有效时间、身份、基数、未知处理、算法前提与结论权威。平台约束迫使语义改变时返回模型阶段，不能删要求或改阈值来通过编译。
4. 使用 Kit 的正式 wire。Mapping 和 Scope 由 ecp-data-mapping 在真实结构阶段编制；本阶段输出它们必须供给的事实要求，不推测来源字段。
5. Rule Set 含 SHACL 且用于 Engine Run 时，必须具有 asserted/domain/feature/change/output/provenance 六个 Stage 的完整唯一绑定。单纯本体审查不虚造空 Stage；尚未具备运行所需形状时明确阻塞。
6. Evaluation Definition 和 EvaluationAsset 分开。没有针对相同 Rule Series 和 Definition 字节的平台预检结果，就把 Definition 标为 DRAFT_ONLY 放在导入包外；不得自填 `compilerContract.expect`、摘要或编译器版本。发布阶段取得的诊断返回本技能，由本技能完成 Envelope 后重新检查。
7. 规则身份、依赖谓词、结果类型、证据投影及测试合同标识应一致。Case 标识指向验收规格，不自动授权生成测试代码；预期不得为了匹配实现而改变。
8. Action Policy 只引用逻辑能力，不含 Endpoint、Token 或任意回调。规则产生 Candidate 不能被说明为正式 Decision 或已执行行动。
9. 资产与输出文件的真实摘要一致；本地有限检查与平台编译证据分开。没有平台证据，状态为 NOT_EXECUTED。

审查稿包括领域模型到 IRI/规则的对应、表达取舍、依赖、事实要求、案例落实和 Capability Gap。语义实现负责人确认精确版本后才交给 Mapping；业务定义变化先返回 domain-model。

本目录提供工具：`scripts/validate_ecp_assets.py` 做有限静态检查，`scripts/validate_shacl_instance.py` 做标准 SHACL 实例检查。执行遵守当前任务授权与工作区验证规则，工具成功不证明 ECP 编译或真实数据运行。
