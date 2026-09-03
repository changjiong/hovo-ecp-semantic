# ECP Semantic Workspace Package 1.0 / 2.0

文档状态：当前规范说明

日期：2026-08-14

## 1. 目的与权威边界

`ECP Semantic Workspace Package`是交换和导入便利格式：同一个ZIP可以被“本体模型”、“数据映射”和“规则、约束与求值范围”页面使用，每个页面只读取自己拥有的资产。V1保持既有严格合同；V2是为了显式携带`SCOPE`资产而新增的协议版本。两者都不是可执行语义权威，也不绕过Draft Revision、CAS、发布编译或Published Semantic Release。

摘要用于证明包内原始字节、Ontology/Mapping绑定和Schema快照没有在打包后变更；摘要本身不能证明本体语义正确、Mapping与当前本体一致，或Hovo中当前表/字段仍然存在。

## 2. 正式V1布局

ZIP可以直接包含文件，或包含唯一的顶层工作目录。macOS生成的`__MACOSX/`、`.DS_Store`和`._*`元数据会被忽略。业务文件路径使用NFC、正斜杠且不得目录穿越。

```text
manifest.json
ontology/<ontology>.ttl
mapping/<mapping>.json
rules/manifest.json
rules/shacl/<stage>.ttl
rules/derivation/<rule>.json
rules/evaluation/<rule>.json
rules/action-policy/<policy>.json
data-sources/<data-source-code>/schema.json
```

根`manifest.json`必须遵循下载中心的`Semantic Workspace Package Manifest v1 JSON Schema`，并使用：

```json
{
  "schemaVersion": 1,
  "kind": "ECP_SEMANTIC_WORKSPACE_PACKAGE",
  "bundleFormat": "enterprise-cognitive/semantic-workspace-package/1.0.0",
  "semanticProfileId": "enterprise-cognitive/semantic-profile/1.0.0",
  "semanticProfileDigest": "sha256:<profile digest>",
  "ontology": { "path": "ontology/model.ttl", "mediaType": "text/turtle", "sourceDigest": "sha256:<bytes>" },
  "mapping": { "path": "mapping/model.json", "mediaType": "application/json", "sourceDigest": "sha256:<bytes>", "ontologySourceDigest": "sha256:<same ontology bytes>" },
  "ruleSet": { "manifestPath": "rules/manifest.json", "sourceDigest": "sha256:<manifest bytes>" },
  "schemas": [{ "dataSourceCode": "source", "environment": "dev", "path": "data-sources/source/schema.json", "sourceDigest": "sha256:<bytes>" }]
}
```

`rules/manifest.json`仍是严格的Rule Set Bundle v1 Manifest；它的成员路径相对于工作包根目录，例如`rules/shacl/asserted.ttl`。规则页面只把该Manifest登记的规则正文送入规则集替换协议，不会把本体、Mapping、Schema快照或未登记文件误当规则。

## 3. 显式V2与Scope

V1不会接受新增`scopes`字段。需要携带Scope的工作包必须同时使用`schemaVersion: 2`和
`enterprise-cognitive/semantic-workspace-package/2.0.0`，并在根Manifest声明：

```json
{
  "schemaVersion": 2,
  "kind": "ECP_SEMANTIC_WORKSPACE_PACKAGE",
  "bundleFormat": "enterprise-cognitive/semantic-workspace-package/2.0.0",
  "scopes": [
    {
      "assetSeriesId": "scope_enterprise_investigation",
      "path": "scopes/enterprise-investigation.json",
      "mediaType": "application/json",
      "sourceDigest": "sha256:<bytes>"
    }
  ]
}
```

示例省略了仍然必需且与V1相同的Profile、Ontology、Mapping、Rule Set和Schema字段。Scope路径和Series ID必须唯一，文件摘要逐字节复核。规则集替换只处理其规则Manifest登记的四类规则；V2 Scope不会被静默并入Rule Set或批量覆盖既有Scope Draft。当前Admin可在语义配置编辑器中选择解包后的Scope JSON，完成独立源码预检、Revision CAS和Release选择。

Scope格式、运行时边界和企业UBO实例见[`Scoped Semantic Evaluation and Investigation Case v1`](scoped-semantic-evaluation.md)。

## 4. 兼容现有工作目录

为兼容已有Authoring Kit风格目录，若根`manifest.json`本身是有效的`ECP_RULE_SET_BUNDLE`，且同目录还包含唯一的`ontology/*.ttl`、`mapping/*.json`和/或`data-sources/`，系统把它识别为Legacy Workspace Layout：根规则Manifest是唯一规则权威，其他同包资产仅供对应页面读取。`manifest-rules.json`不是正式V1字段，不会覆盖根Manifest；请迁移到正式布局，避免存在两个互相矛盾的规则Manifest。

普通规则ZIP仍必须精确匹配其Manifest；未被识别为工作包时，任何额外业务文件都将失败关闭。

## 5. 页面校验顺序

1. 本体页面从包读取TTL，进行Profile/Projection/源码校验，并以当前所有Draft Head优先、最新Published Release补足缺失Series的候选编译预检；候选TTL自身有效即可追加新的Ontology Draft。若旧Mapping/规则仍不兼容，页面显示后续导入提示而不是把版本迁移卡死；
2. Mapping页面从包读取JSON，校验包内声明与当前Ontology Draft的精确摘要、完整语义候选，并从Hovo重新发现当前表、View和字段；候选Mapping自身及当前Hovo结构有效即可追加Mapping Draft，跨资产候选编译诊断必须在发布前清零；
3. 规则页面对规则Manifest、成员摘要和Profile执行服务端ZIP安全校验；V2 Scope只做声明和摘要复核，不进入规则集替换；
4. Scope编辑器按独立Asset Series执行闭合JSON与Release上下文预检；
5. 任何保存只创建不可变Revision并CAS推进Draft Head；导入的次序可以短暂形成不可发布Draft，方便把同一个工作包的Ontology、Mapping与规则逐项替换。发布时对选定精确Revision再次完整编译；运行时Snapshot或Scoped Fact Bundle仍检测Schema和身份漂移。

同一个工作包在三个页面分别导入时，页面仍只持久化自己拥有的资产；但规则页会读取同包Ontology/Mapping的摘要作为候选闭包诊断。若包内规则引用的IRI（例如`urn:…:v2:WeightedOwnershipPath`）与当前Ontology Draft中的同名但不同IRI（例如`urn:…:v1:WeightedOwnershipPath`）不一致，规则不会被写入。提示会明确列出包内与当前Draft的路径、摘要和IRI；应从同一ZIP依次保存Ontology、Mapping、再保存规则，而不是在Release窗口手工猜测SHACL Stage或忽略摘要不一致。

包中的`data-sources/*/schema.json`是可审阅的Schema快照，不携带连接信息，也不能替代当前Hovo发现或运行期Snapshot校验。
