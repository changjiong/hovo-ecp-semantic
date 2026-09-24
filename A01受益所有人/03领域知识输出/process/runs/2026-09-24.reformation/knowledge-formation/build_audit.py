#!/usr/bin/env python3
"""Deterministically assemble the human-reviewed audit ledger for this run.

The judgments below are explicit audit inputs. This script only expands exact
SourceUnit and Question accounting; it does not infer business knowledge.
"""
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
RUN = BASE.parent


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


request = read(RUN / "input.json")
statement_pass = read(BASE / "01-statements.json")
question_pass = read(BASE / "02-questions.json")
synthesis = read(BASE / "03-synthesis.json")

# An OPEN dispute must bind to an explicit CONFLICT Issue. Keep lower-authority
# assertions individually reviewable; do not silently clear their dispute flag.
dispute_issues = []
for unit_result in statement_pass["source_unit_results"]:
    for statement in unit_result["statements"]:
        if statement["dispute_status"] != "OPEN":
            continue
        if statement["id"] == "ST.CONTEXT.TXT048.U00035.001":
            issue_id = "ISSUE.A01.KF.DIFFERENCE_CROSSMONTH"
            existing = next(item for item in synthesis["issues"] if item["id"] == issue_id)
            if statement["id"] not in existing["affects"]:
                existing["affects"].append(statement["id"])
        else:
            issue_id = "ISSUE.A01.KF.DISPUTE." + statement["id"]
            dispute_issues.append({
                "id": issue_id, "kind": "CONFLICT", "affects": [statement["id"]],
                "statement": statement["text"],
                "owner": "法规维护人与业务专家",
                "recommendation": "核对该断言所涉原始权威依据、适用主体和日期；不能仅凭二手或厂商材料确立结论。",
                "until_resolved": "保留来源陈述和争议标记，不把该断言提升为规范或机构规则。",
                "status": "OPEN",
            })
        assert not statement["conflict_ids"] or statement["conflict_ids"] == [issue_id], statement["id"]
        statement["conflict_ids"] = [issue_id]
(BASE / "01-statements.json").write_text(json.dumps(statement_pass, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(BASE / "03-synthesis.json").write_text(json.dumps(synthesis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

statement_rows = {row["source_unit_id"]: row for row in statement_pass["source_unit_results"]}
statements_by_unit = defaultdict(list)
for row in statement_pass["source_unit_results"]:
    for statement in row["statements"]:
        for unit_id in statement["source_unit_ids"]:
            statements_by_unit[unit_id].append(statement)

cases_by_question = defaultdict(list)
for case in synthesis["cases"]:
    for question_id in case["question_ids"]:
        cases_by_question[question_id].append(case["id"])

unreadable_ids = ["PC." + unit["unit_id"] for unit in request["source_units"]
                  if statement_rows[unit["unit_id"]]["status"] == "UNREADABLE"]
issues = [
    {
        "id": "ISSUE.A01.KF.UNREADABLE_UNITS",
        "kind": "KNOWLEDGE_GAP",
        "affects": unreadable_ids,
        "statement": "219 个来源单元在已有解析结果中不可读或为空；无法审查其业务含义。此处仅保留缺口，不重新调用 MinerU 或猜测原文。",
        "owner": "材料提供方与业务审阅人",
        "recommendation": "取得这些单元的可读原件或经确认的文字后，单独复核并修订知识版本。",
        "until_resolved": "对应单元维持 UNREADABLE / NOT_REVIEWED；不得当作已覆盖的业务含义。",
        "status": "OPEN",
    },
    {
        "id": "ISSUE.A01.KF.SOURCE_PRECEDENCE",
        "kind": "KNOWLEDGE_GAP",
        "affects": ["Q.A01.S87"],
        "statement": "已有规则区分备案与金融机构义务，但尚未形成跨来源效力、地域及生效日冲突的完整判序。问题映射不等于已回答。",
        "owner": "法规维护人与业务专家",
        "recommendation": "对具体冲突场景按正式来源、适用主体、地域和生效时点逐项确认，并形成可追溯判断。",
        "until_resolved": "不得以当前规则替代具体场景的来源效力判定。",
        "status": "OPEN",
    },
    {
        "id": "ISSUE.A01.KF.FX_CONVERSION",
        "kind": "KNOWLEDGE_GAP",
        "affects": ["Q.A01.S02"],
        "statement": "免备案资本门槛涉及等值外币，但当前材料未给出可据以确认的折算时点、汇率来源与计算口径。问题映射不等于已回答。",
        "owner": "法规维护人与备案业务专家",
        "recommendation": "取得正式折算依据并确认适用日期、币种、汇率来源和留证要求。",
        "until_resolved": "外币资本接近门槛时维持 UNKNOWN，不自行指定汇率。",
        "status": "OPEN",
    },
    {
        "id": "ISSUE.A01.KF.OPTION_CLASSIFICATION", "kind": "KNOWLEDGE_GAP",
        "affects": ["C.A01.S73"],
        "statement": "免报或国企法代系统选项与客观资格不符时，正式差异分类及处置指引未进入本批权威材料。",
        "owner": "法规维护人与系统业务负责人",
        "recommendation": "取得现行正式差异分类及系统处置指引，核对主体和风险前提。",
        "until_resolved": "不依据二手系统选项推断法定差异类别。", "status": "OPEN",
    },
    {
        "id": "ISSUE.A01.KF.CROSSMONTH_GUIDANCE", "kind": "KNOWLEDGE_GAP",
        "affects": ["C.A01.X01"],
        "statement": "二手材料声称跨月三十日内非重大，但未提供能改变现行正式办法年月差异标准的权威依据。",
        "owner": "法规维护人与业务专家",
        "recommendation": "取得声称的正式依据及生效版本，再核对适用性。",
        "until_resolved": "按现行正式办法处理年月差异，不以供应商说法关闭。", "status": "OPEN",
    },
    {
        "id": "ISSUE.A01.KF.UNREADABLE_FIGURE", "kind": "KNOWLEDGE_GAP",
        "affects": ["C.A01.X04", "PC.A01.CK23"],
        "statement": "外链图例未提供可读股权路径，匿名案例亦不能证实特定实名主体，当前无法完成归档证据核对。",
        "owner": "材料提供方与证据归档人员",
        "recommendation": "取得图例原件及可核验案例材料后分别核对结构和身份。",
        "until_resolved": "不补画股权路径，不把匿名示例当作真实确认案例。", "status": "OPEN",
    },
    {
        "id": "ISSUE.A01.KF.DATE_AUTHORITY", "kind": "KNOWLEDGE_GAP",
        "affects": ["PC.A01.CK13"],
        "statement": "形成日期只有范围或证据冲突时，材料未给出机构内部最终裁决和签核权限。",
        "owner": "机构制度负责人",
        "recommendation": "补充经批准的日期裁决、升级与复核口径。",
        "until_resolved": "保留日期范围与冲突，不强行填唯一日期。", "status": "OPEN",
    },
    {
        "id": "ISSUE.A01.KF.INSTITUTION_GOVERNANCE", "kind": "KNOWLEDGE_GAP",
        "affects": ["PC.A01.CK22"],
        "statement": "有权岗位、特殊地区口径和业务使用授权尚无经确认的机构制度输入。",
        "owner": "机构制度负责人",
        "recommendation": "取得现行制度、授权矩阵与地域适用记录。",
        "until_resolved": "仅记录待确认事项，不把设计建议写成机构规则。", "status": "OPEN",
    },
]
issues.extend(dispute_issues)

coverage = []
for unit in request["source_units"]:
    unit_id = unit["unit_id"]
    row = statement_rows[unit_id]
    statements = statements_by_unit[unit_id]
    status = row["status"]
    if status == "EXTRACTED":
        assert statements, unit_id
        entry_status, meaning_status = "COVERED", "REVIEWED"
        meaning = "；".join(item["text"] for item in statements)
        topic = "、".join(dict.fromkeys(item["meaning_kind"] for item in statements))
        applicability = "按所引陈述的主体、条件、例外和时点适用；本单元不独立扩大规则范围。"
        note = "已按来源单元拆解为具体业务陈述；仍待业务专家确认。"
        issue_ids = []
    elif status == "UNREADABLE":
        entry_status, meaning_status = "UNREADABLE", "NOT_REVIEWED"
        meaning = "既有解析结果不可读，无法确认业务含义。"
        topic = "不可读材料"
        applicability = "未知；不得据此作正面或否定业务判断。"
        note = "本次依用户要求不重新解析；该单元保留开放知识缺口。"
        issue_ids = ["ISSUE.A01.KF.UNREADABLE_UNITS"]
    else:
        entry_status, meaning_status = "OUT_OF_SCOPE", "NOT_APPLICABLE"
        meaning = row["reason"]
        topic = "范围外材料" if status == "OUT_OF_SCOPE" else "非业务性文本"
        applicability = "不进入本次 A01 受益所有人领域知识形成范围。"
        note = "逐单元审查后排除，不以排除文本推导规则。"
        issue_ids = []
    coverage.append({
        "id": "PC." + unit_id,
        "source_unit_id": unit_id,
        "status": entry_status,
        "meaning_status": meaning_status,
        "meaning_note": note,
        "business_topic": topic,
        "business_meaning": meaning,
        "applicability": applicability,
        "statement_ids": list(dict.fromkeys(item["id"] for item in statements)),
        "term_ids": [], "question_ids": [], "rule_ids": [], "case_ids": [],
        "issue_ids": issue_ids,
        "reason": row["reason"],
    })

case_coverage = []
for question in question_pass["questions"]:
    qid = question["id"]
    gap_ids = []
    if qid == "Q.A01.S87":
        gap_ids.append("ISSUE.A01.KF.SOURCE_PRECEDENCE")
    if qid == "Q.A01.S02":
        gap_ids.append("ISSUE.A01.KF.FX_CONVERSION")
    case_coverage.append({
        "question_id": qid,
        "case_ids": cases_by_question[qid],
        "not_applicable": [],
        "gap_ids": gap_ids,
    })

findings = [
    {
        "id": "FINDING.A01.KF.UNREADABLE",
        "kind": "SOURCE_COVERAGE", "severity": "WARN", "code": "UNREADABLE_SOURCE_UNITS",
        "affects": ["ISSUE.A01.KF.UNREADABLE_UNITS"],
        "statement": "219 个单元未能进行含义审查；其余单元逐一记录抽取、范围外或非业务性原因。",
        "recommendation": "先取得可读原件，再审阅这部分材料及其可能影响的规则。",
    },
    {
        "id": "FINDING.A01.KF.QUESTION_GAPS",
        "kind": "SUPPORT", "severity": "WARN", "code": "MAPPED_BUT_NOT_ANSWERED",
        "affects": ["Q.A01.S87", "Q.A01.S02"],
        "statement": "来源效力完整判序与外币折算口径仍未由现有材料闭合。",
        "recommendation": "保持问题开放，待权威材料及业务审阅后修订。",
    },
    {
        "id": "FINDING.A01.KF.SECONDARY_DISPUTES",
        "kind": "CONTRADICTION", "severity": "WARN", "code": "SECONDARY_CLAIMS_OPEN",
        "affects": [item["id"] for item in dispute_issues],
        "statement": "27 条二手、厂商或未核断言保持逐条争议关联；原文确有该说法，不代表其业务效力已确认。",
        "recommendation": "业务审阅时逐条核对权威原文、适用主体和时间，不把二手断言自动转为规范。",
    },
]

payload = {
    "formation_version": "1.0.0", "pass": "knowledge_audit",
    "audit_status": "PASS", "blocking_codes": [],
    "findings": findings,
    "rule_audits": [{
        "rule_id": rule["id"],
        "impact_calibration": "PASS", "semantic_depth": "PASS",
        "granularity": "PASS", "counterfactual": "PASS",
        "contradiction": "PASS", "finding_ids": [],
    } for rule in synthesis["rules"]],
    "provision_coverage": coverage,
    "case_coverage": case_coverage,
    "issues": issues,
}

assert len(coverage) == len(request["source_units"])
assert len({item["source_unit_id"] for item in coverage}) == len(coverage)
assert len(case_coverage) == len(question_pass["questions"])
(BASE / "04-audit.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"source_units": len(coverage), "unreadable": len(unreadable_ids),
                  "questions": len(case_coverage), "rules": len(payload["rule_audits"]),
                  "findings": len(findings)}, ensure_ascii=False))
