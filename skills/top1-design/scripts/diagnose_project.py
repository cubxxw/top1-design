#!/usr/bin/env python3
"""Diagnose project maturity, adapter support, and safe change granularity."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable


IGNORED_PARTS = {
    ".git",
    ".next",
    ".top1-design",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "vendor",
}
SOURCE_SUFFIXES = {".css", ".html", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}
COMPONENT_SUFFIXES = {".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}
STAGES = {"auto", "early", "middle", "late"}


class DiagnosisError(ValueError):
    """Raised when a project profile cannot be diagnosed safely."""


def _iter_files(project: Path) -> Iterable[Path]:
    for path in project.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        yield path


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DiagnosisError(f"cannot read {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise DiagnosisError(f"{label} must contain a JSON object")
    return value


def _dependencies(package: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        values = package.get(key, {})
        if isinstance(values, dict):
            result.update(name.lower() for name in values)
    return result


def _framework(dependencies: set[str], files: list[Path]) -> str:
    if "next" in dependencies:
        return "nextjs"
    if "nuxt" in dependencies:
        return "nuxt"
    if "react" in dependencies:
        return "react"
    if "vue" in dependencies:
        return "vue"
    if "svelte" in dependencies or "@sveltejs/kit" in dependencies:
        return "svelte"
    if any(path.suffix.lower() in {".html", ".css"} for path in files):
        return "static-web"
    return "unknown"


def _has_any(dependencies: set[str], names: set[str]) -> bool:
    return bool(dependencies & names)


def _has_path(project: Path, candidates: Iterable[str]) -> bool:
    return any((project / candidate).exists() for candidate in candidates)


def _relative_parts(path: Path, project: Path) -> tuple[str, ...]:
    return tuple(part.lower() for part in path.relative_to(project).parts)


def collect_signals(project: Path) -> dict[str, Any]:
    project = project.expanduser().resolve()
    package_path = project / "package.json"
    package = _load_json(package_path, "package.json") if package_path.exists() else {}
    dependencies = _dependencies(package)
    files = list(_iter_files(project))
    source_files = [path for path in files if path.suffix.lower() in SOURCE_SUFFIXES]
    components = [
        path
        for path in source_files
        if path.suffix.lower() in COMPONENT_SUFFIXES
        and "components" in _relative_parts(path, project)
    ]
    tests = [
        path
        for path in files
        if path.name.lower().endswith(
            (
                ".spec.js",
                ".spec.jsx",
                ".spec.ts",
                ".spec.tsx",
                ".test.js",
                ".test.jsx",
                ".test.ts",
                ".test.tsx",
            )
        )
        or "tests" in _relative_parts(path, project)
        or "__tests__" in _relative_parts(path, project)
    ]
    token_files = [
        path
        for path in files
        if any(
            marker in path.stem.lower()
            for marker in ("design-token", "design_token", "tokens", "theme")
        )
        and path.suffix.lower() in {".css", ".json", ".js", ".ts", ".tsx"}
    ]
    scripts = package.get("scripts", {})
    if not isinstance(scripts, dict):
        scripts = {}
    framework = _framework(dependencies, files)
    tailwind = _has_any(dependencies, {"tailwindcss", "@tailwindcss/postcss"}) or _has_path(
        project,
        (
            "tailwind.config.js",
            "tailwind.config.cjs",
            "tailwind.config.mjs",
            "tailwind.config.ts",
        ),
    )
    storybook = any(name.startswith("@storybook/") for name in dependencies) or (
        project / ".storybook"
    ).exists()
    e2e = _has_any(dependencies, {"@playwright/test", "playwright", "cypress"})
    accessibility = any(
        name in dependencies or name.startswith("@axe-core/")
        for name in ("axe-core", "jest-axe", "eslint-plugin-jsx-a11y")
    )
    visual_regression = _has_any(
        dependencies,
        {"@chromatic-com/storybook", "chromatic", "loki", "reg-suit"},
    )
    ci = _has_path(project, (".github/workflows", ".gitlab-ci.yml", "Jenkinsfile"))
    component_library = storybook or _has_any(
        dependencies,
        {
            "@chakra-ui/react",
            "@mui/material",
            "@radix-ui/react-dialog",
            "antd",
            "shadcn",
        },
    )
    return {
        "framework": framework,
        "tailwind": tailwind,
        "source_file_count": len(source_files),
        "component_file_count": len(components),
        "test_file_count": len(tests),
        "design_token_file_count": len(token_files),
        "storybook": storybook,
        "component_library": component_library,
        "end_to_end_tests": e2e,
        "accessibility_tooling": accessibility,
        "visual_regression": visual_regression,
        "continuous_integration": ci,
        "package_scripts": sorted(str(name) for name in scripts),
        "has_dev_script": "dev" in scripts or "start" in scripts,
        "has_build_script": "build" in scripts,
        "has_test_script": "test" in scripts,
        "monorepo": bool(package.get("workspaces"))
        or _has_path(project, ("pnpm-workspace.yaml", "turbo.json", "nx.json")),
    }


def validate_profile(profile: dict[str, Any]) -> None:
    if profile.get("schema_version", "1.0") != "1.0":
        raise DiagnosisError('profile schema_version must be "1.0"')
    stage = profile.get("declared_stage", "auto")
    if stage not in STAGES:
        raise DiagnosisError("declared_stage must be auto, early, middle, or late")
    runtime = profile.get("runtime", {})
    if not isinstance(runtime, dict):
        raise DiagnosisError("runtime must be an object")
    for key in ("start_verified", "primary_flow_verified"):
        if key in runtime and not isinstance(runtime[key], bool):
            raise DiagnosisError(f"runtime.{key} must be boolean")
    boundaries = profile.get("boundaries", {})
    if not isinstance(boundaries, dict):
        raise DiagnosisError("boundaries must be an object")


def infer_stage(signals: dict[str, Any], declared_stage: str) -> tuple[str, float, list[str]]:
    if declared_stage != "auto":
        labels = {"early": "greenfield", "middle": "rescue", "late": "governed"}
        return labels[declared_stage], 1.0, [f"declared_stage={declared_stage}"]

    governance_signals = sum(
        (
            signals["design_token_file_count"] > 0,
            signals["component_file_count"] >= 20,
            signals["storybook"],
            signals["end_to_end_tests"],
            signals["accessibility_tooling"],
            signals["visual_regression"],
            signals["continuous_integration"],
            signals["test_file_count"] >= 10,
        )
    )
    if governance_signals >= 5:
        return (
            "governed",
            0.72,
            [f"{governance_signals}/8 mature-system signals detected"],
        )
    if (
        signals["source_file_count"] < 30
        and signals["component_file_count"] < 8
        and signals["design_token_file_count"] == 0
        and not signals["storybook"]
    ):
        return (
            "greenfield",
            0.62,
            ["small UI surface with no detected design-system infrastructure"],
        )
    return (
        "rescue",
        0.65,
        ["existing UI detected without enough governance signals for governed mode"],
    )


def adapter_support(
    signals: dict[str, Any],
    runtime: dict[str, Any],
    target_url: str | None,
) -> dict[str, Any]:
    framework = signals["framework"]
    review_ready = bool(target_url) or runtime.get("start_verified") is True
    review = {
        "status": "ready" if review_ready else "conditional",
        "reason": (
            "a verified or explicit browser target is available"
            if review_ready
            else "review requires a stable local or remote browser target"
        ),
    }

    reasons: list[str] = []
    if framework not in {"nextjs", "react"}:
        status = "review_only"
        reasons.append("first-release mutation adapters support React and Next.js")
    else:
        if not signals["tailwind"]:
            reasons.append("Tailwind CSS was not detected")
        if not signals["has_build_script"]:
            reasons.append("package.json has no build script")
        if not signals["has_dev_script"] and not review_ready:
            reasons.append("no dev/start script or verified target was found")
        status = "supported" if not reasons else "conditional"

    return {
        "review": review,
        "automatic_modification": {
            "status": status,
            "adapter": (
                f"{framework}-tailwind"
                if framework in {"nextjs", "react"} and signals["tailwind"]
                else None
            ),
            "reasons": reasons
            or ["supported first-release stack and build boundary detected"],
        },
    }


def change_policy(
    mode: str,
    modification_status: str,
    signals: dict[str, Any],
) -> dict[str, Any]:
    if modification_status == "review_only":
        recommended, maximum = 0, 0
    elif mode == "greenfield":
        recommended, maximum = 5, 5
    elif mode == "rescue":
        recommended = 3 if signals["design_token_file_count"] else 2
        maximum = 4
    else:
        recommended, maximum = 1, 2

    if modification_status == "conditional":
        recommended = min(recommended, 1)
        maximum = min(maximum, 2)

    level_names = {
        0: "review only",
        1: "single surface",
        2: "shared components",
        3: "design tokens",
        4: "visual system",
        5: "product design direction",
    }
    return {
        "recommended_level": recommended,
        "recommended_label": level_names[recommended],
        "maximum_without_new_authority": maximum,
        "maximum_label": level_names[maximum],
        "levels": {str(key): value for key, value in level_names.items()},
        "rule": "choose the highest-return level whose blast radius is testable and reversible",
    }


def diagnose(
    project: Path,
    profile: dict[str, Any] | None = None,
    target_url: str | None = None,
) -> dict[str, Any]:
    project = project.expanduser().resolve()
    if not project.is_dir():
        raise DiagnosisError(f"project directory does not exist: {project}")
    profile = dict(profile or {})
    validate_profile(profile)
    signals = collect_signals(project)
    runtime = profile.get("runtime", {})
    mode, confidence, rationale = infer_stage(
        signals,
        profile.get("declared_stage", "auto"),
    )
    support = adapter_support(signals, runtime, target_url or runtime.get("target_url"))
    policy = change_policy(mode, support["automatic_modification"]["status"], signals)
    boundaries = profile.get("boundaries", {})

    return {
        "schema_version": "1.0",
        "project": str(project),
        "strategy": {
            "mode": mode,
            "confidence": confidence,
            "source": (
                "declared" if profile.get("declared_stage", "auto") != "auto" else "inferred"
            ),
            "rationale": rationale,
        },
        "capability": support,
        "change_policy": policy,
        "signals": signals,
        "boundaries": {
            "declared": boundaries,
            "always_requires_confirmation": [
                "product strategy or primary workflow changes",
                "factual claims, pricing, analytics, publishing, or destructive actions",
                "changes above maximum_without_new_authority",
            ],
        },
        "next_step": (
            "run browser review and create isolated candidates"
            if support["review"]["status"] == "ready"
            else "establish a stable browser target before scoring or mutation"
        ),
        "disclaimer": (
            "Repository signals select a safe operating posture; they do not prove "
            "organizational maturity or authorize changes."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--profile", type=Path, help="Optional PROJECT_PROFILE JSON")
    parser.add_argument("--target-url", help="Verified local or remote browser target")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    try:
        profile = _load_json(args.profile, "profile") if args.profile else None
        result = diagnose(args.project, profile=profile, target_url=args.target_url)
    except (OSError, DiagnosisError) as exc:
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
