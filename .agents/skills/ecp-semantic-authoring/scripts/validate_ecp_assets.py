#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "references" / "ecp-authoring-kit-1.8"
STAGES = {"asserted","domain","feature","change","output","provenance"}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate_schema(value, schema_path: Path):
    schema = load_json(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: list(e.absolute_path))
    return [f"{list(e.absolute_path)}: {e.message}" for e in errors]

def digest(path: Path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()

def parse_turtle(path: Path):
    Graph().parse(path, format="turtle")

def main():
    p = argparse.ArgumentParser(description="有限检查 ECP V3 技术语义资产；不替代目标平台原生候选编译。")
    p.add_argument("--ontology", type=Path, required=True)
    p.add_argument("--mapping", type=Path, required=True)
    p.add_argument("--shape", action="append", default=[], help="stage=path，可重复")
    p.add_argument("--derivation", type=Path, action="append", default=[])
    p.add_argument("--evaluation", type=Path, action="append", default=[])
    p.add_argument("--lifecycle", type=Path)
    p.add_argument("--action-policy", type=Path)
    args = p.parse_args()
    failures = []
    try: parse_turtle(args.ontology)
    except Exception as e: failures.append({"asset":str(args.ontology),"reason":f"ONTOLOGY_TURTLE_INVALID: {e}"})
    mapping = load_json(args.mapping)
    for err in validate_schema(mapping, KIT/"contracts"/"v3-mapping-definition.schema.json"):
        failures.append({"asset":str(args.mapping),"reason":err})
    actual = digest(args.ontology)
    if mapping.get("ontologySourceDigest") != actual:
        failures.append({"asset":str(args.mapping),"reason":f"ontologySourceDigest mismatch: expected {actual}"})
    for item in args.shape:
        if "=" not in item:
            failures.append({"asset":item,"reason":"shape 参数必须为 stage=path"})
            continue
        stage, raw = item.split("=",1)
        if stage not in STAGES:
            failures.append({"asset":raw,"reason":f"unknown SHACL stage: {stage}"})
            continue
        try: parse_turtle(Path(raw))
        except Exception as e: failures.append({"asset":raw,"reason":f"SHACL_TURTLE_INVALID: {e}"})
    for path in args.derivation:
        value = load_json(path)
        direct = value.get("profileId") == "ecp-declarative-derivation/1.0.0"
        module = value.get("kind") == "ECP_V3_DERIVATION_MODULE" and isinstance(value.get("profile"),dict) and value["profile"].get("profileId") == "ecp-declarative-derivation/1.0.0"
        if not (direct or module):
            failures.append({"asset":str(path),"reason":"not current V3 derivation envelope/profile"})
    for path in args.evaluation:
        value = load_json(path)
        ok = value.get("kind") == "ECP_V3_EVALUATION_MODULE" and isinstance(value.get("profile"),dict) and value["profile"].get("profileId") == "ecp-scoped-evaluation/1.0.0"
        if not ok:
            failures.append({"asset":str(path),"reason":"not current V3 evaluation envelope/profile"})
    if args.lifecycle:
        value = load_json(args.lifecycle)
        for err in validate_schema(value, KIT/"contracts"/"v3-lifecycle-binding.schema.json"):
            failures.append({"asset":str(args.lifecycle),"reason":err})
    if args.action_policy:
        value = load_json(args.action_policy)
        for err in validate_schema(value, KIT/"contracts"/"v3-action-policy.schema.json"):
            failures.append({"asset":str(args.action_policy),"reason":err})
    result = {"status":"PASS" if not failures else "FAIL","failures":failures,
              "boundary":"有限静态检查；单项通过不证明跨资产 V3 候选可编译，也不证明源覆盖、运行质量或发布许可。"}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if not failures else 1)

if __name__ == "__main__":
    main()
