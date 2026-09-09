# A01源字段到本体的实际映射

由最终Mapping和随包Schema逐字段展开；业务含义和完整原表注释见 [源结构原文](inputs/source-schema.md)。本表不是live schema发现或实例执行报告。

`a01:`展开为`urn:hovo:ecp:a01-ubo:ontology:`；身份模板及9项FK的精确Join见Mapping。全部源值保持来源含义，不表示已核实现实事实。

| 表.字段 | 原类型 / 可空 | 当前目标IRI或关系 | 值类型 / 空值处理 | 问题 |
| --- | --- | --- | --- | --- |
| `company.id` | bigint unsigned / 否 | a01:sourceRecordId | integer / REJECT | CQ-01/07 |
| `company.company_name` | varchar(512) / 否 | a01:companyName | string / REJECT | CQ-01/07 |
| `company.unified_social_credit_code` | varchar(64) / 是 | a01:unifiedSocialCreditCode | string / OMIT | CQ-01/07 |
| `company.registration_status` | varchar(64) / 是 | a01:registrationStatus | string / OMIT | CQ-01/07 |
| `company.legal_representative` | varchar(255) / 是 | a01:legalRepresentativeName | string / OMIT | CQ-01/07 |
| `company.enterprise_type` | varchar(255) / 是 | a01:enterpriseType | string / OMIT | CQ-01/07 |
| `company.establishment_date` | date / 是 | a01:establishmentDate | date / OMIT | CQ-01/07 |
| `company_change.id` | bigint unsigned / 否 | a01:sourceRecordId | integer / REJECT | CQ-03/04/08 |
| `company_change.company_id` | bigint unsigned / 否 | a01:changeForCompanySourceRecord | IRI关系 / REJECT | CQ-03/04/08 |
| `company_change.change_date` | date / 是 | a01:changeDate | date / OMIT | CQ-03/04/08 |
| `company_change.change_item` | varchar(512) / 是 | a01:changeItem | string / OMIT | CQ-03/04/08 |
| `company_change.content_before_digest` | char(64) / 是 | a01:contentBeforeDigest | string / OMIT | CQ-03/04/08 |
| `company_change.content_after_digest` | char(64) / 是 | a01:contentAfterDigest | string / OMIT | CQ-03/04/08 |
| `company_change.data_source` | varchar(128) / 是 | a01:changeDataSource | string / OMIT | CQ-03/04/08 |
| `company_change.content_before` | text / 是 | a01:contentBefore | string / OMIT | CQ-03/04/08 |
| `company_change.content_after` | text / 是 | a01:contentAfter | string / OMIT | CQ-03/04/08 |
| `controller_edge.id` | bigint / 否 | a01:sourceRecordId | integer / REJECT | CQ-02/07 |
| `controller_edge.company_id` | bigint unsigned / 否 | a01:controllerEdgeForCompanySourceRecord | IRI关系 / REJECT | CQ-02/07 |
| `controller_edge.ac_id` | varchar(64) / 是 | a01:reportedActualControllerId | string / OMIT | CQ-02/07 |
| `controller_edge.ac_name` | varchar(512) / 是 | a01:reportedActualControllerName | string / OMIT | CQ-02/07 |
| `controller_edge.is_personal` | tinyint / 是 | a01:reportedPersonalFlag | integer / OMIT | CQ-02/07 |
| `controller_edge.vote_percent` | varchar(32) / 是 | a01:reportedVotePercentText | string / OMIT | CQ-02/07 |
| `controller_edge.beneficia_proportion` | varchar(64) / 是 | a01:reportedBeneficiaProportionText | string / OMIT | CQ-02/07 |
| `controller_edge.path_seq` | int / 否 | a01:pathSequence | integer / REJECT | CQ-02/07 |
| `controller_edge.edge_seq` | int / 否 | a01:edgeSequence | integer / REJECT | CQ-02/07 |
| `controller_edge.start_name` | varchar(512) / 是 | a01:startName | string / OMIT | CQ-02/07 |
| `controller_edge.start_node_id` | varchar(64) / 是 | a01:startNodeId | string / OMIT | CQ-02/07 |
| `controller_edge.start_node_type` | varchar(16) / 是 | a01:startNodeType | string / OMIT | CQ-02/07 |
| `controller_edge.end_name` | varchar(512) / 是 | a01:endName | string / OMIT | CQ-02/07 |
| `controller_edge.end_node_id` | varchar(64) / 是 | a01:endNodeId | string / OMIT | CQ-02/07 |
| `controller_edge.end_node_type` | varchar(16) / 是 | a01:endNodeType | string / OMIT | CQ-02/07 |
| `controller_edge.edge_type` | varchar(32) / 是 | a01:edgeType | string / OMIT | CQ-02/07 |
| `controller_edge.proportion` | varchar(32) / 是 | a01:reportedProportionText | string / OMIT | CQ-02/07 |
| `controller_edge.proportion_value` | decimal(12,8) / 是 | a01:reportedProportionValue | decimal / OMIT | CQ-02/07 |
| `controller_edge.ratio_quality` | varchar(24) / 否 | a01:ratioQuality | string / REJECT | CQ-02/07 |
| `executive.id` | bigint unsigned / 否 | a01:sourceRecordId | integer / REJECT | CQ-01/02/05 |
| `executive.company_id` | bigint unsigned / 否 | a01:executiveForCompanySourceRecord | IRI关系 / REJECT | CQ-01/02/05 |
| `executive.person_name` | varchar(255) / 是 | a01:personName | string / OMIT | CQ-01/02/05 |
| `executive.gender` | varchar(16) / 是 | a01:gender | string / OMIT | CQ-01/02/05 |
| `executive.position` | varchar(512) / 是 | a01:position | string / OMIT | CQ-01/02/05 |
| `penetration.id` | bigint unsigned / 否 | a01:sourceRecordId | integer / REJECT | CQ-02/07 |
| `penetration.root_company_id` | bigint unsigned / 否 | a01:penetrationRootCompanySourceRecord | IRI关系 / REJECT | CQ-02/07 |
| `penetration.target_company_id` | bigint unsigned / 否 | a01:penetrationTargetCompanySourceRecord | IRI关系 / REJECT | CQ-02/07 |
| `penetration.owner_company_id` | bigint unsigned / 是 | a01:penetrationOwnerCompanySourceRecord | IRI关系 / OMIT | CQ-02/07 |
| `penetration.shareholder_name` | varchar(512) / 否 | a01:shareholderName | string / REJECT | CQ-02/07 |
| `penetration.shareholding_ratio` | decimal(10,6) / 是 | a01:shareholdingRatio | decimal / OMIT | CQ-02/07 |
| `penetration.level` | int / 否 | a01:penetrationLevel | integer / REJECT | CQ-02/07 |
| `penetration.shareholder_id` | bigint unsigned / 是 | a01:penetrationShareholderSourceRecord | IRI关系 / OMIT | CQ-02/07 |
| `penetration.is_terminal` | tinyint / 否 | a01:reportedTerminalFlag | integer / REJECT | CQ-02/07 |
| `penetration.ratio_quality` | varchar(24) / 否 | a01:ratioQuality | string / REJECT | CQ-02/07 |
| `penetration.equity_ratio` | decimal(12,8) / 是 | a01:equityRatioToRoot | decimal / OMIT | CQ-02/07 |
| `shareholder.id` | bigint unsigned / 否 | a01:sourceRecordId | integer / REJECT | CQ-02/03/07 |
| `shareholder.company_id` | bigint unsigned / 否 | a01:shareholderOfCompanySourceRecord | IRI关系 / REJECT | CQ-02/03/07 |
| `shareholder.owner_company_id` | bigint unsigned / 是 | a01:ownerCompanySourceRecord | IRI关系 / OMIT | CQ-02/03/07 |
| `shareholder.participant_name` | varchar(512) / 是 | a01:participantName | string / OMIT | CQ-02/03/07 |
| `shareholder.participant_type` | varchar(128) / 是 | a01:participantType | string / OMIT | CQ-02/03/07 |
| `shareholder.share_type` | varchar(128) / 是 | a01:shareType | string / OMIT | CQ-02/03/07 |
| `shareholder.share_count` | bigint / 是 | a01:shareCount | integer / OMIT | CQ-02/03/07 |
| `shareholder.subscribed_capital_value` | decimal(22,6) / 是 | a01:subscribedCapitalValue | decimal / OMIT | CQ-02/03/07 |
| `shareholder.subscribed_capital_currency` | varchar(8) / 是 | a01:subscribedCapitalCurrency | string / OMIT | CQ-02/03/07 |
| `shareholder.subscribed_capital_date` | date / 是 | a01:subscribedCapitalDate | date / OMIT | CQ-02/03/07 |
| `shareholder.subscribed_share_ratio` | decimal(10,6) / 是 | a01:subscribedShareRatio | decimal / OMIT | CQ-02/03/07 |
| `shareholder.ratio_quality` | varchar(24) / 否 | a01:ratioQuality | string / REJECT | CQ-02/03/07 |
| `source_row.source_table` | varchar(64) / 否 | a01:sourceTable | string / REJECT | CQ-07 |
| `source_row.source_id` | decimal(20,0) / 否 | a01:sourceId | integer / REJECT | CQ-07 |
| `source_row.standard_table` | varchar(64) / 是 | a01:standardTable | string / OMIT | CQ-07 |
| `source_row.standard_id` | decimal(20,0) / 是 | a01:standardId | integer / OMIT | CQ-07 |
| `source_row.disposition` | varchar(16) / 否 | a01:disposition | string / REJECT | CQ-07 |
| `source_row.issues_json` | json / 否 | 未投影；只在扫描列与schema声明 | UNSUPPORTED：无已证明JSON投影；语义问题明细不完整 | CQ-07 |
| `source_row.ratio_missing_flag` | tinyint / 否 | a01:ratioMissingFlag | integer / REJECT | CQ-07 |
| `source_row.ratio_out_of_range_flag` | tinyint / 否 | a01:ratioOutOfRangeFlag | integer / REJECT | CQ-07 |

合计7表、71列：61列以数据属性投影，9个外键字段由关系投影承载，1个JSON字段不投影。读取列清单完整不等于运行时业务字段覆盖完整。

`source_row.source_id/standard_id`为decimal(20,0)，按整数语义映射xsd:integer。目标平台仍须确认20位值的精确词法与无损处理；本地文件核对不能代替该执行证据。其他比例以xsd:decimal保留百分点，不用浮点舍入作临界判断。

所有权比例或日期的业务规则不会从本表自动执行。当前包无SHACL实例质量门禁；源不可用、部分读取和拒绝行由Mapping Coverage要求UNKNOWN，实际传播行为须在平台运行验证。
