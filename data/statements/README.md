# Statement registry

This directory contains the executable statement forms used by the reference program parser.

| Keyword | AST kind | Executable form | Status |
|---|---|---|---|
| `DIM` | `dim_statement` | keyword + identifier | inferred |
| `SET` | `set_statement` | keyword + identifier | inferred |

These forms are parser scaffolding and remain experimentally unverified.

```bash
python tools/validate_statements.py
```
