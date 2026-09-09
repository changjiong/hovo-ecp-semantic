import json, unittest
from pathlib import Path
from src.semantic_case import build_view, compute_ownership
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf8"))
class FirstContracts(unittest.TestCase):
 def setUp(self):
  self.raw=load("fixtures/source-records.json"); self.sel=load("fixtures/selection.json"); self.cov=load("fixtures/coverage.json")
  self.exp=load("spec/expected.json")["base"]
 def test_base_has_five_deduplicated_positions(self):
  v=build_view(self.raw,self.sel,"2026-02-15","2026-02-15T00:00:00Z")
  self.assertEqual(len(v["facts"]),self.exp["facts"])
 def test_exact_ownership_totals(self):
  v=build_view(self.raw,self.sel,"2026-02-15","2026-02-15T00:00:00Z")
  c=compute_ownership(v,self.raw,self.cov,"T","0.25")
  self.assertEqual(c["totals"],self.exp["ownership_totals"])
 def test_ownership_threshold_matches_are_not_full_ubo(self):
  v=build_view(self.raw,self.sel,"2026-02-15","2026-02-15T00:00:00Z")
  c=compute_ownership(v,self.raw,self.cov,"T","0.25")
  self.assertEqual(c["threshold_matches"],self.exp["threshold_matches"])
if __name__=="__main__": unittest.main()
