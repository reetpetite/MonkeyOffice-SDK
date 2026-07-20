# AST contract

## Purpose

The reference tokenizer and parsers now produce a stable, machine-checkable
JSON representation.

The contract is defined in:

```text
data/ast/schema.json
```

This separates three concerns:

```text
source syntax
    -> parser implementation
    -> stable JSON AST contract
```

Downstream tools should consume the AST contract rather than depending on
Python dataclasses internal to the parser.

## Source spans

Every node contains zero-based half-open source offsets:

```text
start <= character offset < end
```

For example, parsing:

```text
NOT value
```

produces a unary node spanning the complete expression and an identifier node
spanning only `value`.

`tools/validate_ast.py` additionally rejects nodes whose `end` offset precedes
their `start` offset.

## Operator identity

Unary and binary nodes store stable language-symbol identifiers:

```text
op-not
op-power
op-and
op-or
```

They do not store normalized display spelling. This keeps the AST independent
of source capitalization and future spelling aliases.

## Validation

Expression:

```bash
python tools/parse_expression.py 'NOT a AND b ^ c'   | python tools/validate_ast.py
```

Program:

```bash
printf 'DIM amount\nSET result\nNOT amount AND result\n'   | python tools/parse_program.py   | python tools/validate_ast.py
```

## Current boundary

The schema intentionally contains only node kinds emitted by the current
reference implementation. New grammar features must extend the parser, schema,
documentation, and tests together.
