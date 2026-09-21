# domain-knowledge

从 PDF、DOCX、扫描件等原始业务材料出发，形成业务人员能独立阅读、审查并用于需求访谈的《领域业务知识说明书》和结构化领域知识。Hovo 1.0.0，本地候选。用户请求合同 1.0.0，内部规范化输入与领域知识输出合同 4.0.0。

> 使用 domain-knowledge，依据这些材料形成业务知识说明书，讲清概念、判断依据和案例，并列出下次需求访谈需要确认的问题。

> 使用 domain-knowledge，审查这份尚未确认的知识说明，列出缺少依据和需要访谈的事项。

## 输入与交付

创建只需要业务目标、使用者和原始 PDF/DOCX/扫描件等 documents；审查只需要已有文件；修订需要原成果、变更请求和新增/变更 documents。PRODUCE/REVISE 由内部 `document-intake` 调用已配置外部解析服务，再生成 `SourceRef + source_units + source_extractions` 作为 Structured Document IR；知识形成仍从该 IR 开始。用户不需要构造这些内部对象。Skill 不内置 OCR/PDF/DOCX 解析库。

创建或修订首先交付 `review.md`。文档开头先给出领域认知速览：业务目标、核心概念导航、按业务主题组织的主线和推荐阅读路径；随后再展开概念与边界、逐个问题的判断解释、案例、访谈确认清单和来源依据索引。来源覆盖、问题清洗和编号索引属于追溯信息，不作为业务理解的前置步骤。业务人员无需阅读 JSON、理解技术编号或掌握平台知识。全量覆盖台账、陈述、案例与候选问题去向放在 `coverage.md`；`output.json` 是同一成果的结构化记录。问题由原文含义和业务流程两路发现，不预设问题数量。原文摘录、材料映射、语义审查和业务确认分别记录。

审查已有文件时交付《领域业务知识审查意见》，列清原文、问题、业务影响、建议和限制。业务认可依赖真实确认记录。具体内容见 [业务交付要求](references/business-delivery.md)，成品阅读样式见 [设备维护示例](examples/equipment-maintenance.md)，完成条件见 [验收清单](references/acceptance.md)。

## 独立使用与检查

完整目录可放入宿主支持的 skills 目录单独调用。本包不依赖其他语义工程技能或 ECP 平台；PRODUCE/REVISE 需要配置一个可访问的外部文档解析端点。Python 3.10+ 依赖见 [requirements.txt](requirements.txt)，不包含 OCR/PDF/DOCX 解析库。在本技能目录运行：

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt

# 1. 用户/编排请求：原始文档
.venv/bin/python scripts/validate_contract.py validate request /path/to/project/domain-knowledge/request.json --project-root /path/to/project

# 2. Skill 内部文档 intake：调用已配置外部 parser，生成规范化内部输入
export DOMAIN_KNOWLEDGE_PARSER_URL=https://your-parser.example/parse
.venv/bin/python modules/document-intake/document_intake.py /path/to/project/domain-knowledge/request.json --project-root /path/to/project --output /path/to/project/domain-knowledge/input.json

# 3. 后续沿用既有知识形成合同
.venv/bin/python scripts/validate_contract.py validate input /path/to/project/domain-knowledge/input.json --project-root /path/to/project
.venv/bin/python scripts/render_documents.py /path/to/project/domain-knowledge/output.json --project-root /path/to/project
.venv/bin/python scripts/validate_contract.py validate output /path/to/project/domain-knowledge/output.json --project-root /path/to/project
```

`document_intake.py` 只负责外部解析调用与规范化，见 [document-intake](modules/document-intake/README.md)；真实解析服务若接口不同，只调整这一模块的调用/响应适配，不改变用户请求和 Structured Document IR。 `render_documents.py` 仍只把知识内容投影为双文档并更新摘要，不解析原始文档，也不提取或判断业务含义。内部 IR 见 [Structured Document IR](references/structured-document-ir.md)。

## 排查与证据

缺少 `review.md` 或 `coverage.md`、文档版本不一致或正文定位遗漏时，补齐真实业务内容并更新附件中的摘要，不能只补空锚点。概念或判断解释不清时按 [审阅方法](references/review-guide.md) 修订；案例预期变化应退回知识责任人确认。

本地检查证明结构、文件及定位覆盖，不证明正文语义一致或实际读者可理解。作者自查、业务读者复述和领域责任人确认分别记录；未开展的审阅保留待验证。当前示例为合成教学稿，尚无真实业务读者或领域专家验收，也未完成宿主安装验证。本次记录见 [0.8.0 历史修订记录](reports/0.8.0-revision.md)；旧报告只证明所列旧版本。资料快照见 [sources.json](references/sources.json)，权利与方法借鉴见 [来源说明](THIRD_PARTY_NOTICES.md)。
