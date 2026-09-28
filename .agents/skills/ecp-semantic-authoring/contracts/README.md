# ecp-semantic-authoring 资产合同 2.0.0

2.0.0 是破坏性合同：删除独立 ecp-data-mapping 阶段，把 Mapping 与 Ontology、SHACL、Derivation、Evaluation、Lifecycle、Action Policy 放进同一个 authoring 输出闭包。

输入以 domain-model 5.0.0 的 output.json 为业务基线，并要求真实 Schema 快照、数据源身份、Semantic Authoring Kit 1.8、语义 Profile、目标部署能力回执和案例。imports/domain-model.schema.json 与 imports/domain-common.schema.json 固定当前 domain-model 5.0.0 交付合同。

output.json 的 content 同时记录 domain_model、business_model、平台 Profile、目标部署能力、Schema 快照、实际 V3 资产、implementation_map、fact_bindings、case_bindings 与 candidate_closure。

READY 只表示本地闭包完整，不表示目标平台已经编译。平台编译状态在本阶段保持 NOT_EXECUTED，真实编译由 ecp-semantic-release 记录。

确认仍然职责分离：语义实现负责人和数据负责人分别确认同一精确 authoring 输出。发布阶段必须同时取得这两份外部确认记录。
