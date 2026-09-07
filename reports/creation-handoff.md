# hovo-ecp-semantic 创建交接

## 结果

- Skill（技能）：`hovo-ecp-semantic`
- Version（版本）：`0.2.0`
- 模式：Governed（受治理）
- 目标：把业务领域知识、数据 Schema（模式）和规则需求转换为 ECP Semantic Authoring Kit 1.7 / Semantic Profile 1.0 边界内的本体语义资产，并提供本地确定性校验与工作包打包。
- 发布状态：未发布；仅生成本地候选技能包。

## 创建权威

使用 `joeseesun/qiaomu-meta-skill` 的技能工程方法：单根 `SKILL.md`、判断下沉 `references/`、确定性逻辑进入 `scripts/`、回归进入 `evals/`、证据进入 `reports/`；采用 Governed（受治理）门禁。

## 研究过的参考技能

### New1Direction/OntologyEX — ontology-extraction

- 学到：范围、能力问题、现实业务优先于数据库结构、关系实体化、真实数据 round-trip（往返）验证。
- 采用位置：`references/ontology-engineering-method.md`。
- 拒绝：其四层本体结构不是 ECP 官方资产结构；不照搬完整 OWL 能力。

### Mokee04/ontology_research — ontology-agent-suite

- 学到：能力问题优先、证据优先、构建/验证分离、高风险人工审查。
- 采用位置：技能工作流和信任边界。
- 拒绝：强制多 Agent（智能体）组织和每阶段人工暂停。

### mareasw/ontoskills

- 学到：必须用确定性工具验证本体/SHACL，而不是依赖语言模型自评。
- 采用位置：`scripts/validate_ecp_assets.py` 和回归测试。
- 拒绝：完整 OWL 2 / 通用 SPARQL Runtime（运行时）的假设，不符合 ECP Profile 1.0。

## Keep / Adapt / Reject / Invent 总结

- Keep（保留）：能力问题、证据、概念化、确定性验证、人工高风险边界。
- Adapt（改造）：全部方法映射到 ECP 官方资产模型和有限 Profile。
- Reject（拒绝）：先写 OWL、表即本体、任意 SWRL/SPARQL/SQL/JS、伪造编译合同。
- Invent（原创）：ECP 资产规划、跨资产摘要一致性、Evaluation Draft 隔离、Scope v2 工作包门禁、精确证据状态机。

## 优势与证据标签

- `design advantage`（设计优势）：先概念化再 ECP 形式化，避免“表结构翻译成本体”。
- `design advantage`（设计优势）：一个技能覆盖 ONTOLOGY、MAPPING、六阶段 SHACL、DERIVATION、EVALUATION、ACTION_POLICY、SCOPE 和 Workspace Package，但由资产计划决定最小输出，不机械全生成。
- `design advantage`（设计优势）：所有发布性结论按 `INVALID / NEEDS_INPUT / LOCALLY_VALID / ECP_PREFLIGHT_REQUIRED / ECP_PREFLIGHT_VALID / RELEASE_READY` 精确表达。
- `design advantage`（设计优势）：禁止伪造 `compilerContract.expect`，没有 ECP 编译器证据的 Evaluation 只能保持 Draft（草稿）。
- `validated advantage`（已验证优势）：触发边界回归 16/16 通过；ECP 本地资产回归 5/5 通过；技能包结构与受治理硬规则检查 0 失败、0 警告。证据见 `reports/trigger-eval.json`、`reports/output-eval.json` 和 `reports/package-validation.json`。
- `hypothesis`（假设）：该资产规划和门禁方式能显著减少 ECP 候选编译失败与跨资产漂移，但真实 ECP 平台对照实验仍为 `missing evidence`。

## 未验证内容

- 真实 ECP Admin 只预检：`missing evidence`。
- 精确 Revision Set 候选编译：`missing evidence`。
- Semantic Release 发布：`missing evidence`。
- 干净 `npx skills add` 安装：`missing evidence`，因为当前技能尚未发布到远端仓库。
- 人工盲评和多场景效果提升：`missing evidence`。


## 0.2.0 流程升级

- `design advantage`（设计优势）：默认执行模型由 interview-first（访谈优先）调整为 evidence-first + bounded HITL（证据优先 + 有界人工参与）。
- `design advantage`：澄清预算固化为最多 1 轮、最多 5 个高影响 `OPEN` 问题；事实查证和低风险可逆设计不打断用户。
- `design advantage`：引入 `CONFIRMED / INFERRED / ASSUMED / OPEN / BLOCKED` 五态，并用 Asset Dependency Graph（资产依赖图）实现局部阻塞。
- `design advantage`：多轮 Workshop（研讨）仅在用户明确要求时启用，避免无界交互式拷问。
- `validated advantage`（已验证优势）：上述规则被纳入静态包验证与专门回归测试。
