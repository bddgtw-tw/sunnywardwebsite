#!/usr/bin/env python3
"""Synchronize the structured B2B enquiry brief across contact pages."""

from __future__ import annotations

import re
from pathlib import Path

from render_contact_brief import render_contact_form


ROOT = Path(__file__).resolve().parents[1]
for lang in ("en", "tw", "jp"):
    page = ROOT / lang / "contact.html"
    text = page.read_text(encoding="utf-8")
    replacement = render_contact_form(lang)
    text, count = re.subn(
        r'<form class="contact-form" id="contact-inquiry-form">.*?</form>',
        replacement,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        raise RuntimeError(f"Expected one enquiry form in {page}")
    text = re.sub(r'inquiry-context\.js\?v=[^"\']+', 'inquiry-context.js?v=20260715-b2b-brief', text)
    text = re.sub(r'contact-inquiry\.js\?v=[^"\']+', 'contact-inquiry.js?v=20260715-b2b-brief', text)
    page.write_text(text, encoding="utf-8", newline="\n")
    print(f"governed B2B enquiry brief {page.relative_to(ROOT)}")
