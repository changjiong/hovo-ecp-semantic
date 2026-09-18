# 来源检索与选型 · 2026-09-16

本轮以用户指定的 qiaomu-meta-skill 2.8.1 为唯一技能工程方法，保留 Hovo 所有权及 domain-model 身份。目标：把描述性模型交付改为具有正式语法、有限类型语义和可重放实例的本地 DSL。

通过其 research_prior_art.py，以 domain modeling DSL、ontology modeling validation、state machine specification 检索 skills.sh 与 SkillsMP；两目录三组查询完成，70 个候选族。原始报告见 prior-art-candidates.json。目录安装数与仓库星标是不同指标，仅作发现信号，不证明质量或安全。

## 实际阅读的两个技能

1. [mattpocock/skills: domain-modeling](https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md)。已读取 SKILL.md 完整源文。采用具体边界场景澄清术语、领域语言排除实现细节的方法；不采用仅 CONTEXT.md 词汇表加 ADR 的核心输出，因为本任务需要可校验模型。代码现状只可作为差异诊断，不能取代用户指定的知识权威。目录星标信号与许可证、维护承诺未做独立审计；没有复制源码或安装运行。
2. [eclipse-langium/langium-ai: lai-gen-descriptor](https://github.com/eclipse-langium/langium-ai/blob/main/skills/lai-gen-descriptor/SKILL.md)。已读取 SKILL.md 完整源文及项目 README。采用单一声明驱动衍生产物、真实路径核对、语言变化后重新校验及覆盖语言特性的有效示例。拒绝引入 Langium/Node/LSP 工具链：本任务现有 Python/JSON Schema 足够。仓库展示 MIT，具体提交许可证与维护频率未另审；未复制其实现或执行外部 CLI。

## Keep / Adapt / Reject / Invent

| 决策 | 来源或本地依据 | 落地 |
| --- | --- | --- |
| Keep | Hovo 既有精确版本、未决问题、确认边界 | 输入合同与交互评审继续保留 |
| Adapt | domain-modeling 的反例澄清 | 类型正反例、问题与案例覆盖 |
| Adapt | lai-gen-descriptor 的单一声明及示例机制 | model.yaml 生成两个视图，交接检查防漂移 |
| Reject | 仅词汇表作为模型交付 | 必须类型、表达式、迁移的形式语法 |
| Reject | 引入完整 Langium 工具链 | 使用现有 Python 环境加 PyYAML |
| Invent | 本任务要求与本地知识合同 | 三值表达式、Date 连续区间运算、人工判断缺口、固定知识与 DSL 交接 |

OWL state-machine 候选在目录有发现信号，但尝试的 raw 源路径返回 404；未完成源码阅读，未据它作机制结论。其余候选仅作目录筛选。上述借鉴不证明优于原技能；跨模型生成质量、实际触发与业务可读性仍缺独立证据。
