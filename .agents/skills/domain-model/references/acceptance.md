# Domain Model（领域模型）验收

- [ ] 业务审阅稿第一屏能直接回答“这个业务世界有哪些稳定对象、关系和领域判断”，无需先理解 YAML（层级配置格式）、DSL（领域专用语言）或 Process（流程）。
- [ ] 核心模型以对象、关系、事实、证据、时间和领域判断为中心，不以 Rule（规则）数量、Process（流程）数量或可执行程度证明完整。
- [ ] 每条范围内 Knowledge Rule（知识规则）都有 `modeling_classification` 和明确理由：CORE_STRUCTURE（核心结构）、DOMAIN_DECISION（领域判断）、EXTERNAL_CONTEXT（外部上下文）或 NO_MODEL_CHANGE（无模型变化）。
- [ ] `NO_MODEL_CHANGE` 没有被强行创建模型元素；纯 `EXTERNAL_CONTEXT` 没有扩张成邻接领域模型。
- [ ] 多条知识规则反复依赖同一结构时复用同一模型元素，没有“一条 Rule 一个 Type”的机械翻译。
- [ ] Domain Decision（领域判断）绑定真实业务事实，输出明确结果；UNKNOWN（未知）不能自动变成 false（否）或 0。
- [ ] non_sufficient_facts（非充分事实）没有被错误设计成可单独触发结果的条件。
- [ ] 固有人工判断有证据、准则和责任；“DSL暂不能执行”没有被错误标成人工裁量。
- [ ] Evidence（证据）与被证明的关系/事实分开；证据来源不能直接替代业务事实。
- [ ] 关系和安排的有效时间可表达，当前状态不会覆盖历史。
- [ ] Process（流程）和 StateMachine（状态机）不是强制项；若存在，能说明为什么它本身是稳定领域事实而不是实现流程。
- [ ] Question（业务问题）仅用于二次覆盖检查；Case（案例）沿用上游 input_facts / expected / forbidden（输入事实/预期/禁止结果），不改写真值。
- [ ] 全部上游 OPEN（未决）有去向，未被建模默认值静默关闭。
- [ ] review.md（业务审阅稿）使用业务语言；coverage.md（覆盖审计）保存规则分类、理由和精确模型映射。
- [ ] 下游 ECP（可执行语义协议）可以从 Domain Knowledge + Domain Model 继续转译，而无需 Domain Model 自己承担平台执行逻辑。
