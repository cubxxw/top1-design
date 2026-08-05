#!/usr/bin/env python3
"""Score a TOP1 DESIGN evaluation without external dependencies."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


MODE_WEIGHTS: dict[str, dict[str, int]] = {
    "persuade": {
        "goal_fit": 18,
        "specificity": 12,
        "hierarchy": 15,
        "typography": 10,
        "layout": 10,
        "color_material": 8,
        "interaction_states": 10,
        "motion": 6,
        "copy": 11,
    },
    "operate": {
        "goal_fit": 15,
        "specificity": 10,
        "hierarchy": 12,
        "typography": 9,
        "layout": 12,
        "color_material": 6,
        "interaction_states": 18,
        "motion": 8,
        "copy": 10,
    },
    "read": {
        "goal_fit": 16,
        "specificity": 10,
        "hierarchy": 17,
        "typography": 15,
        "layout": 13,
        "color_material": 5,
        "interaction_states": 8,
        "motion": 2,
        "copy": 14,
    },
    "experience": {
        "goal_fit": 12,
        "specificity": 18,
        "hierarchy": 14,
        "typography": 10,
        "layout": 10,
        "color_material": 12,
        "interaction_states": 8,
        "motion": 12,
        "copy": 4,
    },
}


class EvaluationError(ValueError):
    """Raised when an evaluation is structurally invalid."""


def _number(value: Any, label: str, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise EvaluationError(f"{label} must be a number")
    result = float(value)
    if not math.isfinite(result) or not minimum <= result <= maximum:
        raise EvaluationError(f"{label} must be between {minimum} and {maximum}")
    return result


def validate_report(report: dict[str, Any]) -> None:
    if report.get("schema_version") != "1.0":
        raise EvaluationError('schema_version must be "1.0"')
    mode = report.get("mode")
    if mode not in MODE_WEIGHTS:
        raise EvaluationError(f"mode must be one of: {', '.join(MODE_WEIGHTS)}")
    _number(report.get("threshold", 95), "threshold", 0, 100)
    required_depth = report.get("required_depth")
    if isinstance(required_depth, bool) or not isinstance(required_depth, int):
        raise EvaluationError("required_depth must be an integer")
    if not 0 <= required_depth <= 12:
        raise EvaluationError("required_depth must be between 0 and 12")
    gates = report.get("required_hard_gates")
    if not isinstance(gates, list) or not gates:
        raise EvaluationError("required_hard_gates must be a non-empty list")
    if any(not isinstance(gate, str) or not gate for gate in gates):
        raise EvaluationError("required_hard_gates entries must be non-empty strings")
    nodes = report.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise EvaluationError("nodes must be a non-empty list")

    ids: set[str] = set()
    for index, node in enumerate(nodes):
        label = f"nodes[{index}]"
        if not isinstance(node, dict):
            raise EvaluationError(f"{label} must be an object")
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id:
            raise EvaluationError(f"{label}.id must be a non-empty string")
        if node_id in ids:
            raise EvaluationError(f"duplicate node id: {node_id}")
        ids.add(node_id)
        depth = node.get("depth")
        if isinstance(depth, bool) or not isinstance(depth, int) or depth < 0:
            raise EvaluationError(f"{label}.depth must be a non-negative integer")
        _number(node.get("confidence"), f"{label}.confidence", 0, 1)
        scores = node.get("scores")
        if not isinstance(scores, dict):
            raise EvaluationError(f"{label}.scores must be an object")
        for metric in MODE_WEIGHTS[mode]:
            if metric not in scores:
                raise EvaluationError(f"{label}.scores is missing {metric}")
            _number(scores[metric], f"{label}.scores.{metric}", 0, 100)
        if not isinstance(node.get("hard_gates"), dict):
            raise EvaluationError(f"{label}.hard_gates must be an object")
        evidence = node.get("evidence")
        if not isinstance(evidence, list):
            raise EvaluationError(f"{label}.evidence must be a list")
        if "required" in node and not isinstance(node["required"], bool):
            raise EvaluationError(f"{label}.required must be boolean")

    for index, node in enumerate(nodes):
        parent_id = node.get("parent_id")
        if parent_id is not None and parent_id not in ids:
            raise EvaluationError(f"nodes[{index}].parent_id does not exist: {parent_id}")


def weighted_score(scores: dict[str, float], mode: str) -> float:
    weights = MODE_WEIGHTS[mode]
    return sum(float(scores[name]) * weight for name, weight in weights.items()) / 100.0


def score_report(report: dict[str, Any]) -> dict[str, Any]:
    validate_report(report)
    mode = report["mode"]
    threshold = float(report.get("threshold", 95))
    required_depth = int(report["required_depth"])
    required_gates: list[str] = report["required_hard_gates"]
    nodes: list[dict[str, Any]] = report["nodes"]

    children: dict[str, list[str]] = {node["id"]: [] for node in nodes}
    node_by_id = {node["id"]: node for node in nodes}
    for node in nodes:
        if node.get("parent_id") is not None:
            children[node["parent_id"]].append(node["id"])

    results: list[dict[str, Any]] = []
    result_by_id: dict[str, dict[str, Any]] = {}

    for node in nodes:
        raw = weighted_score(node["scores"], mode)
        confidence = float(node["confidence"])
        cap = 80.0 + 20.0 * confidence
        effective = min(raw, cap)
        gate_values = node["hard_gates"]
        missing_gates = [gate for gate in required_gates if gate not in gate_values]
        failed_gates = [
            gate for gate in required_gates if gate_values.get(gate) is not True
        ]
        issues: list[str] = []
        if missing_gates:
            issues.append("missing hard gates: " + ", ".join(missing_gates))
        if failed_gates:
            issues.append("failed hard gates: " + ", ".join(failed_gates))
        if not node["evidence"]:
            issues.append("no evidence")

        if failed_gates or not node["evidence"]:
            status = "blocked"
        elif effective + 1e-9 < threshold:
            status = "repair"
        elif node["depth"] < required_depth and not children[node["id"]]:
            status = "promote"
        else:
            status = "pass"

        weakest_metric = min(
            MODE_WEIGHTS[mode],
            key=lambda name: (
                float(node["scores"][name]),
                -MODE_WEIGHTS[mode][name],
            ),
        )
        item = {
            "id": node["id"],
            "parent_id": node.get("parent_id"),
            "scope": node.get("scope", node["id"]),
            "depth": node["depth"],
            "required": node.get("required", True),
            "weighted_score": round(raw, 2),
            "confidence": round(confidence, 3),
            "confidence_cap": round(cap, 2),
            "effective_score": round(effective, 2),
            "status": status,
            "weakest_metric": weakest_metric,
            "weakest_metric_score": float(node["scores"][weakest_metric]),
            "failed_gates": failed_gates,
            "issues": issues,
            "children": children[node["id"]],
        }
        results.append(item)
        result_by_id[node["id"]] = item

    required_ids = {
        node["id"] for node in nodes if node.get("required", True)
    }
    terminal_ids = [
        node_id
        for node_id in required_ids
        if not any(child in required_ids for child in children[node_id])
    ]
    terminal_results = [result_by_id[node_id] for node_id in terminal_ids]
    release = bool(terminal_results) and all(
        item["status"] == "pass" for item in terminal_results
    )

    priority = {"blocked": 0, "repair": 1, "promote": 2, "pass": 3}
    unresolved = [
        item for item in terminal_results if item["status"] != "pass"
    ]
    unresolved.sort(
        key=lambda item: (
            priority[item["status"]],
            item["effective_score"],
            item["depth"],
            item["id"],
        )
    )
    next_action = None
    if unresolved:
        target = unresolved[0]
        if target["status"] == "blocked":
            action = "repair or verify hard gates and evidence"
        elif target["status"] == "repair":
            action = f"repair weakest metric: {target['weakest_metric']}"
        else:
            action = "bisect this scope into at most two coherent children"
        next_action = {"node_id": target["id"], "action": action}

    return {
        "schema_version": "1.0",
        "run_id": report.get("run_id"),
        "target": report.get("target"),
        "mode": mode,
        "rubric_version": report.get("rubric_version", "1.0"),
        "threshold": threshold,
        "required_depth": required_depth,
        "release_status": "release_candidate" if release else "not_releasable",
        "required_terminal_nodes": terminal_ids,
        "next_action": next_action,
        "nodes": results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evaluation", type=Path, help="Evaluation JSON")
    parser.add_argument("--output", type=Path, help="Optional result JSON path")
    args = parser.parse_args(argv)

    try:
        report = json.loads(args.evaluation.read_text(encoding="utf-8"))
        result = score_report(report)
    except (OSError, json.JSONDecodeError, EvaluationError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["release_status"] == "release_candidate" else 2


if __name__ == "__main__":
    raise SystemExit(main())
