from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
verified_source = json.loads((ROOT / "data" / "verified_product_pages.json").read_text(encoding="utf-8"))["products"]
verified_skus = {item["sku"] for item in verified_source}
assert len(verified_skus) == 3

sku_category_check = {}
sku_image_check = {}
for lang in ("en", "tw", "jp"):
    catalog = json.loads((ROOT / lang / "products.json").read_text(encoding="utf-8"))["products"]
    assert all("pricing" not in item and "logistics" not in item and "specs" not in item for item in catalog)
    
    # Assert unique SKUs
    skus = [item["sku"] for item in catalog]
    assert len(skus) == len(set(skus)), f"Duplicate SKUs found: {lang}"
    
    # Assert total count is 149
    assert len(catalog) == 149, f"Expected 149 products in catalog, found {len(catalog)} for {lang}"
    
    # Assert category counts
    counts = {"outdoor": 0, "office": 0, "project": 0}
    for item in catalog:
        cat = item.get("category")
        assert cat in counts, f"Unknown category '{cat}' in {lang}/{item['sku']}"
        counts[cat] += 1
        
        # Track SKU mapping to check cross-language consistency
        sku = item["sku"]
        if sku not in sku_category_check:
            sku_category_check[sku] = {}
        sku_category_check[sku][lang] = cat
        if sku not in sku_image_check:
            sku_image_check[sku] = {}
        sku_image_check[sku][lang] = tuple(item.get("images", []))
        
    assert counts["outdoor"] == 27, f"Expected 27 outdoor products, found {counts['outdoor']} in {lang}"
    assert counts["office"] == 21, f"Expected 21 office products, found {counts['office']} in {lang}"
    assert counts["project"] == 101, f"Expected 101 project products, found {counts['project']} in {lang}"
    
    public = [item for item in catalog if item.get("detail_page") and item.get("frontend_visible") is True and item.get("frontend_status") == "published" and (item.get("data_quality") or {}).get("image_status") == "verified_reference"]
    assert verified_skus.issubset({item["sku"] for item in public}), f"Public product mismatch: {lang}"

    page = (ROOT / lang / "products.html").read_text(encoding="utf-8")
    assert "Boolean(product.detail_page)" in page
    assert "product.frontend_status === 'published'" in page
    assert "const results = getVisibleProducts().filter(p => {" in page
    assert "key === 'materials' ||" not in page
    assert "if (document.querySelector('.matcher-option-top') && document.querySelector('.matcher-option-base'))" in page
    assert page.count("function shouldShowOnFrontend(product)") == 1

# Assert cross-language category consistency
for sku, mappings in sku_category_check.items():
    assert len(set(mappings.values())) == 1, f"Category mismatch for SKU {sku} across languages: {mappings}"
for sku, mappings in sku_image_check.items():
    assert len(set(mappings.values())) == 1, f"Image mismatch for SKU {sku} across languages: {mappings}"
print("Verified that three public catalogues expose governed and auxiliary product records.")
