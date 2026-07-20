#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from monkey_tokenize import Token, TokenizeError, tokenize
from parse_expression import (
    Node as ExpressionNode,
    ParseError as ExpressionParseError,
    Parser as ExpressionParser,
    node_to_dict,
)

STATEMENT_REGISTRY = ROOT / "data/statements/registry.json"


@dataclass(frozen=True)
class StatementNode:
    kind: str
    start: int
    end: int
    name: str | None = None
    type_name: str | None = None
    initializer: ExpressionNode | None = None
    value: ExpressionNode | None = None
    expression: ExpressionNode | None = None


@dataclass(frozen=True)
class ProgramNode:
    kind: str
    start: int
    end: int
    body: tuple[StatementNode, ...]


class ProgramParseError(ValueError):
    def __init__(self, message: str, token: Token) -> None:
        super().__init__(message)
        self.token = token


def load_statements(path: Path = STATEMENT_REGISTRY) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {entry["symbolId"]: entry for entry in data["statements"]}


def eof_after(tokens: list[Token]) -> Token:
    if tokens:
        token = tokens[-1]
        return Token(
            "eof",
            "",
            token.end,
            token.end,
            token.line,
            token.column + len(token.lexeme),
        )
    return Token("eof", "", 0, 0, 1, 1)


def split_lines(tokens: list[Token]) -> list[list[Token]]:
    lines: list[list[Token]] = []
    current: list[Token] = []
    for token in tokens:
        if token.kind == "eof":
            break
        if token.kind == "newline":
            lines.append(current)
            current = []
        else:
            current.append(token)
    if current:
        lines.append(current)
    return lines


def expect_identifier(tokens: list[Token], index: int, message: str) -> Token:
    if index >= len(tokens):
        raise ProgramParseError(message, tokens[-1])
    token = tokens[index]
    if token.kind != "identifier":
        raise ProgramParseError(message, token)
    return token


def expect_symbol(tokens: list[Token], index: int, symbol_id: str, message: str) -> Token:
    if index >= len(tokens):
        raise ProgramParseError(message, tokens[-1])
    token = tokens[index]
    if token.kind != "symbol" or token.symbol_id != symbol_id:
        raise ProgramParseError(message, token)
    return token


def parse_expression_tokens(tokens: list[Token]) -> ExpressionNode:
    if not tokens:
        raise ProgramParseError("Ausdruck erwartet", eof_after(tokens))
    try:
        return ExpressionParser([*tokens, eof_after(tokens)]).parse()
    except ExpressionParseError as exc:
        raise ProgramParseError(str(exc), exc.token) from exc


def parse_dim(tokens: list[Token], definition: dict[str, Any]) -> StatementNode:
    first = tokens[0]
    name = expect_identifier(tokens, 1, "Bezeichner nach DIM erwartet")
    expect_symbol(tokens, 2, "kw-as", "AS nach Variablennamen erwartet")
    type_name = expect_identifier(tokens, 3, "Typname nach AS erwartet")

    if len(tokens) == 4:
        return StatementNode(
            definition["astKind"],
            first.start,
            type_name.end,
            name=name.lexeme,
            type_name=type_name.lexeme,
        )

    equals = tokens[4]
    if equals.kind != "equals":
        raise ProgramParseError("'=' oder Zeilenende nach Typname erwartet", equals)
    if len(tokens) == 5:
        raise ProgramParseError("Ausdruck nach '=' erwartet", equals)
    initializer = parse_expression_tokens(tokens[5:])
    return StatementNode(
        definition["astKind"],
        first.start,
        initializer.end,
        name=name.lexeme,
        type_name=type_name.lexeme,
        initializer=initializer,
    )


def parse_set(tokens: list[Token], definition: dict[str, Any]) -> StatementNode:
    first = tokens[0]
    name = expect_identifier(tokens, 1, "Bezeichner nach SET erwartet")
    separator = expect_symbol(tokens, 2, "kw-to", "TO nach Zuweisungsziel erwartet")
    if len(tokens) == 3:
        raise ProgramParseError("Ausdruck nach TO erwartet", separator)
    value = parse_expression_tokens(tokens[3:])
    return StatementNode(
        definition["astKind"],
        first.start,
        value.end,
        name=name.lexeme,
        value=value,
    )


def parse_statement(tokens: list[Token], definitions: dict[str, dict[str, Any]]) -> StatementNode:
    first = tokens[0]
    if first.kind == "symbol" and first.symbol_id in definitions:
        definition = definitions[first.symbol_id]
        form = definition["form"]
        if form == "dim-declaration":
            return parse_dim(tokens, definition)
        if form == "set-assignment":
            return parse_set(tokens, definition)
        raise ProgramParseError(f"nicht unterstützte Statementform {form!r}", first)

    expression = parse_expression_tokens(tokens)
    return StatementNode(
        "expression_statement",
        expression.start,
        expression.end,
        expression=expression,
    )


def parse_program(source: str) -> ProgramNode:
    definitions = load_statements()
    body = tuple(
        parse_statement(line, definitions)
        for line in split_lines(tokenize(source))
        if line
    )
    return ProgramNode(
        "program",
        body[0].start if body else 0,
        body[-1].end if body else 0,
        body,
    )


def statement_to_dict(node: StatementNode) -> dict[str, Any]:
    result: dict[str, Any] = {
        "kind": node.kind,
        "start": node.start,
        "end": node.end,
    }
    if node.name is not None:
        result["name"] = node.name
    if node.type_name is not None:
        result["typeName"] = node.type_name
    if node.initializer is not None:
        result["initializer"] = node_to_dict(node.initializer)
    if node.value is not None:
        result["value"] = node_to_dict(node.value)
    if node.expression is not None:
        result["expression"] = node_to_dict(node.expression)
    return result


def program_to_dict(node: ProgramNode) -> dict[str, Any]:
    return {
        "kind": node.kind,
        "start": node.start,
        "end": node.end,
        "body": [statement_to_dict(statement) for statement in node.body],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parst einen zeilenorientierten MonKey-Office-Programmkern."
    )
    parser.add_argument("path", nargs="?")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    source = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()

    try:
        program = parse_program(source)
    except TokenizeError as exc:
        print(
            f"Tokenisierung fehlgeschlagen bei {exc.line}:{exc.column}: {exc}",
            file=sys.stderr,
        )
        return 1
    except ProgramParseError as exc:
        print(
            f"Parserfehler bei {exc.token.line}:{exc.token.column}: {exc}",
            file=sys.stderr,
        )
        return 1

    print(
        json.dumps(
            program_to_dict(program),
            ensure_ascii=False,
            indent=None if args.compact else 2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
