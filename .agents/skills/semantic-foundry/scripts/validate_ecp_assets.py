#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from urllib.parse import urlparse
from decimal import Decimal, InvalidOperation
import tempfile
import zipfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from workspace_files import PackageError, collect_files, enforce_rule_bundle_limits, safe_path, read_json, unpack_zip, snapshot_digest

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
TOOL_MANIFEST = read_json(SKILL_ROOT / "manifest.json")
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
    if level == "check": item["status"] = "EXECUTED"
    if path:
        item["path"] = str(path)
    report[level + "s"].append(item)


def load_json(path: Path, report: dict[str, Any]) -> Any | None:
    try:
        return read_json(path)
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
    validator = validator_cls(schema, format_checker=jsonschema.FormatChecker())
    add(report, "check", "JSON_SCHEMA_EXECUTED", f"已执行结构合同: {schema_path.name}", asset_path)
    for err in sorted(validator.iter_errors(instance), key=lambda e: str(list(e.path))):
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

    for term in {t for triple in g for t in triple if isinstance(t, URIRef)}:
        if urlparse(str(term)).scheme not in {"http", "https", "urn"} or any(c.isspace() for c in str(term)):
            add(report, "error", "ONTOLOGY_IRI", f"不支持或非绝对IRI: {term}", path)
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
                elif os not in declared_classes:
                    add(report, "error", "ONTOLOGY_INSTANCE_CLASS", f"实例类型未在本文件声明: {os}", path)
            else:
                add(report, "error", "ONTOLOGY_TYPE_KIND", "rdf:type 的对象必须是IRI", path)
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
    static_shape_parameters(g, path, report)
    add(report, "check", "SHACL_STATIC_EXECUTED", f"有限配置及参数检查，共 {len(g)} triples；未执行实例约束", path)


def static_shape_parameters(g: Graph, path: Path, report: dict[str, Any]) -> None:
    def err(code, text): add(report, "error", code, text, path)
    def objects(subject, local): return list(g.objects(subject, URIRef(SH+local)))
    property_shapes=set(g.subjects(RDF.type, URIRef(SH+"PropertyShape"))) | set(g.objects(None,URIRef(SH+"property"))) | set(g.subjects(URIRef(SH+"path"),None))
    for shape in property_shapes:
        paths=objects(shape,"path")
        if len(paths)!=1 or not isinstance(paths[0],URIRef):err("SHACL_PATH_COUNT",f"属性形状必须恰好有一个直接IRI路径: {shape}")
    for shape in g.subjects(RDF.type,URIRef(SH+"NodeShape")):
        if not any(list(g.objects(shape,URIRef(t))) for t in ALLOWED_SH_TARGET_PREDS):
            err("SHACL_NODE_TARGET",f"ECP具名节点形状缺少支持的目标: {shape}")
        if objects(shape,"path"):err("SHACL_NODE_PATH",f"节点形状不能带属性路径: {shape}")
    single=["severity","path"]  # ECP正式配置§6.1允许同一约束参数重复并按合取执行
    for local in single:
        pred=URIRef(SH+local)
        for shape in set(g.subjects(pred,None)):
            vals=list(g.objects(shape,pred))
            if len(vals)!=1:err("SHACL_PARAMETER_COUNT",f"参数必须单值: {shape} {local}")
    for local in ["minCount","maxCount"]:
        for shape,value in g.subject_objects(URIRef(SH+local)):
            valid=isinstance(value,Literal) and value.datatype==XSD.integer and re.fullmatch(r"[+]?[0-9]+",str(value)) is not None
            if not valid or not 0<=int(str(value))<=1000000:err("SHACL_COUNT",f"{local}必须是0到1000000的xsd:integer: {shape}")
    for shape in property_shapes:
        lo,hi=objects(shape,"minCount"),objects(shape,"maxCount")
        if lo and hi:
            try:
                if max(map(int,lo))>min(map(int,hi)):add(report,"warning","SHACL_COUNT_RANGE",f"有效最小基数大于最大基数，需核对意图及目标: {shape}",path)
            except (ValueError,TypeError):pass
    for local in ["datatype","class","path","targetClass","targetSubjectsOf","targetObjectsOf"]:
        for shape,value in g.subject_objects(URIRef(SH+local)):
            if not isinstance(value,URIRef):err("SHACL_PARAMETER_IRI",f"{local}参数必须是IRI: {shape}")
    for shape,value in g.subject_objects(URIRef(SH+"datatype")):
        if str(value) not in ALLOWED_DATATYPES:err("SHACL_DATATYPE",f"不支持的数据类型: {value}")
    for shape,value in g.subject_objects(URIRef(SH+"nodeKind")):
        if value!=URIRef(SH+"IRI"):err("SHACL_NODE_KIND",f"ECP仅支持sh:IRI: {shape}")
    for local in ["message","pattern"]:
        for shape,value in g.subject_objects(URIRef(SH+local)):
            if not isinstance(value,Literal) or value.datatype not in {None,XSD.string,RDF.langString}:
                err("SHACL_TEXT",f"{local}必须是文本: {shape}")
    # 模式使用ECMAScript；不能以Python正则编译冒充平台方言验证。
    if any(g.triples((None,URIRef(SH+"pattern"),None))):
        add(report,"warning","PATTERN_DIALECT_NOT_EXECUTED","ECMAScript模式执行留待平台；这里只检查文本类型",path)
    for local in ["minInclusive","maxInclusive"]:
        for shape,value in g.subject_objects(URIRef(SH+local)):
            if not isinstance(value,Literal):err("SHACL_BOUND_TYPE",f"{local}必须是字面量: {shape}")
            elif value.datatype in {XSD.decimal,XSD.integer}:
                try:
                    if not Decimal(str(value)).is_finite():raise ValueError()
                except (ValueError,InvalidOperation):err("SHACL_BOUND_VALUE",f"{local}数值非法: {shape}")
    for local in ["in","or","and"]:
        for shape,head in g.subject_objects(URIRef(SH+local)):
            seen=set(); count=0; node=head
            while node!=RDF.nil:
                if node in seen or count>=4096:
                    err("SHACL_LIST",f"列表有环或超限: {shape} {local}");break
                if not isinstance(node,BNode):
                    err("SHACL_LIST",f"ECP列表单元必须为空白节点: {shape} {local}");break
                seen.add(node); fs=list(g.objects(node,RDF.first)); rs=list(g.objects(node,RDF.rest))
                if len(fs)!=1 or len(rs)!=1:
                    err("SHACL_LIST",f"列表结构不完整: {shape} {local}");break
                if local in {"or","and"} and not isinstance(fs[0],(URIRef,BNode)):
                    err("SHACL_LIST",f"逻辑列表成员不是形状引用: {shape}")
                node=rs[0];count+=1
    for local in ["not","property"]:
        for shape,value in g.subject_objects(URIRef(SH+local)):
            if not isinstance(value,(URIRef,BNode)):err("SHACL_SHAPE_REFERENCE",f"{local}必须引用形状而非字面量: {shape}")
    if len(g)==0:
        add(report,"warning","EMPTY_STAGE_SHAPES","空形状仅能作为显式阶段占位，不证明任何数据质量",path)


def validate_mapping_references(data: dict[str, Any], path: Path, report: dict[str, Any]) -> None:
    """Check IDs and local references; Hovo discovery and compiler checks remain remote."""
    def items(name: str) -> list[dict[str, Any]]:
        value=data.get(name,[])
        return [item for item in value if isinstance(item,dict)] if isinstance(value,list) else []

    def index(name: str, key: str="id") -> dict[str, dict[str, Any]]:
        result={}
        for item in items(name):
            value=item.get(key)
            if not isinstance(value,str):
                continue
            if value in result:
                add(report,"error","MAPPING_DUPLICATE_ID",f"{name} 存在重复 {key}: {value}",path)
            else:
                result[value]=item
        return result

    def require(indexed: dict[str, dict[str, Any]], value: Any, code: str, text: str) -> bool:
        if not isinstance(value,str) or value not in indexed:
            add(report,"error",code,text,path)
            return False
        return True

    sources=index("dataSources","ref")
    scans=index("scans")
    joins=index("joins")
    entities=index("entities")
    properties=index("properties")
    relationships=index("relationships")
    filters=index("filters")

    def scan_column(scan_id: Any, column: Any, code: str, text: str) -> bool:
        if not require(scans,scan_id,code,text):
            return False
        if not isinstance(column,str) or column not in scans[scan_id].get("columns",[]):
            add(report,"error",code,text,path)
            return False
        return True

    for scan_id, scan in scans.items():
        require(sources,scan.get("dataSourceRef"),"MAPPING_DATASOURCE_REF",f"Scan {scan_id} 引用不存在的数据源")
        for column in scan.get("recordKey",[]):
            if column not in scan.get("columns",[]):
                add(report,"error","MAPPING_RECORD_KEY",f"Scan {scan_id} 的 recordKey 不在 columns 中: {column}",path)

    join_endpoints={}
    for join_id, join in joins.items():
        left=join.get("left",{}); right=join.get("right",{})
        left_id=left.get("scanId") if isinstance(left,dict) else None
        right_id=right.get("scanId") if isinstance(right,dict) else None
        left_ok=require(scans,left_id,"MAPPING_JOIN_SCAN",f"Join {join_id} 左侧 Scan 不存在")
        right_ok=require(scans,right_id,"MAPPING_JOIN_SCAN",f"Join {join_id} 右侧 Scan 不存在")
        if left_ok and right_ok and scans[left_id].get("dataSourceRef")!=scans[right_id].get("dataSourceRef"):
            add(report,"error","MAPPING_JOIN_DATASOURCE",f"Join {join_id} 两端必须属于同一数据源",path)
        left_columns=left.get("columns",[]) if isinstance(left,dict) else []
        right_columns=right.get("columns",[]) if isinstance(right,dict) else []
        if len(left_columns)!=len(right_columns):
            add(report,"error","MAPPING_JOIN_ARITY",f"Join {join_id} 两端列数必须相同",path)
        for column in left_columns:
            scan_column(left_id,column,"MAPPING_JOIN_COLUMN",f"Join {join_id} 左侧列未在 Scan 中声明: {column}")
        for column in right_columns:
            scan_column(right_id,column,"MAPPING_JOIN_COLUMN",f"Join {join_id} 右侧列未在 Scan 中声明: {column}")
        if left_ok and right_ok:
            join_endpoints[join_id]=(left_id,right_id)

    for entity_id, entity in entities.items():
        anchor=entity.get("anchorScanId")
        require(scans,anchor,"MAPPING_ENTITY_ANCHOR",f"Entity {entity_id} 的 anchorScanId 不存在")
        selected=[]
        for join_id in entity.get("joinIds",[]):
            if require(joins,join_id,"MAPPING_ENTITY_JOIN",f"Entity {entity_id} 引用不存在的 Join: {join_id}"):
                selected.append(join_id)
        if isinstance(anchor,str) and anchor in scans:
            reachable={anchor}; remaining=set(selected)
            while remaining:
                expanded={join_id for join_id in remaining if join_id in join_endpoints and (join_endpoints[join_id][0] in reachable or join_endpoints[join_id][1] in reachable)}
                if not expanded:
                    break
                for join_id in expanded:
                    reachable.update(join_endpoints[join_id])
                remaining-=expanded
            for join_id in sorted(remaining):
                add(report,"error","MAPPING_ENTITY_JOIN_REACHABILITY",f"Entity {entity_id} 的 Join 不可从 anchorScanId 到达: {join_id}",path)
        identity=entity.get("identity",{})
        if not isinstance(identity,dict):
            continue
        template=identity.get("template","")
        template_vars=set(re.findall(r"\{([A-Za-z][A-Za-z0-9_-]{0,62})\}",template)) if isinstance(template,str) else set()
        bindings={}
        for binding in identity.get("bindings",[]) if isinstance(identity.get("bindings"),list) else []:
            if not isinstance(binding,dict):
                continue
            variable=binding.get("variable")
            if isinstance(variable,str):
                if variable in bindings:
                    add(report,"error","MAPPING_IDENTITY_BINDING",f"Entity {entity_id} 的 identity binding 重复: {variable}",path)
                bindings[variable]=binding
            source=binding.get("source",{})
            if isinstance(source,dict):
                scan_column(source.get("scanId"),source.get("column"),"MAPPING_IDENTITY_SOURCE",f"Entity {entity_id} 的 identity source 未在 Scan columns 中声明")
        if template_vars!=set(bindings):
            add(report,"error","MAPPING_IDENTITY_TEMPLATE",f"Entity {entity_id} 的 identity template 变量必须与 bindings 完全一致",path)

    for property_id, prop in properties.items():
        require(entities,prop.get("entityId"),"MAPPING_PROPERTY_ENTITY",f"Property {property_id} 引用不存在的 Entity")
        source=prop.get("source",{})
        if isinstance(source,dict):
            scan_column(source.get("scanId"),source.get("column"),"MAPPING_PROPERTY_SOURCE",f"Property {property_id} 的 source 未在 Scan columns 中声明")
    for relationship_id, relationship in relationships.items():
        require(entities,relationship.get("subjectEntityId"),"MAPPING_RELATIONSHIP_ENTITY",f"Relationship {relationship_id} 的 subject Entity 不存在")
        require(entities,relationship.get("objectEntityId"),"MAPPING_RELATIONSHIP_ENTITY",f"Relationship {relationship_id} 的 object Entity 不存在")
        for join_id in relationship.get("joinIds",[]):
            require(joins,join_id,"MAPPING_RELATIONSHIP_JOIN",f"Relationship {relationship_id} 引用不存在的 Join: {join_id}")
    for filter_id, filter_item in filters.items():
        target=filter_item.get("target",{})
        if isinstance(target,dict):
            if target.get("kind")=="SCAN":
                require(scans,target.get("scanId"),"MAPPING_FILTER_TARGET",f"Filter {filter_id} 的目标 Scan 不存在")
            elif target.get("kind")=="ENTITY":
                require(entities,target.get("entityId"),"MAPPING_FILTER_TARGET",f"Filter {filter_id} 的目标 Entity 不存在")
        for condition in filter_item.get("conditions",[]) if isinstance(filter_item.get("conditions"),list) else []:
            column=condition.get("column",{}) if isinstance(condition,dict) else {}
            if isinstance(column,dict):
                scan_column(column.get("scanId"),column.get("column"),"MAPPING_FILTER_COLUMN",f"Filter {filter_id} 引用未声明的 Scan column")
    coverage_by_entity={}
    coverage=data.get("coverage",{})
    requirements=coverage.get("requirements",[]) if isinstance(coverage,dict) else []
    for requirement in requirements if isinstance(requirements,list) else []:
        if not isinstance(requirement,dict):
            continue
        entity_id=requirement.get("entityId")
        if require(entities,entity_id,"MAPPING_COVERAGE_ENTITY","Coverage 引用不存在的 Entity"):
            coverage_by_entity[entity_id]=coverage_by_entity.get(entity_id,0)+1
        for scan_id in requirement.get("requiredScanIds",[]):
            require(scans,scan_id,"MAPPING_COVERAGE_SCAN",f"Coverage {entity_id} 引用不存在的 Scan: {scan_id}")
    for entity_id in entities:
        if coverage_by_entity.get(entity_id,0)!=1:
            add(report,"error","MAPPING_COVERAGE_CARDINALITY",f"Entity {entity_id} 必须恰好有一个 Coverage Requirement",path)
    add(report,"check","MAPPING_LOCAL_REFERENCES","已检查包内 ID、Scan/Join、列引用、身份变量与 Coverage；未执行当前数据源发现",path)


def validate_scope_mapping(scope: dict[str, Any], mapping: dict[str, Any], path: Path, report: dict[str, Any]) -> None:
    """Check Scope references fully determined by the packaged Mapping."""
    scans={item.get("id"):item for item in mapping.get("scans",[]) if isinstance(item,dict) and isinstance(item.get("id"),str)}
    joins={item.get("id"):item for item in mapping.get("joins",[]) if isinstance(item,dict) and isinstance(item.get("id"),str)}
    binding=scope.get("mapping",{})
    if not isinstance(binding,dict) or binding.get("mappingId")!=mapping.get("mappingId") or binding.get("mappingVersion")!=mapping.get("version"):
        add(report,"error","SCOPE_MAPPING_BINDING","Scope 必须精确绑定同一工作包 Mapping 的 mappingId 与 version",path)
    root=scope.get("root",{})
    root_id=root.get("scanId") if isinstance(root,dict) else None
    if root_id not in scans:
        add(report,"error","SCOPE_ROOT_SCAN","Scope root.scanId 未在 Mapping 中声明",path)
        return
    if root.get("keyColumns")!=scans[root_id].get("recordKey"):
        add(report,"error","SCOPE_ROOT_KEY","Scope root.keyColumns 必须与 Mapping recordKey 逐列相同",path)
    selection=scope.get("selection",{})
    if not isinstance(selection,dict):
        return
    required=selection.get("requiredScanIds",[])
    join_ids=selection.get("joinIds",[])
    full_scan_ids=selection.get("fullScanIds",[])
    if set(required) != set(scans):
        add(report,"error","SCOPE_REQUIRED_SCANS","Scope requiredScanIds 必须完整覆盖 Mapping 的全部 Scan",path)
    if set(join_ids) != set(joins):
        add(report,"error","SCOPE_JOINS","Scope joinIds 必须完整覆盖 Mapping 的全部 Join",path)
    endpoint_scans={side.get("scanId") for join in joins.values() for side in (join.get("left",{}),join.get("right",{})) if isinstance(side,dict)}
    reachable={root_id}
    for binding_item in selection.get("rootBindings",[]) if isinstance(selection.get("rootBindings"),list) else []:
        if not isinstance(binding_item,dict):
            continue
        scan_id=binding_item.get("scanId")
        columns=binding_item.get("columns",[])
        root_columns=binding_item.get("rootColumns",[])
        if scan_id not in scans:
            add(report,"error","SCOPE_ROOT_BINDING_SCAN","Scope rootBinding Scan 未在 Mapping 中声明",path)
            continue
        if len(columns)!=len(root_columns):
            add(report,"error","SCOPE_ROOT_BINDING_ARITY","Scope rootBinding columns 与 rootColumns 数量必须相同",path)
        for column in columns:
            if column not in scans[scan_id].get("columns",[]):
                add(report,"error","SCOPE_ROOT_BINDING_COLUMN","Scope rootBinding 列未在 Mapping Scan 中声明",path)
        for column in root_columns:
            if column not in scans[root_id].get("columns",[]):
                add(report,"error","SCOPE_ROOT_BINDING_ROOT_COLUMN","Scope rootBinding rootColumns 未在 Root Scan 中声明",path)
        reachable.add(scan_id)
    for full_scan_id in full_scan_ids:
        if full_scan_id not in scans:
            add(report,"error","SCOPE_FULL_SCAN","Scope fullScanId 未在 Mapping 中声明",path)
        elif full_scan_id in endpoint_scans:
            add(report,"error","SCOPE_FULL_SCAN_JOIN","Scope fullScanId 不得参与 Mapping Join",path)
    remaining=set(join_ids) & set(joins)
    while remaining:
        expanded={join_id for join_id in remaining if any(isinstance(side,dict) and side.get("scanId") in reachable for side in (joins[join_id].get("left",{}),joins[join_id].get("right",{})))}
        if not expanded:
            break
        for join_id in expanded:
            for side in (joins[join_id].get("left",{}),joins[join_id].get("right",{})):
                if isinstance(side,dict) and isinstance(side.get("scanId"),str):
                    reachable.add(side["scanId"])
        remaining-=expanded
    for scan_id in set(scans)-set(full_scan_ids):
        if scan_id not in reachable:
            add(report,"error","SCOPE_REACHABILITY",f"Scope 非 Full Scan 不可从 Root/Binding/Join 闭包到达: {scan_id}",path)
    add(report,"check","SCOPE_MAPPING_REFERENCES","已检查 Scope 的 Mapping 版本、Root、Scan/Join 覆盖及结构可达性；未执行 Fact Provider",path)


def validate_json_asset(path: Path, data: Any, report: dict[str, Any], ontology_digest: str | None = None) -> None:
    recursive_key_scan(data, report, path)
    if not isinstance(data, dict):
        add(report,"error","ASSET_TYPE","语义资产必须是JSON对象",path)
        return
    kind = data.get("kind")
    if "mappingId" in data and data.get("schemaVersion") == 1 and kind is None:
        validate_json_schema(data, CONTRACTS / "mapping-definition-v1.schema.json", report, path)
        validate_mapping_references(data, path, report)
        if ontology_digest is None:
            add(report,"warning","MAPPING_CONTEXT_REQUIRED","只执行映射结构合同；未提供本体上下文，跨资产语义引用未验证",path)
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
        add(report,"check","DERIVATION_ENVELOPE","已检查派生封装；类型化算子计划未由平台编译",path)
        report["localIncomplete"] = True
        add(report, "warning", "COMPILER_PREFLIGHT", "Derivation 的有限算子、类型、依赖和 DAG 仍需 ECP Compiler 预检", path)
    elif kind == "EvaluationAsset" or (kind is None and data.get("apiVersion") == "enterprise-cognitive/evaluation-definition/v1"):
        add(report,"check","EVALUATION_ENVELOPE","已识别求值封装；编译合同真实性未核验",path)
        report["localIncomplete"] = True
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
    else:
        add(report,"error","ASSET_KIND_UNSUPPORTED",f"未识别的语义资产类型: {kind!r}",path)


def _member_json(path, expected, report, ontology_digest=None):
    data=load_json(path,report)
    if data is None:return None
    recognized={"MAPPING": isinstance(data,dict) and "mappingId" in data and "kind" not in data,
                "DERIVATION":isinstance(data,dict) and data.get("kind")=="FeatureDefinition",
                "EVALUATION":isinstance(data,dict) and data.get("kind")=="EvaluationAsset",
                "ACTION_POLICY":isinstance(data,dict) and data.get("kind")=="ActionPolicy",
                "SCOPE":isinstance(data,dict) and data.get("kind")=="ScopeDefinition"}
    if not recognized.get(expected,False):add(report,"error","MEMBER_KIND",f"成员内容与清单资产类型不符: {expected}",path)
    validate_json_asset(path,data,report,ontology_digest)
    return data


def _profile_binding(data,path,report):
    if data.get("semanticProfileId")!=PROFILE_ID or data.get("semanticProfileDigest")!=PROFILE_DIGEST:
        add(report,"error","PROFILE_BINDING","语义配置标识或摘要不匹配",path)


def validate_rule_manifest(manifest_path,package_root,report):
    data=load_json(manifest_path,report)
    if not isinstance(data,dict):return
    validate_json_schema(data,CONTRACTS/"rule-set-bundle-manifest-v1.schema.json",report,manifest_path)
    _profile_binding(data,manifest_path,report)
    stages=[]; ids=set()
    for m in data.get("members",[]):
        if not isinstance(m,dict):continue
        member=safe_path(package_root,m.get("path"))
        if m.get("sourceDigest")!=sha256_file(member):add(report,"error","RULE_MEMBER_DIGEST","规则成员字节摘要不匹配",member)
        aid=m.get("assetSeriesId")
        if aid in ids:add(report,"error","RULE_MEMBER_ID","规则资产标识重复",manifest_path)
        ids.add(aid)
        typ=m.get("assetType")
        if typ=="SHACL":
            stages.append(m.get("shaclStage"))
            if m.get("mediaType")!="text/turtle":add(report,"error","MEMBER_MEDIA","形状成员媒体类型错误",member)
            validate_shacl(member,report)
        elif typ in {"DERIVATION","EVALUATION","ACTION_POLICY"}:
            if m.get("shaclStage") is not None:add(report,"error","MEMBER_STAGE","非形状成员不能指定形状阶段",member)
            if m.get("mediaType")!="application/json":add(report,"error","MEMBER_MEDIA","JSON成员媒体类型错误",member)
            _member_json(member,typ,report)
        else:add(report,"error","MEMBER_KIND","未知规则成员类型",member)
    if stages and (len(stages)!=6 or set(stages)!={"asserted","domain","feature","change","output","provenance"}):
        add(report,"error","SHACL_STAGE_SET",f"使用形状时必须六阶段各一次: {stages}",manifest_path)
    return data


def cross_asset_refs(ontology_path,mapping,shape_paths,report):
    g=Graph();g.parse(ontology_path,format="turtle")
    classes=set(g.subjects(RDF.type,OWL.Class))|set(g.subjects(RDF.type,RDFS.Class))
    dprops=set(g.subjects(RDF.type,OWL.DatatypeProperty)); oprops=set(g.subjects(RDF.type,OWL.ObjectProperty))
    if isinstance(mapping,dict):
        entities={e.get("id"):e for e in mapping.get("entities",[]) if isinstance(e,dict)}
        for entity in entities.values():
            if URIRef(entity.get("classIri","")) not in classes:add(report,"error","MAPPING_CLASS_UNDECLARED",f"映射类未声明: {entity.get('classIri')}",ontology_path)
        for group,props,code in [("properties",dprops,"MAPPING_DATAPROPERTY_UNDECLARED"),("relationships",oprops,"MAPPING_OBJECTPROPERTY_UNDECLARED")]:
            for item in mapping.get(group,[]):
                if not isinstance(item,dict):continue
                pred=URIRef(item.get("predicateIri",""))
                if pred not in props:add(report,"error",code,f"映射谓词未声明或类型不符: {pred}",ontology_path)
                if group=="properties":
                    ranges=list(g.objects(pred,RDFS.range))
                    if ranges and str(ranges[0])!=item.get("datatypeIri"):add(report,"error","MAPPING_DATATYPE_RANGE",f"映射数据类型与本体不符: {pred}",ontology_path)
    for path in shape_paths:
        sg=Graph();sg.parse(path,format="turtle")
        for s,p,o in sg:
            if str(p) in {SH+"targetClass",SH+"class"} and o not in classes:
                add(report,"error","SHACL_CLASS_UNDECLARED",f"形状引用未声明类: {o}",path)
            if str(p) in {SH+"path",SH+"targetSubjectsOf",SH+"targetObjectsOf"} and o not in dprops|oprops and o!=RDF.type:
                add(report,"error","SHACL_PROPERTY_UNDECLARED",f"形状引用未声明谓词: {o}",path)
    add(report,"check","CROSS_ASSET_REFERENCES","已检查映射及形状中的类、谓词、属性值类型引用；完整映射执行仍需平台",ontology_path)


def validate_directory(root,report,archive_bytes=None):
    files=collect_files(root)
    report["inputDigest"]=snapshot_digest(files)
    report["validatedFiles"]=sorted(files)
    add(report,"check","MANIFEST_CLOSURE",f"清单闭包与目录一致，共{len(files)}个文件",root)
    mp=root/"manifest.json"; m=load_json(mp,report)
    if not isinstance(m,dict):
        return
    if m["kind"]=="ECP_RULE_SET_BUNDLE":
        try:
            enforce_rule_bundle_limits(files,m.get("members"),archive_bytes)
        except PackageError as exc:
            add(report,"error",exc.code,str(exc),mp)
        validate_rule_manifest(mp,root,report)
        add(report,"warning","ONTOLOGY_CONTEXT_MISSING","规则集未提供本体上下文；未执行跨资产语义引用校验",mp)
        return
    version=m.get("schemaVersion")
    if version not in {1,2}:
        add(report,"error","WORKSPACE_VERSION","工作区版本必须是1或2",mp);return
    validate_json_schema(m,CONTRACTS/f"semantic-workspace-package-manifest-v{version}.schema.json",report,mp)
    _profile_binding(m,mp,report)
    if m.get("scopes") and version!=2:add(report,"error","SCOPE_REQUIRES_V2","范围资产要求V2工作区",mp)
    op=safe_path(root,m["ontology"]["path"]);od=sha256_file(op)
    if m["ontology"].get("sourceDigest")!=od:add(report,"error","WORKSPACE_ONTOLOGY_DIGEST","本体摘要不一致",op)
    validate_ontology(op,report)
    map_path=safe_path(root,m["mapping"]["path"])
    if m["mapping"].get("sourceDigest")!=sha256_file(map_path):add(report,"error","WORKSPACE_MAPPING_DIGEST","映射摘要不一致",map_path)
    if m["mapping"].get("ontologySourceDigest")!=od:add(report,"error","WORKSPACE_MAPPING_ONTOLOGY_DIGEST","映射引用本体摘要不一致",map_path)
    mapping=_member_json(map_path,"MAPPING",report,od)
    rp=safe_path(root,m["ruleSet"]["manifestPath"])
    if m["ruleSet"].get("sourceDigest")!=sha256_file(rp):add(report,"error","WORKSPACE_RULESET_DIGEST","规则集摘要不一致",rp)
    rules=validate_rule_manifest(rp,root,report)
    shape_paths=[safe_path(root,x["path"]) for x in rules.get("members",[]) if x.get("assetType")=="SHACL"] if rules else []
    if not report["errors"]:cross_asset_refs(op,mapping,shape_paths,report)
    for group in ["schemas","scopes"]:
        for item in m.get(group,[]):
            p=safe_path(root,item["path"])
            if item.get("sourceDigest")!=sha256_file(p):add(report,"error","SOURCE_DIGEST",f"{group}成员摘要不一致",p)
            if group=="scopes":
                scope=_member_json(p,"SCOPE",report)
                if isinstance(scope,dict) and isinstance(mapping,dict):
                    validate_scope_mapping(scope,mapping,p,report)
            else:
                data=load_json(p,report)
                if not isinstance(data,dict):add(report,"error","SCHEMA_SNAPSHOT_TYPE","来源模式快照须为对象",p)
                else:
                    recursive_key_scan(data,report,p)
                    add(report,"check","SCHEMA_SNAPSHOT_BYTES","已核对快照字节；不证明实时数据库仍然一致",p)
    add(report,"warning","ECP_PREFLIGHT_REQUIRED","本地检查不替代当前源发现、实例约束执行、候选编译和业务批准",mp)


def validate_path(path: Path) -> dict[str, Any]:
    path=Path(path).absolute()
    report={"tool":TOOL_MANIFEST["name"]+"/local-validator","toolVersion":TOOL_MANIFEST["version"],"ecpProfileId":PROFILE_ID,"ecpProfileDigest":PROFILE_DIGEST,"target":str(path),"errors":[],"warnings":[],"checks":[],"localIncomplete":False}
    execution_error=False
    try:
        if path.is_symlink():raise PackageError("SYMLINK","目标不能是符号链接")
        if not path.exists():add(report,"error","PATH_MISSING","目标路径不存在",path)
        elif path.is_dir():validate_directory(path,report)
        elif path.suffix.lower()==".zip":
            with tempfile.TemporaryDirectory() as td:
                unpack_zip(path,Path(td));validate_directory(Path(td),report,path.stat().st_size)
        elif path.suffix.lower()==".ttl":
            graph=Graph();graph.parse(path,format="turtle")
            has_shacl=any(str(p).startswith(SH) or (p==RDF.type and str(o).startswith(SH)) for _,p,o in graph)
            if has_shacl and any(graph.subjects(RDF.type,OWL.Ontology)):
                add(report,"error","MIXED_TTL_ASSET","不得将本体和形状混入同一资产",path)
            elif has_shacl:validate_shacl(path,report)
            else:validate_ontology(path,report)
        elif path.suffix.lower()==".json":
            data=load_json(path,report)
            if data is not None:validate_json_asset(path,data,report)
        else:add(report,"error","UNSUPPORTED_TARGET","只支持清单目录、ZIP、TTL、JSON",path)
    except PackageError as exc:add(report,"error",exc.code,str(exc),path)
    except (ValueError,KeyError,TypeError,OSError) as exc:add(report,"error","INPUT_ERROR",str(exc),path)
    except Exception as exc:
        execution_error=True;add(report,"error","VALIDATOR_ERROR",f"验证未完成: {type(exc).__name__}: {exc}",path)
    if not report["checks"] and not report["errors"]:add(report,"error","NO_CHECKS_EXECUTED","没有可验证资产或检查未执行",path)
    status="ERROR" if execution_error else "INVALID" if report["errors"] else "INCOMPLETE" if report["localIncomplete"] else "LOCALLY_VALID"
    report["summary"]={"errorCount":len(report["errors"]),"warningCount":len(report["warnings"]),"checkCount":len(report["checks"]),"status":status,"releaseReady":False,"ecpPreflightRequired":True}
    report["evidence"]={"boundedStaticChecks":"ERROR" if execution_error else "FAIL" if report["errors"] else "INCOMPLETE" if report["localIncomplete"] else "PASS", "crossAssetReferences":"PASS" if any(c["code"]=="CROSS_ASSET_REFERENCES" for c in report["checks"]) and not report["errors"] else "NOT_EXECUTED", "shaclInstanceValidation":"NOT_EXECUTED","owlConsistency":"NOT_EXECUTED","domainExpertReview":"NOT_EXECUTED","modelGenerationEvaluation":"NOT_EXECUTED","ecpImport":"NOT_EXECUTED","ecpCompilation":"NOT_EXECUTED","ecpDataRun":"NOT_EXECUTED"}
    report["coverageNote"]="仅执行checks中列示的有限本地检查；完整数据类型词法、模式执行、算子类型/计划、连接拓扑、当前源发现及运行期完整性仍需对应工具或ECP证据。"
    report.pop("localIncomplete",None)
    return report


def main() -> int:
    ap=argparse.ArgumentParser(description="ECP有限静态检查；不代表完整推理、实例约束或平台编译。")
    ap.add_argument("path");ap.add_argument("--json-out")
    args=ap.parse_args();target=Path(args.path).absolute()
    if args.json_out and target.is_dir() and Path(args.json_out).resolve().is_relative_to(target.resolve()):
        ap.error("验证报告必须写到导入工作区之外，避免新增未登记成员")
    report=validate_path(target);text=json.dumps(report,ensure_ascii=False,indent=2)
    if args.json_out:
        out=Path(args.json_out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text+"\n",encoding="utf-8")
    print(text)
    return 1 if report["errors"] else 2 if report["summary"]["status"]=="INCOMPLETE" else 0

if __name__=="__main__":raise SystemExit(main())
