from __future__ import annotations

import html
import json
import re
from pathlib import Path
from site_config import public_url


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = json.loads((ROOT / "data" / "verified_product_pages.json").read_text(encoding="utf-8"))["products"]
PROJECTS = json.loads((ROOT / "data" / "verified_project_pages.json").read_text(encoding="utf-8"))["projects"]
LANGS = {
    "en":{"schema_lang":"en","og_locale":"en_US","products":"Verified commercial outdoor furniture","projects":"Verified furniture installation records","contact":"Commercial furniture project enquiries"},
    "tw":{"schema_lang":"zh-TW","og_locale":"zh_TW","products":"已核對商用戶外家具","projects":"已核對家具安裝紀錄","contact":"商用家具專案詢價"},
    "jp":{"schema_lang":"ja","og_locale":"ja_JP","products":"確認済み業務用アウトドア家具","projects":"確認済み家具導入記録","contact":"業務用家具プロジェクトお問い合わせ"},
}
META_COPY = {
    "en": {
        "index":("Sunnyward | Commercial Furniture Sourcing & Project Records","Commercial furniture sourcing, verified product information and media-backed installation records for architects, designers and hospitality project buyers."),
        "products":("Verified Commercial Outdoor Furniture | Sunnyward","Explore Sunnyward's pilot catalogue of three commercial outdoor furniture products with cross-checked dimensions, materials, images and enquiry links."),
        "projects":("Furniture Installation Project Records | Sunnyward","Review media-backed restaurant, cafeteria and poolside furniture installation records with archived video and site images."),
        "contact":("Commercial Furniture Project Enquiry | Sunnyward","Prepare a commercial furniture enquiry with company, delivery market and project requirements, then continue by Email or WhatsApp."),
    },
    "tw": {
        "index":("Sunnyward｜商用家具選品與專案紀錄","為設計師、建築師及旅宿餐飲採購提供商用家具選品、已核對產品資訊與具媒體佐證的安裝紀錄。"),
        "products":("已核對商用戶外家具｜Sunnyward","瀏覽 Sunnyward 首批三項商用戶外家具；尺寸、材質、圖片與詢價入口均已依現有來源交叉核對。"),
        "projects":("家具安裝專案紀錄｜Sunnyward","查看具影片與現場圖片佐證的餐廳、餐飲空間及池畔家具安裝紀錄。"),
        "contact":("商用家具專案詢價｜Sunnyward","填寫公司、交貨市場與專案需求，準備商用家具詢價草稿，再透過 Email 或 WhatsApp 確認傳送。"),
    },
    "jp": {
        "index":("Sunnyward｜業務用家具選定・プロジェクト記録","デザイナー、建築家、ホスピタリティ購買担当者向けに、業務用家具選定、確認済み製品情報、導入記録を提供します。"),
        "products":("確認済み業務用アウトドア家具｜Sunnyward","寸法、素材、画像、問い合わせ先を現行資料と照合した、3製品のパイロットカタログです。"),
        "projects":("家具導入プロジェクト記録｜Sunnyward","映像と現場写真で確認できる、レストラン、カフェテリア、プールサイドの家具導入記録です。"),
        "contact":("業務用家具プロジェクトお問い合わせ｜Sunnyward","会社名、納品市場、案件要件を入力し、Email または WhatsApp で送信するお問い合わせ下書きを作成できます。"),
    },
}


def extract(text: str, pattern: str, path: Path) -> str:
    match = re.search(pattern, text, re.S | re.I)
    if not match:
        raise RuntimeError(f"Missing metadata in {path}: {pattern}")
    return html.unescape(match.group(1).strip())


def schema_for(kind: str, lang: str, canonical: str, title: str, description: str) -> list[dict]:
    language = LANGS[lang]["schema_lang"]
    org_id = public_url("#organization")
    if kind == "index":
        return [{"@context":"https://schema.org","@type":"WebSite","@id":public_url("#website"),"url":public_url(),"name":"Sunnyward","publisher":{"@id":org_id},"inLanguage":["en","zh-TW","ja"]}]
    if kind == "products":
        items = [{"@type":"ListItem","position":i,"name":p["locales"][lang]["name"],"url":public_url(f"{lang}/products/{p['slug']}.html")} for i,p in enumerate(PRODUCTS,1)]
        return [{"@context":"https://schema.org","@type":"CollectionPage","name":title,"description":description,"url":canonical,"inLanguage":language,"about":{"@id":org_id},"mainEntity":{"@type":"ItemList","numberOfItems":len(items),"itemListElement":items}}]
    if kind == "projects":
        items = [{"@type":"ListItem","position":i,"name":p["locales"][lang]["name"],"url":public_url(f"{lang}/projects/{p['slug']}.html")} for i,p in enumerate(PROJECTS,1)]
        return [{"@context":"https://schema.org","@type":"CollectionPage","name":title,"description":description,"url":canonical,"inLanguage":language,"about":{"@id":org_id},"mainEntity":{"@type":"ItemList","numberOfItems":len(items),"itemListElement":items}}]
    return [{"@context":"https://schema.org","@type":"ContactPage","name":title,"description":description,"url":canonical,"inLanguage":language,"mainEntity":{"@type":"Organization","@id":org_id,"name":"Sunnyward","email":"sales@sunnyward.com","telephone":"+6016-526-2894","contactPoint":[{"@type":"ContactPoint","contactType":"sales","email":"sales@sunnyward.com","telephone":"+6016-526-2894","availableLanguage":["en","zh-TW","ja"]},{"@type":"ContactPoint","contactType":"sales support","email":"sales@sunnyward.com","telephone":"+6016-725-2894","availableLanguage":["en","zh-TW","ja"]}]}}]


def enhance(path: Path, lang: str, kind: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'\s*<!-- search-semantics:start -->.*?<!-- search-semantics:end -->', '', text, flags=re.S)
    text = re.sub(r'\s*<meta\s+(?:property="og:[^"]+"|name="twitter:[^"]+")[^>]*>', '', text, flags=re.I)
    governed_title, governed_description = META_COPY[lang][kind]
    text = re.sub(r'<title>.*?</title>', f'<title>{html.escape(governed_title)}</title>', text, count=1, flags=re.S | re.I)
    text = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', rf'\1{html.escape(governed_description, quote=True)}\2', text, count=1, flags=re.I)
    title = extract(text, r'<title>(.*?)</title>', path)
    description = extract(text, r'<meta\s+name="description"\s+content="([^"]*)"', path)
    canonical = extract(text, r'<link\s+rel="canonical"\s+href="([^"]*)"', path)
    image = "Product_Images/03_Outdoor_Furniture/swf_91704140_1.png" if kind in {"index","products","contact"} else PROJECTS[0]["images"][0]
    block = ["  <!-- search-semantics:start -->", '  <meta property="og:type" content="website">', '  <meta property="og:site_name" content="Sunnyward">', f'  <meta property="og:locale" content="{LANGS[lang]["og_locale"]}">', f'  <meta property="og:title" content="{html.escape(title, quote=True)}">', f'  <meta property="og:description" content="{html.escape(description, quote=True)}">', f'  <meta property="og:url" content="{canonical}">', f'  <meta property="og:image" content="{public_url(image)}">', f'  <meta property="og:image:alt" content="{html.escape(LANGS[lang][kind if kind != "index" else "products"], quote=True)}">', '  <meta name="twitter:card" content="summary_large_image">', f'  <meta name="twitter:title" content="{html.escape(title, quote=True)}">', f'  <meta name="twitter:description" content="{html.escape(description, quote=True)}">', f'  <meta name="twitter:image" content="{public_url(image)}">']
    for schema in schema_for(kind, lang, canonical, title, description):
        block.append(f'  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>')
    block.append("  <!-- search-semantics:end -->")
    text = text.replace("</head>", "\n".join(block) + "\n</head>", 1)
    path.write_text(text, encoding="utf-8", newline="\n")


for lang in LANGS:
    for filename, kind in (("index.html","index"),("products.html","products"),("projects.html","projects"),("contact.html","contact")):
        enhance(ROOT / lang / filename, lang, kind)
print("Enhanced 12 multilingual landing pages with governed social metadata and page-type schemas.")
