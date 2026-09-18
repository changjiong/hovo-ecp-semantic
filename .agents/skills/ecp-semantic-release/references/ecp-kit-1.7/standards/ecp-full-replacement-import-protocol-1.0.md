# Full Replacement Import Protocol 1.0

文档状态：当前规范说明

日期：2026-08-14

## 1. 目的

本协议定义ECP管理端导入Ontology、Mapping以及规则与约束时的完整替换语义。它只管理当前Workspace的Draft候选，不改变不可变Revision、Published Semantic Release、Committed Run或运行制品。

`ECP Semantic Profile 1.0`回答“ECP保证执行哪些语义构造”；各资产编写指南回答“如何编写一个资产”；本协议回答“一个完整候选如何经过预检、差异确认和原子提交进入Draft”。三者不能互相替代。

## 2. 共同合同

任何完整替换MUST按以下顺序执行：

1. 读取当前Draft Head身份，建立不可变预览基线；
2. 对候选执行严格语法、闭合合同、Semantic Profile和可用的Draft优先/Published补足上下文编译预检；
3. 计算新增、修改、移除和不变项，不产生数据库写入；
4. 向操作者明确展示“候选中未包含的内容将从当前Draft移除”；
5. 获得操作者显式确认；
6. 使用预览基线身份执行CAS，并在该替换单位的事务边界内提交；
7. 写入不可变Revision并更新或移除Draft Head；完整规则集还必须记录集合级替换审计；
8. 重新读取服务端Draft状态，不能仅用浏览器本地状态推测结果。

候选无效、确认取消、CAS冲突或事务失败时，该提交单位的旧Draft MUST保持不变。服务端不得先清空旧内容再逐项写入候选。

“移除”只表示删除当前`semantic_asset_draft_head`引用。相关`semantic_asset_revision`、`semantic_release_membership`、Published Release及运行记录MUST保留并继续可读。

Ontology和Mapping的替换单位分别是一个Asset Series；其CAS基线是该Series当前Draft Revision。规则集的替换单位是四类规则Series的完整Draft Head集合；其CAS基线是集合摘要，并在一个数据库事务中原子提交。三者不能被描述为同一种集合级事务。

## 3. Ontology完整替换

Ontology的替换单位是一个Asset Series的完整Turtle正文：

- 候选Turtle中的全部受支持声明构成新的Ontology Draft；
- 旧正文中存在、候选正文中不存在的定义不属于新Draft；
- 保存成功追加一个不可变Revision并以CAS移动该Series的Draft Head；
- Turtle解析、Ontology Projection和`ECP Semantic Profile 1.0`静态检查必须在确认前完成；
- 管理端必须优先组合当前全部Draft Head，只对缺失Series以最新Published Release补足，再展示把候选Ontology及虚拟重绑Mapping放入该闭包后的编译诊断；候选Ontology源码无效时不能提交。若源码有效而整体诊断仅因当前旧Mapping、规则或历史Draft尚未替换而无效，允许追加该Ontology Draft并明确要求继续导入同包依赖资产；这种中间Draft不得发布Release；
- Mapping与规则的跨资产兼容性在发布前重复检查。

Ontology导入不删除其他Asset Series。若Ontology源摘要变化，管理端在Ontology Revision提交后把现有Mapping完整内容重绑到新`ontologySourceDigest`并通过Mapping自身CAS追加Revision；两次Series提交不是一个跨Series事务。重绑失败时Ontology Revision保持已提交状态，管理端必须明确告警，且旧Mapping不能形成可发布候选。

## 4. Mapping完整替换

Mapping的替换单位是一个Asset Series的完整`Mapping Definition v1` JSON对象：

- `dataSources`、`scans`、`joins`、`entities`、`properties`、`relationships`、`filters`和`coverage`均为完整集合；
- 候选集合中不存在的旧映射项从新Draft移除；
- 管理端在确认前按稳定ID展示各集合的新增、修改和移除计数；
- 候选必须通过闭合JSON Schema、引用完整性、Ontology源码摘要绑定和凭据安全检查；
- 管理端必须把规范化后实际将保存的完整JSON提交给Definition Development源码预检，并展示可用Published Release上下文的编译状态和诊断；JSON自身或当前Hovo结构无效时不能保存。若诊断只反映其他尚未迁移的Draft，允许保存该Mapping Draft并把完整编译留给发布门禁；
- 管理端还必须通过服务端Hovo Catalog重新发现候选引用的当前表/View、关系类型和字段；包内Schema快照仅用于审阅，不能代替此校验和运行时Snapshot漂移检测；
- 提交继续使用该Mapping Series的Draft Head CAS并追加不可变Revision。

Mapping导入不删除Ontology或规则Asset Series。

## 5. 完整规则集Bundle

### 5.1 替换范围

规则集是当前Workspace中以下四类活动Draft Head的完整集合：

- `SHACL`；
- `DERIVATION`；
- `EVALUATION`；
- `ACTION_POLICY`。

一个单独的Turtle或JSON文件只能用于单项编辑，MUST NOT解释为完整规则集导入。完整规则集只能通过版本化ZIP Bundle导入。

### 5.2 ZIP布局

普通规则ZIP根目录MUST包含且只包含Manifest登记的文件：

```text
manifest.json
rules/<stable-name>.ttl
rules/<stable-name>.json
```

`manifest.json`遵循`enterprise-cognitive/rule-set-bundle/1.0.0`合同，并包含：

- 固定`schemaVersion`、`kind`和`bundleFormat`；
- 精确`semanticProfileId`和`semanticProfileDigest`；
- 每个成员的稳定Asset Series ID、类型、名称、说明、相对路径、媒体类型、源码摘要和可选SHACL Stage；
- 唯一、NFC、无目录穿越的成员路径和Asset Series ID。

如果Bundle包含SHACL，则MUST为`asserted`、`domain`、`feature`、`change`、`output`和`provenance`六个Stage各绑定一个SHACL成员，不能部分绑定或重复绑定。非SHACL成员的Stage必须为`null`。

Manifest未登记文件、缺失文件、重复路径、摘要不符、非UTF-8正文、Profile身份不符及不安全ZIP路径都必须失败关闭。当前上限为4,000,000字节压缩包、20,000,000字节解压内容、128个文件和96个成员。

`ECP Semantic Workspace Package 1.0 / 2.0`是受控例外：它可携带本体、Mapping、Schema快照和规则子目录，V2还可显式携带独立Scope成员；规则页面只抽取规则Manifest声明的逻辑规则文件后继续执行本节的严格检查，不把Scope混入四类规则集合。包可直接压缩唯一顶层目录，并忽略macOS归档元数据；正式布局和Legacy兼容条件见[`ECP Semantic Workspace Package 1.0 / 2.0`](semantic-workspace-package.md)。

### 5.3 预览与提交身份

预览返回：

- 当前规则集Draft集合摘要；
- Archive和Manifest摘要；
- 绑定预览基线及候选成员的Candidate Digest；
- 每个Series的`ADDED`、`MODIFIED`、`REMOVED`或`UNCHANGED`差异；
- 当前完整候选可执行时的编译结果，或可处理的上下文诊断。

规则集提交请求MUST携带预览得到的集合摘要和Candidate Digest。事务在Workspace行锁内重新计算集合摘要；不一致时拒绝全部写入。相同Candidate Digest的网络重试返回同一替换审计结果，不重复创建Revision。

若当前Workspace没有Ontology Draft，规则成员仍可完成各自源码合同校验；预览返回`NOT_RUN`及`ONTOLOGY_DRAFT_UNAVAILABLE`警告，允许保存Draft但不得声称完整候选已经可执行。只要存在可运行的Ontology上下文且完整编译结果为`INVALID`，提交必须失败关闭。Published Release Composer始终重复完整编译门禁。

新成员创建Asset Series和Revision；修改成员追加Revision；不变成员复用当前Revision；遗漏成员只移除Draft Head。整个变化集和编译诊断写入`semantic_draft_replacement`审计记录。

同一`assetSeriesId`的`assetType`是长期身份，导入不得改变它；Manifest中的名称和说明则是当前作者元数据，会随完整规则集替换原子更新。显式清空仍只移除Draft Head而保留Series、历史Revision和Release；因此清空后可以用同一个ID重新导入，而不必为显示名称或说明变化另建ID。

## 6. 显式清空

空ZIP、空Manifest和空文件MUST NOT解释为“清空”。完整规则集Bundle至少包含一个成员。

清空当前规则集Draft是独立危险操作，必须：

1. 读取并展示当前全部活动规则成员；
2. 使用当前规则集Draft集合摘要作为CAS基线；
3. 要求独立确认文本；
4. 在单事务中移除四类规则Asset Series的Draft Head；
5. 写入`RULE_SET_CLEAR`替换审计。

清空后历史Revision和Published Release仍可浏览、导出和用于历史运行审计。

## 7. 并发、失败与安全

- 所有摘要使用小写`sha256:`身份并绑定候选内容；
- ZIP解压必须在写事务前完成并受文件数、成员数和解压字节上限约束；
- 数据库写入必须锁定Workspace并以当前Draft集合摘要执行CAS；
- 浏览器提供的用户ID不可信，审计操作者来自服务端Platform Session；
- Manifest和源码不得包含凭据、连接配置、任意JavaScript、任意SQL或外部回调；
- Profile预检不能替代发布门禁，Published Release仍须对精确Revision集合重复完整编译。

## 8. 符合性检查

实现至少需要覆盖以下自动化案例：

- 非法Base64、摘要不符、ZIP Bomb预算、目录穿越和额外文件拒绝；
- Profile身份不符、成员源码无效和六Stage不完整拒绝；
- 新增、修改、移除、不变的确定性差异；
- 预览零写入、失败零写入和CAS冲突整包回滚；
- 相同提交幂等重试；
- 被移除Draft的历史Revision和Published Release保持可读；
- 显式清空不接受空ZIP替代，并保留全部历史边界。
