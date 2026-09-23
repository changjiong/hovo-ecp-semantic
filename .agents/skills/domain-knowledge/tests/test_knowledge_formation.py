#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_ROOT))

from knowledge_formation import (
    validate_audit_pass,
    validate_statement_pass,
    validate_synthesis_pass,
)


def source(source_id: str, role: str):
    return {"source_id": source_id, "source_role": role}


def unit(unit_id: str, source_id: str):
    return {"unit_id": unit_id, "source_id": source_id}


def statement(statement_id: str, source_id: str, unit_id: str):
    return {
        "id": statement_id,
        "text": "业务含义",
        "source_ids": [source_id],
        "source_unit_ids": [unit_id],
        "basis": "fixture",
        "origin": "SOURCE_STATED",
        "meaning_kind": "CRITERION",
        "review_status": "PENDING",
        "dispute_status": "UNCONTESTED",
        "conflict_ids": [],
        "supporting_statement_ids": [],
    }


def question():
    return {
        "id": "Q1",
        "question": "如何判断？",
        "topic": "识别",
        "consumer": "业务人员",
        "decision_use": "形成判断",
        "unknown_policy": "UNKNOWN",
    }


def rule(*, rule_class="INTERPRETIVE", impact="HIGH", statement_id="S1", case_ids=None):
    return {
        "id": "R1",
        "statement_ids": [statement_id],
        "question_ids": ["Q1"],
        "name": "实际控制判断",
        "rule_class": rule_class,
        "impact": impact,
        "scope": "法人或非法人组织",
        "preconditions": "未满足第一标准",
        "conditions": "结合具体支配事实判断",
        "result": "形成控制判断",
        "exceptions": "职位不是当然证明",
        "missing_evidence": "保持UNKNOWN",
        "effective_period": "控制事实有效期间",
        "authority": "来源陈述",
        "origin": "INFERRED",
        "review_status": "PENDING",
        "dispute_status": "UNCONTESTED",
        "conflict_ids": [],
        "business_conclusion": "实际控制必须由实质支配事实支持。",
        "required_facts": ["人事任免", "重大决策", "财务或重要资产支配"],
        "decision_steps": ["先排除标准一", "再核实具体控制事实", "证据不足保持UNKNOWN"],
        "evidence_requirements": ["章程、协议、决议或实际行为证据"],
        "non_sufficient_facts": ["第一大股东", "法定代表人", "创始人", "亲属关系", "第三方平台标签"],
        "unknown_behavior": "缺治理与行为证据时保持UNKNOWN并转核实，不写FALSE。",
        "human_boundary": "来源冲突或控制事实不足时由有权限人员复核。",
        "case_ids": case_ids or ["C1"],
    }


def case(*, origin="SYNTHETIC_PROBE", source_ids=None):
    return {
        "id": "C1",
        "question_ids": ["Q1"],
        "rule_ids": ["R1"],
        "case_origin": origin,
        "validation_role": "MISSING_EVIDENCE",
        "input_facts": ["只有第三方实际控制人标签，缺章程协议决议。"],
        "expected": "保持实际控制UNKNOWN并补证。",
        "forbidden": "不得写FALSE，也不得直接进入管理人员兜底。",
        "source_ids": source_ids or [],
        "reasoning": "第三方标签是线索，不足以单独证明或否定实际控制。",
    }


class KnowledgeFormationRegressionTest(unittest.TestCase):
    def test_fresh_run_cannot_drop_expert_source_unit(self):
        request = {
            "sources": [
                source("SRC.norm", "NORMATIVE_RULE"),
                source("SRC.expert", "EXPERT_KNOWLEDGE"),
            ],
            "source_units": [
                unit("SRC.norm.U1", "SRC.norm"),
                unit("SRC.expert.U1", "SRC.expert"),
            ],
        }
        payload = {
            "formation_version": "1.0.0",
            "pass": "statement_pass",
            "source_unit_results": [
                {
                    "source_unit_id": "SRC.norm.U1",
                    "status": "EXTRACTED",
                    "reason": "有规范含义",
                    "statements": [statement("S1", "SRC.norm", "SRC.norm.U1")],
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "every SourceUnit"):
            validate_statement_pass(payload, request)

    def test_thin_high_impact_rule_is_rejected(self):
        request = {
            "sources": [source("SRC.norm", "NORMATIVE_RULE")],
            "source_units": [unit("SRC.norm.U1", "SRC.norm")],
        }
        sp = {
            "source_unit_results": [{
                "source_unit_id": "SRC.norm.U1",
                "status": "EXTRACTED",
                "reason": "有含义",
                "statements": [statement("S1", "SRC.norm", "SRC.norm.U1")],
            }]
        }
        qp = {"questions": [question()]}
        thin = rule()
        thin["required_facts"] = []
        synthesis = {
            "formation_version": "1.0.0",
            "pass": "knowledge_synthesis",
            "terms": [{"id": "T1", "statement_ids": ["S1"]}],
            "rules": [thin],
            "cases": [case()],
            "issues": [],
        }
        with self.assertRaisesRegex(ValueError, "HIGH impact rule"):
            validate_synthesis_pass(synthesis, sp, qp, request)

    def test_operating_policy_requires_enterprise_cognition_source(self):
        request = {
            "sources": [source("SRC.norm", "NORMATIVE_RULE")],
            "source_units": [unit("SRC.norm.U1", "SRC.norm")],
        }
        sp = {"source_unit_results": [{
            "source_unit_id": "SRC.norm.U1",
            "status": "EXTRACTED",
            "reason": "有含义",
            "statements": [statement("S1", "SRC.norm", "SRC.norm.U1")],
        }]}
        qp = {"questions": [question()]}
        synthesis = {
            "formation_version": "1.0.0",
            "pass": "knowledge_synthesis",
            "terms": [{"id": "T1", "statement_ids": ["S1"]}],
            "rules": [rule(rule_class="OPERATING_POLICY")],
            "cases": [case()],
            "issues": [],
        }
        with self.assertRaisesRegex(ValueError, "OPERATING_POLICY"):
            validate_synthesis_pass(synthesis, sp, qp, request)

    def test_expert_backed_operating_policy_is_allowed(self):
        request = {
            "sources": [source("SRC.expert", "EXPERT_KNOWLEDGE")],
            "source_units": [unit("SRC.expert.U1", "SRC.expert")],
        }
        sp = {"source_unit_results": [{
            "source_unit_id": "SRC.expert.U1",
            "status": "EXTRACTED",
            "reason": "正式专家口径",
            "statements": [statement("S1", "SRC.expert", "SRC.expert.U1")],
        }]}
        qp = {"questions": [question()]}
        synthesis = {
            "formation_version": "1.0.0",
            "pass": "knowledge_synthesis",
            "terms": [{"id": "T1", "statement_ids": ["S1"]}],
            "rules": [rule(rule_class="OPERATING_POLICY")],
            "cases": [case()],
            "issues": [],
        }
        validate_synthesis_pass(synthesis, sp, qp, request)


    def test_semantic_depth_block_is_a_valid_audit_but_not_pass(self):
        request = {
            "sources": [source("SRC.norm", "NORMATIVE_RULE")],
            "source_units": [unit("SRC.norm.U1", "SRC.norm")],
        }
        synthesis = {
            "rules": [rule()],
        }
        qp = {"questions": [question()]}
        audit = {
            "formation_version": "1.0.0",
            "pass": "knowledge_audit",
            "audit_status": "BLOCKED",
            "blocking_codes": ["SEMANTIC_DEPTH_INSUFFICIENT"],
            "findings": [{
                "id": "F1",
                "kind": "SEMANTIC_DEPTH",
                "severity": "BLOCK",
                "code": "SEMANTIC_DEPTH_INSUFFICIENT",
                "affects": ["R1"],
                "statement": "规则只有形式字段，没有足够业务判断深度。",
                "recommendation": "补充独立控制事实、非充分事实、UNKNOWN和人工边界。",
            }],
            "rule_audits": [{
                "rule_id": "R1",
                "impact_calibration": "PASS",
                "semantic_depth": "BLOCK",
                "granularity": "PASS",
                "counterfactual": "PASS",
                "contradiction": "PASS",
                "finding_ids": ["F1"],
            }],
            "provision_coverage": [{"source_unit_id": "SRC.norm.U1"}],
            "case_coverage": [{"question_id": "Q1"}],
            "issues": [],
        }
        validate_audit_pass(audit, synthesis, request, qp)

    def test_semantic_depth_failure_cannot_be_reported_as_pass(self):
        request = {
            "sources": [source("SRC.norm", "NORMATIVE_RULE")],
            "source_units": [unit("SRC.norm.U1", "SRC.norm")],
        }
        synthesis = {"rules": [rule()]}
        qp = {"questions": [question()]}
        audit = {
            "formation_version": "1.0.0",
            "pass": "knowledge_audit",
            "audit_status": "PASS",
            "blocking_codes": [],
            "findings": [],
            "rule_audits": [{
                "rule_id": "R1",
                "impact_calibration": "PASS",
                "semantic_depth": "BLOCK",
                "granularity": "PASS",
                "counterfactual": "PASS",
                "contradiction": "PASS",
                "finding_ids": [],
            }],
            "provision_coverage": [{"source_unit_id": "SRC.norm.U1"}],
            "case_coverage": [{"question_id": "Q1"}],
            "issues": [],
        }
        with self.assertRaisesRegex(ValueError, "require audit_status=BLOCKED"):
            validate_audit_pass(audit, synthesis, request, qp)

    def test_synthetic_probe_cannot_claim_source_authority(self):
        request = {
            "sources": [source("SRC.norm", "NORMATIVE_RULE")],
            "source_units": [unit("SRC.norm.U1", "SRC.norm")],
        }
        sp = {"source_unit_results": [{
            "source_unit_id": "SRC.norm.U1",
            "status": "EXTRACTED",
            "reason": "有含义",
            "statements": [statement("S1", "SRC.norm", "SRC.norm.U1")],
        }]}
        qp = {"questions": [question()]}
        bad_case = case(source_ids=["SRC.norm"])
        synthesis = {
            "formation_version": "1.0.0",
            "pass": "knowledge_synthesis",
            "terms": [{"id": "T1", "statement_ids": ["S1"]}],
            "rules": [rule()],
            "cases": [bad_case],
            "issues": [],
        }
        with self.assertRaisesRegex(ValueError, "synthetic probe"):
            validate_synthesis_pass(synthesis, sp, qp, request)


if __name__ == "__main__":
    unittest.main()
