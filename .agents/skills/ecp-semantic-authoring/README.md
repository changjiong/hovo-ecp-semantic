# ecp-semantic-authoring

将固定 Business Domain Model（业务领域模型）和真实数据结构编制成一个 ECP V3（第三版）技术语义模型闭包。Hovo 0.3.0，合同 2.0.0，面向 Semantic Authoring Kit 1.8（语义编制工具包 1.8）。

本技能已经吸收原 ecp-data-mapping（ECP 数据映射）的职责。Mapping（映射）不是下游独立阶段，而是 Ontology（本体）与规则资产之间的同一 Revision（修订版本）成员。

正式输出目录只放 input.json、output.json、review.md 和实际 Ontology/SHACL/Mapping/Derivation/Evaluation/Lifecycle/Action Policy（本体/形状约束/映射/派生/求值/生命周期/动作策略）资产；生成日志和试验文件放 process/。

安装依赖：
    python3 -m pip install -r requirements.txt

合同检查：
    python3 scripts/validate_contract.py --check-schemas
    python3 scripts/validate_contract.py validate input /path/to/project/ecp-semantic-authoring/input.json --project-root /path/to/project
    python3 scripts/validate_contract.py validate output /path/to/project/ecp-semantic-authoring/output.json --project-root /path/to/project

V3 静态资产检查：
    python3 scripts/validate_ecp_assets.py --ontology ontology.ttl --mapping mapping.json

references/ecp-authoring-kit-1.8/ 是 2026-09-28 从 enterprise-cognitive dev 当前建模入口同步的固定快照，只用于作者参考和有限静态校验。目标 Workspace 的 deployment_boundary（部署能力回执）仍必须作为本次输入；不能用随包快照冒充目标环境能力。

完整验收见 references/acceptance.md。平台编译和发布不属于本技能。
