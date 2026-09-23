#!/usr/bin/env python3
"""Build the 2026-09-22 fresh domain-knowledge draft from the existing Structured Document IR."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "A01受益所有人"
WORK = PROJECT / "03领域知识输出" / "process" / "runs" / "2026-09-22.latest"
OUTDIR = PROJECT / "03领域知识输出" / "candidates" / "2026-09-22.latest"
OLD_INPUT = PROJECT / "03领域知识输出" / "input.json"
FRESH_INPUT = WORK / "input.json"
OUTPUT = OUTDIR / "output.json"


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


raw = json.loads(OLD_INPUT.read_text(encoding="utf-8"))
fresh = {
    "request_id": "A01.DomainKnowledge.Request.20260922.Latest",
    "contract_version": "4.0.0",
    "mode": "PRODUCE",
    "scope": "仅依据01业务输入/01制度原文七份材料形成受益所有人领域业务知识；旧知识输出、旧确认、旧规则、旧案例和同业实践不属于本次输入。",
    "business_goal": "形成可由业务人员直接审阅的受益所有人知识草案，明确识别路径、条件、证据、时间、例外、差异反馈和接口边界，并保留未知与待确认事项。",
    "consumers": ["业务负责人", "反洗钱合规人员", "运营核实人员", "需求访谈人员"],
    "sources": raw["sources"],
    "source_units": raw["source_units"],
    "source_extractions": raw["source_extractions"],
}
FRESH_INPUT.write_text(json.dumps(fresh, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

sources = fresh["sources"]
units = {u["unit_id"]: u for u in fresh["source_units"]}
by_source = {s["source_id"]: s for s in sources}


def unit(sid: str, uid: str) -> dict:
    key = f"{sid}.{uid}" if not uid.startswith(f"{sid}.") else uid
    if key not in units:
        raise KeyError(key)
    return units[key]


def basis(sid: str, uid: str) -> str:
    u = unit(sid, uid)
    return f"{u['locator']}；来源单元 {u['unit_id']}。"


statements: list[dict] = []
statement_by_unit: dict[str, str] = {}


def excerpt(sid: str, uid: str) -> str:
    u = unit(sid, uid)
    sid_full = u["unit_id"]
    if sid_full in statement_by_unit:
        return statement_by_unit[sid_full]
    ident = "ST.EX." + sid_full.replace(".", "_")
    statements.append({
        "id": ident,
        "text": "原文摘录：" + u["text"],
        "source_ids": [sid],
        "source_unit_ids": [sid_full],
        "basis": basis(sid, uid),
        "origin": "SOURCE_STATED",
        "meaning_kind": "SOURCE_EXCERPT",
        "review_status": "PENDING",
        "dispute_status": "UNCONTESTED",
        "conflict_ids": [],
    })
    statement_by_unit[sid_full] = ident
    return ident


semantic_specs = [
    ("ST.P01", "SRC02", "U0006", "金融机构识别核实受益所有人必须遵循风险原则，采取与风险程度相匹配的差异化措施。", "CRITERION"),
    ("ST.P02", "SRC02", "U0008", "仅查询受益所有人信息查询管理系统，或用批量、自动化手段代替必要的风险判断和识别核实，不足以履行金融机构的识别义务。", "PROHIBITION"),
    ("ST.P03", "SRC02", "U0014", "标准一：自然人直接或间接最终拥有法人或非法人组织25%以上股权、股份或合伙权益。", "CRITERION"),
    ("ST.P04", "SRC02", "U0015", "标准二：自然人虽未满足股权、股份或合伙权益标准，但最终享有25%以上收益权或表决权。", "CRITERION"),
    ("ST.P05", "SRC02", "U0016", "标准三：自然人虽未满足前两项，但单独或联合对法人或非法人组织实施实际控制；控制方式包括协议、关系密切者、人事任免、重大经营决策、财务收支或长期支配重要资产和主要资金。", "CRITERION"),
    ("ST.P06", "SRC05", "U0042", "备案主体应逐一对照三条识别标准，所有符合标准的自然人均应作为受益所有人备案；只有三条标准均不能确认时，才进入日常经营管理人员兜底路径。", "PROCEDURE"),
    ("ST.P07", "SRC05", "U0044", "多个自然人分别满足不同识别标准时，应并列保留并备案，不能因为已经找到一名受益所有人而停止检查其他标准。", "OBLIGATION"),
    ("ST.P08", "SRC05", "U0047", "多层控股结构需要逐层穿透并计算自然人最终拥有的股权、股份或合伙权益比例；不能只看备案主体的直接登记股东。", "PROCEDURE"),
    ("ST.P09", "SRC05", "U0052", "收益权是股权或合伙权益所产生收益的权利，典型形式包括分红和权益增值；收益权可以与登记股权分离。", "DEFINITION"),
    ("ST.P10", "SRC05", "U0055", "实际控制不以持有股权为必要条件；协议、关系密切者、任免权、重大决策权、财务支配或重要资产和资金支配均可能构成控制事实。", "DEFINITION"),
    ("ST.P11", "SRC05", "U0058", "同一自然人同时享有25%以上表决权并据此实施实际控制时，应同时记录标准二和标准三两种受益所有权关系。", "OBLIGATION"),
    ("ST.P12", "SRC02", "U0017", "国内法人或非法人组织分支机构一般沿用所属主体的受益所有人；外国公司分支机构还应识别所属外国公司的受益所有人以及至少一名高级管理人员。", "CRITERION"),
    ("ST.P13", "SRC03", "U0016", "外国公司在其本国享受的受益所有人申报豁免标准，不适用于中国境内外国公司分支机构的备案判断。", "PROHIBITION"),
    ("ST.P14", "SRC02", "U0037", "信托受益所有人包括委托人、受托人、受益人、监察人（如有）以及对信托实施最终有效控制的其他自然人。", "DEFINITION"),
    ("ST.P15", "SRC02", "U0038", "信托当事人为非自然人时，应逐一、逐层追溯到最终有效控制的自然人；最终有效控制包括处分信托财产、决定投资或分配、变更或终止信托、变更受益人或任免受托人等。", "PROCEDURE"),
    ("ST.P16", "SRC02", "U0025", "金融机构对列举的低风险或特定类型主体，可以在充分评估风险后采取与风险匹配的简化识别措施；简化不是自动适用。", "PERMISSION"),
    ("ST.P17", "SRC05", "U0031", "备案主体承诺免报必须同时满足注册资本或出资额不超过1000万元、股东或合伙人全部为自然人、没有外部自然人控制或获益、没有股权或合伙权益以外的控制或获益四项条件。", "CRITERION"),
    ("ST.P18", "SRC02", "U0078", "无法准确判断非自然人客户是否符合简化或豁免条件，或者客户出现高风险特定情形时，不得采取简化或豁免措施。", "PROHIBITION"),
    ("ST.P19", "SRC02", "U0048", "金融机构应按客户类型留存能够证明所有权、控制权和受益关系的可靠材料；合伙企业至少需要身份文件、合伙协议、合伙人名单、责任承担方式和权益比例等材料。", "EVIDENCE"),
    ("ST.P20", "SRC02", "U0048", "信托材料至少包括信托合同、成立或登记证明（如有）、受益权登记记录（如有）、信托当事人名单以及最终控制自然人信息。", "EVIDENCE"),
    ("ST.P21", "SRC02", "U0053", "受益所有人身份应通过政府公开渠道、外国政府或国际组织官方认证信息核实；无法通过官方渠道核实时，才可用有效身份证明及客户补充资料，并保留核实理由。", "EVIDENCE"),
    ("ST.P22", "SRC03", "U0027", "备案信息应记录受益所有权关系类型及形成、终止日期；股权路径记录权益比例，收益或表决路径记录相应比例，控制路径记录控制方式。", "TIME"),
    ("ST.P23", "SRC05", "U0066", "关系形成日期应反映拥有、控制或最终获益法律关系实际生效的时间；不能用查询日期、备案日期或当前登记状态倒推形成日期。", "TIME"),
    ("ST.P24", "SRC02", "U0072", "业务关系存续期间应持续关注客户整体状况和交易情况；所有权、收益权、表决权或控制权发生可能影响受益所有权的重大变化时，应审核并在必要时更新信息。", "OBLIGATION"),
    ("ST.P25", "SRC02", "U0079", "查询核对发现备案信息错误、不一致或不完整时，应按差异反馈规则处理；查询结果不能替代金融机构自身识别核实。", "OBLIGATION"),
    ("ST.P26", "SRC02", "U0085", "影响受益所有权关系最终认定的人员增减、关键身份要素、权益或控制信息不一致，以及形成或终止时间出现年月差异，属于重大差异。", "CRITERION"),
    ("ST.P27", "SRC02", "U0089", "不影响受益所有权关系最终认定的姓名书写差异或权利状况非重大差异，无需提交差异报告，但仍应保留判断依据。", "EXCEPTION"),
    ("ST.P28", "SRC02", "U0081", "认定差异由金融机构自身识别错误造成时，应更正自身识别；认定为备案信息错误且差异重大时，应在发现之日起30个工作日内提交差异报告并留存理由、确认过程和佐证。", "PROCEDURE"),
    ("ST.P29", "SRC02", "U0092", "客户应备案但尚未备案时，应先沟通提示；客户仍未备案的，金融机构应报送差异报告。经营主体未备案不等于没有受益所有人。", "PROCEDURE"),
    ("ST.P30", "SRC02", "U0093", "差异分析同时发现涉嫌洗钱或恐怖融资犯罪活动时，差异报告和可疑交易报告应分别报送，差异报告不得提及可疑交易报告报送情况。", "PROHIBITION"),
    ("ST.P31", "SRC06", "U0350", "接口流程要求义务机构在查询前先完成核验；核验流水号有有效期，经营主体未备案时不能直接查询。", "PROCEDURE"),
    ("ST.P32", "SRC06", "U0928", "接口核验结果代码cons表示核验一致、inco表示核验不一致、unrg表示经营主体未备案；这些代码描述系统结果，不直接裁定受益所有人实体结论。", "DEFINITION"),
    ("ST.P33", "SRC06", "U1778", "接口把经营主体未备案作为报文错误或业务状态处理；该状态只能说明系统中没有可供查询的备案主体记录，不能证明不存在受益所有人。", "CONTEXT"),
    ("ST.P34", "SRC03", "U0028", "国家机关、金融机构和特定非金融机构可依法查询受益所有人信息，但对依法获得的信息负有保密义务。", "OBLIGATION"),
    ("ST.P35", "SRC02", "U0034", "国有参股公司识别受益所有人时可以不再识别国有资本部分的受益所有人；这不等于所有国有参股主体都可以直接把法定代表人作为受益所有人。", "EXCEPTION"),
    ("ST.P36", "SRC01", "U0008", "国资交易规章中的国有及国有控股企业、国有实际控制企业定义服务于国有资产交易监管，不能单独替代受益所有人制度对主体资格和控制事实的判断。", "CONTEXT"),
]

conflict_statement_ids = {"ST.P32", "ST.P33"}
for sid, src, uid, text, kind in semantic_specs:
    support = [excerpt(src, uid)]
    statements.append({
        "id": sid,
        "text": text,
        "source_ids": [src],
        "source_unit_ids": [unit(src, uid)["unit_id"]],
        "basis": basis(src, uid),
        "origin": "INFERRED" if sid not in {"ST.P03", "ST.P04", "ST.P05", "ST.P14", "ST.P16", "ST.P17", "ST.P22", "ST.P26", "ST.P27", "ST.P28", "ST.P29", "ST.P30", "ST.P32", "ST.P34"} else "SOURCE_STATED",
        "meaning_kind": kind,
        "review_status": "PENDING",
        "dispute_status": "OPEN" if sid in conflict_statement_ids else "UNCONTESTED",
        "conflict_ids": ["K.CONFLICT.INTERFACE_RELATION_RESULT"] if sid in conflict_statement_ids else [],
        "supporting_statement_ids": support,
    })

S = {s["id"]: s for s in statements}

terms = [
    ("TERM.BENEFICIAL_OWNER", "受益所有人", "符合至少一条法定识别路径的自然人；备案和金融机构客户识别分别有对应适用范围。", ["最终受益人"], ["ST.P03", "ST.P04", "ST.P05"], "受益所有人不是系统返回结果的同义词；查询、备案和金融机构识别是不同环节。"),
    ("TERM.OWNERSHIP_PATH", "股权/股份/合伙权益路径", "自然人直接或间接最终拥有主体25%以上股权、股份或合伙权益的识别路径。", ["标准一"], ["ST.P03", "ST.P08"], "直接登记比例与最终穿透比例不是同一事实。"),
    ("TERM.BENEFIT_RIGHT", "收益权", "取得股权或合伙权益收益的权利，包括分红、权益增值等典型收益。", [], ["ST.P04", "ST.P09"], "收益权可与登记股权分离，不能用登记持股替代。"),
    ("TERM.VOTING_RIGHT", "表决权", "对主体决策表达和形成表决结果的权利，可因协议等安排与股权分离。", [], ["ST.P04", "ST.P11"], "表决权比例和股权比例需要分别取证。"),
    ("TERM.ACTUAL_CONTROL", "实际控制", "单独或联合决定人事、重大经营管理、财务收支或长期支配重要资产和主要资金等控制事实。", ["标准三"], ["ST.P05", "ST.P10"], "法定代表人身份本身不等于实际控制证据。"),
    ("TERM.FALLBACK_MANAGER", "日常经营管理人员兜底", "三条识别标准均不能确认自然人时，才使用日常经营管理人员作为兜底识别对象。", [], ["ST.P06"], "缺少股权或控制证据不能直接触发兜底。"),
    ("TERM.TRUST_PARTY", "信托当事人", "委托人、受托人、受益人、监察人（如有）及最终有效控制自然人构成信托识别范围。", [], ["ST.P14", "ST.P15"], "信托不能套用普通公司股东路径。"),
    ("TERM.SIMPLIFIED", "简化识别", "在风险充分评估且满足特定主体或产品条件时采取的与风险匹配的较简识别措施。", [], ["ST.P16", "ST.P18"], "简化不是免除识别，也不是自动选项。"),
    ("TERM.EXEMPTION", "承诺免报/豁免", "在规定条件全部满足且无相反高风险事实时，允许不另行备案或免除特定识别步骤的制度安排。", [], ["ST.P17", "ST.P18"], "豁免条件无法准确判断时不得适用。"),
    ("TERM.FORMATION_DATE", "受益所有权关系形成日期", "拥有、控制或最终获益法律关系实际生效的日期。", [], ["ST.P22", "ST.P23"], "查询日期、备案日期和形成日期不能混用。"),
    ("TERM.MATERIAL_DIFFERENCE", "重大差异", "足以影响受益所有权关系最终认定的人员、身份、权利状况或形成/终止时间差异。", [], ["ST.P26", "ST.P28"], "年月差异在影响关系认定时即可能重大。"),
    ("TERM.NON_MATERIAL_DIFFERENCE", "非重大差异", "不影响受益所有权关系最终认定的书写或权利状况差异。", [], ["ST.P27"], "非重大不等于无需留痕或无需核实。"),
    ("TERM.UNREGISTERED", "经营主体未备案", "系统查询不到备案主体记录的系统状态。", [], ["ST.P29", "ST.P32", "ST.P33"], "不等于没有受益所有人。"),
    ("TERM.VERIFICATION_RESULT", "核验结果", "系统对比返回的一致、不一致或未备案状态，不替代业务识别判断。", ["cons/inco/unrg"], ["ST.P25", "ST.P32"], "接口代码属于系统事实，实体结论需要业务核实。"),
    ("TERM.SOURCE_AUTHORITY", "来源层级", "规范、操作指南、系统接口和案例事实在业务知识中的不同证明效力。", [], ["ST.P34", "ST.P36"], "接口和地方指南不能扩大上位制度。"),
]
term_objs = [
    {"id": i, "name": n, "definition": d, "aliases": a, "statement_ids": ss, "distinctions": x}
    for i, n, d, a, ss, x in terms
]

question_specs = [
    ("Q01", "哪些自然人符合受益所有人识别标准？", "三条识别路径", "合规人员", "确定完整受益所有人集合", "证据不足时保留未决，不把未知改写为否。"),
    ("Q02", "如何计算直接和间接股权、股份或合伙权益？", "所有权穿透", "核实人员", "形成比例计算底稿", "缺少任一层结构时标记证据不足。"),
    ("Q03", "收益权或表决权与登记股权分离时如何识别？", "收益权与表决权", "合规人员", "判断标准二及其证据", "没有有效协议或权益证明时不能推定。"),
    ("Q04", "哪些事实构成单独或联合实际控制？", "实际控制", "合规人员", "判断标准三及控制方式", "法定代表人身份不单独构成控制结论。"),
    ("Q05", "何时可以使用日常经营管理人员兜底？", "兜底路径", "备案人员", "决定是否进入兜底", "必须先记录三条标准均未确认。"),
    ("Q06", "外国公司分支机构和国内分支机构如何处理？", "特殊主体", "备案人员", "确定分支机构识别范围", "外国法上的豁免不能直接沿用。"),
    ("Q07", "信托应识别哪些当事人和最终控制人？", "信托", "金融机构", "确定信托识别对象及证据", "非自然人当事人必须逐层追溯。"),
    ("Q08", "哪些主体可以简化识别或承诺免报？", "简化与豁免", "合规人员", "决定简化/豁免是否可用", "无法准确判断或高风险时禁止适用。"),
    ("Q09", "识别和核实需要哪些证据？", "证据与核实", "核实人员", "建立证据链", "来源不可靠或无法相互印证时保持部分状态。"),
    ("Q10", "备案需要记录哪些身份、关系和比例信息？", "备案字段", "备案人员", "形成完整备案记录", "字段缺失不能补猜。"),
    ("Q11", "如何确定关系形成和终止日期？", "时间语义", "合规人员", "判断关系期间和更新时点", "没有生效文件时保留日期缺口。"),
    ("Q12", "什么变化会触发持续关注和信息更新？", "持续义务", "金融机构", "决定复核和更新", "仅凭系统字段变化不能判断业务重大性。"),
    ("Q13", "何时属于重大差异，何时属于非重大差异？", "差异分类", "差异处理人员", "选择反馈路径", "影响关系认定的差异不能按格式问题处理。"),
    ("Q14", "差异由金融机构识别错误还是备案错误造成时怎么办？", "差异归因", "差异处理人员", "决定更正或提交报告", "归因未核实前不得直接归责。"),
    ("Q15", "客户应备案但未备案时可以得出什么结论？", "未备案", "金融机构", "提示客户并决定是否报告", "未备案不等于没有受益所有人。"),
    ("Q16", "查询、核验和差异报告的接口状态分别表示什么？", "系统接口", "接口运营人员", "解释报文结果", "接口代码不直接替代实体识别。"),
    ("Q17", "国有独资、国有控股和国有参股情形如何区分？", "国有主体", "合规人员", "选择特殊识别路径", "需先证明主体资格，不能由法定代表人反推。"),
    ("Q18", "地方指南、接口规范与部门规章冲突时如何处理？", "来源层级", "领域负责人", "决定采用的业务口径", "保留冲突并提交责任人裁定。"),
]
questions = [
    {"id": i, "question": q, "topic": t, "consumer": c, "decision_use": u, "unknown_policy": p}
    for i, q, t, c, u, p in question_specs
]

rules = [
    ("R01", "三路径并列识别", ["ST.P03", "ST.P04", "ST.P05", "ST.P06", "ST.P07"], ["Q01"], "所有法人和非法人组织的受益所有人识别", "先收集所有权、收益权、表决权和控制权事实，再逐项检查三条标准。", "满足任一标准的自然人均纳入；同一人可同时满足多条标准。", "三条标准均不能确认时才可进入日常经营管理人员兜底。", "无法证明的路径保持证据不足。", "持续适用；具体备案/金融机构场景分别按对应规范。", "2024年第3号令第6条、2025年第12号令第8条及备案指南2.1.1-2.1.2。"),
    ("R02", "间接权益必须穿透计算", ["ST.P03", "ST.P08"], ["Q02"], "存在一层以上法人或合伙企业持有关系的主体", "取得每一层股权或合伙权益比例及主体身份。", "逐层计算自然人最终拥有比例，达到25%以上时进入标准一。", "任一层缺失时不得按直接登记比例作完整结论。", "控制协议可能使收益权或控制权另行适用标准二、三。", "关系实际生效期间。", "金融机构客户识别办法第8条、备案指南3.1。"),
    ("R03", "收益权与表决权单独判断", ["ST.P04", "ST.P09", "ST.P11"], ["Q03"], "登记股权与收益或表决安排分离的主体", "取得分红、增值、表决或代理安排的有效文件。", "最终享有25%以上收益权或表决权即可满足标准二；同时控制的需并列记录标准三。", "没有生效协议、收益安排或表决证据时不得推定比例。", "标准一已满足时仍应记录已发现的其他事实关系，不能删掉并列关系。", "以权利安排生效、终止时间为准。", "2024年第3号令第6条、备案指南3.2.1和3.2.3。"),
    ("R04", "实际控制需要控制事实", ["ST.P05", "ST.P10"], ["Q04"], "股权比例不足或没有股权但存在控制安排的主体", "核实协议、人事任免、重大经营决策、财务、资产和资金支配事实。", "能证明单独或联合控制即可满足标准三。", "仅有法定代表人、董事或高管身份不够。", "联合控制需要说明共同控制主体和依据。", "控制安排生效至终止期间。", "2025年第12号令第8条、备案指南3.2.2。"),
    ("R05", "兜底路径受三标准穷尽约束", ["ST.P06"], ["Q05"], "三条标准均无法确认自然人的主体", "保存三条路径核查结果和缺证说明。", "确认不存在标准一、二、三后，才将负责日常经营管理人员作为兜底对象。", "缺资料不能直接等同于不存在三条路径。", "未来取得新证据时应重新识别。", "当前核查时点；更新后重新判断。", "备案指南2.1.2及深圳指引中的流程说明。"),
    ("R06", "分支机构按主体类型处理", ["ST.P12", "ST.P13"], ["Q06"], "国内法人分支和外国公司分支", "取得所属主体受益所有人和外国分支高级管理人员资料。", "国内分支一般沿用所属主体；外国分支还需至少一名高级管理人员。", "不能援引外国法豁免替代中国备案要求。", "所属主体识别结论变化时分支结果随之复核。", "分支关系存续期间。", "2025年第12号令第9条、2024年第3号令第8条。"),
    ("R07", "信托单列识别路径", ["ST.P14", "ST.P15", "ST.P20"], ["Q07"], "民事信托、财富管理信托、公益慈善信托和其他信托", "取得合同、登记、受益权和当事人控制资料。", "识别委托人、受托人、受益人、监察人及最终有效控制自然人。", "非自然人当事人缺少逐层控制资料时保持未决。", "资产管理产品按产品规则参照第八条，不能反向套用普通信托规则。", "信托设立、生效、变更和终止期间。", "2025年第12号令第12-15条、第17条。"),
    ("R08", "简化或免报必须先满足条件", ["ST.P16", "ST.P17", "ST.P18"], ["Q08"], "金融机构低风险客户和备案承诺免报主体", "核实主体类型、资本、股东/合伙人、外部控制或获益及风险状态。", "全部条件满足且无高风险事实时，才可适用对应简化或免报。", "无法准确判断或出现高风险时禁止简化/豁免。", "简化、免报和完全不识别不是同一概念。", "以客户/备案判断时点和后续风险变化为准。", "2025年第12号令第11、20、25条；备案指南1.2。"),
    ("R09", "证据需要相互印证", ["ST.P19", "ST.P20", "ST.P21"], ["Q09"], "所有受益所有人识别和核实任务", "根据主体类型取得登记、协议、名册、身份和控制资料。", "来源可靠且相互印证后，才能形成身份和权利状况结论。", "证据不足时标记 insufficient_evidence，不得填空或猜测。", "官方核实不可得时使用替代材料需说明理由。", "识别时点及持续更新时点。", "2025年第12号令第16-19条。"),
    ("R10", "备案字段承接关系事实", ["ST.P22", "ST.P23"], ["Q10", "Q11"], "备案主体向系统填报受益所有人", "取得身份、关系类型、比例/控制方式和形成终止日期。", "根据实际关系类型填写对应字段，不以当前登记或查询日期代替形成日期。", "缺少生效文件时保留日期缺口。", "终止日期如无应明确长期或未知的制度口径。", "关系实际期间。", "2024年第3号令第11条、备案指南5.1和5.3。"),
    ("R11", "重大变化触发持续复核", ["ST.P24"], ["Q12"], "金融机构业务关系存续期间", "持续关注所有权、控制权、交易和风险变化。", "可能影响受益所有权的重大变化触发审核并在必要时更新。", "仅系统字段变化而没有业务影响时不能自动判定重大。", "与高风险情形同时出现时适用加强措施。", "业务关系存续期间持续适用。", "2025年第12号令第24条。"),
    ("R12", "差异按影响程度分类", ["ST.P25", "ST.P26", "ST.P27"], ["Q13"], "金融机构识别结果与备案信息核对", "比较人员集合、关键身份、权益/控制信息和形成终止时间。", "影响关系最终认定的属于重大差异；不影响最终认定的为非重大差异。", "年月差异需结合是否影响关系认定判断。", "金融机构采用更严格标准造成的小于25%差异另按制度处理。", "发现差异时点及报告期限。", "2025年第12号令第26-29条。"),
    ("R13", "差异归因决定动作", ["ST.P28"], ["Q14"], "已发现重大或非重大差异", "与客户沟通并核实差异来源。", "自身识别错误则更正；备案错误且重大则30个工作日内提交差异报告。", "归因不清时不得直接提交带有错误事实的报告。", "重大差异可在风险可控下先建立或维持关系，但仍需完成报告义务。", "发现之日起30个工作日。", "2025年第12号令第27条。"),
    ("R14", "未备案先提示后报告", ["ST.P29"], ["Q15"], "客户应备案但系统无备案记录", "确认主体依法应备案并与客户沟通。", "客户仍未备案时提交差异报告。", "未备案只能说明缺少系统记录，不能得出无受益所有人结论。", "若系统状态与实际主体资料矛盾，先核实主体身份。", "发现未备案时。", "2025年第12号令第30条及接口规范。"),
    ("R15", "接口状态不等于实体结论", ["ST.P31", "ST.P32", "ST.P33"], ["Q16"], "核验、查询和差异报告接口", "先取得有效核验流水，再解释cons/inco/unrg。", "cons表示系统核验一致，inco表示存在不一致，unrg表示系统未找到备案主体。", "任何接口状态都不能替代业务识别和风险判断。", "流水失效、主体未备案和数据缺失按接口错误规则分开处理。", "按接口流水有效期和报文时点。", "接口规范V2.0；实体认定仍以两部规章为准。"),
    ("R16", "国有情形先证主体资格", ["ST.P35", "ST.P36"], ["Q17"], "国有独资、国有控股和国有参股主体", "取得国有资本比例、控股/实际控制资格和官方证明。", "国有参股可不识别国有资本部分；特殊法定代表人路径须满足对应制度主体条件。", "法定代表人、国资交易材料或系统标签不能单独证明国有主体资格。", "国资交易监管定义不自动改变受益所有人识别规则。", "主体资格和控制事实有效期间。", "2024年第3号令第7条、2025年第12号令第11条及第32号令第4条。"),
    ("R17", "来源层级冲突保留", ["ST.P32", "ST.P33", "ST.P36"], ["Q18"], "规范、指南与系统接口出现表述差异", "标记每条来源的authority和source_role。", "部门规章定义实体规则；指南解释办理；接口描述系统状态；冲突提交责任人裁定。", "未裁定前不得用低层级材料覆盖高层级规则。", "接口字段互斥不代表业务关系事实只能保留一条，需补充数据字典确认。", "以具体版本和生效日期为准。", "来源层级和本次材料的适用边界。"),
]
rule_objs = []
for rid, name, sids, qids, scope, pre, cond, result, exc, period, authority in rules:
    rule_objs.append({"id": rid, "name": name, "statement_ids": sids, "question_ids": qids, "scope": scope, "preconditions": pre, "conditions": cond, "result": result, "exceptions": exc, "missing_evidence": "相关证据缺失时保留证据不足状态，不以空值或猜测补全。", "effective_period": period, "authority": authority, "origin": "INFERRED", "review_status": "PENDING", "dispute_status": "OPEN" if rid in {"R15", "R17"} else "UNCONTESTED", "conflict_ids": ["K.CONFLICT.INTERFACE_RELATION_RESULT"] if rid in {"R15", "R17"} else []})

issues = [
    {"id": "K.GAP.SOURCE_REVIEW", "kind": "KNOWLEDGE_GAP", "statement": "2456个来源单元中，只有与核心业务主题直接相关的单元完成了本轮语义回读，其余实质性单元仍需逐单元审查。", "affects": [], "owner": "领域知识责任人", "recommendation": "按来源和章节继续回读并补充语义陈述、规则和问题去向。", "until_resolved": "本版本只能作为部分完成草案，不能宣称全量知识完成。", "status": "OPEN", "severity": "HIGH"},
    {"id": "K.GAP.SUBJECT_EVIDENCE", "kind": "KNOWLEDGE_GAP", "statement": "本次材料不包含具体客户主体、股权链、控制协议、身份材料或形成日期证据，不能输出个案受益所有人结论。", "affects": ["Q01", "Q02", "Q03", "Q04", "Q05", "Q06", "Q07", "Q09", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q17"], "owner": "业务责任人", "recommendation": "提供目标主体的登记资料、全层权益、协议、身份和日期化证据。", "until_resolved": "所有个案判断保持 insufficient_evidence。", "status": "OPEN", "severity": "HIGH"},
    {"id": "K.GAP.INSTITUTION_POLICY", "kind": "KNOWLEDGE_GAP", "statement": "材料没有给出本机构风险评级、复核周期、差异归因和报告审批口径。", "affects": ["Q08", "Q12", "Q13", "Q14", "Q15"], "owner": "反洗钱合规负责人", "recommendation": "补充机构内部政策、岗位责任和时限配置。", "until_resolved": "只交付法规和材料层规则，不推断机构内部作业口径。", "status": "OPEN", "severity": "MEDIUM"},
    {"id": "K.CONFLICT.INTERFACE_RELATION_RESULT", "kind": "CONFLICT", "statement": "接口规范中关系类型字段存在互斥描述，而指南要求同一自然人可同时保留标准二和标准三关系；需确认字段约束与业务事实是否为不同层次。", "affects": ["ST.P32", "ST.P33", "R15", "R17"], "owner": "接口与合规联合责任人", "recommendation": "取得当前数据字典、接口验收规则和样例，确认字段互斥是否仅针对单次报文值。", "until_resolved": "不得删除并列业务关系；系统映射保持待确认。", "status": "OPEN", "severity": "HIGH"},
    {"id": "K.GAP.INTERFACE_CONFIRMATION", "kind": "KNOWLEDGE_GAP", "statement": "接口关系类型字段的当前数据字典、互斥约束和报文验收样例尚未取得。", "affects": ["Q18", "CAND.OPEN.INTERFACE"], "owner": "接口与合规联合责任人", "recommendation": "补充当前版本数据字典、报文样例和验收规则。", "until_resolved": "保留业务层并列关系，不把接口单值限制当作实体规则。", "status": "OPEN", "severity": "HIGH"},
    {"id": "K.GAP.REAL_CASES", "kind": "KNOWLEDGE_GAP", "statement": "本次输入没有经业务确认的真实案例，案例仅用于边界演示。", "affects": [q[0] for q in question_specs], "owner": "业务专家", "recommendation": "补充脱敏真实案例并记录事实、证据和结果。", "until_resolved": "不得用合成案例证明规则已被业务验证。", "status": "OPEN", "severity": "MEDIUM"},
]

questions_by_id = {q["id"]: q for q in questions}

case_templates = [
    ("Q01", "POSITIVE", ["主体存在自然人甲直接持有30%股权、乙享有25%收益权、丙通过协议控制重大经营决策。"], "甲、乙、丙均进入受益所有人识别结果，并分别记录对应关系类型。", "不得只保留持股最高的甲。", ["SRC02", "SRC05"]),
    ("Q02", "BOUNDARY", ["自然人甲持有中间公司60%，中间公司持有目标公司50%；另一层公司的登记资料缺失。"], "已知链条可计算部分需保留，但不能对完整最终比例作确定结论。", "不得把甲直接写成最终25%以上而忽略缺失层。", ["SRC02", "SRC05"]),
    ("Q03", "POSITIVE", ["自然人乙无登记股权，但协议使其取得目标公司30%分红权。"], "乙可能满足标准二，需以有效协议和生效日期核实。", "不得因为乙不是登记股东就排除。", ["SRC02", "SRC05"]),
    ("Q04", "POSITIVE", ["自然人丙持股10%，但有协议任免执行事务合伙人并决定重大投资。"], "丙可能满足标准三，需核实协议效力和实际执行。", "不得仅按10%持股否定控制。", ["SRC02", "SRC05"]),
    ("Q05", "MISSING_EVIDENCE", ["已取得股东名册，但没有完整控制协议和收益安排材料。"], "不能直接启用日常经营管理人员兜底；先列证据缺口。", "不得把法定代表人直接填成兜底对象。", ["SRC05"]),
    ("Q06", "BOUNDARY", ["外国公司分支机构所属外国公司在当地享有豁免，但中国分支存在一名高级管理人员。"], "按中国规则识别所属外国公司受益所有人并纳入至少一名高级管理人员。", "不得直接沿用外国法豁免。", ["SRC02", "SRC03"]),
    ("Q07", "POSITIVE", ["信托委托人为公司，受托人为自然人，受益人为自然人，另有监察人。"], "识别全部信托当事人，并穿透公司委托人至最终控制自然人。", "不得只识别受益人。", ["SRC02"]),
    ("Q08", "NEGATIVE", ["主体资本超过1000万元，股东全部为自然人，但存在股东之外的协议控制人。"], "不满足承诺免报条件，不能适用免报。", "不得因股东全部为自然人而直接免报。", ["SRC02", "SRC05"]),
    ("Q09", "MISSING_EVIDENCE", ["只有系统查询回执，没有合伙协议、合伙人名单和身份佐证。"], "证据不足，不能完成可靠识别。", "不得把查询回执当作完整证据链。", ["SRC02"]),
    ("Q10", "POSITIVE", ["自然人甲满足标准一，形成日期由股权转让协议生效日确定。"], "填报标准一、权益比例和实际形成日期，终止日期按事实填写。", "不得用备案提交日替代形成日期。", ["SRC03", "SRC05"]),
    ("Q11", "BOUNDARY", ["协议签署日为2025-01-01，生效条件于2025-02-15满足。"], "形成日期应以法律关系实际生效日为准，除非材料证明签署即生效。", "不得机械使用签署日。", ["SRC03", "SRC05"]),
    ("Q12", "POSITIVE", ["客户控制权发生重大变化且交易风险上升。"], "触发持续关注、审核和必要的信息更新。", "不得等年度复核才处理。", ["SRC02"]),
    ("Q13", "BOUNDARY", ["系统比例从30%变为20%，并导致标准一是否成立发生变化。"], "属于可能影响关系认定的重大差异，应按重大差异流程核实。", "不得按普通格式差异关闭。", ["SRC02"]),
    ("Q14", "MISSING_EVIDENCE", ["金融机构记录与备案记录不一致，但尚未与客户核实来源。"], "先沟通、核实并归因，不能直接判定由任一方错误造成。", "不得未经核实提交归责结论。", ["SRC02"]),
    ("Q15", "NEGATIVE", ["系统返回unrg，客户仍未提供备案证明。"], "确认依法应备案后先提示客户，仍未备案再报送差异报告；不能认定无受益所有人。", "不得把unrg解释为不存在受益所有人。", ["SRC02", "SRC06"]),
    ("Q16", "POSITIVE", ["核验返回cons，但金融机构掌握的控制协议显示人员发生变化。"], "cons只表示系统核验一致，仍需按自身识别和持续关注义务复核。", "不得以cons终止业务判断。", ["SRC02", "SRC06"]),
    ("Q17", "MISSING_EVIDENCE", ["企业自称国有控股，但没有官方持股和控制证明。"], "不能直接适用国有主体特殊路径；先补主体资格证据。", "不得以法定代表人身份或系统标签证明国有资格。", ["SRC01", "SRC02"]),
    ("Q18", "BOUNDARY", ["接口字段要求单值关系类型，指南记录显示同一人同时满足标准二和三。"], "保留两种业务关系事实，接口互斥约束作为开放冲突处理。", "不得为适配字段而删除一条关系。", ["SRC05", "SRC06"]),
]
cases = []
for idx, (qid, kind, facts, expected, forbidden, sids) in enumerate(case_templates, 1):
    cases.append({"id": f"CASE.{idx:02d}", "question_ids": [qid], "kind": kind, "input_facts": facts, "expected": expected, "forbidden": forbidden, "source_ids": sids, "synthetic": True, "reasoning": "这是用于验证规则边界的合成教学案例，不代表具体客户事实。改变关键事实后应重新判断。"})

case_by_q = {c["question_ids"][0]: c["id"] for c in cases}

candidate_units = {
    "Q01": ["SRC02.U0014", "SRC02.U0015", "SRC02.U0016", "SRC05.U0042"],
    "Q02": ["SRC05.U0047"], "Q03": ["SRC05.U0052"], "Q04": ["SRC05.U0055"], "Q05": ["SRC05.U0042"],
    "Q06": ["SRC02.U0017", "SRC03.U0016"], "Q07": ["SRC02.U0037", "SRC02.U0038"],
    "Q08": ["SRC02.U0025", "SRC02.U0078", "SRC05.U0031"], "Q09": ["SRC02.U0048", "SRC02.U0053"],
    "Q10": ["SRC03.U0027", "SRC05.U0066"], "Q11": ["SRC05.U0066"], "Q12": ["SRC02.U0072"],
    "Q13": ["SRC02.U0085", "SRC02.U0089"], "Q14": ["SRC02.U0081"],
    "Q15": ["SRC02.U0092", "SRC06.U0928"], "Q16": ["SRC06.U0350", "SRC06.U0928", "SRC06.U1778"],
    "Q17": ["SRC02.U0034", "SRC01.U0008"], "Q18": ["SRC06.U0928", "SRC05.U0058"],
}

question_discovery = {
    "scope_question_ids": [q["id"] for q in questions],
    "candidates": [],
    "process_checks": [],
}
for q in questions:
    question_discovery["candidates"].append({"id": "CAND." + q["id"], "question": q["question"], "origin": "PROCESS" if q["id"] in {"Q09", "Q12", "Q14", "Q16"} else "SOURCE", "source_unit_ids": candidate_units[q["id"]], "disposition": "RETAINED", "target_question_ids": [q["id"]], "reason": "由制度含义和办理/核验流程共同保留，作为知识覆盖轴。", "issue_ids": []})
question_discovery["candidates"].extend([
    {"id": "CAND.MERGE.PATH", "question": "是否应把股权、收益权、表决权、控制权拆成四个互斥问题？", "origin": "SOURCE", "source_unit_ids": ["SRC02.U0014", "SRC02.U0015", "SRC02.U0016"], "disposition": "MERGED", "target_question_ids": ["Q01", "Q03", "Q04"], "reason": "三条法定标准是并列路径，收益权与表决权在同一标准中共同检查，不另造重复总问题。", "issue_ids": []},
    {"id": "CAND.OPEN.INSTITUTION", "question": "机构内部风险评级、复核周期和差异审批由谁负责？", "origin": "PROCESS", "source_unit_ids": ["SRC02.U0072", "SRC02.U0081"], "disposition": "OPEN", "target_question_ids": [], "reason": "制度规定持续义务和报告要求，但未给出本机构岗位和配置。", "issue_ids": ["K.GAP.INSTITUTION_POLICY"]},
    {"id": "CAND.OPEN.INTERFACE", "question": "接口关系类型字段的互斥约束是否只针对单次报文值？", "origin": "PROCESS", "source_unit_ids": ["SRC06.U0928", "SRC05.U0058"], "disposition": "OPEN", "target_question_ids": [], "reason": "系统字段与业务关系并列记录之间存在待裁定的层次差异。", "issue_ids": ["K.GAP.INTERFACE_CONFIRMATION"]},
])
question_discovery["process_checks"] = [
    {"id": "PC01", "actor": "备案人员", "stage": "主体分类", "concern": "是否先区分公司、合伙企业、外国公司分支、国有主体和免报主体？", "source_unit_ids": ["SRC05.U0004", "SRC07.U0034", "SRC07.U0095"], "question_ids": ["Q06", "Q08", "Q17"], "status": "COVERED", "reason": "指南和地方指引给出入口分类，但主体资格仍需证据。", "issue_ids": []},
    {"id": "PC02", "actor": "核实人员", "stage": "识别核实", "concern": "是否按三条标准逐一核查并收集对应证据？", "source_unit_ids": ["SRC05.U0042", "SRC02.U0042"], "question_ids": ["Q01", "Q09"], "status": "COVERED", "reason": "制度和指南均要求逐条识别及可靠证据。", "issue_ids": []},
    {"id": "PC03", "actor": "差异处理人员", "stage": "差异反馈", "concern": "是否先沟通、核实、归因，再决定更正或报告？", "source_unit_ids": ["SRC02.U0081", "SRC02.U0092"], "question_ids": ["Q13", "Q14", "Q15"], "status": "COVERED", "reason": "差异章节明确沟通、核实、归因和报告路径。", "issue_ids": []},
    {"id": "PC04", "actor": "机构合规负责人", "stage": "机构作业", "concern": "风险评级、审批、复核周期和留痕责任如何落地？", "source_unit_ids": ["SRC02.U0072", "SRC02.U0081"], "question_ids": ["Q08", "Q12", "Q14"], "status": "GAP", "reason": "现有材料未给出本机构的岗位和配置。", "issue_ids": ["K.GAP.INSTITUTION_POLICY"]},
]

selected_units = set()
for ids in candidate_units.values():
    selected_units.update(ids)
for s in statements:
    selected_units.update(s["source_unit_ids"])

rule_by_q = {}
for r in rule_objs:
    for qid in r["question_ids"]:
        rule_by_q.setdefault(qid, []).append(r["id"])
term_by_statement = {}
for t in term_objs:
    for sid in t["statement_ids"]:
        term_by_statement.setdefault(sid, []).append(t["id"])

coverage = []
for uid, u in units.items():
    pcid = "PCOV." + uid.replace(".", "_")
    if uid in selected_units:
        sids = [s["id"] for s in statements if uid in s["source_unit_ids"] and s["meaning_kind"] != "SOURCE_EXCERPT"]
        stids = [s["id"] for s in statements if uid in s["source_unit_ids"]]
        qids = [q["id"] for q in questions if uid in sum((candidate_units[q["id"]] for q in questions), [])]
        rids = [r["id"] for r in rule_objs if set(r["question_ids"]).intersection(qids)]
        cids = [c["id"] for c in cases if set(c["question_ids"]).intersection(qids)]
        coverage.append({"id": pcid, "source_unit_id": uid, "status": "COVERED", "meaning_status": "REVIEWED", "meaning_note": "已回读并拆解为来源陈述和业务语义；仍需业务责任人审阅。", "business_topic": "；".join(sorted({questions_by_id[q]["topic"] for q in qids})) or "核心制度语义", "business_meaning": "已形成可追溯的业务含义陈述。", "applicability": "按来源角色和具体主体类型判断。", "statement_ids": stids, "term_ids": sorted({tid for sid in stids for tid in term_by_statement.get(sid, [])}), "question_ids": qids, "rule_ids": rids, "case_ids": cids, "issue_ids": [], "reason": "源单元被纳入本轮核心业务主题语义回读。"})
    elif u.get("kind") in {"PREAMBLE", "HEADER", "FOOTER", "PAGE_NUMBER"} or not u.get("text", "").strip() or u.get("text", "").startswith(("首页", "目录", "网站地图")):
        coverage.append({"id": pcid, "source_unit_id": uid, "status": "OUT_OF_SCOPE", "meaning_status": "NOT_APPLICABLE", "meaning_note": "网页导航、页眉页脚、目录或非业务正文。", "business_topic": "范围外材料", "business_meaning": "不形成本领域业务规则。", "applicability": "不适用", "statement_ids": [], "term_ids": [], "question_ids": [], "rule_ids": [], "case_ids": [], "issue_ids": [], "reason": "仅作为文档结构或导航信息保留，不进入业务语义范围。"})
    else:
        coverage.append({"id": pcid, "source_unit_id": uid, "status": "PARTIAL", "meaning_status": "NOT_REVIEWED", "meaning_note": "本轮未完成该源单元的逐单元语义回读。", "business_topic": "待审材料", "business_meaning": "尚未形成可交付业务含义。", "applicability": "待审", "statement_ids": [], "term_ids": [], "question_ids": [], "rule_ids": [], "case_ids": [], "issue_ids": ["K.GAP.SOURCE_REVIEW"], "reason": "保留原始覆盖记录，等待下一轮语义审查。"})

partial_ids = [row["id"] for row in coverage if row["status"] == "PARTIAL"]
for issue in issues:
    if issue["id"] == "K.GAP.SOURCE_REVIEW":
        issue["affects"] = partial_ids

for issue in issues:
    for item in question_discovery["candidates"]:
        if issue["id"] in item["issue_ids"]:
            issue["affects"].append(item["id"])
    for item in question_discovery["process_checks"]:
        if issue["id"] in item["issue_ids"]:
            issue["affects"].append(item["id"])
    issue["affects"] = list(dict.fromkeys(issue["affects"]))

case_coverage = []
for q in questions:
    case_coverage.append({"question_id": q["id"], "case_ids": [case_by_q[q["id"]]], "not_applicable": [], "gap_ids": ["K.GAP.REAL_CASES"]})

OUTDIR.mkdir(parents=True, exist_ok=True)
(OUTDIR / "review.md").write_text("# 领域业务知识说明书\n\n等待结构化渲染。\n", encoding="utf-8")
(OUTDIR / "coverage.md").write_text("# 领域知识审计附件\n\n等待结构化渲染。\n", encoding="utf-8")

input_ref = {"artifact_id": fresh["request_id"], "content_version": "2026-09-22.latest.input", "contract_version": "4.0.0", "path": "03领域知识输出/process/runs/2026-09-22.latest/input.json", "digest": digest(FRESH_INPUT)}
payload = {
    "artifact_id": "A01.DomainKnowledge.20260922.Latest",
    "content_version": "2026-09-22.latest.1",
    "contract_version": "4.0.0",
    "stage": "domain-knowledge",
    "mode": "PRODUCE",
    "input_refs": [input_ref],
    "files": [
        {"artifact_id": "A01.DomainKnowledge.20260922.Latest.Review", "content_version": "2026-09-22.latest.1", "contract_version": "text/markdown", "path": "03领域知识输出/candidates/2026-09-22.latest/review.md", "digest": digest(OUTDIR / "review.md")},
        {"artifact_id": "A01.DomainKnowledge.20260922.Latest.Coverage", "content_version": "2026-09-22.latest.1", "contract_version": "text/markdown", "path": "03领域知识输出/candidates/2026-09-22.latest/coverage.md", "digest": digest(OUTDIR / "coverage.md")},
    ],
    "evidence": [],
    "states": {
        "structure_checked": {"status": "NOT_EXECUTED", "evidence_ids": [], "reason": "新鲜草案尚未执行本版本结构校验。"},
        "business_reviewed": {"status": "NOT_EXECUTED", "evidence_ids": [], "reason": "本版本尚未开展业务读者复述或责任人确认。"},
    },
    "confirmation": {"status": "PENDING", "scope_ids": [q["id"] for q in questions], "evidence_ids": []},
    "issues": issues,
    "trace": [{"from_id": r["id"], "to_id": r["statement_ids"][0], "relation": "FORMALIZES", "basis": "规则由对应来源陈述形成。"} for r in rule_objs],
    "content": {
        "scope": fresh["scope"],
        "sources": sources,
        "statements": statements,
        "terms": term_objs,
        "questions": questions,
        "rules": rule_objs,
        "cases": cases,
        "case_coverage": case_coverage,
        "provision_coverage": coverage,
        "question_discovery": question_discovery,
    },
}
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"input": str(FRESH_INPUT), "output": str(OUTPUT), "units": len(units), "statements": len(statements), "terms": len(term_objs), "questions": len(questions), "rules": len(rule_objs), "cases": len(cases), "partial_units": len(partial_ids)}, ensure_ascii=False))
