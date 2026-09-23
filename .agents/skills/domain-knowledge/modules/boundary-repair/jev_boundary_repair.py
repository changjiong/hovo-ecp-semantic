#!/usr/bin/env python3
"""Use TypeSafe Jev to repair only ambiguous document boundaries."""
from __future__ import annotations

from typing import Any

from typesafe_sdk import Choice, TypeSafeClient, TypeSafeError

MODEL = "jev-latest"
DEFAULT_MIN_CONFIDENCE = 0.90
QUESTION_VERSION = "boundary-relation-v1"
BOUNDARY_OPTIONS = (
    "CONTINUE_PREVIOUS",
    "START_NEW_UNIT",
    "CHILD_OF_PREVIOUS",
    "UNRESOLVED",
)

BOUNDARY_QUESTION = Choice(
    instructions=(
        "Determine the structural relationship of current_block to the immediately "
        "preceding semantic content. Judge document structure only. Do not infer "
        "domain rules, rewrite text, or repair missing text."
    ),
    criteria={
        "CONTINUE_PREVIOUS": (
            "current_block continues the same sentence, paragraph, clause, or "
            "semantic unit as the preceding content"
        ),
        "START_NEW_UNIT": (
            "current_block starts a new independent semantic unit at the same "
            "structural level"
        ),
        "CHILD_OF_PREVIOUS": (
            "current_block starts a distinct subordinate item whose parent is the "
            "preceding semantic unit"
        ),
        "UNRESOLVED": (
            "the supplied local document evidence is insufficient to determine "
            "the structural relationship reliably"
        ),
    },
)


class JevBoundaryRepair:
    """Narrow Jev adapter: state in, typed boundary decision out."""

    def __init__(
        self,
        *,
        api_key: str,
        min_confidence: float = DEFAULT_MIN_CONFIDENCE,
        timeout: float = 30.0,
    ) -> None:
        if not 0.0 <= min_confidence <= 1.0:
            raise ValueError("min_confidence 必须位于 0 到 1 之间")
        self.min_confidence = float(min_confidence)
        self._client = TypeSafeClient(
            api_key=api_key,
            model=MODEL,
            timeout=timeout,
        )

    def close(self) -> None:
        self._client.close()

    def judge(self, state: dict[str, Any]) -> dict[str, Any]:
        try:
            response = self._client.system_one(
                state=state,
                questions={"boundary_relation": BOUNDARY_QUESTION},
            )
        except TypeSafeError as exc:
            raise RuntimeError(
                f"Jev boundary repair 调用失败: {type(exc).__name__}"
            ) from exc

        answer = response.choices["boundary_relation"]
        selected = str(answer.choice)
        if selected not in BOUNDARY_OPTIONS:
            raise RuntimeError(f"Jev 返回未知边界选项: {selected}")

        confidence = float(answer.confidence)
        probabilities = {
            option: float(answer.probabilities.get(option, 0.0))
            for option in BOUNDARY_OPTIONS
        }
        applied = (
            selected
            if confidence >= self.min_confidence
            else "UNRESOLVED"
        )

        result = {
            "selected": selected,
            "applied": applied,
            "confidence": confidence,
            "threshold": self.min_confidence,
            "probabilities": probabilities,
            "model": str(response.model),
            "question_version": QUESTION_VERSION,
        }
        request_id = getattr(response, "request_id", None)
        if request_id:
            result["request_id"] = str(request_id)
        return result
