# SPEC-STR-001: Trimming ASCII spaces

**Status:** verified  
**Supported by:** `EVD-0001`

`Trim(value)` returns `value` without leading or trailing ASCII space
characters. ASCII spaces between non-space characters are preserved.

The behaviour of tabs, line breaks, non-breaking spaces, and other Unicode
whitespace characters is not specified by this rule.
