# document-intake

`document-intake` 是 `domain-knowledge` 内部模块，不是独立 Skill，也不是通用文档解析平台。

用户/调用方只提供原始 PDF、DOCX、扫描件或图片引用。该模块负责：

```text
raw documents
  -> call configured external parser
  -> normalize provider blocks
  -> SourceRef / SourceUnit / SourceExtraction
  -> normalized-input.json
```

后续 Knowledge Formation 继续使用现有结构化文档 IR 和知识合同。

## 配置

只支持一个当前配置的 HTTP 解析端点，不建设 Provider Registry（供应商注册表）：

- `DOMAIN_KNOWLEDGE_PARSER_URL`：解析服务 URL；
- `DOMAIN_KNOWLEDGE_PARSER_TOKEN`：可选 Bearer Token（承载令牌）；
- CLI（命令行接口） `--endpoint` 可覆盖 URL。

解析实现可以是公司 MinerU 服务或其他现成服务。本模块不安装 OCR、PDF、DOCX 解析库。

## 最小 HTTP 边界

当前调用函数发送 JSON：

```json
{
  "filename": "policy.pdf",
  "media_type": "application/pdf",
  "content_base64": "...",
  "sha256": "sha256:..."
}
```

解析端点返回一个块列表：

```json
{
  "status": "COMPLETE",
  "parser": {
    "name": "configured-parser",
    "version": "1"
  },
  "limitations": "",
  "blocks": [
    {
      "type": "title",
      "text": "第一章 总则",
      "page": 1,
      "block_id": "b1"
    },
    {
      "type": "text",
      "text": "第一条 ……",
      "page": 1,
      "block_id": "b2"
    }
  ]
}
```

这是本模块当前唯一外部接缝，不是仓库级标准。接入真实解析服务时，如果它的请求/响应不同，只修改本模块中的 `call_parser()` / `normalize_response()`，不改变用户请求和内部 Structured Document IR（结构化文档中间表示）。

## 输出

输出 `normalized-input.json`，继续满足现有 `contracts/input.schema.json`（内部规范化输入 4.0.0）。后续知识形成、来源覆盖、审计、`review.md` / `coverage.md` / `output.json` 不需要知道解析服务实现。
