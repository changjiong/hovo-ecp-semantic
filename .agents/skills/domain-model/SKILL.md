
---
name: domain-model
description: 将固定版本、已审阅范围明确的 Domain Knowledge（领域知识）抽象为平台无关、纯业务视角的 Domain Model（领域模型）。核心产物只表达业务对象、业务关系、业务判断和必要外部上下文；规则覆盖、案例覆盖、OPEN（未决）和审计信息进入独立 coverage.json，不再混入 model.yaml。PRODUCE（创建）默认 FULL_BASELINE（全量基线）且必须从固定知识重新建模，不读取旧模型作为语义来源。
metadata:
  author: Hovo
  version: "1.0.0"
---

# 业务领域模型

Domain Model（领域模型）必须首先是业务人员描述业务世界的模型，不是为了让技术实现方便而设计的中间语言。

它只回答三类问题：

> 这个业务世界里稳定存在什么业务对象？

> 这些对象之间有什么稳定业务关系？

> 基于这些对象和关系，业务上要做哪些稳定判断？

如果一个结构主要用于计算、流程编排、数据库实现、接口集成、审计追踪或平台执行，它不属于核心 Domain Model。

## 两个正式输出层

model.yaml 是唯一业务模型，只允许包含：
- business_objects（业务对象）
- business_relations（业务关系）
- business_decisions（业务判断）
- external_contexts（外部上下文）

model.yaml 不得包含 Knowledge Rule Coverage（知识规则覆盖）、Question Coverage（问题覆盖）、Case Explanation（案例解释）、上游未决绑定、MODEL_GAP 审计、Process（流程）、StateMachine（状态机）、Execution Rule（执行规则）、平台算子或表达式树。

coverage.json 是独立覆盖与审计账本，保存每条 Knowledge Rule 的建模分类和理由、Question 覆盖、Case 解释、上游 OPEN 的去向，以及真正影响核心业务模型的 MODEL_GAP。

coverage.md 由 coverage.json 确定生成；review.md 只从 model.yaml 生成。

## 输入边界

PRODUCE（创建）只消费固定 Domain Knowledge 5.0.0：Term、Rule、Question、Case、Issue / OPEN、来源与确认引用。

不得重新读取原始法规、PDF、MinerU 输出、数据库字段、ECP 资产来改写上游业务含义。

PRODUCE 不得使用旧 model.yaml、coverage.json、archive、旧 builder（生成器）或旧脚本作为业务语义来源。基于旧模型修改必须使用 REVISE（修订）。

## Scope（范围）

PRODUCE 默认并原则上使用 FULL_BASELINE（全量基线）。

FULL_BASELINE 时，固定知识中的全部 Rule 必须先进入范围审计，再决定：
- CORE_STRUCTURE（核心结构）
- DOMAIN_DECISION（领域判断）
- EXTERNAL_CONTEXT（外部上下文）
- NO_MODEL_CHANGE（无模型变化）

只有用户或调用方明确限定范围时，才允许 EXPLICIT_SUBSET（显式子集），并必须保留 explicit_scope_request。

## 业务对象建模规则

一个概念只有满足以下条件之一才成为 business_object（业务对象）：
1. 在业务世界中有独立身份；
2. 有自己的生命周期；
3. 会被多个业务关系或判断独立引用；
4. 业务人员会把它当成一个明确的“东西”来讨论。

### 禁止过度抽象

如果两个概念在业务上具有不同身份条件、不同适用规则、不同关系能力或不同生命周期，就不得为了减少对象数量把它们压成一个通用父对象。

例如 NaturalPerson（自然人）与 Organization（组织）不能仅靠 kind 字段合并成 Party（当事人），如果这样会允许“组织成为候选自然人”这类无效组合。

Trust（信托）和 AssetProduct（资产管理产品）若适用规则和角色结构明显不同，应保持业务上可区分。

不能为了技术复用让大量字段只对某个 kind 才有意义。

### 禁止技术对象冒充业务对象

以下通常不建成 business_object：
- 路径步骤
- 计算中间量
- 查询任务
- 审批任务
- 状态机节点
- 工作流步骤
- 数据库记录容器
- 仅为排序、回放或实现存在的结构

## 业务关系建模规则

business_relation（业务关系）表达现实业务对象之间稳定存在的关系，例如权益关系、控制关系、角色关系、隶属关系、代持/委托/一致行动等安排。

关系必须明确参与方及其业务角色、关系自身属性、时间语义、证据语义、例子和反例。

证据不能替代关系本身；协议文件是 Evidence（证据），协议形成的代持/控制安排才是业务关系。

## 业务判断建模规则

business_decision（业务判断）表达“已有业务事实在本领域意味着什么”。

每个判断必须写清：
- business_question（业务问题）
- inputs（业务输入）
- outcomes（业务结果）
- criteria（判断准则）
- non_sufficient_facts（非充分事实）
- unknown_behavior（缺证/未知行为）
- evidence_requirements（证据要求）
- human_boundary（人工边界）
- external_context_ids（外部上下文）

Domain Model 不再保存可执行表达式树。确定性阈值也写成业务准则，例如“最终权益比例达到或超过25%”。

完整算法和平台表达由后续 ECP 语义编制负责。

### 特殊路径必须表达“最终认谁”

若某条规则决定使用简化/特殊识别方式，领域模型不能只表达 route = SIMPLIFIED（简化）。

还必须在业务判断中明确：
- 适用什么业务角色或候选范围；
- 最终要形成什么自然人人选语义；
- 哪些条件未知时不能产生该结果。

否则下游仍需重新阅读 Domain Knowledge 才知道“简化之后认谁”。

## 外部上下文

external_context（外部上下文）只表示本领域判断需要消费、但不属于本领域核心业务世界的输入，例如 AML/KYC 风险结果、客户关系状态、某笔交易的判断时点、BOMIS 查询结果、机构岗位授权。

只声明“需要什么输入”和“由哪个外部领域提供”，不在本模型中重建邻接领域。

机构审批人员、风险岗、合规岗等责任信息写在 business_decision.human_boundary 中；除非它本身是目标业务领域的稳定业务角色，否则不得建立成核心 Role（角色）对象。

## OPEN（未决）的处理

上游 OPEN 不等于 MODEL_GAP。

只有当 OPEN 直接阻止核心 business_object / business_relation / business_decision 的业务语义确定时，才在 coverage.json 中创建 model_issue。

如果 OPEN 只影响 EXTERNAL_CONTEXT、NO_MODEL_CHANGE、邻接业务流程、机构治理或报告操作，则只在 upstream_issue_bindings 中记录，不制造 MODEL_GAP。

## 生成步骤

1. 固定 Domain Knowledge 版本和范围；
2. 对全部范围内 Rule 做分类；
3. 从 CORE_STRUCTURE 中发现最小且业务上真实可辨的对象；
4. 建立对象之间的业务关系；
5. 从 DOMAIN_DECISION 中抽象稳定业务判断；
6. 对 EXTERNAL_CONTEXT 只声明最小外部输入；
7. 合并同义结构，但禁止为了“少”而过度抽象；
8. 用 Case 验证对象、关系、判断能否解释业务结果；
9. 将知识覆盖、案例、OPEN 全部写入 coverage.json；
10. 生成业务优先的 review.md 和独立 coverage.md。

## 完成条件

完成不是“模型元素最少”或“全部规则可执行”，而是同时满足：
- 业务人员能直接看懂对象、关系和判断；
- 不存在明显无效组合，例如“组织作为候选自然人”；
- 业务概念没有被技术父类抹平；
- 业务判断不依赖重新阅读上游知识才能知道结果语义；
- 外部上下文没有扩张成邻接领域模型；
- 只有真正核心语义缺口才成为 MODEL_GAP；
- FULL_BASELINE 下全部 Rule 都有覆盖分类；
- Case 不改写上游 expected / forbidden；
- 下游 ECP 编制可以同时消费 Domain Knowledge + Domain Model，而不需要从技术 DSL 反推业务语义。

完成本技能后结束，不自动启动 ECP 编制。
