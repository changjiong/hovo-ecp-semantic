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
- 结构采集时间：2026-09-29T01:19:20.734Z
- 已勾选表：13

## ubo_mvp_standardized.std_benefit_right_relation

- 类型：TABLE
- 中文说明：收益权关系
- 主键：`benefit_relation_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `benefit_relation_id` | 收益权关系ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 2 | `target_subject_id` | 目标主体ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 3 | `target_subject_name` | 目标主体名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 4 | `beneficiary_party_type_code` | 收益权人类型 | `varchar` | `varchar(16)` | 否 | length=16 |
| 5 | `beneficiary_party_id` | 收益权人ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 6 | `beneficiary_party_name` | 收益人名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 7 | `benefit_ratio` | 收益权比例 | `decimal` | `decimal(12,8)` | 是 | precision=12, scale=8 |
| 8 | `benefit_type_code` | 收益权类型 | `varchar` | `varchar(64)` | 是 | length=64 |
| 9 | `basis_description` | 收益权依据说明 | `text` | `text` | 是 | length=65535 |
| 10 | `agreement_or_document_ref` | 协议/文件引用 | `varchar` | `varchar(1024)` | 是 | length=1024 |
| 11 | `valid_from` | 权利生效时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 12 | `valid_to` | 权利终止时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 13 | `source_type_code` | 来源类型（SOURCE_TYPE） | `varchar` | `varchar(32)` | 是 | length=32 |

### 唯一键与索引

未声明。

### 外键

未声明。

## ubo_mvp_standardized.std_branch_relation

- 类型：TABLE
- 中文说明：分支机构关系
- 主键：`branch_relation_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `branch_relation_id` | 分支关系ID | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 2 | `branch_subject_id` | 分支机构主体ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 3 | `branch_subject_name` | 分支机构主体名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 4 | `parent_subject_id` | 上级主体ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 5 | `parent_subject_name` | 上级主体名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 6 | `branch_region_code` | 境内/境外 | `varchar` | `varchar(16)` | 是 | length=16 |
| 7 | `branch_level` | 分支层级 | `int` | `int(11)` | 是 | precision=11, scale=0 |
| 8 | `valid_from` | 归属关系生效时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 9 | `valid_to` | 归属关系终止时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |

### 唯一键与索引

未声明。

### 外键

未声明。

## ubo_mvp_standardized.std_change_record

- 类型：TABLE
- 中文说明：变更记录
- 主键：`change_record_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `change_record_id` | 变更记录ID | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 2 | `subject_id` | 主体ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 3 | `subject_name` | 主体名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 4 | `change_date` | 变更日期 | `date` | `date` | 否 | - |
| 5 | `change_item_code` | 变更项目 | `varchar` | `varchar(64)` | 否 | length=64 |
| 6 | `change_type_code` | 变更类型 | `varchar` | `varchar(32)` | 否 | length=32 |
| 7 | `related_party_type_code` | 关联对象类型 | `varchar` | `varchar(16)` | 否 | length=16 |
| 8 | `related_party_name_snapshot` | 关联对象名称快照 | `varchar` | `varchar(512)` | 否 | length=512 |
| 9 | `before_party_text` | 未提供 | `varchar` | `varchar(512)` | 是 | length=512 |
| 10 | `after_party_text` | 未提供 | `varchar` | `varchar(512)` | 是 | length=512 |
| 11 | `before_value_num` | 变更前数值 | `decimal` | `decimal(22,8)` | 是 | precision=22, scale=8 |
| 12 | `after_value_num` | 变更后数值 | `decimal` | `decimal(22,8)` | 是 | precision=22, scale=8 |
| 13 | `before_value_text` | 变更原始前文本值 | `text` | `text` | 是 | length=65535 |
| 14 | `after_value_text` | 变更原始后文本值 | `text` | `text` | 是 | length=65535 |
| 15 | `parse_confidence_score` | 解析可信度 | `varchar` | `varchar(16)` | 是 | length=16 |

### 唯一键与索引

未声明。

### 外键

未声明。

## ubo_mvp_standardized.std_control_relation

- 类型：TABLE
- 中文说明：控制关系表
- 主键：`control_relation_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `control_relation_id` | 控制关系ID-自增 | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 2 | `target_subject_id` | 被控制主体ID-稳定序号 | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 3 | `target_subject_name` | 被控制主体名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 4 | `controller_party_type_code` | 控制方类型 PERSON/SUBJECT | `varchar` | `varchar(16)` | 否 | length=16 |
| 5 | `controller_party_id` | 控制方ID-稳定序号(同控制方同ID) | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 6 | `controller_party_name` | 控制方名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 7 | `control_type_code` | 控制方式 | `varchar` | `varchar(64)` | 否 | length=64 |
| 8 | `control_description` | 控制关系说明 | `text` | `text` | 是 | length=65535 |
| 9 | `joint_control_flag` | 是否共同控制 | `tinyint` | `tinyint(1)` | 是 | precision=1, scale=0 |
| 10 | `related_party_group_id` | 一致行动/关系密切组ID-稳定序号 | `bigint` | `bigint(20)` | 是 | precision=20, scale=0 |
| 11 | `agreement_or_document_ref` | 控制协议/文件引用 | `varchar` | `varchar(1024)` | 是 | length=1024 |
| 12 | `control_strength_or_scope` | 控制强度/范围说明 | `text` | `text` | 是 | length=65535 |
| 13 | `valid_from` | 生效时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 14 | `valid_to` | 终止时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 15 | `source_type_code` | 来源类型（SOURCE_TYPE） | `varchar` | `varchar(32)` | 是 | length=32 |
| 16 | `is_adopted` | 采用标志：1采用 0不采用 | `tinyint` | `tinyint(1)` | 是 | precision=1, scale=0 |
| 17 | `adoption_source` | 判定来源（ADOPTION_SOURCE：SYSTEM/MANUAL） | `varchar` | `varchar(16)` | 是 | length=16 |
| 18 | `adoption_by` | 人工判定操作人 | `varchar` | `varchar(64)` | 是 | length=64 |
| 19 | `adoption_time` | 人工判定时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 20 | `adoption_reason` | 判定理由 | `text` | `text` | 是 | length=65535 |

### 唯一键与索引

| 名称 | 类型 | 字段 |
|---|---|---|
| idx_control_ctrl | INDEX | `controller_party_name` |
| idx_control_target | INDEX | `target_subject_id` |

### 外键

未声明。

## ubo_mvp_standardized.std_control_third_party

- 类型：TABLE
- 中文说明：未提供
- 主键：-

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `control_relation_id` | 控制关系ID-自增序号 | `varchar` | `varchar(64)` | 否 | length=64 |
| 2 | `target_subject_id` | 被控制主体ID(STD_SUBJECT.subject_id) | `varchar` | `varchar(64)` | 否 | length=64 |
| 3 | `controller_party_id` | 控制方ID-稳定序号 | `varchar` | `varchar(64)` | 否 | length=64 |
| 4 | `controller_party_name` | 控制方名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 5 | `target_subject_name` | 被控制主体名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 6 | `control_type_code` | 控制方式代码(全部OTHER) | `varchar` | `varchar(64)` | 否 | length=64 |
| 7 | `data_source` | 数据来源(水滴) | `varchar` | `varchar(512)` | 是 | length=512 |
| 8 | `retrieve_date` | 获取日期(2026-04-30) | `date` | `date` | 是 | - |

### 唯一键与索引

未声明。

### 外键

未声明。

## ubo_mvp_standardized.std_customer_context

- 类型：TABLE
- 中文说明：银行客户上下文
- 主键：`customer_context_id` + `subject_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `customer_context_id` | 客户上下文ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 2 | `subject_id` | 主体ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 3 | `subject_name` | 主体名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 4 | `bank_customer_id` | 银行客户号 | `varchar` | `varchar(64)` | 否 | length=64 |
| 5 | `institution_code` | 所属机构代码 | `varchar` | `varchar(64)` | 是 | length=64 |
| 6 | `customer_status_code` | 客户状态 | `varchar` | `varchar(32)` | 是 | length=32 |
| 7 | `ubo_enterprise_code` | 未提供 | `varchar` | `varchar(64)` | 是 | length=64 |
| 8 | `aml_risk_level_code` | 反洗钱风险等级 | `varchar` | `varchar(32)` | 是 | length=32 |
| 9 | `risk_assessed_at` | 风险等级评估时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 10 | `kyc_status_code` | 客户尽调状态 | `varchar` | `varchar(32)` | 是 | length=32 |
| 11 | `last_kyc_date` | 最近尽调日期 | `date` | `date` | 是 | - |
| 12 | `business_relationship_from` | 业务关系开始时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 13 | `business_relationship_to` | 业务关系结束时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |

### 唯一键与索引

未声明。

### 外键

未声明。

## ubo_mvp_standardized.std_ownership_relation

- 类型：TABLE
- 中文说明：股权/股份关系
- 主键：`ownership_relation_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `ownership_relation_id` | 所有权关系ID | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 2 | `target_subject_id` | 目标主体ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 3 | `participant_name` | 股东名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 4 | `target_subject_name` | 目标主体名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 5 | `owner_party_type_code` | 持有人类型 | `varchar` | `varchar(16)` | 否 | length=16 |
| 6 | `ownership_type_code` | 权益类型 | `varchar` | `varchar(32)` | 否 | length=32 |
| 7 | `share_count` | 持有股份数 | `bigint` | `bigint(20)` | 是 | precision=20, scale=0 |
| 8 | `direct_ownership_ratio` | 直接持有比例 | `decimal` | `decimal(12,8)` | 是 | precision=12, scale=8 |
| 9 | `subscribed_capital_amount` | 认缴出资额 | `decimal` | `decimal(22,6)` | 是 | precision=22, scale=6 |
| 10 | `subscribed_capital_currency` | 认缴出资币种 | `char` | `char(3)` | 是 | length=3 |
| 11 | `subscribed_capital_date` | 认缴出资日期 | `date` | `date` | 是 | - |
| 12 | `paid_in_capital_amount` | 实缴出资额 | `decimal` | `decimal(22,6)` | 是 | precision=22, scale=6 |
| 13 | `paid_in_capital_currency` | 实缴出资币种 | `char` | `char(3)` | 是 | length=3 |
| 14 | `holding_method_code` | 持有方式 | `varchar` | `varchar(32)` | 是 | length=32 |
| 15 | `valid_from` | 权益生效时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 16 | `valid_to` | 权益终止时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 17 | `source_record_no` | 来源序号 | `bigint` | `bigint(20)` | 是 | precision=20, scale=0 |
| 18 | `source_type_code` | 来源类型（SOURCE_TYPE：BUSINESS_REGISTRY/BANK_INTERNAL/CUSTOMER_DOCUMENT/PUBLIC_DISCLOSURE/THIRD_PARTY_DATA/OTHER） | `varchar` | `varchar(32)` | 是 | length=32 |
| 19 | `is_adopted` | 采用标志：1采用 0不采用 | `tinyint` | `tinyint(1)` | 是 | precision=1, scale=0 |
| 20 | `adoption_source` | 判定来源（ADOPTION_SOURCE：SYSTEM系统自动/MANUAL人工判定） | `varchar` | `varchar(16)` | 是 | length=16 |
| 21 | `adoption_by` | 人工判定操作人 | `varchar` | `varchar(64)` | 是 | length=64 |
| 22 | `adoption_time` | 人工判定时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 23 | `adoption_reason` | 判定理由 | `text` | `text` | 是 | length=65535 |

### 唯一键与索引

未声明。

### 外键

未声明。

## ubo_mvp_standardized.std_partnership_relation

- 类型：TABLE
- 中文说明：合伙权益关系
- 主键：`partnership_relation_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `partnership_relation_id` | 合伙关系ID | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 2 | `partnership_subject_id` | 合伙企业主体ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 3 | `partnership_subject_name` | 合伙企业主体名称 | `varchar` | `varchar(255)` | 否 | length=255 |
| 4 | `partner_party_type_code` | 合伙人类型 | `varchar` | `varchar(16)` | 否 | length=16 |
| 5 | `partner_party_id` | 合伙人ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 6 | `partner_party_name` | 合伙人名称 | `varchar` | `varchar(255)` | 否 | length=255 |
| 7 | `partner_role_code` | 合伙人角色 | `varchar` | `varchar(16)` | 否 | length=16 |
| 8 | `liability_type_code` | 责任承担方式 | `varchar` | `varchar(32)` | 是 | length=32 |
| 9 | `partnership_interest_ratio` | 合伙权益比例 | `decimal` | `decimal(12,8)` | 是 | precision=12, scale=8 |
| 10 | `subscribed_contribution_amount` | 认缴出资额 | `decimal` | `decimal(22,6)` | 是 | precision=22, scale=6 |
| 11 | `contribution_currency` | 出资币种 | `char` | `char(3)` | 是 | length=3 |
| 12 | `contribution_method_code` | 出资方式 | `varchar` | `varchar(32)` | 是 | length=32 |
| 13 | `executive_partner_flag` | 是否执行事务合伙人 | `tinyint` | `tinyint(1)` | 是 | precision=1, scale=0 |
| 14 | `executive_partner_representative_person_id` | 执行事务合伙人委派代表自然人ID | `varchar` | `varchar(64)` | 是 | length=64 |
| 15 | `valid_from` | 合伙权益生效时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 16 | `valid_to` | 合伙权益终止时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |

### 唯一键与索引

未声明。

### 外键

未声明。

## ubo_mvp_standardized.std_person_role_relation

- 类型：TABLE
- 中文说明：人员任职关系
- 主键：`role_relation_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `role_relation_id` | 任职关系ID | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 2 | `subject_id` | 任职主体ID | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 3 | `subject_name` | 主体名称 | `varchar` | `varchar(255)` | 是 | length=255 |
| 4 | `person_name` | 人员名称 | `varchar` | `varchar(64)` | 是 | length=64 |
| 5 | `role_type_code` | 角色类型 | `varchar` | `varchar(64)` | 否 | length=64 |
| 6 | `role_title` | 原始职务名称 | `varchar` | `varchar(255)` | 是 | length=255 |
| 7 | `appointment_method_code` | 产生/任命方式 | `varchar` | `varchar(64)` | 是 | length=64 |
| 8 | `decision_power_description` | 职务决策权限描述 | `text` | `text` | 是 | length=65535 |
| 9 | `valid_from` | 任职生效时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 10 | `valid_to` | 任职终止时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 11 | `current_flag` | 当前有效标志 | `tinyint` | `tinyint(1)` | 是 | precision=1, scale=0 |
| 12 | `source_type_code` | 来源类型（SOURCE_TYPE） | `varchar` | `varchar(32)` | 是 | length=32 |

### 唯一键与索引

未声明。

### 外键

未声明。

## ubo_mvp_standardized.std_record_regulatory_policy_documents

- 类型：TABLE
- 中文说明：监管政策文件
- 主键：`policy_documents_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `policy_documents_id` | 政策文件ID | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 2 | `Document_No` | 文号 | `varchar` | `varchar(512)` | 是 | length=512 |
| 3 | `policy_name` | 政策名称 | `varchar` | `varchar(512)` | 是 | length=512 |
| 4 | `Issuing_Authority` | 发布机构 | `varchar` | `varchar(512)` | 是 | length=512 |
| 5 | `Issue_Date` | 发布日期 | `date` | `date` | 是 | - |
| 6 | `Effective_Date` | 生效日期 | `date` | `date` | 是 | - |
| 7 | `Expiration_Date` | 失效日期（有效时9999-12-31） | `date` | `date` | 是 | - |
| 8 | `Full_Text_Link` | 全文链接 | `varchar` | `varchar(256)` | 是 | length=256 |
| 9 | `Brief_Description` | 简要说明 | `text` | `text` | 是 | length=65535 |

### 唯一键与索引

未声明。

### 外键

未声明。

## ubo_mvp_standardized.std_subject

- 类型：TABLE
- 中文说明：主体基本信息
- 主键：`subject_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `subject_id` | 未提供 | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 2 | `subject_type_code` | 主体类型 | `varchar` | `varchar(32)` | 否 | length=32 |
| 3 | `subject_name` | 主体名称 | `varchar` | `varchar(512)` | 否 | length=512 |
| 4 | `unified_social_credit_code` | 统一社会信用代码 | `varchar` | `varchar(64)` | 是 | length=64 |
| 5 | `registration_number` | 其他登记/注册号 | `varchar` | `varchar(128)` | 是 | length=128 |
| 6 | `registration_country_code` | 登记国家/地区 | `char` | `char(2)` | 是 | length=2 |
| 7 | `registration_authority` | 登记机关 | `varchar` | `varchar(255)` | 是 | length=255 |
| 8 | `registration_status_code` | 登记状态 | `varchar` | `varchar(32)` | 是 | length=32 |
| 9 | `enterprise_type` | 企业类型 | `varchar` | `varchar(255)` | 是 | length=255 |
| 10 | `legal_form_code` | 法律形式 | `varchar` | `varchar(64)` | 是 | length=64 |
| 11 | `organization_nature_code` | 组织性质 | `varchar` | `varchar(64)` | 是 | length=64 |
| 12 | `ownership_nature_code` | 所有制性质 | `varchar` | `varchar(64)` | 是 | length=64 |
| 13 | `listing_status_code` | 上市状态 | `varchar` | `varchar(32)` | 是 | length=32 |
| 14 | `ubo_enterprise_code` | 未提供 | `varchar` | `varchar(64)` | 是 | length=64 |
| 15 | `stock_code` | 证券代码 | `varchar` | `varchar(32)` | 是 | length=32 |
| 16 | `establishment_date` | 成立日期 | `date` | `date` | 是 | - |
| 17 | `registered_capital_amount` | 注册资本金额 | `decimal` | `decimal(22,6)` | 是 | precision=22, scale=6 |
| 18 | `registered_capital_currency` | 注册资本币种 | `char` | `char(3)` | 是 | length=3 |
| 19 | `paid_in_capital_amount` | 实缴资本金额 | `decimal` | `decimal(22,6)` | 是 | precision=22, scale=6 |
| 20 | `paid_in_capital_currency` | 实缴资本币种 | `char` | `char(3)` | 是 | length=3 |
| 21 | `business_term_from` | 营业期限自 | `date` | `date` | 是 | - |
| 22 | `business_term_to` | 营业期限至 | `date` | `date` | 是 | - |
| 23 | `no_fixed_term_flag` | 无固定期限标志 | `tinyint` | `tinyint(1)` | 是 | precision=1, scale=0 |
| 24 | `registered_address` | 注册地址 | `varchar` | `varchar(1024)` | 是 | length=1024 |
| 25 | `mailing_address` | 通信地址 | `varchar` | `varchar(1024)` | 是 | length=1024 |
| 26 | `former_names` | 曾用名 | `text` | `text` | 是 | length=65535 |
| 27 | `english_name` | 英文名称 | `varchar` | `varchar(512)` | 是 | length=512 |
| 28 | `enterprise_scale_code` | 企业规模 | `varchar` | `varchar(32)` | 是 | length=32 |
| 29 | `industry_sector_code` | 未提供 | `varchar` | `varchar(64)` | 是 | length=64 |
| 30 | `industry_major_code` | 未提供 | `varchar` | `varchar(64)` | 是 | length=64 |
| 31 | `industry_medium_code` | 未提供 | `varchar` | `varchar(64)` | 是 | length=64 |
| 32 | `industry_minor_code` | 未提供 | `varchar` | `varchar(64)` | 是 | length=64 |
| 33 | `business_scope` | 经营范围 | `text` | `text` | 是 | length=65535 |
| 34 | `company_profile` | 主体简介 | `text` | `text` | 是 | length=65535 |
| 35 | `official_website` | 官方网站 | `varchar` | `varchar(512)` | 是 | length=512 |
| 36 | `taxpayer_qualification` | 纳税人资质 | `varchar` | `varchar(64)` | 是 | length=64 |
| 37 | `legal_representative` | 未提供 | `varchar` | `varchar(128)` | 是 | length=128 |

### 唯一键与索引

未声明。

### 外键

未声明。

## ubo_mvp_standardized.std_ubo_para_info

- 类型：TABLE
- 中文说明：UBO识别参数表
- 主键：`param_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `param_id` | 参数ID | `bigint` | `bigint(20)` | 否 | precision=20, scale=0 |
| 2 | `param_code` | 参数代码 | `varchar` | `varchar(64)` | 否 | length=64 |
| 3 | `param_name` | 参数名称 | `varchar` | `varchar(128)` | 否 | length=128 |
| 4 | `param_type_code` | 参数类型（代码集param_type：THRESHOLD阈值/SWITCH开关/SEQUENCE序列/ENUM枚举） | `varchar` | `varchar(32)` | 否 | length=32 |
| 5 | `param_value` | 参数值（统一文本存储） | `varchar` | `varchar(256)` | 否 | length=256 |
| 6 | `para_description` | 参数描述 | `varchar` | `varchar(512)` | 是 | length=512 |
| 7 | `legal_basis` | 法规依据 | `varchar` | `varchar(256)` | 是 | length=256 |
| 8 | `policy_documents_id` | 政策文件ID（逻辑外键→STD_RECORD_REGULATORY_POLICY_DOCUMENTS） | `bigint` | `bigint(20)` | 是 | precision=20, scale=0 |
| 9 | `valid_from` | 生效日期 | `date` | `date` | 否 | - |
| 10 | `valid_to` | 失效日期（有效时9999-12-31） | `date` | `date` | 否 | - |
| 11 | `created_at` | 创建时间 | `datetime` | `datetime` | 是 | datetime precision=0 |
| 12 | `updated_at` | 更新时间 | `datetime` | `datetime` | 是 | datetime precision=0 |

### 唯一键与索引

| 名称 | 类型 | 字段 |
|---|---|---|
| uk_param_version | UNIQUE KEY | `param_code` + `valid_from` |
| idx_param_policy | INDEX | `policy_documents_id` |
| idx_param_valid | INDEX | `valid_from` + `valid_to` |
| uk_param_version | UNIQUE INDEX | `param_code` + `valid_from` |

### 外键

| 名称 | 本表字段 | 引用表 | 引用字段 |
|---|---|---|---|
| fk_ubo_para_policy_documents | `policy_documents_id` | `ubo_mvp_standardized.std_record_regulatory_policy_documents` | `policy_documents_id` |

## ubo_mvp_standardized.std_voting_right_relation

- 类型：TABLE
- 中文说明：表决权关系
- 主键：`voting_relation_id`

### 字段

| 顺序 | 字段名 | 中文说明 | 数据类型 | 原生类型 | 可空 | 长度 / 精度 |
|---:|---|---|---|---|---|---|
| 1 | `voting_relation_id` | 表决权关系ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 2 | `target_subject_id` | 目标主体ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 3 | `target_subject_name` | 目标主体名称 | `varchar` | `varchar(522)` | 否 | length=522 |
| 4 | `holder_party_type_code` | 表决权人类型 | `varchar` | `varchar(16)` | 否 | length=16 |
| 5 | `holder_party_id` | 表决权人ID | `varchar` | `varchar(64)` | 否 | length=64 |
| 6 | `holder_party_name` | 表决权人名称 | `varchar` | `varchar(522)` | 否 | length=522 |
| 7 | `voting_ratio` | 表决权比例 | `decimal` | `decimal(12,8)` | 是 | precision=12, scale=8 |
| 8 | `voting_basis_code` | 表决权依据 | `varchar` | `varchar(64)` | 是 | length=64 |
| 9 | `basis_description` | 表决权依据说明 | `text` | `text` | 是 | length=65535 |
| 10 | `agreement_or_document_ref` | 协议/文件引用 | `varchar` | `varchar(1024)` | 是 | length=1024 |
| 11 | `valid_from` | 权利生效时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 12 | `valid_to` | 权利终止时间 | `datetime` | `datetime(6)` | 是 | datetime precision=6 |
| 13 | `source_type_code` | 来源类型（SOURCE_TYPE） | `varchar` | `varchar(32)` | 是 | length=32 |

### 唯一键与索引

未声明。

### 外键

未声明。
