#!/usr/bin/env python3
"""Author a new A01 knowledge draft from this run's source inventory only.

The statements/rules below are deliberately reviewed prose, not a pick-list of
keywords. The mechanical part only builds references and an honest coverage ledger.
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
SOURCE = RUN / "input.json"
data = json.loads(SOURCE.read_text())
units = {u["unit_id"]: u for u in data["source_units"]}
sources = {s["source_id"]: s for s in data["sources"]}
statements = []
terms = []
questions = []
rules = []
cases = []
issues = []
case_units = {}


def unique(values):
    return list(dict.fromkeys(values))


def S(text, refs, kind, basis, *, origin="SOURCE_STATED", conflict=None):
    ident = f"ST{len(statements)+1:03d}"
    refs = refs.split()
    assert all(ref in units for ref in refs), refs
    statements.append({
        "id": ident, "text": text, "source_ids": unique(units[u]["source_id"] for u in refs),
        "source_unit_ids": refs, "basis": basis, "origin": origin,
        "meaning_kind": kind, "review_status": "PENDING",
        "dispute_status": "OPEN" if conflict else "UNCONTESTED",
        "conflict_ids": [conflict] if conflict else [],
    })
    return ident


def T(name, definition, refs, distinction, example=None, counterexample=None, aliases=None):
    ident = f"T{len(terms)+1:02d}"
    item = {"id": ident, "name": name, "definition": definition,
            "aliases": aliases or [], "statement_ids": refs.split(), "distinctions": distinction}
    if example:
        item["example"] = example
    if counterexample:
        item["counterexample"] = counterexample
    terms.append(item)
    return ident


def Q(question, topic, use, unknown):
    ident = f"Q{len(questions)+1:02d}"
    questions.append({"id": ident, "question": question, "topic": topic,
                      "consumer": "客户尽调、合规复核、备案及差异处理人员",
                      "decision_use": use, "unknown_policy": unknown})
    return ident


def R(name, statements_, questions_, scope, pre, cond, result, exception, missing, period, authority, *, conflict=None):
    ident = f"R{len(rules)+1:02d}"
    rules.append({"id": ident, "name": name, "statement_ids": statements_.split(),
                  "question_ids": questions_.split(), "scope": scope,
                  "preconditions": pre, "conditions": cond, "result": result,
                  "exceptions": exception, "missing_evidence": missing,
                  "effective_period": period, "authority": authority,
                  "origin": "SOURCE_STATED", "review_status": "PENDING",
                  "dispute_status": "OPEN" if conflict else "UNCONTESTED",
                  "conflict_ids": [conflict] if conflict else []})
    return ident


def C(kind, qs, facts, expected, forbidden, refs, source_ids, *, synthetic=False, reasoning=""):
    ident = f"C{len(cases)+1:02d}"
    cases.append({"id": ident, "question_ids": qs.split(), "kind": kind,
                  "input_facts": facts, "expected": expected, "forbidden": forbidden,
                  "source_ids": source_ids.split(), "synthetic": synthetic,
                  "reasoning": reasoning or "先核验适用主体与权利事实，再按相应标准判断；缺失事实不作肯定推断。"})
    case_units[ident] = refs.split()
    return ident


def I(kind, message, affects, recommendation, locator, severity="medium"):
    ident = f"I{len(issues)+1:02d}"
    issues.append({"id": ident, "kind": kind, "statement": message,
                   "affects": affects.split(), "owner": "业务与合规复核负责人",
                   "recommendation": recommendation,
                   "until_resolved": "保持待核与人工复核，不扩展为自动判定。",
                   "status": "OPEN", "locator": locator, "severity": severity.upper()})
    return ident


# Source-backed business propositions: filing duty, bank due diligence and
# interface behaviour are different authorities and are not merged.
s01 = S("受益所有人是最终拥有或实际控制备案主体，或者享有其最终收益的自然人；法定代表人、直接股东和受益所有人不能无条件互代。", "SRC.SRC01.U0005 SRC.TXT001.U00009", "DEFINITION", "3号令第十五条；业务问题说明第9段")
s02 = S("公司、合伙企业、外国公司分支机构属于现行受益所有人备案主体；个体工商户无需备案。", "SRC.SRC01.U0005 SRC.SRC06.U0010 SRC.SRC06.U0011", "CRITERION", "3号令第二条；第二版指南1.1")
s03 = S("注册资本或出资额不超过1000万元、股东或合伙人均为自然人、且不存在外部自然人控制或获益及非股权方式控制或获益的备案主体，承诺后可免报。", "SRC.SRC01.U0005 SRC.SRC06.U0014 SRC.SRC06.U0015 SRC.SRC06.U0016 SRC.SRC06.U0017 SRC.SRC06.U0018", "EXCEPTION", "3号令第三条，四项条件须同时成立")
s04 = S("备案主体的自然人直接或间接最终拥有25%以上股权、股份或合伙权益时符合第一识别标准；指南明确25%以上含25%。", "SRC.SRC01.U0005 SRC.SRC06.U0036 SRC.SRC06.U0041", "CRITERION", "3号令第六条第一项及指南脚注")
s05 = S("未满足股权第一标准，但最终享有25%以上收益权或表决权的自然人，符合第二识别标准。", "SRC.SRC01.U0005 SRC.SRC06.U0042 SRC.SRC06.U0075", "CRITERION", "3号令第六条第二项")
s06 = S("未满足股权第一标准，但单独或联合对主体进行实际控制的自然人，符合第三识别标准；控制可体现为人事、重大决策、财务或重要资产支配。", "SRC.SRC01.U0005 SRC.SRC06.U0043 SRC.SRC06.U0085 SRC.SRC06.U0090", "CRITERION", "3号令第六条第三项及指南3.2.2")
s07 = S("备案主体应逐项检查三种标准，识别全部符合条件的自然人；仅在三种情形都不存在时，才以负责日常经营管理的人员兜底。", "SRC.SRC01.U0005 SRC.SRC06.U0046 SRC.SRC06.U0049 SRC.SRC06.U0057", "PROCEDURE", "3号令第六条末款及指南2.1、2.2")
s08 = S("同一自然人已满足第一标准时按第一标准备案；未满足第一但同时满足第二、第三标准时，两个关系类型均应体现。", "SRC.SRC06.U0044 SRC.SRC06.U0053 SRC.SRC06.U0055", "CRITERION", "第二版指南2.1.1及示例说明")
s09 = S("间接持股需逐层追溯至自然人，沿路径计算并汇总最终权益；指南示例中同一自然人的两条路径合计为31.5%。", "SRC.SRC06.U0061 SRC.SRC06.U0067 SRC.SRC06.U0070 SRC.SRC06.U0071", "PROCEDURE", "第二版指南3.1示例4")
s10 = S("收益权与名义股权可分离；收益权转让后，须分别判断保留股权者与取得收益权者是否符合不同标准。", "SRC.SRC06.U0076 SRC.SRC06.U0081 SRC.SRC06.U0083", "CRITERION", "第二版指南3.2.1示例5、6")
s11 = S("协议投票、代持、亲属关系、创始人影响力或执行事务权等可形成实际控制，但必须查明具体支配事实，不能仅凭关系名称认定。", "SRC.SRC06.U0088 SRC.SRC06.U0089 SRC.SRC06.U0094 SRC.SRC06.U0096 SRC.SRC06.U0098 SRC.SRC06.U0114", "CRITERION", "3号令第六条；第二版指南示例7至9、12")
s12 = S("国有独资公司、国有控股公司的备案口径将法定代表人视为受益所有人；国有参股公司仍按一般标准识别，国有资本部分可不向自然人追溯。", "SRC.SRC01.U0005 SRC.SRC06.U0117 SRC.SRC06.U0118 SRC.SRC06.U0121 SRC.SRC06.U0122", "EXCEPTION", "3号令第七条；第二版指南4.1")
s13 = S("外国公司分支机构备案时应包含外国公司按一般标准识别的受益所有人及分支机构高级管理人员；境外申报豁免不自动适用于中国。", "SRC.SRC01.U0005 SRC.SRC06.U0124 SRC.SRC06.U0125", "CRITERION", "3号令第八条；第二版指南4.2")
s14 = S("备案主体设立登记时备案；不能通过登记系统办理设立登记的，在设立登记后30日内备案；信息变化或承诺免报条件消失后30日内更新。", "SRC.SRC01.U0005", "TIME", "3号令第九、十条；这里是自然日而非12号令差异报告的工作日")
s15 = S("备案信息包括自然人身份、受益所有权关系类型、形成日期及终止日期如有；不同识别标准分别补充权益比例或实际控制方式。", "SRC.SRC01.U0005 SRC.SRC06.U0130 SRC.SRC06.U0131 SRC.SRC06.U0132 SRC.SRC06.U0133", "EVIDENCE", "3号令第十一条；第二版指南5.1")
s16 = S("受益所有权关系形成日期是最终拥有、控制或收益的法律关系生效时间，应按实质重于形式回溯生效文件，不默认等于登记、查询或核实日期。", "SRC.SRC06.U0137 SRC.TXT001.U00025 SRC.TXT001.U00026", "TIME", "第二版指南5.3；业务问题材料区分六类时间")
s17 = S("金融机构应按客户组织形式和风险识别并合理核实非自然人客户受益所有人，不能只依赖BOMIS查询或自动化识别结果。", "SRC.SRC02.U0009 SRC.SRC02.U0011 SRC.SRC02.U0012 SRC.SRC02.U0013", "OBLIGATION", "12号令第三、四条")
s18 = S("金融机构对法人、非法人组织采用最终拥有25%以上股权/合伙权益、未满足前项但享有25%以上收益/表决权、未满足前项但实际控制三种标准；均无时以日常管理人员兜底。", "SRC.SRC02.U0018 SRC.SRC02.U0019 SRC.SRC02.U0020 SRC.SRC02.U0021", "CRITERION", "12号令第八条")
s19 = S("国内分支机构一般沿用所属法人或非法人组织的受益所有人；外国公司分支机构另须认定至少一名分支机构高级管理人员。", "SRC.SRC02.U0022", "CRITERION", "12号令第九条")
s20 = S("12号令第十条列明可免于识别受益所有人的主体类别；该金融机构识别豁免与备案主体承诺免报是不同制度。", "SRC.SRC02.U0023 SRC.SRC02.U0024 SRC.SRC02.U0025 SRC.SRC02.U0026 SRC.SRC02.U0027 SRC.SRC02.U0028 SRC.SRC01.U0005", "EXCEPTION", "12号令第十条与3号令第三条分别适用")
s21 = S("12号令第十一条的简化识别须先充分评估洗钱与恐怖融资风险，按主体类别适用；国有独资、国有控股等特定企业可将法定代表人认定为受益所有人，国有参股只豁免追溯国有资本部分。", "SRC.SRC02.U0030 SRC.SRC02.U0031 SRC.SRC02.U0032 SRC.SRC02.U0033 SRC.SRC02.U0034 SRC.SRC02.U0035 SRC.SRC02.U0036 SRC.SRC02.U0037 SRC.SRC02.U0038", "PERMISSION", "12号令第十一条，不得把32号令国有实际控制企业直接并入")
s22 = S("信托识别覆盖委托人、受托人、受益人、监察人如有及其他最终有效控制的自然人；非自然人信托当事人须逐层追溯，受益人未具体列明时记录受益人范围。", "SRC.SRC02.U0040 SRC.SRC02.U0041 SRC.SRC02.U0042", "CRITERION", "12号令第十二条")
s23 = S("财富管理服务信托、公益慈善信托、民事和外国信托依信托规则识别；其他资产服务信托的简化取决于结构简单且风险较低。", "SRC.SRC02.U0043", "EXCEPTION", "12号令第十三条")
s24 = S("资管产品以风险为基础参照一般三标准识别；公开募集且按规定备案登记的金融机构管理产品或特定低风险产品，在托管等服务场景可将管理产品的自然人认定为受益所有人。", "SRC.SRC02.U0044", "PERMISSION", "12号令第十四条，需核对产品、管理人、业务服务及风险条件")
s25 = S("信托公司作为受托人与其他金融机构建立或存续业务关系，应提供信托受益所有人资料；接受方有条件采信，明显疑点、缺陷或不配合时须采取进一步措施。", "SRC.SRC02.U0045", "OBLIGATION", "12号令第十五条")
s26 = S("金融机构识别应使用来源可靠的材料了解所有权与控制权结构，依据不同组织形式收集章程、股东或合伙人信息、信托与产品权益资料等；核实身份及权利状况需多源综合判断。", "SRC.SRC02.U0047 SRC.SRC02.U0048 SRC.SRC02.U0049 SRC.SRC02.U0050 SRC.SRC02.U0051 SRC.SRC02.U0052 SRC.SRC02.U0053 SRC.SRC02.U0057", "EVIDENCE", "12号令第十六、十七、十九条")
s27 = S("金融机构至少识别留存受益所有人身份与权利状况信息，其中权利关系包含类型及形成、终止时间；比例或控制方式随识别标准而定。", "SRC.SRC02.U0054 SRC.SRC02.U0055 SRC.SRC02.U0056", "EVIDENCE", "12号令第十八条")
s28 = S("权利状况核实以客户佐证为基础，必要时结合官方、公开及机构信息；确属低风险可直接采信客户权利状况信息，但高风险触发加强措施。", "SRC.SRC02.U0057", "EVIDENCE", "12号令第十九条")
s29 = S("复杂跨境持股、循环或交叉持股、协议控制和代持、无理由频繁变化、重大差异或涉嫌洗钱等触发风险相配的加强识别。", "SRC.SRC02.U0058 SRC.SRC02.U0059 SRC.SRC02.U0060 SRC.SRC02.U0061 SRC.SRC02.U0062 SRC.SRC02.U0063", "CRITERION", "12号令第二十条")
s30 = S("加强措施可包括额外独立资料、补充协议、回访、交易监测、提高更新频率、较严格阈值如10%及高级管理层批准；10%不是一般识别默认阈值。", "SRC.SRC02.U0064 SRC.SRC02.U0065 SRC.SRC02.U0066 SRC.SRC02.U0067 SRC.SRC02.U0068 SRC.SRC02.U0069 SRC.SRC02.U0070 SRC.SRC02.U0071 SRC.SRC02.U0072", "PROCEDURE", "12号令第二十一条")
s31 = S("简化或豁免条件无法准确判断时不得适用；出现第二十条特定风险时也不得适用简化或豁免。", "SRC.SRC02.U0081", "PROHIBITION", "12号令第二十五条")
s32 = S("对符合3号令第二条备案范围的客户，金融机构核实受益所有人时应将自身识别结果与BOMIS备案信息查询核对。", "SRC.SRC02.U0074 SRC.SRC01.U0005", "OBLIGATION", "12号令第二十三条；3号令第二条")
s33 = S("查询核对发现差异后应与客户沟通核实；自身识别错误则更正自身结果，备案信息错误且属重大差异则在发现后30个工作日内提交差异报告及佐证。", "SRC.SRC02.U0083 SRC.SRC02.U0084", "PROCEDURE", "12号令第二十六、二十七条")
s34 = S("重大差异包括受益所有人多出或遗漏、关键身份要素不一致、影响关系类型认定的权利状况差异，或形成终止时间出现年月差异等。", "SRC.SRC02.U0085 SRC.SRC02.U0086 SRC.SRC02.U0087 SRC.SRC02.U0088 SRC.SRC02.U0089", "CRITERION", "12号令第二十八条，列举为开放式")
s35 = S("拼写或缩写差异、不影响关系类型的权利数值差异、因机构更严格阈值产生的不一致等属非重大差异；无需提交差异报告，但30个工作日内需记录分析与不报原因并提示客户。", "SRC.SRC02.U0090 SRC.SRC02.U0091 SRC.SRC02.U0092 SRC.SRC02.U0093 SRC.SRC02.U0094", "PROCEDURE", "12号令第二十九条")
s36 = S("应备案未备案的客户，金融机构先沟通提示；客户仍未备案时提交差异报告。", "SRC.SRC02.U0095", "PROCEDURE", "12号令第三十条")
s37 = S("差异分析发现涉嫌洗钱或恐怖融资等犯罪活动时，另按规定提交可疑交易报告；两类报告分别提交，差异报告不得提及可疑交易报告。", "SRC.SRC02.U0096", "PROCEDURE", "12号令第三十一条")
s38 = S("发现重大差异并不当然中止业务关系；在洗钱和恐怖融资风险可控时可以先建立或维持关系。", "SRC.SRC02.U0084", "PERMISSION", "12号令第二十七条第二款")
s39 = S("业务关系存续期间，应随所有权、收益权、表决权、控制权或关键人员重大变化，以及信托当事人变化等审核并在必要时更新受益所有人信息。", "SRC.SRC02.U0075 SRC.SRC02.U0076 SRC.SRC02.U0077 SRC.SRC02.U0078 SRC.SRC02.U0079 SRC.SRC02.U0080", "OBLIGATION", "12号令第二十四条")
s40 = S("12号令自2026年1月20日起实施；较高风险以上存量客户6个月、全部存量客户2年内完成识别核实，长期不动或严格限制客户有条件延期。", "SRC.SRC02.U0003 SRC.SRC02.U0128 SRC.SRC02.U0130", "TIME", "12号令第三十九、四十一条")
s41 = S("BOMIS接口规范描述查询与差异报告异步处理：受理响应不等于最终办理完成，须区分查询、提交、反馈及状态。", "SRC.SRC07.U0055 SRC.SRC07.U0139 SRC.SRC07.U0140 SRC.SRC07.U0385 SRC.SRC07.U0398", "CONTEXT", "BOMIS V2接口说明，只说明系统交互，不改变12号令业务义务")
s42 = S("国资32号令定义国有及国有控股企业、国有实际控制企业用于国有资产交易监管，其分类范围不能直接替代12号令第十一条的简化识别主体列举。", "SRC.SRC03.U0005 SRC.SRC02.U0037 SRC.SRC02.U0038", "CONTEXT", "32号令第四条与12号令第十一条适用目的不同")
s43 = S("同一自然人连接多家客户可供关联风险分析，但共同受益所有人本身不等于交易可疑或违规。", "SRC.TXT001.U00013 SRC.SRC02.U0073", "CONTEXT", "业务问题说明；12号令第二十二条仅在特定高风险时要求关联分析")
s44 = S("历史交易应按当时有效的权利关系判断；形成、终止、登记、核实、备案日期可能不同，不能用当前受益所有人直接替代历史状态。", "SRC.TXT001.U00021 SRC.TXT001.U00025 SRC.TXT001.U00026 SRC.SRC06.U0137", "CONTEXT", "业务问题说明与第二版指南5.3")
s45 = S("备案信息依法查询取得后应保密，查询用途及信息披露应受相应规定约束。", "SRC.SRC01.U0005 SRC.SRC02.U0016 SRC.SRC07.U0324", "OBLIGATION", "3号令第十二条；12号令第七条；BOMIS查询返回说明")
s46 = S("BOMIS接口规范仍列有‘非重大差异报备’报文场景，而12号令第二十九条明确非重大差异无需提交差异报告；接口存在不等于现行法律义务。", "SRC.SRC07.U0347 SRC.SRC02.U0094", "CONTEXT", "接口V2与12号令适用口径有待业务核定", conflict="I01")
s47 = S("同业产品文章把‘优先推荐’用于展示次序，但同时完整输出各标准识别的所有自然人；推荐顺序不是法定识别排除规则。", "SRC.TXT063.U00024 SRC.TXT063.U00032 SRC.TXT063.U00034 SRC.TXT063.U00044 SRC.TXT063.U00046 SRC.SRC06.U0049", "CONTEXT", "企查查推荐规则文章属同业产品口径；完整识别依据以第二版指南为准")
s48 = S("同业文章建议总公司注销后直接取分支机构负责人作为日常管理人员；12号令第九条没有明写此替代，且第八条兜底有三标准均无结果的前提。", "SRC.TXT068.U00021 SRC.TXT068.U00022 SRC.TXT068.U00023 SRC.SRC02.U0021 SRC.SRC02.U0022", "CONTEXT", "边界案例待合规确认，不作为可自动适用的规则")
s49 = S("同业文章提出同一年内形成/终止日相差30个自然日可不认定重大差异；12号令第二十八条明列形成、终止时间出现年月差异为重大差异，附加容差依据尚未从本次权威输入确认。", "SRC.TXT048.U00034 SRC.TXT048.U00035 SRC.SRC02.U0088", "CONTEXT", "同业解释与12号令条文存在口径冲突", conflict="I08")
s50 = S("合伙企业同业文章称12号令第八条有‘四类识别标准’，但该条文本列三项标准并在均不成立时设置日常管理兜底；兜底不应提前并列为第四项。", "SRC.TXT018.U00012 SRC.SRC02.U0018 SRC.SRC02.U0019 SRC.SRC02.U0020 SRC.SRC02.U0021", "CONTEXT", "同业文章与制度结构不同", conflict="I09")
s51 = S("假冒国企材料提示：客户自称央企子公司、股权登记或名称含国资字样，不足以确认其可使用国企简化；官方公告、真实股权与控制事实须相互核实。", "SRC.TXT047.U00011 SRC.TXT047.U00026 SRC.TXT065.U00015 SRC.SRC02.U0057 SRC.SRC02.U0081", "EVIDENCE", "同业案例仅作风险线索；规范上的核实和禁止无证简化来自12号令")
s52 = S("同业合伙企业案例中，持有15%财产份额的合伙人可因协议享有30%利润分配权而满足收益权标准；案例需要以实际合伙协议核实。", "SRC.TXT018.U00014 SRC.TXT018.U00015 SRC.SRC02.U0020", "CRITERION", "同业教学案例与12号令第八条第二项一致，不证明任何真实客户")
s53 = S("同业产品把自然人新增、退出和识别关系类型变化作为变化监控提示；这是一种产品归类，不穷尽12号令第二十四条‘可能影响受益所有权’的复核情形。", "SRC.TXT064.U00073 SRC.TXT064.U00079 SRC.SRC02.U0075 SRC.SRC02.U0076 SRC.SRC02.U0077 SRC.SRC02.U0078", "CONTEXT", "同业产品方法与监管持续审核义务分层")
s54 = S("北京办理指引将承诺免报、国有独资/控股和自行填报分为办理选项，并提示逐项检查三种标准、录入全部符合者；界面选项本身不证明主体符合资格。", "SRC.SRC04.U0009 SRC.SRC04.U0012 SRC.SRC04.U0021 SRC.SRC04.U0022", "PROCEDURE", "北京备案办理指引；资格条件仍由3号令决定")
s55 = S("深圳办理指引要求填报身份、关系类型和形成/终止日期，第二及第三标准并存时同时填报；外国公司分支机构须增加至少一名最高层级高管。", "SRC.SRC05.U0070 SRC.SRC05.U0096 SRC.SRC05.U0292", "PROCEDURE", "深圳备案办理指引；其字段和界面说明不替代3号令")

# Domain vocabulary. Definitions preserve the actor and the legal purpose.
T("受益所有人", "最终拥有、控制或享有主体最终收益的自然人。", "ST001 ST004 ST005 ST006", "不是法人、法定代表人或名义股东的同义词。", "持股30%的自然人可符合第一标准。", "仅任法定代表人但并无适用兜底或特例，不能当然入选。", ["最终受益人"])
T("备案主体", "按3号令承担受益所有人备案义务的主体。", "ST002", "与12号令所称金融机构非自然人客户不是同一集合。")
T("承诺免报", "满足3号令第三条全部条件后，经承诺免于填报受益所有人信息。", "ST003", "不同于金融机构免于识别客户受益所有人。")
T("最终拥有", "自然人经直接或多层股权、股份、合伙权益路径最终拥有目标主体。", "ST004 ST009", "不等于只看登记的直接股东。")
T("最终收益权", "自然人最终享有股权或合伙权益收益的权利。", "ST005 ST010", "可与名义股权分离；一般经营收入不是当然的股权收益权。")
T("表决权", "对主体决议表达意见并形成表决结果的权利。", "ST005 ST010", "可经协议与名义股权分离，须核对实际享有比例。")
T("实际控制", "自然人单独或联合对人事、重大经营、财务或重要资产形成实质支配。", "ST006 ST011", "亲属、创始人或普通合伙人身份本身不等于已证明控制。")
T("日常经营管理兜底", "三项一般标准均找不到自然人时，对负责日常经营管理人员的替代识别。", "ST007 ST018", "是最后顺位，不得覆盖已经找到的受益所有人。")
T("权利路径", "从目标主体沿股权、协议、收益或控制关系到最终自然人的可说明链条。", "ST009 ST026", "数值路径与实际控制事实可能并行，不能仅以乘积覆盖协议控制。")
T("国有资本部分", "在国有参股主体中可不继续向自然人追溯的国有出资部分。", "ST012 ST021", "不能把整个国有参股公司免于识别。")
T("信托当事人", "信托委托人、受托人、受益人以及监察人如有。", "ST022", "其他最终有效控制者不因未列为信托当事人而被排除。")
T("管理产品的自然人", "在满足特定资管产品简化条件时可被认定的管理该产品的人。", "ST024", "不是所有资管产品一概取管理人法定代表人。")
T("佐证材料", "用于证明自然人身份、权利关系、结构和生效时间的可靠材料、数据或信息。", "ST026 ST028", "客户自报、BOMIS数据和自动化结果各有证明边界。")
T("受益所有权关系形成时间", "最终拥有、实际控制或享有最终收益的法律关系生效时间。", "ST016 ST027 ST044", "不同于工商登记日、查询日及机构核实日。")
T("权利终止时间", "具体受益所有权关系停止存在的时间，如有。", "ST015 ST027 ST044", "受益所有人名单变动不自动说明旧关系的终止日。")
T("基于风险的识别", "按客户组织形式、洗钱及恐怖融资风险配置识别与核实强度。", "ST017 ST028", "不能以低风险为由省略必须识别的自然人。")
T("加强识别", "出现特定风险后采用匹配风险的额外核实、监测、阈值或批准措施。", "ST029 ST030", "10%阈值只是可选加强措施，不是通用门槛。")
T("简化识别", "在列明主体、产品及风险条件下适用较简方式的识别。", "ST021 ST023 ST024 ST031", "与无条件豁免、备案承诺免报均不同。")
T("BOMIS备案信息", "受益所有人信息查询管理系统保存的备案结果。", "ST032 ST041", "它是核对对象，不自动替代机构自己的识别结论。")
T("重大差异", "足以影响受益所有人或关键身份、权利类型及重要时间认定的备案与识别差异。", "ST034", "非每个数值、拼写差异都属于重大差异。")
T("非重大差异", "不影响最终识别等、按12号令第二十九条无须提交差异报告的差异。", "ST035 ST046", "仍须记录分析、不报原因并提示客户。")
T("差异报告", "在规定情形下经查询、沟通、核实后向BOMIS提交的差异反馈。", "ST033 ST036 ST037 ST041", "不同于可疑交易报告或接口受理回执。")
T("持续审核更新", "业务关系存续期间出现可能影响受益所有权变化时再审并必要时更新。", "ST039", "不是开户时识别一次后永久有效。")
T("业务时点的权利状态", "某项交易或尽调时间点上实际生效的拥有、控制和收益关系。", "ST016 ST044", "不能直接用今天的名单回填历史。")
T("推荐标识", "同业产品在完整识别结果之外提供的优先展示或关系类型标注。", "ST047", "推荐不缩减依法应识别的全部自然人，也不是监管裁定。", "甲乙丙分别符合三标准，界面优先显示甲但仍保留乙丙。", "只显示推荐的一人并删除其他符合者。")

term_examples = {
    "T02": ("公司A属于3号令的备案主体。", "个体工商户不在现行备案范围内。"),
    "T03": ("自然人股东、出资额500万元且不存在额外控制获益安排的公司可经真实承诺申请免报。", "有外部代持受益人的公司不能仅凭注册资本较低而免报。"),
    "T04": ("甲沿两层公司持股路径最终拥有A公司30%。", "只知道B公司直接持有A公司30%，尚未知道B公司背后的自然人。"),
    "T05": ("丙不持股，但依据有效协议享有A公司30%股权的分红收益。", "丙从A公司取得劳务报酬，不因此拥有30%股权收益权。"),
    "T06": ("丙经股东协议实际享有A公司51%表决权。", "丙只是列席会议，无表决权或代理授权。"),
    "T07": ("甲持股5%，依一致行动协议实际决定董事任免。", "甲与大股东是亲属，但没有可证实的共同决策或支配事实。"),
    "T08": ("三标准均经核对无人满足后，确认最高层级日常经营管理人员。", "已有持股30%的自然人，却仅填法定代表人。"),
    "T09": ("丙经B和C两条持股路径分别取得14%和17.5%，合计31.5%。", "只有工商直接股东名单而没有上层股权链。"),
    "T10": ("国有资本持有参股公司30%，其余自然人股权仍逐项识别。", "把国有参股公司整体视作无须识别受益所有人。"),
    "T11": ("信托合同列明委托人、受托人、受益人与监察人。", "只登记受托人，遗漏拥有分配方案决定权的其他自然人。"),
    "T12": ("符合12号令第十四条条件的公募登记产品，在托管服务中认定具体管理产品的自然人。", "仅因产品名称含‘基金’就直接认定管理人法定代表人。"),
    "T13": ("生效的股权转让协议配合章程、登记及身份资料说明路径和日期。", "单个商业数据库搜索结果而无独立核验。"),
    "T14": ("股权转让协议约定并实际于6月1日生效。", "机构9月1日查询到该股权就把9月1日写为形成日。"),
    "T15": ("控制协议明确于8月31日终止并有后续执行证据。", "某人不在今天名单上就推定其去年已经终止控制。"),
    "T16": ("复杂代持客户增加独立资料和回访。", "不区分风险，对全部客户一律收取所有可能材料。"),
    "T17": ("重大差异后补充独立证据、提高更新频率。", "把10%作为所有普通客户的统一法定阈值。"),
    "T18": ("经充分风险评估的国有控股公司，按12号令第十一条采用相应简化措施。", "因为企业名称含‘国资’就不调查其控制结构。"),
    "T19": ("机构查询到客户备案的甲并与自身识别结果核对。", "BOMIS显示甲就不再核实甲的权利状况。"),
    "T20": ("备案遗漏一名已证实的受益所有人。", "同一人的非汉字姓名仅有缩写差异。"),
    "T21": ("已证实同一人英文名缩写不同，仍按规定记录并提示。", "备案少了一名真正的受益所有人。"),
    "T22": ("有充分证据证明备案遗漏受益所有人，经沟通核实后提交重大差异报告。", "接口同步受理回执不是报告最终办结。"),
    "T23": ("控制协议重大变更后重新审核实际控制人。", "开户时名单未经复核就永久沿用。"),
    "T24": ("追查2024年交易时，使用当时已生效且尚未终止的股权关系。", "拿2026年当前股东直接认定其控制2024年交易。"),
}
for term in terms:
    if term["id"] in term_examples:
        term["example"], term["counterexample"] = term_examples[term["id"]]

q_scope = Q("当前事项是备案主体备案、金融机构客户识别，还是接口查询反馈？", "适用范围与责任", "选定正确义务主体和依据", "角色或组织类型不明时不套用其他制度")
q_exempt = Q("该主体能否承诺免报、免于识别或简化识别？", "适用范围与责任", "决定能否使用例外口径", "条件不明则不适用简化或豁免")
q_equity = Q("哪些自然人经直接或间接路径最终拥有至少25%的股权或合伙权益？", "自然人识别", "识别第一标准及路径", "缺股权链或比例时保持待核")
q_benefit = Q("未满足第一标准的人是否最终享有至少25%的收益权或表决权？", "自然人识别", "识别分离的收益和表决权", "协议或比例不明时不作肯定结论")
q_control = Q("未满足第一标准的人是否单独或联合实施实际控制？", "自然人识别", "识别人事、决策、财物支配", "只有关系名称无支配事实时待核")
q_fallback = Q("三项标准均无结果时，谁负责日常经营管理？", "自然人识别", "兜底识别", "三项标准未核完不得提前兜底")
q_special = Q("国有企业、分支机构或合伙企业有哪些特例与边界？", "特殊主体", "适用专门标准及排除错误类推", "国企性质及控制证据不足时先核实")
q_trust = Q("信托及资管产品的全部相关自然人如何识别？", "特殊主体", "区分信托、资管及简化条件", "产品性质、角色与风险不明时待核")
q_evidence = Q("识别结果由哪些身份、权利与结构证据支持，可信度是否足够？", "证据与时间", "核实自然人身份及关系", "不得把系统命中当作充分核实")
q_time = Q("权利何时形成或终止，历史业务时点实际由谁拥有或控制？", "证据与时间", "追溯历史与解释日期差异", "无生效依据则记录未知而非补默认日期")
q_risk = Q("哪些风险触发加强措施，哪些低风险允许合理简化？", "风险与持续管理", "选择相称尽调强度", "风险未评估时不推定低风险")
q_compare = Q("应否与备案信息查询核对，查询结果与机构识别如何区分？", "核对与差异", "履行核对义务", "不以查询成功或接口回执替代业务结论")
q_diff = Q("差异原因与重大性如何判断，何时更正、记录或报送？", "核对与差异", "区分自身错误、重大、非重大、未备案", "事实未核清先沟通并保留待核")
q_ongoing = Q("何种变化要求重新审核、更新或关联分析？", "风险与持续管理", "维护存续期结论", "变化是否影响权利不明时复核")
q_record = Q("识别与差异处理需要留下什么可复核记录，时限如何区分？", "证据与时间", "形成可追溯的业务记录", "不混淆自然日和工作日、受理和终态")

FILING = "备案主体；3号令"
BANK = "承担客户尽调义务的金融机构；12号令"
GUIDE = "3号令及受益所有人信息备案指南第二版"
R("备案主体与个体工商户范围", "ST002", "Q01", FILING, "确认主体法律形态", "公司、合伙企业或外国公司分支机构", "承担备案义务；个体工商户不备案", "主管部门规定的其他主体须另核", "营业执照及主体形态不明则待核", "自2024-11-01起", "3号令第二条")
R("承诺免报须四项同时成立", "ST003 ST054", "Q02", FILING, "属于备案主体", "资本不超1000万元、股东/合伙人均自然人、无外部自然人控制获益、无非股权方式控制获益，且作真实承诺", "可承诺免于备案信息", "任一条件不成立或承诺不实不能使用", "缺资本、股东名单或协议控制调查时不得推定免报", "自2024-11-01起", "3号令第三条；北京指引只说明办理选项")
R("股权第一标准含25%", "ST004 ST009", "Q03", "备案主体或金融机构一般识别", "取得完整直接与间接股权链", "自然人最终拥有比例达到25%，多路径合并计算", "识别该自然人为第一标准受益所有人", "名义持股不等于最终拥有", "链条、比例或最终权利人不明则待核", "按所适用3号令/12号令期间", "3号令第六条；12号令第八条；第二版指南3.1")
R("收益表决第二标准", "ST005 ST010", "Q04", "备案主体或金融机构一般识别", "该自然人不满足第一标准", "最终收益权或表决权达到25%", "按第二标准识别，并记录比例与来源", "不能把普通营业收入视为股权收益权", "缺协议、权利比例或最终享有事实则待核", "按所适用3号令/12号令期间", "3号令第六条；12号令第八条")
R("实际控制第三标准", "ST006 ST011", "Q05", "备案主体或金融机构一般识别", "该自然人不满足第一标准", "查明单独或联合支配人事、重大决策、财物的具体事实", "按第三标准识别并说明控制方式", "亲属或创始人身份不单独构成证明", "缺协议、决议、行为事实则待核", "按所适用3号令/12号令期间", "3号令第六条；12号令第八条")
R("多自然人完整识别", "ST007 ST008", "Q03 Q04 Q05", "备案主体", "分别检查三标准", "不同自然人分别符合一项或多项", "记录全部符合者；同一人第一标准优先，第二与第三可并存", "不得只选一名最高比例人", "任一分支未调查应标明未完成", "自2024-11-01起", "3号令第六条；第二版指南2.1")
R("日常管理兜底仅最后适用", "ST007 ST018", "Q06", "备案主体或金融机构一般识别", "三标准已查明均无符合自然人", "存在负责日常经营管理的自然人", "以日常经营管理人员兜底", "已找到任一标准受益所有人时不得以兜底替代", "三项调查不完整则不得兜底", "按所适用3号令/12号令期间", "3号令第六条；12号令第八条")
R("国有独资控股备案特例", "ST012", "Q07", FILING, "核实确属国有独资或国有控股公司", "适用3号令第七条", "将法定代表人视为受益所有人备案", "国有参股不适用整体法定代表人特例", "仅凭名称或宣传自称国企不得适用", "自2024-11-01起", "3号令第七条；第二版指南4.1")
R("国有参股只免追国资部分", "ST012 ST021", "Q07", "国有参股公司", "核实国有资本比例和控制性质", "国有资本参与但主体非国有独资/控股特例", "一般标准识别非国资部分；国资部分可不继续识别", "不得免除其他自然人路径", "国资结构不清须核实，不以名称代替", "按所适用3号令/12号令期间", "第二版指南4.1；12号令第十一条第八项")
R("境内分支机构沿用总机构", "ST019", "Q07", BANK, "确认国内法人或非法人组织分支机构及其总机构", "总机构受益所有人已按规定识别", "一般将总机构受益所有人认定为分支机构受益所有人，可合规复用已有信息", "若总机构信息过期仍需核实", "总机构主体或结果缺失则待核", "自2026-01-20起", "12号令第九条第一款")
R("外国公司分支机构追加高管", "ST013 ST019 ST055", "Q07", "外国公司分支机构备案或金融机构识别", "识别所属外国公司受益所有人", "分支机构存在高级管理人员", "另纳入分支机构至少一名高管；备案不沿用境外豁免", "不能只识别外国总公司股东", "高管身份或所属公司结构不明则待核", "按所适用3号令/12号令期间", "3号令第八条；12号令第九条；深圳指引")
R("合伙企业控制权独立核对", "ST006 ST011", "Q05 Q07", "合伙企业特别是有限合伙", "取得合伙协议与经营决策事实", "普通合伙人即便仅1%出资，仍可决定财务、人事和投资", "按实际控制标准识别该自然人", "不能以普通合伙人身份自动认定", "协议与实际控制事实不明则待核", "自2024-11-01起", "第二版指南示例12；3号令第六条")
R("信托当事人及最终控制者", "ST022", "Q08", BANK, "确认服务对象为信托", "识别各信托当事人及其他最终有效控制人，非自然人当事人逐层穿透", "纳入相应自然人；具体受益人未定时记录范围", "其他产品不得不加区分套用信托条款", "信托合同或受益人范围缺失时标明待核", "自2026-01-20起", "12号令第十二条")
R("资产服务信托简化条件", "ST023", "Q08 Q02", BANK, "服务对象为财富管理服务信托以外的其他资产服务信托", "所有权控制结构简单且洗钱恐融风险较低", "可采取简化识别", "财富管理服务、公益慈善、民事和外国信托按第十二条", "类型与风险无法确认不得简化", "自2026-01-20起", "12号令第十三条")
R("资管产品识别及托管简化", "ST024", "Q08 Q02", BANK, "确认资管产品、管理/受托主体及提供的金融服务", "公开募集且登记备案，或其他低风险并充分评估", "在规定服务场景可认定管理产品的自然人", "不满足条件仍须风险基础上参照一般标准", "产品合同、备案及风险材料不足则待核", "自2026-01-20起", "12号令第十四条")
R("信托公司提供资料及有条件采信", "ST025", "Q08 Q09", BANK, "信托公司作为受托人与非信托机构建立/维持业务", "信托公司提供资料，接受方确认体系有效且无明显疑点", "可有条件采信；疑点或缺陷时要求重识别，严重不配合时采取风险措施", "采信不等于免除接受方审慎义务", "材料、体系或疑点未核实时不直接采信", "自2026-01-20起", "12号令第十五条")
R("身份与权利双重证据", "ST017 ST026 ST027 ST028", "Q09", BANK, "正在识别非自然人客户", "有可靠身份、结构、权利资料，风险相称核实", "形成有依据的自然人及权利结论并留存规定要素", "确属低风险可直接采信客户权利状况信息，身份仍需核实", "仅BOMIS、自动计算或单方断言不足时列待核", "自2026-01-20起", "12号令第四、十六至十九条")
R("权利形成日期取法律生效日", "ST015 ST016 ST027 ST044", "Q10 Q15", "备案主体及金融机构各自记录", "取得章程、合伙协议、转让协议或控制安排", "可确认权利关系生效时间", "记录关系类型、形成时间、终止时间如有及依据", "不自动取登记、查询、机构识别日", "缺生效文件记录未知及核实任务", "按适用制度", "3号令第十一条；12号令第十八条；第二版指南5.3")
R("备案设立及变化时限", "ST014", "Q15", FILING, "确认登记与变化日期", "设立登记、非系统登记或信息变化/免报条件消失", "分别在设立时、登记后30日、变化后30日备案/更新", "不同于机构差异报告30个工作日", "日期或变化事实不明则核实", "自2024-11-01起", "3号令第九、十条")
R("金融机构可免识别类别", "ST020", "Q02", BANK, "核实客户是否属于第十条列举主体", "主体身份与法定类别匹配", "可免于识别其受益所有人", "不等于备案主体承诺免报；第二十条特定风险时不得适用", "分类不明不得豁免", "自2026-01-20起", "12号令第十、二十五条")
R("金融机构简化先评风险", "ST021 ST031", "Q02 Q11", BANK, "客户落入第十一条对应类别", "充分评估风险，且无第二十条风险", "采用与风险匹配的简化措施", "国有实际控制企业不自动等同国有控股公司", "风险或主体分类不明不得简化", "自2026-01-20起", "12号令第十一、二十五条")
R("风险触发加强识别", "ST029 ST030", "Q11", BANK, "存在第二十条特定情形", "高风险地区、复杂结构、异常变化、资料疑点或犯罪怀疑等", "采用匹配的一种或多种加强措施", "10%仅为可选更严格阈值", "风险信号不清应调查，不能直接判低风险", "自2026-01-20起", "12号令第二十、二十一条")
R("超出风险能力时拒绝或终止", "ST030", "Q11", BANK, "已经采取相应加强措施", "洗钱或恐融风险仍超出机构风险管理能力", "应拒绝办理业务或终止已建立关系", "是否超能力由机构按事实与权限判断", "风险评价资料不足不得自动作出终止结论", "自2026-01-20起", "12号令第二十一条")
R("备案客户必须查询核对", "ST032", "Q12", BANK, "客户符合3号令第二条备案范围，正在核实受益所有人", "机构已有独立识别结果", "与BOMIS保存的备案信息查询核对", "查询结果不是独立识别的替代", "查询失败、无返回或字段受限保持待核", "自2026-01-20起", "12号令第二十三条")
R("自身识别错先更正", "ST033", "Q13", BANK, "核对发现差异并已与客户沟通", "有合理理由认定差异由本机构识别不准造成", "更正机构自身受益所有人信息", "不得把自身错误直接转报为备案错误", "差异原因未查明时继续核实", "自2026-01-20起", "12号令第二十七条")
R("重大备案差异30工作日报告", "ST033 ST034", "Q13 Q15", BANK, "核对差异且经沟通核实", "有合理理由认为备案不准且差异重大", "发现差异后30个工作日内提交报告，留存理由、过程、佐证", "重大差异不当然中止业务", "证据不足时先核实重大性与归因", "自2026-01-20起", "12号令第二十七、二十八条")
R("非重大差异记录不报告", "ST035", "Q13 Q15", BANK, "核对差异并分析确认非重大", "拼写、非实质权利差异或更严格阈值等", "不提交差异报告；30个工作日内记录分析、不报原因和措施并提示客户", "若影响受益所有人或关系类型则重新判重大", "重大性未定不得先结案", "自2026-01-20起", "12号令第二十九条")
R("应备案未备案的处理", "ST036", "Q13", BANK, "客户属于应备案主体且查询发现未备案", "已沟通提示后仍未备案", "提交差异报告", "不得仅因未备案直接等同可疑交易", "客户备案状态或沟通结果缺失则待核", "自2026-01-20起", "12号令第三十条")
R("差异报告与可疑交易报告分离", "ST037", "Q13", BANK, "差异分析中发现涉嫌犯罪活动", "同时满足两类报告触发条件", "分别提交；差异报告不提可疑交易报送情况", "不能用差异报告替代可疑交易报告", "涉嫌事实未核明交有权岗位判断", "自2026-01-20起", "12号令第三十一条")
R("重大差异下业务关系可控继续", "ST038", "Q13 Q11", BANK, "发现重大差异", "洗钱和恐怖融资风险可控", "可以先建立或维持业务关系", "并非无条件继续，仍履行核实与报告", "风险不可判断时不自动放行", "自2026-01-20起", "12号令第二十七条")
R("持续变化再审核更新", "ST039", "Q14", BANK, "客户关系存续", "权益、控制、关键人员或信托当事人变化可能影响受益所有权", "审核并在必要时更新受益所有人信息", "并非所有人员变化都自动改变受益所有人", "变化是否影响权利不明时先复核", "自2026-01-20起", "12号令第二十四条")
R("自然人高风险关联分析", "ST043", "Q14 Q11", BANK, "自然人客户行为或交易出现较高洗钱/恐融风险", "该自然人可能是本机构其他非自然人客户的受益所有人", "视情形筛查全部关联客户并采取必要措施", "共同受益所有人本身不是违法结论", "身份关联不稳时不得强并", "自2026-01-20起", "12号令第二十二条")
R("异步接口受理不等于办结", "ST041", "Q12 Q15", "BOMIS V2系统交互", "已提交查询或差异报文", "收到同步响应或待审核反馈", "继续追踪异步终态并保留业务判断记录", "接口状态不改变法定报告判断", "反馈缺失或终止需追查状态", "按接口适用版本", "BOMIS V2接口规范场景及108反馈")
R("存量客户过渡期限", "ST040", "Q15", BANK, "2026-01-20前已建立业务/交易且识别不符合新要求", "较高风险以上或其他存量客户", "分别按6个月及2年期限完成；长期不动/严格限制客户有条件延期", "不得把过渡期用于新增客户", "风险层级或账户状态不明则核实", "自2026-01-20起", "12号令第三十九条")
R("历史时点不以当前覆盖", "ST016 ST044", "Q10", "历史交易调查与持续记录", "已取得关系生效和终止证据", "查询业务时点的有效权利", "以该时点有效关系解释，不将现时名单倒填历史", "旧权利终止时间仍需证实", "无法证实形成时间时保留未知", "持续适用", "业务问题材料；第二版指南5.3")
R("保密与查询用途", "ST045", "Q09 Q12", "获取备案或核实信息的机构", "依法为尽调/反洗钱目的取得信息", "仅为履行相应义务取得信息", "按授权用途使用并保密", "不得把取得权限理解为可任意传播", "用途声明和授权不明则停止扩用", "按适用法规及接口版本", "3号令第十二条；12号令第七条")
R("产品推荐不得缩减完整识别", "ST047 ST007", "Q03 Q04 Q05", "同业产品输出或机构使用其结果", "已分别核实三种标准", "系统设置优先推荐或展示顺序", "仍保留并复核所有符合条件的自然人", "产品推荐规则不等于法定义务的替代", "只返回推荐对象时视为结果不完整", "按当前制度和具体产品版本", "第二版指南2.1.3；同业产品推荐文章为产品说明")
R("国企简化先核真实身份", "ST031 ST051", "Q02 Q07 Q09", "金融机构拟对声称国企客户简化", "取得官方来源、股权与控制证据", "能够确认客户确属12号令第十一条适用类别且无加强情形", "才可按风险适用相应简化", "仅凭自称、名称、商业标签或虚假登记不得简化", "官方公告或出资关系无法核实时转为一般/加强调查", "自2026-01-20起", "12号令第十一、十九、二十五条；同业假冒国企案例仅供线索")

# Boundary and negative examples are intentionally prominent.
C("BOUNDARY", "Q03", ["A公司自然人甲55%、乙20%、丙25%。"], "甲与丙符合第一标准；25%含本数。", "把丙排除或把乙纳入。", "SRC.SRC06.U0065", "SRC.SRC06", reasoning="按每人最终股权比较含本数的25%门槛。")
C("POSITIVE", "Q03", ["A公司甲直接30%；丙沿两条路径合计31.5%，乙21%，丁17.5%。"], "甲和丙符合第一标准。", "只计算丙的一条路径或把乙纳入。", "SRC.SRC06.U0067 SRC.SRC06.U0070 SRC.SRC06.U0071", "SRC.SRC06", reasoning="逐路径乘积并按同一自然人汇总，最终股权达到25%者入选。")
C("POSITIVE", "Q04", ["甲、乙各持股30%、70%；甲将其30%股权的收益权转让给不持股的丙，仍保留投票权。"], "甲乙按股权第一标准、丙按收益第二标准识别。", "因甲转让收益权就删除其股权标准结论。", "SRC.SRC06.U0081", "SRC.SRC06", reasoning="名义及最终股权、收益权分开判断。")
C("BOUNDARY", "Q04", ["甲仅持股10%，另经协议获得20%股权所附收益权，合计收益权30%。"], "甲按第二标准识别。", "把10%股权与20%收益权相加成30%股权。", "SRC.SRC06.U0083", "SRC.SRC06", reasoning="股权比例未达25%，收益权比例已达30%。")
C("POSITIVE", "Q05", ["甲仅持股5%，与多名股东有一致投票协议，能够决定董事长和重大决策。"], "甲可按实际控制第三标准识别。", "因持股未达25%而排除甲。", "SRC.SRC06.U0094", "SRC.SRC06", reasoning="协议联同行使投票并支配人事/重大决策是实质事实。")
C("MISSING_EVIDENCE", "Q05 Q09", ["仅知某人是创始人或亲属，未取得控制安排、决策行为或资金支配证据。"], "保持实际控制待核并补证。", "直接认定其为实际控制型受益所有人。", "SRC.SRC06.U0090 SRC.SRC06.U0096 SRC.SRC06.U0098", "SRC.SRC06", synthetic=True, reasoning="身份关系只是线索，缺少具体支配事实。")
C("NEGATIVE", "Q06", ["股权、收益和控制三条标准尚未调查完，已知道法定代表人姓名。"], "不得提前使用日常管理兜底。", "直接把法定代表人作为唯一受益所有人。", "SRC.SRC06.U0057", "SRC.SRC06", synthetic=True)
C("POSITIVE", "Q07 Q05", ["有限合伙普通合伙人甲仅出资1%，但决定企业财务、人事和投资。"], "甲以实际控制第三标准入选。", "仅以1%出资比例将甲排除。", "SRC.SRC06.U0114", "SRC.SRC06", reasoning="出资比例与控制事实分开。")
C("BOUNDARY", "Q07", ["国有资本30%，自然人甲60%、乙10%；国资非第一大股东且不能实际控制。"], "甲入选，国资部分可不追溯，乙不因10%入选。", "把国有参股公司整体按国有控股简化。", "SRC.SRC06.U0121 SRC.SRC06.U0122", "SRC.SRC06")
C("NEGATIVE", "Q07 Q02", ["企业自称有国资背景，但只取得商业宣传，未核对股权与控制事实。"], "国企性质及简化资格待核。", "自动按国有控股或国有独资处理。", "SRC.SRC02.U0037 SRC.SRC06.U0117", "SRC.SRC02 SRC.SRC06", synthetic=True)
C("BOUNDARY", "Q07", ["客户是外国公司在中国的分支机构，已有外国总公司受益所有人清单。"], "还需识别分支机构至少一名高级管理人员。", "只复制总公司名单即结束。", "SRC.SRC02.U0022", "SRC.SRC02", synthetic=True)
C("MISSING_EVIDENCE", "Q08", ["信托合同没有列出具体受益人，只给出受益人类别。"], "记录受益人范围并继续识别信托当事人及最终控制者。", "因未有具体受益人而写为无受益所有人。", "SRC.SRC02.U0042", "SRC.SRC02", synthetic=True)
C("BOUNDARY", "Q08 Q02", ["某资管产品由金融机构管理，但未证明公开募集、登记备案或低风险条件。"], "不能直接采用管理产品自然人简化口径，先核实产品条件及风险。", "所有金融机构管理产品一律简化。", "SRC.SRC02.U0044", "SRC.SRC02", synthetic=True)
C("MISSING_EVIDENCE", "Q09 Q12", ["BOMIS命中自然人甲，但机构没有取得股权结构或控制协议。"], "把命中作为核对线索，继续识别核实。", "仅凭查询结果确认权利与路径。", "SRC.SRC02.U0013 SRC.SRC02.U0047", "SRC.SRC02", synthetic=True)
C("BOUNDARY", "Q10", ["股权协议2024-06-01生效，工商变更2024-06-20，机构2026-03-01核实。"], "在证据充分时以权利法律关系生效时间解释形成日，保留登记和核实日各自含义。", "默认用2026-03-01或2024-06-20作为权利形成日。", "SRC.SRC06.U0137 SRC.TXT001.U00025", "SRC.SRC06 SRC.TXT001", synthetic=True)
C("MISSING_EVIDENCE", "Q10 Q09", ["仅查得当前40%持股，缺少从30%升至40%的协议生效日。"], "当前比例形成日期待核，已知首次达到门槛日期另行保留。", "把首次入选日期硬填为当前比例的形成日期。", "SRC.TXT001.U00028 SRC.TXT001.U00029 SRC.TXT001.U00030", "SRC.TXT001", synthetic=True)
C("NEGATIVE", "Q11 Q02", ["客户存在无法核实的境外持股与代持安排，却申请简化识别。"], "触发加强识别，不得简化。", "因主体名称满足第十一条类别就自动简化。", "SRC.SRC02.U0060 SRC.SRC02.U0081", "SRC.SRC02", synthetic=True)
C("BOUNDARY", "Q11", ["客户风险升高，机构考虑将股权门槛降至10%。"], "10%可作为匹配风险的加强措施，需记录适用理由。", "宣称所有客户一般识别门槛已改为10%。", "SRC.SRC02.U0070", "SRC.SRC02", synthetic=True)
C("MISSING_EVIDENCE", "Q12 Q15", ["差异报文已收到接口同步响应，但未收到最终处理反馈。"], "保留待处理，查询异步状态。", "把接口受理记作报告已办结。", "SRC.SRC07.U0055 SRC.SRC07.U0385", "SRC.SRC07", synthetic=True)
C("BOUNDARY", "Q13", ["同一受益所有人的非汉字姓名仅拼写缩写不同，其他身份和权利已核对。"], "按非重大差异处理，记录原因并提示客户。", "自动提交重大差异报告。", "SRC.SRC02.U0091 SRC.SRC02.U0094", "SRC.SRC02", synthetic=True)
C("POSITIVE", "Q13 Q15", ["备案遗漏一名经充分证据确认的受益所有人，机构已与客户沟通确认备案不准。"], "按重大差异在30个工作日内提交报告并留证。", "仅作为普通拼写差异不报。", "SRC.SRC02.U0084 SRC.SRC02.U0086", "SRC.SRC02", synthetic=True)
C("BOUNDARY", "Q13 Q10", ["同一受益所有权关系，机构证据指向2025年2月生效，备案为2025年3月。"], "年月差异可属于重大差异，需核实归因和生效证据。", "仅因日差不一致的规则直接套用于年月差异。", "SRC.SRC02.U0088", "SRC.SRC02", synthetic=True)
C("NEGATIVE", "Q13", ["机构与BOMIS人名不同，复核证明是机构自己错认自然人。"], "更正机构识别结论。", "把自身错误当作备案错误提交重大差异。", "SRC.SRC02.U0084", "SRC.SRC02", synthetic=True)
C("BOUNDARY", "Q13 Q11", ["发现重大差异，但补充核查后洗钱与恐融风险可控。"], "可先维持业务关系，同时履行报告和核实义务。", "重大差异即一律终止业务。", "SRC.SRC02.U0084", "SRC.SRC02", synthetic=True)
C("POSITIVE", "Q14", ["客户通过新协议将表决权委托给外部自然人，可能改变实际控制。"], "重新审核受益所有人并在必要时更新。", "沿用开户时原结果不复核。", "SRC.SRC02.U0075 SRC.SRC02.U0076", "SRC.SRC02", synthetic=True)
C("NEGATIVE", "Q14", ["两家客户由同一自然人最终拥有，但没有异常交易或其他高风险证据。"], "可记录关联供风险分析，不直接作违法结论。", "仅凭共同受益所有人判定可疑交易。", "SRC.TXT001.U00013 SRC.SRC02.U0073", "SRC.TXT001 SRC.SRC02", synthetic=True)
C("BOUNDARY", "Q15", ["备案主体权利变化后第30日更新；机构重大差异发现后第30个工作日报告。"], "分别按3号令自然日与12号令工作日计时。", "将两种时限混为同一个30日。", "SRC.SRC01.U0005 SRC.SRC02.U0084", "SRC.SRC01 SRC.SRC02", synthetic=True)
C("BOUNDARY", "Q04 Q07", ["合伙人持有15%财产份额，合伙协议另约定享有30%利润分配权。"], "若协议有效且最终享有30%收益权，按第二标准识别。", "仅看15%出资比例就排除。", "SRC.TXT018.U00015 SRC.SRC02.U0020", "SRC.TXT018 SRC.SRC02", synthetic=True, reasoning="同业文章提供场景，规范结论需以12号令第八条和具体协议核实。")
C("MISSING_EVIDENCE", "Q07 Q06", ["国内分支机构总公司已注销，同业产品建议直接取分公司负责人。"], "先核总公司终止前后的权利、分支机构法律状态及三标准，再由合规决定适用口径。", "直接把产品建议当作12号令第九条的明确替代规则。", "SRC.TXT068.U00023 SRC.SRC02.U0022", "SRC.TXT068 SRC.SRC02", synthetic=True)
C("BOUNDARY", "Q13 Q10", ["两份材料的权利形成日期分别为同年1月28日和2月20日。"], "保留年月差异并按12号令第二十八条评估重大性；同业‘30日容差’待核权威依据。", "自动套用同业文章的30日豁免。", "SRC.TXT048.U00035 SRC.SRC02.U0088", "SRC.TXT048 SRC.SRC02", synthetic=True)
C("NEGATIVE", "Q03 Q04 Q05", ["产品对甲优先打推荐标识，乙和丙分别满足其他标准。"], "完整保留甲乙丙的识别结果。", "仅因推荐标识就删除乙丙。", "SRC.TXT063.U00034 SRC.SRC06.U0049", "SRC.TXT063 SRC.SRC06", synthetic=True)

I("CONFLICT", "BOMIS V2接口规范包含非重大差异报备型报文，而现行12号令第二十九条写明非重大差异无需提交差异报告；需核定接口场景的适用时间、业务意图和当前操作口径。", "ST046", "按现行12号令形成义务判断；请合规与接口主管确认非重大报备型是否只为特定历史/技术场景。", "SRC.SRC07.U0347；SRC.SRC02.U0094", "high")
I("KNOWLEDGE_GAP", "同一来源单元内的3号令全文、国资32号令多条款及BOMIS大表尚未逐段完成业务含义审阅。", "PC.SRC.SRC01.U0005 PC.SRC.SRC03.U0005 PC.SRC.SRC07.U0347", "按条款/表格分段回读，核对已抽取事实与遗漏。", "SRC.SRC01.U0005；SRC.SRC03.U0005；SRC.SRC07.U0347", "high")
I("KNOWLEDGE_GAP", "部分PDF/DOCX存在低置信边界或页数缺口；Markdown中图片仅保留链接，没有读取图内内容。", "Q09", "补核原页及图片，尤其BOMIS V2缺失页面和地方备案流程图。", "本轮input.json/source_extractions", "high")
I("KNOWLEDGE_GAP", "已纳入台账但尚未逐来源完成语义审阅的材料，不得视为业务覆盖完成。", "Q01", "分批审阅剩余来源单元并按其权威等级整合；先核监管原文，再用同业材料发现边界。", "本轮provision_coverage", "high")
I("KNOWLEDGE_GAP", "真实客户的国企身份、协议控制、历史生效文件和信托产品条款没有随输入提供，本文案例仅用于判断边界。", "Q07 Q09 Q10", "业务评审时提供真实脱敏材料，逐项验证。", "A01受益所有人/01业务输入", "medium")
I("KNOWLEDGE_GAP", "BOMIS V2文档声明115页但解析结果只有100页；无法认定接口合同已完整覆盖。", "Q12", "核对原文件缺失页及解析服务输出，再审接口章节。", "SRC.SRC07", "high")
I("KNOWLEDGE_GAP", "国有实际控制企业与12号令第十一条国有独资、国有控股类别不完全等同，不能仅用国资32号令分类推导简化资格。", "Q07", "由合规复核具体企业分类和适用规范，不以商业文章扩张法条。", "SRC.SRC03.U0005；SRC.SRC02.U0037", "high")
I("CONFLICT", "同业文章称同年跨月且相差30自然日可免重大差异；12号令第二十八条将形成/终止年月差异列入重大差异，输入中缺少支持该容差的权威依据。", "ST049 Q13", "按12号令先标记重大性待核，不将同业容差自动写成豁免。", "SRC.TXT048.U00035；SRC.SRC02.U0088", "high")
I("CONFLICT", "同业文章把三项识别标准和日常管理兜底合称四类；12号令第八条明确前三项均不成立才兜底。", "ST050 Q06", "按制度三项加最后兜底表达，文章只作为错误口径警示。", "SRC.TXT018.U00012；SRC.SRC02.U0021", "medium")
I("KNOWLEDGE_GAP", "总公司注销、分支机构仍存续时的替代识别，同业产品直接取负责人；12号令第九条未给出这一显式替代，适用第八条兜底还需先查三项标准。", "Q07 Q06", "请合规审查分支机构法律状态、总公司历史权利及负责人事实后确认机构口径。", "SRC.TXT068.U00023；SRC.SRC02.U0022", "high")

stmt_by_unit = defaultdict(list)
for statement in statements:
    for ref in statement["source_unit_ids"]:
        stmt_by_unit[ref].append(statement["id"])
term_by_statement = defaultdict(list)
for term in terms:
    for ref in term["statement_ids"]:
        term_by_statement[ref].append(term["id"])
rule_by_statement = defaultdict(list)
for rule in rules:
    for ref in rule["statement_ids"]:
        rule_by_statement[ref].append(rule["id"])
case_by_unit = defaultdict(list)
for case_id, refs in case_units.items():
    for ref in refs:
        case_by_unit[ref].append(case_id)

coverage = []
for unit in data["source_units"]:
    uid = unit["unit_id"]
    pcid = "PC." + uid
    statement_ids = stmt_by_unit[uid]
    term_ids = unique(t for sid in statement_ids for t in term_by_statement[sid])
    rule_ids = unique(r for sid in statement_ids for r in rule_by_statement[sid])
    question_ids = unique(q for rule in rules if rule["id"] in rule_ids for q in rule["question_ids"])
    case_ids = case_by_unit[uid]
    broad = uid in {"SRC.SRC01.U0005", "SRC.SRC03.U0005", "SRC.SRC07.U0347"}
    unreadable = unit["text"] == "[UNREADABLE_OR_EMPTY]"
    reviewed = bool(statement_ids) and not broad and not unreadable
    status = "UNREADABLE" if unreadable else "COVERED" if reviewed else "PARTIAL"
    meaning = "REVIEWED" if reviewed else "PARTIAL" if broad and statement_ids else "NOT_REVIEWED"
    issue_ids = [] if reviewed else ["I02" if broad else "I04"]
    if unit["source_id"] == "SRC.SRC07" and not reviewed:
        issue_ids = unique(issue_ids + ["I06"])
    if unit["source_id"] in {"SRC.SRC04", "SRC.SRC05", "SRC.SRC06"} and not reviewed:
        issue_ids = unique(issue_ids + ["I03"])
    coverage.append({
        "id": pcid, "source_unit_id": uid, "status": status,
        "meaning_status": meaning,
        "meaning_note": "已将本单元具体业务含义写入陈述，仍待业务确认。" if reviewed else
                        "单元覆盖多条款/大表，仅审阅其中明确引用的内容。" if broad and statement_ids else
                        "已入来源台账，尚未逐单元形成可审阅业务含义。",
        "business_topic": "已审阅：" + "/".join(question_ids[:3]) if reviewed else "待分主题审阅",
        "business_meaning": "；".join(s["text"] for s in statements if s["id"] in statement_ids) if reviewed else "本单元尚未完成独立语义审阅。",
        "applicability": sources[unit["source_id"]]["source_role"] + "；以适用义务主体和权威等级为准",
        "statement_ids": statement_ids, "term_ids": term_ids, "question_ids": question_ids,
        "rule_ids": rule_ids, "case_ids": case_ids, "issue_ids": issue_ids,
        "reason": "形成了可回溯知识陈述。" if reviewed else "仅部分形成知识，或尚待业务含义审阅。",
    })

# Every partial provision points to an issue that explicitly lists it.
issue_index = {i["id"]: i for i in issues}
for row in coverage:
    for issue_id in row["issue_ids"]:
        issue_index[issue_id]["affects"] = unique(issue_index[issue_id]["affects"] + [row["id"]])

case_coverage = []
for q in questions:
    linked = [c["id"] for c in cases if q["id"] in c["question_ids"]]
    case_coverage.append({"question_id": q["id"], "case_ids": linked,
                          "not_applicable": [] if linked else [{"kind": "POSITIVE", "reason": "本轮尚无独立案例，需业务评审补充。"}],
                          "gap_ids": [i["id"] for i in issues if i["kind"] == "KNOWLEDGE_GAP" and q["id"] in i["affects"]]})

candidates = []
for q in questions:
    relevant = unique(ref for r in rules if q["id"] in r["question_ids"] for sid in r["statement_ids"]
                      for s in statements if s["id"] == sid for ref in s["source_unit_ids"])
    candidates.append({"id": "QC." + q["id"], "question": q["question"],
                       "origin": "SOURCE", "source_unit_ids": relevant[:6],
                       "disposition": "RETAINED", "target_question_ids": [q["id"]],
                       "reason": "由本轮源文的主体、标准、证据或流程问题归纳；见关联单元。", "issue_ids": []})
process_checks = [
    {"id": "PX01", "actor": "备案主体", "stage": "设立与变更备案", "concern": "主体、承诺免报、全体自然人和日期", "source_unit_ids": ["SRC.SRC01.U0005", "SRC.SRC06.U0137"], "question_ids": ["Q01", "Q02", "Q03", "Q04", "Q05", "Q10", "Q15"], "status": "COVERED", "reason": "3号令与指南构成备案链条；案例仍需真实业务复核。", "issue_ids": []},
    {"id": "PX02", "actor": "金融机构", "stage": "客户尽调与存续期", "concern": "识别、核实、风险措施及变化更新", "source_unit_ids": ["SRC.SRC02.U0009", "SRC.SRC02.U0047", "SRC.SRC02.U0075"], "question_ids": ["Q03", "Q05", "Q09", "Q11", "Q14"], "status": "COVERED", "reason": "12号令覆盖识别核实与持续维护。", "issue_ids": []},
    {"id": "PX03", "actor": "金融机构与BOMIS", "stage": "查询核对与差异反馈", "concern": "查询、差异归因、报告和异步终态", "source_unit_ids": ["SRC.SRC02.U0074", "SRC.SRC02.U0084", "SRC.SRC07.U0055"], "question_ids": ["Q12", "Q13", "Q15"], "status": "COVERED", "reason": "12号令给出义务，接口说明只给出系统交互。", "issue_ids": []},
]

digest = "sha256:" + hashlib.sha256(SOURCE.read_bytes()).hexdigest()
input_ref = {"artifact_id": data["request_id"], "content_version": "2026-09-23.fresh-full.1",
             "contract_version": "4.0.0", "path": str(SOURCE.relative_to(ROOT)), "digest": digest}
output = {
    "artifact_id": "A01-DOMAIN-KNOWLEDGE-2026-09-23-FULL",
    "content_version": "2026-09-23.fresh-full.1", "contract_version": "4.0.0",
    "stage": "domain-knowledge", "mode": "PRODUCE", "input_refs": [input_ref],
    "files": [], "evidence": [],
    "states": {"structure_checked": {"status": "NOT_EXECUTED", "evidence_ids": [], "reason": "待执行合同校验。"},
               "business_reviewed": {"status": "NOT_EXECUTED", "evidence_ids": [], "reason": "新稿尚未经业务负责人审阅。"}},
    "confirmation": {"status": "PENDING", "scope_ids": [q["id"] for q in questions], "evidence_ids": []},
    "issues": issues,
    "trace": [{"from_id": s["id"], "to_id": ref, "relation": "SUPPORTS", "basis": "陈述通过 source_unit_ids 回指本轮输入的来源单元。"}
              for s in statements for ref in s["source_ids"]] +
             [{"from_id": r["id"], "to_id": sid, "relation": "DEPENDS_ON", "basis": "业务规则取自所列陈述。"}
              for r in rules for sid in r["statement_ids"]],
    "content": {"scope": "仅以A01受益所有人/01业务输入的75份材料为来源台账；正文基于已逐条回读的主要制度、指南及业务问题材料形成，未回读单元在覆盖台账标明。范围包括备案主体、金融机构尽调、信托资管、证据时间、BOMIS核对和差异反馈。本稿待业务审阅，不是已批准结论。",
                "sources": data["sources"], "statements": statements, "terms": terms,
                "questions": questions, "rules": rules, "cases": cases,
                "case_coverage": case_coverage, "provision_coverage": coverage,
                "question_discovery": {"scope_question_ids": [q["id"] for q in questions],
                                       "candidates": candidates, "process_checks": process_checks}},
}
out_path = RUN / "output.json"
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"sources": len(sources), "units": len(units), "statements": len(statements),
                  "terms": len(terms), "questions": len(questions), "rules": len(rules),
                  "cases": len(cases), "reviewed_units": sum(c["meaning_status"] == "REVIEWED" for c in coverage)}, ensure_ascii=False))
