#!/usr/bin/env python3
"""Validate FAP metadata and run local uFBT checks for one app."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "appid": r'appid\s*=\s*"([^"]+)"',
    "name": r'name\s*=\s*"([^"]+)"',
    "entry_point": r'entry_point\s*=\s*"([^"]+)"',
    "stack_size": r"stack_size\s*=",
    "fap_version": r'fap_version\s*=\s*"([^"]+)"',
    "fap_category": r'fap_category\s*=\s*"([^"]+)"',
    "fap_description": r'fap_description\s*=\s*"([^"]+)"',
    "fap_author": r'fap_author\s*=\s*"([^"]+)"',
    "fap_icon": r'fap_icon\s*=\s*"([^"]+)"',
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", help="Path to app directory")
    parser.add_argument("--skip-ufbt", action="store_true", help="Only validate metadata")
    return parser.parse_args()


def read_manifest(app_dir: Path) -> str:
    manifest = app_dir / "application.fam"
    if not manifest.exists():
        raise SystemExit(f"Missing {manifest}")
    return manifest.read_text(encoding="utf-8")


def validate_manifest(app_dir: Path, text: str) -> dict[str, str]:
    errors: list[str] = []
    values: dict[str, str] = {}

    if "apptype=FlipperAppType.EXTERNAL" not in text and "apptype = FlipperAppType.EXTERNAL" not in text:
        errors.append("application.fam must set apptype=FlipperAppType.EXTERNAL")

    for field, pattern in REQUIRED_FIELDS.items():
        match = re.search(pattern, text)
        if not match:
            errors.append(f"application.fam missing {field}")
            continue
        if match.groups():
            values[field] = match.group(1)

    version = values.get("fap_version")
    if version and not re.match(r"^\d+\.\d+$", version):
        errors.append("fap_version must use major.minor format")

    icon = values.get("fap_icon")
    if icon and not (app_dir / icon).exists():
        errors.append(f"fap_icon file does not exist: {icon}")

    readme = app_dir / "README.md"
    changelog = app_dir / "docs" / "changelog.md"
    if not readme.exists():
        errors.append("README.md is required")
    if not changelog.exists():
        errors.append("docs/changelog.md is required")

    if errors:
        raise SystemExit("\n".join(errors))
    return values


def run(command: list[str], cwd: Path) -> None:
    print(f"+ {' '.join(command)}")
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    args = parse_args()
    app_dir = Path(args.app).resolve()
    text = read_manifest(app_dir)
    values = validate_manifest(app_dir, text)
    print(f"metadata ok: {values['appid']} {values['fap_version']} ({values['fap_category']})")

    if args.skip_ufbt:
        return 0
    if shutil.which("ufbt") is None:
        raise SystemExit("ufbt is not installed or not on PATH; install with `python3 -m pip install --upgrade ufbt`")

    run(["ufbt", "lint"], app_dir)
    run(["ufbt"], app_dir)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
