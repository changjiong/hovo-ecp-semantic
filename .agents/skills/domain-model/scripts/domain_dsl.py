#!/usr/bin/env python3
"""Parse, validate, evaluate, and render the platform-independent model DSL."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

import yaml
from yaml.nodes import MappingNode
from yaml.resolver import BaseResolver
from yaml.tokens import AliasToken, AnchorToken, TagToken
from jsonschema import Draft202012Validator, exceptions

from dsl_expression import (
    DSLExpressionError,
    UNKNOWN,
    ValueSpec,
    declaration_spec,
    evaluate_expression,
    field_spec,
    infer_expression,
    render_expression,
    validate_field_value,
    validate_ref,
)


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = SKILL_ROOT / "contracts" / "domain-model.dsl.schema.json"
MAX_MODEL_BYTES = 2 * 1024 * 1024


class DSLLoadError(ValueError):
    def __init__(self, code: str, location: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.location = location
        self.message = message


class RestrictedLoader(yaml.SafeLoader):
    """SafeLoader without timestamp coercion or duplicate mapping keys."""


RestrictedLoader.yaml_implicit_resolvers = {
    key: [
        (tag, regexp)
        for tag, regexp in resolvers
        if tag != "tag:yaml.org,2002:timestamp"
    ]
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def _construct_mapping(loader: RestrictedLoader, node: MappingNode, deep: bool = False) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise yaml.YAMLError("YAML 映射键必须是文本")
        if key == "<<":
            raise yaml.YAMLError("DSL 禁止 YAML merge key")
        if key in mapping:
            raise yaml.YAMLError(f"YAML 存在重复键: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


RestrictedLoader.add_constructor(BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def _error(code: str, location: str, message: str) -> dict[str, str]:
    return {"code": code, "location": location, "message": message}


def _location(parts: Iterable[Any]) -> str:
    return "/" + "/".join(str(part) for part in parts)


def _forbidden_path(path: Path | PurePosixPath) -> bool:
    return any("trash" in part.casefold() for part in path.parts)


def _safe_regular_file(path: Path) -> Path:
    if _forbidden_path(path):
        raise DSLLoadError("DSL_PATH_FORBIDDEN", str(path), "路径包含禁止读取的名称")
    absolute = Path(os.path.abspath(path))
    for parent in (absolute, *absolute.parents):
        if parent.is_symlink():
            raise DSLLoadError("DSL_PATH_SYMLINK", str(path), "路径不能经过符号链接")
    if not absolute.is_file():
        raise DSLLoadError("DSL_FILE_INVALID", str(path), "文件不存在或不是普通文件")
    return absolute


def _ensure_json_data(value: Any, location: str = "/") -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise DSLLoadError("DSL_NUMBER_INVALID", location, "YAML 数字不能为 NaN 或无穷")
        return value
    if isinstance(value, list):
        return [_ensure_json_data(item, f"{location}/{index}") for index, item in enumerate(value)]
    if isinstance(value, dict):
        output: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise DSLLoadError("DSL_KEY_INVALID", location, "DSL 对象键必须是文本")
            if key == "<<":
                raise DSLLoadError("DSL_MERGE_FORBIDDEN", f"{location}/{key}", "DSL 禁止 merge key")
            output[key] = _ensure_json_data(item, f"{location}/{key}")
        return output
    raise DSLLoadError("DSL_VALUE_INVALID", location, "DSL 只允许 JSON 兼容的纯数据")


def load_model(path: Path) -> dict[str, Any]:
    """Read a DSL YAML model without aliases, tags, timestamps, or executable values."""
    safe_path = _safe_regular_file(path)
    raw = safe_path.read_bytes()
    if len(raw) > MAX_MODEL_BYTES:
        raise DSLLoadError("DSL_FILE_TOO_LARGE", str(path), "DSL 文件超过安全大小限制")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DSLLoadError("DSL_ENCODING_INVALID", str(path), "DSL 必须为 UTF-8") from exc
    try:
        for token in yaml.scan(text, Loader=RestrictedLoader):
            if isinstance(token, (AliasToken, AnchorToken)):
                raise DSLLoadError("DSL_ALIAS_FORBIDDEN", str(path), "DSL 禁止 YAML anchors 和 aliases")
            if isinstance(token, TagToken):
                raise DSLLoadError("DSL_TAG_FORBIDDEN", str(path), "DSL 禁止显式 YAML tags")
        document = yaml.load(text, Loader=RestrictedLoader)
    except DSLLoadError:
        raise
    except yaml.YAMLError as exc:
        raise DSLLoadError("DSL_YAML_INVALID", str(path), str(exc)) from exc
    data = _ensure_json_data(document)
    if not isinstance(data, dict):
        raise DSLLoadError("DSL_ROOT_INVALID", "/", "DSL 根节点必须是对象")
    return data


def _load_schema() -> dict[str, Any]:
    path = _safe_regular_file(SCHEMA_PATH)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DSLLoadError("DSL_SCHEMA_INVALID", str(path), str(exc)) from exc
    if not isinstance(value, dict):
        raise DSLLoadError("DSL_SCHEMA_INVALID", str(path), "DSL Schema 根节点必须是对象")
    return value


def _schema_errors(model: dict[str, Any]) -> list[dict[str, str]]:
    try:
        schema = _load_schema()
        Draft202012Validator.check_schema(schema)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(model),
            key=lambda item: (list(item.absolute_path), item.message),
        )
        return [
            _error("DSL_SCHEMA_INVALID", _location(error.absolute_path), error.message)
            for error in errors
        ]
    except (DSLLoadError, exceptions.SchemaError) as exc:
        if isinstance(exc, DSLLoadError):
            return [_error(exc.code, exc.location, exc.message)]
        return [_error("DSL_SCHEMA_INVALID", "/schema", str(exc))]


def _index(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in items}


def _semantic_errors(model: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    def add(code: str, location: str, message: str) -> None:
        errors.append(_error(code, location, message))

    def check_ref(identifier: Any, candidates: set[str], location: str, label: str) -> None:
        if not isinstance(identifier, str) or identifier not in candidates:
            add("DSL_REFERENCE_UNDEFINED", location, f"{label} 未定义: {identifier}")

    sections = ("types", "temporal", "rules", "state_machines", "judgments", "constraints", "processes", "issues")
    ids: dict[str, str] = {}
    for section in sections:
        for index, item in enumerate(model[section]):
            identifier = item["id"]
            location = f"/{section}/{index}/id"
            if identifier in ids:
                add("DSL_ID_DUPLICATE", location, f"id 与 {ids[identifier]} 重复: {identifier}")
            else:
                ids[identifier] = location
    for machine_index, machine in enumerate(model["state_machines"]):
        for transition_index, transition in enumerate(machine["transitions"]):
            identifier = transition["id"]
            location = f"/state_machines/{machine_index}/transitions/{transition_index}/id"
            if identifier in ids:
                add("DSL_ID_DUPLICATE", location, f"id 与 {ids[identifier]} 重复: {identifier}")
            else:
                ids[identifier] = location

    for process_index, process in enumerate(model["processes"]):
        for step_index, step in enumerate(process["steps"]):
            location = f"/processes/{process_index}/steps/{step_index}/id"
            if step["id"] in ids:
                add("DSL_ID_DUPLICATE", location, f"重复 id: {step['id']}")
            else:
                ids[step["id"]] = location

    types = _index(model["types"])
    type_ids = set(types)
    type_names: set[str] = set()
    type_fields: dict[str, dict[str, dict[str, Any]]] = {}
    for type_index, type_def in enumerate(model["types"]):
        location = f"/types/{type_index}"
        if type_def["name"] in type_names:
            add("TYPE_NAME_DUPLICATE", location + "/name", "类型 name 必须唯一")
        type_names.add(type_def["name"])
        fields: dict[str, dict[str, Any]] = {}
        for field_index, field in enumerate(type_def["fields"]):
            field_location = f"{location}/fields/{field_index}"
            if field["name"] in fields:
                add("FIELD_NAME_DUPLICATE", field_location + "/name", "同一类型的字段 name 必须唯一")
            fields[field["name"]] = field
            cardinality = field["cardinality"]
            maximum = cardinality["max"]
            if maximum is not None and cardinality["min"] > maximum:
                add("CARDINALITY_INVALID", field_location + "/cardinality", "cardinality.min 不能大于 max")
        type_fields[type_def["id"]] = fields
        for identity_name in type_def["identity"]:
            identity_field = fields.get(identity_name)
            if identity_field is None:
                add("IDENTITY_FIELD_UNDEFINED", location + "/identity", f"identity 字段不存在: {identity_name}")
                continue
            cardinality = identity_field["cardinality"]
            if cardinality["min"] < 1 or cardinality["max"] != 1:
                add("IDENTITY_CARDINALITY_INVALID", location + "/identity", "身份字段必须单值且 min 为 1；缺证不能当作空身份")

    for type_index, type_def in enumerate(model["types"]):
        location = f"/types/{type_index}"
        fields = type_fields[type_def["id"]]
        for field_name, field in fields.items():
            if field["type"] == "Ref":
                check_ref(field["target"], type_ids, f"{location}/fields/{field_name}/target", "Ref target")
        if type_def["kind"] == "ROLE":
            bearer = fields.get(type_def["bearer_field"])
            if bearer is None:
                add("ROLE_BEARER_UNDEFINED", location + "/bearer_field", "ROLE 的 bearer_field 必须是字段")
            elif bearer["type"] != "Ref" or bearer["cardinality"]["min"] < 1 or bearer["cardinality"]["max"] != 1:
                add("ROLE_BEARER_INVALID", location + "/bearer_field", "ROLE bearer_field 必须是单值必填 Ref")
            elif bearer["target"] not in type_ids:
                add("ROLE_BEARER_TARGET_INVALID", location + "/bearer_field", "ROLE bearer_field 的 target 不存在")

    temporal_ids = {item["id"] for item in model["temporal"]}
    rule_ids = {item["id"] for item in model["rules"]}
    machine_ids = {item["id"] for item in model["state_machines"]}
    judgment_ids = {item["id"] for item in model["judgments"]}
    transition_ids = {
        transition["id"] for machine in model["state_machines"] for transition in machine["transitions"]
    }
    model_element_ids = set(ids) - {i["id"] for i in model["issues"]}
    issue_index = _index(model["issues"])
    issue_ids = set(issue_index)
    scope = set(model["question_scope_ids"])

    for temporal_index, temporal in enumerate(model["temporal"]):
        location = f"/temporal/{temporal_index}"
        check_ref(temporal["type_id"], type_ids, location + "/type_id", "Temporal type_id")
        fields = type_fields.get(temporal["type_id"], {})
        start = fields.get(temporal["start_field"])
        end = fields.get(temporal["end_field"])
        end_status = fields.get(temporal["end_status_field"])
        if start is None:
            add("TEMPORAL_START_UNDEFINED", location + "/start_field", "Temporal start_field 不存在")
        if end is None:
            add("TEMPORAL_END_UNDEFINED", location + "/end_field", "Temporal end_field 不存在")
        if len({temporal["start_field"], temporal["end_field"], temporal["end_status_field"]}) != 3:
            add("TEMPORAL_FIELDS_OVERLAP", location, "起点、终点和终止状态必须是不同字段")
        if start and start["cardinality"]["min"] != 1:
            add("TEMPORAL_START_REQUIRED", location, "时间起点必须为必需单值")
        if end and end["cardinality"]["min"] != 0:
            add("TEMPORAL_END_OPTIONAL", location, "终点必须允许未知或尚未终止")
        if start and end:
            if start["type"] not in {"Date", "DateTime"} or end["type"] != start["type"]:
                add("TEMPORAL_TYPE_INVALID", location, "start_field 和 end_field 必须同为单值 Date 或 DateTime")
            if start["cardinality"]["max"] != 1 or end["cardinality"]["max"] != 1:
                add("TEMPORAL_CARDINALITY_INVALID", location, "时间起止字段必须是单值")
        if end_status is None:
            add("TEMPORAL_STATUS_UNDEFINED", location + "/end_status_field", "Temporal end_status_field 不存在")
        elif end_status["type"] != "Enum" or not {"OPEN", "KNOWN", "UNKNOWN"}.issubset(set(end_status["values"])):
            add("TEMPORAL_STATUS_INVALID", location + "/end_status_field", "end_status_field 必须是含 OPEN、KNOWN、UNKNOWN 的 Enum")
        elif end_status["cardinality"]["max"] != 1 or end_status["cardinality"]["min"] != 1:
            add("TEMPORAL_STATUS_CARDINALITY_INVALID", location + "/end_status_field", "end_status_field 必须单值")

    for rule_index, rule in enumerate(model["rules"]):
        location = f"/rules/{rule_index}"
        environment: dict[str, ValueSpec] = {}
        for input_index, declaration in enumerate(rule["inputs"]):
            input_location = f"{location}/inputs/{input_index}"
            if declaration["name"] in environment:
                add("RULE_INPUT_DUPLICATE", input_location + "/name", "Rule 输入 name 必须唯一")
                continue
            try:
                spec = declaration_spec(declaration, input_location)
                if spec.target:
                    check_ref(spec.target, type_ids, input_location + "/target", "Rule 输入 target")
                environment[declaration["name"]] = spec
            except DSLExpressionError as exc:
                add(exc.code, exc.location, exc.message)
        try:
            result_spec = declaration_spec(rule["result"], location + "/result")
            if result_spec.target:
                check_ref(result_spec.target, type_ids, location + "/result/target", "Rule result target")
            expression_spec = infer_expression(rule["expression"], environment, types, location + "/expression")
            if not _same_type(expression_spec, result_spec):
                add("RULE_RESULT_TYPE_INVALID", location + "/result", "Rule expression 的结果类型与 result 不一致")
        except DSLExpressionError as exc:
            add(exc.code, exc.location, exc.message)

    for machine_index, machine in enumerate(model["state_machines"]):
        location = f"/state_machines/{machine_index}"
        check_ref(machine["type_id"], type_ids, location + "/type_id", "StateMachine type_id")
        fields = type_fields.get(machine["type_id"], {})
        state_field = fields.get(machine["state_field"])
        values: set[str] = set()
        if state_field is None:
            add("STATE_FIELD_UNDEFINED", location + "/state_field", "state_field 不存在")
        elif state_field["type"] != "Enum" or state_field["cardinality"]["max"] != 1 or state_field["cardinality"]["min"] != 1:
            add("STATE_FIELD_INVALID", location + "/state_field", "state_field 必须是单值 Enum")
        else:
            values = set(state_field["values"])
            if machine["initial"] not in values:
                add("STATE_INITIAL_INVALID", location + "/initial", "initial 必须属于 state_field 枚举")
        routes: set[tuple[str, str]] = set()
        guard_environment = {"self": ValueSpec("Ref", target=machine["type_id"])}
        for transition_index, transition in enumerate(machine["transitions"]):
            transition_location = f"{location}/transitions/{transition_index}"
            for source in transition["from"]:
                if source not in values:
                    add("STATE_SOURCE_INVALID", transition_location + "/from", "迁移 from 必须属于状态枚举")
                route = (source, transition["event"])
                if route in routes:
                    add("STATE_ROUTE_AMBIGUOUS", transition_location, "同一 source 和 event 不能有多个迁移")
                routes.add(route)
            if transition["to"] not in values:
                add("STATE_TARGET_INVALID", transition_location + "/to", "迁移 to 必须属于状态枚举")
            try:
                guard_spec = infer_expression(transition["guard"], guard_environment, types, transition_location + "/guard")
                if guard_spec.data_type != "Boolean" or guard_spec.max_items != 1:
                    add("STATE_GUARD_TYPE_INVALID", transition_location + "/guard", "迁移 guard 必须返回 Boolean")
            except DSLExpressionError as exc:
                add(exc.code, exc.location, exc.message)

    for judgment_index, judgment in enumerate(model["judgments"]):
        location = f"/judgments/{judgment_index}"
        names: set[str] = set()
        for collection_name in ("inputs", "outputs"):
            for item_index, declaration in enumerate(judgment[collection_name]):
                item_location = f"{location}/{collection_name}/{item_index}"
                if declaration["name"] in names:
                    add("JUDGMENT_IO_DUPLICATE", item_location + "/name", "Judgment 输入与输出 name 必须唯一")
                names.add(declaration["name"])
                try:
                    spec = declaration_spec(declaration, item_location)
                    if spec.target:
                        check_ref(spec.target, type_ids, item_location + "/target", "Judgment target")
                except DSLExpressionError as exc:
                    add(exc.code, exc.location, exc.message)
        role = types.get(judgment["responsible_role"])
        if role is None or role["kind"] != "ROLE":
            add("JUDGMENT_ROLE_INVALID", location + "/responsible_role", "responsible_role 必须引用 ROLE 类型")
        for question_id in judgment["question_ids"]:
            check_ref(question_id, scope, location + "/question_ids", "Judgment question_id")
        for issue_id in judgment["issue_ids"]:
            check_ref(issue_id, issue_ids, location + "/issue_ids", "Judgment issue_id")
        open_gaps = [issue_index[i] for i in judgment["issue_ids"] if i in issue_index and issue_index[i]["kind"] == "MODEL_GAP" and issue_index[i]["status"] == "OPEN"]
        if judgment["nature"] == "UNRESOLVED_POLICY" and (not open_gaps or not set(judgment["question_ids"]).issubset({q for i in open_gaps for q in i["affects"]})):
            add("JUDGMENT_GAP_REQUIRED", location, "未决业务口径必须有影响所有关联问题的开放 MODEL_GAP")

    upstream_issue_ids: set[str] = set()
    for binding_index, binding in enumerate(model["upstream_issue_bindings"]):
        location = f"/upstream_issue_bindings/{binding_index}"
        if binding["knowledge_issue_id"] in upstream_issue_ids:
            add("UPSTREAM_ISSUE_DUPLICATE", location + "/knowledge_issue_id", "knowledge_issue_id 只能绑定一次")
        upstream_issue_ids.add(binding["knowledge_issue_id"])
        for model_issue_id in binding["model_issue_ids"]:
            issue = issue_index.get(model_issue_id)
            if issue is None or issue["kind"] != "MODEL_GAP" or issue["status"] != "OPEN":
                add("UPSTREAM_BINDING_INVALID", location + "/model_issue_ids", "上游未决项必须绑定 OPEN MODEL_GAP")

    allowed_affects = model_element_ids | issue_ids | scope | upstream_issue_ids | {r["knowledge_rule_id"] for r in model["rule_coverage"]}
    for issue_index_value, issue in enumerate(model["issues"]):
        location = f"/issues/{issue_index_value}"
        for affected in issue["affects"]:
            check_ref(affected, allowed_affects, location + "/affects", "Issue affects")

    coverage_seen: set[str] = set()
    for coverage_index, coverage in enumerate(model["question_coverage"]):
        location = f"/question_coverage/{coverage_index}"
        question_id = coverage["question_id"]
        if question_id in coverage_seen:
            add("QUESTION_COVERAGE_DUPLICATE", location + "/question_id", "问题只能覆盖一次")
        coverage_seen.add(question_id)
        check_ref(question_id, scope, location + "/question_id", "Coverage question_id")
        for model_id in coverage["model_ids"]:
            check_ref(model_id, model_element_ids, location + "/model_ids", "Coverage model_id")
        expected_gaps = {
            identifier
            for identifier, issue in issue_index.items()
            if issue["kind"] == "MODEL_GAP" and issue["status"] == "OPEN" and question_id in issue["affects"]
        }
        if set(coverage["gap_ids"]) != expected_gaps:
            add("QUESTION_GAPS_INCOMPLETE", location + "/gap_ids", "必须列出所有影响该问题的 OPEN MODEL_GAP")
        if coverage["status"] == "MODELED":
            if not coverage["model_ids"] or coverage["gap_ids"]:
                add("COVERAGE_MODELED_INVALID", location, "MODELED 必须有模型要素且没有开放 MODEL_GAP")
        elif coverage["status"] == "PARTIAL":
            if not coverage["model_ids"] or not coverage["gap_ids"]:
                add("COVERAGE_PARTIAL_INVALID", location, "PARTIAL 必须有模型要素和开放 MODEL_GAP")
        elif coverage["status"] == "DEFERRED" and not coverage["gap_ids"]:
            add("COVERAGE_DEFERRED_INVALID", location, "DEFERRED 必须有开放 MODEL_GAP")
    if coverage_seen != scope:
        missing = sorted(scope - coverage_seen)
        extra = sorted(coverage_seen - scope)
        if missing:
            add("QUESTION_COVERAGE_MISSING", "/question_coverage", f"未覆盖问题: {missing}")
        if extra:
            add("QUESTION_COVERAGE_EXTRA", "/question_coverage", f"范围外问题: {extra}")

    coverage_by_question = {item["question_id"]: item for item in model["question_coverage"]}
    case_ids: set[str] = set()
    for case_index, case in enumerate(model["case_explanations"]):
        location = f"/case_explanations/{case_index}"
        if case["case_id"] in case_ids:
            add("CASE_EXPLANATION_DUPLICATE", location + "/case_id", "案例只能解释一次")
        case_ids.add(case["case_id"])
        for model_id in case["model_ids"]:
            check_ref(model_id, model_element_ids, location + "/model_ids", "Case model_id")
        if case["status"] == "EXPLAINED" and not case["model_ids"]:
            add("CASE_EXPLANATION_INVALID", location, "EXPLAINED 必须关联至少一个模型要素")
        if case["status"] == "BLOCKED" and not any(
            coverage["status"] in {"PARTIAL", "DEFERRED"} and coverage["gap_ids"]
            for coverage in coverage_by_question.values()
        ):
            add("CASE_BLOCKED_UNJUSTIFIED", location, "BLOCKED 案例必须有范围内开放模型缺口")

    from dsl_semantics import advanced_errors
    errors.extend(advanced_errors(model))
    return sorted(errors, key=lambda item: (item["location"], item["code"], item["message"]))


def _same_type(left: ValueSpec, right: ValueSpec) -> bool:
    from dsl_semantics import assignable
    return assignable(left, right)


def validate_model(model: dict[str, Any]) -> list[dict[str, str]]:
    """Return schema and semantic violations without reading upstream knowledge artifacts."""
    schema_errors = _schema_errors(model)
    if schema_errors:
        return schema_errors
    return _semantic_errors(model)


def _validated(model: dict[str, Any]) -> None:
    errors = validate_model(model)
    if errors:
        raise DSLLoadError("DSL_MODEL_INVALID", "/", json.dumps(errors, ensure_ascii=False))


def _types(model: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _index(model["types"])


def _json_value(value: Any) -> Any:
    from decimal import Decimal

    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    return value


def _record_constraints(model, value, spec, types, location):
    """Check constraints on supplied Ref records, including nested references."""
    if value is UNKNOWN or spec.data_type != "Ref":
        return []
    records = value if spec.is_collection else [value]
    failures = []
    for index, record in enumerate(records):
        if record is UNKNOWN:
            continue
        here = f"{location}/{index}" if spec.is_collection else location
        for constraint in model["constraints"]:
            if constraint["type_id"] != spec.target:
                continue
            result = evaluate_expression(constraint["expression"], {"self": record},
                                         {"self": spec.item()}, types, here)
            if result is not True:
                failures.append({"constraint": constraint["id"], "location": here,
                                 "outcome": "UNKNOWN" if result is UNKNOWN else "VIOLATED",
                                 "action": constraint["on_unknown"] if result is UNKNOWN else "BLOCK"})
        for field in types[spec.target]["fields"]:
            if field["type"] == "Ref" and field["name"] in record:
                failures.extend(_record_constraints(model, record[field["name"]],
                    field_spec(field, here), types, here + "/" + field["name"]))
    return failures


def evaluate_rule(model: dict[str, Any], rule_id: str, values: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate one declared rule; UNKNOWN is a valid, explicit outcome."""
    _validated(model)
    rules = _index(model["rules"])
    if rule_id not in rules:
        raise DSLLoadError("RULE_NOT_FOUND", "/rule_id", f"Rule 不存在: {rule_id}")
    if not isinstance(values, Mapping):
        raise DSLLoadError("RUNTIME_INPUT_INVALID", "/values", "Rule 输入必须是对象")
    rule = rules[rule_id]
    types = _types(model)
    environment = {
        declaration["name"]: declaration_spec(declaration, f"/rules/{rule_id}/inputs/{index}")
        for index, declaration in enumerate(rule["inputs"])
    }
    canonical = {name: validate_field_value(values.get(name), spec, types, "/inputs/" + name)
                 for name, spec in environment.items()}
    failures = []
    for name, spec in environment.items():
        failures.extend(_record_constraints(model, canonical[name], spec, types, "/inputs/" + name))
    if failures:
        return {"status": "BLOCKED", "value": None, "constraint_failures": failures}
    result = evaluate_expression(rule["expression"], canonical, environment, types, f"/rules/{rule_id}/expression")
    result_spec = declaration_spec(rule["result"], f"/rules/{rule_id}/result")
    result = validate_field_value(result, result_spec, types, f"/rules/{rule_id}/result")
    return {
        "status": "UNKNOWN" if result is UNKNOWN else "KNOWN",
        "value": _json_value(result),
    }


def evaluate_transition(model: dict[str, Any], machine_id: str, event: str, record: Mapping[str, Any]) -> dict[str, Any]:
    """Apply the unique true transition, or report BLOCKED/NO_TRANSITION explicitly."""
    _validated(model)
    machines = _index(model["state_machines"])
    if machine_id not in machines:
        raise DSLLoadError("MACHINE_NOT_FOUND", "/machine_id", f"StateMachine 不存在: {machine_id}")
    if not isinstance(event, str) or not event:
        raise DSLLoadError("EVENT_INVALID", "/event", "event 必须是非空文本")
    machine = machines[machine_id]
    types = _types(model)
    self_spec = ValueSpec("Ref", target=machine["type_id"])
    canonical_record = validate_ref(record, self_spec, types, "/record")
    if canonical_record is UNKNOWN:
        return {"status": "BLOCKED", "from": None, "to": None, "reason": "记录为 UNKNOWN"}
    failures = _record_constraints(model, canonical_record, self_spec, types, "/record")
    if failures:
        return {"status": "BLOCKED", "from": canonical_record.get(machine["state_field"]),
                "to": None, "reason": "记录约束未通过", "constraint_failures": failures}
    current = canonical_record.get(machine["state_field"], UNKNOWN)
    if current is UNKNOWN:
        return {"status": "BLOCKED", "from": None, "to": None, "reason": "当前状态缺失或未知"}
    matches = [
        transition
        for transition in machine["transitions"]
        if transition["event"] == event and current in transition["from"]
    ]
    if not matches:
        return {"status": "NO_TRANSITION", "from": current, "to": None, "reason": "没有匹配当前状态与事件的迁移"}
    transition = matches[0]
    guard = evaluate_expression(
        transition["guard"],
        {"self": canonical_record},
        {"self": self_spec},
        types,
        f"/state_machines/{machine_id}/transitions/{transition['id']}/guard",
    )
    if guard is True:
        return {"status": "APPLIED", "from": current, "to": transition["to"], "reason": "guard 为 true"}
    return {
        "status": "BLOCKED",
        "from": current,
        "to": transition["to"],
        "reason": "guard 为 UNKNOWN" if guard is UNKNOWN else "guard 为 false",
    }


def _markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    output.extend("| " + " | ".join(value.replace("|", "\\|").replace("\n", " ") for value in row) + " |" for row in rows)
    return output


def _cardinality(value: dict[str, Any]) -> str:
    return f"{value['min']}..{value['max'] if value['max'] is not None else '*'}"


def render_review(model: dict[str, Any]) -> str:
    _validated(model)
    from dsl_render import business_review
    return business_review(model)


def render_coverage(model: dict[str, Any]) -> str:
    _validated(model)
    from dsl_render import audit_coverage
    return audit_coverage(model)


def _load_json_input(path: Path) -> dict[str, Any]:
    safe_path = _safe_regular_file(path)
    try:
        def reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"重复 JSON 属性: {key}")
                result[key] = value
            return result

        value = json.loads(safe_path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise DSLLoadError("DSL_JSON_INPUT_INVALID", str(path), str(exc)) from exc
    if not isinstance(value, dict):
        raise DSLLoadError("DSL_JSON_INPUT_INVALID", str(path), "JSON 根节点必须是对象")
    return value


def _safe_output_dir(path: Path) -> Path:
    if _forbidden_path(path):
        raise DSLLoadError("DSL_OUTPUT_FORBIDDEN", str(path), "输出路径包含禁止名称")
    absolute = Path(os.path.abspath(path))
    for parent in (absolute, *absolute.parents):
        if parent.exists() and parent.is_symlink():
            raise DSLLoadError("DSL_OUTPUT_SYMLINK", str(path), "输出路径不能经过符号链接")
    absolute.mkdir(parents=True, exist_ok=True)
    if not absolute.is_dir():
        raise DSLLoadError("DSL_OUTPUT_INVALID", str(path), "输出路径不是目录")
    return absolute


def _print_json(value: Mapping[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "render"):
        command = commands.add_parser(name)
        command.add_argument("model", type=Path)
    commands.choices["render"].add_argument("--output-dir", type=Path, required=True)
    evaluate = commands.add_parser("evaluate")
    evaluate.add_argument("model", type=Path)
    evaluate.add_argument("--rule", required=True)
    evaluate.add_argument("--inputs", type=Path, required=True)
    transition = commands.add_parser("transition")
    transition.add_argument("model", type=Path)
    transition.add_argument("--machine", required=True)
    transition.add_argument("--event", required=True)
    transition.add_argument("--record", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        model = load_model(args.model)
        if args.command == "validate":
            errors = validate_model(model)
            _print_json({"status": "PASS" if not errors else "FAIL", "errors": errors})
            return 0 if not errors else 1
        if args.command == "render":
            _validated(model)
            output_dir = _safe_output_dir(args.output_dir)
            (output_dir / "review.md").write_text(render_review(model), encoding="utf-8")
            (output_dir / "coverage.md").write_text(render_coverage(model), encoding="utf-8")
            _print_json({"status": "PASS", "files": ["review.md", "coverage.md"]})
            return 0
        if args.command == "evaluate":
            result = evaluate_rule(model, args.rule, _load_json_input(args.inputs))
            _print_json(result)
            return 0
        result = evaluate_transition(model, args.machine, args.event, _load_json_input(args.record))
        _print_json(result)
        return 0
    except (DSLLoadError, DSLExpressionError) as exc:
        _print_json({"status": "ERROR", "errors": [_error(exc.code, exc.location, exc.message)]})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
