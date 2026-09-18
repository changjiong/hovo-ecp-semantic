"""DSL 2 checks for business bindings, ordered processes and rule-facet coverage.

These checks establish structural traceability, not the truth of business prose.
"""
from __future__ import annotations

from dsl_expression import DSLExpressionError, ValueSpec, declaration_spec, field_spec, infer_expression


def elements(model):
    result = {x['id']: x for group in ('types', 'temporal', 'rules', 'state_machines',
              'judgments', 'constraints', 'processes', 'issues') for x in model[group]}
    for machine in model['state_machines']:
        result.update((x['id'], x) for x in machine['transitions'])
    for process in model['processes']:
        result.update((x['id'], x) for x in process['steps'])
    return result


def semantic_references(model):
    """Exact references: element IDs, Type.field and selected semantic members."""
    result = set(elements(model))
    for kind in model['types']:
        result.update(kind['id'] + '.' + f['name'] for f in kind['fields'])
    for rule in model['rules']:
        result.update(rule['id'] + '.' + key for key in ('expression', 'on_unknown', 'result_binding'))
    for item in model['constraints']:
        result.update(item['id'] + '.' + key for key in ('expression', 'on_unknown'))
    for item in model['judgments']:
        result.update(item['id'] + '.' + key for key in ('criteria', 'required_evidence', 'on_missing', 'review_requirements'))
    for process in model['processes']:
        result.add(process['id'] + '.trigger')
        for step in process['steps']:
            result.update(step['id'] + '.' + key for key in ('reads', 'writes', 'depends_on', 'on_missing'))
    for machine in model['state_machines']:
        result.update(t['id'] + '.guard' for t in machine['transitions'])
    return result


def assignable(actual, expected):
    """Widen scalar types only; collection shape must agree."""
    if (actual.max_items is None or actual.max_items > 1) != (expected.max_items is None or expected.max_items > 1):
        return False
    if expected.max_items is not None and (actual.max_items is None or actual.max_items > expected.max_items):
        return False
    if actual.data_type == 'Integer' and expected.data_type == 'Decimal':
        return True
    if actual.data_type == 'Enum' and expected.data_type == 'Text':
        return True
    # A Text expression may construct a member of a declared Enum; runtime checks membership.
    if actual.data_type == 'Text' and expected.data_type == 'Enum':
        return True
    if actual.data_type != expected.data_type:
        return False
    if actual.data_type == 'Ref':
        return actual.target == expected.target
    if actual.data_type == 'Enum':
        return set(actual.values).issubset(expected.values)
    return True


def advanced_errors(model):
    errors = []

    def fail(code, location, message):
        errors.append(dict(code=code, location=location, message=message))

    types = {t['id']: t for t in model['types']}
    fields = {t['id'] + '.' + f['name']: f for t in model['types'] for f in t['fields']}
    all_elements = elements(model)
    refs = semantic_references(model)
    rules = {r['id']: r for r in model['rules']}
    judgments = {j['id']: j for j in model['judgments']}
    machines = {m['id']: m for m in model['state_machines']}
    constraints = {c['id']: c for c in model['constraints']}
    processes = {p['id']: p for p in model['processes']}
    issues = {i['id']: i for i in model['issues']}
    scope = set(model['question_scope_ids'])
    for type_def in model['types']:
        for field in type_def['fields']:
            if 'value_labels' in field:
                if field['type'] != 'Enum' or set(field['value_labels']) != set(field.get('values', [])):
                    fail('ENUM_LABELS_INCOMPLETE', type_def['id'] + '.' + field['name'], '业务枚举标签必须恰好覆盖全部枚举值')

    def references(values, valid, location):
        for value in values:
            if value not in valid:
                fail('DSL_REFERENCE_UNDEFINED', location, '未定义引用: ' + value)

    def binding(spec, reference, location):
        if reference in fields:
            expected = field_spec(fields[reference], location)
        elif reference in types:
            # A whole-type binding supplies records; cardinality belongs to the input declaration.
            expected = ValueSpec('Ref', target=reference, max_items=spec.max_items)
        else:
            fail('BINDING_UNDEFINED', location, '绑定必须指向已声明类型或字段: ' + reference)
            return
        if (spec.data_type != expected.data_type or spec.target != expected.target or set(spec.values) != set(expected.values) or spec.max_items != expected.max_items):
            fail('BINDING_TYPE_MISMATCH', location, '绑定字段与声明的类型、目标或基数不一致')

    def dag(items, location):
        graph = {i['id']: set(i['depends_on']) for i in items}
        for identifier, dependencies in graph.items():
            references(dependencies, graph, location + '/' + identifier + '/depends_on')
        pending, done = set(graph), set()
        while pending:
            ready = {i for i in pending if graph[i].issubset(done)}
            if not ready:
                # An unknown dependency is already a separate error; report actual cycles only.
                if all(graph[i].issubset(graph) for i in pending):
                    fail('DEPENDENCY_CYCLE', location, '依赖存在循环: ' + ', '.join(sorted(pending)))
                break
            done.update(ready)
            pending.difference_update(ready)

    dag(model['rules'], '/rules')
    for rule in model['rules']:
        loc = '/rules/' + rule['id']
        references(rule['question_ids'], scope, loc + '/question_ids')
        if not rule['question_ids']:
            fail('RULE_QUESTION_REQUIRED', loc, '规则必须关联至少一个范围内业务问题')
        input_bindings = {i['binding'] for i in rule['inputs']}
        try:
            for declaration in rule['inputs']:
                binding(declaration_spec(declaration, loc), declaration['binding'], loc + '/inputs/' + declaration['name'])
            if rule['result_binding'] not in fields:
                fail('RESULT_FIELD_REQUIRED', loc, '规则结果必须绑定具体字段')
            else:
                binding(declaration_spec(rule['result'], loc), rule['result_binding'], loc + '/result_binding')
        except DSLExpressionError as exc:
            fail(exc.code, exc.location, exc.message)
        for dependency in rule['depends_on']:
            predecessor = rules.get(dependency)
            if predecessor and predecessor['result_binding'] not in input_bindings:
                fail('DEPENDENCY_RESULT_UNUSED', loc, '前序规则结果必须作为显式输入绑定: ' + dependency)

    for judgment in model['judgments']:
        loc = '/judgments/' + judgment['id']
        try:
            for declaration in judgment['inputs'] + judgment['outputs']:
                binding(declaration_spec(declaration, loc), declaration['binding'], loc + '/' + declaration['name'])
        except DSLExpressionError as exc:
            fail(exc.code, exc.location, exc.message)
        references(judgment['record_fields'], fields, loc + '/record_fields')
        for output in judgment['outputs']:
            if output['binding'] not in judgment['record_fields']:
                fail('JUDGMENT_OUTPUT_UNRECORDED', loc, '人工判断输出必须列入结果记录字段')

    for constraint in model['constraints']:
        loc = '/constraints/' + constraint['id']
        references([constraint['type_id']], types, loc + '/type_id')
        try:
            spec = infer_expression(constraint['expression'], {'self': ValueSpec('Ref', target=constraint['type_id'])}, types, loc)
            if spec.data_type != 'Boolean' or spec.max_items != 1:
                fail('CONSTRAINT_BOOLEAN_REQUIRED', loc, '约束必须返回单值 Boolean')
        except DSLExpressionError as exc:
            fail(exc.code, exc.location, exc.message)

    usable = set(rules) | set(judgments) | set(machines) | set(constraints)
    for process in model['processes']:
        loc = '/processes/' + process['id']
        references(process['question_ids'], scope, loc + '/question_ids')
        dag(process['steps'], loc + '/steps')
        for step in process['steps']:
            sloc = loc + '/' + step['id']
            references(step['reads'], fields, sloc + '/reads')
            references(step['writes'], fields, sloc + '/writes')
            references(step['uses'], usable, sloc + '/uses')
            if step['kind'] in {'DETERMINE', 'VERIFY'} and not step['uses']:
                fail('PROCESS_DECISION_UNBOUND', sloc, '判断或核验步骤必须绑定规则、约束、状态迁移或人工判断')
            for identifier in step['uses']:
                if identifier in rules:
                    mechanism = rules[identifier]
                    needed = {i['binding'] for i in mechanism['inputs'] if i['binding'] in fields}
                    produced = {mechanism['result_binding']}
                elif identifier in judgments:
                    mechanism = judgments[identifier]
                    needed = {i['binding'] for i in mechanism['inputs'] if i['binding'] in fields}
                    produced = {i['binding'] for i in mechanism['outputs']}
                elif identifier in machines:
                    machine = machines[identifier]
                    needed = produced = {machine['type_id'] + '.' + machine['state_field']}
                else:
                    continue
                if not needed.issubset(step['reads']) or not produced.issubset(step['writes']):
                    fail('PROCESS_DATAFLOW_INCOMPLETE', sloc, '步骤未声明所用机制的全部输入字段或输出字段: ' + identifier)

    formal_conditions = {r['id'] + '.expression' for r in model['rules']}
    formal_conditions |= {c['id'] + '.expression' for c in model['constraints']}
    formal_conditions |= {t['id'] + '.guard' for m in model['state_machines'] for t in m['transitions']}
    manual_conditions = {j['id'] + '.criteria' for j in model['judgments']}
    covered_rules = set()
    for row in model['rule_coverage']:
        loc = '/rule_coverage/' + row['knowledge_rule_id']
        if row['knowledge_rule_id'] in covered_rules:
            fail('RULE_COVERAGE_DUPLICATE', loc, '知识规则只能覆盖一次')
        covered_rules.add(row['knowledge_rule_id'])
        references(row['question_ids'], scope, loc + '/question_ids')
        references(row['model_ids'], all_elements, loc + '/model_ids')
        references(row['gap_ids'], issues, loc + '/gap_ids')
        if (row['status'] == 'MODELED') != (not row['gap_ids']):
            fail('RULE_COVERAGE_STATUS_INVALID', loc, '完整建模与开放缺口状态不一致')
        for gap in row['gap_ids']:
            if gap in issues and (issues[gap]['status'] != 'OPEN' or issues[gap]['kind'] != 'MODEL_GAP'):
                fail('RULE_GAP_NOT_OPEN', loc, '规则缺口必须关联开放 MODEL_GAP')
        for facet_name, facet in row['facets'].items():
            floc = loc + '/facets/' + facet_name
            references(facet['model_refs'], refs, floc + '/model_refs')
            if facet['status'] == 'GAP' and not row['gap_ids']:
                fail('FACET_GAP_UNBOUND', floc, '缺口必须列入规则 gap_ids')
            if facet['status'] == 'MANUAL' and not set(facet['model_refs']) & (set(judgments) | manual_conditions):
                fail('FACET_MANUAL_UNBOUND', floc, '人工处理必须关联具体判断及其准则')
            if facet['status'] == 'MIXED' and (not set(facet['model_refs']) & formal_conditions or not set(facet['model_refs']) & manual_conditions):
                fail('FACET_MIXED_UNBOUND', floc, '混合条件必须同时关联表达式和人工准则')
            if facet_name == 'conditions' and facet['status'] == 'FORMALIZED' and not set(facet['model_refs']) & formal_conditions:
                fail('RULE_CONDITION_NOT_FORMALIZED', floc, '条件必须关联实际表达式或迁移守卫，不能只引用类型或说明')
            if facet_name == 'conditions' and facet['status'] == 'MANUAL' and not set(facet['model_refs']) & manual_conditions:
                fail('RULE_CONDITION_NOT_SPECIFIED', floc, '人工条件必须关联具体 criteria')
    for row in model['question_coverage']:
        loc = '/question_coverage/' + row['question_id']
        references(row['process_ids'], processes, loc + '/process_ids')
        references(row['rule_ids'], covered_rules, loc + '/rule_ids')
    for case in model['case_explanations']:
        loc = '/case_explanations/' + case['case_id']
        for step in case['steps']:
            references(step['model_ids'], all_elements, loc + '/steps')
        if (case['execution'] == 'NOT_EXECUTED') != (not case['evaluation_ids']):
            fail('CASE_EXECUTION_EVIDENCE_INVALID', loc, '执行或人工审查声明必须有证据标识，未执行不能携带执行证据')
    return errors
