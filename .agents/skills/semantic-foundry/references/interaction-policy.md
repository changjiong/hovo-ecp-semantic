# 阶段审查、访谈与确认

当前流程有四个生产阶段，但确认责任不是“四个人一次签完”。

1. domain-knowledge：领域负责人确认知识基线。
2. domain-model：领域负责人确认 Business Domain Model。
3. ecp-semantic-authoring：对同一个技术语义模型输出保留两份独立确认：
   - 语义实现负责人确认业务模型被忠实表达；
   - 数据负责人确认真实源绑定、身份、Join、NULL、时间、Coverage 与 UNKNOWN 传播。
4. ecp-semantic-release：平台写入、候选编译、发布和运行分别依用户授权与真实回执；业务验收另行记录。

authoring 的双确认是治理职责分离，不是两个串行技能，也不产生两个可以彼此漂移的技术模型版本。

每次确认必须绑定精确 ArtifactRef、范围和真实答复记录。内容或摘要变化后原确认失效；不得把“继续”“Schema VALID”或编译成功推断为业务、数据或发布批准。

状态仍使用 DRAFT、AWAITING_CONFIRMATION、CONFIRMED、REJECTED、STALE、BLOCKED。某个子范围阻塞时，只阻塞依赖它的后续，不伪造通过状态。
