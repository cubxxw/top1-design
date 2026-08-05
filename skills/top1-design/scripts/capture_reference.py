#!/usr/bin/env python3
"""Capture a reference through Kimi WebBridge and write provenance metadata."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_DAEMON = "http://127.0.0.1:10086/command"


class WebBridgeError(RuntimeError):
    """Raised when Kimi WebBridge cannot complete a command."""


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise ValueError("slug must contain at least one letter or digit")
    return slug[:80]


def post_command(
    daemon: str,
    session: str,
    action: str,
    args: dict[str, Any],
    timeout: float = 30.0,
) -> dict[str, Any]:
    body = json.dumps(
        {"action": action, "args": args, "session": session},
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        daemon,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise WebBridgeError(f"{action} failed: {exc}") from exc
    if not payload.get("ok"):
        raise WebBridgeError(f"{action} failed: {payload}")
    data = payload.get("data")
    if not isinstance(data, dict):
        raise WebBridgeError(f"{action} returned no data")
    return data


def try_start_daemon() -> bool:
    candidates = [
        Path.home() / ".kimi-webbridge/bin/kimi-webbridge",
        Path.home() / ".kimi-webbridge/bin/kimi-webbridge.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            subprocess.run(
                [str(candidate), "start"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
    return False


def build_card(
    slug: str,
    requested_url: str,
    captured_at: str,
    page: dict[str, Any],
    screenshot_path: Path,
    session: str,
    role: str,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "id": slug,
        "source_url": page.get("url") or requested_url,
        "requested_url": requested_url,
        "title": page.get("title"),
        "captured_at": captured_at,
        "capture": {
            "tool": "Kimi WebBridge",
            "session": session,
            "screenshot": screenshot_path.name,
            "viewport": page.get("viewport"),
            "device_pixel_ratio": page.get("devicePixelRatio"),
            "document": page.get("document"),
            "platform": platform.platform(),
        },
        "role": role,
        "scope": [],
        "quality_branches": [],
        "observed": [],
        "interpretation": [],
        "transfer": [],
        "avoid_copy": [],
        "fails_when": [],
        "rights": "link-only",
    }


def capture(
    url: str,
    slug: str,
    output: Path,
    session: str,
    group_title: str,
    daemon: str = DEFAULT_DAEMON,
    role: str = "positive-reference",
    selector: str | None = None,
    wait_seconds: float = 2.0,
    save_snapshot: bool = False,
    freeze_motion: bool = False,
) -> dict[str, Any]:
    slug = safe_slug(slug)
    output = output.expanduser().resolve()
    destination = output / slug
    destination.mkdir(parents=True, exist_ok=True)
    captured_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = captured_at.replace(":", "").replace("+00:00", "Z")

    try:
        navigation = post_command(
            daemon,
            session,
            "navigate",
            {"url": url, "newTab": True, "group_title": group_title},
        )
    except WebBridgeError:
        if not try_start_daemon():
            raise
        time.sleep(0.5)
        navigation = post_command(
            daemon,
            session,
            "navigate",
            {"url": url, "newTab": True, "group_title": group_title},
        )

    if wait_seconds:
        time.sleep(wait_seconds)

    metadata = post_command(
        daemon,
        session,
        "evaluate",
        {
            "code": """(() => JSON.stringify({
              url: location.href,
              title: document.title,
              viewport: {width: innerWidth, height: innerHeight},
              devicePixelRatio: devicePixelRatio,
              document: {
                width: document.documentElement.scrollWidth,
                height: document.documentElement.scrollHeight,
                language: document.documentElement.lang || null
              }
            }))()"""
        },
    )
    value = metadata.get("value")
    try:
        page = json.loads(value) if isinstance(value, str) else {}
    except json.JSONDecodeError:
        page = {}
    page.setdefault("url", navigation.get("url", url))

    if freeze_motion:
        post_command(
            daemon,
            session,
            "evaluate",
            {
                "code": """(() => {
                  const style = document.createElement('style');
                  style.dataset.top1DesignFreeze = 'true';
                  style.textContent = `*,*::before,*::after {
                    transition-duration: 0.001ms !important;
                    transition-delay: 0ms !important;
                    animation-duration: 0.001ms !important;
                    animation-delay: 0ms !important;
                    animation-iteration-count: 1 !important;
                    scroll-behavior: auto !important;
                  }`;
                  document.head.appendChild(style);
                  for (const animation of document.getAnimations()) {
                    try { animation.finish(); } catch (_) {}
                  }
                  return true;
                })()"""
            },
        )
        time.sleep(0.1)

    screenshot_path = destination / f"capture-{stamp}.png"
    screenshot_args: dict[str, Any] = {
        "format": "png",
        "path": str(screenshot_path),
    }
    if selector:
        screenshot_args["selector"] = selector
    screenshot = post_command(
        daemon,
        session,
        "screenshot",
        screenshot_args,
    )

    card = build_card(
        slug=slug,
        requested_url=url,
        captured_at=captured_at,
        page=page,
        screenshot_path=screenshot_path,
        session=session,
        role=role,
    )
    card["capture"]["size_bytes"] = screenshot.get("sizeBytes")
    card["capture"]["tab_id"] = navigation.get("tabId")
    card["capture"]["motion_frozen"] = freeze_motion

    if save_snapshot:
        snapshot = post_command(daemon, session, "snapshot", {})
        snapshot_path = destination / f"snapshot-{stamp}.json"
        snapshot_path.write_text(
            json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        card["capture"]["snapshot"] = snapshot_path.name

    card_path = destination / f"card-{stamp}.json"
    card_path.write_text(
        json.dumps(card, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "card": str(card_path),
        "screenshot": str(screenshot_path),
        "source_url": card["source_url"],
        "session": session,
        "notice": "Browser tabs remain open. Raw screenshot is local evidence.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("slug")
    parser.add_argument("--output", type=Path, default=Path(".top1-design/references"))
    parser.add_argument("--session", default="top1-design-reference-capture")
    parser.add_argument("--group-title", default="TOP1 Design references")
    parser.add_argument("--daemon", default=os.environ.get("KIMI_WEBBRIDGE_URL", DEFAULT_DAEMON))
    parser.add_argument(
        "--role",
        choices=["positive-reference", "anti-reference", "calibration"],
        default="positive-reference",
    )
    parser.add_argument("--selector")
    parser.add_argument("--wait", type=float, default=2.0)
    parser.add_argument("--save-snapshot", action="store_true")
    parser.add_argument(
        "--freeze-motion",
        action="store_true",
        help="Freeze finite CSS/Web Animations for a static evidence frame.",
    )
    args = parser.parse_args(argv)

    try:
        result = capture(
            url=args.url,
            slug=args.slug,
            output=args.output,
            session=args.session,
            group_title=args.group_title,
            daemon=args.daemon,
            role=args.role,
            selector=args.selector,
            wait_seconds=max(0.0, min(args.wait, 30.0)),
            save_snapshot=args.save_snapshot,
            freeze_motion=args.freeze_motion,
        )
    except (OSError, ValueError, WebBridgeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
