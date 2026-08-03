from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COPY = {
    "en": {
        "eyebrow":"Commercial Furniture Sourcing & Project Catalog",
        "description":"Explore Sunnyward's full commercial furniture collection for outdoor spaces, office environments, and commercial projects. Select items, view dimensions, and request custom quotes.",
    },
    "tw": {
        "eyebrow":"商用家具選集與專案採購目錄",
        "description":"瀏覽 Sunnyward 完整的商用戶外家具、辦公家具與商業專案家具選集。包含尺寸、規格與採購洽詢服務。",
    },
    "jp": {
        "eyebrow":"業務用家具カタログ＆調達コレクション",
        "description":"Sunnywardの業務用アウトドア家具、オフィス家具、空間プロジェクト用家具の全ラインナップを掲載しています。寸法・仕様の確認とお見積もり依頼が可能です。",
    },
}


def main() -> None:
    for lang, copy in COPY.items():
        path = ROOT / lang / "products.html"
        text = path.read_text(encoding="utf-8")
        text = re.sub(r'(<div class="catalog-header reveal">\s*<div>\s*)<span class="eyebrow">.*?</span>', rf'\1<span class="eyebrow">{copy["eyebrow"]}</span>', text, count=1, flags=re.S)
        text = re.sub(r'(<div class="catalog-header reveal">\s*<div>\s*<span class="eyebrow">.*?</span>\s*<h1>.*?</h1>\s*)<p[^>]*>.*?</p>', rf'\1<p>{copy["description"]}</p>', text, count=1, flags=re.S)
        text = re.sub(
            r'function shouldShowOnFrontend\(product\) \{.*?\n    \}',
            "function shouldShowOnFrontend(product) {\n      return Boolean(product.detail_page)\n        && product.frontend_visible === true\n        && product.frontend_status === 'published';\n    }",
            text,
            count=1,
            flags=re.S,
        )
        text = text.replace("const results = allProducts.filter(p => {", "const results = getVisibleProducts().filter(p => {")
        text = text.replace("Object.keys(catTranslations).filter(key => key === 'materials' || counts[key] > 0)", "Object.keys(catTranslations).filter(key => counts[key] > 0)")
        text = text.replace("      // Initialize matching tool events\n      initMatcherEvents();", "      // Initialize the optional matching tool only when its governed content is present.\n      if (document.querySelector('.matcher-option-top') && document.querySelector('.matcher-option-base')) {\n        initMatcherEvents();\n      }")
        path.write_text(text, encoding="utf-8", newline="\n")
    print("Governed three public catalogues to full commercial catalogue copy and visibility.")


if __name__ == "__main__":
    main()
