# A01 形成日期与差异闭环 DSL 聚焦草案 领域模型审查稿

- DSL：1.0.0
- 资产：A01.DomainModel.DslPreview / 0.1.0
- 知识依据：DRAFT，A01.DomainKnowledge / 2.1.0

> 本文由同一 DSL 生成，用于业务审阅；不是业务批准、平台发布、运行记录或结论。

## 范围与未知

UNKNOWN 表示缺证或无法确定，不等于 false 或 0。只有条件为 true 才计算允许迁移；BLOCKED 不会实际更改业务状态。

承接问题：K.Q.11.HISTORY、K.Q.19.CLOSE

## 类型与属性

### 差异事项（TASK，M.Difference）

差异事项

身份：id

| 属性 | 字段 | 类型 | 基数 | 业务含义 |
| --- | --- | --- | --- | --- |
| 系统复核一致 | consistent | Boolean | 0..1 | 系统复核一致 |
| 客户已实际更正 | corrected | Boolean | 0..1 | 客户已实际更正 |
| 实际更正证据 | correction_evidence | Text | 0..1 | 实际更正证据 |
| 业务身份标识 | id | Text | 1..1 | 业务身份标识 |
| 系统复核证据 | recheck_evidence | Text | 0..1 | 系统复核证据 |
| 处置状态 | state | Enum | 1..1 | 处置状态 |

正例：有对应业务证据的记录

反例：缺证时臆造身份或把推测写成事实

### 自然人（ENTITY，M.Person）

自然人

身份：id

| 属性 | 字段 | 类型 | 基数 | 业务含义 |
| --- | --- | --- | --- | --- |
| 业务身份标识 | id | Text | 1..1 | 业务身份标识 |

正例：有对应业务证据的记录

反例：缺证时臆造身份或把推测写成事实

### 资格有效区间（FACT，M.Qualification）

资格有效区间

身份：id

| 属性 | 字段 | 类型 | 基数 | 业务含义 |
| --- | --- | --- | --- | --- |
| 达标关系类型 | basis_kind | Enum | 1..1 | 达标关系类型 |
| 本区间终止日期 | end | Date | 0..1 | 本区间终止日期 |
| 终止信息状态 | end_status | Enum | 1..1 | 终止信息状态 |
| 生效依据摘要 | evidence | Text | 1..1 | 生效依据摘要 |
| 业务身份标识 | id | Text | 1..1 | 业务身份标识 |
| 资格所属自然人 | person | Ref → M.Person | 1..1 | 资格所属自然人 |
| 本区间生效日期 | start | Date | 1..1 | 本区间生效日期 |

正例：有对应业务证据的记录

反例：缺证时臆造身份或把推测写成事实

## 时间语义

区间采用 [起点, 终点)；OPEN 是已知尚未终止，UNKNOWN 是终止信息不明，不能把空终点一律视作永久有效。

| ID | 对象 | 起点 | 终点 | 终止状态 |
| --- | --- | --- | --- | --- |
| M.Interval | M.Qualification | start | end | end_status |

## 判断规则

### 是否具备闭环条件（M.CanResolve）

实际更正与系统复核一致须同时成立；布尔事实必须有外部证据支持。

输入：corrected:Boolean、consistent:Boolean

结果：Boolean

逻辑：(corrected 且 consistent)

未知处理：传播为 UNKNOWN。

### 当前形成日期（M.CurrentFormation）

取最近一次包含核对时点的连续达标区间起点；完整历史与连续性未核实返回未知。

输入：intervals:IntervalSet、as_of:Date、history_complete:Boolean、continuity_verified:Boolean

结果：Date

逻辑：当前连续区间起点(intervals，as_of，history_complete，continuity_verified)

未知处理：传播为 UNKNOWN。

## 状态变化

### M.DifferenceFlow（M.Difference）

初始状态：PENDING；状态字段：state。

| 迁移 | 原状态 | 事件 | 目标状态 | 守卫条件 |
| --- | --- | --- | --- | --- |
| M.Resolve | PENDING | RECHECK | RESOLVED | (self.corrected 且 self.consistent) |

## 人工判断

本模型没有人工判断节点。

## 覆盖与待确认

| 问题 | 状态 | 理由 |
| --- | --- | --- |
| K.Q.11.HISTORY | PARTIAL | 本示例计算当前日期；尚未形式化回访展示、完整证据核验及跨类型事件的全部语义。 |
| K.Q.19.CLOSE | PARTIAL | 本示例只判断及计算状态迁移；证据真实性核验、历史记录留存和实际业务写入仍由业务流程负责。 |

案例与开放缺口详见 coverage.md。

## 业务案例与未完成部分

### K.C.PILOT.07（BLOCKED）

日期计算或状态迁移可用示例求值；完整回访、证据与历史留存尚未全部形式化，整例保持 BLOCKED。

应有结果：当前形成日期为2024年6月2日；回访同时展示2019年形成、2021年终止事件、中断及本次重新形成。

禁止结果：不得删去历史中断，或将当前形成日期写成2019年3月1日。

### K.C.PILOT.08（BLOCKED）

日期计算或状态迁移可用示例求值；完整回访、证据与历史留存尚未全部形式化，整例保持 BLOCKED。

应有结果：保留各关系类型事件并补控制协议生效时间；核实整体连续后沿用原总体形成日期。

禁止结果：不得在缺生效证据时宣布连续或中断；不得因类型变化本身重置总体形成日期。

### K.C.PILOT.13（BLOCKED）

日期计算或状态迁移可用示例求值；完整回访、证据与历史留存尚未全部形式化，整例保持 BLOCKED。

应有结果：将该差异标为已解决，保留更正、查询复核和既有处置记录。

禁止结果：不得抹去历史，也不得从闭环状态推断其他法定记录义务消失。

### K.C.PILOT.14（BLOCKED）

日期计算或状态迁移可用示例求值；完整回访、证据与历史留存尚未全部形式化，整例保持 BLOCKED。

应有结果：保留待复核或待处理。

禁止结果：不得标为已解决。

### K.C.REVIEW.TYPE_CONTINUITY（BLOCKED）

日期计算或状态迁移可用示例求值；完整回访、证据与历史留存尚未全部形式化，整例保持 BLOCKED。

应有结果：总体形成日期沿用2024年5月1日，股权类型终止与控制类型形成分别记2026年6月1日。

禁止结果：不得把总体日期重置为类型切换日；不得将本轮口径称为制度原文直接规定。
