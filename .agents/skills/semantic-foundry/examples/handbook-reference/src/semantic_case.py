"""所有权语义教学切片：显式采信、事实视图及有限条件计算。

不是通用本体推理器，不是SHACL替代实现，也不是完整受益所有人识别引擎。
所有来源与采信均是随包合成数据；本模块没有网络请求和外部业务写入。
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef, XSD

ROOT = Path(__file__).resolve().parents[1]
H = Namespace('urn:hovo:semantic:')
X = Namespace('urn:hovo:demo:')


def bytes_digest(data: bytes) -> str:
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def instant(text: str) -> datetime:
    value = datetime.fromisoformat(text.replace('Z', '+00:00'))
    if value.tzinfo is None:
        raise ValueError('知识和采信时间必须带时区。')
    return value.astimezone(timezone.utc)


def exact_text(value: Fraction) -> str:
    """无舍入输出有限小数；非有限小数保留精确分数。"""
    n, d = value.numerator, value.denominator
    d0 = d
    twos = fives = 0
    while d % 2 == 0:
        twos += 1
        d //= 2
    while d % 5 == 0:
        fives += 1
        d //= 5
    if d != 1:
        return f'{n}/{d0}'
    places = max(twos, fives)
    scaled = abs(n) * 2 ** (places - twos) * 5 ** (places - fives)
    if places == 0:
        return str(n)
    digits = str(scaled).zfill(places + 1)
    text = (digits[:-places] + '.' + digits[-places:]).rstrip('0').rstrip('.')
    return ('-' if n < 0 else '') + text


def normalize_ratio(value: str, scale: str) -> Fraction:
    if not isinstance(value, str):
        raise ValueError('比例只接受十进制字符串，避免浮点隐式转换。')
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError('非法比例字符串。') from exc
    if not number.is_finite():
        raise ValueError('比例不能为非有限数。')
    if scale not in {'PERCENT', 'FRACTION'}:
        raise ValueError('未支持的比例尺度。')
    result = Fraction(number) / (100 if scale == 'PERCENT' else 1)
    if not 0 <= result <= 1:
        raise ValueError('归一化比例必须在0至1之间。')
    return result


def validate_raw(raw: dict[str, Any]) -> None:
    schema = json.loads((ROOT / 'spec/source.schema.json').read_text(encoding='utf8'))
    jsonschema.Draft202012Validator(schema).validate(raw)
    for name in ('subjects', 'records'):
        ids = [r['id'] for r in raw[name]]
        if len(ids) != len(set(ids)):
            raise ValueError(f'{name}中标识重复；不能重复导入形成不同事实。')


def map_raw(raw: dict[str, Any]) -> Graph:
    """映射到断言图，不把原始断言提升为全局持股事实。"""
    validate_raw(raw)
    g = Graph(identifier=URIRef('urn:hovo:graph:raw-assertions'))
    g.bind('h', H)
    g.bind('ex', X)
    for s in raw['subjects']:
        node = X[s['id']]
        g.add((node, RDF.type, H[s['kind']]))
        g.add((node, RDF.type, H.Subject))
        g.add((node, RDFS.label, Literal(s['label'], lang='zh')))
    for r in raw['records']:
        a = X['assertion:' + r['id']]
        p = X['position:' + r['position']]
        g.add((a, RDF.type, H.Assertion))
        g.add((a, RDF.subject, p))
        g.add((a, RDF.predicate, H.shareRatio))
        g.add((a, H.aboutPosition, p))
        for field in ('value', 'scale', 'right', 'share_class', 'denominator',
                      'valid_from', 'valid_to', 'end_kind', 'known_at', 'source',
                      'origin', 'evidence_locator'):
            if r[field] is not None:
                g.add((a, H['raw_' + field], Literal(r[field])))
        if r['value'] is not None:
            # 原值与尺度已经保存在断言上；可归一化时才形成完整语句重述。
            try:
                value = normalize_ratio(r['value'], r['scale'])
            except ValueError:
                g.add((a, H.mappingStatus, Literal('INVALID_RATIO')))
            else:
                g.add((a, RDF.type, RDF.Statement))
                g.add((a, RDF.object, Literal(exact_text(value), datatype=XSD.decimal)))
        for field in ('holder', 'issuer'):
            if r[field] is not None:
                g.add((a, H['asserted_' + field], X[r[field]]))
        for old in r['supersedes']:
            g.add((a, H.supersedes, X['assertion:' + old]))
    return g


def build_view(raw: dict[str, Any], selection: dict[str, Any],
               business_date: str, cutoff: str) -> dict[str, Any]:
    validate_raw(raw)
    when, until = date.fromisoformat(business_date), instant(cutoff)
    by_id = {r['id']: r for r in raw['records']}
    subject_types = {s['id']: s['kind'] for s in raw['subjects']}
    if selection.get('synthetic') is not True:
        raise ValueError('此教学入口仅接受明确合成采信输入。')
    entries = selection['accepted_assertions']
    accepted_ids = [e['assertion_id'] for e in entries]
    if len(set(accepted_ids)) != len(accepted_ids):
        raise ValueError('采信记录重复。')
    if set(accepted_ids) & set(selection.get('excluded_assertions', [])):
        raise ValueError('同一断言不能同时明确选入和排除。')
    issues: list[dict[str, Any]] = []
    ignored: list[dict[str, str]] = []

    def issue(r: dict[str, Any], code: str, detail: str = '') -> None:
        issues.append({'code': code, 'position': r['position'],
                       'issuer': r['issuer'], 'assertion_id': r['id'], 'detail': detail})

    active: list[dict[str, Any]] = []
    for e in entries:
        rid = e['assertion_id']
        if rid not in by_id:
            raise ValueError(f'采信引用不存在的来源断言：{rid}')
        r = by_id[rid]
        if instant(e['accepted_at']) < instant(r['known_at']):
            raise ValueError('采信时间不能早于本系统获知来源的时间。')
        if instant(r['known_at']) > until or instant(e['accepted_at']) > until:
            ignored.append({'assertion_id': rid, 'reason': 'NOT_KNOWN_OR_ACCEPTED_AT_CUTOFF'})
            continue
        if r['right'] != 'OWNERSHIP':
            ignored.append({'assertion_id': rid, 'reason': 'OTHER_RIGHT_NOT_IN_OWNERSHIP_BRANCH'})
            continue
        if r['valid_from'] is None or r['end_kind'] == 'UNKNOWN':
            issue(r, 'UNKNOWN_VALIDITY')
            continue
        try:
            start = date.fromisoformat(r['valid_from'])
            if r['end_kind'] == 'FINITE':
                if r['valid_to'] is None:
                    issue(r, 'UNKNOWN_VALIDITY')
                    continue
                end = date.fromisoformat(r['valid_to'])
                if start >= end:
                    issue(r, 'INVALID_INTERVAL')
                    continue
            else:
                if r['valid_to'] is not None:
                    issue(r, 'OPEN_END_CONTRADICTION')
                    continue
                end = None
        except (ValueError, TypeError):
            issue(r, 'INVALID_TIME')
            continue
        if when < start or (end is not None and when >= end):
            ignored.append({'assertion_id': rid, 'reason': 'OUTSIDE_VALID_INTERVAL'})
            continue
        active.append(r)

    # 只有已知、已采信且本业务时点适用的明确更正，才替代相同位置的旧陈述。
    suppressed: set[str] = set()
    for r in active:
        for old_id in r['supersedes']:
            old = by_id.get(old_id)
            if old is None or old['position'] != r['position'] or old_id == r['id']:
                issue(r, 'INVALID_REPLACEMENT', old_id)
                continue
            if any(old[k] != r[k] for k in ('holder','issuer','right','share_class','denominator')):
                issue(r, 'INVALID_REPLACEMENT_IDENTITY', old_id)
                continue
            if instant(old['known_at']) >= instant(r['known_at']):
                issue(r, 'INVALID_REPLACEMENT_ORDER', old_id)
                continue
            suppressed.add(old_id)
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in active:
        if r['id'] not in suppressed:
            groups[r['position']].append(r)
    facts: list[dict[str, Any]] = []
    identity_fields = ('holder', 'issuer', 'right', 'share_class', 'denominator')
    for position, rows in sorted(groups.items()):
        r = rows[0]
        if len({tuple(x[k] for k in identity_fields) for x in rows}) != 1:
            for x in rows:
                issue(x, 'POSITION_IDENTITY_CONFLICT')
            continue
        if r['holder'] not in subject_types or subject_types.get(r['issuer']) != 'Organization':
            issue(r, 'UNRESOLVED_SUBJECT')
            continue
        if r['share_class'] != 'ORDINARY' or r['denominator'] != 'TOTAL_OUTSTANDING_EQUITY':
            issue(r, 'UNSUPPORTED_MEASUREMENT_BASIS')
            continue
        values: list[Fraction] = []
        unusable = False
        for x in rows:
            if x['value'] is None:
                issue(x, 'MISSING_RATIO')
                unusable = True
                continue
            try:
                values.append(normalize_ratio(x['value'], x['scale']))
            except ValueError as exc:
                issue(x, 'INVALID_RATIO', str(exc))
                unusable = True
        if unusable:
            continue
        if len(set(values)) != 1:
            issue(r, 'VALUE_CONFLICT', ','.join(exact_text(v) for v in values))
            continue
        facts.append({'position': position, **{k: r[k] for k in identity_fields},
                      'ratio': exact_text(values[0]),
                      'assertion_ids': sorted(x['id'] for x in rows),
                      'origins': sorted({x['origin'] for x in rows})})
    return {'business_date': business_date, 'knowledge_cutoff': cutoff,
            'selection_id': selection['id'], 'facts': facts, 'issues': issues,
            'suppressed_assertions': sorted(suppressed), 'ignored': ignored,
            'scope': 'ordinary-ownership-only', 'synthetic': True}


def facts_graph(view: dict[str, Any], raw: dict[str, Any]) -> Graph:
    g = Graph(identifier=URIRef('urn:hovo:graph:fact-view'))
    g.bind('h', H)
    g.bind('ex', X)
    for s in raw['subjects']:
        g.add((X[s['id']], RDF.type, H[s['kind']]))
        g.add((X[s['id']], RDF.type, H.Subject))
        g.add((X[s['id']], RDFS.label, Literal(s['label'], lang='zh')))
    for f in view['facts']:
        p = X['position:' + f['position']]
        g.add((p, RDF.type, H.OwnershipPosition))
        g.add((p, H.holder, X[f['holder']]))
        g.add((p, H.issuer, X[f['issuer']]))
        g.add((p, H.shareRatio, Literal(f['ratio'], datatype=XSD.decimal)))
        for field in ('right', 'share_class', 'denominator'):
            g.add((p, H[field], Literal(f[field])))
        for a in f['assertion_ids']:
            g.add((p, H.supportedBy, X['assertion:' + a]))
    task = X['view:current']
    g.add((task, RDF.type, H.FactView))
    g.add((task, H.businessDate, Literal(view['business_date'], datatype=XSD.date)))
    g.add((task, H.knowledgeCutoff, Literal(view['knowledge_cutoff'], datatype=XSD.dateTime)))
    g.add((task, H.selectionId, Literal(view['selection_id'])))
    return g


def compute_ownership(view: dict[str, Any], raw: dict[str, Any], coverage: dict[str, Any],
                      target: str, threshold: str) -> dict[str, Any]:
    """显式主体标识下的普通股无环比例传递；不是完整监管规则。"""
    kinds = {s['id']: s['kind'] for s in raw['subjects']}
    if kinds.get(target) != 'Organization':
        raise ValueError('目标必须是输入中明确存在的组织。')
    limit = normalize_ratio(threshold, 'FRACTION')
    incoming: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for f in view['facts']:
        incoming[f['issuer']].append(f)
    totals: dict[str, Fraction] = defaultdict(Fraction)
    paths: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    visited: set[str] = set()
    known = instant(view['knowledge_cutoff'])
    business = date.fromisoformat(view['business_date'])
    coverage_valid = (coverage.get('synthetic') is True
        and coverage.get('dimension') == 'ORDINARY_OWNERSHIP_ONLY'
        and instant(coverage['known_at']) <= known
        and date.fromisoformat(coverage['valid_from']) <= business < date.fromisoformat(coverage['valid_to']))
    visits = 0

    def walk(org: str, weight: Fraction, stack: tuple[str, ...], edge_path: list[str]) -> None:
        nonlocal visits
        visits += 1
        if visits > 10000 or len(stack) > 32:
            issues.append({'code': 'PATH_BUDGET_EXCEEDED', 'issuer': org})
            return
        if org in stack:
            issues.append({'code': 'UNSUPPORTED_CYCLE', 'issuer': org, 'path': list(stack) + [org]})
            return
        visited.add(org)
        edges = incoming.get(org, [])
        if not coverage_valid or org not in coverage['complete_for']:
            issues.append({'code': 'NO_COVERAGE_DECLARATION', 'issuer': org})
        total = sum((Fraction(e['ratio']) for e in edges), Fraction())
        if total != 1:
            issues.append({'code': 'INCOMPLETE_EQUITY_SUM', 'issuer': org, 'sum': exact_text(total)})
        if not edges:
            issues.append({'code': 'UNRESOLVED_ORGANIZATION', 'issuer': org})
        for e in edges:
            share = weight * Fraction(e['ratio'])
            path = edge_path + [e['position']]
            if kinds.get(e['holder']) == 'NaturalPerson':
                totals[e['holder']] += share
                paths.append({'person': e['holder'], 'positions': list(reversed(path)),
                              'ratio': exact_text(share)})
            elif kinds.get(e['holder']) == 'Organization':
                walk(e['holder'], share, stack + (org,), path)
            else:
                issues.append({'code': 'UNRESOLVED_SUBJECT', 'issuer': org})

    walk(target, Fraction(1), (), [])
    # 不相关公司中的缺失不阻塞目标；根目标和已到达上游的缺失仍需披露。
    issues.extend(i for i in view['issues'] if i.get('issuer') is None or i.get('issuer') in visited)
    unique = {json.dumps(i, sort_keys=True, ensure_ascii=False): i for i in issues}
    issues = list(unique.values())
    complete = not issues
    threshold_matches = sorted(p for p, value in totals.items() if value >= limit) if complete else []
    return {'target': target, 'totals': {p: exact_text(v) for p, v in sorted(totals.items())},
            'paths': sorted(paths, key=lambda p: (p['person'], p['positions'])),
            'complete': complete, 'completeness_dimension': 'ORDINARY_OWNERSHIP_ONLY',
            'measurement_status': 'complete_within_declared_scope' if complete else 'partial_known_paths',
            'threshold_matches': threshold_matches, 'threshold': threshold,
            'issues': issues, 'full_ubo_assessment': False, 'automatic_fallback': False,
            'business_approval': 'NOT_PERFORMED', 'result_kind': 'OWNERSHIP_THRESHOLD_DEMO'}


def graph_contract(g: Graph, expected_positions: list[URIRef],
                   target_class: URIRef = H.OwnershipPosition) -> dict[str, Any]:
    """显式应用合同检查，不解释SHACL文件，不冒充标准验证器。"""
    actual = set(g.subjects(RDF.type, target_class))
    expected = set(expected_positions)
    violations = []
    for p in sorted(actual):
        for prop, code in ((H.holder, 'MISSING_HOLDER'), (H.issuer, 'MISSING_ISSUER'),
                           (H.shareRatio, 'MISSING_RATIO')):
            if not list(g.objects(p, prop)):
                violations.append({'position': str(p), 'code': code})
    return {'check_kind': 'EXPLICIT_APP_CONTRACT_NOT_SHACL',
            'expected_targets': len(expected), 'actual_targets': len(actual),
            'coverage_pass': actual == expected,
            'missing_targets': sorted(map(str, expected - actual)),
            'unexpected_targets': sorted(map(str, actual - expected)),
            'violations': violations,
            'pass': actual == expected and not violations}


def validate_result_record(kind: str, subject_kind: str) -> list[str]:
    """校验本样板声明的结果记录主体范围，不判断该认定是否成立。"""
    if kind not in {'ActualControllerDetermination', 'BeneficialOwnerDetermination'}:
        return ['UNSUPPORTED_RESULT_KIND']
    if kind == 'BeneficialOwnerDetermination' and subject_kind != 'NaturalPerson':
        return ['NATURAL_PERSON_REQUIRED']
    if subject_kind not in {'NaturalPerson', 'Organization'}:
        return ['UNSUPPORTED_SUBJECT_KIND']
    return []
