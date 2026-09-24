"""Internal module: audit DSL-to-knowledge bindings, not business truth."""
from collections import Counter
from dsl_semantics import elements, semantic_references


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def check_content(payload, failures, knowledge=None, model=None):
    def fail(code, location, message):
        failures.append(dict(code=code, location=location, message=message))

    def refs(values, allowed, location):
        for value in values:
            if value not in allowed:
                fail('REFERENCE_UNDEFINED', location, f'未定义或类型不符的引用: {value}')

    def exact(values, expected, location):
        counts = Counter(values)
        for value in sorted(expected - counts.keys()):
            fail('COVERAGE_MISSING', location, f'未覆盖: {value}')
        for value, count in counts.items():
            if value not in expected or count != 1:
                fail('COVERAGE_INVALID', location, f'范围外或重复覆盖: {value}')

    issues = {i['id']: i for i in payload['issues']}
    allowed = {o['artifact_id'] for o in objects(payload) if 'artifact_id' in o} | set(issues)
    allowed |= {e['evidence_id'] for e in payload['evidence']}
    if payload['mode'] == 'REVIEW':
        for subject in payload['content']['subjects']:
            if subject not in payload['input_refs']:
                fail('REVIEW_SUBJECT_UNBOUND', 'content/subjects', '审查对象必须是精确输入引用')
    else:
        if knowledge is None or model is None:
            fail('BASELINE_REQUIRED', 'content', '缺少 DSL 或知识基线')
            return
        kc = knowledge['content']
        questions = {i['id']: i for i in kc['questions']}
        cases = {i['id']: i for i in kc['cases']}
        ki = {i['id']: i for i in knowledge['issues']}
        basis = {i['id'] for group in ['statements', 'terms', 'rules'] for i in kc[group]}
        knowledge_ids = {i['id'] for i in objects(kc) if 'id' in i} | set(ki)
        model_ids = set(elements(model)) - set(issues)
        allowed |= knowledge_ids | semantic_references(model) | {s['source_id'] for s in kc['sources']}
        for identifier in model_ids & knowledge_ids:
            fail('ID_NAMESPACE_COLLISION', identifier, '模型和知识标识不能重复')
        scope = set(model['question_scope_ids'])
        if model['scope_mode'] == 'FULL_BASELINE' and scope != set(questions):
            fail('FULL_BASELINE_SCOPE_INCOMPLETE', 'question_scope_ids', '全量模型必须覆盖知识基线全部问题')
        refs(scope, questions, 'question_scope_ids')
        refs(scope, set(knowledge['confirmation']['scope_ids']), 'knowledge/declared_scope')
        if set(payload['confirmation']['scope_ids']) != scope:
            fail('CONFIRMATION_SCOPE_MISMATCH', 'confirmation', '模型确认范围必须与本次问题范围一致')
        if model['knowledge_basis'] == 'DRAFT' and payload['confirmation']['status'] != 'PENDING':
            fail('DRAFT_FORMAL_CONFIRMATION_FORBIDDEN', 'confirmation', 'DRAFT 必须保持 PENDING')
        if model['knowledge_ref'] not in payload['input_refs']:
            fail('KNOWLEDGE_REF_UNBOUND', 'input_refs', '知识基线必须登记为精确输入引用')
        if model['issues'] != payload['issues']:
            fail('ISSUE_PROJECTION_DRIFT', 'issues', '交接问题清单必须由 DSL 原样生成')
        for item in objects(model):
            if 'basis_ids' in item:
                refs(item['basis_ids'], basis, item.get('id','model')+'/basis_ids')
        bindings = model['upstream_issue_bindings']
        exact([r['knowledge_issue_id'] for r in bindings], {k for k,v in ki.items() if v['status']=='OPEN'}, 'upstream_issue_bindings')
        for row in bindings:
            upstream = ki.get(row['knowledge_issue_id'], {})
            refs(row['model_issue_ids'], issues, 'upstream_issue_bindings')
            impact = set(upstream.get('affects', [])) & scope
            # A shared type or a chapter/process grouping is not a business dependency.
            # Propagate source rule/statement changes through actual rule dependencies.
            affected_sources = {r['id'] for r in kc['rules']
                                if r['id'] in upstream.get('affects', [])
                                or set(r['statement_ids']) & set(upstream.get('affects', []))}
            impact |= {q for r in kc['rules'] if r['id'] in affected_sources for q in r['question_ids']} & scope
            affected_rules = {r['id'] for r in model['rules'] if set(r['basis_ids']) & affected_sources}
            while True:
                expanded = affected_rules | {r['id'] for r in model['rules'] if set(r['depends_on']) & affected_rules}
                if expanded == affected_rules:
                    break
                affected_rules = expanded
            impact |= {q for r in model['rules'] if r['id'] in affected_rules for q in r['question_ids']}
            bound = set()
            for identifier in row['model_issue_ids']:
                issue = issues.get(identifier, {})
                if issue.get('kind') != 'MODEL_GAP' or issue.get('status') != 'OPEN':
                    fail('UPSTREAM_ISSUE_INVALID', identifier, '上游开放事项必须关联开放 MODEL_GAP')
                if row['knowledge_issue_id'] not in issue.get('affects', []):
                    fail('UPSTREAM_ISSUE_IMPACT_MISSING', identifier, '未登记上游问题标识')
                bound.update(issue.get('affects', []))
            if not impact.issubset(bound):
                fail('UPSTREAM_QUESTION_IMPACT_MISSING', row['knowledge_issue_id'], '未完整承接上游对本范围的影响')
            if impact and row['handling'] == 'NOT_APPLICABLE':
                fail('UPSTREAM_NOT_APPLICABLE_INVALID', row['knowledge_issue_id'], '已影响本范围，不能标记不适用')
        exact([r['question_id'] for r in model['question_coverage']], scope, 'question_coverage')
        coverage = {r['question_id']:r for r in model['question_coverage']}
        source_rules = {r['id']:r for r in kc['rules'] if scope & set(r['question_ids'])}
        exact([r['knowledge_rule_id'] for r in model['rule_coverage']], set(source_rules), 'rule_coverage')
        for row in model['rule_coverage']:
            rule = source_rules.get(row['knowledge_rule_id'])
            if rule is None:
                continue
            exact(row['question_ids'], set(rule['question_ids']) & scope, row['knowledge_rule_id']+'/question_ids')
            refs(row['model_ids'], model_ids, row['knowledge_rule_id']+'/model_ids')
            classes = set(row['modeling_classification'])
            has_domain_model = bool(classes & {'CORE_STRUCTURE','DOMAIN_DECISION'})
            if 'NO_MODEL_CHANGE' in classes and len(classes) != 1:
                fail('RULE_MODELING_CLASS_INVALID', row['knowledge_rule_id'], 'NO_MODEL_CHANGE 必须单独使用')
            if row['status'] == 'MODELED':
                if not has_domain_model or not row['model_ids'] or row['gap_ids']:
                    fail('RULE_MODELING_STATUS_INVALID', row['knowledge_rule_id'], 'MODELED 必须有核心结构/领域判断模型引用且无开放缺口')
            elif row['status'] == 'PARTIAL':
                if not has_domain_model or not row['model_ids'] or not row['gap_ids']:
                    fail('RULE_MODELING_STATUS_INVALID', row['knowledge_rule_id'], 'PARTIAL 必须已有模型引用且仍有开放缺口')
            elif row['status'] == 'EXTERNAL_CONTEXT':
                if classes != {'EXTERNAL_CONTEXT'} or row['model_ids'] or row['gap_ids']:
                    fail('RULE_MODELING_STATUS_INVALID', row['knowledge_rule_id'], '纯外部上下文不得伪造模型引用或模型缺口')
            elif row['status'] == 'NO_MODEL_CHANGE':
                if classes != {'NO_MODEL_CHANGE'} or row['model_ids'] or row['gap_ids']:
                    fail('RULE_MODELING_STATUS_INVALID', row['knowledge_rule_id'], '无模型变化规则不得伪造模型引用或模型缺口')
            elif row['status'] == 'DEFERRED' and not row['gap_ids']:
                fail('RULE_MODELING_STATUS_INVALID', row['knowledge_rule_id'], 'DEFERRED 必须有开放模型缺口')
            for name, facet in row['facets'].items():
                if facet['source_text'] != rule[name]:
                    fail('RULE_FACET_SOURCE_CHANGED', row['knowledge_rule_id']+'/'+name, '覆盖表必须原样保留固定知识的规则要素')
            if row['status'] in {'EXTERNAL_CONTEXT','NO_MODEL_CHANGE'}:
                if any(facet['status'] != 'NOT_MODELED' or facet['model_refs'] for facet in row['facets'].values()):
                    fail('RULE_NOT_MODELED_FACET_INVALID', row['knowledge_rule_id'], '未进入模型的规则要素必须标 NOT_MODELED 且不得伪造模型引用')
            expected_gaps = {identifier for identifier, issue in issues.items()
                             if issue['kind']=='MODEL_GAP' and issue['status']=='OPEN'
                             and (set(issue['affects']) & (set(row['model_ids']) | {row['knowledge_rule_id']}))}
            if not expected_gaps.issubset(row['gap_ids']):
                fail('RULE_GAPS_INCOMPLETE', row['knowledge_rule_id'], '遗漏影响该规则或其模型要素的开放缺口')
        for row in coverage.values():
            refs(row['model_ids'], model_ids, 'question_coverage/model_ids')
            question = questions.get(row['question_id'])
            if question and row['question'] != question['question']:
                fail('QUESTION_TITLE_CHANGED', row['question_id'], '审阅问题必须保留知识基线的问题原文')
            exact(row['rule_ids'], {r['id'] for r in source_rules.values() if row['question_id'] in r['question_ids']}, row['question_id']+'/rule_ids')
            exact(row['case_ids'], {c['id'] for c in cases.values() if row['question_id'] in c['question_ids']}, row['question_id']+'/case_ids')
            for process_id in row['process_ids']:
                process = next((p for p in model['processes'] if p['id']==process_id), None)
                if process and row['question_id'] not in process['question_ids']:
                    fail('QUESTION_PROCESS_SCOPE_MISMATCH', row['question_id'], '关联流程没有声明该业务问题')
            gaps = {k for k,v in issues.items() if v['kind']=='MODEL_GAP' and v['status']=='OPEN' and row['question_id'] in v['affects']}
            if set(row['gap_ids']) != gaps:
                fail('QUESTION_GAPS_INCOMPLETE', row['question_id'], '必须列出全部影响该问题的开放模型缺口')
            if (row['status']=='MODELED' and gaps) or (row['status']!='MODELED' and not gaps):
                fail('COVERAGE_STATUS_INVALID', row['question_id'], '覆盖状态与开放缺口不一致')
        exact([r['case_id'] for r in model['case_explanations']], {k for k,v in cases.items() if scope & set(v['question_ids'])}, 'case_explanations')
        for row in model['case_explanations']:
            refs(row['model_ids'], model_ids, 'case_explanations/model_ids')
            case = cases.get(row['case_id'], {})
            if row['expected'] != case.get('expected') or row['forbidden'] != case.get('forbidden'):
                fail('CASE_EXPECTATION_CHANGED', row['case_id'], '不得改写上游预期或禁止结果')
            if row['input_facts'] != case.get('input_facts'):
                fail('CASE_INPUT_FACTS_CHANGED', row['case_id'], '不得改写上游案例输入事实')
            evidence_ids = {e['evidence_id'] for e in payload['evidence']}
            refs(row['evaluation_ids'], evidence_ids, row['case_id']+'/evaluation_ids')
            if row['status']=='BLOCKED' and not any(coverage[q]['gap_ids'] for q in case.get('question_ids',[]) if q in coverage):
                fail('CASE_BLOCKED_UNJUSTIFIED', row['case_id'], 'BLOCKED 必须由关联问题的开放缺口说明')
        for judgment in model['judgments']:
            refs(judgment['question_ids'], scope, judgment['id']+'/question_ids')
    for issue in issues.values():
        refs(issue['affects'], allowed, issue['id']+'/affects')
    for trace in payload['trace']:
        refs([trace['from_id'],trace['to_id']], allowed, 'trace')
