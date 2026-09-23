#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_ROOT))

from domain_checks import check_source_inventory


def digest(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def payload(*, status: str, confidence: float, applied: str):
    source_id = "SRC.demo"
    block1 = {
        "block_id": f"{source_id}.B00001",
        "source_id": source_id,
        "sequence": 1,
        "text": "要求如下：",
        "digest": digest("要求如下："),
    }
    block2 = {
        "block_id": f"{source_id}.B00002",
        "source_id": source_id,
        "sequence": 2,
        "text": "1. 核验身份证明。",
        "digest": digest("1. 核验身份证明。"),
    }
    unit1 = {
        "unit_id": f"{source_id}.U0001",
        "source_id": source_id,
        "sequence": 1,
        "text": block1["text"],
        "digest": block1["digest"],
        "source_block_ids": [block1["block_id"]],
        "context": {"ancestor_unit_ids": []},
    }
    unit2 = {
        "unit_id": f"{source_id}.U0002",
        "source_id": source_id,
        "sequence": 2,
        "text": block2["text"],
        "digest": block2["digest"],
        "source_block_ids": [block2["block_id"]],
        "parent_unit_id": unit1["unit_id"],
        "context": {
            "ancestor_unit_ids": [unit1["unit_id"]],
            "previous_unit_id": unit1["unit_id"],
        },
    }
    return {
        "sources": [
            {
                "source_id": source_id,
                "artifact": {"digest": digest("artifact")},
            }
        ],
        "source_blocks": [block1, block2],
        "boundary_decisions": [
            {
                "decision_id": f"{source_id}.D0001",
                "source_id": source_id,
                "previous_block_id": block1["block_id"],
                "current_block_id": block2["block_id"],
                "selected": "CHILD_OF_PREVIOUS",
                "applied": applied,
                "confidence": confidence,
                "threshold": 0.90,
                "probabilities": {
                    "CONTINUE_PREVIOUS": 0.01,
                    "START_NEW_UNIT": 0.01,
                    "CHILD_OF_PREVIOUS": 0.97,
                    "UNRESOLVED": 0.01,
                },
            }
        ],
        "source_units": [unit1, unit2],
        "source_extractions": [
            {
                "source_id": source_id,
                "status": status,
                "block_ids": [block1["block_id"], block2["block_id"]],
                "boundary_decision_ids": [f"{source_id}.D0001"],
                "unit_ids": [unit1["unit_id"], unit2["unit_id"]],
            }
        ],
    }


class BoundaryInventoryCheckTest(unittest.TestCase):
    def test_unresolved_boundary_cannot_be_complete(self):
        data = payload(status="COMPLETE", confidence=0.60, applied="UNRESOLVED")
        failures = []

        check_source_inventory(data, failures)

        codes = {failure["code"] for failure in failures}
        self.assertIn("UNRESOLVED_BOUNDARY_REQUIRES_PARTIAL", codes)

    def test_low_confidence_choice_cannot_be_applied(self):
        data = payload(
            status="PARTIAL",
            confidence=0.60,
            applied="CHILD_OF_PREVIOUS",
        )
        failures = []

        check_source_inventory(data, failures)

        codes = {failure["code"] for failure in failures}
        self.assertIn("BOUNDARY_LOW_CONFIDENCE_APPLIED", codes)


if __name__ == "__main__":
    unittest.main()
