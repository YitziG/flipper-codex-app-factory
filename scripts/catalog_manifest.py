#!/usr/bin/env python3
"""Generate a Flipper Apps Catalog manifest.yml for one app."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", help="Path to app directory")
    parser.add_argument("--origin", required=True, help="Public GitHub repository URL")
    parser.add_argument("--commit-sha", required=True, help="Committed source SHA")
    parser.add_argument("--subdir", help="Source subdirectory to include in manifest")
    parser.add_argument("--output-root", default=str(ROOT / "dist" / "catalog"), help="Manifest output root")
    return parser.parse_args()


def extract(text: str, field: str) -> str | None:
    match = re.search(rf'{field}\s*=\s*"([^"]+)"', text)
    return match.group(1) if match else None


def yaml_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def screenshot_paths(app_dir: Path) -> list[str]:
    screenshots = app_dir / "screenshots"
    if not screenshots.exists():
        return []
    return sorted(
        str(path.relative_to(app_dir))
        for path in screenshots.iterdir()
        if path.is_file() and path.name != ".gitkeep" and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )


def main() -> int:
    args = parse_args()
    app_dir = Path(args.app).resolve()
    manifest_path = app_dir / "application.fam"
    if not manifest_path.exists():
        raise SystemExit(f"Missing {manifest_path}")
    if not re.match(r"^[0-9a-fA-F]{40}$", args.commit_sha):
        raise SystemExit("--commit-sha must be a 40-character Git SHA")

    text = manifest_path.read_text(encoding="utf-8")
    appid = extract(text, "appid")
    category = extract(text, "fap_category")
    if not appid or not category:
        raise SystemExit("application.fam must define appid and fap_category")

    shots = screenshot_paths(app_dir)
    if not shots:
        shots = ["screenshots/ss0.png"]

    lines = [
        "sourcecode:",
        "  type: git",
        "  location:",
        f"    origin: {yaml_string(args.origin)}",
        f"    commit_sha: {args.commit_sha}",
    ]
    if args.subdir:
        lines.append(f"    subdir: {yaml_string(args.subdir)}")

    lines.extend(
        [
            "short_description: " + yaml_string(extract(text, "fap_description") or ""),
            'description: "@README.md"',
            'changelog: "@docs/changelog.md"',
            "screenshots:",
        ]
    )
    lines.extend(f"  - {yaml_string(path)}" for path in shots)
    lines.append("")

    output = Path(args.output_root) / category / appid / "manifest.yml"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
