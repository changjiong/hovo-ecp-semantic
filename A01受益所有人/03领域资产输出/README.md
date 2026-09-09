# A01受益所有人领域资产

已生成 [a01-ubo-import-1.0.0.zip](a01-ubo-import-1.0.0.zip)，用于ECP导入识别和预检。当前为Draft候选：包文件成功生成，有限本地检查0错误、3警告，整体为 `INCOMPLETE / ECP_PREFLIGHT_REQUIRED`。没有执行平台导入、编译、发布或数据运行。

业务审阅从 [domain-review.md](design/domain-review.md) 开始；本稿覆盖谁被识别、权利及路径、形成时间、历史、证据、差异和后续责任，明确当前数据支持与缺口。

| 文件 | 用途 |
| --- | --- |
| [业务审查稿](design/domain-review.md) | 8个能力问题、概念、认知机理和5组待确认项 |
| [设计契约](design/contract.json) | 来源、身份、事实采用、平台适配和不确定性的结构化约定 |
| [逐字段映射](design/field-map.md) | 7表71列的实际落点：61个数据属性、9个FK关系、1个未投影JSON字段 |
| [知识萃取](design/knowledge-coverage.md) | 手册29项原编号的适用内容、依据、责任及缺口 |
| [验收规格](design/acceptance-cases.md) | 22个合成业务案例和2条派生规则合同；未执行 |
| [交付状态](reports/delivery-status.md) | 检查、打包、未执行和阻塞事项的分别记录 |
| [制度复核](reports/legal-evidence.md) | 第12号令、第3号令、指南、BOMIS和同业反例的依据定位 |
| [来源登记](reports/source-register.json) | 76份输入文件的原字节摘要与两份随交付输入原文副本 |

ZIP内仅7个文件：本体、映射、两条来源限制Derivation、Schema快照及两个清单。当前没有SHACL、Evaluation、Scope或Action Policy；不能直接当作可执行Release。

现有源缺已核实自然人身份、权利生效材料、完整路径/覆盖与机构/BOMIS记录。包内不自动生成受益所有人名单、形成日期、国企简化、兜底或差异报送结果。`source_row.issues_json`未投影，其完整问题明细仍是数据接入依赖。

ZIP摘要：`sha256:7dd2e065357cc125db5f399d142cbe377e709fadd2848d526861c93657f9222e`。包内工作区字节闭包摘要：`sha256:69c431b2897a101267f9030803af28ce2505b4ad3feba95b358ac99e34a1210e`。完整记录见 [package-result.json](reports/package-result.json)。
