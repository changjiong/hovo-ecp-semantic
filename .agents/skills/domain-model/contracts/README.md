# 合同 5.0.0 与 DSL 2.0.0

输入 input.schema.json 固定知识 4.0.0、scope_mode及问题范围、DRAFT/CONFIRMED 和评审方式。REVIEW 使用 subjects；REVISE 还需变更请求。CONFIRMED 入口必须有真实外部确认记录。

模型唯一来源为 model.yaml，结构见 domain-model.dsl.schema.json。output.schema.json 的 content 仅有 model_ref 与 request_ref；业务内容不再重复抄入 JSON。model_ref.contract_version=`domain-model-dsl/2.0.0`，request_ref.contract_version=`5.0.0`；请求没有独立内容版本，其引用 content_version 使用本次模型版本并以字节摘要锁定。

output.json 的 issues 是 DSL 问题清单原样投影，不是另一个编辑入口。input_refs 保留请求、知识、旧版对象；files 登记 DSL 及生成文档。修改 DSL 要重生成并更新摘要；不能只改 JSON 或文档来宣称覆盖完成。

结构检查、业务评审和确认各有独立状态。生成器保留 NOT_EXECUTED/PENDING；真实验证报告独立记录，不循环把报告写进自身摘要。正式确认必须绑定本次成果、model.yaml、review.md、coverage.md及责任人真实答复。旧版合同 3.0.0 不再是当前可生成格式；需要按固定知识重新建模，不能靠字段迁移冒充形式化。

所有 schema 随包离线解析。知识合同快照使用其原始命名空间；模型公共合同使用 domain-model/5，避免不同阶段同版号的 schema 身份碰撞。平台转译与编译不在本包范围，消费者必须显式升级到 DSL 2.0.0。

FULL_BASELINE必须覆盖上游全部问题；EXPLICIT_SUBSET须来自明确任务范围。新旧DSL和模型合同不兼容，旧版本只作历史归档，不提供迁移兜底。
