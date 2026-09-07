#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys, zipfile
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate and package an ECP Semantic Workspace directory.")
    ap.add_argument("workspace")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    root = Path(args.workspace).resolve()
    output = Path(args.output).resolve()
    if not (root / "manifest.json").exists():
        raise SystemExit("workspace 缺少 manifest.json")
    data = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if data.get("kind") != "ECP_SEMANTIC_WORKSPACE_PACKAGE":
        raise SystemExit("根 manifest 不是 ECP_SEMANTIC_WORKSPACE_PACKAGE")

    refresh = Path(__file__).with_name("refresh_workspace_digests.py")
    validate = Path(__file__).with_name("validate_ecp_assets.py")
    subprocess.run([sys.executable, str(refresh), str(root)], check=True)
    proc = subprocess.run([sys.executable, str(validate), str(root)], check=False)
    if proc.returncode != 0:
        raise SystemExit("本地校验失败，拒绝生成正式 Workspace ZIP")

    allowed_prefixes = ("ontology/", "mapping/", "rules/", "scopes/", "data-sources/")
    files = [root / "manifest.json"]
    for p in root.rglob("*"):
        if not p.is_file() or p == root / "manifest.json":
            continue
        rel = p.relative_to(root).as_posix()
        if rel.startswith(allowed_prefixes):
            files.append(p)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(files):
            zf.write(p, p.relative_to(root).as_posix())
    print(f"created: {output}")
    print("status: LOCALLY_VALID; ECP_PREFLIGHT_REQUIRED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
