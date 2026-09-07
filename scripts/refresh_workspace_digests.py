#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

PROFILE_ID = "enterprise-cognitive/semantic-profile/1.0.0"
PROFILE_DIGEST = "sha256:708246ab3a0ce13a23977d39712a82f9a363f16a9c2fe428fe0311e4147b1882"


def digest(p: Path) -> str:
    return "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()


def write_json(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Refresh exact source digests in an ECP workspace without inventing semantic IDs.")
    ap.add_argument("workspace")
    args = ap.parse_args()
    root = Path(args.workspace).resolve()
    mp = root / "manifest.json"
    if not mp.exists():
        raise SystemExit("manifest.json 不存在；本脚本不会猜测 Workspace 结构")
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    if manifest.get("kind") != "ECP_SEMANTIC_WORKSPACE_PACKAGE":
        raise SystemExit("根 manifest 不是 ECP_SEMANTIC_WORKSPACE_PACKAGE")

    scopes_present = bool(list((root / "scopes").glob("*.json"))) if (root / "scopes").exists() else False
    if scopes_present and manifest.get("schemaVersion") != 2:
        raise SystemExit("存在 Scope 时必须使用 Workspace Package v2；请直接修正版本，不添加兼容层")
    if not scopes_present and manifest.get("schemaVersion") == 2 and manifest.get("scopes"):
        raise SystemExit("v2 Manifest 声明 Scope，但 scopes/ 中没有对应文件")

    manifest["semanticProfileId"] = PROFILE_ID
    manifest["semanticProfileDigest"] = PROFILE_DIGEST

    opath = root / manifest["ontology"]["path"]
    od = digest(opath)
    manifest["ontology"]["sourceDigest"] = od

    mpath = root / manifest["mapping"]["path"]
    mapping = json.loads(mpath.read_text(encoding="utf-8"))
    mapping["ontologySourceDigest"] = od
    write_json(mpath, mapping)
    md = digest(mpath)
    manifest["mapping"]["sourceDigest"] = md
    manifest["mapping"]["ontologySourceDigest"] = od

    rmpath = root / manifest["ruleSet"]["manifestPath"]
    rules = json.loads(rmpath.read_text(encoding="utf-8"))
    rules["semanticProfileId"] = PROFILE_ID
    rules["semanticProfileDigest"] = PROFILE_DIGEST
    for member in rules.get("members", []):
        p = root / member["path"]
        if not p.exists():
            raise SystemExit(f"规则成员不存在: {member['path']}")
        member["sourceDigest"] = digest(p)
    write_json(rmpath, rules)
    manifest["ruleSet"]["sourceDigest"] = digest(rmpath)

    for s in manifest.get("schemas", []):
        p = root / s["path"]
        if not p.exists():
            raise SystemExit(f"Schema 快照不存在: {s['path']}")
        s["sourceDigest"] = digest(p)

    if manifest.get("schemaVersion") == 2:
        for s in manifest.get("scopes", []):
            p = root / s["path"]
            if not p.exists():
                raise SystemExit(f"Scope 不存在: {s['path']}")
            s["sourceDigest"] = digest(p)

    write_json(mp, manifest)
    print(f"refreshed: {mp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
