# 数据事实化验收

依据本地手册 02 §5.4、[来源核对](source-intake.md)、[Mapping 指南](ecp-kit-1.7/guides/ecp-mapping-json-format.md) 和其 [正式 Schema](ecp-kit-1.7/contracts/mapping-definition-v1.schema.json)。本阶段输出合同记录工程说明，不能替代 Mapping wire。

1. 核对 Ontology 原始 TTL 字节、Authoring 确认及事实需求。`ontologySourceDigest` 必须等于所绑定 TTL 原字节摘要；语义相同但空白变化仍要重绑。未导入平台时注明本地计算，导入时核对服务端摘要。
2. 固定数据源 code、environment、结构采集方式、时间和责任人。DDL/字典只证明提供的结构；没有当前发现证据时 `live_discovery=NOT_EXECUTED`，不能宣称已连接。不得索取或复制凭据到资产。
3. 每个 Scan 列真实存在，recordKey 有依据，且来源行身份不冒充现实对象身份。说明跨源匹配、同名不同人、重复、版本、更名和缺键策略；缺稳定身份时保留 DATA_GAP。
4. Join 有业务意义、键依据、左右列、真实基数及不匹配处理。不得靠相似字段名猜关联。当前 Mapping wire 只支持同源等值 INNER/LEFT 及 ONE_TO_ONE/ONE_TO_MANY/MANY_TO_ONE；真实多对多可以在审查合同中报告，不能塞入不支持的 wire。治理桥接是否成立需要实际结构与责任人依据。
5. 每个绑定说明 0、false、UNKNOWN、NOT_APPLICABLE、MISSING 如何区分，单位/尺度/分母/精度/舍入及时间含义。源中的 25 或百分号文本不自动等于领域 0.25。
6. 转换按当前平台真实能力决定执行归属。先核对 Mapping 合同是否支持转换；不支持就交给已确认治理来源、Authoring 的受支持规则，或记录 Gap。禁止私造 transform 字段、SQL、隐藏视图和运行时回调。
7. 类型与 SHACL 一致；OMIT 与必填形状、多值与单值形状等矛盾返回责任阶段。不能降低业务要求来迁就脏数据。来源异常可以留在证据或观察范围，不得混入已采用事实。
8. 原始字段、报文、载荷保存在受治理来源/快照及审查资料中，保留记录身份与存证引用。没有消费需求与平台支持时不把整行 JSON 灌入主本体。
9. 分别报告来源读取、映射覆盖和业务事实完整性。拒绝行、部分扫描、身份缺口、关系不明必须传播 UNKNOWN。完整扫描不能证明现实世界完整。
10. 需要局部调查时，按 [Scope 指南](ecp-kit-1.7/guides/ecp-scope-json-format.md) 在 Mapping 稳定后编制独立 Scope 候选。Root key 对齐 recordKey，全量 Scan/Join、可达性、rootBindings/fullScan 和限额均有依据。全量 Run 不强制 Scope；Scope 不是 Evaluation.objectScope。发布技能只核对与组装它，不重新设计事实边界。
11. 向 Authoring 返回类型、基数、事实供应能力和错误证据；改变身份或业务意义则返回 domain-model。数据负责人确认固定版本与缺口处理后才能进入发布准备。

交付 `output.json`、`review.md`、真实来源 Schema 快照、所能生成的 Mapping/Scope。受阻时交付缺口与可完成部分，不以占位符构成“可运行映射”。审查稿用“来源字段、业务含义、目标槽位、转换归属、身份与关联、缺值/时间/单位、覆盖及确认”组织。
