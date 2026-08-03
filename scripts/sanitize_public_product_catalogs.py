#!/usr/bin/env python3
"""Reduce localized product catalogues to an explicit public-safe schema."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGS = ("en", "tw", "jp")
PUBLIC_FIELDS = (
    "id",
    "sku",
    "name",
    "brand",
    "category",
    "sub_category",
    "collection",
    "description",
    "materials",
    "dimensions",
    "origin",
    "images",
    "image_dimensions",
    "detail_page",
    "frontend_visible",
    "frontend_status",
    "data_quality",
)


def public_record(record: dict) -> dict:
    clean = {key: record[key] for key in PUBLIC_FIELDS if key in record}
    quality = clean.get("data_quality")
    if isinstance(quality, dict):
        clean["data_quality"] = {
            "image_status": quality["image_status"]
        } if "image_status" in quality else {}
    return clean


def main() -> None:
    for lang in LANGS:
        path = ROOT / lang / "products.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["products"] = [public_record(item) for item in payload["products"]]
        payload["catalog_policy"] = (
            "Public product catalogue. Pricing, suppliers, margins, packaging, "
            "freight and loading data are intentionally excluded."
        )
        payload["total_products"] = len(payload["products"])
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print("Sanitized three localized product catalogues to the public-safe schema.")


if __name__ == "__main__":
    main()
