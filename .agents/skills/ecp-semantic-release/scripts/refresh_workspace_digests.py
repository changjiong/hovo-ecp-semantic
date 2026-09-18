#!/usr/bin/env python3
"""显式刷新源摘要。必须在确认修改后单独调用；刷新会使旧快照验证证据不再适用。"""
from __future__ import annotations
import argparse
import json
import os
import tempfile
from pathlib import Path
from workspace_files import PackageError, collect_files, digest_bytes, json_text, safe_path, snapshot_digest
from validate_ecp_assets import PROFILE_ID, PROFILE_DIGEST

def refresh(root:Path)->dict:
    root=root.absolute(); before=collect_files(root); after=dict(before)
    manifest=json_text(before['manifest.json'].decode())
    if manifest.get('kind')!='ECP_SEMANTIC_WORKSPACE_PACKAGE':raise PackageError('MANIFEST_KIND','摘要刷新入口仅接受工作区')
    def profile(obj):
        if obj.get('semanticProfileId')!=PROFILE_ID or obj.get('semanticProfileDigest')!=PROFILE_DIGEST:
            raise PackageError('PROFILE_BINDING','语义配置不匹配；摘要刷新不会替换语义配置')
    profile(manifest)
    def encode(obj):return (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    ontology_digest=digest_bytes(before[manifest['ontology']['path']]);manifest['ontology']['sourceDigest']=ontology_digest
    map_name=manifest['mapping']['path'];mapping=json_text(before[map_name].decode());mapping['ontologySourceDigest']=ontology_digest
    after[map_name]=encode(mapping);manifest['mapping']['sourceDigest']=digest_bytes(after[map_name]);manifest['mapping']['ontologySourceDigest']=ontology_digest
    rule_name=manifest['ruleSet']['manifestPath'];rules=json_text(before[rule_name].decode());profile(rules)
    for member in rules['members']:member['sourceDigest']=digest_bytes(before[member['path']])
    after[rule_name]=encode(rules);manifest['ruleSet']['sourceDigest']=digest_bytes(after[rule_name])
    for group in ['schemas','scopes']:
        for item in manifest.get(group,[]):item['sourceDigest']=digest_bytes(before[item['path']])
    after['manifest.json']=encode(manifest)
    if collect_files(root)!=before:raise PackageError('CONCURRENT_CHANGE','读取后文件发生变化；未写入')
    changed=[name for name in sorted(after) if after[name]!=before[name]]
    # 全部计算和路径核对完成后再写入；最后写顶层清单。
    for name in sorted(changed,key=lambda n:n=='manifest.json'):
        p=safe_path(root,name);fd,tmp=tempfile.mkstemp(prefix='.digest-',dir=p.parent)
        try:
            with os.fdopen(fd,'wb') as f:f.write(after[name])
            os.replace(tmp,p)
        finally:Path(tmp).unlink(missing_ok=True)
    return {'status':'REVALIDATION_REQUIRED' if changed else 'UNCHANGED','changedFiles':changed,'previousInputDigest':snapshot_digest(before),'currentInputDigest':snapshot_digest(after),'previousEvidenceInvalidated':bool(changed),'note':'归档保留旧证据，但只能按其原输入摘要引用；没有删除历史或修改业务语义'}

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('workspace');a=ap.parse_args()
    try:print(json.dumps(refresh(Path(a.workspace)),ensure_ascii=False,indent=2));return 0
    except (PackageError,KeyError,ValueError,OSError) as e:print(json.dumps({'error':getattr(e,'code','REFRESH_ERROR'),'message':str(e)},ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
