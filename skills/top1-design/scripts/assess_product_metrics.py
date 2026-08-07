#!/usr/bin/env python3
"""Assess whether a cohort meets the four TOP1 DESIGN product-success targets."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


DEFAULT_TARGETS = {
    "severe_defect_free_rate": 0.95,
    "release_bar_rate": 0.90,
    "blind_preference_rate": 0.70,
    "human_edit_time_reduction": 0.50,
}


class MetricsError(ValueError):
    """Raised when cohort evidence is structurally invalid."""


def _number(value: Any, label: str, minimum: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise MetricsError(f"{label} must be a number")
    result = float(value)
    if not math.isfinite(result) or result < minimum:
        raise MetricsError(f"{label} must be at least {minimum}")
    return result


def _count(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise MetricsError(f"{label} must be a non-negative integer")
    return value


def validate_cohort(cohort: dict[str, Any]) -> None:
    if cohort.get("schema_version") != "1.0":
        raise MetricsError('schema_version must be "1.0"')
    targets = cohort.get("targets", {})
    if not isinstance(targets, dict):
        raise MetricsError("targets must be an object")
    for key, default in DEFAULT_TARGETS.items():
        value = _number(targets.get(key, default), f"targets.{key}")
        if value > 1:
            raise MetricsError(f"targets.{key} must be between 0 and 1")
    records = cohort.get("records")
    if not isinstance(records, list) or not records:
        raise MetricsError("records must be a non-empty list")
    ids: set[str] = set()
    for index, record in enumerate(records):
        label = f"records[{index}]"
        if not isinstance(record, dict):
            raise MetricsError(f"{label} must be an object")
        run_id = record.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            raise MetricsError(f"{label}.run_id must be a non-empty string")
        if run_id in ids:
            raise MetricsError(f"duplicate run_id: {run_id}")
        ids.add(run_id)
        if not isinstance(record.get("eligible"), bool):
            raise MetricsError(f"{label}.eligible must be boolean")
        if not isinstance(record.get("release_bar_met"), bool):
            raise MetricsError(f"{label}.release_bar_met must be boolean")
        audits = _count(record.get("audited_units"), f"{label}.audited_units")
        clean = _count(
            record.get("severe_defect_free_units"),
            f"{label}.severe_defect_free_units",
        )
        if clean > audits:
            raise MetricsError(
                f"{label}.severe_defect_free_units cannot exceed audited_units"
            )
        comparisons = record.get("blind_comparisons")
        if not isinstance(comparisons, dict):
            raise MetricsError(f"{label}.blind_comparisons must be an object")
        for key in ("taste_engine_wins", "control_wins", "ties"):
            _count(comparisons.get(key), f"{label}.blind_comparisons.{key}")
        time = record.get("human_edit_minutes")
        if not isinstance(time, dict):
            raise MetricsError(f"{label}.human_edit_minutes must be an object")
        baseline = _number(time.get("baseline"), f"{label}.human_edit_minutes.baseline")
        _number(time.get("taste_engine"), f"{label}.human_edit_minutes.taste_engine")
        if record["eligible"] and baseline <= 0:
            raise MetricsError(
                f"{label}.human_edit_minutes.baseline must be greater than 0 "
                "for an eligible record"
            )


def assess_product_metrics(cohort: dict[str, Any]) -> dict[str, Any]:
    validate_cohort(cohort)
    targets = {**DEFAULT_TARGETS, **cohort.get("targets", {})}
    eligible = [record for record in cohort["records"] if record["eligible"]]
    audited_units = sum(record["audited_units"] for record in eligible)
    clean_units = sum(record["severe_defect_free_units"] for record in eligible)
    release_count = sum(record["release_bar_met"] for record in eligible)
    wins = sum(
        record["blind_comparisons"]["taste_engine_wins"] for record in eligible
    )
    control_wins = sum(
        record["blind_comparisons"]["control_wins"] for record in eligible
    )
    ties = sum(record["blind_comparisons"]["ties"] for record in eligible)
    comparisons = wins + control_wins + ties
    baseline_minutes = sum(
        float(record["human_edit_minutes"]["baseline"]) for record in eligible
    )
    engine_minutes = sum(
        float(record["human_edit_minutes"]["taste_engine"]) for record in eligible
    )

    values: dict[str, float | None] = {
        "severe_defect_free_rate": (
            clean_units / audited_units if audited_units else None
        ),
        "release_bar_rate": release_count / len(eligible) if eligible else None,
        "blind_preference_rate": wins / comparisons if comparisons else None,
        "human_edit_time_reduction": (
            1.0 - engine_minutes / baseline_minutes if baseline_minutes else None
        ),
    }
    sample_sizes = {
        "eligible_projects": len(eligible),
        "audited_units": audited_units,
        "blind_comparisons": comparisons,
        "baseline_human_minutes": round(baseline_minutes, 2),
    }
    metric_results: dict[str, dict[str, Any]] = {}
    for key, target in targets.items():
        value = values[key]
        metric_results[key] = {
            "value": round(value, 4) if value is not None else None,
            "target": float(target),
            "passed": value is not None and value + 1e-12 >= float(target),
        }
    success = all(item["passed"] for item in metric_results.values())
    return {
        "schema_version": "1.0",
        "cohort_id": cohort.get("cohort_id"),
        "product_success": success,
        "status": "targets_met" if success else "targets_not_met",
        "metrics": metric_results,
        "sample_sizes": sample_sizes,
        "definitions": {
            "severe_defect_free_rate": (
                "eligible audited units with no unresolved blocker/severe visual "
                "or interaction defect divided by all eligible audited units"
            ),
            "release_bar_rate": (
                "eligible projects that meet the declared Release Bar divided by "
                "all eligible projects"
            ),
            "blind_preference_rate": (
                "Taste Engine wins divided by all valid blinded comparisons, "
                "including ties in the denominator"
            ),
            "human_edit_time_reduction": (
                "one minus total Taste Engine human-edit minutes divided by total "
                "matched baseline human-edit minutes"
            ),
        },
        "claim_boundary": (
            "These targets validate engineering quality, releasability, preference, "
            "and labor savings. They do not claim a 95% top-design success rate."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cohort", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    try:
        cohort = json.loads(args.cohort.read_text(encoding="utf-8"))
        if not isinstance(cohort, dict):
            raise MetricsError("cohort must contain a JSON object")
        result = assess_product_metrics(cohort)
    except (OSError, json.JSONDecodeError, MetricsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["product_success"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
