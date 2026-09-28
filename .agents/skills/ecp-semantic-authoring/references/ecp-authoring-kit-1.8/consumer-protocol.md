# Consumer Input, Output and Execution Contract

文档类型：规范

文档状态：当前

权威范围：任意宿主集成 Semantic Execution Engine 时必须遵守的边界

权威来源：`crates/runtime`、`crates/semantic-model`、运行时协议测试

适用版本：`ecp-v3-native-runtime/6`

最后核验日期：2026-09-23

## 1. 依赖方向

消费方提供受治理输入并消费结果；引擎不读取消费方源码、数据库、对象存储、任务队列或业务配置。宿主坐标、凭据、用户令牌和部署路径不得进入引擎语义身份。

## 2. 模型输入

版本化模型包包含原始语义资产及身份：本体和锁定导入闭包、Mapping、SHACL、派生、求值，以及可选生命周期、身份迁移和动作策略。编译成功只证明当前构建接受该模型，不证明源输入完整、计算质量合格或宿主允许发布。

## 3. 数据输入

- 全量：按声明 Scan 提供完整、类型化且有稳定 Record Key 的 `SourceRow`；
- 增量：提供 INSERT/UPDATE/DELETE 或完整变化捕获，并绑定预期旧版本；
- 模拟：在固定基线上提供隔离假设，不推进当前状态；
- 恢复：提供与模型、边界、运行时、词典和前序身份一致的检查点链。

宿主负责数据源认证、一致性读取、覆盖证明、事件连续性和事务边界。未报告记录不能自动解释为删除。

## 4. 原生会话

`ecp-v3-runtime`通过有界 JSONL 请求/响应协议提供能力读取、编译、分块输入、全量完成、刷新／事件／模拟候选、保存恢复、提升／丢弃、生命周期计划以及固定状态分页读取。调用方必须持续消费 stdout/stderr、核对 requestId、遵守帧和资源上限，并显式关闭可重放游标。

进程成功响应、进程正常退出、候选被 PROMOTE 和宿主事务提交是四个不同事件，不能互相替代。

## 5. 输出

固定状态可提供：

- Asserted、Entailed、Derived 事实及变化；
- 三态 Evaluation、Candidate 和质量诊断；
- Source Origin、Support、充分见证、全部贡献和 PROV-O 投影；
- 生命周期计划、Equality 注记、状态摘要和检查点引用；
- 资源指标、警告和稳定错误码。

事实、变化、求值、质量和证据均绑定同一状态。分页结果必须验证类别、状态、序列、摘要和完成语义。

## 6. 四种执行模式

| 模式 | 基线 | 是否允许修改宿主生产状态 |
|---|---|---|
| 全量 | 新输入 | 由宿主验收和事务决定 |
| 增量 | 精确前序 | 由宿主验收和事务决定 |
| 追溯 | 固定不可变状态 | 否，只读 |
| 模拟 | 固定基线 + 隔离假设 | 否 |

同一模型、最终输入和上下文下，全量与增量必须语义等价；模拟使用相同计算计划；追溯不得重新解释当前状态。

## 7. 准入与失败

`executionAssessment`、`strictCommitAllowed`、`qualityAssessment`和 Provenance 验证各自只证明其声明范围。最终发布许可属于宿主。语法、类型、覆盖、质量、语义、资源、检查点身份和进程故障必须保留不同错误分类并失败关闭。

## 8. 版本与兼容性

模型摘要、边界、运行时 ABI、依赖锁、检查点和前序均参与兼容性判断。开发期可以拒绝旧检查点并要求完整重建，禁止修改摘要或伪装运行时身份强行恢复。

## 9. ABI 6 网络引用

网络算子输出增加 `NETWORK_FOLD {stage, root, member}` 引用；member 为具体资源符号或明确的 null 诊断。它只在精确状态和词典内有效，消费者需更新封闭引用校验。输入为声明式有限关系，不增加数据库、脚本或任意函数执行接口。旧运行时/检查点不因 ABI 6 自动兼容；先按既有授权确定重建或保留策略。

数值未决时，诊断生产者与可能的成员输出分开。可能输出保留端口中已知的root/actor键，其数值仍为UNKNOWN，不制造完整RDF事实；未知身份不能退化为全局通配成员或零成员成功。完整来源与冷恢复保留这些键及原因，未相关root的确定不存在仍可判断。`SIMPLE_PATH_EXPOSURE`明确拒绝root的策略诊断没有可能的数值成员域。UNKNOWN闭包的列索引和同阶段双域投影只减少重复计算，不删掉通配匹配、独立已知组合或替代原因；原工作量/事实预算及失败合同保持。

## 10. 有限集合阈值闭包

`ecp-bounded-network-fold/2`增加`AGGREGATE_THRESHOLD_CLOSURE`。主查询仍为四列边键/from/to/精确weight；四个端口依次为一列roots、一列seeds、两列node/blocked及三列policy/aggregateThreshold/uniqueMaximumThreshold。阈值端口必须恰好一行；0 < aggregateThreshold <= 1，0 <= uniqueMaximumThreshold < aggregateThreshold。重复或矛盾节点策略、被阻止的seed、非法权重、重复边和耗尽预算均拒绝，不返回截断成功。

全部seed作为同一集合求最小固定点：目标未被blocked时，已入集合的直接入边权重合计>=聚合阈值，或其唯一最大直接入边来自该集合且权重严格>唯一最大阈值，才加入集合。无seed的环不自行产生成员。阻止节点既不能被推导加入，也不能作为seed；合计条件与唯一最大条件保留各自边界，不按显示小数判断。

仅为声明roots输出成员；`NETWORK_FOLD.member`等于root资源自身，表示集合判定而非个人或经济权益。普通九列输出中total为最终集合内直接入边合计，显式seed的total=1是成员标记，不表示经济持有比例。证据保留该root所有逆向可达竞争边、相关seed/阻止策略及阈值；源版本改变仍改变证据身份。协议帧与ABI 6引用结构不变，机器边界摘要和精确运行时制品身份变化；旧构建不接受新算法，新旧检查点不能伪装兼容。

## 11. 逐根网络边界

`ecp-bounded-network-fold/3`增加`FRONTIER_PRIORITIZED_CLAIMS`与`FRONTIER_THRESHOLD_CLOSURE`。它们在原算法的端口之后增加两列node/boolean frontier策略；标志必须为有效`xsd:boolean`，字符串、整数及语言字面值不能隐式替代。重复或矛盾node策略拒绝。每个root计算时，仅删除to为true frontier且to不等于当前root的经济边。边界节点的出向经济边保留；同一节点作为自身root时，其入向边仍可计算。端口为空或全false等价于原算法，所有输入仍必须通过原权重、唯一边及资源校验。

frontier不删除单独声明的归属claim或结构化控制证据；它也不替代原control node policy的natural/boundary/requiresEvidence合同。这些事实是否适用由模型明确声明，引擎不解释节点的业务名称、类型或标签。相同frontier图的普通roots共享一次有限图构建/控制闭包，但不宣称已具备M4局部增量或百万资格。

完整证据保留原逆向可达竞争输入及相关frontier策略，不能只返回被保留路径。同值新来源仍改变完整证据身份。ABI 6帧和引用结构不变；机器边界摘要及精确运行时身份改变，旧模型的离线资格制品需保留其准确身份，不能冒充新旧Checkpoint兼容或正式运行结果。

## 12. 路径限定的控制解限

`ecp-bounded-network-fold/4`增加`RESOLVED_FRONTIER_THRESHOLD_CLOSURE`，端口依次为四列经济边、一列roots、一列actors、五列node/natural/targetBoundary/requiresEvidence/restrictMinorSource、七列evidence/from/to/weight/decisive/listed/resolvesSource、六列policy/absolute/unique/important/tie/maximumPathNodes及两列frontier。布尔字段严格要求有效xsd:boolean；路径节点上限严格为xsd:integer的2至4096。旧算法继续使用其原端口，不能混入新字段或声称兼容旧Checkpoint。

目标边界阻止节点进入控制闭包；源节点限制只拒绝小于absolute的首层来源，两者独立。decisive事实可以使节点进入闭包，但不会自行跳过重要来源或上市低比例门禁。路径仅枚举当前actor到当前root的简单路径：中间节点必须已控制，特殊中间节点必须通过结构化边进入；范围由maximumPathNodes明确声明。它是模型的语义范围，不是隐藏资源截断。资源预算耗尽返回失败，不采纳局部路径作为成功。

当前actor/root的任一有效路径含resolvesSource时，可解除特殊首层来源缺少结构化末端边的限制；最终一段为明确resolvesSource证据时，该段来源可跳过首层门禁。上市标志按当前actor/root的所有有效路径判断。其他actor、其他root及需要重复节点的循环不能授予解限。控制权重仍按原特殊来源过滤合计，不因解限而制造表决权或经济权益。

重复或矛盾节点策略、重复控制证据身份及非法权重拒绝。完整证据保留全部逆向可达竞争边、结构化证据、节点/frontier策略及路径/数值阈值；同值新来源改变证据身份。引擎不解释任何业务名称或文档角色。协议帧及ABI 6引用结构不变；机器边界和精确制品身份变化，资格、部署及新持久状态分别验收。

## 13. 显式字符清理表达式

`ecp-finite-string-strip/1`声明有限表达式`STRING_STRIP {input, characters, position}`。`characters`是模型中的固定Unicode字符集；`ALL`移除所有匹配字符，`ENDS`仅移除首尾匹配字符。它不接受正则、脚本、动态回调或隐式标准化。只接受`xsd:string`和`rdf:langString`，结果保留数据类型与语言，原始源词项和来源版本不变。缺绑定或非字符串产生类型化UNKNOWN；输入或计算预算耗尽失败，不被IF/COALESCE转为成功。

`ecp-bounded-output-branches/1`的资产操作为`BRANCHED_ROWS {branches}`及`BRANCHED_LEFT_JOIN {right, leftKeyColumns, rightKeyColumns, branches}`，每个分支为`{condition, outputs}`。分支1—16个且各输出非空，合计最多128模板；查询、连接键、绑定和阶段限制沿用既有合同。只有boolean true发出确定输出，false延迟跳过输出表达式，UNKNOWN/非boolean保留该分支的可能输出和诊断，不能解释为不存在。输出证据序号按全部分支模板展开且不会因false分支重排。条件常量使用主查询图的别名域，输出使用各自图的别名域。既有Rows/LeftJoin生产者保留双方及替代来源，删除、模拟和冷恢复按原模型身份执行。边界和制品摘要变化，不授权旧身份恢复或正式发布；ABI 6帧及证据引用种类保持。

分支模型的`OUTPUT_ISSUES.basis`附带`outputConditions`，与`outputs`逐项等长，按输出序号解释具体条件；全局`condition`为null。旧非分支模型省略该字段，保持其原解释。消费者必须接收此有限扩展后才能使用分支模型；不能忽略未知输出或将某分支的条件套用到所有输出。

`ecp-bounded-window-order/1`扩展既有`WINDOW`资产为可选`secondaryOrderBy: [{expression, direction}]`，最多8项；主键仍为`orderBy`/`direction`，各方向仅`ASCENDING`或`DESCENDING`。按声明顺序进行RDF值比较，最后全相等才按稳定事实身份；默认空列表在序列化时省略。所有键均须求值，缺失、自身不可排序或实际比较不相容使整个分区UNKNOWN，单行也适用；语言字面值不被隐式转换为string。计算预算错误直接失败。确定和UNKNOWN窗口证据均包含本分区全部竞争绑定及完整来源版本；未选中行同值新来源也改变选中结果的证明身份。证据引用种类与ABI 6帧保持，精确边界/制品身份改变；旧检查点不能以新身份伪装恢复，性能和生产门禁须分别验收。

`EVIDENCE`接受已声明的`WINDOW`和`LEFT_JOIN`引用，返回其输入绑定链接；这些算子引用没有事实词项描述，不进入`FACT_DESCRIPTION`路径。`PROOF`继续按固定状态构造完整证书。证明构造超限仍返回`STATE_BUDGET_EXCEEDED`，诊断消息可包含耗尽的`NODES`、`SUPPORTS`、`PREMISES`、`WORK`、`ENCODED_BYTES`或`OUTPUT_BYTES`及观察值/上限；消息是运行诊断，不属于语义身份。预算和计数口径保持，拒绝不产生截断成功或改变原状态。保存后须使用精确制品和完整谱系恢复，不能以ABI相同替代制品身份检查。

编译期字符集上限为64个标量及256字节；运行期输入上限1048576字节，输入字节数乘去重字符数上限4194304。字符集为空、非法位置和未知字段拒绝。ABI 6帧保持，机器边界和精确运行时身份变化；消费方必须编译及验收准确制品，不得伪装旧检查点兼容或将局部资格说成已部署。

## 14. 显式简单路径暴露

`ecp-bounded-network-fold/5`增加`SIMPLE_PATH_EXPOSURE`。主查询为四列边identity/from/to/精确weight，端口依次为一列roots、一列actors、五列policy/maximumPathNodes/maximumPathsPerActorRoot/requireResolvedRoot/requirePositiveResolvedEntry及两列node/frontier。policy必须恰好一行且identity为资源；两个上限严格为xsd:integer，分别2至4096及1至65536，标志严格为有效xsd:boolean。重复边/端点对、非法权重、重复frontier策略、矛盾端口或非本算法的额外replay配置拒绝。

逐actor/root枚举声明节点范围内的全部简单路径；节点不重复，到root即停止。路径长度是模型明确的语义范围，路径数量上限是资源预算；超过数量或计算预算时整个请求失败，不能保留前若干路径作为成功。每条路径精确相乘，路径间精确相加，最后按既有输出scale格式化；direct与total均为该和，raw/adjusted为零。不作SCC逆矩阵调整、归属claim、控制闭包或隐式业务阈值判定。actor等于root、零可达路径不输出成员。

requireResolvedRoot为true且当前过滤图中的root分量不能唯一求得非负暴露时，只输出`ROOT_COMPONENT_UNRESOLVED_REPLAY_DISALLOWED`诊断；可解的目标循环不因其他上游循环未解而被拒绝。requirePositiveResolvedEntry为true时，仅为有正向已解入口的actor回放：沿分量DAG求得已解贡献，未解分量不提供贡献，上游独立已解入口可保留。此资格量不作为完整暴露输出、不把未解分量宣称为零，也不取代既有严格算法的UNKNOWN诊断；最终比例仍由完整声明范围内简单路径的精确和决定。两标志均为false时只进行路径求和，不声称已解循环。逐根frontier沿用其他true节点入向边切断、当前root豁免和出向边保留合同。

完整证据保留原逆向可达的全部竞争经济边、相关actor/frontier及replay policy；未被求和采用的竞争循环来源改变时，完整证明身份仍改变。ABI 6帧及NETWORK_FOLD引用保持，机器边界和精确制品身份变化；新旧Checkpoint不能伪装兼容。该算法不声明M4局部成本、百万资格或正式发布。

## 15. 严格网络折叠的已解循环范围

`ecp-bounded-network-fold/6`为全部数值行增加第8列（从0计数）严格`xsd:boolean`，其他算法固定为false。对`TARGET_EXPOSURE`、`PRIORITIZED_CLAIMS`和`FRONTIER_PRIORITIZED_CLAIMS`，仅当当前root经frontier过滤后的逆向可达图包含已解循环分量时为true；这是整个root的审计范围标记，不声称每个actor必经该循环。该root同时输出`SOLVED_CYCLIC_COMPONENT_IN_SCOPE`信息性诊断；它不构造不确定成员域，不改变既有分数、精确商或归属值。未解循环仍沿用既有UNKNOWN合同；`SIMPLE_PATH_EXPOSURE`不产生该信息诊断。新增行计入输出预算，超限整体失败。来源证明覆盖与检查点恢复仍按实际运行时制品和新边界摘要验收；ABI帧编号保持6。
