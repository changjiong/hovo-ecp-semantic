#!/usr/bin/env python3
"""Validate local cross-skill schemas and handoff artifacts; never proves business or ECP runtime state."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker, exceptions
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable
from referencing.jsonschema import DRAFT202012


SKILL_ROOT = Path(__file__).resolve().parents[1]
SUITE_ROOT = SKILL_ROOT.parent
STAGES = (
    "domain-knowledge",
    "domain-model",
    "ecp-semantic-authoring",
    "ecp-data-mapping",
    "ecp-semantic-release",
)


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


def schema_paths() -> dict[str, Path]:
    paths = {"common": SKILL_ROOT / "contracts/common.schema.json", "pipeline": SKILL_ROOT / "contracts/pipeline.schema.json",
             "domain-common": SUITE_ROOT / "domain-knowledge/contracts/common.schema.json"}
    for stage in STAGES:
        contract_dir = SUITE_ROOT / stage / "contracts"
        paths[f"{stage}:input"] = contract_dir / "input.schema.json"
        paths[f"{stage}:output"] = contract_dir / "output.schema.json"
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


def check_handoff(direction: str, file: Path, project_root: Path, stage: str) -> dict[str, Any]:
    script = SUITE_ROOT / stage / "scripts/validate_contract.py"
    try:
        safe_regular_file(script)
        result = subprocess.run(
            [sys.executable, str(script), "validate", direction, str(file), "--project-root", str(project_root)],
            cwd=script.parent.parent, capture_output=True, text=True, timeout=60, check=False,
        )
        payload = json.loads(result.stdout)
        if not isinstance(payload, dict) or payload.get("status") not in {"PASS", "FAIL"}:
            raise ValueError("阶段校验器未返回有效诊断")
        if (result.returncode == 0) != (payload["status"] == "PASS"):
            raise ValueError("阶段校验器退出状态与诊断不一致")
        return payload
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        return report("FAIL", [{"code": "STAGE_VALIDATION_FAILED", "location": stage, "message": str(exc)}],
                      mode="stage", checked={"stage": stage, "direction": direction})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-schemas", action="store_true", help="验证共享及五个阶段的 input/output JSON Schema")
    subparsers = parser.add_subparsers(dest="command")
    stage = subparsers.add_parser("stage", help="验证单个阶段交接合同")
    stage.add_argument("direction", choices=("input", "output"))
    stage.add_argument("file", type=Path)
    stage.add_argument("--project-root", type=Path, required=True)
    stage.add_argument("--skill", choices=STAGES, required=True)
    args = parser.parse_args()
    if args.check_schemas == (args.command == "stage"):
        parser.error("使用 --check-schemas，或使用 stage input|output FILE --project-root ROOT --skill NAME")
    if args.check_schemas:
        result = check_schemas()
    else:
        result = check_handoff(args.direction, args.file.absolute(), args.project_root.absolute(), args.skill)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
