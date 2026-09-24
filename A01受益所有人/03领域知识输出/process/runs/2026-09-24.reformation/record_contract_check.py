#!/usr/bin/env python3
"""Bind a passing structural validation record to the rendered draft."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
OUTPUT = ROOT / "A01受益所有人/03领域知识输出/output.json"
VALIDATOR = ROOT / ".agents/skills/domain-knowledge/scripts/validate_contract.py"


def digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


cmd = [sys.executable, str(VALIDATOR), "validate", "--project-root", str(ROOT),
       "output", str(OUTPUT)]
proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
result = json.loads(proc.stdout)
if proc.returncode or result["status"] != "PASS" or result["failures"]:
    raise SystemExit("Contract validation did not pass; no evidence was bound")

payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
report = {
    "run_id": "2026-09-24.reformation",
    "check": "domain-knowledge contract 5.0.0 output validation",
    "status": result["status"],
    "failures": result["failures"],
    "input_digest": payload["input_refs"][0]["digest"],
    "pre_binding_output_digest": digest(OUTPUT),
    "checked": {
        key: result["checked"][key]
        for key in ("sourceInventory", "businessReferences", "coverage", "sourceUnitCoverage",
                    "statementPass", "knowledgeSynthesis", "semanticAudit", "ruleDepth",
                    "caseValidation", "knowledgeCoverage", "questionDiscovery",
                    "openKnowledgeGapCount", "openQuestionCandidateCount", "processGapCount")
    },
    "boundary": result["boundary"],
}
report_path = RUN / "contract-check.json"
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

record = {
    "artifact_id": "A01.DomainKnowledge.ContractCheck",
    "content_version": payload["content_version"],
    "contract_version": "report/1.0.0",
    "path": str(report_path.relative_to(ROOT)),
    "digest": digest(report_path),
}
doc_refs = [item for item in payload["files"] if item["artifact_id"] in {
    "A01.DomainKnowledge.Review", "A01.DomainKnowledge.Coverage"}]
if len(doc_refs) != 2:
    raise SystemExit("Expected both rendered documents before evidence binding")
payload["evidence"] = [{
    "evidence_id": "EV.A01.KF.CONTRACT_CHECK",
    "record": record,
    "locator": "contract-check.json: status, checked, boundary",
    "claim": "当前渲染草稿完成领域知识合同及跨文档引用校验；仅证明结构与引用，不证明业务语义获批准。",
    "subject_refs": payload["input_refs"] + doc_refs,
}]
payload["states"]["structure_checked"] = {
    "status": "PASS", "evidence_ids": ["EV.A01.KF.CONTRACT_CHECK"],
    "reason": "领域知识合同与引用校验通过；业务含义和正式确认仍独立待审。",
}
OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"bound_evidence": record["path"], "status": "PASS"}, ensure_ascii=False))
