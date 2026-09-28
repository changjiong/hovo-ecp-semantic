#!/usr/bin/env python3
"""Build the A01 practical UBO identification model from a fixed knowledge artifact."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[5]
KNOWLEDGE_PATH = ROOT / "A01受益所有人/03领域知识输出/output.json"
MODEL_DIR = ROOT / "A01受益所有人/04领域模型输出"
RUN_DIR = MODEL_DIR / "process/runs/2026-09-24.practical-ubo"
KNOWLEDGE_SHA256 = "d09b3b448b3077d84c41fd167cf73030ae7b0b902c8767902ea98676131585e1"
QUESTION_IDS = [
    "Q.A01.S12", "Q.A01.S13", "Q.A01.S14", "Q.A01.S16", "Q.A01.S17",
    "Q.A01.S18", "Q.A01.S20", "Q.A01.S21", "Q.A01.S22", "Q.A01.S23",
    "Q.A01.S24", "Q.A01.S25", "Q.A01.S26", "Q.A01.S27", "Q.A01.S28",
    "Q.A01.S29", "Q.A01.S30", "Q.A01.S31", "Q.A01.S32", "Q.A01.S33",
    "Q.A01.S34", "Q.A01.S35", "Q.A01.S36", "Q.A01.S45", "Q.A01.S47",
    "Q.A01.S49", "Q.A01.S50", "Q.A01.S52", "Q.A01.S53", "Q.A01.S56",
    "Q.A01.S57", "Q.A01.S58", "Q.A01.S60", "Q.A01.S61", "Q.A01.S62",
]
TERM_IDS = [
    "TERM.A01.KF.02", "TERM.A01.KF.03", "TERM.A01.KF.04",
    "TERM.A01.KF.05", "TERM.A01.KF.06", "TERM.A01.KF.07",
    "TERM.A01.KF.09", "TERM.A01.KF.10", "TERM.A01.KF.13",
]
RULE_IDS = [
    "RULE.A01.KF.PROFILE", "RULE.A01.KF.EQUITY", "RULE.A01.KF.NOMINEE",
    "RULE.A01.KF.RETURNS_VOTES", "RULE.A01.KF.CONTROL",
    "RULE.A01.KF.FALLBACK", "RULE.A01.KF.SOE", "RULE.A01.KF.BRANCHES",
    "RULE.A01.KF.EXCEPTIONS", "RULE.A01.KF.IDENTITY", "RULE.A01.KF.RISK", "RULE.A01.KF.DATES",
]

SCOPE = (
    "金融机构对一般法人、非法人组织客户的自然人受益所有人识别实操模型："
    "客户识别路由、直接/间接权益、收益与表决权、实际控制、组织级备位前提、"
    "身份与权利证据及权利形成时点。"
    "不建模备案办理、信托、资产管理产品、BOMIS、差异分析/报告、"
    "历史交易归责及机构内部审批工作流。模型为知识草案的显式子集。"
)


def field(name, label, kind, description, minimum=0, maximum=1, target=None, values=None, labels=None):
    item = {
        "name": name,
        "label": label,
        "type": kind,
        "cardinality": {"min": minimum, "max": maximum},
        "description": description,
    }
    if target:
        item["target"] = target
    if values:
        item["values"] = values
    if labels:
        item["value_labels"] = labels
    return item


def ref(name, label, target, description, minimum=0, maximum=1):
    return field(name, label, "Ref", description, minimum, maximum, target=target)


def enum(name, label, values, description, minimum=0, maximum=1, labels=None):
    return field(name, label, "Enum", description, minimum, maximum, values=values, labels=labels)


def typ(identifier, name, kind, description, basis, identity, fields, sentence, why, identity_text, examples, counterexamples, bearer=None, origin="PROPOSED"):
    result = {
        "id": identifier,
        "name": name,
        "kind": kind,
        "description": description,
        "basis_ids": basis,
        "identity": identity,
        "fields": fields,
        "examples": examples,
        "counterexamples": counterexamples,
        "term_origin": origin,
        "business_sentence": sentence,
        "why_object": why,
        "identity_description": identity_text,
    }
    if bearer:
        result["bearer_field"] = bearer
    return result


def io(name, label, kind, binding, target=None, values=None, cardinality=None):
    item = {"name": name, "label": label, "type": kind, "binding": binding}
    if target:
        item["target"] = target
    if values:
        item["values"] = values
    if cardinality:
        item["cardinality"] = cardinality
    return item


def base_ids(*rule_ids):
    return list(dict.fromkeys([*TERM_IDS, *rule_ids]))


def build_types():
    return [
        typ(
            "M.Organization", "组织主体", "ENTITY",
            "受益所有人识别的目标客户或持有权益链中的中间组织。分支机构不与所属组织合并。",
            ["TERM.A01.KF.02", "TERM.A01.KF.07", "RULE.A01.KF.PROFILE", "RULE.A01.KF.SOE"],
            ["registration_identifier", "jurisdiction"],
            [
                field("registration_identifier", "登记识别号", "Text", "官方登记或设立文件中的稳定主体识别号。缺失时不能虚构组织身份。", 1),
                field("jurisdiction", "登记/设立法域", "Text", "该组织登记或依法设立的法域，用于解释组织身份及证据适用范围。", 1),
                field("official_name", "法定名称", "Text", "与判断时点相符的登记或设立文件名称。", 1),
                enum("organization_form", "组织形式", ["COMPANY", "PARTNERSHIP", "OTHER_LEGAL", "NON_LEGAL", "DOMESTIC_BRANCH", "FOREIGN_BRANCH", "STATE_OWNED_ENTITY", "UNKNOWN"], "按适用文件确认的组织形式；UNKNOWN不得映射为一般公司。", 1),
                enum("state_ownership_status", "国资状态", ["WHOLLY_OWNED", "CONTROLLED", "PARTICIPATING_ONLY", "NOT_STATE_OWNED", "UNKNOWN"], "国资状态必须由出资、治理和实际支配证据确定，名称或国资股东标签不足。"),
                ref("supporting_evidence", "组织身份依据", "M.Evidence", "登记、设立、产权、章程或治理依据。", 1, None),
            ],
            "金融机构把组织主体作为客户，或把它作为权益链中的中间节点来识别最终自然人。",
            "目标客户、中间持股主体和分支所属组织承担不同上下文；组织形式和时点会改变适用识别路由。",
            "以登记识别号与登记/设立法域区分同名组织；更名或恢复登记须有连续身份和有效期间证据。",
            ["有登记号和法域、且在判断日存续的公司客户。"],
            ["国资交易系统标注的‘实际控制企业’不是自然人受益所有人。"],
            origin="KNOWLEDGE",
        ),
        typ(
            "M.NaturalPerson", "自然人", "ENTITY",
            "最终受益所有人必须落到的现实自然人；身份同一性与其权利是否达标分别判断。",
            ["TERM.A01.KF.02", "TERM.A01.KF.04", "RULE.A01.KF.IDENTITY", "RULE.A01.KF.CONTROL"],
            ["document_kind", "document_number", "issuer"],
            [
                field("document_kind", "身份证明类别", "Text", "官方核验或有效身份证明所载类别。", 1),
                field("document_number", "身份证明号码", "Text", "与签发法域共同用于识别个人的号码。", 1),
                field("issuer", "签发国家或地区", "Text", "身份证明签发国家或地区。", 1),
                field("name", "姓名", "Text", "自然人姓名；同名不能作为合并身份的依据。", 1),
                field("gender", "性别", "Text", "金融机构一般客户识别所需身份信息。"),
                field("nationality", "国籍/地区", "Text", "金融机构一般客户识别所需身份信息。"),
                field("birth_date", "出生日期", "Date", "金融机构一般客户识别所需身份信息。"),
                field("document_expiry", "证件有效期限", "Date", "所用身份证明的有效期限；过期不自动抹除历史身份。"),
            ],
            "某个自然人依据股权、最终收益/表决权、实际控制，或特定条件下的备位路径，被评估是否为组织客户的受益所有人。",
            "权利证据可能指向不同候选人；只有身份核实后才能把权利事实绑定到一个现实自然人。",
            "优先按证件类别、号码与签发法域识别；同名、证件更新或多份证据之间的连续性需要独立核实。",
            ["甲以已核验证件身份持有目标公司的间接权益。"],
            ["仅以姓名字符串相同就合并的两名自然人。"],
            origin="KNOWLEDGE",
        ),
        typ(
            "M.Evidence", "识别证据", "EVIDENCE",
            "支持组织身份、自然人身份、权益/控制关系、有效期间或风险判断的来源记录。",
            ["RULE.A01.KF.EQUITY", "RULE.A01.KF.NOMINEE", "RULE.A01.KF.IDENTITY", "RULE.A01.KF.RISK"],
            ["source_reference", "locator"],
            [
                field("source_reference", "来源记录标识", "Text", "来源文件、官方查询或客户原始材料的可回溯标识。", 1),
                field("locator", "材料位置", "Text", "页码、条款、登记记录或查询结果位置。", 1),
                field("claim", "支持的事实", "Text", "该材料实际支持的身份、权利、时间或风险事实，不超出来源内容。", 1),
                enum("source_authority", "来源性质", ["OFFICIAL", "CUSTOMER_ORIGINAL", "PUBLIC_DISCLOSURE", "INSTITUTION_OBSERVATION", "THIRD_PARTY", "UNKNOWN"], "来源类型不是可靠性结论。"),
                enum("verification_state", "核实状态", ["VERIFIED", "CORROBORATED", "CONFLICTED", "UNVERIFIED", "UNAVAILABLE"], "记录材料核实结果；UNVERIFIED不得视作已证实。"),
                field("issued_on", "材料出具日", "Date", "来源材料被出具的日期，不自动视为权利生效日。"),
                field("obtained_on", "材料取得日", "Date", "金融机构取得该材料的日期。"),
                field("verified_on", "机构核实日", "Date", "机构完成该材料核实的日期；不替代权利形成日。"),
                field("disclosed_on", "对外披露日", "Date", "来源事实对外披露的日期；不替代法律关系生效日。"),
                field("applicable_period", "材料适用期间", "Text", "描述材料所支持事实的时点或期间；不得把材料日期直接替代权利生效日。"),
            ],
            "尽调人员用某份可定位材料支持或质疑一个特定身份、权利、关系期间或风险事实。",
            "增加第二份材料不会自动增加一个业务主体；证据需与它支持的事实和期间绑定。",
            "以来源标识与材料位置区分；同一材料的不同页、条款或查询快照分别定位，不以系统流水号替代来源事实。",
            ["章程特定条款支持某人有权提名多数董事。"],
            ["第三方平台给出的比例标签直接作为已核实的最终权益。"],
        ),
        typ(
            "M.OwnershipLink", "权益持有关系", "FACT",
            "某组织在特定期间向另一组织或自然人持有股权、股份或合伙权益的单条关系边。",
            ["TERM.A01.KF.03", "TERM.A01.KF.04", "RULE.A01.KF.EQUITY", "RULE.A01.KF.NOMINEE"],
            ["target_organization", "holder_kind", "share_class", "relationship_reference"],
            [
                ref("target_organization", "被投资/持有权益的组织", "M.Organization", "路径中接受该段权益的组织。", 1),
                enum("holder_kind", "持有人类别", ["ORGANIZATION", "NATURAL_PERSON"], "每条关系边只有一个持有人类别。", 1),
                ref("holder_organization", "持有人组织", "M.Organization", "当 holder_kind 为 ORGANIZATION 时填写。"),
                ref("holder_person", "持有人自然人", "M.NaturalPerson", "当 holder_kind 为 NATURAL_PERSON 时填写。"),
                field("share_class", "权益类别", "Text", "能够区分同一双方之间不同权益安排的业务类别。", 1),
                field("relationship_reference", "权益关系依据标识", "Text", "来源文件/登记权利关系中的稳定引用；无依据不构造事实边。", 1),
                field("percentage", "本段权益比例", "Decimal", "以百分比数值表示，例如25表示25%；缺失不得按零处理。", 1),
                field("effective_from", "本段关系精确生效日", "Date", "仅在可证实精确法律生效日时填写；登记或查询日期不能代替。"),
                enum("effective_from_precision", "生效时点精度", ["EXACT", "MONTH", "YEAR", "INTERVAL", "UNKNOWN"], "按来源保留精度；非EXACT不得伪造具体日。", 1),
                field("effective_from_period_note", "生效期间说明", "Text", "仅知月份/年份/区间时记录对应来源描述。"),
                field("effective_to", "本段关系终止日", "Date", "有证据时记录终止日；未知或未终止与OPEN状态分别处理。"),
                enum("end_status", "关系终止状态", ["OPEN", "KNOWN", "UNKNOWN"], "OPEN表示有依据确认仍持续；UNKNOWN表示无法判断是否终止。", 1),
                ref("evidence", "持有关系证据", "M.Evidence", "支持持有人、比例和期间的材料。", 1, None),
            ],
            "在某一时点，某个组织或自然人通过一条有效权益边持有另一个组织的一定股权或合伙权益。",
            "直接与多层间接比例须按边计算并区分多条路径；把关系作为事实边可保留路径、期间和证据。",
            "同一目标、持有人、权益类别与生效区间构成关系身份；若身份字段或期间不明，不生成伪造的完整关系。",
            ["甲持有B公司30%，B公司持有客户A 80%，两条边分别留存。"],
            ["把B公司控制客户A解释成甲持有A公司100%权益。"],
        ),
        typ(
            "M.EquityPath", "权益穿透路径", "FACT",
            "从一个自然人经由有序权益关系边抵达目标组织的单条无环路径及其权益贡献。",
            ["RULE.A01.KF.EQUITY", "RULE.A01.KF.DATES"],
            ["target_organization", "person", "as_of", "path_key"],
            [
                ref("target_organization", "目标组织", "M.Organization", "路径终点组织。", 1),
                ref("person", "最终自然人", "M.NaturalPerson", "路径起点自然人。", 1),
                field("as_of", "路径判断时点", "Date", "所有路径边按同一时点筛选。", 1),
                field("path_key", "路径标识", "Text", "区分同一人到同一组织的不同关系路径。", 1),
                ref("steps", "有序路径步骤", "M.EquityPathStep", "按 step_order 排序，每步引用一条权益边。", 1, None),
                field("path_percentage", "单路径权益贡献", "Decimal", "路径边逐段相乘后的比例贡献，例如30表示30%。"),
                enum("path_status", "路径状态", ["VALID", "INCOMPLETE", "CYCLICAL", "CONFLICTED", "UNKNOWN"], "不完整、循环或冲突路径不按零计入。", 1),
                ref("evidence", "路径核验证据", "M.Evidence", "支持路径中各边及期间的来源材料。", 0, None),
            ],
            "识别人员逐条记录自然人到目标组织的权益路径及逐边相乘的单路径贡献。",
            "显式保留有序边和路径贡献，避免把中间组织控制当作100%权益或丢失多路径依据。",
            "以目标组织、自然人、时点和有序边序列区分；关系变化产生新的时点路径。",
            ["甲通过B再到目标组织的间接路径按两段比例相乘。"],
            ["把B控制目标组织解释为甲持有目标组织100%权益。"],
        ),
        typ(
            "M.EquityPathStep", "权益路径步骤", "FACT",
            "某权益关系边在一条穿透路径中的有序位置。",
            ["RULE.A01.KF.EQUITY"],
            ["path", "step_order"],
            [
                ref("path", "所属路径", "M.EquityPath", "对应的单条权益路径。", 1),
                ref("ownership_link", "权益关系边", "M.OwnershipLink", "该步骤采用的已核权益边。", 1),
                field("step_order", "路径顺序", "Integer", "从自然人一侧到目标组织一侧的正整数顺序。", 1),
            ],
            "一条权益边在某条具体路径中占据确定顺序位置。",
            "同一关系边可被多条路径引用；序号支持逐边计算回放。",
            "以路径与路径内序号区分。",
            ["路径P的第2步引用B持有目标组织的权益边。"],
            ["把多条不同路径合并成无序边集合。"],
        ),
        typ(
            "M.OtherRight", "收益或表决权安排", "FACT",
            "自然人最终享有的收益权或表决权关系，独立于股权边记录。",
            ["TERM.A01.KF.04", "RULE.A01.KF.RETURNS_VOTES", "RULE.A01.KF.NOMINEE"],
            ["target_organization", "person", "right_kind", "arrangement_reference"],
            [
                ref("target_organization", "目标组织", "M.Organization", "发生收益或表决权关系的组织。", 1),
                ref("person", "权利自然人", "M.NaturalPerson", "收益或表决权最终归属/行使的自然人。", 1),
                enum("right_kind", "权利类型", ["ECONOMIC_BENEFIT", "VOTING"], "收益与表决是不同权利，不得混同。", 1),
                field("arrangement_reference", "权利安排依据标识", "Text", "协议、章程或权利来源中的稳定引用。", 1),
                field("percentage", "最终权利比例", "Decimal", "按最终权利计算的百分比，25含本数；缺失保持UNKNOWN。", 1),
                field("effective_from", "权利精确生效日", "Date", "仅在证据支持精确法律生效日时填写。"),
                enum("effective_from_precision", "生效时点精度", ["EXACT", "MONTH", "YEAR", "INTERVAL", "UNKNOWN"], "按来源保留精度，不能自动补月首或年初。", 1),
                field("effective_from_period_note", "生效期间说明", "Text", "记录非精确生效期间及其来源。"),
                field("effective_to", "权利终止日", "Date", "有证据时填写，不能以材料更新时间替代。"),
                enum("end_status", "权利终止状态", ["OPEN", "KNOWN", "UNKNOWN"], "区分仍有效与终止状态未知。", 1),
                ref("evidence", "权利安排证据", "M.Evidence", "协议、章程、实际分配/投票记录及核验材料。", 1, None),
            ],
            "某自然人在特定期间最终享有目标组织的收益权或表决权。",
            "相同比例可能来自不同权利，且与股权、控制的判断条件不同，需要独立记录。",
            "以目标组织、自然人、权利类型和生效期间区分；协议续期、变更或终止形成不同的有效关系。",
            ["非股东甲依据生效协议享有目标组织25%的表决权。"],
            ["仅有一笔分红流水便断言甲最终收益权达到25%。"],
        ),
        typ(
            "M.ControlArrangement", "实际控制安排", "FACT",
            "自然人单独或通过有证据的联合机制对组织重大事项形成最终支配的安排及实际作用。",
            ["TERM.A01.KF.05", "RULE.A01.KF.CONTROL", "RULE.A01.KF.NOMINEE"],
            ["target_organization", "person", "control_domain", "arrangement_reference"],
            [
                ref("target_organization", "目标组织", "M.Organization", "被支配或共同控制的组织。", 1),
                ref("person", "控制候选人", "M.NaturalPerson", "被评估是否实际控制的自然人。", 1),
                enum("control_domain", "支配领域", ["APPOINTMENT", "MAJOR_DECISIONS", "FINANCIAL_AFFAIRS", "IMPORTANT_ASSETS_OR_FUNDS", "JOINT_CONTROL"], "分别记录人事、重大决策、财务、重要资产/主要资金或联合控制。", 1),
                field("arrangement_reference", "控制安排依据标识", "Text", "有效协议、章程或治理决议中的稳定关系引用。", 1),
                field("decision_power", "具体支配能力", "Text", "具体事项、权限来源和该人如何影响组织决定。", 1),
                field("actual_exercise", "实际作用证据摘要", "Text", "区分有效权限与持续/真实行使；仅职位或签字不充分。"),
                field("joint_group", "联合机制说明", "Text", "仅共同控制时说明共同机制和该自然人自身权限。"),
                field("effective_from", "安排精确生效日", "Date", "仅在证据支持精确法律生效日时填写。"),
                enum("effective_from_precision", "生效时点精度", ["EXACT", "MONTH", "YEAR", "INTERVAL", "UNKNOWN"], "非精确日保留原有精度，不以披露/核实日替代。", 1),
                field("effective_from_period_note", "生效期间说明", "Text", "记录来源支持的月份、年份或区间。"),
                field("effective_to", "安排终止日", "Date", "有证据时填写。"),
                enum("end_status", "安排终止状态", ["OPEN", "KNOWN", "UNKNOWN"], "未知不得表示为已经结束。", 1),
                ref("evidence", "控制安排证据", "M.Evidence", "协议、任免、决策、预算、资产支配和长期实际行使证据。", 1, None),
            ],
            "某自然人基于有效权限和实际作用，最终决定组织的人事、重大事项、财务或重要资产。",
            "职位名称、法定代表人身份和单次签名不等于实际控制；共同控制时须分别记录每个人的权限。",
            "以目标组织、自然人、支配领域与有效起始时点区分；共同安排的变化不改写历史期间。",
            ["甲依持续有效的协议与表决记录共同决定目标公司的重大经营事项。"],
            ["某人只因担任法定代表人或签过一次付款单而被认定为实际控制人。"],
        ),
        typ(
            "M.CandidateAssessment", "自然人识别评估", "FACT",
            "针对一个自然人、一个目标组织和一个判断时点，分别记录三项一般标准及备位前提。",
            ["TERM.A01.KF.02", "TERM.A01.KF.03", "TERM.A01.KF.04", "TERM.A01.KF.05", "TERM.A01.KF.06", "RULE.A01.KF.EQUITY", "RULE.A01.KF.RETURNS_VOTES", "RULE.A01.KF.FALLBACK"],
            ["target_organization", "person", "as_of"],
            [
                ref("target_organization", "目标组织", "M.Organization", "本次识别对象。", 1),
                ref("person", "被评估自然人", "M.NaturalPerson", "身份已核实或作为待核候选的自然人。", 1),
                field("as_of", "判断时点", "Date", "所有权益和控制事实均对应的同一判断时点。", 1),
                field("first_qualified_on", "首次达标法律生效日", "Date", "该自然人首次达到任一一般识别标准的法律关系生效日；具体依据仍以受益所有权关系区分。"),
                enum("first_qualified_precision", "首次达标日期精度", ["EXACT", "MONTH", "YEAR", "INTERVAL", "UNKNOWN"], "只保留来源支持的精度，不用月首或年初补造具体日。", 1),
                field("first_qualified_period_note", "首次达标期间说明", "Text", "日期非精确时记录来源支持的月份、年份或区间。"),
                field("final_equity_percentage", "最终权益比例", "Decimal", "直接及有效间接路径在同一人层面的合计百分比；路径不完整或有循环争议时必须为UNKNOWN。"),
                field("final_benefit_percentage", "最终收益权比例", "Decimal", "最终收益权比例；不能从单笔分配金额臆算。"),
                field("final_voting_percentage", "最终表决权比例", "Decimal", "生效授权范围对应的最终表决权比例。"),
                field("equity_path_status", "权益路径状态", "Enum", "路径完整性及循环/交叉关系状态。", 1, 1, values=["COMPLETE", "INCOMPLETE", "CYCLICAL_OR_CROSS", "CONFLICTED", "UNKNOWN"]),
                ref("equity_paths", "权益穿透路径", "M.EquityPath", "逐条说明路径边、乘积和贡献，作为最终比例的审计依据。", 0, None),
                field("meets_standard1", "符合权益标准", "Boolean", "由最终权益比例与25%含本数规则得出；缺失比例按UNKNOWN传播。"),
                field("meets_standard2", "符合收益/表决标准", "Boolean", "仅在不符合标准一时，依据最终收益权或表决权任一达到25%判断。"),
                field("meets_standard3", "符合实际控制标准", "Boolean", "由人工依据具体支配能力、实际作用和证据形成；未知不能记为否。"),
                ref("ownership_links", "权益关系边", "M.OwnershipLink", "用于解释直接及间接路径，不代表已经完成图遍历。", 0, None),
                ref("other_rights", "收益/表决关系", "M.OtherRight", "按权利类型和有效期间分别引用。", 0, None),
                ref("control_arrangements", "控制安排", "M.ControlArrangement", "支持实际控制人工评估的事实。", 0, None),
                ref("evidence", "候选评估证据", "M.Evidence", "身份、权益、收益/表决、控制和风险的来源材料。", 0, None),
                enum("assessment_state", "评估状态", ["IN_REVIEW", "SUPPORTED", "NOT_SUPPORTED", "INCOMPLETE", "UNKNOWN"], "区分评估进度与业务结论；有缺口不得标为SUPPORTED。", 1),
            ],
            "尽调人员在判断时点逐人检查权益、收益/表决、实际控制及证据；组织级候选全集核查另行判断备位前提。",
            "同一自然人的标准可以重合但不能重复计人；三项标准的否定状态必须与未知状态分开。",
            "以目标组织、自然人和判断时点识别一份评估快照；新证据或新时点形成新评估，不覆盖旧结论。",
            ["甲在2026-09-01的最终权益比例为26%，三项判断和支持材料均按该日记录。"],
            ["只保存‘甲是受益所有人’而没有时点、权利依据或未知项。"],
        ),
        typ(
            "M.CandidatePopulationAssessment", "组织级候选全集核查", "DECISION",
            "针对一个目标组织与判断时点，记录自然人候选是否穷尽、是否存在满足一般标准者以及备位前提。",
            ["RULE.A01.KF.FALLBACK"],
            ["target_organization", "as_of"],
            [
                ref("target_organization", "目标组织", "M.Organization", "候选全集对应的客户组织。", 1),
                field("as_of", "判断时点", "Date", "候选全集和权利状态所对应的日期。", 1),
                ref("candidate_assessments", "逐人评估", "M.CandidateAssessment", "包括所有入选、排除和待核候选。", 0, None),
                field("search_complete", "候选与路径核查是否穷尽", "Boolean", "只有全部相关权益、收益/表决和控制路径均已核对才为TRUE。"),
                field("any_qualifying_candidate", "是否存在满足一般标准者", "Boolean", "全部候选均评估后判定；全集不完整时保持UNKNOWN。"),
                field("fallback_available", "组织级备位前提", "Boolean", "只有全集穷尽且不存在任何符合一般标准者时才为TRUE。"),
                ref("evidence", "全集与排除依据", "M.Evidence", "证明候选搜索完整性和逐人入选/排除结论。", 1, None),
                ref("reviewer", "责任人员", "M.IdentificationReviewer", "由金融机构责任人员核定候选全集完整性。", 1),
            ],
            "责任人员穷尽核查同一组织的全部自然人候选及相关路径后，才判断是否确无符合一般标准者。",
            "一个不达标候选人的评估不能证明组织中没有其他达标自然人。",
            "以目标组织和判断时点识别候选全集快照；新路径、新证据或新时点形成新评估。",
            ["全部自然人候选及控制路径均已核实，三项一般标准均无人符合。"],
            ["只评估一名候选未达标就把法定代表人作为备位人选。"],
        ),
        typ(
            "M.IdentificationReviewer", "金融机构识别责任角色", "ROLE",
            "金融机构承担客户受益所有人识别、合理核实和风险判断职责的经办/复核角色。",
            ["RULE.A01.KF.PROFILE", "RULE.A01.KF.IDENTITY", "RULE.A01.KF.RISK"],
            ["person", "institution"],
            [
                ref("person", "承担职责的自然人", "M.NaturalPerson", "具体人员须在业务记录中有真实身份。", 1),
                ref("institution", "金融机构", "M.Organization", "该人员承担识别职责的机构。", 1),
                field("assigned_function", "职责范围", "Text", "记录经办/复核职责来源；本模型不规定机构岗位名称或内部审批权限。", 1),
            ],
            "某名金融机构人员在具体职责授权下完成或复核客户受益所有人识别。",
            "业务责任角色有独立职责，但具体岗位分权来自机构制度而非本模型推定。",
            "以人员、金融机构和有效职责范围区分；岗位变更不会改写历史识别记录。",
            ["机构授权的尽调人员核验客户控制安排证据。"],
            ["服务供应商的自动输出代替金融机构履行识别职责。"],
            bearer="person",
        ),
        typ(
            "M.IdentificationRouteAssessment", "识别路由评估", "DECISION",
            "对目标组织的客户识别适用范围、一般/简化/免识别路线及风险门槛作有据判断。",
            ["RULE.A01.KF.PROFILE", "RULE.A01.KF.EXCEPTIONS", "RULE.A01.KF.SOE", "RULE.A01.KF.BRANCHES", "RULE.A01.KF.RISK"],
            ["target_organization", "as_of"],
            [
                ref("target_organization", "识别对象", "M.Organization", "目标客户或分支机构。", 1),
                field("as_of", "评估时点", "Date", "以该业务判断日的法律形态和风险状态判断。", 1),
                enum("route", "识别路由", ["GENERAL", "SIMPLIFIED", "EXEMPT", "BLOCKED", "UNKNOWN"], "免识别和简化识别不是同一结果；资格未知不得默认适用。", 1),
                field("route_basis", "路由依据", "Text", "说明适用类别、法条路线与组织事实，备案义务不在本模型内。", 1),
                field("risk_gate_passed", "风险门槛是否满足", "Boolean", "仅在事实和依据充分时填写；风险未知保持UNKNOWN。"),
                ref("evidence", "路由证据", "M.Evidence", "官方设立/登记、产权、组织类别及客户风险资料。", 1, None),
                ref("reviewer", "评估人员", "M.IdentificationReviewer", "金融机构责任角色。", 1),
            ],
            "金融机构先判断组织客户是否适用一般识别、某一法定简化路线或免识别，再决定具体识别深度。",
            "组织形式、国资性质、分支关系和风险条件影响识别路由；相似名称不足以替代资格证明。",
            "以目标组织和判断时点识别；组织形式、风险或所属关系改变时形成新路由判断。",
            ["经官方材料确认为适用类别且风险门槛通过的客户使用对应法定简化路线。"],
            ["仅因客户自称低风险或名称含‘协会’就免识别。"],
        ),
        typ(
            "M.BranchAffiliation", "分支所属关系", "FACT",
            "特定分支机构与其所属总公司之间在某期间的真实有效关系。",
            ["RULE.A01.KF.BRANCHES", "RULE.A01.KF.PROFILE"],
            ["branch_organization", "head_organization", "effective_from"],
            [
                ref("branch_organization", "分支机构", "M.Organization", "分支客户或组织节点。", 1),
                ref("head_organization", "所属总公司", "M.Organization", "经材料证实的所属组织。", 1),
                field("effective_from", "所属关系生效日", "Date", "有证据支持的所属关系起始日。", 1),
                field("effective_to", "所属关系终止日", "Date", "关系终止时记录。"),
                enum("end_status", "所属关系终止状态", ["OPEN", "KNOWN", "UNKNOWN"], "注销、恢复或登记异常期间需区分UNKNOWN。", 1),
                ref("evidence", "所属关系证据", "M.Evidence", "分支和总部登记、存续、恢复状态及关系材料。", 1, None),
                ref("branch_manager", "分支管理人员", "M.NaturalPerson", "外国公司分支识别时所需的至少一名分支高管候选。", 0, None),
            ],
            "在特定期间，某个分支机构隶属于某个总公司，金融机构据此判断何时可承继已核实的总公司受益所有人。",
            "所属关系存在独立时点和证据；总公司注销、恢复或名称变化不能简单沿用旧链。",
            "以分支、总公司及有效区间区分；关系终止后不得把旧受益人作为当前结果。",
            ["有存续证据和关系材料证明境内分支在判断日属于总公司。"],
            ["只凭历史总公司名称或分支营业执照推定当前关系仍然有效。"],
        ),
        typ(
            "M.RiskAssessment", "识别风险评估", "DECISION",
            "记录影响识别核实深度的风险事实、对应措施及剩余缺口；不直接给出洗钱定性。",
            ["RULE.A01.KF.RISK", "RULE.A01.KF.EXCEPTIONS"],
            ["target_organization", "as_of"],
            [
                ref("target_organization", "风险评估对象", "M.Organization", "客户组织。", 1),
                field("as_of", "评估时点", "Date", "风险事实及措施适用的判断时点。", 1),
                enum("triggers", "风险触发事实", ["HIGH_RISK_JURISDICTION", "FOREIGN_RECORD_UNAVAILABLE", "NOMINEE_ARRANGEMENT", "CIRCULAR_OR_CROSS_HOLDING", "FREQUENT_CHANGE", "ML_TF_SUSPICION", "OTHER"], "仅记录有事实支持的风险触发项。", 0, None),
                enum("selected_measures", "加强核实措施", ["INDEPENDENT_SOURCE", "OBTAIN_RIGHTS_AGREEMENT", "CUSTOMER_VISIT", "TRANSACTION_MONITORING", "LOWER_THRESHOLD", "INCREASE_REVIEW_FREQUENCY", "OTHER"], "逐项说明与具体缺口的关系；降低阈值是可选加强措施，不是通用25%替代值。", 0, None),
                field("measure_reason", "措施理由", "Text", "解释每一风险事实如何对应所选措施及其效果。"),
                enum("residual_risk", "剩余风险状态", ["ACCEPTABLE_FOR_REVIEW", "UNRESOLVED", "EXCEEDS_CAPABILITY", "UNKNOWN"], "本模型不决定业务接受或拒绝客户。"),
                ref("evidence", "风险证据", "M.Evidence", "支撑触发事实和措施效果的材料。", 0, None),
            ],
            "金融机构针对特定风险事实选择相称的加强核实措施，并记录核实后的剩余风险。",
            "风险触发事实、措施和剩余风险分开，避免把复杂、境外或代持标签自动等同可疑或拒办。",
            "以组织与评估时点区分；触发事实和措施需能回溯至当时材料。",
            ["境外上层登记无法核实，机构记录失败原因并补充独立可靠来源。"],
            ["仅因持有境外股东就直接判定存在洗钱，或把所有客户默认改为10%阈值。"],
        ),
        typ(
            "M.UBOQualification", "受益所有权关系角色", "ROLE",
            "自然人在目标组织上依据一个或多个独立识别标准承担的、具有期间与证据的受益所有人角色。",
            ["TERM.A01.KF.02", "TERM.A01.KF.03", "TERM.A01.KF.04", "TERM.A01.KF.05", "TERM.A01.KF.06", "RULE.A01.KF.EQUITY", "RULE.A01.KF.RETURNS_VOTES", "RULE.A01.KF.CONTROL", "RULE.A01.KF.FALLBACK"],
            ["person", "target_organization", "qualification_basis"],
            [
                ref("person", "受益所有人自然人", "M.NaturalPerson", "角色承担者必须是自然人。", 1),
                ref("target_organization", "目标组织", "M.Organization", "受益所有权所指向的组织。", 1),
                enum("qualification_basis", "识别依据", ["EQUITY", "ECONOMIC_BENEFIT", "VOTING", "ACTUAL_CONTROL", "FALLBACK_MANAGER"], "同一自然人可以有多个有证据支持的识别依据；备位仅在三项标准均确定不成立时使用。", 1),
                field("first_qualified_on", "首次达标法律生效日", "Date", "保留第一次达到标准的时点，不因比例变更而覆盖。"),
                enum("first_qualified_precision", "首次达标日期精度", ["EXACT", "MONTH", "YEAR", "INTERVAL", "UNKNOWN"], "按证据保留精度，不推定具体日。", 1),
                field("first_qualified_period_note", "首次达标期间说明", "Text", "精度不是EXACT时描述来源支持的期间。"),
                field("effective_from", "当前权利状态生效日", "Date", "当前比例/控制方式对应的法律生效日；不能用登记日替代。"),
                enum("effective_from_precision", "当前权利日期精度", ["EXACT", "MONTH", "YEAR", "INTERVAL", "UNKNOWN"], "仅使用来源支持的日期精度。", 1),
                field("effective_period_note", "当前权利期间说明", "Text", "说明当前权利状态的期间或日期证据缺口。"),
                field("effective_to", "关系终止日", "Date", "有证据时记录。"),
                enum("end_status", "关系终止状态", ["OPEN", "KNOWN", "UNKNOWN"], "未知不等于持续，也不等于终止。", 1),
                ref("candidate_assessment", "自然人评估", "M.CandidateAssessment", "连接比例、控制判断和判断时点。", 1),
                ref("evidence", "关系证据", "M.Evidence", "支持身份、权利和期间的来源材料。", 1, None),
            ],
            "某自然人在有证据支持的期间内，因特定权益、收益、表决、实际控制或严格备位标准而与一个组织形成受益所有权关系。",
            "把受益所有人角色与自然人身份、底层权利事实及最终识别判断分开，便于一人多标准和期间变化解释。",
            "目标组织、自然人、识别依据与生效期间共同识别一段关系；退出后重新达标形成新的关系区间。",
            ["甲因最终权益达到25%在特定期间承担权益标准的受益所有人角色。"],
            ["把名义股东身份本身当作受益所有人关系。"],
            bearer="person",
        ),
        typ(
            "M.IdentificationConclusion", "受益所有人识别结论", "DECISION",
            "金融机构针对一个组织客户和判断时点形成的自然人识别结果、路由、范围完整性和未决事项。",
            ["RULE.A01.KF.PROFILE", "RULE.A01.KF.FALLBACK", "RULE.A01.KF.IDENTITY", "RULE.A01.KF.RISK"],
            ["target_organization", "as_of"],
            [
                ref("target_organization", "识别对象", "M.Organization", "目标客户或适用分支。", 1),
                field("as_of", "判断时点", "Date", "本结论覆盖的客户关系时点。", 1),
                ref("route_assessment", "识别路由判断", "M.IdentificationRouteAssessment", "一般、简化、免识别或阻断状态及依据。", 1),
                enum("result_state", "结果完整性", ["COMPLETE", "PARTIAL", "UNDETERMINED", "EXEMPT"], "COMPLETE仅表示本范围内人选及必要关系均有足够依据，不表示业务批准。", 1),
                ref("qualifications", "已支持的受益所有权关系", "M.UBOQualification", "逐人列明权利标准与有效区间。", 0, None),
                ref("candidate_assessments", "候选评估", "M.CandidateAssessment", "包含已入选和未能排除的候选。", 0, None),
                ref("candidate_population", "组织级候选全集", "M.CandidatePopulationAssessment", "是否穷尽候选及可否启用备位的组织级依据。"),
                field("unresolved_items", "未决事项", "Text", "逐项说明缺证、冲突或未确定的路由，并注明受影响结论。", 0, None),
                ref("reviewer", "识别责任角色", "M.IdentificationReviewer", "金融机构有权尽调人员；本模型不规定准入/授信/报告审批岗位。", 1),
            ],
            "金融机构按明确客户范围和时点，交付已支持的自然人关系，并将未决候选、路径或证据缺口显式保留。",
            "受益所有人姓名、路径、时间、证据、判断状态和业务审批是不同事实；将其合并成单一标签会隐去未知与冲突。",
            "以目标组织与判断时点识别一份结论快照；新证据可修订新版本，不覆盖原判断依据。",
            ["结论列出甲的控制关系及证据，同时保留另一候选人的路径未知事项。"],
            ["仅保存一份无时点、无依据、未决项被清空的自然人名单。"],
        ),
    ]


MODEL_IDS_BY_RULE = {
    "RULE.A01.KF.PROFILE": ["M.Organization", "M.IdentificationRouteAssessment", "M.IdentificationConclusion"],
    "RULE.A01.KF.EQUITY": ["M.OwnershipLink", "M.EquityPath", "M.EquityPathStep", "M.CandidateAssessment", "M.AssessOwnershipPaths", "M.SumEquityPaths", "M.MeetsEquityThreshold"],
    "RULE.A01.KF.NOMINEE": ["M.OwnershipLink", "M.OtherRight", "M.ControlArrangement", "M.ReviewCandidateEvidence"],
    "RULE.A01.KF.RETURNS_VOTES": ["M.OtherRight", "M.CandidateAssessment", "M.MeetsBenefitVoteThreshold"],
    "RULE.A01.KF.CONTROL": ["M.ControlArrangement", "M.CandidateAssessment", "M.AssessActualControl"],
    "RULE.A01.KF.FALLBACK": ["M.CandidateAssessment", "M.CandidatePopulationAssessment", "M.ReviewCandidatePopulation", "M.FallbackAvailable", "M.SelectFallbackManager"],
    "RULE.A01.KF.SOE": ["M.Organization", "M.IdentificationRouteAssessment", "M.SelectIdentificationRoute"],
    "RULE.A01.KF.BRANCHES": ["M.BranchAffiliation", "M.ReviewBranchAffiliation", "M.IdentificationConclusion"],
    "RULE.A01.KF.EXCEPTIONS": ["M.IdentificationRouteAssessment", "M.SelectIdentificationRoute", "M.RiskAssessment"],
    "RULE.A01.KF.IDENTITY": ["M.NaturalPerson", "M.Evidence", "M.CandidateAssessment", "M.ReviewCandidateEvidence"],
    "RULE.A01.KF.RISK": ["M.RiskAssessment", "M.SelectRiskMeasures", "M.IdentificationConclusion"],
    "RULE.A01.KF.DATES": ["M.CandidateAssessment", "M.UBOQualification", "M.OwnershipLink", "M.OtherRight", "M.ControlArrangement", "M.AssessOwnershipPaths"],
}

QUESTION_MODEL_IDS = {
    "Q.A01.S12": ["M.Organization", "M.IdentificationRouteAssessment", "M.IdentificationConclusion"],
    "Q.A01.S13": ["M.OwnershipLink", "M.EquityPath", "M.CandidateAssessment", "M.AssessOwnershipPaths", "M.SumEquityPaths", "M.MeetsEquityThreshold"],
    "Q.A01.S14": ["M.OwnershipLink", "M.EquityPath", "M.EquityPathStep", "M.CandidateAssessment", "M.AssessOwnershipPaths", "M.SumEquityPaths", "M.MeetsEquityThreshold"],
    "Q.A01.S16": ["M.OwnershipLink", "M.OtherRight", "M.ReviewCandidateEvidence"],
    "Q.A01.S17": ["M.OtherRight", "M.CandidateAssessment", "M.MeetsBenefitVoteThreshold"],
    "Q.A01.S18": ["M.OtherRight", "M.CandidateAssessment", "M.MeetsBenefitVoteThreshold"],
    "Q.A01.S20": ["M.CandidateAssessment", "M.MeetsBenefitVoteThreshold", "M.AssessActualControl"],
    "Q.A01.S21": ["M.OtherRight", "M.ControlArrangement", "M.ReviewCandidateEvidence", "M.AssessActualControl"],
    "Q.A01.S22": ["M.ControlArrangement", "M.AssessActualControl"],
    "Q.A01.S23": ["M.ControlArrangement", "M.AssessActualControl"],
    "Q.A01.S24": ["M.ControlArrangement", "M.AssessActualControl"],
    "Q.A01.S25": ["M.ControlArrangement", "M.AssessActualControl"],
    "Q.A01.S26": ["M.ControlArrangement", "M.AssessActualControl"],
    "Q.A01.S27": ["M.Organization", "M.IdentificationConclusion"],
    "Q.A01.S28": ["M.CandidateAssessment", "M.CandidatePopulationAssessment", "M.ReviewCandidatePopulation", "M.FallbackAvailable"],
    "Q.A01.S29": ["M.CandidatePopulationAssessment", "M.ReviewCandidatePopulation", "M.FallbackAvailable", "M.SelectFallbackManager"],
    "Q.A01.S30": ["M.Organization", "M.IdentificationRouteAssessment", "M.SelectIdentificationRoute"],
    "Q.A01.S31": ["M.Organization", "M.IdentificationRouteAssessment", "M.SelectIdentificationRoute"],
    "Q.A01.S32": ["M.Organization", "M.OwnershipLink", "M.IdentificationRouteAssessment"],
    "Q.A01.S33": ["M.BranchAffiliation", "M.ReviewBranchAffiliation", "M.IdentificationConclusion"],
    "Q.A01.S34": ["M.BranchAffiliation", "M.ReviewBranchAffiliation", "M.IdentificationConclusion"],
    "Q.A01.S35": ["M.BranchAffiliation", "M.ReviewBranchAffiliation", "M.IdentificationConclusion"],
    "Q.A01.S36": ["M.BranchAffiliation", "M.ReviewBranchAffiliation", "M.IdentificationConclusion"],
    "Q.A01.S45": ["M.Organization", "M.IdentificationRouteAssessment", "M.SelectIdentificationRoute"],
    "Q.A01.S47": ["M.Organization", "M.IdentificationRouteAssessment", "M.SelectIdentificationRoute"],
    "Q.A01.S49": ["M.IdentificationRouteAssessment", "M.RiskAssessment", "M.SelectIdentificationRoute"],
    "Q.A01.S50": ["M.RiskAssessment", "M.SelectRiskMeasures"],
    "Q.A01.S52": ["M.RiskAssessment", "M.SelectRiskMeasures"],
    "Q.A01.S53": ["M.RiskAssessment", "M.SelectRiskMeasures"],
    "Q.A01.S56": ["M.NaturalPerson", "M.Evidence", "M.ReviewCandidateEvidence"],
    "Q.A01.S57": ["M.Evidence", "M.CandidateAssessment", "M.ReviewCandidateEvidence"],
    "Q.A01.S58": ["M.Evidence", "M.CandidateAssessment", "M.ReviewCandidateEvidence"],
    "Q.A01.S60": ["M.CandidateAssessment", "M.UBOQualification", "M.OwnershipLink", "M.OtherRight", "M.ControlArrangement"],
    "Q.A01.S61": ["M.CandidateAssessment", "M.UBOQualification", "M.OwnershipLink", "M.OtherRight", "M.ControlArrangement"],
    "Q.A01.S62": ["M.CandidateAssessment", "M.UBOQualification"],
    "Q.A01.S63": ["M.CandidateAssessment", "M.IdentificationConclusion"],
}

QUESTION_ANSWERS = {
    "Q.A01.S12": "本模型只表达金融机构对客户的独立识别；不包含企业备案办理，也不以备案记录替代机构核实。",
    "Q.A01.S13": "按经核实的直接权益比例判断；25%含本数。低于该标准仍须继续检查收益/表决和实际控制。",
    "Q.A01.S14": "逐层核实有效权益边，对每条无环路径逐段相乘，再合计同一自然人的互异有效路径；循环、交叉或缺边时受影响合计保持UNKNOWN。",
    "Q.A01.S16": "登记名义人不自动等于最终权利人；分别核对最终权益、收益、表决及实际控制的协议、履行和期间。",
    "Q.A01.S17": "仅在该自然人未达到标准一时，按最终收益权是否达到25%判断标准二；单笔分配额不足以证明最终比例。",
    "Q.A01.S18": "仅在未达到标准一时，按生效委托/一致行动的范围和期间核算最终表决权；达到25%含本数时符合该项。",
    "Q.A01.S20": "同一自然人达到标准一后不重复按标准二归类；若其实际控制事实另经核实，控制关系仍单独评价和记录。",
    "Q.A01.S21": "从生效协议、授权和实际行使中判断权利来源与期间；亲属关系、头衔或单次签字只能作为线索。",
    "Q.A01.S22": "核实谁实际决定组织任免及其权限和行使；被任命者或法定代表人身份本身不能证明其控制他人任免。",
    "Q.A01.S23": "以重大事项决定权限及决议/实际执行记录识别支配能力；只有参与会议不等于最终决定权。",
    "Q.A01.S24": "识别持续决定财务收支的人；经办、签字或执行已授权付款不等于决定财务事项。",
    "Q.A01.S25": "结合资产重要性、支配持续性和实际行使记录判断；一次接触资金或临时保管不充分。",
    "Q.A01.S26": "分别记录每个自然人的权限、共同决策机制和实际作用；不能把联合安排压成一个虚拟控制人。",
    "Q.A01.S27": "企业或国资语境的控制标签不是最终自然人结论；继续核查具体自然人的所有权、收益/表决和实际控制。",
    "Q.A01.S28": "只有权益、收益/表决、实际控制三项均经完整核实且确定不成立，备位前提才为真；任一UNKNOWN时不得启用。",
    "Q.A01.S29": "识别实际负责日常经营管理且位于适用最高层级的自然人，并以职责、任职和实际履职证据支持；不能直接填法定代表人。",
    "Q.A01.S30": "根据官方产权、组织治理及实际控制材料区分独资、控股与仅参股；名称或持股标签不足以定性。",
    "Q.A01.S31": "金融机构对符合条件的国有独资/控股客户存在可选简化识别路线；须独立核实客户类别和风险前提，不与备案义务混同。",
    "Q.A01.S32": "国有参股本身不停止社会资本及非股权控制识别；只按已证实的规则处理国资部分，不把国资交易控制标签扩展成金融机构资格。",
    "Q.A01.S33": "先核实分支与所属主体在判断时点的真实关系；满足条件时才可承继已核实的所属主体识别结果。",
    "Q.A01.S34": "金融机构识别侧应核实所属外国公司自然人及至少一名分支高管；外国分支备案事项在本模型外。",
    "Q.A01.S35": "注销或登记缺失不能直接证明无总分关系或前三项标准均不存在；补充存续、所属关系、上层权利与控制证据。",
    "Q.A01.S36": "把注销、恢复和仍登记存续分别作为有时点的组织状态；仅在关系和旧识别资料持续有效且已核实后才承继。",
    "Q.A01.S45": "只有经设立/登记材料确认属于法定免识别类别才可采用免识别；不能凭名称或客户自述。",
    "Q.A01.S47": "按各自组织类别与对应条款判断允许的人选和风险门槛；不得把专业机构负责人、个人独资投资人等横向套用。",
    "Q.A01.S49": "类别、候选人或风险门槛无法准确确定，或出现禁止简化的风险触发时，回到一般/加强识别并保留依据与缺口。",
    "Q.A01.S50": "逐项记录境外核验失败、代持、循环交叉等具体事实，并按缺口选择相称措施；标签本身不证明风险事实成立。",
    "Q.A01.S52": "由金融机构按适用风险规则评估相关客户范围；本模型只保留评估对象、事实和措施，不输出洗钱定性。",
    "Q.A01.S53": "措施应对应具体缺口并复核效果；降低阈值仅为可选加强方式，不能将普通25%标准改成默认10%。",
    "Q.A01.S56": "优先用官方渠道核验身份；无法使用时依据有效身份证明及补充材料，并记录具体核实路径。",
    "Q.A01.S57": "以客户材料为基础，按风险与独立官方/公开/机构发现信息交叉验证；证据须对应具体权利及适用期间。",
    "Q.A01.S58": "仅在明确低风险且可用材料足够支持相关事实时才可采信或部分采信客户材料；记录理由，不能以字段齐全代替权利核实。",
    "Q.A01.S60": "首次达标日与当前权利状态生效日分别记录；登记、披露和核实等流程日期不作为权利形成日替代。",
    "Q.A01.S61": "依据转让文件、章程、决议和控制协议的生效条款及条件完成证据判断权利形成日；签署或登记日不当然等于生效日。",
    "Q.A01.S62": "保留首次达到识别标准的日期；持续达标期间的比例或控制方式变化另建当前状态时点，不覆盖首次达标日。",
    "Q.A01.S63": "结论按明确业务判断时点还原当时有效关系与证据；材料不足时标明未知，不用当前快照填补历史。",
}


def build_judgments():
    reviewer = "M.IdentificationReviewer"
    return [
        {
            "id": "M.AssessOwnershipPaths", "name": "核验并计算权益穿透路径",
            "description": "逐条核实路径节点与边，计算每条有效路径贡献并核定路径全集状态；合计由 M.SumEquityPaths 给出。",
            "inputs": [io("candidate", "自然人评估", "Ref", "M.CandidateAssessment", target="M.CandidateAssessment"), io("links", "权益关系边", "Ref", "M.CandidateAssessment.ownership_links", target="M.OwnershipLink", cardinality={"min": 0, "max": None})],
            "outputs": [io("paths", "有序穿透路径", "Ref", "M.CandidateAssessment.equity_paths", target="M.EquityPath", cardinality={"min": 0, "max": None}), io("path_status", "整体路径状态", "Enum", "M.CandidateAssessment.equity_path_status", values=["COMPLETE", "INCOMPLETE", "CYCLICAL_OR_CROSS", "CONFLICTED", "UNKNOWN"])],
            "responsible_role": reviewer, "required_evidence": ["每段持有人身份及比例的有效依据", "同一判断时点的完整上层结构", "循环、交叉、重复路径和关系期间核对记录"],
            "question_ids": ["Q.A01.S13", "Q.A01.S14", "Q.A01.S60", "Q.A01.S61", "Q.A01.S62"], "issue_ids": ["M.Gap.EvidenceConflict"],
            "on_missing": "BLOCK", "basis_ids": base_ids("RULE.A01.KF.EQUITY", "RULE.A01.KF.DATES"),
            "nature": "BUSINESS_DISCRETION", "criteria": ["从自然人一侧到目标组织一侧为每条路径建立有序边步骤。", "逐边相乘并记下每条路径贡献；不得把中间组织控制比例当作100%权益。", "同一自然人的互异有效路径分别计算后合计，不重复计入同一关系路径。", "缺边、循环、冲突或日期不明影响总量时整体保留UNKNOWN，不把未查明比例按零处理。"],
            "record_fields": ["M.CandidateAssessment.equity_paths", "M.CandidateAssessment.final_equity_percentage", "M.CandidateAssessment.equity_path_status", "M.CandidateAssessment.evidence"],
            "review_requirements": "这是有序图事实上的人工/确定性计算边界；本领域模型未声称提供任意深度图遍历运行时。",
        },
        {
            "id": "M.ReviewCandidateEvidence", "name": "核实自然人身份与权利证据",
            "description": "分别核对自然人身份、权利来源、证据可靠性及适用时点；资料字段齐全不等于权利已核实。",
            "inputs": [io("candidate", "候选评估", "Ref", "M.CandidateAssessment", target="M.CandidateAssessment"), io("evidence", "候选证据", "Ref", "M.CandidateAssessment.evidence", target="M.Evidence", cardinality={"min": 0, "max": None})],
            "outputs": [io("assessment_state", "评估状态", "Enum", "M.CandidateAssessment.assessment_state", values=["IN_REVIEW", "SUPPORTED", "NOT_SUPPORTED", "INCOMPLETE", "UNKNOWN"])],
            "responsible_role": reviewer, "required_evidence": ["自然人官方身份核验结果或有效身份证明与补充材料", "组织登记/章程/协议/权利记录及其生效期间", "独立来源交叉核实、冲突与风险取舍记录"],
            "question_ids": ["Q.A01.S16", "Q.A01.S21", "Q.A01.S56", "Q.A01.S57", "Q.A01.S58"], "issue_ids": ["M.Gap.EvidenceConflict", "M.Gap.ProposedPolicy"],
            "on_missing": "BLOCK", "basis_ids": base_ids("RULE.A01.KF.IDENTITY", "RULE.A01.KF.NOMINEE"),
            "nature": "BUSINESS_DISCRETION", "criteria": ["身份真实性与自然人身份同一性可被可靠来源支持。", "材料支持具体权益、收益/表决或控制关系及对应期间，而非仅有姓名或比例标签。", "客户材料与独立信息相符；存在冲突时先记录受影响事实并补证。", "低风险采信或部分佐证须说明适用条件、理由和剩余风险。"],
            "record_fields": ["M.CandidateAssessment.assessment_state", "M.CandidateAssessment.evidence", "M.CandidateAssessment.equity_path_status"],
            "review_requirements": "核验结论由金融机构责任人员记录；具体岗位授权依机构制度，本模型不作推定。缺身份或权利证据时阻断受影响结论而非把未知记为否。",
        },
        {
            "id": "M.ReviewCandidatePopulation", "name": "核定组织级候选全集及备位前提",
            "description": "确定候选与路径核查是否穷尽，以及是否存在任何符合三项一般标准的自然人。",
            "inputs": [io("population", "候选全集评估", "Ref", "M.CandidatePopulationAssessment", target="M.CandidatePopulationAssessment"), io("candidates", "逐人评估", "Ref", "M.CandidatePopulationAssessment.candidate_assessments", target="M.CandidateAssessment", cardinality={"min": 0, "max": None})],
            "outputs": [io("search_complete", "候选核查完整", "Boolean", "M.CandidatePopulationAssessment.search_complete"), io("any_qualifying", "存在符合者", "Boolean", "M.CandidatePopulationAssessment.any_qualifying_candidate")],
            "responsible_role": reviewer, "required_evidence": ["所有相关自然人候选来源和完整权益/收益/表决/控制路径", "每位候选人的三类标准状态及未知/冲突处理依据"],
            "question_ids": ["Q.A01.S28", "Q.A01.S29"], "issue_ids": ["M.Gap.EvidenceConflict", "M.Gap.ProposedPolicy"],
            "on_missing": "BLOCK", "basis_ids": base_ids("RULE.A01.KF.FALLBACK"),
            "nature": "BUSINESS_DISCRETION", "criteria": ["所有可能自然人及其直接/间接权益、收益/表决和实际控制路径均已覆盖。", "候选全集任何缺口、代持争议或控制UNKNOWN都使search_complete不能为TRUE。", "只要任一候选满足任何一项一般标准，any_qualifying_candidate为TRUE。", "只有全集完整且所有候选三项均确定不成立时才允许备位。"],
            "record_fields": ["M.CandidatePopulationAssessment.search_complete", "M.CandidatePopulationAssessment.any_qualifying_candidate", "M.CandidatePopulationAssessment.fallback_available", "M.CandidatePopulationAssessment.evidence"],
            "review_requirements": "单个候选人三项均否不等于组织级无人符合；责任人员必须确认候选全集完整。",
        },
        {
            "id": "M.AssessActualControl", "name": "裁定实际控制",
            "description": "依据具体决定权限、实际作用和证据判断自然人是否单独或联合最终支配组织。",
            "inputs": [io("arrangements", "控制安排", "Ref", "M.CandidateAssessment.control_arrangements", target="M.ControlArrangement", cardinality={"min": 0, "max": None})],
            "outputs": [io("meets_standard3", "实际控制标准结论", "Boolean", "M.CandidateAssessment.meets_standard3")],
            "responsible_role": reviewer, "required_evidence": ["章程、协议和权限条款", "任免、重大决策、预算财务或重要资产长期支配记录", "联合控制中每个人的权限和共同作用证据"],
            "question_ids": [f"Q.A01.S{i}" for i in range(21, 27)], "issue_ids": ["M.Gap.EvidenceConflict"],
            "on_missing": "BLOCK", "basis_ids": base_ids("RULE.A01.KF.CONTROL"),
            "nature": "BUSINESS_DISCRETION", "criteria": ["候选人为自然人且明确指向目标组织。", "能指出其最终决定的具体事项以及权限来源。", "区分持续实际支配与一般任职、执行、签字或亲属关系。", "联合控制时逐人说明权限、共同机制及其在结论中的作用。"],
            "record_fields": ["M.CandidateAssessment.meets_standard3", "M.CandidateAssessment.control_arrangements", "M.CandidateAssessment.assessment_state"],
            "review_requirements": "只有证据足以支持或排除实际控制时才输出TRUE/FALSE；权限范围或实际作用有冲突时输出UNKNOWN并补证。",
        },
        {
            "id": "M.SelectFallbackManager", "name": "选择备位日常管理人员",
            "description": "只有前三项标准均已确定不成立时，才按真实日常经营管理职责识别备位人员。",
            "inputs": [io("population", "组织级候选全集核查", "Ref", "M.CandidatePopulationAssessment", target="M.CandidatePopulationAssessment")],
            "outputs": [io("fallback_person", "备位自然人", "Ref", "M.UBOQualification.person", target="M.NaturalPerson")],
            "responsible_role": reviewer, "required_evidence": ["三项一般识别标准逐项排查与排除理由", "章程/治理文件、任职和实际日常管理职责证据"],
            "question_ids": ["Q.A01.S28", "Q.A01.S29"], "issue_ids": [],
            "on_missing": "BLOCK", "basis_ids": base_ids("TERM.A01.KF.06", "RULE.A01.KF.FALLBACK"),
            "nature": "BUSINESS_DISCRETION", "criteria": ["M.FallbackAvailable必须对目标组织的完整候选全集为TRUE；单个候选人三项为FALSE不足以触发。", "不得存在任何符合一般标准的自然人；全集未穷尽或任一相关路径UNKNOWN时阻断。", "候选人实际负责日常经营管理并具备适用层级/职责证据。", "法定代表人、董事长或经理头衔本身不足以确定人选。"],
            "record_fields": ["M.CandidatePopulationAssessment.fallback_available", "M.UBOQualification.person", "M.UBOQualification.qualification_basis", "M.IdentificationConclusion.unresolved_items"],
            "review_requirements": "发现上层结构未穿透、代持未核或控制仍有争议时停止备位路径；不以职位字段默认补人。",
        },
        {
            "id": "M.SelectStateOwnedRoute", "name": "核定国资客户识别路线",
            "description": "区分国有独资/控股与国有参股，分别应用金融机构识别规则，不把备案要求带入本模型。",
            "inputs": [io("organization", "组织", "Ref", "M.Organization", target="M.Organization"), io("route", "当前路由评估", "Ref", "M.IdentificationRouteAssessment", target="M.IdentificationRouteAssessment")],
            "outputs": [io("selected_route", "组织类别和适用路线", "Enum", "M.IdentificationRouteAssessment.route", values=["GENERAL", "SIMPLIFIED", "EXEMPT", "BLOCKED", "UNKNOWN"])],
            "responsible_role": reviewer, "required_evidence": ["官方产权/出资链、章程及表决结构", "国资控制证据、组织存续状态及法定代表人任职材料", "客户风险评估及适用的金融机构识别规则"],
            "question_ids": ["Q.A01.S30", "Q.A01.S31", "Q.A01.S32"], "issue_ids": ["M.Gap.StateControlScope"],
            "on_missing": "BLOCK", "basis_ids": base_ids("TERM.A01.KF.07", "RULE.A01.KF.SOE"),
            "nature": "BUSINESS_DISCRETION", "criteria": ["官方产权/治理材料证明独资、控股或仅参股，不依赖企业名称或供应商标签。", "适用金融机构简化路径时另核第十一条组织类别及风险条件。", "国有参股时继续核社会资本和非股权控制。"],
            "record_fields": ["M.Organization.state_ownership_status", "M.IdentificationRouteAssessment.route", "M.IdentificationRouteAssessment.route_basis"],
            "review_requirements": "第32号令国资交易语境的控制结论不能替代金融机构规则；边界或实际控制不清时保持UNKNOWN。",
        },
        {
            "id": "M.ReviewBranchAffiliation", "name": "核实分支所属关系",
            "description": "先验证分支、所属组织和有效期间，再决定金融机构识别结果能否承继或需要追加分支高管。",
            "inputs": [io("affiliation", "分支所属关系", "Ref", "M.BranchAffiliation", target="M.BranchAffiliation"), io("evidence", "关系证据", "Ref", "M.BranchAffiliation.evidence", target="M.Evidence", cardinality={"min": 0, "max": None})],
            "outputs": [io("result", "承继/追加判断", "Enum", "M.IdentificationConclusion.result_state", values=["COMPLETE", "PARTIAL", "UNDETERMINED", "EXEMPT"])],
            "responsible_role": reviewer, "required_evidence": ["分支与总公司当前登记/存续/恢复材料", "总公司当前受益所有人资料及既有尽调核实状态", "外国公司分支自身高管任命和有效期间"],
            "question_ids": ["Q.A01.S33", "Q.A01.S34", "Q.A01.S35", "Q.A01.S36"], "issue_ids": ["M.Gap.EvidenceConflict", "M.Gap.CrossBorder"],
            "on_missing": "BLOCK", "basis_ids": base_ids("RULE.A01.KF.BRANCHES"),
            "nature": "BUSINESS_DISCRETION", "criteria": ["分支与所属主体关系在判断日经可靠材料证明。", "境内分支仅在所属主体识别资料已核且时点适用时考虑承继。", "外国公司分支的金融机构识别还核所属公司自然人及至少一名分支高管。", "注销或恢复状态、旧总公司名或关系异常时不得沿用失效关系。"],
            "record_fields": ["M.BranchAffiliation.effective_from", "M.BranchAffiliation.effective_to", "M.BranchAffiliation.end_status", "M.IdentificationConclusion.result_state"],
            "review_requirements": "国外登记不可核时结合风险评估保留UNKNOWN和补证事项；备案职责和材料不在本模型。",
        },
        {
            "id": "M.SelectIdentificationRoute", "name": "判定客户识别路由",
            "description": "基于组织类别、分支关系、国资事实及风险闸门，判定一般识别、特定简化或免识别。",
            "inputs": [io("organization", "组织主体", "Ref", "M.IdentificationRouteAssessment.target_organization", target="M.Organization"), io("evidence", "类别与风险材料", "Ref", "M.IdentificationRouteAssessment.evidence", target="M.Evidence", cardinality={"min": 1, "max": None})],
            "outputs": [io("route", "识别路由", "Enum", "M.IdentificationRouteAssessment.route", values=["GENERAL", "SIMPLIFIED", "EXEMPT", "BLOCKED", "UNKNOWN"])],
            "responsible_role": reviewer, "required_evidence": ["组织形式与依法设立类别的官方材料", "适用简化/豁免路线的人选/负责人材料", "与路线相称的客户风险核查事实"],
            "question_ids": ["Q.A01.S12", "Q.A01.S27", "Q.A01.S30", "Q.A01.S31", "Q.A01.S32", "Q.A01.S45", "Q.A01.S47", "Q.A01.S49"], "issue_ids": ["M.Gap.StateControlScope", "M.Gap.CrossBorder"],
            "on_missing": "BLOCK", "basis_ids": base_ids("RULE.A01.KF.PROFILE", "RULE.A01.KF.EXCEPTIONS", "RULE.A01.KF.SOE"),
            "nature": "BUSINESS_DISCRETION", "criteria": ["免识别仅在组织属于法定类别且证据匹配时成立。", "简化识别须同时满足各类别自身人选条件与适用风险闸门。", "不满足类别、候选人或风险条件时回一般识别；资格未知时不能默认免识别/简化。", "国企简化与一般豁免单独核实，不借备案办理或信托/资管产品类别推路线。"],
            "record_fields": ["M.IdentificationRouteAssessment.route", "M.IdentificationRouteAssessment.route_basis", "M.IdentificationRouteAssessment.risk_gate_passed"],
            "review_requirements": "本模型只记录金融机构客户识别路径，不形成备案办理、客户准入/授信或对外报告审批结论。",
        },
        {
            "id": "M.SelectRiskMeasures", "name": "选择相称加强核实措施",
            "description": "针对有事实支持的风险触发项选择措施并复核效果；不替代客户准入/拒办裁定。",
            "inputs": [io("assessment", "风险评估", "Ref", "M.RiskAssessment", target="M.RiskAssessment")],
            "outputs": [io("measures", "加强措施", "Enum", "M.RiskAssessment.selected_measures", values=["INDEPENDENT_SOURCE", "OBTAIN_RIGHTS_AGREEMENT", "CUSTOMER_VISIT", "TRANSACTION_MONITORING", "LOWER_THRESHOLD", "INCREASE_REVIEW_FREQUENCY", "OTHER"], cardinality={"min": 0, "max": None})],
            "responsible_role": reviewer, "required_evidence": ["触发风险事实及其具体客户/路径", "所选措施与风险缺口对应理由", "实施结果与剩余风险"],
            "question_ids": ["Q.A01.S50", "Q.A01.S52", "Q.A01.S53"], "issue_ids": ["M.Gap.CrossBorder"],
            "on_missing": "BLOCK", "basis_ids": base_ids("RULE.A01.KF.RISK"),
            "nature": "BUSINESS_DISCRETION", "criteria": ["先指明法规列举风险事实中的具体触发项。", "逐项把材料缺口与补充来源、协议、回访、监测、阈值或频率措施对应。", "措施不充分时再评价剩余风险；不能把未知自动映射为低风险。", "阈值降低属于可选加强措施，不改变普通25%标准。"],
            "record_fields": ["M.RiskAssessment.triggers", "M.RiskAssessment.selected_measures", "M.RiskAssessment.residual_risk"],
            "review_requirements": "记录风险理由与执行效果；本模型不自动认定洗钱/恐怖融资，也不决定接受或拒绝客户。",
        },
    ]


FACET_REFS = {
    "scope": ["M.Organization", "M.IdentificationRouteAssessment"],
    "preconditions": ["M.IdentificationRouteAssessment", "M.CandidateAssessment"],
    "conditions": ["M.MeetsEquityThreshold", "M.MeetsBenefitVoteThreshold", "M.FallbackAvailable", "M.AssessActualControl", "M.SelectIdentificationRoute"],
    "result": ["M.IdentificationConclusion", "M.UBOQualification"],
    "exceptions": ["M.CandidateAssessment", "M.RiskAssessment", "M.IdentificationConclusion"],
    "missing_evidence": ["M.Evidence", "M.ReviewCandidateEvidence", "M.IdentificationConclusion"],
    "effective_period": ["M.OwnershipLink", "M.OtherRight", "M.ControlArrangement", "M.UBOQualification", "M.BranchAffiliation"],
}


FACET_NOTES = {
    "scope": "按显式子集锁定为金融机构非自然人客户的受益所有人识别；备案办理、信托/资管产品和差异报告不在模型范围。",
    "preconditions": "仅在目标组织、自然人候选与同一判断时点可识别后进入相应标准；范围、类别或事实未知时保留未知。",
    "conditions": "阈值与确定性逻辑使用有限DSL表达；图路径、事实真实性、组织类别或实际控制仍按来源证据和人工准则判断。",
    "result": "结果落在具体自然人—目标组织—识别依据—期间的关系及结论记录中；候选和正式确认不混为一谈。",
    "exceptions": "不将例外扩大到相似名称/身份；循环、缺边、证据冲突或风险禁用条件按来源保持UNKNOWN/阻断。",
    "missing_evidence": "缺证明确指向受影响的人、权利或适用路线，并进入结论中的未决事项；不以空值补成否。",
    "effective_period": "权利和控制关系均保留有证据的生效/终止期间；身份核实日、资料日期和权利生效日不互相替代。",
}

RULE_FACET_REFS = {
    "RULE.A01.KF.PROFILE": {"scope": ["M.Organization", "M.IdentificationRouteAssessment"], "preconditions": ["M.Organization.organization_form", "M.IdentificationRouteAssessment.as_of"], "conditions": ["M.SelectIdentificationRoute.criteria"], "result": ["M.IdentificationConclusion", "M.IdentificationRouteAssessment"], "exceptions": ["M.IdentificationRouteAssessment.route"], "missing_evidence": ["M.IdentificationRouteAssessment.evidence"], "effective_period": ["M.IdentificationRouteAssessment.as_of"]},
    "RULE.A01.KF.EQUITY": {"scope": ["M.OwnershipLink", "M.EquityPath", "M.CandidateAssessment"], "preconditions": ["M.CandidateAssessment.as_of", "M.CandidateAssessment.equity_path_status"], "conditions": ["M.AssessOwnershipPaths.criteria", "M.SumEquityPaths.expression", "M.MeetsEquityThreshold.expression"], "result": ["M.CandidateAssessment.final_equity_percentage", "M.CandidateAssessment.meets_standard1"], "exceptions": ["M.CandidateAssessment.equity_path_status"], "missing_evidence": ["M.OwnershipLink.evidence", "M.EquityPath.evidence", "M.CandidateAssessment.evidence"], "effective_period": ["M.OwnershipLink.effective_from", "M.OwnershipLink.end_status"]},
    "RULE.A01.KF.NOMINEE": {"scope": ["M.OwnershipLink", "M.OtherRight", "M.ControlArrangement"], "preconditions": ["M.CandidateAssessment.as_of", "M.Evidence.verification_state"], "conditions": ["M.ReviewCandidateEvidence.criteria", "M.AssessActualControl.criteria"], "result": ["M.UBOQualification"], "exceptions": ["M.Evidence.verification_state"], "missing_evidence": ["M.Evidence", "M.ReviewCandidateEvidence.required_evidence"], "effective_period": ["M.OwnershipLink.effective_from", "M.OtherRight.effective_from", "M.ControlArrangement.effective_from"]},
    "RULE.A01.KF.RETURNS_VOTES": {"scope": ["M.OtherRight", "M.CandidateAssessment"], "preconditions": ["M.CandidateAssessment.meets_standard1"], "conditions": ["M.MeetsBenefitVoteThreshold.expression"], "result": ["M.CandidateAssessment.meets_standard2", "M.UBOQualification.qualification_basis"], "exceptions": ["M.OtherRight.right_kind", "M.OtherRight.end_status"], "missing_evidence": ["M.OtherRight.evidence", "M.ReviewCandidateEvidence.criteria"], "effective_period": ["M.OtherRight.effective_from", "M.OtherRight.end_status"]},
    "RULE.A01.KF.CONTROL": {"scope": ["M.ControlArrangement", "M.CandidateAssessment"], "preconditions": ["M.CandidateAssessment.as_of"], "conditions": ["M.AssessActualControl.criteria"], "result": ["M.CandidateAssessment.meets_standard3", "M.UBOQualification"], "exceptions": ["M.ControlArrangement.actual_exercise", "M.CandidateAssessment.assessment_state"], "missing_evidence": ["M.ControlArrangement.evidence", "M.AssessActualControl.required_evidence"], "effective_period": ["M.ControlArrangement.effective_from", "M.ControlArrangement.end_status"]},
    "RULE.A01.KF.FALLBACK": {"scope": ["M.CandidatePopulationAssessment", "M.UBOQualification"], "preconditions": ["M.CandidatePopulationAssessment.search_complete", "M.CandidatePopulationAssessment.any_qualifying_candidate"], "conditions": ["M.FallbackAvailable.expression"], "result": ["M.SelectFallbackManager.criteria", "M.UBOQualification.qualification_basis"], "exceptions": ["M.CandidatePopulationAssessment.fallback_available"], "missing_evidence": ["M.SelectFallbackManager.required_evidence", "M.ReviewCandidatePopulation.required_evidence"], "effective_period": ["M.CandidatePopulationAssessment.as_of", "M.UBOQualification.effective_from"]},
    "RULE.A01.KF.SOE": {"scope": ["M.Organization.state_ownership_status", "M.IdentificationRouteAssessment"], "preconditions": ["M.Organization.supporting_evidence"], "conditions": ["M.SelectStateOwnedRoute.criteria"], "result": ["M.IdentificationRouteAssessment.route", "M.IdentificationConclusion"], "exceptions": ["M.Organization.state_ownership_status", "M.Gap.StateControlScope"], "missing_evidence": ["M.SelectStateOwnedRoute.required_evidence"], "effective_period": ["M.IdentificationRouteAssessment.as_of"]},
    "RULE.A01.KF.BRANCHES": {"scope": ["M.BranchAffiliation", "M.IdentificationConclusion"], "preconditions": ["M.BranchAffiliation.effective_from", "M.BranchAffiliation.end_status"], "conditions": ["M.ReviewBranchAffiliation.criteria"], "result": ["M.ReviewBranchAffiliation", "M.IdentificationConclusion"], "exceptions": ["M.BranchAffiliation.end_status", "M.Gap.CrossBorder"], "missing_evidence": ["M.BranchAffiliation.evidence", "M.ReviewBranchAffiliation.required_evidence"], "effective_period": ["M.BranchAffiliation.effective_from", "M.BranchAffiliation.end_status"]},
    "RULE.A01.KF.EXCEPTIONS": {"scope": ["M.IdentificationRouteAssessment"], "preconditions": ["M.Organization.organization_form", "M.RiskAssessment"], "conditions": ["M.SelectIdentificationRoute.criteria"], "result": ["M.IdentificationRouteAssessment.route"], "exceptions": ["M.IdentificationRouteAssessment.risk_gate_passed", "M.RiskAssessment.triggers"], "missing_evidence": ["M.IdentificationRouteAssessment.evidence"], "effective_period": ["M.IdentificationRouteAssessment.as_of"]},
    "RULE.A01.KF.IDENTITY": {"scope": ["M.NaturalPerson", "M.CandidateAssessment"], "preconditions": ["M.CandidateAssessment.target_organization", "M.CandidateAssessment.as_of"], "conditions": ["M.ReviewCandidateEvidence.criteria"], "result": ["M.CandidateAssessment.assessment_state", "M.IdentificationConclusion"], "exceptions": ["M.Evidence.verification_state"], "missing_evidence": ["M.Evidence", "M.ReviewCandidateEvidence.required_evidence"], "effective_period": ["M.CandidateAssessment.as_of", "M.OwnershipLink.effective_from"]},
    "RULE.A01.KF.RISK": {"scope": ["M.RiskAssessment", "M.IdentificationConclusion"], "preconditions": ["M.RiskAssessment.triggers"], "conditions": ["M.SelectRiskMeasures.criteria"], "result": ["M.RiskAssessment.selected_measures", "M.RiskAssessment.residual_risk"], "exceptions": ["M.RiskAssessment.residual_risk"], "missing_evidence": ["M.RiskAssessment.evidence", "M.SelectRiskMeasures.required_evidence"], "effective_period": ["M.RiskAssessment.as_of"]},
    "RULE.A01.KF.DATES": {"scope": ["M.CandidateAssessment", "M.UBOQualification"], "preconditions": ["M.CandidateAssessment.as_of", "M.UBOQualification.first_qualified_precision"], "conditions": ["M.AssessOwnershipPaths.criteria"], "result": ["M.CandidateAssessment.first_qualified_on", "M.UBOQualification.first_qualified_on", "M.UBOQualification.effective_from"], "exceptions": ["M.UBOQualification.first_qualified_precision", "M.UBOQualification.effective_from_precision"], "missing_evidence": ["M.AssessOwnershipPaths.required_evidence"], "effective_period": ["M.OwnershipLink.effective_from", "M.OtherRight.effective_from", "M.ControlArrangement.effective_from"]},
}


def build_rules():
    return [
        {
            "id": "M.SumEquityPaths", "name": "汇总同一自然人有效权益路径", "description": "路径全集完整且每条路径有效时，合计互异路径贡献；否则结果为UNKNOWN。",
            "inputs": [io("paths", "互异权益路径", "Ref", "M.CandidateAssessment.equity_paths", target="M.EquityPath", cardinality={"min": 0, "max": None}), io("path_status", "整体路径状态", "Enum", "M.CandidateAssessment.equity_path_status", values=["COMPLETE", "INCOMPLETE", "CYCLICAL_OR_CROSS", "CONFLICTED", "UNKNOWN"])],
            "result": {"type": "Decimal"},
            "expression": {"op": "if", "args": [
                {"op": "and", "args": [
                    {"op": "eq", "args": [{"input": "path_status"}, {"literal": {"type": "Text", "value": "COMPLETE"}}]},
                    {"op": "all", "args": [{"query": {"from": {"op": "distinct", "args": [{"input": "paths"}]}, "as": "path", "where": {"literal": {"type": "Boolean", "value": True}}, "select": {"op": "eq", "args": [{"field": {"of": {"input": "path"}, "name": "path_status"}}, {"literal": {"type": "Text", "value": "VALID"}}]}}}]},
                ]},
                {"op": "sum", "args": [{"query": {"from": {"op": "distinct", "args": [{"input": "paths"}]}, "as": "path", "where": {"literal": {"type": "Boolean", "value": True}}, "select": {"field": {"of": {"input": "path"}, "name": "path_percentage"}}}}]},
                {"literal": {"type": "Decimal", "value": None}},
            ]},
            "on_unknown": "PROPAGATE", "basis_ids": ["RULE.A01.KF.EQUITY"], "question_ids": ["Q.A01.S13", "Q.A01.S14"], "depends_on": [],
            "result_binding": "M.CandidateAssessment.final_equity_percentage", "business_meaning": "完整性仍须由责任人员据全图证据核定；仅对已核实、互异且有效的路径贡献求和。",
        },
        {
            "id": "M.MeetsEquityThreshold", "name": "权益比例达到25%", "description": "在最终自然人权益比例已可确定时，判断是否达到25%含本数；未知比例传播为UNKNOWN。",
            "inputs": [io("equity_percentage", "最终权益比例（百分比）", "Decimal", "M.CandidateAssessment.final_equity_percentage"), io("path_status", "整体路径状态", "Enum", "M.CandidateAssessment.equity_path_status", values=["COMPLETE", "INCOMPLETE", "CYCLICAL_OR_CROSS", "CONFLICTED", "UNKNOWN"])],
            "result": {"type": "Boolean"},
            "expression": {"op": "if", "args": [{"op": "eq", "args": [{"input": "path_status"}, {"literal": {"type": "Text", "value": "COMPLETE"}}]}, {"op": "gte", "args": [{"input": "equity_percentage"}, {"literal": {"type": "Decimal", "value": 25}}]}, {"literal": {"type": "Boolean", "value": None}}]},
            "on_unknown": "PROPAGATE", "basis_ids": ["RULE.A01.KF.EQUITY"], "question_ids": ["Q.A01.S13", "Q.A01.S14"], "depends_on": ["M.SumEquityPaths"],
            "result_binding": "M.CandidateAssessment.meets_standard1", "business_meaning": "25含本数；仅对同一判断时点、证据支持的最终权益比例求值。路径不完整、循环或冲突时比例保持未知，不按0处理。",
        },
        {
            "id": "M.MeetsBenefitVoteThreshold", "name": "收益/表决权标准达到25%", "description": "只在自然人不符合权益标准一时，分别看最终收益与表决权是否任一达到25%含本数。",
            "inputs": [io("meets_standard1", "已符合权益标准", "Boolean", "M.CandidateAssessment.meets_standard1"), io("benefit_percentage", "最终收益权比例", "Decimal", "M.CandidateAssessment.final_benefit_percentage"), io("voting_percentage", "最终表决权比例", "Decimal", "M.CandidateAssessment.final_voting_percentage")],
            "result": {"type": "Boolean"},
            "expression": {"op": "if", "args": [{"input": "meets_standard1"}, {"literal": {"type": "Boolean", "value": False}}, {"op": "or", "args": [{"op": "gte", "args": [{"input": "benefit_percentage"}, {"literal": {"type": "Decimal", "value": 25}}]}, {"op": "gte", "args": [{"input": "voting_percentage"}, {"literal": {"type": "Decimal", "value": 25}}]}]}]},
            "on_unknown": "PROPAGATE", "basis_ids": ["RULE.A01.KF.RETURNS_VOTES"], "question_ids": ["Q.A01.S17", "Q.A01.S18", "Q.A01.S20"], "depends_on": ["M.MeetsEquityThreshold"],
            "result_binding": "M.CandidateAssessment.meets_standard2", "business_meaning": "权益标准一为真时标准二归类为假；否则收益权或表决权任一达到25%即为真。标准一未知或两种权利均无法确定时按三值逻辑传播未知。",
        },
        {
            "id": "M.FallbackAvailable", "name": "三项一般标准均确定不成立", "description": "仅当权益、收益/表决与实际控制三个标准均确定为不成立时，备位前提才成立。",
            "inputs": [io("search_complete", "组织级候选及路径已穷尽", "Boolean", "M.CandidatePopulationAssessment.search_complete"), io("any_qualifying", "存在满足一般标准者", "Boolean", "M.CandidatePopulationAssessment.any_qualifying_candidate")],
            "result": {"type": "Boolean"}, "expression": {"op": "and", "args": [{"op": "eq", "args": [{"input": "search_complete"}, {"literal": {"type": "Boolean", "value": True}}]}, {"op": "eq", "args": [{"input": "any_qualifying"}, {"literal": {"type": "Boolean", "value": False}}]}]},
            "on_unknown": "PROPAGATE", "basis_ids": ["RULE.A01.KF.FALLBACK"], "question_ids": ["Q.A01.S28", "Q.A01.S29"], "depends_on": [],
            "result_binding": "M.CandidatePopulationAssessment.fallback_available", "business_meaning": "只有完整候选全集已核且不存在任何达到任一一般标准的自然人时，组织级备位前提才为真；否则为FALSE或UNKNOWN。",
        },
    ]


def build_process():
    process = {
        "id": "M.IdentifyNaturalBeneficialOwners", "name": "金融机构客户受益所有人识别",
        "question_ids": QUESTION_IDS,
        "trigger": "金融机构需要对法人、非法人组织客户或适用分支机构识别自然人受益所有人时。",
        "basis_ids": RULE_IDS,
        "steps": [
            {"id": "M.Step.Scope", "name": "确认客户与判断时点", "kind": "DETERMINE", "uses": ["M.SelectIdentificationRoute"], "reads": ["M.Organization.organization_form", "M.Organization.state_ownership_status"], "writes": ["M.IdentificationRouteAssessment.route", "M.IdentificationRouteAssessment.as_of"], "depends_on": [], "on_missing": "BLOCK", "description": "确认金融机构客户身份、组织类别和同一判断时点；不办理或评价备案。", "basis_ids": ["RULE.A01.KF.PROFILE", "RULE.A01.KF.EXCEPTIONS"]},
            {"id": "M.Step.Branch", "name": "核实分支所属关系", "kind": "VERIFY", "uses": ["M.ReviewBranchAffiliation"], "reads": ["M.BranchAffiliation.branch_organization", "M.BranchAffiliation.head_organization", "M.BranchAffiliation.effective_from", "M.BranchAffiliation.end_status"], "writes": ["M.BranchAffiliation.evidence", "M.IdentificationConclusion.result_state"], "depends_on": ["M.Step.Scope"], "on_missing": "CONTINUE_WITH_GAP", "description": "仅在分支为目标或权益路径节点时执行；关系不明则阻断承继。", "basis_ids": ["RULE.A01.KF.BRANCHES"]},
            {"id": "M.Step.Route", "name": "判定一般、简化或免识别路线", "kind": "DETERMINE", "uses": ["M.SelectIdentificationRoute", "M.SelectStateOwnedRoute"], "reads": ["M.Organization.organization_form", "M.Organization.state_ownership_status", "M.RiskAssessment.triggers"], "writes": ["M.IdentificationRouteAssessment.route", "M.IdentificationRouteAssessment.route_basis", "M.IdentificationRouteAssessment.risk_gate_passed"], "depends_on": ["M.Step.Scope"], "on_missing": "BLOCK", "description": "一般识别为基线；只有组织类别、人选及风险闸门均满足相应规定才采用简化或免识别。", "basis_ids": ["RULE.A01.KF.EXCEPTIONS", "RULE.A01.KF.SOE"]},
            {"id": "M.Step.Relationships", "name": "建立权益、收益、表决与控制事实", "kind": "VERIFY", "uses": ["M.ReviewCandidateEvidence", "M.AssessActualControl"], "reads": ["M.OwnershipLink.target_organization", "M.OtherRight.target_organization", "M.ControlArrangement.target_organization"], "writes": ["M.OwnershipLink.evidence", "M.OtherRight.evidence", "M.ControlArrangement.evidence"], "depends_on": ["M.Step.Route"], "on_missing": "CONTINUE_WITH_GAP", "description": "把名义持有与最终权利、收益权、表决权、实际控制分开，并逐条绑定材料和期间。", "basis_ids": ["RULE.A01.KF.EQUITY", "RULE.A01.KF.NOMINEE", "RULE.A01.KF.RETURNS_VOTES", "RULE.A01.KF.CONTROL"]},
            {"id": "M.Step.Candidate", "name": "核验自然人并逐项评估三类标准", "kind": "DETERMINE", "uses": ["M.AssessOwnershipPaths", "M.ReviewCandidateEvidence", "M.MeetsEquityThreshold", "M.MeetsBenefitVoteThreshold", "M.AssessActualControl"], "reads": ["M.CandidateAssessment.final_equity_percentage", "M.CandidateAssessment.final_benefit_percentage", "M.CandidateAssessment.final_voting_percentage", "M.CandidateAssessment.equity_path_status"], "writes": ["M.CandidateAssessment.meets_standard1", "M.CandidateAssessment.meets_standard2", "M.CandidateAssessment.meets_standard3", "M.CandidateAssessment.assessment_state"], "depends_on": ["M.Step.Relationships"], "on_missing": "CONTINUE_WITH_GAP", "description": "先逐条有序核算权益路径，再评估三项标准；实际控制与证据真实性由责任人员裁定，未核路径不得按零。", "basis_ids": ["RULE.A01.KF.EQUITY", "RULE.A01.KF.RETURNS_VOTES", "RULE.A01.KF.CONTROL", "RULE.A01.KF.IDENTITY", "RULE.A01.KF.DATES"]},
            {"id": "M.Step.Fallback", "name": "仅在组织级无人符合时评估备位", "kind": "DETERMINE", "uses": ["M.ReviewCandidatePopulation", "M.FallbackAvailable", "M.SelectFallbackManager"], "reads": ["M.CandidatePopulationAssessment.candidate_assessments"], "writes": ["M.CandidatePopulationAssessment.search_complete", "M.CandidatePopulationAssessment.any_qualifying_candidate", "M.CandidatePopulationAssessment.fallback_available", "M.UBOQualification.qualification_basis"], "depends_on": ["M.Step.Candidate"], "on_missing": "BLOCK", "description": "只有候选全集和全部相关路径核查完整且无人符合一般标准时才启用备位；单个候选不达标不足以触发。", "basis_ids": ["TERM.A01.KF.06", "RULE.A01.KF.FALLBACK"]},
            {"id": "M.Step.Risk", "name": "选择相称加强核实措施", "kind": "DETERMINE", "uses": ["M.SelectRiskMeasures"], "reads": ["M.RiskAssessment.triggers", "M.RiskAssessment.evidence"], "writes": ["M.RiskAssessment.selected_measures", "M.RiskAssessment.residual_risk"], "depends_on": ["M.Step.Candidate"], "on_missing": "CONTINUE_WITH_GAP", "description": "针对具体风险事实补证并评价效果；不把风险措施变成通用识别阈值或拒办决定。", "basis_ids": ["RULE.A01.KF.RISK", "RULE.A01.KF.EXCEPTIONS"]},
            {"id": "M.Step.Conclusion", "name": "形成有依据的识别结论", "kind": "RECORD", "uses": [], "reads": ["M.CandidateAssessment.assessment_state", "M.CandidateAssessment.evidence", "M.UBOQualification.qualification_basis", "M.RiskAssessment.residual_risk"], "writes": ["M.IdentificationConclusion.result_state", "M.IdentificationConclusion.qualifications", "M.IdentificationConclusion.unresolved_items"], "depends_on": ["M.Step.Fallback", "M.Step.Risk"], "on_missing": "CONTINUE_WITH_GAP", "description": "按自然人、权利标准、有效期间、证据和未决事项记录可支持部分；不输出备案或差异报告。", "basis_ids": ["RULE.A01.KF.IDENTITY", "RULE.A01.KF.RISK", "RULE.A01.KF.FALLBACK"]},
        ],
    }
    next(step for step in process["steps"] if step["id"] == "M.Step.Candidate")["uses"].insert(2, "M.SumEquityPaths")
    fields = {
        f"{type_def['id']}.{field_def['name']}"
        for type_def in build_types() for field_def in type_def["fields"]
    }
    mechanisms = {}
    for rule in build_rules():
        mechanisms[rule["id"]] = (
            {item["binding"] for item in rule["inputs"] if item["binding"] in fields},
            {rule["result_binding"]},
        )
    for judgment in build_judgments():
        mechanisms[judgment["id"]] = (
            {item["binding"] for item in judgment["inputs"] if item["binding"] in fields},
            {item["binding"] for item in judgment["outputs"]},
        )
    for step in process["steps"]:
        for used in step["uses"]:
            reads, writes = mechanisms[used]
            step["reads"] = sorted(set(step["reads"]) | reads)
            step["writes"] = sorted(set(step["writes"]) | writes)
    return process


def build_constraints():
    def self_field(name):
        return {"field": {"of": {"input": "self"}, "name": name}}

    def known(name):
        return {"op": "is_known", "args": [self_field(name)]}

    def eq(name, value):
        return {"op": "eq", "args": [self_field(name), {"literal": {"type": "Text", "value": value}}]}

    constraints = [{
        "id": "M.Constraint.OwnershipHolderMatchesKind", "name": "权益持有人类别与引用一致", "type_id": "M.OwnershipLink",
        "expression": {"op": "or", "args": [
            {"op": "and", "args": [eq("holder_kind", "ORGANIZATION"), known("holder_organization"), {"op": "not", "args": [known("holder_person")]}]},
            {"op": "and", "args": [eq("holder_kind", "NATURAL_PERSON"), known("holder_person"), {"op": "not", "args": [known("holder_organization")]}]},
        ]},
        "on_unknown": "BLOCK", "basis_ids": ["RULE.A01.KF.EQUITY"],
    }]
    for type_id, suffix in [
        ("M.OwnershipLink", "Ownership"),
        ("M.OtherRight", "OtherRight"),
        ("M.ControlArrangement", "Control"),
    ]:
        constraints.append({
            "id": "M.Constraint." + suffix + "DatePrecision",
            "name": "权利生效日期精度与日期值一致",
            "type_id": type_id,
            "expression": {"op": "or", "args": [
                {"op": "and", "args": [eq("effective_from_precision", "EXACT"), known("effective_from")]},
                {"op": "and", "args": [{"op": "not", "args": [eq("effective_from_precision", "EXACT")]}, {"op": "not", "args": [known("effective_from")]}, known("effective_from_period_note")]},
            ]},
            "on_unknown": "BLOCK",
            "basis_ids": ["RULE.A01.KF.DATES"],
        })
    paths = self_field("equity_paths")
    distinct_paths = {"op": "distinct", "args": [paths]}
    path_values = {"query": {"from": distinct_paths, "as": "path", "where": {"literal": {"type": "Boolean", "value": True}}, "select": {"field": {"of": {"input": "path"}, "name": "path_percentage"}}}}
    path_validity = {"query": {"from": distinct_paths, "as": "path", "where": {"literal": {"type": "Boolean", "value": True}}, "select": {"op": "eq", "args": [{"field": {"of": {"input": "path"}, "name": "path_status"}}, {"literal": {"type": "Text", "value": "VALID"}}]}}}
    constraints.append({
        "id": "M.Constraint.CandidateEquityConsistent",
        "name": "权益阈值输入必须等于完整有效路径之和",
        "type_id": "M.CandidateAssessment",
        "expression": {"op": "if", "args": [
            eq("equity_path_status", "COMPLETE"),
            {"op": "and", "args": [
                {"op": "all", "args": [path_validity]},
                {"op": "eq", "args": [self_field("final_equity_percentage"), {"op": "sum", "args": [path_values]}]},
            ]},
            {"op": "not", "args": [known("final_equity_percentage")]},
        ]},
        "on_unknown": "BLOCK",
        "basis_ids": ["RULE.A01.KF.EQUITY"],
    })
    return constraints


def question_process_ids(question_id):
    return ["M.IdentifyNaturalBeneficialOwners"]


def build_model(knowledge, knowledge_ref):
    kc = knowledge["content"]
    question_map = {q["id"]: q for q in kc["questions"]}
    case_map = {c["id"]: c for c in kc["cases"]}
    selected_questions = set(QUESTION_IDS)
    selected_rules = [r for r in kc["rules"] if selected_questions.intersection(r["question_ids"])]
    if {r["id"] for r in selected_rules} != set(RULE_IDS):
        raise ValueError("显式问题范围触发的知识规则集合与策划的规则集合不符。")

    issue_source = {item["id"]: item for item in knowledge["issues"] if item["status"] == "OPEN"}
    selected_rule_map = {r["id"]: r for r in selected_rules}
    selected_statement_ids = {s for r in selected_rules for s in r["statement_ids"]}
    relevant_issue_rules = {}
    for issue_id, issue in issue_source.items():
        affects = set(issue.get("affects", []))
        impacted = [
            rule["id"] for rule in selected_rules
            if rule["id"] in affects or bool(set(rule["statement_ids"]) & affects)
        ]
        direct_questions = selected_questions & affects
        if impacted or direct_questions:
            relevant_issue_rules[issue_id] = impacted

    model_issues = []
    issue_bindings = []
    issue_to_gap = {}
    for issue_id, impacted_rule_ids in relevant_issue_rules.items():
        source = issue_source[issue_id]
        slug = issue_id.removeprefix("ISSUE.A01.KF.")
        model_issue_id = "M.Gap." + "".join(part.title() for part in slug.replace(".", "_").split("_") if part)
        affected_questions = sorted({
            q for rid in impacted_rule_ids for q in selected_rule_map[rid]["question_ids"] if q in selected_questions
        } | (selected_questions & set(source.get("affects", []))))
        affected_models = sorted({mid for rid in impacted_rule_ids for mid in MODEL_IDS_BY_RULE[rid]})
        model_issues.append({
            "id": model_issue_id,
            "kind": "MODEL_GAP",
            "statement": (source["statement"] + "（该源事项实质争点为备案期限，明确不进入本模型判断；因上游同时关联 DATES 规则，合同仍要求保留其追溯绑定。）") if issue_id == "ISSUE.A01.KF.DATED_PUBLISHING" else source["statement"],
            "affects": list(dict.fromkeys([issue_id, *impacted_rule_ids, *affected_questions, *affected_models])),
            "owner": source.get("owner", "领域知识责任人"),
            "recommendation": source.get("recommendation", "取得与本次判断范围相关的直接业务证据后再评审。"),
            "until_resolved": source.get("until_resolved", "相关候选结论保持UNKNOWN或PARTIAL，不得自动补齐。"),
            "status": "OPEN",
            "severity": source.get("severity", "MEDIUM"),
        })
        issue_to_gap[issue_id] = model_issue_id
        issue_bindings.append({
            "knowledge_issue_id": issue_id,
            "model_issue_ids": [model_issue_id],
            "handling": "DEFERRED",
            "reason": "该未决事项直接影响本次显式子集的识别规则/问题，按原状态保留，不在模型阶段关闭。",
        })

    out_of_scope_ids = sorted(set(issue_source) - set(relevant_issue_rules))
    if out_of_scope_ids:
        model_issues.append({
            "id": "M.Gap.OutOfSubsetKnowledgeIssues",
            "kind": "MODEL_GAP",
            "statement": "其余上游OPEN事项已逐项登记，但只影响本次明确排除的备案办理、信托/资管产品、BOMIS、差异报告或其他范围，不在本模型内解决。",
            "affects": out_of_scope_ids,
            "owner": "领域知识阶段责任人",
            "recommendation": "若将来扩展模型范围，先核对固定领域知识版本并重新确认哪些上游事项进入模型范围。",
            "until_resolved": "这些事项继续在领域知识版本中保持OPEN；本模型不引用其结论。",
            "status": "OPEN",
            "severity": "LOW",
        })
        for issue_id in out_of_scope_ids:
            issue_bindings.append({
                "knowledge_issue_id": issue_id,
                "model_issue_ids": ["M.Gap.OutOfSubsetKnowledgeIssues"],
                "handling": "NOT_APPLICABLE",
                "reason": "经显式核对，该事项不影响本次受益所有人识别子集的模型问题或元素；原上游状态仍保留。",
            })

    issues_by_question = {
        qid: sorted(i["id"] for i in model_issues if i["kind"] == "MODEL_GAP" and qid in i["affects"])
        for qid in QUESTION_IDS
    }
    question_coverage = []
    for qid in QUESTION_IDS:
        question = question_map[qid]
        source_rules = sorted(r["id"] for r in selected_rules if qid in r["question_ids"])
        cases = sorted(c["id"] for c in kc["cases"] if qid in c["question_ids"])
        gaps = issues_by_question[qid]
        question_coverage.append({
            "question_id": qid,
            "model_ids": QUESTION_MODEL_IDS[qid],
            "gap_ids": gaps,
            "status": "PARTIAL" if gaps else "MODELED",
            "reason": "该问题的核心识别结构已建模；关联知识OPEN缺口保持未决。" if gaps else "该问题在本模型显式范围内由模型元素和识别流程覆盖。",
            "question": question["question"],
            "answer": QUESTION_ANSWERS[qid],
            "rule_ids": source_rules,
            "process_ids": question_process_ids(qid),
            "case_ids": cases,
        })

    rule_coverage = []
    for rule in selected_rules:
        rid = rule["id"]
        qids = sorted(set(rule["question_ids"]) & selected_questions)
        refs = RULE_FACET_REFS[rid]
        gaps = sorted(i["id"] for i in model_issues if i["kind"] == "MODEL_GAP" and (rid in i["affects"] or set(MODEL_IDS_BY_RULE[rid]) & set(i["affects"])))
        facets = {}
        for facet_name in ["scope", "preconditions", "conditions", "result", "exceptions", "missing_evidence", "effective_period"]:
            note = FACET_NOTES[facet_name]
            if rid in {"RULE.A01.KF.PROFILE", "RULE.A01.KF.SOE", "RULE.A01.KF.BRANCHES", "RULE.A01.KF.IDENTITY"}:
                note += "本规则的备案侧、备案专属字段或备案办理时限明确留在模型边界之外；只交接金融机构客户识别侧。"
            model_refs = list(refs[facet_name])
            if facet_name == "conditions":
                judgment_refs = {
                    "RULE.A01.KF.PROFILE": ["M.SelectIdentificationRoute.criteria"],
                    "RULE.A01.KF.EQUITY": ["M.ReviewCandidateEvidence.criteria"],
                    "RULE.A01.KF.NOMINEE": ["M.ReviewCandidateEvidence.criteria", "M.AssessActualControl.criteria"],
                    "RULE.A01.KF.RETURNS_VOTES": ["M.ReviewCandidateEvidence.criteria"],
                    "RULE.A01.KF.CONTROL": ["M.AssessActualControl.criteria"],
                    "RULE.A01.KF.FALLBACK": ["M.SelectFallbackManager.criteria"],
                    "RULE.A01.KF.SOE": ["M.SelectStateOwnedRoute.criteria"],
                    "RULE.A01.KF.BRANCHES": ["M.ReviewBranchAffiliation.criteria"],
                    "RULE.A01.KF.EXCEPTIONS": ["M.SelectIdentificationRoute.criteria"],
                    "RULE.A01.KF.IDENTITY": ["M.ReviewCandidateEvidence.criteria"],
                    "RULE.A01.KF.RISK": ["M.SelectRiskMeasures.criteria"],
                    "RULE.A01.KF.DATES": ["M.AssessOwnershipPaths.criteria"],
                }[rid]
                model_refs = list(dict.fromkeys([*model_refs, *judgment_refs]))
                has_expression = any(reference.endswith(".expression") for reference in model_refs)
                facets[facet_name] = {
                    "source_text": rule[facet_name], "model_refs": model_refs,
                    "explanation": note, "status": "MIXED" if has_expression else "MANUAL",
                }
                continue
            if facet_name == "exceptions":
                exception_judgment = {
                    "RULE.A01.KF.PROFILE": "M.SelectIdentificationRoute.criteria",
                    "RULE.A01.KF.EQUITY": "M.ReviewCandidateEvidence.criteria",
                    "RULE.A01.KF.NOMINEE": "M.ReviewCandidateEvidence.criteria",
                    "RULE.A01.KF.RETURNS_VOTES": "M.ReviewCandidateEvidence.criteria",
                    "RULE.A01.KF.CONTROL": "M.AssessActualControl.criteria",
                    "RULE.A01.KF.FALLBACK": "M.SelectFallbackManager.criteria",
                    "RULE.A01.KF.SOE": "M.SelectStateOwnedRoute.criteria",
                    "RULE.A01.KF.BRANCHES": "M.ReviewBranchAffiliation.criteria",
                    "RULE.A01.KF.EXCEPTIONS": "M.SelectIdentificationRoute.criteria",
                    "RULE.A01.KF.IDENTITY": "M.ReviewCandidateEvidence.criteria",
                    "RULE.A01.KF.RISK": "M.SelectRiskMeasures.criteria",
                    "RULE.A01.KF.DATES": "M.AssessOwnershipPaths.criteria",
                }[rid]
                facets[facet_name] = {
                    "source_text": rule[facet_name],
                    "model_refs": model_refs + [exception_judgment],
                    "explanation": note, "status": "MANUAL",
                }
                continue
            facets[facet_name] = {
                "source_text": rule[facet_name],
                "model_refs": model_refs,
                "explanation": note,
                "status": "FORMALIZED",
            }
        rule_coverage.append({
            "knowledge_rule_id": rid,
            "question_ids": qids,
            "model_ids": MODEL_IDS_BY_RULE[rid],
            "status": "PARTIAL" if gaps else "MODELED",
            "gap_ids": gaps,
            "facets": facets,
        })

    case_explanations = []
    for case in kc["cases"]:
        case_questions = sorted(set(case["question_ids"]) & selected_questions)
        if not case_questions:
            continue
        case_rules = sorted({rid for q in case_questions for rid in next(row for row in question_coverage if row["question_id"] == q)["rule_ids"]})
        model_ids = sorted({mid for rid in case_rules for mid in MODEL_IDS_BY_RULE.get(rid, [])})
        blocked = any(issues_by_question[q] for q in case_questions)
        case_explanations.append({
            "case_id": case["id"],
            "model_ids": model_ids,
            "explanation": case.get("reasoning", "本案例只用于解释上游预期对应的模型结构，不构成运行结论。"),
            "expected": case["expected"],
            "forbidden": case["forbidden"],
            "status": "BLOCKED" if blocked else "EXPLAINED",
            "title": case.get("reasoning", case["id"]),
            "input_facts": case["input_facts"],
            "steps": [{"model_ids": model_ids, "explanation": "仅用模型对象/事实/判断说明上游案例真值；未重写输入、预期或禁止结果。"}],
            "execution": "NOT_EXECUTED",
            "evaluation_ids": [],
        })

    digest = "sha256:" + KNOWLEDGE_SHA256
    knowledge_ref = {
        "artifact_id": knowledge["artifact_id"],
        "content_version": knowledge["content_version"],
        "contract_version": knowledge["contract_version"],
        "path": "A01受益所有人/03领域知识输出/output.json",
        "digest": digest,
    }
    request = {
        "request_id": "A01.DomainModel.PracticalUBO.Request.2026-09-24",
        "mode": "PRODUCE",
        "scope": SCOPE,
        "knowledge": knowledge_ref,
        "knowledge_basis": "DRAFT",
        "review_mode": "DEFERRED",
        "question_scope_ids": QUESTION_IDS,
        "scope_mode": "EXPLICIT_SUBSET",
    }
    model = {
        "dsl_version": "2.0.0",
        "artifact_id": "A01.DomainModel",
        "content_version": "2026-09-24.practical-ubo.1",
        "name": "受益所有人识别实操领域模型",
        "knowledge_ref": knowledge_ref,
        "knowledge_basis": "DRAFT",
        "question_scope_ids": QUESTION_IDS,
        "types": build_types(),
        "temporal": [
            {"id": "M.Time.BranchAffiliation", "type_id": "M.BranchAffiliation", "start_field": "effective_from", "end_field": "effective_to", "end_status_field": "end_status", "basis_ids": ["RULE.A01.KF.BRANCHES", "TERM.A01.KF.10"]},
        ],
        "rules": build_rules(),
        "state_machines": [],
        "judgments": build_judgments(),
        "question_coverage": question_coverage,
        "case_explanations": case_explanations,
        "upstream_issue_bindings": issue_bindings,
        "issues": model_issues,
        "scope_mode": "EXPLICIT_SUBSET",
        "constraints": build_constraints(),
        "processes": [build_process()],
        "rule_coverage": rule_coverage,
    }
    return request, model


def main():
    raw = KNOWLEDGE_PATH.read_bytes()
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != KNOWLEDGE_SHA256:
        raise SystemExit(f"固定知识摘要变化，停止：{actual_sha}")
    knowledge = json.loads(raw)
    if knowledge.get("contract_version") != "5.0.0" or knowledge.get("content_version") != "2026-09-24.draft.1":
        raise SystemExit("固定知识身份变化，停止生成。")
    request, model = build_model(knowledge, None)
    (MODEL_DIR / "input.json").write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    class NoAliasSafeDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

    (MODEL_DIR / "model.yaml").write_text(yaml.dump(model, Dumper=NoAliasSafeDumper, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    print(json.dumps({
        "request": str(MODEL_DIR / "input.json"),
        "model": str(MODEL_DIR / "model.yaml"),
        "knowledge_digest": "sha256:" + actual_sha,
        "question_count": len(QUESTION_IDS),
        "rule_count": len(RULE_IDS),
        "model_issue_count": len(model["issues"]),
        "case_count": len(model["case_explanations"]),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
