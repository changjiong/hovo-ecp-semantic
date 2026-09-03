#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, tempfile, zipfile
from pathlib import Path
from typing import Any

try:
    import jsonschema
except Exception:
    jsonschema = None
try:
    from rdflib import BNode, Graph, URIRef
    from rdflib.namespace import OWL, RDF, RDFS, XSD
except Exception:
    Graph = None

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "references" / "ecp-kit-1.7" / "contracts"
PROFILE_ID = "enterprise-cognitive/semantic-profile/1.0.0"
PROFILE_DIGEST = "sha256:708246ab3a0ce13a23977d39712a82f9a363f16a9c2fe428fe0311e4147b1882"
SH = "http://www.w3.org/ns/shacl#"
SKOS = "http://www.w3.org/2004/02/skos/core#"
ALLOWED_DATATYPES = {str(XSD.string), str(XSD.date), str(XSD.dateTime), str(XSD.gYearMonth), str(XSD.decimal), str(XSD.integer), str(XSD.boolean)} if Graph else set()
REJECTED_OWL = {"Restriction","equivalentClass","equivalentProperty","sameAs","differentFrom","unionOf","intersectionOf","complementOf","oneOf","TransitiveProperty","SymmetricProperty","FunctionalProperty","InverseFunctionalProperty","propertyChainAxiom","hasKey","disjointWith","imports","cardinality","minCardinality","maxCardinality","qualifiedCardinality","minQualifiedCardinality","maxQualifiedCardinality","someValuesFrom","allValuesFrom","hasValue"}
BANNED_KEYS = {"endpoint","url","header","headers","token","password","secret","apikey","api_key","bucket","objectkey","object_key","etag","localpath","local_path","connectionstring","connection_string","javascript","script","callback","sql"}


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def add(report: dict[str, Any], level: str, code: str, message: str, path: Path | None = None) -> None:
    item = {"code": code, "message": message}
    if path: item["path"] = str(path)
    report[level + "s"].append(item)


def load_json(path: Path, report: dict[str, Any]) -> Any | None:
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        add(report, "error", "JSON_PARSE", f"JSON 解析失败: {exc}", path); return None


def recursive_key_scan(value: Any, report: dict[str, Any], path: Path) -> None:
    if isinstance(value, dict):
        for k, v in value.items():
            if str(k).replace("-", "_").lower() in BANNED_KEYS:
                add(report, "error", "BANNED_CONFIG", f"语义资产中禁止字段: {k}", path)
            recursive_key_scan(v, report, path)
    elif isinstance(value, list):
        for v in value: recursive_key_scan(v, report, path)


def schema_validate(data: Any, schema_name: str, report: dict[str, Any], path: Path) -> None:
    sp = CONTRACTS / schema_name
    if not sp.exists() or jsonschema is None: return
    try:
        schema = json.loads(sp.read_text(encoding="utf-8"))
        for err in jsonschema.validators.validator_for(schema)(schema).iter_errors(data):
            add(report, "error", "JSON_SCHEMA", err.message, path)
    except Exception as exc:
        add(report, "error", "JSON_SCHEMA", str(exc), path)


def validate_ontology(path: Path, report: dict[str, Any]) -> None:
    if Graph is None:
        add(report, "error", "RDFLIB_MISSING", "缺少 rdflib", path); return
    g = Graph()
    try: g.parse(path, format="turtle")
    except Exception as exc:
        add(report, "error", "TTL_PARSE", f"Turtle 解析失败: {exc}", path); return
    if any(isinstance(x, BNode) for t in g for x in t):
        add(report, "error", "ONTOLOGY_BNODE", "ECP Ontology Profile 禁止 Blank Node", path)
    if not any(isinstance(s, URIRef) for s in g.subjects(RDF.type, OWL.Ontology)):
        add(report, "error", "ONTOLOGY_DECL", "至少需要一个具名 owl:Ontology", path)
    for s,p,o in g:
        for x in (s,p,o):
            xs = str(x)
            if xs.startswith(str(OWL)) and xs.rsplit("#",1)[-1] in REJECTED_OWL:
                add(report, "error", "ONTOLOGY_UNSUPPORTED", f"使用了 ECP Profile 不支持的 OWL 构造: {xs}", path)
    classes = {str(s) for s in g.subjects(RDF.type, OWL.Class)} | {str(s) for s in g.subjects(RDF.type, RDFS.Class)}
    objp = {str(s) for s in g.subjects(RDF.type, OWL.ObjectProperty)}
    datap = {str(s) for s in g.subjects(RDF.type, OWL.DatatypeProperty)}
    for prop in objp | datap:
        p = URIRef(prop); domains=list(g.objects(p,RDFS.domain)); ranges=list(g.objects(p,RDFS.range)); inv=list(g.objects(p,OWL.inverseOf))
        if len(domains)>1: add(report,"error","ONTOLOGY_DOMAIN_COUNT",f"{prop} 多个 domain",path)
        if len(ranges)>1: add(report,"error","ONTOLOGY_RANGE_COUNT",f"{prop} 多个 range",path)
        if len(inv)>1: add(report,"error","ONTOLOGY_INVERSE_COUNT",f"{prop} 多个 inverse",path)
        if domains and str(domains[0]) not in classes: add(report,"error","ONTOLOGY_DOMAIN_UNDECLARED",f"{prop} domain 未声明",path)
        if prop in objp and ranges and str(ranges[0]) not in classes: add(report,"error","ONTOLOGY_OBJECT_RANGE",f"{prop} range 必须是 Class",path)
        if prop in datap and ranges and str(ranges[0]) not in ALLOWED_DATATYPES: add(report,"error","ONTOLOGY_DATATYPE_RANGE",f"{prop} datatype 不支持",path)
    add(report,"check","ONTOLOGY_PARSED",f"Ontology 本地解析完成，共 {len(g)} triples",path)


def validate_shacl(path: Path, report: dict[str, Any]) -> None:
    if Graph is None: return
    g=Graph()
    try: g.parse(path, format="turtle")
    except Exception as exc:
        add(report,"error","TTL_PARSE",str(exc),path); return
    if any(isinstance(x,BNode) for t in g for x in t):
        add(report,"error","SHACL_BNODE","ECP SHACL Profile 禁止匿名复杂结构之外的未受控 Blank Node",path)
    for _,p,_ in g:
        if str(p).startswith(SH) and str(p).rsplit("#",1)[-1] in {"sparql","js"}:
            add(report,"error","SHACL_UNSUPPORTED",f"不支持 {p}",path)


def validate_json_asset(path: Path, data: Any, report: dict[str, Any], ontology_digest: str | None = None) -> None:
    recursive_key_scan(data, report, path)
    if not isinstance(data, dict): return
    kind = data.get("kind")
    api = str(data.get("apiVersion", ""))
    if "evaluation-definition" in api and not data.get("compilerContract"):
        add(report,"warning","EVALUATION_DRAFT","Evaluation definition 缺少编译器权威 compilerContract；仅可作为草稿",path)
        add(report,"warning","ECP_PREFLIGHT_REQUIRED","需要 ECP 编译预检",path)
    if kind == "ActionPolicy": schema_validate(data,"action-policy-v1.schema.json",report,path)
    if kind == "ScopeDefinition": schema_validate(data,"scope-definition-v1.schema.json",report,path)
    if data.get("mappingId") or kind == "MappingDefinition":
        schema_validate(data,"mapping-definition-v1.schema.json",report,path)
        if ontology_digest and data.get("ontologySourceDigest") != ontology_digest:
            add(report,"error","MAPPING_ONTOLOGY_DIGEST","Mapping ontologySourceDigest 与 Ontology 摘要不一致",path)


def validate_rule_manifest(path: Path, root: Path, report: dict[str, Any]) -> None:
    data=load_json(path,report)
    if not isinstance(data,dict): return
    schema_validate(data,"rule-set-bundle-manifest-v1.schema.json",report,path)
    stages=[]
    for m in data.get("members",[]):
        rel=m.get("path"); p=root/rel if rel else None
        if not p or not p.exists(): add(report,"error","RULE_MEMBER_MISSING",f"Manifest 成员不存在: {rel}",path); continue
        if m.get("sourceDigest") != sha256_file(p): add(report,"error","RULE_MEMBER_DIGEST",f"摘要不一致: {rel}",path)
        if m.get("assetType")=="SHACL": stages.append(m.get("shaclStage")); validate_shacl(p,report)
        elif p.suffix==".json":
            j=load_json(p,report)
            if j is not None: validate_json_asset(p,j,report)
    if stages and (set(stages)!={"asserted","domain","feature","change","output","provenance"} or len(stages)!=6):
        add(report,"error","SHACL_STAGE_SET",f"含 SHACL 时必须六阶段各且仅一个；当前 {stages}",path)


def validate_workspace(root: Path, report: dict[str, Any]) -> None:
    mp=root/"manifest.json"; data=load_json(mp,report)
    if not isinstance(data,dict): return
    version=data.get("schemaVersion")
    schema_validate(data,"semantic-workspace-package-manifest-v2.schema.json" if version==2 else "semantic-workspace-package-manifest-v1.schema.json",report,mp)
    scopes=list((root/"scopes").glob("*.json")) if (root/"scopes").exists() else []
    if scopes and version!=2: add(report,"error","SCOPE_REQUIRES_V2","包含 Scope 时 Workspace Package 必须使用 V2",mp)
    om=data.get("ontology",{}); op=root/om.get("path",""); od=None
    if op.exists():
        od=sha256_file(op); validate_ontology(op,report)
        if om.get("sourceDigest")!=od: add(report,"error","WORKSPACE_ONTOLOGY_DIGEST","Ontology sourceDigest 不一致",mp)
    else: add(report,"error","WORKSPACE_ONTOLOGY_MISSING","Ontology 文件不存在",mp)
    mm=data.get("mapping",{}); mpath=root/mm.get("path","")
    if mpath.exists():
        if mm.get("sourceDigest")!=sha256_file(mpath): add(report,"error","WORKSPACE_MAPPING_DIGEST","Mapping sourceDigest 不一致",mp)
        if od and mm.get("ontologySourceDigest")!=od: add(report,"error","WORKSPACE_MAPPING_ONTOLOGY_DIGEST","Mapping ontologySourceDigest 不一致",mp)
        j=load_json(mpath,report)
        if j is not None: validate_json_asset(mpath,j,report,od)
    rm=data.get("ruleSet",{}); rp=root/rm.get("manifestPath","")
    if rp.exists(): validate_rule_manifest(rp,root,report)
    add(report,"warning","ECP_PREFLIGHT_REQUIRED","本地校验不替代 ECP 源码预检、候选编译与发布门禁",mp)


def validate_directory(root: Path, report: dict[str, Any]) -> None:
    mp=root/"manifest.json"
    if mp.exists():
        d=load_json(mp,report)
        if isinstance(d,dict) and d.get("kind")=="ECP_SEMANTIC_WORKSPACE_PACKAGE": validate_workspace(root,report); return
        if isinstance(d,dict) and d.get("kind")=="ECP_RULE_SET_BUNDLE": validate_rule_manifest(mp,root,report)
    od=None
    for ttl in root.rglob("*.ttl"):
        if "shacl" in ttl.parts or "shape" in ttl.name.lower(): validate_shacl(ttl,report)
        else:
            validate_ontology(ttl,report)
            if od is None: od=sha256_file(ttl)
    for js in root.rglob("*.json"):
        if js==mp: continue
        d=load_json(js,report)
        if d is not None: validate_json_asset(js,d,report,od)


def validate_path(path: Path) -> dict[str, Any]:
    report={"tool":"hovo-ecp-semantic/local-validator","ecpProfileId":PROFILE_ID,"ecpProfileDigest":PROFILE_DIGEST,"target":str(path),"errors":[],"warnings":[],"checks":[]}
    if not path.exists(): add(report,"error","PATH_MISSING","目标路径不存在",path)
    elif path.is_dir(): validate_directory(path,report)
    elif path.suffix.lower()==".zip":
        try:
            with tempfile.TemporaryDirectory() as td:
                with zipfile.ZipFile(path) as zf:
                    for info in zf.infolist():
                        if info.filename.startswith("/") or ".." in Path(info.filename).parts: add(report,"error","ZIP_PATH",f"非法路径: {info.filename}",path)
                    zf.extractall(td)
                validate_directory(Path(td),report)
        except Exception as exc: add(report,"error","ZIP_PARSE",str(exc),path)
    elif path.suffix.lower()==".ttl": validate_shacl(path,report) if ("shape" in path.name.lower() or "shacl" in path.name.lower()) else validate_ontology(path,report)
    elif path.suffix.lower()==".json":
        d=load_json(path,report)
        if d is not None: validate_json_asset(path,d,report)
    else: add(report,"error","UNSUPPORTED_TARGET","只支持目录、ZIP、TTL、JSON",path)
    report["summary"]={"errorCount":len(report["errors"]),"warningCount":len(report["warnings"]),"checkCount":len(report["checks"]),"status":"INVALID" if report["errors"] else "LOCALLY_VALID","releaseReady":False,"ecpPreflightRequired":True}
    return report


def main() -> int:
    ap=argparse.ArgumentParser(description="Validate ECP semantic assets against local Authoring Kit 1.7 contracts and static profile rules.")
    ap.add_argument("path"); ap.add_argument("--json-out")
    args=ap.parse_args(); report=validate_path(Path(args.path).resolve()); text=json.dumps(report,ensure_ascii=False,indent=2)
    if args.json_out:
        out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(text+"\n",encoding="utf-8")
    print(text); return 1 if report["errors"] else 0

if __name__=="__main__": raise SystemExit(main())
