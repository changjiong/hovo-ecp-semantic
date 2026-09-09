# Semantic Foundry

从业务材料和真实数据源结构生成 ECP 领域资产，同时交付业务人员能审查、实施团队能据此访谈确认的设计材料。

当前版本：`0.4.0` 候选；参考四册金融语义工程手册 V2.1、ECP Authoring Kit 1.7。技能规定各阶段验收要求，并提供有限本地检查工具；特定领域资产能否导入、编译和运行，需要该资产在目标 ECP 的实际证据。

## 提供什么输入

- 业务资料：业务目标、制度、流程、规则说明、历史案例，保留版本与段落定位。
- 数据源结构：DDL、数据字典、接口模式或 JSON Schema，包括字段类型、主键、可空性和关联依据。
- 已有资产及约束：现有概念、IRI、Profile、可用数据源与算子；有授权时提供脱敏样本。无需在材料中填写连接密码。

只提供材料时可以先形成概念和访谈草案；只提供 schema 时先标出尚无业务依据的含义。缺少目标平台连接不妨碍设计，但平台运行状态会保留为未执行。

## 自然使用示例

> 使用 semantic-foundry，根据这些业务材料和数据源结构生成领域资产。先贯通一个核心业务问题，交付业务审查稿、工程设计契约、ECP 工作区和验证状态；明确概念、认知机理、数据缺口及后续访谈确认事项。

> 审阅这套 ECP 资产：比例、时点和身份口径是否正确，哪些结论不能推出，现有字段是否能实现。此次只做审阅。

> 按这份业务确认记录修订相关概念与 Mapping，列出受影响的规则、案例和摘要；平台操作按已授权范围处理。

## 会得到什么

| 交付 | 用途 |
| --- | --- |
| `design/domain-review.md` | 业务任务、概念关系、事实采用、计算/判断机理、字段落实、需求访谈及确认 |
| `design/contract.json` | 用稳定 ID 和 IRI 连接来源、能力问题、模型、适配、案例和未决项 |
| `workspace/` | 按 ECP 正式合同生成的本体、映射、约束及所需规则/Scope；只装登记成员 |
| `reports/` | 本地检查、平台导入、编译、数据运行和业务确认分别记录证据与缺口 |

业务审查稿按[模板](assets/domain-review.template.md)呈现。完整要求见[输出合同](references/output-contract.md)，资料阅读路线见[四册索引](references/handbook-index.md)。单资产任务按范围裁剪。

## 本地工具

Python 依赖见 [requirements.txt](requirements.txt)，可在项目隔离环境中安装。标准 SHACL 实例验证还需要 [requirements-shacl.txt](requirements-shacl.txt)。以下示例从技能目录运行，输出放在导入包外：

```bash
python3 scripts/validate_skill.py .
python3 scripts/scaffold_design.py /path/to/project
python3 scripts/validate_design.py /path/to/project
python3 scripts/validate_ecp_assets.py /path/to/project/workspace --json-out /path/to/project/reports/assets.json
python3 scripts/package_workspace.py /path/to/project/workspace --output /path/to/project/domain-assets.zip
```

`scaffold_design.py` 只创建待填写的结构模板；业务审查稿按任务填写，不会从 schema 自动获得正确业务定义。`validate_design.py` 检查结构和引用，不替代专家；`validate_ecp_assets.py` 是有限静态检查，不连接 ECP。打包不修改内容或自动刷新摘要。

现有非 UI 验证入口为 `scripts/run_verification.py --output <report-directory>`，仅在任务已授权且由指定验证角色执行时使用。现有样例和报告是合成参考工程，不是客户数据或平台运行证明。

## 安装与更新

本目录已处于项目 `.agents/skills/semantic-foundry/`。支持项目技能发现的宿主可从根 `SKILL.md` 读取；入口名和目录名统一为 `semantic-foundry`。宿主当前会话可能仍缓存旧入口，需要新会话重新发现。跨宿主与干净环境安装证据尚未取得，不承诺已在所有列出的目标宿主验证。

## 常见问题

| 现象 | 处理 |
| --- | --- |
| 缺少真实字段或数据源标识 | 保留设计与字段缺口；不伪造可运行 Mapping |
| 本地通过但 ECP 拒绝导入/编译 | 对照目标 Profile、页面导入责任、真实 schema、依赖修订及诊断；本地报告不覆盖全部平台检查 |
| 求值缺 `compilerContract.expect` | 取得真实编译器预期，或将求值保留为包外草稿 |
| 资产修改后摘要不一致 | 审阅差异，单独刷新相关摘要，再验证；不能沿用旧修订证据 |
| 业务确认未完成 | 交付具体议题与影响；用户沉默不构成确认 |
| 生成了 ZIP，但没有运行证据 | 只能报告完成打包，导入/编译/Run 分项保持未执行 |

本技能由 Hovo 维护；每季度或 Profile/手册发生变化时复核。设计方法借鉴 qiaomu-meta-skill、OntologyEX 和 ontology-agent-suite，具体取舍见[研究记录](reports/prior-art-research.md)。参考材料权利与再分发范围见[来源说明](THIRD_PARTY_NOTICES.md)，未经授权不发布材料或平台资产。
