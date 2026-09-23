"""Business reference and coverage checks for platform-independent domain assets."""
from __future__ import annotations

import hashlib
from collections import Counter
from graphlib import CycleError, TopologicalSorter
from typing import Any


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def index(items, key="id"):
    return {item[key]: item for item in items}


def check_source_inventory(payload: dict[str, Any], failures: list[dict[str, str]]) -> None:
    """Validate parser-block preservation and one-owner semantic reconstruction."""
    def fail(code, location, message):
        failures.append({"code": code, "location": location, "message": message})

    sources = index(payload.get("sources", []), "source_id")

    block_rows = payload.get("source_blocks", [])
    block_counts = Counter(item["block_id"] for item in block_rows)
    for block_id, count in block_counts.items():
        if count != 1:
            fail("SOURCE_BLOCK_ID_DUPLICATE", "source_blocks", f"来源块标识重复: {block_id}")
    blocks = index(block_rows, "block_id")
    block_sequences: dict[str, Counter] = {}
    for block_id, block in blocks.items():
        source_id = block["source_id"]
        if source_id not in sources:
            fail("SOURCE_BLOCK_SOURCE_UNDEFINED", block_id, f"来源块引用未声明来源: {source_id}")
        digest = "sha256:" + hashlib.sha256(block["text"].encode("utf-8")).hexdigest()
        if block["digest"] != digest:
            fail("SOURCE_BLOCK_DIGEST_MISMATCH", block_id, "来源块文本摘要不匹配")
        block_sequences.setdefault(source_id, Counter())[block["sequence"]] += 1
    for source_id, counts in block_sequences.items():
        for sequence, count in counts.items():
            if count != 1:
                fail("SOURCE_BLOCK_SEQUENCE_DUPLICATE", source_id, f"同一来源出现重复块顺序: {sequence}")

    unit_rows = payload.get("source_units", [])
    unit_counts = Counter(item["unit_id"] for item in unit_rows)
    for unit_id, count in unit_counts.items():
        if count != 1:
            fail("SOURCE_UNIT_ID_DUPLICATE", "source_units", f"语义单元标识重复: {unit_id}")
    units = index(unit_rows, "unit_id")
    unit_sequences: dict[str, Counter] = {}
    block_owners: Counter = Counter()

    for unit_id, unit in units.items():
        source_id = unit["source_id"]
        if source_id not in sources:
            fail("SOURCE_UNIT_SOURCE_UNDEFINED", unit_id, f"语义单元引用未声明来源: {source_id}")
        digest = "sha256:" + hashlib.sha256(unit["text"].encode("utf-8")).hexdigest()
        if unit["digest"] != digest:
            fail("SOURCE_UNIT_DIGEST_MISMATCH", unit_id, "语义单元文本摘要不匹配")

        parent_id = unit.get("parent_unit_id")
        if parent_id:
            parent = units.get(parent_id)
            if parent is None:
                fail("SOURCE_UNIT_PARENT_UNDEFINED", unit_id, f"父级语义单元不存在: {parent_id}")
            elif parent["source_id"] != source_id:
                fail("SOURCE_UNIT_PARENT_SOURCE_MISMATCH", unit_id, "父子语义单元必须属于同一来源文档")

        for block_id in unit.get("source_block_ids", []):
            block_owners[block_id] += 1
            block = blocks.get(block_id)
            if block is None:
                fail("SOURCE_UNIT_BLOCK_UNDEFINED", unit_id, f"语义单元引用未定义来源块: {block_id}")
            elif block["source_id"] != source_id:
                fail("SOURCE_UNIT_BLOCK_SOURCE_MISMATCH", unit_id, f"语义单元与来源块不属于同一来源: {block_id}")

        unit_sequences.setdefault(source_id, Counter())[unit["sequence"]] += 1

    for source_id, counts in unit_sequences.items():
        for sequence, count in counts.items():
            if count != 1:
                fail("SOURCE_UNIT_SEQUENCE_DUPLICATE", source_id, f"同一来源出现重复语义顺序: {sequence}")

    for block_id in blocks:
        owner_count = block_owners[block_id]
        if owner_count == 0:
            fail("SOURCE_BLOCK_UNOWNED", block_id, "来源块没有归属任何语义单元")
        elif owner_count != 1:
            fail("SOURCE_BLOCK_MULTI_OWNED", block_id, f"来源块被 {owner_count} 个语义单元重复归属")
    for block_id in block_owners:
        if block_id not in blocks:
            fail("SOURCE_BLOCK_UNDEFINED", "source_units", f"语义单元引用不存在的来源块: {block_id}")

    extraction_rows = payload.get("source_extractions", [])
    extraction_counts = Counter(item["source_id"] for item in extraction_rows)
    for source_id, count in extraction_counts.items():
        if count != 1:
            fail("SOURCE_EXTRACTION_DUPLICATE", "source_extractions", f"来源抽取记录重复: {source_id}")
    extractions = index(extraction_rows, "source_id")
    if set(extractions) != set(sources):
        for source_id in sorted(set(sources) - set(extractions)):
            fail("SOURCE_EXTRACTION_MISSING", "source_extractions", f"来源没有抽取记录: {source_id}")
        for source_id in sorted(set(extractions) - set(sources)):
            fail("SOURCE_EXTRACTION_UNKNOWN", "source_extractions", f"抽取记录引用未声明来源: {source_id}")

    for source_id, extraction in extractions.items():
        declared_blocks = set(extraction["block_ids"])
        actual_blocks = {
            block_id for block_id, block in blocks.items()
            if block["source_id"] == source_id
        }
        if declared_blocks != actual_blocks:
            for block_id in sorted(actual_blocks - declared_blocks):
                fail("SOURCE_BLOCK_NOT_DECLARED", source_id, f"抽取记录遗漏来源块: {block_id}")
            for block_id in sorted(declared_blocks - actual_blocks):
                fail("SOURCE_BLOCK_UNDEFINED", source_id, f"抽取记录包含未定义来源块: {block_id}")

        declared_units = set(extraction["unit_ids"])
        actual_units = {
            unit_id for unit_id, unit in units.items()
            if unit["source_id"] == source_id
        }
        if declared_units != actual_units:
            for unit_id in sorted(actual_units - declared_units):
                fail("SOURCE_UNIT_NOT_DECLARED", source_id, f"抽取记录遗漏语义单元: {unit_id}")
            for unit_id in sorted(declared_units - actual_units):
                fail("SOURCE_UNIT_UNDEFINED", source_id, f"抽取记录包含未定义语义单元: {unit_id}")

        if extraction["status"] == "FAILED" and (actual_blocks or actual_units):
            fail("FAILED_EXTRACTION_HAS_CONTENT", source_id, "FAILED 结果不能声明来源块或语义单元")
        if extraction["status"] != "FAILED" and (not actual_blocks or not actual_units):
            fail("SOURCE_WITHOUT_CONTENT", source_id, "非 FAILED 来源必须至少有一个来源块和一个语义单元")

        parser = extraction.get("parser")
        if parser and source_id in sources:
            expected_digest = sources[source_id]["artifact"]["digest"]
            if parser["input_digest"] != expected_digest:
                fail("PARSER_INPUT_DIGEST_MISMATCH", source_id, "解析器 input_digest 必须绑定当前原始来源文档字节")


def check_content(payload: dict[str, Any], failures: list[dict[str, str]], knowledge=None, request=None):
    """Check declared references; business truth still needs domain review."""
    def fail(code, location, message):
        failures.append({"code": code, "location": location, "message": message})

    def refs(values, allowed, location):
        for value in values:
            if value not in allowed:
                fail("REFERENCE_UNDEFINED", location, f"未定义或类型不符的引用: {value}")

    def exact_coverage(values, expected, location):
        counts = Counter(values)
        for value in sorted(expected - counts.keys()):
            fail("COVERAGE_MISSING", location, f"未覆盖: {value}")
        for value, count in counts.items():
            if value not in expected or count != 1:
                fail("COVERAGE_INVALID", location, f"范围外或重复覆盖: {value}")

    def acyclic(graph, location):
        try:
            tuple(TopologicalSorter(graph).static_order())
        except CycleError as exc:
            fail("REFERENCE_CYCLE", location, f"循环依赖: {exc.args[1]}")

    content = payload["content"]
    issues = index(payload["issues"])
    evidence_ids = {item["evidence_id"] for item in payload["evidence"]}
    artifact_ids = {item["artifact_id"] for item in objects(payload) if "artifact_id" in item}
    local_ids = {item["id"] for item in objects(payload) if "id" in item}
    allowed = artifact_ids | local_ids | evidence_ids
    if payload["mode"] == "REVIEW":
        for subject in content["subjects"]:
            if subject not in payload["input_refs"]:
                fail("REVIEW_SUBJECT_UNBOUND", "content/subjects", "审查对象必须是精确输入引用")
    elif payload["stage"] == "domain-knowledge":
        sources = index(content["sources"], "source_id")
        statements = index(content["statements"])
        terms = index(content["terms"])
        questions = index(content["questions"])
        rules = index(content["rules"])
        cases = index(content["cases"])
        coverage = index(content["provision_coverage"])
        discovery = content["question_discovery"]
        candidates = index(discovery["candidates"])
        process_checks = index(discovery["process_checks"])
        allowed |= sources.keys()
        if request is None:
            fail("SOURCE_INVENTORY_REQUIRED", "input_refs", "领域知识输出必须绑定含条款清单的精确输入")
            source_units = {}
        else:
            source_units = index(request["source_units"], "unit_id")
            requested_sources = index(request["sources"], "source_id")
            if set(sources) != set(requested_sources):
                fail("SOURCE_SET_MISMATCH", "content/sources", "输出来源集合必须与输入来源集合完全一致")
            for source_id in set(sources).intersection(requested_sources):
                if sources[source_id] != requested_sources[source_id]:
                    fail("SOURCE_REF_MISMATCH", source_id, "输出来源必须逐字节沿用输入 SourceRef")
        for item in statements.values():
            refs(item["source_ids"], sources, item["id"] + "/source_ids")
            refs(item["source_unit_ids"], source_units, item["id"] + "/source_unit_ids")
            unit_sources = {source_units[unit_id]["source_id"] for unit_id in item["source_unit_ids"] if unit_id in source_units}
            if unit_sources != set(item["source_ids"]):
                fail("STATEMENT_SOURCE_MISMATCH", item["id"], "陈述的来源集合必须与所引条款单元来源完全一致")
            refs(item.get("supporting_statement_ids", []), statements, item["id"] + "/supporting_statement_ids")
        acyclic({key: value.get("supporting_statement_ids", []) for key, value in statements.items()}, "statements")
        for item in questions.values():
            parent_id = item.get("parent_question_id")
            if parent_id is not None:
                refs([parent_id], questions, item["id"] + "/parent_question_id")
        acyclic(
            {
                key: [value["parent_question_id"]] if "parent_question_id" in value else []
                for key, value in questions.items()
            },
            "questions/parent_question_id",
        )
        scope_questions = set(discovery["scope_question_ids"])
        refs(scope_questions, questions, "question_discovery/scope_question_ids")
        for item in candidates.values():
            refs(item["source_unit_ids"], source_units, item["id"] + "/source_unit_ids")
            refs(item["target_question_ids"], scope_questions, item["id"] + "/target_question_ids")
            refs(item["issue_ids"], issues, item["id"] + "/issue_ids")
            if item["disposition"] == "OPEN":
                gaps = {
                    issue_id
                    for issue_id in item["issue_ids"]
                    if issue_id in issues
                    and issues[issue_id]["kind"] == "KNOWLEDGE_GAP"
                    and issues[issue_id]["status"] == "OPEN"
                    and item["id"] in issues[issue_id]["affects"]
                }
                if not gaps:
                    fail("QUESTION_CANDIDATE_GAP_REQUIRED", item["id"], "OPEN 候选问题必须关联影响该候选的开放知识缺口")
        for item in process_checks.values():
            refs(item["source_unit_ids"], source_units, item["id"] + "/source_unit_ids")
            refs(item["question_ids"], scope_questions, item["id"] + "/question_ids")
            refs(item["issue_ids"], issues, item["id"] + "/issue_ids")
            if item["status"] in {"COVERED", "GAP"} and not item["question_ids"]:
                fail("PROCESS_CHECK_SCOPE_REQUIRED", item["id"], "已覆盖或有缺口的流程核对必须指向已声明范围内的业务问题")
            if item["status"] == "GAP":
                gaps = {
                    issue_id
                    for issue_id in item["issue_ids"]
                    if issue_id in issues
                    and issues[issue_id]["kind"] == "KNOWLEDGE_GAP"
                    and issues[issue_id]["status"] == "OPEN"
                    and item["id"] in issues[issue_id]["affects"]
                }
                if not gaps:
                    fail("PROCESS_CHECK_GAP_REQUIRED", item["id"], "GAP 流程核对必须关联影响该核对的开放知识缺口")
        candidate_targets = {q for item in candidates.values() for q in item["target_question_ids"]}
        for question_id in scope_questions - candidate_targets:
            if not any(issue["kind"] == "KNOWLEDGE_GAP" and issue["status"] == "OPEN" and question_id in issue["affects"] for issue in issues.values()):
                fail("QUESTION_DISCOVERY_SCOPE_UNACCOUNTED", question_id, "本轮问题须回指候选去向或显式开放知识缺口")
        if not process_checks:
            fail("PROCESS_CHECK_REQUIRED", "question_discovery/process_checks", "必须记录适用流程补查，或明确不适用理由")
        for item in terms.values():
            refs(item["statement_ids"], statements, item["id"] + "/statement_ids")
        for item in rules.values():
            refs(item["statement_ids"], statements, item["id"] + "/statement_ids")
            refs(item["question_ids"], questions, item["id"] + "/question_ids")
        for item in (*statements.values(), *rules.values()):
            conflicts = {key: issue for key, issue in issues.items() if issue["kind"] == "CONFLICT"}
            refs(item["conflict_ids"], conflicts, item["id"] + "/conflict_ids")
            for conflict_id in item["conflict_ids"]:
                conflict = conflicts.get(conflict_id)
                if conflict and item["id"] not in conflict["affects"]:
                    fail("CONFLICT_BINDING_INVALID", item["id"], "冲突没有关联当前陈述或规则")
                if conflict and item["dispute_status"] == "RESOLVED" and conflict["status"] != "RESOLVED":
                    fail("CONFLICT_UNRESOLVED", item["id"], "冲突记录尚未解决")
        for item in cases.values():
            refs(item["question_ids"], questions, item["id"] + "/question_ids")
            refs(item["source_ids"], sources, item["id"] + "/source_ids")
        exact_coverage([row["question_id"] for row in content["case_coverage"]], set(questions), "case_coverage")
        for row in content["case_coverage"]:
            refs(row["case_ids"], cases, "case_coverage/case_ids")
            gaps = {key for key, item in issues.items() if item["kind"] == "KNOWLEDGE_GAP" and item["status"] == "OPEN" and row["question_id"] in item["affects"]}
            refs(row["gap_ids"], gaps, "case_coverage/gap_ids")
            linked = {key for key, item in cases.items() if row["question_id"] in item["question_ids"]}
            if set(row["case_ids"]) != linked:
                fail("CASE_COVERAGE_MISMATCH", row["question_id"], "案例目录与能力问题覆盖不一致")
            represented = {cases[key]["kind"] for key in row["case_ids"] if key in cases}
            excluded = [item["kind"] for item in row["not_applicable"]]
            if len(excluded) != len(set(excluded)) or represented.intersection(excluded):
                fail("CASE_APPLICABILITY_CONFLICT", row["question_id"], "同类案例同时声明覆盖、不适用或重复排除")
            if not row["case_ids"] and not row["not_applicable"] and not row["gap_ids"]:
                fail("CASE_COVERAGE_EMPTY", row["question_id"], "案例覆盖必须给出具体案例、明确不适用说明或开放知识缺口")
        exact_coverage([row["source_unit_id"] for row in coverage.values()], set(source_units), "provision_coverage")
        for item in coverage.values():
            source_unit = source_units.get(item["source_unit_id"])
            refs(item["statement_ids"], statements, item["id"] + "/statement_ids")
            refs(item["term_ids"], terms, item["id"] + "/term_ids")
            refs(item["question_ids"], questions, item["id"] + "/question_ids")
            refs(item["rule_ids"], rules, item["id"] + "/rule_ids")
            refs(item["case_ids"], cases, item["id"] + "/case_ids")
            refs(item["issue_ids"], issues, item["id"] + "/issue_ids")
            for statement_id in item["statement_ids"]:
                statement = statements.get(statement_id)
                if statement and item["source_unit_id"] not in statement["source_unit_ids"]:
                    fail("PROVISION_STATEMENT_MISMATCH", item["id"], f"关联陈述未引用当前条款单元: {statement_id}")
            mapped = item["statement_ids"] + item["term_ids"] + item["question_ids"] + item["rule_ids"] + item["case_ids"]
            if item["status"] == "COVERED" and not mapped:
                fail("PROVISION_MAPPING_REQUIRED", item["id"], "COVERED 条款必须关联至少一个知识对象")
            if source_unit and source_unit["text"] == "[UNREADABLE_OR_EMPTY]" and item["status"] != "UNREADABLE":
                fail("UNREADABLE_STATUS_REQUIRED", item["id"], "不可读输入单元必须标记为 UNREADABLE")
            if item["status"] == "OUT_OF_SCOPE" and item["meaning_status"] != "NOT_APPLICABLE":
                fail("OUT_OF_SCOPE_MEANING_STATUS_INVALID", item["id"], "OUT_OF_SCOPE 条款必须标记为 NOT_APPLICABLE")
            if item["meaning_status"] == "NOT_APPLICABLE" and item["status"] != "OUT_OF_SCOPE":
                fail("NOT_APPLICABLE_SCOPE_STATUS_INVALID", item["id"], "NOT_APPLICABLE 仅用于 OUT_OF_SCOPE 条款")
            if item["status"] == "UNREADABLE" and item["meaning_status"] == "REVIEWED":
                fail("UNREADABLE_MEANING_REVIEW_INVALID", item["id"], "不可读条款不能标记为已完成业务含义审查")
            meaning_gaps = {
                issue_id
                for issue_id in item["issue_ids"]
                if issue_id in issues
                and issues[issue_id]["kind"] == "KNOWLEDGE_GAP"
                and issues[issue_id]["status"] == "OPEN"
                and item["id"] in issues[issue_id]["affects"]
            }
            if item["meaning_status"] in {"PARTIAL", "NOT_REVIEWED"} and not meaning_gaps:
                fail("PROVISION_MEANING_GAP_REQUIRED", item["id"], "未完成或部分完成业务含义审查的条款必须关联开放知识缺口")
            if item["meaning_status"] == "REVIEWED":
                meaningful_statements = [
                    statement_id
                    for statement_id in item["statement_ids"]
                    if statement_id in statements
                    and statements[statement_id]["meaning_kind"] != "SOURCE_EXCERPT"
                    and item["source_unit_id"] in statements[statement_id]["source_unit_ids"]
                ]
                if not meaningful_statements:
                    fail("PROVISION_MEANING_STATEMENT_REQUIRED", item["id"], "REVIEWED 条款必须关联当前单元的非 SOURCE_EXCERPT 业务陈述")
            if item["status"] in {"PARTIAL", "UNREADABLE"}:
                if not meaning_gaps:
                    fail("PROVISION_GAP_REQUIRED", item["id"], "PARTIAL 或 UNREADABLE 条款必须关联开放的知识缺口")
        refs(payload["confirmation"]["scope_ids"], questions, "confirmation/scope_ids")
    elif payload["stage"] == "domain-model":
        if knowledge is None:
            fail("KNOWLEDGE_REQUIRED", "content/knowledge_ref", "模型输出必须绑定可核对的知识基线")
            return
        kc = knowledge["content"]
        statements, terms = index(kc["statements"]), index(kc["terms"])
        rules, questions, cases = index(kc["rules"]), index(kc["questions"]), index(kc["cases"])
        knowledge_ids = statements.keys() | terms.keys() | rules.keys() | questions.keys() | cases.keys()
        allowed |= knowledge_ids
        allowed |= {s["source_id"] for s in kc["sources"]}
        concepts = index(content["concepts"])
        attributes = index(content["attributes"])
        relationships = index(content["relationships"])
        mechanisms = index(content["mechanisms"])
        policies = {
            policy["id"]: policy
            for aspect in content["semantics"].values()
            for policy in aspect["policies"]
        }
        model_ids = concepts.keys() | attributes.keys() | relationships.keys() | mechanisms.keys() | policies.keys()
        core_ids = concepts.keys() | attributes.keys() | relationships.keys()
        for collision in sorted(model_ids & knowledge_ids):
            fail("ID_NAMESPACE_COLLISION", collision, "模型新标识不能与知识标识重复；请使用明确前缀")
        scope = set(content["question_scope_ids"])
        refs(scope, questions, "question_scope_ids")
        refs(scope, set(knowledge["confirmation"]["scope_ids"]), "knowledge/confirmation_scope")
        if set(payload["confirmation"]["scope_ids"]) != scope:
            fail("CONFIRMATION_SCOPE_MISMATCH", "confirmation/scope_ids", "模型确认范围必须与能力问题范围一致")
        if content["knowledge_ref"] not in payload["input_refs"]:
            fail("KNOWLEDGE_REF_UNBOUND", "content/knowledge_ref", "知识基线必须登记为精确输入引用")
        basis_ids = statements.keys() | terms.keys() | rules.keys()
        for item in (*concepts.values(), *attributes.values(), *relationships.values(), *policies.values()):
            refs(item["basis_ids"], basis_ids, item["id"] + "/basis_ids")
        for item in concepts.values():
            refs(item.get("parent_ids", []), concepts, item["id"] + "/parent_ids")
            if "role_bearer_id" in item:
                refs([item["role_bearer_id"]], concepts, item["id"] + "/role_bearer_id")
        acyclic({key: value.get("parent_ids", []) for key, value in concepts.items()}, "concepts/parent_ids")
        for item in attributes.values():
            refs([item["owner_id"]], concepts.keys() | relationships.keys(), item["id"] + "/owner_id")
        for item in relationships.values():
            refs([item["from_id"], item["to_id"]], concepts, item["id"] + "/endpoints")
        for item in objects(content):
            if set(item) == {"min", "max"} and item["max"] is not None and item["min"] > item["max"]:
                fail("CARDINALITY_INVALID", "content", "基数最小值超过最大值")
        for policy in policies.values():
            refs(policy["applies_to_ids"], core_ids, policy["id"] + "/applies_to_ids")
        for item in mechanisms.values():
            refs(item["rule_ids"], rules, item["id"] + "/rule_ids")
            refs(item["question_ids"], scope, item["id"] + "/question_ids")
            refs(item["input_ids"], core_ids, item["id"] + "/input_ids")
            refs(item["output_ids"], core_ids, item["id"] + "/output_ids")
            refs(item["policy_ids"], policies, item["id"] + "/policy_ids")
            available = set(item["input_ids"])
            produced = set()
            for step in item["steps"]:
                refs(step["input_ids"], core_ids, step["id"] + "/input_ids")
                refs(step["input_ids"], available, step["id"] + "/available_inputs")
                refs(step["output_ids"], core_ids, step["id"] + "/output_ids")
                refs(step["rule_ids"], set(item["rule_ids"]), step["id"] + "/rule_ids")
                if step["kind"] == "APPLY_RULE" and not step["rule_ids"]:
                    fail("STEP_RULE_REQUIRED", step["id"], "应用规则步骤必须引用具体业务规则")
                available.update(step["output_ids"])
                produced.update(step["output_ids"])
            refs(item["output_ids"], produced, item["id"] + "/produced_outputs")
        exact_coverage([row["question_id"] for row in content["question_coverage"]], scope, "question_coverage")
        for row in content["question_coverage"]:
            refs(row["model_ids"], model_ids, "question_coverage/model_ids")
            gaps = {key for key, item in issues.items() if item["kind"] == "MODEL_GAP" and item["status"] == "OPEN" and row["question_id"] in item["affects"]}
            refs(row["gap_ids"], gaps, "question_coverage/gap_ids")
            linked = {key for key, item in mechanisms.items() if row["question_id"] in item["question_ids"]}
            if linked and not linked.intersection(row["model_ids"]) and not row["gap_ids"]:
                fail("MECHANISM_COVERAGE_MISSING", row["question_id"], "能力问题没有关联对应判断机理")
        expected_cases = {key for key, item in cases.items() if scope.intersection(item["question_ids"])}
        exact_coverage([row["case_id"] for row in content["case_explanations"]], expected_cases, "case_explanations")
        for item in content["case_explanations"]:
            refs(item["model_ids"], model_ids, "case_explanations/model_ids")
            case = cases.get(item["case_id"])
            if case and (item["expected"] != case["expected"] or item["forbidden"] != case["forbidden"]):
                fail("CASE_EXPECTATION_CHANGED", item["case_id"], "模型不能改写知识基线的预期或禁止结果")
    for issue in issues.values():
        refs(issue["affects"], allowed, issue["id"] + "/affects")
    for item in payload["trace"]:
        refs([item["from_id"], item["to_id"]], allowed, "trace")
