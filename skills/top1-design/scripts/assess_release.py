#!/usr/bin/env python3
"""Assess a candidate against the auditable TOP1 DESIGN release bar."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from score_design import EvaluationError, score_report


CHECK_FAMILIES = {
    "visual",
    "interaction",
    "responsive",
    "accessibility",
    "functional",
}
CHECK_STATUSES = {"pass", "fail", "not_applicable"}
DEFECT_SEVERITIES = {"blocker", "severe", "moderate", "minor"}
DEFECT_STATUSES = {"open", "fixed", "accepted_risk"}
CHANGE_CONTROL_KEYS = {
    "within_authority",
    "tests_passed",
    "blast_radius_reviewed",
    "rollback_ready",
}


class ReleaseError(ValueError):
    """Raised when release evidence is structurally invalid."""


def _strings(value: Any, label: str, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise ReleaseError(f"{label} must be a list")
    if any(not isinstance(item, str) or not item for item in value):
        raise ReleaseError(f"{label} entries must be non-empty strings")
    if not allow_empty and not value:
        raise ReleaseError(f"{label} must not be empty")
    return value


def validate_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("schema_version") != "1.0":
        raise ReleaseError('schema_version must be "1.0"')
    evaluation = manifest.get("evaluation")
    if not isinstance(evaluation, (str, dict)):
        raise ReleaseError("evaluation must be a path or evaluation object")
    coverage = manifest.get("coverage")
    if not isinstance(coverage, dict):
        raise ReleaseError("coverage must be an object")
    for key in (
        "required_check_families",
        "required_viewports",
        "required_flows",
        "required_states",
        "required_accessibility_methods",
    ):
        _strings(coverage.get(key), f"coverage.{key}", allow_empty=key != "required_check_families")
    unknown_families = set(coverage["required_check_families"]) - CHECK_FAMILIES
    if unknown_families:
        raise ReleaseError(
            "unknown required check families: " + ", ".join(sorted(unknown_families))
        )

    checks = manifest.get("checks")
    if not isinstance(checks, list) or not checks:
        raise ReleaseError("checks must be a non-empty list")
    check_ids: set[str] = set()
    for index, check in enumerate(checks):
        label = f"checks[{index}]"
        if not isinstance(check, dict):
            raise ReleaseError(f"{label} must be an object")
        check_id = check.get("id")
        if not isinstance(check_id, str) or not check_id:
            raise ReleaseError(f"{label}.id must be a non-empty string")
        if check_id in check_ids:
            raise ReleaseError(f"duplicate check id: {check_id}")
        check_ids.add(check_id)
        if check.get("family") not in CHECK_FAMILIES:
            raise ReleaseError(f"{label}.family is invalid")
        if check.get("status") not in CHECK_STATUSES:
            raise ReleaseError(f"{label}.status is invalid")
        _strings(check.get("evidence"), f"{label}.evidence", allow_empty=True)
        if "required" in check and not isinstance(check["required"], bool):
            raise ReleaseError(f"{label}.required must be boolean")

    defects = manifest.get("defects", [])
    if not isinstance(defects, list):
        raise ReleaseError("defects must be a list")
    defect_ids: set[str] = set()
    for index, defect in enumerate(defects):
        label = f"defects[{index}]"
        if not isinstance(defect, dict):
            raise ReleaseError(f"{label} must be an object")
        defect_id = defect.get("id")
        if not isinstance(defect_id, str) or not defect_id:
            raise ReleaseError(f"{label}.id must be a non-empty string")
        if defect_id in defect_ids:
            raise ReleaseError(f"duplicate defect id: {defect_id}")
        defect_ids.add(defect_id)
        if defect.get("family") not in CHECK_FAMILIES:
            raise ReleaseError(f"{label}.family is invalid")
        if defect.get("severity") not in DEFECT_SEVERITIES:
            raise ReleaseError(f"{label}.severity is invalid")
        if defect.get("status") not in DEFECT_STATUSES:
            raise ReleaseError(f"{label}.status is invalid")
        _strings(defect.get("evidence"), f"{label}.evidence", allow_empty=True)

    control = manifest.get("change_control")
    if not isinstance(control, dict):
        raise ReleaseError("change_control must be an object")
    for key in CHANGE_CONTROL_KEYS:
        if not isinstance(control.get(key), bool):
            raise ReleaseError(f"change_control.{key} must be boolean")


def _load_evaluation(manifest: dict[str, Any], base: Path) -> dict[str, Any]:
    evaluation = manifest["evaluation"]
    if isinstance(evaluation, dict):
        return evaluation
    path = Path(evaluation)
    if not path.is_absolute():
        path = base / path
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReleaseError(f"cannot read evaluation: {exc}") from exc
    if not isinstance(value, dict):
        raise ReleaseError("evaluation must contain a JSON object")
    return value


def _coverage_gate(
    checks: list[dict[str, Any]],
    family: str,
    field: str | None = None,
    required_values: list[str] | None = None,
) -> tuple[bool, list[str]]:
    candidates = [
        check
        for check in checks
        if check["family"] == family and check.get("required", True)
    ]
    failures: list[str] = []
    if not candidates:
        return False, [f"no required {family} check"]
    for check in candidates:
        if check["status"] != "pass":
            failures.append(f"{check['id']} is {check['status']}")
        if not check["evidence"]:
            failures.append(f"{check['id']} has no evidence")
    for value in required_values or []:
        matching = [
            check
            for check in candidates
            if check.get(field) == value
            and check["status"] == "pass"
            and check["evidence"]
        ]
        if not matching:
            failures.append(f"missing passing {family} evidence for {field}={value}")
    return not failures, failures


def assess_release(
    manifest: dict[str, Any],
    base: Path = Path("."),
) -> dict[str, Any]:
    validate_manifest(manifest)
    evaluation = _load_evaluation(manifest, base)
    scored = score_report(evaluation)
    coverage = manifest["coverage"]
    checks = manifest["checks"]
    gate_results: list[dict[str, Any]] = []

    def add_gate(gate: str, passed: bool, reasons: list[str]) -> None:
        gate_results.append({"gate": gate, "passed": passed, "reasons": reasons})

    add_gate(
        "recursive_score",
        scored["release_status"] == "release_candidate",
        []
        if scored["release_status"] == "release_candidate"
        else [
            "score report is not release_candidate",
            f"next action: {scored.get('next_action')}",
        ],
    )

    family_dimensions = {
        "responsive": ("viewport", coverage["required_viewports"]),
        "functional": ("flow", coverage["required_flows"]),
        "interaction": ("state", coverage["required_states"]),
        "accessibility": ("method", coverage["required_accessibility_methods"]),
        "visual": (None, []),
    }
    for family in coverage["required_check_families"]:
        field, values = family_dimensions[family]
        passed, reasons = _coverage_gate(checks, family, field, values)
        add_gate(f"{family}_evidence", passed, reasons)

    unresolved_severe = [
        defect
        for defect in manifest.get("defects", [])
        if defect["severity"] in {"blocker", "severe"} and defect["status"] != "fixed"
    ]
    add_gate(
        "severe_defects",
        not unresolved_severe,
        [
            f"{defect['id']} ({defect['family']}, {defect['severity']}, {defect['status']})"
            for defect in unresolved_severe
        ],
    )

    control_failures = [
        key for key in sorted(CHANGE_CONTROL_KEYS) if manifest["change_control"][key] is not True
    ]
    add_gate(
        "change_control",
        not control_failures,
        [f"{key} is not verified" for key in control_failures],
    )

    passed = all(gate["passed"] for gate in gate_results)
    blocking_reasons = [
        f"{gate['gate']}: {reason}"
        for gate in gate_results
        if not gate["passed"]
        for reason in gate["reasons"]
    ]
    return {
        "schema_version": "1.0",
        "run_id": manifest.get("run_id") or scored.get("run_id"),
        "release_status": "release_candidate" if passed else "not_releasable",
        "release_bar_met": passed,
        "score_release_status": scored["release_status"],
        "gate_results": gate_results,
        "blocking_reasons": blocking_reasons,
        "defect_summary": {
            severity: sum(
                defect["severity"] == severity and defect["status"] != "fixed"
                for defect in manifest.get("defects", [])
            )
            for severity in sorted(DEFECT_SEVERITIES)
        },
        "score_report": scored,
        "claim_boundary": (
            "Passing means this candidate met the declared release evidence bar; "
            "it is not proof of objective or top-tier aesthetic quality."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ReleaseError("manifest must contain a JSON object")
        result = assess_release(manifest, base=args.manifest.resolve().parent)
    except (OSError, json.JSONDecodeError, EvaluationError, ReleaseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["release_bar_met"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
