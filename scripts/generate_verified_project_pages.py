from __future__ import annotations

import html
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from build_search_sitemap import build_sitemap
from render_shared_footer import render_public_footer
from organization_schema import ORGANIZATION_ID, organization_schema
from site_config import public_url


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "verified_project_pages.json"
PRODUCT_SOURCE = ROOT / "data" / "verified_product_pages.json"
LANGS = {
    "en": {"html_lang":"en","home":"Home","projects":"Projects","products":"Products","contact":"Contact","record":"Verified project media record","space":"Space type","date":"Archive date","evidence":"Available evidence","evidence_text":"Installation video and four site images","standard":"Publication standard","standard_text":"Exact product models, quantities, contractual scope, client quotations and measured outcomes remain unpublished until supporting documents are verified.","planning":"Products for planning a similar space","planning_note":"These verified products suit a similar space type. They are planning references only and are not presented as the products installed in this project.","planning_empty_note":"No verified product has been matched to this space type yet. The current verified catalogue remains available for broader project exploration.","browse":"Browse the verified product catalogue","view_product":"View verified product","inquire":"Discuss a similar project","back":"Back to all projects","video":"Project installation video","gallery":"Installation image"},
    "tw": {"html_lang":"zh-TW","home":"首頁","projects":"專案案例","products":"產品系列","contact":"聯絡我們","record":"已核對的專案媒體紀錄","space":"空間類型","date":"媒體存檔日期","evidence":"現有佐證","evidence_text":"安裝影片與四張現場圖片","standard":"發布標準","standard_text":"確切產品型號、數量、合約範圍、客戶引言與量化成效，須待相關文件核實後才會發布。","planning":"相似空間的產品規劃參考","planning_note":"下列已核對產品適合相近的空間類型，僅供規劃參考；不代表本案例現場實際使用這些產品。","planning_empty_note":"目前尚未有已核對產品與此空間類型完成精準匹配；仍可從現有已核對型錄探索其他專案方向。","browse":"瀏覽已核對產品型錄","view_product":"查看已核對產品","inquire":"洽談類似專案","back":"返回所有案例","video":"專案家具安裝影片","gallery":"家具安裝現場圖片"},
    "jp": {"html_lang":"ja","home":"ホーム","projects":"導入事例","products":"製品情報","contact":"お問い合わせ","record":"確認済みプロジェクトメディア記録","space":"空間タイプ","date":"メディア保存日","evidence":"確認可能な資料","evidence_text":"導入映像と現場写真4点","standard":"公開基準","standard_text":"製品品番、数量、契約範囲、顧客コメント、定量的成果は、根拠資料の確認後にのみ公開します。","planning":"類似空間の製品計画参考","planning_note":"以下の確認済み製品は、同様の空間タイプを計画する際の参考です。本事例で実際に採用された製品を示すものではありません。","planning_empty_note":"現時点では、この空間タイプに適合する確認済み製品を特定していません。現在の確認済みカタログから、ほかの計画候補をご覧いただけます。","browse":"確認済み製品カタログを見る","view_product":"確認済み製品を見る","inquire":"類似プロジェクトを相談する","back":"導入事例一覧へ戻る","video":"家具導入プロジェクト映像","gallery":"家具導入現場写真"},
}
LANGUAGE_LABELS = {"en": ("EN", "English"), "tw": ("繁中", "繁中"), "jp": ("日本語", "日本語")}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def language_navigation(lang: str, path: str) -> tuple[str, str]:
    current = LANGUAGE_LABELS[lang][0]
    links = "".join(
        f'<li class="lang-item"><a href="../../{folder}/{path}" class="lang-dropdown-item{" active" if folder == lang else ""}" data-lang="{folder}" lang="{LANGS[folder]["html_lang"]}">{label}</a></li>'
        for folder, (_, label) in LANGUAGE_LABELS.items()
    )
    mobile_links = "".join(
        f'<a href="../../{folder}/{path}" class="{"active" if folder == lang else ""}" data-lang="{folder}" lang="{LANGS[folder]["html_lang"]}">{label}</a>'
        for folder, (_, label) in LANGUAGE_LABELS.items()
    )
    desktop = f'<div class="nav-actions"><div class="lang-dropdown"><button type="button" class="lang-current" aria-label="Select language">{current} ▾</button><ul class="lang-list">{links}</ul></div></div>'
    mobile = f'<div class="mobile-language-switch" aria-label="Language"><span>Language</span><div>{mobile_links}</div></div>'
    return desktop, mobile


def render(project: dict, lang: str, products: list[dict]) -> str:
    ui, loc = LANGS[lang], project["locales"][lang]
    slug = project["slug"]
    language_desktop, language_mobile = language_navigation(lang, f"projects/{slug}.html")
    footer = render_public_footer(lang)
    canonical = public_url(f"{lang}/projects/{slug}.html")
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{code}" href="{public_url(f"{folder}/projects/{slug}.html")}">'
        for code, folder in (("x-default","en"),("en","en"),("zh-TW","tw"),("ja","jp"))
    )
    gallery = "\n".join(
        f'<figure><img src="../../{esc(path)}" alt="{esc(loc["name"])} — {ui["gallery"]} {i}" '
        f'width="{dimensions[0]}" height="{dimensions[1]}" loading="lazy" decoding="async"></figure>'
        for i, (path, dimensions) in enumerate(
            zip(project["images"], project["image_dimensions"], strict=True), 1
        )
    )
    related_products = [product for product in products if product.get("planning_reference") == slug]
    if related_products:
        cards = "\n".join(
            f'''<article class="project-product-card"><a href="../products/{esc(product['slug'])}.html"><img src="../../{esc(product['images'][0])}" alt="{esc(product['locales'][lang]['name'])}" width="{product['image_dimensions'][0][0]}" height="{product['image_dimensions'][0][1]}" loading="lazy" decoding="async"></a><div><p class="project-product-sku">{esc(product['sku'])}</p><h3><a href="../products/{esc(product['slug'])}.html">{esc(product['locales'][lang]['name'])}</a></h3><p>{esc(product['dimensions']['raw'])}</p><a class="project-product-link" href="../products/{esc(product['slug'])}.html">{ui['view_product']} →</a></div></article>'''
            for product in related_products
        )
    else:
        cards = f'<p><a class="project-product-link" href="../products.html">{ui["browse"]} →</a></p>'
    planning_note = ui["planning_note"] if related_products else ui["planning_empty_note"]
    planning = f'''<section class="project-product-planning" aria-labelledby="planning-products"><div class="project-product-intro"><h2 id="planning-products">{ui['planning']}</h2><p>{planning_note}</p></div><div class="project-product-grid">{cards}</div></section>'''
    organization = organization_schema()
    creative_work = {
        "@context":"https://schema.org", "@type":"CreativeWork", "name":loc["name"],
        "description":loc["description"], "dateCreated":project["date"], "url":canonical,
        "image":[public_url(p) for p in project["images"]],
        "video":{"@type":"VideoObject","name":loc["name"],"description":loc["description"],"contentUrl":public_url(project['video']),"uploadDate":f"{project['date']}-01"},
        "publisher":{"@id":ORGANIZATION_ID}
    }
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":ui["home"],"item":public_url(f"{lang}/")},
        {"@type":"ListItem","position":2,"name":ui["projects"],"item":public_url(f"{lang}/projects.html")},
        {"@type":"ListItem","position":3,"name":loc["name"],"item":canonical}]}
    return f'''<!DOCTYPE html>
<html lang="{ui['html_lang']}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(loc['name'])} | Sunnyward</title>
  <meta name="description" content="{esc(loc['description'])}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1,max-snippet:-1">
  <link rel="canonical" href="{canonical}">
{alternates}
  <meta property="og:type" content="article"><meta property="og:title" content="{esc(loc['name'])} | Sunnyward">
  <meta property="og:description" content="{esc(loc['description'])}"><meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{public_url(esc(project['images'][0]))}">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(loc['name'])} | Sunnyward">
  <meta name="twitter:description" content="{esc(loc['description'])}"><meta name="twitter:image" content="{public_url(esc(project['images'][0]))}">
  <link rel="stylesheet" href="../../css/style.css?v=20260715-b2b-paths">
  <script type="application/ld+json">{json.dumps(organization, ensure_ascii=False, separators=(',', ':'))}</script>
  <script type="application/ld+json">{json.dumps(creative_work, ensure_ascii=False, separators=(',', ':'))}</script>
  <script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False, separators=(',', ':'))}</script>
</head>
<body>
  <header id="site-header"><div class="nav-container"><a href="../index.html" class="logo">SUNNYWARD<span>.</span></a><button class="mobile-nav-toggle" id="mobile-toggle" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button><ul class="nav-menu"><li><a href="../index.html" class="nav-link">{ui['home']}</a></li><li><a href="../products.html" class="nav-link">{ui['products']}</a></li><li><a href="../projects.html" class="nav-link active">{ui['projects']}</a></li><li><a href="../contact.html" class="nav-link">{ui['contact']}</a></li></ul>{language_desktop}</div></header>
  <nav class="mobile-drawer" id="mobile-drawer"><a href="../index.html" class="nav-link">{ui['home']}</a><a href="../products.html" class="nav-link">{ui['products']}</a><a href="../projects.html" class="nav-link active">{ui['projects']}</a><a href="../contact.html" class="nav-link">{ui['contact']}</a>{language_mobile}</nav>
  <main class="verified-project-page"><div class="container">
    <nav class="product-breadcrumb" aria-label="Breadcrumb"><a href="../index.html">{ui['home']}</a><span>/</span><a href="../projects.html">{ui['projects']}</a><span>/</span><span>{esc(loc['name'])}</span></nav>
    <header class="verified-project-header"><span class="eyebrow">{ui['record']}</span><h1>{esc(loc['name'])}</h1><p>{esc(loc['intro'])}</p></header>
    <section class="verified-project-media"><video controls playsinline preload="none" poster="../../{esc(project['images'][0])}" aria-label="{esc(ui['video'])}"><source src="../../{esc(project['video'])}" type="video/mp4">{ui['video']}</video></section>
    <section class="verified-project-facts"><div><h2>{ui['space']}</h2><p>{esc(loc['space'])}</p></div><div><h2>{ui['date']}</h2><p>{esc(project['date'])}</p></div><div><h2>{ui['evidence']}</h2><p>{ui['evidence_text']}</p></div></section>
    <aside class="verified-project-standard"><h2>{ui['standard']}</h2><p>{ui['standard_text']}</p></aside>
    {planning}
    <div class="verified-project-actions"><a class="btn btn-primary" href="../contact.html?project={esc(slug)}">{ui['inquire']}</a><a href="../projects.html">← {ui['back']}</a></div>
  </div></main>{footer}<script src="../../js/main.js?v=20260715-b2b-paths"></script>
</body></html>'''


def add_list_link(page: Path, project: dict, lang: str) -> None:
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    section = soup.find("section", id=project["id"])
    if section is None or "ultimate-case-section" not in section.get("class", []):
        raise RuntimeError(f"Missing {project['id']} in {page}")
    for old in section.select("a.project-detail-link"):
        old.decompose()
    target = section.select_one(".uc-narrative")
    if target is None:
        raise RuntimeError(f"Missing narrative for {project['id']} in {page}")
    link = soup.new_tag("a", href=f'projects/{project["slug"]}.html')
    link["class"] = ["project-detail-link"]
    link.string = f'{LANGS[lang]["record"]} →'
    target.append(link)
    page.write_text(str(soup), encoding="utf-8", newline="\n")


def main() -> None:
    projects = json.loads(SOURCE.read_text(encoding="utf-8"))["projects"]
    products = json.loads(PRODUCT_SOURCE.read_text(encoding="utf-8"))["products"]
    for lang in LANGS:
        out = ROOT / lang / "projects"
        out.mkdir(exist_ok=True)
        for project in projects:
            (out / f'{project["slug"]}.html').write_text(render(project, lang, products), encoding="utf-8", newline="\n")
            add_list_link(ROOT / lang / "projects.html", project, lang)
    build_sitemap()
    print(f"Generated {len(projects) * len(LANGS)} verified project pages.")


if __name__ == "__main__":
    main()
