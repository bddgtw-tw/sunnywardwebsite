from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "verified_project_pages.json").read_text(encoding="utf-8"))
PRODUCTS = json.loads((ROOT / "data" / "verified_product_pages.json").read_text(encoding="utf-8"))["products"]
LABELS = {
    "en": {"meta":"PROJECT MEDIA RECORD", "badge":"Video and site images verified"},
    "tw": {"meta":"專案媒體紀錄", "badge":"已核對影片與現場圖片"},
    "jp": {"meta":"プロジェクトメディア記録", "badge":"映像・現場写真を確認済み"},
}
HOME = {
    "en": {
        "label":"Commercial furniture · Verified product and project records",
        "title":"Commercial furniture,<br><em>for hospitality</em><br>and project spaces.",
        "hero":"Sunnyward supports designers, architects and hospitality buyers with commercial furniture sourcing, verified product information and project coordination.",
        "stats":[("3","Language editions"),("3","Verified product records"),("10","Project media records")],
        "lead_title":"Commercial furniture decisions supported by clear project information.",
        "lead":"We publish verified dimensions, materials and media where source records are available, and confirm project-specific requirements during quotation.",
        "strengths":[("Project coordination","Production, delivery timing and site requirements are reviewed against the information supplied for each enquiry."),("Evidence-led specifications","Published pilot products use cross-checked dimensions, materials and images. Certification is stated only when supporting documents are available."),("Commercial material options","Current verified records include aluminum, rope, Batyline mesh and cushion configurations, with additional requirements confirmed per project.")],
        "spotlight":"Verified product record", "view":"View verified product details", "projects_title":"Verified Project Records"
    },
    "tw": {
        "label":"商用家具選品 · 已核對產品與專案紀錄",
        "title":"商用家具，<br><em>服務餐旅</em><br>與專案空間。",
        "hero":"Sunnyward 為設計師、建築師與旅宿餐飲採購提供商用家具選品、已核對產品資訊與專案協調服務。",
        "stats":[("3","語言版本"),("3","已核對產品紀錄"),("10","專案媒體紀錄")],
        "lead_title":"以清楚的專案資訊，協助商用家具決策。",
        "lead":"現有來源可核對時，我們會公開尺寸、材質與媒體；專案特定規格則在詢價階段依需求逐項確認。",
        "strengths":[("專案協調","依每次詢價提供的資料，確認生產條件、交付時程與現場需求。"),("以證據為準的規格","首批公開產品的尺寸、材質與圖片均經交叉核對；認證資訊僅在具備佐證文件時標示。"),("商用材質選項","目前已核對資料包含鋁合金、繩編、Batyline 網布與坐墊配置，其他需求依專案確認。")],
        "spotlight":"已核對產品紀錄", "view":"查看已核對產品資料", "projects_title":"已核對專案紀錄"
    },
    "jp": {
        "label":"業務用家具選定 · 確認済み製品・プロジェクト記録",
        "title":"ホスピタリティと<br><em>プロジェクト空間</em><br>の業務用家具。",
        "hero":"Sunnyward は、デザイナー、建築家、ホスピタリティ分野の購買担当者に、業務用家具の選定、確認済み製品情報、プロジェクト調整を提供します。",
        "stats":[("3","言語版"),("3","確認済み製品記録"),("10","プロジェクト資料記録")],
        "lead_title":"明確なプロジェクト情報で、業務用家具の選定を支援します。",
        "lead":"根拠資料を確認できる場合に寸法、素材、画像を公開し、案件固有の仕様は見積もり時に個別確認します。",
        "strengths":[("プロジェクト調整","お問い合わせ時の情報に基づき、生産条件、納期、現場要件を案件ごとに確認します。"),("根拠に基づく仕様情報","公開中の製品は寸法、素材、画像を照合済みです。認証情報は裏付け資料がある場合にのみ掲載します。"),("業務用素材の選択肢","現在の確認済み資料にはアルミ、ロープ、Batyline メッシュ、クッション仕様が含まれ、その他は案件ごとに確認します。")],
        "spotlight":"確認済み製品記録", "view":"確認済み製品情報を見る", "projects_title":"確認済みプロジェクト記録"
    },
}


def card(project: dict, lang: str, index: int) -> str:
    loc = project["locales"][lang]
    delay = " delay-2" if index == 1 else ""
    return f'''        <a class="project-card reveal{delay}" href="projects/{html.escape(project['slug'])}.html">
          <div class="project-img-wrapper">
            <img src="../{html.escape(project['images'][0])}" alt="{html.escape(loc['name'])}" loading="lazy">
          </div>
          <div class="project-info">
            <span class="project-meta">{LABELS[lang]['meta']} · {html.escape(project['date'])}</span>
            <h3 class="project-card__title">{html.escape(loc['name'])}</h3>
            <p class="project-desc">{html.escape(loc['description'])}</p>
            <span class="project-product-badge">{LABELS[lang]['badge']}</span>
          </div>
        </a>'''


def product_spotlights(lang: str) -> str:
    selected = (PRODUCTS[0], PRODUCTS[2])
    blocks = []
    for index, product in enumerate(selected):
        loc = product["locales"][lang]
        reverse = " split-section--reverse" if index else ""
        dark_class = ' split-section--dark' if index else ''
        dark_style = ' style="background:var(--bg-invert);"' if index else ''
        text_style = ' style="color:var(--cream);"' if index else ''
        paragraph_style = ' style="margin:1.2rem 0 2rem; color:rgba(248,245,240,0.68);"' if index else ' style="margin:1.2rem 0 2rem;"'
        link_style = ' style="color:var(--copper-light);"' if index else ''
        blocks.append(f'''  <div class="split-section{reverse} reveal-fade">
    <div class="split-section__image"><img src="../{html.escape(product['images'][0])}" alt="{html.escape(loc['name'])}" loading="lazy"></div>
    <div class="split-section__content{dark_class}"{dark_style}>
      <span class="eyebrow">{HOME[lang]['spotlight']}</span>
      <h2{text_style}>{html.escape(loc['name'])}</h2>
      <p{paragraph_style}>{html.escape(loc['intro'])}</p>
      <a href="products/{html.escape(product['slug'])}.html" class="btn-arrow"{link_style}>{HOME[lang]['view']}</a>
    </div>
  </div>''')
    return "\n\n".join(blocks)


def sync_claims(text: str, lang: str) -> str:
    cfg = HOME[lang]
    text = re.sub(r'<span class="hero__label-text">.*?</span>', f'<span class="hero__label-text">{cfg["label"]}</span>', text, count=1, flags=re.S)
    text = re.sub(r'<h1 class="hero__title">.*?</h1>', f'<h1 class="hero__title">{cfg["title"]}</h1>', text, count=1, flags=re.S)
    text = re.sub(r'<p class="hero__desc">.*?</p>', f'<p class="hero__desc">{cfg["hero"]}</p>', text, count=1, flags=re.S)
    text = re.sub(
        r'\s*<div class="hero__stats">.*?</div>\s*</div>\s*(?=<div class="hero__scroll">)',
        "\n      </div>\n    </div>\n\n    ",
        text,
        count=1,
        flags=re.S,
    )
    strengths = "\n".join(f'''        <div class="strength-card reveal delay-{i}">
          <span class="strength-number">0{i}</span>
          <h3>{title}</h3>
          <p>{body}</p>
        </div>''' for i, (title, body) in enumerate(cfg["strengths"], 1))
    text = re.sub(r'(<span class="eyebrow">(?:Why Sunnyward|品牌核心優勢|サニーワードの強み)</span>)\s*<h2>.*?</h2>\s*<p style="margin-top:1rem;">.*?</p>', rf'\1\n        <h2>{cfg["lead_title"]}</h2>\n        <p style="margin-top:1rem;">{cfg["lead"]}</p>', text, count=1, flags=re.S)
    text = re.sub(r'      <div class="strengths-grid">.*?</div>\s*</div>\s*</section>', f'      <div class="strengths-grid">\n{strengths}\n      </div>\n    </div>\n  </section>', text, count=1, flags=re.S)
    text = re.sub(r'  <!-- ===== EDITORIAL SPLIT.*?<!-- ===== FEATURED PROJECTS ===== -->', product_spotlights(lang) + '\n\n  <!-- ===== FEATURED PROJECTS ===== -->', text, count=1, flags=re.S)
    for old in ("Global Project Showcase", "全球商業專案實績", "グローバルプロジェクト実績"):
        text = text.replace(old, cfg["projects_title"])
    return text


def main() -> None:
    projects = DATA["projects"]
    for lang in LABELS:
        path = ROOT / lang / "index.html"
        text = path.read_text(encoding="utf-8")
        text = sync_claims(text, lang)
        grid = '<div class="projects-grid">\n' + "\n\n".join(card(p, lang, i) for i, p in enumerate(projects)) + "\n      </div>"
        text, count = re.subn(r'<div class="projects-grid">.*?</div>\s*</div>\s*</section>', grid + '\n    </div>\n  </section>', text, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError(f"Could not replace homepage project grid: {path}")
        if lang == "jp":
            text = re.sub(r'("contactPoint":\[\{"@type":")[^"]+("[,}])', r'\1ContactPoint\2', text, count=1)
        path.write_text(text, encoding="utf-8", newline="\n")
    print("Synchronized three homepages with verified project records and repaired Japanese organization schema.")


if __name__ == "__main__":
    main()
