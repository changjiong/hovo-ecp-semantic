#!/usr/bin/env python3
"""Assemble authored Statement rows only after every SourceUnit is accounted for."""

from __future__ import annotations

import json
from pathlib import Path


RUN = Path(__file__).resolve().parent


def main() -> None:
    input_data = json.loads((RUN / "input.json").read_text(encoding="utf-8"))
    expected = {unit["unit_id"] for unit in input_data["source_units"]}
    rows: dict[str, dict] = {}
    files = sorted((RUN / "parts").glob("statements_*.json"))
    if not files:
        raise ValueError("No authored Statement parts")
    for file in files:
        part = json.loads(file.read_text(encoding="utf-8"))
        for row in part["source_unit_results"]:
            unit_id = row["source_unit_id"]
            if unit_id in rows:
                raise ValueError(f"Duplicate SourceUnit: {unit_id}")
            if unit_id not in expected:
                raise ValueError(f"Unknown SourceUnit: {unit_id}")
            if row.get("reason") is None:
                if row["status"] != "EXTRACTED" or not row["statements"]:
                    raise ValueError(f"Missing disposition reason: {unit_id}")
                row["reason"] = "该单元已形成可追溯的独立业务陈述"
            rows[unit_id] = row
    missing = expected - rows.keys()
    if missing:
        raise ValueError(f"Statement Pass incomplete: {len(missing)} SourceUnits missing")
    payload = {
        "formation_version": "1.0.0",
        "pass": "statement_pass",
        "source_unit_results": [rows[unit["unit_id"]] for unit in input_data["source_units"]],
    }
    output = RUN / "knowledge-formation" / "01-statements.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"parts": len(files), "source_units": len(rows), "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
