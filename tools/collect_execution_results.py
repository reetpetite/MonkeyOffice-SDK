#!/usr/bin/env python3
"""Record manually observed MonKey Office experiment results."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "runner" / "execution-manifest.yaml"
ALLOWED_STATUSES = {
    "not-run",
    "accepted",
    "parser-error",
    "runtime-error",
    "unexpected-output",
    "crash",
    "hang",
    "skipped",
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in {path}")
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)


def load_manifest() -> dict[str, Any]:
    return load_yaml(MANIFEST_PATH)


def experiment_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in manifest.get("experiments", [])}


def result_path(experiment: dict[str, Any], build: int) -> Path:
    return ROOT / experiment["result_pattern"].format(build=build)


def report_path(experiment: dict[str, Any], build: int) -> Path:
    return ROOT / experiment["report_pattern"].format(build=build)


def fresh_result(experiment: dict[str, Any], build: int) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "experiment": experiment["id"],
        "build": build,
        "recorded_at": None,
        "environment": {
            "product_version": None,
            "operating_system": None,
            "locale": None,
            "notes": None,
        },
        "complete": False,
        "cases": {
            case["id"]: {
                "status": "not-run",
                "success_signal": None,
                "message": None,
                "notes": None,
            }
            for case in experiment["cases"]
        },
    }


def load_or_create(experiment: dict[str, Any], build: int) -> tuple[Path, dict[str, Any]]:
    path = result_path(experiment, build)
    if path.exists():
        return path, load_yaml(path)
    return path, fresh_result(experiment, build)


def update_completion(data: dict[str, Any]) -> None:
    statuses = [case.get("status") for case in data.get("cases", {}).values()]
    data["complete"] = bool(statuses) and all(status != "not-run" for status in statuses)
    data["recorded_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")


def require_experiment(manifest: dict[str, Any], experiment_id: str) -> dict[str, Any]:
    experiments = experiment_map(manifest)
    if experiment_id not in experiments:
        raise ValueError(f"Unknown experiment: {experiment_id}")
    return experiments[experiment_id]


def cmd_init(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    created = 0
    for experiment in manifest["experiments"]:
        path = result_path(experiment, args.build)
        if path.exists() and not args.force:
            print(f"exists:  {path.relative_to(ROOT)}")
            continue
        write_yaml(path, fresh_result(experiment, args.build))
        print(f"created: {path.relative_to(ROOT)}")
        created += 1
    print(f"Initialized {created} result file(s).")
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    if args.status not in ALLOWED_STATUSES - {"not-run"}:
        raise ValueError(f"Status cannot be recorded: {args.status}")
    if args.status == "accepted" and not args.success_signal:
        raise ValueError("accepted requires --success-signal")
    if args.status == "skipped" and not args.notes:
        raise ValueError("skipped requires --notes")

    manifest = load_manifest()
    experiment = require_experiment(manifest, args.experiment)
    known_cases = {case["id"] for case in experiment["cases"]}
    if args.case not in known_cases:
        raise ValueError(f"Unknown case {args.case} for {args.experiment}")

    path, data = load_or_create(experiment, args.build)
    data["cases"][args.case] = {
        "status": args.status,
        "success_signal": args.success_signal,
        "message": args.message,
        "notes": args.notes,
    }
    update_completion(data)
    write_yaml(path, data)
    print(f"Recorded {args.experiment}/{args.case}: {args.status}")
    print(path.relative_to(ROOT))
    return 0


def cmd_environment(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    experiment = require_experiment(manifest, args.experiment)
    path, data = load_or_create(experiment, args.build)
    environment = data.setdefault("environment", {})
    for key in ("product_version", "operating_system", "locale", "notes"):
        value = getattr(args, key)
        if value is not None:
            environment[key] = value
    update_completion(data)
    write_yaml(path, data)
    print(f"Updated environment for {args.experiment} build {args.build}.")
    return 0


def observation_text(case: dict[str, Any]) -> str:
    values = []
    if case.get("success_signal"):
        values.append(f"`{case['success_signal']}`")
    if case.get("message"):
        values.append(str(case["message"]).replace("\n", "<br>"))
    if case.get("notes"):
        values.append(str(case["notes"]).replace("\n", "<br>"))
    return " — ".join(values) if values else "—"


def render_report(experiment: dict[str, Any], data: dict[str, Any]) -> str:
    env = data.get("environment", {})
    lines = [
        f"# {experiment['id']} — Build {data['build']}",
        "",
        f"- Product version: {env.get('product_version') or 'not recorded'}",
        f"- Operating system: {env.get('operating_system') or 'not recorded'}",
        f"- Locale: {env.get('locale') or 'not recorded'}",
        f"- Completion: {'complete' if data.get('complete') else 'incomplete'}",
        "",
        "| Case | Status | Observation |",
        "|------|--------|-------------|",
    ]
    for case in experiment["cases"]:
        result = data["cases"][case["id"]]
        lines.append(
            f"| {case['id']} | {result['status']} | {observation_text(result)} |"
        )
    if env.get("notes"):
        lines.extend(["", "## Environment notes", "", str(env["notes"])])
    return "\n".join(lines) + "\n"


def cmd_report(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    rendered = 0
    selected = manifest["experiments"]
    if args.experiment:
        selected = [require_experiment(manifest, args.experiment)]
    for experiment in selected:
        source = result_path(experiment, args.build)
        if not source.exists():
            print(f"missing: {source.relative_to(ROOT)}")
            continue
        data = load_yaml(source)
        destination = report_path(experiment, args.build)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_report(experiment, data), encoding="utf-8", newline="\n")
        print(f"rendered: {destination.relative_to(ROOT)}")
        rendered += 1
    print(f"Rendered {rendered} report(s).")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    total = completed = observed = 0
    for experiment in manifest["experiments"]:
        path = result_path(experiment, args.build)
        case_count = len(experiment["cases"])
        total += case_count
        if not path.exists():
            print(f"{experiment['id']}: 0/{case_count} (not initialized)")
            continue
        data = load_yaml(path)
        count = sum(
            case.get("status") != "not-run" for case in data.get("cases", {}).values()
        )
        observed += count
        if data.get("complete"):
            completed += 1
        print(f"{experiment['id']}: {count}/{case_count}")
    print(
        f"Overall: {observed}/{total} cases resolved; "
        f"{completed}/{len(manifest['experiments'])} experiments complete."
    )
    return 0


def parser() -> argparse.ArgumentParser:
    manifest = load_manifest()
    default_build = int(manifest.get("default_build", 249))
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create empty observation files")
    init.add_argument("--build", type=int, default=default_build)
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)

    record = sub.add_parser("record", help="Record one observed case")
    record.add_argument("experiment")
    record.add_argument("case")
    record.add_argument("--build", type=int, default=default_build)
    record.add_argument("--status", required=True, choices=sorted(ALLOWED_STATUSES - {"not-run"}))
    record.add_argument("--success-signal")
    record.add_argument("--message")
    record.add_argument("--notes")
    record.set_defaults(func=cmd_record)

    environment = sub.add_parser("environment", help="Record execution environment")
    environment.add_argument("experiment")
    environment.add_argument("--build", type=int, default=default_build)
    environment.add_argument("--product-version")
    environment.add_argument("--operating-system")
    environment.add_argument("--locale")
    environment.add_argument("--notes")
    environment.set_defaults(func=cmd_environment)

    report = sub.add_parser("report", help="Render Markdown reports")
    report.add_argument("--build", type=int, default=default_build)
    report.add_argument("--experiment")
    report.set_defaults(func=cmd_report)

    status = sub.add_parser("status", help="Show execution progress")
    status.add_argument("--build", type=int, default=default_build)
    status.set_defaults(func=cmd_status)
    return root


def main() -> int:
    try:
        args = parser().parse_args()
        return args.func(args)
    except (OSError, ValueError, KeyError, yaml.YAMLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
