#!/usr/bin/env python3
"""Turn a raw domain-knowledge request into the existing normalized source input."""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
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
from domain_checks import check_source_inventory


TERMINAL_JOB_STATUS = {"completed", "partial", "failed", "canceled"}
EXCLUDED_BLOCK_TYPES = {"header", "footer", "page_number"}
CHAPTER_RE = re.compile(r"^第[一二三四五六七八九十百零〇两\d]+章")
ARTICLE_RE = re.compile(r"^(第[一二三四五六七八九十百零〇两\d]+条)")
CLAUSE_RE = re.compile(r"^[（(]([一二三四五六七八九十百零〇两\d]+)[）)]")
WEB_CHROME_PATTERNS = (
    re.compile(r"^<u>\s*打印本页.*关闭窗"),
    re.compile(r"^字号\s*[大中小 ]+$"),
    re.compile(r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$"),
)


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


def _headers(api_key: str | None, *, json_body: bool = True) -> dict[str, str]:
    headers = {"Accept": "application/json"}
    if json_body:
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    return headers


def _json_request(
    method: str,
    url: str,
    *,
    api_key: str | None,
    body: dict[str, Any] | None = None,
    timeout: int,
) -> dict[str, Any]:
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=_headers(api_key, json_body=body is not None), method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read(4096).decode("utf-8", errors="replace")
        raise RuntimeError(f"MinerU 返回 HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"MinerU 不可达: {exc.reason}") from exc
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("MinerU 没有返回有效 UTF-8 JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("MinerU JSON 响应根节点必须是对象")
    return payload


def _same_origin(base_url: str, target_url: str) -> bool:
    base = urllib.parse.urlsplit(base_url)
    target = urllib.parse.urlsplit(target_url)

    def origin(parts):
        port = parts.port or (443 if parts.scheme == "https" else 80)
        return parts.scheme.lower(), (parts.hostname or "").lower(), port

    return origin(base) == origin(target)


def _upload_bytes(
    base_url: str,
    upload: dict[str, Any],
    data: bytes,
    *,
    api_key: str | None,
    timeout: int,
) -> None:
    upload_url = upload.get("upload_url")
    if not isinstance(upload_url, str) or not upload_url:
        raise RuntimeError("MinerU pending upload 缺少 upload_url")
    method = upload.get("upload_method") or "PUT"
    if method != "PUT":
        raise RuntimeError(f"MinerU 返回不支持的 upload_method: {method}")
    resolved = urllib.parse.urljoin(base_url.rstrip("/") + "/", upload_url)
    returned_headers = upload.get("upload_headers") or {}
    if not isinstance(returned_headers, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in returned_headers.items()
    ):
        raise RuntimeError("MinerU upload_headers 必须是字符串映射")
    headers = dict(returned_headers)
    if api_key and _same_origin(base_url, resolved):
        headers["Authorization"] = "Bearer " + api_key
    request = urllib.request.Request(resolved, data=data, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(request, timeout=timeout):
            return
    except urllib.error.HTTPError as exc:
        detail = exc.read(4096).decode("utf-8", errors="replace")
        raise RuntimeError(f"MinerU 文件上传返回 HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"MinerU 文件上传失败: {exc.reason}") from exc


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _download_output(
    base_url: str,
    file_id: str,
    *,
    api_key: str | None,
    timeout: int,
) -> bytes:
    url = f"{base_url.rstrip('/')}/v1/files/{file_id}/content"
    request = urllib.request.Request(url, headers=_headers(api_key, json_body=False), method="GET")
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        if exc.code not in {301, 302, 303, 307, 308}:
            detail = exc.read(4096).decode("utf-8", errors="replace")
            raise RuntimeError(f"MinerU 产物下载返回 HTTP {exc.code}: {detail}") from exc
        location = exc.headers.get("Location")
        if not location:
            raise RuntimeError("MinerU 产物重定向缺少 Location") from exc
        redirected = urllib.parse.urljoin(url, location)
        headers = (
            _headers(api_key, json_body=False)
            if _same_origin(base_url, redirected)
            else {"Accept": "application/json"}
        )
        redirected_request = urllib.request.Request(redirected, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(redirected_request, timeout=timeout) as response:
                return response.read()
        except urllib.error.HTTPError as redirected_exc:
            detail = redirected_exc.read(4096).decode("utf-8", errors="replace")
            raise RuntimeError(
                f"MinerU 产物重定向下载返回 HTTP {redirected_exc.code}: {detail}"
            ) from redirected_exc
        except urllib.error.URLError as redirected_exc:
            raise RuntimeError(
                f"MinerU 产物重定向下载失败: {redirected_exc.reason}"
            ) from redirected_exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"MinerU 产物下载失败: {exc.reason}") from exc


def call_mineru(
    path: Path,
    media_type: str,
    digest: str,
    *,
    api_url: str,
    api_key: str | None,
    tier: str,
    ocr_mode: str,
    request_timeout: int,
    poll_timeout: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Run one document through MinerU 4.x V1 and return structured_content + job metadata."""
    base_url = api_url.rstrip("/")
    data = path.read_bytes()
    digest_hex = digest.removeprefix("sha256:")

    upload = _json_request(
        "POST",
        f"{base_url}/v1/uploads",
        api_key=api_key,
        body={
            "filename": path.name,
            "bytes": len(data),
            "mime_type": media_type,
            "purpose": "parse",
            "sha256sum": digest_hex,
        },
        timeout=request_timeout,
    )
    status = upload.get("status")
    if status == "pending":
        _upload_bytes(base_url, upload, data, api_key=api_key, timeout=request_timeout)
        upload_id = upload.get("id")
        if not isinstance(upload_id, str) or not upload_id:
            raise RuntimeError("MinerU upload 缺少 id")
        upload = _json_request(
            "POST",
            f"{base_url}/v1/uploads/{upload_id}/complete",
            api_key=api_key,
            body={"sha256sum": digest_hex},
            timeout=request_timeout,
        )
        status = upload.get("status")
    if status != "completed":
        raise RuntimeError(f"MinerU upload 未完成: {status!r}")
    file_obj = upload.get("file")
    if not isinstance(file_obj, dict) or not isinstance(file_obj.get("id"), str):
        raise RuntimeError("MinerU completed upload 缺少 file.id")
    file_id = file_obj["id"]

    job = _json_request(
        "POST",
        f"{base_url}/v1/parse/jobs",
        api_key=api_key,
        body={
            "files": [{"source": {"type": "file_id", "file_id": file_id}}],
            "tier": tier,
            "ocr_mode": ocr_mode,
            "output_formats": ["structured_content"],
        },
        timeout=request_timeout,
    )
    job_id = job.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        raise RuntimeError("MinerU parse job 缺少 job_id")

    deadline = time.monotonic() + poll_timeout
    interval = 2.0
    while job.get("status") not in TERMINAL_JOB_STATUS:
        if time.monotonic() >= deadline:
            raise TimeoutError(f"MinerU parse job 超时但未取消: {job_id}")
        time.sleep(interval)
        job = _json_request(
            "GET",
            f"{base_url}/v1/parse/jobs/{job_id}",
            api_key=api_key,
            timeout=request_timeout,
        )
        interval = min(interval * 1.5, 15.0)

    if job.get("status") not in {"completed", "partial"}:
        raise RuntimeError(
            f"MinerU parse job 失败: {job.get('status')} job_id={job_id}"
        )
    files = job.get("files")
    if not isinstance(files, list) or len(files) != 1 or not isinstance(files[0], dict):
        raise RuntimeError("MinerU 单文件 parse job 返回了异常 files")
    file_result = files[0]
    if file_result.get("status") != "completed":
        error = file_result.get("error")
        raise RuntimeError(f"MinerU 文件解析失败: {error or file_result.get('status')}")
    output_files = file_result.get("output_files")
    if not isinstance(output_files, dict):
        raise RuntimeError("MinerU 文件结果缺少 output_files")
    structured_ref = output_files.get("structured_content")
    if not isinstance(structured_ref, dict) or not isinstance(
        structured_ref.get("file_id"), str
    ):
        raise RuntimeError("MinerU 未返回 structured_content 产物")

    raw = _download_output(
        base_url,
        structured_ref["file_id"],
        api_key=api_key,
        timeout=request_timeout,
    )
    try:
        structured = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("MinerU structured_content 不是有效 UTF-8 JSON") from exc
    if not isinstance(structured, dict):
        raise RuntimeError("MinerU structured_content 根节点必须是对象")

    job_meta = {
        "job_id": job_id,
        "job_status": job.get("status"),
        "tier": job.get("tier") or tier,
        "finished_at": job.get("finished_at"),
        "model_used": (file_result.get("parse") or {}).get("model_used"),
        "parser_version": (file_result.get("parse") or {}).get("parser_version"),
    }
    return structured, job_meta


def normalize_source_text(text: str) -> str:
    """Normalize CJK compatibility glyphs without converting Chinese punctuation to ASCII."""
    out: list[str] = []
    for char in text:
        codepoint = ord(char)
        if (0x2E80 <= codepoint <= 0x2FDF) or (0xF900 <= codepoint <= 0xFAFF):
            out.append(unicodedata.normalize("NFKC", char))
        elif char == "\u00a0":
            out.append(" ")
        else:
            out.append(char)
    return "".join(out).strip()


def _block_text(block: dict[str, Any]) -> str:
    content = block.get("content")
    text = content if isinstance(content, str) else ""
    if block.get("type") == "image" and not text:
        pieces: list[str] = []
        for key in ("captions", "footnotes"):
            values = block.get(key) or []
            if isinstance(values, list):
                pieces.extend(
                    item for item in values
                    if isinstance(item, str) and item.strip()
                )
        text = "\n".join(pieces)
    return normalize_source_text(text)


def _is_web_chrome(text: str) -> bool:
    if any(pattern.search(text) for pattern in WEB_CHROME_PATTERNS):
        return True
    return "法律声明" in text and "网站主办单位" in text and "网站地图" in text


def _classify_unit(block_type: str, text: str) -> tuple[str, str]:
    if block_type == "table":
        return "TABLE", "表格"
    chapter = CHAPTER_RE.match(text)
    if block_type == "paragraph_title" or chapter:
        return "SECTION", text[:80]
    article = ARTICLE_RE.match(text)
    if article:
        return "ARTICLE", article.group(1)
    clause = CLAUSE_RE.match(text)
    if clause:
        return "CLAUSE", f"（{clause.group(1)}）"
    if block_type == "image":
        return "PAGE_BLOCK", "图片"
    return "PAGE_BLOCK", "正文块"


def normalize_structured_content(
    document: dict[str, Any],
    path: Path,
    digest: str,
    structured: dict[str, Any],
    job_meta: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    pages = structured.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError(
            f"{document['document_id']}: structured_content.pages 缺失或为空"
        )

    metadata = (
        structured.get("metadata")
        if isinstance(structured.get("metadata"), dict)
        else {}
    )
    producer = (
        metadata.get("producer")
        if isinstance(metadata.get("producer"), dict)
        else {}
    )
    parser_name = (
        producer.get("name")
        if isinstance(producer.get("name"), str)
        else "mineru"
    )
    parser_version = (
        producer.get("version")
        if isinstance(producer.get("version"), str)
        else str(job_meta.get("parser_version") or "unknown")
    )

    document_id = document["document_id"]
    source_id = "SRC." + document_id
    media_type = (
        document.get("media_type")
        or mimetypes.guess_type(path.name)[0]
        or "application/octet-stream"
    )
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
    current_section: str | None = None
    current_article: str | None = None
    previous_unit: dict[str, Any] | None = None
    excluded_count = 0

    for page in pages:
        page_idx = page.get("page_idx")
        blocks = page.get("blocks")
        if not isinstance(page_idx, int) or page_idx < 0 or not isinstance(blocks, list):
            raise ValueError(f"{document_id}: structured_content page 结构无效")
        physical_page = page_idx + 1

        for block_position, block in enumerate(blocks, start=1):
            if not isinstance(block, dict):
                raise ValueError(
                    f"{document_id}: page {physical_page} block {block_position} 不是对象"
                )
            block_type = str(block.get("type") or "other")
            if block_type in EXCLUDED_BLOCK_TYPES:
                excluded_count += 1
                continue
            text = _block_text(block)
            if not text:
                excluded_count += 1
                continue
            if _is_web_chrome(text):
                excluded_count += 1
                continue

            sequence = len(units) + 1
            unit_id = f"{source_id}.U{sequence:04d}"
            block_id = f"p{physical_page}.b{block_position}"
            kind, label = _classify_unit(block_type, text)
            if label in {"表格", "图片", "正文块"}:
                label = f"第{physical_page}页{label}{block_position}"

            parent_unit_id: str | None = None
            if kind == "SECTION":
                current_section = unit_id
                current_article = None
            elif kind == "ARTICLE":
                parent_unit_id = current_section
                current_article = unit_id
            elif kind == "CLAUSE":
                parent_unit_id = current_article or current_section
            else:
                continuation = (
                    previous_unit is not None
                    and previous_unit["page"] < physical_page
                    and previous_unit["kind"] in {"ARTICLE", "CLAUSE", "PAGE_BLOCK"}
                    and not re.search(r"[。！？；;.!?：:]$", previous_unit["text"])
                )
                parent_unit_id = (
                    previous_unit["unit_id"]
                    if continuation
                    else (current_article or current_section)
                )

            unit: dict[str, Any] = {
                "unit_id": unit_id,
                "source_id": source_id,
                "kind": kind,
                "label": label,
                "locator": f"第{physical_page}页 {block_id}",
                "source_locator": {
                    "kind": "BLOCK",
                    "value": f"第{physical_page}页 {block_id}",
                    "page": physical_page,
                    "block_id": block_id,
                },
                "sequence": sequence,
                "text": text,
                "digest": sha256_text(text),
            }
            if parent_unit_id:
                unit["parent_unit_id"] = parent_unit_id
            units.append(unit)
            previous_unit = {
                "unit_id": unit_id,
                "kind": kind,
                "page": physical_page,
                "text": text,
            }

    if not units:
        raise ValueError(f"{document_id}: structured_content 没有可用正文单元")

    declared_page_count = (
        (metadata.get("document") or {}).get("page_count")
        if isinstance(metadata.get("document"), dict)
        else None
    )
    full_document = structured.get("is_full_document") is True
    page_count_ok = (
        not isinstance(declared_page_count, int)
        or declared_page_count == len(pages)
    )
    status = "COMPLETE" if full_document and page_count_ok else "PARTIAL"
    limitation_parts = [
        f"由 MinerU structured_content 规范化；过滤 {excluded_count} 个 "
        "header/footer/page_number、空内容或明显网页界面块。"
    ]
    if not full_document:
        limitation_parts.append("MinerU 标记 is_full_document=false。")
    if not page_count_ok:
        limitation_parts.append(
            f"metadata.page_count={declared_page_count}，实际 pages={len(pages)}。"
        )

    profile_parts = [f"tier={job_meta.get('tier') or 'unknown'}"]
    extensions = structured.get("extensions")
    if isinstance(extensions, dict):
        mineru_ext = extensions.get("mineru")
        if isinstance(mineru_ext, dict):
            parse_mode = mineru_ext.get("parse_mode")
            if parse_mode:
                profile_parts.append(f"parse_mode={parse_mode}")
    if job_meta.get("model_used"):
        profile_parts.append(f"model={job_meta['model_used']}")
    if job_meta.get("parser_version"):
        profile_parts.append(f"parser_version={job_meta['parser_version']}")

    parser_metadata: dict[str, Any] = {
        "name": parser_name,
        "version": parser_version,
        "profile": ";".join(profile_parts),
        "input_digest": digest,
    }
    if job_meta.get("job_id"):
        parser_metadata["run_id"] = str(job_meta["job_id"])
    if isinstance(job_meta.get("finished_at"), str):
        parser_metadata["produced_at"] = job_meta["finished_at"]

    extraction = {
        "source_id": source_id,
        "status": status,
        "method": "mineru:v1:structured_content",
        "unit_ids": [item["unit_id"] for item in units],
        "limitations": " ".join(limitation_parts),
        "structured_document_contract": "1.0.0",
        "parser": parser_metadata,
    }
    return source, units, extraction


def normalize_request(
    request: dict[str, Any],
    project_root: Path,
    *,
    api_url: str,
    api_key: str | None,
    tier: str,
    ocr_mode: str,
    request_timeout: int,
    poll_timeout: int,
) -> dict[str, Any]:
    if request["mode"] == "REVIEW":
        raise ValueError("REVIEW 不需要 document-intake；直接使用现有 subjects")
    sources: list[dict[str, Any]] = []
    units: list[dict[str, Any]] = []
    extractions: list[dict[str, Any]] = []
    document_ids = [item["document_id"] for item in request["documents"]]
    if len(set(document_ids)) != len(document_ids):
        raise ValueError("documents 中的 document_id 必须唯一")

    for document in request["documents"]:
        path = safe_regular_file(
            canonical_artifact_path(project_root, document["path"]),
            root=project_root,
        )
        digest = sha256_bytes(path.read_bytes())
        media_type = (
            document.get("media_type")
            or mimetypes.guess_type(path.name)[0]
            or "application/octet-stream"
        )
        structured, job_meta = call_mineru(
            path,
            media_type,
            digest,
            api_url=api_url,
            api_key=api_key,
            tier=tier,
            ocr_mode=ocr_mode,
            request_timeout=request_timeout,
            poll_timeout=poll_timeout,
        )
        source, document_units, extraction = normalize_structured_content(
            document,
            path,
            digest,
            structured,
            job_meta,
        )
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
    absolute.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "request",
        type=Path,
        help="满足 contracts/request.schema.json 的用户请求",
    )
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="生成的内部 normalized-input.json",
    )
    parser.add_argument("--api-url", default=os.getenv("MINERU_API_URL"))
    parser.add_argument("--api-key", default=os.getenv("MINERU_API_KEY"))
    parser.add_argument(
        "--tier",
        default=os.getenv("DOMAIN_KNOWLEDGE_MINERU_TIER", "standard"),
    )
    parser.add_argument(
        "--ocr-mode",
        default=os.getenv("DOMAIN_KNOWLEDGE_MINERU_OCR_MODE", "auto"),
    )
    parser.add_argument("--request-timeout", type=int, default=60)
    parser.add_argument("--poll-timeout", type=int, default=900)
    args = parser.parse_args()

    if not args.api_url:
        parser.error("缺少 --api-url 或 MINERU_API_URL")
    if args.ocr_mode not in {"auto", "txt", "ocr"}:
        parser.error("--ocr-mode 必须是 auto/txt/ocr")

    project_root = args.project_root.absolute()
    request_path = (
        args.request
        if args.request.is_absolute()
        else project_root / args.request
    )
    output_path = (
        args.output
        if args.output.is_absolute()
        else project_root / args.output
    )
    request = load_json(request_path.absolute(), root=project_root)
    validate_request(request)
    normalized = normalize_request(
        request,
        project_root,
        api_url=args.api_url,
        api_key=args.api_key,
        tier=args.tier,
        ocr_mode=args.ocr_mode,
        request_timeout=args.request_timeout,
        poll_timeout=args.poll_timeout,
    )

    schemas, registry = load_schema_registry()
    validator = Draft202012Validator(
        schemas["domain-knowledge:input"],
        registry=registry,
        format_checker=FormatChecker(),
    )
    errors = sorted(
        validator.iter_errors(normalized),
        key=lambda item: str(list(item.absolute_path)),
    )
    if errors:
        error = errors[0]
        pointer = "/" + "/".join(str(part) for part in error.absolute_path)
        raise ValueError(
            f"内部规范化结果不满足 input.schema.json: "
            f"{pointer or '/'} {error.message}"
        )
    inventory_failures: list[dict[str, str]] = []
    check_source_inventory(normalized, inventory_failures)
    if inventory_failures:
        first = inventory_failures[0]
        raise ValueError(
            f"内部 Structured Document IR 检查失败: "
            f"{first['code']} {first['message']}"
        )

    write_output(output_path, project_root, normalized)
    print(json.dumps({
        "status": "PASS",
        "request_id": request["request_id"],
        "documents": len(request.get("documents", [])),
        "source_units": len(normalized["source_units"]),
        "output": str(output_path),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
