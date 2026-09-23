#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parents[1] / "modules" / "document-normalizer"
sys.path.insert(0, str(MODULE_ROOT))

from document_normalizer import normalize_structured_content


class DocumentNormalizerTest(unittest.TestCase):
    def test_reconstructs_article_and_cross_page_clause(self):
        structured = {
            "pages": [
                {
                    "page_idx": 0,
                    "blocks": [
                        {"type": "paragraph_title", "content": "第二章 受益所有人识别"},
                        {"type": "text", "content": "第十条 金融机构应当按照下列方式"},
                        {"type": "text", "content": "识别受益所有人："},
                        {"type": "text", "content": "（一）公司，应当识别"},
                    ],
                },
                {
                    "page_idx": 1,
                    "blocks": [
                        {
                            "type": "text",
                            "content": "直接或者间接拥有百分之二十五以上股权的自然人。",
                        },
                        {"type": "text", "content": "（二）合伙企业，应当识别合伙权益持有人。"},
                    ],
                },
            ]
        }

        blocks, units, decisions, stats = normalize_structured_content("SRC.demo", structured)

        self.assertEqual(6, len(blocks))
        self.assertEqual(4, len(units))
        self.assertEqual([], decisions)
        self.assertEqual(
            ["SECTION", "ARTICLE", "CLAUSE", "CLAUSE"],
            [unit["kind"] for unit in units],
        )

        article = units[1]
        self.assertEqual(
            ["SRC.demo.B00002", "SRC.demo.B00003"],
            article["source_block_ids"],
        )
        self.assertEqual(
            "第十条 金融机构应当按照下列方式\n识别受益所有人：",
            article["text"],
        )

        first_clause = units[2]
        self.assertEqual(
            ["SRC.demo.B00004", "SRC.demo.B00005"],
            first_clause["source_block_ids"],
        )
        self.assertIn("百分之二十五以上股权", first_clause["text"])
        self.assertEqual(article["unit_id"], first_clause["parent_unit_id"])
        self.assertEqual(
            ["第二章 受益所有人识别", "第十条"],
            first_clause["context"]["heading_path"],
        )

        owned_blocks = [
            block_id
            for unit in units
            for block_id in unit["source_block_ids"]
        ]
        self.assertEqual(
            [block["block_id"] for block in blocks],
            owned_blocks,
        )
        self.assertEqual(6, stats["source_block_count"])
        self.assertEqual(4, stats["semantic_unit_count"])

    def test_generic_text_does_not_merge_into_image_unit(self):
        structured = {
            "pages": [
                {
                    "page_idx": 0,
                    "blocks": [
                        {"type": "image", "captions": ["图一"]},
                        {"type": "text", "content": "这是图片后的独立正文。"},
                    ],
                }
            ]
        }

        _blocks, units, decisions, _stats = normalize_structured_content("SRC.image", structured)

        self.assertEqual(2, len(units))
        self.assertEqual([], decisions)
        self.assertEqual(["PAGE_BLOCK", "PAGE_BLOCK"], [unit["kind"] for unit in units])
        self.assertEqual("图一", units[0]["text"])
        self.assertEqual("这是图片后的独立正文。", units[1]["text"])

    def test_jev_repairs_ambiguous_child_boundary(self):
        structured = {
            "pages": [
                {
                    "page_idx": 0,
                    "blocks": [
                        {"type": "text", "content": "办理要求如下："},
                        {"type": "text", "content": "1. 核验身份证明。"},
                        {"type": "text", "content": "后续独立说明。"},
                    ],
                }
            ]
        }

        def repair(state):
            self.assertEqual("办理要求如下：", state["previous_block"]["text"])
            self.assertEqual("1. 核验身份证明。", state["current_block"]["text"])
            return {
                "selected": "CHILD_OF_PREVIOUS",
                "applied": "CHILD_OF_PREVIOUS",
                "confidence": 0.97,
                "threshold": 0.90,
                "probabilities": {
                    "CONTINUE_PREVIOUS": 0.01,
                    "START_NEW_UNIT": 0.01,
                    "CHILD_OF_PREVIOUS": 0.97,
                    "UNRESOLVED": 0.01,
                },
                "model": "jev-test",
                "question_version": "boundary-relation-v1",
                "request_id": "req-test",
            }

        blocks, units, decisions, stats = normalize_structured_content(
            "SRC.jev",
            structured,
            boundary_repair=repair,
        )

        self.assertEqual(3, len(blocks))
        self.assertEqual(3, len(units))
        self.assertEqual(1, len(decisions))
        self.assertEqual("CHILD_OF_PREVIOUS", decisions[0]["applied"])
        self.assertEqual(units[0]["unit_id"], units[1]["parent_unit_id"])
        self.assertEqual(1, stats["boundary_decision_count"])
        self.assertEqual(0, stats["unresolved_boundary_count"])

    def test_article_colon_can_create_jev_child(self):
        structured = {
            "pages": [
                {
                    "page_idx": 0,
                    "blocks": [
                        {"type": "text", "content": "第十条 金融机构应当采取以下措施："},
                        {"type": "text", "content": "1. 核验客户身份证明。"},
                    ],
                }
            ]
        }

        def repair(state):
            self.assertEqual("ARTICLE", state["previous_unit"]["kind"])
            self.assertEqual("第十条", state["previous_unit"]["label"])
            return {
                "selected": "CHILD_OF_PREVIOUS",
                "applied": "CHILD_OF_PREVIOUS",
                "confidence": 0.99,
                "threshold": 0.90,
                "probabilities": {
                    "CONTINUE_PREVIOUS": 0.0,
                    "START_NEW_UNIT": 0.0,
                    "CHILD_OF_PREVIOUS": 0.99,
                    "UNRESOLVED": 0.01,
                },
                "model": "jev-test",
                "question_version": "boundary-relation-v1",
            }

        _blocks, units, decisions, _stats = normalize_structured_content(
            "SRC.article-child",
            structured,
            boundary_repair=repair,
        )

        self.assertEqual(["ARTICLE", "PAGE_BLOCK"], [unit["kind"] for unit in units])
        self.assertEqual(units[0]["unit_id"], units[1]["parent_unit_id"])
        self.assertEqual("CHILD_OF_PREVIOUS", decisions[0]["applied"])

    def test_list_shape_without_colon_triggers_jev(self):
        structured = {
            "pages": [
                {
                    "page_idx": 0,
                    "blocks": [
                        {"type": "text", "content": "前序说明已经结束。"},
                        {"type": "text", "content": "1. 第一项要求。"},
                    ],
                }
            ]
        }

        calls = []

        def repair(state):
            calls.append(state)
            return {
                "selected": "START_NEW_UNIT",
                "applied": "START_NEW_UNIT",
                "confidence": 0.96,
                "threshold": 0.90,
                "probabilities": {
                    "CONTINUE_PREVIOUS": 0.01,
                    "START_NEW_UNIT": 0.96,
                    "CHILD_OF_PREVIOUS": 0.02,
                    "UNRESOLVED": 0.01,
                },
                "model": "jev-test",
                "question_version": "boundary-relation-v1",
            }

        _blocks, units, decisions, stats = normalize_structured_content(
            "SRC.list",
            structured,
            boundary_repair=repair,
        )

        self.assertEqual(1, len(calls))
        self.assertEqual(2, len(units))
        self.assertEqual("START_NEW_UNIT", decisions[0]["applied"])
        self.assertEqual(1, stats["boundary_decision_count"])

    def test_child_continuation_remains_in_child_unit(self):
        structured = {
            "pages": [
                {
                    "page_idx": 0,
                    "blocks": [
                        {"type": "text", "content": "办理要求如下："},
                        {"type": "text", "content": "1. 客户属于高风险情形的，"},
                        {"type": "text", "content": "除另有规定外，"},
                        {"type": "text", "content": "应当进一步核实身份。"},
                    ],
                }
            ]
        }

        calls = []

        def repair(_state):
            calls.append(1)
            return {
                "selected": "CHILD_OF_PREVIOUS",
                "applied": "CHILD_OF_PREVIOUS",
                "confidence": 0.98,
                "threshold": 0.90,
                "probabilities": {
                    "CONTINUE_PREVIOUS": 0.005,
                    "START_NEW_UNIT": 0.005,
                    "CHILD_OF_PREVIOUS": 0.98,
                    "UNRESOLVED": 0.01,
                },
                "model": "jev-test",
                "question_version": "boundary-relation-v1",
            }

        _blocks, units, decisions, stats = normalize_structured_content(
            "SRC.child",
            structured,
            boundary_repair=repair,
        )

        self.assertEqual(1, len(calls))
        self.assertEqual(2, len(units))
        self.assertEqual(1, len(decisions))
        self.assertEqual(units[0]["unit_id"], units[1]["parent_unit_id"])
        self.assertEqual(
            "1. 客户属于高风险情形的，\n除另有规定外，\n应当进一步核实身份。",
            units[1]["text"],
        )
        self.assertEqual(
            ["SRC.child.B00002", "SRC.child.B00003", "SRC.child.B00004"],
            units[1]["source_block_ids"],
        )
        self.assertEqual(0, stats["unresolved_boundary_count"])

    def test_low_confidence_boundary_stays_unresolved(self):
        structured = {
            "pages": [
                {
                    "page_idx": 0,
                    "blocks": [
                        {"type": "text", "content": "材料包括："},
                        {"type": "text", "content": "其他证明材料。"},
                    ],
                }
            ]
        }

        def repair(_state):
            return {
                "selected": "CONTINUE_PREVIOUS",
                "applied": "UNRESOLVED",
                "confidence": 0.61,
                "threshold": 0.90,
                "probabilities": {
                    "CONTINUE_PREVIOUS": 0.58,
                    "START_NEW_UNIT": 0.20,
                    "CHILD_OF_PREVIOUS": 0.12,
                    "UNRESOLVED": 0.10,
                },
                "model": "jev-test",
                "question_version": "boundary-relation-v1",
            }

        _blocks, units, decisions, stats = normalize_structured_content(
            "SRC.low",
            structured,
            boundary_repair=repair,
        )

        self.assertEqual(2, len(units))
        self.assertEqual("UNRESOLVED", decisions[0]["applied"])
        self.assertEqual(1, stats["unresolved_boundary_count"])

    def test_ambiguous_boundary_requires_repair(self):
        structured = {
            "pages": [
                {
                    "page_idx": 0,
                    "blocks": [
                        {"type": "text", "content": "办理要求如下："},
                        {"type": "text", "content": "核验身份证明。"},
                    ],
                }
            ]
        }

        with self.assertRaisesRegex(ValueError, "boundary_repair"):
            normalize_structured_content("SRC.required", structured)

    def test_resolves_cross_article_reference_without_changing_ownership(self):
        structured = {
            "pages": [
                {
                    "page_idx": 0,
                    "blocks": [
                        {"type": "text", "content": "第十条 客户应当提供身份证明。"},
                        {"type": "text", "content": "第十一条 符合第十条规定的，可以继续办理。"},
                    ],
                }
            ]
        }

        _blocks, units, decisions, _stats = normalize_structured_content("SRC.refs", structured)

        self.assertEqual(2, len(units))
        self.assertEqual([], decisions)
        self.assertEqual(
            [{"target_label": "第十条", "target_unit_id": units[0]["unit_id"]}],
            units[1]["references"],
        )


if __name__ == "__main__":
    unittest.main()
