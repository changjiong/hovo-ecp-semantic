"""预期来自spec/expected.json与手工构造反例，不由被测输出生成。"""
import copy, json, unittest
from pathlib import Path
from rdflib import Graph, Namespace, RDF, Literal, XSD
from jsonschema import ValidationError
from rdflib.compare import isomorphic
from src.semantic_case import (build_view, compute_ownership, map_raw, facts_graph,
                              normalize_ratio, graph_contract, validate_result_record,
                              validate_raw, bytes_digest)
ROOT=Path(__file__).resolve().parents[1]
H=Namespace('urn:hovo:semantic:'); X=Namespace('urn:hovo:demo:')
def load(p): return json.loads((ROOT/p).read_text(encoding='utf8'))
class Boundaries(unittest.TestCase):
 def setUp(self):
  self.raw=load('fixtures/source-records.json');self.sel=load('fixtures/selection.json');self.cov=load('fixtures/coverage.json')
  self.exp=load('spec/expected.json')
 def view(self, cutoff='2026-02-15T00:00:00Z', business='2026-02-15'):
  return build_view(self.raw,self.sel,business,cutoff)
 def calc(self,view=None,threshold='0.25'):
  return compute_ownership(view or self.view(),self.raw,self.cov,'T',threshold)
 def add(self,r):
  self.raw['records'].append(r);self.sel['accepted_assertions'].append({'assertion_id':r['id'],'accepted_at':r['known_at'],'basis':'合成测试'})
 def copy_first(self,id='a6',**changes):
  r=copy.deepcopy(self.raw['records'][0]);r.update(id=id,**changes);return r
 def test_04_reified_statement_does_not_create_direct_fact(self):
  g=map_raw(self.raw)
  self.assertEqual(len(list(g.subjects(RDF.type,H.Assertion))),5)
  self.assertEqual(len(list(g.triples((None,H.shareRatio,None)))),0)
 def test_05_fact_view_has_direct_query_and_provenance(self):
  g=facts_graph(self.view(),self.raw)
  q=(ROOT/'queries/direct-holders.rq').read_text()
  result=[str(r.holder).split(':')[-1] for r in g.query(q,initBindings={'target':X.T})]
  self.assertEqual(result,self.exp['base']['direct_holders'])
  self.assertEqual(len(list(g.query((ROOT/'queries/provenance.rq').read_text()))),5)
 def test_06_duplicate_evidence_is_not_duplicate_equity(self):
  self.add(self.copy_first(origin='DEMO-DOC-a1'))
  self.assertEqual(len(self.view()['facts']),5)
  self.assertEqual(self.calc()['totals'],self.exp['base']['ownership_totals'])
  self.assertEqual(len(self.view()['facts'][0]['assertion_ids']),2)
 def test_07_conflicting_values_are_not_averaged_or_voted(self):
  self.add(self.copy_first(value='55',origin='DIFFERENT-DOC'))
  self.assertIn('VALUE_CONFLICT',{i['code'] for i in self.view()['issues']})
  self.assertFalse(self.calc()['complete']);self.assertEqual(self.calc()['threshold_matches'],[])
 def test_08_multiple_copies_do_not_outvote_conflict(self):
  self.add(self.copy_first(value='55'))
  self.add(self.copy_first(id='a7'));self.add(self.copy_first(id='a8'))
  self.assertIn('VALUE_CONFLICT',{i['code'] for i in self.view()['issues']})
 def test_09_nonoverlapping_intervals_are_not_value_conflict(self):
  self.raw['records'][0]['valid_to']='2026-03-01'
  self.add(self.copy_first(valid_from='2026-03-01',valid_to='2026-07-01',value='55'))
  self.assertNotIn('VALUE_CONFLICT',{i['code'] for i in self.view()['issues']})
  self.assertEqual(self.calc()['totals']['P1'],'0.42')
 def test_10_explicit_corrections_are_bitemporal(self):
  self.add(self.copy_first(value='55',known_at='2026-04-01T00:00:00Z',supersedes=['a1']))
  r=copy.deepcopy(self.raw['records'][1]);r.update(id='a7',value='45',known_at='2026-04-01T00:00:00Z',supersedes=['a2']);self.add(r)
  self.assertEqual(self.calc(self.view())['totals'],self.exp['base']['ownership_totals'])
  self.assertEqual(self.calc(self.view('2026-05-01T00:00:00Z'))['totals'],self.exp['retrospective'])
 def test_11_late_acceptance_is_not_known_at_earlier_task(self):
  self.sel['accepted_assertions'][0]['accepted_at']='2026-04-01T00:00:00Z'
  self.assertNotIn('P1',self.calc()['totals']);self.assertFalse(self.calc()['complete'])
 def test_12_right_endpoint_is_exclusive(self):
  v=self.view('2026-07-01T00:00:00Z','2026-07-01')
  self.assertEqual(v['facts'],[]);self.assertFalse(self.calc(v)['complete'])
 def test_13_unknown_end_is_not_open_end(self):
  self.raw['records'][0].update(valid_to=None,end_kind='UNKNOWN')
  self.assertIn('UNKNOWN_VALIDITY',{i['code'] for i in self.view()['issues']})
 def test_14_explicit_open_end_can_be_used(self):
  self.raw['records'][0].update(valid_to=None,end_kind='OPEN')
  self.assertEqual(self.calc()['totals'],self.exp['base']['ownership_totals'])
 def test_15_missing_ratio_preserves_raw_but_excludes_calculation(self):
  self.raw['records'][0]['value']=None
  self.assertEqual(len(list(map_raw(self.raw).subjects(RDF.type,H.Assertion))),5)
  self.assertIn('MISSING_RATIO',{i['code'] for i in self.view()['issues']})
  self.assertNotIn('P1',self.calc()['totals'])
 def test_16_missing_start_is_not_invented(self):
  self.raw['records'][0]['valid_from']=None
  self.assertIn('UNKNOWN_VALIDITY',{i['code'] for i in self.view()['issues']})
 def test_17_scale_is_explicit(self):
  self.assertEqual(normalize_ratio('25','PERCENT'),normalize_ratio('0.25','FRACTION'))
  with self.assertRaises(ValueError):normalize_ratio('25','FRACTION')
 def test_18_invalid_numbers_are_rejected(self):
  for val in ['NaN','Infinity','-1','101']:
   with self.subTest(val=val):
    with self.assertRaises(ValueError):normalize_ratio(val,'PERCENT')
 def test_19_display_rounding_does_not_change_threshold(self):
  self.raw['records'][0]['value']='24.999';self.raw['records'][1]['value']='75.001'
  # 对A直接持股24.999%，即使显示25.00%，也不应命中25%门槛。
  c=compute_ownership(self.view(),self.raw,self.cov,'A','0.25')
  self.assertNotIn('P1',c['threshold_matches']);self.assertIn('P2',c['threshold_matches'])
 def test_20_multiple_distinct_paths_are_summed(self):
  self.raw['records'][4]['holder']='P1'
  self.assertEqual(self.calc()['totals'],self.exp['multi_path'])
 def test_21_cycles_are_explicitly_unsupported(self):
  self.raw['records'][1]['holder']='T'
  c=self.calc();self.assertFalse(c['complete'])
  self.assertIn('UNSUPPORTED_CYCLE',{i['code'] for i in c['issues']});self.assertEqual(c['threshold_matches'],[])
 def test_22_unaccounted_equity_blocks_complete_claim(self):
  self.raw['records'].pop();self.sel['accepted_assertions'].pop()
  self.assertFalse(self.calc()['complete'])
  self.assertIn('INCOMPLETE_EQUITY_SUM',{i['code'] for i in self.calc()['issues']})
 def test_23_sum_one_without_coverage_declaration_is_not_complete(self):
  self.cov['complete_for']=[]
  self.assertFalse(self.calc()['complete'])
 def test_24_same_name_different_subjects_do_not_merge(self):
  self.raw['subjects'][1]['label']=self.raw['subjects'][0]['label']
  self.assertEqual(self.calc()['totals'],self.exp['base']['ownership_totals'])
 def test_25_position_identity_mismatch_is_detected(self):
  self.add(self.copy_first(holder='P2'))
  self.assertIn('POSITION_IDENTITY_CONFLICT',{i['code'] for i in self.view()['issues']})
 def test_26_different_rights_do_not_mix(self):
  self.add(self.copy_first(position='V1',right='VOTING',value='55'))
  self.assertNotIn('VALUE_CONFLICT',{i['code'] for i in self.view()['issues']})
  self.assertEqual(self.calc()['totals'],self.exp['base']['ownership_totals'])
 def test_27_organization_controller_allowed_but_not_ubo_person(self):
  self.assertEqual(validate_result_record('ActualControllerDetermination','Organization'),[])
  self.assertIn('NATURAL_PERSON_REQUIRED',validate_result_record('BeneficialOwnerDetermination','Organization'))
 def test_28_no_empty_set_fallback_or_automatic_approval(self):
  self.raw['records']=[];self.sel['accepted_assertions']=[]
  c=self.calc();self.assertFalse(c['full_ubo_assessment']);self.assertFalse(c['automatic_fallback'])
  self.assertEqual(c['threshold_matches'],[])
 def test_29_zero_target_is_a_coverage_failure(self):
  g=facts_graph(self.view(),self.raw)
  result=graph_contract(g,[X['position:E'+str(i)] for i in range(1,6)],H.TypoPosition)
  self.assertEqual(result['actual_targets'],0);self.assertFalse(result['coverage_pass'])
 def test_30_missing_holder_is_a_specific_app_contract_failure(self):
  g=facts_graph(self.view(),self.raw);p=X['position:E1'];g.remove((p,H.holder,None))
  r=graph_contract(g,[X['position:E'+str(i)] for i in range(1,6)])
  self.assertIn({'position':str(p),'code':'MISSING_HOLDER'},r['violations'])
 def test_31_bytes_and_graph_equality_are_different(self):
  a='@prefix h: <urn:h:> . h:a h:p h:b . h:a h:q h:c .'
  b='@prefix h: <urn:h:> . h:a h:q h:c . h:a h:p h:b .'
  self.assertTrue(isomorphic(Graph().parse(data=a,format='turtle'),Graph().parse(data=b,format='turtle')))
  self.assertNotEqual(bytes_digest(a.encode()),bytes_digest(b.encode()))
 def test_32_source_schema_enforced_and_no_numeric_float(self):
  validate_raw(self.raw)
  self.raw['records'][0]['value']=0.6
  with self.assertRaises(ValidationError):validate_raw(self.raw)
 def test_33_source_and_selection_are_not_mutated(self):
  before=copy.deepcopy((self.raw,self.sel));self.view();self.calc()
  self.assertEqual((self.raw,self.sel),before)
 def test_34_unauthorized_or_unknown_acceptance_id_rejected(self):
  self.sel['accepted_assertions'].append({'assertion_id':'does-not-exist','accepted_at':'2026-01-10T00:00:00Z','basis':'测试'})
  with self.assertRaises(ValueError):self.view()
 def test_35_duplicate_source_identity_rejected(self):
  self.raw['records'].append(copy.deepcopy(self.raw['records'][0]))
  with self.assertRaises(ValueError):validate_raw(self.raw)
 def test_36_unrelated_source_gap_does_not_block_target(self):
  self.raw['subjects'].append({'id':'Z','kind':'Organization','label':'无关公司'})
  self.add(self.copy_first(position='EZ',issuer='Z',value=None))
  self.assertTrue(self.calc()['complete'])
 def test_37_three_business_record_kinds_can_coexist(self):
  g=Graph().parse(ROOT/'model/record-examples.ttl')
  kinds={str(v) for v in g.objects(None,H.recordKind)}
  self.assertEqual(kinds,{'客户申报','备案查询','机构拟识别'})
 def test_38_reversing_relation_breaks_query_contract(self):
  g=facts_graph(self.view(),self.raw)
  p=X['position:E3'];g.remove((p,H.issuer,X.T));g.add((X.T,H.issuer,p))
  rows=list(g.query((ROOT/'queries/direct-holders.rq').read_text(),initBindings={'target':X.T}))
  self.assertEqual(sorted(str(r.holder).split(':')[-1] for r in rows),['P3','P4'])
 def test_39_reified_ratio_is_normalized_but_raw_value_preserved(self):
  g=map_raw(self.raw);a=X['assertion:a1']
  self.assertEqual(g.value(a,RDF.object),Literal('0.6',datatype=XSD.decimal))
  self.assertEqual(str(g.value(a,H.raw_value)),'60')
 def test_40_correction_must_not_change_position_identity(self):
  self.add(self.copy_first(holder='P2',value='55',known_at='2026-04-01T00:00:00Z',supersedes=['a1']))
  v=self.view('2026-05-01T00:00:00Z')
  self.assertIn('INVALID_REPLACEMENT_IDENTITY',{i['code'] for i in v['issues']})
 def test_41_acceptance_before_source_knowledge_is_invalid(self):
  self.sel['accepted_assertions'][0]['accepted_at']='2026-01-01T00:00:00Z'
  with self.assertRaises(ValueError):self.view()
if __name__=='__main__':unittest.main()
