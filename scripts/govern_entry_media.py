#!/usr/bin/env python3
"""Add deterministic dimensions and loading hints to public entry-page media."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
IMG_RE = re.compile(r"<img\s+[^>]*>")
VIDEO_RE = re.compile(r"<video\s+[^>]*>")
ATTR_RE = re.compile(r'([:\w-]+)="([^"]*)"')
HERO_ASSET = "486466926_1193879656080876_2767098548785792068_n_hero.jpg"


def replace_attrs(tag: str, additions: dict[str, str]) -> str:
    for key in additions:
        tag = re.sub(rf'\s{re.escape(key)}="[^"]*"', "", tag)
    suffix = "".join(f' {key}="{value}"' for key, value in additions.items())
    return tag[:-1] + suffix + ">"


def local_dimensions(page: Path, url: str) -> tuple[int, int]:
    asset = (page.parent / urlsplit(url).path).resolve()
    if not asset.is_file() or ROOT.resolve() not in asset.parents:
        raise RuntimeError(f"Missing or external entry asset: {page} -> {url}")
    with Image.open(asset) as image:
        return image.width, image.height


def govern_image(page: Path, tag: str) -> str:
    attrs = dict(ATTR_RE.findall(tag))
    src = attrs.get("src", "")
    if not src:
        return replace_attrs(tag, {"width": "1200", "height": "900", "decoding": "async"})
    if page.name == "index.html" and src.endswith(HERO_ASSET):
        width, height = local_dimensions(page, src)
        return replace_attrs(tag, {"width": str(width), "height": str(height), "loading": "eager", "fetchpriority": "high", "decoding": "async"})
    width, height = local_dimensions(page, src)
    return replace_attrs(tag, {"width": str(width), "height": str(height), "decoding": "async"})


def govern_video(page: Path, tag: str) -> str:
    attrs = dict(ATTR_RE.findall(tag))
    if not attrs.get("poster"):
        return replace_attrs(tag, {"width": "1200", "height": "675", "preload": "none"})
    width, height = local_dimensions(page, attrs["poster"])
    return replace_attrs(tag, {"width": str(width), "height": str(height)})


for lang in ("en", "tw", "jp"):
    for name in ("index.html", "projects.html"):
        page = ROOT / lang / name
        text = page.read_text(encoding="utf-8")
        text = IMG_RE.sub(lambda match: govern_image(page, match.group(0)), text)
        text = VIDEO_RE.sub(lambda match: govern_video(page, match.group(0)), text)
        page.write_text(text, encoding="utf-8", newline="\n")
        print(f"governed entry media {page.relative_to(ROOT)}")


for lang in ("en", "tw", "jp"):
    page = ROOT / lang / "products.html"
    text = page.read_text(encoding="utf-8")
    old = 'class="product-img" loading="lazy" onerror="markImagePending(this)"'
    new = 'class="product-img" width="${p.image_dimensions[0][0]}" height="${p.image_dimensions[0][1]}" loading="lazy" decoding="async" onerror="markImagePending(this)"'
    if old in text:
        text = text.replace(old, new, 1)
    elif new not in text:
        raise RuntimeError(f"Dynamic product image template not found: {page}")
    text = re.sub(
        r'<img id="modal-product-img" src="" alt=""(?:\s[^>]*)?>',
        '<img id="modal-product-img" src="" alt="" width="1200" height="900" decoding="async">',
        text,
        count=1,
    )
    page.write_text(text, encoding="utf-8", newline="\n")
    print(f"governed dynamic catalogue media {page.relative_to(ROOT)}")
