# 输出合同

## 1. 最小化原则

用户只要一个资产，就只生成该资产和必要报告；不要为了形式完整创建空目录或无业务意义的规则。

## 2. 推荐工作目录

多资产任务：

```text
<project>/
├── design/
│   ├── 00-scope.md
│   ├── 10-competency-questions.md
│   ├── 20-knowledge-elicitation.md
│   ├── 30-conceptual-model.md
│   └── 40-asset-plan.md
├── ecp-workspace/
│   ├── manifest.json
│   ├── ontology/
│   ├── mapping/
│   ├── rules/
│   ├── scopes/                  # 仅 V2
│   └── data-sources/
└── reports/
    ├── authoring-report.md
    └── ecp-validation.json
```

`design/` 与 `reports/` 不进入正式 ECP Workspace ZIP；打包脚本只压缩 `ecp-workspace/` 中受合同管理的内容。

## 3. Authoring Report（编写报告）

至少记录：目标任务；输入材料；范围；Competency Questions（能力问题）；关键概念化决策；生成资产清单；未生成资产及理由；缺失输入；本地验证状态；需要 ECP 平台预检的内容；Full Replacement、Scope、Action 等风险提醒。

## 4. 状态词

只使用：`INVALID`、`NEEDS_INPUT`、`LOCALLY_VALID`、`ECP_PREFLIGHT_REQUIRED`、`ECP_PREFLIGHT_VALID`、`RELEASE_READY`。

其中后三个必须有对应外部 ECP 证据，不能由语言模型推测。

## 5. 单资产输出

Ontology：

```text
ontology/model.ttl
reports/authoring-report.md
reports/ecp-validation.json
```

Mapping：必须同时引用精确 Ontology TTL 或明确提供其 Source Digest。

Evaluation：没有真实 compilerContract 时只能输出 `*.draft.json`，并明确非导入资产。

## 6. 工作包输出

只有以下条件满足后才生成正式 `.zip`：根 manifest 能通过对应 v1/v2 JSON Schema；Ontology Profile 本地静态检查通过；Mapping/Action/Scope 等有公开 Schema 的资产通过 JSON Schema；所有路径和 SHA-256 摘要正确；Rule Set Manifest 与成员一致；六阶段 SHACL 完整（如使用）；无敏感配置或任意代码；无未完成 Evaluation Draft 被错误登记为正式规则。

即使 ZIP 生成成功，默认状态仍最多是 `LOCALLY_VALID` 或 `ECP_PREFLIGHT_REQUIRED`。

## 交互与不确定性报告

任何 design/generate/repair 任务的报告应在存在对应项时包含：

- `confirmed_facts`：已确认事实及来源；
- `inferences`：推定及依据；
- `assumptions`：采用的可逆假设及影响范围；
- `open_decisions`：高影响待决策项；
- `blocked_assets`：被缺失输入局部阻塞的资产及其下游；
- `clarification_budget_used`：本次是否触发 Decision Gate、问题数量。

默认模式不得把非阻塞的 `OPEN` 或 `BLOCKED` 扩散为整个任务停止。若没有 `OPEN`，不得为了“确认一下”而主动打断用户。
