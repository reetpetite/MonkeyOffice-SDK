# Operator Precedence and Associativity

> **Evidence level:** verified  
> **Scope:** arithmetic, comparison, and logical expressions  
> **Practical classification:** warning

## Conclusion

The verified precedence order, from strongest to weakest, is:

1. parenthesized expressions,
2. `^`,
3. `*` and `/`,
4. `+` and `-`,
5. comparison operators,
6. `AND` and `OR`.

The arithmetic operators tested so far are left-associative. `AND` and `OR`
have equal precedence and are also left-associative.

## Verified rules

```text
^
* /
+ -
comparisons
AND OR
```

### Power is left-associative

```text
2 ^ 3 ^ 2
```

is evaluated as:

```text
(2 ^ 3) ^ 2
```

not as:

```text
2 ^ (3 ^ 2)
```

### Multiplication and division are left-associative

```text
8 / 4 / 2
```

is evaluated as:

```text
(8 / 4) / 2
```

### Addition and subtraction are left-associative

```text
10 - 3 - 2
```

is evaluated as:

```text
(10 - 3) - 2
```

### Comparisons bind more strongly than logical operators

A comparison is formed before surrounding `AND` or `OR` operations are applied.

### `AND` and `OR` have equal precedence

```text
TRUE OR FALSE AND FALSE
```

is evaluated as:

```text
(TRUE OR FALSE) AND FALSE
```

## Recommendation

Authors should use parentheses whenever an expression combines `AND` and `OR`.
The language behaviour differs from many mainstream programming languages and
is easy to misread.

## Specification impact

This evidence supports:

- `spec/expressions.md`
- `spec/grammar/monkey-office.ebnf`
- `model/ast.md`

## Open questions

- Unary minus relative to power expressions.
- Whether chained comparisons are accepted.
- Whether additional operators exist.
