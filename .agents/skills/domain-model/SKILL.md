---
name: domain-model
description: 将固定版本、已审阅范围明确的 Domain Knowledge（领域知识）抽象为平台无关、业务可读、机器可校验的 Domain Model（领域模型）。核心表达稳定业务结构与稳定领域判断：对象、关系、事实、角色、安排、证据、时间、判断和结果。Knowledge Rule（知识规则）先审查是否揭示 CORE_STRUCTURE（核心结构）、DOMAIN_DECISION（领域判断）、EXTERNAL_CONTEXT（外部上下文）或 NO_MODEL_CHANGE（无模型变化）；不要求每条规则都生成模型元素，不重新解释原始制度，不设计数据库、机构流程或 ECP（可执行语义协议）执行资产。
metadata:
  author: Hovo
  version: "0.9.0"
---

# 领域模型

Domain Model（领域模型）只回答两个问题：

> 这个业务世界里稳定存在什么对象、关系和事实？

> 基于这些结构，业务上有哪些稳定、可复用的判断？

它不是第二份 Domain Knowledge（领域知识），也不是 Workflow（工作流）、Policy（机构政策）、Database Model（数据库模型）或 ECP（可执行语义协议）运行时。

## 核心边界

```text
Domain Knowledge（领域知识）
业务是什么、为什么、怎么判断
          ↓
Domain Model（领域模型）
稳定业务结构 + 稳定领域判断
          ↓
ECP Semantic Authoring（ECP语义资产编制）
把知识与模型转成平台可计算/执行资产
```

本技能不把所有 Knowledge Rule（知识规则）机械翻译为 Rule（规则）/Process（流程）。Rule 是建模依据，不是待复制对象。

## 产物目录

调用方项目的 `domain-model/`（或同等阶段目录）根部只放：

- `input.json`
- `model.yaml`
- `output.json`
- `review.md`
- `coverage.md`

生成请求、校验和调试记录放 `process/`；旧模型放 `archive/`。

## 输入边界

开始前必须读：

1. [Knowledge → Domain Model 提示词](prompts/01-knowledge-to-domain-model.md)
2. [业务建模方法](references/business-modeling.md)
3. [合同](contracts/README.md)
4. [Domain DSL（领域模型专用语言）](references/domain-dsl.md)

只消费固定版本 Domain Knowledge 5.0.0：

- Term（业务概念）
- Rule（业务规则）
- Case（案例）
- Issue / OPEN（未决）
- Question（业务问题，仅用于覆盖检查）
- 来源和确认引用

**不得重新读取原始法规、PDF（便携式文档格式）、MinerU（文档解析工具）结果、数据库表字段、DDL（数据定义语言）、SQL（结构化查询语言）或 ECP 算子来改写上游业务含义。**

知识缺失或冲突时退回 `domain-knowledge（领域知识形成）`。

## 每条 Knowledge Rule 先做模型范围审计

每条范围内 Rule 必须先标记 `modeling_classification`：

- `CORE_STRUCTURE`：揭示稳定对象、关系、事实、角色、安排、证据或时间；
- `DOMAIN_DECISION`：定义基于这些结构形成的稳定业务判断或结果；
- `EXTERNAL_CONTEXT`：本领域会引用，但属于邻接领域；只有同时包含领域判断时才引用必要上下文，不扩建邻接领域模型；
- `NO_MODEL_CHANGE`：期限、操作、治理、过渡安排等知识，不需要改变本领域结构或判断。

一条 Rule 可以同时是 `CORE_STRUCTURE + DOMAIN_DECISION`；`NO_MODEL_CHANGE` 必须单独使用。

**完整覆盖不等于全部建模。** `EXTERNAL_CONTEXT` 和 `NO_MODEL_CHANGE` 只要理由清楚、上游语义保留，就属于正确处理。

## 生成步骤

1. **固定知识基线。** 锁定 knowledge_ref（知识引用）、knowledge_basis（知识依据）、范围内 Term / Rule / Case / OPEN。
2. **逐 Rule 做模型范围审计。** 先判断它是否揭示核心结构、领域判断、外部上下文或无模型变化；禁止先创建模型对象再反推理由。
3. **抽象最小稳定结构。** 只建立具有独立业务身份或稳定关系语义的 Entity（实体）、Role（角色）、Fact（事实）、Relation（关系）、Arrangement（安排）、Evidence（证据）、Event（事件）及 Temporal（时间）。值、阈值、标签和流程步骤不能自然升级为对象。
4. **抽象稳定领域判断。** 将“事实怎样形成业务结果”表达成 Domain Decision（领域判断）。确定性、长期稳定的判断可用 Rule（规则）表达；固有人工裁定用 Judgment（人工判断）表达。两者都必须保留 UNKNOWN（未知）、非充分事实、证据和人工边界。
5. **保持最小模型。** 多条 Knowledge Rule 若依赖同一稳定结构，应复用同一模型元素；不为每条规则创建专用 Type（类型）或流程。
6. **限制外部上下文。** 例如客户关系、交易、机构审批、接口状态等，仅在它们为领域判断提供必要输入时引用最小上下文；不得扩展成完整邻接领域。
7. **Process（流程）和 StateMachine（状态机）默认不是核心。** 只有当过程/状态本身是跨实现长期稳定、且业务专家认为它是领域事实时才建模；不得为了“串起规则”强行创建。
8. **反向验证。** 用 Knowledge Rule、Case 和 OPEN 检查：核心事实是否可表达、领域判断是否不改义、外部上下文是否没有侵入、未决是否仍保持未决。
9. **生成业务审阅视图。** `review.md` 第一屏必须先展示“业务世界有什么、怎样连接、有哪些核心判断”；流程、DSL表达式和覆盖矩阵后置。

## 领域判断与执行规则的边界

Domain Decision（领域判断）属于领域模型，例如：

- 最终拥有比例达到阈值 → 标准一判断；
- 收益权/表决权达到阈值 → 标准二判断；
- 控制事实是否构成实际控制 → 标准三判断；
- 前三项均明确不存在 → 才可进入管理人员兜底；
- 主体性质 + 风险事实 → 是否具备简化资格。

Execution Rule（执行规则）不属于核心领域模型，例如：

- 接口轮询；
- 数据库递归查询；
- 机构审批链；
- 自动补证动作；
- 生产工作流；
- 平台函数编排。

## Domain DSL 的边界

DSL（领域模型专用语言）用于无歧义表达和静态检查业务结构、领域判断与未知行为。本地 evaluate（求值）仅用于有限验证，不是完成条件。

不要为了可执行而扩张模型。复杂算法只固定：

- 输入事实
- 输出结果
- 业务/数学语义
- UNKNOWN 行为
- 适用前提

具体算法由后续实现阶段选择。

## 完成条件

一个 Domain Model 可以完成，即使存在 OPEN，只要：

1. 核心对象、关系、证据、时间和结果形成连贯业务结构；
2. 稳定领域判断有明确事实输入、结果和 UNKNOWN 语义；
3. 每条 Knowledge Rule 都有建模分类和理由；
4. `EXTERNAL_CONTEXT` / `NO_MODEL_CHANGE` 不被强行造成本领域对象；
5. 上游 OPEN 未被静默关闭；
6. Case 能由现有结构和判断解释，且不改写上游 expected / forbidden；
7. 业务专家无需理解 YAML（层级配置格式）或 DSL 即能审阅模型骨架；
8. 下游 ECP 编制无需重新阅读原始法规即可继续工作。

完成本技能后结束，不自动启动 ECP 编制。
