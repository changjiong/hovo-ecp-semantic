# 五类技能建设交接

日期：2026-09-09。所有者 Hovo。semantic-foundry 0.5.0；五个生产技能分别为 0.1.0。依据用户明确给出的五类建设方案，使用 qiaomu-meta-skill 2.8.1。这里只建设技能包，不改 A01 业务资产，不导入或发布 ECP。

## 生成顺序与合同

先建立 shared contract 1.0.0，随后依次建立 domain-knowledge、domain-model、ecp-semantic-authoring、ecp-data-mapping、ecp-semantic-release。每个技能先落输入/输出 Schema 与验收清单，再写精简 SKILL、README、manifest 和接口。最后把 semantic-foundry 改为编排入口。

各阶段默认产出 output.json 与业务 review.md，阶段确认绑定版本和字节摘要。共享 schema 定义引用、来源、证据、确认、案例、问题、追溯和独立状态；各阶段仅扩展自己的业务内容。没有新增通用运行时或平台 API。

## 参考研究

本次补充两条意图检索：`domain knowledge requirements modeling`、`semantic data mapping release validation`。qiaomu 内置双目录研究得到39个归并候选族；第一条 skills.sh 查询30秒超时，另三个目录查询成功。原始证据见 [pipeline-prior-art-candidates.json](pipeline-prior-art-candidates.json)。安装数与仓库 stars 不合并，也不解释为质量评分；研究完整性为 partial。

继续参考并回读此前研究的 [OntologyEX / ontology-extraction](https://github.com/New1Direction/OntologyEX/blob/main/ontology-extraction/SKILL.md)、[ontology-agent-suite](https://github.com/Mokee04/ontology_research/blob/main/ontology-agent-suite/SKILL.md)，以及用户提供的 [qiaomu-meta-skill](https://github.com/joeseesun/qiaomu-meta-skill)。此前候选实读与许可缺口见 [原研究记录](prior-art-research.md)。未执行第三方候选代码、安装候选或根据流行度排名声明效果。当前维护频率、独立安全审计与用户评分仍无充分证据。

| 参考 | 具体采用 | 本次取舍 |
| --- | --- | --- |
| qiaomu-meta-skill | 合同先行、精简入口、按需参考、完成声明由证据支持 | 使用用户指定名称与 Hovo 所有权；不自动发布；没有模型评估就不宣称生产验证 |
| ontology-extraction | 从消费者和能力问题确定模型，区分领域语义与应用映射 | 不继承固定上位类数量、固定四层或机械表转类 |
| ontology-agent-suite | 阶段成果、来源与建模决定可审查 | 采用用户要求的明确阶段确认；不继承固定团队树或自动执行多个生产角色 |

原0.4.0研究中“每阶段停等”的拒绝是当时交互取舍，本次用户明确要求分阶段确认，现已被本方案替代。原报告作为历史研究保留，不再控制当前流程。

## 新增机制与证据等级

- `design advantage`：五个根技能具有排他的生产责任和10份输入/输出 Schema；共享合同只有一份，依赖在 manifest 明示。
- `design advantage`：领域模型输入排除物理结构与平台细节，同时明确保留标准业务属性；新增更换系统后的语义稳定性检查。
- `design advantage`：前序成果经明确确认才进入下游；变更按资产归属退回并使受影响旧证据失效；发布不负责改业务规则。
- `design advantage`：Scope 在真实 Mapping 稳定后由映射阶段编制，发布阶段只检查并组装；Evaluation 编译预期只来自真实平台。
- `hypothesis`：这些约束能够降低字段搬家、静默业务取舍和跨阶段语义漂移；尚无真实模型执行对照或专家验收证明效果。

## 验证边界

初次检查发现03手册的受控摘要滞后于本轮开始前已存在的提交 c00785d。已读取该提交相对上一提交的完整文档差异：版本行去掉“收敛版”，删除若干历史版本、交付状态和样板范围说明，正文主要模型不变。本次不改原文；来源清单明确接受当前已提交文件，03原摘要 `1ea7595e7279a1582ce29d530442486067a765e267099acb51b1e3930744bbd0`/34390字节更新为 `97eae974cc70933c6e307b1727c66348d577de9a645cbfc6dd66b80273a9332c`/33319字节。其余三册与 Kit 不变。原文删除这些说明不产生新的运行、业务或法规验证证据，五技能继续独立执行证据边界。

本次只创建/修订技能、Schema、指引与生产校验工具；未新增或修改测试代码。新包目前为 scaffold candidate，目标是团队生产使用，发布技能目标为 governed。模式标记反映当前证据成熟度，不表示已经验证业务能力。

本地检查结果见 [本次验证记录](pipeline-verification.md)。0.4.0的工具回归、关键词样例、旧 design-contract 和合成工程报告不证明五技能路由与阶段执行。尤其旧关键词分类器不是模型行为评测，不用它宣称新路由通过。

仍缺：五技能实际模型触发与生成评估、领域专家审查、宿主干净安装及上下文隔离、目标 ECP 导入/编译/发布/Run、真实数据发现及业务验收。Schema 能限制结构并检查有限引用，不能证明模型遵守输入边界、确认人的身份或业务定义正确。

同级六目录共同构成可调用技能集合；单阶段入口可以独立调用，但共享合同与参考工具依赖 semantic-foundry。没有验证独立目录搬移后的安装，不宣称单包零依赖。
