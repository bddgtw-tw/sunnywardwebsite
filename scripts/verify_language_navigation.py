#!/usr/bin/env python3
"""Verify reciprocal, keyboard-accessible language navigation on every public page."""

from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
LANGS = {"en": "en", "tw": "zh-TW", "jp": "ja"}
checked = 0

for current in LANGS:
    for page in (ROOT / current).glob("**/*.html"):
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        robots = soup.select_one('meta[name="robots"]')
        if robots and "noindex" in robots.get("content", "").lower():
            continue
        relative = page.relative_to(ROOT / current)
        controls = soup.select('button.lang-current[type="button"][aria-label]')
        assert len(controls) == 1, f"Language button missing: {page}"
        desktop = soup.select(".lang-list a.lang-dropdown-item")
        mobile = soup.select(".mobile-language-switch a[data-lang]")
        assert len(desktop) == len(LANGS), f"Desktop language links wrong: {page}"
        assert len(mobile) == len(LANGS), f"Mobile language links wrong: {page}"
        for group in (desktop, mobile):
            assert {link.get("data-lang") for link in group} == set(LANGS), page
            active = [link for link in group if "active" in link.get("class", [])]
            assert len(active) == 1 and active[0].get("data-lang") == current, page
            for link in group:
                target_lang = link["data-lang"]
                target = (page.parent / link["href"]).resolve()
                expected = (ROOT / target_lang / relative).resolve()
                assert target == expected, f"Language path mismatch: {page} -> {link['href']}"
                assert target.is_file(), f"Language target missing: {target}"
                assert link.get("lang") == LANGS[target_lang], f"Language annotation wrong: {page}"
        checked += 1

javascript = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
assert 'e.key !== "Escape"' in javascript
assert 'current.focus()' in javascript
stylesheet = (ROOT / "css" / "style.css").read_text(encoding="utf-8")
assert "\nheader{" not in stylesheet, "Generic header selector would pin content headers"
assert "#site-header{position:fixed" in stylesheet
assert ".nav-actions{display:none}" in stylesheet
print(f"verified reciprocal desktop/mobile language navigation on {checked} public pages")
