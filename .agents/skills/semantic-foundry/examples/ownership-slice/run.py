#!/usr/bin/env python3
"""复用手册实现完成合成所有权切片；平台形式适配与本地数据检查分开报告。"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
from rdflib import Graph, RDF, URIRef
E=Path(__file__).resolve().parent;ROOT=E.parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(E.parent/'handbook-reference'))
from src.semantic_case import H,X,build_view,map_raw,facts_graph
from validate_ecp_assets import validate_path,cross_asset_refs
from workspace_files import digest_bytes

def load(rel):return json.loads((E/rel).read_text(encoding='utf8'))
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    out=a.output.resolve()
    if out.is_relative_to(E.resolve()):raise SystemExit('证据输出必须在样例源目录之外，避免修改已固定输入')
    out.mkdir(parents=True,exist_ok=True)
    raw,selection,conf=load('source/source-records.json'),load('source/selection.json'),load('source/execution.json')
    expected=load('expected/results.json');view=build_view(raw,selection,conf['business_date'],conf['knowledge_cutoff']);facts=facts_graph(view,raw)
    original=map_raw(raw);claims=Graph()
    for s,pred,obj in original:
        if pred in {RDF.subject,RDF.predicate} or (pred==RDF.type and obj==RDF.Statement):continue
        claims.add((s,H.claimRatio if pred==RDF.object else pred,obj))
    query=(E/'queries/direct-holders.rq').read_text()
    direct=sorted(str(row.holder).rsplit(':',1)[-1] for row in facts.query(query,initBindings={'target':X[conf['target']]}))
    raw_count=len(list(claims.triples((None,H.shareRatio,None))))
    issues=[];checks=[]
    def check(name,condition,detail):
        checks.append({'name':name,'status':'PASS' if condition else 'FAIL','detail':detail})
        if not condition:issues.append(name)
    check('direct-holders',direct==expected['direct_holders'],{'actual':direct,'expected':expected['direct_holders']})
    check('position-count',len(view['facts'])==expected['positions'],{'actual':len(view['facts'])})
    check('assertion-not-fact',raw_count==0,{'rawShareRatioTriples':raw_count,'claims':len(list(claims.subjects(RDF.type,H.Assertion)))})
    duplicate=copy.deepcopy(raw);extra=copy.deepcopy(raw['records'][0]);extra['id']='a1_duplicate';duplicate['records'].append(extra)
    selected=copy.deepcopy(selection);selected['accepted_assertions'].append({'assertion_id':'a1_duplicate','accepted_at':'2026-01-10T00:00:00Z','basis':'合成重复证据回归'})
    dv=build_view(duplicate,selected,conf['business_date'],conf['knowledge_cutoff'])
    same=lambda vv:sorted((r['position'],r['ratio']) for r in vv['facts'])
    check('duplicate-evidence-not-position',same(dv)==same(view),{'positionCount':len(dv['facts'])})
    conflict=copy.deepcopy(duplicate);conflict['records'][-1]['value']='55'
    cv=build_view(conflict,selected,conf['business_date'],conf['knowledge_cutoff'])
    check('conflict-not-averaged',any(i['code']=='VALUE_CONFLICT' for i in cv['issues']) and not any(f['position']=='E1' for f in cv['facts']),{'issues':cv['issues']})
    collision='ASK { ?s a <urn:hovo:semantic:NaturalPerson>, <urn:hovo:semantic:Organization> }'
    check('simultaneous-type-positive',not bool(facts.query(collision)), '本地显式类型反例查询；不是标准形状验证')
    bad=Graph()
    for triple in facts:bad.add(triple)
    bad.add((X.P1,RDF.type,H.Organization))
    check('simultaneous-type-negative',bool(bad.query(collision)), '故意同时类型能够被指定查询检出；不冒充OWL一致性测试')
    static={}
    for f in ['ontology.ttl','view-shapes.ttl']:
        r=validate_path(E/'assets'/f);static[f]=r;check('static-'+f,not r['errors'],r['summary'])
    ref={'errors':[],'warnings':[],'checks':[]};cross_asset_refs(E/'assets/ontology.ttl',None,[E/'assets/view-shapes.ttl'],ref)
    check('shape-references',not ref['errors'],ref)
    for name,g in [('raw-claims',claims),('fact-view',facts),('simultaneous-type-negative',bad)]:g.serialize(destination=out/f'{name}.ttl',format='turtle')
    targets=sorted(str(s) for s in facts.subjects(RDF.type,H.OwnershipPosition))
    coverage={'shapeTargets':{'urn:hovo:semantic:PositionShape':targets,'urn:hovo:semantic:PersonShape':sorted(str(s) for s in facts.subjects(RDF.type,H.NaturalPerson))}}
    (out/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    report={'status':'FAIL' if issues else 'PASS','evaluationType':'author-produced-synthetic-slice-and-local-adaptation','checks':checks,'staticChecks':static,'directHolders':direct,'ecpCompilation':'NOT_EXECUTED','standardShaclValidation':'NOT_EXECUTED','owlConsistency':'NOT_EXECUTED','independentModelGenerationComparison':'NOT_EXECUTED','independentBusinessReview':'NOT_EXECUTED','inputs':{str(p.relative_to(E)):digest_bytes(p.read_bytes()) for d in ['source','assets','expected','queries','design'] for p in sorted((E/d).rglob('*')) if p.is_file()},'scope':'直接持有人与采信桥接；没有完整平台工作区、真实源或监管识别承诺'}
    (out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'status':report['status'],'checks':len(checks),'failures':issues,'output':str(out)},ensure_ascii=False));return 0 if not issues else 1
if __name__=='__main__':raise SystemExit(main())
