# hovo-ecp-semantic

把业务领域知识、表结构和规则需求转换成 **ECP（企业认知平台）可审查的本体语义资产**，并在本地执行有限 Profile（配置边界）、JSON Schema（JSON 模式）、摘要和跨资产一致性检查。

> 核心原则：先把业务世界建模正确，再生成 ECP 文件；本地有效不等于 ECP 可发布。

## 能生成什么

- Ontology TTL（本体 Turtle）
- Mapping JSON（数据映射）
- 六阶段 SHACL（形状约束）
- Derivation JSON（派生规则）
- Evaluation JSON（对象级求值）
- Action Policy JSON（动作策略）
- Scope JSON（局部事实范围）
- Rule Set Bundle（规则集包）
- Semantic Workspace Package v1/v2（语义工作区包）

## 典型使用

- “根据这份监管制度、业务说明和表结构，生成 ECP 本体语义资产。”
- “把这个 UBO（最终受益所有人）语义模型生成 Ontology + Mapping + 六阶段 SHACL。”
- “检查这个 ECP Workspace ZIP 是否符合 Authoring Kit 1.7。”
- “修复这份 Mapping 和 Ontology 摘要不一致的问题。”
- “为对象级调查增加 Scope v1，并生成 Workspace Package v2。”
- “只生成一份符合 ECP Profile 1.0 的 Ontology TTL，不要生成其他资产。”

## 不适用

- 仅解释 RDF（资源描述框架）、OWL（网络本体语言）或 SHACL（形状约束语言）；
- 非 ECP 的通用知识图谱工程；
- 编写任意 SQL/JavaScript 规则；
- 扩展 ECP Runtime Operator（运行时算子）；
- 未提供真实表结构时凭空生成可导入 Mapping；
- 没有 ECP 编译证据时声称 Release Ready（可发布）。

## 默认交互策略

默认采用 **evidence-first（证据优先）+ bounded HITL（有界人工参与）**：

- 能从附件、规范、代码、Schema（模式）或已有资产得到的事实，技能自己查，不问用户；
- 低风险、可逆的设计选择采用推荐默认，并记录为 `ASSUMED`（假设）；
- 高影响且无法可靠推断的语义分叉标记为 `OPEN`（待决策），最多集中询问 1 轮、最多 5 题；
- 缺少真实 Schema、IRI、阈值等必需输入时标记为 `BLOCKED`（阻塞），只阻塞依赖它的资产；
- 只有明确要求“研讨/访谈/逐项挑战”时才进入多轮 Workshop（研讨）模式。

## 工作方式

```text
业务范围 / 能力问题
        ↓
知识萃取与概念化
        ↓
ECP 资产计划
        ↓
Ontology
        ↓
Mapping
        ↓
SHACL / Derivation / Evaluation / Action / Scope
        ↓
本地静态校验
        ↓
ECP 平台预检与候选编译
        ↓
Published Semantic Release（平台侧）
```

## 本地工具

依赖：Python 3.11+，建议已有 `rdflib`（RDF 库）和 `jsonschema`（JSON 模式校验库）。

```bash
python3 scripts/validate_ecp_assets.py ./workspace
python3 scripts/refresh_workspace_digests.py ./workspace
python3 scripts/package_workspace.py ./workspace --output workspace.zip
```

技能包自检：

```bash
python3 scripts/validate_skill.py .
python3 scripts/trigger_eval.py . --cases evals/trigger_cases.json --output reports/trigger-eval.json
python3 -m unittest discover -s tests -v
```

## 权威材料

技能内嵌用户提供的 `ECP Semantic Authoring Kit 1.7`，保存在：

`references/ecp-kit-1.7/`

执行时必须遵循：

1. `standards/ecp-semantic-profile-1.0.md`
2. `standards/ecp-semantic-development-guide.md`
3. 对应资产的 `guides/*.md`
4. `contracts/*.json`

工具箱材料由用户提供；本技能不对其版权或再分发许可作额外声明。

## 当前证据状态

- 本地技能包结构校验：可执行；
- ECP 静态资产校验脚本：可执行；
- 回归测试：随包提供；
- 真实 ECP Admin “只预检”、候选编译、发布和干净安装证据：`missing evidence`（缺少证据）。

Hovo semantic engineering skill.

Skill engineering methodology inspired by `joeseesun/qiaomu-meta-skill`.
