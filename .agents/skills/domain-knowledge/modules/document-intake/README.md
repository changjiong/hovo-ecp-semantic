# document-intake

`document-intake` 是 `domain-knowledge` 内部模块，不是独立 Skill，也不是通用文档解析平台。

用户/调用方只提供原始 PDF、DOCX、扫描件或图片引用。该模块负责：

```text
raw documents
  -> MinerU 4.x V1 API
  -> structured_content
  -> SourceBlock
  -> document-normalizer L1
  -> ambiguous boundary -> Jev Choice
  -> deterministic assembler
  -> SourceUnit
  -> SourceRef / SourceExtraction
  -> normalized-input.json
```

后续 Knowledge Formation（知识形成）使用 Semantic Document IR（语义文档中间表示）和知识合同。

## 前置配置

运行环境只需要：

- `MINERU_API_URL`：MinerU API 根地址，位于 `/v1` 之前；
- `MINERU_API_KEY`：Bearer Token；服务端无需鉴权时可留空；
- `TYPESAFE_API_KEY`：TypeSafe API Key，用于 Jev 模糊边界判断；
- `DOMAIN_KNOWLEDGE_MINERU_TIER`：可选，默认 `standard`；
- `DOMAIN_KNOWLEDGE_MINERU_OCR_MODE`：可选，默认 `auto`；
- `DOMAIN_KNOWLEDGE_JEV_MIN_CONFIDENCE`：可选，默认 `0.90`。

用户请求合同不暴露 tier、OCR 模式、API URL 或密钥。

## MinerU 调用链

当前实现按 MinerU 4.x V1 API：

```text
POST /v1/uploads
  -> PUT upload_url
  -> POST /v1/uploads/{upload_id}/complete
  -> POST /v1/parse/jobs
  -> GET /v1/parse/jobs/{job_id}
  -> GET /v1/files/{structured_content_file_id}/content
```

解析任务固定请求：

```json
{
  "tier": "standard",
  "ocr_mode": "auto",
  "output_formats": ["structured_content"]
}
```

实际 tier / OCR 模式可由环境变量覆盖。生产链只消费 `structured_content`；`middle_json` 可用于人工调试，但不是 Skill 正常输入，也不会进入后续知识合同。

## Semantic Document IR 形成

document-intake 不再把 MinerU block（块）直接转换成知识来源单元。它先保留解析器输出，再调用 [document-normalizer](../document-normalizer/README.md)：

```text
structured_content
  -> SourceBlock（逐块保留文本、页码、阅读顺序、bbox 和摘要）
  -> document-normalizer
  -> SourceUnit（按结构恢复后的语义单元）
  -> normalized-input.json
```

SourceBlock 是解析器事实，BoundaryDecision 是模糊结构边界的模型判断记录，SourceUnit 才是 Knowledge Formation（知识形成）的归属单位。条、款等显式结构节点优先形成语义边界；被 MinerU 拆开的连续正文合并回所属条/款；普通非条款文档只在上一块明显未结束时合并，避免把整个章节粗暴拼接。每个保留的 SourceBlock 必须且只能归属一个 SourceUnit。

SourceUnit 同时记录标题路径、祖先、前后单元和可解析的条文交叉引用，供处理窗口读取。上下文只帮助理解，不能改变当前 SourceUnit 的知识归属。

解析状态只有在 MinerU 标记 `is_full_document=true` 且页数闭合时才记为 `COMPLETE`；否则记为 `PARTIAL`。复杂表格、扫描缺失或版式恢复不确定时仍需回看原件，不在规范化层猜测业务含义。

## 安全边界

- API Key 只通过运行环境或 CLI 传入，不写进 request/output；
- 上传 URL 若与 MinerU API 同源才附带 MinerU Bearer Token；不同源预签名 URL 不携带 API Key；
- 解析产物下载遇到跨源重定向时不转发 MinerU API Key；
- Skill 不安装 OCR、PDF 或 DOCX 解析库。

## 输出

输出 `normalized-input.json`，满足 `contracts/input.schema.json`（内部规范化输入 4.0.0），并携带 `source_blocks`、`source_units` 与 `source_extractions`。后续知识形成、来源覆盖、审计、`review.md` / `coverage.md` / `output.json` 不需要知道 MinerU API 细节。
