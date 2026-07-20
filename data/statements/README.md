# Statement registry

This directory contains the executable statement forms used by the reference program parser.

| Keyword | AST kind | Executable form | Status |
|---|---|---|---|
| `DIM` | `dim_statement` | `DIM name AS type [= expression]` | documented |
| `SET` | `set_statement` | `SET name TO expression` | documented |

The syntax is documentation-backed. Acceptance and detailed runtime semantics in a
specific MonKey Office build remain subject to experiments.

```bash
python tools/validate_statements.py
```
