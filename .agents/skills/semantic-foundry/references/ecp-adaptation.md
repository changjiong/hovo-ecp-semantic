# ECP 平台适配

业务设计契约与 ECP 工作区是两种权威。前者保留来源、能力问题、对象身份、时间、采信政策、预期与禁止结果、未知处理和人工责任；后者只包含目标协议登记的机器资产。来源字段记录一个值，不能自动证明领域概念或已确认的现实事实。

每项重要业务承诺必须记录一种落点：直接由 [Profile](ecp-kit-1.7/standards/ecp-semantic-profile-1.0.md) 表达；由指定 SHACL Stage 检查；由有界 Derivation/Evaluation 计算；交给外部责任；或明确不支持并说明损失。不能删去不支持的公理后宣称等价。单一数据图的 SHACL 结果不是 OWL 一致性，计算路径也不是已断言事实或已批准决定。

| 资产 | 负责 | 不负责 |
| --- | --- | --- |
| Ontology | Class/Property 含义和受支持蕴含 | 完整性、来源访问、批准 |
| Mapping | 来源引用、Scan/Join、稳定 IRI、投影、Coverage | 凭据、任意 SQL、实时 schema 证明 |
| SHACL | 指定 Stage 的图验证 | 通用 SHACL/SPARQL、未执行的实例覆盖 |
| Derivation | 有界类型化事实转换 | 新 Runtime 算子、来源访问 |
| Evaluation | 对象级 Candidate 与证据投影 | 正式 Decision、Action 回执、Outcome |
| Action Policy | 逻辑 Capability 绑定 | Endpoint、Token、连接器成功 |
| Scope | 从 Root 出发的关系型事实闭包 | Evaluation objectScope、SQL、部署坐标 |

`Evaluation.objectScope` 选择语义对象；Release `SCOPE` 选择来源事实，两者不可替代。Mapping 只能基于已授权的真实 schema 与稳定 source binding 编写。随包 `schema.json` 只供审阅，不能证明当前 Hovo 的数据源、表/View、字段或关系仍可用。缺真实 schema 时可以交付设计，但 Mapping 与数据运行验收必须标为 `BLOCKED`；样例必须标明合成。

格式以 Kit 原文和机器合同为准：[Ontology Turtle](ecp-kit-1.7/guides/ecp-ontology-ttl-format.md)、[Mapping JSON](ecp-kit-1.7/guides/ecp-mapping-json-format.md) 及其 [Schema](ecp-kit-1.7/contracts/mapping-definition-v1.schema.json)、[SHACL Turtle](ecp-kit-1.7/guides/ecp-shacl-turtle-format.md)、[Derivation](ecp-kit-1.7/guides/ecp-derivation-json-format.md)、[Evaluation](ecp-kit-1.7/guides/ecp-evaluation-json-format.md)、[Action Policy](ecp-kit-1.7/guides/ecp-action-policy-json-format.md) 及其 [Schema](ecp-kit-1.7/contracts/action-policy-v1.schema.json)、[Scope](ecp-kit-1.7/guides/ecp-scope-json-format.md) 及其 [Schema](ecp-kit-1.7/contracts/scope-definition-v1.schema.json)、[Rule Set Bundle](ecp-kit-1.7/guides/ecp-rule-set-bundle-format.md) 及其 [Manifest Schema](ecp-kit-1.7/contracts/rule-set-bundle-manifest-v1.schema.json)。Derivation/Evaluation 的完整计划由版本化平台编译器所有，没有公开 JSON Schema 可替代。说明文字不能取代 Schema 或平台编译器。

Rule Set 含 SHACL 时，必须唯一绑定 `asserted`、`domain`、`feature`、`change`、`output`、`provenance` 六个 Stage；部分绑定不能进入 Engine Run。各 Stage 看到的图和通过策略由 [Profile 第 6 节](ecp-kit-1.7/standards/ecp-semantic-profile-1.0.md) 定义，不能用空 Stage 或后续推理掩盖原始缺值。

任何资产不得含 SQL、JavaScript、回调、连接参数、密钥、Endpoint、S3 坐标或本地暂存路径。`compilerContract.expect` 是编译器证据，不是作者注释；只可来自该 Rule Series 与 Definition 字节对应的平台预检。没有该证据时，Evaluation Definition 只能留在正式 Rule Set 外，并报告 `NOT_EXECUTED`。

内容经确认后，先单独运行 `refresh_workspace_digests.py` 更新受影响的清单摘要，再对最终字节执行本地校验，最后打包同一清单闭包。打包不得刷新摘要；任何正文变化都会废弃旧摘要和相关检查证据。Ontology 原始摘要变化还要求平台按 Mapping Series 创建与之绑定的新 Revision，不能只改 Workspace 文本。

业务审查、本地静态检查、Draft 预检、Release 编译和 Run 证据必须分列。`LOCALLY_VALID` 只表示列出的本地检查通过，绝不表示已导入、已编译、已发布、已连接当前来源或已获业务批准。
