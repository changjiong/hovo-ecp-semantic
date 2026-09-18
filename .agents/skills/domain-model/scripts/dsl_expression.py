"""Closed, deterministic expression interpreter for domain-model DSL 2."""
from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, localcontext, Inexact, Rounded
import json
import re
from typing import Any, Mapping


UNKNOWN = None
SCALAR_TYPES = frozenset({"Text", "Boolean", "Integer", "Decimal", "Date", "DateTime"})
FIELD_TYPES = frozenset((*SCALAR_TYPES, "Enum", "Ref", "IntervalSet"))
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
MAX_EXPRESSION_DEPTH = 64
MAX_REF_DEPTH = 16


class DSLExpressionError(ValueError):
    def __init__(self, code: str, location: str, message: str) -> None:
        super().__init__(message)
        self.code, self.location, self.message = code, location, message


@dataclass(frozen=True)
class ValueSpec:
    data_type: str
    target: str | None = None
    values: tuple[str, ...] = ()
    max_items: int | None = 1
    min_items: int = 0

    @property
    def is_collection(self) -> bool:
        return self.max_items is None or self.max_items > 1

    def item(self) -> "ValueSpec":
        return ValueSpec(self.data_type, self.target, self.values, 1, 0)

    def collection(self) -> "ValueSpec":
        return ValueSpec(self.data_type, self.target, self.values, None, 0)


def _fail(code: str, location: str, message: str) -> None:
    raise DSLExpressionError(code, location, message)


def _keys(value: Any, allowed: set[str], location: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        _fail("EXPR_OBJECT_REQUIRED", location, "表达式必须是对象")
    if set(value) != allowed:
        _fail("EXPR_SHAPE_INVALID", location, f"表达式字段必须且只能是 {sorted(allowed)}")
    return value


def _cardinality(value: Mapping[str, Any], location: str) -> tuple[int, int | None]:
    raw = value.get("cardinality")
    if raw is None:
        return 0, 1
    if not isinstance(raw, dict) or set(raw) != {"min", "max"}:
        _fail("CARDINALITY_INVALID", location + "/cardinality", "cardinality 必须含 min 和 max")
    minimum, maximum = raw["min"], raw["max"]
    if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 0:
        _fail("CARDINALITY_INVALID", location + "/cardinality/min", "min 必须是非负整数")
    if maximum is not None and (
        not isinstance(maximum, int) or isinstance(maximum, bool) or maximum < 1 or minimum > maximum
    ):
        _fail("CARDINALITY_INVALID", location + "/cardinality/max", "max 必须是不小于 min 的正整数或 null")
    return minimum, maximum


def declaration_spec(declaration: Mapping[str, Any], location: str) -> ValueSpec:
    """Return the runtime type from a field, input, or result declaration."""
    if not isinstance(declaration, Mapping):
        _fail("DECLARATION_INVALID", location, "输入、输出或字段声明必须是对象")
    data_type = declaration.get("type")
    if data_type not in FIELD_TYPES:
        _fail("TYPE_INVALID", location + "/type", "不支持的 DSL 类型")
    target, values = declaration.get("target"), declaration.get("values")
    if data_type == "Ref":
        if not isinstance(target, str) or not target:
            _fail("REF_TARGET_REQUIRED", location + "/target", "Ref 必须声明 target")
    elif target is not None:
        _fail("TYPE_TARGET_INVALID", location + "/target", "只有 Ref 可以声明 target")
    if data_type == "Enum":
        if not isinstance(values, list) or not values or not all(isinstance(x, str) and x for x in values):
            _fail("ENUM_VALUES_REQUIRED", location + "/values", "Enum 必须声明非空文本 values")
        if len(values) != len(set(values)):
            _fail("ENUM_VALUES_DUPLICATE", location + "/values", "Enum values 不能重复")
    elif values is not None:
        _fail("TYPE_VALUES_INVALID", location + "/values", "只有 Enum 可以声明 values")
    minimum, maximum = _cardinality(declaration, location)
    if data_type == "IntervalSet" and maximum != 1:
        _fail("INTERVAL_SET_CARDINALITY_INVALID", location + "/cardinality", "IntervalSet 是单个区间集合，不能再声明为多值")
    return ValueSpec(data_type, target, tuple(values or ()), maximum, minimum)


def field_spec(field: Mapping[str, Any], location: str) -> ValueSpec:
    if "cardinality" not in field:
        _fail("CARDINALITY_REQUIRED", location + "/cardinality", "字段必须声明 cardinality")
    return declaration_spec(field, location)


def _decimal(value: Any, location: str) -> Decimal:
    if isinstance(value, bool):
        _fail("DECIMAL_INVALID", location, "Boolean 不能作为 Decimal")
    try:
        parsed = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError):
        _fail("DECIMAL_INVALID", location, "不是有效十进制数")
    if not parsed.is_finite():
        _fail("DECIMAL_NONFINITE", location, "Decimal 不得为 NaN 或无穷")
    if len(parsed.as_tuple().digits) + abs(parsed.as_tuple().exponent) > 10000:
        _fail("DECIMAL_LIMIT_EXCEEDED", location, "十进制精度或指数超过10000，拒绝近似计算")
    return parsed


def exact_decimal(left: Decimal, right: Decimal, operation: str, location: str) -> Decimal:
    """Bounded exact addition/multiplication; never silently round a threshold."""
    left, right = _decimal(left, location), _decimal(right, location)
    a, b = left.as_tuple(), right.as_tuple()
    if operation == "multiply":
        precision = len(a.digits) + len(b.digits)
        exponent = a.exponent + b.exponent
    else:
        exponent = min(a.exponent, b.exponent)
        precision = max(len(a.digits) + a.exponent, len(b.digits) + b.exponent) - exponent + 1
    if precision + abs(exponent) > 10000:
        _fail("DECIMAL_LIMIT_EXCEEDED", location, "精确计算超过10000位，拒绝舍入结果")
    with localcontext() as context:
        context.prec = max(precision, 1)
        context.traps[Inexact] = True
        context.traps[Rounded] = True
        return left * right if operation == "multiply" else left + right


def _date(value: Any, location: str) -> str:
    if not isinstance(value, str):
        _fail("DATE_INVALID", location, "Date 必须是 YYYY-MM-DD")
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        _fail("DATE_INVALID", location, "Date 必须是 YYYY-MM-DD")
    if parsed.isoformat() != value:
        _fail("DATE_INVALID", location, "Date 必须是 YYYY-MM-DD")
    return value


def _datetime(value: Any, location: str) -> str:
    if not isinstance(value, str) or "T" not in value:
        _fail("DATETIME_INVALID", location, "DateTime 必须是带时区的 ISO 日期时间")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        _fail("DATETIME_INVALID", location, "DateTime 必须是带时区的 ISO 日期时间")
    if parsed.tzinfo is None:
        _fail("DATETIME_INVALID", location, "DateTime 必须带时区")
    return parsed.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _single_value(value: Any, spec: ValueSpec, types: Mapping[str, Mapping[str, Any]], location: str, depth: int) -> Any:
    if value is UNKNOWN:
        return UNKNOWN
    if spec.data_type == "Text":
        if not isinstance(value, str):
            _fail("RUNTIME_TYPE_INVALID", location, "期望 Text")
        return value
    if spec.data_type == "Boolean":
        if not isinstance(value, bool):
            _fail("RUNTIME_TYPE_INVALID", location, "期望 Boolean")
        return value
    if spec.data_type == "Integer":
        if not isinstance(value, int) or isinstance(value, bool):
            _fail("RUNTIME_TYPE_INVALID", location, "期望 Integer")
        return value
    if spec.data_type == "Decimal":
        return _decimal(value, location)
    if spec.data_type == "Date":
        return _date(value, location)
    if spec.data_type == "DateTime":
        return _datetime(value, location)
    if spec.data_type == "Enum":
        if not isinstance(value, str) or value not in spec.values:
            _fail("RUNTIME_ENUM_INVALID", location, "枚举值不在声明范围内")
        return value
    if spec.data_type == "Ref":
        return validate_ref(value, spec, types, location, depth + 1)
    if spec.data_type == "IntervalSet":
        return validate_interval_set(value, location)
    _fail("RUNTIME_TYPE_INVALID", location, "未知 DSL 类型")


def validate_field_value(
    value: Any,
    spec: ValueSpec,
    types: Mapping[str, Mapping[str, Any]],
    location: str,
    minimum: int | None = None,
    depth: int = 0,
) -> Any:
    """Validate and canonicalize a scalar, collection, Ref, or IntervalSet."""
    if depth > MAX_REF_DEPTH:
        _fail("REF_DEPTH_EXCEEDED", location, "Ref 嵌套超过安全深度")
    required = spec.min_items if minimum is None else minimum
    if spec.is_collection:
        if value is UNKNOWN:
            if required:
                _fail("RUNTIME_REQUIRED_VALUE_MISSING", location, "必填多值字段不能为未知")
            return UNKNOWN
        if not isinstance(value, list):
            _fail("RUNTIME_CARDINALITY_INVALID", location, "多值字段必须是数组")
        if len(value) < required or (spec.max_items is not None and len(value) > spec.max_items):
            _fail("RUNTIME_CARDINALITY_INVALID", location, "字段值数量不符合 cardinality")
        return [_single_value(item, spec.item(), types, f"{location}/{index}", depth) for index, item in enumerate(value)]
    if isinstance(value, list) and spec.data_type != "IntervalSet":
        _fail("RUNTIME_CARDINALITY_INVALID", location, "单值字段不能使用数组")
    if value is UNKNOWN and required:
        _fail("RUNTIME_REQUIRED_VALUE_MISSING", location, "必填字段不能为未知")
    return _single_value(value, spec.item(), types, location, depth)


def validate_ref(value: Any, spec: ValueSpec, types: Mapping[str, Mapping[str, Any]], location: str, depth: int = 0) -> dict[str, Any] | None:
    if value is UNKNOWN:
        return UNKNOWN
    if not isinstance(value, dict):
        _fail("RUNTIME_REF_INVALID", location, "Ref 必须是对象或 UNKNOWN")
    if spec.target not in types:
        _fail("RUNTIME_REF_TARGET_INVALID", location, "Ref target 不存在")
    fields = {field["name"]: field for field in types[spec.target].get("fields", [])}
    extra = set(value) - set(fields)
    if extra:
        _fail("RUNTIME_REF_UNKNOWN_FIELD", location, f"Ref 含未声明字段: {sorted(extra)}")
    result: dict[str, Any] = {}
    for name, field in fields.items():
        if name not in value:
            if field["cardinality"]["min"] > 0:
                _fail("RUNTIME_REQUIRED_VALUE_MISSING", f"{location}/{name}", "缺少必需字段")
            continue
        result[name] = validate_field_value(
            value[name], field_spec(field, f"{location}/{name}"), types, f"{location}/{name}",
            minimum=field["cardinality"]["min"], depth=depth,
        )
    for name in types[spec.target].get("identity", []):
        if name not in result or result[name] is UNKNOWN:
            _fail("RUNTIME_REF_IDENTITY_MISSING", location, f"Ref 缺少身份字段: {name}")
    return result


def validate_interval_set(value: Any, location: str) -> list[dict[str, Any]] | None:
    if value is UNKNOWN:
        return UNKNOWN
    if not isinstance(value, list):
        _fail("INTERVAL_SET_INVALID", location, "IntervalSet 必须是区间数组或 UNKNOWN")
    result: list[dict[str, Any]] = []
    for index, interval in enumerate(value):
        here = f"{location}/{index}"
        if not isinstance(interval, dict) or set(interval) != {"start", "end", "end_status"}:
            _fail("INTERVAL_SHAPE_INVALID", here, "区间必须且只能有 start、end、end_status")
        start = _date(interval["start"], here + "/start")
        status, end = interval["end_status"], interval["end"]
        if status not in {"OPEN", "KNOWN", "UNKNOWN"}:
            _fail("INTERVAL_STATUS_INVALID", here + "/end_status", "end_status 必须为 OPEN、KNOWN 或 UNKNOWN")
        if status == "OPEN":
            if end is not None:
                _fail("INTERVAL_OPEN_END_INVALID", here + "/end", "OPEN 区间的 end 必须为 null")
        elif status == "KNOWN":
            end = _date(end, here + "/end")
            if date.fromisoformat(end) <= date.fromisoformat(start):
                _fail("INTERVAL_ORDER_INVALID", here, "KNOWN 区间必须满足 end 大于 start")
        elif end is not None:
            end = _date(end, here + "/end")
        result.append({"start": start, "end": end, "end_status": status})
    return result


def _compatible(left: ValueSpec, right: ValueSpec, *, cardinality: bool = False) -> bool:
    if cardinality and (left.max_items != right.max_items or left.min_items != right.min_items):
        return False
    if left.data_type == right.data_type:
        if left.data_type == "Ref":
            return left.target == right.target
        return left.data_type != "Enum" or left.values == right.values
    return {left.data_type, right.data_type} <= {"Integer", "Decimal"} or {left.data_type, right.data_type} <= {"Enum", "Text"}


def _joined(left: ValueSpec, right: ValueSpec, location: str, *, cardinality: bool = True) -> ValueSpec:
    if not _compatible(left, right, cardinality=cardinality):
        _fail("TYPE_INCOMPATIBLE", location, "分支或列表元素必须具有兼容类型和基数")
    if left.data_type == right.data_type:
        return left
    if {left.data_type, right.data_type} <= {"Integer", "Decimal"}:
        return ValueSpec("Decimal", max_items=left.max_items, min_items=left.min_items)
    return ValueSpec("Text", max_items=left.max_items, min_items=left.min_items)


def _single(spec: ValueSpec, location: str) -> None:
    if spec.is_collection:
        _fail("MULTI_VALUE_EXPRESSION_FORBIDDEN", location, "多值字段不能直接用于单值表达式")


def _numeric(spec: ValueSpec) -> bool:
    return not spec.is_collection and spec.data_type in {"Integer", "Decimal"}


def _literal_text(expr: Any, location: str) -> str:
    if (
        not isinstance(expr, dict) or set(expr) != {"literal"} or not isinstance(expr["literal"], dict)
        or set(expr["literal"]) != {"type", "value"} or expr["literal"].get("type") != "Text"
        or not isinstance(expr["literal"].get("value"), str) or not NAME_RE.fullmatch(expr["literal"]["value"])
    ):
        _fail("FIELD_LITERAL_REQUIRED", location, "字段名必须是符合 DSL 名称规则的 Text literal")
    return expr["literal"]["value"]


def _enum_literal(enum_spec: ValueSpec, expr: Any, location: str) -> None:
    if (
        enum_spec.data_type == "Enum" and isinstance(expr, dict) and set(expr) == {"literal"}
        and isinstance(expr["literal"], dict) and expr["literal"].get("type") == "Text"
        and expr["literal"].get("value") not in enum_spec.values
    ):
        _fail("ENUM_LITERAL_INVALID", location, "Text literal 不在可比较的 Enum values 中")


def infer_expression(expr: Any, environment: Mapping[str, ValueSpec], types: Mapping[str, Mapping[str, Any]], location: str = "/expression") -> ValueSpec:
    return _infer(expr, environment, types, location, 0)


def _infer(expr: Any, environment: Mapping[str, ValueSpec], types: Mapping[str, Mapping[str, Any]], location: str, depth: int) -> ValueSpec:
    if depth > MAX_EXPRESSION_DEPTH:
        _fail("EXPR_DEPTH_EXCEEDED", location, "表达式嵌套超过安全深度")
    if not isinstance(expr, dict):
        _fail("EXPR_SHAPE_INVALID", location, "表达式必须是对象")
    keys = set(expr)
    if keys == {"input"}:
        name = expr["input"]
        if not isinstance(name, str) or name not in environment:
            _fail("EXPR_INPUT_UNKNOWN", location + "/input", "表达式引用了未声明输入")
        return environment[name]
    if keys == {"literal"}:
        literal = _keys(expr["literal"], {"type", "value"}, location + "/literal")
        if literal["type"] not in SCALAR_TYPES:
            _fail("LITERAL_TYPE_INVALID", location + "/literal/type", "literal 只允许标量类型")
        spec = ValueSpec(literal["type"])
        _single_value(literal["value"], spec, types, location + "/literal/value", 0)
        return spec
    if keys == {"field"}:
        node = _keys(expr["field"], {"of", "name"}, location + "/field")
        source = _infer(node["of"], environment, types, location + "/field/of", depth + 1)
        if source.is_collection or source.data_type != "Ref" or not source.target:
            _fail("FIELD_ACCESS_INVALID", location + "/field/of", "field.of 必须是单值 Ref；集合须先用 query")
        if not isinstance(node["name"], str) or not NAME_RE.fullmatch(node["name"]):
            _fail("FIELD_NAME_INVALID", location + "/field/name", "field.name 必须是 DSL 名称")
        fields = {field["name"]: field for field in types.get(source.target, {}).get("fields", [])}
        if node["name"] not in fields:
            _fail("FIELD_UNKNOWN", location + "/field/name", "field.name 未在 Ref target 中声明")
        return field_spec(fields[node["name"]], location + "/field/name")
    if keys == {"query"}:
        node = _keys(expr["query"], {"from", "as", "where", "select"}, location + "/query")
        source = _infer(node["from"], environment, types, location + "/query/from", depth + 1)
        if not source.is_collection or source.data_type == "IntervalSet":
            _fail("QUERY_SOURCE_INVALID", location + "/query/from", "query.from 必须是非 IntervalSet 的多值表达式")
        alias = node["as"]
        if not isinstance(alias, str) or not NAME_RE.fullmatch(alias):
            _fail("QUERY_ALIAS_INVALID", location + "/query/as", "query.as 必须是 DSL 名称")
        if alias in environment:
            _fail("QUERY_ALIAS_SHADOW", location + "/query/as", "query.as 不能覆盖既有变量")
        local = dict(environment)
        local[alias] = source.item()
        where = _infer(node["where"], local, types, location + "/query/where", depth + 1)
        if where.is_collection or where.data_type != "Boolean":
            _fail("QUERY_WHERE_INVALID", location + "/query/where", "query.where 必须返回单值 Boolean")
        selected = _infer(node["select"], local, types, location + "/query/select", depth + 1)
        if selected.is_collection:
            _fail("QUERY_SELECT_COLLECTION", location + "/query/select", "query.select 不能返回嵌套集合")
        return selected.collection()
    if keys != {"op", "args"} or not isinstance(expr["op"], str) or not isinstance(expr["args"], list):
        _fail("EXPR_SHAPE_INVALID", location, "表达式必须是 input、literal、field、query，或含 op 和 args")
    op, args = expr["op"], expr["args"]
    specs = [_infer(arg, environment, types, f"{location}/args/{i}", depth + 1) for i, arg in enumerate(args)]
    if op == "identity_key":
        if len(specs) != 1 or specs[0].is_collection or specs[0].data_type != "Ref":
            _fail("OPERATOR_TYPE_INVALID", location, "identity_key需要单值Ref")
        return ValueSpec("Text")
    if op == "dag_path_products":
        if len(specs) != 6 or not specs[0].is_collection or specs[0].data_type != "Ref":
            _fail("OPERATOR_TYPE_INVALID", location, "dag_path_products需要边记录集合、起终节点及三个字段名")
        if any(v.is_collection or v.data_type != "Text" for v in specs[1:]):
            _fail("OPERATOR_TYPE_INVALID", location, "路径节点及字段名必须是单值Text")
        names = [_literal_text(args[i], f"{location}/args/{i}") for i in (3,4,5)]
        fields = {f['name']: f for f in types.get(specs[0].target, {}).get('fields', [])}
        for name, expected in zip(names, ['Text','Text','Decimal']):
            f = fields.get(name)
            if not f or f['type'] != expected or f['cardinality']['max'] != 1:
                _fail("GRAPH_FIELD_INVALID", location, "路径边必须具有单值Text起点、Text终点和Decimal权重")
        return ValueSpec("Decimal", max_items=None)
    if op == "is_known":
        if len(specs) != 1:
            _fail("OPERATOR_TYPE_INVALID", location, "is_known 需要一个表达式")
        return ValueSpec("Boolean")
    if op in {"and", "or"}:
        if len(specs) < 2 or any(s.is_collection or s.data_type != "Boolean" for s in specs):
            _fail("OPERATOR_TYPE_INVALID", location, f"{op} 需要至少两个单值 Boolean")
        return ValueSpec("Boolean")
    if op == "not":
        if len(specs) != 1 or specs[0].is_collection or specs[0].data_type != "Boolean":
            _fail("OPERATOR_TYPE_INVALID", location, "not 需要一个单值 Boolean")
        return ValueSpec("Boolean")
    if op == "if":
        if len(specs) != 3 or specs[0].is_collection or specs[0].data_type != "Boolean":
            _fail("OPERATOR_TYPE_INVALID", location, "if 需要 Boolean 条件和两个兼容分支")
        return _joined(specs[1], specs[2], location)
    if op in {"eq", "ne"}:
        if len(specs) != 2 or any(s.is_collection or s.data_type in {"Ref", "IntervalSet"} for s in specs) or not _compatible(specs[0], specs[1]):
            _fail("OPERATOR_TYPE_INVALID", location, f"{op} 需要两个兼容的可比较单值")
        _enum_literal(specs[0], args[1], f"{location}/args/1")
        _enum_literal(specs[1], args[0], f"{location}/args/0")
        return ValueSpec("Boolean")
    if op in {"lt", "lte", "gt", "gte"}:
        if len(specs) != 2 or any(s.is_collection for s in specs):
            _fail("OPERATOR_TYPE_INVALID", location, f"{op} 需要两个单值")
        valid = (_numeric(specs[0]) and _numeric(specs[1])) or (
            specs[0].data_type == specs[1].data_type and specs[0].data_type in {"Date", "DateTime"}
        )
        if not valid:
            _fail("OPERATOR_TYPE_INVALID", location, f"{op} 只支持数字、同类型 Date 或同类型 DateTime")
        return ValueSpec("Boolean")
    if op in {"add", "multiply"}:
        if len(specs) < 2 or any(not _numeric(s) for s in specs):
            _fail("OPERATOR_TYPE_INVALID", location, f"{op} 需要至少两个单值数字")
        return ValueSpec("Decimal")
    if op == "list":
        if not specs:
            return ValueSpec("Text", max_items=None)
        if any(s.is_collection or s.data_type == "IntervalSet" for s in specs):
            _fail("LIST_ELEMENT_INVALID", location, "list 只接受非集合、非 IntervalSet 元素")
        item = specs[0]
        for i, spec in enumerate(specs[1:], 1):
            item = _joined(item, spec, f"{location}/args/{i}", cardinality=False)
        return item.collection()
    if op in {"count", "sum", "product", "all", "any", "distinct"}:
        if len(specs) != 1 or not specs[0].is_collection:
            _fail("COLLECTION_REQUIRED", location, f"{op} 需要一个多值集合")
        item = specs[0].item()
        if op == "count":
            return ValueSpec("Integer")
        if op in {"sum", "product"}:
            if item.data_type not in {"Integer", "Decimal"}:
                _fail("OPERATOR_TYPE_INVALID", location, f"{op} 只接受数字集合")
            return ValueSpec("Decimal")
        if op in {"all", "any"}:
            if item.data_type != "Boolean":
                _fail("OPERATOR_TYPE_INVALID", location, f"{op} 只接受 Boolean 集合")
            return ValueSpec("Boolean")
        if item.data_type == "IntervalSet":
            _fail("OPERATOR_TYPE_INVALID", location, "distinct 不接受 IntervalSet")
        return specs[0]
    if op == "contains":
        if len(specs) != 2 or not specs[0].is_collection or specs[0].data_type in {"Ref", "IntervalSet"} or specs[1].is_collection or not _compatible(specs[0].item(), specs[1]):
            _fail("OPERATOR_TYPE_INVALID", location, "contains 需要一个可比较集合和一个兼容单值")
        _enum_literal(specs[0].item(), args[1], f"{location}/args/1")
        return ValueSpec("Boolean")
    if op in {"date_add_days", "date_add_months"}:
        if len(specs) != 2 or specs[0].is_collection or specs[1].is_collection or specs[0].data_type != "Date" or specs[1].data_type != "Integer":
            _fail("OPERATOR_TYPE_INVALID", location, f"{op} 需要 Date 和 Integer")
        return ValueSpec("Date")
    if op in {"date_year", "date_month"}:
        if len(specs) != 1 or specs[0].is_collection or specs[0].data_type != "Date":
            _fail("OPERATOR_TYPE_INVALID", location, f"{op} 需要 Date")
        return ValueSpec("Integer")
    if op == "intervals_of":
        if len(specs) != 4 or not specs[0].is_collection or specs[0].data_type != "Ref" or not specs[0].target:
            _fail("OPERATOR_TYPE_INVALID", location, "intervals_of 首项必须是 Ref 集合")
        names = [_literal_text(args[i], f"{location}/args/{i}") for i in range(1, 4)]
        fields = {field["name"]: field for field in types.get(specs[0].target, {}).get("fields", [])}
        start, end, status = (fields.get(name) for name in names)
        if start is None or end is None or status is None:
            _fail("INTERVAL_FIELDS_UNDEFINED", location, "intervals_of 指定的字段未定义")
        start_spec, end_spec, status_spec = (
            field_spec(start, f"{location}/args/1"),
            field_spec(end, f"{location}/args/2"),
            field_spec(status, f"{location}/args/3"),
        )
        if (
            start_spec.data_type != "Date" or end_spec.data_type != "Date" or status_spec.data_type != "Enum"
            or start_spec.is_collection or end_spec.is_collection or status_spec.is_collection
            or not {"OPEN", "KNOWN", "UNKNOWN"}.issubset(status_spec.values)
        ):
            _fail("INTERVAL_FIELDS_INVALID", location, "intervals_of 需要单值 Date、Date 和含 OPEN/KNOWN/UNKNOWN 的 Enum")
        return ValueSpec("IntervalSet")
    if op == "current_interval_start":
        expected = ("IntervalSet", "Date", "Boolean", "Boolean")
        if len(specs) != 4 or any(s.is_collection for s in specs) or tuple(s.data_type for s in specs) != expected:
            _fail("OPERATOR_TYPE_INVALID", location, "current_interval_start 参数必须为 IntervalSet、Date、Boolean、Boolean")
        return ValueSpec("Date")
    _fail("OPERATOR_UNKNOWN", location + "/op", "不支持的 operator")


def _evaluate(expr: Mapping[str, Any], env: Mapping[str, Any], specs: Mapping[str, ValueSpec], types: Mapping[str, Mapping[str, Any]], location: str, depth: int) -> Any:
    if depth > MAX_EXPRESSION_DEPTH:
        _fail("EXPR_DEPTH_EXCEEDED", location, "表达式嵌套超过安全深度")
    if set(expr) == {"input"}:
        return env.get(expr["input"], UNKNOWN)
    if set(expr) == {"literal"}:
        literal = expr["literal"]
        return _single_value(literal["value"], ValueSpec(literal["type"]), types, location + "/literal/value", 0)
    if set(expr) == {"field"}:
        node = expr["field"]
        source = _evaluate(node["of"], env, specs, types, location + "/field/of", depth + 1)
        return UNKNOWN if source is UNKNOWN else source.get(node["name"], UNKNOWN)
    if set(expr) == {"query"}:
        node = expr["query"]
        source = _evaluate(node["from"], env, specs, types, location + "/query/from", depth + 1)
        if source is UNKNOWN:
            return UNKNOWN
        source_spec = _infer(node["from"], specs, types, location + "/query/from", depth + 1)
        scoped_specs = dict(specs)
        scoped_specs[node["as"]] = source_spec.item()
        result: list[Any] = []
        for i, item in enumerate(source):
            scoped_env = dict(env)
            scoped_env[node["as"]] = item
            where = _evaluate(node["where"], scoped_env, scoped_specs, types, f"{location}/query/where/{i}", depth + 1)
            if where is UNKNOWN:
                return UNKNOWN
            if where is True:
                selected = _evaluate(node["select"], scoped_env, scoped_specs, types, f"{location}/query/select/{i}", depth + 1)
                if selected is UNKNOWN:
                    return UNKNOWN
                result.append(selected)
        return result
    op, args = expr["op"], expr["args"]
    if op == "if":
        condition = _evaluate(args[0], env, specs, types, f"{location}/args/0", depth + 1)
        if condition is UNKNOWN:
            return UNKNOWN
        branch = 1 if condition is True else 2
        return _evaluate(args[branch], env, specs, types, f"{location}/args/{branch}", depth + 1)
    if op == "list":
        return [_evaluate(arg, env, specs, types, f"{location}/args/{i}", depth + 1) for i, arg in enumerate(args)]
    values = [_evaluate(arg, env, specs, types, f"{location}/args/{i}", depth + 1) for i, arg in enumerate(args)]
    if op == "identity_key":
        from dsl_graph import identity_key
        spec = _infer(args[0], specs, types, location + "/args/0", depth + 1)
        return identity_key(values[0], spec.target, types, location)
    if op == "dag_path_products":
        from dsl_graph import path_products
        edge_spec = _infer(args[0], specs, types, location + "/args/0", depth + 1)
        return path_products(*values, edge_spec.target, types, location)
    if op == "is_known":
        return values[0] is not UNKNOWN
    if op == "and":
        return False if any(x is False for x in values) else (UNKNOWN if any(x is UNKNOWN for x in values) else True)
    if op == "or":
        return True if any(x is True for x in values) else (UNKNOWN if any(x is UNKNOWN for x in values) else False)
    if op == "not":
        return UNKNOWN if values[0] is UNKNOWN else not values[0]
    if op in {"eq", "ne", "lt", "lte", "gt", "gte"}:
        if any(x is UNKNOWN for x in values):
            return UNKNOWN
        left, right = values
        return {
            "eq": left == right, "ne": left != right, "lt": left < right, "lte": left <= right,
            "gt": left > right, "gte": left >= right,
        }[op]
    if op in {"add", "multiply"}:
        if any(x is UNKNOWN for x in values):
            return UNKNOWN
        total = Decimal("0") if op == "add" else Decimal("1")
        for value in values:
            total = exact_decimal(total, Decimal(value), op, location)
        return total
    if op == "count":
        return UNKNOWN if values[0] is UNKNOWN else len(values[0])
    if op in {"sum", "product"}:
        if values[0] is UNKNOWN or any(x is UNKNOWN for x in values[0]):
            return UNKNOWN
        total = Decimal("0") if op == "sum" else Decimal("1")
        for value in values[0]:
            total = exact_decimal(total, Decimal(value), "add" if op == "sum" else "multiply", location)
        return total
    if op == "all":
        if values[0] is UNKNOWN:
            return UNKNOWN
        return False if any(x is False for x in values[0]) else (UNKNOWN if any(x is UNKNOWN for x in values[0]) else True)
    if op == "any":
        if values[0] is UNKNOWN:
            return UNKNOWN
        return True if any(x is True for x in values[0]) else (UNKNOWN if any(x is UNKNOWN for x in values[0]) else False)
    if op == "contains":
        collection, wanted = values
        if collection is UNKNOWN or wanted is UNKNOWN:
            return UNKNOWN
        if any(x is not UNKNOWN and x == wanted for x in collection):
            return True
        return UNKNOWN if any(x is UNKNOWN for x in collection) else False
    if op == "distinct":
        spec = _infer(args[0], specs, types, f"{location}/args/0", depth + 1).item()
        return _distinct(values[0], spec, types, location)
    if op == "date_add_days":
        return UNKNOWN if any(x is UNKNOWN for x in values) else (date.fromisoformat(values[0]) + timedelta(days=values[1])).isoformat()
    if op == "date_add_months":
        if any(x is UNKNOWN for x in values):
            return UNKNOWN
        current = date.fromisoformat(values[0])
        index = current.month - 1 + values[1]
        year, month = current.year + index // 12, index % 12 + 1
        return date(year, month, min(current.day, calendar.monthrange(year, month)[1])).isoformat()
    if op == "date_year":
        return UNKNOWN if values[0] is UNKNOWN else date.fromisoformat(values[0]).year
    if op == "date_month":
        return UNKNOWN if values[0] is UNKNOWN else date.fromisoformat(values[0]).month
    if op == "intervals_of":
        return _intervals_of(values[0], args[1]["literal"]["value"], args[2]["literal"]["value"], args[3]["literal"]["value"], location)
    if op == "current_interval_start":
        return current_interval_start(values[0], values[1], values[2], values[3], location)
    _fail("OPERATOR_UNKNOWN", location + "/op", "不支持的 operator")


def evaluate_expression(expr: Any, environment: Mapping[str, Any], specs: Mapping[str, ValueSpec], types: Mapping[str, Mapping[str, Any]], location: str = "/expression") -> Any:
    """Evaluate one typed DSL expression.  UNKNOWN is an explicit valid result."""
    result_spec = infer_expression(expr, specs, types, location)
    extra = set(environment) - set(specs)
    if extra:
        _fail("RUNTIME_INPUT_UNKNOWN", location, f"输入含未声明变量: {sorted(extra)}")
    canonical = {
        name: validate_field_value(environment.get(name, UNKNOWN), spec, types, f"{location}/inputs/{name}")
        for name, spec in specs.items()
    }
    result = _evaluate(expr, canonical, specs, types, location, 0)
    return UNKNOWN if result is UNKNOWN else validate_field_value(result, result_spec, types, location + "/result")


def _identity_key(record: Mapping[str, Any], type_id: str, types: Mapping[str, Mapping[str, Any]], location: str, trail: tuple[str, ...] = ()) -> tuple[Any, ...]:
    if type_id in trail:
        _fail("DISTINCT_IDENTITY_CYCLE", location, "Ref 身份存在递归循环，不能安全去重")
    type_def = types.get(type_id)
    if type_def is None:
        _fail("DISTINCT_IDENTITY_TARGET_INVALID", location, "Ref target 不存在")
    fields = {field["name"]: field for field in type_def.get("fields", [])}
    key: list[Any] = [type_id]
    for name in type_def.get("identity", []):
        if name not in record or record[name] is UNKNOWN:
            _fail("DISTINCT_IDENTITY_MISSING", location, f"去重记录缺少身份字段: {name}")
        field = fields.get(name)
        if field is None:
            _fail("DISTINCT_IDENTITY_INVALID", location, f"身份字段未定义: {name}")
        spec, value = field_spec(field, f"{location}/{name}"), record[name]
        if spec.is_collection or spec.data_type == "IntervalSet":
            _fail("DISTINCT_IDENTITY_UNSUPPORTED", location, "多值或 IntervalSet 身份不能安全去重")
        if spec.data_type == "Ref":
            if not isinstance(value, Mapping) or not spec.target:
                _fail("DISTINCT_IDENTITY_INVALID", location, "Ref 身份值无效")
            key.append((name, _identity_key(value, spec.target, types, f"{location}/{name}", trail + (type_id,))))
        elif spec.data_type == "Decimal":
            key.append((name, "Decimal", format(value, "f")))
        else:
            key.append((name, spec.data_type, value))
    return tuple(key)


def _distinct(collection: Any, item_spec: ValueSpec, types: Mapping[str, Mapping[str, Any]], location: str) -> Any:
    if collection is UNKNOWN or any(item is UNKNOWN for item in collection):
        return UNKNOWN
    seen: dict[Any, Any] = {}
    result: list[Any] = []
    for index, item in enumerate(collection):
        here = f"{location}/args/0/{index}"
        if item_spec.data_type == "Ref":
            if not item_spec.target or not isinstance(item, Mapping):
                _fail("DISTINCT_REF_INVALID", here, "distinct 的 Ref 元素无效")
            key = _identity_key(item, item_spec.target, types, here)
        elif item_spec.data_type == "Decimal":
            key = ("Decimal", format(item, "f"))
        else:
            key = (item_spec.data_type, item)
        if key in seen:
            if seen[key] != item:
                _fail("DISTINCT_IDENTITY_CONFLICT", here, "同一身份的 Ref 含冲突字段，不能任意选择事实")
            continue
        seen[key] = item
        result.append(item)
    return result


def _intervals_of(collection: Any, start_name: str, end_name: str, status_name: str, location: str) -> Any:
    if collection is UNKNOWN:
        return UNKNOWN
    intervals: list[dict[str, Any]] = []
    for index, record in enumerate(collection):
        if record is UNKNOWN:
            return UNKNOWN
        start, end, status = record.get(start_name, UNKNOWN), record.get(end_name, UNKNOWN), record.get(status_name, UNKNOWN)
        if start is UNKNOWN or status is UNKNOWN or (status == "KNOWN" and end is UNKNOWN):
            return UNKNOWN
        intervals.append({"start": start, "end": end, "end_status": status})
    return validate_interval_set(intervals, location + "/intervals")


def current_interval_start(intervals: Any, as_of: Any, history_complete: Any, continuity_verified: Any, location: str) -> str | None:
    if intervals is UNKNOWN or as_of is UNKNOWN or history_complete is UNKNOWN or continuity_verified is UNKNOWN:
        return UNKNOWN
    if history_complete is not True or continuity_verified is not True:
        return UNKNOWN
    normalized = validate_interval_set(intervals, location + "/intervals")
    if normalized is UNKNOWN or not normalized or any(item["end_status"] == "UNKNOWN" for item in normalized):
        return UNKNOWN
    as_of_value = date.fromisoformat(_date(as_of, location + "/as_of"))
    merged: list[dict[str, Any]] = []
    for interval in sorted(normalized, key=lambda item: item["start"]):
        item = dict(interval)
        if not merged:
            merged.append(item)
            continue
        previous = merged[-1]
        if previous["end"] is None or date.fromisoformat(item["start"]) <= date.fromisoformat(previous["end"]):
            if previous["end"] is None or item["end"] is None:
                previous["end"], previous["end_status"] = None, "OPEN"
            elif date.fromisoformat(item["end"]) > date.fromisoformat(previous["end"]):
                previous["end"] = item["end"]
        else:
            merged.append(item)
    for interval in merged:
        if date.fromisoformat(interval["start"]) <= as_of_value and (
            interval["end"] is None or as_of_value < date.fromisoformat(interval["end"])
        ):
            return interval["start"]
    return UNKNOWN


def render_expression(expr: Any, labels: Mapping[str, str] | None = None) -> str:
    """Render the closed DSL expression as a compact Chinese explanation."""
    labels = labels or {}
    label = lambda value: labels.get(str(value), str(value))
    if not isinstance(expr, dict):
        return "无效表达式"
    if set(expr) == {"input"}:
        return label(expr["input"])
    if set(expr) == {"literal"}:
        return json.dumps(expr["literal"].get("value"), ensure_ascii=False, default=str)
    if set(expr) == {"field"}:
        node, name = expr["field"], expr["field"].get("name")
        return f"{render_expression(node.get('of'), labels)}.{labels.get(f'field.{name}', label(name))}"
    if set(expr) == {"query"}:
        node = expr["query"]
        return f"从 {render_expression(node.get('from'), labels)} 中逐项取 {label(node.get('as'))}，满足 {render_expression(node.get('where'), labels)}，得到 {render_expression(node.get('select'), labels)}"
    if set(expr) != {"op", "args"}:
        return "无效表达式"
    op, args = expr.get("op"), [render_expression(arg, labels) for arg in expr.get("args", [])]
    symbols = {"and": " 且 ", "or": " 或 ", "eq": " = ", "ne": " ≠ ", "lt": " < ", "lte": " ≤ ", "gt": " > ", "gte": " ≥ ", "add": " + ", "multiply": " × "}
    if op in symbols:
        return "(" + symbols[op].join(args) + ")"
    if op == "not":
        return "非(" + (args[0] if args else "？") + ")"
    if op == "if":
        return f"若 {args[0]}，则 {args[1]}，否则 {args[2]}" if len(args) == 3 else "条件表达式"
    names = {
        "identity_key": "业务身份键", "dag_path_products": "无环路径逐条连乘", "is_known": "已取得值", "list": "列表", "count": "数量", "sum": "求和", "product": "求积", "all": "全部为真",
        "any": "任一为真", "contains": "包含", "distinct": "去重", "date_add_days": "日期加天数",
        "date_add_months": "日期加月数", "date_year": "日期年份", "date_month": "日期月份",
        "intervals_of": "形成时间区间", "current_interval_start": "当前连续区间起点",
    }
    return names.get(str(op), str(op)) + "(" + "，".join(args) + ")"
