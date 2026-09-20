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


SKILL_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_REF_FIELDS = frozenset({"artifact_id", "content_version", "contract_version", "path", "digest"})


def report(status: str, failures: list[dict[str, str]], *, mode: str, checked: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": status,
        "mode": mode,
        "failures": failures,
        "checked": checked,
        "boundary": "只验证 JSON Schema、路径、字节摘要、ID 和证据引用；不证明业务确认、平台导入、编译、发布或 ECP 数据运行。",
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
        "design-time-data-lineage": repo_root / "contracts/lineage/v1/design-time-data-lineage.schema.json",
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


def check_confirmations(payload, project_root, schemas, registry, failures):
    pairs = (("knowledge", "knowledge_confirmation", "domain-knowledge"),
             ("domain_model", "model_confirmation", "domain-model"),
             ("authoring", "authoring_confirmation", "ecp-semantic-authoring"),
             ("mapping", "mapping_confirmation", "ecp-data-mapping"))
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
                raise ValueError("被确认成果不满足前序输出合同: " + errors[0].message)
            for key in ("artifact_id", "content_version", "contract_version"):
                if reference[key] != baseline[key]:
                    raise ValueError("被确认成果与引用的 " + key + " 不一致")
            if not set(baseline["confirmation"]["scope_ids"]).issubset(record["scope_ids"]):
                raise ValueError("确认记录没有覆盖该成果的交接范围")
            check_artifact_refs(baseline, project_root, failures)
            check_ids(baseline, failures)
            check_evidence_references(baseline, failures)
        except (KeyError, TypeError, OSError, ValueError) as exc:
            failure(failures, "CONFIRMATION_INVALID", confirmation_key, str(exc))
    return count


def check_data_lineage(payload, project_root, schemas, registry, failures):
    content = payload.get("content", {})
    reference = content.get("data_lineage")
    if not isinstance(reference, dict):
        failure(failures, "DATA_LINEAGE_REQUIRED", "content/data_lineage", "当前映射交付必须登记设计期 data-lineage.json")
        return "MISSING"
    try:
        if reference not in payload.get("files", []):
            failure(failures, "DATA_LINEAGE_FILE_UNREGISTERED", "content/data_lineage", "data_lineage ArtifactRef 必须同时登记在 files")
        lineage = load_json(canonical_artifact_path(project_root, reference["path"]), root=project_root)
        validator = Draft202012Validator(
            schemas["design-time-data-lineage"], registry=registry, format_checker=FormatChecker()
        )
        errors = list(validator.iter_errors(lineage))
        if errors:
            failure(failures, "DATA_LINEAGE_SCHEMA_INVALID", reference["path"], errors[0].message)
            return "FAIL"

        for key, value in (
            ("artifact_id", lineage["lineage_id"]),
            ("content_version", lineage["content_version"]),
            ("contract_version", lineage["contract_version"]),
        ):
            if reference[key] != value:
                failure(failures, "DATA_LINEAGE_REF_MISMATCH", reference["path"], f"{key} 与血缘文件不一致")
        if reference["content_version"] != payload["content_version"]:
            failure(failures, "DATA_LINEAGE_CONTENT_VERSION_MISMATCH", reference["path"], "数据血缘必须与当前 Mapping 输出使用同一内容版本")

        if lineage["schema_snapshot"] != content["schema_snapshot"]:
            failure(failures, "DATA_LINEAGE_SCHEMA_SNAPSHOT_MISMATCH", reference["path"], "血缘文件必须绑定同一 Schema Snapshot")

        mapping_refs = {item["artifact_id"]: item for item in content["mappings"]}
        lineage_mapping_refs = {item["artifact_id"]: item for item in lineage["mapping_refs"]}
        if len(lineage_mapping_refs) != len(lineage["mapping_refs"]):
            failure(failures, "DATA_LINEAGE_MAPPING_ID_DUPLICATE", reference["path"], "血缘文件存在重复 Mapping artifact_id")
        if lineage_mapping_refs != mapping_refs:
            failure(failures, "DATA_LINEAGE_MAPPING_SET_MISMATCH", reference["path"], "血缘文件必须精确绑定当前 Mapping 资产集合")

        bindings = {item["id"]: item for item in content["bindings"]}
        lineage_by_binding = {item["binding_id"]: item for item in lineage["facts"]}
        if len(lineage_by_binding) != len(lineage["facts"]):
            failure(failures, "DATA_LINEAGE_BINDING_DUPLICATE", reference["path"], "同一 Binding 不能出现多条设计期血缘")
        if set(lineage_by_binding) != set(bindings):
            failure(failures, "DATA_LINEAGE_BINDING_COVERAGE_MISMATCH", reference["path"], "每个 Binding 必须且只能有一条设计期数据血缘")
        join_ids = {item["id"] for item in content["joins"]}
        mapping_ids = set(mapping_refs)
        for binding_id, binding in bindings.items():
            row = lineage_by_binding.get(binding_id)
            if row is None:
                continue
            if row["fact_id"] != binding["fact_id"]:
                failure(failures, "DATA_LINEAGE_FACT_MISMATCH", binding_id, "fact_id 与 Binding 不一致")
            if row["predicate_iri"] != binding["predicate_iri"]:
                failure(failures, "DATA_LINEAGE_PREDICATE_MISMATCH", binding_id, "predicate_iri 与 Binding 不一致")
            if row["execution_owner"] != binding["execution_owner"]:
                failure(failures, "DATA_LINEAGE_EXECUTION_OWNER_MISMATCH", binding_id, "execution_owner 与 Binding 不一致")
            locators = {field["locator"] for field in row["source_fields"]}
            if locators != set(binding["source_columns"]):
                failure(failures, "DATA_LINEAGE_SOURCE_FIELD_MISMATCH", binding_id, "source_fields 必须精确覆盖 Binding.source_columns")
            if not set(row["mapping_artifact_ids"]).issubset(mapping_ids):
                failure(failures, "DATA_LINEAGE_MAPPING_REF_UNDEFINED", binding_id, "血缘引用了当前交付之外的 Mapping")
            if not set(row["join_ids"]).issubset(join_ids):
                failure(failures, "DATA_LINEAGE_JOIN_UNDEFINED", binding_id, "血缘引用了未声明 Join")

        identities = {item["id"]: item for item in content["identity_rules"]}
        lineage_identities = {item["identity_rule_id"]: item for item in lineage["identities"]}
        if len(lineage_identities) != len(lineage["identities"]):
            failure(failures, "DATA_LINEAGE_IDENTITY_DUPLICATE", reference["path"], "同一 Identity Rule 不能出现多条身份血缘")
        if set(lineage_identities) != set(identities):
            failure(failures, "DATA_LINEAGE_IDENTITY_COVERAGE_MISMATCH", reference["path"], "每个 Identity Rule 必须且只能有一条身份血缘")
        for identity_id, identity in identities.items():
            row = lineage_identities.get(identity_id)
            if row is None:
                continue
            if row["entity_iri"] != identity["entity_iri"]:
                failure(failures, "DATA_LINEAGE_IDENTITY_IRI_MISMATCH", identity_id, "entity_iri 与 Identity Rule 不一致")
            record_fields = {field["locator"] for field in row["record_key_fields"]}
            if record_fields != set(identity["record_key"]):
                failure(failures, "DATA_LINEAGE_RECORD_KEY_MISMATCH", identity_id, "record_key_fields 必须精确覆盖 Identity.record_key")
            if not set(row["mapping_artifact_ids"]).issubset(mapping_ids):
                failure(failures, "DATA_LINEAGE_IDENTITY_MAPPING_UNDEFINED", identity_id, "身份血缘引用了当前交付之外的 Mapping")

        evidence_ids = {item["evidence_id"] for item in payload.get("evidence", [])}
        for row in lineage["facts"] + lineage["identities"]:
            undefined = set(row.get("evidence_ids", [])) - evidence_ids
            if undefined:
                failure(failures, "DATA_LINEAGE_EVIDENCE_UNDEFINED", reference["path"], "血缘引用未定义 evidence_id: " + ", ".join(sorted(undefined)))

        check_artifact_refs(lineage, project_root, failures)
        return "CHECKED"
    except (KeyError, TypeError, OSError, ValueError) as exc:
        failure(failures, "DATA_LINEAGE_INVALID", reference.get("path", "content/data_lineage"), str(exc))
        return "FAIL"


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
        if direction == "input" and not failures:
            checked["confirmationBindings"] = check_confirmations(payload, project_root, schemas, registry, failures)
        if direction == "output" and not failures and stage == "ecp-data-mapping":
            checked["designTimeDataLineage"] = check_data_lineage(payload, project_root, schemas, registry, failures)
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
