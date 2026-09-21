# document-intake

`document-intake` 是 `domain-knowledge` 内部模块，不是独立 Skill，也不是通用文档解析平台。

用户/调用方只提供原始 PDF、DOCX、扫描件或图片引用。该模块负责：

```text
raw documents
  -> MinerU 4.x V1 API
  -> structured_content
  -> normalize
  -> SourceRef / SourceUnit / SourceExtraction
  -> normalized-input.json
```

后续 Knowledge Formation 继续使用现有 Structured Document IR 和知识合同。

## 前置配置

运行环境只需要：

- `MINERU_API_URL`：MinerU API 根地址，位于 `/v1` 之前；
- `MINERU_API_KEY`：Bearer Token；服务端无需鉴权时可留空；
- `DOMAIN_KNOWLEDGE_MINERU_TIER`：可选，默认 `standard`；
- `DOMAIN_KNOWLEDGE_MINERU_OCR_MODE`：可选，默认 `auto`。

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

## Structured Document IR 规范化

规范化规则保持克制：

- 保留页码、block 顺序、bbox 所对应的页/block 定位；
- 过滤 MinerU 已标成 `header`、`footer`、`page_number` 的块、空内容和明显网页界面块；
- `paragraph_title` 或章标题映射为 `SECTION`；
- “第X条”映射为 `ARTICLE`；
- “（X）”映射为 `CLAUSE`；
- 其他正文保留为 `PAGE_BLOCK`，不做业务语义判断；
- 跨页正文不强行拼接；若上一块明显未结束，则下一页首块通过 `parent_unit_id` 继续挂接，保留原始块定位；
- 仅规范化 CJK 兼容字形（例如“⼈”→“人”），不把中文标点整体转换为 ASCII。

解析状态只有在 MinerU 标记 `is_full_document=true` 且页数闭合时才记为 `COMPLETE`；否则记为 `PARTIAL`。

## 安全边界

- API Key 只通过运行环境或 CLI 传入，不写进 request/output；
- 上传 URL 若与 MinerU API 同源才附带 MinerU Bearer Token；不同源预签名 URL 不携带 API Key；
- 解析产物下载遇到跨源重定向时不转发 MinerU API Key；
- Skill 不安装 OCR、PDF 或 DOCX 解析库。

## 输出

输出 `normalized-input.json`，继续满足现有 `contracts/input.schema.json`（内部规范化输入 4.0.0）。后续知识形成、来源覆盖、审计、`review.md` / `coverage.md` / `output.json` 不需要知道 MinerU API 细节。
