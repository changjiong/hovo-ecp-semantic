# Semantic Foundry 0.4.0 修订交接

交付：从业务材料与真实源结构生成可审查、可确认、按 ECP 合同实现的领域资产。当前为本地修订候选；未提交、发布、安装到新宿主或操作 ECP。

## 已修订的设计

- 根入口与目录统一为 `semantic-foundry`，版本0.4.0，来源更新到四册 V2.1，保留 Hovo 所有权。
- 默认交付业务审查稿、工程设计契约及所需 ECP 工作区，分别承接业务理解、工程追溯与平台识别。
- 认知机理必须说明事实采用、查询/计算/规则、前提、例外、结果权威、不足处理及后续责任。
- 需求确认事项直接关联 CQ、概念 IRI、字段、规则、案例及修订；答复后同步资产和证据。
- 本地检查、业务确认、导入回读、编译和数据运行分别记录，不由一个通过状态替代。

## 学习与取舍

实读参考为 qiaomu-meta-skill、OntologyEX 的 ontology-extraction、ontology-agent-suite，完整来源与缺口见[研究记录](prior-art-research.md)。

| 参考 | 采用的具体机制 | 本次取舍 |
| --- | --- | --- |
| qiaomu-meta-skill | 精简入口、输出合同、研究与证据边界 | 保持既有品牌；不因治理模式自动发版 |
| OntologyEX | 消费者范围、概念来源、源实例往返 | 不强制四层和上位类数量 |
| ontology-agent-suite | 来源记录、建模决定与阶段审阅 | 内部先审查，集中澄清高影响问题，长期访谈材料随包外交付 |

新增连接点是把 V2.1 的认知主线、需求确认回写和 ECP 运行证据放到同一能力问题的交付链；没有新增语义运行时或改写平台协议。

## 优势与证据

| 标签 | 当前能支持的结论 | 依据 |
| --- | --- | --- |
| `design advantage` | 新增可直接用于需求审查与确认的完整业务模板 | `assets/domain-review.template.md` |
| `design advantage` | 业务含义、认知机理、字段与平台责任可逐项追溯 | `references/output-contract.md`、`references/source-intake.md` |
| `design advantage` | 旧路径修复为当前原文快照和一致的技能身份 | 根入口、manifest、source-manifest 与包检查器 |
| `validated advantage` | 当前包合同与16条既有关键词边界通过；参考工程41项和标准 SHACL 通过 | [验证记录](verification-summary.md)；仅限列明的检查范围 |
| `hypothesis` | 能减少后续访谈中概念和数据口径的反复 | 缺实际业务用户评审和生成对照证据，尚未证实 |

验证结果见[验证记录](verification-summary.md)。工具回归50项中49项通过，1项因旧手册路径报错；总状态仍为 partial/FAILED，不宣称全部通过。测试代码未获修订授权，保持原样。源材料摘要只证明文件一致，不认证材料内容。

## 尚未取得的证据

业务用户实际评审、真实模型生成对照、目标 ECP 导入/编译/数据运行、干净宿主安装、公开再分发批准仍为 `missing evidence`。这些步骤需要具体业务输入、目标环境或相应授权。本次技能修订不代替任何领域资产的业务确认或运行验收。
