# Diagnostic Model

> Status: Working design

## Purpose

Diagnostics are stable, machine-readable reports produced by the lexer, parser,
semantic analyzer, validator, formatter, runtime adapter, and repository tools.

A diagnostic must be useful in three contexts:

- command-line output
- automated tests
- editor and language-server integration

## Design goals

- stable identifiers
- deterministic ordering
- precise source locations
- separation of severity from category
- optional related locations
- optional machine-applicable fixes
- compatibility with future language versions

## Diagnostic identity

Every diagnostic has a stable code.

Format:

```text
MO-<SUBSYSTEM>-<NUMBER>
```

Subsystem prefixes:

| Prefix | Subsystem |
|---|---|
| `LEX` | Lexer |
| `PAR` | Parser |
| `SEM` | Semantic analysis |
| `FMT` | Formatter |
| `RUN` | Runtime adapter |
| `CFG` | Repository/configuration tooling |

Examples:

```text
MO-LEX-0001
MO-PAR-0001
MO-SEM-0001
```

Codes are never reassigned after publication. A retired diagnostic remains
reserved and is marked deprecated in the registry.

## Severity

Supported severities:

- `error`
- `warning`
- `information`
- `hint`

Severity describes presentation and build impact. It does not replace the
diagnostic category.

Default policy:

- errors fail validation or compilation
- warnings do not fail by default
- information and hints never fail by default

Tools may offer stricter policies, but the emitted diagnostic retains its
canonical severity.

## Diagnostic structure

```text
Diagnostic
├── code
├── severity
├── message
├── primaryRange
├── relatedInformation[]
├── fixes[]
├── phase
├── languageVersion
└── metadata
```

## Source ranges

Ranges are half-open:

```text
[start, end)
```

Each position stores:

- UTF-8 byte offset
- line
- column

Line and column are 1-based in user-facing output.

Internal implementations may also track UTF-16 columns for Language Server
Protocol conversion, but the canonical model remains independent of LSP.

## Primary and related locations

Every source diagnostic has one primary range.

Related information may point to:

- the original declaration
- another conflicting declaration
- the matching opening delimiter
- the evidence source for a build-specific rule

A repository-level diagnostic may omit a source range only when no source file
exists.

## Messages

Messages should:

- describe the problem, not the implementation
- avoid unstable wording in identifiers
- mention the unexpected token or value where helpful
- avoid embedding absolute paths when a repository-relative path is available

Tests should normally assert the diagnostic code and range. Exact message text
may be asserted when wording is part of the public interface.

## Fixes

A diagnostic may expose zero or more fixes.

```text
Fix
├── title
├── applicability
└── edits[]
```

Applicability:

- `automatic`: safe without user review
- `suggested`: requires user review
- `unsafe`: may change program meaning

An edit contains:

- source file
- replacement range
- replacement text

Edits within one fix must not overlap.

## Deterministic ordering

Diagnostics are sorted by:

1. source file
2. primary start offset
3. primary end offset
4. severity rank
5. diagnostic code
6. message

Recommended severity rank:

```text
error < warning < information < hint
```

## Recovery diagnostics

The parser may emit one root diagnostic and suppress secondary cascades caused by
the same missing token.

Suppression must not hide diagnostics that are independently actionable.

## Versioning

Each diagnostic registry entry may declare:

- `introducedIn`
- `deprecatedIn`
- `removedIn`
- supported build range

The diagnostic code remains reserved even after removal.

## Registry

The machine-readable registry lives in:

```text
data/diagnostics/registry.json
```

Its schema lives in:

```text
data/diagnostics/schema.json
```

The registry is the canonical source for:

- code ownership
- default severity
- summary
- lifecycle status
- documentation links

## Initial diagnostic families

### Lexer

- invalid character
- unterminated string literal
- malformed numeric literal

### Parser

- unexpected token
- expected token
- unmatched closing parenthesis
- missing closing parenthesis

### Semantic analysis

- unknown identifier
- duplicate declaration
- type mismatch
- invalid assignment target
- wrong function arity

### Runtime adapter

- division by zero
- unsupported host function
- build-specific incompatibility

## Testing

Diagnostic tests should assert:

- code
- severity
- primary range
- related ranges
- fix applicability
- replacement edits
- deterministic ordering

Conformance tests may optionally declare expected diagnostics using this model.

## Language Server Protocol mapping

The SDK model maps cleanly to LSP diagnostics:

| SDK | LSP |
|---|---|
| `error` | `DiagnosticSeverity.Error` |
| `warning` | `DiagnosticSeverity.Warning` |
| `information` | `DiagnosticSeverity.Information` |
| `hint` | `DiagnosticSeverity.Hint` |

The SDK must not store LSP-specific numeric enums in canonical data.

## Open questions

The following remain evidence- or implementation-driven:

- whether columns count Unicode scalar values or grapheme clusters in CLI output
- whether warnings should fail CI in strict mode
- whether runtime diagnostics can always be tied to source ranges
- whether build-specific host errors need a separate namespace
