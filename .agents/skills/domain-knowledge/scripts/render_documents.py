#!/usr/bin/env python3
"""Render the business document and audit ledger from a contract 4.0.0 output.

This is a deterministic presentation step, not knowledge extraction or review.
It updates the two document references and resets structural verification.
"""
import argparse
from collections import Counter
import hashlib
import html
import copy
import json
import os
from pathlib import Path
from urllib.parse import quote


def safe(path, root):
    if "trash" in str(path).lower():
        raise ValueError("Forbidden path component")
    result = path.resolve()
    if "trash" in str(result).lower() or not result.is_relative_to(root):
        raise ValueError("Path must stay within the project root")
    return result


def digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def anchor(identifier, label):
    return f'<a id="{html.escape(identifier, quote=True)}"></a>\n{label}\n'


def link(label, identifier, document=""):
    return f"[{label}]({quote(document, safe='/.-_')}#{quote(identifier, safe='.-_')})"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.project_root.resolve()
    output_path = safe(args.output, root)
    payload = json.loads(output_path.read_text())
    if payload["contract_version"] != "4.0.0" or payload["mode"] not in {"PRODUCE", "REVISE"} or payload["stage"] != "domain-knowledge":
        raise ValueError("Rendering requires a PRODUCE/REVISE contract 4.0.0 knowledge output")
    if payload["confirmation"]["status"] in {"CONFIRMED", "REJECTED"}:
        raise ValueError("Signed documents must not be regenerated; revise into a new draft version and path")
    references = payload["input_refs"]
    if len(references) != 1:
        raise ValueError("Exactly one source inventory input is required")
    source_path = safe(root / references[0]["path"], root)
    if digest(source_path) != references[0]["digest"]:
        raise ValueError("Input digest mismatch")
    request = json.loads(source_path.read_text())
    # Escape business prose before assembling our own links and anchors. Keep
    # the original JSON bytes/meaning intact when updating document references.
    prose_fields = {"scope", "business_goal", "question", "topic", "consumer", "decision_use", "unknown_policy", "explanation", "name", "definition", "aliases", "distinctions", "example", "counterexample", "text", "basis", "input_facts", "expected", "forbidden", "reasoning", "preconditions", "conditions", "result", "exceptions", "missing_evidence", "effective_period", "authority", "statement", "owner", "recommendation", "until_resolved", "locator", "issuer", "date", "label", "business_topic", "business_meaning", "applicability", "meaning_note", "reason", "actor", "stage", "concern", "method", "limitations"}
    def display(value, field=""):
        if isinstance(value, dict):
            return {k: display(v, k) for k, v in value.items()}
        if isinstance(value, list):
            return [display(v, field) for v in value]
        if isinstance(value, str) and field in prose_fields:
            return html.escape(value, quote=False).replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")
        return value
    content = display(copy.deepcopy(payload["content"]))
    issues = display(copy.deepcopy(payload["issues"]))
    request = display(request)
    statements = {s["id"]: s for s in content["statements"]}
    questions = {q["id"]: q for q in content["questions"]}
    sources = {s["source_id"]: s for s in content["sources"]}
    units = {u["unit_id"]: u for u in request["source_units"]}
    scope = set(content["question_discovery"]["scope_question_ids"])
    partial_scope = scope != set(questions)
    pc_ids = {row["source_unit_id"]: row["id"] for row in content["provision_coverage"]}
    names = {key: display(Path(s["artifact"]["path"]).name, "name") for key, s in sources.items()}
    version = payload["content_version"]
    review_path = safe(output_path.parent / "review.md", root)
    coverage_path = safe(output_path.parent / "coverage.md", root)
    for filename, expected in [("review.md", review_path), ("coverage.md", coverage_path)]:
        refs = [ref for ref in payload["files"] if Path(ref["path"]).name == filename]
        if len(refs) > 1 or any(safe(root / ref["path"], root) != expected for ref in refs):
            raise ValueError("Ambiguous document reference: " + filename)

    def source_links(ids, document=""):
        return "；".join(link(names[s], s, document) for s in dict.fromkeys(ids)) or "用户口径或合成讨论材料，非制度原文"

    def statement_sources(ids):
        return source_links([s for ident in ids for s in statements[ident]["source_ids"]])

    def case_text(case, audit=False, number=None):
        head = "#### " + (f"案例 {number:02d}｜" if number else "") + case["input_facts"][0] + (f"（{case['id']}）" if number else "")
        result = [anchor(case["id"], head), "用于回答：" + "；".join(link(questions[q]["question"], q, "review.md" if audit else "") for q in case["question_ids"])]
        result.append("案例性质：" + ("合成教学案例，不代表客户事实。" if case["synthetic"] else "来源材料案例。"))
        result.extend("- " + fact for fact in case["input_facts"])
        result.extend(["", "判断过程：" + case.get("reasoning", "尚未补充，应保留为案例解释缺口。"),
                       "预期结果：" + case["expected"], "不得得出：" + case["forbidden"],
                       "依据：" + source_links(case["source_ids"], "review.md" if audit else ""), ""])
        return "\n\n".join(result)

    topic_questions = {}
    for q in questions.values():
        if q["id"] in scope and not q.get("parent_question_id"):
            topic_questions.setdefault(q["topic"], []).append(q)

    review = ["# 领域业务知识说明书",
              f"内容版本：{version}。正式确认记录独立保存，以绑定本版本内容的记录为准。" + (" 本次内容变更后需重新审阅。" if payload["confirmation"]["status"] == "STALE" else ""),
              anchor("section-scope", "## 先读这里：领域认知速览"),
              "### 这个领域要解决什么", content["scope"],
              request.get("business_goal", ""),
              "### 这个业务世界里的核心概念",
              "先记住这些业务词即可，详细定义、边界、实例和反例见后文“关键概念与边界”。",
              "、".join(term["name"] for term in content["terms"]) or "本轮尚未形成可交付的核心概念。",
              "### 业务主线与主要问题",
              "下面按业务主题组织主问题，先帮助读者理解事情怎样展开；问题编号和知识工程来源不影响业务阅读。"]
    if topic_questions:
        review += ["| 业务主题 | 主要问题 |", "| --- | --- |"]
        for topic, topic_items in topic_questions.items():
            review.append("| " + str(topic).replace("|", "\\|").replace("\n", " ") + " | " + "；".join(link(q["question"], q["id"]) for q in topic_items) + " |")
    review += ["",
               "### 推荐阅读路径",
               "先读本节建立业务全貌，再读“关键概念与边界”→“业务问题与判断依据”→“具体案例与变化后的结果”→“未决事项与访谈”。下面的来源覆盖、问题发现过程和编号索引用于追溯，业务审阅时可以跳过。",
               ("本轮先按部分业务问题形成深度样章，其他问题保留概要并显式标明待重审。" if partial_scope else "本轮按当前范围形成完整业务问题集。") + "作者整理、材料映射和实际业务确认分别记录。",
               anchor("section-provisions", "## 追溯区：材料处理与语义审查概览"),
               "以下属于知识工程追溯信息，不是理解业务的前置内容。逐条台账、原文摘录、全部案例以及候选问题归并理由见 [审计附件](coverage.md)。",
               "| 来源 | 抽取状态 | 输入单元 | 材料有映射 | 材料部分映射 | 无法读取 | 范围外 | 含义已审 | 含义部分审查 | 含义待审 |",
               "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    trace_start = next(i for i, value in enumerate(review) if 'section-provisions' in value)
    for sid in sources:
        rows = [r for r in content["provision_coverage"] if units[r["source_unit_id"]]["source_id"] == sid]
        material = Counter(r["status"] for r in rows)
        meaning = Counter(r["meaning_status"] for r in rows)
        extraction = next(x for x in request["source_extractions"] if x["source_id"] == sid)
        extraction_label = {"COMPLETE": "已完成登记", "PARTIAL": "部分完成", "FAILED": "失败"}[extraction["status"]]
        review.append(f"| {link(names[sid], sid)} | {extraction_label} | {len(rows)} | {material['COVERED']} | {material['PARTIAL']} | {material['UNREADABLE']} | {material['OUT_OF_SCOPE']} | {meaning['REVIEWED']} | {meaning['PARTIAL']} | {meaning['NOT_REVIEWED']} |")
    review.extend(["", "含义已审表示作者回读并拆解过该单元，仍须审阅其正确性；范围外也须保留排除理由。表中数量和脚本通过不能证明业务知识完整。",
                   anchor("section-question-cleaning", "## 追溯区：业务问题发现与归并"),
                   "这里先展示从制度含义和业务流程中发现的候选问题，再进入下方逐题判断。候选问题不会静默丢弃：保留项进入正文问题，归并项显示其目标问题，待决项保留原问法并关联未决事项。",
                   f"本轮共发现 {len(content['question_discovery']['candidates'])} 个候选问题；" + "；".join(f"{label} {count} 个" for label, count in [("保留", Counter(item['disposition'] for item in content['question_discovery']['candidates'])['RETAINED']), ("归并", Counter(item['disposition'] for item in content['question_discovery']['candidates'])['MERGED']), ("待决", Counter(item['disposition'] for item in content['question_discovery']['candidates'])['OPEN'])]) + f"。正文现有 {len(questions)} 个最终问题。待决项不进入‘业务问题与判断依据’的规则回答，但仍是本版本必须处理的业务问题。",
                   "| 候选问题 | 来源 | 清洗结果 | 进入正文的目标问题 | 处理理由 | 未决事项 |",
                   "| --- | --- | --- | --- | --- | --- |"])
    disposition_labels = {"RETAINED": "保留", "MERGED": "归并", "OPEN": "待决", "OUT_OF_SCOPE": "范围外"}
    origin_labels = {"SOURCE": "制度/材料含义", "PROCESS": "业务流程补查"}
    def table_cell(value):
        return str(value).replace("|", "\\|").replace("\n", " ")
    for candidate in content["question_discovery"]["candidates"]:
        targets = "；".join(link(questions[q]["question"], q) for q in candidate["target_question_ids"] if q in questions)
        if not targets:
            targets = "未进入正文判断（待决）"
        issue_links = "；".join(link(issue_id, issue_id) for issue_id in candidate["issue_ids"]) or "无"
        review.append("| " + " | ".join(table_cell(value) for value in [
            candidate["question"],
            origin_labels.get(candidate["origin"], candidate["origin"]),
            disposition_labels.get(candidate["disposition"], candidate["disposition"]),
            targets,
            candidate["reason"],
            issue_links,
        ]) + " |")
    q_no = {q["id"]: i + 1 for i, q in enumerate(questions.values())}
    rule_order = []
    for _q in questions.values():
        for _r in content["rules"]:
            if _q["id"] in _r["question_ids"] and _r["id"] not in rule_order:
                rule_order.append(_r["id"])
    for _r in content["rules"]:
        if _r["id"] not in rule_order:
            rule_order.append(_r["id"])
    r_no = {rid: i + 1 for i, rid in enumerate(rule_order)}
    scoped_cases = [c for c in content["cases"] if set(c["question_ids"]) & scope]
    c_no = {c["id"]: i + 1 for i, c in enumerate(scoped_cases)}
    rule_of = {}
    for _r in content["rules"]:
        for _q in _r["question_ids"]:
            rule_of.setdefault(_q, []).append(_r["id"])
    review.extend([anchor("section-index", "## 追溯区：问题与规则定位索引"),
                   "同一问题或规则在正文与审计附件中使用稳定编号（问题01–%02d、规则01–%02d、案例01–%02d）；括号内为结构化标识，可跨版本引用。" % (len(q_no), len(r_no), len(c_no)),
                   "| 问题编号 | 业务问题 | 主题 | 对应规则编号 |",
                   "| --- | --- | --- | --- |"])
    for qid_, qobj in questions.items():
        rids = "、".join(f"{r_no[r]:02d}" for r in rule_of.get(qid_, []) if r in r_no)
        review.append(f"| 问题 {q_no[qid_]:02d} | [" + qobj["question"] + f"](#{qid_}) | " + qobj["topic"] + f" | {rids or '—'} |")
    review.extend(["", "| 规则编号 | 规则名称 | 对应问题编号 | 结构化标识 |", "| --- | --- | --- | --- |"])
    for rid_ in rule_order:
        _rule = next(r for r in content["rules"] if r["id"] == rid_)
        qids_ = "、".join(f"{q_no[q]:02d}" for q in _rule["question_ids"] if q in q_no)
        review.append(f"| 规则 {r_no[rid_]:02d} | {_rule.get('name') or '—'} | {qids_ or '—'} | `{rid_}` |")
    trace_sections = review[trace_start:]
    del review[trace_start:]
    review.extend([anchor("section-concepts", "## 关键概念与边界")])
    for term in content["terms"]:
        review.extend([anchor(term["id"], "### " + term["name"]), term["definition"],
                       "容易混淆的边界：" + term["distinctions"]])
        if term["aliases"]:
            review.append("同义称呼：" + "、".join(term["aliases"]))
        for key, label in [("example", "实例"), ("counterexample", "反例")]:
            if term.get(key):
                review.append(label + "：" + term[key])
        if not term.get("example") or not term.get("counterexample"):
            review.append("审阅限制：该概念尚未补齐本轮要求的具体实例与反例。")
        review.append("依据：" + statement_sources(term["statement_ids"]))
    review.append(anchor("section-judgements", "## 业务问题与判断依据"))
    rule_seen = set()
    for question in questions.values():
        qid = question["id"]
        review.extend([anchor(qid, "### " + f"问题 {q_no[qid]:02d}｜{question['question']}（{qid}）"), "主题：" + question["topic"],
                       "本轮含义整理范围；具体确认状态见文末。" if qid in scope else "既有问题概要；尚未按新方法重审，不视为完整规则说明。",
                       "使用者：" + question["consumer"] + "。结果用于：" + question["decision_use"]])
        if question.get("parent_question_id"):
            parent = questions[question["parent_question_id"]]
            review.append("所属业务问题：" + link(parent["question"], parent["id"]))
        if question.get("explanation"):
            review.append(question["explanation"])
        for rule in content["rules"]:
            if qid not in rule["question_ids"]:
                continue
            if rule["id"] in rule_seen:
                review.append(link("同一规则的完整判断说明", rule["id"]))
                continue
            rule_seen.add(rule["id"])
            _rname = rule.get("name")
            _rhead = f"规则 {r_no[rule['id']]:02d}｜{_rname}（{rule['id']}）" if _rname else f"规则 {r_no[rule['id']]:02d}｜判断依据与步骤（{rule['id']}）"
            review.append(anchor(rule["id"], "#### " + _rhead))
            _qlinks = "；".join(f"问题 {q_no[_q]:02d} " + link(questions[_q]["question"], _q) for _q in rule["question_ids"] if _q in questions)
            if _qlinks:
                review.append("对应问题：" + _qlinks)
            for key, label in [("scope", "适用范围"), ("preconditions", "先核实什么"), ("conditions", "如何判断"),
                               ("result", "可以得出什么"), ("exceptions", "例外与边界"), ("missing_evidence", "缺证时怎么办"),
                               ("effective_period", "适用时间"), ("authority", "依据及口径来源")]:
                review.append(label + "：" + rule[key])
            review.append("规则依据索引：" + statement_sources(rule["statement_ids"]))
        review.append("尚不清楚时：" + question["unknown_policy"])
    # Rules not currently attached to a question are still visible for review.
    for rule in content["rules"]:
        if rule["id"] not in rule_seen:
            review.extend([anchor(rule["id"], f"### 尚未归入问题的规则 规则 {r_no[rule['id']]:02d}（{rule['id']}）"), rule["conditions"], rule["result"]])
    review.append(anchor("section-cases", "## 具体案例与变化后的结果"))
    review.append("以下选取本轮问题发现范围内的案例。案例缺口见未决事项；全部案例记录见 [审计附件](coverage.md#section-cases)。")
    review.extend(case_text(case, number=c_no.get(case["id"])) for case in scoped_cases)
    review.append(anchor("section-interviews", "## 未决事项与访谈"))
    for issue in issues:
        review.extend([anchor(issue["id"], "### " + issue["statement"]), "当前状态：" + {"OPEN": "待处理", "RESOLVED": "已解决", "ACCEPTED": "已接受"}.get(issue["status"], issue["status"]),
                       "适合答复或处理的角色：" + issue["owner"], "具体处理建议：" + issue["recommendation"],
                       "未解决前：" + issue["until_resolved"], "业务定位：" + issue.get("locator", "见相关判断说明")])
    review.append(anchor("section-sources", "## 来源与依据索引"))
    for sid, source in sources.items():
        raw_path = safe(root / source["artifact"]["path"], root)
        relative = quote(os.path.relpath(raw_path, review_path.parent), safe="/.")
        review.extend([anchor(sid, "### " + names[sid]),
                       f"提供方：{source['issuer']}。日期/版本：{source['date']}。",
                       f"[原始材料]({relative})；定位：{source['locator']}。",
                       "使用边界：" + {"NORMATIVE_RULE": "实体制度依据，仍须判断具体适用范围。", "PROCEDURAL_GUIDANCE": "办理指引，不得改变上位制度。", "SYSTEM_INTERFACE": "系统接口、报文与操作规则，不作为新增实体认定标准。"}.get(source["source_role"], "解释或背景材料，不能替代制度依据。")])
    review.extend([anchor("section-confirmation", "## 待确认范围与审阅记录"),
                   "业务审阅登记：" + {"NOT_EXECUTED": "尚未开展", "PASS": "已登记通过", "FAIL": "需修订", "BLOCKED": "有待解决依赖"}.get(payload["states"]["business_reviewed"]["status"], "见结构化记录") + "。" + html.escape(payload["states"]["business_reviewed"]["reason"]) + " 作者或智能体审阅不能替代实际业务读者复述或责任人批准。",
                   "会话中有实际答复的事项依其证据单独登记；只询问未决含义和新版本审阅反馈，不要求业务人员逐条确认条款编号。",
                   "本版本待确认问题：" + "；".join(link(questions[q]["question"], q) for q in payload["confirmation"]["scope_ids"] if q in questions)])

    review.extend(["", "## 附：知识工程追溯", "以下内容用于来源、问题发现和编号追溯，不作为理解业务的前置阅读。"])
    review.extend(trace_sections)

    audit = ["# 领域知识审计附件", f"内容版本：{version}。对应 [业务说明书](review.md) 与同目录 output.json。",
             "本附件保存全量追溯，不作为业务读者逐项签署清单。材料映射与含义审查独立；原文摘录不视为已完成含义拆解。",
             "## 来源抽取记录"]
    for extraction in request["source_extractions"]:
        audit.extend(["### " + names[extraction["source_id"]], "抽取状态：" + extraction["status"],
                      "方法：" + extraction["method"], "限制：" + extraction["limitations"],
                      "完整单元集合：" + "、".join(link(u, pc_ids[u]) for u in extraction["unit_ids"])])
    audit.append(anchor("section-provisions", "## 逐条材料覆盖与含义审查"))
    for row in content["provision_coverage"]:
        unit = units[row["source_unit_id"]]
        audit.extend([anchor(row["id"], "### " + unit.get("label", row["source_unit_id"])),
                      f"来源：{source_links([unit['source_id']], 'review.md')}；定位：{unit['locator']}。",
                      f"材料映射：{row['status']}；业务含义审查：{row['meaning_status']}。",
                      "主题：" + row["business_topic"], "已记录含义：" + row["business_meaning"],
                      "适用范围：" + row["applicability"], "审查说明：" + row["meaning_note"], "映射理由：" + row["reason"]])
        for key, label, doc in [("statement_ids", "陈述", ""), ("term_ids", "概念", "review.md"), ("question_ids", "问题", "review.md"), ("rule_ids", "规则", "review.md"), ("case_ids", "案例", ""), ("issue_ids", "缺口", "review.md")]:
            if row[key]:
                audit.append(label + "：" + "、".join(link(ident, ident, doc) for ident in row[key]))
    audit.append(anchor("section-statements", "## 原文摘录与拆解后的业务陈述"))
    for item in statements.values():
        audit.extend([anchor(item["id"], "### " + item["meaning_kind"]), item["text"],
                      "出处性质：" + item["origin"] + "；确认状态：" + item["review_status"],
                      "定位与依据：" + item["basis"], "来源：" + source_links(item["source_ids"], "review.md"),
                      "单元：" + "、".join(link(u, pc_ids[u]) for u in item["source_unit_ids"])])
    audit.append(anchor("section-cases", "## 全部案例"))
    audit.extend(case_text(case, True) for case in content["cases"])
    audit.append(anchor("section-discovery", "## 候选问题去向与流程补查"))
    for item in content["question_discovery"]["candidates"]:
        audit.extend([anchor(item["id"], "### " + item["question"]), "来源路径：" + item["origin"] + "；处理：" + item["disposition"],
                      "理由：" + item["reason"], "去向：" + "；".join(link(questions[q]["question"], q, "review.md") for q in item["target_question_ids"]),
                      "依据单元：" + "、".join(link(u, pc_ids[u]) for u in item["source_unit_ids"]),
                      "未决事项：" + "、".join(link(i, i, "review.md") for i in item["issue_ids"])])
    for item in content["question_discovery"]["process_checks"]:
        audit.extend([anchor(item["id"], "### " + item["actor"] + " / " + item["stage"]), item["concern"],
                      "检查状态：" + item["status"] + "；理由：" + item["reason"],
                      "问题：" + "；".join(link(questions[q]["question"], q, "review.md") for q in item["question_ids"]),
                      "依据单元：" + "、".join(link(u, pc_ids[u]) for u in item["source_unit_ids"]),
                      "未决事项：" + "、".join(link(i, i, "review.md") for i in item["issue_ids"])])
    review_path.write_text("\n\n".join(review) + "\n", encoding="utf-8")
    # Keep table rows contiguous in Markdown.
    review_path.write_text(review_path.read_text().replace("|\n\n|", "|\n|"), encoding="utf-8")
    coverage_path.write_text("\n\n".join(audit) + "\n", encoding="utf-8")
    payload["files"] = [r for r in payload["files"] if safe(root / r["path"], root) not in {review_path, coverage_path}]
    for name, path in [("Review", review_path), ("Coverage", coverage_path)]:
        payload["files"].append({"artifact_id": payload["artifact_id"] + "." + name, "content_version": version,
                                 "contract_version": "text/markdown", "path": str(path.relative_to(root)), "digest": digest(path)})
    rendered_digests = {
        str(path.relative_to(root)): digest(path)
        for path in (review_path, coverage_path)
    }
    for evidence in payload.get("evidence", []):
        for reference in evidence.get("subject_refs", []):
            if reference.get("path") in rendered_digests:
                reference["digest"] = rendered_digests[reference["path"]]
                reference["content_version"] = version
    payload["states"]["structure_checked"] = {"status": "NOT_EXECUTED", "evidence_ids": [], "reason": "文档重新生成；等待本版本独立合同检查。"}
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"review": str(review_path), "coverage": str(coverage_path), "content_version": version, "verification": "NOT_EXECUTED"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
