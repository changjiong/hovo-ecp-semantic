# Knowledge → Domain Model（知识 → 领域模型）

## 任务

基于固定版本 Domain Knowledge（领域知识），形成平台无关的 Domain Model（领域模型）。

领域模型只表达：

1. **稳定业务结构**：对象、关系、事实、角色、安排、证据、时间；
2. **稳定领域判断**：这些事实怎样形成业务判断和业务结果。

不要重新解释法规，不要复制整段 Knowledge Rule（知识规则），不要为了覆盖而创建对象，也不要把机构流程、数据库、接口或平台执行机制塞进模型。

## 第一步：逐条 Rule 做范围审计

对每条 Knowledge Rule 先回答两个问题：

1. 它是否揭示了新的稳定业务结构？
2. 它是否定义了一个稳定领域判断？

据此填写 `modeling_classification`：

- `CORE_STRUCTURE`：有新的或需要复用的稳定结构；
- `DOMAIN_DECISION`：有稳定领域判断；
- `EXTERNAL_CONTEXT`：只提供邻接领域上下文；
- `NO_MODEL_CHANGE`：不产生本领域结构或判断变化。

规则可同时为 `CORE_STRUCTURE + DOMAIN_DECISION`。  
`NO_MODEL_CHANGE` 不得与其他分类组合。

不要因为 Rule 存在就强行生成 model element（模型元素）。

## 第二步：只抽最小稳定结构

对 `CORE_STRUCTURE` 规则，寻找：

- 谁/什么具有独立业务身份？
- 对象之间有什么长期稳定关系？
- 关系上有哪些重要事实？
- 关系何时形成、何时终止？
- 什么证据支撑这些事实？
- 是否存在权利/控制安排改变表面关系？

只有满足上述业务需要时才建立 Type（类型）或字段。

以下通常不应成为独立对象：

- 阈值；
- 布尔条件；
- “高风险”等标签；
- 规则编号；
- 流程步骤；
- 查询/审批动作；
- 只为技术实现存在的中间量。

优先用少量通用结构解释多条 Rule，而不是一条 Rule 一个 Type。

## 第三步：抽象稳定领域判断

对 `DOMAIN_DECISION` 规则，明确：

- 输入哪些已存在的业务事实；
- 输出什么业务判断/结果；
- 哪些事实单独不足以证明结果；
- 缺证时返回 FALSE（否）、UNKNOWN（未知）还是阻断判断；
- 哪些部分可以确定计算；
- 哪些部分是业务固有人工裁定。

### 确定判断

长期稳定、跨实现的阈值、布尔、比例、日期等判断，可用 DSL Rule（DSL规则）表达。

### 固有人工判断

只有确实需要专业人员对证据效力、冲突和业务责任做裁定时，使用 Judgment（人工判断）。

“DSL 暂时不会算”不等于人工判断。

### 不复制 Knowledge Rule

Domain Knowledge 负责把规则讲透；Domain Model 只保留让该判断可被无歧义表达所必需的：

- 事实输入；
- 判断结果；
- UNKNOWN；
- 非充分事实；
- 证据；
- 人工边界。

## 第四步：限制外部上下文

若 Rule 属于 `EXTERNAL_CONTEXT`，例如：

- 客户关系状态；
- 某笔交易的发生时点；
- 机构审批；
- 可疑交易报告；
- 接口异步状态；

只引用当前领域判断真正需要的最小上下文。

例如历史 UBO 判断只需要 `as_of_time（判断时点）`，不要因此建立完整 Transaction（交易）领域模型。

## 第五步：处理无模型变化规则

若 Rule 只是：

- 备案/报告期限；
- 机构内部治理；
- 操作步骤；
- 过渡政策；
- 接口处理；

且没有定义本领域结构或稳定领域判断，则标记 `NO_MODEL_CHANGE`。

保留 Rule 原文和分类理由，但不创建伪模型对象、伪 Process（流程）或伪 StateMachine（状态机）。

## Process 与 StateMachine

默认不创建。

只有业务专家能独立说明：

> “这个过程/状态本身就是领域中长期稳定存在的业务事实，而不是系统实现方式。”

才进入模型。

不得为了让 Rule 彼此串联而创建 Process。

## 反向验证

完成结构和判断后，用上游材料反查：

- 每条 `CORE_STRUCTURE` Rule 所需事实能否表达；
- 每条 `DOMAIN_DECISION` Rule 是否能从模型事实得到正确判断语义；
- `EXTERNAL_CONTEXT` 是否只保留最小引用；
- `NO_MODEL_CHANGE` 是否没有制造模型噪音；
- Case 的 expected / forbidden 是否都能解释；
- OPEN 是否仍保持 OPEN。

## 输出

继续输出现有 `model.yaml`，但核心阅读顺序必须是：

1. Types / Relations / Evidence / Temporal（类型、关系、证据、时间）
2. Domain Decisions（领域判断）
3. Issues（未决）
4. 可选 Process / StateMachine（流程/状态机）
5. Coverage（覆盖）

`rule_coverage` 对每条 Knowledge Rule 必须记录：

- `modeling_classification`
- `reason`
- `model_ids`
- `status`
- 原七要素 facets（规则要素）

正确的“未建模”也是完成的一部分：

- 仅外部上下文 → `status=EXTERNAL_CONTEXT`
- 无模型变化 → `status=NO_MODEL_CHANGE`

最终质量标准：

> 一个业务专家看完模型后，首先能说清“这个业务世界有哪些稳定东西、它们怎样连接、基于这些事实做哪些稳定判断”，而不是先看到一套规则引擎或工作流。
