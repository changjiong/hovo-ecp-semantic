#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

MODULE_ROOT = Path(__file__).resolve().parents[1] / "modules" / "boundary-repair"
sys.path.insert(0, str(MODULE_ROOT))

from jev_boundary_repair import JevBoundaryRepair


class FakeClient:
    def __init__(self, *, confidence: float) -> None:
        self.confidence = confidence
        self.closed = False

    def system_one(self, *, state, questions):
        self.state = state
        self.questions = questions
        return SimpleNamespace(
            choices={
                "boundary_relation": SimpleNamespace(
                    choice="CONTINUE_PREVIOUS",
                    confidence=self.confidence,
                    probabilities={
                        "CONTINUE_PREVIOUS": 0.80,
                        "START_NEW_UNIT": 0.10,
                        "CHILD_OF_PREVIOUS": 0.05,
                        "UNRESOLVED": 0.05,
                    },
                )
            },
            model="jev-1.13.0",
            request_id="req-test",
        )

    def close(self):
        self.closed = True


def make_repair(confidence: float) -> JevBoundaryRepair:
    repair = object.__new__(JevBoundaryRepair)
    repair.min_confidence = 0.90
    repair._client = FakeClient(confidence=confidence)
    return repair


class JevBoundaryRepairTest(unittest.TestCase):
    def test_reads_typed_choice_accessor_and_preserves_trace(self):
        repair = make_repair(0.95)

        result = repair.judge({"current_block": {"text": "demo"}})

        self.assertEqual("CONTINUE_PREVIOUS", result["selected"])
        self.assertEqual("CONTINUE_PREVIOUS", result["applied"])
        self.assertEqual("jev-1.13.0", result["model"])
        self.assertEqual("req-test", result["request_id"])
        self.assertIn("boundary_relation", repair._client.questions)

    def test_low_confidence_does_not_apply_selected_choice(self):
        repair = make_repair(0.62)

        result = repair.judge({"current_block": {"text": "demo"}})

        self.assertEqual("CONTINUE_PREVIOUS", result["selected"])
        self.assertEqual("UNRESOLVED", result["applied"])


if __name__ == "__main__":
    unittest.main()
