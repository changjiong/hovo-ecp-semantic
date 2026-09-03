# ECP 动作策略 JSON 编写指南

文档版本：Action Policy V1

动作策略把已提交语义变化转换为有限能力调用意图。策略只声明能力、操作和参数来源，不包含下游地址、凭据或可执行脚本。

## 必要结构

- `apiVersion`：固定为 `enterprise-cognitive/action-policy/v1`
- `kind`：固定为 `ActionPolicy`
- `metadata.policyId`：稳定策略 ID
- `metadata.policyVersion`：策略版本
- `metadata.status`：例如 `ACTIVE`
- `trigger`：受支持的语义变化触发器
- `actions`：一个或多个有限动作声明

`executorBindingRef` 只引用服务端部署绑定。Endpoint、Secret、Bucket 或本地路径不得进入语义资产。

## 示例

```json action-policy-example
{
  "apiVersion": "enterprise-cognitive/action-policy/v1",
  "kind": "ActionPolicy",
  "metadata": {
    "policyId": "notify_customer_review",
    "policyVersion": "1.0.0",
    "status": "ACTIVE"
  },
  "trigger": {
    "kind": "SEMANTIC_CHANGE",
    "changeKinds": ["ADDED"],
    "predicateIris": ["urn:example:ontology:reviewStatus"]
  },
  "actions": [
    {
      "actionId": "notify",
      "capabilityIri": "urn:ecp:capability:notification",
      "operation": "send",
      "executorBindingRef": "notification_v1",
      "arguments": [
        { "name": "workspaceId", "source": "WORKSPACE_ID" },
        { "name": "runId", "source": "RUN_ID" },
        { "name": "changeSemanticId", "source": "CHANGE_SEMANTIC_ID" }
      ]
    }
  ]
}
```

## 安全与确定性

- 只使用合同列出的 Trigger、Change Kind、Argument Source 和 Operation。
- 不写 HTTP URL、Header、Token、密码或重试脚本。
- 同一变化和动作必须产生稳定 Intent Identity，以支持幂等投递。
- 下游连接和凭据由部署配置解析，不参与 Semantic Digest。
- Semantic Investigation不会执行Lifecycle或Action Policy，也不会创建Intent/Outbox。不要编写依赖Case
  Revision或局部Change触发外部动作的策略；需要真实动作时，先把已核实事实写回源系统，再执行完整Run。
