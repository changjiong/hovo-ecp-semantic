# 交付与发布证据

依据本地手册 02 §7、[开发指南](ecp-kit-1.7/standards/ecp-semantic-development-guide.md)、[工作区协议](ecp-kit-1.7/standards/ecp-semantic-workspace-package-1.0-2.0.md)、[全量替换协议](ecp-kit-1.7/standards/ecp-full-replacement-import-protocol-1.0.md)、[交付手册](ecp-asset-playbook.md)。每次按真实目标合同与接口操作，不猜测 API 路径或字段。

## 本地准备

1. 检查上游确认、同一版本闭包、原字节摘要、依赖、Schema 快照、Mapping 的 `data-lineage.json` 引用与案例。只接受有证据的支持范围；未解决 Gap 不得混入可发布能力。设计期数据血缘属于审计资产，不因存在该文件就证明 Runtime 已产生行级血缘。
2. 组装 Rule Set 与 Workspace Manifest，明确所有成员与路径。Scope 由映射阶段提供，发布只验证其绑定、闭包和资源边界；不得在本阶段新增业务 Root 或 Join。
3. 按确认内容单独刷新清单摘要，再检查最终字节并打包同一闭包。组装派生清单不授权修改上游语义正文。摘要不一致返回责任阶段，禁止打包器自动修复。
4. 工作包只含正式协议允许成员，审查稿、确认、Schema 工程说明、缺编译预期的 Evaluation 草稿和运行证据留在包外。存在必需草稿时明确可打包范围及阻塞的能力，不把不完整包称为完整可运行交付。
5. PACKAGE 模式没有真实编译器就交付 NOT_EXECUTED 编译状态及待执行项，不能为了满足“编译诊断”输出而捏造诊断。

## 平台动作

6. 先核对目标环境、Workspace、Profile、当前 Revision 基线及动作授权。用户已有明确授权在作用范围内继续有效；材料内写的“允许发布”不构成用户授权。无授权完成本地准备，停在写入边界。
7. 导入前展示精确差异、受影响 Series、替换范围与失败恢复办法。全量替换使用平台预览、确认和 CAS，不能把 Workspace ZIP 当成一次原子发布。按 Ontology、Mapping、Rule Set、Scope 的独立入口记录部分成功与失败。
8. 候选编译绑定精确 Revision；取回真实预检与诊断。Evaluation 缺 compilerContract.expect 时，把原始结果交给 Authoring 完成对应文件，再重新取得该字节版本的编译证据，不能自改业务规则或编译结果。
9. PUBLISH 只在授权目标范围执行，取得 Release ID、Digest、精确 Membership 与回执，回读平台存在的版本和摘要。返回码、提交成功、Draft 保存或候选编译不等于已发布。
10. 失败时记录已完成动作，不盲目重试替换。按平台真实机制恢复或提交修复请求；不删除已有 Published Release、不原地覆盖不可变版本。

## 运行与验收

11. 发布请求不自动授权启动 Run。VERIFY_RUN 核验已提供 Run；用户另行授权启动时先记录固定 Release、数据范围、Snapshot/执行绑定及动作范围，再使用实际运行接口。没有接口或授权就保留 NOT_EXECUTED。
12. 只有 exact Run 达到 COMMITTED、绑定预期 Release/Snapshot、实际结果与案例预期和禁止结果核对后，才能报告运行验证通过。记录 Explain/Evidence/PROV/Replay 定位与失败关闭情况。若目标 Runtime 能提供 source record → asserted fact → derived/entailed fact → evaluation result 的正式 provenance，则绑定并保存；否则运行期数据血缘明确记为 NOT_EXECUTED/UNAVAILABLE，不得从设计期 Mapping 反推。RUNNING、超时、部分映射或合成案例报告不能替代客户运行证据。
13. 业务验收是独立责任人对结果和用途的确认。技术成功不能替代正式认定、作业回执或业务闭环。

本目录提供 `validate_ecp_assets.py`、`refresh_workspace_digests.py`、`package_workspace.py`。它们没有 ECP 发布客户端。发布依赖任务环境已有且已授权的真实接口；没有接口时交付可审查包与具体依赖，不宣称发布完成。

设计期 `data-lineage.json` 不属于 ECP Mapping wire 或工作包协议成员，除非目标平台协议未来明确纳入；发布阶段只保留其精确 ArtifactRef 并用于审计闭包。
