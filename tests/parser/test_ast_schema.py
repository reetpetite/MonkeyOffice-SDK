from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from parse_expression import node_to_dict, parse_expression
from parse_program import parse_program, program_to_dict
from validate_ast import validate


class AstSchemaTests(unittest.TestCase):
    def test_expression_parser_output_is_valid(self) -> None:
        document = node_to_dict(parse_expression("NOT a AND b ^ c"))
        self.assertEqual(validate(document), [])

    def test_program_parser_output_is_valid(self) -> None:
        document = program_to_dict(
            parse_program("DIM amount\nSET result\nNOT amount AND result\n")
        )
        self.assertEqual(validate(document), [])

    def test_empty_program_is_valid(self) -> None:
        self.assertEqual(validate(program_to_dict(parse_program(""))), [])

    def test_unknown_node_kind_is_rejected(self) -> None:
        errors = validate({"kind": "mystery", "start": 0, "end": 1})
        self.assertTrue(errors)

    def test_missing_binary_operand_is_rejected(self) -> None:
        document = {
            "kind": "binary",
            "start": 0,
            "end": 3,
            "operator": "op-and",
            "left": {
                "kind": "identifier",
                "start": 0,
                "end": 1,
                "value": "a",
            },
        }
        self.assertTrue(validate(document))

    def test_invalid_span_is_rejected(self) -> None:
        document = {
            "kind": "identifier",
            "start": 5,
            "end": 2,
            "value": "a",
        }
        errors = validate(document)
        self.assertTrue(any("liegt vor start" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
