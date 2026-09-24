#!/usr/bin/env python3
"""Serialize manually authored Statement Pass decisions for BUSINESS_SCOPE source.

The authored rows below are the semantic work. The code only expands schema fields.
"""

import json
from pathlib import Path


RUN = Path(__file__).resolve().parents[1]
SOURCE_ID = "SRC.TXT001"
AUTHORED = {
    3: [("CONTEXT", "本文是业务归纳，面向业务、合规和产品人员，不替代具体法规口径或机构操作规程。")],
    5: [("CONTEXT", "受益所有人识别要有依据地了解非自然人客户最终由谁拥有、实际控制或享有最终收益，并结合权利形成及变化理解客户风险。")],
    6: [("DEFINITION", "本文使用的受益所有人涵盖最终拥有、控制或享有收益的自然人，不仅是收取分红的人；日常‘最终受益人’在本文指向这一含义。")],
    7: [("EVIDENCE", "登记股东、法定代表人和组织形式可能不足以揭示多层持股、代持、表决权委托或合伙协议下的实际利益与控制关系；需要有证据和时间范围的关系还原。")],
    9: [("PROCEDURE", "识别客户背后的自然人应继续追溯直接股东，并综合所有权、收益权、表决权和实际控制关系。"), ("CRITERION", "法定代表人、直接股东、实际控制人与受益所有人可能重合也可能不同，不能直接互相替代。")],
    11: [("EVIDENCE", "客户声称国资背景或不存在其他实际控制人，需要材料核实；身份包装、虚假股权和未披露协议等疑点影响识别方法与调查深度。")],
    13: [("PROCEDURE", "同一自然人拥有或控制多个客户可作为关联交易、风险集中和资金往来分析的线索。"), ("EXCEPTION", "存在共同受益所有人本身不等于交易可疑或构成违规。")],
    15: [("TIME", "业务时点的权利状态与当前状态应区分；开户后股权、控制协议和人员变化可能改变识别结论，需保留历史并判断是否重新识别。")],
    17: [("PROCEDURE", "识别结果、证据和疑点应交相关岗位，用于补充材料、加强调查、调整风险评价或其他管理措施的判断。"), ("CRITERION", "受益所有人信息是业务决策输入，最终业务判断仍由有权限的人员和机构承担。")],
    19: [("TIME", "受益所有权关系形成日期是权利关系本身的重要属性，用于把人和权利置于业务发生时点理解，不能仅作为报告附注。")],
    21: [("TIME", "核查历史交易应使用交易发生时的所有权和控制关系，不能用当前受益所有人替代历史关系状态。"), ("PROHIBITION", "不能仅因当前受益所有人身份而直接认定其对历史交易负责。")],
    22: [("TIME", "客户备案、机构记录和外部数据可能反映不同时间的权利状态，形成日期与依据材料可帮助区分真实关系冲突、资料未更新与版本差异。")],
    23: [("PROCEDURE", "权利变化时应分别记录继续存在、已终止和新形成的关系，并关联新旧结果与依据材料以支持复核和审计。")],
    25: [("DEFINITION", "首次成为受益所有人的日期，是首次满足相应识别条件的时间。"), ("DEFINITION", "当前权利状态的形成日期，是当前比例、关系类型或控制安排对应的生效时间。"), ("DEFINITION", "权利关系终止日期，是某项已记录关系结束的时间。"), ("DEFINITION", "工商登记或公告日期，是相关信息登记或对外披露的时间。"), ("DEFINITION", "机构识别或核实日期，是机构完成调查与判断的时间。"), ("DEFINITION", "备案或更新日期，是信息提交或更新至备案系统的时间。")],
    26: [("TIME", "不同时间字段可能相同也可能不同；形成日期应结合适用规则和公司章程、合伙协议、股权转让协议、控制安排等生效材料判断。"), ("PROHIBITION", "不能默认用企业成立日、认缴出资日、查询日或工商变更日替代权利形成日期。")],
    28: [("CONTEXT", "示例中甲于2024年取得30%股权、2025年增至40%、机构2026年核实；首次达到识别条件、当前40%股权生效和机构核实分别是不同业务事实。")],
    29: [("PROCEDURE", "业务记录应保留权利比例和形成时间的演变，不能只存最新比例与核实年份。"), ("TIME", "对外填报形成日期，应按具体字段的适用口径选取并说明依据，不能把首次日期或最新变化日期统一套用所有场景。")],
    30: [("EVIDENCE", "形成日期尚无法确定时，应记录已取得证据、已知时间范围和待核事项并按流程补充确认，不应由系统默认日期制造确定性。")],
    32: [("EVIDENCE", "可用于业务判断的识别结果应让有权限人员复核自然人身份、使其被识别的权利、权利存续时间及结论可信依据。")],
    34: [("EVIDENCE", "识别结果应说明受益所有人身份、对应客户和必要的身份核实信息。"), ("EVIDENCE", "识别结果应说明权利关系类型、适用识别依据、比例或控制方式，以及客户至自然人的关系路径。"), ("TIME", "识别结果应说明关系形成、终止及历次变化和当前有效状态。"), ("EVIDENCE", "识别结果应保留材料来源、材料时间、生效依据、核实动作和判断理由。"), ("PROCEDURE", "识别结果应记录信息不一致、证据缺口、复核意见及待完成事项。")],
    35: [("EXCEPTION", "识别结果的信息组织要求不等于对所有客户无差别采集全部材料；具体采集范围和措施强度应结合客户类型、风险和适用要求确定。")],
    37: [("PROCEDURE", "业务流程先确认客户类型和风险以选择识别方法，再收集材料、分析权利关系及形成时间、核实自然人身份和权利状况。"), ("PROCEDURE", "对适用客户核对备案信息并分析差异，由相应岗位复核、更新、反馈或报告，归档后持续关注可能改变结论的情况。")],
    38: [("TIME", "机构需同时维护当前可用结果与可还原历史；只保留最新人名无法追溯，只保留历史报告而不更新业务系统则会继续使用过时信息。")],
    40: [("CRITERION", "业务成效包括避免遗漏关键自然人、解释权利及形成时间、还原业务时点关系、变化或差异发生后按流程处理并留痕。")],
    41: [("PROCEDURE", "数据平台、图谱、RPA和AI可辅助查询、计算、材料整理、变化提示和报告初稿。"), ("EVIDENCE", "无法核实的代持或控制安排仍属证据缺口，系统输出人名不等于已完成核实。"), ("EXCEPTION", "被识别为受益所有人不意味着自然人违法，也不当然承担企业全部历史行为责任。")],
    42: [("CRITERION", "受益所有人管理应形成可核实、可追溯、可更新的业务记录，说明自然人何时通过何种关系拥有、控制客户或享有收益，以及机构判断依据和疑点处理。")],
}


def main() -> None:
    input_data = json.loads((RUN / "input.json").read_text(encoding="utf-8"))
    results = []
    for unit in input_data["source_units"]:
        if unit["source_id"] != SOURCE_ID:
            continue
        number = int(unit["unit_id"].rsplit("U", 1)[1])
        authored = AUTHORED.get(number, [])
        statements = []
        for offset, (meaning_kind, text) in enumerate(authored, start=1):
            statements.append({
                "id": f"ST.TXT001.U{number:05d}.{offset:02d}",
                "text": text,
                "source_ids": [SOURCE_ID],
                "source_unit_ids": [unit["unit_id"]],
                "basis": unit["text"],
                "origin": "SOURCE_STATED",
                "meaning_kind": meaning_kind,
                "review_status": "PENDING",
                "dispute_status": "UNCONTESTED",
                "conflict_ids": [],
                "supporting_statement_ids": [],
            })
        results.append({
            "source_unit_id": unit["unit_id"],
            "status": "EXTRACTED" if statements else "NO_BUSINESS_MEANING",
            "reason": "依据当前来源单元逐项拆解业务含义" if statements else "标题或元信息，不单独表达可判断的业务含义",
            "statements": statements,
        })
    if len(results) != 42:
        raise ValueError("Unexpected BUSINESS_SCOPE unit count")
    out = Path(__file__).with_name("statements_scope.json")
    out.write_text(json.dumps({"source_unit_results": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
