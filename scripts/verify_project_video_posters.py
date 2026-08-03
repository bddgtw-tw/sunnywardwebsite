#!/usr/bin/env python3
"""Verify public project videos use complete, local poster artwork."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
POSTER_RE = re.compile(r'<video\b[^>]*poster="(?P<poster>[^"]+)"[^>]*>')
posters = 0
title_cards = 0

for lang in ("en", "tw", "jp"):
    for page in sorted((ROOT / lang).rglob("*.html")):
        html = page.read_text(encoding="utf-8")
        if page.name == "projects.html":
            assert html.count('class="uc-video-poster"') == 10, f"Wrong title-card count in {page}"
            assert html.count('class="uc-video-poster__title"') == 10, f"Missing project titles in {page}"
            assert html.count('class="uc-video-poster__play"') == 10, f"Missing play affordance in {page}"
            assert html.count('data-controls="on-demand"') == 10, f"Controls must start behind title cards in {page}"
            title_cards += 10
        for match in POSTER_RE.finditer(html):
            poster = match.group("poster")
            if "_assets/projects/" not in poster:
                continue
            assert poster.endswith("_cropped.jpg"), f"Fragmented project poster in {page}: {poster}"
            asset = (page.parent / poster).resolve()
            assert asset.is_file() and ROOT.resolve() in asset.parents, f"Missing poster: {page} -> {poster}"
            with Image.open(asset) as image:
                assert image.width >= 800 and image.height >= 500, f"Poster too small: {asset}"
            posters += 1

assert posters == 39, f"Expected 39 localized project video posters, found {posters}"
assert title_cards == 30, f"Expected 30 localized listing title cards, found {title_cards}"
css = (ROOT / "css" / "style.css").read_text(encoding="utf-8")
assert ".uc-video-wrap video" in css and "aspect-ratio: 16 / 9" in css
assert "object-fit: cover" in css
javascript = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
assert "uc-video-poster" in javascript and "video.play()" in javascript
print("verified 39 complete video posters and 30 localized project title cards")
