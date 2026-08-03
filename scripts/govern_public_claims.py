#!/usr/bin/env python3
"""Remove unsupported public claims and route catalogue RFQs to the governed enquiry page."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTACT_INTRO = {
    "en": "Share the product, project type, quantity, delivery location and target timing. The business development team will review the information provided and continue the discussion by Email or WhatsApp.",
    "tw": "請提供產品、專案類型、數量、交貨地點與目標時程；商務開發小組將依您提供的資訊審閱需求，並透過 Email 或 WhatsApp 繼續聯繫。",
    "jp": "製品、プロジェクト種別、数量、納品先、希望時期をご記入ください。ご提供いただいた情報を営業窓口で確認し、Email または WhatsApp でご連絡します。",
}
CONTACT_INTRO.update({
    "en": "Tell us briefly what you are planning. We will follow up by Email or WhatsApp.",
    "tw": "簡單告訴我們您正在規劃的家具或空間，我們會透過 Email 或 WhatsApp 與您聯繫。",
    "jp": "ご検討中の家具や空間について簡単にお聞かせください。Email または WhatsApp でご連絡します。",
})
UNPUBLISHED_LOCATION = {"en": "Location not published", "tw": "地點未公開", "jp": "所在地非公開"}


for lang in ("en", "tw", "jp"):
    contact = ROOT / lang / "contact.html"
    text = contact.read_text(encoding="utf-8")
    text, count = re.subn(
        r'(<div class="section-header scroll-reveal">.*?<h1>.*?</h1>)\s*<p>.*?</p>',
        rf'\1\n        <p>{CONTACT_INTRO[lang]}</p>',
        text,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        raise RuntimeError(f"Contact introduction not found: {contact}")
    
    # Update direct lines WhatsApp info
    whatsapp_info = {
        "en": 'WhatsApp: <a href="https://wa.me/60165262894" target="_blank" rel="noopener">+6016-526 2894</a> &amp; <a href="https://wa.me/60167252894" target="_blank" rel="noopener">+6016-725 2894</a>',
        "tw": 'WhatsApp：<a href="https://wa.me/60165262894" target="_blank" rel="noopener">+6016-526 2894</a> &amp; <a href="https://wa.me/60167252894" target="_blank" rel="noopener">+6016-725 2894</a>',
        "jp": 'WhatsApp：<a href="https://wa.me/60165262894" target="_blank" rel="noopener">+6016-526 2894</a> &amp; <a href="https://wa.me/60167252894" target="_blank" rel="noopener">+6016-725 2894</a>',
    }
    text, wa_count = re.subn(
        r'(<p style="font-size:1\.1rem; font-weight: 500; margin-top:0\.5rem;">\s*)WhatsApp.*?(</p>)',
        rf'\1{whatsapp_info[lang]}\2',
        text,
        count=1,
        flags=re.DOTALL,
    )
    if wa_count != 1:
        raise RuntimeError(f"WhatsApp direct line not found: {contact}")
        
    contact.write_text(text, encoding="utf-8", newline="\n")

    projects = ROOT / lang / "projects.html"
    text = projects.read_text(encoding="utf-8").replace('location: "Global"', f'location: "{UNPUBLISHED_LOCATION[lang]}"')
    projects.write_text(text, encoding="utf-8", newline="\n")

    products = ROOT / lang / "products.html"
    text = products.read_text(encoding="utf-8")
    text = re.sub(r'\s*<!-- RFQ INQUIRY MODAL -->.*?(?=\s*<!-- FOOTER -->)', '', text, count=1, flags=re.DOTALL)
    text, count = re.subn(
        r'    function openRfqModal\(.*?(?=    function initMatcherEvents\(\))',
        "    function inquire(name, sku, quantity = 1) {\n      window.location.href = `contact.html?product=${encodeURIComponent(sku)}`;\n    }\n\n",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1 and "window.location.href = `contact.html?product=${encodeURIComponent(sku)}`" not in text:
        raise RuntimeError(f"Legacy RFQ function block not found: {products}")
    products.write_text(text, encoding="utf-8", newline="\n")

for page in (ROOT / "tw").glob("*.html"):
    text = page.read_text(encoding="utf-8").replace("全球實績", "專案案例")
    page.write_text(text, encoding="utf-8", newline="\n")
