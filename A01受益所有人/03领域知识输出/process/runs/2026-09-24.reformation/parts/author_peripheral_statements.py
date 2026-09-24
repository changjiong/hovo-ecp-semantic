#!/usr/bin/env python3
"""Serialize reviewed peripheral-document Statement decisions."""

import json
from pathlib import Path


RUN = Path(__file__).resolve().parents[1]
AUTHORED = {
    "SRC.TXT027": {
        48: [("TIME", "文章转载的强制注销办法规定：公司自被强制注销登记之日起终止；判断注销后的客户主体状态须看生效时点。")],
        49: [("EXCEPTION", "强制注销登记不影响原公司股东、清算义务人的责任；主体终止不等于历史责任或关系当然消失。")],
        64: [("TIME", "转载的强制注销办法规定恢复公司登记决定作出后，主体恢复至强制注销登记前状态并公示；恢复登记不自动证明旧受益所有权关系仍然成立。")],
        71: [("CONTEXT", "文章转载的办法称分公司强制注销登记参照适用该办法；此处不解决总公司已注销但分支仍存续的受益所有人识别口径。")],
    },
    "SRC.TXT034": {
        27: [("CONTEXT", "二手客户尽调新规解读将法人或非法人组织客户的受益所有人识别核实列为客户尽调措施之一，并与客户身份、交易目的和持续尽调并列；具体义务须核对原规章。")],
        33: [("CONTEXT", "二手解读称在难以中断正常交易且风险可控时，可于建立业务关系后尽快完成受益所有人核实，未完成期间应有风险管理措施；这不是无条件延后核实授权。")],
        57: [("CONTEXT", "二手解读将受益所有人信息纳入客户身份资料及尽调记录保存范围；保存期限和具体范围须核对原规章。")],
        125: [("CONTEXT", "二手解读指出人寿保险保单受益人若为较高风险的法人或非法人组织，赔付时可能涉及识别并核实该受益人的受益所有人；不得把保险受益人与企业受益所有人混同。")],
        139: [("CONTEXT", "二手解读指出信托相关客户尽调需要了解信托业务、所有权和控制结构，并依规定识别信托受益所有人；具体身份和范围须以信托适用规范确认。")],
    },
    "SRC.TXT035": {
        12: [("CONTEXT", "同业文章转述的金融机构许可规则中，信托公司股东资质审查涉及穿透识别受益所有人，银行卡清算机构申请材料涉及实际控制人和受益所有人说明；该二手转述不能替代原规章。")],
        23: [("CONTEXT", "同业文章转述信托公司开展信托业务时需识别和记录信托受益所有人信息；具体适用范围与要求须回到原规章核验。")],
    },
    "SRC.TXT046": {
        11: [("CONTEXT", "同业监管动态文章记载《受益所有人信息备案指南（第二版）》于2026年1月30日公布；该时间为二手报道，应与指南封面和正式发布信息核对。")],
        47: [("CONTEXT", "同业文章概述金融机构受益所有人识别办法涉及识别核实流程、标准和差异反馈制度；具体规范以办法原文为准。")],
    },
    "SRC.TXT049": {
        29: [("CONTEXT", "厂商 AI 尽调演示的查询指令使用‘持股≥25%’筛选自然人；这是演示提示词，不是正式识别阈值，与规范来源口径须分开。")],
        33: [("CONTEXT", "厂商声称可自动合并直接和间接持股比例并筛出达到25%阈值的自然人；这是未经本次运行核验的产品能力声称，不能取代收益、表决或实际控制判断。")],
        41: [("CONTEXT", "厂商演示把股权冻结列为控制权不稳定的风险提示线索；该标签本身不能证明控制关系已经变化。")],
        67: [("CONTEXT", "厂商尽调演示把循环嵌套和交叉持股标为风险线索；是否需要加强措施须按正式规范及客户事实判断。")],
        68: [("CONTEXT", "厂商尽调演示把境外持股且无法核实登记信息标为风险线索；缺少境外权属证据不能自动认定最终自然人。")],
        69: [("CONTEXT", "厂商演示将上述结构风险直接输出为触发加强尽调条件；该自动结论为产品示例，不是经确认的机构风险决定。")],
        71: [("EVIDENCE", "厂商演示提出补充获取详细股权结构文件，以核实复杂持股路径；文件需求是演示建议，证据充分性仍需按客户情形判断。")],
        77: [("CONTEXT", "厂商演示提供监测股权结构变化的能力声称；本次未验证产品运行，不能把监测提示视为已完成金融机构持续识别。")],
    },
    "SRC.TXT050": {
        46: [("CONTEXT", "同业文章根据2025年银行年报观察，建设银行披露推进受益所有人信息报送；这是公开实践描述，不等于本机构已实施或完成报送。")],
    },
}
REASONS = {
    "SRC.TXT027": "强制注销文章其余内容主要规定公司登记机关的强制注销、异议和恢复程序，或为厂商链接；不形成受益所有人识别知识。",
    "SRC.TXT034": "文章其余内容是泛客户尽调、交易记录保存或不同金融产品的规定转述，超出本次受益所有人识别知识边界。",
    "SRC.TXT035": "文章其余内容为金融机构准入、反洗钱培训及泛化监管趋势，或厂商页脚；不作为本次受益所有人识别规则依据。",
    "SRC.TXT046": "文章其余内容是泛反洗钱政策动态、交叉推广链接和页脚；不提供独立受益所有人判断。",
    "SRC.TXT049": "文章其余内容是 AI/厂商尽调演示、泛风险筛查与营销说明；不能据演示输出形成受益所有人规则。",
    "SRC.TXT050": "文章其余内容是银行年报的泛反洗钱实践统计、营销及页脚；不提供本次识别规则或已确认案例。",
}


def main() -> None:
    data = json.loads((RUN / "input.json").read_text(encoding="utf-8"))
    rows = []
    found: dict[str, set[int]] = {source: set() for source in AUTHORED}
    for unit in data["source_units"]:
        source = unit["source_id"]
        if source not in AUTHORED:
            continue
        number = int(unit["unit_id"].rsplit("U", 1)[1])
        authored = AUTHORED[source].get(number, [])
        if authored:
            found[source].add(number)
        statements = [{
            "id": f"ST.{source.split('.')[-1]}.U{number:05d}.{offset:02d}",
            "text": text,
            "source_ids": [source],
            "source_unit_ids": [unit["unit_id"]],
            "basis": unit["text"],
            "origin": "SOURCE_STATED",
            "meaning_kind": kind,
            "review_status": "PENDING",
            "dispute_status": "UNCONTESTED",
            "conflict_ids": [],
            "supporting_statement_ids": [],
        } for offset, (kind, text) in enumerate(authored, start=1)]
        rows.append({
            "source_unit_id": unit["unit_id"],
            "status": "EXTRACTED" if statements else "OUT_OF_SCOPE",
            "reason": "与受益所有人业务状态相关的二手来源陈述，须核对原规章" if statements else REASONS[source],
            "statements": statements,
        })
    for source, authored in AUTHORED.items():
        if found[source] != authored.keys():
            raise ValueError(f"Missing selected SourceUnit in {source}")
    out = Path(__file__).with_name("statements_peripheral.json")
    out.write_text(json.dumps({"source_unit_results": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"sources": len(AUTHORED), "source_units": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
