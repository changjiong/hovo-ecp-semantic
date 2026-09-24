#!/usr/bin/env python3
"""Serialize reviewed source-level scope decisions into SourceUnit rows.

Selected derivative-summary units are kept as secondary question/conflict
clues; they are never promoted to independent normative authority.
"""

import json
from pathlib import Path


RUN = Path(__file__).resolve().parents[1]
REASONS = {
    "SRC.TXT021": "此文件是同一批文章的二次分类摘要，不是独立原始业务事实或已确认机构口径；相关原文文章仍逐篇处理。",
    "SRC.TXT022": "此文件是同一批文章的分类索引表，不是独立原始业务事实或已确认机构口径；相关原文文章仍逐篇处理。",
    "SRC.TXT029": "本文是反洗钱个人处罚统计，受益所有人仅见延伸链接或产品页脚；不表达本次受益所有人识别判断。",
    "SRC.TXT031": "本文讨论律师行业双向诈骗治理，受益所有人仅见产品页脚；超出本次识别知识范围。",
    "SRC.TXT033": "本文是反电诈受害人案例白皮书，受益所有人仅见产品页脚；不作为受益所有人识别案例。",
    "SRC.TXT036": "本文是研讨会邀请，提及受益所有人议题但未提供问题答案、案例事实或形成的作业口径。",
    "SRC.TXT038": "本文是研讨会活动回顾，提及受益所有人议题但未公开具体案例事实或可复核判断。",
    "SRC.TXT044": "本文列举2026年2月FATF黑灰名单，受益所有人仅见产品页脚；名单风险判断不属于本次识别规则。",
    "SRC.TXT054": "本文讨论对外制裁阻断措施和商业数据库，没有受益所有人识别含义。",
    "SRC.TXT060": "本文讨论出口管制及政府采购名单，没有受益所有人识别含义。",
    "SRC.TXT061": "本文列举2026年6月FATF黑灰名单，受益所有人仅见产品页脚；名单风险判断不属于本次识别规则。",
}
AUTHORED = {
    "SRC.TXT021": {
        16: [("CONTEXT", "二次分类摘要区分企业备案、金融机构独立识别核实及 BOMIS 查询核对；已有备案不等于金融机构已完成核实。")],
        17: [("CONTEXT", "二次分类摘要提示识别前须区分客户组织形式和风险，国企、简化或豁免资格需要证据，单查到国有股东不足以定性。")],
        18: [("CONTEXT", "二次分类摘要指出持股计算不能代替收益、表决、协议或联合控制识别；产品推荐顺序不等于排除其他自然人。")],
        19: [("EVIDENCE", "二次分类摘要要求结果之外保留权利路径、识别标准、形成时间、材料和核实过程；单一查询截图不能证明全部权利与控制。")],
        20: [("PROCEDURE", "二次分类摘要提出差异先比较和查因，再补证、判断、审核、处理、留痕；字段不同不等于机械报送。")],
        31: [("CONTEXT", "二次分类摘要列出草案/正式版存量期限、发布时间、30日/30工作日、国企查询未命中、记录保存期限、重大变化人数指标等二手材料间冲突；这些只是待核线索，不能独立确立规范结论。")],
    },
}


def main() -> None:
    data = json.loads((RUN / "input.json").read_text(encoding="utf-8"))
    rows = []
    for unit in data["source_units"]:
        reason = REASONS.get(unit["source_id"])
        if reason is None:
            continue
        number = int(unit["unit_id"].rsplit("U", 1)[1])
        authored = AUTHORED.get(unit["source_id"], {}).get(number, [])
        statements = [{
            "id": f"ST.{unit['source_id'].split('.')[-1]}.U{number:05d}.{offset:02d}",
            "text": text,
            "source_ids": [unit["source_id"]],
            "source_unit_ids": [unit["unit_id"]],
            "basis": unit["text"],
            "origin": "SOURCE_STATED",
            "meaning_kind": kind,
            "review_status": "PENDING",
            "dispute_status": "OPEN" if number == 31 else "UNCONTESTED",
            "conflict_ids": [],
            "supporting_statement_ids": [],
        } for offset, (kind, text) in enumerate(authored, start=1)]
        rows.append({
            "source_unit_id": unit["unit_id"],
            "status": "EXTRACTED" if statements else "OUT_OF_SCOPE",
            "reason": "二次分类摘要仅作业务问题和来源冲突线索，不独立证明规范结论" if statements else reason,
            "statements": statements,
        })
    out = Path(__file__).with_name("statements_out_of_scope.json")
    out.write_text(json.dumps({"source_unit_results": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"sources": len(REASONS), "source_units": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
