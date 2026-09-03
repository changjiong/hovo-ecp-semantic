# Bounded Weighted Transitive Closure Operator

文档状态：当前有限算子合同

日期：2026-08-18

## 1. 定位

`WeightedTransitiveClosure`是在已提交语义图上执行有界、确定性加权路径遍历的Feature Operator。它面向股权穿透、依赖传播和其他“边权沿路径连乘”的通用场景，不包含UBO阈值、法条顺序或具体领域ID分派。

该算子只产生路径事实和不完整性诊断。路径到达自然人、路径权重达到某个阈值，都不自动等于最终UBO结论；同人多路径汇总、证据门禁、规则优先级和最终认定仍由Published Release中的后续Derivation与Evaluation决定。

## 2. 输入

算子引用三个已经由前序Feature Operator生成的数据集：

| 输入 | 必需变量类型 | 含义 |
|---|---|---|
| `rootInput` | `root: resource` | 每个待计算根对象 |
| `edgeInput` | `edge/from/to: resource`、`weight: decimal` | 有稳定身份的有向加权边 |
| `terminalInput` | `terminal: resource` | 可结束路径的目标对象集合 |

`direction`决定邻接方向：`FORWARD`沿`from -> to`遍历，`REVERSE`沿`to -> from`遍历。股权事实若表达“持有人 `from` 持有主体 `to`”，从目标企业向最终持有人穿透时使用`REVERSE`。

`weightUnit`必须显式声明：

- `UNIT_INTERVAL`：源值`0.25`表示25%；每段必须位于`[0, 1]`；
- `PERCENT`：源值`25`表示25%；Runtime使用Decimal除以100，并在遍历前验证规范值位于`[0, 1]`。

零权重边不参与遍历。相同Edge IRI的重复行会合并Support；若端点或权重冲突则失败关闭。

## 3. 确定性和资源边界

每条路径使用Decimal逐边连乘，只枚举简单路径；再次进入当前路径已有节点时输出`CYCLE_CUT`，不会继续展开。输入、邻接和最终记录都按Unicode Code Point稳定排序，`pathKey`由根、结果、终点和有序Edge IRI计算内容摘要，因此输入行顺序不影响结果。

Definition必须同时声明三个单根限制：

| 限制 | 合同上限 | 命中结果 |
|---|---:|---|
| `maxDepth` | 100 | `DEPTH_LIMIT` |
| `maxPathsPerRoot` | 100000 | `PATH_LIMIT` |
| `maxExpandedStatesPerRoot` | 1000000 | `STATE_LIMIT` |

限制命中不是正常“无匹配”。Runtime保留前沿路径、当前权重和Support；领域规则必须把受影响根对象视为计算不完整，不能据此产生否定结论或错误兜底。

仅有单根限制不足以约束多根运行：总成本会随Root数量继续线性放大。因此当前Feature Operator Set还定义两个跨全部Root的全局预算：

| 限制 | 省略时默认值 | 合同硬上限 | 命中行为 |
|---|---:|---:|---|
| `maxPathRecordsTotal` | 25000 | 25000 | 整个Feature求值失败关闭，诊断码`WTC_GLOBAL_PATH_RECORD_LIMIT` |
| `maxTraversalStatesTotal` | 250000 | 250000 | 整个Feature求值失败关闭，诊断码`WTC_GLOBAL_TRAVERSAL_STATE_LIMIT` |

`maxPathRecordsTotal`统计所有Root产生的`TERMINAL`和各类截断/死路记录；`maxTraversalStatesTotal`在把一个新DFS状态放入待处理前沿之前计数，因而宽图不能先建立超大内存前沿再等待超时。两个字段为了兼容既有不可变Release而允许省略，此时使用表中的确定性、有界兼容上限；新Definition必须显式填写经过领域基数与RSS门禁验证的更小预算，且只能选择不高于平台硬上限的正整数。默认等于硬上限并不表示推荐作者采用该值。

全局预算与单根诊断的语义刻意不同。单根限制产生可归属于该Root的不完整性事实；全局限制表示本次执行无法证明未处理Root的结果完整，因此不得提交已产生的部分结果，也不得把它们解释为否定结论。运行在`FEATURE_RULE_EXECUTION`阶段失败，批次日志保留具体诊断码、算子ID和命中的预算。

## 4. 输出

`bindings`为每条结果绑定以下变量：

| 变量 | 类型 | 含义 |
|---|---|---|
| `root` | resource | 根对象 |
| `terminal` | resource | 终点或被截断的前沿节点 |
| `pathKey` | string | 稳定路径结果键 |
| `pathNodes` | sequence:resource | 有序节点路径 |
| `pathEdges` | sequence:resource | 有序边路径 |
| `pathNodesCanonical` | string | 保留节点次序的Canonical JSON数组 |
| `pathEdgesCanonical` | string | 保留边次序的Canonical JSON数组 |
| `pathWeight` | decimal | 规范化后的路径连乘值 |
| `outcome` | string | `TERMINAL`、`DEAD_END`、`CYCLE_CUT`、`DEPTH_LIMIT`、`STATE_LIMIT`或`PATH_LIMIT` |

所有输出变量的Lineage都包含根、路径边和命中Terminal的Assertion Support。`ProjectAssertions`可以把记录投影为路径ABox；同一根、同一终点、同一比例语义的`TERMINAL`记录再通过`GroupBy`的Decimal `Sum`汇总。不同权利类型、不同根对象或诊断结果不得混加。

## 5. Definition示例

下面只展示算子节点；`roots`、`weightedEdges`和`naturalPersons`必须由前序算子生成：

```json
{
  "id": "ownershipPaths",
  "op": "WeightedTransitiveClosure",
  "rootInput": "roots",
  "root": "targetEnterprise",
  "edgeInput": "weightedEdges",
  "edge": "ownershipEdge",
  "from": "owner",
  "to": "ownedEntity",
  "weight": "ownershipPercent",
  "terminalInput": "naturalPersons",
  "terminal": "naturalPerson",
  "weightUnit": "PERCENT",
  "direction": "REVERSE",
  "limits": {
    "maxDepth": 50,
    "maxPathsPerRoot": 10000,
    "maxExpandedStatesPerRoot": 100000,
    "maxPathRecordsTotal": 5000,
    "maxTraversalStatesTotal": 25000
  },
  "bindings": {
    "root": "pathRoot",
    "terminal": "pathTerminal",
    "pathKey": "pathKey",
    "pathNodes": "pathNodes",
    "pathEdges": "pathEdges",
    "pathNodesCanonical": "pathNodesCanonical",
    "pathEdgesCanonical": "pathEdgesCanonical",
    "pathWeight": "pathWeight",
    "outcome": "pathOutcome"
  }
}
```

## 6. 版本与门禁

本算子属于当前Feature Operator Set `enterprise-risk-feature-operators/1.9.0`，新V2运行要求Node Runtime
ABI `enterprise-cognitive-node-runtime/2.0.0-alpha.13`。该版本继续为省略新字段的既有不可变Release保留确定性、
有硬上限的兼容预算，并包含受影响Root定位、父指针路径状态和V2增量执行合同。旧Published Run继续绑定其原Runtime身份；新运行使用新的
Execution Binding，不能声称复现alpha.10或更早Runtime摘要。

实现门禁覆盖直接、多层、多路径、重复Support、输入乱序、环路、死路、三个单根资源限制、两个跨根失败关闭预算、宽前沿预留保护、非法权重、冲突Edge、Compiler静态类型、公开批次诊断和Feature Plan端到端证据传播。
