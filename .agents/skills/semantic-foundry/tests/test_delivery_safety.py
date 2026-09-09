"""正向打包、摘要重验、来源完整性与空验证边界。"""
import unittest,tempfile,sys,json,zipfile,shutil,hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from test_contracts_030 import make_workspace
from package_workspace import package
from refresh_workspace_digests import refresh
from workspace_files import collect_files,PackageError
from validate_ecp_assets import validate_path
from validate_skill import validate
from validate_shacl_instance import target_nodes
from rdflib import Graph,URIRef
class DeliverySafety(unittest.TestCase):
 def test_package_exactly_matches_validated_bytes(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'w';make_workspace(root);before=collect_files(root);z=Path(t)/'p.zip';report=package(root,z)
   with zipfile.ZipFile(z) as f:
    self.assertEqual(set(f.namelist()),set(before))
    self.assertTrue(all(f.read(n)==b for n,b in before.items()))
   self.assertEqual(collect_files(root),before);self.assertFalse(report['releaseReady']);self.assertFalse(validate_path(z)['errors'])
 def test_packaging_is_reproducible(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'w';make_workspace(root);a=Path(t)/'a.zip';b=Path(t)/'b.zip';package(root,a);package(root,b)
   self.assertEqual(a.read_bytes(),b.read_bytes())
 def test_output_inside_workspace_refused(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'w';make_workspace(root)
   with self.assertRaises(PackageError):package(root,root/'out.zip')
 def test_existing_package_not_overwritten(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'w';make_workspace(root);out=Path(t)/'o.zip';out.write_bytes(b'keep')
   with self.assertRaises(PackageError):package(root,out)
   self.assertEqual(out.read_bytes(),b'keep')
 def test_explicit_refresh_requires_new_evidence(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'w';make_workspace(root)
   with (root/'ontology/model.ttl').open('a') as f:f.write('\n# intentional text change\n')
   self.assertTrue(validate_path(root)['errors']);r=refresh(root)
   self.assertEqual(r['status'],'REVALIDATION_REQUIRED');self.assertTrue(r['previousEvidenceInvalidated']);self.assertFalse(validate_path(root)['errors'])
 def test_refresh_does_not_replace_profile(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'w';make_workspace(root);p=root/'manifest.json';m=json.loads(p.read_text());m['semanticProfileDigest']='sha256:'+'1'*64;p.write_text(json.dumps(m));before=p.read_bytes()
   with self.assertRaises(PackageError):refresh(root)
   self.assertEqual(p.read_bytes(),before)
 def test_source_handbook_change_detected(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'hovo-ecp-semantic';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('__pycache__'))
   p=root/'references/handbooks-v2/01-methodology.md'
   with p.open('a') as f:f.write('\nchange\n')
   result=validate(root);self.assertFalse(result['ok']);self.assertTrue(any('手册原文摘要' in x for x in result['failures']))
 def test_target_typo_is_observable_independently(self):
  data=Graph().parse(data='<urn:x> a <urn:C>.',format='turtle')
  shapes=Graph().parse(data='@prefix sh:<http://www.w3.org/ns/shacl#>. <urn:s> a sh:NodeShape;sh:targetClass <urn:Typo>.',format='turtle')
  actual=target_nodes(data,shapes,URIRef('urn:s'));expected={URIRef('urn:x')}
  self.assertNotEqual(actual,expected);self.assertEqual(len(actual),0)
 def test_static_checks_never_imply_standard_or_business_approval(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);make_workspace(root);r=validate_path(root)
   self.assertEqual(r['evidence']['shaclInstanceValidation'],'NOT_EXECUTED');self.assertEqual(r['evidence']['ecpCompilation'],'NOT_EXECUTED');self.assertEqual(r['evidence']['domainExpertReview'],'NOT_EXECUTED')
 def test_scaffold_does_not_invent_platform_assets(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'new'
   p=subprocess.run([sys.executable,str(ROOT/'scripts/scaffold_design.py'),str(root)],capture_output=True,text=True);self.assertEqual(p.returncode,0)
   self.assertEqual([x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file()],['design/contract.json'])
   p=subprocess.run([sys.executable,str(ROOT/'scripts/validate_design.py'),str(root)],capture_output=True,text=True)
   self.assertEqual(p.returncode,2);self.assertEqual(json.loads(p.stdout)['status'],'INCOMPLETE')
if __name__=='__main__':unittest.main()
