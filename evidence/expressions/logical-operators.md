# Logical Operators

> **Evidence level:** verified  
> **Scope:** `AND`, `OR`, and Boolean operand handling  
> **Practical classification:** warning

## Conclusion

`AND` and `OR`:

- require Boolean operands,
- have equal precedence,
- are left-associative,
- and do not short-circuit.

## Strict Boolean typing

Operands are not implicitly converted from numbers or strings to Boolean values
in the verified cases.

Expressions that provide incompatible operand types fail instead of applying
truthiness rules.

## No short-circuit evaluation

Both operands are evaluated.

This means that the right-hand side may raise an error even when the left-hand
side would already determine the result in a short-circuiting language.

Conceptual example:

```text
FALSE AND failing_expression
```

The right-hand expression is still evaluated.

Likewise:

```text
TRUE OR failing_expression
```

does not suppress evaluation of the right-hand expression.

## Equal precedence and left associativity

```text
A OR B AND C
```

is grouped as:

```text
(A OR B) AND C
```

## Recommendation

Do not use logical operators as guards for potentially failing expressions.
Perform validation in a separate expression or statement where possible.

Use parentheses in mixed `AND`/`OR` expressions.

## Specification impact

This evidence supports the logical-expression grammar and runtime evaluation
rules.

## Open questions

- Exact error categories for non-Boolean operands.
- Whether evaluation order is always strictly left-to-right.
