#!/usr/bin/env python3
"""Scaffold a Flipper Zero C FAP app from the factory template."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "factory" / "templates" / "c-app"
APPS_DIR = ROOT / "apps"
APPID_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--appid", required=True, help="Lowercase Flipper app id, e.g. my_tool")
    parser.add_argument("--name", required=True, help="Display name, e.g. My Tool")
    parser.add_argument("--category", default="Tools", help="Flipper Apps Catalog category")
    parser.add_argument("--author", default="Unknown", help="App author")
    parser.add_argument(
        "--short-description",
        default="Generated Flipper Zero app",
        help="Short FAP/catalog description",
    )
    parser.add_argument("--version", default="0.1", help="FAP version, major.minor")
    parser.add_argument("--output-dir", default=str(APPS_DIR), help="Parent directory for generated app")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing generated app")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if not APPID_RE.match(args.appid):
        raise SystemExit("APPID must start with a lowercase letter and contain only lowercase letters, numbers, and underscores")
    if not re.match(r"^\d+\.\d+$", args.version):
        raise SystemExit("VERSION must use major.minor format, e.g. 0.1")
    if not args.name.strip():
        raise SystemExit("NAME must not be empty")
    if not args.category.strip():
        raise SystemExit("CATEGORY must not be empty")


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_icon(path: Path) -> None:
    # 10x10 1-bit PNG generated from a tiny static bitmap. Kept local so
    # scaffolded apps do not need image tooling just to become buildable.
    import zlib
    import struct

    width = height = 10
    rows = []
    for y in range(height):
        row = [0, 0]
        for x in range(width):
            border = x in (0, width - 1) or y in (0, height - 1)
            diagonal = x == y or x == width - y - 1
            if border or diagonal:
                row[x // 8] |= 1 << (7 - (x % 8))
        rows.append(bytes([0, *row]))

    def chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 1, 0, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(b"".join(rows))) + chunk(b"IEND", b"")
    path.write_bytes(png)


def scaffold(args: argparse.Namespace) -> Path:
    output_root = Path(args.output_dir)
    app_dir = output_root / args.appid
    if app_dir.exists():
        if not args.force:
            raise SystemExit(f"{app_dir} already exists; pass --force to replace it")
        shutil.rmtree(app_dir)

    values = {
        "APPID": args.appid,
        "NAME": args.name,
        "CATEGORY": args.category,
        "AUTHOR": args.author,
        "SHORT_DESCRIPTION": args.short_description,
        "VERSION": args.version,
    }
    write_text(app_dir / "application.fam", render((TEMPLATE / "application.fam.tpl").read_text(encoding="utf-8"), values))
    write_text(app_dir / f"{args.appid}.c", render((TEMPLATE / "app.c.tpl").read_text(encoding="utf-8"), values))
    write_text(app_dir / "README.md", render((TEMPLATE / "README.md.tpl").read_text(encoding="utf-8"), values))
    write_text(app_dir / "docs" / "changelog.md", render((TEMPLATE / "changelog.md.tpl").read_text(encoding="utf-8"), values))
    write_text(app_dir / "screenshots" / ".gitkeep", "")
    write_icon(app_dir / f"{args.appid}_10px.png")
    return app_dir


def main() -> int:
    args = parse_args()
    validate_args(args)
    app_dir = scaffold(args)
    print(f"Created {app_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
