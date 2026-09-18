#!/usr/bin/env python3
"""Emit draft handoff and generated reading views from an authored model.yaml."""
import argparse
import hashlib
import json
import os
from pathlib import Path

from domain_dsl import load_model, validate_model, render_review, render_coverage
from validate_contract import check_handoff, load_json, safe_regular_file, contains_forbidden_name


def emit(model_path, request_path, directory, project_root, refresh_draft=False):
    project_root = Path(os.path.abspath(project_root))
    model_path = safe_regular_file(model_path, root=project_root)
    request_path = safe_regular_file(request_path, root=project_root)
    directory = Path(os.path.abspath(directory))
    directory.relative_to(project_root)
    if contains_forbidden_name(directory) or any(p.is_symlink() for p in (directory, *directory.parents)):
        raise ValueError('交付路径不能含禁读名称或经过符号链接')
    targets = [directory/name for name in ('review.md','coverage.md','output.json')]
    if any(p.exists() for p in targets) and not refresh_draft:
        raise ValueError('目标交付文件已存在；修订前须先完整归档旧版模型、请求和交付文件，再更新当前目录。不得覆盖未归档评审字节')
    old = None
    if any(p.exists() for p in targets) and refresh_draft:
        old = load_json(directory/'output.json', root=project_root)
        if old.get('confirmation', {}).get('status') != 'PENDING' or old.get('states', {}).get('business_reviewed', {}).get('status') != 'NOT_EXECUTED':
            raise ValueError('仅可刷新尚未进行业务评审的待审草稿；已评审成果须归档并产生新版本')
    checked = check_handoff('input', request_path, project_root)
    if checked['status'] != 'PASS':
        return checked
    request = load_json(request_path, root=project_root)
    if request['mode']=='REVIEW':
        raise ValueError('REVIEW 不生成新模型，按审查输出合同交付')
    model = load_model(model_path)
    errors = validate_model(model)
    if errors:
        return {'status':'FAIL', 'failures':errors}
    if old is not None and any(old.get(k) != model[k] for k in ('artifact_id','content_version')):
        raise ValueError('刷新草稿必须是相同模型身份和草稿版本；新版本先归档旧交付')
    for mk,rk in [('knowledge_ref','knowledge'),('knowledge_basis','knowledge_basis'),('question_scope_ids','question_scope_ids'),('scope_mode','scope_mode')]:
        if model[mk] != request[rk]:
            raise ValueError(f'DSL 与请求不一致: {mk}')
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'review.md').write_text(render_review(model),encoding='utf-8')
    (directory/'coverage.md').write_text(render_coverage(model),encoding='utf-8')
    def ref(path,identifier,contract='5.0.0'):
        return dict(artifact_id=identifier,content_version=model['content_version'],contract_version=contract,path=path.relative_to(project_root).as_posix(),digest='sha256:'+hashlib.sha256(path.read_bytes()).hexdigest())
    mr=ref(model_path,model['artifact_id'],'domain-model-dsl/2.0.0')
    rr=ref(request_path,request['request_id'])
    not_run={'status':'NOT_EXECUTED','evidence_ids':[],'reason':'证据另由本次校验记录或真实责任人评审提供；生成不等于通过。'}
    evidence=list(request.get('evidence',[]))
    if request['knowledge_basis']=='CONFIRMED':
        evidence.append(request['knowledge_confirmation'])
    payload=dict(artifact_id=model['artifact_id'],content_version=model['content_version'],contract_version='5.0.0',stage='domain-model',mode=request['mode'],input_refs=[rr,model['knowledge_ref']]+request.get('subjects',[]),files=[mr,ref(directory/'review.md',model['artifact_id']+'.Review'),ref(directory/'coverage.md',model['artifact_id']+'.Coverage')],evidence=evidence,states={'structure_checked':dict(not_run),'business_reviewed':dict(not_run)},issues=model['issues'],trace=[dict(from_id=model['artifact_id'],to_id=model['knowledge_ref']['artifact_id'],relation='FORMALIZES',basis='固定知识版本下的领域 DSL 草案；形式化范围见 model.yaml')],content={'model_ref':mr,'request_ref':rr},confirmation={'status':'PENDING','scope_ids':model['question_scope_ids'],'evidence_ids':[]})
    (directory/'output.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result=check_handoff('output',directory/'output.json',project_root)
    result['output']=str(directory/'output.json')
    result['boundary']='校验结果在本报告；output.json 中的评审与确认不会因生成自动升级。'
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model',type=Path)
    parser.add_argument('--request',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--project-root',type=Path,required=True)
    parser.add_argument('--refresh-draft',action='store_true',help='重生成尚未进行业务评审的同版待审草稿；不会继承旧验证或确认状态')
    args=parser.parse_args()
    try:
        result=emit(args.model,args.request,args.output_dir,args.project_root,args.refresh_draft)
    except (OSError,ValueError,KeyError,TypeError) as exc:
        result={'status':'FAIL','failures':[{'code':'DELIVERY_FAILED','message':str(exc)}]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':
    raise SystemExit(main())
