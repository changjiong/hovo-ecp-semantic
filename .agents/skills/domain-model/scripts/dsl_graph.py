"""Bounded, domain-neutral identity and acyclic path calculations for DSL2."""
from decimal import Decimal
import json


def identity_key(record, target, types, location, depth=0):
    from dsl_expression import DSLExpressionError
    if record is None:
        return None
    if depth > 16:
        raise DSLExpressionError('IDENTITY_DEPTH_EXCEEDED', location, '身份引用超过安全深度')
    definition = types[target]
    fields = {f['name']: f for f in definition['fields']}
    parts = []
    for name in definition['identity']:
        value = record.get(name)
        if value is None:
            return None
        field = fields[name]
        if field['type'] == 'Ref':
            value = identity_key(value, field['target'], types, location + '/' + name, depth + 1)
        elif isinstance(value, Decimal):
            value = format(value, "f")
            if "." in value:
                value = value.rstrip("0").rstrip(".")
            if Decimal(value) == 0:
                value = "0"
        parts.append([name, value])
    return json.dumps([target, parts], ensure_ascii=False, separators=(',', ':'))


def path_products(edges, source, target, start_field, end_field, weight_field, edge_type, types, location):
    """All path products in a supplied complete directed acyclic graph.

    Unknown records/weights or any cycle in the supplied graph return unknown.
    Caller must establish graph completeness and use a coherent effective-time slice.
    Duplicate edge identities with conflicting contents are errors, never extra paths.
    """
    from dsl_expression import DSLExpressionError, exact_decimal
    if edges is None or source is None or target is None or any(e is None for e in edges):
        return None
    if len(edges) > 10000:
        raise DSLExpressionError('GRAPH_LIMIT_EXCEEDED', location, '图边数超过10000，不能声称结果完整')
    adjacency, indegree, seen = {}, {}, {}
    for edge in edges:
        a, b, weight = edge.get(start_field), edge.get(end_field), edge.get(weight_field)
        if a is None or b is None or weight is None:
            return None
        key = identity_key(edge, edge_type, types, location)
        if key is None:
            return None
        if key in seen:
            if seen[key] != edge:
                raise DSLExpressionError('GRAPH_EDGE_IDENTITY_CONFLICT', location, '同一边身份存在冲突事实')
            continue
        seen[key] = edge
        adjacency.setdefault(a, []).append((b, Decimal(weight)))
        adjacency.setdefault(b, [])
        indegree.setdefault(a, 0)
        indegree[b] = indegree.get(b, 0) + 1
    queue = [node for node, degree in indegree.items() if degree == 0]
    visited = 0
    while queue:
        node = queue.pop()
        visited += 1
        for nxt, _ in adjacency[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    if visited != len(indegree):
        return None
    if source == target:
        # No implicit zero-edge ownership or dependency path.
        return []
    results, stack, traversed = [], [(source, Decimal('1'))], 0
    while stack:
        node, value = stack.pop()
        for nxt, weight in adjacency.get(node, []):
            traversed += 1
            if traversed > 100000:
                raise DSLExpressionError('GRAPH_LIMIT_EXCEEDED', location, '路径展开超过100000步，不能声称结果完整')
            product = exact_decimal(value, weight, "multiply", location)
            if nxt == target:
                results.append(product)
            else:
                stack.append((nxt, product))
    return results
