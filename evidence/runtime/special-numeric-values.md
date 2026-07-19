# Special Numeric Values

> **Evidence level:** verified  
> **Scope:** `Na`, infinities, signed zero, comparisons, and division  
> **Practical classification:** warning

## Runtime values

The interpreter exposes behaviour corresponding to:

```text
Na
inf
-inf
+0
-0
```

The spelling shown here describes observed values and output. Literal syntax for
constructing every value directly is a separate question.

## Division by zero

The division operator and the `DIV()` function behave differently.

```text
1 / 0
```

raises a runtime error.

```text
DIV(1, 0)
```

returns positive infinity in the verified case.

This distinction is observable and must be preserved by compatible tooling.

## Comparisons involving `Na`

Whenever either operand is `Na`, every tested comparison operator returns
`FALSE`:

```text
=
<>
<
<=
>
>=
```

This includes:

```text
Na <> Na
```

which also evaluates to `FALSE`.

This differs from the common IEEE-style expectation that “not equal” involving
NaN is true. Compatible implementations must reproduce the observed language
behaviour rather than substitute host-language comparison semantics.

## Arithmetic propagation

Arithmetic involving `Na` and infinities follows the verified result patterns
recorded by the experiments. A future conformance table should enumerate each
tested operator/value combination explicitly.

## Signed zero

Positive and negative zero are distinguishable in some operations and output
paths.

A serialized AST or conformance-result format must not collapse `-0` into `0`.

## Implementation warning

Languages such as JavaScript, Python, and JSON differ in how they serialize or
compare non-finite values and negative zero.

Implementations must introduce an explicit representation instead of relying
blindly on host-language defaults.

## Specification impact

This evidence supports:

- the numeric-value model,
- comparison semantics,
- division semantics,
- AST serialization requirements,
- and future conformance tests.

## Open questions

- Complete arithmetic tables for all operators.
- String conversion of each special value.
- Ordering behaviour in library functions.
- Exact origins and spellings of `Na`, `inf`, and `-inf`.
