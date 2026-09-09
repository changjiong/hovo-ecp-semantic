# A01导入候选包交付状态

交付日期：2026-09-09。目标目录为 `A01受益所有人/03领域资产输出`；本次范围止于生成导入包。ZIP已生成并完成内置回读，尚未导入ECP。业务能力覆盖为partial，工作区本地判断为 `INCOMPLETE / ECP_PREFLIGHT_REQUIRED`，不是 `LOCALLY_VALID` 或 `RELEASE_READY`。

## 1. 交付内容

| 内容 | 位置及实际范围 |
| --- | --- |
| 导入候选ZIP | `a01-ubo-import-1.0.0.zip`，Workspace V1，7个正式成员 |
| Ontology | `workspace/ontology/a01-ubo-source-evidence.ttl`；现实主体、权利、时间、材料和工作记录概念，与来源观察分开 |
| Mapping | `workspace/mapping/a01-ubo-source-evidence.json`；7表71个扫描列，61个数据属性映射、9个明示FK关系、1个JSON字段未投影 |
| Derivation | `a01_identity_verification_gap`、`a01_rights_time_evidence_gap`；逐股东来源行输出身份解析与权利生效证据使用限制，不输出已核实自然人或UBO |
| Schema及清单 | 随包7表schema、根manifest和rules/manifest；所有内容摘要绑定原字节 |
| 业务审查与设计契约 | `design/domain-review.md`、`design/contract.json`；8个能力问题、完整概念检查、事实政策和5组确认项 |
| 知识与验收 | `design/knowledge-coverage.md`的29项原编号；`design/acceptance-cases.md`的22个合成业务规格和2条派生合同 |
| 输入与复核证据 | 76份原始输入摘要、2份原文副本、制度复核、字段映射和各实际检查报告 |

缺少SHACL、Evaluation、Scope和Action Policy是当前Draft切片的明确限制。进入Engine Run需要适用的完整六阶段SHACL、正式求值及其精确编译证据等；本次没有用空规则或伪造compilerContract.expect满足目录形式。

## 2. 实际检查与未执行项

| 事项 | 预期 | 实际结果与状态 | 证据 |
| --- | --- | --- | --- |
| 输入盘点 | 记录指定输入路径及原字节身份 | PASS：76文件已登记；不等于全部同业文章全文审阅 | `source-register.json`、`source-intake.md` |
| 业务及制度材料复核 | 来源、适用、反例和缺口可定位 | PASS：完成有限作者审查与UBO专项AI只读复核；不代表人工专家或机构批准 | `legal-evidence.md` |
| 业务确认 | 有明确确认人、角色、时点及答复 | NOT_EXECUTED：Q-01至Q-05无业务签认 | `design/domain-review.md`第5节 |
| 7表与Mapping独立对照 | 字段、PK、FK和空值策略与提供字典一致 | PASS：7/7表、全部字段/主键及9项FK匹配；唯一未投影字段issues_json已披露 | 验真只读审计；`design/field-map.md` |
| 设计契约结构 | 设计Schema、概念声明及来源/验收引用可解析 | PASS：退出码0，2项结构与引用检查，无错误；不替代含义审查和业务批准 | `design-validation.json` |
| 工作区有限本地检查 | 公开格式、Profile有限语法、映射引用和摘要闭包 | INCOMPLETE：0错误、3警告、10项检查；退出码2。未完成Derivation类型计划判断 | `workspace-validation.json` |
| 打包及归档回读 | 生成同一不可变字节闭包，归档读回一致 | PASS：退出码0，7个成员，内置回读通过；继承localValidationStatus=INCOMPLETE | `package-result.json` |
| ZIP独立只读核对 | 无缺失、额外或重复成员，摘要与工作区字节一致 | PASS：7成员与工作区逐字节相同，ZIP及inputDigest一致 | 验真追加审计，本报告第4节 |
| SHACL实例验证 / 测试套件 | 当前真实或合成实例与预期对照 | NOT_EXECUTED：未写测试代码、未跑测试套件；22项业务案例是文本规格 | `design/acceptance-cases.md` |
| live数据源、真实样本与行数 | 目标目录和数据库实际证据 | NOT_EXECUTED：只使用提供的schema快照 | `source-intake.md` |
| 平台导入识别、Draft回读 | 平台环境和不可变Revision | NOT_EXECUTED | 无平台Revision |
| 精确Revision编译 | 目标编译器接受完整修订集合 | NOT_EXECUTED | 无编译报告；Derivation待ABI预检 |
| Release / Snapshot / Run / Candidate | 固定源快照和成功运行结果对照 | NOT_EXECUTED | 未发布、无Run及Candidate Set |
| BOMIS业务回执、正式决定与动作 | 权限、业务反馈、复核/办结 | NOT_EXECUTED | 当前无相关数据或绑定 |

有限检查的3个警告：两条 `COMPILER_PREFLIGHT` 分别对应两条派生规则，以及 `ECP_PREFLIGHT_REQUIRED`。本地工具仅检查FeatureDefinition封装，不能判断目标Runtime的全部算子类型、依赖和执行行为。跨资产引用项PASS只覆盖工具实际检查的Mapping等引用，不能替代计划编译。

## 3. 字节与工具依据

- ZIP SHA-256：`7dd2e065357cc125db5f399d142cbe377e709fadd2848d526861c93657f9222e`。
- 工作区字节闭包：`sha256:69c431b2897a101267f9030803af28ce2505b4ad3feba95b358ac99e34a1210e`。
- 设计契约原字节摘要：`sha256:a790f8b4669162d1991e4205f7174ab6113b8045dc5ad769e7e75482e179dcfe`。
- 技能：semantic-foundry 0.4.0；手册2.1；Kit1.7；Profile `enterprise-cognitive/semantic-profile/1.0.0`。
- Profile摘要：`sha256:708246ab3a0ce13a23977d39712a82f9a363f16a9c2fe428fe0311e4147b1882`，来自随Kit合同，未与目标平台回读匹配。
- 实际解释器：`.agents/skills/semantic-foundry/.venv/bin/python`；观察到rdflib 7.6.0、jsonschema 4.26.0。

| 工具文件（技能scripts目录） | 本次文件SHA-256 |
| --- | --- |
| package_workspace.py | `887da76dddfc2a322f7a3d848a7df6b9352365d38822cc2af839a117b08df6a4` |
| validate_ecp_assets.py | `b57ed04e09ebe55e7029d3d4334d4490b2ef1d66a04c6de002575d3a71fde4fa` |
| validate_design.py | `b437568f13a3578d04dcf649280be2da747430402c4f0eab2873d12909f15070` |
| workspace_files.py | `f5a197763243c3b44efeaf668d2a2071ca831a49127edd8612a30002ff84573f` |
| refresh_workspace_digests.py | `3a38c5238a86f34690987cf5b18cfd4eb960eaee4767bbf52166097282fff589` |

初始使用系统Python刷新摘要时，因系统环境没有rdflib，校验器在初始化时出现 `NameError: OWL`。主代理核对真实导入后改用技能已有虚拟环境，刷新命令成功退出0。没有修改技能源码或安装依赖。最终检查和打包仅引用成功刷新后的字节，初始失败不计为通过证据。

工作区检查命令：

```bash
.agents/skills/semantic-foundry/.venv/bin/python .agents/skills/semantic-foundry/scripts/validate_ecp_assets.py A01受益所有人/03领域资产输出/workspace --json-out A01受益所有人/03领域资产输出/reports/workspace-validation.json
```

设计检查命令：

```bash
.agents/skills/semantic-foundry/.venv/bin/python .agents/skills/semantic-foundry/scripts/validate_design.py A01受益所有人/03领域资产输出 --json-out A01受益所有人/03领域资产输出/reports/design-validation.json
```

打包命令：

```bash
.agents/skills/semantic-foundry/.venv/bin/python .agents/skills/semantic-foundry/scripts/package_workspace.py A01受益所有人/03领域资产输出/workspace --output A01受益所有人/03领域资产输出/a01-ubo-import-1.0.0.zip
```

打包命令要求新输出路径；已存在ZIP不会被覆盖。正文变化后须刷新受影响摘要、按授权重新检查并生成新版本包，不能沿用本次字节证据。

## 4. 独立审阅范围

UBO专项复核分派给 `ubo_evidence_specialist`，选择 `gpt-5.6-sol/high`，只读制度、字典和业务材料；检查点是适用制度、25%边界、所有权/控制、国企/兜底、形成日期和BOMIS职责。

资产核对分派给 `verification_auditor`，按固定要求选择 `gpt-5.6-luna/max`，执行本任务打包所需的既有静态格式入口与独立字段核对。没有新测试或测试套件执行。父会话为danger-full-access，审阅只读是任务指令约束，不能宣称由沙箱强制隔离。未观察调用账单或模型实际计费，不报告费用估算。

收尾审计核对20个概念IRI、全部Mapping引用、两条Derivation的扫描类/输出谓词和原因字符串，未发现设计与资产相互矛盾。独立ZIP回读确认missing、unknown、duplicate均为空，7个成员全部与工作区原字节一致。工作区静态检查约0.20秒、退出码2；设计格式检查约0.13秒、退出码0。这些耗时只对应工具执行，不代表整体生成耗时或模型费用。

## 5. 未闭合能力与使用限制

1. 缺自然人稳定身份、源类型枚举、权利种类/分母、完整路径、图覆盖和事实采用，不能得到完整UBO集合、控制认定、国企简化或兜底。
2. 缺法律生效材料、有效区间、获知时间和历史版本，不能确定形成/终止或还原历史关系；源变更、认缴、成立日期只保留其原含义。
3. 缺三方识别/申报/备案记录、差异指引原文和机构流程，不能判断或反馈BOMIS差异。通用响应与业务办结必须分开。
4. `issues_json`不投影，源问题明细不完整；decimal(20,0) ID到整数的20位精度与词法处理仍待实际平台证明。
5. 当前Profile与源目录尚未目标回读；没有精确Revision、Release、Snapshot/Run，也没有SHACL实例门禁或编译预期。

上述缺口均有责任、补充材料和回写位置，见业务审查稿Q-01至Q-05。它们限制后续识别和运行，不改变本次已生成的候选包与配套设计文件。

## 6. 操作边界

本次没有读取真实客户数据、执行平台或外部写操作、启动服务、构建生产镜像、进行浏览器手工测试或Git提交/推送。仓库原有技能和输入改动均保留；任务新增内容集中在指定输出目录。未来规则集完整替换导入需要先核对将移除的活动Draft及恢复依据，本次没有对此操作作任何执行承诺。
