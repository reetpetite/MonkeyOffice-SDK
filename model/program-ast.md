# Program AST

`tools/parse_program.py` extends the reference implementation from isolated expressions to a line-oriented program.

```text
program := (blank-line | statement newline?)*
statement := dim-statement | set-statement | expression-statement
dim-statement := DIM identifier AS type-name (= expression)?
set-statement := SET identifier TO expression
expression-statement := expression
```

The concrete `DIM` and `SET` forms are documented. Runtime acceptance and semantic
details must still be recorded per tested MonKey Office build.

Example:

```text
DIM amount AS number = 5
SET amount TO 10
NOT amount AND result
```

The parser dispatches by stable symbol IDs from `data/statements/registry.json`,
not by source spelling. It does not yet implement calls, blocks, conditions,
loops, comments, or statement separators other than newlines.

```bash
printf 'DIM amount AS number = 5\nSET amount TO 10\nNOT amount AND result\n' | python tools/parse_program.py
```
