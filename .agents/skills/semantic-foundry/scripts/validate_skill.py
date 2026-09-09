#!/usr/bin/env python3
"""技能入口、当前版本、规范来源摘要与必要制品检查；不是模型行为评测。"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
import yaml
from workspace_files import safe_path,read_json,PackageError
REQUIRED=[
'SKILL.md','README.md','manifest.json','agents/interface.yaml','THIRD_PARTY_NOTICES.md',
'references/handbook-index.md','references/ontology-engineering-method.md','references/ecp-adaptation.md','references/modeling-patterns.md','references/output-contract.md','references/interaction-policy.md',
'assets/design-contract.schema.json','assets/design-contract.template.json',
'scripts/validate_ecp_assets.py','scripts/workspace_files.py','scripts/package_workspace.py','scripts/refresh_workspace_digests.py','scripts/validate_design.py','scripts/scaffold_design.py','scripts/run_verification.py','scripts/validate_shacl_instance.py',
'evals/trigger_cases.json','evals/model-generation/tasks.json','evals/model-generation/result-template.json',
'examples/ownership-slice/run.py','examples/ownership-slice/design/contract.json',
'reports/creation-handoff.md']

def validate(root:Path)->dict:
    root=root.absolute();failures=[];warnings=[];verified=[]
    for rel in REQUIRED:
        if not (root/rel).is_file():failures.append('缺少制品: '+rel)
    try:
        text=(root/'SKILL.md').read_text(encoding='utf8');parts=text.split('---',2)
        if len(parts)!=3:raise ValueError('入口缺少完整元数据')
        fm=yaml.safe_load(parts[1]);manifest=read_json(root/'manifest.json')
        if fm.get('name')!='hovo-ecp-semantic' or root.name!=fm.get('name'):failures.append('技能名称或目录不一致')
        if manifest.get('name')!=fm.get('name') or manifest.get('version')!=fm.get('metadata',{}).get('version'):failures.append('版本/名称不一致')
        if not isinstance(fm.get('description'),str) or not 1<=len(fm['description'])<=1024:failures.append('描述长度或类型不合格')
        if any(not isinstance(v,str) for v in fm.get('metadata',{}).values()):failures.append('技能metadata必须为字符串值')
        if len(text.splitlines())>500:failures.append('入口超过500行，应移至按需材料')
        for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)',text):
            if not link.startswith(('https://','http://')):
                try:safe_path(root,link)
                except PackageError as e:failures.append(str(e))
        for token in ['能力问题','不得伪造','最多 1 轮','最多 5 个','BLOCKED','INFERRED','ASSUMED','NOT_EXECUTED']:
            # NOT_EXECUTED的标准英文状态可由输出合同承载，不要求重复入口。
            body=text if token!='NOT_EXECUTED' else (root/'references/output-contract.md').read_text()
            if token not in body:failures.append('缺少执行边界: '+token)
        for book in read_json(root/'references/handbooks-v2/source-manifest.json')['files']:
            p=safe_path(root,book['path']);data=p.read_bytes();actual=hashlib.sha256(data).hexdigest()
            if actual!=book['sha256'] or len(data)!=book['byteLength']:failures.append('手册原文摘要不一致: '+book['path'])
            else:verified.append(book['path'])
        kit=root/'references/ecp-kit-1.7';km=read_json(kit/'manifest.json')
        for item in km['files']:
            p=safe_path(kit,item['path']);data=p.read_bytes()
            if 'sha256:'+hashlib.sha256(data).hexdigest()!=item['contentDigest'] or len(data)!=item['byteLength']:failures.append('工具箱摘要不一致: '+item['path'])
            else:verified.append('references/ecp-kit-1.7/'+item['path'])
        old=['scripts/scaffold_workspace.py','scripts/output_eval.py']
        for rel in old:
            if (root/rel).exists():failures.append('废弃执行路径仍存在: '+rel)
        if len(list(root.rglob('SKILL.md')))!=1:failures.append('存在嵌套或重复技能入口')
    except Exception as e:failures.append(f'包检查未完成: {e}')
    return {'ok':not failures,'status':'FAIL' if failures else 'PASS','failures':failures,'warnings':warnings,'verifiedAuthorityFiles':verified,'modelBehavior':'NOT_EXECUTED','note':'这是制品与规范快照检查；公开许可和业务批准需独立确认'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('skill_dir',nargs='?',default='.');a=p.parse_args();r=validate(Path(a.skill_dir));print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['ok'] else 1
if __name__=='__main__':raise SystemExit(main())
