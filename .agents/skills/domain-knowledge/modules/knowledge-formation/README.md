# Knowledge Formation

把 `SourceUnit（来源单元） → output.json（结构化领域知识）` 从一次性 Agent 黑盒改为四个可检查、可中断、可恢复的认知阶段。

## 责任边界

- LLM（大语言模型）负责业务语义理解、归并、解释、反例和冲突分析。
- Python 只负责 pass 状态、合同校验、引用闭包、确定性组装和发布门禁。
- 本模块不重新解析 PDF/DOCX，不改变 SourceUnit，不设计 Domain Model，不调用 ECP。
- `output.json` 仍是正式知识真相源；`process/knowledge-formation/*` 是可回放的形成证据，不是第二套知识基线。

## 四个强制 Pass

```text
SourceUnit
   ↓
01 Statement Pass
   ↓
Statements
   ↓
02 Question Discovery
   ↓
Questions + QuestionDiscovery
   ↓
03 Knowledge Synthesis
   ↓
Terms + Rules + Cases + Issues
   ↓
04 Knowledge Audit
   ↓
ProvisionCoverage + CaseCoverage + Semantic Audit
   ↓
knowledge_formation.py assemble
   ↓
output.json
```

前一 Pass 未通过 schema 和确定性引用检查时，不进入后一 Pass。Agent 不得跳过中间工件直接写完整 `output.json`。

## 调用项目目录

```text
domain-knowledge/
├─ input.json
├─ output.json
├─ review.md
├─ coverage.md
└─ process/
   └─ knowledge-formation/
      ├─ manifest.json
      ├─ 01-statements.json
      ├─ 02-questions.json
      ├─ 03-synthesis.json
      └─ 04-audit.json
```

## Fresh 的定义

`fresh` 只表示不继承旧的**生成产物**。已经作为正式输入纳入 SourceRef 的以下企业认知不得因为 fresh run 丢失：

- `EXPERT_KNOWLEDGE`：已沉淀专家认知；
- `INSTITUTION_POLICY`：机构正式作业口径；
- `CASE_EVIDENCE`：真实案例与校准材料；
- `BUSINESS_SCOPE`：业务目标、流程和问题范围。

这些材料仍走 SourceUnit → Statement → Knowledge Formation 主链，不走旁路。

## Rule 的三个知识类别

- `NORMATIVE`：法规、规章、正式制度直接规定的规范规则。
- `INTERPRETIVE`：对规范、证据、缺证、时间和边界的可复核业务解释。
- `OPERATING_POLICY`：机构经授权采用的作业、人工边界、自动化或风险处理口径。

`rule_class`、`origin`、`review_status` 是三个不同维度，不得合并成“置信度”。

## 语义质量门禁

对 `impact=HIGH` 的 Rule，Knowledge Audit 必须检查：

1. 需要哪些业务事实；
2. 判断步骤是否可复述；
3. 哪些事实不足以证明结论；
4. 缺证时是 UNKNOWN、BLOCK 还是其他明确处理；
5. 时间何时成立/失效；
6. 自动判断与人工判断边界；
7. 至少一个案例是否能检验规则；
8. 改变关键事实时，规则是否能解释结果变化。

出现以下 blocking code 时不得 assemble：

- `IMPACT_UNDERCLASSIFIED`\n- `SEMANTIC_DEPTH_INSUFFICIENT`
- `RULE_SPLIT_REQUIRED`
- `COUNTERFACTUAL_FAILED`
- `UNRESOLVED_CONTRADICTION`
- `SYNTHETIC_CASE_CIRCULAR_SUPPORT`

## 合同

Domain Knowledge v5 是 breaking contract，不接受 4.0.0 产物作为当前输出。旧成果只归档，不做隐式兼容。Domain Model 的适配另开 PR。
