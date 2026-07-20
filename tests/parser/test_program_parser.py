from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from parse_program import ProgramParseError, parse_program, program_to_dict


class ProgramParserTests(unittest.TestCase):
    def test_empty_program(self) -> None:
        self.assertEqual(program_to_dict(parse_program(""))["body"], [])

    def test_blank_lines_are_ignored(self) -> None:
        program = parse_program("\n\nDIM amount AS number\n\n")
        self.assertEqual(len(program_to_dict(program)["body"]), 1)

    def test_dim_statement(self) -> None:
        statement = program_to_dict(parse_program("DIM amount AS number"))["body"][0]
        self.assertEqual(statement["kind"], "dim_statement")
        self.assertEqual(statement["name"], "amount")
        self.assertEqual(statement["typeName"], "number")
        self.assertNotIn("initializer", statement)

    def test_dim_statement_with_initializer(self) -> None:
        statement = program_to_dict(parse_program("DIM amount AS number = 5"))["body"][0]
        self.assertEqual(statement["initializer"]["kind"], "number")
        self.assertEqual(statement["initializer"]["value"], "5")

    def test_set_statement(self) -> None:
        statement = program_to_dict(parse_program("set Result to 10"))["body"][0]
        self.assertEqual(statement["kind"], "set_statement")
        self.assertEqual(statement["name"], "Result")
        self.assertEqual(statement["value"]["value"], "10")

    def test_expression_statement_reuses_expression_parser(self) -> None:
        expression = program_to_dict(parse_program("a OR b AND c"))["body"][0]["expression"]
        self.assertEqual(expression["operator"], "op-and")
        self.assertEqual(expression["left"]["operator"], "op-or")

    def test_multiple_statements(self) -> None:
        source = "DIM amount AS number\nSET amount TO 10\nNOT amount AND result\n"
        kinds = [item["kind"] for item in program_to_dict(parse_program(source))["body"]]
        self.assertEqual(kinds, ["dim_statement", "set_statement", "expression_statement"])

    def test_dim_requires_identifier(self) -> None:
        with self.assertRaises(ProgramParseError):
            parse_program("DIM 12 AS number")

    def test_dim_requires_as(self) -> None:
        with self.assertRaises(ProgramParseError):
            parse_program("DIM amount number")

    def test_dim_requires_type_name(self) -> None:
        with self.assertRaises(ProgramParseError):
            parse_program("DIM amount AS")

    def test_initializer_requires_expression(self) -> None:
        with self.assertRaises(ProgramParseError):
            parse_program("DIM amount AS number =")

    def test_set_requires_to(self) -> None:
        with self.assertRaises(ProgramParseError):
            parse_program("SET amount 10")

    def test_set_requires_value(self) -> None:
        with self.assertRaises(ProgramParseError):
            parse_program("SET amount TO")


if __name__ == "__main__":
    unittest.main()
