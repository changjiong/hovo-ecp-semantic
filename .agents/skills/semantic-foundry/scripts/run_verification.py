#!/usr/bin/env python3
"""分层运行本地验证；关键词、参考工程、样例及外部缺口分别报告。"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime,timezone
import hashlib
import importlib.metadata
import io
import json
from pathlib import Path
import platform
import subprocess
import sys
import unittest
import warnings
ROOT=Path(__file__).resolve().parents[1]

def skill_identity()->dict[str,str]:
    manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    name=manifest.get('name');version=manifest.get('version')
    if not isinstance(name,str) or not name or not isinstance(version,str) or not version:
        raise ValueError('manifest.json 必须提供非空 name 和 version 作为验证报告身份')
    return {'name':name,'version':version}

class Result(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.records=[]
    def addSuccess(self,t):super().addSuccess(t);self.records.append({'test':t.id(),'status':'PASS'})
    def addFailure(self,t,e):super().addFailure(t,e);self.records.append({'test':t.id(),'status':'FAIL'})
    def addError(self,t,e):super().addError(t,e);self.records.append({'test':t.id(),'status':'ERROR'})
    def addSkip(self,t,r):super().addSkip(t,r);self.records.append({'test':t.id(),'status':'NOT_EXECUTED','reason':r})
def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output.absolute();out.mkdir(parents=True,exist_ok=True)
    identity=skill_identity()
    def dump(name,data):(out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    log=io.StringIO()
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter('always')
        suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
        result=unittest.TextTestRunner(stream=log,verbosity=2,resultclass=Result).run(suite)
    (out/'unit-tests.log').write_text(log.getvalue(),encoding='utf8')
    units={'run':result.testsRun,'passed':sum(r['status']=='PASS' for r in result.records),'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'cases':result.records,'warningTypes':dict(Counter(type(w.message).__name__ for w in observed)),'scope':'本地工具、文档合同及作者样例；不代表宿主模型遵从'}
    dump('unit-tests.json',units)
    commands=[]
    def run(name,args,allowed=(0,)):
        argv=[sys.executable,*map(str,args)]
        try:
            proc=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=120)
            (out/(name+'.log')).write_text(proc.stdout+'\n'+proc.stderr,encoding='utf8')
            rec={'name':name,'command':argv,'exitCode':proc.returncode,'status':'PASS' if proc.returncode==0 else 'NOT_EXECUTED' if proc.returncode==2 and 2 in allowed else 'FAIL'}
            commands.append(rec)
            return proc.returncode in allowed
        except subprocess.TimeoutExpired:
            commands.append({'name':name,'command':argv,'exitCode':None,'status':'ERROR','reason':'验证超时'});return False
    ok=result.wasSuccessful() and not result.skipped
    ok=run('package-check',[ROOT/'scripts/validate_skill.py',ROOT]) and ok
    ok=run('keyword-routing',[ROOT/'scripts/trigger_eval.py',ROOT,'--output',out/'keyword-routing.json']) and ok
    ok=run('design-contract',[ROOT/'scripts/validate_design.py',ROOT/'examples/ownership-slice','--json-out',out/'design-contract.json']) and ok
    ok=run('ownership-slice',[ROOT/'examples/ownership-slice/run.py','--output',out/'ownership-slice']) and ok
    ok=run('handbook-reference',[ROOT/'examples/handbook-reference/run.py','--output',out/'handbook-reference']) and ok
    ok=run('standard-shacl',[ROOT/'scripts/validate_shacl_instance.py','--data',out/'ownership-slice/fact-view.ttl','--shapes',ROOT/'examples/ownership-slice/assets/view-shapes.ttl','--contract',out/'ownership-slice/coverage.json','--json-out',out/'standard-shacl.json'],allowed=(0,2)) and ok
    versions={}
    for dep in ['rdflib','jsonschema','PyYAML','pyparsing','attrs','referencing','rpds-py','jsonschema-specifications']:
        try:versions[dep]=importlib.metadata.version(dep)
        except importlib.metadata.PackageNotFoundError:versions[dep]='NOT_INSTALLED'
    files=[ROOT/'SKILL.md',ROOT/'manifest.json',*sorted((ROOT/'scripts').glob('*.py')),*sorted((ROOT/'tests').glob('*.py'))]
    fingerprints={str(f.relative_to(ROOT)):'sha256:'+hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    def optional(name):
        file=out/name
        return json.loads(file.read_text()) if file.is_file() else {'status':'NOT_EXECUTED'}
    report={'skill':identity['name'],'version':identity['version'],'executedAt':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'dependencies':versions,'unitTests':units,'commands':commands,'keywordRouting':optional('keyword-routing.json').get('summary'), 'handbookReference':optional('handbook-reference/verification.json').get('tests'),'ownershipSlice':optional('ownership-slice/verification.json').get('checks'),'standardShacl':optional('standard-shacl.json'),'inputFingerprints':fingerprints,'externalEvidence':{'modelGenerationComparison':'NOT_EXECUTED','fullOwlConsistency':'NOT_EXECUTED','ecpCompilation':'NOT_EXECUTED','independentExpertReview':'NOT_EXECUTED','productionAuthorization':'NOT_EXECUTED'},'status':'LOCAL_VERIFICATION_PASSED_WITH_EXTERNAL_GAPS' if ok else 'FAILED'}
    dump('verification.json',report)
    print(json.dumps({'status':report['status'],'unitTests':{k:v for k,v in units.items() if k!='cases'},'commands':commands,'output':str(out)},ensure_ascii=False,indent=2))
    return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
