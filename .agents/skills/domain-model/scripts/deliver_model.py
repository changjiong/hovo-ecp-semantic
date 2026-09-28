#!/usr/bin/env python3
"""Generate review.md, coverage.md and output.json from business model artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from domain_model import load_json, load_yaml, render_coverage, render_review, validate_coverage, validate_model
from validate_contract import check_handoff, safe_regular_file, contains_forbidden_name


def artifact_ref(path: Path, identifier: str, content_version: str, contract_version: str, project_root: Path) -> dict:
    return {
        "artifact_id": identifier,
        "content_version": content_version,
        "contract_version": contract_version,
        "path": path.relative_to(project_root).as_posix(),
        "digest": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def emit(model_path: Path, coverage_path: Path, request_path: Path, directory: Path, project_root: Path, refresh_draft: bool = False) -> dict:
    project_root = Path(os.path.abspath(project_root))
    model_path = safe_regular_file(model_path, root=project_root)
    coverage_path = safe_regular_file(coverage_path, root=project_root)
    request_path = safe_regular_file(request_path, root=project_root)
    directory = Path(os.path.abspath(directory))
    directory.relative_to(project_root)

    if contains_forbidden_name(directory) or any(p.is_symlink() for p in (directory, *directory.parents)):
        raise ValueError("交付路径不能含禁读名称或经过符号链接")

    targets = [directory / name for name in ("review.md", "coverage.md", "output.json")]
    if any(p.exists() for p in targets) and not refresh_draft:
        raise ValueError("目标交付文件已存在；新版本须先归档旧交付")
    if any(p.exists() for p in targets) and refresh_draft:
        old = load_json(directory / "output.json")
        if old.get("confirmation", {}).get("status") != "PENDING":
            raise ValueError("仅可刷新尚未确认的草稿")

    request_result = check_handoff("input", request_path, project_root)
    if request_result["status"] != "PASS":
        return request_result
    request = load_json(request_path)
    if request["mode"] == "REVIEW":
        raise ValueError("REVIEW 不生成新模型")

    model = load_yaml(model_path)
    failures = validate_model(model)
    coverage = load_json(coverage_path)
    failures.extend(validate_coverage(coverage, model))
    if failures:
        return {"status": "FAIL", "failures": failures}

    for model_key, request_key in (
        ("knowledge_ref", "knowledge"),
        ("knowledge_basis", "knowledge_basis"),
        ("question_scope_ids", "question_scope_ids"),
        ("scope_mode", "scope_mode"),
    ):
        if model[model_key] != request[request_key]:
            raise ValueError(f"模型与请求不一致: {model_key}")

    expected_model_ref = artifact_ref(
        model_path, model["artifact_id"], model["content_version"],
        "business-domain-model/1.0.0", project_root
    )
    if coverage["model_ref"] != expected_model_ref:
        raise ValueError("coverage.json 的 model_ref 必须精确绑定当前 model.yaml")
    if coverage["knowledge_ref"] != model["knowledge_ref"]:
        raise ValueError("coverage.json 与 model.yaml 必须绑定同一知识版本")
    if coverage["scope_mode"] != model["scope_mode"] or coverage["question_scope_ids"] != model["question_scope_ids"]:
        raise ValueError("coverage.json 与 model.yaml 范围必须一致")

    directory.mkdir(parents=True, exist_ok=True)
    (directory / "review.md").write_text(render_review(model), encoding="utf-8")
    (directory / "coverage.md").write_text(render_coverage(coverage), encoding="utf-8")

    request_ref = artifact_ref(request_path, request["request_id"], model["content_version"], "5.0.0", project_root)
    coverage_ref = artifact_ref(
        coverage_path, coverage["artifact_id"], model["content_version"],
        "domain-model-coverage/1.0.0", project_root
    )
    review_ref = artifact_ref(
        directory / "review.md", model["artifact_id"] + ".Review", model["content_version"], "5.0.0", project_root
    )
    coverage_md_ref = artifact_ref(
        directory / "coverage.md", model["artifact_id"] + ".CoverageView", model["content_version"], "5.0.0", project_root
    )

    evidence = list(request.get("evidence", []))
    if request["knowledge_basis"] == "CONFIRMED":
        evidence.append(request["knowledge_confirmation"])

    not_run = {
        "status": "NOT_EXECUTED",
        "evidence_ids": [],
        "reason": "生成和结构校验不等于业务评审或确认。",
    }

    output_issues = []
    for issue in coverage["model_issues"]:
        output_issues.append({
            "id": issue["id"],
            "kind": "MODEL_GAP",
            "statement": issue["statement"],
            "affects": issue["affects"],
            "owner": issue["owner"],
            "recommendation": issue["recommendation"],
            "until_resolved": issue["until_resolved"],
            "status": issue["status"],
            **({"severity": issue["severity"]} if "severity" in issue else {}),
        })

    payload = {
        "artifact_id": model["artifact_id"],
        "content_version": model["content_version"],
        "contract_version": "5.0.0",
        "stage": "domain-model",
        "mode": request["mode"],
        "input_refs": [request_ref, model["knowledge_ref"]] + request.get("subjects", []),
        "files": [expected_model_ref, coverage_ref, review_ref, coverage_md_ref],
        "evidence": evidence,
        "states": {
            "structure_checked": dict(not_run),
            "business_reviewed": dict(not_run),
        },
        "issues": output_issues,
        "trace": [{
            "from_id": model["artifact_id"],
            "to_id": model["knowledge_ref"]["artifact_id"],
            "relation": "FORMALIZES",
            "basis": "业务领域模型由固定领域知识抽象；知识覆盖与审计见 coverage.json。",
        }],
        "content": {
            "model_ref": expected_model_ref,
            "coverage_ref": coverage_ref,
            "request_ref": request_ref,
        },
        "confirmation": {
            "status": "PENDING",
            "scope_ids": model["question_scope_ids"],
            "evidence_ids": [],
        },
    }
    (directory / "output.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = check_handoff("output", directory / "output.json", project_root)
    result["output"] = str(directory / "output.json")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("--coverage", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--refresh-draft", action="store_true")
    args = parser.parse_args()
    try:
        result = emit(args.model, args.coverage, args.request, args.output_dir, args.project_root, args.refresh_draft)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {"status": "FAIL", "failures": [{"code": "DELIVERY_FAILED", "message": str(exc)}]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
