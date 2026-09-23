#!/usr/bin/env python3
"""Add line-addressed plain-text sources to a fresh MinerU input."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
INPUT_DIR = ROOT / "A01受益所有人/01业务输入"
SOURCE_DIR = "A01受益所有人/01业务输入"
HEADING = re.compile(r"^(#{1,6})\s+(.+)$")
ARTICLE = re.compile(r"^第[一二三四五六七八九十百零〇两\d]+条")


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def read_markdown(path: Path) -> tuple[dict[str, str], list[tuple[int, int, str]]]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    metadata: dict[str, str] = {}
    start = 0
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is not None:
            raw = yaml.safe_load("\n".join(lines[1:end])) or {}
            if isinstance(raw, dict):
                metadata = {str(k): str(v) for k, v in raw.items() if v is not None}
            start = end + 1

    paragraphs: list[tuple[int, int, str]] = []
    pending: list[str] = []
    first_line = 0

    def flush(last_line: int) -> None:
        nonlocal pending, first_line
        if pending:
            paragraphs.append((first_line, last_line, "\n".join(pending).strip()))
            pending = []

    for index in range(start, len(lines)):
        line = lines[index].rstrip()
        if not line.strip():
            flush(index)
            continue
        if HEADING.match(line) or line.startswith("|"):
            if pending and not (line.startswith("|") and pending[0].startswith("|")):
                flush(index)
            if HEADING.match(line):
                paragraphs.append((index + 1, index + 1, line))
                continue
        if not pending:
            first_line = index + 1
        pending.append(line)
    flush(len(lines))
    return metadata, paragraphs


def source_records(path: Path, index: int) -> tuple[dict, dict, list[dict], list[dict], dict]:
    rel = path.relative_to(ROOT).as_posix()
    document_id = f"TXT{index:03d}"
    source_id = f"SRC.{document_id}"
    media_type = "text/tab-separated-values" if path.suffix == ".tsv" else "text/markdown"
    raw = path.read_bytes()
    metadata: dict[str, str] = {}
    if path.suffix == ".md":
        metadata, segments = read_markdown(path)
    else:
        segments = [
            (number, number, line)
            for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1)
            if line.strip()
        ]
    if not segments:
        raise ValueError(f"Text source is empty: {rel}")

    is_business_brief = rel == f"{SOURCE_DIR}/00业务问题.md"
    is_index = path.suffix == ".tsv" or path.name == "尽调与合规文章分类总结.md"
    authority = "EXPERT" if is_business_brief else "SECONDARY"
    role = "EXPERT_EXPLANATION" if is_business_brief else "SECONDARY_CONTEXT"
    issuer = metadata.get("account") or ("A01业务讨论整理" if is_business_brief else "同业材料整理者")
    source_date = metadata.get("date") or ("2026-09-09" if is_business_brief else "未标明")
    source = {
        "source_id": source_id,
        "artifact": {
            "artifact_id": f"ART.{document_id}",
            "content_version": digest(raw)[7:23],
            "contract_version": media_type,
            "path": rel,
            "digest": digest(raw),
        },
        "issuer": issuer,
        "date": source_date,
        "locator": "全文（行号定位）",
        "authority": authority,
        "source_role": role,
    }
    document = {
        "document_id": document_id,
        "path": rel,
        "label": metadata.get("title") or path.stem,
        "media_type": media_type,
        "issuer": issuer,
        "date": source_date,
        "authority": authority,
        "source_role": role,
    }
    blocks: list[dict] = []
    units: list[dict] = []
    headings: list[tuple[int, str, str]] = []
    for sequence, (first, last, text) in enumerate(segments, 1):
        block_id = f"{source_id}.B{sequence:05d}"
        unit_id = f"{source_id}.U{sequence:05d}"
        locator = f"第{first}行" if first == last else f"第{first}-{last}行"
        heading = HEADING.match(text) if first == last else None
        if heading:
            level = len(heading.group(1))
            headings = [item for item in headings if item[0] < level]
            kind = "SECTION"
            label = heading.group(2).strip()
        elif path.suffix == ".tsv" or text.startswith("|"):
            kind, label = "TABLE", "表格行" if path.suffix == ".tsv" else "表格"
        elif ARTICLE.match(text):
            kind, label = "ARTICLE", ARTICLE.match(text).group(0)
        else:
            kind, label = "PAGE_BLOCK", "正文段落"
        block = {
            "block_id": block_id,
            "source_id": source_id,
            "block_type": "markdown_heading" if heading else "table" if kind == "TABLE" else "paragraph",
            "semantic_hint": kind,
            "page": 1,
            "page_block_index": sequence,
            "sequence": sequence,
            "parser_block_id": f"line{first}-{last}",
            "locator": locator,
            "text": text,
            "digest": digest(text.encode("utf-8")),
        }
        parent = headings[-1][2] if headings else None
        unit = {
            "unit_id": unit_id,
            "source_id": source_id,
            "kind": kind,
            "label": label,
            "locator": locator,
            "source_locator": {"kind": "TABLE" if kind == "TABLE" else "PARAGRAPH", "value": locator},
            "source_block_ids": [block_id],
            "sequence": sequence,
            "text": text,
            "digest": block["digest"],
            "context": {
                "heading_path": [item[1] for item in headings] + ([label] if heading else []),
                "ancestor_unit_ids": [item[2] for item in headings],
            },
        }
        if parent:
            unit["parent_unit_id"] = parent
        if units:
            unit["context"]["previous_unit_id"] = units[-1]["unit_id"]
            units[-1]["context"]["next_unit_id"] = unit_id
        blocks.append(block)
        units.append(unit)
        if heading:
            headings.append((level, label, unit_id))

    image_count = sum(len(re.findall(r"!\[[^]]*\]\([^)]*\)|<img\b", unit["text"])) for unit in units)
    limitations = (
        f"UTF-8 文本按显式标题和空行保留 {len(units)} 个行定位单元；"
        "Markdown 标记和外链原样保留，未抓取外部页面。"
    )
    if image_count:
        limitations += f" 含 {image_count} 个图片引用，图片内容未解析。"
    if is_index:
        limitations += " 此文件是分类索引或整理摘要，不独立证明其指向文章的业务事实。"
    extraction = {
        "source_id": source_id,
        "status": "PARTIAL" if image_count else "COMPLETE",
        "method": "local-utf8-markdown-lines:v1" if path.suffix == ".md" else "local-utf8-tsv-rows:v1",
        "block_ids": [item["block_id"] for item in blocks],
        "boundary_decision_ids": [],
        "unit_ids": [item["unit_id"] for item in units],
        "limitations": limitations,
        "semantic_document_contract": "2.1.0",
        "parser": {
            "name": "local-text-intake",
            "version": "1",
            "profile": "line-addressed markdown" if path.suffix == ".md" else "line-addressed tsv",
            "input_digest": source["artifact"]["digest"],
        },
    }
    return document, source, blocks, units, extraction


def main() -> None:
    binary_request = json.loads((RUN / "request.json").read_text(encoding="utf-8"))
    binary_input = json.loads((RUN / "binary-input.json").read_text(encoding="utf-8"))
    paths = sorted(path for path in INPUT_DIR.rglob("*") if path.is_file() and "trash" not in str(path).lower())
    text_paths = [path for path in paths if path.suffix.lower() in {".md", ".tsv"}]
    if len(paths) != len(binary_request["documents"]) + len(text_paths):
        raise ValueError("Unexpected input media type or missing binary document")
    binary_paths = {item["path"] for item in binary_request["documents"]}
    if binary_paths != {path.relative_to(ROOT).as_posix() for path in paths if path not in text_paths}:
        raise ValueError("Binary intake request does not match the current source directory")
    for source in binary_input["sources"]:
        path = ROOT / source["artifact"]["path"]
        if digest(path.read_bytes()) != source["artifact"]["digest"]:
            raise ValueError(f"Binary source changed after MinerU intake: {path}")

    request = dict(binary_request)
    request["request_id"] = "DK.A01.20260923.FULL"
    request["scope"] = "A01受益所有人/01业务输入全部材料：制度原文、业务问题、同业实践文章与分类索引。"
    request["business_goal"] = (
        "从全部当前业务输入重新形成可审阅的受益所有人领域知识；制度原文确定规范边界，"
        "同业实践用于发现案例、分歧与访谈问题，不继承任何旧领域知识产物或确认。"
    )
    merged = dict(binary_input)
    merged["request_id"] = request["request_id"]
    merged["scope"] = request["scope"]
    merged["business_goal"] = request["business_goal"]
    for index, path in enumerate(text_paths, 1):
        document, source, blocks, units, extraction = source_records(path, index)
        request["documents"].append(document)
        merged["sources"].append(source)
        merged["source_blocks"].extend(blocks)
        merged["source_units"].extend(units)
        merged["source_extractions"].append(extraction)
    (RUN / "full-request.json").write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RUN / "input.json").write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "documents": len(request["documents"]),
        "text_documents": len(text_paths),
        "sources": len(merged["sources"]),
        "source_blocks": len(merged["source_blocks"]),
        "source_units": len(merged["source_units"]),
        "partial_extractions": sum(item["status"] == "PARTIAL" for item in merged["source_extractions"]),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
