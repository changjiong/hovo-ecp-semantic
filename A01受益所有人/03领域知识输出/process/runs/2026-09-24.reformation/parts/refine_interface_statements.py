#!/usr/bin/env python3
"""Apply manually authored semantic splits to selected BOMIS interface SourceUnits."""

import json
from pathlib import Path


RUN = Path(__file__).resolve().parents[1]
SOURCE_ID = "SRC.SRC07"
AUTHORED = {
    50: [("PROCEDURE", "BOMIS 在接收、保存和处理备案信息基础上，向有关系统及义务机构提供备案主体受益所有人信息核验和查询，并接收、反馈差异报告。"), ("CONTEXT", "接口文档称系统同时支持统计分析与监测预警，以改善信息充分性、准确性和及时性；这属于系统设计目标，不是已验证运行成效。")],
    55: [("PROCEDURE", "BOMIS 对提交的业务先入队并即时应答，业务处理完成后再异步推送结果；即时应答不等于最终业务处理成功。"), ("PROCEDURE", "核验或差异报告提交未通过时，反馈报文提示具体原因；义务机构可查询差异报告审批进度。")],
    110: [("DEFINITION", "接口分别提供收益权比例、收益权关系形成日期和终止日期字段，不应把比例与时间合并成单一当前值。"), ("DEFINITION", "接口分别提供表决权比例、表决权关系形成日期和终止日期字段；收益权与表决权的时间字段不能互相替代。"), ("DEFINITION", "接口记录实际控制上一层市场主体名称与统一社会信用代码，以及有关高级管理人员职位信息。")],
    122: [("PROCEDURE", "BOMIS 支持单笔实时核验和批量核验；义务机构的每日核验上限是由人民银行按机构规模设定的参数 X，而非本文件给出的固定数量。"), ("EXCEPTION", "批量报文部分备案主体触及当日上限时，该批次仍全部核验，后续报文不再处理；计次按批次中的备案主体数计算。")],
    128: [("TIME", "批量核验在夜间跑批处理，单条批量报文最多包含100家备案主体。")],
    133: [("PROCEDURE", "义务机构查询备案主体信息前须先核验；未备案的经营主体不可查询。"), ("TIME", "每个核验流水号的有效期由参数 X 控制，文档给出的初始值为180天，不能把它写成永恒固定期限。")],
    139: [("PROCEDURE", "核验结果有差异时，义务机构可先查询备案主体信息、线下核实，再按查询反馈提交差异报告。"), ("EXCEPTION", "核验结果无差异但后续查询发现其他信息差异时，仍可根据查询反馈提交差异报告；‘核验一致’不排除其他信息差异。")],
    142: [("PROCEDURE", "备案主体信息更新后，该主体下所有待审核差异报告全部终止，系统下发终止处理结果；待审核报告不能继续当作有效在办。")],
    216: [("DEFINITION", "BOMIS 核验一致表示所有受益所有人均核对一致；不一致表示至少一人不一致；经营主体未备案表示查询不到备案主体。")],
    218: [("DEFINITION", "个人信息要素不一致反馈指出有差异的要素，不返回具体差异值。"), ("DEFINITION", "‘义务机构受益所有人遗漏’表示 BOMIS 中存在但机构上传名单中不存在的人，反馈遗漏人数和人员信息。"), ("DEFINITION", "‘义务机构受益所有人多出’表示机构上传名单中存在但 BOMIS 中不存在的人，反馈多出人数和人员信息。"), ("DEFINITION", "系统还区分承诺免报与国有公司填报类型下的受益所有人空列表情形；空列表不能不看填报类型就解释为资料缺失。")],
    265: [("PROCEDURE", "查询报文的用途声明影响反馈字段展示：声明用于履行反洗钱和反恐怖融资义务时返回加密传输的明文要素，否则返回掩码要素；这是接口返回规则，不等于自动授予查询权限。")],
    279: [("PROCEDURE", "查询反馈的身份要素范围随核验提交内容而变：只提交姓名、性别、国籍、出生日期四要素时只返回四要素，提交含证件类型和号码的六要素时才返回六要素。"), ("PROCEDURE", "查询用途声明决定反馈明文加密还是掩码；缺少适用声明时不能把掩码结果误当成原始明文信息。")],
    324: [("PROCEDURE", "备案主体历史信息查询只返回受益所有人的姓名、性别、国籍、出生日期四项基本信息。"), ("PROCEDURE", "历史查询的用途声明决定结果明文加密或掩码发送；历史查询接口的个人要素范围不等同于当前信息查询。")],
    331: [("PROCEDURE", "差异报告提交报文用于义务机构完成线下核实后上报差异部分信息；查询或核验结果本身不等于已完成线下核实。")],
    343: [("PROCEDURE", "退回补充材料的差异报告可重新提交，并更新差异分析报告、证明材料及原差异信息。")],
    347: [("PROCEDURE", "非重大差异报备要求统一社会信用代码和差异分析报告，证明材料选传；报送差异项键即可，不要求填报具体差异值。"), ("CONTEXT", "接口将非重大差异报备等四类列为报备型差异报告，此分类是报文填报约束，不足以单独证明差异在法规意义上的重大性。")],
    351: [("PROCEDURE", "补充类差异报告不得传差异项列表和原受益所有人信息；须传现受益所有人信息，操作类型限新增。")],
    353: [("PROCEDURE", "接口对补充类报文的受益所有人数量和关系类型设定随备案主体填报类型变化的条件，不能将不同填报类型混用同一校验规则。")],
}


def main() -> None:
    path = Path(__file__).with_name("statements_interface.json")
    part = json.loads(path.read_text(encoding="utf-8"))
    units = {
        item["unit_id"]: item
        for item in json.loads((RUN / "input.json").read_text(encoding="utf-8"))["source_units"]
        if item["source_id"] == SOURCE_ID
    }
    changed = 0
    for row in part["source_unit_results"]:
        number = int(row["source_unit_id"].rsplit("U", 1)[1])
        authored = AUTHORED.get(number)
        if authored is None:
            continue
        unit = units[row["source_unit_id"]]
        row["status"] = "EXTRACTED"
        row["reason"] = "按接口语义拆分，保留系统合同与业务规范边界"
        row["statements"] = [{
            "id": f"ST.SRC07.U{number:04d}.{offset:02d}",
            "text": text,
            "source_ids": [SOURCE_ID],
            "source_unit_ids": [row["source_unit_id"]],
            "basis": unit["text"],
            "origin": "SOURCE_STATED",
            "meaning_kind": meaning_kind,
            "review_status": "PENDING",
            "dispute_status": "UNCONTESTED",
            "conflict_ids": [],
            "supporting_statement_ids": [],
        } for offset, (meaning_kind, text) in enumerate(authored, start=1)]
        changed += 1
    if changed != len(AUTHORED):
        raise ValueError("A selected interface SourceUnit was not found")
    # Protocol/field-table excerpts are retained in input.json, but they are not
    # semantic business Statements. Only explicitly reviewed interface behavior
    # above enters the domain knowledge formation chain.
    excluded = 0
    for row in part["source_unit_results"]:
        if row["status"] != "EXTRACTED":
            continue
        raw = [st for st in row["statements"] if st["meaning_kind"] == "SOURCE_EXCERPT"]
        if not raw:
            continue
        row["statements"] = [st for st in row["statements"] if st["meaning_kind"] != "SOURCE_EXCERPT"]
        if not row["statements"]:
            row["status"] = "OUT_OF_SCOPE"
            row["reason"] = "接口报文字段、传输/安全协议或版本记录原文；保留于解析输入，不作为独立业务语义陈述"
        excluded += len(raw)
    path.write_text(json.dumps(part, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"semantic_units_refined": changed, "raw_excerpts_excluded": excluded}, ensure_ascii=False))


if __name__ == "__main__":
    main()
