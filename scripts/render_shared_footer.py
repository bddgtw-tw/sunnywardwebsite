"""Render the shared multilingual public footer."""

from __future__ import annotations

import html


COPY = {
    "en": {"home":"Home","about":"About","products":"Products","projects":"Projects","contact":"Contact","navigation":"Navigation","sales":"Project enquiries","offices":"Offices","malaysia":"Malaysia operations","singapore":"Singapore regional office","statement":"Commercial furniture sourcing, customisation and project coordination across Southeast Asia.","rights":"All rights reserved."},
    "tw": {"home":"首頁","about":"關於 Sunnyward","products":"產品","projects":"案例","contact":"聯絡我們","navigation":"網站導覽","sales":"專案洽詢","offices":"區域據點","malaysia":"馬來西亞營運據點","singapore":"新加坡區域辦公室","statement":"為東南亞商業空間提供家具選品、客製開發與專案協調。","rights":"版權所有。"},
    "jp": {"home":"ホーム","about":"Sunnywardについて","products":"製品","projects":"導入事例","contact":"お問い合わせ","navigation":"サイト案内","sales":"プロジェクトのご相談","offices":"地域拠点","malaysia":"マレーシア運営拠点","singapore":"シンガポール地域オフィス","statement":"東南アジアの商業空間に向けた家具調達、カスタマイズ、プロジェクト調整。","rights":"無断転載を禁じます。"},
}


def render_public_footer(lang: str, prefix: str = "../") -> str:
    ui = COPY[lang]
    nav = "".join(
        f'<li><a href="{prefix}{path}">{html.escape(ui[key])}</a></li>'
        for key, path in (("home","index.html"),("about","about.html"),("products","products.html"),("projects","projects.html"),("contact","contact.html"))
    )
    return f'''<footer class="detail-footer">
  <div class="container">
    <div class="footer-top footer-grid">
      <div class="footer-brand footer-col"><a href="{prefix}index.html" class="logo">SUNNYWARD<span>.</span></a><p>{html.escape(ui['statement'])}</p></div>
      <div class="footer-col"><h2 class="footer-col__title">{html.escape(ui['navigation'])}</h2><ul class="footer-links">{nav}</ul></div>
      <div class="footer-col"><h2 class="footer-col__title">{html.escape(ui['sales'])}</h2><ul class="footer-links"><li><a href="mailto:sales@sunnyward.com">sales@sunnyward.com</a></li><li><a href="https://wa.me/60165262894" target="_blank" rel="noopener">WhatsApp +60 16-526 2894</a> &amp; <a href="https://wa.me/60167252894" target="_blank" rel="noopener">+60 16-725 2894</a></li><li><a href="tel:+60165262894">+60 16-526 2894</a> / <a href="tel:+60167252894">+60 16-725 2894</a></li></ul></div>
      <div class="footer-col footer-address"><h2 class="footer-col__title">{html.escape(ui['offices'])}</h2><address><strong>{html.escape(ui['malaysia'])}</strong><br>27, Jalan Impian Emas 18, Taman Perusahaan Ringan Pulai, 81300 Johor Bahru, Johor<br><br><strong>{html.escape(ui['singapore'])}</strong><br>101 Upper Cross Street, #B1-71, People's Park Centre, Singapore 058387</address></div>
    </div>
    <div class="footer-bottom"><p>© 2026 SUNNYWARD PTE LTD. {html.escape(ui['rights'])}</p><p><a href="mailto:sales@sunnyward.com">sales@sunnyward.com</a></p></div>
  </div>
</footer>'''
