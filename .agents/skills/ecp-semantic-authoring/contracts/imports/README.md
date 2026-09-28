# 输入合同快照

domain-model.schema.json 与 domain-common.schema.json 是当前 domain-model 5.0.0 输出合同的固定快照，用于核对被确认的领域模型交付。

它们不是运行时依赖，也不允许自动读取其他技能目录的最新版。业务模型正文由 domain-model 输出中的 model_ref 指向 business-domain-model/1.0.0 文件。
