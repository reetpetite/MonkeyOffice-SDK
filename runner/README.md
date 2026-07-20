# Interpreter execution harness

This directory contains the human-operated execution harness for MonKey Office
interpreter experiments. It does not automate MonKey Office itself. Instead, it
creates deterministic result files, records one observation at a time, and
renders reviewable Markdown reports.

## Safety boundary

The harness never treats an expected result as an observation. A case starts as
`not-run` and changes only through an explicit recording action after the exact
script has been executed in MonKey Office.

Allowed case statuses are:

- `not-run` — no observation has been made
- `accepted` — the script reached its unique success signal
- `parser-error` — parsing or compilation failed before execution
- `runtime-error` — execution began but failed before the success signal
- `unexpected-output` — execution completed with a different observable result
- `crash` — MonKey Office terminated abnormally
- `hang` — execution did not complete within the chosen observation window
- `skipped` — deliberately not executed, with a reason in `notes`

## Typical workflow

Initialize result files for the target build:

```bash
python tools/collect_execution_results.py init --build 249
```

Run a script manually in MonKey Office, then record exactly what happened:

```bash
python tools/collect_execution_results.py record \
  MO-030 D01 --build 249 --status accepted \
  --success-signal 'MO-030|D01=accepted'
```

For an error, preserve the message verbatim where possible:

```bash
python tools/collect_execution_results.py record \
  MO-030 D03 --build 249 --status parser-error \
  --message 'Unexpected token ,'
```

Add environment metadata once per experiment result:

```bash
python tools/collect_execution_results.py environment \
  MO-030 --build 249 \
  --product-version 'MonKey Office 2026' \
  --operating-system 'macOS 26.5.2' \
  --locale 'de-DE'
```

Inspect progress and render reports:

```bash
python tools/collect_execution_results.py status --build 249
python tools/collect_execution_results.py report --build 249
```

The `complete` field becomes true only when no case remains `not-run`. A skipped
case therefore counts as deliberately resolved but must carry a reason.

## Files

The manifest is [`execution-manifest.yaml`](execution-manifest.yaml). Result and
report locations are declared there with `{build}` placeholders. The command
line tool writes only to those declared locations.
