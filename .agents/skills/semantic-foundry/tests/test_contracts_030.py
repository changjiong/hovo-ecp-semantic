"""已审阅缺陷与安全边界的确定性回归；不代表模型行为评估。"""
from __future__ import annotations
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
SPEC = importlib.util.spec_from_file_location('validator030', ROOT/'scripts/validate_ecp_assets.py')
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)

def dump(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def run_script(name, *args):
    return subprocess.run([sys.executable, str(ROOT/'scripts'/name), *map(str,args)], capture_output=True, text=True)

def make_workspace(root):
    """实际存在的合成源结构来自工具箱示例；不声明银行数据已连接。"""
    (root/'ontology').mkdir(parents=True)
    (root/'ontology/model.ttl').write_text('''@prefix ex: <urn:example:ontology:> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:ontology a owl:Ontology .
ex:Customer a owl:Class .
ex:customerName a owl:DatatypeProperty; rdfs:domain ex:Customer; rdfs:range xsd:string .
''', encoding='utf-8')
    guide=(ROOT/'references/ecp-kit-1.7/guides/ecp-mapping-json-format.md').read_text()
    mapping=json.loads(re.search(r'```json mapping-example\n(.*?)\n```',guide,re.S).group(1))
    mapping['ontologySourceDigest']=v.sha256_file(root/'ontology/model.ttl')
    dump(root/'mapping/model.json', mapping)
    rules={'schemaVersion':1,'kind':'ECP_RULE_SET_BUNDLE','bundleFormat':'enterprise-cognitive/rule-set-bundle/1.0.0','semanticProfileId':v.PROFILE_ID,'semanticProfileDigest':v.PROFILE_DIGEST,'members':[]}
    for stage in ['asserted','domain','feature','change','output','provenance']:
        rel=f'rules/shacl/{stage}.ttl'; p=root/rel;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(f'''@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <urn:example:ontology:> .
<urn:test:{stage}> a sh:NodeShape; sh:targetClass ex:Customer; sh:property [sh:path ex:customerName; sh:minCount 0] .
''',encoding='utf-8')
        rules['members'].append({'assetSeriesId':stage,'assetType':'SHACL','name':stage,'description':'合成回归','path':rel,'mediaType':'text/turtle','sourceDigest':v.sha256_file(p),'shaclStage':stage})
    dump(root/'rules/manifest.json',rules)
    manifest={'schemaVersion':1,'kind':'ECP_SEMANTIC_WORKSPACE_PACKAGE','bundleFormat':'enterprise-cognitive/semantic-workspace-package/1.0.0','semanticProfileId':v.PROFILE_ID,'semanticProfileDigest':v.PROFILE_DIGEST,
    'ontology':{'path':'ontology/model.ttl','mediaType':'text/turtle','sourceDigest':v.sha256_file(root/'ontology/model.ttl')},
    'mapping':{'path':'mapping/model.json','mediaType':'application/json','sourceDigest':v.sha256_file(root/'mapping/model.json'),'ontologySourceDigest':mapping['ontologySourceDigest']},
    'ruleSet':{'manifestPath':'rules/manifest.json','sourceDigest':v.sha256_file(root/'rules/manifest.json')},'schemas':[]}
    dump(root/'manifest.json',manifest)
    return manifest

class ReviewedRegressions(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(); self.root=Path(self.t.name)
    def tearDown(self): self.t.cleanup()
    def codes(self,r): return {e['code'] for e in r['errors']}
    def test_empty_json_not_valid(self):
        p=self.root/'x.json';dump(p,{})
        self.assertNotEqual(v.validate_path(p)['summary']['status'],'LOCALLY_VALID')
    def test_unknown_kind_not_valid(self):
        p=self.root/'x.json';dump(p,{'kind':'UnrecognizedSemanticAsset'})
        self.assertNotEqual(v.validate_path(p)['summary']['status'],'LOCALLY_VALID')
    def test_nonobject_json_not_valid(self):
        p=self.root/'x.json';dump(p,[])
        self.assertNotEqual(v.validate_path(p)['summary']['status'],'LOCALLY_VALID')
    def test_empty_directory_not_valid(self):
        self.assertNotEqual(v.validate_path(self.root)['summary']['status'],'LOCALLY_VALID')
    def test_bad_min_count_rejected(self):
        p=self.root/'shape.ttl';p.write_text('@prefix sh:<http://www.w3.org/ns/shacl#>. <urn:s> a sh:NodeShape;sh:targetClass <urn:C>;sh:property [sh:path <urn:p>;sh:minCount "oops"].')
        self.assertIn('SHACL_COUNT',self.codes(v.validate_path(p)))
    def test_negative_count_rejected(self):
        p=self.root/'shape.ttl';p.write_text('@prefix sh:<http://www.w3.org/ns/shacl#>. <urn:s> a sh:NodeShape;sh:targetClass <urn:C>;sh:property [sh:path <urn:p>;sh:minCount -1].')
        self.assertIn('SHACL_COUNT',self.codes(v.validate_path(p)))
    def test_property_shape_missing_path(self):
        p=self.root/'shape.ttl';p.write_text('@prefix sh:<http://www.w3.org/ns/shacl#>. <urn:s> a sh:NodeShape;sh:targetClass <urn:C>;sh:property [sh:minCount 1].')
        self.assertIn('SHACL_PATH_COUNT',self.codes(v.validate_path(p)))
    def test_bad_list_rejected(self):
        p=self.root/'shape.ttl';p.write_text('@prefix sh:<http://www.w3.org/ns/shacl#>. <urn:s> a sh:NodeShape;sh:targetClass <urn:C>;sh:in <urn:nonlist>.')
        self.assertIn('SHACL_LIST',self.codes(v.validate_path(p)))
    def test_valid_workspace_accepted(self):
        make_workspace(self.root)
        r=v.validate_path(self.root);self.assertFalse(r['errors'],r['errors'])
    def test_unlisted_draft_rejected(self):
        make_workspace(self.root);dump(self.root/'rules/hidden.draft.json',{'password':'SYNTHETIC-NOT-REAL'})
        self.assertIn('UNLISTED_FILE',self.codes(v.validate_path(self.root)))
    def test_unlisted_file_never_packaged(self):
        w=self.root/'w';make_workspace(w);dump(w/'rules/hidden.draft.json',{'password':'SYNTHETIC-NOT-REAL'})
        p=run_script('package_workspace.py',w,'--output',self.root/'out.zip')
        self.assertNotEqual(p.returncode,0);self.assertFalse((self.root/'out.zip').exists())
    def test_package_does_not_refresh_digests(self):
        w=self.root/'w';make_workspace(w);m=(w/'manifest.json').read_bytes()
        with (w/'ontology/model.ttl').open('a') as f:f.write('\n# changed\n')
        p=run_script('package_workspace.py',w,'--output',self.root/'out.zip')
        self.assertNotEqual(p.returncode,0);self.assertEqual((w/'manifest.json').read_bytes(),m)
    def test_missing_mapping_class_rejected(self):
        make_workspace(self.root);p=self.root/'mapping/model.json';d=json.loads(p.read_text());d['entities'][0]['classIri']='urn:example:ontology:NeverDeclared';dump(p,d)
        m=json.loads((self.root/'manifest.json').read_text());m['mapping']['sourceDigest']=v.sha256_file(p);dump(self.root/'manifest.json',m)
        self.assertIn('MAPPING_CLASS_UNDECLARED',self.codes(v.validate_path(self.root)))
    def test_invalid_rule_member_type_not_silently_ignored(self):
        make_workspace(self.root);p=self.root/'rules/manifest.json';d=json.loads(p.read_text());d['members'][0]['assetType']='DERIVATION';dump(p,d)
        r=v.validate_path(self.root);self.assertTrue(r['errors'])
    def test_trigger_requires_actual_skill(self):
        d=self.root/'empty';(d/'evals').mkdir(parents=True);(d/'evals/trigger_cases.json').write_bytes((ROOT/'evals/trigger_cases.json').read_bytes())
        p=run_script('trigger_eval.py',d)
        self.assertNotEqual(p.returncode,0)
    def test_duplicate_json_keys_rejected(self):
        p=self.root/'x.json';p.write_text('{"kind":"ActionPolicy","kind":"Unknown"}')
        self.assertIn('JSON_PARSE',self.codes(v.validate_path(p)))
    def test_nonfinite_json_rejected(self):
        p=self.root/'x.json';p.write_text('{"kind":"Unknown","value":NaN}')
        self.assertIn('JSON_PARSE',self.codes(v.validate_path(p)))
    def test_no_filename_heuristic_for_shacl(self):
        p=self.root/'anything.ttl';p.write_text('@prefix sh:<http://www.w3.org/ns/shacl#>. <urn:s> a sh:NodeShape;sh:targetClass <urn:C>;sh:property [sh:path <urn:p>;sh:minCount 1].')
        self.assertFalse(v.validate_path(p)['errors'])
    def test_zip_traversal_rejected_before_extraction(self):
        p=self.root/'bad.zip'
        with zipfile.ZipFile(p,'w') as z:z.writestr('../bad.json','{}')
        self.assertTrue(v.validate_path(p)['errors'])
    def test_workspace_symlink_rejected(self):
        w=self.root/'w';make_workspace(w);p=w/'ontology/model.ttl';raw=p.read_bytes();p.unlink();(self.root/'outside.ttl').write_bytes(raw);p.symlink_to(self.root/'outside.ttl')
        self.assertIn('SYMLINK',self.codes(v.validate_path(w)))

if __name__=='__main__':unittest.main()
