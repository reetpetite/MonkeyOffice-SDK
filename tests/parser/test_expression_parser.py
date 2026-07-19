from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from parse_expression import ParseError, node_to_dict, parse_expression


class ExpressionParserTests(unittest.TestCase):
    def test_power_is_left_associative(self) -> None:
        tree = node_to_dict(parse_expression("2 ^ 3 ^ 2"))
        self.assertEqual(tree["operator"], "op-power")
        self.assertEqual(tree["left"]["operator"], "op-power")
        self.assertEqual(tree["left"]["left"]["value"], "2")
        self.assertEqual(tree["left"]["right"]["value"], "3")
        self.assertEqual(tree["right"]["value"], "2")

    def test_and_and_or_share_precedence_and_associate_left(self) -> None:
        tree = node_to_dict(parse_expression("a OR b AND c"))
        self.assertEqual(tree["operator"], "op-and")
        self.assertEqual(tree["left"]["operator"], "op-or")
        self.assertEqual(tree["right"]["value"], "c")

    def test_not_binds_before_and(self) -> None:
        tree = node_to_dict(parse_expression("NOT a AND b"))
        self.assertEqual(tree["operator"], "op-and")
        self.assertEqual(tree["left"]["operator"], "op-not")
        self.assertEqual(tree["left"]["operand"]["value"], "a")

    def test_power_binds_before_not_operand_finishes(self) -> None:
        tree = node_to_dict(parse_expression("NOT a ^ b"))
        self.assertEqual(tree["operator"], "op-not")
        self.assertEqual(tree["operand"]["operator"], "op-power")

    def test_parentheses_override_precedence(self) -> None:
        tree = node_to_dict(parse_expression("(a OR b) ^ c"))
        self.assertEqual(tree["operator"], "op-power")
        self.assertEqual(tree["left"]["kind"], "group")
        self.assertEqual(tree["left"]["operand"]["operator"], "op-or")

    def test_literals_and_identifier(self) -> None:
        self.assertEqual(parse_expression("name").kind, "identifier")
        self.assertEqual(parse_expression("12.5").kind, "number")
        self.assertEqual(parse_expression('"text"').kind, "string")

    def test_trailing_token_is_rejected(self) -> None:
        with self.assertRaises(ParseError):
            parse_expression("a b")

    def test_missing_closing_parenthesis_is_rejected(self) -> None:
        with self.assertRaises(ParseError):
            parse_expression("(a OR b")


if __name__ == "__main__":
    unittest.main()
