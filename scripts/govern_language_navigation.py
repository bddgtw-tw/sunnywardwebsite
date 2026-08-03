#!/usr/bin/env python3
"""Make language navigation keyboard-accessible on multilingual landing pages."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGS = {"en": ("EN", "English", "en"), "tw": ("繁中", "繁中", "zh-TW"), "jp": ("日本語", "日本語", "ja")}
PAGES = ("index.html", "about.html", "products.html", "projects.html", "contact.html")


def mobile_switch(current: str, page_name: str) -> str:
    links = "".join(
        f'<a href="{page_name if folder == current else f"../{folder}/{page_name}"}" '
        f'class="{"active" if folder == current else ""}" data-lang="{folder}" lang="{html_lang}">{label}</a>'
        for folder, (_, label, html_lang) in LANGS.items()
    )
    return f'<div class="mobile-language-switch" aria-label="Language"><span>Language</span><div>{links}</div></div>'


for folder, (short, _, _) in LANGS.items():
    for page_name in PAGES:
        path = ROOT / folder / page_name
        text = path.read_text(encoding="utf-8")
        text, count = re.subn(
            r'<(?:div|button)\b(?=[^>]*class="[^"]*lang-current[^"]*")[^>]*>.*?</(?:div|button)>',
            f'<button type="button" class="lang-current" aria-label="Select language">{short} ▾</button>',
            text,
            count=1,
            flags=re.DOTALL,
        )
        if count != 1:
            raise RuntimeError(f"Missing desktop language control: {path}")
        def annotate_language(match: re.Match[str]) -> str:
            tag = match.group(0)
            if re.search(r'\slang="', tag):
                return tag
            target = re.search(r'data-lang="(en|tw|jp)"', tag).group(1)
            return tag[:-1] + f' lang="{LANGS[target][2]}">'

        text = re.sub(
            r'<a\b(?=[^>]*class="lang-dropdown-item)(?=[^>]*data-lang="(?:en|tw|jp)")[^>]*>',
            annotate_language,
            text,
        )
        if 'class="mobile-language-switch"' not in text:
            pattern = r'(<nav class="mobile-drawer" id="mobile-drawer">.*?)(</nav>)'
            text, count = re.subn(
                pattern,
                lambda match: match.group(1) + mobile_switch(folder, page_name) + match.group(2),
                text,
                count=1,
                flags=re.DOTALL,
            )
            if count != 1:
                raise RuntimeError(f"Missing mobile drawer: {path}")
        text = re.sub(r'href="\.\./css/style\.css(?:\?[^\"]*)?"', 'href="../css/style.css?v=20260715-b2b-paths"', text)
        text = re.sub(r'src="\.\./js/main\.js(?:\?[^\"]*)?"', 'src="../js/main.js?v=20260715-b2b-paths"', text)
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"governed {path.relative_to(ROOT)}")
