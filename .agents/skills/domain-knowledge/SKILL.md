---
name: domain-knowledge
description: 接收 PDF、DOCX、扫描件等原始业务材料，经 MinerU（文档解析器）和 Semantic Document IR（语义文档中间表示）形成 SourceUnit（来源单元），再通过显式四阶段 Knowledge Formation（知识形成）流水线生成平台无关的企业领域知识。Statement（来源陈述）先于 Question（业务问题）和 Term/Rule（业务概念/业务规则）；高影响 Rule 必须通过语义深度、颗粒度、反事实和冲突审查。保留来源、专家认知、机构作业口径、真实案例、冲突与未知；不设计领域模型，不编制 ECP 资产或数据映射。
metadata:
  author: Hovo
  version: "1.4.0"
---

# 领域知识形成

目标是把“业务材料”转成**业务专家能够理解、复述、质疑、确认，并能直接用于后续领域建模的企业认知知识**。

最终正式真相源仍是 `output.json`。但是从 `SourceUnit` 到 `output.json` 不再允许一次性黑盒生成，必须经过可回放的四阶段 Knowledge Formation。

## 核心对象地位

- **Statement（来源陈述）**：材料实际表达了什么，是来源文本和企业知识之间的语义桥梁。
- **Question（业务问题）**：知识发现、导航和完整性检查轴，不是领域知识主体。
- **Term（业务概念）**：跨来源稳定的业务概念、边界、实例和反例。
- **Rule（业务规则）**：领域知识主体；表达可独立影响业务判断的稳定知识。
- **Case（案例）**：用于验证、证伪和校准 Rule；不能循环证明本次生成的规则。
- **Issue（缺口/冲突）**：不能可靠闭合的知识必须显式保留。
- **ProvisionCoverage（条款覆盖）**：证明材料有没有处理，不证明知识是否充分。

## 总体流水线

```text
原始 PDF / DOCX / 扫描件
        ↓
document-intake / MinerU
        ↓
SourceBlock
        ↓
document-normalizer
        ↓
SourceUnit
        ↓
────────────────────────────
Knowledge Formation
────────────────────────────
        ↓
① Statement Pass
        ↓
Statements
        ↓
② Question Discovery
        ↓
Questions + QuestionDiscovery
        ↓
③ Knowledge Synthesis
        ↓
Terms + Rules + Cases + Issues
        ↓
④ Knowledge Audit
        ↓
Coverage + Contradiction + Gap + Semantic Quality
        ↓
knowledge_formation.py assemble
        ↓
output.json
        ↓
render_documents.py
        ↓
review.md / coverage.md
```

LLM（大语言模型）负责语义理解、归并、解释、反例和冲突分析。Python 只负责 pass 状态、合同、引用闭包、确定性组装和门禁；不得在 Python 中重写业务知识。

## 第一层：Document Understanding

PRODUCE/REVISE 先经过 [document-intake](modules/document-intake/README.md) 和 [document-normalizer](modules/document-normalizer/README.md)。

MinerU block 边界不是知识抽取边界。document-normalizer 先做确定性结构恢复，仅对模糊边界使用 Jev Choice，最终得到 SourceUnit。每个保留 SourceBlock 必须且只能归属一个 SourceUnit；上下文可帮助理解，但不能改变 Statement 的真实来源归属。

这一层只回答：

> **原文是什么结构？**

它不产生 Term、Rule 或机构口径。

## 第二层：Knowledge Formation

详细协议见 [knowledge-formation](modules/knowledge-formation/README.md)。

### Pass 1 — Statement Extraction

必须逐 SourceUnit 处理。

一个 SourceUnit 可产生 0、1 或多个 Statement；0 个时必须说明是无业务含义、范围外、不可读等哪一种原因。

Statement 应按业务含义拆分，不按段落机械压成一句。例如同一条“实际控制”条款中的：

- 人事任免；
- 重大经营管理决策；
- 财务收支；
- 重要资产/主要资金支配；
- 单独/联合控制；

如果会独立影响判断，就不能只抽成一句“存在实际控制”。

**禁止从 SourceUnit 直接跳到 Rule。**

### Pass 2 — Question Discovery

必须独立执行两个方向：

1. **Source → Question**：从 Statement 的定义、义务、条件、例外、证据、时间发现业务问题；
2. **Business Process → Question**：从参与者、阶段、判断、缺证、冲突、变化、确认、结束条件补查问题。

不得先写最终问题清单，再反填 QuestionDiscovery。

问题文字相近不是合并理由；只要前提、结果、证据、缺证或时间会独立改变结论，就应保留独立问题或明确子问题。

### Pass 3 — Knowledge Synthesis

此时才允许形成 Term / Rule / Case / Issue。

Knowledge Synthesis 只做三件事：

1. 明确本主题要帮助业务人员作出什么判断；
2. 按业务判断顺序，把分散依据组织成“适用条件 → 关键事实 → 事实如何影响结论 → 证据与非充分线索 → 缺证/冲突/时间/人工边界”的完整说明；
3. 用正例、反例或缺证情形检查：关键事实变化后，这份知识能否解释结论为什么变化或暂时不能作出。

Questions 只用于范围组织和覆盖检查，不能作为 Rule 的依据。Statements 是语义索引，不是原文替代品；涉及适用范围、例外、时间、歧义或来源冲突时，应回看可获得的 SourceUnit / 原文必要上下文，输入不足则形成 Issue，不得静默补造。

Rule 必须标记三类企业知识之一：

- `NORMATIVE`：规范规则；
- `INTERPRETIVE`：解释规则；
- `OPERATING_POLICY`：机构作业规则。

这与 `origin=SOURCE_STATED/INFERRED/PROPOSED`、`review_status` 分属不同维度。

Rule 的粒度原则：

> **一个 Rule 承载一个可以独立理解、应用和维护的完整业务判断，并保留判断内部必要的条件分支。只有适用范围、业务用途或治理/维护依据确实独立时，才拆成不同 Rule。**

简单判断允许很短；复杂判断必须充分展开。禁止用“查明事实”“缺证待核”等模板句替代真实的业务判断，也禁止为了增加 Rule 数量机械拆分条件分支。

### Pass 4 — Knowledge Audit

这是独立语义审查，不重新生成另一份知识。

必须检查：

1. Source → Knowledge Coverage；
2. Knowledge → Source Support；
3. Rule Granularity；
4. Semantic Depth；
5. Counterfactual；
6. Contradiction；
7. Case Independence。

以下 finding 为发布阻断：

- `IMPACT_UNDERCLASSIFIED`
- `SEMANTIC_DEPTH_INSUFFICIENT`
- `RULE_SPLIT_REQUIRED`
- `COUNTERFACTUAL_FAILED`
- `UNRESOLVED_CONTRADICTION`
- `SYNTHETIC_CASE_CIRCULAR_SUPPORT`

Audit BLOCKED 时，`knowledge_formation.py assemble` 必须拒绝生成正式 `output.json`。

## 高影响 Rule 的最低语义深度

`impact=HIGH` 的 Rule 除七要素外，必须具有：

- `business_conclusion`
- `required_facts[]`
- `decision_steps[]`
- `evidence_requirements[]`
- `non_sufficient_facts[]`
- `unknown_behavior`
- `human_boundary`
- `case_ids[]`

高影响 Rule 必须达到：

> 业务专家不重新阅读原法规，也能够据此解释正常案例、边界案例和缺证案例。

“查明事实”“缺证待核”“满足条件则通过”不构成语义充分性。

## 企业认知作为正式输入

fresh run 只是不继承旧生成产物，不得遗忘已经正式纳入输入的企业认知。

调用项目建议按以下目录组织：

```text
01业务输入/
├─ 00业务问题.md
├─ 01制度原文/
├─ 02专家确认口径/
├─ 03真实案例与校准/
└─ 04同业实践材料/
```

它们全部走正常 document-intake → SourceUnit → Statement 主链，不走旁路。

SourceRef.source_role 用于区分：

- `NORMATIVE_RULE`
- `OFFICIAL_GUIDANCE`
- `BUSINESS_SCOPE`
- `INSTITUTION_POLICY`
- `EXPERT_KNOWLEDGE`
- `CASE_EVIDENCE`
- `SYSTEM_INTERFACE`
- `SECONDARY_CONTEXT`

因此：

> **fresh output ≠ fresh brain**

已经正式沉淀的专家知识、机构政策和真实案例不会因为重新生成 output.json 而消失。

## Case 的来源与责任

Case 必须区分：

- `REAL_CONFIRMED`：真实且已经确认；必须绑定 CASE_EVIDENCE 来源与真实确认记录；
- `SOURCE_CASE`：来源材料案例；
- `SYNTHETIC_PROBE`：合成测试案例。

验证角色：

- `SUPPORT`
- `COUNTEREXAMPLE`
- `BOUNDARY`
- `MISSING_EVIDENCE`

每个 Case 必须通过 `rule_ids` 指向所验证规则。

`SYNTHETIC_PROBE` 只能测试、找反例和暴露缺口；不得成为规则权威依据。

## 文档覆盖与知识覆盖分开

**Document Coverage** 回答：

> 所有 SourceBlock / SourceUnit 是否被读取、定位、处理？

**Knowledge Coverage** 回答：

> 业务问题是否有知识回答、明确未决或明确范围外？重要知识是否有足够深度？

二者不能互相替代。

全部 SourceUnit 有 ProvisionCoverage，不代表领域知识完整。

## 中间工件

调用项目保存：

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

中间工件用于回放和失败定位；最终业务知识真相源仍为通过 v5 合同的 `output.json`。

## 交付

`review.md` 给业务专家阅读；`coverage.md` 给审计和知识工程追溯；`output.json` 给下游机器消费。

高影响 Rule 在 review.md 中按认知复杂度展开，不要求每条规则固定相同篇幅。

render_documents.py 只负责确定性展示，不得补充 output.json 中不存在的业务结论。

## 完成边界

一个范围可以保留明确 OPEN，但至少满足：

1. 所有 SourceUnit 已经过 Statement Pass 或明确说明无业务含义/范围外/不可读；
2. Question Discovery 同时完成来源路径和业务流程路径；
3. Term / Rule 均能回到 Statement，再回到 SourceUnit；
4. NORMATIVE / INTERPRETIVE / OPERATING_POLICY 未混写；
5. HIGH Rule 全部通过语义深度、颗粒度、反事实和冲突审查；
6. Case 来源和验证角色清楚，合成案例不循环自证；
7. ProvisionCoverage 和 Knowledge Coverage 分开报告；
8. fresh run 不丢失正式输入的 EXPERT_KNOWLEDGE / INSTITUTION_POLICY / CASE_EVIDENCE；
9. Knowledge Audit 为 PASS；
10. 业务确认与结构 PASS 分开记录，脚本 PASS 不替代领域责任人确认。

完成本技能后结束，不自动启动 domain-model。Domain Model 只能消费固定、已审阅的领域知识，不得重新阅读法规补业务规则。

## 合同边界

Domain Knowledge 当前内部 normalized input / output 使用 **Contract 5.0.0**，与旧 4.0.0 不兼容，不提供隐式迁移或兜底。

对外 raw-document request 仍使用 Request Contract 2.0.0；Semantic Document IR 仍为 2.1.0。
