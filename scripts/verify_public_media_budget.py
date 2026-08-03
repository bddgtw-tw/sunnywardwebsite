#!/usr/bin/env python3
"""Guard the verified public media set against accidental page-weight regressions."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = json.loads((ROOT / "data" / "verified_product_pages.json").read_text(encoding="utf-8"))["products"]
PROJECTS = json.loads((ROOT / "data" / "verified_project_pages.json").read_text(encoding="utf-8"))["projects"]

MAX_PRODUCT_IMAGE = 500_000
MAX_PRODUCT_GALLERY = 1_500_000
MAX_PROJECT_POSTER = 250_000

for product in PRODUCTS:
    assets = [ROOT / path for path in product["images"]]
    sizes = [path.stat().st_size for path in assets]
    assert all(path.is_file() and size > 0 for path, size in zip(assets, sizes, strict=True))
    assert max(sizes) <= MAX_PRODUCT_IMAGE, f"Product image budget exceeded: {product['sku']} {max(sizes)}"
    assert sum(sizes) <= MAX_PRODUCT_GALLERY, f"Product gallery budget exceeded: {product['sku']} {sum(sizes)}"
    assert len(product["image_dimensions"]) == len(assets)
    print(f"product {product['sku']}: {sum(sizes):,} bytes across {len(assets)} images")

for project in PROJECTS:
    posters = [ROOT / path for path in project["images"]]
    sizes = [path.stat().st_size for path in posters]
    assert max(sizes) <= MAX_PROJECT_POSTER, f"Project poster budget exceeded: {project['slug']}"
    assert len(project["image_dimensions"]) == len(posters)
    print(f"project {project['slug']}: {sum(sizes):,} image bytes; video loads on demand")

print("public media budget verification passed")
