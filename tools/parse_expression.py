#!/usr/bin/env python3
"""Registry-driven Pratt parser for MonKey Office expressions."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from monkey_tokenize import Token, TokenizeError, tokenize  # noqa: E402

OPERATOR_REGISTRY = ROOT / "data" / "operators" / "registry.json"


@dataclass(frozen=True)
class Node:
    kind: str
    start: int
    end: int
    value: str | None = None
    operator: str | None = None
    operand: "Node | None" = None
    left: "Node | None" = None
    right: "Node | None" = None


class ParseError(ValueError):
    def __init__(self, message: str, token: Token) -> None:
        super().__init__(message)
        self.token = token


def load_operators(path: Path = OPERATOR_REGISTRY) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {entry["symbolId"]: entry for entry in data["operators"]}


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = [token for token in tokens if token.kind != "newline"]
        self.index = 0
        self.operators = load_operators()

    @property
    def current(self) -> Token:
        return self.tokens[self.index]

    def advance(self) -> Token:
        token = self.current
        if token.kind != "eof":
            self.index += 1
        return token

    def expect(self, kind: str) -> Token:
        token = self.current
        if token.kind != kind:
            raise ParseError(f"erwartet {kind}, gefunden {token.kind}", token)
        return self.advance()

    def parse(self) -> Node:
        node = self.parse_expression(0)
        if self.current.kind != "eof":
            raise ParseError("unerwartetes Token nach Ausdruck", self.current)
        return node

    def parse_expression(self, minimum_precedence: int) -> Node:
        left = self.parse_prefix()

        while self.current.kind == "symbol":
            entry = self.operators.get(self.current.symbol_id or "")
            if not entry or entry["fixity"] != "infix":
                break

            precedence = entry["precedence"]
            if precedence < minimum_precedence:
                break

            operator_token = self.advance()
            next_minimum = (
                precedence + 1
                if entry["associativity"] == "left"
                else precedence
            )
            right = self.parse_expression(next_minimum)
            left = Node(
                kind="binary",
                start=left.start,
                end=right.end,
                operator=operator_token.symbol_id,
                left=left,
                right=right,
            )

        return left

    def parse_prefix(self) -> Node:
        token = self.current

        if token.kind == "symbol":
            entry = self.operators.get(token.symbol_id or "")
            if entry and entry["fixity"] == "prefix":
                self.advance()
                operand = self.parse_expression(entry["precedence"])
                return Node(
                    kind="unary",
                    start=token.start,
                    end=operand.end,
                    operator=token.symbol_id,
                    operand=operand,
                )

        if token.kind == "identifier":
            self.advance()
            return Node(
                kind="identifier",
                start=token.start,
                end=token.end,
                value=token.lexeme,
            )

        if token.kind == "number":
            self.advance()
            return Node(
                kind="number",
                start=token.start,
                end=token.end,
                value=token.lexeme,
            )

        if token.kind == "string":
            self.advance()
            return Node(
                kind="string",
                start=token.start,
                end=token.end,
                value=token.lexeme,
            )

        if token.kind == "lparen":
            opening = self.advance()
            expression = self.parse_expression(0)
            closing = self.expect("rparen")
            return Node(
                kind="group",
                start=opening.start,
                end=closing.end,
                operand=expression,
            )

        raise ParseError("Ausdruck erwartet", token)


def parse_expression(source: str) -> Node:
    return Parser(tokenize(source)).parse()


def node_to_dict(node: Node) -> dict[str, Any]:
    result: dict[str, Any] = {
        "kind": node.kind,
        "start": node.start,
        "end": node.end,
    }
    if node.value is not None:
        result["value"] = node.value
    if node.operator is not None:
        result["operator"] = node.operator
    if node.operand is not None:
        result["operand"] = node_to_dict(node.operand)
    if node.left is not None:
        result["left"] = node_to_dict(node.left)
    if node.right is not None:
        result["right"] = node_to_dict(node.right)
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    cli = argparse.ArgumentParser(description="Parst einen MonKey-Office-Ausdruck.")
    cli.add_argument("expression", nargs="?", help="Ausdruck; sonst stdin")
    cli.add_argument("--compact", action="store_true", help="kompaktes JSON")
    return cli.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    source = args.expression if args.expression is not None else sys.stdin.read()

    try:
        node = parse_expression(source)
    except TokenizeError as exc:
        print(
            f"Tokenisierung fehlgeschlagen bei {exc.line}:{exc.column}: {exc}",
            file=sys.stderr,
        )
        return 1
    except ParseError as exc:
        token = exc.token
        print(
            f"Parserfehler bei {token.line}:{token.column}: {exc}",
            file=sys.stderr,
        )
        return 1

    print(
        json.dumps(
            node_to_dict(node),
            ensure_ascii=False,
            indent=None if args.compact else 2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
