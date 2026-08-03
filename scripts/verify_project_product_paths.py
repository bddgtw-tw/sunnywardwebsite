#!/usr/bin/env python3
"""Verify bounded, reciprocal product discovery from project records."""

from __future__ import annotations

import json
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = json.loads((ROOT / "data" / "verified_project_pages.json").read_text(encoding="utf-8"))["projects"]
PRODUCTS = json.loads((ROOT / "data" / "verified_product_pages.json").read_text(encoding="utf-8"))["products"]
DISCLAIMERS = {
    "en": "Final selection depends on the project brief",
    "tw": "最終選擇仍依專案需求而定",
    "jp": "最終選定は案件要件に合わせて行います",
}
EMPTY_NOTES = {
    "en": "Final selection depends on the project brief",
    "tw": "最終選擇仍依專案需求而定",
    "jp": "最終選定は案件要件に合わせて行います",
}


checked = 0
for lang, disclaimer in DISCLAIMERS.items():
    for project in PROJECTS:
        page = ROOT / lang / "projects" / f"{project['slug']}.html"
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        section = soup.select_one("section.project-product-planning")
        assert section, f"Planning section missing: {page}"
        section_text = section.get_text(" ", strip=True)

        expected = {
            f"../products/{product['slug']}.html"
            for product in PRODUCTS
            if product.get("planning_reference") == project["slug"]
        }
        actual = {link["href"] for link in section.select('a[href^="../products/"]')}
        assert actual == expected, f"Product planning links mismatch: {page}: {actual} != {expected}"
        if expected:
            assert disclaimer in section_text, f"Bounded-use note missing: {page}"
            for href in actual:
                assert (page.parent / href).resolve().is_file(), f"Broken product path: {page} -> {href}"
        else:
            assert EMPTY_NOTES[lang] in section_text, f"No-match disclosure missing: {page}"
            assert section.select_one('a[href="../products.html"]'), f"Catalogue fallback missing: {page}"
        checked += 1

for product in PRODUCTS:
    reference = product.get("planning_reference")
    assert any(project["slug"] == reference for project in PROJECTS), f"Unknown project reference: {product['sku']}"

assert checked == 9, f"Expected 9 localized project pages, checked {checked}"
print("verified bounded project-to-product discovery on 9 project pages")
