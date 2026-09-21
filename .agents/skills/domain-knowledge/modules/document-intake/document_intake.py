#!/usr/bin/env python3
"""Turn a raw domain-knowledge request into the existing normalized source input."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from validate_contract import (
    canonical_artifact_path,
    load_json,
    load_schema_registry,
    safe_regular_file,
)


ALLOWED_STATUS = {"COMPLETE", "PARTIAL", "FAILED"}
KIND_MAP = {
    "title": "SECTION",
    "heading": "SECTION",
    "section": "SECTION",
    "article": "ARTICLE",
    "clause": "CLAUSE",
    "table": "TABLE",
    "appendix": "APPENDIX",
    "preamble": "PREAMBLE",
    "text": "PAGE_BLOCK",
    "paragraph": "PAGE_BLOCK",
    "image_text": "PAGE_BLOCK",
    "other": "PAGE_BLOCK",
}


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate_request(payload: dict[str, Any]) -> None:
    schemas, registry = load_schema_registry()
    validator = Draft202012Validator(
        schemas["domain-knowledge:request"],
        registry=registry,
        format_checker=FormatChecker(),
    )
    errors = sorted(validator.iter_errors(payload), key=lambda item: str(list(item.absolute_path)))
    if errors:
        error = errors[0]
        pointer = "/" + "/".join(str(part) for part in error.absolute_path)
        raise ValueError(f"用户请求不满足 request.schema.json: {pointer or '/'} {error.message}")


def call_parser(path: Path, media_type: str, digest: str, *, endpoint: str, token: str | None, timeout: int) -> dict[str, Any]:
    """Call the single configured parser endpoint.

    Keep provider-specific adaptation here. Do not leak it into the user request
    or Structured Document IR.
    """
    data = path.read_bytes()
    body = json.dumps(
        {
            "filename": path.name,
            "media_type": media_type,
            "content_base64": base64.b64encode(data).decode("ascii"),
            "sha256": digest,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read(4096).decode("utf-8", errors="replace")
        raise RuntimeError(f"解析服务返回 HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"解析服务不可达: {exc.reason}") from exc
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("解析服务没有返回有效 UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("解析服务响应根节点必须是对象")
    return payload


def block_kind(raw: Any) -> str:
    key = str(raw or "other").strip().lower()
    return KIND_MAP.get(key, "PAGE_BLOCK")


def locator_for(block: dict[str, Any], position: int) -> tuple[str, dict[str, Any] | None]:
    explicit = block.get("locator")
    page = block.get("page")
    block_id = block.get("block_id")
    if isinstance(explicit, str) and explicit.strip():
        locator = explicit.strip()
    elif isinstance(page, int) and page >= 1 and isinstance(block_id, str) and block_id.strip():
        locator = f"第{page}页 {block_id.strip()}"
    elif isinstance(page, int) and page >= 1:
        locator = f"第{page}页 第{position}块"
    else:
        locator = f"第{position}块"

    if isinstance(block_id, str) and block_id.strip():
        source_locator: dict[str, Any] = {
            "kind": "BLOCK",
            "value": locator,
            "block_id": block_id.strip(),
        }
        if isinstance(page, int) and page >= 1:
            source_locator["page"] = page
        return locator, source_locator
    if isinstance(page, int) and page >= 1:
        return locator, {"kind": "PAGE", "value": f"第{page}页", "page": page}
    return locator, None


def normalize_response(document: dict[str, Any], path: Path, digest: str, response: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    status = response.get("status")
    if status not in ALLOWED_STATUS:
        raise ValueError(f"{document['document_id']}: parser.status 必须是 COMPLETE/PARTIAL/FAILED")

    parser = response.get("parser")
    if not isinstance(parser, dict) or not isinstance(parser.get("name"), str) or not parser["name"].strip():
        raise ValueError(f"{document['document_id']}: parser.name 缺失")
    if not isinstance(parser.get("version"), str) or not parser["version"].strip():
        raise ValueError(f"{document['document_id']}: parser.version 缺失")

    blocks = response.get("blocks", [])
    if not isinstance(blocks, list):
        raise ValueError(f"{document['document_id']}: blocks 必须是数组")
    if status == "FAILED" and blocks:
        raise ValueError(f"{document['document_id']}: FAILED 不能同时返回 blocks")
    if status != "FAILED" and not blocks:
        raise ValueError(f"{document['document_id']}: 非 FAILED 必须至少返回一个 block")

    document_id = document["document_id"]
    source_id = "SRC." + document_id
    media_type = document.get("media_type") or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    source = {
        "source_id": source_id,
        "artifact": {
            "artifact_id": "ART." + document_id,
            "content_version": digest.removeprefix("sha256:")[:16],
            "contract_version": media_type,
            "path": document["path"],
            "digest": digest,
        },
        "issuer": document.get("issuer", "UNKNOWN"),
        "date": document.get("date", "UNKNOWN"),
        "locator": "全文",
        "authority": document.get("authority", "UNKNOWN"),
        "source_role": document.get("source_role", "UNKNOWN"),
    }

    units: list[dict[str, Any]] = []
    for position, block in enumerate(blocks, start=1):
        if not isinstance(block, dict):
            raise ValueError(f"{document_id}: blocks[{position - 1}] 必须是对象")
        text = block.get("text")
        if not isinstance(text, str):
            raise ValueError(f"{document_id}: blocks[{position - 1}].text 必须是字符串")
        text = text.strip() or "[UNREADABLE_OR_EMPTY]"
        unit_id = f"{source_id}.U{position:04d}"
        locator, source_locator = locator_for(block, position)
        label = block.get("label")
        if not isinstance(label, str) or not label.strip():
            label = text[:60].replace("\n", " ") if block_kind(block.get("type")) == "SECTION" else f"来源单元 {position}"
        unit: dict[str, Any] = {
            "unit_id": unit_id,
            "source_id": source_id,
            "kind": block_kind(block.get("type")),
            "label": label.strip(),
            "locator": locator,
            "sequence": position,
            "text": text,
            "digest": sha256_text(text),
        }
        if source_locator:
            unit["source_locator"] = source_locator
        parent_index = block.get("parent_index")
        if parent_index is not None:
            if not isinstance(parent_index, int) or parent_index < 1 or parent_index >= position:
                raise ValueError(f"{document_id}: parent_index 必须引用前面的 block")
            unit["parent_unit_id"] = f"{source_id}.U{parent_index:04d}"
        units.append(unit)

    limitations = response.get("limitations")
    if not isinstance(limitations, str) or not limitations.strip():
        limitations = "解析服务未声明限制。" if status == "COMPLETE" else "解析服务未提供具体限制说明。"

    parser_metadata: dict[str, Any] = {
        "name": parser["name"].strip(),
        "version": parser["version"].strip(),
        "input_digest": digest,
    }
    for key in ("profile", "run_id", "produced_at"):
        value = parser.get(key)
        if isinstance(value, str) and value.strip():
            parser_metadata[key] = value.strip()

    extraction = {
        "source_id": source_id,
        "status": status,
        "method": "external-parser:" + parser_metadata["name"],
        "unit_ids": [item["unit_id"] for item in units],
        "limitations": limitations.strip(),
        "structured_document_contract": "1.0.0",
        "parser": parser_metadata,
    }
    return source, units, extraction


def normalize_request(request: dict[str, Any], project_root: Path, *, endpoint: str, token: str | None, timeout: int) -> dict[str, Any]:
    if request["mode"] == "REVIEW":
        raise ValueError("REVIEW 不需要 document-intake；直接使用现有 subjects")
    sources: list[dict[str, Any]] = []
    units: list[dict[str, Any]] = []
    extractions: list[dict[str, Any]] = []

    for document in request["documents"]:
        path = safe_regular_file(canonical_artifact_path(project_root, document["path"]), root=project_root)
        digest = sha256_bytes(path.read_bytes())
        media_type = document.get("media_type") or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        response = call_parser(path, media_type, digest, endpoint=endpoint, token=token, timeout=timeout)
        source, document_units, extraction = normalize_response(document, path, digest, response)
        sources.append(source)
        units.extend(document_units)
        extractions.append(extraction)

    normalized: dict[str, Any] = {
        "request_id": request["request_id"],
        "contract_version": "4.0.0",
        "mode": request["mode"],
        "scope": request["scope"],
        "sources": sources,
        "source_units": units,
        "source_extractions": extractions,
    }
    for key in ("business_goal", "consumers", "subjects", "change_request", "evidence"):
        if key in request:
            normalized[key] = request[key]
    return normalized


def write_output(path: Path, project_root: Path, payload: dict[str, Any]) -> None:
    absolute = Path(os.path.abspath(path))
    root = Path(os.path.abspath(project_root))
    try:
        absolute.relative_to(root)
    except ValueError as exc:
        raise ValueError("输出路径必须位于 project-root 内") from exc
    absolute.parent.mkdir(parents=True, exist_ok=True)
    absolute.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path, help="满足 contracts/request.schema.json 的用户请求")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="生成的内部 normalized-input.json")
    parser.add_argument("--endpoint", default=os.getenv("DOMAIN_KNOWLEDGE_PARSER_URL"))
    parser.add_argument("--token", default=os.getenv("DOMAIN_KNOWLEDGE_PARSER_TOKEN"))
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    if not args.endpoint:
        parser.error("缺少 --endpoint 或 DOMAIN_KNOWLEDGE_PARSER_URL")
    project_root = args.project_root.absolute()
    request = load_json(args.request.absolute(), root=project_root)
    validate_request(request)
    normalized = normalize_request(
        request,
        project_root,
        endpoint=args.endpoint,
        token=args.token,
        timeout=args.timeout,
    )

    schemas, registry = load_schema_registry()
    validator = Draft202012Validator(
        schemas["domain-knowledge:input"],
        registry=registry,
        format_checker=FormatChecker(),
    )
    errors = sorted(validator.iter_errors(normalized), key=lambda item: str(list(item.absolute_path)))
    if errors:
        error = errors[0]
        pointer = "/" + "/".join(str(part) for part in error.absolute_path)
        raise ValueError(f"内部规范化结果不满足 input.schema.json: {pointer or '/'} {error.message}")

    write_output(args.output, project_root, normalized)
    print(json.dumps({
        "status": "PASS",
        "request_id": request["request_id"],
        "documents": len(request.get("documents", [])),
        "source_units": len(normalized["source_units"]),
        "output": str(args.output),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
