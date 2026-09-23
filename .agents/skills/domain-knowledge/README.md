# domain-knowledge

从 PDF、DOCX、扫描件等原始业务材料出发，形成业务人员能独立阅读、审查并用于需求访谈的《领域业务知识说明书》和结构化领域知识。Hovo 1.4.0，本地候选。用户请求合同 2.0.0，Semantic Document IR（语义文档中间表示）2.1.0，内部规范化输入与领域知识输出合同 5.0.0，Knowledge Formation（知识形成）协议 1.0.0。

> 使用 domain-knowledge，依据这些材料形成业务知识说明书，讲清概念、判断依据和案例，并列出下次需求访谈需要确认的问题。

> 使用 domain-knowledge，审查这份尚未确认的知识说明，列出缺少依据和需要访谈的事项。

## 输入与交付

创建只需要业务目标、使用者和原始 PDF/DOCX/扫描件等 documents；审查只需要已有文件；修订需要原成果、变更请求和新增/变更 documents。PRODUCE/REVISE 由内部 `document-intake` 调用已配置外部解析服务，保留 `SourceBlock`；随后 `document-normalizer` 先按确定性结构规则重建，只有模糊边界才调用 Jev（判断模型）的 `Choice（选择）`，形成 `SourceRef + source_blocks + boundary_decisions + source_units + source_extractions` 的 Semantic Document IR（语义文档中间表示）。知识形成只以 SourceUnit 作为知识归属边界，SourceBlock 只用于精确溯源。随后强制经过 Statement Pass → Question Discovery → Knowledge Synthesis → Knowledge Audit 四阶段；Agent 不再允许从整个 input.json 一步生成 output.json。用户不需要构造这些内部对象。Skill 不内置 OCR/PDF/DOCX 解析库。

创建或修订首先交付 `review.md`。文档开头先给出领域认知速览：业务目标、核心概念导航、核心业务规则和按业务主题组织的问题框架；随后再展开规则边界、案例验证、访谈确认和来源依据。**Question（业务问题）用于知识发现、导航和覆盖检查，Term（业务概念）与 Rule（业务规则）才是知识主体。**来源覆盖、问题清洗和编号索引属于追溯信息，不作为业务理解的前置步骤。业务人员无需阅读 JSON、理解技术编号或掌握平台知识。全量来源单元、原文陈述、问题发现过程和案例台账放在 `coverage.md`；`output.json` 保存同一业务知识基线。文档覆盖与知识覆盖分别验收，不能用“全部 SourceUnit 已登记”证明业务知识完整。

审查已有文件时交付《领域业务知识审查意见》，列清原文、问题、业务影响、建议和限制。业务认可依赖真实确认记录。具体内容见 [业务交付要求](references/business-delivery.md)，成品阅读样式见 [设备维护示例](examples/equipment-maintenance.md)，完成条件见 [验收清单](references/acceptance.md)。

## 独立使用与检查

完整目录可放入宿主支持的 skills 目录单独调用。本包不依赖其他语义工程技能或 ECP 平台；PRODUCE/REVISE 需要可访问的 MinerU 4.x V1 API 与 TypeSafe Jev API。Python 3.10+ 依赖见 [requirements.txt](requirements.txt)，不包含 OCR/PDF/DOCX 解析库。在本技能目录运行：

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt

# 1. 用户/编排请求：原始文档
.venv/bin/python scripts/validate_contract.py validate request /path/to/project/domain-knowledge/request.json --project-root /path/to/project

# 2. Skill 内部 document-intake：调用 MinerU V1，生成规范化内部输入
export MINERU_API_URL=https://mineru.example
export MINERU_API_KEY=***
export TYPESAFE_API_KEY=***
export DOMAIN_KNOWLEDGE_JEV_MIN_CONFIDENCE=0.90
export DOMAIN_KNOWLEDGE_MINERU_TIER=standard
export DOMAIN_KNOWLEDGE_MINERU_OCR_MODE=auto
.venv/bin/python modules/document-intake/document_intake.py /path/to/project/domain-knowledge/request.json --project-root /path/to/project --output /path/to/project/domain-knowledge/input.json

# 3. 后续沿用既有知识形成合同
.venv/bin/python scripts/validate_contract.py validate input /path/to/project/domain-knowledge/input.json --project-root /path/to/project
.venv/bin/python scripts/render_documents.py /path/to/project/domain-knowledge/output.json --project-root /path/to/project
.venv/bin/python scripts/validate_contract.py validate output /path/to/project/domain-knowledge/output.json --project-root /path/to/project
```

`document_intake.py` 已按 MinerU 4.x V1 upload / parse-job / file-content 流程接入，并固定消费 `structured_content`。`middle_json` 仅用于调试，不进入正常知识形成。MinerU 输出先保留为 SourceBlock，再由 [document-normalizer](modules/document-normalizer/README.md) 执行 L1 deterministic reconstruction（确定性结构重建）；仅真实模糊边界交给 [boundary-repair](modules/boundary-repair/README.md) 的 Jev `Choice（选择）`。低置信度结果记录为 `UNRESOLVED（未解决）`，不静默猜测；固定 token（词元）分块和 overlap（重叠）不作为语义边界。`render_documents.py` 仍只把既有知识内容投影为双文档并更新摘要。内部协议见 [Semantic Document IR](references/semantic-document-ir.md)。

## 排查与证据

缺少 `review.md` 或 `coverage.md`、文档版本不一致或正文定位遗漏时，补齐真实业务内容并更新附件中的摘要，不能只补空锚点。概念或判断解释不清时按 [审阅方法](references/review-guide.md) 修订；案例预期变化应退回知识责任人确认。

本地检查现在会分别报告 sourceUnitCoverage、statementPass、questionDiscovery、knowledgeSynthesis、semanticAudit、ruleDepth、caseValidation 与 knowledgeCoverage；这些状态仍不证明来源真实或实际业务读者已认可。知识完成以“业务问题有去向、核心概念/规则有依据、关键歧义获必要确认、案例能够校准边界”为准；SourceUnit 数量、候选问题数量和合成案例数量都不是完成指标。作者自查、业务读者复述和领域责任人确认分别记录；未开展的审阅保留待验证。旧报告只证明所列旧版本。资料快照见 [sources.json](references/sources.json)，权利与方法借鉴见 [来源说明](THIRD_PARTY_NOTICES.md)。
