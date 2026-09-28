#!/usr/bin/env python3
"""Regenerate the practical UBO core using Domain Model 0.9.0 semantics."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[5]
STAGE = ROOT / "A01受益所有人/04领域模型输出"
KNOWLEDGE = ROOT / "A01受益所有人/03领域知识输出/output.json"
PRIOR_BUILDER = STAGE / "process/runs/2026-09-24.practical-ubo/build_model.py"
KNOWLEDGE_SHA256 = "d09b3b448b3077d84c41fd167cf73030ae7b0b902c8767902ea98676131585e1"

QUESTION_IDS = [
    "Q.A01.S13", "Q.A01.S14", "Q.A01.S16", "Q.A01.S17", "Q.A01.S18",
    "Q.A01.S20", "Q.A01.S21", "Q.A01.S22", "Q.A01.S23", "Q.A01.S24",
    "Q.A01.S25", "Q.A01.S26", "Q.A01.S28", "Q.A01.S29", "Q.A01.S56",
    "Q.A01.S57", "Q.A01.S60", "Q.A01.S61", "Q.A01.S62",
]
RULE_IDS = [
    "RULE.A01.KF.EQUITY", "RULE.A01.KF.NOMINEE",
    "RULE.A01.KF.RETURNS_VOTES", "RULE.A01.KF.CONTROL",
    "RULE.A01.KF.FALLBACK", "RULE.A01.KF.IDENTITY", "RULE.A01.KF.DATES",
]
TYPE_IDS = {
    "M.Organization", "M.NaturalPerson", "M.Evidence", "M.OwnershipLink",
    "M.EquityPath", "M.EquityPathStep", "M.OtherRight",
    "M.ControlArrangement", "M.CandidateAssessment",
    "M.CandidatePopulationAssessment", "M.IdentificationReviewer",
    "M.UBOQualification", "M.IdentificationConclusion",
}
JUDGMENT_IDS = {
    "M.AssessOwnershipPaths", "M.ReviewCandidateEvidence",
    "M.ReviewCandidatePopulation", "M.AssessActualControl",
    "M.SelectFallbackManager",
}
RULE_REASONS = {
    "RULE.A01.KF.EQUITY": "权益边、穿透路径及判断时点是可复用结构；完整路径的最终比例和25%达标是稳定领域判断。路径完整性须由证据确认，不能由计算式自证。",
    "RULE.A01.KF.NOMINEE": "名义持有和最终收益、表决、控制可指向不同自然人；须分别保留安排与证据，最终归属依协议效力和实际履行裁定。",
    "RULE.A01.KF.RETURNS_VOTES": "最终收益权和表决权是独立的权利事实；在标准一未入选时，任一权利达到25%构成稳定判断，重复归类不能增加人数。",
    "RULE.A01.KF.CONTROL": "控制安排的权限、作用、共同机制和有效期间是稳定事实；是否构成实际控制属于需要证据裁定的领域判断。",
    "RULE.A01.KF.FALLBACK": "候选全集完整性和前三项标准均无人符合是组织级事实；仅当前提明确成立，才能判断备位资格和实际管理人选。",
    "RULE.A01.KF.IDENTITY": "现实自然人身份、权利事实和各自证据必须分离；身份同一性及证据可靠性决定候选结论能否成立，字段齐全并不充分。",
    "RULE.A01.KF.DATES": "权利形成、变化、终止和判断时点属于关系本身的时间事实；首次达标与当前状态不可互相覆盖，未知精度不得补成具体日期。",
}


def load_prior_builder():
    spec = importlib.util.spec_from_file_location("a01_prior_model_builder", PRIOR_BUILDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.QUESTION_IDS = QUESTION_IDS
    module.RULE_IDS = RULE_IDS
    module.SCOPE = (
        "金融机构对一般法人、非法人组织客户识别自然人受益所有人的核心领域："
        "直接及间接权益、代持后的最终权利、收益/表决权、实际控制、组织级备位、"
        "自然人身份与权利证据、权利形成及变化时点。显式子集不包含备案办理、信托、"
        "资管、BOMIS、差异分析，也不扩建国资特例、分支、免识别/简化路由、"
        "风险措施和机构内部工作流。"
    )
    module.question_process_ids = lambda _question_id: []
    return module


def main():
    raw = KNOWLEDGE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != KNOWLEDGE_SHA256:
        raise SystemExit("固定领域知识摘要已变化，停止生成。")
    knowledge = json.loads(raw)
    if knowledge["contract_version"] != "5.0.0" or knowledge["content_version"] != "2026-09-24.draft.1":
        raise SystemExit("固定领域知识版本已变化，停止生成。")

    builder = load_prior_builder()
    request, model = builder.build_model(knowledge, None)
    model["dsl_version"] = "2.1.0"
    model["content_version"] = "2026-09-24.practical-ubo-core.2"
    model["name"] = "受益所有人识别核心领域模型"
    model["types"] = [item for item in model["types"] if item["id"] in TYPE_IDS]
    model["judgments"] = [item for item in model["judgments"] if item["id"] in JUDGMENT_IDS]
    model["temporal"] = []
    model["processes"] = []
    for item in model["types"]:
        if item["id"] == "M.Organization":
            item["description"] = "受益所有人识别的目标组织或权益链中的中间组织。"
            item["why_object"] = "目标组织与中间持股组织具有独立身份；权益路径必须明确每段指向的组织。"
            item["counterexamples"] = ["名称相同但登记身份不同的组织不能合并为同一主体。"]
            item["basis_ids"] = ["TERM.A01.KF.02", "RULE.A01.KF.EQUITY"]
            item["fields"] = [field for field in item["fields"] if field["name"] not in {"organization_form", "state_ownership_status"}]
        if item["id"] == "M.Evidence":
            item["description"] = "支持自然人身份、组织身份、权利关系或有效期间的可定位来源记录。"
            item["business_sentence"] = "识别人员用可定位材料支持或质疑一个特定身份、权利事实及其有效期间。"
            item["basis_ids"] = [basis for basis in item["basis_ids"] if basis != "RULE.A01.KF.RISK"]
        if item["id"] == "M.CandidateAssessment":
            for field in item["fields"]:
                if field["name"] == "evidence":
                    field["description"] = "支持身份、权益、收益/表决及控制事实的来源材料。"
        if item["id"] == "M.IdentificationReviewer":
            item["description"] = "承担自然人身份、权利事实和识别结论复核责任的机构人员角色。"
        if item["id"] == "M.IdentificationConclusion":
            item["fields"] = [field for field in item["fields"] if field["name"] != "route_assessment"]
            item["description"] = "针对一个目标组织和判断时点形成的自然人识别结果及未决事项。"
            for field in item["fields"]:
                if field["name"] == "target_organization":
                    field["description"] = "受益所有人识别的目标组织。"
    for item in model["judgments"]:
        item["question_ids"] = [question_id for question_id in item["question_ids"] if question_id in QUESTION_IDS]
        if item["id"] == "M.ReviewCandidateEvidence":
            item["criteria"] = [criterion for criterion in item["criteria"] if "低风险采信" not in criterion]
            item["required_evidence"] = [
                evidence.replace("、冲突与风险取舍记录", "及冲突处理记录")
                for evidence in item["required_evidence"]
            ]
    for row in model["question_coverage"]:
        row["process_ids"] = []
        row["reason"] = (
            "核心识别结构和判断已承接；关联的上游OPEN事项继续保持未决。"
            if row["gap_ids"] else "由稳定事实、权利关系和领域判断承接，不依赖工作流。"
        )
    for issue in model["issues"]:
        issue["affects"] = [
            identifier for identifier in issue["affects"]
            if not identifier.startswith("M.")
        ]
        if issue["id"] == "M.Gap.DatedPublishing":
            issue["statement"] = (
                "上游备案期限事项与权利形成日规则共享来源陈述，合同要求继续追溯；"
                "备案期限本身不进入本模型，也不改变权利生效日的判断。"
            )
            issue["recommendation"] = "由领域知识阶段另行处理备案期限口径；本模型只核权利生效证据和日期精度。"
            issue["until_resolved"] = "备案期限保持上游OPEN；不得把登记、披露或备案日替代权利形成日。"
        if issue["id"] == "M.Gap.EvidenceConflict":
            issue["statement"] = (
                "具体客户的代持效力、最终权利归属或实际控制证据可能冲突；"
                "未取得并核对案件材料前，不确认受影响自然人及关系形成时点。"
            )
    for row in model["rule_coverage"]:
        row["modeling_classification"] = ["CORE_STRUCTURE", "DOMAIN_DECISION"]
        row["reason"] = RULE_REASONS[row["knowledge_rule_id"]]
        row["gap_ids"] = [
            issue["id"] for issue in model["issues"]
            if row["knowledge_rule_id"] in issue["affects"]
        ]
        row["status"] = "PARTIAL" if row["gap_ids"] else "MODELED"
        for facet in row["facets"].values():
            facet["explanation"] = "仅承接自然人识别所需的稳定事实或判断；备案、机构操作和风险治理口径仍留在固定领域知识。"
    request["request_id"] = "A01.DomainModel.PracticalUBOCore.Request.2026-09-24"

    class NoAliasSafeDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

    (STAGE / "input.json").write_text(json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (STAGE / "model.yaml").write_text(
        yaml.dump(model, Dumper=NoAliasSafeDumper, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    print(json.dumps({
        "knowledge_digest": "sha256:" + KNOWLEDGE_SHA256,
        "questions": len(model["question_coverage"]),
        "rules": len(model["rule_coverage"]),
        "types": len(model["types"]),
        "judgments": len(model["judgments"]),
        "cases": len(model["case_explanations"]),
        "open_issues": len(model["issues"]),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
