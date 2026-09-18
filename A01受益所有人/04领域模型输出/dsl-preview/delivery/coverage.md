# A01 形成日期与差异闭环 DSL 聚焦草案 覆盖与审计台账

- DSL：1.0.0
- 资产：A01.DomainModel.DslPreview / 0.1.0
- 知识依据：DRAFT，A01.DomainKnowledge / 2.1.0
- 知识摘要：sha256:0962cfa90d0c2ee6ca60d02cefc3c4e06229368b3537e12f8b2fb701c7c9f0d9

> 此台账显示模型范围、缺口和追溯 ID；不是业务确认或受益所有人结论。

## 问题覆盖

| 问题 | 状态 | 模型要素 | 开放缺口 | 原因 |
| --- | --- | --- | --- | --- |
| K.Q.11.HISTORY | PARTIAL | M.Person、M.Qualification、M.Interval、M.CurrentFormation | M.Upstream.SEMANTIC_REVIEW、M.Gap.History | 本示例计算当前日期；尚未形式化回访展示、完整证据核验及跨类型事件的全部语义。 |
| K.Q.19.CLOSE | PARTIAL | M.Difference、M.CanResolve、M.DifferenceFlow、M.Resolve | M.Upstream.SEMANTIC_REVIEW、M.Gap.Closure | 本示例只判断及计算状态迁移；证据真实性核验、历史记录留存和实际业务写入仍由业务流程负责。 |

## 案例解释

| 案例 | 状态 | 模型要素 | 预期 | 禁止结果 | 解释 |
| --- | --- | --- | --- | --- | --- |
| K.C.PILOT.07 | BLOCKED | M.Person、M.Qualification、M.Interval、M.CurrentFormation | 当前形成日期为2024年6月2日；回访同时展示2019年形成、2021年终止事件、中断及本次重新形成。 | 不得删去历史中断，或将当前形成日期写成2019年3月1日。 | 日期计算或状态迁移可用示例求值；完整回访、证据与历史留存尚未全部形式化，整例保持 BLOCKED。 |
| K.C.PILOT.08 | BLOCKED | M.Person、M.Qualification、M.Interval、M.CurrentFormation | 保留各关系类型事件并补控制协议生效时间；核实整体连续后沿用原总体形成日期。 | 不得在缺生效证据时宣布连续或中断；不得因类型变化本身重置总体形成日期。 | 日期计算或状态迁移可用示例求值；完整回访、证据与历史留存尚未全部形式化，整例保持 BLOCKED。 |
| K.C.PILOT.13 | BLOCKED | M.Difference、M.CanResolve、M.DifferenceFlow、M.Resolve | 将该差异标为已解决，保留更正、查询复核和既有处置记录。 | 不得抹去历史，也不得从闭环状态推断其他法定记录义务消失。 | 日期计算或状态迁移可用示例求值；完整回访、证据与历史留存尚未全部形式化，整例保持 BLOCKED。 |
| K.C.PILOT.14 | BLOCKED | M.Difference、M.CanResolve、M.DifferenceFlow、M.Resolve | 保留待复核或待处理。 | 不得标为已解决。 | 日期计算或状态迁移可用示例求值；完整回访、证据与历史留存尚未全部形式化，整例保持 BLOCKED。 |
| K.C.REVIEW.TYPE_CONTINUITY | BLOCKED | M.Person、M.Qualification、M.Interval、M.CurrentFormation | 总体形成日期沿用2024年5月1日，股权类型终止与控制类型形成分别记2026年6月1日。 | 不得把总体日期重置为类型切换日；不得将本轮口径称为制度原文直接规定。 | 日期计算或状态迁移可用示例求值；完整回访、证据与历史留存尚未全部形式化，整例保持 BLOCKED。 |

## 上游未决项

| 知识问题 | 模型问题 | 处理 | 原因 |
| --- | --- | --- | --- |
| K.ISSUE.02 | M.Upstream.02 | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.CURRENT_TARGET_RISK | M.Upstream.CURRENT_TARGET_RISK | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.EXT.GOV.BROAD_UNITS | M.Upstream.EXT.GOV.BROAD_UNITS | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.EXT.GOV.PENALTY_BASIS | M.Upstream.EXT.GOV.PENALTY_BASIS | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.EXT.GOV.RETENTION | M.Upstream.EXT.GOV.RETENTION | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.EXT.GOV.REVIEW_FREQUENCY | M.Upstream.EXT.GOV.REVIEW_FREQUENCY | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.INTERFACE_IDENTITY | M.Upstream.INTERFACE_IDENTITY | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.INTERFACE_REPORT_DUTY | M.Upstream.INTERFACE_REPORT_DUTY | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.INTERFACE_THRESHOLD | M.Upstream.INTERFACE_THRESHOLD | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.REV.IDENTITY.AM_MANAGER | M.Upstream.REV.IDENTITY.AM_MANAGER | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.REV.IDENTITY.CIRCULAR_CALC | M.Upstream.REV.IDENTITY.CIRCULAR_CALC | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.REV.IDENTITY.FX_EQUIV | M.Upstream.REV.IDENTITY.FX_EQUIV | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.REV.IDENTITY.MISSING_ORDER11 | M.Upstream.REV.IDENTITY.MISSING_ORDER11 | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.REV.IDENTITY.TIED_MANAGERS | M.Upstream.REV.IDENTITY.TIED_MANAGERS | NOT_APPLICABLE | 本次仅形成日期和差异闭环；不涉及该事项的规则或问题，保留上游未决记录。 |
| K.ISSUE.SEMANTIC_REVIEW | M.Upstream.SEMANTIC_REVIEW | MODEL_LIMITATION | 影响本次问题，继承未确认或语义审查限制。 |

## 模型问题

| ID | 类型 | 状态 | 影响 | 解决前行为 |
| --- | --- | --- | --- | --- |
| M.Gap.Closure | MODEL_GAP | OPEN | K.Q.19.CLOSE | 保持 PARTIAL，不将规则示例视为整题完成。 |
| M.Gap.History | MODEL_GAP | OPEN | K.Q.11.HISTORY | 保持 PARTIAL，不将规则示例视为整题完成。 |
| M.Upstream.02 | MODEL_GAP | OPEN | K.ISSUE.02 | 标记待更新并保留跟踪，不能把30日作为日期容差或差异豁免；不臆定内部处置时限。 |
| M.Upstream.CURRENT_TARGET_RISK | MODEL_GAP | OPEN | K.ISSUE.CURRENT_TARGET_RISK | 制度链条继续作为应遵守的判断依据；现状单列。不得把评审记录“冲突解除”解释为合规差异已经裁定。 |
| M.Upstream.EXT.GOV.BROAD_UNITS | MODEL_GAP | OPEN | K.ISSUE.EXT.GOV.BROAD_UNITS | 不得将本补丁描述为7份文件全部业务语义审查完成。 |
| M.Upstream.EXT.GOV.PENALTY_BASIS | MODEL_GAP | OPEN | K.ISSUE.EXT.GOV.PENALTY_BASIS | 可识别规章内违法类型和档位，不作具体案件必然处罚结论。 |
| M.Upstream.EXT.GOV.RETENTION | MODEL_GAP | OPEN | K.ISSUE.EXT.GOV.RETENTION | 只陈述现有留存义务，不写10年、不自定起算日。 |
| M.Upstream.EXT.GOV.REVIEW_FREQUENCY | MODEL_GAP | OPEN | K.ISSUE.EXT.GOV.REVIEW_FREQUENCY | 执行事件触发复核；加强情形提高频率，但不填造季度、年度等统一周期。 |
| M.Upstream.INTERFACE_IDENTITY | MODEL_GAP | OPEN | K.ISSUE.INTERFACE_IDENTITY | 可继续业务判断与材料整理；不将未经澄清的字段匹配顺序作为已核验运行事实。 |
| M.Upstream.INTERFACE_REPORT_DUTY | MODEL_GAP | OPEN | K.ISSUE.INTERFACE_REPORT_DUTY | 可完成差异识别和非重大差异记录；不将接口可报备自动变成必须报送。 |
| M.Upstream.INTERFACE_THRESHOLD | MODEL_GAP | OPEN | K.ISSUE.INTERFACE_THRESHOLD | 业务识别依制度边界；该报送边界未经明确前不能声称已完成接口适配。 |
| M.Upstream.REV.IDENTITY.AM_MANAGER | MODEL_GAP | OPEN | K.ISSUE.REV.IDENTITY.AM_MANAGER | 不得默认选择管理机构法定代表人、产品经理或任一经办人；事实不足时保持证据不足。 |
| M.Upstream.REV.IDENTITY.CIRCULAR_CALC | MODEL_GAP | OPEN | K.ISSUE.REV.IDENTITY.CIRCULAR_CALC | 普通无环结构按逐路径相乘和同一自然人合计；循环、交叉结构停止精确比例与完整清单结论并加强核实。 |
| M.Upstream.REV.IDENTITY.FX_EQUIV | MODEL_GAP | OPEN | K.ISSUE.REV.IDENTITY.FX_EQUIV | 外币注册资本接近边界时返回证据不足，不自定汇率或容差；人民币案例按小于等于1000万元执行。 |
| M.Upstream.REV.IDENTITY.MISSING_ORDER11 | MODEL_GAP | OPEN | K.ISSUE.REV.IDENTITY.MISSING_ORDER11 | 仅表述为‘第11号令规定的客户尽调义务机构’，不按常识、机构名称或历史清单穷举。 |
| M.Upstream.REV.IDENTITY.TIED_MANAGERS | MODEL_GAP | OPEN | K.ISSUE.REV.IDENTITY.TIED_MANAGERS | 确认前三项均无人满足后可遵守‘至少一名最高层级’最低要求，但不宣称限定材料已规定同层优先顺序。 |
| M.Upstream.SEMANTIC_REVIEW | MODEL_GAP | OPEN | K.ISSUE.SEMANTIC_REVIEW、K.Q.11.HISTORY、K.Q.19.CLOSE | 本版可供按主题业务评审；不作为全量制度无遗漏或接口实现完备的保证。 |
