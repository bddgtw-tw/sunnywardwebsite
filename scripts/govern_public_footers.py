#!/usr/bin/env python3
"""Replace legacy landing-page footers with the evidence-bounded shared footer."""

from __future__ import annotations

import re
from pathlib import Path

from render_shared_footer import render_public_footer


ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "about.html", "products.html", "projects.html", "contact.html")

for lang in ("en", "tw", "jp"):
    replacement = render_public_footer(lang, prefix="")
    for name in PAGES:
        page = ROOT / lang / name
        text = page.read_text(encoding="utf-8")
        text, count = re.subn(r'\s*<footer(?:\s[^>]*)?>.*?</footer>', '', text, flags=re.DOTALL)
        if count < 1:
            raise RuntimeError(f"Expected at least one footer in {page}")
        if text.count("</body>") != 1:
            raise RuntimeError(f"Expected one body end in {page}")
        text = text.replace("</body>", f"{replacement}\n</body>", 1)
        page.write_text(text, encoding="utf-8", newline="\n")
        print(f"governed footer {page.relative_to(ROOT)}")
