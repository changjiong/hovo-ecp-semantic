# 信任与权限报告

## 结论

`hovo-ecp-semantic` 的设计边界是“本地编写 + 本地确定性验证 + 可选工作包打包”。默认不进行任何 GitHub/ECP 远端写入。

## 权威来源

1. 用户提供的 `ECP Semantic Authoring Kit 1.7`。
2. Kit 内 `ECP Semantic Profile 1.0` 是运行语义的最高权威。
3. 资产 Guide（指南）与 JSON Contract（JSON合同）负责具体格式，但不得扩大 Profile 能力。
4. 外部本体技能只用于工程方法参考，不覆盖 ECP 正式规范。

## 文件权限

允许：
- 读取用户提供的领域材料、表结构和 ECP 资产；
- 写入用户指定语义工作目录；
- 写入技能自身 `reports/`；
- 在打包前刷新摘要。

默认禁止：
- 改动 ECP 远端 Workspace Head；
- 创建 Revision/Release；
- 发布 GitHub；
- 删除历史语义资产。

## 语义安全硬边界

生成资产中禁止：
- Secret、Token、Password、API Key；
- URL/Endpoint、数据库连接串；
- S3 Bucket/Object Key/ETag；
- 本地文件路径；
- 任意 SQL、JavaScript、SHACL-JS、SHACL-SPARQL；
- 未登记 Runtime Operator（运行时算子）。

## 证据边界

本地工具可以证明：
- JSON/TTL 可解析；
- 公开 JSON Schema 合同；
- ECP Profile 有限静态构造；
- 摘要一致性；
- Rule Set/Workspace 成员路径和结构；
- 部分跨资产静态一致性。

本地工具不能证明：
- 当前数据源物理表/字段仍存在；
- Fact Provider（事实提供器）可用；
- ECP 编译器完整 expectation；
- 当前候选 Release 跨资产编译通过；
- Published Release（已发布版本）存在。

对应状态必须保留为 `missing evidence` 或 `ECP_PREFLIGHT_REQUIRED`。

## 回滚与破坏性语义

- Full Replacement（完整替换）包可能让候选 Draft Head 中未包含的历史成员退出当前候选集合。
- 技能只负责报告该风险，不替用户执行平台侧确认。
- 不添加旧 Profile 兼容层；目标版本改变时按新版本重新生成正确资产。


## 有界人工参与

默认采用 evidence-first（证据优先）与 bounded HITL（有界人工参与）。用户只负责真正的高影响业务语义决策，不负责代替技能查规范、附件、代码或可访问环境中的事实。默认主动澄清最多一轮五题；多轮 Workshop（研讨）必须由用户明确请求。
