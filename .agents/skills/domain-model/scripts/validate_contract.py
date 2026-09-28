#!/usr/bin/env python3
"""Validate domain-model input/output contracts and business-model consistency."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker, exceptions
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable
from referencing.jsonschema import DRAFT202012

from domain_model import load_yaml, render_coverage, render_review, validate_coverage, validate_model


SKILL_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_REF_FIELDS = frozenset({"artifact_id", "content_version", "contract_version", "path", "digest"})
FORBIDDEN_NAMES = {".git", ".env", ".venv", "__pycache__"}


def contains_forbidden_name(path: Path | PurePosixPath) -> bool:
    return any(part in FORBIDDEN_NAMES for part in path.parts)


def safe_regular_file(path: Path, *, root: Path | None = None) -> Path:
    path = Path(os.path.abspath(path))
    if root is not None:
        root = Path(os.path.abspath(root))
        try:
            relative = path.relative_to(root)
        except ValueError as exc:
            raise ValueError("文件越出项目根目录") from exc
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
        for key, value in pairs:
            if key in result:
                raise ValueError(f"重复 JSON 属性: {key}")
            result[key] = value
        return result
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
    if not isinstance(value, dict):
        raise ValueError("JSON 根节点必须是对象")
    return value


def failure(failures: list[dict[str, str]], code: str, location: str, message: str) -> None:
    failures.append({"code": code, "location": location, "message": message})


def report(status: str, failures: list[dict[str, str]], **checked: Any) -> dict[str, Any]:
    return {
        "status": status,
        "failures": failures,
        "checked": checked,
        "boundary": "只验证合同、引用、覆盖和生成一致性；不证明业务知识真实或业务判断正确。",
    }


def schema_paths() -> dict[str, Path]:
    paths = {
        "common": SKILL_ROOT / "contracts/common.schema.json",
        "business-model": SKILL_ROOT / "contracts/business-domain-model.schema.json",
        "coverage": SKILL_ROOT / "contracts/coverage.schema.json",
        "input": SKILL_ROOT / "contracts/input.schema.json",
        "output": SKILL_ROOT / "contracts/output.schema.json",
        "domain-knowledge": SKILL_ROOT / "contracts/imports/domain-knowledge.schema.json",
        "domain-knowledge-common": SKILL_ROOT / "contracts/imports/domain-knowledge-common.schema.json",
    }
    return paths


def load_schema_registry() -> tuple[dict[str, dict[str, Any]], Registry]:
    schemas: dict[str, dict[str, Any]] = {}
    resources = []
    for name, path in schema_paths().items():
        schema = load_json(path)
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            raise ValueError(f"{name} 缺少 $id")
        schemas[name] = schema
        resources.append((schema_id, Resource.from_contents(schema, default_specification=DRAFT202012)))
    return schemas, Registry().with_resources(resources)


def schema_refs(value: Any) -> list[str]:
    refs = []
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
    checked = []
    try:
        schemas, registry = load_schema_registry()
        for name, schema in schemas.items():
            try:
                Draft202012Validator.check_schema(schema)
                Draft202012Validator(schema, registry=registry)
                resolver = registry.resolver(base_uri=schema["$id"])
                for ref in schema_refs(schema):
                    resolver.lookup(ref)
                checked.append(name)
            except (exceptions.SchemaError, LookupError, Unresolvable, ValueError) as exc:
                failure(failures, "SCHEMA_INVALID", name, str(exc))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        failure(failures, "SCHEMA_LOAD_FAILED", "schemas", str(exc))
    return report("PASS" if not failures else "FAIL", failures, schemas=checked)


def canonical_artifact_path(project_root: Path, raw: Any) -> Path:
    if not isinstance(raw, str) or not raw:
        raise ValueError("ArtifactRef.path 必须是非空字符串")
    relative = PurePosixPath(raw)
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
        raise ValueError("ArtifactRef.path 必须是规范相对路径")
    if contains_forbidden_name(relative):
        raise ValueError("ArtifactRef.path 包含禁止读取名称")
    return project_root.joinpath(*relative.parts)


def walk_objects(value: Any, pointer: str = ""):
    if isinstance(value, dict):
        yield pointer or "/", value
        for key, child in value.items():
            yield from walk_objects(child, f"{pointer}/{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_objects(child, f"{pointer}/{index}")


def check_artifact_refs(value: dict[str, Any], project_root: Path, failures: list[dict[str, str]]) -> int:
    count = 0
    for pointer, item in walk_objects(value):
        if not ARTIFACT_REF_FIELDS.issubset(item):
            continue
        count += 1
        try:
            path = safe_regular_file(canonical_artifact_path(project_root, item["path"]), root=project_root)
            digest = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != item["digest"]:
                failure(failures, "ARTIFACT_DIGEST_MISMATCH", pointer, f'摘要不匹配: {item["path"]}')
        except (OSError, ValueError) as exc:
            failure(failures, "ARTIFACT_REF_INVALID", pointer, str(exc))
    return count


def validate_with_schema(value: dict[str, Any], schema: dict[str, Any], registry: Registry, failures: list[dict[str, str]]) -> None:
    validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(value), key=lambda e: str(list(e.absolute_path))):
        pointer = "/" + "/".join(str(x) for x in error.absolute_path)
        failure(failures, "SCHEMA_VALIDATION_FAILED", pointer or "/", error.message)


def load_knowledge(reference: dict, project_root: Path, schemas: dict, registry: Registry, failures: list[dict[str, str]]) -> dict | None:
    try:
        path = canonical_artifact_path(project_root, reference["path"])
        knowledge = load_json(path, root=project_root)
        validate_with_schema(knowledge, schemas["domain-knowledge"], registry, failures)
        for key in ("artifact_id", "content_version", "contract_version"):
            if knowledge.get(key) != reference.get(key):
                failure(failures, "KNOWLEDGE_IDENTITY_MISMATCH", key, "领域知识引用身份或版本不一致")
        check_artifact_refs(knowledge, project_root, failures)
        return knowledge
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        failure(failures, "KNOWLEDGE_BASELINE_INVALID", "knowledge", str(exc))
        return None


def check_confirmation(payload: dict, knowledge: dict, project_root: Path, schemas: dict, registry: Registry, failures: list[dict[str, str]]) -> None:
    evidence = payload.get("knowledge_confirmation")
    if not isinstance(evidence, dict):
        failure(failures, "CONFIRMATION_MISSING", "knowledge_confirmation", "CONFIRMED 输入必须有确认记录")
        return
    try:
        record_path = canonical_artifact_path(project_root, evidence["record"]["path"])
        record = load_json(record_path, root=project_root)
        validator = Draft202012Validator(
            {"$ref": schemas["common"]["$id"] + "#/$defs/ConfirmationRecord"},
            registry=registry,
            format_checker=FormatChecker(),
        )
        errors = list(validator.iter_errors(record))
        if errors:
            failure(failures, "CONFIRMATION_INVALID", "knowledge_confirmation", errors[0].message)
            return
        check_artifact_refs(record, project_root, failures)
        if record["status"] != "APPROVED":
            failure(failures, "CONFIRMATION_NOT_APPROVED", "knowledge_confirmation", "知识确认记录未批准")
        reference = payload["knowledge"]
        if reference not in evidence["subject_refs"] or reference not in record["subjects"]:
            failure(failures, "CONFIRMATION_SUBJECT_MISMATCH", "knowledge_confirmation", "确认记录没有绑定当前知识字节")
        scope = set(payload["question_scope_ids"])
        if not scope.issubset(set(record["scope_ids"])):
            failure(failures, "CONFIRMATION_SCOPE_MISMATCH", "knowledge_confirmation", "确认记录没有覆盖本次问题范围")
        if knowledge.get("confirmation", {}).get("status") in {"REJECTED", "STALE"}:
            failure(failures, "KNOWLEDGE_CONFIRMATION_STALE", "knowledge/confirmation", "知识基线已拒绝或失效")
        documents = {PurePosixPath(item["path"]).name: item for item in knowledge.get("files", [])}
        for name in ("review.md", "coverage.md"):
            document = documents.get(name)
            if document is not None and document not in record["subjects"]:
                failure(failures, "CONFIRMATION_DOCUMENT_UNBOUND", "knowledge_confirmation", "确认记录未绑定知识评审材料: " + name)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        failure(failures, "CONFIRMATION_INVALID", "knowledge_confirmation", str(exc))


def check_input(payload: dict, project_root: Path, schemas: dict, registry: Registry, failures: list[dict[str, str]]) -> dict | None:
    validate_with_schema(payload, schemas["input"], registry, failures)
    if failures:
        return None
    check_artifact_refs(payload, project_root, failures)

    if payload["mode"] in {"REVIEW", "REVISE"}:
        subject_contracts = {item.get("contract_version") for item in payload.get("subjects", [])}
        if any(contract and contract.startswith("domain-model-dsl/") for contract in subject_contracts):
            failure(failures, "OLD_DOMAIN_MODEL_REJECTED", "subjects", "Domain DSL 2.x 仅可归档，不能作为 1.0.0 REVIEW/REVISE 输入")
        if payload["mode"] == "REVISE" and "business-domain-model/1.0.0" not in subject_contracts:
            failure(failures, "REVISE_CURRENT_MODEL_REQUIRED", "subjects", "REVISE 必须显式绑定当前 Business Domain Model 1.0.0")
    if failures or payload["mode"] == "REVIEW":
        return None

    knowledge = load_knowledge(payload["knowledge"], project_root, schemas, registry, failures)
    if knowledge is None:
        return None

    scope = set(payload.get("question_scope_ids", []))
    all_questions = {q["id"] for q in knowledge["content"]["questions"]}
    if payload["scope_mode"] == "FULL_BASELINE" and scope != all_questions:
        failure(failures, "FULL_BASELINE_SCOPE_INCOMPLETE", "question_scope_ids", "FULL_BASELINE 必须包含全部知识问题")
    if payload["scope_mode"] == "EXPLICIT_SUBSET":
        if not payload.get("explicit_scope_request"):
            failure(failures, "EXPLICIT_SUBSET_REQUEST_MISSING", "explicit_scope_request", "显式子集必须保存用户/调用方明确范围")
        if scope == all_questions:
            failure(failures, "EXPLICIT_SUBSET_NOT_STRICT", "question_scope_ids", "问题全集必须使用 FULL_BASELINE")
    if not scope or not scope.issubset(all_questions):
        failure(failures, "QUESTION_SCOPE_INVALID", "question_scope_ids", "问题范围为空或越出知识范围")
    declared_scope = set(knowledge.get("confirmation", {}).get("scope_ids", []))
    if not declared_scope or not scope.issubset(declared_scope):
        failure(failures, "KNOWLEDGE_DECLARED_SCOPE_MISMATCH", "question_scope_ids", "请求范围超出知识基线声明范围")

    if payload["mode"] == "PRODUCE":
        forbidden = [k for k in ("existing_models", "public_models", "subjects", "change_request") if k in payload]
        if forbidden:
            failure(failures, "PRODUCE_PRIOR_MODEL_INPUT_FORBIDDEN", ",".join(forbidden), "PRODUCE 不得以旧模型或旧交付作为语义输入")

    if payload["knowledge_basis"] == "CONFIRMED":
        check_confirmation(payload, knowledge, project_root, schemas, registry, failures)
    elif "knowledge_confirmation" in payload:
        failure(failures, "DRAFT_CONFIRMATION_FORBIDDEN", "knowledge_confirmation", "DRAFT 不得携带确认记录")

    return knowledge


def expected_source_rules(knowledge: dict, scope: set[str]) -> dict[str, dict]:
    return {r["id"]: r for r in knowledge["content"]["rules"] if scope & set(r["question_ids"])}


def relevant_issues(knowledge: dict, scope: set[str], source_rules: dict[str, dict]) -> set[str]:
    if scope == {q["id"] for q in knowledge["content"]["questions"]}:
        return {i["id"] for i in knowledge["issues"]}
    related = set(scope) | set(source_rules)
    for rule in source_rules.values():
        related.update(rule.get("statement_ids", []))
    return {i["id"] for i in knowledge["issues"] if related & set(i["affects"])}


def check_coverage_against_knowledge(coverage: dict, model: dict, knowledge: dict, failures: list[dict[str, str]]) -> None:
    scope = set(model["question_scope_ids"])
    source_rules = expected_source_rules(knowledge, scope)
    actual_rules = {r["knowledge_rule_id"]: r for r in coverage["rule_coverage"]}
    if set(actual_rules) != set(source_rules):
        failure(failures, "RULE_COVERAGE_SCOPE_MISMATCH", "rule_coverage", "规则覆盖必须与知识范围内规则精确一致")
    facet_names = ("scope", "preconditions", "conditions", "result", "exceptions", "missing_evidence", "effective_period")
    for rule_id, source in source_rules.items():
        row = actual_rules.get(rule_id)
        if row is None:
            continue
        if set(row["question_ids"]) != (set(source["question_ids"]) & scope):
            failure(failures, "RULE_QUESTION_SCOPE_MISMATCH", rule_id, "规则问题范围与固定知识不一致")
        for name in facet_names:
            if row["facets"][name]["source_text"] != source[name]:
                failure(failures, "RULE_FACET_SOURCE_CHANGED", f"{rule_id}/{name}", "覆盖审计不得改写固定知识规则原文")

    questions = {q["id"]: q for q in knowledge["content"]["questions"] if q["id"] in scope}
    actual_questions = {q["question_id"]: q for q in coverage["question_coverage"]}
    if set(actual_questions) != set(questions):
        failure(failures, "QUESTION_COVERAGE_SCOPE_MISMATCH", "question_coverage", "问题覆盖必须与模型范围精确一致")
    for qid, source in questions.items():
        if actual_questions[qid]["question"] != source["question"]:
            failure(failures, "QUESTION_TEXT_CHANGED", qid, "问题覆盖不得改写问题原文")

    cases = {
        c["id"]: c for c in knowledge["content"]["cases"]
        if scope & set(c["question_ids"])
    }
    actual_cases = {c["case_id"]: c for c in coverage["case_coverage"]}
    if set(actual_cases) != set(cases):
        failure(failures, "CASE_COVERAGE_SCOPE_MISMATCH", "case_coverage", "案例覆盖必须与模型范围内案例精确一致")
    for cid, source in cases.items():
        row = actual_cases[cid]
        if row["expected"] != source["expected"] or row["forbidden"] != source["forbidden"]:
            failure(failures, "CASE_TRUTH_CHANGED", cid, "不得改写上游案例 expected / forbidden")

    expected_issues = relevant_issues(knowledge, scope, source_rules)
    actual_bindings = {x["knowledge_issue_id"] for x in coverage["upstream_issue_bindings"]}
    if actual_bindings != expected_issues:
        failure(failures, "UPSTREAM_ISSUE_BINDING_MISMATCH", "upstream_issue_bindings", "上游 OPEN 绑定范围不完整或包含无关事项")


def check_generated_docs(payload: dict, model: dict, coverage: dict, project_root: Path, failures: list[dict[str, str]]) -> None:
    by_name = defaultdict(list)
    for ref in payload["files"]:
        by_name[PurePosixPath(ref["path"]).name].append(ref)
    for name, rendered in (("review.md", render_review(model)), ("coverage.md", render_coverage(coverage))):
        refs = by_name.get(name, [])
        if len(refs) != 1:
            failure(failures, "REQUIRED_DOCUMENT_INVALID", name, f"必须且只能登记一份 {name}")
            continue
        path = safe_regular_file(canonical_artifact_path(project_root, refs[0]["path"]), root=project_root)
        if path.read_text(encoding="utf-8") != rendered:
            failure(failures, "GENERATED_DOCUMENT_DRIFT", name, "生成文档必须与当前业务模型/覆盖审计一致")


def check_output(payload: dict, project_root: Path, schemas: dict, registry: Registry, failures: list[dict[str, str]]) -> None:
    validate_with_schema(payload, schemas["output"], registry, failures)
    if failures:
        return
    check_artifact_refs(payload, project_root, failures)
    if failures or payload["mode"] == "REVIEW":
        return

    content = payload["content"]
    request_path = canonical_artifact_path(project_root, content["request_ref"]["path"])
    request_result = check_handoff("input", request_path, project_root)
    failures.extend(request_result["failures"])
    if failures:
        return
    request = load_json(request_path, root=project_root)
    if request["knowledge_basis"] == "CONFIRMED" and request.get("knowledge_confirmation") not in payload.get("evidence", []):
        failure(failures, "CONFIRMATION_UNBOUND", "evidence", "输出必须保留输入的知识确认记录")

    model_path = safe_regular_file(canonical_artifact_path(project_root, content["model_ref"]["path"]), root=project_root)
    coverage_path = safe_regular_file(canonical_artifact_path(project_root, content["coverage_ref"]["path"]), root=project_root)
    model = load_yaml(model_path)
    coverage = load_json(coverage_path, root=project_root)
    failures.extend(validate_model(model))
    failures.extend(validate_coverage(coverage, model))
    if failures:
        return

    if content["model_ref"] not in payload["files"] or content["coverage_ref"] not in payload["files"]:
        failure(failures, "CORE_ARTIFACT_UNBOUND", "files", "model.yaml 与 coverage.json 必须登记在 files")
    if model["artifact_id"] != payload["artifact_id"] or model["content_version"] != payload["content_version"]:
        failure(failures, "MODEL_IDENTITY_MISMATCH", "model", "模型与 output 身份版本不一致")
    if coverage["content_version"] != model["content_version"]:
        failure(failures, "COVERAGE_VERSION_MISMATCH", "coverage", "覆盖版本必须与模型一致")
    if coverage["model_ref"] != content["model_ref"]:
        failure(failures, "COVERAGE_MODEL_REF_MISMATCH", "coverage/model_ref", "覆盖必须精确绑定当前模型")

    if coverage["knowledge_ref"] != request["knowledge"]:
        failure(failures, "REQUEST_COVERAGE_KNOWLEDGE_MISMATCH", "coverage/knowledge_ref", "coverage 必须精确绑定请求中的固定领域知识")
    if coverage["knowledge_basis"] != request["knowledge_basis"]:
        failure(failures, "REQUEST_COVERAGE_BASIS_MISMATCH", "coverage/knowledge_basis", "coverage 的知识依据状态必须与请求一致")
    if coverage["scope_mode"] != request["scope_mode"] or coverage["question_scope_ids"] != request["question_scope_ids"]:
        failure(failures, "REQUEST_COVERAGE_SCOPE_MISMATCH", "coverage", "coverage 的范围必须与请求一致")

    knowledge = load_knowledge(coverage["knowledge_ref"], project_root, schemas, registry, failures)
    if knowledge is None or failures:
        return

    check_coverage_against_knowledge(coverage, model, knowledge, failures)
    check_generated_docs(payload, model, coverage, project_root, failures)

    expected_issue_ids = {x["id"] for x in coverage["model_issues"]}
    actual_issue_ids = {x["id"] for x in payload["issues"]}
    if expected_issue_ids != actual_issue_ids:
        failure(failures, "OUTPUT_MODEL_ISSUES_MISMATCH", "issues", "output.json 只能投影 coverage.json 中真正的 MODEL_GAP")


def check_handoff(direction: str, file: Path, project_root: Path) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    try:
        project_root = Path(os.path.abspath(project_root))
        payload = load_json(file, root=project_root)
        schemas, registry = load_schema_registry()
        if direction == "input":
            check_input(payload, project_root, schemas, registry, failures)
        elif direction == "output":
            check_output(payload, project_root, schemas, registry, failures)
        else:
            raise ValueError("direction 必须为 input 或 output")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, yaml.YAMLError, exceptions.SchemaError, Unresolvable) as exc:
        failure(failures, "HANDOFF_LOAD_FAILED", str(file), str(exc))
    return report("PASS" if not failures else "FAIL", failures, direction=direction, file=str(file))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-schemas", action="store_true")
    sub = parser.add_subparsers(dest="command")
    p = sub.add_parser("validate")
    p.add_argument("direction", choices=("input", "output"))
    p.add_argument("file", type=Path)
    p.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()

    if args.check_schemas:
        result = check_schemas()
    elif args.command == "validate":
        result = check_handoff(args.direction, args.file.absolute(), args.project_root.absolute())
    else:
        parser.error("使用 --check-schemas 或 validate input|output")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
