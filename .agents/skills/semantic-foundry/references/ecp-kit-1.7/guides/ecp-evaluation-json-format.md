# ECP 评估规则 JSON 编写指南

文档版本：Evaluation Asset V1 / Evaluation Definition V1

评估规则对本体对象运行有限 Typed Plan，并生成对象级结果、证据与可审计投影。

## 外层 Envelope

- `apiVersion`：`enterprise-cognitive/evaluation-asset/v1`
- `kind`：`EvaluationAsset`
- `definition`：Evaluation Definition V1 正文
- `compilerContract.contractVersion`：固定为 `enterprise-cognitive/evaluation-compiler-contract/v1`
- `compilerContract.source`：必须是 `semantic-asset:<Rule Series ID>`
- `compilerContract.expect`：必须列出有限编译器对该规则产生的语义投影；字段不能缺失、增加或使用占位值。旧版 Kit 有两项受限兼容：可省略由 Definition 中 `materialEvidence.*.canonical` 直接派生的`decimalProjectionPolicies`；`factDependencies`可遗漏后来补充的用途标记，但谓词集合必须完全一致且已声明用途必须精确匹配。实际依赖始终由 Definition 编译，不能被合同削弱。

## Definition 要点

- `metadata.id` 应稳定且与 Series 语义一致。
- `spec.severity` 使用系统支持的严重级别。
- `spec.rule.kind` 固定为 `typedPlan`。
- `clockBasis` 明确使用评估日期等有限时钟来源。
- `coveragePolicy` 不得绕过 Source Coverage。
- `objectScope.anchorOperatorId` 指向候选对象算子。
- `spec.rule.parameters` 仅在规则使用 `Param` 表达式时提供；无参数的固定规则可省略，编译器会规范化为空映射。引用未声明参数仍会失败关闭。
- `identity` 定义稳定结果身份维度。
- `projection` 定义输出 Class、Scope、对象关联、证据和 trace。
- `lifecycle.profileEvidence` 定义生命周期证据；没有额外证据时使用空对象。
- `tests.cases` 是非空测试合同标识；数据库 Revision 不会从该路径加载可执行代码。

修改 Definition 的算子、依赖、身份、投影或生命周期后，必须同步更新 `compilerContract.expect`，并以页面“只预检”的结果为准。Compiler Contract 不是可省略的注释，也不接受 `null` 摘要占位。

## 字符串 Compare

`Compare`支持`EQ/NE/LT/LTE/GT/GTE/CONTAINS/STARTS_WITH`。其中`CONTAINS`和`STARTS_WITH`的左右
表达式必须都由编译器静态判定为`string`；不能对IRI、Decimal、日期、布尔值或集合使用，也不会在Runtime
执行隐式字符串转换。两种算子先对左右值执行Unicode NFC规范化，再进行区分大小写的精确比较；不Trim、
不做Locale Case Folding、不解释通配符或正则表达式。空右值遵循精确字符串语义，因此两种比较都返回
`true`。Feature与Evaluation使用同一实现和同一Golden合同。

`NE/CONTAINS/STARTS_WITH`要求Compiler Contract中的`operatorSetVersion`为
`enterprise-risk-operators/1.5.0`。历史Published Revision若仍固定为1.4，可以继续由当前Runtime按1.4
子集执行，但不能在原合同下使用这三个算子；请通过页面预检重新生成Expectation，保存为新的Revision并发布
新的Semantic Release。不要只手工修改版本字符串，因为完整Expectation仍会逐字段精确校验。

```json
{
  "op": "Compare",
  "operator": "STARTS_WITH",
  "left": { "op": "Var", "name": "eventTitle" },
  "right": { "op": "String", "value": "风险-" }
}
```

## 不要混淆两种 Scope

Evaluation中的`objectScope`和`projection.scope`描述“对哪个语义对象求值”以及结果身份字段；Release中的
`SCOPE`资产描述“从哪个关系型Root出发，如何完整读取局部事实闭包”。前者属于Evaluation Definition，后者
是独立`Scope Definition v1`，二者不能互相替代。

同一Evaluation会被完整Run和Scoped Evaluation复用。不要在Evaluation中写Root Record Key、Scan/Join、
Fact Provider或资源预算；若规则新增事实依赖，应分别更新Mapping和必要的Scope Revision，再对完整Release
执行编译。Case Revision产生的局部Change只用于调查比较，不进入全局Lifecycle或Action。

## 最小示例

```json evaluation-example
{
  "apiVersion": "enterprise-cognitive/evaluation-asset/v1",
  "kind": "EvaluationAsset",
  "definition": {
    "apiVersion": "enterprise-cognitive/evaluation-definition/v1",
    "kind": "EvaluationDefinition",
    "metadata": {
      "id": "customer_review",
      "version": "1.0.0",
      "name": "客户复核",
      "description": "识别需要复核的客户",
      "category": "urn:example:ontology:ReviewCategory",
      "status": "active"
    },
    "spec": {
      "severity": "MEDIUM",
      "rule": {
        "kind": "typedPlan",
        "clockBasis": "evaluationDate",
        "coveragePolicy": "REQUIRE_COMPLETE_SOURCE_COVERAGE",
        "objectScope": { "anchorOperatorId": "candidate" },
        "parameters": {
          "ruleVersion": { "op": "String", "value": "v1" }
        },
        "operators": [
          {
            "id": "scan",
            "op": "ScanClass",
            "class": "urn:example:ontology:Customer",
            "bind": "customer"
          },
          { "id": "candidate", "op": "ProjectCandidate", "input": "scan" }
        ]
      },
      "identity": {
        "revision": 1,
        "dimensions": {
          "customer": { "value": { "op": "Var", "name": "customer" }, "type": "string" }
        }
      },
      "projection": {
        "ontologyClass": "urn:example:ontology:CustomerReview",
        "scope": {
          "type": "Customer",
          "fields": {
            "customer": { "value": { "op": "Var", "name": "customer" }, "type": "string" }
          }
        },
        "aboutObjectIris": { "value": { "op": "Var", "name": "customer" }, "type": "stringSet" },
        "materialEvidence": {
          "ruleVersion": {
            "value": { "op": "Param", "name": "ruleVersion" },
            "type": "string"
          }
        },
        "trace": { "supportingFactIds": { "value": { "op": "SupportIds" }, "type": "stringSet" } },
        "enrichment": {}
      },
      "lifecycle": { "profileEvidence": {} },
      "tests": { "cases": "embedded-evaluation-contract.json" }
    }
  },
  "compilerContract": {
    "contractVersion": "enterprise-cognitive/evaluation-compiler-contract/v1",
    "source": "semantic-asset:customer_review",
    "expect": {
      "valid": true,
      "definitionId": "customer_review",
      "definitionVersion": "1.0.0",
      "definitionStatus": "active",
      "categoryIri": "urn:example:ontology:ReviewCategory",
      "severity": "MEDIUM",
      "implementationKind": "typed-operators",
      "operatorSetVersion": "enterprise-risk-operators/1.5.0",
      "dependencyMode": "staticTypedPlan",
      "coveragePolicy": "REQUIRE_COMPLETE_SOURCE_COVERAGE",
      "objectScopeAnchor": "candidate",
      "operatorSequence": ["ScanClass", "ProjectCandidate"],
      "identityRevision": 1,
      "identityDimensions": ["customer"],
      "scopeType": "Customer",
      "materialEvidenceFields": ["ruleVersion"],
      "traceFields": ["supportingFactIds"],
      "enrichmentFields": [],
      "contextDependencies": ["evaluationDate"],
      "semanticViewDependencies": [],
      "factDependencies": [
        {
          "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
          "purposes": ["condition", "identity", "scope", "trace"]
        }
      ],
      "evaluationProfile": "ECP_EVALUATION_OUTPUT_V1",
      "aboutTargetField": "aboutObjectIris",
      "profileEvidenceFields": []
    }
  }
}
```

示例中的 `Customer`、`CustomerReview` 和 `ReviewCategory` 必须在同一候选 Ontology 中分别声明为输入 Class、输出 Class 和 Evaluation Category。保存时系统会检查 JSON 结构；整体发布时还会检查 Ontology 引用、有限算子、类型、Scope、Coverage 和 Compiler Contract 的逐字段一致性。
