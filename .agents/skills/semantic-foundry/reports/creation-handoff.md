# Semantic Foundry 0.5.0 交接

按用户指定顺序生成五个0.1.0技能：domain-knowledge、domain-model、ecp-semantic-authoring、ecp-data-mapping、ecp-semantic-release。semantic-foundry 仅承担编排，维护共享合同与参考工具。

每个技能具备独立入口、输入/输出 Schema、验收清单、README、manifest 和接口；跨阶段共用版本、摘要、证据、确认与案例结构。具体研究参考、设计取舍和未验证事项见 [建设记录](pipeline-creation.md)。

参考技能是 qiaomu-meta-skill、OntologyEX 的 ontology-extraction、ontology-agent-suite。前者贡献合同与证据边界；OntologyEX 提供领域与应用映射分工；ontology-agent-suite 提供阶段审阅与决定记录。采用用户要求的精确版本确认，拒绝固定类数量、机械字段搬家、未授权下游改写和自动发布。

以上属于 design advantage；减少概念污染与反复访谈属于 hypothesis，尚无模型行为或专家对照证据。技能包与合同的静态检查另行报告，不能转换成平台能力证明。

本次未改 A01 业务成果，未修改测试代码，未执行平台导入、发布或 Run。旧0.4.0验证记录保留为历史，本次五技能的模型评估、专家确认和安装证据均未取得。
