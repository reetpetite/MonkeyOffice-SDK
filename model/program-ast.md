# Program AST

`tools/parse_program.py` extends the reference implementation from isolated expressions to a line-oriented program.

```text
program := (blank-line | statement newline?)*
statement := registered-keyword-statement | expression-statement
registered-keyword-statement := DIM identifier | SET identifier
expression-statement := expression
```

The concrete `DIM` and `SET` forms are currently **inferred** and must be verified experimentally.

Example:

```text
DIM amount
SET result
NOT amount AND result
```

The parser dispatches by stable symbol IDs from `data/statements/registry.json`, not by source spelling. It does not yet implement assignments, calls, blocks, conditions, loops, comments, or statement separators other than newlines.

```bash
printf 'DIM amount\nSET result\nNOT amount AND result\n' | python tools/parse_program.py
```
