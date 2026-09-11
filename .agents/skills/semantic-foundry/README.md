# Semantic Foundry

按需编排五个独立技能，将业务资料经过确认的知识、领域模型、平台表达和数据映射，形成可审查的 ECP 交付。知识与模型技能为0.3.0，编制技能为0.2.1，映射与发布技能为0.2.0；均为本地候选。五个技能不依赖本编排器。

## 顺序与使用

| 顺序 | 技能 | 交付 |
| --- | --- | --- |
| 1 | domain-knowledge | 有来源的知识、术语、规则、冲突和案例 |
| 2 | domain-model | 数据与平台无关的概念、业务属性、关系和判断机理 |
| 3 | ecp-semantic-authoring | Ontology、SHACL、规则、实现对应与能力缺口 |
| 4 | ecp-data-mapping | Schema、Mapping、身份/Join/NULL/单位/时间及必要 Scope |
| 5 | ecp-semantic-release | 清单、工作包、依赖检查及授权后的发布回读 |

> 使用 semantic-foundry，从这些业务材料开始建设语义资产。每个阶段先交付可审查版本，经明确确认后再推进；数据结构只进入允许的阶段。

每个技能均可直接调用，完整目录包含自己的 SKILL.md、Schema、验收清单、README、宿主接口、参考资料与所需工具，可以分别安装。输入来自人工、其他工具或其他技能均可，按内容合同和确认依据验收。公共合同采用同版本本地副本，不需要运行时读取本包。只有选择跨阶段编排时才需要本技能。

## 交付与检查

当前阶段交付 input.json、output.json 和 review.md，形成精确输入引用、摘要、来源链、案例与未决问题。知识、模型、平台表达和映射分别确认；发布动作单独按授权。详见 [阶段路由](references/pipeline.md)、[共享合同](contracts/README.md)、[交付合同](references/output-contract.md)。

Python 依赖见 [requirements.txt](requirements.txt)。公共结构检查：

```bash
python3 scripts/validate_pipeline.py --check-schemas
python3 scripts/validate_pipeline.py stage input /path/to/project/domain-model/input.json --project-root /path/to/project --skill domain-model
python3 scripts/validate_pipeline.py stage output /path/to/project/domain-model/output.json --project-root /path/to/project --skill domain-model
```

上述 validate_pipeline.py 是本仓库整套 Schema 的可选检查入口，需要当前仓库中的五阶段 Schema；各技能独立使用各自的 scripts/validate_contract.py，不调用本脚本。ECP 技能各自携带所需静态检查、摘要或打包脚本。它们不包含平台发布客户端，不证明业务批准或 ECP 编译/Run。examples 中的合成参考工程及旧报告不作为新流水线验证证据。

## 当前边界

五个技能的单目录检查见 [独立使用验证](reports/standalone-verification.md)；前两个领域技能0.3.0及模型接收同步的最新记录见 [领域基础修订](reports/domain-foundation-revision.md)。模型生成效果、宿主上下文隔离、专家确认、宿主安装与 ECP 导入/编译/发布/Run 仍需对应实际证据。不能把 Schema 检查当成完整工程能力认证。测试代码本次不新增或修改；现有测试执行遵守任务和角色授权。

Hovo 维护并保留现有所有权，使用用户指定的 qiaomu-meta-skill 方法。新技能暂列 scaffold 候选，目标为团队生产使用；研究、取舍和证据缺口见 [建设记录](reports/pipeline-creation.md)。手册及 Kit 来源权利见 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)。
