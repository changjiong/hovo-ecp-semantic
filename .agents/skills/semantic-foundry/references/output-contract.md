# 五阶段交付合同

每个生产技能拥有自己的输入、输出 Schema 与验收清单。共享对象、摘要规则、状态与变更关系定义在 [共享合同](../contracts/README.md)。本文件规定项目布局和编排交接，不再用一份混合设计合同同时承载知识、领域模型与字段映射。

```text
<project>/
  sources/                     已有资料可直接引用，不强制搬移
  domain-knowledge/
    input.json
    output.json
    review.md
  domain-model/                同样的 input/output/review
  ecp-semantic-authoring/      加实际 TTL、规则及包外草稿
  ecp-data-mapping/            加 Schema 快照、Mapping 及所需 Scope
  ecp-semantic-release/        加清单、工作包和实际回执
  pipeline.json               仅跨阶段编排时需要；独立技能不要求此文件
  confirmations/              实际确认记录，不提前生成签字
  reports/                    实际检查及交付状态
```

按任务范围创建到当前阶段，不预填未来阶段为空壳成果。输入引用相对项目根目录；来源材料的版本和摘要必须可定位。原有 examples 中的 design-contract 工具和合成报告仅作为既有参考工程，不是新流水线输入合同，也不提供自动迁移或兼容路径。

## 分阶段交接

| 阶段 | 业务审查主线 | 下游使用 |
| --- | --- | --- |
| 知识 | 问题、陈述、术语、规则、冲突与案例 | 确认后的业务知识，不传递物理字段正文 |
| 模型 | 概念、属性、关系、身份、时间、证据与判断机理 | 固定 Domain Model 与业务确认 |
| 平台表达 | 模型到 IRI/规则、事实要求及 Capability Gap | 精确资产字节、定义及实现确认 |
| 映射 | 字段语义、身份、Join、基数、NULL/单位/时间、覆盖 | Schema、Mapping、必要 Scope 与数据确认 |
| 发布 | 精确依赖、清单、摘要、动作和回执 | 实际 Revision/Release/Run 及案例对照 |

每项关键能力审查正例、反例、边界、缺证输入的预期与禁止结果。业务案例规格不等于测试代码；创建/修改测试仍需任务授权。

## 本地工具与证明范围

独立使用时，在当前技能目录、使用已安装本包 requirements.txt 的 Python 环境：

```bash
python3 scripts/validate_contract.py --check-schemas
python3 scripts/validate_contract.py validate input /path/to/project/domain-model/input.json --project-root /path/to/project
python3 scripts/validate_contract.py validate output /path/to/project/domain-model/output.json --project-root /path/to/project
```

以下命令在 ecp-semantic-release 技能目录执行：

```bash
python3 scripts/validate_ecp_assets.py /path/to/project/ecp-semantic-release/workspace --json-out /path/to/project/reports/assets.json
python3 scripts/package_workspace.py /path/to/project/ecp-semantic-release/workspace --output /path/to/project/ecp-semantic-release/assets.zip
```

各技能校验器只使用本包 $id Registry 解析 Schema，不访问 hovo.local 或其他技能目录。它检查结构、路径、摘要和有限 ID/证据引用；不会证明文本中的业务语义、确认人身份或输入隔离已由宿主强制执行。阶段验收清单及明确确认仍不可省略。ECP 工具仅声明其实现的静态范围，不连接平台。

semantic-foundry 保留 scripts/validate_pipeline.py 作为本仓库全套合同的可选检查工具；它使用同级五阶段 Schema，不是单技能的验收依赖。单项交接使用 --skill 指定阶段并调用该技能校验器。知识与模型采用平台无关合同2.0.0；其余阶段保留各自合同版本，通过精确输入引用衔接，不要求所有阶段同时升级。

## 五项目标

概念正确需要定义、身份、时间与反例的专业审查；业务可理解需要具体例子和责任人反馈；认知机理可审查需要采用事实、方法前提、参数、例外、未知及权威；需求确认需要可定位事项与回写；ECP 可运行需要精确修订的真实编译、Published Release、Source Snapshot、COMMITTED Run 及案例结果。

交付报告分列 Business Confirmed、Static Checked、Platform Compiled、Released、Runtime Validated、Business Accepted。不存在一个由脚本授予的全局 PASS。未执行写 NOT_EXECUTED；实际失败写 FAIL，工具异常写 ERROR；不适用说明原因。

没有真实编译器则编译诊断未执行；没有发布则 Revision/Release 回执留空；没有 Run 则结果不填。历史证据归档保留，但不能证明摘要已改变的新资产。
