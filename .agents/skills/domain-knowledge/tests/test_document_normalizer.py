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

        blocks, units, stats = normalize_structured_content("SRC.demo", structured)

        self.assertEqual(6, len(blocks))
        self.assertEqual(4, len(units))
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

        _blocks, units, _stats = normalize_structured_content("SRC.refs", structured)

        self.assertEqual(2, len(units))
        self.assertEqual(
            [{"target_label": "第十条", "target_unit_id": units[0]["unit_id"]}],
            units[1]["references"],
        )


if __name__ == "__main__":
    unittest.main()
