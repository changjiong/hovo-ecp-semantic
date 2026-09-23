#!/usr/bin/env python3
"""Deterministic controller for domain-knowledge Knowledge Formation 1.0.

The script NEVER performs business reasoning or calls a model. It only:
- initializes and tracks the four required pass artifacts;
- validates pass schemas and cross-reference invariants;
- blocks assembly when semantic audit reports a blocking finding;
- deterministically assembles the semantic content into contract 5.0.0 output.json.

LLM/Agent reasoning remains responsible for the contents of the four pass files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
FORMATION_ROOT = SKILL_ROOT / "modules" / "knowledge-formation"
SCHEMA_ROOT = FORMATION_ROOT / "contracts"

PASS_FILES = {
    "statement_pass": ("01-statements.json", "statement-pass.schema.json"),
    "question_discovery": ("02-questions.json", "question-pass.schema.json"),
    "knowledge_synthesis": ("03-synthesis.json", "synthesis-pass.schema.json"),
    "knowledge_audit": ("04-audit.json", "audit-pass.schema.json"),
}

BLOCKING_CODES = {
    "SEMANTIC_DEPTH_INSUFFICIENT",
    "RULE_SPLIT_REQUIRED",
    "COUNTERFACTUAL_FAILED",
    "UNRESOLVED_CONTRADICTION",
    "SYNTHETIC_CASE_CIRCULAR_SUPPORT",
}


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def safe(path: Path, root: Path) -> Path:
    root = root.resolve()
    result = path.resolve()
    if not result.is_relative_to(root):
        fail(f"path escapes project root: {path}")
    return result


def validate_schema(payload: dict[str, Any], schema_name: str) -> None:
    schema = load_json(SCHEMA_ROOT / schema_name)
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(payload),
        key=lambda item: str(list(item.absolute_path)),
    )
    if errors:
        first = errors[0]
        location = "/".join(str(x) for x in first.absolute_path) or "<root>"
        fail(f"{schema_name} validation failed at {location}: {first.message}")


def ids(items: list[dict[str, Any]], key: str = "id") -> set[str]:
    result: set[str] = set()
    for item in items:
        value = item[key]
        if value in result:
            fail(f"duplicate {key}: {value}")
        result.add(value)
    return result


def require_refs(values: list[str], allowed: set[str], location: str) -> None:
    missing = sorted(set(values) - allowed)
    if missing:
        fail(f"{location} contains unknown refs: {missing}")


def input_unit_index(request: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["unit_id"]: item for item in request["source_units"]}


def input_source_index(request: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["source_id"]: item for item in request["sources"]}


def validate_statement_pass(payload: dict[str, Any], request: dict[str, Any]) -> None:
    validate_schema(payload, "statement-pass.schema.json")
    units = input_unit_index(request)
    sources = input_source_index(request)
    rows = payload["source_unit_results"]
    row_ids = [row["source_unit_id"] for row in rows]
    if len(row_ids) != len(set(row_ids)) or set(row_ids) != set(units):
        fail("Statement Pass must account for every SourceUnit exactly once")

    statement_ids: set[str] = set()
    statements: dict[str, dict[str, Any]] = {}
    for row in rows:
        unit_id = row["source_unit_id"]
        if row["status"] == "EXTRACTED" and not row["statements"]:
            fail(f"{unit_id}: EXTRACTED requires at least one Statement")
        if row["status"] != "EXTRACTED" and row["statements"]:
            fail(f"{unit_id}: non-EXTRACTED result must not smuggle Statements")
        for statement in row["statements"]:
            sid = statement["id"]
            if sid in statement_ids:
                fail(f"duplicate statement id: {sid}")
            statement_ids.add(sid)
            statements[sid] = statement
            if unit_id not in statement["source_unit_ids"]:
                fail(f"{sid}: Statement must cite its owning SourceUnit")
            require_refs(statement["source_unit_ids"], set(units), f"{sid}.source_unit_ids")
            require_refs(statement["source_ids"], set(sources), f"{sid}.source_ids")
            unit_sources = {units[u]["source_id"] for u in statement["source_unit_ids"]}
            if unit_sources != set(statement["source_ids"]):
                fail(f"{sid}: source_ids must equal the sources of source_unit_ids")

    for statement in statements.values():
        require_refs(statement["supporting_statement_ids"], statement_ids, f"{statement['id']}.supporting_statement_ids")


def validate_question_pass(payload: dict[str, Any], request: dict[str, Any]) -> None:
    validate_schema(payload, "question-pass.schema.json")
    qids = ids(payload["questions"])
    discovery = payload["question_discovery"]
    if set(discovery["scope_question_ids"]) != qids:
        fail("QuestionDiscovery.scope_question_ids must equal the final Question set")

    units = set(input_unit_index(request))
    candidates = ids(discovery["candidates"])
    for item in discovery["candidates"]:
        require_refs(item["source_unit_ids"], units, f"{item['id']}.source_unit_ids")
        require_refs(item["target_question_ids"], qids, f"{item['id']}.target_question_ids")
        if item["origin"] == "SOURCE" and not item["source_unit_ids"]:
            fail(f"{item['id']}: SOURCE candidate requires source_unit_ids")
        if item["disposition"] in {"RETAINED", "MERGED"} and not item["target_question_ids"]:
            fail(f"{item['id']}: retained/merged candidate needs a target Question")
        if item["disposition"] in {"OUT_OF_SCOPE", "OPEN"} and item["target_question_ids"]:
            fail(f"{item['id']}: out-of-scope/open candidate must not target a final Question")

    if not discovery["process_checks"]:
        fail("Question Discovery requires independent business-process checks")
    for item in discovery["process_checks"]:
        require_refs(item["source_unit_ids"], units, f"{item['id']}.source_unit_ids")
        require_refs(item["question_ids"], qids, f"{item['id']}.question_ids")


def flatten_statements(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [s for row in payload["source_unit_results"] for s in row["statements"]]


def validate_synthesis_pass(
    payload: dict[str, Any],
    statement_payload: dict[str, Any],
    question_payload: dict[str, Any],
    request: dict[str, Any],
) -> None:
    validate_schema(payload, "synthesis-pass.schema.json")
    statement_ids = ids(flatten_statements(statement_payload))
    question_ids = ids(question_payload["questions"])
    rule_ids = ids(payload["rules"])
    case_ids = ids(payload["cases"])
    source_index = input_source_index(request)

    for term in payload["terms"]:
        if "id" not in term or "statement_ids" not in term:
            fail("Every Term must contain id and statement_ids")
        require_refs(term["statement_ids"], statement_ids, f"{term['id']}.statement_ids")

    for rule in payload["rules"]:
        require_refs(rule["statement_ids"], statement_ids, f"{rule['id']}.statement_ids")
        require_refs(rule["question_ids"], question_ids, f"{rule['id']}.question_ids")
        require_refs(rule["case_ids"], case_ids, f"{rule['id']}.case_ids")
        if rule["impact"] == "HIGH":
            for field in ("required_facts", "decision_steps", "evidence_requirements", "case_ids"):
                if not rule[field]:
                    fail(f"{rule['id']}: HIGH impact rule requires non-empty {field}")
        if rule["rule_class"] == "OPERATING_POLICY":
            source_roles = {
                source_index[sid]["source_role"]
                for st in flatten_statements(statement_payload)
                if st["id"] in rule["statement_ids"]
                for sid in st["source_ids"]
                if sid in source_index
            }
            if not source_roles.intersection({"INSTITUTION_POLICY", "EXPERT_KNOWLEDGE"}):
                fail(f"{rule['id']}: OPERATING_POLICY requires institution/expert source provenance")

    for case in payload["cases"]:
        require_refs(case["question_ids"], question_ids, f"{case['id']}.question_ids")
        require_refs(case["rule_ids"], rule_ids, f"{case['id']}.rule_ids")
        require_refs(case["source_ids"], set(source_index), f"{case['id']}.source_ids")
        if case["case_origin"] == "SYNTHETIC_PROBE" and case["source_ids"]:
            fail(f"{case['id']}: synthetic probe cannot claim source authority")
        if case["case_origin"] in {"SOURCE_CASE", "REAL_CONFIRMED"} and not case["source_ids"]:
            fail(f"{case['id']}: source/real case must cite at least one source")

    for rule in payload["rules"]:
        backlinks = {case["id"] for case in payload["cases"] if rule["id"] in case["rule_ids"]}
        if set(rule["case_ids"]) != backlinks:
            fail(f"{rule['id']}: rule.case_ids and case.rule_ids must be exact backlinks")


def validate_audit_pass(
    payload: dict[str, Any],
    synthesis_payload: dict[str, Any],
    request: dict[str, Any],
    question_payload: dict[str, Any],
) -> None:
    validate_schema(payload, "audit-pass.schema.json")
    rules = {r["id"]: r for r in synthesis_payload["rules"]}
    audits = {r["rule_id"]: r for r in payload["rule_audits"]}
    if set(audits) != set(rules):
        fail("Knowledge Audit must audit every Rule exactly once")

    findings = {f["id"]: f for f in payload["findings"]}
    for row in audits.values():
        require_refs(row["finding_ids"], set(findings), f"{row['rule_id']}.finding_ids")
        if rules[row["rule_id"]]["impact"] == "HIGH":
            if any(row[field] != "PASS" for field in ("semantic_depth", "granularity", "counterfactual", "contradiction")):
                fail(f"{row['rule_id']}: HIGH impact Rule did not pass all semantic gates")

    blocking = {f["code"] for f in findings.values() if f["severity"] == "BLOCK"}
    if not blocking.issubset(BLOCKING_CODES):
        fail(f"Unknown blocking code(s): {sorted(blocking - BLOCKING_CODES)}")
    if payload["audit_status"] == "PASS" and blocking:
        fail("audit_status PASS cannot contain BLOCK findings")
    if payload["audit_status"] == "BLOCKED" and not blocking:
        fail("audit_status BLOCKED requires at least one BLOCK finding")
    if set(payload["blocking_codes"]) != blocking:
        fail("blocking_codes must exactly match BLOCK finding codes")

    units = set(input_unit_index(request))
    pc_units = [row.get("source_unit_id") for row in payload["provision_coverage"]]
    if None in pc_units or len(pc_units) != len(set(pc_units)) or set(pc_units) != units:
        fail("Audit provision_coverage must account for every SourceUnit exactly once")

    questions = ids(question_payload["questions"])
    cc_questions = [row.get("question_id") for row in payload["case_coverage"]]
    if None in cc_questions or len(cc_questions) != len(set(cc_questions)) or set(cc_questions) != questions:
        fail("Audit case_coverage must account for every Question exactly once")


def artifact_ref(path: Path, root: Path, artifact_id: str, content_version: str) -> dict[str, str]:
    return {
        "artifact_id": artifact_id,
        "content_version": content_version,
        "contract_version": "formation/1.0.0",
        "path": str(path.resolve().relative_to(root.resolve())),
        "digest": digest(path),
    }


def validate_named_pass(manifest_path: Path, pass_name: str, root: Path, update_manifest: bool = True) -> None:
    manifest = load_json(manifest_path)
    validate_schema(manifest, "formation-manifest.schema.json")
    if pass_name not in PASS_FILES:
        fail(f"unknown pass: {pass_name}")
    input_path = safe(root / manifest["input_ref"]["path"], root)
    if digest(input_path) != manifest["input_ref"]["digest"]:
        fail("input.json digest changed; restart formation on a fixed input")
    request = load_json(input_path)

    pass_path = safe(root / manifest["passes"][pass_name]["path"], root)
    payload = load_json(pass_path)
    schema_name = PASS_FILES[pass_name][1]
    validate_schema(payload, schema_name)

    statement_payload = None
    question_payload = None
    synthesis_payload = None
    if pass_name == "statement_pass":
        validate_statement_pass(payload, request)
    else:
        statement_payload = load_json(safe(root / manifest["passes"]["statement_pass"]["path"], root))
        validate_statement_pass(statement_payload, request)
        if pass_name == "question_discovery":
            validate_question_pass(payload, request)
        else:
            question_payload = load_json(safe(root / manifest["passes"]["question_discovery"]["path"], root))
            validate_question_pass(question_payload, request)
            if pass_name == "knowledge_synthesis":
                validate_synthesis_pass(payload, statement_payload, question_payload, request)
            else:
                synthesis_payload = load_json(safe(root / manifest["passes"]["knowledge_synthesis"]["path"], root))
                validate_synthesis_pass(synthesis_payload, statement_payload, question_payload, request)
                validate_audit_pass(payload, synthesis_payload, request, question_payload)

    if update_manifest:
        manifest["passes"][pass_name]["status"] = "COMPLETE" if payload.get("audit_status") != "BLOCKED" else "BLOCKED"
        write_json(manifest_path, manifest)


def cmd_init(args: argparse.Namespace) -> None:
    root = args.project_root.resolve()
    input_path = safe(args.input, root)
    request = load_json(input_path)
    if request.get("contract_version") != "5.0.0":
        fail("Knowledge Formation 1.0 requires normalized input contract 5.0.0")
    process_dir = safe(args.process_dir, root)
    process_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = process_dir / "manifest.json"
    if manifest_path.exists() and not args.force:
        fail(f"manifest already exists: {manifest_path}")
    input_ref = {
        "artifact_id": request["request_id"],
        "content_version": args.content_version,
        "contract_version": "5.0.0",
        "path": str(input_path.relative_to(root)),
        "digest": digest(input_path),
    }
    manifest = {
        "formation_version": "1.0.0",
        "contract_version": "5.0.0",
        "artifact_id": args.artifact_id,
        "content_version": args.content_version,
        "mode": request["mode"],
        "scope": request["scope"],
        "input_ref": input_ref,
        "process_dir": str(process_dir.relative_to(root)),
        "passes": {
            name: {"path": str((process_dir / filename).relative_to(root)), "status": "PENDING"}
            for name, (filename, _) in PASS_FILES.items()
        },
    }
    validate_schema(manifest, "formation-manifest.schema.json")
    write_json(manifest_path, manifest)
    print(json.dumps({"manifest": str(manifest_path), "passes": list(PASS_FILES)}, ensure_ascii=False))


def cmd_status(args: argparse.Namespace) -> None:
    root = args.project_root.resolve()
    manifest_path = safe(args.manifest, root)
    manifest = load_json(manifest_path)
    validate_schema(manifest, "formation-manifest.schema.json")
    result = {}
    for name, spec in manifest["passes"].items():
        path = safe(root / spec["path"], root)
        result[name] = {"status": spec["status"], "exists": path.exists(), "path": spec["path"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_validate_pass(args: argparse.Namespace) -> None:
    root = args.project_root.resolve()
    manifest_path = safe(args.manifest, root)
    validate_named_pass(manifest_path, args.pass_name, root, update_manifest=True)
    print(json.dumps({"pass": args.pass_name, "status": "COMPLETE"}, ensure_ascii=False))


def merge_issues(*collections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for collection in collections:
        for issue in collection:
            ident = issue["id"]
            if ident in result and result[ident] != issue:
                fail(f"conflicting issue definition: {ident}")
            result[ident] = issue
    return list(result.values())


def cmd_assemble(args: argparse.Namespace) -> None:
    root = args.project_root.resolve()
    manifest_path = safe(args.manifest, root)
    manifest = load_json(manifest_path)
    validate_schema(manifest, "formation-manifest.schema.json")

    for name in PASS_FILES:
        validate_named_pass(manifest_path, name, root, update_manifest=True)
    manifest = load_json(manifest_path)
    if any(spec["status"] != "COMPLETE" for spec in manifest["passes"].values()):
        fail("All four passes must be COMPLETE before assembly")

    request_path = safe(root / manifest["input_ref"]["path"], root)
    request = load_json(request_path)
    statement_path = safe(root / manifest["passes"]["statement_pass"]["path"], root)
    question_path = safe(root / manifest["passes"]["question_discovery"]["path"], root)
    synthesis_path = safe(root / manifest["passes"]["knowledge_synthesis"]["path"], root)
    audit_path = safe(root / manifest["passes"]["knowledge_audit"]["path"], root)
    statements_pass = load_json(statement_path)
    questions_pass = load_json(question_path)
    synthesis = load_json(synthesis_path)
    audit = load_json(audit_path)

    if audit["audit_status"] != "PASS" or audit["blocking_codes"]:
        fail("Knowledge Audit blocks output assembly")

    statements = flatten_statements(statements_pass)
    questions = questions_pass["questions"]
    issues = merge_issues(synthesis["issues"], audit["issues"])
    finding_ids = [item["id"] for item in audit["findings"]]

    process_files = [
        artifact_ref(manifest_path, root, manifest["artifact_id"] + ".FormationManifest", manifest["content_version"]),
        artifact_ref(statement_path, root, manifest["artifact_id"] + ".StatementPass", manifest["content_version"]),
        artifact_ref(question_path, root, manifest["artifact_id"] + ".QuestionPass", manifest["content_version"]),
        artifact_ref(synthesis_path, root, manifest["artifact_id"] + ".SynthesisPass", manifest["content_version"]),
        artifact_ref(audit_path, root, manifest["artifact_id"] + ".AuditPass", manifest["content_version"]),
    ]

    trace = []
    for statement in statements:
        for source_id in statement["source_ids"]:
            trace.append({"from_id": statement["id"], "to_id": source_id, "relation": "DEPENDS_ON", "basis": "Statement provenance"})
    for term in synthesis["terms"]:
        for statement_id in term.get("statement_ids", []):
            trace.append({"from_id": term["id"], "to_id": statement_id, "relation": "DEPENDS_ON", "basis": "Term synthesis"})
    for rule in synthesis["rules"]:
        for statement_id in rule["statement_ids"]:
            trace.append({"from_id": rule["id"], "to_id": statement_id, "relation": "DEPENDS_ON", "basis": "Rule synthesis"})
    for case in synthesis["cases"]:
        for rule_id in case["rule_ids"]:
            trace.append({"from_id": case["id"], "to_id": rule_id, "relation": "EXERCISES", "basis": "Case validation"})
    if not trace:
        fail("Cannot assemble knowledge without provenance trace")

    output = {
        "artifact_id": manifest["artifact_id"],
        "content_version": manifest["content_version"],
        "contract_version": "5.0.0",
        "stage": "domain-knowledge",
        "input_refs": [manifest["input_ref"]],
        "files": process_files,
        "evidence": [],
        "states": {
            "structure_checked": {"status": "NOT_EXECUTED", "evidence_ids": [], "reason": "Awaiting contract validation after deterministic rendering."},
            "business_reviewed": {"status": "NOT_EXECUTED", "evidence_ids": [], "reason": "Knowledge formation complete; business review still required."},
        },
        "confirmation": {"status": "PENDING", "scope_ids": [q["id"] for q in questions], "evidence_ids": []},
        "issues": issues,
        "trace": trace,
        "content": {
            "scope": manifest["scope"],
            "sources": request["sources"],
            "statements": statements,
            "terms": synthesis["terms"],
            "questions": questions,
            "rules": synthesis["rules"],
            "cases": synthesis["cases"],
            "case_coverage": audit["case_coverage"],
            "provision_coverage": audit["provision_coverage"],
            "question_discovery": questions_pass["question_discovery"],
            "formation_summary": {
                "formation_version": "1.0.0",
                "process_dir": manifest["process_dir"],
                "pass_status": {name: "COMPLETE" for name in PASS_FILES},
                "audit_status": "PASS",
                "blocking_codes": [],
                "audit_finding_ids": finding_ids,
            },
        },
        "mode": manifest["mode"],
    }
    output_path = safe(args.output, root)
    write_json(output_path, output)
    print(json.dumps({"output": str(output_path), "rules": len(synthesis["rules"]), "questions": len(questions), "audit": "PASS"}, ensure_ascii=False))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project-root", type=Path, required=True)
    sub = p.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("input", type=Path)
    init.add_argument("--process-dir", type=Path, required=True)
    init.add_argument("--artifact-id", required=True)
    init.add_argument("--content-version", required=True)
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)

    status = sub.add_parser("status")
    status.add_argument("manifest", type=Path)
    status.set_defaults(func=cmd_status)

    vp = sub.add_parser("validate-pass")
    vp.add_argument("manifest", type=Path)
    vp.add_argument("pass_name", choices=list(PASS_FILES))
    vp.set_defaults(func=cmd_validate_pass)

    assemble = sub.add_parser("assemble")
    assemble.add_argument("manifest", type=Path)
    assemble.add_argument("--output", type=Path, required=True)
    assemble.set_defaults(func=cmd_assemble)
    return p


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
