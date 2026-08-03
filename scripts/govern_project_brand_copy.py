#!/usr/bin/env python3
"""Keep internal evidence governance out of customer-facing project copy."""

from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
COPY = {
    "en": {
        "title": "Commercial Furniture Projects",
        "intro": "Explore how Sunnyward furniture solutions support restaurants, hospitality, leisure and other commercial spaces across Southeast Asia.",
        "meta": "COMMERCIAL PROJECT",
        "blocks": (
            ("Project context", "A completed commercial furniture installation showing how furniture selection and placement support the character and use of the space."),
            ("Design focus", "Layout, materials and finishes are coordinated around the space type, operational needs and overall design direction."),
            ("Project support", "For similar projects, Sunnyward can assist with furniture sourcing, customization, delivery planning and installation coordination."),
        ),
        "detail": "Commercial project", "media": "Project media", "media_text": "Installation video and site images",
        "date": "Project date", "header": "This completed project shows how furniture selection and placement support the layout, use and character of a commercial space.",
        "planning_text": "These products may be considered when planning a similar space. Final selection depends on the project brief.", "view": "View product", "browse": "Browse products", "link": "View project",
        "note": "Project planning", "note_text": "Furniture models, finishes and specifications are developed for each project brief.",
    },
    "tw": {
        "title": "商用家具空間案例", "intro": "探索 Sunnyward 家具方案如何應用於東南亞的餐飲、旅宿、休閒及其他商業空間。",
        "meta": "商業空間案例",
        "blocks": (("專案情境", "完整呈現商用家具在空間中的配置方式，以及家具選擇如何回應場域用途與整體氛圍。"), ("設計重點", "依照空間類型、營運需求與設計方向，協調家具配置、材料與表面處理。"), ("專案支援", "相似專案可由 Sunnyward 協助家具選品、客製開發、交付規劃與安裝協調。")),
        "detail": "商業空間案例", "media": "專案影像", "media_text": "安裝影片與現場圖片", "date": "專案日期", "header": "本案例呈現家具選擇與配置如何回應商業空間的動線、用途與整體氛圍。", "planning_text": "下列產品可作為相似空間的規劃參考，最終選擇仍依專案需求而定。", "view": "查看產品", "browse": "瀏覽產品", "link": "查看案例", "note": "專案規劃", "note_text": "家具型號、表面處理與規格會依每個專案需求進行規劃。",
    },
    "jp": {
        "title": "業務用家具の導入事例", "intro": "東南アジアのレストラン、ホテル、レジャー施設などで、Sunnywardの家具ソリューションがどのように活用されているかをご覧ください。",
        "meta": "商業空間プロジェクト",
        "blocks": (("プロジェクト概要", "家具の選定と配置が、空間の用途や雰囲気をどのように支えているかを紹介する導入事例です。"), ("デザインの要点", "空間タイプ、運営上の要件、デザイン方針に合わせ、レイアウト、素材、仕上げを調整します。"), ("プロジェクト支援", "同様の案件では、家具調達、カスタマイズ、納品計画、設置調整までSunnywardが支援します。")),
        "detail": "商業空間プロジェクト", "media": "プロジェクト映像", "media_text": "導入映像と現場写真", "date": "プロジェクト時期", "header": "家具の選定と配置が、商業空間の動線、用途、雰囲気にどのように応えているかを紹介する事例です。", "planning_text": "以下の製品は類似空間を計画する際の参考です。最終選定は案件要件に合わせて行います。", "view": "製品を見る", "browse": "製品を見る", "link": "事例を見る", "note": "プロジェクト計画", "note_text": "家具モデル、仕上げ、仕様は案件ごとの要件に合わせて計画します。",
    },
}

CONTACT_LINK = {
    "en": "Plan a similar space",
    "tw": "規劃相似空間",
    "jp": "同様の空間を相談する",
}

NARRATIVE_LABELS = {
    "en": ("Project overview", "What to notice", "Potential project value"),
    "tw": ("案例概覽", "配置重點", "可預期的空間價值"),
    "jp": ("プロジェクト概要", "注目ポイント", "期待できる空間価値"),
}

SPACE_COPY = {
    "en": {
        "fb": "The installation is shown in its completed dining environment, making it possible to review furniture scale, spacing and its relationship with customer circulation.",
        "office": "The completed setting shows how the furniture supports workplace use while remaining coordinated with the surrounding architecture.",
        "wellness": "The installed furniture is presented within the finished interior, showing how seating contributes to a calm arrival and waiting environment.",
        "public": "The completed public-space installation shows how outdoor furniture is distributed across a large leisure environment.",
    },
    "tw": {
        "fb": "透過完成後的用餐空間，可直接觀察家具尺度、座位間距，以及桌椅配置與顧客動線的關係。",
        "office": "完成後的場景呈現家具如何支援辦公使用，並與周圍建築及空間語彙保持協調。",
        "wellness": "現場圖片呈現家具在完整室內環境中的效果，以及座椅如何形塑沉穩的迎賓與等候氛圍。",
        "public": "完成後的公共休閒空間呈現戶外家具如何分布於大尺度場域。",
    },
    "jp": {
        "fb": "完成後のダイニング空間から、家具のスケール、座席間隔、テーブル配置と来店者動線の関係を確認できます。",
        "office": "完成した空間を通じて、家具が業務利用を支えながら周囲の建築と調和する様子を確認できます。",
        "wellness": "完成したインテリアの中で、家具が落ち着いた受付・待合環境づくりにどう寄与するかを紹介しています。",
        "public": "完成した公共レジャー空間における屋外家具の配置と広がりを確認できます。",
    },
}

PRODUCT_COPY = {
    "en": {
        "chair": "Review seating density, table relationships, aisle clearance and the visual consistency of repeated chair placement.",
        "sofa": "Review lounge-seat placement, usable clearances and how upholstered volumes relate to the surrounding finishes.",
        "outdoor": "Review furniture spacing, exposure conditions, circulation routes and the relationship between seating and the outdoor setting.",
    },
    "tw": {
        "chair": "可留意座位密度、桌椅關係、通道寬度，以及大量座椅重複配置後的整體一致性。",
        "sofa": "可留意休憩座位的位置、實際通行空間，以及軟墊家具量體與周圍材質的關係。",
        "outdoor": "可留意家具間距、戶外曝曬條件、主要動線，以及座位與周圍環境的關係。",
    },
    "jp": {
        "chair": "座席密度、テーブルとの関係、通路幅、チェアを連続配置した際の統一感に注目できます。",
        "sofa": "ラウンジ席の配置、有効な通行スペース、張り家具のボリュームと周囲の仕上げとの関係に注目できます。",
        "outdoor": "家具間隔、屋外環境への露出、主要動線、座席と周辺空間との関係に注目できます。",
    },
}

VALUE_COPY = {
    "en": {
        "fb": "A coordinated furniture plan can support clearer circulation, a more consistent dining atmosphere and a guest environment that better reflects the operator's concept.",
        "office": "A well-resolved furniture layout can support more comfortable everyday use, clearer movement and a workplace environment with stronger visual coherence.",
        "wellness": "Furniture selected as part of the complete interior can help establish a calmer first impression and a more comfortable transition into the customer experience.",
        "public": "A coordinated outdoor furniture plan can help define rest zones, maintain clearer circulation and create a more inviting leisure environment for different visitor groups.",
    },
    "tw": {
        "fb": "整合式家具規劃可望帶來更清楚的用餐動線、更一致的空間氛圍，並讓顧客體驗更貼近營運品牌的定位。",
        "office": "完整的家具配置可望支援更舒適的日常使用、更清楚的移動路徑，並提升辦公環境的視覺一致性。",
        "wellness": "將家具納入整體室內規劃，可望建立更沉穩的第一印象，並讓顧客更自然地進入後續服務體驗。",
        "public": "整合式戶外家具規劃可望界定休憩區域、維持清楚動線，並為不同訪客創造更具吸引力的休閒環境。",
    },
    "jp": {
        "fb": "家具を一体的に計画することで、より明確な動線、統一感のあるダイニングの雰囲気、運営ブランドのコンセプトに沿った顧客体験が期待できます。",
        "office": "家具レイアウトを整えることで、日常利用の快適性、移動のしやすさ、ワークプレイス全体の視覚的な統一感が期待できます。",
        "wellness": "家具をインテリア全体の一部として選定することで、落ち着いた第一印象と、その後のサービス体験への自然な導入が期待できます。",
        "public": "屋外家具を一体的に計画することで、休憩ゾーンを明確にし、動線を保ちながら、多様な来場者にとって魅力的なレジャー環境をつくることが期待できます。",
    },
}

# Add only approved, source-traceable client quotations here.
APPROVED_FEEDBACK = {}


for lang, copy in COPY.items():
    listing_path = ROOT / lang / "projects.html"
    soup = BeautifulSoup(listing_path.read_text(encoding="utf-8"), "html.parser")
    soup.body["class"] = list(dict.fromkeys([*(soup.body.get("class") or []), "project-listing-page"]))
    header = soup.select_one(".projects-intro, .ultimate-header, main header")
    h1 = soup.select_one("h1")
    if h1:
        h1.string = copy["title"]
        intro = h1.find_next("p")
        if intro:
            intro.string = copy["intro"]
    for section in soup.select("section.ultimate-case-section"):
        meta = section.select_one(".meta")
        if meta:
            date = meta.get_text(" ", strip=True).split("·")[-1].strip()
            meta.string = f'{copy["meta"]} · {date}'
        narrative = section.select_one(".uc-narrative")
        if narrative:
            links = list(narrative.select("a.project-detail-link"))
            narrative.clear()
            labels = NARRATIVE_LABELS[lang]
            narrative_copy = (
                (labels[0], SPACE_COPY[lang][section.get("data-space")]),
                (labels[1], PRODUCT_COPY[lang][section.get("data-product")]),
                (labels[2], VALUE_COPY[lang][section.get("data-space")]),
            )
            for heading, text in narrative_copy:
                block = soup.new_tag("div")
                block["class"] = ["uc-text-block"]
                h4 = soup.new_tag("h4"); h4.string = heading
                p = soup.new_tag("p"); p.string = text
                block.extend((h4, p)); narrative.append(block)
            feedback = APPROVED_FEEDBACK.get((lang, section.get("id")))
            if feedback:
                quote, author = feedback
                testimonial = soup.new_tag("figure")
                testimonial["class"] = ["uc-testimonial"]
                quotation = soup.new_tag("blockquote"); quotation.string = quote
                caption = soup.new_tag("figcaption"); caption.string = author
                testimonial.extend((quotation, caption)); narrative.append(testimonial)
            if links:
                for link in links:
                    if link.get("href") == "contact.html":
                        link.string = f'{CONTACT_LINK[lang]} →'
                    else:
                        link.string = f'{copy["link"]} →'
                    narrative.append(link)
            else:
                link = soup.new_tag("a", href="contact.html")
                link["class"] = ["project-detail-link"]
                link.string = f'{CONTACT_LINK[lang]} →'
                narrative.append(link)
    listing_path.write_text(str(soup), encoding="utf-8", newline="\n")

    for detail_path in (ROOT / lang / "projects").glob("*.html"):
        detail = BeautifulSoup(detail_path.read_text(encoding="utf-8"), "html.parser")
        eyebrow = detail.select_one(".verified-project-header .eyebrow")
        if eyebrow: eyebrow.string = copy["detail"]
        header_intro = detail.select_one(".verified-project-header > p")
        if header_intro: header_intro.string = copy["header"]
        facts = detail.select(".verified-project-facts > div")
        if len(facts) >= 3:
            facts[1].select_one("h2").string = copy["date"]
            facts[2].select_one("h2").string = copy["media"]
            facts[2].select_one("p").string = copy["media_text"]
        note = detail.select_one(".verified-project-standard")
        if note:
            note.select_one("h2").string = copy["note"]
            note.select_one("p").string = copy["note_text"]
        planning = detail.select_one(".project-product-intro p")
        if planning: planning.string = copy["planning_text"]
        for product_link in detail.select("a.project-product-link"):
            product_link.string = f'{copy["browse"] if product_link.get("href", "").endswith("products.html") else copy["view"]} →'
        detail_path.write_text(str(detail), encoding="utf-8", newline="\n")

print("Reframed project pages for commercial buyers in three languages.")
