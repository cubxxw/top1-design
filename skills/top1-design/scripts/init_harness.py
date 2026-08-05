#!/usr/bin/env python3
"""Install the TOP1 DESIGN persistent harness into a project."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


def install_harness(project: Path, overwrite: bool = False) -> dict[str, object]:
    project = project.expanduser().resolve()
    if not project.exists() or not project.is_dir():
        raise ValueError(f"project directory does not exist: {project}")

    template = Path(__file__).resolve().parent.parent / "assets" / "harness-template"
    if not template.is_dir():
        raise ValueError(f"harness template is missing: {template}")

    created: list[str] = []
    preserved: list[str] = []
    replaced: list[str] = []

    for source in sorted(template.rglob("*")):
        relative = source.relative_to(template)
        target = project / relative
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not overwrite:
            preserved.append(str(relative))
            continue
        if target.exists():
            replaced.append(str(relative))
        else:
            created.append(str(relative))
        shutil.copy2(source, target)

    for directory in (
        ".top1-design/baselines",
        ".top1-design/references",
        ".top1-design/runs",
    ):
        (project / directory).mkdir(parents=True, exist_ok=True)
    (project / ".top1-design/ledger.jsonl").touch(exist_ok=True)

    return {
        "project": str(project),
        "created": created,
        "preserved": preserved,
        "replaced": replaced,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing harness files. Off by default.",
    )
    args = parser.parse_args(argv)

    try:
        result = install_harness(args.project, overwrite=args.overwrite)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
