#!/usr/bin/env python3
"""运行合成参考切片和全部本地合同测试；不调用平台或生成真实认定。"""
from __future__ import annotations
import argparse
from collections import Counter
import contextlib
from datetime import datetime, timezone
import importlib.metadata
import io
import json
from pathlib import Path
import platform
import sys
import unittest
import warnings
from rdflib import Graph
from src.semantic_case import (X, build_view, compute_ownership, facts_graph,
                               map_raw, graph_contract, bytes_digest)
ROOT=Path(__file__).resolve().parent

def load(path: str):
    return json.loads((ROOT/path).read_text(encoding='utf8'))

def write_json(path: Path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

class EvidenceResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.records=[]
    def addSuccess(self,test):
        super().addSuccess(test);self.records.append({'test':test.id(),'status':'PASS'})
    def addFailure(self,test,err):
        super().addFailure(test,err);self.records.append({'test':test.id(),'status':'FAIL'})
    def addError(self,test,err):
        super().addError(test,err);self.records.append({'test':test.id(),'status':'ERROR'})
    def addSkip(self,test,reason):
        super().addSkip(test,reason);self.records.append({'test':test.id(),'status':'NOT_EXECUTED','reason':reason})

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'reports',help='本地证据输出目录')
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    conf=load('spec/execution.json');raw=load('fixtures/source-records.json')
    selection=load('fixtures/selection.json');coverage=load('fixtures/coverage.json')
    rules=load('spec/rules.json');expected=load('spec/expected.json')['base']
    parsed=[]
    for path in sorted((ROOT/'model').glob('*.ttl')):
        graph=Graph().parse(path,format='turtle')
        parsed.append({'path':str(path.relative_to(ROOT)),'triples':len(graph),'status':'PASS_SYNTAX_ONLY'})
    for path in sorted((ROOT/'spec').glob('*.json')):
        json.loads(path.read_text(encoding='utf8'))
    view=build_view(raw,selection,conf['business_date'],conf['knowledge_cutoff'])
    raw_graph=map_raw(raw);graph=facts_graph(view,raw)
    raw_graph.serialize(destination=out/'raw-assertions.ttl',format='turtle')
    graph.serialize(destination=out/'fact-view.ttl',format='turtle')
    calc=compute_ownership(view,raw,coverage,conf['target'],rules['threshold'])
    contract=graph_contract(graph,[X['position:E'+str(i)] for i in range(1,6)])
    write_json(out/'fact-view.json',view);write_json(out/'ownership-result.json',calc)
    write_json(out/'app-contract-report.json',contract)
    logs=io.StringIO()
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter('always')
        direct=[str(row.holder).split(':')[-1] for row in graph.query(
            (ROOT/'queries/direct-holders.rq').read_text(),initBindings={'target':X[conf['target']]})]
        suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
        result=unittest.TextTestRunner(stream=logs,verbosity=2,resultclass=EvidenceResult).run(suite)
    (out/'test-results.log').write_text(logs.getvalue(),encoding='utf8')
    exact_match=(calc['totals']==expected['ownership_totals']
                 and direct==expected['direct_holders']
                 and calc['threshold_matches']==expected['threshold_matches']
                 and contract['pass'])
    versions={}
    for name in ['rdflib','jsonschema','pyparsing','attrs','referencing','rpds-py','jsonschema-specifications']:
        versions[name]=importlib.metadata.version(name)
    evidence={'reference_version':'2.0.0', 'generated_at_utc':datetime.now(timezone.utc).isoformat(),
        'python':platform.python_version(),'dependencies':versions,
        'declared_scope':'合成普通股所有权语义与计算切片；非完整受益所有人识别',
        'tests':{'run':result.testsRun,'passed':len(result.records)-len(result.failures)-len(result.errors)-len(result.skipped),
                 'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'cases':result.records},
        'rdf_parse':parsed,'base_expected_matches':exact_match,
        'direct_holders':direct,
        'checks':{'application_contract':'PASS' if contract['pass'] else 'FAIL',
                  'standard_shacl_validation':'NOT_EXECUTED',
                  'full_owl_consistency_and_satisfiability':'NOT_EXECUTED',
                  'ecp_import_compile':'NOT_EXECUTED',
                  'independent_business_review':'NOT_EXECUTED',
                  'production_authorization':'NOT_EXECUTED'},
        'dependency_warnings':dict(Counter(type(w.message).__name__ for w in observed)),
        'evidence_limit':'依赖库出现弃用警告已记录；没有将缺失的标准验证器替换成自写验证器。标准SHACL检查需另运行validate_shacl.py；其独立报告不由本文件代填。',
        'status':'LOCALLY_TESTED_REFERENCE_CANDIDATE' if result.wasSuccessful() and exact_match else 'FAILED'}
    write_json(out/'verification.json',evidence)
    print(json.dumps({'status':evidence['status'],'tests_run':result.testsRun,'failures':len(result.failures),
                      'errors':len(result.errors),'expected_matches':exact_match,
                      'unexecuted':['standard_shacl_validation','full_owl_consistency_and_satisfiability','ecp_import_compile','independent_business_review'],
                      'output':str(out)},ensure_ascii=False,indent=2))
    return 0 if result.wasSuccessful() and exact_match else 1

if __name__=='__main__':
    raise SystemExit(main())
