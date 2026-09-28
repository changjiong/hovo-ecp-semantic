# 跨阶段合同 2.0.0

semantic-foundry 当前只编排四个生产技能：domain-knowledge、domain-model、ecp-semantic-authoring、ecp-semantic-release。

本目录的 pipeline.schema.json 只登记阶段身份、状态、精确输入输出引用、确认依据和变更，不复制阶段正文。各生产技能维护自己的合同版本与验收规则。

关键边界：
- domain-model 保持平台与数据无关；
- ecp-semantic-authoring 同时承接 ECP V3 技术表达和真实数据 Mapping；
- authoring 的语义确认与数据确认是同一输出上的两个治理责任；
- ecp-semantic-release 只承担 Revision、候选编译、发布、回读和 Run 等平台副作用。

Schema 合格只表示结构条件。业务确认、数据确认、平台操作授权、编译、发布、运行与业务验收必须分别有真实依据。

ArtifactRef 使用稳定 artifact_id、content_version、contract_version、相对 path 和 SHA-256；任何内容改变都会使绑定旧摘要的确认和平台证据失效。
