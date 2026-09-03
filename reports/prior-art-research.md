# 先例研究报告

## 研究目标

为 `hovo-ecp-semantic` 寻找可复用的 Agent Skill（智能体技能）工程机制，同时确保最终技能以用户提供的 ECP Semantic Authoring Kit 1.7 为正式语义权威，而不是以外部通用本体项目替代 ECP Profile（配置边界）。

## 研究对象

### joeseesun/qiaomu-meta-skill

作为技能创建和治理方法参考。采用：单一根 `SKILL.md`、判断规则下沉 `references/`、确定性行为放 `scripts/`、回归放 `evals/`、证据放 `reports/`，并采用 Governed（受治理）门禁和 `missing evidence` 证据边界。

### New1Direction/OntologyEX

采用：Scope（范围）优先、Competency Questions（能力问题）作为验收合同、现实业务优先于数据库结构、关系实体化和真实数据往返验证。

拒绝：固定四层本体结构作为 ECP 的强制架构；ECP 资产边界仍由 ECP Semantic Profile 1.0 决定。

### Mokee04/ontology_research

采用：能力问题优先、证据优先、构建与验证分离、重要建模决策需要人工审查。

拒绝：默认 Mandatory Discovery Question Set（强制发现问题集）和持续访谈。`hovo-ecp-semantic` 改为 evidence-first（证据优先）+ bounded HITL（有界人工参与）。

### mareasw/ontoskills

采用：确定性校验、SHACL Gatekeeper（SHACL 门禁）和语义漂移显式失败的工程思想。

拒绝：完整 OWL 2 / 通用 SPARQL Runtime 假设，因为 ECP Semantic Profile 1.0 明确只支持有限子集。

### mattpocock/skills

采用：事实由 Agent 自行查证；深度 `grilling`（追问式澄清）作为显式流程而非默认；`to-spec` 在上下文足够时直接综合；`prototype` 在低风险歧义时允许采用明确假设继续推进；Frontier（当前可推进前沿）用于只阻塞依赖缺失输入的资产。

## 综合结论

`hovo-ecp-semantic` 的原创执行模型是：

**evidence-first（证据优先） + uncertainty classification（不确定性分类） + bounded HITL（有界人工参与） + asset-local blocking（资产级局部阻塞） + ECP finite-profile validation（ECP 有限配置边界校验）。**

本技能不把先例文字拼贴进提示词，而是吸收机制并以 ECP Authoring Kit 1.7 作为最终技术权威。
