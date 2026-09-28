# ECP V3 发布验收

1. 输入必须是 ecp-semantic-authoring 2.0.0 的精确输出，candidate_closure 必须为 READY。
2. semantic_confirmation 与 data_confirmation 必须分别由真实责任人确认，并绑定同一个 authoring 输出字节；release 使用的 Profile 与 deployment_boundary 也必须与 authoring 精确一致。
3. members 必须与 authoring 的资产闭包一致；release 不新增、修改或删除业务语义资产。
4. 每个写入平台的资产都创建稳定 Series 下的不可变 Revision，并记录平台摘要和真实回执。
5. COMPILE 必须调用目标 Workspace 当前 V3 原生跨资产候选编译；单文件 Schema VALID、Turtle 可解析或本地静态检查不能代替。
6. 编译拒绝完整记录有界原因并返回 authoring 修订；release 不偷偷改 Ontology、Mapping、规则、阈值或 UNKNOWN 语义。
7. PUBLISH 仅在同一精确候选编译成功且取得明确发布授权后执行；发布后回读 Release ID、Digest 和 Membership。
8. VERIFY_RUN 仅针对固定 Release/Run/Case；实际结果、Trace 和源证据与案例 expected/forbidden 分开记录。
9. platform_compiled、released、runtime_validated、business_accepted 是不同状态。编译成功不证明源数据完整、运行质量、生产准入或业务正确。
