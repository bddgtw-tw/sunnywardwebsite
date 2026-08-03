#!/usr/bin/env python3
"""Apply the approved B2B homepage positioning after data-driven sections are synced."""

from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
HERO = "../_assets/projects/486466926_1193879656080876_2767098548785792068_n_hero.jpg"
HERO_VIDEO = "../_assets/hero/brand/sunnyward-brand-hero-canva-v1.mp4"
HERO_POSTER = "../_assets/hero/brand/sunnyward-brand-hero-canva-v1-poster.jpg"
COPY = {
    "en": {
        "label": "Commercial furniture project partner",
        "title": "From Design Concepts to Commercial Spaces",
        "desc": "Sunnyward provides commercial furniture sourcing, customization and project coordination for restaurants, hospitality, leisure, office and commercial spaces across Southeast Asia.",
        "products": "Explore Products", "contact": "Discuss a Project", "strength_eyebrow": "Company Strength",
        "strength_title": "Built for the realities of commercial furniture projects.",
        "strength_intro": "Regional experience, coordinated sourcing and practical project support from concept review to delivery planning.",
        "strengths": [("Since 1988", "Decades of furniture and international trade experience."), ("Southeast Asia Operations", "Local presence in Malaysia and Singapore for regional coordination."), ("One-Stop Furniture Solutions", "A consolidated route from sourcing and customization to delivery planning."), ("Commercial Project Expertise", "Support shaped around hospitality, leisure, office and retail requirements.")],
        "space_eyebrow": "Space Solutions", "space_title": "Furniture planning for the spaces your customers use.",
        "spaces": ["Restaurants & Cafés", "Hotels & Resorts", "Outdoor & Leisure", "Office & Training", "Retail & Commercial", "Custom Project Furniture"],
        "projects_eyebrow": "Selected Work", "projects_title": "Commercial Projects",
        "cta": "Share your floor plan, furniture schedule, reference images, quantities, project location and target completion date. We will review the brief and recommend the most practical next step.",
        "meta": "Commercial furniture sourcing, customization and project coordination for hospitality, restaurant, leisure, office and retail spaces across Southeast Asia.",
    },
    "tw": {
        "label": "商用家具專案夥伴", "title": "從設計概念，到真正落地的商業空間",
        "desc": "Sunnyward 為東南亞的餐飲、旅宿、休閒、辦公與商業空間，提供商用家具採購、客製化與專案協調服務。",
        "products": "瀏覽產品", "contact": "洽談專案", "strength_eyebrow": "企業實力",
        "strength_title": "為商用家具專案的真實需求而生。", "strength_intro": "從概念審視、家具採購與客製，到交期與交付規劃，提供務實而一致的區域協作。",
        "strengths": [("始於 1988", "累積數十年的家具與國際貿易經驗。"), ("東南亞營運據點", "以馬來西亞與新加坡據點支援區域專案協調。"), ("一站式家具方案", "整合採購、客製化與交付規劃，降低多方溝通成本。"), ("商用專案經驗", "理解旅宿、餐飲、休閒、辦公與零售空間的實際需求。")],
        "space_eyebrow": "空間解決方案", "space_title": "依照空間用途，規劃合適的家具組合。",
        "spaces": ["餐廳與咖啡廳", "飯店與度假村", "戶外與休閒空間", "辦公與培訓空間", "零售與商業空間", "專案客製家具"],
        "projects_eyebrow": "精選案例", "projects_title": "商用空間專案",
        "cta": "歡迎提供平面圖、家具清單、參考圖片、數量、專案地點與預計完成日期。我們會審視需求，並建議最務實的下一步。",
        "meta": "Sunnyward 為東南亞旅宿、餐飲、休閒、辦公與零售空間提供商用家具採購、客製化與專案協調。",
    },
    "jp": {
        "label": "業務用家具プロジェクトパートナー", "title": "デザインの構想を、実際の商業空間へ",
        "desc": "Sunnywardは東南アジアのレストラン、ホテル、レジャー、オフィス、商業施設に向け、業務用家具の調達、カスタマイズ、プロジェクト調整を提供します。",
        "products": "製品を見る", "contact": "プロジェクトを相談", "strength_eyebrow": "企業力",
        "strength_title": "商業家具プロジェクトの現実に応える体制。", "strength_intro": "構想の確認から家具調達、カスタマイズ、納品計画まで、地域に根ざした実務支援を行います。",
        "strengths": [("1988年創業", "家具と国際取引における長年の経験。"), ("東南アジアの運営拠点", "マレーシアとシンガポールから地域案件を調整。"), ("ワンストップ家具ソリューション", "調達、カスタマイズ、納品計画を一つの窓口で連携。"), ("商業プロジェクトの知見", "ホテル、飲食、レジャー、オフィス、小売の要件に対応。")],
        "space_eyebrow": "空間ソリューション", "space_title": "空間の用途に合わせた家具計画。",
        "spaces": ["レストラン・カフェ", "ホテル・リゾート", "屋外・レジャー", "オフィス・研修", "小売・商業施設", "プロジェクト特注家具"],
        "projects_eyebrow": "導入事例", "projects_title": "商業空間プロジェクト",
        "cta": "平面図、家具リスト、参考画像、数量、案件場所、希望納期をお送りください。内容を確認し、実現性の高い次のステップをご提案します。",
        "meta": "Sunnywardは東南アジアのホテル、飲食、レジャー、オフィス、小売空間に業務用家具の調達、カスタマイズ、プロジェクト調整を提供します。",
    },
}

PROJECT_DESCRIPTIONS = {
    "en": [
        "Restaurant dining installation with coordinated tables and seating for a contemporary guest environment.",
        "High-traffic cafeteria furniture installation planned for flexible family dining.",
        "Poolside furniture installation supporting outdoor leisure, circulation and guest comfort.",
    ],
    "tw": [
        "以桌椅配置回應餐廳用餐動線與當代空間氛圍。",
        "為高使用頻率的家庭餐飲空間規劃彈性家具配置。",
        "以戶外家具支援池畔休憩、動線與訪客舒適度。",
    ],
    "jp": [
        "テーブルとチェアの配置で、レストランの動線と現代的な雰囲気を整えた事例です。",
        "利用頻度の高いファミリー向けダイニングに、柔軟な家具配置を計画した事例です。",
        "屋外家具でプールサイドの休憩、動線、快適性を支えた事例です。",
    ],
}

PROJECT_LINK_TEXT = {"en": "View project", "tw": "查看案例", "jp": "事例を見る"}


def fragment(html: str):
    return BeautifulSoup(html, "html.parser")


for locale, c in COPY.items():
    path = ROOT / locale / "index.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    hero = soup.select_one("section.hero")
    assert hero is not None
    image = hero.select_one(".hero__bg img")
    image["src"] = HERO
    image["alt"] = c["title"]
    image["width"], image["height"] = "846", "504"
    existing_video = hero.select_one(".hero__video")
    if existing_video:
        existing_video.decompose()
    video = fragment(
        f'<video class="hero__video" autoplay muted playsinline preload="metadata" width="1364" height="768" '
        f'poster="{HERO_POSTER}" aria-hidden="true" tabindex="-1">'
        f'<source src="{HERO_VIDEO}" type="video/mp4"></video>'
    ).video
    image.insert_before(video)
    hero.select_one(".hero__label-text").string = c["label"]
    title = hero.select_one("h1.hero__title")
    title.clear(); title.string = c["title"]
    hero.select_one(".hero__desc").string = c["desc"]
    actions = hero.select(".hero__actions a")
    actions[0].string, actions[1].string = c["products"], c["contact"]

    first = soup.select_one("section.section")
    strengths = "".join(f'<article class="home-strength"><span class="home-strength__mark" aria-hidden="true"></span><h3>{title}</h3><p>{text}</p></article>' for title, text in c["strengths"])
    spaces = "".join(f'<article class="home-solution"><svg aria-hidden="true" viewBox="0 0 32 32"><path d="M5 25V10l11-5 11 5v15M10 25v-8h12v8M4 25h24"/></svg><h3>{name}</h3></article>' for name in c["spaces"])
    replacement = fragment(f'''<section class="section home-positioning"><div class="container"><div class="about-section-heading reveal"><span class="eyebrow">{c['strength_eyebrow']}</span><h2>{c['strength_title']}</h2><p>{c['strength_intro']}</p></div><div class="home-strengths">{strengths}</div><div class="home-solutions-heading reveal"><span class="eyebrow">{c['space_eyebrow']}</span><h2>{c['space_title']}</h2></div><div class="home-solutions">{spaces}</div></div></section>''').section
    first.replace_with(replacement)

    selected = next((section for section in soup.select("section") if section.select_one(".projects-grid")), None)
    if selected:
        eyebrow = selected.select_one(".eyebrow")
        heading = selected.select_one("h2")
        if eyebrow: eyebrow.string = c["projects_eyebrow"]
        heading.string = c["projects_title"]
        descriptions = selected.select(".project-desc")
        assert len(descriptions) == len(PROJECT_DESCRIPTIONS[locale])
        for description, text in zip(descriptions, PROJECT_DESCRIPTIONS[locale]):
            description.string = text
        for badge in selected.select(".project-product-badge"):
            badge.string = PROJECT_LINK_TEXT[locale]

    closing = soup.select_one("section.section--dark")
    if closing and closing.select_one("p"):
        closing.select_one("p").string = c["cta"]

    for tag in soup.select('link[href*="unsplash"], link[href*="images.unsplash"]'):
        tag.decompose()
    for selector in ('meta[name="description"]', 'meta[property="og:description"]', 'meta[name="twitter:description"]'):
        tag = soup.select_one(selector)
        if tag: tag["content"] = c["meta"]
    path.write_text(str(soup), encoding="utf-8")

print("Applied approved B2B positioning to three homepages.")
