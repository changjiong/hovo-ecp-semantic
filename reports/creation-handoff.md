# hovo-ecp-semantic 0.2.0 创建交接

## 结果

- Skill：`hovo-ecp-semantic`
- Version：`0.2.0`
- Mode：Governed（受治理）
- 核心任务：把业务资料、真实数据 Schema、领域语义和规则需求转换为符合 ECP Semantic Profile 1.0 / Authoring Kit 1.7 的候选语义资产，并精确区分本地有效与平台预检/发布证据。

## 关键设计

- `design advantage`：evidence-first（证据优先）而不是 interview-first（访谈优先）。
- `design advantage`：不确定性统一为 `CONFIRMED / INFERRED / ASSUMED / OPEN / BLOCKED`。
- `design advantage`：默认澄清预算最多一轮五题；Workshop（研讨）必须显式请求。
- `design advantage`：资产依赖局部阻塞；缺 Mapping 所需 Schema 不阻塞 Ontology、CQ（能力问题）和概念模型。
- `design advantage`：ECP Profile、资产指南和 JSON Contract（JSON 合同）按权威层级使用；通用 OWL/SHACL 知识不得扩大 ECP 支持边界。
- `design advantage`：`compilerContract.expect`、候选编译和 Release Ready（可发布）状态必须由 ECP 平台证据证明。

## 验证证据

本地创建阶段已验证：

- Trigger Eval：16/16；
- ECP 资产回归：5/5；
- 交互策略回归：4/4；
- Skill Package Validation：0 failures / 0 warnings。

以上仅证明本地技能与确定性回归，不证明真实 ECP Admin 预检、候选编译或发布。

## Missing evidence（缺少证据）

- 真实 ECP Admin “只预检”；
- 精确 Revision 集合候选编译；
- Published Semantic Release；
- 远端安装后的独立运行验证。

这些证据缺失时不得声称 `ECP_PREFLIGHT_VALID` 或 `RELEASE_READY`。
