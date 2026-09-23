# boundary-repair

`boundary-repair` 是 `domain-knowledge` 内部的局部结构判断模块，只处理 deterministic normalizer（确定性规范化器）无法可靠决定的边界。

当前实现使用 TypeSafe Jev 的 `Choice`：

```text
SourceBlock A
    ↓
ambiguous boundary
    ↓
SourceBlock B
    ↓
Jev Choice
    ├─ CONTINUE_PREVIOUS
    ├─ START_NEW_UNIT
    ├─ CHILD_OF_PREVIOUS
    └─ UNRESOLVED
```

## 决策合同

Jev 接收的 state（状态）只包含局部结构信息：

- `heading_path`；
- `previous_unit.kind / label`；
- `previous_block`；
- `current_block`；
- 可用时的 `next_block`。

问题固定为“判断当前块与紧邻前序语义内容的结构关系”。禁止 Jev：

- 解释业务规则；
- 改写、补写或摘要原文；
- 决定 Term / Rule / Question 等领域知识；
- 直接修改 SourceUnit。

Jev 只返回结构选择、概率分布和 confidence（置信度）；真正的 merge / new / child 由确定性 assembler（组装器）执行。

## 模型与阈值

- SDK：`typesafe-sdk>=0.7.1,<0.8`
- model：固定请求 `jev-latest`
- 默认自动应用阈值：`0.90`
- 可通过 `DOMAIN_KNOWLEDGE_JEV_MIN_CONFIDENCE` 调整阈值。

若 `confidence < threshold`，不应用模型首选项，统一记录为 `UNRESOLVED`。若 Jev 本身高置信度选择 `UNRESOLVED`，同样保持未解决。存在任一未解决边界时，对应 SourceExtraction 必须为 `PARTIAL`。

阈值是风险策略而不是模型真理；生产前应使用本领域中文材料的人工 Gold Set（黄金测试集）校准高置信度错误率与自动覆盖率。

## 失败边界

`TYPESAFE_API_KEY` 是 PRODUCE / REVISE 的运行依赖。Jev API 调用失败时直接失败，不静默退回规则猜测。明确结构仍由 deterministic normalizer 处理，不调用 Jev。

完整决策写入 `boundary_decisions`，保留：

- previous/current/next SourceBlock 标识；
- Jev selected（首选）与 applied（实际应用）；
- probability distribution（概率分布）；
- confidence（置信度）与 threshold（阈值）；
- 实际 resolved model（解析后的模型版本）；
- question version（问题版本）；
- TypeSafe request id（若返回）。
