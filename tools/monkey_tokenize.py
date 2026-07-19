#!/usr/bin/env python3
"""Reference tokenizer for the verified MonKey Office core language."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SYMBOL_REGISTRY = ROOT / "data" / "language-symbols" / "registry.json"

IDENTIFIER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
NUMBER_RE = re.compile(
    r"(?:(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?)"
)
STRUCTURAL_PUNCTUATION = {
    "(": "lparen",
    ")": "rparen",
}


@dataclass(frozen=True)
class Token:
    kind: str
    lexeme: str
    start: int
    end: int
    line: int
    column: int
    symbol_id: str | None = None


class TokenizeError(ValueError):
    def __init__(self, message: str, offset: int, line: int, column: int) -> None:
        super().__init__(message)
        self.offset = offset
        self.line = line
        self.column = column


def load_symbols(path: Path = SYMBOL_REGISTRY) -> tuple[dict[str, str], dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    words: dict[str, str] = {}
    punctuation: dict[str, str] = {}

    for entry in data["symbols"]:
        spelling = entry["spelling"]
        symbol_id = entry["id"]
        if spelling and (spelling[0].isalpha() or spelling[0] == "_"):
            words[entry["canonicalSpelling"]] = symbol_id
        else:
            punctuation[spelling] = symbol_id

    return words, punctuation


def advance_position(text: str, line: int, column: int) -> tuple[int, int]:
    for char in text:
        if char == "\n":
            line += 1
            column = 1
        else:
            column += 1
    return line, column


def tokenize(source: str) -> list[Token]:
    words, punctuation = load_symbols()
    punctuation_spellings = sorted(punctuation, key=len, reverse=True)

    tokens: list[Token] = []
    offset = 0
    line = 1
    column = 1

    while offset < len(source):
        char = source[offset]

        if char in " \t\r":
            start = offset
            while offset < len(source) and source[offset] in " \t\r":
                offset += 1
            line, column = advance_position(source[start:offset], line, column)
            continue

        if char == "\n":
            tokens.append(Token("newline", "\n", offset, offset + 1, line, column))
            offset += 1
            line += 1
            column = 1
            continue

        start = offset
        start_line = line
        start_column = column

        structural_kind = STRUCTURAL_PUNCTUATION.get(char)
        if structural_kind:
            tokens.append(
                Token(structural_kind, char, start, start + 1, line, column)
            )
            offset += 1
            column += 1
            continue

        if char == '"':
            offset += 1
            while offset < len(source):
                if source[offset] == '"':
                    if offset + 1 < len(source) and source[offset + 1] == '"':
                        offset += 2
                        continue
                    offset += 1
                    break
                offset += 1
            else:
                raise TokenizeError(
                    "nicht abgeschlossene Zeichenkette",
                    start,
                    start_line,
                    start_column,
                )

            lexeme = source[start:offset]
            tokens.append(
                Token("string", lexeme, start, offset, start_line, start_column)
            )
            line, column = advance_position(lexeme, line, column)
            continue

        number_match = NUMBER_RE.match(source, offset)
        if number_match:
            offset = number_match.end()
            lexeme = source[start:offset]
            tokens.append(
                Token("number", lexeme, start, offset, start_line, start_column)
            )
            line, column = advance_position(lexeme, line, column)
            continue

        identifier_match = IDENTIFIER_RE.match(source, offset)
        if identifier_match:
            offset = identifier_match.end()
            lexeme = source[start:offset]
            symbol_id = words.get(lexeme.upper())
            kind = "symbol" if symbol_id else "identifier"
            tokens.append(
                Token(
                    kind,
                    lexeme,
                    start,
                    offset,
                    start_line,
                    start_column,
                    symbol_id,
                )
            )
            line, column = advance_position(lexeme, line, column)
            continue

        matched = False
        for spelling in punctuation_spellings:
            if source.startswith(spelling, offset):
                offset += len(spelling)
                tokens.append(
                    Token(
                        "symbol",
                        spelling,
                        start,
                        offset,
                        start_line,
                        start_column,
                        punctuation[spelling],
                    )
                )
                line, column = advance_position(spelling, line, column)
                matched = True
                break
        if matched:
            continue

        raise TokenizeError(
            f"unbekanntes Zeichen {char!r}",
            offset,
            line,
            column,
        )

    tokens.append(Token("eof", "", offset, offset, line, column))
    return tokens


def token_rows(tokens: Iterable[Token]) -> list[dict[str, object]]:
    return [asdict(token) for token in tokens]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tokenisiert MonKey-Office-Quelltext mit der Symbol-Registry."
    )
    parser.add_argument("path", nargs="?", help="Quelldatei; sonst stdin")
    parser.add_argument("--json", action="store_true", help="Tokens als JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    source = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()

    try:
        tokens = tokenize(source)
    except TokenizeError as exc:
        print(
            f"Tokenisierung fehlgeschlagen bei {exc.line}:{exc.column}: {exc}",
            file=sys.stderr,
        )
        return 1

    rows = token_rows(tokens)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            symbol = f" {row['symbol_id']}" if row["symbol_id"] else ""
            print(
                f"{row['line']}:{row['column']} "
                f"{row['kind']:<10} {row['lexeme']!r}{symbol}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
