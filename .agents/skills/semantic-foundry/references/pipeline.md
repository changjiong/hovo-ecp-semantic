# 四阶段路由与责任

| 已有输入 | 下一阶段 | 允许进入的新增信息 |
| --- | --- | --- |
| 业务材料、法规、案例、专家说明 | domain-knowledge | 来源、业务用途、冲突与问题 |
| 已确认领域知识 | domain-model | 仅业务知识；隔离物理 Schema 和平台能力 |
| 已确认 Business Domain Model | ecp-semantic-authoring | 真实 Schema、数据源身份、ECP V3 Profile、部署能力回执、案例 |
| 已完成语义与数据双确认的 authoring 闭包 | ecp-semantic-release | 目标 Workspace、操作授权、Release/Run 引用 |

## 核心边界

authoring 与 Mapping 不再是两个阶段。Ontology、SHACL、Mapping、Derivation、Evaluation、Lifecycle 和 Action Policy 在 V3 中共同构成跨资产候选编译单元。Mapping 的 ontologySourceDigest 还直接绑定 Ontology 字节，因此不能在 Ontology 先独立封版后再以另一个阶段追加 Mapping。

职责仍然分离：语义实现负责人确认平台表达忠实性；数据负责人确认真实源绑定、身份、Join、NULL、时间、Coverage 和 UNKNOWN 传播。两份确认指向同一个 authoring 输出。

编译拒绝默认返回 authoring。只有当修复需要改变业务对象、关系、判断、阈值、UNKNOWN 口径或案例预期时，才形成 CHANGE_REQUEST 返回 domain-model 或 domain-knowledge。

pipeline.json 只用于跨阶段编排，不复制任何阶段正文。
