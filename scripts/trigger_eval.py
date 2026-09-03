#!/usr/bin/env python3
"""Lightweight routing-boundary evaluation for hovo-ecp-semantic."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\u4e00-\u9fff]+", " ", s.lower())).strip()


def hit(text: str, phrases: list[str]) -> bool:
    t = norm(text)
    return any(norm(p) in t for p in phrases)


def load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def predict(text: str, cfg: dict[str, Any]) -> tuple[bool, list[str], str | None]:
    neg = next((p for p in cfg.get("negative_patterns", []) if hit(text, [p])), None)
    concepts = cfg.get("positive_concepts", {})
    hits = [name for name, phrases in concepts.items() if hit(text, phrases)]
    required_any = set(cfg.get("required_any", ["ecp", "semantic_asset"]))
    action = "authoring_action" in hits
    domain = bool(required_any.intersection(hits))
    predicted = neg is None and action and domain
    return predicted, sorted(hits), neg


def evaluate(cases: dict[str, Any]) -> dict[str, Any]:
    results = []; failures = []
    for bucket, expected in [("should_trigger", True), ("should_not_trigger", False), ("near_neighbor", False)]:
        for raw in cases.get(bucket, []):
            item = {"text": raw, "family": "default"} if isinstance(raw, str) else raw
            predicted, hits, neg = predict(str(item.get("text", "")), cases)
            passed = predicted == expected
            rec = {"bucket": bucket, "family": item.get("family", "default"), "prompt": item.get("text", ""), "expected_trigger": expected, "predicted_trigger": predicted, "matched_concepts": hits, "negative_pattern": neg, "passed": passed}
            results.append(rec)
            if not passed: failures.append(rec)
    return {"ok": not failures, "summary": {"total": len(results), "passed": len(results)-len(failures), "false": len(failures)}, "failures": failures, "results": results}


def main() -> None:
    ap = argparse.ArgumentParser(description="Evaluate routing boundaries for hovo-ecp-semantic.")
    ap.add_argument("skill_dir", nargs="?", default=".")
    ap.add_argument("--cases", default="evals/trigger_cases.json")
    ap.add_argument("--output", "-o")
    args = ap.parse_args()
    root = Path(args.skill_dir).resolve(); cases_path = Path(args.cases)
    if not cases_path.is_absolute(): cases_path = root / cases_path
    result = evaluate(load(cases_path)); rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        out = Path(args.output); out = out if out.is_absolute() else root / out; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(rendered+"\n", encoding="utf-8")
    print(rendered)
    if not result["ok"]: raise SystemExit(2)


if __name__ == "__main__": main()
