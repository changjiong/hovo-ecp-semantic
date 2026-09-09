#!/usr/bin/env python3
"""检查最小建模契约的完整性与引用；不自动判断专家语义正确性。"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import jsonschema
from rdflib import Graph, URIRef, RDF, OWL, RDFS
from workspace_files import PackageError, safe_path, read_json, digest_bytes
ROOT=Path(__file__).resolve().parents[1]

def validate_design(root:Path)->dict:
    errors=[];checks=[]
    def error(code,message):errors.append({'code':code,'message':message})
    def resolve(rel):
        try:return safe_path(root,rel)
        except PackageError as e:error(e.code,str(e));return None
    path=resolve('design/contract.json')
    if not path:return {'status':'FAIL','errors':errors,'checks':checks}
    try:
        d=read_json(path);schema=read_json(ROOT/'assets/design-contract.schema.json')
        for err in jsonschema.Draft202012Validator(schema).iter_errors(d):error('DESIGN_SCHEMA',f'{list(err.path)}: {err.message}')
        if isinstance(d,dict) and d.get('status')=='DRAFT':return {'status':'INCOMPLETE','errors':errors,'checks':['草案尚需补齐，不是已通过设计'],'expertReview':'NOT_EXECUTED'}
        if errors:return {'status':'FAIL','errors':errors,'checks':checks}
        text=json.dumps(d,ensure_ascii=False)
        if d['status']=='DRAFT' or '待填写' in text or 'REPLACE_ME' in text:
            return {'status':'INCOMPLETE','errors':[],'checks':['结构模板存在；尚不能作为完成设计'],'expertReview':'NOT_EXECUTED'}
        op=resolve(d['ontology']);g=Graph()
        if op:g.parse(op,format='turtle')
        declared=set(g.subjects(RDF.type,OWL.Class))|set(g.subjects(RDF.type,RDFS.Class))|set(g.subjects(RDF.type,OWL.ObjectProperty))|set(g.subjects(RDF.type,OWL.DatatypeProperty))|set(g.subjects(RDF.type,OWL.AnnotationProperty))
        seen=set()
        for c in d['concepts']:
            if c['iri'] in seen:error('CONCEPT_DUPLICATE',c['iri'])
            seen.add(c['iri'])
            if URIRef(c['iri']) not in declared:error('CONCEPT_NOT_DECLARED',c['iri'])
        ids=set()
        for q in d['questions']:
            if q['id'] in ids:error('CQ_DUPLICATE',q['id'])
            ids.add(q['id'])
            for rel in q['inputs']+[q['expected_file'],q['test_file']]:resolve(rel)
        for s in d['sources']:resolve(s['path'])
        for a in d['adaptations']:resolve(a['test_file'])
        review=d['review']
        if 'EVIDENCE_ATTACHED' in [review['independent_expert'],review['model_generation_comparison']]:
            if not review.get('evidence_files'):error('REVIEW_EVIDENCE_MISSING','声明外部证据但未引用文件')
            for rel in review.get('evidence_files',[]):resolve(rel)
        checks=['设计结构合同已执行','概念声明与来源/预期/测试路径已检查；未执行契约中任何命令']
        return {'status':'FAIL' if errors else 'PASS','errors':errors,'checks':checks,'designDigest':digest_bytes(path.read_bytes()),'expertReview':'NOT_EXECUTED','modelGenerationEvaluation':'NOT_EXECUTED','note':'字段和引用合格不证明文字含义正确；外部证据文件存在也不自动证明其真实性'}
    except Exception as e:return {'status':'ERROR','errors':[{'code':'DESIGN_ERROR','message':str(e)}],'checks':checks}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');p.add_argument('--json-out');a=p.parse_args();r=validate_design(Path(a.project).absolute())
    text=json.dumps(r,ensure_ascii=False,indent=2)
    if a.json_out:
        out=Path(a.json_out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text+'\n',encoding='utf8')
    print(text);return 0 if r['status']=='PASS' else 2 if r['status']=='INCOMPLETE' else 1
if __name__=='__main__':raise SystemExit(main())
