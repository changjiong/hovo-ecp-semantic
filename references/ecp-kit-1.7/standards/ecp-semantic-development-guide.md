# Semantic Development Guide

文档状态：当前开发流程

日期：2026-08-26

## 1. 目标与边界

本指南面向开发本体语义配置的人员，说明如何从标准TTL和业务表结构形成一个可验证、可发布、可执行的Semantic Release。生产权威始终是ECP MySQL中的不可变Published Release；仓库根级客户风险文件仅作为种子和兼容Fixture。

开发流程不能把任意JavaScript、SQL回调、网络地址或凭据写入Definition。新的执行能力必须先实现为通用有限Operator，版本化Runtime ABI并进入Execution Closure。
现有算子无法覆盖通用需求时，平台开发流程见[`按业务需求扩展 ECP V2 有限算子并在语义模型中使用`](runtime-operator-extension-guide.md)；只修改Definition或Admin展示不能创造新的执行能力。

## 2. 语义资产组成

| Asset Type | 内容 | 发布要求 |
|---|---|---|
| `ONTOLOGY` | 原始Turtle中的Class、Property和公理 | 一个可执行Release必须确定唯一Ontology |
| `SHACL` | `asserted/domain/feature/change/output/provenance`阶段约束 | 只要包含SHACL，就必须六阶段完整且唯一绑定 |
| `MAPPING` | Data Source、Scan、Join、Entity、Property、Relationship、Filter和Coverage | 最多一个，且精确绑定Release Ontology |
| `DERIVATION` | 计算属性和派生事实的有限Feature Definition | 必须通过类型、依赖、Scope和DAG编译 |
| `EVALUATION` | 对象级条件和Candidate输出计划 | 必须通过Ontology、Range、Cardinality、Coverage及明确Output Profile编译 |
| `ACTION_POLICY` | 语义变化或领域事件到外部Capability的声明式策略 | 只保存逻辑Binding和有限参数Source，不保存连接配置 |
| `SCOPE` | 围绕一个Root选择完整对象局部事实闭包的声明式策略 | 必须绑定同一Release Mapping的全部Scan/Join、明确Root Binding/Full Scan和有限资源上限 |

### 2.1 三层规范与帮助入口

ECP按三层分发语义建模合同：

1. **正式规范**：`ECP Semantic Profile 1.0`定义RDF、有限蕴含、Ontology和SHACL支持边界；`Full Replacement Import Protocol 1.0`定义完整Draft导入语义。两者在全局“文档中心”阅读；
2. **资产编写指南**：Ontology Turtle、Mapping JSON、SHACL Turtle、Derivation JSON、Evaluation JSON、Action Policy JSON、Scope JSON、完整规则集ZIP及统一工作包指南，提供当前页面所需的闭合格式和可用示例；
3. **机器可执行合同**：Profile Manifest、Mapping/Action Policy/Scope/Rule Set Manifest以及Workspace Package v1/v2 Manifest JSON Schema和版本化编译器断言。

侧边栏账户设置菜单提供个人信息、文档中心、下载中心和退出登录。下载中心还提供确定性生成的`ECP Semantic Authoring Kit 1.7` ZIP，把正式规范、全部编写指南和公开机器合同放入一个带SHA-256清单的离线工具包。Kit 1.7明确Scope Definition v1的Root Binding是作用于闭包中每一条已选Root行的双向等值边；它保留Kit 1.6的Feature/Evaluation `CONTAINS`与`STARTS_WITH`、Kit 1.5的`WeightedTransitiveClosure`跨Root预算、Kit 1.4的有限`DateFromDateTime`、Mapping–SHACL一致性、当前源快照直接执行、Workspace Package v2及跨资产联动指导。上游批次完成声明仍可由生产者自行保留，但不是ECP的运行前置条件。Kit升级不改变`ECP Semantic Profile 1.0`的RDF、蕴含或SHACL执行语义。

## 3. 第一步：创建或导入Ontology Draft

在Admin Web导入或粘贴标准Turtle。API会先解析TTL、执行受控Profile和静态检查，再生成绑定原始Source Digest的Ontology Projection和Validation Report。管理端按Ontology声明、Class及三类Property展示新增、修改和移除差异；源码有效但Release上下文编译失败时仍展示诊断，但禁用提交。

“完整替换本体”在Registry中的准确含义是为同一Asset Series追加一个新Draft Revision并以CAS推进Draft Head；候选中未出现的旧定义不进入新正文。历史Revision、Published Release和运行记录不被修改。失败的TTL、取消确认或CAS冲突都不会替换当前Draft Head。若候选TTL自身有效、但当前旧Mapping或规则仍指向上一版本本体，页面会明确提示“需要继续导入同包依赖资产”：这不阻止保存新Ontology Draft，也绝不允许发布Release，直到完整候选重新编译通过。

Ontology Projection只用于本体卡片、索引和Mapping开发。不得单独编辑Projection来绕过原始TTL。

## 4. 第二步：发现数据源并设计Mapping

数据源必须来自Hovo `hovo_data_source`中状态为`enabled`的`mysql`或`oceanbase_mysql`定义。后端解析直接值、`secret_ref_json`和`@@@from-env:*`，浏览器只接收数据源摘要及脱敏Schema。

Mapping v1的设计顺序：

1. 为每个物理表或View定义`scan`、稳定别名、Record Key和需要读取的列；
2. 用受控`INNER/LEFT`等值Join连接同一Hovo Data Source内的Scan；
3. 为每个Entity声明Ontology Class、稳定IRI模板和身份字段；
4. 将列映射为Datatype Property，或将另一个Entity映射为Object Property；
5. 声明Join Cardinality、NULL策略、有限Filter及Source Coverage要求；
6. 在页面Drawer逐属性配置，或按页面展示的Mapping Definition v1 JSON格式整体粘贴导入；同一个Semantic Workspace Package ZIP也可直接选择，页面只读取其中的`mapping/`资产。

Mapping JSON导入表示完整Mapping Draft：所有顶层集合都以候选为准，未出现的旧对象会从新Draft移除。页面先执行严格合同校验，把规范化后实际保存的JSON交给服务器做Draft优先候选预检，并通过Hovo重新发现当前表/View和字段，再按稳定ID展示对象级差异并要求显式确认；提交仍通过该Mapping Series的Draft Revision CAS自动保存。

无法由有限DSL表达的复杂逻辑应先由源系统提供受治理View。不要在Mapping中保存任意SQL。

## 5. 第三步：定义SHACL、派生、求值和Action

六个SHACL阶段分别验证Asserted输入、领域基础图、Feature、Change、Output和Provenance。Shape源仍是标准Turtle；当前Profile支持受控SHACL Core，不支持把SHACL-SPARQL当作已验证能力。

DERIVATION和EVALUATION使用版本化JSON合同及有限Typed Operator：

- 输入必须显式声明事实、Feature、时钟和对象Scope依赖；
- 输出Property和Datatype必须存在于精确Ontology；
- Feature依赖必须形成确定性无环图；
- 缺失输入应投影为局部Coverage或对象级UNKNOWN，不能编造值；
- 不允许按Signal ID在TypeScript中增加业务分派。

Feature与Evaluation的`Compare`都支持`CONTAINS`和`STARTS_WITH`。它们只接受两个静态类型为`string`的表达式，按Unicode NFC规范化后执行区分大小写的精确包含/前缀比较；不Trim、不做Locale折叠、不解释正则或通配符，也不把其他Typed Value隐式转成字符串。空右值按标准字符串语义匹配成功。

需要沿图执行比例连乘时使用版本化[`WeightedTransitiveClosure`](weighted-transitive-closure-operator.md)。它只输出路径事实和不完整性诊断，不替代领域阈值、规则顺序或最终结论；命中单根深度、路径或状态上限必须传播为对象级不完整性。作者还必须评估跨Root基数，并为新Definition显式设置不高于平台上限的`maxPathRecordsTotal`和`maxTraversalStatesTotal`。全局预算命中表示未处理Root的完整性无法证明，Runtime会失败关闭且不提交部分结果。

已物化的两个Feature数据集需要按资源或Typed Value相等关联时，使用`EquiJoinRows`。它只允许显式的多列等值条件、`INNER/LEFT`、`exactlyOne/zeroOrOne/many`基数合同和完整右侧变量声明；运行时合并两侧Support，基数违约失败关闭。它是Feature DAG内的事实关联，不是任意SQL Join。

`ProjectAssertions.assertions[*].when`可用Typed Boolean表达式条件化投影单条断言。条件为假时不求值`object`，适用于`LEFT` Join中只在匹配时产生的属性；不得用它隐藏对结论有影响的`UNKNOWN`或证据排除决定。

需要从`xsd:dateTime`取得自然日时，`ReadProperty`使用`valueType: "dateTime"`，再通过`DateFromDateTime`把该词法值表达的本地日历日期转换为`date`。该有限表达式不会跨时区改写时刻；数据库`DATETIME`因而保留源本地日期。它用于Feature层的类型化计算，不改变Mapping仍分别物化的业务对象，也不允许把任意SQL函数装入Definition。

ACTION_POLICY只匹配受治理Semantic Change或版本化Domain Event，声明Capability、Operation、逻辑`executorBindingRef`和有限参数来源。实际Connector、URL、Token和模板属于部署环境。

SCOPE使用`ScopeDefinition v1`严格JSON。它声明Root Scan及Record Key、全部Mapping Scan/Join、Root Binding、必须全量读取的Scan、双向Join闭包深度，以及行数、Frontier、Patch、Overlay、Fact Bundle和结果预算。每个Root Binding都是Root Scan列与辅助Scan列之间的双向等值边，适用于初始或后来由Join/Overlay选中的每一条Root行，不能按“一次性请求Root补数”理解。Scope不能保存SQL、JavaScript、Endpoint、Token、数据库配置或S3坐标。发布预检会对同一候选Mapping验证可达性与完整性；`ACTIVE`可创建Investigation Case，`RETIRED`只保留历史身份。

单项编辑继续只影响一个规则Series。需要用外部资产整体同步当前规则候选时，必须使用“导入完整规则集”ZIP：它把当前Workspace全部活动`SHACL`、`DERIVATION`、`EVALUATION`和`ACTION_POLICY` Draft Head作为一个集合进行预检、差异、确认和原子替换。ZIP遗漏的成员只移除当前Draft Head，历史Revision和Published Release保留。空ZIP不能清空；清空使用独立危险操作和确认文本。

保存前会先做本地JSON语法定位，再由Definition Development服务执行正式源码预检：

1. 按资产类型执行与Registry写入相同的Turtle或JSON闭合合同校验，并返回JSON Pointer字段路径；
2. 把未保存候选放入“当前所有Draft Head优先、最新Published Release补足缺失Series”的完整闭包，运行同一发布预检并展示诊断；候选源码自身的严格校验决定能否追加Draft；
3. 若既无足以构成候选的Ontology Draft也无Published Ontology，明确返回上下文不可用警告，允许保存Revision，但不声称已完成Release编译；
4. 完整规则集ZIP的`manifest.json`为每个SHACL声明唯一`shaclStage`，导入时写入当前Draft Head；发布窗口自动带入该绑定并冻结到Release；
5. 同一工作包的Ontology、Mapping与规则必须来自同一版本闭包：先保存同包Ontology，再保存同包Mapping，最后导入规则。系统会比较同包和当前Draft的源码摘要及规则引用的完整IRI；同名但`v1`/`v2`不同的术语不是同一个本体对象，不能混合发布。

预检不创建Asset Series、Revision、Release或Run，真正保存仍使用Draft Head CAS，真正发布仍对完整的精确Revision集合重复全部编译门禁。Draft可处于尚不可发布的中间状态，Release绝不可以。

## 6. 第四步：校验和候选编译

保存每类Draft前可在Admin执行上述只读源码预检；保存后仍须对精确Revision执行校验，再对准备发布的Draft Head集合执行候选编译：

```bash
corepack pnpm --filter @enterprise-cognitive/ecp-engine-cli cli definitions validate \
  --workspace-id <workspace-id> \
  --asset-series-id <asset-series-id> \
  --draft-revision <revision-number> \
  --revision-digest <sha256:digest>

corepack pnpm --filter @enterprise-cognitive/ecp-engine-cli cli definitions compile \
  --manifest <candidate-manifest.json>
```

候选Manifest只引用精确Revision身份，不携带定义正文。编译前后都会检查Draft Head没有漂移；成功只生成只读报告，不创建Release或Run。

## 7. 第五步：发布不可变Release

在Admin Release Composer显式选择每个成员Revision，并为六个SHACL成员指定唯一阶段。发布事务会：复核所有Revision Source、Projection和Digest；确定唯一Ontology和可选唯一Mapping；完整编译DERIVATION、EVALUATION、ACTION_POLICY和SCOPE；计算Membership及Release身份；在一个InnoDB事务中写入不可变Release和Membership。

发布失败不会留下部分Release。Published Release不能覆盖；任何内容或阶段角色变化都必须产生新Revision和新Release。

发布后执行独立复验：

```bash
corepack pnpm --filter @enterprise-cognitive/ecp-engine-cli cli definitions verify \
  --workspace-id <workspace-id> \
  --release-id <release-id> \
  --release-digest <sha256:digest>
```

## 8. 第六步：建立运行边界

运行前还必须完成：Hovo源定义及服务端环境变量可解析；Mapping引用的源表、字段和关系在当前一致性快照中可读取；MySQL Migration和四个S3 Bucket检查通过；Release绑定当前Runtime Artifact、Dependency Lock和Execution Closure；选择通用`NONE`或明确版本的领域Lifecycle Profile；调用方保存明确Release ID/Digest、日期、时区、Calendar Policy Digest和Request Revision。

如果使用Scoped Semantic Evaluation，还必须配置服务端Fact Provider并验证其能按Published Scope返回完整闭包；Endpoint和Token只在部署环境中。Investigation Case另行绑定Scope Revision、Root和Execution Binding，不复用或推进Workspace Head。

## 9. 第七步：验收与观察

首次发布至少完成：Baseline Run，确认没有伪造ADDED变化；一个有业务变化的Run，核对Asserted、Derived、Change、Evaluation和Lifecycle；相同Logical Request重试，确认幂等收敛；ABox浏览、Explain、Evidence和PROV核对；Replay零差异及What-if生产零写入证明；源表/字段或Schema漂移、SHACL失败和CAS竞争反例；如含Action Policy，核对Intent/Outbox原子提交和Connector幂等协议。

## 10. Definition变更分类

| 变更 | 必要动作 |
|---|---|
| TTL、Mapping、规则、Action或Scope内容改变 | 新Revision和新Release |
| SHACL阶段角色改变 | 新Release |
| 新有限Operator或执行语义改变 | 新Runtime ABI/Artifact/Lock/Closure，并建立新Execution Binding |
| Signal退出目录 | 使用显式Retirement语义 |
| Signal业务身份模型改变 | 使用一对一Identity Migration |
| 仅部署Connector地址或密钥改变 | 更新部署配置，不改变Semantic Release |
| S3 Endpoint/Bucket改变 | 更新适配器配置，不改变语义身份 |

## 11. 发布检查清单

- 原始TTL和Projection摘要严格绑定；
- Mapping覆盖每个需要的Class/Property并保留跨表Membership；
- 六阶段SHACL完整，未使用不受支持能力；
- Mapping的NULL/Cardinality/Datatype输出与六阶段SHACL约束一致，候选预检无静态矛盾；
- 所有Definition通过当前Compiler且没有业务ID代码分派；
- Source Coverage、Cardinality和对象Scope明确；上游批次完整性不作为ECP引擎门禁；
- Scoped Evaluation使用的Root Binding、Full Scan、闭包完整性和资源预算明确；
- Release、Runtime和Lifecycle Profile均为显式身份；
- 不含连接配置、凭据、S3物理坐标或任意代码；
- Baseline、变化、UNKNOWN、失败和幂等案例均有门禁。
