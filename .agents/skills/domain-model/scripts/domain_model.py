#!/usr/bin/env python3
"""Validate and render the business-first domain model and coverage artifacts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


SKILL_ROOT = Path(__file__).resolve().parents[1]
MODEL_SCHEMA = SKILL_ROOT / "contracts/business-domain-model.schema.json"
COVERAGE_SCHEMA = SKILL_ROOT / "contracts/coverage.schema.json"
COMMON_SCHEMA = SKILL_ROOT / "contracts/common.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON 根节点必须是对象")
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("YAML 根节点必须是对象")
    return value


def schema_registry() -> dict[str, dict[str, Any]]:
    schemas = {}
    for path in (COMMON_SCHEMA, MODEL_SCHEMA, COVERAGE_SCHEMA):
        schema = load_json(path)
        schemas[schema["$id"]] = schema
    return schemas


def validate_schema(instance: dict[str, Any], schema_path: Path) -> list[dict[str, str]]:
    schemas = schema_registry()
    schema = load_json(schema_path)
    validator = Draft202012Validator(
        schema,
        registry=Registry().with_resources(
            [(uri, Resource.from_contents(doc)) for uri, doc in schemas.items()]
        ),
        format_checker=FormatChecker(),
    )
    errors = []
    for error in sorted(validator.iter_errors(instance), key=lambda e: str(list(e.absolute_path))):
        location = "/" + "/".join(str(x) for x in error.absolute_path)
        errors.append({"code": "SCHEMA", "location": location or "/", "message": error.message})
    return errors


def duplicate(values: list[str]) -> set[str]:
    seen, dup = set(), set()
    for value in values:
        if value in seen:
            dup.add(value)
        seen.add(value)
    return dup


def model_refs(model: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    for obj in model["business_objects"]:
        refs.add(obj["id"])
        refs.update(f'{obj["id"]}.{a["name"]}' for a in obj["attributes"])
    for relation in model["business_relations"]:
        refs.add(relation["id"])
        refs.update(f'{relation["id"]}.{a["name"]}' for a in relation["attributes"])
    for decision in model["business_decisions"]:
        refs.add(decision["id"])
    for context in model["external_contexts"]:
        refs.add(context["id"])
    return refs


def validate_model(model: dict[str, Any]) -> list[dict[str, str]]:
    failures = validate_schema(model, MODEL_SCHEMA)

    groups = [
        model["business_objects"],
        model["business_relations"],
        model["business_decisions"],
        model["external_contexts"],
    ]
    ids = [item["id"] for group in groups for item in group]
    for identifier in sorted(duplicate(ids)):
        failures.append({"code": "DUPLICATE_MODEL_ID", "location": identifier, "message": "模型标识必须全局唯一"})

    object_ids = {x["id"] for x in model["business_objects"]}
    decision_ids = {x["id"] for x in model["business_decisions"]}
    context_ids = {x["id"] for x in model["external_contexts"]}
    allowed_refs = model_refs(model)

    for obj in model["business_objects"]:
        names = [a["name"] for a in obj["attributes"]]
        if duplicate(names):
            failures.append({"code": "DUPLICATE_ATTRIBUTE", "location": obj["id"], "message": "业务对象属性名必须唯一"})
        missing = set(obj["identity_attributes"]) - set(names)
        if missing:
            failures.append({"code": "IDENTITY_ATTRIBUTE_MISSING", "location": obj["id"], "message": "身份属性未定义: " + ", ".join(sorted(missing))})

    for relation in model["business_relations"]:
        roles = [p["role"] for p in relation["participants"]]
        if duplicate(roles):
            failures.append({"code": "DUPLICATE_PARTICIPANT_ROLE", "location": relation["id"], "message": "同一关系的参与角色必须唯一"})
        attribute_names = [a["name"] for a in relation["attributes"]]
        if duplicate(attribute_names):
            failures.append({"code": "DUPLICATE_RELATION_ATTRIBUTE", "location": relation["id"], "message": "同一关系属性名必须唯一"})
        for participant in relation["participants"]:
            if participant["object_id"] not in object_ids:
                failures.append({"code": "RELATION_OBJECT_UNDEFINED", "location": relation["id"], "message": f'参与对象未定义: {participant["object_id"]}'})

    for decision in model["business_decisions"]:
        for item in decision["inputs"]:
            if item["ref"] not in allowed_refs:
                failures.append({"code": "DECISION_INPUT_UNDEFINED", "location": decision["id"], "message": f'判断输入未定义: {item["ref"]}'})
        missing_context = set(decision["external_context_ids"]) - context_ids
        if missing_context:
            failures.append({"code": "DECISION_CONTEXT_UNDEFINED", "location": decision["id"], "message": "外部上下文未定义: " + ", ".join(sorted(missing_context))})
        values = [x["value"] for x in decision["outcomes"]]
        if duplicate(values):
            failures.append({"code": "DUPLICATE_DECISION_OUTCOME", "location": decision["id"], "message": "业务判断结果值必须唯一"})

    for context in model["external_contexts"]:
        unknown = set(context["used_by_decision_ids"]) - decision_ids
        if unknown:
            failures.append({"code": "CONTEXT_DECISION_UNDEFINED", "location": context["id"], "message": "引用了未定义业务判断: " + ", ".join(sorted(unknown))})
        input_names = [item["name"] for item in context["required_inputs"]]
        if duplicate(input_names):
            failures.append({"code": "DUPLICATE_CONTEXT_INPUT", "location": context["id"], "message": "同一外部上下文输入名称必须唯一"})

    return failures


def validate_coverage(coverage: dict[str, Any], model: dict[str, Any] | None = None) -> list[dict[str, str]]:
    failures = validate_schema(coverage, COVERAGE_SCHEMA)
    model_allowed = model_refs(model) if model else set()
    issue_ids = {x["id"] for x in coverage["model_issues"]}

    rule_ids = [x["knowledge_rule_id"] for x in coverage["rule_coverage"]]
    for identifier in sorted(duplicate(rule_ids)):
        failures.append({"code": "DUPLICATE_RULE_COVERAGE", "location": identifier, "message": "知识规则覆盖必须唯一"})

    for row in coverage["rule_coverage"]:
        classes = set(row["modeling_classification"])
        status = row["status"]
        refs = set(row["model_refs"])
        gaps = set(row["gap_ids"])
        if model is not None and not refs.issubset(model_allowed):
            failures.append({"code": "COVERAGE_MODEL_REF_UNDEFINED", "location": row["knowledge_rule_id"], "message": "覆盖引用包含未定义模型元素"})
        if not gaps.issubset(issue_ids):
            failures.append({"code": "COVERAGE_GAP_UNDEFINED", "location": row["knowledge_rule_id"], "message": "覆盖引用包含未定义模型缺口"})
        if "NO_MODEL_CHANGE" in classes and len(classes) != 1:
            failures.append({"code": "NO_MODEL_CHANGE_MIXED", "location": row["knowledge_rule_id"], "message": "NO_MODEL_CHANGE 必须单独使用"})
        if status == "MODELED" and (not refs or gaps):
            failures.append({"code": "RULE_STATUS_INVALID", "location": row["knowledge_rule_id"], "message": "MODELED 必须有模型引用且无缺口"})
        if status == "PARTIAL" and (not refs or not gaps):
            failures.append({"code": "RULE_STATUS_INVALID", "location": row["knowledge_rule_id"], "message": "PARTIAL 必须同时有模型引用和缺口"})
        if status == "DEFERRED" and not gaps:
            failures.append({"code": "RULE_STATUS_INVALID", "location": row["knowledge_rule_id"], "message": "DEFERRED 必须有模型缺口"})
        if status == "EXTERNAL_CONTEXT" and (classes != {"EXTERNAL_CONTEXT"} or refs or gaps):
            failures.append({"code": "RULE_STATUS_INVALID", "location": row["knowledge_rule_id"], "message": "纯外部上下文不得伪造核心模型引用或 MODEL_GAP"})
        if status == "NO_MODEL_CHANGE" and (classes != {"NO_MODEL_CHANGE"} or refs or gaps):
            failures.append({"code": "RULE_STATUS_INVALID", "location": row["knowledge_rule_id"], "message": "无模型变化不得伪造核心模型引用或 MODEL_GAP"})

    question_ids = [row["question_id"] for row in coverage["question_coverage"]]
    for identifier in sorted(duplicate(question_ids)):
        failures.append({"code": "DUPLICATE_QUESTION_COVERAGE", "location": identifier, "message": "业务问题覆盖必须唯一"})
    for row in coverage["question_coverage"]:
        refs = set(row["model_refs"])
        gaps = set(row["gap_ids"])
        if model is not None and not refs.issubset(model_allowed):
            failures.append({"code": "QUESTION_MODEL_REF_UNDEFINED", "location": row["question_id"], "message": "问题覆盖引用包含未定义模型元素"})
        if not gaps.issubset(issue_ids):
            failures.append({"code": "QUESTION_GAP_UNDEFINED", "location": row["question_id"], "message": "问题覆盖引用包含未定义 MODEL_GAP"})

    case_ids = [row["case_id"] for row in coverage["case_coverage"]]
    for identifier in sorted(duplicate(case_ids)):
        failures.append({"code": "DUPLICATE_CASE_COVERAGE", "location": identifier, "message": "案例覆盖必须唯一"})
    for row in coverage["case_coverage"]:
        refs = set(row["model_refs"])
        if model is not None and not refs.issubset(model_allowed):
            failures.append({"code": "CASE_MODEL_REF_UNDEFINED", "location": row["case_id"], "message": "案例覆盖引用包含未定义模型元素"})

    binding_ids = [row["knowledge_issue_id"] for row in coverage["upstream_issue_bindings"]]
    for identifier in sorted(duplicate(binding_ids)):
        failures.append({"code": "DUPLICATE_ISSUE_BINDING", "location": identifier, "message": "上游未决绑定必须唯一"})
    for binding in coverage["upstream_issue_bindings"]:
        mids = set(binding["model_issue_ids"])
        if not mids.issubset(issue_ids):
            failures.append({"code": "ISSUE_BINDING_UNDEFINED", "location": binding["knowledge_issue_id"], "message": "绑定了未定义 MODEL_GAP"})
        if binding["handling"] != "CORE_MODEL_GAP" and mids:
            failures.append({"code": "EXTERNAL_OPEN_PROMOTED_TO_GAP", "location": binding["knowledge_issue_id"], "message": "非核心未决不得创建 MODEL_GAP"})
        if binding["handling"] == "CORE_MODEL_GAP" and not mids:
            failures.append({"code": "CORE_GAP_MISSING", "location": binding["knowledge_issue_id"], "message": "核心未决必须绑定 MODEL_GAP"})

    return failures


def md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    esc = lambda x: str(x).replace("|", "\\|").replace("\n", "<br>")
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines += ["| " + " | ".join(esc(cell) for cell in row) + " |" for row in rows]
    return lines


def render_review(model: dict[str, Any]) -> str:
    category_labels = {
        "PARTICIPANT": "业务参与方",
        "BUSINESS_OBJECT": "业务对象",
        "EVIDENCE": "业务证据",
        "RESULT": "业务结果",
    }
    decision_labels = {
        "DETERMINISTIC": "确定性判断",
        "PROFESSIONAL_JUDGMENT": "专业判断",
        "MIXED": "混合判断",
    }
    lines = [
        f'# {model["name"]}：业务审阅稿', "",
        f'领域：{model["domain_name"]}', "",
        model["domain_purpose"], "",
        "## 业务世界总览", "",
        "### 业务对象", "",
    ]
    lines += md_table(
        ["业务对象", "类别", "业务定义"],
        [[x["name"], category_labels[x["category"]], x["definition"]] for x in model["business_objects"]],
    )
    lines += ["", "### 业务关系", ""]
    relation_rows = []
    labels = {x["id"]: x["name"] for x in model["business_objects"]}
    for rel in model["business_relations"]:
        participants = "；".join(f'{p["label"]}→{labels.get(p["object_id"], p["object_id"])}' for p in rel["participants"])
        relation_rows.append([rel["name"], participants, rel["definition"]])
    lines += md_table(["业务关系", "参与对象", "业务定义"], relation_rows)
    lines += ["", "### 核心业务判断", ""]
    lines += md_table(
        ["业务判断", "业务问题", "判断方式", "可能结果"],
        [
            [d["name"], d["business_question"], decision_labels[d["decision_mode"]], "、".join(o["label"] for o in d["outcomes"])]
            for d in model["business_decisions"]
        ],
    )
    lines += ["", "### 外部上下文边界", ""]
    if model["external_contexts"]:
        lines += md_table(
            ["外部上下文", "来源领域", "本模型只消费什么"],
            [[x["name"], x["source_domain"], "；".join(i["meaning"] for i in x["required_inputs"])] for x in model["external_contexts"]],
        )
    else:
        lines.append("本模型不依赖外部上下文。")

    lines += ["", "## 业务对象详解", ""]
    for obj in model["business_objects"]:
        lines += [
            f'### {obj["name"]}', "",
            obj["definition"], "",
            f'**如何识别同一业务对象：** {obj["identity_description"]}', "",
        ]
        lines += md_table(
            ["业务属性", "类型", "数量", "业务含义"],
            [
                [
                    a["label"],
                    a["type"] + ("/" + "、".join(a.get("values", [])) if a["type"] == "Enum" else ""),
                    f'{a["cardinality"]["min"]}..{"*" if a["cardinality"]["max"] is None else a["cardinality"]["max"]}',
                    a["meaning"],
                ]
                for a in obj["attributes"]
            ],
        )
        lines += ["", "**例子：** " + "；".join(obj["examples"]), "", "**不能混同：** " + "；".join(obj["counterexamples"]), ""]

    lines += ["## 业务关系详解", ""]
    for rel in model["business_relations"]:
        lines += [f'### {rel["name"]}', "", rel["definition"], ""]
        lines += md_table(
            ["参与角色", "业务对象", "数量", "含义"],
            [
                [
                    p["label"], labels.get(p["object_id"], p["object_id"]),
                    f'{p["cardinality"]["min"]}..{"*" if p["cardinality"]["max"] is None else p["cardinality"]["max"]}',
                    p["meaning"],
                ]
                for p in rel["participants"]
            ],
        )
        lines += ["", f'**时间语义：** {rel["temporal_semantics"]}', "", f'**证据语义：** {rel["evidence_semantics"]}', "",
                  "**例子：** " + "；".join(rel["examples"]), "", "**不能混同：** " + "；".join(rel["counterexamples"]), ""]

    lines += ["## 业务判断详解", ""]
    for decision in model["business_decisions"]:
        lines += [f'### {decision["name"]}', "", f'**业务问题：** {decision["business_question"]}', "", decision["definition"], ""]
        lines += ["**判断输入：**"] + [f'- {i["meaning"]}' for i in decision["inputs"]] + [""]
        lines += ["**判断准则：**"] + [f'- {x}' for x in decision["criteria"]] + [""]
        if decision["non_sufficient_facts"]:
            lines += ["**单独不足以证明结论：**"] + [f'- {x}' for x in decision["non_sufficient_facts"]] + [""]
        lines += [f'**缺证/未知：** {decision["unknown_behavior"]}', ""]
        if decision["evidence_requirements"]:
            lines += ["**需要的证据：**"] + [f'- {x}' for x in decision["evidence_requirements"]] + [""]
        lines += [f'**人工边界：** {decision["human_boundary"]}', "",
                  f'**结果落地语义：** {decision["result_semantics"]}', ""]
    return "\n".join(lines).rstrip() + "\n"


def render_coverage(coverage: dict[str, Any]) -> str:
    lines = [f'# {coverage["artifact_id"]}：覆盖与审计', "",
             f'覆盖版本：{coverage["content_version"]}；范围模式：{coverage["scope_mode"]}。', "",
             "## 规则覆盖", ""]
    lines += md_table(
        ["知识规则", "建模分类", "状态", "模型引用", "MODEL_GAP", "理由"],
        [
            [
                r["knowledge_rule_id"],
                " + ".join(r["modeling_classification"]),
                r["status"],
                ", ".join(r["model_refs"]),
                ", ".join(r["gap_ids"]),
                r["reason"],
            ]
            for r in coverage["rule_coverage"]
        ],
    )
    lines += ["", "## 问题覆盖", ""]
    lines += md_table(
        ["问题", "状态", "模型引用", "缺口", "说明"],
        [[q["question"], q["status"], ", ".join(q["model_refs"]), ", ".join(q["gap_ids"]), q["reason"]] for q in coverage["question_coverage"]],
    )
    lines += ["", "## 案例覆盖", ""]
    lines += md_table(
        ["案例", "状态", "模型引用", "解释"],
        [[c["case_id"], c["status"], ", ".join(c["model_refs"]), c["explanation"]] for c in coverage["case_coverage"]],
    )
    lines += ["", "## 上游 OPEN 去向", ""]
    lines += md_table(
        ["上游事项", "处理", "MODEL_GAP", "说明"],
        [[x["knowledge_issue_id"], x["handling"], ", ".join(x["model_issue_ids"]), x["reason"]] for x in coverage["upstream_issue_bindings"]],
    )
    lines += ["", "## 真正的核心模型缺口", ""]
    if coverage["model_issues"]:
        lines += md_table(
            ["缺口", "影响", "责任", "解决前处理"],
            [[x["statement"], ", ".join(x["affects"]), x["owner"], x["until_resolved"]] for x in coverage["model_issues"]],
        )
    else:
        lines.append("当前没有核心 MODEL_GAP。")
    return "\n".join(lines).rstrip() + "\n"


def report(failures: list[dict[str, str]]) -> dict[str, Any]:
    return {"status": "PASS" if not failures else "FAIL", "failures": failures}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("validate")
    p.add_argument("model", type=Path)
    p = sub.add_parser("validate-coverage")
    p.add_argument("coverage", type=Path)
    p.add_argument("--model", type=Path)
    p = sub.add_parser("render-review")
    p.add_argument("model", type=Path)
    p = sub.add_parser("render-coverage")
    p.add_argument("coverage", type=Path)
    args = parser.parse_args()

    try:
        if args.command == "validate":
            result = report(validate_model(load_yaml(args.model)))
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["status"] == "PASS" else 1
        if args.command == "validate-coverage":
            model = load_yaml(args.model) if args.model else None
            result = report(validate_coverage(load_json(args.coverage), model))
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["status"] == "PASS" else 1
        if args.command == "render-review":
            print(render_review(load_yaml(args.model)), end="")
            return 0
        if args.command == "render-coverage":
            print(render_coverage(load_json(args.coverage)), end="")
            return 0
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "failures": [{"code": "LOAD_FAILED", "message": str(exc)}]}, ensure_ascii=False, indent=2))
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
