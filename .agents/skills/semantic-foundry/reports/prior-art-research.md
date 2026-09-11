# 本次技能修订的参考研究

历史范围：本报告记录0.4.0研究。当前0.5.0五阶段方案与交互取舍见 [五技能建设记录](pipeline-creation.md)，尤其“拒绝每阶段停等”已由用户本次明确要求的阶段确认替代。

研究日期：2026-09-09。方法来源：用户指定的 qiaomu-meta-skill 2.8.1。任务是修订既有 Hovo 技能，保持所有权与目录身份，不改为 qiaomu 命名、不发布。

## 检索与证据

双目录查询为 `ontology engineering`、`semantic modeling requirements`，覆盖领域建模、执行质量和需求落实。通过元技能内置 `research_prior_art.py` 使用严格模式执行，两次查询在 skills.sh 与 SkillsMP 均成功，按仓库/技能族归并后得到54个候选族。原始查询、指标和归并记录保存在 [prior-art-candidates.json](prior-art-candidates.json)。

skills.sh 安装数和 SkillsMP 仓库 stars 分列，不合计、不解释为用户评分。检索候选中领域工程条目 `daemon-blockint-tech/agentic-enteprises-skill:ontology-engineer` 观察到41次安装，但尝试的源入口未取得内容，未采纳。大仓库中的科学术语解析、EFO 查询和通用上下文技能与本任务重合有限，不因仓库 stars 高而采用。

补充查询既有 manifest 中的候选原仓库，实读下列入口；跨翻译页面和 raw/网页副本按同一仓库与技能路径视为同一来源。没有把只出现在搜索列表的候选列为已研究技能。

| 实读参考 | 可采纳机制与落点 | 明确拒绝 | 信号、许可与缺口 |
| --- | --- | --- | --- |
| [qiaomu-meta-skill](https://github.com/joeseesun/qiaomu-meta-skill)，用户指定本地2.8.1全文及相关方法 | 精简根入口、按需资源、输出与证据分开，落实到 SKILL、references、reports | 继承默认作者/名称、为修订任务自动发布或多建基础设施 | 本地版本已读；远端维护与安装未验证 |
| [OntologyEX / ontology-extraction](https://github.com/New1Direction/OntologyEX/blob/main/ontology-extraction/SKILL.md) | 先确定消费者与边界、能力问题、每个概念有来源、源记录往返，落实到输入核对与建模方法 | 强制四层、固定数量上位概念、单层任务也交付其他层空壳 | 入口与 MIT LICENSE 实读；当前维护频率、安装指标、安全审计、用户评分未取得 |
| [ontology_research / ontology-agent-suite](https://github.com/Mokee04/ontology_research/blob/main/ontology-agent-suite/SKILL.md) | 保存来源、建模取舍与审阅结果，落实到业务审查稿和确认回写 | 每阶段强制暂停确认、固定团队树、依赖包外共享入口 | raw 抓取失败后取得 GitHub 页面全文；许可、独立安全审计和用户评分未核实 |

另读了 [OntoSkills README](https://github.com/mareasw/ontoskills)，其主要任务是将技能编译为 OWL 并提供自身运行时，与生成 ECP 领域资产不同。未研究其技能入口，因此不列为已研究技能，也不继承其确定性宣传或新增运行时。

## 取舍与原创

- `keep`：能力问题先行、来源可定位、实际证据才支持完成声明；保留既有有限校验和只读打包机制。
- `adapt`：阶段反馈改为内部审查与有界高影响澄清；把长期访谈确认清单作为交付物，不要求当前用户回答全部问题。
- `reject`：固定上位本体层数、机械把表转类、每阶段停等、把 OWL/SHACL 通过当业务批准、自带运行时替换 ECP。
- `invent`：将 V2.1 的目标、事实、事理、判断与行动具体落实为可审查模板；通过 CQ/IRI/字段/规则/案例/确认 ID 回写同一资产集合；将平台导入识别、精确修订编译和固定数据运行列为不同证据事项。

## 结论边界

上述是针对当前需求的设计取舍，没有执行第三方代码、安装技能或进行模型对比。目录查询成功不等于候选质量验证；维护频率、独立审计、用户满意度、干净安装、真实生成效果及 ECP 运行均不得由本研究推断。缺少这些证据不妨碍本地修订，但阻止相应效果与发布声明。
