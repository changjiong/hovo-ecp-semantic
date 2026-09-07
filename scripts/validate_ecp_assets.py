#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

try:
    import jsonschema
except Exception as exc:  # pragma: no cover
    jsonschema = None
    JSONSCHEMA_IMPORT_ERROR = str(exc)
else:
    JSONSCHEMA_IMPORT_ERROR = None

try:
    from rdflib import BNode, Graph, Literal, URIRef
    from rdflib.namespace import OWL, RDF, RDFS, XSD
except Exception as exc:  # pragma: no cover
    Graph = None
    RDFLIB_IMPORT_ERROR = str(exc)
else:
    RDFLIB_IMPORT_ERROR = None

SKILL_ROOT = Path(__file__).resolve().parents[1]
KIT_ROOT = SKILL_ROOT / "references" / "ecp-kit-1.7"
CONTRACTS = KIT_ROOT / "contracts"
PROFILE_MANIFEST = CONTRACTS / "ecp-semantic-profile-1.0.json"

PROFILE_ID = "enterprise-cognitive/semantic-profile/1.0.0"
PROFILE_DIGEST = "sha256:708246ab3a0ce13a23977d39712a82f9a363f16a9c2fe428fe0311e4147b1882"

SH = "http://www.w3.org/ns/shacl#"
SKOS = "http://www.w3.org/2004/02/skos/core#"

ALLOWED_ONTOLOGY_TYPES = {
    str(OWL.Ontology),
    str(OWL.Class),
    str(RDFS.Class),
    str(OWL.ObjectProperty),
    str(OWL.DatatypeProperty),
    str(OWL.AnnotationProperty),
    str(OWL.NamedIndividual),
}
ALLOWED_SCHEMA_PREDS = {
    str(RDFS.subClassOf), str(RDFS.subPropertyOf), str(RDFS.domain), str(RDFS.range), str(OWL.inverseOf)
}
ALLOWED_METADATA_PREDS = {
    str(RDFS.label), str(RDFS.comment), SKOS + "prefLabel", str(OWL.versionIRI), str(OWL.versionInfo)
}
ALLOWED_DATATYPES = {
    str(XSD.string), str(XSD.date), str(XSD.dateTime), str(XSD.gYearMonth),
    str(XSD.decimal), str(XSD.integer), str(XSD.boolean)
}
REJECTED_OWL_TERMS = {
    str(OWL.Restriction), str(OWL.equivalentClass), str(OWL.equivalentProperty), str(OWL.sameAs),
    str(OWL.differentFrom), str(OWL.unionOf), str(OWL.intersectionOf), str(OWL.complementOf),
    str(OWL.oneOf), str(OWL.TransitiveProperty), str(OWL.SymmetricProperty), str(OWL.FunctionalProperty),
    str(OWL.InverseFunctionalProperty), str(OWL.propertyChainAxiom), str(OWL.hasKey), str(OWL.disjointWith),
    str(OWL.imports), str(OWL.cardinality), str(OWL.minCardinality), str(OWL.maxCardinality),
    str(OWL.qualifiedCardinality), str(OWL.minQualifiedCardinality), str(OWL.maxQualifiedCardinality),
    str(OWL.someValuesFrom), str(OWL.allValuesFrom), str(OWL.hasValue)
}

ALLOWED_SH_PREDS = {
    SH + x for x in [
        "targetClass", "targetNode", "targetSubjectsOf", "targetObjectsOf", "property", "path", "severity",
        "message", "minCount", "maxCount", "datatype", "nodeKind", "class", "minInclusive", "maxInclusive",
        "pattern", "in", "hasValue", "or", "and", "not"
    ]
}
ALLOWED_SH_TYPES = {SH + "NodeShape", SH + "PropertyShape"}
ALLOWED_SH_SEVERITIES = {SH + "Violation", SH + "Warning", SH + "Info"}
ALLOWED_SH_TARGET_PREDS = {SH + x for x in ["targetClass", "targetNode", "targetSubjectsOf", "targetObjectsOf"]}

BANNED_JSON_KEYS = {
    "endpoint", "url", "header", "headers", "token", "password", "secret", "apikey", "api_key",
    "bucket", "objectkey", "object_key", "etag", "localpath", "local_path", "connectionstring",
    "connection_string", "javascript", "script", "callback", "sql"
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def add(report: dict[str, Any], level: str, code: str, message: str, path: Path | None = None) -> None:
    item = {"level": level, "code": code, "message": message}
    if path:
        item["path"] = str(path)
    report[level + "s"].append(item)


def load_json(path: Path, report: dict[str, Any]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        add(report, "error", "JSON_PARSE", f"JSON 解析失败: {exc}", path)
        return None


def validate_json_schema(instance: Any, schema_path: Path, report: dict[str, Any], asset_path: Path) -> None:
    if jsonschema is None:
        add(report, "error", "JSONSCHEMA_MISSING", f"缺少 jsonschema 依赖: {JSONSCHEMA_IMPORT_ERROR}", asset_path)
        return
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        pointer = "/" + "/".join(str(x) for x in err.path) if err.path else "/"
        add(report, "error", "JSON_SCHEMA", f"{schema_path.name} {pointer}: {err.message}", asset_path)


def recursive_key_scan(value: Any, report: dict[str, Any], path: Path, location: str = "$") -> None:
    if isinstance(value, dict):
        for k, v in value.items():
            norm = str(k).replace("-", "_").lower()
            if norm in BANNED_JSON_KEYS:
                add(report, "error", "BANNED_CONFIG", f"语义资产中禁止字段 {location}.{k}", path)
            recursive_key_scan(v, report, path, location + "." + str(k))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            recursive_key_scan(item, report, path, f"{location}[{i}]")


def validate_ontology(path: Path, report: dict[str, Any]) -> None:
    if Graph is None:
        add(report, "error", "RDFLIB_MISSING", f"缺少 rdflib 依赖: {RDFLIB_IMPORT_ERROR}", path)
        return
    g = Graph()
    try:
        g.parse(path, format="turtle")
    except Exception as exc:
        add(report, "error", "TTL_PARSE", f"Turtle 解析失败: {exc}", path)
        return
    if len(g) > 100000:
        add(report, "error", "ONTOLOGY_LIMIT", f"Ontology triple 数 {len(g)} 超过 100000", path)
    if any(isinstance(t, BNode) for triple in g for t in triple):
        add(report, "error", "ONTOLOGY_BNODE", "ECP Ontology Profile 禁止 Blank Node（空白节点）", path)

    ontologies = [s for s in g.subjects(RDF.type, OWL.Ontology) if isinstance(s, URIRef)]
    if not ontologies:
        add(report, "error", "ONTOLOGY_DECL", "至少需要一个具名 owl:Ontology", path)

    declared_classes = {str(s) for s in g.subjects(RDF.type, OWL.Class)} | {str(s) for s in g.subjects(RDF.type, RDFS.Class)}
    obj_props = {str(s) for s in g.subjects(RDF.type, OWL.ObjectProperty)}
    data_props = {str(s) for s in g.subjects(RDF.type, OWL.DatatypeProperty)}
    ann_props = {str(s) for s in g.subjects(RDF.type, OWL.AnnotationProperty)}
    declared_props = obj_props | data_props | ann_props

    for s, p, o in g:
        if str(s) in REJECTED_OWL_TERMS or str(p) in REJECTED_OWL_TERMS or str(o) in REJECTED_OWL_TERMS:
            add(report, "error", "ONTOLOGY_UNSUPPORTED", f"使用了 ECP Profile 不支持的 OWL 构造: {(s, p, o)}", path)
        ps = str(p)
        if ps == str(RDF.type):
            if isinstance(o, URIRef):
                os = str(o)
                if os.startswith(str(OWL)) or os.startswith(str(RDFS)):
                    if os not in ALLOWED_ONTOLOGY_TYPES and os not in declared_classes:
                        add(report, "error", "ONTOLOGY_TYPE_UNSUPPORTED", f"不支持的类型声明: {os}", path)
            continue
        if ps.startswith(str(OWL)) or ps.startswith(str(RDFS)) or ps.startswith(str(RDF)) or ps.startswith(SKOS):
            if ps not in ALLOWED_SCHEMA_PREDS | ALLOWED_METADATA_PREDS:
                add(report, "error", "ONTOLOGY_PRED_UNSUPPORTED", f"不支持的 Schema/元数据谓词: {ps}", path)
        elif ps not in declared_props:
            add(report, "warning", "ONTOLOGY_CUSTOM_PRED", f"出现未声明为 Property 的自定义谓词: {ps}", path)

    for prop in obj_props | data_props:
        p = URIRef(prop)
        domains = list(g.objects(p, RDFS.domain))
        ranges = list(g.objects(p, RDFS.range))
        inverses = list(g.objects(p, OWL.inverseOf))
        if len(domains) > 1:
            add(report, "error", "ONTOLOGY_DOMAIN_COUNT", f"Property {prop} 声明了多个 domain", path)
        if len(ranges) > 1:
            add(report, "error", "ONTOLOGY_RANGE_COUNT", f"Property {prop} 声明了多个 range", path)
        if len(inverses) > 1:
            add(report, "error", "ONTOLOGY_INVERSE_COUNT", f"Property {prop} 声明了多个 inverse", path)
        if domains and str(domains[0]) not in declared_classes:
            add(report, "error", "ONTOLOGY_DOMAIN_UNDECLARED", f"Property {prop} domain 未声明为 Class: {domains[0]}", path)
        if prop in obj_props:
            if ranges and str(ranges[0]) not in declared_classes:
                add(report, "error", "ONTOLOGY_OBJECT_RANGE", f"ObjectProperty {prop} range 必须是已声明 Class: {ranges[0]}", path)
            for inv in inverses:
                if str(inv) not in obj_props:
                    add(report, "error", "ONTOLOGY_INVERSE_KIND", f"inverseOf 另一端不是已声明 ObjectProperty: {inv}", path)
        else:
            if ranges and str(ranges[0]) not in ALLOWED_DATATYPES:
                add(report, "error", "ONTOLOGY_DATATYPE_RANGE", f"DatatypeProperty {prop} range 不在 ECP 支持范围: {ranges[0]}", path)

    for child, parent in g.subject_objects(RDFS.subClassOf):
        if str(child) not in declared_classes or str(parent) not in declared_classes:
            add(report, "error", "ONTOLOGY_SUBCLASS_UNDECLARED", f"subClassOf 两端必须是已声明 Class: {child} -> {parent}", path)
    for child, parent in g.subject_objects(RDFS.subPropertyOf):
        c, par = str(child), str(parent)
        if c not in obj_props | data_props or par not in obj_props | data_props:
            add(report, "error", "ONTOLOGY_SUBPROPERTY_UNDECLARED", f"subPropertyOf 两端必须是已声明 Property: {child} -> {parent}", path)
        elif (c in obj_props) != (par in obj_props):
            add(report, "error", "ONTOLOGY_SUBPROPERTY_KIND", f"subPropertyOf 两端 Property Kind 不一致: {child} -> {parent}", path)

    add(report, "check", "ONTOLOGY_PARSED", f"Ontology 本地解析完成，共 {len(g)} triples", path)


def validate_shacl(path: Path, report: dict[str, Any]) -> None:
    if Graph is None:
        add(report, "error", "RDFLIB_MISSING", f"缺少 rdflib 依赖: {RDFLIB_IMPORT_ERROR}", path)
        return
    g = Graph()
    try:
        g.parse(path, format="turtle")
    except Exception as exc:
        add(report, "error", "SHACL_PARSE", f"SHACL Turtle 解析失败: {exc}", path)
        return
    if len(g) > 50000:
        add(report, "error", "SHACL_LIMIT", f"单 Stage Shape triple 数 {len(g)} 超过 50000", path)
    has_target = False
    for s, p, o in g:
        ps = str(p)
        if ps.startswith(SH):
            if ps not in ALLOWED_SH_PREDS:
                add(report, "error", "SHACL_PRED_UNSUPPORTED", f"不支持的 SHACL Predicate: {ps}", path)
            if ps in ALLOWED_SH_TARGET_PREDS:
                has_target = True
                if not isinstance(o, URIRef):
                    add(report, "error", "SHACL_TARGET_KIND", f"SHACL Target 必须是具名 IRI: {o}", path)
            if ps == SH + "path" and not isinstance(o, URIRef):
                add(report, "error", "SHACL_PATH", "Property Shape 的 sh:path 必须是直接具名 IRI", path)
            if ps == SH + "severity" and str(o) not in ALLOWED_SH_SEVERITIES:
                add(report, "error", "SHACL_SEVERITY", f"不支持的 severity: {o}", path)
        if ps == str(RDF.type) and isinstance(o, URIRef) and str(o).startswith(SH):
            if str(o) not in ALLOWED_SH_TYPES:
                add(report, "error", "SHACL_TYPE_UNSUPPORTED", f"不支持的 SHACL 类型: {o}", path)
    if len(g) > 0 and not has_target:
        add(report, "warning", "SHACL_NO_TARGET", "Shape Graph 非空但未发现受支持 Target；请确认是否为仅被引用的 Shape", path)
    add(report, "check", "SHACL_PARSED", f"SHACL 本地解析完成，共 {len(g)} triples", path)


def validate_json_asset(path: Path, data: Any, report: dict[str, Any], ontology_digest: str | None = None) -> None:
    recursive_key_scan(data, report, path)
    if not isinstance(data, dict):
        return
    kind = data.get("kind")
    if "mappingId" in data and data.get("schemaVersion") == 1:
        validate_json_schema(data, CONTRACTS / "mapping-definition-v1.schema.json", report, path)
        if ontology_digest and data.get("ontologySourceDigest") != ontology_digest:
            add(report, "error", "MAPPING_ONTOLOGY_DIGEST", f"Mapping ontologySourceDigest 与 Ontology 原始字节摘要不一致；期望 {ontology_digest}", path)
    elif kind == "ActionPolicy":
        validate_json_schema(data, CONTRACTS / "action-policy-v1.schema.json", report, path)
    elif kind == "ScopeDefinition":
        validate_json_schema(data, CONTRACTS / "scope-definition-v1.schema.json", report, path)
    elif kind == "FeatureDefinition":
        if data.get("apiVersion") != "enterprise-risk/feature-definition/v2":
            add(report, "error", "DERIVATION_VERSION", "Derivation 必须使用 enterprise-risk/feature-definition/v2", path)
        if data.get("spec", {}).get("kind") != "typedPlan":
            add(report, "error", "DERIVATION_KIND", "Derivation spec.kind 必须是 typedPlan", path)
        add(report, "warning", "COMPILER_PREFLIGHT", "Derivation 的有限算子、类型、依赖和 DAG 仍需 ECP Compiler 预检", path)
    elif kind == "EvaluationAsset" or data.get("apiVersion") == "enterprise-cognitive/evaluation-definition/v1":
        if kind == "EvaluationAsset":
            if "compilerContract" not in data:
                add(report, "error", "EVALUATION_COMPILER_CONTRACT", "正式 EvaluationAsset 缺少 compilerContract；不得伪造，需 ECP 预检生成", path)
            else:
                add(report, "warning", "COMPILER_CONTRACT_UNVERIFIED", "compilerContract.expect 无法由本地工具证明为 ECP 编译器真实输出", path)
        else:
            add(report, "warning", "EVALUATION_DRAFT", "检测到 Evaluation Definition 草稿；未包装真实 compilerContract，不能登记进正式规则 Manifest", path)
    elif data.get("kind") == "ECP_RULE_SET_BUNDLE":
        validate_json_schema(data, CONTRACTS / "rule-set-bundle-manifest-v1.schema.json", report, path)
    elif data.get("kind") == "ECP_SEMANTIC_WORKSPACE_PACKAGE":
        schema_version = data.get("schemaVersion")
        schema_name = "semantic-workspace-package-manifest-v2.schema.json" if schema_version == 2 else "semantic-workspace-package-manifest-v1.schema.json"
        validate_json_schema(data, CONTRACTS / schema_name, report, path)


def validate_rule_manifest(manifest_path: Path, package_root: Path, report: dict[str, Any]) -> None:
    data = load_json(manifest_path, report)
    if data is None:
        return
    validate_json_schema(data, CONTRACTS / "rule-set-bundle-manifest-v1.schema.json", report, manifest_path)
    if data.get("semanticProfileId") != PROFILE_ID or data.get("semanticProfileDigest") != PROFILE_DIGEST:
        add(report, "error", "PROFILE_BINDING", "Rule Set Manifest 的 Semantic Profile ID/Digest 与 Kit 1.7 不一致", manifest_path)
    shacl_stages = []
    for m in data.get("members", []):
        rel = m.get("path")
        if not rel:
            continue
        member = package_root / rel
        if not member.exists():
            add(report, "error", "RULE_MEMBER_MISSING", f"Manifest 成员不存在: {rel}", manifest_path)
            continue
        expected = m.get("sourceDigest")
        actual = sha256_file(member)
        if expected != actual:
            add(report, "error", "RULE_MEMBER_DIGEST", f"规则成员摘要不一致 {rel}: {expected} != {actual}", manifest_path)
        asset_type = m.get("assetType")
        if asset_type == "SHACL":
            shacl_stages.append(m.get("shaclStage"))
            validate_shacl(member, report)
        elif asset_type in {"DERIVATION", "EVALUATION", "ACTION_POLICY"}:
            j = load_json(member, report)
            if j is not None:
                validate_json_asset(member, j, report)
                if asset_type == "EVALUATION" and isinstance(j, dict) and j.get("kind") != "EvaluationAsset":
                    add(report, "error", "RULE_MANIFEST_EVAL_DRAFT", f"规则 Manifest 不能登记未包装 compilerContract 的 Evaluation 草稿: {rel}", manifest_path)
    if shacl_stages:
        expected = {"asserted", "domain", "feature", "change", "output", "provenance"}
        if set(shacl_stages) != expected or len(shacl_stages) != 6:
            add(report, "error", "SHACL_STAGE_SET", f"含 SHACL 时必须六阶段各且仅一个；当前 {shacl_stages}", manifest_path)


def validate_workspace(root: Path, report: dict[str, Any]) -> None:
    manifest_path = root / "manifest.json"
    data = load_json(manifest_path, report)
    if data is None:
        return
    if data.get("kind") != "ECP_SEMANTIC_WORKSPACE_PACKAGE":
        return
    version = data.get("schemaVersion")
    if version not in {1, 2}:
        add(report, "error", "WORKSPACE_VERSION", f"Workspace schemaVersion 只支持 1/2，当前 {version}", manifest_path)
        return
    schema = CONTRACTS / ("semantic-workspace-package-manifest-v2.schema.json" if version == 2 else "semantic-workspace-package-manifest-v1.schema.json")
    validate_json_schema(data, schema, report, manifest_path)
    if data.get("semanticProfileId") != PROFILE_ID or data.get("semanticProfileDigest") != PROFILE_DIGEST:
        add(report, "error", "PROFILE_BINDING", "Workspace Manifest 的 Semantic Profile ID/Digest 与 Kit 1.7 不一致", manifest_path)

    scope_files = list((root / "scopes").glob("*.json")) if (root / "scopes").exists() else []
    if scope_files and version != 2:
        add(report, "error", "SCOPE_REQUIRES_V2", "包含 Scope 时 Workspace Package 必须使用 V2", manifest_path)
    if not scope_files and version == 2 and data.get("scopes"):
        add(report, "error", "SCOPE_DECL_MISSING", "Manifest 声明 Scope 但 scopes/ 文件不存在", manifest_path)

    ontology_meta = data.get("ontology", {})
    ontology_path = root / ontology_meta.get("path", "")
    ontology_digest = None
    if ontology_path.exists():
        ontology_digest = sha256_file(ontology_path)
        if ontology_meta.get("sourceDigest") != ontology_digest:
            add(report, "error", "WORKSPACE_ONTOLOGY_DIGEST", "Workspace Ontology sourceDigest 不一致", manifest_path)
        validate_ontology(ontology_path, report)
    else:
        add(report, "error", "WORKSPACE_ONTOLOGY_MISSING", f"Ontology 文件不存在: {ontology_meta.get('path')}", manifest_path)

    mapping_meta = data.get("mapping", {})
    mapping_path = root / mapping_meta.get("path", "")
    if mapping_path.exists():
        md = sha256_file(mapping_path)
        if mapping_meta.get("sourceDigest") != md:
            add(report, "error", "WORKSPACE_MAPPING_DIGEST", "Workspace Mapping sourceDigest 不一致", manifest_path)
        if ontology_digest and mapping_meta.get("ontologySourceDigest") != ontology_digest:
            add(report, "error", "WORKSPACE_MAPPING_ONTOLOGY_DIGEST", "Workspace Manifest mapping.ontologySourceDigest 与 Ontology 摘要不一致", manifest_path)
        mapping = load_json(mapping_path, report)
        if mapping is not None:
            validate_json_asset(mapping_path, mapping, report, ontology_digest)
    else:
        add(report, "error", "WORKSPACE_MAPPING_MISSING", f"Mapping 文件不存在: {mapping_meta.get('path')}", manifest_path)

    rule_meta = data.get("ruleSet", {})
    rule_manifest = root / rule_meta.get("manifestPath", "")
    if rule_manifest.exists():
        if rule_meta.get("sourceDigest") != sha256_file(rule_manifest):
            add(report, "error", "WORKSPACE_RULESET_DIGEST", "Workspace ruleSet sourceDigest 不一致", manifest_path)
        validate_rule_manifest(rule_manifest, root, report)
    else:
        add(report, "error", "WORKSPACE_RULESET_MISSING", f"Rule Set Manifest 不存在: {rule_meta.get('manifestPath')}", manifest_path)

    for s in data.get("schemas", []):
        p = root / s.get("path", "")
        if not p.exists():
            add(report, "error", "SCHEMA_SNAPSHOT_MISSING", f"Schema 快照不存在: {s.get('path')}", manifest_path)
        elif s.get("sourceDigest") != sha256_file(p):
            add(report, "error", "SCHEMA_SNAPSHOT_DIGEST", f"Schema 快照摘要不一致: {s.get('path')}", manifest_path)

    if version == 2:
        for s in data.get("scopes", []):
            p = root / s.get("path", "")
            if not p.exists():
                add(report, "error", "SCOPE_MISSING", f"Scope 文件不存在: {s.get('path')}", manifest_path)
            else:
                if s.get("sourceDigest") != sha256_file(p):
                    add(report, "error", "SCOPE_DIGEST", f"Scope 摘要不一致: {s.get('path')}", manifest_path)
                scope = load_json(p, report)
                if scope is not None:
                    validate_json_asset(p, scope, report)

    add(report, "warning", "ECP_PREFLIGHT_REQUIRED", "本地校验不替代 ECP 源码预检、当前 Hovo Schema 发现、候选编译与发布门禁", manifest_path)


def validate_directory(root: Path, report: dict[str, Any]) -> None:
    manifest = root / "manifest.json"
    if manifest.exists():
        data = load_json(manifest, report)
        if isinstance(data, dict) and data.get("kind") == "ECP_SEMANTIC_WORKSPACE_PACKAGE":
            validate_workspace(root, report)
            return
        if isinstance(data, dict) and data.get("kind") == "ECP_RULE_SET_BUNDLE":
            validate_rule_manifest(manifest, root, report)
    ontology_digest = None
    ontology_files = list(root.rglob("*.ttl"))
    for ttl in ontology_files:
        if "shacl" in ttl.parts or "rules" in ttl.parts and ttl.name.endswith("shapes.ttl"):
            validate_shacl(ttl, report)
        else:
            validate_ontology(ttl, report)
            if ontology_digest is None:
                ontology_digest = sha256_file(ttl)
    for js in root.rglob("*.json"):
        if js == manifest:
            continue
        data = load_json(js, report)
        if data is not None:
            validate_json_asset(js, data, report, ontology_digest)


def validate_path(path: Path) -> dict[str, Any]:
    report: dict[str, Any] = {
        "tool": "hovo-ecp-semantic/local-validator",
        "ecpProfileId": PROFILE_ID,
        "ecpProfileDigest": PROFILE_DIGEST,
        "target": str(path),
        "errors": [], "warnings": [], "checks": []
    }
    if not path.exists():
        add(report, "error", "PATH_MISSING", "目标路径不存在", path)
    elif path.is_dir():
        validate_directory(path, report)
    elif path.suffix.lower() == ".zip":
        try:
            with tempfile.TemporaryDirectory() as td:
                with zipfile.ZipFile(path) as zf:
                    for info in zf.infolist():
                        n = info.filename
                        if n.startswith("/") or ".." in Path(n).parts or "\\" in n:
                            add(report, "error", "ZIP_PATH", f"ZIP 包含非法路径: {n}", path)
                        if info.file_size > 5_242_880:
                            add(report, "error", "ZIP_FILE_LIMIT", f"ZIP 单文件超过 5,242,880 bytes: {n}", path)
                    zf.extractall(td)
                tmp = Path(td)
                roots = [p for p in tmp.iterdir() if p.name not in {"__MACOSX"}]
                root = roots[0] if len(roots) == 1 and roots[0].is_dir() and not (tmp / "manifest.json").exists() else tmp
                validate_directory(root, report)
        except Exception as exc:
            add(report, "error", "ZIP_PARSE", f"ZIP 读取失败: {exc}", path)
    elif path.suffix.lower() == ".ttl":
        text = path.name.lower()
        if "shape" in text or "shacl" in text:
            validate_shacl(path, report)
        else:
            validate_ontology(path, report)
    elif path.suffix.lower() == ".json":
        data = load_json(path, report)
        if data is not None:
            validate_json_asset(path, data, report)
    else:
        add(report, "error", "UNSUPPORTED_TARGET", "只支持目录、ZIP、TTL、JSON", path)

    report["summary"] = {
        "errorCount": len(report["errors"]),
        "warningCount": len(report["warnings"]),
        "checkCount": len(report["checks"]),
        "status": "INVALID" if report["errors"] else "LOCALLY_VALID",
        "releaseReady": False,
        "ecpPreflightRequired": True
    }
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate ECP semantic assets against local Authoring Kit 1.7 contracts and static profile rules.")
    ap.add_argument("path")
    ap.add_argument("--json-out")
    args = ap.parse_args()
    report = validate_path(Path(args.path).resolve())
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
