# SPEC-STR-002: Left with a non-positive count

**Status:** verified for MonKey Office 2025 build 249  
**Supported by:** `EVD-0002`

For a character count of zero or less, `Left(value, count)` returns the empty
string in the verified interpreter build.

This rule remains build-scoped until the same behaviour has been checked in
additional versions.
