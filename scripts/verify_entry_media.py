#!/usr/bin/env python3
"""Verify stable dimensions and bounded loading on public entry pages."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlsplit

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
HERO_ASSET = "486466926_1193879656080876_2767098548785792068_n_hero.jpg"
checked_images = 0

for lang in ("en", "tw", "jp"):
    for name in ("index.html", "projects.html"):
        page = ROOT / lang / name
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        for image in soup.select("img[src]"):
            assert image.get("width") and image.get("height"), f"Image dimensions missing: {page} -> {image['src']}"
            assert image.get("decoding") == "async", f"Async decoding missing: {page} -> {image['src']}"
            if not image["src"]:
                assert image.get("id") == "project-modal-img", f"Unexpected empty image source: {page}"
            elif page.name == "index.html" and image["src"].endswith(HERO_ASSET):
                assert image.get("loading") == "eager" and image.get("fetchpriority") == "high", f"Hero priority wrong: {page}"
                asset = (page.parent / urlsplit(image["src"]).path).resolve()
                assert asset.is_file() and asset.stat().st_size < 100_000, f"Hero image missing or too large: {asset}"
            else:
                asset = (page.parent / urlsplit(image["src"]).path).resolve()
                assert asset.is_file(), f"Entry image missing: {page} -> {image['src']}"
                assert asset.stat().st_size < 100_000, f"Entry image exceeds 100 KB: {asset}"
                assert image.get("loading") == "lazy", f"Below-fold entry image not lazy: {page} -> {image['src']}"
            checked_images += 1
        for video in soup.select("video"):
            if "hero__video" in video.get("class", []):
                assert page.name == "index.html", f"Hero video outside homepage: {page}"
                assert video.get("preload") == "metadata", f"Hero video preload must stay bounded: {page}"
                for attribute in ("autoplay", "muted", "playsinline"):
                    assert video.has_attr(attribute), f"Hero video missing {attribute}: {page}"
                assert not video.has_attr("loop"), f"Hero video must play once and hold its final frame: {page}"
                source = video.select_one('source[type="video/mp4"]')
                assert source and source.get("src"), f"Hero video source missing: {page}"
                asset = (page.parent / urlsplit(source["src"]).path).resolve()
                assert asset.is_file() and asset.stat().st_size < 2_100_000, f"Hero web video missing or too large: {asset}"
                poster = (page.parent / urlsplit(video["poster"]).path).resolve()
                assert poster.is_file() and poster.stat().st_size < 400_000, f"Hero poster missing or too large: {poster}"
            else:
                assert video.get("preload") == "none", f"Entry video must be opt-in: {page}"
            assert video.get("width") and video.get("height"), f"Video dimensions missing: {page}"

    catalogue = json.loads((ROOT / lang / "products.json").read_text(encoding="utf-8"))
    for product in catalogue["products"]:
        assert product.get("image_dimensions"), f"Catalogue image dimensions missing: {lang}/{product['sku']}"
    product_page = (ROOT / lang / "products.html").read_text(encoding="utf-8")
    assert 'width="${p.image_dimensions[0][0]}"' in product_page, f"Dynamic image width missing: {lang}"
    assert 'height="${p.image_dimensions[0][1]}"' in product_page, f"Dynamic image height missing: {lang}"
    assert 'loading="lazy" decoding="async"' in product_page, f"Dynamic loading hints missing: {lang}"
    product_soup = BeautifulSoup(product_page, "html.parser")
    modal_image = product_soup.select_one('img#modal-product-img[src=""]')
    assert modal_image and modal_image.get("width") == "1200" and modal_image.get("height") == "900", f"Product modal canvas missing: {lang}"
    assert modal_image.get("decoding") == "async", f"Product modal decoding hint missing: {lang}"

assert checked_images == 21, f"Expected 21 non-gallery entry images, checked {checked_images}"
print("verified dimensions and bounded loading on 21 non-gallery entry-page images")
