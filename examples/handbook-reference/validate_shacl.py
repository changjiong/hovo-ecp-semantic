#!/usr/bin/env python3
"""调用标准SHACL验证依赖，缺依赖时明确未执行，不使用替代实现。"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import importlib.metadata
from rdflib import Graph, URIRef
from src.semantic_case import H, X, graph_contract
ROOT=Path(__file__).resolve().parent

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'reports/standard-shacl.json')
    a=p.parse_args();a.output.parent.mkdir(parents=True,exist_ok=True)
    try:
        from pyshacl import validate
    except ImportError:
        result={'status':'NOT_EXECUTED','reason':'缺少pyshacl依赖；本次环境安装因网络名称解析失败。',
                'install_command':'python -m pip install -r requirements-shacl.txt',
                'no_custom_fallback':True}
        a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(json.dumps(result,ensure_ascii=False,indent=2));return 2
    data=Graph().parse(ROOT/'reports/fact-view.ttl',format='turtle')
    shapes=Graph().parse(ROOT/'model/shapes.ttl',format='turtle')
    positive, pos_graph, pos_text=validate(data,shacl_graph=shapes,inference='none',
        meta_shacl=True,advanced=False,js=False,do_owl_imports=False,inplace=False)
    coverage=graph_contract(data,[X['position:E'+str(i)] for i in range(1,6)])
    negative=Graph()
    for triple in data:negative.add(triple)
    negative.remove((X['position:E1'],H.holder,None))
    conforms_neg, neg_graph, neg_text=validate(negative,shacl_graph=shapes,inference='none',
        meta_shacl=True,advanced=False,js=False,do_owl_imports=False,inplace=False)
    SH='http://www.w3.org/ns/shacl#'
    exact_negative=[]
    for node in neg_graph.subjects(URIRef(SH+'focusNode'),X['position:E1']):
        if (node,URIRef(SH+'resultPath'),H.holder) in neg_graph and (node,URIRef(SH+'sourceConstraintComponent'),URIRef(SH+'MinCountConstraintComponent')) in neg_graph:
            exact_negative.append(str(node))
    ok=bool(positive and coverage['pass'] and not conforms_neg and exact_negative)
    result={'status':'PASS' if ok else 'FAIL','validator_version':importlib.metadata.version('pyshacl'),
            'positive_conforms':bool(positive),'coverage':coverage,'negative_conforms':bool(conforms_neg),
            'expected_missing_holder_found':bool(exact_negative),'configuration':{'inference':'none','meta_shacl':True,'imports':False},
            'scope':'正例和缺持有人负例；不构成全部业务或全部SHACL能力认证'}
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (a.output.parent/'shacl-positive.txt').write_text(str(pos_text),encoding='utf8')
    (a.output.parent/'shacl-negative.txt').write_text(str(neg_text),encoding='utf8')
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
