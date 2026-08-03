from __future__ import annotations

import html
import json
from pathlib import Path
from build_search_sitemap import build_sitemap
from render_shared_footer import render_public_footer
from organization_schema import organization_schema
from site_config import public_url


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "verified_product_pages.json"
PROJECT_SOURCE = ROOT / "data" / "verified_project_pages.json"
PROJECTS = {
    project["slug"]: project
    for project in json.loads(PROJECT_SOURCE.read_text(encoding="utf-8"))["projects"]
}
LANGS = {
    "en": {"html_lang": "en", "home": "Home", "products": "Products", "projects": "Projects", "contact": "Contact", "details": "Verified product details", "applications": "Suggested applications", "materials": "Materials", "dimensions": "Dimensions", "origin": "Origin", "packaging": "Packaging", "inquire": "Request project quotation", "back": "Back to product catalogue", "sku": "SKU"},
    "tw": {"html_lang": "zh-TW", "home": "首頁", "products": "產品型錄", "projects": "工程案例", "contact": "聯絡我們", "details": "已核對產品資料", "applications": "建議應用空間", "materials": "材質", "dimensions": "尺寸", "origin": "產地", "packaging": "包裝", "inquire": "洽詢專案報價", "back": "返回產品型錄", "sku": "型號"},
    "jp": {"html_lang": "ja", "home": "ホーム", "products": "カタログ", "projects": "導入事例", "contact": "お問い合わせ", "details": "確認済み製品情報", "applications": "想定用途", "materials": "素材", "dimensions": "寸法", "origin": "原産国", "packaging": "梱包", "inquire": "プロジェクト見積もりを依頼", "back": "製品カタログへ戻る", "sku": "品番"},
}
BUYER_GUIDANCE = {
    "en": {
        "before": "Confirm before specification",
        "before_intro": "These commercial conditions are not claimed as verified public facts. Confirm them for the exact order and destination before specification.",
        "checks": ["Current availability, minimum order and project lead time", "Finish, mesh, rope or cushion colour and replacement options", "Outdoor exposure, care and maintenance requirements for the site", "Required testing, certification, warranty and spare-parts support", "Delivery access, assembly and installation responsibilities"],
        "brief": "Prepare a useful quote brief",
        "brief_intro": "Include these details so Sunnyward can qualify the request instead of returning a generic price.",
        "brief_items": ["Product SKU and required quantity", "Company, project type and delivery country or city", "Target delivery or opening date", "Requested finish, cushion or material options", "Site access, installation and documentation requirements"],
        "evidence": "Publication basis",
        "evidence_text": "The dimensions, listed materials, origin and images on this pilot page were cross-checked against Sunnyward's internal source records. Pricing, packaging, freight and unverified commercial conditions are intentionally omitted.",
        "reference": "Related space-planning reference",
        "reference_note": "This case is linked for space and application context only. The archived media does not verify that this exact SKU was installed.",
        "view_reference": "View media-backed project record",
    },
    "tw": {
        "before": "納入規格前請確認",
        "before_intro": "以下商業條件目前不是已公開核實的產品事實，應依實際訂單與交貨地點，在納入規格或下單前確認。",
        "checks": ["目前供應狀況、最低訂購量與專案交期", "表面處理、網布、編織繩或坐墊顏色及替換選項", "依現場曝曬條件確認保養與維護需求", "專案要求的測試、認證、保固與備品支援", "交貨動線、組裝方式與安裝責任"],
        "brief": "準備有效的報價需求",
        "brief_intro": "提供以下資訊，Sunnyward 才能判斷專案條件，而不只是回覆缺乏前提的單一價格。",
        "brief_items": ["產品型號與需求數量", "公司、專案類型及交貨國家或城市", "預計交貨日或開幕日", "指定表面、坐墊或材質選項", "現場進場、安裝及文件需求"],
        "evidence": "資料公開依據",
        "evidence_text": "本試行頁面的尺寸、所列材質、產地、包裝與圖片，已與 Sunnyward 結構化型錄紀錄及對應本機產品檔交叉核對。價格與尚未核實的商業條件刻意不公開。",
        "reference": "相關空間規劃參考",
        "reference_note": "此案例僅供空間及應用情境參考；現有媒體資料無法證明案例中安裝的是本頁同一型號。",
        "view_reference": "查看具媒體佐證的案例紀錄",
    },
    "jp": {
        "before": "仕様決定前の確認事項",
        "before_intro": "以下の取引条件は、公開情報として確認済みの製品事実ではありません。実際の注文内容と納入先に合わせ、仕様決定前にご確認ください。",
        "checks": ["在庫・供給状況、最低発注数量、プロジェクト納期", "仕上げ、メッシュ、ロープ、クッション色と交換オプション", "設置環境に応じた屋外使用条件、手入れ、メンテナンス", "必要な試験、認証、保証、スペアパーツ対応", "搬入経路、組立方法、設置作業の責任範囲"],
        "brief": "見積依頼に必要な情報",
        "brief_intro": "条件のない単価回答ではなく、案件を適切に確認できるよう、以下の情報をお知らせください。",
        "brief_items": ["製品品番と必要数量", "会社名、案件種別、納入国または都市", "希望納期または開業予定日", "希望する仕上げ、クッション、素材オプション", "搬入、設置、提出書類の要件"],
        "evidence": "公開情報の根拠",
        "evidence_text": "本パイロットページの寸法、記載素材、原産国、梱包、画像は、Sunnyward の構造化カタログ記録と対応するローカル製品ファイルを照合しています。価格および未確認の取引条件は意図的に掲載していません。",
        "reference": "関連する空間計画の参考事例",
        "reference_note": "この事例は空間と用途の参考としてのみ掲載しています。保管映像から、本ページと同一品番の採用を確認することはできません。",
        "view_reference": "メディアで確認できる導入記録を見る",
    },
}
LANGUAGE_LABELS = {"en": ("EN", "English"), "tw": ("繁中", "繁中"), "jp": ("日本語", "日本語")}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def material_label(material: str, lang: str) -> str:
    translations = {
        "tw": {"Anthracite aluminum": "碳灰色鋁合金", "Batyline mesh": "Batyline 網布", "Acrylic rope": "壓克力編織繩", "Granite or greige seat cushion": "Granite 或 Greige 坐墊", "Dark grey seat and back cushions": "深灰色坐墊與靠墊"},
        "jp": {"Anthracite aluminum": "アンスラサイト色アルミ", "Batyline mesh": "Batylineメッシュ", "Acrylic rope": "アクリルロープ", "Granite or greige seat cushion": "グラナイトまたはグレージュの座面クッション", "Dark grey seat and back cushions": "ダークグレーの座面・背面クッション"},
    }
    return translations.get(lang, {}).get(material, material)


def product_image(path: str, dimensions: list[int], index: int, name: str) -> str:
    loading = "eager" if index == 1 else "lazy"
    priority = ' fetchpriority="high"' if index == 1 else ""
    return (
        f'<figure><img src="../../{esc(path)}" alt="{esc(name)} — {index}" '
        f'width="{dimensions[0]}" height="{dimensions[1]}" loading="{loading}"'
        f'{priority} decoding="async"></figure>'
    )


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


def render(product: dict, lang: str) -> str:
    ui = LANGS[lang]
    guide = BUYER_GUIDANCE[lang]
    loc = product["locales"][lang]
    reference = PROJECTS[product["planning_reference"]]
    reference_loc = reference["locales"][lang]
    slug = product["slug"]
    language_desktop, language_mobile = language_navigation(lang, f"products/{slug}.html")
    footer = render_public_footer(lang)
    canonical = public_url(f"{lang}/products/{slug}.html")
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{code}" href="{public_url(f"{folder}/products/{slug}.html")}">'
        for code, folder in (("x-default", "en"), ("en", "en"), ("zh-TW", "tw"), ("ja", "jp"))
    )
    images = "\n".join(
        product_image(path, dimensions, index, loc["name"])
        for index, (path, dimensions) in enumerate(
            zip(product["images"], product["image_dimensions"], strict=True), 1
        )
    )
    materials = "".join(f"<li>{esc(material_label(item, lang))}</li>" for item in product["materials"])
    applications = "".join(f"<li>{esc(item)}</li>" for item in loc["applications"])
    specification_checks = "".join(f"<li>{esc(item)}</li>" for item in guide["checks"])
    quote_brief = "".join(f"<li>{esc(item)}</li>" for item in guide["brief_items"])
    organization = organization_schema()
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": loc["name"],
        "sku": product["sku"],
        "description": loc["description"],
        "brand": {"@type": "Brand", "name": product["brand"]},
        "category": product["category"],
        "material": [material_label(item, lang) for item in product["materials"]],
        "countryOfOrigin": {"@type": "Country", "name": product["origin"]},
        "additionalProperty": [
            {"@type": "PropertyValue", "name": ui["dimensions"], "value": product["dimensions"]["raw"]},
        ],
        "image": [public_url(path) for path in product["images"]],
        "url": canonical,
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["home"], "item": public_url(f"{lang}/")},
            {"@type": "ListItem", "position": 2, "name": ui["products"], "item": public_url(f"{lang}/products.html")},
            {"@type": "ListItem", "position": 3, "name": loc["name"], "item": canonical},
        ],
    }
    return f'''<!DOCTYPE html>
<html lang="{ui['html_lang']}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(loc['title'])}</title>
  <meta name="description" content="{esc(loc['description'])}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
  <link rel="canonical" href="{canonical}">
{alternates}
  <meta property="og:type" content="product">
  <meta property="og:title" content="{esc(loc['title'])}">
  <meta property="og:description" content="{esc(loc['description'])}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{public_url(esc(product['images'][0]))}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(loc['title'])}">
  <meta name="twitter:description" content="{esc(loc['description'])}">
  <meta name="twitter:image" content="{public_url(esc(product['images'][0]))}">
  <link rel="stylesheet" href="../../css/style.css?v=20260715-b2b-paths">
  <script type="application/ld+json">{json.dumps(organization, ensure_ascii=False, separators=(',', ':'))}</script>
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script>
  <script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False, separators=(',', ':'))}</script>
</head>
<body>
  <header id="site-header">
    <div class="nav-container">
      <a href="../index.html" class="logo">SUNNYWARD<span>.</span></a>
      <button class="mobile-nav-toggle" id="mobile-toggle" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button>
      <ul class="nav-menu">
        <li><a href="../index.html" class="nav-link">{ui['home']}</a></li>
        <li><a href="../products.html" class="nav-link active">{ui['products']}</a></li>
        <li><a href="../projects.html" class="nav-link">{ui['projects']}</a></li>
        <li><a href="../contact.html" class="nav-link">{ui['contact']}</a></li>
      </ul>
      {language_desktop}
    </div>
  </header>
  <nav class="mobile-drawer" id="mobile-drawer"><a href="../index.html" class="nav-link">{ui['home']}</a><a href="../products.html" class="nav-link active">{ui['products']}</a><a href="../projects.html" class="nav-link">{ui['projects']}</a><a href="../contact.html" class="nav-link">{ui['contact']}</a>{language_mobile}</nav>
  <main class="verified-product-page">
    <div class="container">
      <nav class="product-breadcrumb" aria-label="Breadcrumb"><a href="../index.html">{ui['home']}</a><span>/</span><a href="../products.html">{ui['products']}</a><span>/</span><span>{esc(loc['name'])}</span></nav>
      <section class="verified-product-hero">
        <div class="verified-product-gallery">{images}</div>
        <div class="verified-product-summary">
          <span class="eyebrow">{esc(product['collection'])}</span>
          <h1>{esc(loc['name'])}</h1>
          <p class="verified-product-sku">{ui['sku']}: {esc(product['sku'])}</p>
          <p class="verified-product-intro">{esc(loc['intro'])}</p>
          <a class="btn btn-primary" href="../contact.html?product={esc(product['sku'])}">{ui['inquire']}</a>
        </div>
      </section>
      <section class="verified-product-details">
        <div><span class="eyebrow">{ui['details']}</span><dl><dt>{ui['dimensions']}</dt><dd>{esc(product['dimensions']['raw'])}</dd><dt>{ui['origin']}</dt><dd>{esc(product['origin'])}</dd></dl></div>
        <div><h2>{ui['materials']}</h2><ul>{materials}</ul></div>
        <div><h2>{ui['applications']}</h2><ul>{applications}</ul></div>
      </section>
      <section class="verified-product-procurement" aria-labelledby="procurement-title">
        <div class="verified-product-procurement__intro">
          <h2 id="procurement-title">{esc(guide['evidence'])}</h2>
          <p>{esc(guide['evidence_text'])}</p>
        </div>
        <div class="verified-product-guidance-grid">
          <article><h2>{esc(guide['before'])}</h2><p>{esc(guide['before_intro'])}</p><ul>{specification_checks}</ul></article>
          <article><h2>{esc(guide['brief'])}</h2><p>{esc(guide['brief_intro'])}</p><ul>{quote_brief}</ul><a class="btn btn-primary" href="../contact.html?product={esc(product['sku'])}">{ui['inquire']}</a></article>
        </div>
      </section>
      <aside class="verified-product-reference">
        <div><span class="eyebrow">{esc(guide['reference'])}</span><h2>{esc(reference_loc['name'])}</h2><p>{esc(guide['reference_note'])}</p></div>
        <a class="verified-product-reference__link" href="../projects/{esc(reference['slug'])}.html">{esc(guide['view_reference'])} →</a>
      </aside>
      <a class="verified-product-back" href="../products.html">← {ui['back']}</a>
    </div>
  </main>
  {footer}
  <script src="../../js/main.js?v=20260715-b2b-paths"></script>
</body>
</html>
'''


def sync_catalog_record(product: dict, lang: str, catalog: dict) -> None:
    record = next((item for item in catalog["products"] if item.get("sku") == product["sku"]), None)
    if not record:
        raise RuntimeError(f"Missing {product['sku']} in {lang}/products.json")
    loc = product["locales"][lang]
    record["name"] = loc["name"]
    record["description"] = loc["intro"]
    record["dimensions"] = product["dimensions"]
    record["materials"] = [material_label(item, lang) for item in product["materials"]]
    record["image_dimensions"] = product["image_dimensions"]
    record["detail_page"] = f"products/{product['slug']}.html"


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    products = source["products"]
    for lang in LANGS:
        catalog_path = ROOT / lang / "products.json"
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        output_dir = ROOT / lang / "products"
        output_dir.mkdir(exist_ok=True)
        for product in products:
            sync_catalog_record(product, lang, catalog)
            (output_dir / f"{product['slug']}.html").write_text(render(product, lang), encoding="utf-8", newline="\n")
        catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    build_sitemap()
    print(f"Generated {len(products) * len(LANGS)} product pages and synchronized three catalog files.")


if __name__ == "__main__":
    main()
