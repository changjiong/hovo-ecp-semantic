#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

PROFILE_ID = "enterprise-cognitive/semantic-profile/1.0.0"
PROFILE_DIGEST = "sha256:708246ab3a0ce13a23977d39712a82f9a363f16a9c2fe428fe0311e4147b1882"
ZERO = "sha256:" + "0" * 64


def dump(p: Path, obj: dict):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Create a minimal ECP workspace authoring scaffold. It does not invent business semantics.")
    ap.add_argument("out")
    ap.add_argument("--with-scope", action="store_true")
    args = ap.parse_args()
    root = Path(args.out).resolve()
    for d in ["ontology", "mapping", "rules/shacl", "rules/derivation", "rules/evaluation", "rules/action-policy", "data-sources"]:
        (root / d).mkdir(parents=True, exist_ok=True)
    if args.with_scope:
        (root / "scopes").mkdir(parents=True, exist_ok=True)

    (root / "ontology/model.ttl").write_text(
        '@prefix ex: <urn:replace:ontology:> .\n'
        '@prefix owl: <http://www.w3.org/2002/07/owl#> .\n'
        '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n'
        'ex:ontology a owl:Ontology ;\n'
        '  rdfs:label "待建模本体"@zh-CN ;\n'
        '  rdfs:comment "占位文件：先完成范围、能力问题和概念化后再替换。"@zh-CN .\n', encoding="utf-8")

    dump(root / "mapping/model.json", {
        "schemaVersion": 1,
        "mappingId": "REPLACE_ME",
        "version": "0.1.0",
        "name": "待建模映射",
        "description": "需要真实数据源 Schema 后填写；不要猜测表字段。",
        "ontologySourceDigest": ZERO,
        "dataSources": [], "scans": [], "joins": [], "entities": [], "properties": [], "relationships": [], "filters": [],
        "coverage": {"mode": "FULL_SNAPSHOT", "requirements": []}
    })

    dump(root / "rules/manifest.json", {
        "schemaVersion": 1,
        "kind": "ECP_RULE_SET_BUNDLE",
        "bundleFormat": "enterprise-cognitive/rule-set-bundle/1.0.0",
        "semanticProfileId": PROFILE_ID,
        "semanticProfileDigest": PROFILE_DIGEST,
        "members": []
    })

    version = 2 if args.with_scope else 1
    manifest = {
        "schemaVersion": version,
        "kind": "ECP_SEMANTIC_WORKSPACE_PACKAGE",
        "bundleFormat": f"enterprise-cognitive/semantic-workspace-package/{version}.0.0",
        "semanticProfileId": PROFILE_ID,
        "semanticProfileDigest": PROFILE_DIGEST,
        "ontology": {"path": "ontology/model.ttl", "mediaType": "text/turtle", "sourceDigest": ZERO},
        "mapping": {"path": "mapping/model.json", "mediaType": "application/json", "sourceDigest": ZERO, "ontologySourceDigest": ZERO},
        "ruleSet": {"manifestPath": "rules/manifest.json", "sourceDigest": ZERO},
        "schemas": []
    }
    if args.with_scope:
        manifest["scopes"] = []
    dump(root / "manifest.json", manifest)
    print(f"created scaffold: {root}")
    print("注意：这是结构脚手架，不是可导入资产；必须先补真实业务语义和数据 Schema。")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
