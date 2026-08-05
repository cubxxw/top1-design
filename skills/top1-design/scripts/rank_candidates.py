#!/usr/bin/env python3
"""Rank blinded design comparisons with a deterministic Bradley-Terry fit."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


class PairError(ValueError):
    """Raised when a pairwise record is invalid."""


def load_pairs(lines: Iterable[str]) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    for line_number, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        try:
            item = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise PairError(f"line {line_number}: invalid JSON: {exc}") from exc
        if not isinstance(item, dict):
            raise PairError(f"line {line_number}: record must be an object")
        a, b, winner = item.get("a"), item.get("b"), item.get("winner")
        if not isinstance(a, str) or not a:
            raise PairError(f"line {line_number}: a must be a non-empty string")
        if not isinstance(b, str) or not b or b == a:
            raise PairError(f"line {line_number}: b must differ from a")
        if winner not in (a, b, "tie"):
            raise PairError(f"line {line_number}: winner must equal a, b, or tie")
        confidence = item.get("confidence", 1.0)
        if (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not math.isfinite(float(confidence))
            or not 0 < float(confidence) <= 1
        ):
            raise PairError(f"line {line_number}: confidence must be in (0, 1]")
        normalized = dict(item)
        normalized["confidence"] = float(confidence)
        pairs.append(normalized)
    if not pairs:
        raise PairError("no comparison records")
    return pairs


def rank_pairs(
    pairs: list[dict[str, Any]],
    iterations: int = 1200,
    learning_rate: float = 0.08,
) -> dict[str, Any]:
    candidates = sorted({item["a"] for item in pairs} | {item["b"] for item in pairs})
    ratings = {candidate: 0.0 for candidate in candidates}

    for step in range(iterations):
        gradient = {candidate: -0.01 * ratings[candidate] for candidate in candidates}
        total_weight = 0.0
        for item in pairs:
            a, b = item["a"], item["b"]
            confidence = float(item["confidence"])
            delta = max(-30.0, min(30.0, ratings[a] - ratings[b]))
            probability_a = 1.0 / (1.0 + math.exp(-delta))
            if item["winner"] == a:
                target = 1.0
            elif item["winner"] == b:
                target = 0.0
            else:
                target = 0.5
            error = (target - probability_a) * confidence
            gradient[a] += error
            gradient[b] -= error
            total_weight += confidence

        scale = learning_rate / max(1.0, total_weight)
        scale /= math.sqrt(1.0 + step / 200.0)
        for candidate in candidates:
            ratings[candidate] += scale * gradient[candidate]
        mean_rating = sum(ratings.values()) / len(ratings)
        for candidate in candidates:
            ratings[candidate] -= mean_rating

    counts = Counter()
    for item in pairs:
        counts[item["a"]] += 1
        counts[item["b"]] += 1

    ranking = sorted(candidates, key=lambda name: (-ratings[name], name))
    ranking_output = []
    for index, candidate in enumerate(ranking, start=1):
        versus_average = 100.0 / (1.0 + math.exp(-ratings[candidate]))
        ranking_output.append(
            {
                "rank": index,
                "candidate": candidate,
                "ability": round(ratings[candidate], 4),
                "win_probability_vs_average": round(versus_average, 2),
                "comparisons": counts[candidate],
            }
        )

    non_ties = [item for item in pairs if item["winner"] != "tie"]
    first_position_wins = sum(item["winner"] == item["a"] for item in non_ties)
    first_position_rate = (
        first_position_wins / len(non_ties) if non_ties else None
    )

    orientations: dict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)
    for item in pairs:
        key = tuple(sorted((item["a"], item["b"])))
        orientations[key].add((item["a"], item["b"]))
    unreversed = [
        list(key) for key, seen in orientations.items() if len(seen) < 2
    ]

    warnings: list[str] = []
    if first_position_rate is not None and (
        first_position_rate < 0.35 or first_position_rate > 0.65
    ):
        warnings.append("possible first-position bias")
    if unreversed:
        warnings.append(f"{len(unreversed)} candidate pairs were not side-reversed")
    under_sampled = [candidate for candidate, count in counts.items() if count < 2]
    if under_sampled:
        warnings.append(
            "candidates with fewer than two comparisons: "
            + ", ".join(sorted(under_sampled))
        )

    return {
        "model": "Bradley-Terry logistic fit",
        "comparison_count": len(pairs),
        "candidate_count": len(candidates),
        "ranking": ranking_output,
        "diagnostics": {
            "first_position_win_rate": (
                round(first_position_rate, 3)
                if first_position_rate is not None
                else None
            ),
            "unreversed_pairs": unreversed,
            "warnings": warnings,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pairs", type=Path, help="JSONL comparison records")
    parser.add_argument("--output", type=Path, help="Optional ranking JSON path")
    args = parser.parse_args(argv)

    try:
        pair_data = load_pairs(args.pairs.read_text(encoding="utf-8").splitlines())
        result = rank_pairs(pair_data)
    except (OSError, PairError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
