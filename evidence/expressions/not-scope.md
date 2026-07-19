# Scope of `NOT`

> **Evidence level:** verified  
> **Scope:** parsing of logical expressions  
> **Practical classification:** warning

## Conclusion

`NOT` is represented semantically as a unary operation, but it does not consume
only the immediately following primary expression.

Instead, it consumes the complete following logical expression within the
current parenthesized expression.

## Verified examples

```text
NOT 1 = 1
```

behaves as:

```text
NOT (1 = 1)
```

```text
NOT 1 = 1 OR TRUE
```

behaves as:

```text
NOT ((1 = 1) OR TRUE)
```

```text
TRUE AND NOT FALSE OR FALSE
```

behaves as:

```text
TRUE AND (NOT (FALSE OR FALSE))
```

Multiple `NOT` operators follow the same scope rule:

```text
NOT NOT TRUE OR FALSE
```

behaves consistently with:

```text
NOT (NOT (TRUE OR FALSE))
```

## Parentheses terminate the scope

An enclosing or explicitly inserted parenthesized expression defines the
boundary of the operand consumed by `NOT`.

## Parser model

The working grammar models this as:

```ebnf
not-expression = "NOT" , logical-expression ;
```

The resulting AST may still use a conventional unary node:

```text
UnaryExpression(NOT)
└── operand
```

The unusual behaviour belongs to parsing, not to the AST node shape.

## Recommendation

Always parenthesize the intended operand of `NOT`.

Preferred:

```text
NOT (condition)
```

Avoid relying on implicit scope in production import scripts.

## Supporting experiments

Historical experiments include:

- MO-081
- MO-082
- MO-083
- MO-084
- MO-085
- MO-086

These identifiers should be linked to concrete repository experiments when those
records are imported.

## Specification impact

This evidence supports:

- `spec/expressions.md`
- `spec/grammar/monkey-office.ebnf`
- `model/ast.md`
