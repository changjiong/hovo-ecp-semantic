# 随包上游合同快照

domain-knowledge.schema.json 与 domain-knowledge-common.schema.json 是领域知识 4.0.0 输出合同及其公共 Schema 的固定副本。它们只用于校验本技能接收的上游知识文件，不能替代领域知识技能、来源审查、业务确认或平台运行。

本包拒绝旧知识合同作为 3.0.0 模型合同的输入，不提供兼容层、迁移或本地回退。更新上游合同必须同时更新两个 Schema、输入输出约束、校验器和本文说明。
