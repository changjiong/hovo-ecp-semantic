# ECP 资产交付手册

Workspace ZIP 是跨页面传递封装，不是跨资产原子导入、Release 或 Run。可供访谈确认的业务审查/设计材料置于包外；摘要证明字节与声明绑定，不能证明业务含义或当前来源可用。

1. 形成局部候选：检查登记闭包、摘要、受支持语法/Profile 子集和有限本地引用；未执行的 Compiler、来源和实例检查逐项记录。
2. 按页面导入：Ontology、Mapping、完整 Rule Set，最后将 Scope 作为独立 Series。平台在 Draft Head 优先、Published 回补的上下文预检，展示差异、确认、按正确 CAS 边界创建不可变 Revision，并回读 Draft。中间 Draft 可以存在，但不可发布。
3. Candidate Compile 只引用精确 Revision 身份。编译成功是只读证据，不创建 Release 或 Run。
4. 只有平台对选定精确 Revision 重新完整编译、冻结不可变 Release Membership 和所需 SHACL Stage 后才能发布。Rule Set 含 SHACL 时，`asserted`、`domain`、`feature`、`change`、`output`、`provenance` 必须各唯一绑定一次；内容或 Stage 角色变化都需要新 Revision 与 Release。
5. Engine Run 前绑定 Published Release、Runtime Artifact、Dependency Lock、Execution Closure、Source Snapshot、请求/时间/日历输入和 Lifecycle。
6. 只接受已完成的 Committed Run 回读：核对图和结果身份、Explain、Evidence、PROV、幂等重试与 Replay 零差异。端口、健康响应、Candidate 或 `RUNNING` 状态都不是验收证据。

以下必须留在平台：Mapping 导入重新发现当前 Hovo 数据源、表/View、字段和关系；Release Compile 检查 Mapping-SHACL、算子、Definition 依赖、Coverage 与 Scope；Scoped Execution 检查已部署 Fact Provider 返回完整闭包。本地不得模拟，直到证据给出精确 Revision、Release 或 Committed Run 前，分别报告 `ECP_PREFLIGHT_REQUIRED` 或 `NOT_EXECUTED`。

导入与格式遵循 [完整替换协议](ecp-kit-1.7/standards/ecp-full-replacement-import-protocol-1.0.md)、[工作包协议](ecp-kit-1.7/standards/ecp-semantic-workspace-package-1.0-2.0.md)、[Rule Set Manifest Schema](ecp-kit-1.7/contracts/rule-set-bundle-manifest-v1.schema.json) 和 [开发指南](ecp-kit-1.7/standards/ecp-semantic-development-guide.md)。内容确认后先刷新 Workspace 摘要，再校验最终闭包，最后打包；打包绝不刷新摘要或授予 Release 身份。

首个 Release 的 Run 证据至少包括：无伪造变化的 Baseline、真实变化、UNKNOWN 与失败、schema/字段漂移、SHACL 失败、重试、Explain/Evidence/PROV 和 Replay。含 Action Policy 时，Intent/Outbox 与连接器幂等证据还须独立保存。
