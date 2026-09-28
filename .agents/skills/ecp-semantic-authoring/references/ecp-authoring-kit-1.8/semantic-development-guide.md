# Semantic Development Guide

文档状态：当前产品流程
最后核验日期：2026-09-28

新建 V3 模型先阅读[V3 语义资产编写指南](v3-asset-authoring-guide.md)，并从 Admin 下载绑定当前 Workspace 部署能力回执的 Semantic Authoring Kit 1.8。旧 Mapping Definition V1、Feature Definition V2、Evaluation Asset V1 和 Scope Definition V1 可保存为既有 Draft，但不能据此推断 V3 候选可编译。

## 建模顺序

1. 选择或创建Workspace；
2. 建立Ontology和SHACL；
3. 绑定Hovo数据源、表、主键、实体和属性Mapping；
4. 添加声明式派生、求值、Lifecycle和Action Policy资产；
5. 保存不可变Draft Revision；
6. 在“编译、审查与发布”选择精确Revision；
7. 用V3原生编译候选并发布；
8. 在“V3推理运行”提交BASELINE或REFRESH。

原始TTL/JSON是模型源码；Projection和图形界面只是投影。Published Release不可覆盖，任何变更都产生新Revision和新Release。

## 当前边界

候选审查与最终发布均由 V3 原生编译合同验证。Admin 只显示明确基线的 Revision/Membership 差异、Lifecycle 迁移声明和原生编译回执；不能以页面推测替代 V3 编译失败关闭。

Admin 的“V3 推理运行”已提供固定结果、Trace、源证据、Scenario、Lifecycle、Action Intent 和投递状态入口。应用查询方式见[应用集成与V3查询](../../reference/application-integration-and-v3-query.md)。

引擎语义标准不在本指南定义，以独立`semantic-execution-engine`的标准与能力资产为准。
