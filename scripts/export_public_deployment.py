#!/usr/bin/env python3
"""Create a history-free, allowlisted public deployment from the private source repo."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT_FILES = (".nojekyll", "404.html", "index.html", "llms.txt", "robots.txt", "sitemap.xml")
PUBLIC_DIRS = ("css", "js", "en", "tw", "jp", "projects")
ASSET_ROOTS = ("Product_Images", "_assets", "catalogs")
FORBIDDEN_SUFFIXES = {".xlsx", ".xls", ".py", ".ps1", ".csv", ".sqlite", ".db"}
FORBIDDEN_TERMS = (
    "fob_usd", "fob usd", "capacity_40hq", "40hq capacity",
    "packaging_measurement", "internal_margin", "supplier_code",
    "supplier_name", '"pricing"', '"logistics"',
)


def copy_file(relative: str, destination: Path) -> None:
    source = ROOT / Path(relative)
    if not source.is_file():
        raise RuntimeError(f"Referenced public file is missing: {relative}")
    target = destination / Path(relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def referenced_assets(destination: Path) -> set[str]:
    references: set[str] = set()
    candidates = list(destination.rglob("*.html")) + list(destination.rglob("*.json")) + list(destination.rglob("*.css"))
    for path in candidates:
        text = path.read_text(encoding="utf-8")
        for root in ASSET_ROOTS:
            pattern = rf'(?:https://sunnyward\.com/|(?:\.\./)+)?({re.escape(root)}/[^"\'<>?#)]+)'
            for match in re.finditer(pattern, text):
                relative = PurePosixPath(match.group(1)).as_posix()
                references.add(relative)
    return references


def verify(destination: Path) -> None:
    files = [path for path in destination.rglob("*") if path.is_file()]
    forbidden_files = [str(path.relative_to(destination)) for path in files if path.suffix.lower() in FORBIDDEN_SUFFIXES]
    if forbidden_files:
        raise RuntimeError(f"Forbidden files in public deployment: {forbidden_files}")

    leaks: list[str] = []
    for path in files:
        if path.suffix.lower() not in {".html", ".json", ".js", ".css", ".txt", ".xml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="strict").lower()
        matches = [term for term in FORBIDDEN_TERMS if term in text]
        if matches:
            leaks.append(f"{path.relative_to(destination)}: {matches}")
    if leaks:
        raise RuntimeError("Sensitive terms in public deployment:\n" + "\n".join(leaks))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    destination = args.destination.resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise RuntimeError("Deployment destination must be outside the private source repository.")
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)

    for relative in PUBLIC_ROOT_FILES:
        copy_file(relative, destination)
    for directory in PUBLIC_DIRS:
        shutil.copytree(ROOT / directory, destination / directory, copy_function=shutil.copyfile)
    for relative in sorted(referenced_assets(destination)):
        copy_file(relative, destination)

    products = sum(len(json.loads((destination / lang / "products.json").read_text(encoding="utf-8"))["products"]) for lang in ("en", "tw", "jp"))
    verify(destination)
    count = sum(1 for path in destination.rglob("*") if path.is_file())
    size = sum(path.stat().st_size for path in destination.rglob("*") if path.is_file())
    print(f"Public deployment verified: {count} files, {size / 1024 / 1024:.1f} MiB, {products} localized product records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
