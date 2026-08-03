#!/usr/bin/env python3
"""Verify that public pages stay within the current evidence boundary."""

from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
HOME_TITLES = {
    "en": "From Design Concepts to Commercial Spaces",
    "tw": "從設計概念，到真正落地的商業空間",
    "jp": "デザインの構想を、実際の商業空間へ",
}
BANNED = (
    "Est. 1990", "1990年創立", "創立於 1990 年", "within 24 hours", "24 小時內", "24時間以内",
    'location: "Global"', "全球實績", "Inquiry Sent Successfully", "詢價單已成功送出", "お問い合わせが送信されました",
    'id="rfq-form"', "openRfqModal", "custom contract manufacturing", "特注コントラクト製造",
)

for lang in ("en", "tw", "jp"):
    home = BeautifulSoup((ROOT / lang / "index.html").read_text(encoding="utf-8"), "html.parser")
    assert home.select_one("h1").get_text(" ", strip=True) == HOME_TITLES[lang], f"Homepage positioning mismatch: {lang}"
    assert not home.select(".hero__stats, .hero__stat-item"), f"Internal record counters exposed on homepage: {lang}"
    for page in (ROOT / lang).glob("**/*.html"):
        text = page.read_text(encoding="utf-8")
        for claim in BANNED:
            assert claim not in text, f"Unsupported or misleading claim in {page}: {claim}"
    products = (ROOT / lang / "products.html").read_text(encoding="utf-8")
    assert "window.location.href = `contact.html?product=${encodeURIComponent(sku)}`" in products, f"Governed RFQ routing missing: {lang}"
    assert products.count("<footer") == 1, f"Duplicate catalogue footer: {lang}"

print("verified bounded homepage, location, contact and RFQ claims across three languages")
