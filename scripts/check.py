#!/usr/bin/env python3
"""Safe, read-only conformance check command for Ideias Standard (S1-C01).

Follows CLI_CONTRACT.md and schemas/conformance-report.schema.json.
Exit codes:
  0: PASS (or WARN when not in --strict mode)
  1: FAIL (or WARN when in --strict mode)
  2: Operational error (missing file, unparseable input, CLI misuse)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from scripts.validate_standard import (
        ROOT,
        SCHEMA_FILES,
        current_version,
        self_check,
        validate,
    )
except ModuleNotFoundError:
    from validate_standard import (
        ROOT,
        SCHEMA_FILES,
        current_version,
        self_check,
        validate,
    )

COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"


def check_target(
    target: Path,
    kind: str | None = None,
    offline: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Perform read-only conformance validation against a target file or project."""
    if not target.exists():
        raise FileNotFoundError(f"Target path does not exist: {target}")

    if target.is_dir():
        manifest_json = target / "project-manifest.json"
        manifest_yaml = target / "project-manifest.yaml"
        manifest_yml = target / "project-manifest.yml"
        lock_json = target / "standard.lock"
        lock_json_alt = target / "standard-lock.json"
        lock_yaml = target / "standard.lock.yaml"
        lock_yml = target / "standard.lock.yml"
        lock_yaml_alt = target / "standard-lock.yaml"
        lock_yml_alt = target / "standard-lock.yml"

        context_json = target / "context-manifest.json"
        context_yaml = target / "context-manifest.yaml"
        context_yml = target / "context-manifest.yml"
        context_json_alt = target / "context.json"
        context_yaml_alt = target / "context.yaml"
        context_yml_alt = target / "context.yml"

        artifact_json = target / "artifact-policy.json"
        artifact_yaml = target / "artifact-policy.yaml"
        artifact_yml = target / "artifact-policy.yml"

        if kind == "standard-lock":
            if lock_json.exists():
                report = validate(lock_json.resolve(), "standard-lock")
            elif lock_json_alt.exists():
                report = validate(lock_json_alt.resolve(), "standard-lock")
            elif lock_yaml.exists():
                report = validate(lock_yaml.resolve(), "standard-lock")
            elif lock_yml.exists():
                report = validate(lock_yml.resolve(), "standard-lock")
            elif lock_yaml_alt.exists():
                report = validate(lock_yaml_alt.resolve(), "standard-lock")
            elif lock_yml_alt.exists():
                report = validate(lock_yml_alt.resolve(), "standard-lock")
            else:
                raise FileNotFoundError(f"Directory does not contain standard.lock or standard-lock.json: {target}")
        elif kind == "context-manifest":
            if context_json.exists():
                report = validate(context_json.resolve(), "context-manifest")
            elif context_yaml.exists():
                report = validate(context_yaml.resolve(), "context-manifest")
            elif context_yml.exists():
                report = validate(context_yml.resolve(), "context-manifest")
            elif context_json_alt.exists():
                report = validate(context_json_alt.resolve(), "context-manifest")
            elif context_yaml_alt.exists():
                report = validate(context_yaml_alt.resolve(), "context-manifest")
            elif context_yml_alt.exists():
                report = validate(context_yml_alt.resolve(), "context-manifest")
            else:
                raise FileNotFoundError(f"Directory does not contain context-manifest.json or context.json: {target}")
        elif kind == "artifact-policy":
            if artifact_json.exists():
                report = validate(artifact_json.resolve(), "artifact-policy")
            elif artifact_yaml.exists():
                report = validate(artifact_yaml.resolve(), "artifact-policy")
            elif artifact_yml.exists():
                report = validate(artifact_yml.resolve(), "artifact-policy")
            else:
                raise FileNotFoundError(f"Directory does not contain artifact-policy.json or artifact-policy.yaml: {target}")
        elif manifest_json.exists():
            report = validate(manifest_json.resolve(), kind or "project-manifest")
            if kind is None:
                from scripts.validate_standard import check_project_composition, load_json
                report["checks"].extend(check_project_composition([], target, load_json(manifest_json)))
                report["result"] = "FAIL" if any(c["status"] == "FAIL" for c in report["checks"]) else ("WARN" if any(c["status"] == "WARN" for c in report["checks"]) else "PASS")
        elif manifest_yaml.exists():
            report = validate(manifest_yaml.resolve(), kind or "project-manifest")
            if kind is None:
                from scripts.validate_standard import check_project_composition, load_yaml
                report["checks"].extend(check_project_composition([], target, load_yaml(manifest_yaml)))
                report["result"] = "FAIL" if any(c["status"] == "FAIL" for c in report["checks"]) else ("WARN" if any(c["status"] == "WARN" for c in report["checks"]) else "PASS")
        elif manifest_yml.exists():
            report = validate(manifest_yml.resolve(), kind or "project-manifest")
            if kind is None:
                from scripts.validate_standard import check_project_composition, load_yaml
                report["checks"].extend(check_project_composition([], target, load_yaml(manifest_yml)))
                report["result"] = "FAIL" if any(c["status"] == "FAIL" for c in report["checks"]) else ("WARN" if any(c["status"] == "WARN" for c in report["checks"]) else "PASS")
        elif lock_json.exists():
            report = validate(lock_json.resolve(), kind or "standard-lock")
        elif lock_json_alt.exists():
            report = validate(lock_json_alt.resolve(), kind or "standard-lock")
        elif lock_yaml.exists():
            report = validate(lock_yaml.resolve(), kind or "standard-lock")
        elif lock_yml.exists():
            report = validate(lock_yml.resolve(), kind or "standard-lock")
        elif lock_yaml_alt.exists():
            report = validate(lock_yaml_alt.resolve(), kind or "standard-lock")
        elif lock_yml_alt.exists():
            report = validate(lock_yml_alt.resolve(), kind or "standard-lock")
        elif context_json.exists():
            report = validate(context_json.resolve(), kind or "context-manifest")
        elif context_yaml.exists():
            report = validate(context_yaml.resolve(), kind or "context-manifest")
        elif context_yml.exists():
            report = validate(context_yml.resolve(), kind or "context-manifest")
        elif context_json_alt.exists():
            report = validate(context_json_alt.resolve(), kind or "context-manifest")
        elif context_yaml_alt.exists():
            report = validate(context_yaml_alt.resolve(), kind or "context-manifest")
        elif context_yml_alt.exists():
            report = validate(context_yml_alt.resolve(), kind or "context-manifest")
        elif artifact_json.exists():
            report = validate(artifact_json.resolve(), kind or "artifact-policy")
        elif artifact_yaml.exists():
            report = validate(artifact_yaml.resolve(), kind or "artifact-policy")
        elif artifact_yml.exists():
            report = validate(artifact_yml.resolve(), kind or "artifact-policy")
        elif (target / "VERSION").exists() and (target / "schemas").exists():
            report = self_check()
        else:
            raise ValueError(f"Directory does not contain a recognizable project-manifest, standard.lock, context-manifest, artifact-policy, or Standard root: {target}")
    else:
        report = validate(target.resolve(), kind)

    if offline:
        report["checks"].append({
            "code": "IS-CLI-002",
            "status": "PASS",
            "severity": "INFO",
            "message": "Offline execution active: validation performed strictly against local files with no network access",
            "path": None,
            "rationale": "Enforced by --offline flag",
        })
    if dry_run:
        report["checks"].append({
            "code": "IS-CLI-003",
            "status": "PASS",
            "severity": "INFO",
            "message": "Dry-run execution active: previewing conformance check without modifications or side effects",
            "path": None,
            "rationale": "Enforced by --dry-run flag",
        })

    return report


def determine_exit_code(report: dict[str, Any], strict: bool = False) -> int:
    """Determine exit code according to CLI_CONTRACT.md."""
    result = report.get("result")
    if result == "FAIL":
        return 1
    if result == "WARN":
        return 1 if strict else 0
    if result == "PASS":
        return 0
    return 2


def format_text_report(report: dict[str, Any], use_color: bool = True, details: bool = True) -> str:
    """Format report for human-readable terminal output."""
    result = report.get("result", "UNKNOWN")
    target = report.get("target", "UNKNOWN")

    if use_color:
        if result == "PASS":
            result_label = f"{COLOR_GREEN}PASS{COLOR_RESET}"
        elif result == "WARN":
            result_label = f"{COLOR_YELLOW}WARN{COLOR_RESET}"
        elif result == "FAIL":
            result_label = f"{COLOR_RED}FAIL{COLOR_RESET}"
        else:
            result_label = result
    else:
        result_label = result

    lines = [f"{result_label}: {target}"]
    checks = report.get("checks", []) if details else [c for c in report.get("checks", []) if c.get("status") in {"FAIL", "WARN"}]
    if not details and not checks:
        return f"{result_label}: {target} ({len(report.get('checks', []))} checks)"
    for check in checks:
        st = check.get("status", "UNKNOWN")
        code = check.get("code", "UNKNOWN")
        msg = check.get("message", "")
        path_info = f" ({check['path']})" if check.get("path") else ""

        if use_color:
            if st == "PASS":
                st_label = f"{COLOR_GREEN}{st}{COLOR_RESET}"
            elif st == "WARN":
                st_label = f"{COLOR_YELLOW}{st}{COLOR_RESET}"
            elif st == "FAIL":
                st_label = f"{COLOR_RED}{st}{COLOR_RESET}"
            else:
                st_label = f"{COLOR_CYAN}{st}{COLOR_RESET}"
        else:
            st_label = st

        lines.append(f"- {st_label} {code}: {msg}{path_info}")

    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="check",
        description="Validate structural and semantic conformance of Ideias Standard artifacts.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=None,
        help="Path to file or directory to check. Defaults to self-check if --self-check is passed, or project manifest.",
    )
    parser.add_argument(
        "--kind",
        choices=sorted(SCHEMA_FILES),
        help="Explicit document schema kind override.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit strictly structured JSON conforming to conformance-report.schema.json.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat WARN findings as policy failure (exit code 1) without altering canonical check status.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color codes in output.",
    )
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="Validate internal Standard schemas, catalogs, and references.",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Prohibit network access (check is offline by default).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview check execution (check is read-only by default).",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Show every check; default human output shows only failures and warnings.",
    )
    return parser


def run_check(
    path: Path | None = None,
    kind: str | None = None,
    as_json: bool = False,
    strict: bool = False,
    no_color: bool = False,
    is_self_check: bool = False,
    offline: bool = False,
    dry_run: bool = False,
    details: bool = True,
) -> tuple[int, str]:
    """Execute check command and return (exit_code, output_string)."""
    target_display = str(path) if path is not None else ("SELF" if is_self_check else "DEFAULT")
    version_str = None
    try:
        version_str = current_version()
    except Exception:
        pass

    try:
        if is_self_check:
            report = self_check()
            if offline:
                report["checks"].append({
                    "code": "IS-CLI-002",
                    "status": "PASS",
                    "severity": "INFO",
                    "message": "Offline execution active: validation performed strictly against local files with no network access",
                    "path": None,
                    "rationale": "Enforced by --offline flag",
                })
            if dry_run:
                report["checks"].append({
                    "code": "IS-CLI-003",
                    "status": "PASS",
                    "severity": "INFO",
                    "message": "Dry-run execution active: previewing conformance check without modifications or side effects",
                    "path": None,
                    "rationale": "Enforced by --dry-run flag",
                })
        elif path is not None:
            report = check_target(path, kind, offline=offline, dry_run=dry_run)
        else:
            # Default to checking current directory
            report = check_target(Path.cwd(), kind, offline=offline, dry_run=dry_run)

        exit_code = determine_exit_code(report, strict=strict)
    except Exception as exc:
        report = {
            "schema_version": "0.1",
            "target": target_display,
            "standard_version": version_str,
            "result": "FAIL",
            "checks": [
                {
                    "code": "IS-CLI-001",
                    "status": "FAIL",
                    "severity": "HIGH",
                    "message": str(exc) if str(exc) else exc.__class__.__name__,
                    "path": None,
                    "rationale": "Operational error; see CLI_CONTRACT.md",
                }
            ],
        }
        exit_code = 2

    if as_json:
        output = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        use_color = (
            not no_color
            and "NO_COLOR" not in os.environ
            and hasattr(sys.stdout, "isatty")
            and sys.stdout.isatty()
        )
        output = format_text_report(report, use_color=use_color, details=details)

    return exit_code, output


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if not args.self_check and args.path is None:
        # Check current directory if no path and not self-check
        args.path = Path.cwd()

    exit_code, output = run_check(
        path=args.path if not args.self_check else None,
        kind=args.kind,
        as_json=args.as_json,
        strict=args.strict,
        no_color=args.no_color,
        is_self_check=args.self_check,
        offline=args.offline,
        dry_run=args.dry_run,
        details=args.details,
    )
    print(output)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
