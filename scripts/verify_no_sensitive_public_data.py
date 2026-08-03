#!/usr/bin/env python3
"""Fail the release when public catalogues or tracked files expose internal data."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_FIELDS = {
    "id", "sku", "name", "brand", "category", "sub_category", "collection",
    "description", "materials", "dimensions", "origin", "images",
    "image_dimensions", "detail_page", "frontend_visible", "frontend_status",
    "data_quality",
}
FORBIDDEN_KEYS = {
    "pricing", "price", "fob", "fob_usd", "cost", "supplier",
    "supplier_name", "supplier_code", "margin", "internal_margin", "logistics",
    "cbm", "capacity_40hq", "packaging_measurement", "source_filename",
    "source_file", "internal_source_filename",
}
FORBIDDEN_TRACKED_SUFFIXES = {".xlsx", ".xls"}
FORBIDDEN_TRACKED_PATHS = {
    "data/all_products_structured.json",
    "data/outdoor_products.json",
    "data/outdoor_products_structured.json",
}


def nested_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for item in value.values() for key in nested_keys(item)}
    if isinstance(value, list):
        return {key for item in value for key in nested_keys(item)}
    return set()


def main() -> None:
    for lang in ("en", "tw", "jp"):
        path = ROOT / lang / "products.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        for record in payload["products"]:
            extra = set(record) - ALLOWED_FIELDS
            assert not extra, f"Non-public fields in {path}: {sorted(extra)}"
            exposed = nested_keys(record) & FORBIDDEN_KEYS
            assert not exposed, f"Sensitive keys in {path}: {sorted(exposed)}"

    tracked = subprocess.check_output(
        ["git", "ls-files"], cwd=ROOT, text=True, encoding="utf-8"
    ).splitlines()
    unsafe = [
        path for path in tracked
        if Path(path).suffix.lower() in FORBIDDEN_TRACKED_SUFFIXES
        or path.replace("\\", "/") in FORBIDDEN_TRACKED_PATHS
    ]
    assert not unsafe, f"Internal source files are tracked: {unsafe}"
    print("Verified public catalogues and tracked files contain no governed sensitive product data.")


if __name__ == "__main__":
    main()
