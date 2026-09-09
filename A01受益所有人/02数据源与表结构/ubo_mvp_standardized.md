# A01 UBO 远端标准化源 数据源表说明

> 本文档仅包含 Hovo 公开数据源标识和已勾选表的结构，不包含连接地址、账号、凭据或业务数据。

## 数据源

- 数据源 ID：`ds_ubo_mvp_standardized`
- 名称：A01 UBO 远端标准化源
- Code：`ubo_mvp_standardized`
- 环境：`test`
- 类型：`oceanbase_mysql`
- 状态：`enabled`
- 优先级：90
- 默认 Schema：ubo_mvp_standardized
- 结构采集时间：2026-09-09T04:52:57.015Z
- 已勾选表：7

## ubo_mvp_standardized.company

- 类型：TABLE
- 中文说明：hovo-ubo-standardization-v1 | 企业基本信息：规范化名称合并后的企业主表
- 主键：`id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `id` | 标准企业主键；取兼容同名源记录的最小ID | `bigint` | `bigint(20) unsigned` | 否 | precision=20, scale=0 |
| 2 | `company_name` | 企业名称；经NFC及首尾空白规范化，当前按名称关联 | `varchar` | `varchar(512)` | 否 | length=512 |
| 3 | `unified_social_credit_code` | 统一社会信用代码；大写保存，缺失不代表企业无代码 | `varchar` | `varchar(64)` | 是 | length=64 |
| 4 | `registration_status` | 企业登记状态；保留来源口径 | `varchar` | `varchar(64)` | 是 | length=64 |
| 5 | `legal_representative` | 法定代表人姓名；不等同于实际控制人 | `varchar` | `varchar(255)` | 是 | length=255 |
| 6 | `enterprise_type` | 企业类型；保留来源分类文本 | `varchar` | `varchar(255)` | 是 | length=255 |
| 7 | `establishment_date` | 企业成立日期 | `date` | `date` | 是 | - |

### 唯一键与索引

| 名称 | 类型 | 字段 |
|---|---|---|
| uk_company_credit | UNIQUE KEY | `unified_social_credit_code` |
| uk_company_name | UNIQUE KEY | `company_name` |
| uk_company_credit | UNIQUE INDEX | `unified_social_credit_code` |
| uk_company_name | UNIQUE INDEX | `company_name` |

### 外键

未声明。

## ubo_mvp_standardized.company_change

- 类型：TABLE
- 中文说明：hovo-ubo-standardization-v1 | 企业变更记录：保留变更前后原文及校验摘要
- 主键：`id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `id` | 变更记录主键；去重后保留的源记录ID | `bigint` | `bigint(20) unsigned` | 否 | precision=20, scale=0 |
| 2 | `company_id` | 发生变更的企业ID；关联company.id | `bigint` | `bigint(20) unsigned` | 否 | precision=20, scale=0 |
| 3 | `change_date` | 来源记录的变更日期；不自动等同于控制关系形成日期 | `date` | `date` | 是 | - |
| 4 | `change_item` | 变更项目或事项名称 | `varchar` | `varchar(512)` | 是 | length=512 |
| 5 | `content_before_digest` | 变更前原文的SHA-256十六进制摘要；用于校验和去重，不是内容概述 | `char` | `char(64)` | 是 | length=64 |
| 6 | `content_after_digest` | 变更后原文的SHA-256十六进制摘要；用于校验和去重，不是内容概述 | `char` | `char(64)` | 是 | length=64 |
| 7 | `data_source` | 变更记录的数据来源标识或文本 | `varchar` | `varchar(128)` | 是 | length=128 |
| 8 | `content_before` | 变更前完整原文；不以摘要替代 | `text` | `text` | 是 | length=65535 |
| 9 | `content_after` | 变更后完整原文；不以摘要替代 | `text` | `text` | 是 | length=65535 |

### 唯一键与索引

| 名称 | 类型 | 字段 |
|---|---|---|
| company_id | INDEX | `company_id` |

### 外键

| 名称 | 本表字段 | 引用表 | 引用字段 |
|---|---|---|---|
| company_change_ibfk_1 | `company_id` | `ubo_mvp_standardized.company` | `id` |

## ubo_mvp_standardized.controller_edge

- 类型：TABLE
- 中文说明：hovo-ubo-standardization-v1 | 来源实际控制人路径边：外部报告线索，不是平台最终认定
- 主键：`id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `id` | 控制路径边记录主键；去重后保留的源记录ID | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 2 | `company_id` | 被分析企业ID；关联company.id | `bigint` | `bigint(20) unsigned` | 否 | precision=20, scale=0 |
| 3 | `ac_id` | 来源报告的实际控制主体标识 | `varchar` | `varchar(64)` | 是 | length=64 |
| 4 | `ac_name` | 来源报告的实际控制主体名称或姓名；属于来源结论线索 | `varchar` | `varchar(512)` | 是 | length=512 |
| 5 | `is_personal` | 来源报告的控制主体是否为自然人标记；保留来源编码 | `tinyint` | `tinyint(4)` | 是 | precision=4, scale=0 |
| 6 | `vote_percent` | 来源报告的表决权比例原文本；未在此字段统一数值化 | `varchar` | `varchar(32)` | 是 | length=32 |
| 7 | `beneficia_proportion` | 来源报告的受益比例原文本；保留来源字段拼写及口径 | `varchar` | `varchar(64)` | 是 | length=64 |
| 8 | `path_seq` | 来源控制路径序号 | `int` | `int(11)` | 否 | precision=11, scale=0 |
| 9 | `edge_seq` | 来源路径内边序号 | `int` | `int(11)` | 否 | precision=11, scale=0 |
| 10 | `start_name` | 路径边起点主体名称或姓名 | `varchar` | `varchar(512)` | 是 | length=512 |
| 11 | `start_node_id` | 来源路径边起点节点标识 | `varchar` | `varchar(64)` | 是 | length=64 |
| 12 | `start_node_type` | 来源路径边起点节点类型编码 | `varchar` | `varchar(16)` | 是 | length=16 |
| 13 | `end_name` | 路径边终点主体名称或姓名 | `varchar` | `varchar(512)` | 是 | length=512 |
| 14 | `end_node_id` | 来源路径边终点节点标识 | `varchar` | `varchar(64)` | 是 | length=64 |
| 15 | `end_node_type` | 来源路径边终点节点类型编码 | `varchar` | `varchar(16)` | 是 | length=16 |
| 16 | `edge_type` | 来源路径边的关系类型编码 | `varchar` | `varchar(32)` | 是 | length=32 |
| 17 | `proportion` | 来源路径边比例原文本 | `varchar` | `varchar(32)` | 是 | length=32 |
| 18 | `proportion_value` | 来源路径边比例数值；按既有0至100范围校验，不据此独立认定控制 | `decimal` | `decimal(12,8)` | 是 | precision=12, scale=8 |
| 19 | `ratio_quality` | proportion_value质量：VALID有效、MISSING缺失、OUT_OF_RANGE越界 | `varchar` | `varchar(24)` | 否 | length=24 |

### 唯一键与索引

| 名称 | 类型 | 字段 |
|---|---|---|
| company_id | INDEX | `company_id` |

### 外键

| 名称 | 本表字段 | 引用表 | 引用字段 |
|---|---|---|---|
| controller_edge_ibfk_1 | `company_id` | `ubo_mvp_standardized.company` | `id` |

## ubo_mvp_standardized.executive

- 类型：TABLE
- 中文说明：hovo-ubo-standardization-v1 | 企业高管任职记录：人员及其在企业中的职务
- 主键：`id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `id` | 任职记录主键；去重后保留的源记录ID | `bigint` | `bigint(20) unsigned` | 否 | precision=20, scale=0 |
| 2 | `company_id` | 任职企业ID；关联company.id | `bigint` | `bigint(20) unsigned` | 否 | precision=20, scale=0 |
| 3 | `person_name` | 人员姓名；不作为跨企业自然人唯一身份 | `varchar` | `varchar(255)` | 是 | length=255 |
| 4 | `gender` | 性别；保留来源文本 | `varchar` | `varchar(16)` | 是 | length=16 |
| 5 | `position` | 任职职务；保留来源文本 | `varchar` | `varchar(512)` | 是 | length=512 |

### 唯一键与索引

| 名称 | 类型 | 字段 |
|---|---|---|
| company_id | INDEX | `company_id` |

### 外键

| 名称 | 本表字段 | 引用表 | 引用字段 |
|---|---|---|---|
| executive_ibfk_1 | `company_id` | `ubo_mvp_standardized.company` | `id` |

## ubo_mvp_standardized.penetration

- 类型：TABLE
- 中文说明：hovo-ubo-standardization-v1 | 来源股权穿透链路：同时保留链路比例和对根企业的穿透比例
- 主键：`id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `id` | 穿透记录主键；去重后保留的源记录ID | `bigint` | `bigint(20) unsigned` | 否 | precision=20, scale=0 |
| 2 | `root_company_id` | 穿透分析的根企业ID；关联company.id | `bigint` | `bigint(20) unsigned` | 否 | precision=20, scale=0 |
| 3 | `target_company_id` | 当前链路被持股企业ID；关联company.id | `bigint` | `bigint(20) unsigned` | 否 | precision=20, scale=0 |
| 4 | `owner_company_id` | 股东对应企业ID；关联company.id，未匹配时为空 | `bigint` | `bigint(20) unsigned` | 是 | precision=20, scale=0 |
| 5 | `shareholder_name` | 当前链路股东名称或姓名 | `varchar` | `varchar(512)` | 否 | length=512 |
| 6 | `shareholding_ratio` | 当前股东对当前目标企业的链路持股比例；0至100百分点，不是对根企业的累计比例 | `decimal` | `decimal(10,6)` | 是 | precision=10, scale=6 |
| 7 | `level` | 来源报告的穿透层级；从1开始 | `int` | `int(11)` | 否 | precision=11, scale=0 |
| 8 | `shareholder_id` | 关联的标准股东记录ID；指向shareholder.id，无法唯一确认时为空 | `bigint` | `bigint(20) unsigned` | 是 | precision=20, scale=0 |
| 9 | `is_terminal` | 来源终端节点标记：1是、0否；不自动表示已满足最终识别条件 | `tinyint` | `tinyint(4)` | 否 | precision=4, scale=0 |
| 10 | `ratio_quality` | 原shareholding_ratio质量；不描述新增equity_ratio的质量 | `varchar` | `varchar(24)` | 否 | length=24 |
| 11 | `equity_ratio` | 来源报告的股东对根企业穿透股权比例；0至100百分点，NULL未知；不替代shareholding_ratio，不自动多路径求和 | `decimal` | `decimal(12,8)` | 是 | precision=12, scale=8 |

### 唯一键与索引

| 名称 | 类型 | 字段 |
|---|---|---|
| owner_company_id | INDEX | `owner_company_id` |
| root_company_id | INDEX | `root_company_id` |
| shareholder_id | INDEX | `shareholder_id` |
| target_company_id | INDEX | `target_company_id` |

### 外键

| 名称 | 本表字段 | 引用表 | 引用字段 |
|---|---|---|---|
| penetration_ibfk_1 | `root_company_id` | `ubo_mvp_standardized.company` | `id` |
| penetration_ibfk_2 | `target_company_id` | `ubo_mvp_standardized.company` | `id` |
| penetration_ibfk_3 | `owner_company_id` | `ubo_mvp_standardized.company` | `id` |
| penetration_ibfk_4 | `shareholder_id` | `ubo_mvp_standardized.shareholder` | `id` |

## ubo_mvp_standardized.shareholder

- 类型：TABLE
- 中文说明：hovo-ubo-standardization-v1 | 股东及认缴出资记录：企业与股东的权益关系
- 主键：`id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `id` | 股东记录主键；去重后保留的源记录ID | `bigint` | `bigint(20) unsigned` | 否 | precision=20, scale=0 |
| 2 | `company_id` | 被投资企业ID；关联company.id | `bigint` | `bigint(20) unsigned` | 否 | precision=20, scale=0 |
| 3 | `owner_company_id` | 股东对应的企业ID；关联company.id，未匹配或非企业股东时为空 | `bigint` | `bigint(20) unsigned` | 是 | precision=20, scale=0 |
| 4 | `participant_name` | 股东名称或姓名；姓名本身不是自然人唯一身份 | `varchar` | `varchar(512)` | 是 | length=512 |
| 5 | `participant_type` | 股东主体类型；保留来源分类 | `varchar` | `varchar(128)` | 是 | length=128 |
| 6 | `share_type` | 股份或权益类别；保留来源文本 | `varchar` | `varchar(128)` | 是 | length=128 |
| 7 | `share_count` | 股份数量；单位沿用来源口径 | `bigint` | `bigint(20)` | 是 | precision=20, scale=0 |
| 8 | `subscribed_capital_value` | 认缴出资金额；金额单位沿用来源口径，结合币种读取 | `decimal` | `decimal(22,6)` | 是 | precision=22, scale=6 |
| 9 | `subscribed_capital_currency` | 认缴出资币种；保留来源代码或文本 | `varchar` | `varchar(8)` | 是 | length=8 |
| 10 | `subscribed_capital_date` | 认缴出资日期 | `date` | `date` | 是 | - |
| 11 | `subscribed_share_ratio` | 认缴出资比例；0至100百分点，30表示30% | `decimal` | `decimal(10,6)` | 是 | precision=10, scale=6 |
| 12 | `ratio_quality` | 认缴比例质量：VALID有效、MISSING缺失、OUT_OF_RANGE越界；原型仅装载有效记录 | `varchar` | `varchar(24)` | 否 | length=24 |

### 唯一键与索引

| 名称 | 类型 | 字段 |
|---|---|---|
| company_id | INDEX | `company_id` |
| owner_company_id | INDEX | `owner_company_id` |

### 外键

| 名称 | 本表字段 | 引用表 | 引用字段 |
|---|---|---|---|
| shareholder_ibfk_1 | `company_id` | `ubo_mvp_standardized.company` | `id` |
| shareholder_ibfk_2 | `owner_company_id` | `ubo_mvp_standardized.company` | `id` |

## ubo_mvp_standardized.source_row

- 类型：TABLE
- 中文说明：hovo-ubo-standardization-v1 | ETL来源追踪与隔离记录：逐条记录源数据去向及清洗问题
- 主键：`source_table` + `source_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `source_table` | 原始来源表名；与source_id组成联合主键 | `varchar` | `varchar(64)` | 否 | length=64 |
| 2 | `source_id` | 原始来源记录主键；与source_table共同定位源记录 | `decimal` | `decimal(20,0)` | 否 | precision=20, scale=0 |
| 3 | `standard_table` | 对应标准业务表名；隔离记录为空 | `varchar` | `varchar(64)` | 是 | length=64 |
| 4 | `standard_id` | 对应标准记录主键；多条去重来源可指向同一记录，隔离时为空 | `decimal` | `decimal(20,0)` | 是 | precision=20, scale=0 |
| 5 | `disposition` | 处理去向：LOADED保留、MERGED合并、QUARANTINED隔离；源记录不删除 | `varchar` | `varchar(16)` | 否 | length=16 |
| 6 | `issues_json` | 清洗问题代码数组；一条记录可有多个问题，不能相加作为异常行数 | `json` | `json` | 否 | length=536870911 |
| 7 | `ratio_missing_flag` | 生成标志：issues_json包含RATIO_MISSING时为1；不包含新增EQUITY比例问题 | `tinyint` | `tinyint(4)` | 否 | precision=4, scale=0 |
| 8 | `ratio_out_of_range_flag` | 生成标志：issues_json包含RATIO_OUT_OF_RANGE时为1；不包含新增EQUITY比例问题 | `tinyint` | `tinyint(4)` | 否 | precision=4, scale=0 |

### 唯一键与索引

| 名称 | 类型 | 字段 |
|---|---|---|
| idx_disposition | INDEX | `disposition` |
| idx_standard_row | INDEX | `standard_table` + `standard_id` |

### 外键

未声明。
