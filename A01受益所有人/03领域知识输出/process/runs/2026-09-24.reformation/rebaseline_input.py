#!/usr/bin/env python3
"""Rebaseline already parsed SourceUnits for a fresh Contract 5 knowledge run.

This is a one-time project artifact, not a parser or a contract compatibility path.
It never calls MinerU and never derives business knowledge.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
PRIOR = RUN.parent / "2026-09-23.fresh" / "input.json"
ROLE_MAP = {
    "PROCEDURAL_GUIDANCE": "OFFICIAL_GUIDANCE",
    "EXPERT_EXPLANATION": "BUSINESS_SCOPE",
}


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    prior = json.loads(PRIOR.read_text(encoding="utf-8"))
    if prior["contract_version"] != "4.0.0":
        raise ValueError("Expected the explicitly selected parsed input Contract 4.0.0")
    if len(prior["sources"]) != 75:
        raise ValueError("The selected parse snapshot is not the expected 75-source input")

    changes: list[dict[str, str]] = []
    for source in prior["sources"]:
        relpath = source["artifact"]["path"]
        if "trash" in relpath.lower():
            raise ValueError("Forbidden source path")
        source_path = (ROOT / relpath).resolve()
        if not source_path.is_relative_to(ROOT) or not source_path.is_file():
            raise ValueError(f"Source missing or outside project: {relpath}")
        if sha256(source_path) != source["artifact"]["digest"]:
            raise ValueError(f"Source changed since the parse snapshot: {relpath}")
        previous_role = source["source_role"]
        if previous_role in ROLE_MAP:
            source["source_role"] = ROLE_MAP[previous_role]
            changes.append({
                "source_id": source["source_id"],
                "from": previous_role,
                "to": source["source_role"],
            })

    prior["contract_version"] = "5.0.0"
    prior["request_id"] = "A01.DomainKnowledge.2026-09-24.Reformation"
    save(RUN / "input.json", prior)
    save(RUN / "rebaseline-record.json", {
        "source_input": str(PRIOR.relative_to(ROOT)),
        "source_input_digest": sha256(PRIOR),
        "new_input": str((RUN / "input.json").relative_to(ROOT)),
        "new_input_digest": sha256(RUN / "input.json"),
        "source_count": len(prior["sources"]),
        "source_unit_count": len(prior["source_units"]),
        "source_block_count": len(prior["source_blocks"]),
        "parser_reused": True,
        "mineru_called": False,
        "source_roles_reclassified": changes,
        "source_units_modified": False,
        "source_blocks_modified": False,
    })


if __name__ == "__main__":
    main()
