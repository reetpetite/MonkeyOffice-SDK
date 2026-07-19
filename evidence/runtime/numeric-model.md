# Numeric Runtime Model

> **Evidence level:** verified  
> **Scope:** numeric parsing and arithmetic  
> **Practical classification:** warning

## Conclusion

The tested interpreter behaviour is consistent with IEEE-754 binary64
floating-point values.

This conclusion is based on observable behaviour, including:

- decimal-to-binary rounding,
- parser tie handling,
- the exact integer boundary around `2^53`,
- signed zero,
- infinities,
- and `Na`.

The evidence establishes the externally observable numeric model. It does not by
itself prove a particular internal implementation type.

## Exact integer boundary

Binary64 represents every integer exactly only through the usual exact range
around `2^53`.

Adjacent integer literals beyond that boundary may parse to the same runtime
value.

## Parser rounding

Decimal literals are rounded to the nearest representable binary64 value.

Tie cases observed during literal parsing are consistent with round-to-nearest,
ties-to-even.

## Arithmetic rounding

Arithmetic exhibits the rounding effects expected from binary floating-point.
Decimal fractions that appear exact in source may not have exact internal
representations.

## Decimal separator

The tested locale uses a comma as the decimal separator.

This is a lexical property and may be locale-dependent. The repository must
record the locale and build used for experiments involving numeric literals.

## Specification guidance

The specification should define verified observable results and avoid claiming
an internal C, Objective-C, Swift, or database type without separate evidence.

## Recommendation

Do not compare calculated non-integer values for exact equality unless the
runtime behaviour is intentionally relied upon.

Conformance tests should include values around:

- zero,
- `2^53`,
- halfway parser cases,
- overflow,
- underflow,
- and non-finite results.

## Open questions

- Subnormal-value handling.
- Overflow during literal parsing.
- Underflow and gradual underflow.
- Rounding mode for every arithmetic operation.
- Locale dependence of exponent and decimal syntax.
