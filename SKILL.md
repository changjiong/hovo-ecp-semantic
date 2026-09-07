---
name: hovo-ecp-semantic
description: |
  面向 ECP（企业认知平台）Semantic Profile 1.0 与 Semantic Authoring Kit 1.7 生成、校验、修复和打包本体语义资产。用于把业务规则、领域资料、表结构、既有语义模型或场景需求转化为 ECP 可接受的 ONTOLOGY、MAPPING、六阶段 SHACL、DERIVATION、EVALUATION、ACTION_POLICY、SCOPE、规则集和 Semantic Workspace Package。适用于“生成 ECP 本体语义资产”“把业务场景做成 ECP semantic workspace”“检查或修复 ECP TTL/Mapping/SHACL/Scope”“为对象调查生成 Scope v1”“把一组语义资产打成 ECP 工作包”等任务。不要用于泛泛解释 RDF/OWL、非 ECP 的通用知识图谱设计、任意 SQL/JavaScript 规则编程、Runtime Operator 实现或仅需普通文档总结的请求。
metadata:
  author: Hovo
  version: "0.2.0"
  maturity_tier: governed
  source_authority: "ECP Semantic Authoring Kit 1.7"
---

# Hovo ECP 本体语义资产生成技能

把领域认知转换成 **符合 ECP 有限语义配置边界、可本地校验、可进入 ECP 预检与发布流程的语义资产**。不要把“生成 TTL”误当成本体工程，也不要把 ECP 不支持的 OWL/SWRL/SPARQL 能力偷偷写进资产。

## 路由规则

- 本技能只负责 ECP 语义资产的设计、生成、校验、修复与工作包打包。
- 用户只要求审计/校验时保持只读；明确要求修复、生成或打包时才写文件。
- 不直接发布 Semantic Release（语义发布版本），不创建 ECP Revision（修订版本），不修改 ECP Workspace Head（工作区草稿头）。没有 ECP 平台编译结果时，不声称“Release Ready（可发布）”。
- 若请求属于通用本体设计而未指定 ECP，先说明本技能的 ECP 专用边界，不强行套用。
- 根 `SKILL.md` 只保留路由和最小工作流；详细判断规则读取 `references/`，确定性校验使用 `scripts/`。

## 权威顺序

开始任务后按以下顺序读取；冲突时前者优先：

1. `references/ecp-kit-1.7/standards/ecp-semantic-profile-1.0.md` —— ECP Runtime（运行时）本体与 SHACL 正式支持边界。
2. `references/ecp-kit-1.7/standards/ecp-semantic-development-guide.md` —— 当前开发、候选编译、发布和运行边界。
3. 当前资产对应的 `references/ecp-kit-1.7/guides/*.md` —— 资产具体格式。
4. `references/ecp-kit-1.7/contracts/*.json` —— 可机器执行的结构合同。
5. 本技能的 `references/ontology-engineering-method.md` —— 从业务认知到语义模型的方法。
6. 本技能的 `references/ecp-asset-playbook.md` —— ECP 资产选择和跨资产一致性规则。
7. 本技能的 `references/interaction-policy.md` —— 证据优先、不确定性分类、澄清预算和局部阻塞规则。

正式 Profile（配置边界）、资产指南、机器合同是不同层级；不得用示例覆盖 Profile，也不得把 Workspace Package（工作区包）误当运行时语义权威。

## 紧凑工作流

### 1. 判断任务与输出边界

确定用户要的是：

- `design`：语义设计与资产计划；
- `generate`：生成一个或多个 ECP 资产；
- `validate`：只读校验现有资产；
- `repair`：基于校验报告修复资产；
- `package`：构建 ECP Semantic Workspace Package（语义工作区包）。

默认采用 evidence-first（证据优先）方式：先读取当前对话、附件、已有语义资产、ECP 规范和可访问环境，再决定是否需要用户参与。不要把“存在不确定性”自动等同于“必须提问”。

对所有不确定项先分类：

- `CONFIRMED`（已确认）：有明确来源，直接使用；
- `INFERRED`（推定）：可由现有证据高置信推出，继续执行并留痕；
- `ASSUMED`（假设）：属于低风险、可逆设计选择，采用推荐默认并写入假设清单；
- `OPEN`（待决策）：高影响且无法可靠推断的语义分叉，进入一次性 Decision Gate（决策门禁）；
- `BLOCKED`（阻塞）：缺少生成合法资产所必需的外部输入，只阻塞依赖该输入的资产。

默认澄清预算：**最多 1 轮、最多 5 个 OPEN 问题**。事实性问题由技能自行查证；低风险可逆选择不得打断用户；某项资产缺输入时不得阻塞不依赖它的其他资产。只有用户明确要求 Workshop（研讨）/深度访谈/逐项挑战时，才允许进入多轮交互。详细规则见 `references/interaction-policy.md`。

### 2. 先建业务语义，再写 ECP 文件

按 `references/ontology-engineering-method.md` 执行：

`范围 → 能力问题 → 知识萃取 → 概念化 → 语义精化 → ECP形式化 → 实例/映射 → 验证`

必须先回答：

- 业务世界中存在什么；
- 它们是什么；
- 它们如何关联；
- 哪些语义约束必须成立；
- 哪些属于事实、派生、业务求值或动作；
- 当前 ECP Profile 能否表达。

数据表是证据，不是本体结构。具有独立属性、时间、来源或生命周期的业务关系，应考虑实体化，而不是机械画成一条边。

### 3. 建立资产计划

读取 `references/ecp-asset-playbook.md`，为每项需求判断资产类型：

- `ONTOLOGY`：Class、Property、有限公理与元数据；
- `MAPPING`：关系型源到本体实例；
- `SHACL`：六阶段封闭世界数据质量/结构约束；
- `DERIVATION`：有限 Typed Operator（类型化算子）产生派生事实；
- `EVALUATION`：对象级求值与 Candidate（候选）结果；
- `ACTION_POLICY`：已提交语义变化/领域事件到能力调用意图；
- `SCOPE`：从 Root（根）对象读取完整局部事实闭包；
- Rule Set Bundle（规则集包）与 Workspace Package（工作区包）：交换/导入封装。

不要因为“7+1”存在某一维度，就机械生成所有资产；只生成当前业务需求真正需要且 ECP 支持的资产。建立 Asset Dependency Graph（资产依赖图）：某资产 `BLOCKED` 时，仅阻塞它及其下游，不影响已经具备证据的并行资产。

### 4. 按依赖顺序生成

推荐顺序：

1. Ontology TTL（本体 Turtle 文件）
2. Mapping JSON（映射 JSON）
3. 六阶段 SHACL（如本次 Release 需要 SHACL）
4. Derivation（派生）
5. Evaluation（求值）
6. Action Policy（动作策略）
7. Scope（局部事实范围）
8. Rule Set Manifest（规则集清单）
9. Workspace Manifest（工作区清单）

只有物理数据源 Schema（模式）已被可靠提供或发现时才生成可导入 Mapping；不得凭业务描述发明表名、字段名或 Record Key（记录键）。

### 5. 严守 ECP 有限边界

- Ontology 至少一个具名 `owl:Ontology`；Class/Property/Schema 引用必须是具名绝对 IRI。
- 只使用 ECP Semantic Profile 1.0 支持的有限 RDF/RDFS/OWL 子集；禁止匿名 Restriction（限制）、复杂 Class Expression（类表达式）、`owl:equivalentClass`、`owl:sameAs`、Property Chain（属性链）、OWL Cardinality（基数）等未支持能力。
- 需要必填、基数、数据类型、值域时使用 SHACL，不把封闭世界数据约束伪装成 OWL 公理。
- SHACL 只使用 Profile 支持的 Target、直接 IRI Path（路径）和 13 个约束组件；禁止 SHACL-SPARQL、SHACL-JS 和复杂 Property Path（属性路径）。如果一个可执行 Release 含 SHACL，必须完整绑定 `asserted/domain/feature/change/output/provenance` 六阶段。
- Mapping 不包含任意 SQL、连接地址或凭据；跨资产 `ontologySourceDigest` 必须绑定最终 TTL 原始字节。
- Derivation/Evaluation 只使用 ECP 注册的有限 Typed Operator；输入缺失必须传播 Coverage/UNKNOWN（覆盖度/未知）或失败关闭，禁止编造默认事实。
- Evaluation 的 `compilerContract.expect` 属于 ECP 编译器权威。没有平台“只预检”或编译器输出时，不得伪造；生成非导入 Draft（草稿）并明确 `ECP_COMPILER_PREFLIGHT_REQUIRED`（需要 ECP 编译预检），且不把它登记进最终规则 Manifest。
- Action Policy 不写 URL、Header、Token、密码、Bucket、本地路径或脚本；只声明 Capability（能力）、Operation（操作）、`executorBindingRef` 和有限参数来源。
- Scope 只定义 Mapping Root、Join Closure（连接闭包）、Root Binding（根绑定）、Full Scan（全量扫描）与硬资源预算；不是 Ontology，也不是 Evaluation `objectScope`。
- 含 Scope 的正式 Workspace Package 必须使用 V2；不含 Scope 时使用 V1，不额外造兼容层。

### 6. 本地确定性校验

生成或修复后运行：

```bash
python3 scripts/validate_ecp_assets.py <asset-or-workspace-path> --json-out reports/ecp-validation.json
```

若要打包：

```bash
python3 scripts/refresh_workspace_digests.py <workspace-dir>
python3 scripts/validate_ecp_assets.py <workspace-dir> --json-out reports/ecp-validation.json
python3 scripts/package_workspace.py <workspace-dir> --output <workspace>.zip
```

本地校验通过只意味着 `LOCALLY_VALID`（本地有效）。任何正式 ECP Release 仍必须经过平台源码预检、完整候选编译和发布门禁。

### 7. 交互模式与决策门禁

默认是 `Autonomous`（自主编写）模式：尽量从证据、规范、上下文和工具中自行推进；可逆设计采用推荐默认；仅在高影响 `OPEN` 分叉处触发一次 Decision Gate。

可选 `Review Gate`（评审门禁）模式：先生成推荐方案、关键假设和待决策项，再一次性交给用户审核，不逐题追问。

只有用户明确要求时才进入 `Workshop`（研讨）模式：可使用 Design Tree（设计树）和 Frontier（当前可决策前沿）进行多轮深度澄清。Workshop 不是默认行为。

若用户未指定模式，一律使用 `Autonomous`。

### 8. 输出状态必须精确

最终报告只能使用以下状态：

- `INVALID`：本地结构/Profile/跨资产检查失败；
- `NEEDS_INPUT`：缺少真实 Schema、业务定义、阈值、IRI 等关键输入；
- `LOCALLY_VALID`：本地静态检查通过，但尚无 ECP 候选编译证据；
- `ECP_PREFLIGHT_REQUIRED`：存在编译器拥有的合同或跨资产运行语义，需要 ECP 预检；
- `ECP_PREFLIGHT_VALID`：仅当用户提供真实 ECP 预检结果并可核对时使用；
- `RELEASE_READY`：仅当精确 Revision 集合的 ECP 发布前编译证据存在时使用。

不得把“文件能解析”“JSON Schema 通过”写成“可发布”。

## 输出合同

按请求最小化输出：

- 单资产请求：目标资产 + `reports/authoring-report.md` + 本地校验报告；
- 多资产请求：`design/` + `ecp-workspace/` + `reports/`；
- 工作包请求：在本地校验通过后额外生成 `.zip`；
- 任何无法由本地工具证明的 ECP 编译、Schema 当前存在性、Fact Provider（事实提供器）可用性或发布状态均标记 `missing evidence`（缺少证据）。

详细目录和报告字段见 `references/output-contract.md`。

## 安全与变更边界

- 禁止把 Secret（密钥）、Token（令牌）、Endpoint（端点）、数据库口令、S3 坐标和任意脚本写入语义资产。
- 不为了“兼容旧资产”添加 fallback（回退）、迁移层或双写；按当前目标 Profile 直接生成当前正确版本。
- 生成新资产不删除历史语义资产；Full Replacement（完整替换）导入会移除候选 Draft Head 中遗漏成员，必须在报告中显式提醒。
- 未明确要求发布时，不向 GitHub 或 ECP 写入任何远端状态。

## 参考入口

- 本体构建方法：`references/ontology-engineering-method.md`
- 资产决策和跨资产规则：`references/ecp-asset-playbook.md`
- 输出合同：`references/output-contract.md`
- 信任和失败关闭：`references/trust-boundaries.md`
- 交互与澄清预算：`references/interaction-policy.md`
- ECP 原始规范工具箱：`references/ecp-kit-1.7/`
