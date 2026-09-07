#!/usr/bin/env python3
"""可选标准形状实例验证；明确目标覆盖，缺少依赖时返回未执行。
这是独立作者验证，不等于ECP的ECMAScript正则方言或平台编译认证。
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from rdflib import Graph, RDF, RDFS, URIRef
from workspace_files import read_json, digest_bytes
SH='http://www.w3.org/ns/shacl#'

def target_nodes(data:Graph,shapes:Graph,shape:URIRef)->set:
    result=set(shapes.objects(shape,URIRef(SH+'targetNode')))
    for cls in shapes.objects(shape,URIRef(SH+'targetClass')):
        result.update(row.s for row in data.query('SELECT DISTINCT ?s WHERE { ?s a ?c . ?c <http://www.w3.org/2000/01/rdf-schema#subClassOf>* ?target . }',initBindings={'target':cls}))
    for pred in shapes.objects(shape,URIRef(SH+'targetSubjectsOf')):result.update(data.subjects(pred,None))
    for pred in shapes.objects(shape,URIRef(SH+'targetObjectsOf')):result.update(data.objects(None,pred))
    return result

def evaluate(data_path:Path,shape_path:Path,contract_path:Path)->dict:
    try:from pyshacl import validate
    except ImportError:return {'status':'NOT_EXECUTED','reason':'缺少pyshacl依赖；未运行标准形状验证，无替代实现','noFallback':True}
    try:
        data=Graph().parse(data_path,format='turtle');shapes=Graph().parse(shape_path,format='turtle');contract=read_json(contract_path)
        expected=contract['shapeTargets'];actual={}
        roots=set()
        for pred in ['targetNode','targetClass','targetSubjectsOf','targetObjectsOf']:roots.update(shapes.subjects(URIRef(SH+pred),None))
        coverage_ok={str(x) for x in roots}==set(expected)
        for shape in roots:
            actual[str(shape)]=sorted(str(n) for n in target_nodes(data,shapes,shape))
            coverage_ok=coverage_ok and actual[str(shape)]==sorted(expected.get(str(shape),[]))
        expected_conforms=contract.get('expectConforms',True)
        if not isinstance(expected_conforms,bool):raise ValueError('expectConforms必须是布尔值')
        if not expected_conforms and not contract.get('expectedViolations'):raise ValueError('负例必须指定期望违规，不能用任意失败作为成功')
        conforms,report,text=validate(data,shacl_graph=shapes,inference='none',meta_shacl=True,advanced=False,js=False,do_owl_imports=False,inplace=False)
        violations=[]
        for node in report.subjects(RDF.type,URIRef(SH+'ValidationResult')):
            violations.append({'focusNode':str(report.value(node,URIRef(SH+'focusNode'))),'path':str(report.value(node,URIRef(SH+'resultPath'))),'component':str(report.value(node,URIRef(SH+'sourceConstraintComponent')))})
        exact=all(any(all(v.get(k)==val for k,val in exp.items()) for v in violations) for exp in contract.get('expectedViolations',[]))
        ok=coverage_ok and bool(conforms)==expected_conforms and exact
        return {'status':'PASS' if ok else 'FAIL','dataConforms':bool(conforms),'expectedConforms':expected_conforms,'coverageMatches':coverage_ok,'actualTargets':actual,'expectedTargets':expected,'violations':violations,'configuration':{'inference':'none','meta_shacl':True,'advanced':False,'js':False,'imports':False},'inputs':{str(p):digest_bytes(p.read_bytes()) for p in [data_path,shape_path,contract_path]},'ecpCompilation':'NOT_EXECUTED','note':'标准约束检查仅针对指定图、目标和预期；不是全局OWL推理或平台认证'}
    except Exception as e:return {'status':'ERROR','reason':f'{type(e).__name__}: {e}'}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--data',type=Path,required=True);p.add_argument('--shapes',type=Path,required=True);p.add_argument('--contract',type=Path,required=True);p.add_argument('--json-out',type=Path,required=True);a=p.parse_args()
    r=evaluate(a.data,a.shapes,a.contract);a.json_out.parent.mkdir(parents=True,exist_ok=True);a.json_out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['status']=='PASS' else 2 if r['status']=='NOT_EXECUTED' else 1
if __name__=='__main__':raise SystemExit(main())
