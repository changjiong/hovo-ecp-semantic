#!/usr/bin/env python3
"""Create this fresh A01 draft from the fixed knowledge and prior rule-scope audit."""
from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import yaml


ROOT = Path.cwd()
STAGE = ROOT / "A01受益所有人/04领域模型输出"
KNOWLEDGE_PATH = ROOT / "A01受益所有人/03领域知识输出/output.json"
AUDIT_PATH = STAGE / "process/review/2026-09-28-rule-scope-audit.json"
VERSION = "2026-09-28.fresh-baseline.1"


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def field(name, label, kind, description, *, required=False, many=False, target=None, values=None):
    item = {
        "name": name, "label": label, "type": kind,
        "cardinality": {"min": 1 if required else 0, "max": None if many else 1},
        "description": description,
    }
    if target:
        item["target"] = target
    if values:
        item["values"] = values
    return item


def entity(identifier, name, kind, description, basis, sentence, why, example, counterexample, fields, *, bearer=None):
    item = {
        "id": identifier, "name": name, "kind": kind, "description": description,
        "basis_ids": basis, "identity": ["id"],
        "fields": [field("id", "业务实例标识", "Text", "同一现实对象或事实的稳定区分键，不代表缺证时可编造身份。", required=True)] + fields,
        "examples": [example], "counterexamples": [counterexample],
        "term_origin": "PROPOSED", "business_sentence": sentence,
        "why_object": why, "identity_description": "以原始资料中的对象与权利关系分别核对；标识只用于区分已存在的业务实例。",
    }
    if bearer:
        item["bearer_field"] = bearer
    return item


def build_types():
    return [
        entity(
            "T.Party", "业务当事人", "ENTITY",
            "自然人、组织、分支、信托或产品的同一业务身份；只有自然人可成为最终受益所有人。",
            ["TERM.A01.KF.02", "RULE.A01.KF.EQUITY", "RULE.A01.KF.TRUST"],
            "自然人和组织分别以自身身份参加权益、控制或信托关系。",
            "各关系均需指向同一当事人；登记企业控制标签不能替代自然人身份。",
            "持有目标公司权益的自然人甲与目标公司分别记录。",
            "不能把国资监管语境中的实际控制企业直接记为自然人受益所有人。",
            [
                field("name", "名称或姓名", "Text", "经可靠资料核对的当事人名称；同名不证明同一人。", required=True),
                field("kind", "当事人性质", "Enum", "区分自然人和各类非自然人主体。", required=True,
                      values=["NATURAL_PERSON", "ORGANIZATION", "BRANCH", "TRUST", "PRODUCT", "OTHER"]),
                field("legal_form", "登记组织形态", "Enum", "仅保留识别路径所需的登记形态，不复制工商登记域。",
                      values=["COMPANY", "PARTNERSHIP", "FOREIGN_BRANCH", "DOMESTIC_BRANCH", "INDIVIDUAL_BUSINESS", "OTHER", "UNKNOWN"]),
                field("parent", "所属主体", "Ref", "分支所属主体须按判断时点和有效证据核实。", target="T.Party"),
                field("state_controlled", "国有独资或控股已证实", "Boolean", "必须由产权、控制权和适用口径支持；国有参股不等于控股。"),
                field("registered_on", "设立登记日期", "Date", "仅用于判断适用时点；不替代权利形成日期。"),
            ],
        ),
        entity(
            "T.Right", "逐段权利关系", "FACT",
            "当事人与直接相连主体之间的一段股权、收益权或表决权，逐段记录比例、来源和有效时间；最终自然人比例另由完整路径汇总。",
            ["TERM.A01.KF.03", "TERM.A01.KF.04", "RULE.A01.KF.EQUITY", "RULE.A01.KF.DATES"],
            "某当事人在特定期间对直接相连主体享有一段可核实的权益、收益或表决权。",
            "完整路径由逐段关系连接；名义登记、实际权利及各段有效期间不能混为一条最终比例。",
            "甲持有中间公司20%，中间公司持有目标公司60%；两段分别记录，再计算甲对目标公司的12%。",
            "不能把中间公司60%持股直接全部归给甲，或把最终12%回填成任一段比例。",
            [
                field("holder", "本段实际权利人", "Ref", "可为自然人或中间组织；归属证据不足时保持未知，不能默认登记人。", target="T.Party"),
                field("subject", "本段权利所及主体", "Ref", "该段权利直接对应的组织、信托或产品。", required=True, target="T.Party"),
                field("kind", "权利类别", "Enum", "股权、收益与表决分别判断。", required=True, values=["EQUITY", "BENEFIT", "VOTE"]),
                field("percent", "本段有效比例", "Decimal", "逐段由原始材料核实；最终比例由同日完整路径连乘、去重和汇总，未知段不得按零。"),
                field("nominal_holder", "名义登记人", "Ref", "与最终权利人分开核证。", target="T.Party"),
                field("arrangement", "影响归属的安排", "Ref", "代持、委托等可改变表面归属。", target="T.Arrangement"),
                field("effective_start", "法律关系生效日", "Date", "只有精确日期有证据时填写；不能以登记、核实或报送日代填。"),
                field("formation_bounds", "形成时间已知区间", "IntervalSet", "精确日未知时保留已证实上下界及精度。"),
                field("effective_end", "法律关系终止日", "Date", "若已知终止且有证据则填写。"),
                field("effective_end_bounds", "终止时间已知区间", "IntervalSet", "仅知终止月份或区间时保留上下界、精度与证据，不补造某日。"),
                field("end_status", "终止情况", "Enum", "未终止已证实与终止未知不能混同。", values=["OPEN", "KNOWN", "UNKNOWN"]),
                field("evidence", "权利证据", "Ref", "逐条绑定各边比例、协议及生效材料。", many=True, target="T.Evidence"),
            ],
        ),
        entity(
            "T.Arrangement", "权利与控制安排", "FACT",
            "代持、投票委托、一致行动或信托权力等可能改变最终权利和实际控制的有效安排。",
            ["TERM.A01.KF.04", "TERM.A01.KF.05", "RULE.A01.KF.NOMINEE", "RULE.A01.KF.CONTROL", "RULE.A01.KF.TRUST"],
            "某项有效安排赋予特定当事人对目标的权利或决定能力。",
            "表面持股不能表示协议控制、联合决定和信托处分或指定权。",
            "生效协议赋予甲任免多数董事并决定年度预算的能力。",
            "一次付款签字或亲属关系本身不是实际控制安排。",
            [
                field("actor", "权能行使人", "Ref", "联合控制时各自然人的具体作用须另核。", target="T.Party"),
                field("subject", "受影响主体", "Ref", "安排的目标组织或信托。", required=True, target="T.Party"),
                field("kind", "安排类别", "Enum", "不把不同法律效力的安排合并。", required=True,
                      values=["NOMINEE", "VOTE_PROXY", "JOINT_ACTION", "CONTROL", "TRUST_POWER", "OTHER"]),
                field("power", "实际权限", "Enum", "人事、经营、财务、资产及信托处分或指定权分别核实。", many=True,
                      values=["APPOINTMENT", "MANAGEMENT", "FINANCE", "ASSET", "DISTRIBUTION", "TRUST_CHANGE", "OTHER"]),
                field("effective_start", "安排生效日", "Date", "缺生效证据时保持未知。"),
                field("formation_bounds", "安排形成区间", "IntervalSet", "仅能确定期间时保留范围。"),
                field("effective_end", "安排终止日", "Date", "不可把过期委托计入判断日。"),
                field("effective_end_bounds", "安排终止已知区间", "IntervalSet", "终止日不精确时保留可信范围和精度。"),
                field("end_status", "终止情况", "Enum", "OPEN须有持续有效依据；UNKNOWN不是OPEN。", values=["OPEN", "KNOWN", "UNKNOWN"]),
                field("evidence", "安排证据", "Ref", "协议原件与实际行使记录需要相互核对。", many=True, target="T.Evidence"),
            ],
        ),
        entity(
            "T.Role", "业务角色", "ROLE",
            "自然人或组织在特定主体和期间担任法定代表人、实际日常管理人、信托当事人等角色。",
            ["TERM.A01.KF.06", "TERM.A01.KF.07", "TERM.A01.KF.08", "RULE.A01.KF.BRANCHES"],
            "一个当事人在特定期间对另一主体承担可核实的业务角色。",
            "角色与权利不同；任职名称不能自动证明最终拥有或控制。",
            "甲经任命并实际负责公司日常经营。",
            "登记法定代表人头衔不能证明甲具有最终控制权。",
            [
                field("bearer", "角色承担者", "Ref", "角色承担者身份需独立核实。", required=True, target="T.Party"),
                field("subject", "角色所在主体", "Ref", "所任职组织、分支、信托或产品。", required=True, target="T.Party"),
                field("kind", "角色类别", "Enum", "特定路径的人选资格依角色与有效期间判断。", required=True,
                      values=["LEGAL_REP", "DAILY_MANAGER", "BRANCH_SENIOR", "TRUST_SETTLOR", "TRUST_TRUSTEE", "TRUST_BENEFICIARY", "TRUST_SUPERVISOR", "PRODUCT_MANAGER", "OTHER"]),
                field("effective_start", "任职或角色生效日", "Date", "按任命或信托文件的法律效力核对。"),
                field("formation_bounds", "角色形成区间", "IntervalSet", "精确日期缺证时保留范围。"),
                field("effective_end", "角色终止日", "Date", "角色终止不自动推出其他权利终止。"),
                field("effective_end_bounds", "角色终止已知区间", "IntervalSet", "终止日只知月份或范围时不补造精确日。"),
                field("end_status", "角色终止情况", "Enum", "已证实仍在任、已终止与未知分开。", values=["OPEN", "KNOWN", "UNKNOWN"]),
                field("evidence", "角色证据", "Ref", "官方登记、任命、信托文件及实际职责记录。", many=True, target="T.Evidence"),
            ], bearer="bearer",
        ),
        entity(
            "T.BeneficiaryScope", "信托受益范围", "FACT",
            "信托受益人尚未具体确定时的可核实范围及后来指定事实，与已确认自然人分开。",
            ["TERM.A01.KF.08", "RULE.A01.KF.TRUST"],
            "信托可以先存在一个潜在受益范围，随后才有效指定具体自然人。",
            "未指定范围必须可记录，但不能据此编造每名潜在成员的已确认身份。",
            "信托文件写明未来从家庭成员中指定受益人。",
            "不能在正式指定前把全部家庭成员列为确定受益人。",
            [
                field("trust", "所属信托", "Ref", "对应的具体信托。", required=True, target="T.Party"),
                field("description", "潜在受益范围", "Text", "按信托文件原义保留类别或指定范围。", required=True),
                field("designated_person", "已指定自然人", "Ref", "只有指定已生效且身份获证才填写。", target="T.Party"),
                field("designation_status", "指定情况", "Enum", "潜在、已指定与未知分开。", required=True,
                      values=["POTENTIAL", "CONFIRMED", "UNKNOWN"]),
                field("effective_on", "指定生效日", "Date", "不以信托设立日替代后续指定生效日。"),
                field("evidence", "信托证据", "Ref", "信托文件、指定文件和有效时间资料。", many=True, target="T.Evidence"),
            ],
        ),
        entity(
            "T.Evidence", "权利与身份依据", "EVIDENCE",
            "支持当事人身份、权利归属、角色、期间或判断的可追溯来源及其核实状态。",
            ["TERM.A01.KF.10", "TERM.A01.KF.13", "RULE.A01.KF.IDENTITY"],
            "每一项自然人和权利判断都可以回指具体来源与适用期间。",
            "来源、独立性和冲突会改变结论充分性；系统截图与原始文书不能无差别替代。",
            "已核实的股权转让协议及生效条款。",
            "单一第三方百分比图谱不能证明完整权益路径。",
            [
                field("source", "来源", "Text", "可定位的文件或机构来源。", required=True),
                field("kind", "来源类别", "Enum", "区分原件、官方、客户、机构与外部观察。", required=True,
                      values=["OFFICIAL", "ORIGINAL_DOCUMENT", "CLIENT", "INSTITUTION", "BOMIS", "THIRD_PARTY"]),
                field("issued_on", "资料形成日", "Date", "资料形成日不等于权利生效日。"),
                field("verified_on", "核实日", "Date", "核实行为发生的时间。"),
                field("reliability", "可信及冲突状态", "Enum", "由有权人员依来源与交叉印证判断。",
                      values=["VERIFIED", "UNVERIFIED", "CONFLICTED", "UNKNOWN"]),
                field("claim", "所支持的事实", "Text", "写明材料实际能证明的身份、比例、权能或时间。"),
            ],
        ),
        entity(
            "T.PersonAssessment", "逐人受益所有人判断", "DECISION",
            "同一目标、自然人、判断时点及责任语境下，对每项入选标准分别给出成立、不成立或未知的结果。",
            ["TERM.A01.KF.02", "TERM.A01.KF.06", "RULE.A01.KF.EQUITY", "RULE.A01.KF.GOVERNANCE"],
            "每个候选自然人针对某主体的每项识别标准有一份可解释的判断。",
            "不能只保存姓名和百分比；标准、证据、时间、未知与人工边界都是结果的一部分。",
            "甲在同日两条有效路径合计26%，按权益标准入选。",
            "上层路径缺证时不能给出确定的未入选结论。",
            [
                field("subject", "被识别主体", "Ref", "本次判断的具体目标。", required=True, target="T.Party"),
                field("person", "候选自然人", "Ref", "须独立核实其自然人身份。", required=True, target="T.Party"),
                field("purpose", "结论责任语境", "Enum", "备案与机构独立识别不能互换。", required=True, values=["FILING", "INSTITUTION"]),
                field("as_of", "判断时点", "Date", "历史业务只引用该时点有效关系。", required=True),
                field("criterion", "识别依据", "Enum", "每项标准单独记录，避免同人重复计数。", required=True,
                      values=["EQUITY", "BENEFIT_VOTE", "CONTROL", "FALLBACK", "SOE"]),
                field("outcome", "判断结果", "Enum", "UNKNOWN不等于不成立。", values=["MATCHED", "NOT_MATCHED", "UNKNOWN"]),
                field("is_natural", "自然人身份已证实", "Boolean", "非自然人只可作路径节点。"),
                field("equity_percent", "同人最终权益比例", "Decimal", "完整有效路径连乘、去重并汇总；未知路径不得按零。"),
                field("equity_met", "权益标准成立", "Boolean", "含本数25%阈值判断。"),
                field("benefit_percent", "最终收益比例", "Decimal", "与名义持股分别核实。"),
                field("vote_percent", "最终表决比例", "Decimal", "委托范围、期限和重叠部分均须核实。"),
                field("benefit_vote_met", "收益或表决标准成立", "Boolean", "仅在该人未符合权益标准一时使用。"),
                field("actual_control", "实际控制成立", "Boolean", "人事、重大决策、财务或重要资产支配须有权限与行使证据。"),
                field("is_legal_rep", "有效法定代表人角色", "Boolean", "依有效任职材料和判断时点确认。"),
                field("soe_filing_match", "国控备案法代视同成立", "Boolean", "仅备案路径为应当视同，机构简化另行判断。"),
                field("first_qualified_on", "首次符合标准日", "Date", "持续未退出时不被后来的增持日期覆盖。"),
                field("current_right_formed_on", "当前权利状态形成日", "Date", "与首次达标日和登记披露日区分。"),
                field("rights", "依据的权利关系", "Ref", "可回指逐条权益、收益与表决事实。", many=True, target="T.Right"),
                field("arrangements", "依据的控制安排", "Ref", "可回指代持、控制、信托权能等安排。", many=True, target="T.Arrangement"),
                field("evidence", "判断证据", "Ref", "充分证据逐项绑定；无证部分保持未知。", many=True, target="T.Evidence"),
                field("non_sufficient_facts", "非充分线索", "Text", "记录登记名义、亲属、头衔、单次签字或第三方标签不能单独证明什么。", many=True),
                field("unknown_reason", "未知原因及需补材料", "Text", "明确受影响标准、关系及补证要求。"),
                field("human_boundary", "人工审查边界", "Text", "证据冲突、权利效力和风险判断须由有权人员承担。"),
            ],
        ),
        entity(
            "T.PopulationAssessment", "三标准穷尽与备位判断", "DECISION",
            "对目标主体在同一时点是否已有前三类自然人作整体判断，只有全部证否才能启用备位。",
            ["TERM.A01.KF.06", "RULE.A01.KF.FALLBACK", "RULE.A01.KF.CONTINUOUS"],
            "备位资格依所有必要路径查证后的三项明确否定事实形成。",
            "逐人未找到不等于对整体确认不存在；任一路径未知会阻断备位。",
            "各层权利及控制均查清且前三项都确无自然人，才评估日常管理人。",
            "缺一份可能赋予第三方60%表决权的委托时不能备位。",
            [
                field("subject", "目标主体", "Ref", "同一主体的全部候选路径。", required=True, target="T.Party"),
                field("as_of", "整体判断时点", "Date", "所有路径须在同一时点核对。", required=True),
                field("equity_absent_proven", "权益人不存在已证实", "Boolean", "未知上层路径时保持UNKNOWN。"),
                field("benefit_vote_absent_proven", "收益表决人不存在已证实", "Boolean", "未取得协议时保持UNKNOWN。"),
                field("control_absent_proven", "实际控制人不存在已证实", "Boolean", "未找到材料不等于已证实不存在。"),
                field("fallback_eligible", "可启用备位", "Boolean", "三项全部为真才成立。"),
                field("rights_changed", "人选或关系实质变化", "Boolean", "逐人比较权利与时间，不按总人数净变化判断。"),
                field("evidence", "穷尽检查证据", "Ref", "上层结构、非股权安排及管理职责材料。", many=True, target="T.Evidence"),
                field("unknown_reason", "未完成路径", "Text", "指出哪一项仍是UNKNOWN及待补资料。"),
            ],
        ),
        entity(
            "T.BranchAssessment", "分支受益人组合判断", "DECISION",
            "按同一时点的有效总分关系确定分支应纳入的自然人；外国分支同时承接所属外国公司合格自然人并额外纳入至少一名本分支高级管理人员。",
            ["RULE.A01.KF.BRANCHES"],
            "外国公司中国分支的总部合格自然人与至少一名分支高管须分别核实并共同纳入。",
            "分支高级管理人员是特定增补人选，不要求伪称其达到股权、收益或控制标准；国内分支承继也须核实总分关系。",
            "外国分支总部自然人甲已核实，同时额外纳入任职有效且身份获证的分支高管乙。",
            "只有分支高管乙或旧总部名单，不能认定两个必要人选集合均已核实。",
            [
                field("branch", "目标分支", "Ref", "区分国内分支与外国公司中国分支。", required=True, target="T.Party"),
                field("parent", "同一时点所属主体", "Ref", "注销、恢复或改隶期间须另有有效证据。", target="T.Party"),
                field("as_of", "判断时点", "Date", "总部人选和分支任职均以同一时点核对。", required=True),
                field("headquarters_people", "所属主体合格自然人", "Ref", "按所属主体的一般标准或已核实尽调结果取得。", many=True, target="T.PersonAssessment"),
                field("senior_roles", "有效分支高级管理角色", "Ref", "任命、职责与有效期逐人核实。", many=True, target="T.Role"),
                field("additional_senior_people", "额外纳入的分支高管自然人", "Ref", "外国分支至少一名；不得代替总部合格自然人。", many=True, target="T.Party"),
                field("outcome", "双部分人选核实结果", "Enum", "缺总分关系、总部人选或分支高管证据时为UNKNOWN。",
                      values=["COMPLETE", "INCOMPLETE", "UNKNOWN"]),
                field("evidence", "总分与人选证据", "Ref", "总分关系、所属主体尽调及分支任命履职材料。", many=True, target="T.Evidence"),
                field("non_sufficient_facts", "不充分事实", "Text", "分支营业执照、本地经理头衔或旧总部姓名不能单独证明当前双部分人选。", many=True),
                field("unknown_reason", "未知原因", "Text", "明确尚未核实的所属链、总部穿透或分支任职。"),
                field("human_boundary", "人工核实边界", "Text", "异常登记、境外资料真实性和旧资料复用由有权人员裁定。"),
            ],
        ),
        entity(
            "T.IdentificationRoute", "识别方式资格", "DECISION",
            "针对特定主体、责任语境和时点，区分一般识别、法定免识别、可选择简化及资格未知。",
            ["TERM.A01.KF.09", "RULE.A01.KF.PROFILE", "RULE.A01.KF.EXCEPTIONS"],
            "客户类别、服务关系与风险事实共同决定可否采用特殊识别方式。",
            "同一客户的备案承诺、机构免识别与机构简化不能互换；风险评估是邻域输入。",
            "经核实的低风险特定产品可由机构有权人员考虑简化。",
            "只有产品品名或备案编号不能自动免识别或简化。",
            [
                field("subject", "适用主体", "Ref", "识别方式涉及的客户、信托或产品。", required=True, target="T.Party"),
                field("as_of", "适用时点", "Date", "依当时有效类别与风险判断。", required=True),
                field("purpose", "责任语境", "Enum", "备案与机构规则的责任主体不同。", required=True, values=["FILING", "INSTITUTION"]),
                field("subject_category", "必要主体类别", "Text", "仅引用可否适用识别例外的类别，不建立完整客户分类。"),
                field("service_facts", "必要服务关系", "Text", "只记管理、受托或托管等适用前提。"),
                field("risk_tier", "外部风险结论", "Enum", "由机构风险责任方提供；未知不得当低风险。", values=["LOWER", "ORDINARY", "HIGHER", "UNKNOWN"]),
                field("route", "可采用识别方式", "Enum", "可以简化不等于已批准简化。", values=["GENERAL", "EXEMPT", "SIMPLIFIED", "UNKNOWN"]),
                field("evidence", "资格证据", "Ref", "官方类别、服务合同和机构风险评估记录。", many=True, target="T.Evidence"),
                field("non_sufficient_facts", "不充分条件", "Text", "如公募或持牌名称单独不足以简化。", many=True),
                field("unknown_reason", "资格未知原因", "Text", "缺任一必要类别、合同或风险事实即不放行特殊方式。"),
                field("human_boundary", "人工选择及责任", "Text", "可选路径须由适用机构有权人员决定。"),
            ],
        ),
    ]


def declaration(name, label, binding, fields):
    value = fields[binding]
    result = {"name": name, "label": label, "binding": binding, "type": value["type"],
              "cardinality": deepcopy(value["cardinality"])}
    for key in ("target", "values"):
        if key in value:
            result[key] = deepcopy(value[key])
    return result


def whole(name, label, type_id):
    return {"name": name, "label": label, "binding": type_id, "type": "Ref", "target": type_id}


def literal(kind, value):
    return {"literal": {"type": kind, "value": value}}


def inp(name):
    return {"input": name}


def op(name, *args):
    return {"op": name, "args": list(args)}


def build_rules(fields):
    def rule(identifier, name, description, inputs, result, expression, basis, questions, meaning, *, depends=None):
        result_spec = declaration("result", "判断结果", result, fields)
        del result_spec["name"]
        return {
            "id": identifier, "name": name, "description": description,
            "inputs": [declaration(*item, fields) for item in inputs],
            "result": result_spec, "expression": expression,
            "on_unknown": "PROPAGATE", "basis_ids": basis,
            "question_ids": questions, "depends_on": depends or [],
            "result_binding": result, "business_meaning": meaning,
        }

    return [
        rule("R.NaturalPerson", "自然人身份门槛", "受益所有人结果须指向已核实的自然人。",
             [("person_kind", "候选人的身份性质", "T.Party.kind")], "T.PersonAssessment.is_natural",
             op("eq", inp("person_kind"), literal("Text", "NATURAL_PERSON")),
             ["TERM.A01.KF.02", "RULE.A01.KF.IDENTITY"], ["Q.A01.S13", "Q.A01.S27"],
             "输入是可靠身份资料对应的当事人性质；组织标签不能形成自然人结论。身份未核实则UNKNOWN；同名、系统标签不充分，身份文件冲突由有权人员复核。"),
        rule("R.Equity25", "最终权益达到25%", "对同一自然人、同一目标、同一有效时点，判断完整权益路径合计是否达到含本数25%。",
             [("equity_percent", "已核实最终权益比例", "T.PersonAssessment.equity_percent")],
             "T.PersonAssessment.equity_met", op("gte", inp("equity_percent"), literal("Decimal", 25)),
             ["RULE.A01.KF.EQUITY"], ["Q.A01.S13", "Q.A01.S14"],
             "比例输入须由有效边逐段连乘、互异路径去重并汇总，证据为逐层名册、协议与生效文件。任一路径关键事实未知时受影响合计UNKNOWN，第三方单一比例不充分；路径争议由有权人员裁定。"),
        rule("R.BenefitVote25", "收益或表决达到25%", "只对未符合权益标准一的同一自然人判断有效收益权或表决权是否达到含本数25%。",
             [("equity_met", "权益标准一是否成立", "T.PersonAssessment.equity_met"),
              ("benefit_percent", "最终收益比例", "T.PersonAssessment.benefit_percent"),
              ("vote_percent", "最终表决比例", "T.PersonAssessment.vote_percent")],
             "T.PersonAssessment.benefit_vote_met",
             op("and", op("not", inp("equity_met")),
                op("or", op("gte", inp("benefit_percent"), literal("Decimal", 25)),
                   op("gte", inp("vote_percent"), literal("Decimal", 25)))),
             ["RULE.A01.KF.RETURNS_VOTES"], ["Q.A01.S17", "Q.A01.S18", "Q.A01.S20"],
             "输入须有生效的分配、委托或投票证据并排除重叠；单次分红、未签委托不充分。第一标准或两项权利缺证时按UNKNOWN传播；实际控制另行审查，同一人不重复计数。",
             depends=["R.Equity25"]),
        rule("R.FallbackGate", "备位启用门槛", "前三类自然人均经充分查证确定不存在时，才允许评估日常经营管理人。",
             [("no_equity", "权益人不存在已证实", "T.PopulationAssessment.equity_absent_proven"),
              ("no_benefit_vote", "收益表决人不存在已证实", "T.PopulationAssessment.benefit_vote_absent_proven"),
              ("no_control", "控制人不存在已证实", "T.PopulationAssessment.control_absent_proven")],
             "T.PopulationAssessment.fallback_eligible", op("and", inp("no_equity"), inp("no_benefit_vote"), inp("no_control")),
             ["RULE.A01.KF.FALLBACK"], ["Q.A01.S28", "Q.A01.S29"],
             "三个输入都必须来自完整上层权益、收益表决和控制安排证据；未发现不等于证否。任一UNKNOWN阻断备位，真正日常管理人及职责仍由有权人员核实。"),
        rule("R.SoeFiling", "国控备案法代视同", "国有独资或控股主体的已核实自然人法定代表人在备案责任语境下视同。",
             [("natural", "自然人身份已证实", "T.PersonAssessment.is_natural"),
              ("state_controlled", "国控资格已证实", "T.Party.state_controlled"),
              ("legal_rep", "法定代表人角色有效", "T.PersonAssessment.is_legal_rep")],
             "T.PersonAssessment.soe_filing_match", op("and", inp("natural"), inp("state_controlled"), inp("legal_rep")),
             ["RULE.A01.KF.SOE"], ["Q.A01.S30", "Q.A01.S31", "Q.A01.S32"],
             "仅备案规则为应当视同；国控性质与法代任职须有官方产权和任命证据，参股或国资交易标签单独不充分。任一条件未知则UNKNOWN；机构简化仍由机构按风险另判。",
             depends=["R.NaturalPerson"]),
    ]


def build_judgments(fields):
    def judgment(identifier, name, description, inputs, outputs, evidence, criteria, record_fields, basis, questions, reviewer):
        return {
            "id": identifier, "name": name, "description": description,
            "inputs": [whole(*item) if item[2].startswith("T.") and item[2] in TYPE_IDS else declaration(*item, fields) for item in inputs],
            "outputs": [declaration(*item, fields) for item in outputs],
            "responsible_role": "T.Role", "required_evidence": evidence,
            "question_ids": questions, "issue_ids": [], "on_missing": "BLOCK",
            "basis_ids": basis, "nature": "BUSINESS_DISCRETION", "criteria": criteria,
            "record_fields": record_fields, "review_requirements": "责任边界：" + reviewer + "；逐项记录采用与排除的材料、适用时点、冲突、非充分线索及UNKNOWN原因；具体岗位由机构正式制度确定。",
        }

    return [
        judgment("J.RightAttribution", "名义与真实权利归属", "裁定协议与履行证据能否证明本段真实权利人；证据不足时权利归属UNKNOWN。",
                 [("right", "登记与主张的权利", "T.Right"), ("arrangement", "代持或委托安排", "T.Arrangement"), ("evidence", "协议及履行证据", "T.Evidence")],
                 [("holder", "经核实的本段实际权利人", "T.Right.holder")],
                 ["已生效协议原件及补充协议", "分红、投票与实际履行记录及反向证据"],
                 ["逐项分开权益所有、收益、表决和控制，不以登记名义或亲属关系单独确定最终归属。", "协议真实性、效力期间及实际履行有冲突时保持未知并取得独立佐证。"],
                 ["T.Right.holder", "T.Right.percent", "T.Right.effective_start"],
                 ["RULE.A01.KF.NOMINEE"], ["Q.A01.S16", "Q.A01.S21"], "金融机构有权尽调人员"),
        judgment("J.ActualControl", "自然人实际控制", "依据具体权限和持续行使事实判断最终决定能力；职务或单次经办不是充分事实。",
                 [("arrangement", "控制权安排", "T.Arrangement"), ("role", "任职角色", "T.Role"), ("evidence", "权限与行使证据", "T.Evidence")],
                 [("control", "实际控制结论", "T.PersonAssessment.actual_control")],
                 ["生效协议、章程及共同决策机制", "任免、重大经营决策、资金或重要资产的实际行使记录"],
                 ["逐人核实单独或联合对人事、重大经营、财务或重要资产的最终决定能力。", "第一大股东、法代、亲属、一次签字和公开实控标签仅为线索；证据冲突时UNKNOWN。"],
                 ["T.PersonAssessment.actual_control", "T.PersonAssessment.unknown_reason"],
                 ["RULE.A01.KF.CONTROL"], ["Q.A01.S21", "Q.A01.S22", "Q.A01.S23", "Q.A01.S24", "Q.A01.S25", "Q.A01.S26"], "金融机构有权尽调人员"),
        judgment("J.Evidence", "身份与权利证据充分性", "分开审查身份、权利、日期的来源可靠性和冲突，保留未证实部分。",
                 [("evidence", "待审来源", "T.Evidence"), ("person", "相关当事人", "T.Party")],
                 [("reliability", "来源核实状态", "T.Evidence.reliability")],
                 ["官方身份证明或合规替代资料", "原始权利文件、独立来源及适用时间"],
                 ["资料实际支持哪一自然人、权利比例、控制方式及日期，逐项写明；身份完整不代表权利已证。", "第三方百分比、备案姓名或自动输出单独不足；来源互斥时记冲突并补证。"],
                 ["T.Evidence.reliability", "T.Evidence.claim", "T.PersonAssessment.unknown_reason"],
                 ["RULE.A01.KF.IDENTITY", "RULE.A01.KF.TRUST_RELIANCE", "RULE.A01.KF.GOVERNANCE"],
                 ["Q.A01.S56", "Q.A01.S57", "Q.A01.S58", "Q.A01.S59", "Q.A01.P12"], "适用机构有权核实人员"),
        judgment("J.Route", "免识别与简化资格", "按法定主体/产品类别、必要服务关系和风险事实决定识别方式；可以简化不等于自动简化。",
                 [("party", "目标主体", "T.Party"), ("route", "识别语境和风险", "T.IdentificationRoute"), ("evidence", "类别及风险证据", "T.Evidence")],
                 [("result", "识别方式", "T.IdentificationRoute.route")],
                 ["官方主体或产品类别材料", "管理、受托、托管合同及募集备案资料", "机构当时风险评估与可采信来源"],
                 ["备案承诺、机构免识别和机构可选简化分别适用，不互相代替。", "信托与资管特殊路径须逐项证实类别、服务关系、结构及低风险；高风险或任一关键条件未知时回到一般识别。", "他机构名单有疑点时不能直接采信，机器风险标签也不等于机构批准。"],
                 ["T.IdentificationRoute.route", "T.IdentificationRoute.unknown_reason", "T.IdentificationRoute.human_boundary"],
                 ["RULE.A01.KF.PROFILE", "RULE.A01.KF.TRUST_PRODUCTS", "RULE.A01.KF.ASSET_PRODUCTS", "RULE.A01.KF.EXCEPTIONS", "RULE.A01.KF.RISK"],
                 ["Q.A01.S12", "Q.A01.S41", "Q.A01.S42", "Q.A01.S43", "Q.A01.S44", "Q.A01.S45", "Q.A01.S47", "Q.A01.S49", "Q.A01.S50", "Q.A01.S53"], "适用机构有权尽调及风险人员"),
        judgment("J.Trust", "信托自然人归属", "按信托角色、指定范围与实际最终控制权核实具体自然人。",
                 [("role", "信托当事人角色", "T.Role"), ("scope", "潜在受益范围", "T.BeneficiaryScope"), ("arrangement", "信托权能安排", "T.Arrangement")],
                 [("outcome", "信托自然人判断", "T.PersonAssessment.outcome")],
                 ["信托合同及当事人身份证明", "受益人指定文件与非自然人当事人上层控制链", "信托财产处分、分配与变更权实际行使证据"],
                 ["委托人、受托人、受益人、监察人分别核查；非自然人当事人追至最终有效控制自然人。", "未来指定的类别仅作潜在范围，未指定不编人名；额外处分或变更权须单独核实。"],
                 ["T.PersonAssessment.outcome", "T.PersonAssessment.unknown_reason", "T.BeneficiaryScope.designation_status"],
                 ["RULE.A01.KF.TRUST"], ["Q.A01.S37", "Q.A01.S38", "Q.A01.S39", "Q.A01.S40"], "金融机构有权尽调人员及必要法律支持"),
        judgment("J.BranchInclusion", "分支双部分人选核实", "按有效总分关系同时核实所属主体合格自然人和外国分支额外至少一名高管；缺证部分保持UNKNOWN。",
                 [("branch", "目标分支", "T.Party"), ("parent", "同一时点所属主体", "T.Party"),
                  ("headquarters_person", "所属主体自然人判断", "T.PersonAssessment"),
                  ("senior_role", "分支高管任职", "T.Role"), ("evidence", "总分与任职材料", "T.Evidence")],
                 [("additional_people", "额外纳入分支高管自然人", "T.BranchAssessment.additional_senior_people"),
                  ("outcome", "双部分核实结果", "T.BranchAssessment.outcome")],
                 ["分支与所属主体当前及历史登记、注销恢复与总分关系文件", "所属主体完整自然人尽调档案及有效时点",
                  "外国分支高级管理人员任命、身份、职责和任期证据"],
                 ["国内分支只有总分关系和所属主体尽调有效时才承继；外国分支须另纳入至少一名任职有效的本分支高管。",
                  "外国分支高管人选不替代所属外国公司的合格自然人；总部链未知时双部分结果UNKNOWN，但可独立核实本地高管。",
                  "分支执照、旧总部名称、当地申报豁免或法代头衔单独不充分。"],
                 ["T.BranchAssessment.parent", "T.BranchAssessment.headquarters_people", "T.BranchAssessment.senior_roles",
                  "T.BranchAssessment.additional_senior_people", "T.BranchAssessment.outcome", "T.BranchAssessment.unknown_reason"],
                 ["RULE.A01.KF.BRANCHES"], ["Q.A01.S33", "Q.A01.S34", "Q.A01.S35", "Q.A01.S36"],
                 "适用机构有权尽调人员；异常总分状态与境外材料需专门核实"),
        judgment("J.FormationDate", "权利、安排与角色有效时间", "区分首次达标、当前权利状态、各关系形成与终止区间及披露核实日期；不从月份猜测某日。",
                 [("right", "逐段权利与时间", "T.Right"), ("arrangement", "控制或权利安排与时间", "T.Arrangement"),
                  ("role", "角色与任期", "T.Role"), ("evidence", "生效及终止证据", "T.Evidence")],
                 [("right_formed_on", "权利已证实形成日", "T.Right.effective_start"),
                  ("right_formation_bounds", "权利形成已知区间", "T.Right.formation_bounds"),
                  ("right_ended_on", "权利已证实终止日", "T.Right.effective_end"),
                  ("right_end_bounds", "权利终止已知区间", "T.Right.effective_end_bounds"),
                  ("arrangement_formed_on", "安排已证实形成日", "T.Arrangement.effective_start"),
                  ("arrangement_formation_bounds", "安排形成已知区间", "T.Arrangement.formation_bounds"),
                  ("arrangement_ended_on", "安排已证实终止日", "T.Arrangement.effective_end"),
                  ("arrangement_end_bounds", "安排终止已知区间", "T.Arrangement.effective_end_bounds"),
                  ("role_formed_on", "角色已证实生效日", "T.Role.effective_start"),
                  ("role_formation_bounds", "角色形成已知区间", "T.Role.formation_bounds"),
                  ("role_ended_on", "角色已证实终止日", "T.Role.effective_end"),
                  ("role_end_bounds", "角色终止已知区间", "T.Role.effective_end_bounds")],
                 ["章程、转让、控制协议的生效条件与完成事实", "历史版本及终止、重新进入材料"],
                 ["逐项依真实生效与终止条件记录权利、安排和角色的有效时间；持续持有的首次达标日与后来比例状态日并存。", "仅知年月或文件冲突时保留区间和UNKNOWN；登记、核实、备案日期不自动替代。"],
                 ["T.Right.effective_start", "T.Right.formation_bounds", "T.Right.effective_end", "T.Right.effective_end_bounds",
                  "T.Arrangement.effective_start", "T.Arrangement.formation_bounds", "T.Arrangement.effective_end", "T.Arrangement.effective_end_bounds",
                  "T.Role.effective_start", "T.Role.formation_bounds", "T.Role.effective_end", "T.Role.effective_end_bounds",
                  "T.PersonAssessment.first_qualified_on", "T.PersonAssessment.current_right_formed_on"],
                 ["RULE.A01.KF.DATES", "RULE.A01.KF.HISTORICAL"], ["Q.A01.S60", "Q.A01.S61", "Q.A01.S62", "Q.A01.S63", "Q.A01.P13"], "金融机构有权尽调人员及必要法律支持"),
        judgment("J.ChangeImpact", "人选与权利变化影响", "比较前后逐人关系和期间是否改变结论；不以受益人总人数净差替代。",
                 [("population", "前后整体判断", "T.PopulationAssessment"), ("right", "变化的权利", "T.Right"), ("evidence", "变更资料", "T.Evidence")],
                 [("changed", "人选或关系实质变化", "T.PopulationAssessment.rights_changed")],
                 ["前后逐人名单与各项权利关系", "转让、委托、任免或信托指定文件及生效日期"],
                 ["逐人核实退出、进入、标准或权利类型、比例、有效时间变化。", "净人数相同或普通经理换岗均不能单独决定是否需更新；未证变更保持UNKNOWN。"],
                 ["T.PopulationAssessment.rights_changed", "T.PopulationAssessment.unknown_reason"],
                 ["RULE.A01.KF.CONTINUOUS"], ["Q.A01.S80", "Q.A01.S82"], "金融机构有权尽调人员"),
    ]


TYPE_IDS = {"T.Party", "T.Right", "T.Arrangement", "T.Role", "T.BeneficiaryScope", "T.Evidence",
            "T.PersonAssessment", "T.PopulationAssessment", "T.BranchAssessment", "T.IdentificationRoute"}


RULE_MODEL_IDS = {
    "RULE.A01.KF.SCOPE": [],
    "RULE.A01.KF.FILING": [],
    "RULE.A01.KF.PROFILE": ["T.PersonAssessment", "T.IdentificationRoute", "J.Route"],
    "RULE.A01.KF.EQUITY": ["T.Party", "T.Right", "T.PersonAssessment", "R.Equity25"],
    "RULE.A01.KF.NOMINEE": ["T.Right", "T.Arrangement", "T.Evidence", "J.RightAttribution"],
    "RULE.A01.KF.RETURNS_VOTES": ["T.Right", "T.PersonAssessment", "R.BenefitVote25"],
    "RULE.A01.KF.CONTROL": ["T.Arrangement", "T.PersonAssessment", "J.ActualControl"],
    "RULE.A01.KF.FALLBACK": ["T.Role", "T.PopulationAssessment", "R.FallbackGate"],
    "RULE.A01.KF.SOE": ["T.Party", "T.Role", "T.PersonAssessment", "R.SoeFiling", "J.Route"],
    "RULE.A01.KF.BRANCHES": ["T.Party", "T.Role", "T.PersonAssessment", "T.BranchAssessment", "J.BranchInclusion"],
    "RULE.A01.KF.TRUST": ["T.Role", "T.BeneficiaryScope", "T.Arrangement", "T.PersonAssessment", "J.Trust"],
    "RULE.A01.KF.TRUST_PRODUCTS": ["T.IdentificationRoute", "J.Route"],
    "RULE.A01.KF.ASSET_PRODUCTS": ["T.IdentificationRoute", "J.Route"],
    "RULE.A01.KF.TRUST_RELIANCE": ["T.Evidence", "J.Evidence"],
    "RULE.A01.KF.EXCEPTIONS": ["T.IdentificationRoute", "J.Route"],
    "RULE.A01.KF.IDENTITY": ["T.Party", "T.Evidence", "T.PersonAssessment", "R.NaturalPerson", "J.Evidence"],
    "RULE.A01.KF.RISK": ["T.IdentificationRoute", "J.Route"],
    "RULE.A01.KF.RISK_ACCEPT": [],
    "RULE.A01.KF.DATES": ["T.Right", "T.Arrangement", "T.Role", "T.PersonAssessment", "J.FormationDate"],
    "RULE.A01.KF.BOMIS": [],
    "RULE.A01.KF.DIFFERENCE": [],
    "RULE.A01.KF.FEEDBACK": [],
    "RULE.A01.KF.SUSPICIOUS": [],
    "RULE.A01.KF.CONTINUOUS": ["T.Right", "T.PersonAssessment", "T.PopulationAssessment", "J.ChangeImpact"],
    "RULE.A01.KF.HISTORICAL": ["T.Right", "T.PersonAssessment", "J.FormationDate"],
    "RULE.A01.KF.EXISTING": [],
    "RULE.A01.KF.GOVERNANCE": ["T.PersonAssessment", "T.Evidence", "J.Evidence"],
}
FACET_NAMES = ("scope", "preconditions", "conditions", "result", "exceptions", "missing_evidence", "effective_period")


def issue_id(knowledge_issue_id):
    return knowledge_issue_id.replace("ISSUE.A01.KF.", "GAP.A01.", 1)


def build_issues(knowledge, audit_by_id, dsl_rules):
    questions = {q["id"] for q in knowledge["content"]["questions"]}
    result, bindings = [], []
    for upstream in knowledge["issues"]:
        affected_sources = {
            rule["id"] for rule in knowledge["content"]["rules"]
            if rule["id"] in upstream["affects"] or set(rule["statement_ids"]) & set(upstream["affects"])
        }
        affected_questions = set(upstream["affects"]) & questions
        for rule in knowledge["content"]["rules"]:
            if rule["id"] in affected_sources:
                affected_questions.update(rule["question_ids"])
        affected_dsl_rules = {rule["id"] for rule in dsl_rules if set(rule["basis_ids"]) & affected_sources}
        while True:
            expanded = affected_dsl_rules | {
                rule["id"] for rule in dsl_rules if set(rule["depends_on"]) & affected_dsl_rules
            }
            if expanded == affected_dsl_rules:
                break
            affected_dsl_rules = expanded
        for rule in dsl_rules:
            if rule["id"] in affected_dsl_rules:
                affected_questions.update(rule["question_ids"])
        affected_core_rules = {
            rule_id for rule_id in affected_sources
            if set(audit_by_id[rule_id]["modeling_classification"]) & {"CORE_STRUCTURE", "DOMAIN_DECISION"}
        }
        model_id = issue_id(upstream["id"])
        affects = [upstream["id"]] + sorted(affected_core_rules) + sorted(affected_questions)
        model_issue = {
            "id": model_id, "kind": "MODEL_GAP", "statement": "上游未决：" + upstream["statement"],
            "affects": affects, "owner": upstream["owner"],
            "recommendation": upstream["recommendation"],
            "until_resolved": upstream["until_resolved"], "status": "OPEN",
        }
        if "severity" in upstream:
            model_issue["severity"] = upstream["severity"]
        result.append(model_issue)
        bindings.append({
            "knowledge_issue_id": upstream["id"], "model_issue_ids": [model_id],
            "handling": "MODEL_LIMITATION" if affected_questions else "DEFERRED",
            "reason": "上游仍为OPEN；" + ("相关问题及核心判断保留缺口。" if affected_questions else "本次无直接问题影响，保留待核而不升格为规范。"),
        })
    return result, bindings


def facet_refs(name, mapped):
    rules = [x for x in mapped if x.startswith("R.")]
    judgments = [x for x in mapped if x.startswith("J.")]
    if "T.BranchAssessment" in mapped and name == "missing_evidence":
        return ["T.BranchAssessment.evidence", "T.BranchAssessment.unknown_reason"], "FORMALIZED"
    if "T.BranchAssessment" in mapped and name == "effective_period":
        return ["T.BranchAssessment.as_of", "T.Role.effective_start", "T.Role.effective_end_bounds"], "FORMALIZED"
    if "J.FormationDate" in mapped and "T.Arrangement" in mapped and name == "effective_period":
        return ["T.Right.formation_bounds", "T.Right.effective_end_bounds",
                "T.Arrangement.formation_bounds", "T.Arrangement.effective_end_bounds",
                "T.Role.formation_bounds", "T.Role.effective_end_bounds"], "FORMALIZED"
    if name == "conditions":
        refs = [x + ".expression" for x in rules] + [x + ".criteria" for x in judgments]
        status = "MIXED" if rules and judgments else "FORMALIZED" if rules else "MANUAL"
        return refs, status
    if name == "exceptions":
        return ([rules[0] + ".on_unknown"] if rules else [judgments[0] + ".criteria"]), "FORMALIZED" if rules else "MANUAL"
    if name == "missing_evidence":
        return ["T.Evidence", "T.PersonAssessment.unknown_reason"], "FORMALIZED"
    if name == "effective_period":
        return ["T.PersonAssessment.as_of", "T.Right.effective_start"], "FORMALIZED"
    if name == "result":
        if rules:
            return [rules[0] + ".result_binding"], "FORMALIZED"
        return [judgments[0]], "FORMALIZED"
    return [mapped[0]], "FORMALIZED"


def build_rule_coverage(knowledge, audit_by_id, model_issues):
    covered = []
    for rule in knowledge["content"]["rules"]:
        rule_id = rule["id"]
        audited = audit_by_id[rule_id]
        classes = audited["modeling_classification"]
        mapped = RULE_MODEL_IDS[rule_id]
        is_core = bool(set(classes) & {"CORE_STRUCTURE", "DOMAIN_DECISION"})
        if bool(mapped) != is_core:
            raise ValueError(f"分类与模型映射不一致: {rule_id}")
        gaps = sorted(issue["id"] for issue in model_issues if rule_id in issue["affects"] and is_core)
        if is_core:
            status = "PARTIAL" if gaps else "MODELED"
            reason = audited["reason"] + " 非充分事实：" + "；".join(rule["non_sufficient_facts"])
            reason += " UNKNOWN：" + rule["unknown_behavior"]
            reason += " 证据要求：" + "；".join(rule["evidence_requirements"])
            reason += " 人工边界：" + rule["human_boundary"]
        else:
            status = "NO_MODEL_CHANGE" if classes == ["NO_MODEL_CHANGE"] else "EXTERNAL_CONTEXT"
            reason = audited["reason"]
        facets = {}
        for name in FACET_NAMES:
            if is_core:
                refs, facet_status = facet_refs(name, mapped)
                explanation = "仅抽取核心事实与判断；完整适用语义及例外以固定知识原文为准。"
            else:
                refs, facet_status = [], "NOT_MODELED"
                explanation = "属于" + ("无模型变化" if status == "NO_MODEL_CHANGE" else "外部上下文") + "；已覆盖知识原文，不为其创建核心对象或流程。"
            facets[name] = {"source_text": rule[name], "model_refs": refs, "explanation": explanation, "status": facet_status}
        covered.append({
            "knowledge_rule_id": rule_id, "question_ids": rule["question_ids"],
            "model_ids": mapped, "status": status, "gap_ids": gaps,
            "facets": facets, "modeling_classification": classes, "reason": reason,
        })
    return covered


def build_question_coverage(knowledge, rule_coverage, model_issues):
    rows = []
    by_rule = {row["knowledge_rule_id"]: row for row in rule_coverage}
    for question in knowledge["content"]["questions"]:
        qid = question["id"]
        rules = [rule for rule in knowledge["content"]["rules"] if qid in rule["question_ids"]]
        cases = [case["id"] for case in knowledge["content"]["cases"] if qid in case["question_ids"]]
        model_ids = list(dict.fromkeys(model_id for rule in rules for model_id in by_rule[rule["id"]]["model_ids"]))
        gaps = sorted(issue["id"] for issue in model_issues if qid in issue["affects"])
        if gaps:
            status = "PARTIAL" if model_ids else "DEFERRED"
        elif model_ids:
            status = "MODELED"
        elif any(by_rule[rule["id"]]["status"] == "EXTERNAL_CONTEXT" for rule in rules):
            status = "EXTERNAL_CONTEXT"
        else:
            status = "NO_MODEL_CHANGE"
        conclusions = list(dict.fromkeys(rule["business_conclusion"] for rule in rules))
        answer = "；".join(conclusions) + "。缺证处理：" + question["unknown_policy"]
        reason = "对应知识规则已逐条分类。" + (
            "核心结构或领域判断由列明模型元素承接；开放事项保留。" if model_ids and gaps else
            "核心结构或领域判断由列明模型元素承接。" if model_ids else
            "该问题仍受上游OPEN影响，本次不造核心模型元素。" if gaps else
            "只作为外部上下文保留。" if status == "EXTERNAL_CONTEXT" else
            "属于操作、期限或治理知识，不改变核心模型。"
        )
        rows.append({
            "question_id": qid, "model_ids": model_ids, "gap_ids": gaps, "status": status,
            "reason": reason, "question": question["question"], "answer": answer,
            "rule_ids": [rule["id"] for rule in rules], "process_ids": [], "case_ids": cases,
        })
    return rows


def build_case_explanations(knowledge, audit_by_id):
    names = {rule["id"]: rule["name"] for rule in knowledge["content"]["rules"]}
    cases = []
    for case in knowledge["content"]["cases"]:
        mapped = list(dict.fromkeys(model_id for rule_id in case["rule_ids"] for model_id in RULE_MODEL_IDS[rule_id]))
        context_only = not mapped
        rationale = "；".join(audit_by_id[rule_id]["reason"] for rule_id in case["rule_ids"])
        explanation = ("此例只检验固定知识的外部责任或时限边界；" if context_only else "此例使用同一套权利、证据、时点和判断结构；") + rationale
        cases.append({
            "case_id": case["id"], "model_ids": mapped, "explanation": explanation,
            "expected": case["expected"], "forbidden": case["forbidden"],
            "status": "CONTEXT_ONLY" if context_only else "EXPLAINED",
            "title": "、".join(names[rule_id] for rule_id in case["rule_ids"]),
            "input_facts": case["input_facts"],
            "steps": [{"model_ids": mapped, "explanation": explanation}],
            "execution": "NOT_EXECUTED", "evaluation_ids": [],
        })
    return cases


def main():
    knowledge_bytes = KNOWLEDGE_PATH.read_bytes()
    knowledge = json.loads(knowledge_bytes)
    audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    if knowledge["contract_version"] != "5.0.0" or knowledge["content_version"] != "2026-09-24.draft.1":
        raise ValueError("固定知识版本改变；停止生成并重新审计")
    if audit["knowledge_ref"]["digest"] != "sha256:" + sha256(knowledge_bytes).hexdigest():
        raise ValueError("逐规则审计与知识字节摘要不一致")
    rule_ids = {rule["id"] for rule in knowledge["content"]["rules"]}
    audit_by_id = {row["id"]: row for row in audit["rules"]}
    if len(audit_by_id) != len(audit["rules"]) or set(audit_by_id) != rule_ids or set(RULE_MODEL_IDS) != rule_ids:
        raise ValueError("全部知识规则必须先唯一分类并逐项映射")
    question_ids = [question["id"] for question in knowledge["content"]["questions"]]
    request = {
        "request_id": "A01.DomainModel.Produce.20260928", "mode": "PRODUCE",
        "scope": "A01受益所有人：固定领域知识5.0.0草案全部问题、规则、案例与OPEN，重新创建最小稳定领域模型。",
        "knowledge": audit["knowledge_ref"], "knowledge_basis": "DRAFT",
        "review_mode": "DEFERRED", "scope_mode": "FULL_BASELINE",
        "question_scope_ids": question_ids,
    }
    types = build_types()
    fields = {item["id"] + "." + member["name"]: member for item in types for member in item["fields"]}
    dsl_rules = build_rules(fields)
    model_issues, bindings = build_issues(knowledge, audit_by_id, dsl_rules)
    rule_coverage = build_rule_coverage(knowledge, audit_by_id, model_issues)
    model = {
        "dsl_version": "2.1.0", "artifact_id": "A01.DomainModel", "content_version": VERSION,
        "name": "A01受益所有人领域模型", "knowledge_ref": audit["knowledge_ref"],
        "knowledge_basis": "DRAFT", "question_scope_ids": question_ids,
        "types": types, "temporal": [], "rules": dsl_rules, "state_machines": [],
        "judgments": build_judgments(fields),
        "question_coverage": build_question_coverage(knowledge, rule_coverage, model_issues),
        "case_explanations": build_case_explanations(knowledge, audit_by_id),
        "upstream_issue_bindings": bindings, "issues": model_issues,
        "scope_mode": "FULL_BASELINE", "constraints": [], "processes": [],
        "rule_coverage": rule_coverage,
    }
    (STAGE / "input.json").write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (STAGE / "model.yaml").write_text(yaml.dump(model, Dumper=NoAliasDumper, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    print(json.dumps({"types": len(types), "rules": len(model["rules"]), "judgments": len(model["judgments"]),
                      "knowledge_rules": len(rule_coverage), "questions": len(question_ids),
                      "cases": len(model["case_explanations"]), "open": len(model_issues)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
