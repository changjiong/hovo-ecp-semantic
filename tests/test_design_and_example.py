"""契约与实际合成切片验证，不代表独立宿主模型评测。"""
import sys, unittest, tempfile, shutil, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from validate_design import validate_design
class DesignTests(unittest.TestCase):
 def test_example_has_complete_contract(self):
  r=validate_design(ROOT/'examples/ownership-slice');self.assertEqual(r['status'],'PASS',r)
 def test_missing_granularity_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'e';shutil.copytree(ROOT/'examples/ownership-slice',p)
   c=json.loads((p/'design/contract.json').read_text());del c['concepts'][0]['granularity'];(p/'design/contract.json').write_text(json.dumps(c))
   self.assertEqual(validate_design(p)['status'],'FAIL')
 def test_missing_expected_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'e';shutil.copytree(ROOT/'examples/ownership-slice',p);(p/'expected/results.json').unlink()
   self.assertEqual(validate_design(p)['status'],'FAIL')
 def test_phantom_concept_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'e';shutil.copytree(ROOT/'examples/ownership-slice',p)
   c=json.loads((p/'design/contract.json').read_text());c['concepts'][0]['iri']='urn:missing';(p/'design/contract.json').write_text(json.dumps(c))
   self.assertEqual(validate_design(p)['status'],'FAIL')
 def test_declared_approval_requires_evidence(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'e';shutil.copytree(ROOT/'examples/ownership-slice',p)
   c=json.loads((p/'design/contract.json').read_text());c['review']['independent_expert']='EVIDENCE_ATTACHED';(p/'design/contract.json').write_text(json.dumps(c))
   self.assertEqual(validate_design(p)['status'],'FAIL')
 def test_example_executes_and_preserves_expected(self):
  with tempfile.TemporaryDirectory() as t:
   p=subprocess.run([sys.executable,str(ROOT/'examples/ownership-slice/run.py'),'--output',t],capture_output=True,text=True)
   self.assertEqual(p.returncode,0,p.stderr+p.stdout)
   r=json.loads((Path(t)/'verification.json').read_text());self.assertEqual(r['status'],'PASS');self.assertEqual(r['ecpCompilation'],'NOT_EXECUTED')
if __name__=='__main__':unittest.main()
