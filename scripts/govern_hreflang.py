#!/usr/bin/env python3
"""Normalize indexable pages to absolute, reciprocal hreflang URLs."""

from __future__ import annotations

import re
from pathlib import Path

from site_config import DEFAULT_LANGUAGE, LANGUAGES, ROOT, public_url


LINK = re.compile(
    r'(?m)^\s*<link\s+rel="alternate"\s+hreflang="(?P<code>[^"]+)"\s+href="[^"]+">\s*$'
)


def suffix_for(page: Path, folder: str) -> str:
    relative = page.relative_to(ROOT / folder).as_posix()
    return "" if relative == "index.html" else relative


def href(folder: str, suffix: str) -> str:
    return public_url(f"{folder}/{suffix}")


changed = 0
for folder in LANGUAGES:
    for page in (ROOT / folder).glob("**/*.html"):
        text = page.read_text(encoding="utf-8")
        robots = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', text, re.I)
        if robots and "noindex" in robots.group(1).lower():
            continue
        suffix = suffix_for(page, folder)
        expected = {"x-default": href(DEFAULT_LANGUAGE, suffix)}
        expected.update({code: href(target, suffix) for target, code in LANGUAGES.items()})
        found = LINK.findall(text)
        if set(found) != set(expected):
            raise RuntimeError(f"Unexpected hreflang set in {page}: {found}")

        def replace(match: re.Match[str]) -> str:
            code = match.group("code")
            return f'  <link rel="alternate" hreflang="{code}" href="{expected[code]}">'

        updated = LINK.sub(replace, text)
        if updated != text:
            page.write_text(updated, encoding="utf-8")
            changed += 1

print(f"governed absolute hreflang on {changed} changed pages")
