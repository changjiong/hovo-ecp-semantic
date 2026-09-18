# 0.3.0 行为验证记录

验证时间：2026-09-18（Asia/Shanghai）。模型：`model.yaml` 0.3.0；DSL：2.0.0。该记录只证明本地 DSL 求值器对列明输入的行为，不代表业务确认、平台运行或制度结论。

## 已执行

使用 `scripts/domain_dsl.py evaluate` 对 19 个边界输入求值，使用 `transition` 对 4 个状态迁移求值。

| 范围 | 输入 | 预期 | 实际 |
| --- | --- | --- | --- |
| 备案日期边界 | 2024-11-01 / 2024-10-31 | true / false | true / false |
| 25%阈值 | 0.25 / 0.2499 / UNKNOWN | true / false / UNKNOWN | true / false / UNKNOWN |
| 国企风险门控 | 清洁 / 第二十条触发 | true / false | true / false |
| 年月差异 | 同年同月 / 跨月 | false / true | false / true |
| 差异闭环 | 实际更正且复核一致 / 仅承诺 | true / false | true / false |
| 查询批次 | 100条 / 101条 | true / false | true / false |
| 日额度停止 | 恰好达到 / 未达到 | true / false | true / false |
| 附件可用 | 收到、关联、有实际编号 / 缺编号 | true / false | true / false |
| 失效流水 | expired / valid | true / false | true / false |
| 股权路径 | 0.6 单路径 | 0.6 | 0.6 |
| 图循环 | 含循环 | UNKNOWN | UNKNOWN |
| 缺证路径 | 终止信息 UNKNOWN | BLOCKED | BLOCKED（约束缺证） |
| 记录约束 | 双重权利人 / 目标身份不一致 | BLOCKED | BLOCKED |

状态迁移也分别验证了查询发送的 `APPLIED`、未知守卫的 `BLOCKED`、附件反馈满足关联条件的 `APPLIED`。模型修订后，尚未收到附件反馈时的可选关联字段未知不会误阻塞状态迁移；真正收到反馈但关联不一致仍由约束阻断。

## 验证边界

- 86 个业务案例已完整保留原始输入、应有结果和禁止结果，但尚未逐案执行；它们在 `output.json` 中仍是 `NOT_EXECUTED`。
- 形成日期、人工裁定、国企性质认定和开放事项需要业务/合规人员审查，不能仅凭本地求值器结论关闭。
- 路径计算要求调用方先证明图范围完整、时点一致；循环图和未知边不会被当作零值。
- 约束会在求值和状态迁移前检查 Ref 记录，违反约束或缺少 `BLOCK` 级证据时返回 `BLOCKED`。
- 重复反馈与附件关联约束只在对应事件已明确发生时要求原请求/传输关联，避免把普通处理中记录误判为违规。

## 当前结论

本地关键边界验证通过；全量语义审查、86 案例执行、业务确认和平台运行仍未完成。模型继续保持 DRAFT/PENDING。
