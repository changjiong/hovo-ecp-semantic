# 先例研究报告

## 研究目标

为 `hovo-ecp-semantic` 寻找可复用的 Agent Skill（智能体技能）工程机制，同时确保最终技能以用户提供的 ECP Semantic Authoring Kit 1.7 为正式语义权威，而不是以外部通用本体项目替代 ECP Profile（配置边界）。

## 创建权威

- `joeseesun/qiaomu-meta-skill`
- 用途：技能创建、结构、评估、证据、受治理门禁的元方法。
- 采用：单一根 `SKILL.md`、判断规则下沉 `references/`、确定性行为放 `scripts/`、回归放 `evals/`、证据放 `reports/`；采用 Governed（受治理）模式和 `missing evidence` 边界。

## 候选 1：New1Direction/OntologyEX / ontology-extraction

### 为什么入选

直接面向领域本体构建，强调 Scope（范围）、Competency Questions（能力问题）、source evidence（来源证据）、概念层和验证。

### Keep（保留）

- 能力问题是本体完成定义和验收合同。
- “按现实业务建模，而不是按表、部门和厂商系统建模”。
- 关系具有属性、时间或业务身份时考虑实体化。
- 用真实记录/句子做 round-trip（往返）表达测试。

### Adapt（改造）

- 其 L0/L1/L2/L3 四层不是 ECP 的正式资产分层，因此仅吸收“上下层语义映射”思想，不复制层级结构。
- 输出形式改造成 ECP 的 ONTOLOGY / MAPPING / SHACL / DERIVATION / EVALUATION / ACTION_POLICY / SCOPE 资产集合。

### Reject（拒绝）

- 不把通用 OWL 2（网络本体语言2）能力直接带入 ECP。
- 不把 Agent Task（智能体任务）层强制作为所有 ECP 本体的组成部分。

## 候选 2：Mokee04/ontology_research / ontology-agent-suite

### 为什么入选

将本体工程拆为规划、研究、构建、验证，并强调能力问题、证据、复用优先和人工审查。

### Keep（保留）

- 范围和能力问题先于形式化。
- evidence before claims（先证据后结论）。
- 高风险建模需要人工复核。
- 构建和验证必须分离。

### Adapt（改造）

- 用户输入已经足够时不机械暂停等待确认；按 Qiaomu 元技能要求减少重复提问。
- “SKOS first（SKOS优先）”不作为 ECP 硬规则，因为 ECP Profile 对 SKOS 只保证有限元数据能力。

### Reject（拒绝）

- 不把多 Agent Team（多智能体团队）组织方式写成技能使用的必要条件。
- 不要求每个任务都进行多轮人工停顿。

## 候选 3：mareasw/ontoskills

### 为什么入选

突出 deterministic validation（确定性校验）、OWL 产物编译和 SHACL gatekeeper（SHACL门禁），与本技能需要的“生成后必须机器校验”高度相关。

### Keep（保留）

- 语义资产不能只靠语言模型自评，必须有机器可执行校验。
- SHACL 是开放世界本体之外的重要数据质量门禁。
- semantic drift（语义漂移）应被显式检测，而不是静默兼容。

### Adapt（改造）

- 校验器严格绑定 ECP Semantic Profile 1.0 和 Authoring Kit 1.7 的有限子集。
- 本地校验只证明 `LOCALLY_VALID`，不冒充平台编译器。

### Reject（拒绝）

- 不采用“完整 OWL 2 + 通用 SPARQL Runtime（运行时）”假设。
- 不把技能文本直接编译为本体作为主流程；必须先完成业务概念化。

## Invent（原创贡献）

1. **ECP Profile-aware asset planner（ECP配置边界感知资产规划）**：从业务语义判断应落到哪一种 ECP 资产，而不是默认输出 TTL。
2. **跨资产一致性门禁**：Ontology Source Digest（本体源摘要）、Mapping、Rule Set、Workspace、Scope v1/v2 联动校验。
3. **编译器证据边界**：`compilerContract.expect` 等 ECP 编译器拥有的语义绝不由模型伪造。
4. **Evaluation Draft（求值草稿）隔离**：缺少真实编译合同的求值定义不得进入最终规则清单。
5. **失败关闭**：Scope 预算、Coverage（覆盖度）、摘要、Profile 不确定时拒绝或标记未知，不做猜测性回退。
6. **本体方法与 ECP 资产实现分离**：“29句话/7+1”只作为知识萃取与覆盖检查，不直接把 SWRL/OWL-S/ODRL/SPARQL 等假设映射进 ECP。

## 证据边界

- GitHub 源码级先例审阅：已完成。
- skills.sh 安装量 / SkillsMP stars（仓库星标）双目录量化：`missing evidence`；本次没有取得可核对目录结果，因此不构造流行度排名。
- 人工盲测：`missing evidence`。
- 真实 ECP 平台预检/候选编译：`missing evidence`。


## `mattpocock/skills` 流程研究（2026-09-03）

- `keep`：把事实查证归 Agent（智能体）、高影响决策归用户；把深度 `grilling`（追问式澄清）作为显式工作模式而非所有任务默认行为；使用 Frontier（当前可推进前沿）只处理前置条件已满足的工作。
- `adapt`：引入 `CONFIRMED / INFERRED / ASSUMED / OPEN / BLOCKED` 五态不确定性分类和一次性 Decision Gate（决策门禁）；默认最多一轮、最多五个高影响问题。
- `adapt`：借鉴 `prototype`（原型验证）在真正歧义但可合理默认时继续推进并声明假设；借鉴 `to-spec`（转规格）在上下文充分时禁止重复访谈。
- `reject`：拒绝将 `grilling` 的“遍历完整设计树直到 frontier 为空”作为本技能默认，因为本体领域问题可无限展开，会把资产生成退化成无界访谈。
- `invent`：Asset Dependency Graph（资产依赖图）的局部阻塞语义——缺 Schema 只阻塞 Mapping 及其下游，不阻塞 Ontology、SHACL 草案、CQ（能力问题）和概念模型。
