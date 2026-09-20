#!/usr/bin/env python3
"""Validate this skill and its artifact contracts using bundled resources only."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker, exceptions
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable
from referencing.jsonschema import DRAFT202012

from domain_checks import check_content, check_source_inventory


SKILL_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_REF_FIELDS = frozenset({"artifact_id", "content_version", "contract_version", "path", "digest"})


def report(status: str, failures: list[dict[str, str]], *, mode: str, checked: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": status,
        "mode": mode,
        "failures": failures,
        "checked": checked,
        "boundary": "验证结构、字节引用、业务标识、文档定位及跨文档链接；不证明正文含义一致、可读性、来源真实、判断正确或确认人身份。",
    }


def failure(failures: list[dict[str, str]], code: str, location: str, message: str) -> None:
    failures.append({"code": code, "location": location, "message": message})


def contains_forbidden_name(path: Path | PurePosixPath) -> bool:
    return any("trash" in part.casefold() for part in path.parts)


def safe_regular_file(path: Path, *, root: Path | None = None) -> Path:
    if contains_forbidden_name(path):
        raise ValueError("路径包含禁止读取的名称")
    path = Path(os.path.abspath(path))
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise ValueError("文件路径不能经过符号链接")
    if root is not None:
        root = Path(os.path.abspath(root))
        if root.is_symlink():
            raise ValueError("项目根目录不能是符号链接")
        try:
            relative = path.relative_to(root)
        except ValueError as exc:
            raise ValueError("路径越出项目根目录") from exc
        current = root
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError("引用路径不能经过符号链接")
    elif path.is_symlink():
        raise ValueError("文件不能是符号链接")
    if not path.is_file():
        raise ValueError("文件不存在或不是普通文件")
    return path


def load_json(path: Path, *, root: Path | None = None) -> dict[str, Any]:
    path = safe_regular_file(path, root=root)
    def unique_keys(pairs):
        result = {}
        for key, item in pairs:
            if key in result:
                raise ValueError(f"重复 JSON 属性: {key}")
            result[key] = item
        return result
    def invalid_number(number):
        raise ValueError(f"非有限 JSON 数值: {number}")
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys, parse_constant=invalid_number)
    if not isinstance(value, dict):
        raise ValueError("JSON 根节点必须是对象")
    return value


def skill_name() -> str:
    return load_json(SKILL_ROOT / "manifest.json")["name"]


def schema_paths() -> dict[str, Path]:
    stage = skill_name()
    repo_root = SKILL_ROOT.parents[2]
    paths = {
        "common": SKILL_ROOT / "contracts/common.schema.json",
        "structured-document": repo_root / "contracts/document-structure/v1/structured-document.schema.json",
        f"{stage}:input": SKILL_ROOT / "contracts/input.schema.json",
        f"{stage}:output": SKILL_ROOT / "contracts/output.schema.json",
    }
    for path in sorted((SKILL_ROOT / "contracts/imports").glob("*.schema.json")):
        paths[path.name.removesuffix(".schema.json") + ":output"] = path
    return paths


def load_schema_registry() -> tuple[dict[str, dict[str, Any]], Registry]:
    schemas: dict[str, dict[str, Any]] = {}
    resources: list[tuple[str, Resource]] = []
    for name, path in schema_paths().items():
        schema = load_json(path)
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            raise ValueError(f"{name} 缺少 $id")
        if schema_id in {uri for uri, _ in resources}:
            raise ValueError(f"重复 schema $id: {schema_id}")
        schemas[name] = schema
        resources.append((schema_id, Resource.from_contents(schema, default_specification=DRAFT202012)))
    return schemas, Registry().with_resources(resources)


def format_validation_error(error: exceptions.ValidationError) -> str:
    pointer = "/".join(str(part) for part in error.absolute_path)
    return f"/{pointer}" if pointer else "/"


def schema_refs(value: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        if isinstance(value.get("$ref"), str):
            refs.append(value["$ref"])
        for child in value.values():
            refs.extend(schema_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.extend(schema_refs(child))
    return refs


def check_schemas() -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    checked: dict[str, Any] = {"schemas": []}
    try:
        schemas, registry = load_schema_registry()
        for name, schema in schemas.items():
            try:
                Draft202012Validator.check_schema(schema)
                Draft202012Validator(schema, registry=registry)
                resolver = registry.resolver(base_uri=schema["$id"])
                for reference in schema_refs(schema):
                    resolver.lookup(reference)
                checked["schemas"].append(name)
            except (exceptions.SchemaError, ValueError, LookupError, Unresolvable) as exc:
                failure(failures, "SCHEMA_INVALID", name, str(exc))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        failure(failures, "SCHEMA_LOAD_FAILED", "schemas", str(exc))
    return report("PASS" if not failures else "FAIL", failures, mode="check-schemas", checked=checked)


def canonical_artifact_path(project_root: Path, raw: Any) -> Path:
    if not isinstance(raw, str) or not raw:
        raise ValueError("ArtifactRef.path 必须是非空字符串")
    relative = PurePosixPath(raw)
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
        raise ValueError("ArtifactRef.path 必须是规范相对路径")
    if contains_forbidden_name(relative):
        raise ValueError("ArtifactRef.path 包含禁止读取的名称")
    return project_root.joinpath(*relative.parts)


def walk_objects(value: Any, pointer: str = "") -> list[tuple[str, dict[str, Any]]]:
    found: list[tuple[str, dict[str, Any]]] = []
    if isinstance(value, dict):
        found.append((pointer or "/", value))
        for key, child in value.items():
            found.extend(walk_objects(child, f"{pointer}/{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(walk_objects(child, f"{pointer}/{index}"))
    return found


def check_artifact_refs(value: dict[str, Any], project_root: Path, failures: list[dict[str, str]]) -> int:
    count = 0
    for pointer, item in walk_objects(value):
        if not ARTIFACT_REF_FIELDS.issubset(item):
            continue
        count += 1
        try:
            path = canonical_artifact_path(project_root, item["path"])
            safe_regular_file(path, root=project_root)
            digest = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
            if item.get("digest") != digest:
                failure(failures, "ARTIFACT_DIGEST_MISMATCH", pointer, f"摘要不匹配: {item.get('path')}")
        except (OSError, ValueError) as exc:
            failure(failures, "ARTIFACT_REF_INVALID", pointer, str(exc))
    return count


def check_ids(value: dict[str, Any], failures: list[dict[str, str]]) -> dict[str, int]:
    identifiers: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for pointer, item in walk_objects(value):
        for key in ("id", "source_id", "evidence_id"):
            if key == "source_id" and "artifact" not in item:
                continue
            if key == "evidence_id" and "record" not in item:
                continue
            identifier = item.get(key)
            if isinstance(identifier, str):
                identifiers[key][identifier].append(pointer)
    for key, values in identifiers.items():
        for identifier, locations in values.items():
            if len(locations) > 1:
                failure(failures, "DUPLICATE_ID", ", ".join(locations), f"重复 {key}: {identifier}")
    return {key: len(values) for key, values in identifiers.items()}


def check_evidence_references(value: dict[str, Any], failures: list[dict[str, str]]) -> int:
    evidence = value.get("evidence")
    defined = {
        item.get("evidence_id")
        for item in evidence
        if isinstance(item, dict) and isinstance(item.get("evidence_id"), str)
    } if isinstance(evidence, list) else set()
    references = 0
    for pointer, item in walk_objects(value):
        for key, evidence_ids in item.items():
            if not key.endswith("evidence_ids") or not isinstance(evidence_ids, list):
                continue
            for index, evidence_id in enumerate(evidence_ids):
                references += 1
                if evidence_id not in defined:
                    failure(failures, "EVIDENCE_ID_UNDEFINED", f"{pointer}/{key}/{index}", f"未定义 evidence_id: {evidence_id}")
    return references


class DocumentAnchors(HTMLParser):
    """Read explicit Markdown HTML anchors without rendering or executing HTML."""

    def __init__(self):
        super().__init__()
        self.anchors: list[str] = []
        self.hrefs: list[str] = []
        self.text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attributes = dict(attrs)
            identifier = attributes.get("id")
            if identifier:
                self.anchors.append(identifier)
            href = attributes.get("href")
            if href:
                self.hrefs.append(href)

    def handle_data(self, data):
        self.text.append(data)


ANCHOR_TAG = re.compile(r"<a\b[^>]*\bid\s*=\s*(['\"])([^'\"]+)\1[^>]*>", re.IGNORECASE)
HTML_TAG = re.compile(r"<[^>]+>")
MARKDOWN_LINK = re.compile(r"(?<!!)\[([^]]+)\]\(([^)\s]+)(?:\s+[^)]*)?\)")


def readable_text(line: str) -> str:
    line = HTML_TAG.sub("", line)
    line = MARKDOWN_LINK.sub(r"\1", line)
    return re.sub(r"[\s#>*_`|~\-]", "", line)


def readable_anchor_ids(markdown: str) -> set[str]:
    """Inspect each line once; large audit ledgers must not be rescanned per ID."""
    lines = markdown.splitlines()
    readable = set()
    for position, line in enumerate(lines):
        identifiers = {match.group(2) for match in ANCHOR_TAG.finditer(line)}
        if not identifiers:
            continue
        if len(readable_text(line)) >= 3:
            readable.update(identifiers)
            continue
        following = position + 1
        while following < len(lines) and not lines[following].strip():
            following += 1
        if following < len(lines) and not ANCHOR_TAG.search(lines[following]) and len(readable_text(lines[following])) >= 3:
            readable.update(identifiers)
    return readable


def document_links_to(markdown: str, parser: DocumentAnchors, source_reference, target_reference) -> bool:
    targets = [match.group(2) for match in MARKDOWN_LINK.finditer(markdown)] + parser.hrefs
    for target in targets:
        path = target.split("#", 1)[0]
        if not path:
            continue
        relative = PurePosixPath(path)
        if relative.is_absolute() or ".." in relative.parts:
            continue
        resolved = PurePosixPath(source_reference["path"]).parent.joinpath(*relative.parts)
        if resolved == PurePosixPath(target_reference["path"]):
            return True
    return False


def read_business_document(reference, project_root, failures):
    path = safe_regular_file(canonical_artifact_path(project_root, reference["path"]), root=project_root)
    markdown = path.read_text(encoding="utf-8")
    parser = DocumentAnchors()
    parser.feed(markdown)
    parser.close()
    if not "".join(parser.text).strip():
        failure(failures, "BUSINESS_DOCUMENT_EMPTY", reference["path"], "业务文档没有正文")
    if len(set(parser.anchors)) != len(parser.anchors):
        failure(failures, "BUSINESS_DOCUMENT_DUPLICATE_ANCHOR", reference["path"], "业务文档存在重复定位锚点")
    return markdown, parser


def check_document_locators(reference, markdown, parser, expected, failures):
    anchors = set(parser.anchors)
    readable = readable_anchor_ids(markdown)
    for identifier in sorted(expected):
        if identifier not in anchors:
            failure(failures, "BUSINESS_DOCUMENT_COVERAGE_MISSING", reference["path"], f"业务文档缺少内容定位: {identifier}")
        elif identifier not in readable:
            failure(failures, "BUSINESS_DOCUMENT_EMPTY_LOCATOR", reference["path"], f"业务文档定位没有可读内容: {identifier}")
    return {"expectedLocators": len(expected), "foundLocators": len(expected & anchors)}


def check_business_document(payload, project_root, failures):
    result = {"scope": "PRESENCE_LINKS_AND_LOCATORS_ONLY", "meaningAndReadability": "NOT_VERIFIED"}
    files = payload["files"]
    names = [PurePosixPath(ref["path"]).name for ref in files]
    review_count = names.count("review.md")
    coverage_count = names.count("coverage.md")
    valid_set = review_count == 1 and (coverage_count == 0 if payload["mode"] == "REVIEW" else coverage_count == 1)
    if not valid_set:
        failure(
            failures,
            "BUSINESS_DOCUMENT_SET_INVALID",
            "files",
            "REVIEW 必须且只能有一个 review.md、不得有 coverage.md；PRODUCE 和 REVISE 必须各有一个 review.md 与 coverage.md",
        )
        return result
    documents = {PurePosixPath(reference["path"]).name: reference for reference in files}
    for name, reference in documents.items():
        if reference["content_version"] != payload["content_version"]:
            failure(failures, "BUSINESS_DOCUMENT_VERSION_MISMATCH", reference["path"], "业务文档与结构化附件必须属于同一内容版本")
    review = documents["review.md"]
    review_markdown, review_parser = read_business_document(review, project_root, failures)
    review_expected = {item["id"] for item in payload["issues"]}
    if payload["mode"] == "REVIEW":
        review_expected.update({"section-scope", "section-findings", "section-interviews", "section-limitations"})
        result["review"] = check_document_locators(review, review_markdown, review_parser, review_expected, failures)
        return result
    content = payload["content"]
    review_expected.update(item["id"] for item in content["questions"])
    review_expected.update(item["id"] for item in content["terms"])
    review_expected.update(item["id"] for item in content["rules"])
    review_expected.update(item["source_id"] for item in content["sources"])
    review_expected.update(
        "section-" + section
        for section in {"scope", "provisions", "concepts", "judgements", "cases", "interviews", "sources", "confirmation"}
    )
    result["review"] = check_document_locators(review, review_markdown, review_parser, review_expected, failures)
    if not document_links_to(review_markdown, review_parser, review, documents["coverage.md"]):
        failure(failures, "BUSINESS_DOCUMENT_CROSS_LINK_MISSING", review["path"], "review.md 必须链接到 coverage.md 的完整台账")
    coverage = documents["coverage.md"]
    coverage_markdown, coverage_parser = read_business_document(coverage, project_root, failures)
    coverage_expected = {"section-provisions"}
    coverage_expected.update(item["id"] for item in content["statements"])
    coverage_expected.update(item["id"] for item in content["cases"])
    coverage_expected.update(item["id"] for item in content["provision_coverage"])
    coverage_expected.update(item["id"] for item in content["question_discovery"]["candidates"])
    coverage_expected.update(item["id"] for item in content["question_discovery"]["process_checks"])
    result["coverage"] = check_document_locators(coverage, coverage_markdown, coverage_parser, coverage_expected, failures)
    return result


def check_confirmations(payload, project_root, schemas, registry, failures):
    pairs = (("knowledge", "knowledge_confirmation", "domain-knowledge"),)
    count = 0
    for target_key, confirmation_key, stage in pairs:
        if confirmation_key not in payload:
            continue
        count += 1
        try:
            reference = payload[target_key]
            evidence = payload[confirmation_key]
            record = load_json(canonical_artifact_path(project_root, evidence["record"]["path"]), root=project_root)
            validator = Draft202012Validator(
                {"$ref": schemas["common"]["$id"] + "#/$defs/ConfirmationRecord"},
                registry=registry, format_checker=FormatChecker())
            errors = list(validator.iter_errors(record))
            if errors:
                raise ValueError("确认记录结构错误: " + errors[0].message)
            check_artifact_refs(record, project_root, failures)
            if record["status"] != "APPROVED":
                raise ValueError("前序基线未获批准")
            if reference not in evidence["subject_refs"] or reference not in record["subjects"]:
                raise ValueError("确认记录没有绑定此次输入的完整身份、版本和字节摘要")
            baseline = load_json(canonical_artifact_path(project_root, reference["path"]), root=project_root)
            validator = Draft202012Validator(schemas[f"{stage}:output"], registry=registry, format_checker=FormatChecker())
            errors = list(validator.iter_errors(baseline))
            if errors:
                raise ValueError("被确认成果不满足知识合同: " + errors[0].message)
            if baseline["mode"] == "REVIEW":
                raise ValueError("审查报告不能代替知识基线")
            check_content(baseline, failures)
            for key in ("artifact_id", "content_version", "contract_version"):
                if reference[key] != baseline[key]:
                    raise ValueError("被确认成果与引用的 " + key + " 不一致")
            scope = set(payload.get("question_scope_ids", baseline["confirmation"]["scope_ids"]))
            if not scope.issubset(baseline["confirmation"]["scope_ids"]):
                raise ValueError("请求超出知识基线的交接范围")
            if not scope.issubset(record["scope_ids"]):
                raise ValueError("确认记录没有覆盖该成果的交接范围")
            check_artifact_refs(baseline, project_root, failures)
            check_ids(baseline, failures)
            check_evidence_references(baseline, failures)
        except (KeyError, TypeError, OSError, ValueError) as exc:
            failure(failures, "CONFIRMATION_INVALID", confirmation_key, str(exc))
    return count


def check_output_confirmation_records(payload, project_root, schemas, registry, failures):
    """Bind confirmation claims to exact business/audit document bytes.

    Approval records stay external to the signed documents, avoiding a digest
    cycle. This validates the record, not the real-world identity of its author.
    """
    if payload["mode"] == "REVIEW":
        return 0
    claims = []
    confirmation = payload["confirmation"]
    if confirmation["status"] in {"CONFIRMED", "REJECTED"}:
        claims.append(("confirmation", confirmation["status"], confirmation["scope_ids"], confirmation["evidence_ids"]))
    for item in payload["content"]["statements"] + payload["content"]["rules"]:
        if item["review_status"] in {"CONFIRMED", "REJECTED"}:
            claims.append((item["id"], item["review_status"], [item["id"]], item.get("confirmation_evidence_ids", [])))
    if not claims:
        return 0
    docs = [ref for ref in payload["files"] if PurePosixPath(ref["path"]).name in {"review.md", "coverage.md"}]
    evidence_map = {e["evidence_id"]: e for e in payload["evidence"]}
    validator = Draft202012Validator(
        {"$ref": schemas["common"]["$id"] + "#/$defs/ConfirmationRecord"},
        registry=registry, format_checker=FormatChecker())
    count = 0
    for location, status, scope, evidence_ids in claims:
        covered = set()
        for evidence_id in evidence_ids:
            try:
                evidence = evidence_map[evidence_id]
                record = load_json(canonical_artifact_path(project_root, evidence["record"]["path"]), root=project_root)
                errors = list(validator.iter_errors(record))
                if errors:
                    raise ValueError("确认记录结构错误: " + errors[0].message)
                if record["status"] != ("APPROVED" if status == "CONFIRMED" else "REJECTED"):
                    raise ValueError("确认记录结论与声明不一致")
                if len(docs) != 2 or any(ref not in record["subjects"] or ref not in evidence["subject_refs"] for ref in docs):
                    raise ValueError("确认记录须绑定本内容版本 review.md 和 coverage.md 的完整身份与摘要")
                before = len(failures)
                check_artifact_refs(record, project_root, failures)
                if len(failures) != before:
                    continue
                covered.update(record["scope_ids"])
                count += 1
            except (KeyError, TypeError, OSError, ValueError) as exc:
                failure(failures, "OUTPUT_CONFIRMATION_RECORD_INVALID", location, str(exc))
        if not set(scope).issubset(covered):
            failure(failures, "OUTPUT_CONFIRMATION_SCOPE_UNBOUND", location, "确认声明缺少覆盖本次事项和双文档版本的真实记录")
    return count


def check_handoff(direction: str, file: Path, project_root: Path) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    checked: dict[str, Any] = {"direction": direction, "file": str(file), "projectRoot": str(project_root)}
    try:
        if contains_forbidden_name(project_root):
            raise ValueError("项目根目录包含禁止读取的名称")
        if project_root.is_symlink():
            raise ValueError("项目根目录不能是符号链接")
        payload = load_json(file, root=project_root)
        schemas, registry = load_schema_registry()
        stage = skill_name()
        validator = Draft202012Validator(schemas[f"{stage}:{direction}"], registry=registry, format_checker=FormatChecker())
        checked["stage"] = stage
        for error in sorted(validator.iter_errors(payload), key=lambda item: str(list(item.absolute_path))):
            failure(failures, "SCHEMA_VALIDATION_FAILED", format_validation_error(error), error.message)
        checked["artifactRefs"] = check_artifact_refs(payload, project_root, failures)
        checked["ids"] = check_ids(payload, failures)
        checked["evidenceReferences"] = check_evidence_references(payload, failures)
        if not failures and direction == "input" and payload["mode"] != "REVIEW":
            check_source_inventory(payload, failures)
            checked["sourceInventory"] = "CHECKED"
            checked["confirmationBindings"] = check_confirmations(payload, project_root, schemas, registry, failures)
        if not failures and direction == "output":
            knowledge = None
            request = None
            if stage == "domain-knowledge" and payload["mode"] != "REVIEW":
                if len(payload["input_refs"]) != 1:
                    raise ValueError("领域知识输出必须绑定唯一 input.json")
                reference = payload["input_refs"][0]
                request = load_json(canonical_artifact_path(project_root, reference["path"]), root=project_root)
                validator = Draft202012Validator(
                    schemas["domain-knowledge:input"], registry=registry, format_checker=FormatChecker()
                )
                errors = list(validator.iter_errors(request))
                if errors:
                    raise ValueError("领域知识输入合同错误: " + errors[0].message)
                if reference["artifact_id"] != request["request_id"]:
                    raise ValueError("input_ref.artifact_id 与 request_id 不一致")
                if reference["contract_version"] != "4.0.0":
                    raise ValueError("input_ref.contract_version 必须为 4.0.0")
                if reference["contract_version"] != request["contract_version"]:
                    raise ValueError("input_ref.contract_version 与 input.json 不一致")
                check_source_inventory(request, failures)
                checked["sourceInventory"] = "CHECKED"
            if stage == "domain-model" and payload["mode"] != "REVIEW":
                reference = payload["content"]["knowledge_ref"]
                knowledge = load_json(canonical_artifact_path(project_root, reference["path"]), root=project_root)
                validator = Draft202012Validator(schemas["domain-knowledge:output"], registry=registry, format_checker=FormatChecker())
                errors = list(validator.iter_errors(knowledge))
                if errors:
                    raise ValueError("知识基线合同错误: " + errors[0].message)
                if knowledge["mode"] == "REVIEW":
                    raise ValueError("审查报告不能代替知识基线")
                for key in ("artifact_id", "content_version", "contract_version"):
                    if reference[key] != knowledge[key]:
                        raise ValueError("知识引用身份或版本不匹配: " + key)
                check_artifact_refs(knowledge, project_root, failures)
                check_ids(knowledge, failures)
                check_evidence_references(knowledge, failures)
                check_content(knowledge, failures)
            if not failures:
                content_failure_count = len(failures)
                check_content(payload, failures, knowledge, request)
                checked["businessReferences"] = "CHECKED"
                checked["coverage"] = "CHECKED" if payload["mode"] != "REVIEW" else "NOT_APPLICABLE"
                if stage == "domain-knowledge" and payload["mode"] == "REVIEW":
                    checked["questionDiscovery"] = "NOT_APPLICABLE"
                    checked["openKnowledgeGapCount"] = sum(
                        1
                        for issue in payload["issues"]
                        if issue["kind"] == "KNOWLEDGE_GAP" and issue["status"] == "OPEN"
                    )
                    checked["openQuestionCandidateCount"] = "NOT_APPLICABLE"
                    checked["processGapCount"] = "NOT_APPLICABLE"
                if stage == "domain-knowledge" and payload["mode"] != "REVIEW":
                    source_unit_ids = {item["unit_id"] for item in request["source_units"]}
                    provision_counts: dict[str, int] = defaultdict(int)
                    for provision in payload["content"]["provision_coverage"]:
                        provision_counts[provision["source_unit_id"]] += 1
                    checked["sourceCoverage"] = (
                        "COMPLETE"
                        if set(provision_counts) == source_unit_ids and all(count == 1 for count in provision_counts.values())
                        else "FAIL"
                    )
                    if len(failures) > content_failure_count:
                        checked["knowledgeExtraction"] = "UNKNOWN"
                        checked["questionDiscovery"] = "UNKNOWN"
                        checked["openKnowledgeGapCount"] = "UNKNOWN"
                        checked["openQuestionCandidateCount"] = "UNKNOWN"
                        checked["processGapCount"] = "UNKNOWN"
                    else:
                        incomplete_sources = [
                            item["source_id"] for item in request["source_extractions"]
                            if item["status"] != "COMPLETE"
                        ]
                        source_incomplete = [
                            row["id"] for row in payload["content"]["provision_coverage"]
                            if row["status"] in {"PARTIAL", "UNREADABLE"}
                        ]
                        meaning_incomplete = [
                            row["id"] for row in payload["content"]["provision_coverage"]
                            if row["meaning_status"] in {"PARTIAL", "NOT_REVIEWED"}
                        ]
                        open_knowledge_gaps = [
                            issue["id"]
                            for issue in payload["issues"]
                            if issue["kind"] == "KNOWLEDGE_GAP" and issue["status"] == "OPEN"
                        ]
                        open_candidates = [
                            candidate["id"]
                            for candidate in payload["content"]["question_discovery"]["candidates"]
                            if candidate["disposition"] == "OPEN"
                        ]
                        process_gaps = [
                            process_check["id"]
                            for process_check in payload["content"]["question_discovery"]["process_checks"]
                            if process_check["status"] == "GAP"
                        ]
                        checked["notApplicableProvisions"] = [
                            row["id"] for row in payload["content"]["provision_coverage"]
                            if row["status"] == "OUT_OF_SCOPE"
                        ]
                        checked["sourceExtraction"] = "COMPLETE" if not source_incomplete and not incomplete_sources else "PARTIAL"
                        checked["meaningReview"] = "COMPLETE" if not meaning_incomplete else "PARTIAL"
                        discovery_scope = set(payload["content"]["question_discovery"]["scope_question_ids"])
                        checked["questionDiscoveryScope"] = "DECLARED_QUESTIONS_ONLY"
                        checked["questionDiscoveryQuestionCount"] = len(discovery_scope)
                        checked["questionsOutsideDiscoveryScope"] = [
                            q["id"] for q in payload["content"]["questions"] if q["id"] not in discovery_scope
                        ]
                        checked["questionDiscovery"] = "COMPLETE" if not open_candidates and not process_gaps else "PARTIAL"
                        checked["knowledgeExtraction"] = (
                            "COMPLETE"
                            if (
                                not source_incomplete
                                and not incomplete_sources
                                and not meaning_incomplete
                                and not open_knowledge_gaps
                                and not open_candidates
                                and not process_gaps
                            )
                            else "PARTIAL"
                        )
                        checked["incompleteSources"] = incomplete_sources
                        checked["sourceIncompleteProvisions"] = source_incomplete
                        checked["meaningIncompleteProvisions"] = meaning_incomplete
                        checked["openKnowledgeGapCount"] = len(open_knowledge_gaps)
                        checked["openKnowledgeGapIds"] = open_knowledge_gaps
                        checked["openQuestionCandidateCount"] = len(open_candidates)
                        checked["openQuestionCandidateIds"] = open_candidates
                        checked["processGapCount"] = len(process_gaps)
                        checked["processGapIds"] = process_gaps
                if stage == "domain-knowledge" and not failures:
                    checked["businessDocument"] = check_business_document(payload, project_root, failures)
                    checked["outputConfirmationBindings"] = check_output_confirmation_records(payload, project_root, schemas, registry, failures)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, exceptions.SchemaError, Unresolvable) as exc:
        failure(failures, "HANDOFF_LOAD_FAILED", str(file), str(exc))
    return report("PASS" if not failures else "FAIL", failures, mode="contract", checked=checked)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-schemas", action="store_true", help="离线验证本技能随包合同及所需输入资产 Schema")
    subparsers = parser.add_subparsers(dest="command")
    stage = subparsers.add_parser("validate", help="验证本技能输入或输出，不调用其他技能")
    stage.add_argument("direction", choices=("input", "output"))
    stage.add_argument("file", type=Path)
    stage.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    if args.check_schemas == (args.command == "validate"):
        parser.error("使用 --check-schemas，或使用 validate input|output FILE --project-root ROOT")
    if args.check_schemas:
        result = check_schemas()
    else:
        result = check_handoff(args.direction, args.file.absolute(), args.project_root.absolute())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
