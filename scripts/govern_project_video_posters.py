#!/usr/bin/env python3
"""Use complete project collages instead of cropped social tiles as video posters."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VIDEO_RE = re.compile(r"<video\b[^>]*\bposter=\"(?P<poster>[^\"]+)\"[^>]*>")
SECTION_RE = re.compile(
    r'(?P<open><section\b[^>]*class="[^"]*ultimate-case-section[^"]*"[^>]*data-space="(?P<space>[^"]+)"[^>]*>)'
    r'(?P<body>.*?)</section>',
    re.DOTALL,
)
OVERLAY_RE = re.compile(r'\s*<button\b(?=[^>]*class="[^"]*uc-video-poster[^"]*")[^>]*>.*?</button>\s*', re.DOTALL)
SPACE_LABELS = {
    "en": {"fb": "Dining / F&B", "office": "Office & Training", "spa": "Spa & Wellness", "resort": "Resort & Public"},
    "tw": {"fb": "餐飲空間", "office": "辦公與培訓空間", "spa": "SPA 與健康空間", "resort": "度假與公共空間"},
    "jp": {"fb": "飲食・F&B空間", "office": "オフィス・研修空間", "spa": "スパ・ウェルネス空間", "resort": "リゾート・公共空間"},
}
PLAY_LABELS = {"en": "Play project film", "tw": "播放專案影片", "jp": "プロジェクト映像を再生"}
EYEBROW_LABELS = {"en": "PROJECT FILM", "tw": "專案影片", "jp": "プロジェクト映像"}


def govern(page: Path) -> int:
    text = page.read_text(encoding="utf-8")
    changed = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal changed
        poster = match.group("poster")
        if not poster.endswith("_q1.jpg"):
            return match.group(0)
        complete = poster.removesuffix("_q1.jpg") + "_cropped.jpg"
        asset = (page.parent / complete).resolve()
        if not asset.is_file() or ROOT.resolve() not in asset.parents:
            raise RuntimeError(f"Missing complete project poster: {page} -> {complete}")
        changed += 1
        return match.group(0).replace(f'poster="{poster}"', f'poster="{complete}"')

    governed = VIDEO_RE.sub(replace, text)
    lang = page.parent.name
    if page.name == "projects.html" and lang in SPACE_LABELS:
        def add_title_card(section_match: re.Match[str]) -> str:
            body = OVERLAY_RE.sub("\n", section_match.group("body"))
            body = re.sub(
                r'<video\b(?P<attrs>[^>]*)>',
                lambda video_match: '<video' + re.sub(
                    r'\s(?:controls|data-controls="[^"]*")(?=\s|$)',
                    '',
                    video_match.group('attrs'),
                ) + ' data-controls="on-demand">',
                body,
                count=1,
            )
            title_match = re.search(r"<h2>(.*?)</h2>", body, re.DOTALL)
            meta_match = re.search(r'<span class="meta">.*?([0-9]{4}-[0-9]{2})</span>', body, re.DOTALL)
            wrap_match = re.search(r'<div class="uc-video-wrap">\s*', body)
            if not title_match or not meta_match or not wrap_match:
                raise RuntimeError(f"Missing title-card source in {page}: {section_match.group('space')}")
            title = html.unescape(re.sub(r"<[^>]+>", "", title_match.group(1))).strip()
            space = SPACE_LABELS[lang].get(section_match.group("space"), section_match.group("space"))
            play = PLAY_LABELS[lang]
            eyebrow = EYEBROW_LABELS[lang]
            card = (
                '<button class="uc-video-poster" type="button" '
                f'aria-label="{html.escape(play)}: {html.escape(title)}">'
                f'<span class="uc-video-poster__eyebrow">{html.escape(eyebrow)}</span>'
                f'<span class="uc-video-poster__title">{html.escape(title)}</span>'
                '<span class="uc-video-poster__footer">'
                f'<span>{html.escape(space)} · {meta_match.group(1)}</span>'
                '<span class="uc-video-poster__play" aria-hidden="true">▶</span>'
                '</span></button>\n            '
            )
            _, end = wrap_match.span()
            body = body[:end] + card + body[end:]
            return section_match.group("open") + body + "</section>"

        governed, cards = SECTION_RE.subn(add_title_card, governed)
        if cards != 10:
            raise RuntimeError(f"Expected 10 project title cards in {page}, found {cards}")
    if changed:
        page.write_text(governed, encoding="utf-8", newline="\n")
        print(f"governed {changed} project video poster(s) in {page.relative_to(ROOT)}")
    elif governed != text:
        page.write_text(governed, encoding="utf-8", newline="\n")
        print(f"governed project title cards in {page.relative_to(ROOT)}")
    return changed


total = 0
for lang in ("en", "tw", "jp"):
    for page in sorted((ROOT / lang).rglob("*.html")):
        total += govern(page)

remaining = []
for lang in ("en", "tw", "jp"):
    for page in sorted((ROOT / lang).rglob("*.html")):
        html = page.read_text(encoding="utf-8")
        if re.search(r'<video\b[^>]*poster="[^"]+_q1\.jpg"', html):
            remaining.append(str(page.relative_to(ROOT)))
if remaining:
    raise RuntimeError(f"Cropped social-tile posters remain: {remaining}")
print(f"project video poster governance complete: {total} changed")
