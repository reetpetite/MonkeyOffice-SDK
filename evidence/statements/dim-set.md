# Documented DIM and SET syntax

## Status

Documented in the official MonKey Office scripting-language material available to this project.
Runtime acceptance in build 249 remains a separate experimental question.

## Declaration

```text
dim Name as Datentyp [= Wert]
```

The type clause is mandatory in the documented form. An initializer is optional.

## Assignment

```text
set Variable to Wert
```

`SET` is a statement and uses `TO` between the target name and the value expression.

## Consequences for the reference implementation

- `AS` and `TO` are registered as documented keywords.
- The program parser accepts `DIM name AS type [= expression]`.
- The program parser accepts `SET name TO expression`.
- These documentation-backed forms replace the earlier parser scaffolding
  `DIM name` and `SET name`.
