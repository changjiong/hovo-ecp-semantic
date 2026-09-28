
# Knowledge → Business Domain Model（知识 → 业务领域模型）

## 目标

从固定 Domain Knowledge（领域知识）形成一份业务人员可以直接认知和评审的 Domain Model（领域模型）。

正式产物分成：
- model.yaml：纯业务模型；
- coverage.json：知识覆盖和审计；
- review.md：业务审阅视图；
- coverage.md：覆盖审计视图。

## Pass 0：固定范围与来源

PRODUCE（创建）默认 FULL_BASELINE（全量基线）。

先读取固定 Domain Knowledge 的全部 Term / Rule / Question / Case / OPEN。

不得读取旧 model.yaml、旧 coverage、archive、旧 builder 或历史生成脚本来决定新模型。

## Pass 1：逐 Rule 做范围审计

每条 Rule 必须先分类：
- CORE_STRUCTURE（核心结构）
- DOMAIN_DECISION（领域判断）
- EXTERNAL_CONTEXT（外部上下文）
- NO_MODEL_CHANGE（无模型变化）

分类发生在建模之前。

## Pass 2：发现业务对象

对 CORE_STRUCTURE 逐条问：
1. 业务人员会把它当成一个独立“东西”吗？
2. 它是否有自己的现实身份？
3. 它是否有独立生命周期？
4. 多个关系或判断是否需要独立引用它？
5. 它与另一个候选对象是否真的共享同一套身份条件和属性？

### 强制反过度抽象检查

如果一个通用对象需要大量 kind/type 分支才能避免非法组合，则拆开。

错误倾向：
    Party
      kind = NATURAL_PERSON | ORGANIZATION | TRUST | PRODUCT

如果 PersonAssessment.person 可以引用 Party，就等于结构上允许 Organization / Trust / Product 成为候选自然人。

应改成业务上明确的对象，例如 NaturalPerson、Organization、Branch、Trust、AssetProduct。

不要为了追求 Type 数量少而牺牲业务语义。

### 禁止技术对象

不要建立 PathStep（路径步骤）、CalculationNode（计算节点）、ProcessStep（流程步骤）、ApprovalTask（审批任务）、QueryState（查询状态），以及只为排序、回放或数据库实现存在的结构。

## Pass 3：建立业务关系

对每个稳定关系写清：
- 名称和定义；
- 参与对象及各自角色；
- 关系属性；
- 有效时间；
- 证据要求；
- 业务例子和反例。

典型关系包括权益关系、控制关系、业务角色关系、隶属关系、代持/委托/一致行动等安排。

证据文件与被证实的关系必须分开。

## Pass 4：建立业务判断

对 DOMAIN_DECISION 写成 business_decision：
- 业务问题；
- 输入哪些对象/关系事实；
- 可以得到哪些业务结果；
- 判断准则；
- 非充分事实；
- UNKNOWN 行为；
- 证据要求；
- 人工边界；
- 结果如何落到业务对象、业务角色或正式结论；
- 外部上下文。

不要生成表达式树、算子、Process 或 StateMachine。

确定性规则也用业务语言写清，例如：

> 对同一自然人、同一目标主体、同一时点，将全部有效且互不重复的最终权益路径汇总；达到或超过25%时满足标准一。若存在可能改变结果的未知路径，则结果为 UNKNOWN，而不是按0处理。

### 特殊识别路径必须表达最终结果人选

对于简化、豁免、信托、资管、分支、国企等路径，不能只建 route = SIMPLIFIED。

必须继续回答：
> 该路径成立后，业务上应识别哪类自然人/哪些角色的人？

如果当前知识没有支持这一结果，记录 MODEL_GAP；不要让下游自己猜。

## Pass 5：外部上下文和 OPEN

外部上下文只记录最小输入，例如 AML 风险结论中的 risk_tier、suspicious_flag、complex_structure_flag。

不要建立完整 AML 模型。

OPEN 只有直接影响核心对象、关系或判断时才升级为 MODEL_GAP。

只影响外部流程、报告、机构治理、接口或 NO_MODEL_CHANGE 的 OPEN，写入 coverage.json 的 upstream_issue_bindings，但不得创建 MODEL_GAP。

## Pass 6：案例反向验证

用全部范围内 Case 反问：
- 需要的业务对象是否存在？
- 关系是否能表达？
- 判断是否能解释 expected？
- forbidden 是否不会被模型错误允许？
- 缺证时是否维持 UNKNOWN？
- 是否有概念因为过度抽象产生非法组合？

Case 只验证模型，不改写上游真值。

## 输出质量门禁

最终 review.md 第一屏必须直接展示：
1. 业务对象；
2. 业务关系；
3. 核心业务判断；
4. 外部上下文边界。

不得首先展示 Type / Rule / Judgment 技术分类、DSL 表达式、Process、StateMachine 或 Coverage 矩阵。

业务专家读完第一页，应能直接说：“对，这就是我们业务里的世界。”
