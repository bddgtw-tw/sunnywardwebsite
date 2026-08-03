from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
verified = json.loads((ROOT / "data" / "verified_product_pages.json").read_text(encoding="utf-8"))["products"]
verified_skus = [item["sku"] for item in verified]


for lang in ("en", "tw", "jp"):
    path = ROOT / lang / "products.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    by_sku = {item["sku"]: item for item in payload["products"]}
    missing = [sku for sku in verified_skus if sku not in by_sku]
    if missing:
        raise RuntimeError(f"Verified SKUs missing from {path}: {missing}")
    public_products = [by_sku[sku] for sku in verified_skus]
    payload["products"] = public_products
    payload["catalog_policy"] = "Public pilot catalogue: only products with verified source records and independent detail pages are included."
    payload["total_products"] = len(public_products)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

print(f"Built three public product catalogues with {len(verified_skus)} verified products each.")
