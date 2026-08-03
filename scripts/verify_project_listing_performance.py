#!/usr/bin/env python3
"""Verify project listings do not eagerly load videos or depend on deploy host."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("en", "tw", "jp")
HOST = "bddgtw-tw.github.io/sunnywardwebsite"


def attributes(tag: str) -> dict[str, str | None]:
    return {
        name: value if value is not None else None
        for name, _, value in re.findall(
            r"([:\w-]+)(?:\s*=\s*([\"'])(.*?)\2)?", tag, re.DOTALL
        )
    }


def local_asset(value: str | None, page: Path) -> Path:
    if not value or not value.startswith("../_assets/projects/"):
        raise AssertionError(f"Non-portable media path in {page}: {value}")
    asset = (page.parent / value).resolve()
    if not asset.is_file() or asset.stat().st_size == 0:
        raise AssertionError(f"Missing media asset in {page}: {value}")
    return asset


for lang in LANGS:
    page = ROOT / lang / "projects.html"
    html = page.read_text(encoding="utf-8")
    assert HOST not in html, f"Hard-coded deployment host remains in {page}"
    sections = re.findall(
        r'<section\b[^>]*class="[^"]*ultimate-case-section[^"]*"[^>]*>(.*?)</section>',
        html,
        re.DOTALL,
    )
    assert len(sections) == 10, f"Expected 10 case sections in {page}"
    case_html = "\n".join(sections)
    videos = [attributes(tag) for tag in re.findall(r"<video\b[^>]*>", case_html)]
    images = [attributes(tag) for tag in re.findall(r"<img\b[^>]*>", case_html)]
    assert len(videos) == 10, f"Expected 10 case videos in {page}"
    assert len(images) == 0, f"Screenshot galleries remain in {page}"
    assert "photo-carousel" not in case_html, f"Carousel markup remains in {page}"
    for video in videos:
        assert "autoplay" not in video and "loop" not in video
        assert "controls" not in video and video.get("data-controls") == "on-demand"
        assert "playsinline" in video
        assert video.get("preload") == "none"
        local_asset(video.get("src"), page)
        local_asset(video.get("poster"), page)
    print(f"verified {page.relative_to(ROOT)}: one opt-in video per project, no screenshot galleries")

print("project listing performance verification passed")
