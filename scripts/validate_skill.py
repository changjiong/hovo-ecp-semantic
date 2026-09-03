#!/usr/bin/env python3
"""Validate the hovo-ecp-semantic governed skill package."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:
    yaml = None

REQUIRED_FILES = [
    "SKILL.md", "README.md", "manifest.json", "agents/interface.yaml",
    "references/ontology-engineering-method.md", "references/ecp-asset-playbook.md",
    "references/output-contract.md", "references/trust-boundaries.md", "references/interaction-policy.md",
    "scripts/validate_ecp_assets.py", "scripts/refresh_workspace_digests.py",
    "scripts/package_workspace.py", "scripts/scaffold_workspace.py",
    "evals/trigger_cases.json", "evals/output_cases.json",
    "reports/prior-art-research.md", "reports/skill-ir.json", "reports/creation-handoff.md",
    "reports/trust-report.md",
]
REQUIRED_KIT_FILES = [
    "references/ecp-kit-1.7/standards/ecp-semantic-profile-1.0.md",
    "references/ecp-kit-1.7/standards/ecp-semantic-development-guide.md",
    "references/ecp-kit-1.7/contracts/ecp-semantic-profile-1.0.json",
    "references/ecp-kit-1.7/contracts/mapping-definition-v1.schema.json",
    "references/ecp-kit-1.7/contracts/scope-definition-v1.schema.json",
    "references/ecp-kit-1.7/contracts/action-policy-v1.schema.json",
    "references/ecp-kit-1.7/contracts/rule-set-bundle-manifest-v1.schema.json",
    "references/ecp-kit-1.7/contracts/semantic-workspace-package-manifest-v1.schema.json",
    "references/ecp-kit-1.7/contracts/semantic-workspace-package-manifest-v2.schema.json",
]
FORBIDDEN_REMOTE_MUTATION = ["git push origin main", "git push origin master", "gh release create"]


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    lines = text.splitlines()
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}
    raw = "\n".join(lines[1:end])
    if yaml is not None:
        data = yaml.safe_load(raw) or {}
        return data if isinstance(data, dict) else {}
    result: dict[str, Any] = {}
    current = None
    for line in raw.splitlines():
        if line.startswith("  ") and current:
            result[current] = (str(result.get(current, "")) + "\n" + line.strip()).strip()
        elif ":" in line:
            k, v = line.split(":", 1)
            current = k.strip()
            result[current] = v.strip().strip("'\"|")
    return result


def validate(root: Path) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    root = root.resolve()

    for rel in REQUIRED_FILES + REQUIRED_KIT_FILES:
        if not (root / rel).is_file():
            failures.append(f"missing required file: {rel}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        text = skill_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm.get("name") != "hovo-ecp-semantic":
            failures.append("SKILL.md frontmatter name must be hovo-ecp-semantic")
        desc = str(fm.get("description", ""))
        for token in ["ECP", "本体", "语义", "ONTOLOGY", "MAPPING", "SHACL"]:
            if token.lower() not in desc.lower():
                failures.append(f"SKILL.md description missing routing concept: {token}")
        for required in ["ECP_PREFLIGHT_REQUIRED", "RELEASE_READY", "不得伪造", "能力问题", "最多 1 轮", "最多 5 个", "CONFIRMED", "INFERRED", "ASSUMED", "OPEN", "BLOCKED", "Workshop"]:
            if required not in text:
                failures.append(f"SKILL.md missing governed invariant: {required}")
        if len(text.encode("utf-8")) > 18000:
            warnings.append("SKILL.md is large; consider moving more detail into references/")

    nested = [p.relative_to(root) for p in root.rglob("SKILL.md") if p != root / "SKILL.md"]
    if nested:
        failures.append("nested discoverable SKILL.md found: " + ", ".join(map(str, nested)))

    manifest_path = root / "manifest.json"
    if manifest_path.is_file():
        try:
            manifest = load_json(manifest_path)
        except Exception as exc:
            failures.append(str(exc)); manifest = {}
        if manifest.get("name") != "hovo-ecp-semantic":
            failures.append("manifest name mismatch")
        if manifest.get("maturity_tier") != "governed":
            failures.append("manifest maturity_tier must be governed")
        if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
            failures.append("manifest version must use semver")

    ir = root / "reports/skill-ir.json"
    if ir.is_file() and manifest_path.is_file():
        try:
            ir_data, manifest = load_json(ir), load_json(manifest_path)
            pkg = ir_data.get("package", {})
            if pkg.get("name") != manifest.get("name") or pkg.get("version") != manifest.get("version"):
                failures.append("skill-ir package identity/version does not match manifest")
        except Exception as exc:
            failures.append(str(exc))

    trigger_report = root / "reports/trigger-eval.json"
    if trigger_report.is_file():
        try:
            result = load_json(trigger_report)
            if result.get("ok") is not True:
                failures.append("trigger eval report is failing")
        except Exception as exc:
            failures.append(str(exc))
    else:
        warnings.append("reports/trigger-eval.json not generated yet")

    for script in (root / "scripts").glob("*.py") if (root / "scripts").exists() else []:
        if script.name == "validate_skill.py":
            continue
        text = script.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_REMOTE_MUTATION:
            if forbidden in text:
                failures.append(f"script contains forbidden publication mutation: {script.name}: {forbidden}")

    return {"ok": not failures, "root": str(root), "failures": failures, "warnings": warnings}


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate hovo-ecp-semantic package structure and governed invariants.")
    ap.add_argument("skill_dir", nargs="?", default=".")
    args = ap.parse_args()
    result = validate(Path(args.skill_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
