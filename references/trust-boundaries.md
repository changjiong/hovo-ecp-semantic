# 信任、权限与失败关闭边界

## 1. 不伪造权威

以下信息只有 ECP 平台或真实数据系统可以证明：

- 当前 Hovo 数据源中表/字段确实存在；
- Mapping 在当前 Schema Snapshot 中可执行；
- Compiler Contract 的完整 Expectation；
- Scope 闭包可达性和实际资源基数；
- Fact Provider 可用；
- 候选 Semantic Release 完整编译通过；
- Published Release 已创建；
- Replay/What-if 行为与生产一致。

缺少证据时必须写 `missing evidence` 或 `ECP_PREFLIGHT_REQUIRED`。

## 2. 禁止进入语义资产的内容

- 密码、Token、Secret、API Key；
- HTTP Endpoint、数据库连接串；
- S3 Bucket/Object Key/ETag；
- 本地路径；
- 任意 JavaScript、SQL、SHACL-JS、SHACL-SPARQL 回调；
- 未登记 Runtime Operator。

## 3. 失败关闭

- Profile 不支持的语义构造：拒绝，不降级解释；
- 缺少关键事实：UNKNOWN/Coverage 或拒绝，不编造；
- Mapping 与 SHACL 冲突：拒绝，不依赖“数据恰好不会触发”；
- Scope 预算/完整性无法证明：拒绝，不截断；
- Digest 不一致：拒绝，不自动忽略；
- Evaluation 编译合同缺失：不进入正式规则 Manifest。

## 4. Full Replacement 风险

完整规则集或完整资产导入的“遗漏”可能意味着当前 Draft Head 中成员被移除。生成此类包时，报告必须列出：包内完整成员列表；与现有候选相比可能被移除的成员（如果现有资产已提供）；不可逆远端操作仍需用户在 ECP 页面显式确认。

## 5. 版本和回滚

本技能只生成新文件或修复用户明确要求的工作目录。它不覆盖 Published Release；ECP 的历史 Revision 和 Published Release 由平台不可变机制管理。

不添加旧 Profile 兼容层；当前任务以用户指定或工具箱当前正式版本为目标重新生成正确资产。
