# Grammar Status Notes

> **Status:** Working draft accompanying `monkey-office.ebnf`

This document records which parts of the grammar are considered verified,
inferred, or provisional.

## Verified

- `^` binds more strongly than `*` and `/`.
- `*` and `/` bind more strongly than `+` and `-`.
- Arithmetic operators are left-associative.
- Comparisons bind more strongly than logical operators.
- `AND` and `OR` have equal precedence and are left-associative.
- Parentheses create an expression boundary.
- `NOT` consumes the complete following logical expression inside the current
  parenthesized expression.
- Function calls use parentheses and comma-separated arguments.
- The decimal separator is a comma in the tested locale.

## Inferred

- Function calls are parsed as primary expressions.
- Comparison expressions currently allow at most one comparison operator.
- The parser can be represented by the layered non-terminals used in the EBNF.

## Provisional

- Complete statement syntax.
- Exact statement terminators.
- Type-annotation syntax.
- Identifier character set.
- String escaping.
- Exponent notation.
- Whether unary `+` and `-` belong to the literal grammar or expression grammar.
- Whether chained comparisons are syntactically rejected or evaluated in some
  other way.

## Important implementation note

The rule

```ebnf
not-expression = "NOT" , logical-expression ;
```

is intentional.

It models the verified wide scope of `NOT`. It must not be replaced with the
more conventional form

```ebnf
not-expression = "NOT" , primary-expression ;
```

because that would produce incorrect trees for expressions such as:

```text
NOT 1 = 1 OR TRUE
```

## Next validation targets

1. Unary minus versus power expressions.
2. Chained comparisons.
3. Exact declaration syntax.
4. Exact statement separators.
5. String delimiters and escapes.
6. Identifier case rules and valid characters.
