#!/usr/bin/env python3
"""Offline smoke test for domain-model 1.0.0 bundled contracts and examples."""
from __future__ import annotations

import json
from pathlib import Path

from domain_model import load_json, load_yaml, validate_coverage, validate_model
from validate_contract import check_schemas


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/order"


def main() -> int:
    failures = []

    schema_result = check_schemas()
    if schema_result["status"] != "PASS":
        failures.extend(schema_result["failures"])

    model = load_yaml(EXAMPLE / "model.yaml")
    model_failures = validate_model(model)
    failures.extend(model_failures)

    coverage = load_json(EXAMPLE / "coverage.json")
    coverage_failures = validate_coverage(coverage, model)
    failures.extend(coverage_failures)

    result = {
        "status": "PASS" if not failures else "FAIL",
        "checked": {
            "schemas": schema_result.get("checked", {}),
            "example_model": "PASS" if not model_failures else "FAIL",
            "example_coverage": "PASS" if not coverage_failures else "FAIL",
        },
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
