from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "monkey_tokenize.py"

spec = importlib.util.spec_from_file_location("monkey_tokenize", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class ReferenceLexerTests(unittest.TestCase):
    def test_verified_keywords_are_case_insensitive(self) -> None:
        tokens = module.tokenize("dim Amount\nSeT Result")
        symbols = [
            token.symbol_id
            for token in tokens
            if token.kind == "symbol"
        ]
        self.assertEqual(symbols, ["kw-dim", "kw-set"])

    def test_verified_word_operators_are_registry_driven(self) -> None:
        tokens = module.tokenize("a AND b or NOT c")
        symbols = [
            token.symbol_id
            for token in tokens
            if token.kind == "symbol"
        ]
        self.assertEqual(symbols, ["op-and", "op-or", "op-not"])

    def test_power_operator_is_recognized(self) -> None:
        tokens = module.tokenize("2 ^ 3 ^ 2")
        powers = [
            token for token in tokens if token.symbol_id == "op-power"
        ]
        self.assertEqual(len(powers), 2)

    def test_numbers_and_identifiers_are_distinct(self) -> None:
        tokens = module.tokenize("value 12 3.5 .25 1e3")
        kinds = [token.kind for token in tokens[:-1]]
        self.assertEqual(
            kinds,
            ["identifier", "number", "number", "number", "number"],
        )

    def test_doubled_quote_is_accepted_inside_string(self) -> None:
        tokens = module.tokenize('"a ""quoted"" value"')
        self.assertEqual(tokens[0].kind, "string")
        self.assertEqual(tokens[0].lexeme, '"a ""quoted"" value"')

    def test_unterminated_string_reports_position(self) -> None:
        with self.assertRaises(module.TokenizeError) as context:
            module.tokenize('dim x\n"unterminated')
        self.assertEqual(context.exception.line, 2)
        self.assertEqual(context.exception.column, 1)


if __name__ == "__main__":
    unittest.main()
