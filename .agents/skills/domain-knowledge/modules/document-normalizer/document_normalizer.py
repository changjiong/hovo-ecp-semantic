#!/usr/bin/env python3
"""Reconstruct semantic source units from MinerU structured_content blocks."""
from __future__ import annotations

import hashlib
import re
import unicodedata
from typing import Any, Callable

EXCLUDED_BLOCK_TYPES = {"header", "footer", "page_number"}
CHAPTER_RE = re.compile(r"^第[一二三四五六七八九十百零〇两\d]+章")
ARTICLE_RE = re.compile(r"^(第[一二三四五六七八九十百零〇两\d]+条)")
CLAUSE_RE = re.compile(r"^[（(]([一二三四五六七八九十百零〇两\d]+)[）)]")
ARTICLE_REFERENCE_RE = re.compile(r"第[一二三四五六七八九十百零〇两\d]+条")
TERMINAL_PUNCTUATION_RE = re.compile(r"[。！？；;.!?][”’」』）》】]*$")
AMBIGUOUS_TAIL_RE = re.compile(r"[：:][”’」』）》】]*$")
POTENTIAL_CHILD_RE = re.compile(r"^(?:\\d{1,3}[.、)]|[一二三四五六七八九十百]{1,3}[、.]|[①②③④⑤⑥⑦⑧⑨⑩])")
WEB_CHROME_PATTERNS = (
    re.compile(r"^<u>\s*打印本页.*关闭窗"),
    re.compile(r"^字号\s*[大中小 ]+$"),
    re.compile(r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$"),
)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_source_text(text: str) -> str:
    """Normalize CJK compatibility glyphs without rewriting punctuation."""
    out: list[str] = []
    for char in text:
        codepoint = ord(char)
        if (0x2E80 <= codepoint <= 0x2FDF) or (0xF900 <= codepoint <= 0xFAFF):
            out.append(unicodedata.normalize("NFKC", char))
        elif char == "\u00a0":
            out.append(" ")
        else:
            out.append(char)
    return "".join(out).strip()


def _block_text(block: dict[str, Any]) -> str:
    content = block.get("content")
    text = content if isinstance(content, str) else ""
    if block.get("type") == "image" and not text:
        pieces: list[str] = []
        for key in ("captions", "footnotes"):
            values = block.get(key) or []
            if isinstance(values, list):
                pieces.extend(
                    item for item in values
                    if isinstance(item, str) and item.strip()
                )
        text = "\n".join(pieces)
    return normalize_source_text(text)


def _is_web_chrome(text: str) -> bool:
    if any(pattern.search(text) for pattern in WEB_CHROME_PATTERNS):
        return True
    return "法律声明" in text and "网站主办单位" in text and "网站地图" in text


def _classify_semantic_hint(block_type: str, text: str) -> tuple[str, str]:
    if block_type == "table":
        return "TABLE", "表格"
    chapter = CHAPTER_RE.match(text)
    if chapter:
        return "SECTION", text[:80]
    article = ARTICLE_RE.match(text)
    if article:
        return "ARTICLE", article.group(1)
    clause = CLAUSE_RE.match(text)
    if clause:
        return "CLAUSE", f"（{clause.group(1)}）"
    if block_type == "paragraph_title":
        return "SECTION", text[:80]
    if block_type == "image":
        return "PAGE_BLOCK", "图片"
    return "PAGE_BLOCK", "正文块"


def _looks_incomplete(text: str) -> bool:
    return not TERMINAL_PUNCTUATION_RE.search(text.rstrip())


BoundaryRepair = Callable[[dict[str, Any]], dict[str, Any]]


def _needs_boundary_repair(
    previous_block: dict[str, Any],
    current_block: dict[str, Any],
) -> bool:
    if previous_block["block_type"] == "image" or current_block["block_type"] == "image":
        return False
    return bool(
        AMBIGUOUS_TAIL_RE.search(previous_block["text"].rstrip())
        or POTENTIAL_CHILD_RE.match(current_block["text"].lstrip())
    )


def _build_boundary_state(
    *,
    heading_path: list[str],
    previous_unit: dict[str, Any],
    previous_block: dict[str, Any],
    current_block: dict[str, Any],
    next_block: dict[str, Any] | None,
) -> dict[str, Any]:
    state: dict[str, Any] = {
        "heading_path": heading_path,
        "previous_unit": {
            "kind": previous_unit["kind"],
            "label": previous_unit["label"],
        },
        "previous_block": {
            "block_type": previous_block["block_type"],
            "page": previous_block["page"],
            "text": previous_block["text"],
        },
        "current_block": {
            "block_type": current_block["block_type"],
            "page": current_block["page"],
            "text": current_block["text"],
        },
    }
    if next_block is not None:
        state["next_block"] = {
            "block_type": next_block["block_type"],
            "page": next_block["page"],
            "text": next_block["text"],
        }
    return state


def _source_locator(block: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "BLOCK",
        "value": block["locator"],
        "page": block["page"],
        "block_id": block["parser_block_id"],
    }


def _build_source_blocks(
    source_id: str,
    structured: dict[str, Any],
) -> tuple[list[dict[str, Any]], int]:
    pages = structured.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("structured_content.pages 缺失或为空")

    validated_pages: list[dict[str, Any]] = []
    page_indices: set[int] = set()
    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("structured_content page 不是对象")
        page_idx = page.get("page_idx")
        blocks = page.get("blocks")
        if not isinstance(page_idx, int) or page_idx < 0 or not isinstance(blocks, list):
            raise ValueError("structured_content page 结构无效")
        if page_idx in page_indices:
            raise ValueError(f"structured_content 出现重复 page_idx: {page_idx}")
        page_indices.add(page_idx)
        validated_pages.append(page)

    source_blocks: list[dict[str, Any]] = []
    excluded_count = 0
    for page in sorted(validated_pages, key=lambda item: item["page_idx"]):
        physical_page = page["page_idx"] + 1
        for block_position, raw_block in enumerate(page["blocks"], start=1):
            if not isinstance(raw_block, dict):
                raise ValueError(
                    f"page {physical_page} block {block_position} 不是对象"
                )
            block_type = str(raw_block.get("type") or "other")
            if block_type in EXCLUDED_BLOCK_TYPES:
                excluded_count += 1
                continue
            text = _block_text(raw_block)
            if not text or _is_web_chrome(text):
                excluded_count += 1
                continue

            semantic_hint, _ = _classify_semantic_hint(block_type, text)
            sequence = len(source_blocks) + 1
            parser_block_id = f"p{physical_page}.b{block_position}"
            block: dict[str, Any] = {
                "block_id": f"{source_id}.B{sequence:05d}",
                "source_id": source_id,
                "block_type": block_type,
                "semantic_hint": semantic_hint,
                "page": physical_page,
                "page_block_index": block_position,
                "sequence": sequence,
                "parser_block_id": parser_block_id,
                "locator": f"第{physical_page}页 {parser_block_id}",
                "text": text,
                "digest": sha256_text(text),
            }
            bbox = raw_block.get("bbox")
            if (
                isinstance(bbox, list)
                and len(bbox) == 4
                and all(isinstance(value, (int, float)) for value in bbox)
            ):
                block["bbox"] = bbox
            source_blocks.append(block)
    if not source_blocks:
        raise ValueError("structured_content 没有可用正文块")
    return source_blocks, excluded_count


def _new_unit(
    source_id: str,
    units: list[dict[str, Any]],
    block: dict[str, Any],
    *,
    kind: str,
    label: str,
    parent_unit_id: str | None,
    heading_path: list[str],
    heading_paths: dict[str, list[str]],
    last_blocks: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    sequence = len(units) + 1
    unit_id = f"{source_id}.U{sequence:04d}"
    if label in {"表格", "图片", "正文块"}:
        label = f"第{block['page']}页{label}{block['page_block_index']}"
    unit: dict[str, Any] = {
        "unit_id": unit_id,
        "source_id": source_id,
        "kind": kind,
        "label": label,
        "locator": block["locator"],
        "source_locator": _source_locator(block),
        "source_block_ids": [block["block_id"]],
        "sequence": sequence,
        "text": block["text"],
        "digest": sha256_text(block["text"]),
    }
    if parent_unit_id:
        unit["parent_unit_id"] = parent_unit_id
    units.append(unit)
    heading_paths[unit_id] = list(heading_path)
    last_blocks[unit_id] = block
    return unit


def _append_block(
    unit: dict[str, Any],
    block: dict[str, Any],
    *,
    last_blocks: dict[str, dict[str, Any]],
) -> None:
    unit["source_block_ids"].append(block["block_id"])
    unit["text"] = unit["text"].rstrip() + "\n" + block["text"].lstrip()
    unit["digest"] = sha256_text(unit["text"])
    first = unit["source_locator"]["value"]
    unit["locator"] = first if first == block["locator"] else f"{first} → {block['locator']}"
    last_blocks[unit["unit_id"]] = block


def _assign_context_and_references(
    units: list[dict[str, Any]],
    heading_paths: dict[str, list[str]],
) -> None:
    by_id = {unit["unit_id"]: unit for unit in units}
    article_targets = {
        unit["label"]: unit["unit_id"]
        for unit in units
        if unit["kind"] == "ARTICLE"
    }

    for index, unit in enumerate(units):
        ancestors: list[str] = []
        parent_id = unit.get("parent_unit_id")
        seen: set[str] = set()
        while parent_id and parent_id not in seen:
            seen.add(parent_id)
            ancestors.append(parent_id)
            parent = by_id.get(parent_id)
            parent_id = parent.get("parent_unit_id") if parent else None
        ancestors.reverse()

        context: dict[str, Any] = {
            "heading_path": heading_paths.get(unit["unit_id"], []),
            "ancestor_unit_ids": ancestors,
        }
        if index > 0:
            context["previous_unit_id"] = units[index - 1]["unit_id"]
        if index + 1 < len(units):
            context["next_unit_id"] = units[index + 1]["unit_id"]
        unit["context"] = context

        references: list[dict[str, Any]] = []
        seen_labels: set[str] = set()
        for match in ARTICLE_REFERENCE_RE.finditer(unit["text"]):
            target_label = match.group(0)
            if target_label == unit["label"] or target_label in seen_labels:
                continue
            seen_labels.add(target_label)
            reference: dict[str, Any] = {"target_label": target_label}
            target_id = article_targets.get(target_label)
            if target_id:
                reference["target_unit_id"] = target_id
            references.append(reference)
        if references:
            unit["references"] = references


def normalize_structured_content(
    source_id: str,
    structured: dict[str, Any],
    *,
    boundary_repair: BoundaryRepair | None = None,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, int],
]:
    """Preserve parser blocks, reconstruct units, and repair ambiguous boundaries."""
    source_blocks, excluded_count = _build_source_blocks(source_id, structured)
    units: list[dict[str, Any]] = []
    boundary_decisions: list[dict[str, Any]] = []
    heading_paths: dict[str, list[str]] = {}
    last_blocks: dict[str, dict[str, Any]] = {}

    current_section_id: str | None = None
    current_section_label: str | None = None
    current_article_id: str | None = None
    current_article_label: str | None = None
    current_clause_id: str | None = None
    current_clause_label: str | None = None

    for block_index, block in enumerate(source_blocks):
        kind, label = _classify_semantic_hint(block["block_type"], block["text"])

        if kind == "SECTION":
            unit = _new_unit(
                source_id,
                units,
                block,
                kind=kind,
                label=label,
                parent_unit_id=None,
                heading_path=[],
                heading_paths=heading_paths,
                last_blocks=last_blocks,
            )
            current_section_id = unit["unit_id"]
            current_section_label = unit["label"]
            current_article_id = None
            current_article_label = None
            current_clause_id = None
            current_clause_label = None
            continue

        if kind == "ARTICLE":
            path = [value for value in [current_section_label] if value]
            unit = _new_unit(
                source_id,
                units,
                block,
                kind=kind,
                label=label,
                parent_unit_id=current_section_id,
                heading_path=path,
                heading_paths=heading_paths,
                last_blocks=last_blocks,
            )
            current_article_id = unit["unit_id"]
            current_article_label = unit["label"]
            current_clause_id = None
            current_clause_label = None
            continue

        if kind == "CLAUSE":
            path = [
                value
                for value in [current_section_label, current_article_label]
                if value
            ]
            unit = _new_unit(
                source_id,
                units,
                block,
                kind=kind,
                label=label,
                parent_unit_id=current_article_id or current_section_id,
                heading_path=path,
                heading_paths=heading_paths,
                last_blocks=last_blocks,
            )
            current_clause_id = unit["unit_id"]
            current_clause_label = unit["label"]
            continue

        owner_id = current_clause_id or current_article_id
        if kind == "TABLE":
            path = [
                value
                for value in [
                    current_section_label,
                    current_article_label,
                    current_clause_label,
                ]
                if value
            ]
            _new_unit(
                source_id,
                units,
                block,
                kind=kind,
                label=label,
                parent_unit_id=owner_id or current_section_id,
                heading_path=path,
                heading_paths=heading_paths,
                last_blocks=last_blocks,
            )
            continue

        if owner_id and block["block_type"] != "image":
            owner = next(unit for unit in units if unit["unit_id"] == owner_id)
            _append_block(owner, block, last_blocks=last_blocks)
            continue

        parent_id = owner_id or current_section_id
        previous = units[-1] if units else None
        previous_block = last_blocks.get(previous["unit_id"]) if previous else None
        same_level_previous = (
            previous is not None
            and previous["kind"] == "PAGE_BLOCK"
            and previous.get("parent_unit_id") == parent_id
            and previous_block is not None
            and previous_block["block_type"] != "image"
            and block["block_type"] != "image"
        )

        path = [
            value
            for value in [
                current_section_label,
                current_article_label,
                current_clause_label,
            ]
            if value
        ]

        if (
            same_level_previous
            and _needs_boundary_repair(previous_block, block)
        ):
            if boundary_repair is None:
                raise ValueError(
                    f"{source_id}: 模糊文档边界需要 boundary_repair: "
                    f"{previous_block['block_id']} -> {block['block_id']}"
                )
            next_block = (
                source_blocks[block_index + 1]
                if block_index + 1 < len(source_blocks)
                else None
            )
            repair = boundary_repair(
                _build_boundary_state(
                    heading_path=path,
                    previous_unit=previous,
                    previous_block=previous_block,
                    current_block=block,
                    next_block=next_block,
                )
            )
            decision_id = f"{source_id}.D{len(boundary_decisions) + 1:04d}"
            decision: dict[str, Any] = {
                "decision_id": decision_id,
                "source_id": source_id,
                "previous_block_id": previous_block["block_id"],
                "current_block_id": block["block_id"],
                "selected": repair["selected"],
                "applied": repair["applied"],
                "confidence": repair["confidence"],
                "threshold": repair["threshold"],
                "probabilities": repair["probabilities"],
                "model": repair["model"],
                "question_version": repair["question_version"],
            }
            if next_block is not None:
                decision["next_block_id"] = next_block["block_id"]
            if repair.get("request_id"):
                decision["request_id"] = repair["request_id"]
            boundary_decisions.append(decision)

            if decision["applied"] == "CONTINUE_PREVIOUS":
                _append_block(previous, block, last_blocks=last_blocks)
                continue
            if decision["applied"] == "CHILD_OF_PREVIOUS":
                _new_unit(
                    source_id,
                    units,
                    block,
                    kind="PAGE_BLOCK",
                    label=label,
                    parent_unit_id=previous["unit_id"],
                    heading_path=path,
                    heading_paths=heading_paths,
                    last_blocks=last_blocks,
                )
                continue
            if decision["applied"] in {"START_NEW_UNIT", "UNRESOLVED"}:
                _new_unit(
                    source_id,
                    units,
                    block,
                    kind="PAGE_BLOCK",
                    label=label,
                    parent_unit_id=parent_id,
                    heading_path=path,
                    heading_paths=heading_paths,
                    last_blocks=last_blocks,
                )
                continue
            raise ValueError(
                f"{source_id}: boundary_repair 返回未知 applied: "
                f"{decision['applied']}"
            )

        if same_level_previous and _looks_incomplete(previous_block["text"]):
            _append_block(previous, block, last_blocks=last_blocks)
            continue

        _new_unit(
            source_id,
            units,
            block,
            kind="PAGE_BLOCK",
            label=label,
            parent_unit_id=parent_id,
            heading_path=path,
            heading_paths=heading_paths,
            last_blocks=last_blocks,
        )

    _assign_context_and_references(units, heading_paths)
    unresolved_count = sum(
        1
        for decision in boundary_decisions
        if decision["applied"] == "UNRESOLVED"
    )
    return source_blocks, units, boundary_decisions, {
        "excluded_block_count": excluded_count,
        "source_block_count": len(source_blocks),
        "semantic_unit_count": len(units),
        "boundary_decision_count": len(boundary_decisions),
        "unresolved_boundary_count": unresolved_count,
    }
