#!/usr/bin/env python3
"""Remove internal governance terminology from customer-facing copy and metadata."""

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString


ROOT = Path(__file__).resolve().parents[1]
REPLACEMENTS = {
    "en": {
        "Verified commercial outdoor furniture": "Commercial outdoor furniture",
        "Verified product record": "Featured product",
        "Verified product details": "Product details",
        "View verified product details": "View product details",
        "Verified product information": "Product specifications",
        "Verified specifications": "Product specifications",
        "Verified public product records": "Selected commercial products",
        "verified product information": "product information",
        "verified dimensions, materials and images": "dimensions, materials and product images",
        "verified dimensions": "listed dimensions",
        "verified products": "selected products",
        "verified product": "product",
        "Video and site images verified": "View installation",
        "PROJECT MEDIA RECORD": "COMMERCIAL PROJECT",
        "Project media record": "Commercial project",
        "project media records": "commercial projects",
        "Media-backed project records": "Commercial furniture projects",
        "media-backed installation records": "commercial furniture projects",
        "media-backed": "completed",
        "archived video": "project video",
        "Archive date": "Project date",
        "archived in": "completed in",
        "source verification": "project review",
        "Verified pilot catalogue": "Commercial furniture selection",
        "Verified furniture installation records": "Commercial furniture projects",
        "with dimensions, materials and images cross-checked against current source records. Additional products are released only after verification.": "with dimensions, materials and images for project planning and enquiry.",
        "pilot catalogue of three commercial outdoor furniture products with cross-checked dimensions, materials, images and enquiry links": "selection of commercial outdoor furniture products with dimensions, materials, images and enquiry links",
        "pilot catalogue": "product selection",
        "Verified ": "",
    },
    "tw": {
        "已核對商用戶外家具": "商用戶外家具",
        "已核對產品試行目錄": "商用家具精選",
        "已核對產品紀錄": "精選產品",
        "已核對產品資料": "產品資料",
        "已核對產品資訊": "產品規格",
        "已核對規格": "產品規格",
        "查看已核對產品資料": "查看產品資料",
        "查看已核對產品": "查看產品",
        "瀏覽已核對產品型錄": "瀏覽產品型錄",
        "已核對產品": "精選產品",
        "已核對影片與現場圖片": "查看安裝內容",
        "專案媒體紀錄": "商業空間案例",
        "媒體存檔日期": "專案日期",
        "具影片與現場圖片佐證的": "",
        "具媒體佐證的安裝紀錄": "商用家具案例",
        "佐證": "參考",
        "已核對的": "",
        "提供已核對": "提供",
        "已核對尺寸": "產品尺寸",
        "查看具媒體參考的案例紀錄": "查看相關案例",
        "核實": "確認",
        "已核對": "",
    },
    "jp": {
        "確認済み業務用アウトドア家具": "業務用アウトドア家具",
        "確認済み製品パイロットカタログ": "業務用家具セレクション",
        "確認済み製品記録": "注目製品",
        "確認済み製品情報": "製品仕様",
        "確認済み仕様": "製品仕様",
        "確認済み製品を見る": "製品を見る",
        "確認済み製品カタログを見る": "製品を見る",
        "確認済み製品": "製品候補",
        "映像・現場写真を確認済み": "導入内容を見る",
        "プロジェクトメディア記録": "商業空間プロジェクト",
        "メディア保存日": "プロジェクト時期",
        "確認済み家具導入記録": "業務用家具の導入事例",
        "確認済みの": "",
        "確認済み寸法": "製品寸法",
        "メディアで確認できる導入記録を見る": "関連プロジェクトを見る",
        "確認済み": "",
    },
}


def replace(value: str, lang: str) -> str:
    for old, new in REPLACEMENTS[lang].items():
        value = re.sub(re.escape(old), new, value, flags=re.IGNORECASE)
    return value


PRODUCT_COPY = {
    "en": ("Product details", "Dimensions, materials, origin and product images are provided for project evaluation. Pricing and order terms are confirmed for each enquiry.", "Please confirm the following conditions for the exact order, destination and project requirements before specification.", "View related project →"),
    "tw": ("產品資料", "本頁提供尺寸、材質、產地與產品圖片，供專案選品與評估使用；價格及交易條件將依每次詢價內容確認。", "以下條件請依實際訂單、交貨地點與專案需求，在納入規格或下單前確認。", "查看相關案例 →"),
    "jp": ("製品仕様", "寸法、素材、原産国、製品画像をプロジェクト検討用に掲載しています。価格と取引条件はお問い合わせ内容ごとに確認します。", "以下の条件は、注文内容、納入先、案件要件に合わせ、仕様決定前にご確認ください。", "関連プロジェクトを見る →"),
}

PRODUCT_INDEX_COPY = {
    "en": "Explore product dimensions, materials and images, then discuss finishes, quantities and delivery requirements with our team.",
    "tw": "瀏覽產品尺寸、材質與圖片，並與我們確認表面處理、數量及交付需求。",
    "jp": "製品の寸法、素材、画像を確認し、仕上げ、数量、納品条件についてご相談ください。",
}


for lang in REPLACEMENTS:
    for path in (ROOT / lang).rglob("*.html"):
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        for node in list(soup.find_all(string=True)):
            if not isinstance(node, NavigableString) or node.parent.name in {"style"}:
                continue
            if node.parent.name == "script" and node.parent.get("type") != "application/ld+json":
                continue
            updated = replace(str(node), lang)
            if updated != str(node): node.replace_with(updated)
        for tag in soup.find_all(True):
            for attr in ("content", "title", "alt", "aria-label"):
                if tag.get(attr): tag[attr] = replace(tag[attr], lang)
        if soup.select_one("main.verified-product-page"):
            detail_label, intro, conditions, reference = PRODUCT_COPY[lang]
            eyebrow = soup.select_one(".verified-product-details .eyebrow")
            if eyebrow: eyebrow.string = detail_label
            procurement = soup.select(".verified-product-procurement p")
            if procurement: procurement[0].string = intro
            if len(procurement) > 1: procurement[1].string = conditions
            related = soup.select_one(".verified-product-reference__link")
            if related: related.string = reference
        product_index = soup.select_one(".verified-products-index")
        if product_index:
            intro = product_index.select_one(":scope > .container > p")
            if intro: intro.string = PRODUCT_INDEX_COPY[lang]
        path.write_text(str(soup), encoding="utf-8", newline="\n")

    catalogue = ROOT / lang / "products.json"
    data = json.loads(catalogue.read_text(encoding="utf-8"))
    def walk(value):
        if isinstance(value, str): return replace(value, lang)
        if isinstance(value, list): return [walk(item) for item in value]
        if isinstance(value, dict): return {key: walk(item) for key, item in value.items()}
        return value
    catalogue.write_text(json.dumps(walk(data), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

root_entry = ROOT / "index.html"
root_entry.write_text(root_entry.read_text(encoding="utf-8").replace("verified project records", "commercial furniture projects"), encoding="utf-8", newline="\n")
print("Removed internal governance terminology from customer-facing copy.")
