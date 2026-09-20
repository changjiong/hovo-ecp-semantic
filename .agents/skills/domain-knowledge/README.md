# domain-knowledge

将业务材料整理成业务人员能独立阅读、审查并用于需求访谈的《领域业务知识说明书》。Hovo 0.9.1，本地候选，结构化资产合同 4.0.0。

> 使用 domain-knowledge，依据这些材料形成业务知识说明书，讲清概念、判断依据和案例，并列出下次需求访谈需要确认的问题。

> 使用 domain-knowledge，审查这份尚未确认的知识说明，列出缺少依据和需要访谈的事项。

## 输入与交付

创建需要业务目标、使用者以及上游已结构化的来源资料；审查只需要已有文件；修订需要原成果、变更请求和依据。创建与修订从 `SourceRef + source_units + source_extractions` 开始，再为每个单元形成唯一 `provision_coverage`。原始 PDF/DOCX、OCR、版面和表格解析由上游文档结构化服务负责，本技能不内置生产解析器。文件级来源登记不能替代来源单元覆盖。

创建或修订首先交付 `review.md`。文档开头先给出领域认知速览：业务目标、核心概念导航、按业务主题组织的主线和推荐阅读路径；随后再展开概念与边界、逐个问题的判断解释、案例、访谈确认清单和来源依据索引。来源覆盖、问题清洗和编号索引属于追溯信息，不作为业务理解的前置步骤。业务人员无需阅读 JSON、理解技术编号或掌握平台知识。全量覆盖台账、陈述、案例与候选问题去向放在 `coverage.md`；`output.json` 是同一成果的结构化记录。问题由原文含义和业务流程两路发现，不预设问题数量。原文摘录、材料映射、语义审查和业务确认分别记录。

审查已有文件时交付《领域业务知识审查意见》，列清原文、问题、业务影响、建议和限制。业务认可依赖真实确认记录。具体内容见 [业务交付要求](references/business-delivery.md)，成品阅读样式见 [设备维护示例](examples/equipment-maintenance.md)，完成条件见 [验收清单](references/acceptance.md)。

## 独立使用与检查

本技能不依赖其他语义工程技能或 ECP 平台，但不再是“只复制 skill 目录即可运行”的完全自包含包：合同校验还需要仓库级 `contracts/document-structure/v1` 共享合同。部署/分发时必须同时携带共享合同目录。PRODUCE/REVISE 的文档内容由上游结构化文档服务或调用方按该合同提供。Python 3.10+ 依赖见 [requirements.txt](requirements.txt)。在本技能目录运行：

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python scripts/render_documents.py /path/to/project/domain-knowledge/output.json --project-root /path/to/project
.venv/bin/python scripts/validate_contract.py --check-schemas
.venv/bin/python scripts/validate_contract.py validate input /path/to/project/domain-knowledge/input.json --project-root /path/to/project
.venv/bin/python scripts/validate_contract.py validate output /path/to/project/domain-knowledge/output.json --project-root /path/to/project
```

`render_documents.py` 仅把合同 4.0.0 的知识内容投影为双文档并更新摘要，不解析原始文档，也不提取或判断业务含义。结构化文档合同见 [输入边界](references/structured-document-input.md)。它会将结构检查状态重置为待检查；重生成后必须重新验证。业务内容需要先由技能完成。

## 排查与证据

缺少 `review.md` 或 `coverage.md`、文档版本不一致或正文定位遗漏时，补齐真实业务内容并更新附件中的摘要，不能只补空锚点。概念或判断解释不清时按 [审阅方法](references/review-guide.md) 修订；案例预期变化应退回知识责任人确认。

本地检查证明结构、文件及定位覆盖，不证明正文语义一致或实际读者可理解。作者自查、业务读者复述和领域责任人确认分别记录；未开展的审阅保留待验证。当前示例为合成教学稿，尚无真实业务读者或领域专家验收，也未完成宿主安装验证。本次记录见 [0.8.0 历史修订记录](reports/0.8.0-revision.md)；旧报告只证明所列旧版本。资料快照见 [sources.json](references/sources.json)，权利与方法借鉴见 [来源说明](THIRD_PARTY_NOTICES.md)。
