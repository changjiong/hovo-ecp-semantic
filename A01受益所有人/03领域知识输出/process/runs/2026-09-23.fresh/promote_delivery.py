#!/usr/bin/env python3
"""Promote this fresh, unconfirmed draft to A01's four-file delivery root."""
from __future__ import annotations

import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path


RUN = Path(__file__).resolve().parent
DELIVERY = RUN.parents[2]
ROOT = RUN.parents[4]
assert DELIVERY.name == "03领域知识输出" and ROOT.name == "hovo-ecp-semantic"
source_input = RUN / "input.json"
source_output = RUN / "output.json"
payload = json.loads(source_output.read_text())
assert payload["confirmation"]["status"] == "PENDING"
assert len(payload["content"]["sources"]) == 75
target_input = DELIVERY / "input.json"
target_output = DELIVERY / "output.json"
shutil.copyfile(source_input, target_input)
payload["input_refs"][0]["path"] = str(target_input.relative_to(ROOT))
payload["input_refs"][0]["digest"] = "sha256:" + hashlib.sha256(target_input.read_bytes()).hexdigest()
payload["files"] = []
payload["states"]["structure_checked"] = {"status": "NOT_EXECUTED", "evidence_ids": [], "reason": "根目录交付件待执行合同校验。"}
target_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

input_payload = json.loads(source_input.read_text())
extractions = {e["source_id"]: e for e in input_payload["source_extractions"]}
coverage = payload["content"]["provision_coverage"]
by_source = Counter(row["source_unit_id"].rsplit(".U", 1)[0] for row in coverage if row["meaning_status"] == "REVIEWED")
partial_by_source = Counter(row["source_unit_id"].rsplit(".U", 1)[0] for row in coverage if row["meaning_status"] == "PARTIAL")
statement_by_source = Counter(sid for statement in payload["content"]["statements"] for sid in statement["source_ids"])
source_inventory = {
    "run_id": "2026-09-23.fresh",
    "input_ref": payload["input_refs"][0],
    "scope": "A01受益所有人/01业务输入全部75份材料；不含旧03领域知识输出",
    "totals": {"sources": len(input_payload["sources"]), "source_blocks": len(input_payload["source_blocks"]), "source_units": len(coverage),
               "meaning_reviewed_units": sum(row["meaning_status"] == "REVIEWED" for row in coverage),
               "extraction_statuses": dict(Counter(e["status"] for e in extractions.values()))},
    "sources": [
        {"source_id": s["source_id"], "path": s["artifact"]["path"],
         "digest": s["artifact"]["digest"], "authority": s["authority"],
         "source_role": s["source_role"], "extraction_status": extractions[s["source_id"]]["status"],
         "source_unit_count": len(extractions[s["source_id"]]["unit_ids"]),
         "meaning_reviewed_unit_count": by_source[s["source_id"]],
         "meaning_partial_unit_count": partial_by_source[s["source_id"]],
         "linked_statement_count": statement_by_source[s["source_id"]],
         "limitations": extractions[s["source_id"]]["limitations"]}
        for s in payload["content"]["sources"]
    ],
}
(DELIVERY / "source-inventory.json").write_text(json.dumps(source_inventory, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"delivery": str(DELIVERY), "sources": 75,
                  "meaning_reviewed_units": source_inventory["totals"]["meaning_reviewed_units"]}, ensure_ascii=False))
