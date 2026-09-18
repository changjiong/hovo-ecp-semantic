#!/usr/bin/env python3
"""Validate this skill and its artifact contracts using bundled resources only."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker, exceptions
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable
from referencing.jsonschema import DRAFT202012

from domain_checks import check_content
from domain_dsl import load_model, validate_model, render_review, render_coverage


SKILL_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_REF_FIELDS = frozenset({"artifact_id", "content_version", "contract_version", "path", "digest"})


def report(status: str, failures: list[dict[str, str]], *, mode: str, checked: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": status,
        "mode": mode,
        "failures": failures,
        "checked": checked,
        "boundary": "验证结构、字节引用、业务标识与覆盖一致性；不证明来源真实、判断正确或确认人身份。",
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
    paths = {
        "common": SKILL_ROOT / "contracts/common.schema.json",
        "domain-model:dsl": SKILL_ROOT / "contracts/domain-model.dsl.schema.json",
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


def check_model_documents(payload, model, project_root, failures):
    by_name = defaultdict(list)
    for reference in payload["files"]:
        by_name[PurePosixPath(reference["path"]).name].append(reference)
    for name, rendered in (("review.md", render_review(model)), ("coverage.md", render_coverage(model))):
        matches = by_name[name]
        if len(matches) != 1:
            failure(failures, "REQUIRED_DOCUMENT_INVALID", "files", f"必须且只能登记一份 {name}")
            continue
        if matches[0]["content_version"] != payload["content_version"]:
            failure(failures, "DOCUMENT_VERSION_MISMATCH", name, "文档版本必须与模型一致")
        path = safe_regular_file(canonical_artifact_path(project_root, matches[0]["path"]), root=project_root)
        if path.read_bytes() != rendered.encode("utf-8"):
            failure(failures, "GENERATED_DOCUMENT_DRIFT", name, "文档必须从当前 DSL 生成，不得单独修改")


def load_model_handoff(payload, project_root, schemas, registry, failures):
    reference = payload["content"]["model_ref"]
    path = safe_regular_file(canonical_artifact_path(project_root, reference["path"]), root=project_root)
    model = load_model(path)
    failures.extend(validate_model(model))
    if failures:
        return None, None
    for key in ("artifact_id", "content_version"):
        if model[key] != payload[key] or reference[key] != model[key]:
            failure(failures, "MODEL_IDENTITY_MISMATCH", key, "DSL、引用和交接身份版本不一致")
    if reference not in payload["files"]:
        failure(failures, "MODEL_REF_UNBOUND", "files", "DSL 文件必须登记在交接文件中")
    request_ref = payload["content"]["request_ref"]
    request_path = canonical_artifact_path(project_root, request_ref["path"])
    request_result = check_handoff("input", request_path, project_root)
    failures.extend(request_result["failures"])
    request = load_json(request_path, root=project_root)
    if failures:
        return None, None
    if request_ref not in payload["input_refs"] or request_ref["artifact_id"] != request["request_id"]:
        failure(failures, "REQUEST_UNBOUND", "content/request_ref", "请求身份和输入引用必须一致")
    if request["mode"] != payload["mode"] or request["mode"] == "REVIEW":
        failure(failures, "REQUEST_MODE_MISMATCH", "mode", "生成模式与请求不一致")
        return None, None
    for model_key, request_key in (("knowledge_ref", "knowledge"), ("knowledge_basis", "knowledge_basis"), ("question_scope_ids", "question_scope_ids"), ("scope_mode", "scope_mode")):
        if model[model_key] != request[request_key]:
            failure(failures, "REQUEST_MODEL_MISMATCH", model_key, "DSL 必须精确遵循请求的基线、依据和范围")
    check_artifact_refs(model, project_root, failures)
    knowledge = load_knowledge_baseline(model["knowledge_ref"], project_root, schemas, registry, failures)
    if model["knowledge_basis"] == "CONFIRMED" and request["knowledge_confirmation"] not in payload["evidence"]:
        failure(failures, "CONFIRMATION_UNBOUND", "evidence", "必须保留输入请求的知识确认记录")
    check_model_documents(payload, model, project_root, failures)
    return model, knowledge


def load_knowledge_baseline(reference, project_root, schemas, registry, failures):
    """Load exactly the bundled 4.0.0 knowledge artifact; never borrow another skill's schema."""
    try:
        baseline = load_json(canonical_artifact_path(project_root, reference["path"]), root=project_root)
        validator = Draft202012Validator(
            schemas["domain-knowledge:output"], registry=registry, format_checker=FormatChecker())
        errors = list(validator.iter_errors(baseline))
        if errors:
            raise ValueError("知识基线合同错误: " + errors[0].message)
        if baseline["mode"] == "REVIEW":
            raise ValueError("审查报告不能代替知识基线")
        for key in ("artifact_id", "content_version", "contract_version"):
            if reference[key] != baseline[key]:
                raise ValueError("知识引用身份或版本不匹配: " + key)
        check_artifact_refs(baseline, project_root, failures)
        return baseline
    except (KeyError, TypeError, OSError, ValueError) as exc:
        failure(failures, "KNOWLEDGE_BASELINE_INVALID", "knowledge", str(exc))
        return None


def check_confirmation_evidence(reference, scope, evidence, project_root, schemas, registry, failures, location):
    """Accept only a real external ConfirmationRecord bound to this exact knowledge bytes and scope."""
    try:
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
        if baseline.get("confirmation", {}).get("status") in {"REJECTED", "STALE"}:
            raise ValueError("知识基线已拒绝或失效，不能使用旧批准记录")
        declared = set(baseline.get("confirmation", {}).get("scope_ids", []))
        if not set(scope) or not set(scope).issubset(declared):
            raise ValueError("确认范围为空或超出知识声明范围")
        documents = {PurePosixPath(item["path"]).name: item for item in baseline["files"]}
        for name in ("review.md", "coverage.md"):
            document = documents.get(name)
            if document is None or document not in record["subjects"]:
                raise ValueError("确认记录必须同时绑定知识评审材料: " + name)
        if not set(scope).issubset(record["scope_ids"]):
            raise ValueError("确认记录没有覆盖该成果的交接范围")
        return True
    except (KeyError, TypeError, OSError, ValueError) as exc:
        failure(failures, "CONFIRMATION_INVALID", location, str(exc))
        return False


def check_confirmations(payload, project_root, schemas, registry, failures):
    """knowledge_basis and review_mode are deliberately independent."""
    if payload["mode"] == "REVIEW":
        return 0
    baseline = load_knowledge_baseline(payload["knowledge"], project_root, schemas, registry, failures)
    if baseline is None:
        return 0
    scope = set(payload.get("question_scope_ids", []))
    questions = {item["id"] for item in baseline["content"]["questions"]}
    if payload["scope_mode"] == "FULL_BASELINE" and scope != questions:
        failure(failures, "FULL_BASELINE_SCOPE_INCOMPLETE", "question_scope_ids", "全量模式必须包括固定知识的全部问题")
    declared_scope = set(baseline.get("confirmation", {}).get("scope_ids", []))
    if not scope or not scope.issubset(questions) or not scope.issubset(declared_scope):
        failure(failures, "QUESTION_SCOPE_INVALID", "question_scope_ids", "请求范围为空或超出知识问题与声明范围；声明范围不等于已批准范围")
    if payload["knowledge_basis"] == "DRAFT":
        if "knowledge_confirmation" in payload:
            failure(failures, "DRAFT_CONFIRMATION_FORBIDDEN", "knowledge_confirmation", "DRAFT 不得携带确认记录")
        return 0
    return int(check_confirmation_evidence(
        payload["knowledge"], scope, payload["knowledge_confirmation"],
        project_root, schemas, registry, failures, "knowledge_confirmation"))


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
            checked["confirmationBindings"] = check_confirmations(payload, project_root, schemas, registry, failures)
        if not failures and direction == "output":
            model, knowledge = None, None
            if payload["mode"] != "REVIEW":
                model, knowledge = load_model_handoff(payload, project_root, schemas, registry, failures)
            if not failures:
                check_content(payload, failures, knowledge, model)
                checked["businessReferences"] = "CHECKED"
                checked["coverage"] = "CHECKED" if model else "NOT_APPLICABLE"
                checked["dslVersion"] = model["dsl_version"] if model else "NOT_APPLICABLE"
                checked["generatedDocuments"] = "CHECKED" if model else "NOT_APPLICABLE"
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError, TypeError, exceptions.SchemaError, Unresolvable) as exc:
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
