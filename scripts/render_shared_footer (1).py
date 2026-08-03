"""Render the evidence-bounded footer used by public detail pages."""

from __future__ import annotations

import html


COPY = {
    "en": {"home":"Home","products":"Products","projects":"Projects","contact":"Contact","navigation":"Navigation","sales":"Project enquiries","offices":"Offices","malaysia":"Malaysia operations","singapore":"Singapore office","statement":"Commercial furniture sourcing and project coordination, with public product and project information released only after source review.","rights":"All rights reserved."},
    "tw": {"home":"首頁","products":"產品型錄","projects":"專案案例","contact":"聯絡我們","navigation":"網站導覽","sales":"專案詢價","offices":"辦公地點","malaysia":"馬來西亞營運據點","singapore":"新加坡辦公室","statement":"提供商用家具選品與專案協調；產品及案例資料經來源審核後才公開。","rights":"版權所有。"},
    "jp": {"home":"ホーム","products":"製品情報","projects":"導入事例","contact":"お問い合わせ","navigation":"ナビゲーション","sales":"プロジェクトお問い合わせ","offices":"オフィス","malaysia":"マレーシア事業拠点","singapore":"シンガポールオフィス","statement":"業務用家具の選定とプロジェクト調整を行い、製品・導入情報は情報源の確認後に公開しています。","rights":"無断転載を禁じます。"},
}


def render_public_footer(lang: str, prefix: str = "../") -> str:
    ui = COPY[lang]
    nav = "".join(
        f'<li><a href="{prefix}{path}">{html.escape(ui[key])}</a></li>'
        for key, path in (("home","index.html"),("products","products.html"),("projects","projects.html"),("contact","contact.html"))
    )
    return f'''<footer class="detail-footer">
  <div class="container">
    <div class="footer-top footer-grid">
      <div class="footer-brand footer-col"><a href="{prefix}index.html" class="logo">SUNNYWARD<span>.</span></a><p>{html.escape(ui['statement'])}</p></div>
      <div class="footer-col"><h2 class="footer-col__title">{html.escape(ui['navigation'])}</h2><ul class="footer-links">{nav}</ul></div>
      <div class="footer-col"><h2 class="footer-col__title">{html.escape(ui['sales'])}</h2><ul class="footer-links"><li><a href="mailto:sales@sunnyward.com">sales@sunnyward.com</a></li><li><a href="https://wa.me/60165262894" target="_blank" rel="noopener">WhatsApp +60 16-526 2894</a></li><li><a href="tel:+60165262894">+60 16-526 2894</a></li></ul></div>
      <div class="footer-col footer-address"><h2 class="footer-col__title">{html.escape(ui['offices'])}</h2><address><strong>{html.escape(ui['malaysia'])}</strong><br>27, Jalan Impian Emas 18, Taman Perusahaan Ringan Pulai, 81300 Johor Bahru, Johor<br><br><strong>{html.escape(ui['singapore'])}</strong><br>101 Upper Cross Street, #B1-71, People's Park Centre, Singapore 058387</address></div>
    </div>
    <div class="footer-bottom"><p>© 2026 SUNNYWARD PTE LTD. {html.escape(ui['rights'])}</p><p><a href="mailto:sales@sunnyward.com">sales@sunnyward.com</a></p></div>
  </div>
</footer>'''
