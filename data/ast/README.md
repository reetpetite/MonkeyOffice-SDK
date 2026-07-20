# Reference AST schema

`schema.json` defines the machine-readable JSON contract shared by the
reference expression parser and program parser.

It currently covers:

- identifiers
- number and string literals
- grouped expressions
- unary and binary expressions
- `DIM` and `SET` statement nodes
- expression statements
- complete program nodes

Validate parser output with:

```bash
python tools/parse_expression.py 'NOT a AND b'   | python tools/validate_ast.py

printf 'DIM amount\nSET result\namount AND result\n'   | python tools/parse_program.py   | python tools/validate_ast.py
```

The schema describes the executable reference model. It is not yet a complete
claim about the full proprietary language grammar.
