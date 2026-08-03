#!/usr/bin/env python3
"""Verify evidence-bounded shared footers on every indexable public page."""

from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
LANGS = {
    "en": "Commercial furniture sourcing",
    "tw": "家具選品",
    "jp": "家具調達",
}
EXPECTED_NAV = {"index.html", "about.html", "products.html", "projects.html", "contact.html"}
REQUIRED_TEXT = (
    "SUNNYWARD PTE LTD",
    "27, Jalan Impian Emas 18",
    "101 Upper Cross Street",
)
BANNED_CLAIMS = (
    "premium commercial furniture manufacturer",
    "contract-grade custom production worldwide",
    "最高剛性",
    "高耐用度家具",
    "業務用特注家具メーカー",
)


checked = 0
for lang, evidence_phrase in LANGS.items():
    lang_root = ROOT / lang
    for page in lang_root.glob("**/*.html"):
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        robots = soup.select_one('meta[name="robots"]')
        if robots and "noindex" in robots.get("content", "").lower():
            continue

        footers = soup.select("footer")
        assert len(footers) == 1 and "detail-footer" in footers[0].get("class", []), f"Expected exactly one shared footer: {page}"
        footer = footers[0]
        footer_text = footer.get_text(" ", strip=True)
        footer_lower = footer_text.lower()

        for required in REQUIRED_TEXT:
            assert required in footer_text, f"Missing footer evidence in {page}: {required}"
        assert evidence_phrase in footer_text, f"Missing localized evidence statement: {page}"
        assert not any(claim.lower() in footer_lower for claim in BANNED_CLAIMS), (
            f"Unsupported footer claim remains: {page}"
        )
        assert "info@sunnyward.com" not in footer_lower, f"Legacy email remains: {page}"

        hrefs = [link.get("href", "") for link in footer.select("a[href]")]
        assert hrefs.count("mailto:sales@sunnyward.com") == 2, f"Sales email mismatch: {page}"
        assert "https://wa.me/60165262894" in hrefs, f"WhatsApp missing: {page}"
        assert "https://wa.me/60167252894" in hrefs, f"WhatsApp 2 missing: {page}"
        assert "tel:+60165262894" in hrefs, f"Telephone missing: {page}"
        assert "tel:+60167252894" in hrefs, f"Telephone 2 missing: {page}"

        nav_links = footer.select(".footer-links a[href]")[:5]
        assert len(nav_links) == 5, f"Footer navigation incomplete: {page}"
        targets = set()
        for link in nav_links:
            target = (page.parent / link["href"]).resolve()
            assert target.is_file(), f"Broken footer link: {page} -> {link['href']}"
            assert target.parent == lang_root.resolve(), f"Cross-locale footer link: {page}"
            targets.add(target.name)
        assert targets == EXPECTED_NAV, f"Footer navigation mismatch: {page}"

        assert len(footer.select("h2.footer-col__title")) == 3, f"Heading structure mismatch: {page}"
        assert not footer.select("h5"), f"Legacy heading level remains: {page}"
        checked += 1

assert checked == 33, f"Expected 33 indexable pages, checked {checked}"
print(f"verified evidence-bounded shared footer on {checked} public pages")
