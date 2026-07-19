# Operator registry

This directory contains the executable operator model used by the reference
expression parser.

The language-symbol registry answers which spellings are operators. This
registry answers how those operators bind and evaluate.

The initial verified core contains:

| Operator | Fixity | Precedence | Associativity |
|---|---|---:|---|
| `AND` | infix | 10 | left |
| `OR` | infix | 10 | left |
| `NOT` | prefix | 20 | none |
| `^` | infix | 30 | left |

Higher numbers bind more strongly.

Validation:

```bash
python tools/validate_operators.py
```
