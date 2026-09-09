"""以固定ECP配置原文为依据，避免通用标准假设覆盖平台合同。"""
import unittest,tempfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from validate_ecp_assets import validate_path
class ProfileDetails(unittest.TestCase):
 def check_text(self,text):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'shapes.ttl';p.write_text('@prefix sh:<http://www.w3.org/ns/shacl#>. @prefix rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>. '+text)
   return validate_path(p)
 def test_repeated_constraints_conjunctive_allowed(self):
  r=self.check_text('<urn:s> a sh:NodeShape;sh:targetClass <urn:C>;sh:property [sh:path <urn:p>;sh:minCount 1,2].')
  self.assertFalse(r['errors'],r['errors'])
 def test_list_cells_must_be_blank_nodes(self):
  r=self.check_text('<urn:s> a sh:NodeShape;sh:targetClass <urn:C>;sh:in <urn:list>. <urn:list> rdf:first <urn:x>;rdf:rest rdf:nil.')
  self.assertIn('SHACL_LIST',{e['code'] for e in r['errors']})
 def test_not_parameter_not_a_literal(self):
  r=self.check_text('<urn:s> a sh:NodeShape;sh:targetClass <urn:C>;sh:not "not-a-shape".')
  self.assertIn('SHACL_SHAPE_REFERENCE',{e['code'] for e in r['errors']})
 def test_node_kind_blank_node_unsupported(self):
  r=self.check_text('<urn:s> a sh:NodeShape;sh:targetClass <urn:C>;sh:nodeKind sh:BlankNode.')
  self.assertIn('SHACL_NODE_KIND',{e['code'] for e in r['errors']})
 def test_multiple_paths_rejected(self):
  r=self.check_text('<urn:s> a sh:NodeShape;sh:targetClass <urn:C>;sh:property [sh:path <urn:p>,<urn:q>].')
  self.assertIn('SHACL_PATH_COUNT',{e['code'] for e in r['errors']})
if __name__=='__main__':unittest.main()
