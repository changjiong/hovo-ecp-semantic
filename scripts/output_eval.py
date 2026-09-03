#!/usr/bin/env python3
"""Run deterministic output regressions and emit evidence JSON."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="Run hovo-ecp-semantic output regression tests.")
    ap.add_argument("skill_dir", nargs="?", default=".")
    ap.add_argument("--output", default="reports/output-eval.json")
    args = ap.parse_args()
    root = Path(args.skill_dir).resolve()
    proc = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(root / "tests"), "-v"], capture_output=True, text=True)
    cases = json.loads((root / "evals" / "output_cases.json").read_text(encoding="utf-8"))
    report = {
        "ok": proc.returncode == 0,
        "runner": "python unittest",
        "declaredCases": len(cases.get("cases", [])),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "evidenceBoundary": "本报告只证明本地确定性回归；ECP 平台预检、候选编译与发布仍为 missing evidence。"
    }
    out = Path(args.output); out = out if out.is_absolute() else root / out
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return proc.returncode


if __name__ == "__main__": raise SystemExit(main())
