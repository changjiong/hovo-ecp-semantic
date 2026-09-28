---
name: ecp-semantic-release
description: 将已完成双责任人确认的 ECP V3 技术语义模型闭包写入目标 Workspace 的不可变 Revision，执行跨资产候选编译，并在明确授权时发布、回读和核验运行证据。用于 ECP V3 平台交付；不重新设计业务模型、Ontology、Mapping 或规则，不把编译成功称为源数据完整、发布许可或业务验收。
metadata:
  author: Hovo
  version: "0.3.0"
---

# ECP V3 语义资产发布

本技能只处理平台副作用和真实平台证据。技术语义模型生成全部由 ecp-semantic-authoring 完成。

## 输入边界

必须读取：
- 精确的 ecp-semantic-authoring 2.0.0 输出；
- 语义实现负责人对该精确输出的确认；
- 数据负责人对同一精确输出的确认；
- 目标 Workspace、Profile、边界身份和操作授权；
- 业务案例。

任何一份确认缺失、摘要变化或 authoring 的 candidate_closure 为 BLOCKED，都不得进入平台写操作。

## 动作

仅支持：
1. COMPILE：创建不可变资产 Revision，组装同一候选并执行 V3 原生跨资产编译；
2. PUBLISH：在 COMPILE 成功基础上发布不可变 Release 并回读；
3. VERIFY_RUN：对已发布精确 Release 的运行进行核验。

不再提供旧 PACKAGE、ZIP 打包、旧 Import 或独立 Mapping 阶段。

## 执行顺序

1. 核对 authoring 闭包、双确认、资产摘要、依赖和目标环境。
2. 按稳定 Series 创建不可变 Revision；不得修改资产正文来迎合平台。
3. 组装精确 V3 Candidate，执行目标环境原生跨资产编译，保存完整有界拒绝项或编译回执。
4. 编译拒绝返回 ecp-semantic-authoring；业务含义问题再由 authoring 返回 domain-model。release 不自行修规则、Mapping 或 Ontology。
5. 仅在 PUBLISH 明确授权时发布并回读 Release ID、Digest、Membership。
6. 仅在 VERIFY_RUN 授权时核验固定 Release/Run/Case 的实际结果、Trace 与证据。
7. 分别报告 Revision 已创建、候选已编译、Release 已发布、Run 已核验、业务已验收；不得互相替代。

V3 编译成功仅证明这个精确候选被这个精确部署接受，不证明源数据完整、运行质量、生产准入或业务正确性。
