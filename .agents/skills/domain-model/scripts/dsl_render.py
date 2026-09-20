"""Two deterministic views of the same DSL: business reading and technical audit."""
from dsl_expression import render_expression
from dsl_semantics import elements


STATUS = {'MODELED': '已建模', 'PARTIAL': '部分建模，有待解决事项', 'DEFERRED': '暂缓建模',
          'EXPLAINED': '已有模型解释', 'BLOCKED': '受未决事项影响',
          'NOT_EXECUTED': '尚未执行验证', 'LOCAL_EVALUATION': '已有本地求值记录',
          'MANUAL_REVIEW': '已有人工审查记录', 'OPEN': '待解决',
          'RESOLVED': '已解决', 'REJECTED': '未采纳',
          'MIXED': '计算与人工准则共同表达', 'FORMALIZED': '结构化表达', 'MANUAL': '明确的人工判断', 'GAP': '存在缺口'}
FACETS = {'scope': '适用范围', 'preconditions': '前提', 'conditions': '判断条件',
          'result': '结果', 'exceptions': '例外', 'missing_evidence': '缺证处理',
          'effective_period': '时间要求'}

TYPE_GROUPS = {
    'ENTITY': ('现实对象', '具有持续业务身份的人、组织或其他现实对象'),
    'ROLE': ('业务角色', '由现实对象在特定关系或时点承担的角色'),
    'FACT': ('关系与业务事实', '连接对象并承载比例、时间、状态或其他业务含义的事实'),
    'EVENT': ('业务事件', '推动状态或业务处理发生变化的事件'),
    'OBSERVATION': ('观察与外部结果', '来自查询、系统或材料的观察，尚不自动等于最终业务事实'),
    'EVIDENCE': ('业务证据', '支持身份、关系、时点或判断的证据'),
    'DECISION': ('判断与结果', '由规则或人工审查形成、具有明确适用范围的业务判断'),
    'TASK': ('任务与后续处理', '需要继续补证、复核或办理的工作事项'),
}


def type_group(kind):
    return TYPE_GROUPS.get(kind, ('其他业务对象', '需要结合业务定义理解的模型对象'))


def table(headers, rows):
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', '<br>')
    return ['| ' + ' | '.join(map(cell, headers)) + ' |',
            '| ' + ' | '.join('---' for _ in headers) + ' |'] + [
            '| ' + ' | '.join(map(cell, row)) + ' |' for row in rows]


def quantity(cardinality):
    lo, hi = cardinality['min'], cardinality['max']
    if lo == hi == 1:
        return '必须一项'
    if lo == 0 and hi == 1:
        return '可有一项；缺失时保留未知'
    return f'至少 {lo} 项' + ('，不限最多数量' if hi is None else f'，最多 {hi} 项')


def business_review(model):
    by_id = elements(model)
    labels = {identifier: item.get('name', item.get('statement', identifier)) for identifier, item in by_id.items()}
    fields = {t['id'] + '.' + f['name']: t['name'] + '的' + f['label']
              for t in model['types'] for f in t['fields']}
    labels.update(fields)

    def names(ids):
        return '、'.join(labels.get(i, i) for i in ids)

    def expression(expr, inputs=(), type_id=None):
        lookup = {i['name']: i['label'] for i in inputs}
        if type_id and type_id in by_id:
            lookup['self'] = by_id[type_id]['name']
            lookup.update((f['name'], f['label']) for f in by_id[type_id]['fields'])
        return render_expression(expr, lookup)

    grouped = {}
    for item in model['types']:
        grouped.setdefault(item['kind'], []).append(item)

    relation_rows = []
    for item in model['types']:
        for field in item['fields']:
            if field['type'] == 'Ref':
                relation_rows.append([
                    item['name'],
                    field['label'],
                    labels.get(field['target'], field['target']),
                    quantity(field['cardinality']),
                ])

    lines = [f"# {model['name']}：业务审阅稿", '',
             f"模型版本：{model['content_version']}；知识版本：{model['knowledge_ref']['content_version']}。", '',
             f"本稿覆盖 {len(model['question_coverage'])} 个业务问题、{len(model['rule_coverage'])} 条知识规则、{len(model['case_explanations'])} 个案例。", '',
             '本文与 model.yaml、覆盖表同源生成。model.yaml 是平台无关的规范化领域模型中间表示，不是另一套业务运行平台；本地求值仅用于有限行为验证。', '',
             '## 阅读与反馈', '',
             '建议先读“领域模型总览”，建立对象、关系、过程、判断和证据的整体结构；再进入具体对象、业务流程和逐项问题。', '',
             '请按业务问题、对象名称或案例标题提出意见：名称是否贴切、对象分类是否符合业务认知、关系是否遗漏、判断是否正确、例外是否完整、缺证时是否应停止。无需编辑技术标识。', '',
             '未知表示尚无充分依据，不能当作否定或零值。人工判断具有明确准则和责任；待定业务口径另列为未决事项。', '',
             '## 领域模型总览', '',
             '本节先回答“这个业务世界由什么构成、它们怎样连接”。类型分类用于帮助业务审阅，不等于数据库表、程序类或 ECP 平台资产分类。', '',
             '| 模型层次 | 业务含义 | 本模型中的对象 |',
             '| --- | --- | --- |']
    for kind, items in grouped.items():
        group_name, meaning = type_group(kind)
        lines.append('| ' + group_name + ' | ' + meaning + ' | ' + '、'.join(item['name'] for item in items) + ' |')
    lines += ['', '### 对象关系速览', '',
              '下面只展示模型中明确声明的对象引用关系，帮助建立整体结构；比例、时点、证据条件和判断逻辑仍以对象与规则正文为准。', '']
    if relation_rows:
        lines += table(['从什么对象', '通过什么关系/引用', '指向什么对象', '数量'], relation_rows)
    else:
        lines += ['本模型当前没有声明对象引用关系。']
    lines += ['', '### 业务过程速览', '']
    if model['processes']:
        lines += table(['业务过程', '何时启动', '主要回答的问题'], [
            [process['name'], process['trigger'], names(process['question_ids'])]
            for process in model['processes']
        ])
    else:
        lines += ['本模型当前没有声明业务过程。']
    lines += ['', '## 业务对象及其关系', '',
              '以下逐个解释对象为何存在、如何区分业务实例以及它与其他对象怎样连接。详细字段矩阵和规则原文对应保留在 coverage.md。', '']
    for item in model['types']:
        lines += [f"### {item['name']}", '', item['business_sentence'], '', item['description'], '',
                  '**为何单独建模：**' + item['why_object'], '',
                  '**如何区分实例：**' + item['identity_description'], '',
                  '**名称依据：**' + ('沿用领域知识中的业务用语。' if item['term_origin']=='KNOWLEDGE' else '建模建议用语，需评审其含义和可读性。'), '']
        rows = []
        for field in item['fields']:
            if field['name'] not in item['identity'] and field['type'] not in {'Ref','Date','DateTime'} and field['name'] != 'state':
                continue
            details = field['description']
            if field['type']=='Ref':
                details += '；关联' + labels[field['target']]
            elif field['type']=='Enum':
                vocabulary = field.get('value_labels', {})
                details += '；可选值：' + '、'.join(vocabulary.get(v, STATUS.get(v, v)) for v in field['values'])
            rows.append([field['label'], quantity(field['cardinality']), details])
        lines += table(['记录什么', '数量与缺失要求', '业务含义'], rows)
        lines += ['', '**例子：**' + '；'.join(item['examples']), '',
                  '**不能混同：**' + '；'.join(item['counterexamples']), '']
    lines += ['## 业务处理顺序', '']
    for process in model['processes']:
        lines += [f"### {process['name']}", '', '**启动条件：**' + process['trigger'], '']
        # Declaration order is presentation order; prerequisite names remain explicit.
        for index, step in enumerate(process['steps'], 1):
            lines += [f"{index}. **{step['name']}**：{step['description']}", '']
            if step['depends_on']:
                lines += ['   须先完成：' + names(step['depends_on']) + '。', '']
            if step['on_missing'] != 'BLOCK':
                lines += ['   登记缺口，继续不依赖该资料的工作。', '']
    lines += ['## 逐项业务问题', '']
    shown_rules, shown_judgments = set(), set()
    for row in model['question_coverage']:
        lines += ['### ' + row['question'], '', row['answer'], '',
                  '**建模情况：**' + STATUS[row['status']] + '。' + row['reason'], '']
        for rule in model['rules']:
            if row['question_id'] in rule['question_ids']:
                if rule['id'] in shown_rules:
                    lines += ['沿用前述判断：**' + rule['name'] + '**。', '']
                    continue
                shown_rules.add(rule['id'])
                lines += ['**' + rule['name'] + '：**' + rule['business_meaning'], '',
                          '采用事实：' + '、'.join(i['label'] for i in rule['inputs']) + '。', '',
                          '结果记录在：' + labels[rule['result_binding']] + '；缺失输入按未知值传播。', '']
        for judgment in model['judgments']:
            if row['question_id'] not in judgment['question_ids']:
                continue
            if judgment['id'] in shown_judgments:
                lines += ['沿用前述人工准则：**' + judgment['name'] + '**。', '']
                continue
            shown_judgments.add(judgment['id'])
            lines += ['**' + judgment['name'] + '**', '',
                      '责任：' + labels[judgment['responsible_role']] + '。', '']
            lines += ['- ' + criterion for criterion in judgment['criteria']]
            lines += ['', '所需证据：' + '；'.join(judgment['required_evidence']) + '。', '',
                      '复核要求：' + judgment['review_requirements'], '']
        if row['gap_ids']:
            lines += ['**待解决：**' + '；'.join(by_id[i]['statement'] for i in row['gap_ids']), '']
    lines += ['## 状态变化与历史', '']
    for machine in model['state_machines']:
        state_field = next(f for f in by_id[machine['type_id']]['fields'] if f['name']==machine['state_field'])
        state_names = state_field.get('value_labels', {})
        state = lambda x: state_names.get(x, STATUS.get(x, x))
        lines += ['### ' + machine['name'], '', '对象：' + labels[machine['type_id']] + '；初始状态：' + state(machine['initial']) + '。', '']
        lines += table(['变化', '原状态', '条件', '新状态'], [
            [t['name'], '、'.join(state(v) for v in t['from']), expression(t['guard'], type_id=machine['type_id']), state(t['to'])]
            for t in machine['transitions']])
        lines += ['', '条件为未知时暂停变化；本地求值只计算迁移建议，不保存真实业务状态。', '']
    for temporal in model['temporal']:
        lines += ['- ' + labels[temporal['type_id']] + '分别记录' + names([
            temporal['type_id'] + '.' + temporal[key] for key in ('start_field', 'end_field', 'end_status_field')]) + '。', '']
    lines += ['## 案例逐项审阅', '']
    for index, case in enumerate(model['case_explanations'], 1):
        lines += [f"### 案例 {index}：{case['title']}", '', '**已知情况：**', '']
        lines += ['- ' + fact for fact in case['input_facts']]
        lines += ['', '**模型如何处理：**', '']
        lines += [f"{i}. {step['explanation']}" for i, step in enumerate(case['steps'], 1)]
        lines += ['', '**应有结果：**' + case['expected'], '', '**不能出现的结果：**' + case['forbidden'], '',
                  '**当前证据：**' + STATUS[case['status']] + '；' + STATUS[case['execution']] + '。', '']
    lines += ['## 待决定事项', '']
    for issue in model['issues']:
        if issue['status']=='OPEN':
            lines += ['- **' + issue['statement'] + '** 责任：' + issue['owner'] + '；处理建议：' + issue['recommendation'] + '；解决前：' + issue['until_resolved'], '']
    lines += ['评审意见应注明本模型版本、评审范围与责任人。反馈落实到模型后产生新版本，重新核验受影响规则和案例；局部答复不自动成为全版批准。', '']
    return '\n'.join(lines)


def audit_coverage(model):
    lines = [f"# {model['name']}：覆盖与审计", '',
             f"模型 {model['artifact_id']} / {model['content_version']}；DSL {model['dsl_version']}；范围模式 {model['scope_mode']}。", '',
             '本表核对对应关系与实际证据，不以引用存在代替语义正确性。', '',
             '## 问题覆盖', '']
    lines += table(['问题', '状态', '规则', '流程', '案例', '模型', '缺口'], [
        [r['question_id'], r['status'], ', '.join(r['rule_ids']), ', '.join(r['process_ids']),
         ', '.join(r['case_ids']), ', '.join(r['model_ids']), ', '.join(r['gap_ids'])] for r in model['question_coverage']])
    lines += ['', '## 逐条规则要素', '']
    for row in model['rule_coverage']:
        lines += ['### ' + row['knowledge_rule_id'], '',
                  '状态：' + row['status'] + '；问题：' + ', '.join(row['question_ids']) + '；缺口：' + ', '.join(row['gap_ids']), '']
        lines += table(['要素', '知识原文', '模型引用', '表达方式', '对应解释'], [
            [FACETS[name], facet['source_text'], ', '.join(facet['model_refs']), facet['status'], facet['explanation']]
            for name, facet in row['facets'].items()])
        lines.append('')
    lines += ['## 模型目录与依据', '']
    lines += table(['标识', '名称', '依据'], [[identifier, item.get('name', item.get('statement', '')), ', '.join(item.get('basis_ids', []))]
                                          for identifier, item in elements(model).items()])
    lines += ['', '## 全部业务字段', '']
    for kind in model['types']:
        lines += ['### ' + kind['id'] + ' / ' + kind['name'], '']
        lines += table(['字段', '业务名称', '类型与目标', '基数', '含义'], [
            [field['name'], field['label'], field['type'] + (' → ' + field['target'] if field['type']=='Ref' else ''), quantity(field['cardinality']), field['description']]
            for field in kind['fields']])
        lines.append('')
    lines += ['', '## 字段绑定与依赖', '']
    for rule in model['rules']:
        lines += ['### ' + rule['id'] + ' / ' + rule['name'], '',
                  '前序规则：' + ', '.join(rule['depends_on']), '',
                  '输出字段：' + rule['result_binding'], '', '表达式：' + render_expression(rule['expression']), '']
        lines += table(['输入', '业务名称', '类型', '字段'], [[i['name'], i['label'], i['type'], i['binding']] for i in rule['inputs']])
        lines.append('')
    lines += ['## 案例对应', '']
    lines += table(['案例', '标题', '模型', '解释状态', '执行状态', '验证证据'], [
        [c['case_id'], c['title'], ', '.join(c['model_ids']), c['status'], c['execution'], ', '.join(c['evaluation_ids'])]
        for c in model['case_explanations']])
    lines += ['', '## 上游未决事项', '']
    lines += table(['知识事项', '模型事项', '处理', '说明'], [
        [b['knowledge_issue_id'], ', '.join(b['model_issue_ids']), b['handling'], b.get('reason', b.get('rationale', ''))]
        for b in model['upstream_issue_bindings']])
    lines += ['', '## 模型问题', '']
    lines += table(['标识', '状态', '问题', '影响', '责任', '解决前处理'], [
        [i['id'], i['status'], i['statement'], ', '.join(i['affects']), i['owner'], i['until_resolved']]
        for i in model['issues']])
    return '\n'.join(lines) + '\n'
