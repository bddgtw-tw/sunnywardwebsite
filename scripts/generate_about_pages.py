#!/usr/bin/env python3
"""Generate the three production About pages from one governed structure."""

from __future__ import annotations

import html
import json
from pathlib import Path

from organization_schema import organization_schema
from render_shared_footer import render_public_footer
from site_config import public_url


ROOT = Path(__file__).resolve().parents[1]
HERO = "_assets/projects/486466926_1193879656080876_2767098548785792068_n_hero.jpg"
STORY = "_assets/projects/489433395_1207544954714346_7387054704136033221_n_photo_1.jpg"

COPY = {
"en": {
"html_lang":"en","short":"EN","label":"English","title":"About Sunnyward | Commercial Furniture Solutions Since 1988","description":"Learn about Sunnyward’s commercial furniture experience since 1988 and our regional support for sourcing, customisation, production, delivery and project coordination across Southeast Asia.",
"nav":["Home","About","Products","Projects","Contact"],"eyebrow":"ABOUT SUNNYWARD","hero":"Commercial furniture expertise built across Asia.","intro":"Sunnyward supports designers, hospitality operators and commercial project teams with furniture sourcing, customisation and project coordination across Southeast Asia.","support":"Our experience combines furniture-making knowledge originating from Taiwan with regional operations in Malaysia and Singapore.","projects":"View Our Projects","discuss":"Discuss Your Project",
"story_eye":"OUR STORY","story_h":"From furniture-making experience to regional project support.","story_p":["Sunnyward’s furniture experience began in Taiwan in 1988. That foundation developed into a practical understanding of commercial furniture construction, materials, production and project delivery.","Malaysia became Sunnyward’s operating base in Southeast Asia in 2018, supporting commercial projects, regional sourcing and on-site coordination. The Singapore regional office later expanded business development and cross-border support.","Today, Sunnyward works with designers, architects, operators and project partners to turn furniture concepts into workable commercial solutions—from product selection and custom development to production follow-up, logistics, delivery and installation support."],
"journey_eye":"OUR JOURNEY","journey_h":"Experience developed across three regional foundations.","journey":[("1988","Taiwan foundation","Furniture and commercial project experience began in Taiwan, building knowledge in construction, materials and custom production."),("2018","Malaysia operations","A Southeast Asian operating base for project coordination, sourcing, delivery and local project requirements."),("2025","Singapore regional office","A regional platform supporting partnerships, export activities and Southeast Asian business development."),("Today","Regional project support","Commercial furniture support across F&B, hospitality, outdoor leisure, office, retail and other project environments.")],
"what_eye":"WHAT WE DO","what_h":"One partner across the furniture project journey.","what_intro":"Our role can begin with a product enquiry or a complete project brief. We coordinate resources around the design intent, budget, quantity, schedule and delivery location.","caps":[("Furniture Sourcing","Suitable commercial furniture based on application, quantity, budget and delivery requirements."),("Custom Furniture Development","Review dimensions, finishes, materials, upholstery and construction details for the project."),("Material & Finish Coordination","Compare appearance, durability, maintenance and indoor or outdoor requirements."),("Cost Optimization","Review construction, quantities, packaging and logistics without losing the design intent."),("Production & Quality Coordination","Coordinate drawings, samples, material confirmation, follow-up and inspection requirements."),("Logistics, Delivery & Installation","Support container planning, export, local delivery, installation and after-sales follow-up where applicable.")],
"support_eye":"WHO WE SUPPORT","support_h":"Built for the people delivering commercial spaces.","support_intro":"Our work is shaped around the teams responsible for designing, sourcing, building and operating commercial environments.","people":["Interior Designers","Architects","F&B Operators","Hotel & Resort Operators","Developers","Main Contractors","Furniture Dealers","International Brands"],"spaces":["Restaurants & Cafés","Hotels & Resorts","Outdoor & Poolside","Offices & Training Centres","Retail & Commercial Spaces","Custom Project Environments"],
"presence_eye":"REGIONAL PRESENCE","presence_h":"Local coordination supported by regional experience.","presence":[("Taiwan Heritage","Furniture experience originating from Taiwan since 1988, forming a foundation in materials, construction and commercial furniture development."),("Malaysia Operations","Sunnyward’s Southeast Asian operating base for project coordination, sourcing, local delivery, installation support and after-sales communication."),("Singapore Regional Office","A regional platform supporting business development, export, commercial partnerships and cross-border opportunities.")],
"why_eye":"WHY SUNNYWARD","why_h":"Commercial decisions shaped around real project requirements.","why":[("Commercial Understanding","Recommendations consider traffic, maintenance, operations and commercial use."),("Flexible Solutions","Products can be adapted through dimensions, finishes, upholstery and material alternatives where feasible."),("Project Coordination","Product, production, delivery and site requirements are reviewed together."),("Regional Sourcing Perspective","Local coordination is combined with regional supplier and manufacturing resources.")],
"cta_eye":"START A CONVERSATION","cta_h":"Bring us the brief. We will help shape the furniture solution.","cta_p":"Share your floor plan, furniture schedule, reference images, quantities, project location and required completion date. We will review the information and recommend the most practical next step.","explore":"Explore Products","image_alt":"Sunnyward commercial furniture project installation"
},
"tw": {
"html_lang":"zh-Hant-TW","short":"繁中","label":"繁體中文","title":"關於 Sunnyward｜始於 1988 年的商業空間家具方案","description":"了解 Sunnyward 自 1988 年累積的家具經驗，以及我們在東南亞提供的家具選品、客製開發、生產、物流與專案協調服務。",
"nav":["首頁","關於 Sunnyward","產品","案例","聯絡我們"],"eyebrow":"關於 SUNNYWARD","hero":"跨越亞洲累積的商業空間家具經驗。","intro":"Sunnyward 為設計師、餐旅營運團隊與商業空間專案提供家具選品、客製開發與東南亞區域專案協調。","support":"我們結合始於台灣的家具製作經驗，以及馬來西亞與新加坡的區域營運能力。","projects":"查看專案案例","discuss":"洽談您的專案",
"story_eye":"品牌故事","story_h":"從家具製作經驗，發展為區域專案支援。","story_p":["Sunnyward 的家具經驗始於 1988 年的台灣，逐步累積商業家具結構、材料、生產與專案交付的實務理解。","2018 年，馬來西亞成為 Sunnyward 在東南亞的營運據點，支援當地商業專案、區域採購與現場協調；其後新加坡區域辦公室進一步拓展跨境合作。","今天，我們與設計師、建築師、營運團隊及專案夥伴合作，將家具概念轉化為可執行的商業方案，服務範圍可涵蓋選品、客製開發、生產追蹤、物流、配送與安裝支援。"],
"journey_eye":"發展歷程","journey_h":"由三個區域基礎累積而成的經驗。","journey":[("1988","台灣起點","從家具與商業空間專案經驗出發，累積結構、材料與客製生產知識。"),("2018","馬來西亞營運據點","支援東南亞商業家具專案、區域採購、配送協調與在地需求。"),("2025","新加坡區域辦公室","支援區域合作、出口業務與東南亞商務發展。"),("Today","區域專案支援","服務餐飲、旅宿、戶外休閒、辦公、零售及其他商業環境。")],
"what_eye":"我們的工作","what_h":"從需求到落地，由同一個夥伴協調家具專案。","what_intro":"無論從單一產品詢問或完整專案簡報開始，我們都會依設計意圖、預算、數量、時程與交付地點協調所需資源。","caps":[("家具選品與採購","依空間用途、數量、預算與交期尋找合適的商業家具。"),("客製家具開發","依專案需求檢視尺寸、表面處理、材料、軟墊與結構。"),("材料與表面處理協調","比較外觀、耐用度、維護方式及室內外使用條件。"),("成本優化","在不犧牲設計意圖的前提下，檢視結構、數量、包裝與物流。"),("生產與品質協調","協調圖面、樣品、材料確認、生產追蹤與檢驗需求。"),("物流、配送與安裝","視專案範圍支援裝櫃、出口、在地配送、安裝與售後追蹤。")],
"support_eye":"服務對象","support_h":"為真正負責商業空間落地的團隊而設計。","support_intro":"我們的工作方式圍繞著負責設計、採購、建造與營運商業環境的團隊。","people":["室內設計師","建築師","餐飲營運團隊","飯店與度假村營運團隊","開發商","總承包商","家具經銷商","國際品牌"],"spaces":["餐廳與咖啡館","飯店與度假村","戶外與泳池空間","辦公室與培訓中心","零售與商業空間","客製專案環境"],
"presence_eye":"區域營運","presence_h":"以區域經驗支援在地協調。","presence":[("台灣經驗","始於 1988 年的台灣家具經驗，奠定材料、結構與商業家具開發基礎。"),("馬來西亞營運據點","Sunnyward 的東南亞營運基地，支援專案協調、採購、配送、安裝及售後溝通。"),("新加坡區域辦公室","支援商務發展、出口、商業合作與跨境專案機會的區域平台。")],
"why_eye":"為何選擇 SUNNYWARD","why_h":"依真實專案條件做出商業決策。","why":[("商業空間理解","建議會考量人流、維護、營運方式與商用環境要求。"),("彈性方案","在可行範圍內調整尺寸、表面處理、軟墊及材料。"),("專案協調","產品、生產、配送與現場條件會一起檢視。"),("區域採購視角","結合在地協調與區域供應、製造資源。")],
"cta_eye":"開始對話","cta_h":"把需求交給我們，一起形成可執行的家具方案。","cta_p":"請提供平面圖、家具清單、參考圖片、數量、專案地點與預計完工日期。我們會檢視資料並建議最實際的下一步。","explore":"瀏覽產品","image_alt":"Sunnyward 商業空間家具專案現場"
},
"jp": {
"html_lang":"ja","short":"JP","label":"日本語","title":"Sunnywardについて｜1988年から続く業務用家具ソリューション","description":"1988年に台湾で始まったSunnywardの家具経験と、東南アジアにおける調達、特注開発、生産、物流、プロジェクト調整についてご紹介します。",
"nav":["ホーム","Sunnywardについて","製品","導入事例","お問い合わせ"],"eyebrow":"ABOUT SUNNYWARD","hero":"アジアで培った業務用家具の専門性。","intro":"Sunnywardは、設計者、ホスピタリティ事業者、商業プロジェクトチームに向けて、家具調達、カスタマイズ、東南アジアでのプロジェクト調整を提供します。","support":"台湾に由来する家具づくりの知見と、マレーシアおよびシンガポールでの地域運営を組み合わせています。","projects":"導入事例を見る","discuss":"プロジェクトを相談する",
"story_eye":"OUR STORY","story_h":"家具づくりの経験から、地域プロジェクト支援へ。","story_p":["Sunnywardの家具経験は1988年の台湾から始まり、業務用家具の構造、素材、生産、納品に関する実務的な理解へと発展しました。","2018年にはマレーシアを東南アジアの運営拠点とし、商業プロジェクト、地域調達、現場調整を支援。シンガポール地域オフィスは、その後の事業開発と国境を越えた連携を支えています。","現在はデザイナー、建築家、運営事業者、プロジェクトパートナーと協働し、製品選定、特注開発、生産フォロー、物流、配送、設置支援を通じて、家具の構想を実行可能な商業空間ソリューションへとつなげています。"],
"journey_eye":"OUR JOURNEY","journey_h":"三つの地域基盤から育った経験。","journey":[("1988","台湾での基盤","家具と商業プロジェクトの経験を通じ、構造、素材、特注生産の知見を蓄積。"),("2018","マレーシア運営拠点","東南アジアの業務用家具プロジェクト、地域調達、配送、現地要件を支援。"),("2025","シンガポール地域オフィス","地域パートナーシップ、輸出、東南アジアでの事業開発を支援。"),("Today","地域プロジェクト支援","飲食、宿泊、屋外レジャー、オフィス、小売などの商業環境に対応。")],
"what_eye":"WHAT WE DO","what_h":"家具プロジェクトの流れを、一つの窓口で。","what_intro":"単品のお問い合わせからプロジェクト全体のご相談まで、デザイン意図、予算、数量、スケジュール、納品先に合わせて必要なリソースを調整します。","caps":[("家具調達","用途、数量、予算、納期に合わせて業務用家具を選定。"),("特注家具開発","寸法、仕上げ、素材、張地、構造をプロジェクト要件に合わせて検討。"),("素材・仕上げ調整","外観、耐久性、メンテナンス、屋内外条件を比較。"),("コスト最適化","デザイン意図を保ちながら構造、数量、梱包、物流を検討。"),("生産・品質調整","図面、サンプル、素材確認、生産進捗、検査要件を調整。"),("物流・配送・設置","必要に応じてコンテナ計画、輸出、現地配送、設置、アフター対応を支援。")],
"support_eye":"WHO WE SUPPORT","support_h":"商業空間を実現するチームのために。","support_intro":"設計、調達、施工、運営を担う皆様の実務に合わせて支援します。","people":["インテリアデザイナー","建築家","飲食事業者","ホテル・リゾート運営者","デベロッパー","元請会社","家具販売店","国際ブランド"],"spaces":["レストラン・カフェ","ホテル・リゾート","屋外・プールサイド","オフィス・研修施設","小売・商業空間","特注プロジェクト環境"],
"presence_eye":"REGIONAL PRESENCE","presence_h":"地域経験に基づく現地調整。","presence":[("台湾での経験","1988年に始まる台湾の家具経験が、素材、構造、業務用家具開発の基盤です。"),("マレーシア運営拠点","プロジェクト調整、調達、現地配送、設置支援、アフターコミュニケーションを担う東南アジア拠点。"),("シンガポール地域オフィス","事業開発、輸出、商業パートナーシップ、越境プロジェクトを支える地域プラットフォーム。")],
"why_eye":"WHY SUNNYWARD","why_h":"実際のプロジェクト条件から考える家具提案。","why":[("商業用途への理解","人流、維持管理、運営、商業環境の要件を考慮。"),("柔軟なソリューション","実現可能な範囲で寸法、仕上げ、張地、素材を調整。"),("プロジェクト調整","製品、生産、配送、現場条件を一体で確認。"),("地域調達の視点","現地調整と地域の供給・製造リソースを組み合わせます。")],
"cta_eye":"START A CONVERSATION","cta_h":"ご要望をお聞かせください。実行可能な家具計画へ整えます。","cta_p":"平面図、家具リスト、参考画像、数量、プロジェクト所在地、希望完了時期をご共有ください。内容を確認し、現実的な次のステップをご提案します。","explore":"製品を見る","image_alt":"Sunnywardの業務用家具プロジェクト現場"
}}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


# Governed 2026-07-20 copy, rebuilt from the BFI Group Business Overview and
# Commercial Furniture & Project Solutions source decks. Keeping this separate
# from the earlier draft makes the approved source transition explicit.
ABOUT_V2 = {
    "en": {
        "html_lang": "en", "short": "EN", "label": "English",
        "nav": ["Home", "About", "Products", "Projects", "Contact"],
        "title": "About Sunnyward | BFI Group Commercial Furniture & Project Solutions",
        "description": "Discover how Sunnyward combines BFI Group manufacturing depth, Japan quality experience and Southeast Asia project execution for commercial furniture solutions.",
        "eyebrow": "ABOUT SUNNYWARD", "hero": "Connecting manufacturing strength with commercial spaces across Asia.",
        "intro": "Sunnyward is BFI Group’s Southeast Asian commercial and project solutions platform, supporting furniture sourcing, customisation and practical execution for hospitality, F&B, office and living environments.",
        "support": "Our shared advantage connects Taiwan and Malaysia manufacturing, Japan quality experience and Southeast Asia market execution.",
        "projects": "View Project Cases", "discuss": "Discuss Your Project", "explore": "Explore Products",
        "story_eye": "OUR EVOLUTION", "story_h": "Built through manufacturing, market knowledge and regional execution.",
        "story_p": ["Our foundation began in Taiwan in 1988 and developed through decades of custom manufacturing and overseas client service, especially for the demanding Japanese market.", "From shop fitting and custom project furniture to Malaysia and Singapore operations, the group has steadily expanded its ability to turn products, capabilities and relationships into scalable opportunities across Asia."],
        "journey_eye": "GLOBAL FOOTPRINT", "journey_h": "One foundation, five practical milestones.",
        "journey": [("1988", "Established in Taiwan", "The manufacturing and export foundation."), ("2000", "Shop fitting expansion", "Store fixtures, display systems and customised project production."), ("2015", "Custom project furniture", "Project-specific furniture capability expanded."), ("2018", "Malaysia office", "A Southeast Asian base for commercial projects and sourcing."), ("2025", "Singapore office", "Regional partnerships and business development expanded.")],
        "ecosystem_eye": "BFI GROUP", "ecosystem_h": "Four business engines, one integrated advantage.",
        "ecosystem": [("Big Fame Industrial Corp", "Manufacturing & Export Foundation", "Store fixtures, display systems, racks, POP stands and customised project manufacturing for overseas clients, including hotel furniture solutions."), ("Vitalsun International Co., Ltd", "Japan Market Entry & Medical Support", "Cross-border coordination, industry understanding and trusted relationships shaped by long-term Japan-market experience and rigorous quality requirements."), ("Sunnyward Sdn Bhd / Pte Ltd", "SEA Commercial & Project Solutions", "Commercial furniture, indoor and outdoor solutions, sourcing and practical project execution across hospitality, F&B, office and living environments."), ("Lifestyle & Brand Business", "Brand Incubation & Retail Distribution", "Retail channels, distribution and brand positioning that turn quality products into scalable lifestyle brands across Asia.")],
        "value_eye": "VALUE THROUGH INTEGRATION", "value_h": "More than product supply.",
        "value_intro": "We connect the right capabilities with the right market opportunities.",
        "value": [("Cross-Border Supply Chain Synergy", "Aligning manufacturing, quality control and timelines across borders for more dependable delivery."), ("Seamless Commercial Execution", "End-to-end furniture and spatial support for hospitality, F&B and mixed-use environments."), ("Strategic Market Entry & Compliance", "Helping overseas partners navigate market requirements and trusted distribution networks across Asia."), ("Brand Incubation & Retail Growth", "Turning quality products into scalable brands through positioning and omnichannel distribution.")],
        "what_eye": "COMMERCIAL SOLUTIONS", "what_h": "Who we help and what we do.",
        "what_intro": "We help brands, developers, designers and operators create better commercial spaces—from product selection and customisation to sourcing and delivery coordination.",
        "caps": [("Commercial Furniture Sourcing", "Indoor and outdoor solutions selected around use, budget, quantity and schedule."), ("Customisation", "Custom-made tables, seating, booth solutions, dimensions, finishes and project-specific requirements."), ("Project Coordination", "Practical execution support across suppliers, production, delivery and site requirements."), ("Taiwan + Malaysia Sourcing", "Cross-border supply flexibility for stronger fit, timing and execution.")],
        "support_eye": "WHO WE SUPPORT", "support_h": "For the teams creating and operating commercial spaces.",
        "support_intro": "Typical settings include hospitality, outdoor leisure, F&B and mixed-use public spaces.",
        "people": ["Developers & Project Owners", "Interior Designers", "Hospitality Operators & Hotels", "F&B Brands, Cafes & Restaurants", "Office & Co-working Operators"],
        "spaces": ["Hospitality", "Outdoor Leisure", "F&B", "Office", "Living Environments", "Mixed-use Public Spaces"],
        "why_eye": "WHY SUNNYWARD", "why_h": "A one-stop partner for furniture, customisation and sourcing coordination.",
        "why": [("One-Stop Solution", "From selection to sourcing, customisation and delivery coordination."), ("Indoor + Outdoor Capability", "Solutions across office, hospitality, F&B and outdoor leisure environments."), ("Customisation", "Practical support when timelines, layout constraints and brand fit all matter."), ("Cross-Border Sourcing", "Taiwan and Malaysia sourcing flexibility for practical execution.")],
        "cases_eye": "SELECTED PROJECT CASES", "cases_h": "Coordination proven in real operating environments.",
        "cases": [("Workers’ Dormitory", "Sleeping, lounge and dining furniture delivered on time through coordinated project execution."), ("NORA’s Cafe", "A mix-and-match dining and lounge concept coordinated across eight suppliers for a unified, timely outcome.")],
        "vision_eye": "AN INTEGRATED GROWTH VISION", "vision_h": "Connecting operational depth with market-facing growth.",
        "vision_p": "We are connecting manufacturing strength, rigorous compliance and commercial execution into a unified, future-ready business platform.",
        "leader": "Jacqueline Hsiao", "leader_role": "Managing Director, Sunnyward Sdn Bhd",
        "cta_h": "Let’s build the next success in Asia together.", "cta_p": "If your organisation is exploring strategic partnerships, cross-border sourcing or integrated commercial project solutions across Asia, we would love to connect.",
        "image_alt": "Sunnyward commercial furniture project installation"
    },
    "tw": {
        "html_lang": "zh-Hant-TW", "short": "繁中", "label": "繁體中文",
        "nav": ["首頁", "關於 Sunnyward", "產品", "案例", "聯絡我們"],
        "title": "關於 Sunnyward｜BFI Group 商業家具與專案解決方案",
        "description": "了解 Sunnyward 如何結合 BFI Group 製造實力、日本品質經驗與東南亞專案執行，提供商業家具與空間解決方案。",
        "eyebrow": "關於 SUNNYWARD", "hero": "連結製造實力，成就亞洲商業空間。",
        "intro": "Sunnyward 是 BFI Group 在東南亞的商業家具與專案解決方案平台，為餐旅、餐飲、辦公與生活空間提供家具採購、客製化與務實的專案執行支援。",
        "support": "我們的共同優勢，來自台灣與馬來西亞的製造能力、日本市場的品質經驗，以及東南亞的商業執行能力。",
        "projects": "查看專案案例", "discuss": "洽談您的專案", "explore": "探索產品",
        "story_eye": "發展歷程", "story_h": "由製造、跨境市場經驗與區域執行能力共同累積。",
        "story_p": ["集團基礎始於 1988 年的台灣，透過數十年的客製製造與海外客戶服務，尤其是日本市場的高標準要求，建立深厚的實務能力。", "從店舖設備、客製專案家具，到馬來西亞與新加坡據點，我們持續將產品、能力與商業關係轉化為亞洲市場可持續發展的機會。"],
        "journey_eye": "全球布局", "journey_h": "一個基礎，五個關鍵里程碑。",
        "journey": [("1988", "台灣成立", "建立製造與出口基礎。"), ("2000", "拓展店舖設備", "發展展示系統、貨架與客製專案製造。"), ("2015", "客製專案家具", "強化依專案需求開發家具的能力。"), ("2018", "設立馬來西亞辦公室", "建立東南亞商業專案與採購據點。"), ("2025", "設立新加坡辦公室", "拓展區域合作與商業開發。")],
        "ecosystem_eye": "BFI GROUP", "ecosystem_h": "四大事業引擎，一個整合優勢。",
        "ecosystem": [("Big Fame Industrial Corp", "製造與出口基礎", "為海外客戶提供店舖設備、展示系統、貨架、POP 展示架、客製專案製造與飯店家具方案。"), ("Vitalsun International Co., Ltd", "日本市場進入與醫療事業支援", "長期日本市場經驗所累積的跨境協調、產業理解、信任關係與嚴謹品質要求。"), ("Sunnyward Sdn Bhd / Pte Ltd", "東南亞商業家具與專案方案", "為餐旅、餐飲、辦公與生活環境提供室內外商業家具、採購及務實的專案執行。"), ("生活風格與品牌事業", "品牌孵化與零售通路", "透過零售、經銷與品牌定位，將優質產品發展為亞洲市場具規模的生活品牌。")],
        "value_eye": "整合創造價值", "value_h": "不只是供應產品。",
        "value_intro": "我們將正確的能力，連結到正確的市場機會。",
        "value": [("跨境供應鏈協同", "整合製造、品質管理與跨境時程，提高交付的可靠性。"), ("完整商業執行", "為餐旅、餐飲與複合式環境提供端到端家具及空間支援。"), ("策略性市場進入與合規", "協助海外夥伴理解市場要求並連結亞洲可信賴的通路網絡。"), ("品牌孵化與零售成長", "透過定位與全通路經營，將優質產品發展為可規模化品牌。")],
        "what_eye": "商業空間解決方案", "what_h": "我們服務誰，以及我們做什麼。",
        "what_intro": "我們協助品牌、開發商、設計師與營運者打造更好的商業空間，從產品選擇、客製化到採購及交付協調。",
        "caps": [("商業家具採購", "依用途、預算、數量與時程選擇室內外家具方案。"), ("客製化支援", "提供訂製桌台、座椅、卡座、尺寸、表面處理及專案特殊需求。"), ("專案協調", "協調多方供應商、生產、交付與現場條件，提供務實執行支援。"), ("台灣＋馬來西亞採購", "透過跨境供應彈性，改善適配度、時程與執行效率。")],
        "support_eye": "服務對象", "support_h": "為創造並營運商業空間的團隊而設。",
        "support_intro": "典型場域包括餐旅、戶外休閒、餐飲及複合式公共空間。",
        "people": ["開發商與專案業主", "室內設計師", "餐旅業者與飯店", "餐飲品牌、咖啡館與餐廳", "辦公室與共享空間營運者"],
        "spaces": ["餐旅空間", "戶外休閒", "餐飲空間", "辦公空間", "生活環境", "複合式公共空間"],
        "why_eye": "為何選擇 SUNNYWARD", "why_h": "家具、客製化與採購協調的一站式夥伴。",
        "why": [("一站式方案", "從選品、採購、客製化到交付協調。"), ("室內＋戶外能力", "涵蓋辦公、餐旅、餐飲及戶外休閒環境。"), ("客製化", "在時程、格局限制與品牌契合度都重要時提供務實支援。"), ("跨境採購", "結合台灣與馬來西亞採購彈性，強化專案執行。")],
        "cases_eye": "代表專案", "cases_h": "在真實營運場域中驗證的協調能力。",
        "cases": [("員工宿舍", "整合睡眠、休憩與用餐家具，透過專案協調如期完成交付。"), ("NORA’s Cafe", "跨八家供應商協調餐飲與休憩家具，準時完成風格一致的空間成果。")],
        "vision_eye": "整合成長願景", "vision_h": "連結營運深度與市場成長。",
        "vision_p": "我們正把製造實力、嚴謹合規與商業執行連結成一個整合、面向未來的商業平台。",
        "leader": "Jacqueline Hsiao", "leader_role": "Sunnyward Sdn Bhd 董事總經理",
        "cta_h": "讓我們一起打造下一個亞洲成功案例。", "cta_p": "若您的組織正在探索策略合作、跨境採購或亞洲整合型商業專案方案，歡迎與我們聯繫。",
        "image_alt": "Sunnyward 商業家具專案現場"
    },
    "jp": {
        "html_lang": "ja", "short": "日本語", "label": "日本語",
        "nav": ["ホーム", "Sunnywardについて", "製品", "導入事例", "お問い合わせ"],
        "title": "Sunnywardについて｜BFI Group 業務用家具・プロジェクトソリューション",
        "description": "BFI Groupの製造力、日本市場で培った品質経験、東南アジアでの実行力を結ぶSunnywardの業務用家具ソリューションをご紹介します。",
        "eyebrow": "ABOUT SUNNYWARD", "hero": "製造力を、アジアの商業空間へ。",
        "intro": "Sunnywardは、BFI Groupの東南アジアにおける業務用家具・プロジェクトソリューション拠点です。ホテル、飲食、オフィス、住環境に向けて、調達、カスタマイズ、実務的なプロジェクト支援を提供します。",
        "support": "台湾・マレーシアの製造力、日本市場で培った品質経験、東南アジアでの商業実行力を結びつけます。",
        "projects": "導入事例を見る", "discuss": "プロジェクトを相談する", "explore": "製品を見る",
        "story_eye": "OUR EVOLUTION", "story_h": "製造、市場理解、地域での実行力を積み重ねて。",
        "story_p": ["グループの基盤は1988年に台湾で始まりました。数十年にわたる特注製造と海外顧客対応、特に厳しい基準を持つ日本市場での経験を通じて、実務力を培ってきました。", "店舗什器、特注プロジェクト家具からマレーシア・シンガポール拠点へと発展し、製品、能力、関係性をアジアで拡張可能な事業機会へつなげています。"],
        "journey_eye": "GLOBAL FOOTPRINT", "journey_h": "一つの基盤、五つの節目。",
        "journey": [("1988", "台湾で設立", "製造・輸出の基盤を構築。"), ("2000", "店舗什器事業へ拡大", "什器、ディスプレイ、特注製造を展開。"), ("2015", "特注プロジェクト家具", "案件別の家具開発力を強化。"), ("2018", "マレーシア事務所", "東南アジアの商業案件と調達拠点を設置。"), ("2025", "シンガポール事務所", "地域連携と事業開発を拡大。")],
        "ecosystem_eye": "BFI GROUP", "ecosystem_h": "四つの事業エンジン、一つの統合力。",
        "ecosystem": [("Big Fame Industrial Corp", "製造・輸出基盤", "海外顧客向けに店舗什器、ディスプレイ、ラック、POP、特注製造、ホテル家具ソリューションを提供。"), ("Vitalsun International Co., Ltd", "日本市場参入・医療事業支援", "長年の日本市場経験から得た越境調整、業界理解、信頼関係、厳格な品質要求への対応。"), ("Sunnyward Sdn Bhd / Pte Ltd", "東南アジア商業・プロジェクトソリューション", "ホテル、飲食、オフィス、住環境に向けた屋内外家具、調達、実務的なプロジェクト遂行。"), ("ライフスタイル・ブランド事業", "ブランド育成・小売流通", "小売、流通、ブランドポジショニングを通じ、優れた製品をアジアで成長するブランドへ。")],
        "value_eye": "VALUE THROUGH INTEGRATION", "value_h": "製品供給の、その先へ。",
        "value_intro": "適切な能力と市場機会を結び、価値を生み出します。",
        "value": [("越境サプライチェーン連携", "製造、品質、国境を越えた工程を統合し、納品の確実性を高めます。"), ("一貫した商業実行", "ホテル、飲食、複合施設に家具・空間を一貫して支援。"), ("市場参入・コンプライアンス", "市場要件への対応と信頼できるアジアの流通網を支援。"), ("ブランド育成・小売成長", "ポジショニングと多面的な販売により製品を成長ブランドへ。")],
        "what_eye": "COMMERCIAL SOLUTIONS", "what_h": "支援するお客様と、提供すること。",
        "what_intro": "ブランド、デベロッパー、デザイナー、運営者に向け、製品選定・カスタマイズから調達・納品調整まで商業空間づくりを支援します。",
        "caps": [("業務用家具調達", "用途、予算、数量、工程に合わせた屋内外家具。"), ("カスタマイズ", "テーブル、座席、ボックス席、寸法、仕上げなど案件別要件に対応。"), ("プロジェクト調整", "複数サプライヤー、生産、納品、現場条件を実務的に調整。"), ("台湾＋マレーシア調達", "越境調達の柔軟性で適合性、納期、実行力を向上。")],
        "support_eye": "WHO WE SUPPORT", "support_h": "商業空間をつくり、運営するチームのために。",
        "support_intro": "主な対象はホテル、屋外レジャー、飲食、複合公共空間です。",
        "people": ["デベロッパー・事業主", "インテリアデザイナー", "ホテル・宿泊事業者", "飲食ブランド・カフェ・レストラン", "オフィス・コワーキング運営者"],
        "spaces": ["ホテル・宿泊", "屋外レジャー", "飲食", "オフィス", "住環境", "複合公共空間"],
        "why_eye": "WHY SUNNYWARD", "why_h": "家具、カスタマイズ、調達調整のワンストップパートナー。",
        "why": [("ワンストップ", "選定、調達、カスタマイズ、納品調整まで。"), ("屋内＋屋外", "オフィス、ホテル、飲食、屋外レジャーに対応。"), ("カスタマイズ", "納期、レイアウト、ブランドとの調和を考えた実務支援。"), ("越境調達", "台湾とマレーシアの調達柔軟性を活用。")],
        "cases_eye": "SELECTED PROJECT CASES", "cases_h": "実際の運営環境で証明された調整力。",
        "cases": [("従業員宿舎", "寝室、ラウンジ、食堂家具を調整し、計画どおり納品。"), ("NORA’s Cafe", "8社のサプライヤーを調整し、統一感ある飲食・ラウンジ空間を予定どおり実現。")],
        "vision_eye": "AN INTEGRATED GROWTH VISION", "vision_h": "オペレーションの深さを、市場の成長へ。",
        "vision_p": "製造力、厳格なコンプライアンス、商業実行力を、未来に向けた統合型事業プラットフォームへつなげます。",
        "leader": "Jacqueline Hsiao", "leader_role": "Managing Director, Sunnyward Sdn Bhd",
        "cta_h": "アジアで、次の成功をともに。", "cta_p": "戦略的提携、越境調達、アジアでの統合型商業プロジェクトをご検討の際は、ぜひご相談ください。",
        "image_alt": "Sunnywardの業務用家具プロジェクト現場"
    }
}


def cards(items: list[tuple[str, str]], class_name: str) -> str:
    return "".join(f'<article class="{class_name} reveal"><h3>{esc(title)}</h3><p>{esc(body)}</p></article>' for title, body in items)


def render(lang: str, c: dict) -> str:
    c = ABOUT_V2[lang]
    paths = ("index.html","about.html","products.html","projects.html","contact.html")
    nav = "".join(f'<li><a href="{path}" class="nav-link{" active" if path == "about.html" else ""}">{esc(label)}</a></li>' for path, label in zip(paths, c["nav"], strict=True))
    mobile = "".join(f'<a href="{path}" class="nav-link{" active" if path == "about.html" else ""}">{esc(label)}</a>' for path, label in zip(paths, c["nav"], strict=True))
    language_codes = {"en": "en", "tw": "zh-TW", "jp": "ja"}
    lang_links = "".join(f'<li class="lang-item"><a href="../{folder}/about.html" class="lang-dropdown-item{" active" if folder == lang else ""}" data-lang="{folder}" lang="{language_codes[folder]}">{esc(ABOUT_V2[folder]["label"])}</a></li>' for folder in ABOUT_V2)
    timeline = "".join(f'<article class="about-journey__item reveal"><span class="about-journey__year">{esc(year)}</span><div><h3>{esc(title)}</h3><p>{esc(body)}</p></div></article>' for year,title,body in c["journey"])
    people = "".join(f'<li>{esc(item)}</li>' for item in c["people"])
    spaces = "".join(f'<li>{esc(item)}</li>' for item in c["spaces"])
    story = "".join(f'<p>{esc(p)}</p>' for p in c["story_p"])
    ecosystem = "".join(f'<article class="about-ecosystem__item reveal"><h3>{esc(name)}</h3><strong>{esc(role)}</strong><p>{esc(body)}</p></article>' for name, role, body in c["ecosystem"])
    cases = "".join(f'<article class="about-case reveal"><h3>{esc(title)}</h3><p>{esc(body)}</p></article>' for title, body in c["cases"])
    footer = render_public_footer(lang, prefix="")
    schema = json.dumps(organization_schema(), ensure_ascii=False, separators=(",",":"))
    return f'''<!DOCTYPE html>
<html lang="{c['html_lang']}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(c['title'])}</title><meta name="description" content="{esc(c['description'])}"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="{public_url(f'{lang}/about.html')}"><link rel="alternate" hreflang="x-default" href="{public_url('en/about.html')}"><link rel="alternate" hreflang="en" href="{public_url('en/about.html')}"><link rel="alternate" hreflang="zh-TW" href="{public_url('tw/about.html')}"><link rel="alternate" hreflang="ja" href="{public_url('jp/about.html')}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Sunnyward"><meta property="og:title" content="{esc(c['title'])}"><meta property="og:description" content="{esc(c['description'])}"><meta property="og:url" content="{public_url(f'{lang}/about.html')}"><meta property="og:image" content="{public_url(HERO)}"><meta property="og:image:alt" content="{esc(c['image_alt'])}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(c['title'])}"><meta name="twitter:description" content="{esc(c['description'])}"><meta name="twitter:image" content="{public_url(HERO)}">
<link rel="stylesheet" href="../css/style.css?v=20260716-about"><script type="application/ld+json">{schema}</script></head><body>
<header id="site-header" class="nav-transparent"><div class="nav-container"><a href="index.html" class="logo">SUNNYWARD<span>.</span></a><button class="mobile-nav-toggle" id="mobile-toggle" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button><ul class="nav-menu">{nav}</ul><div class="nav-actions"><div class="lang-dropdown"><button type="button" class="lang-current" aria-label="Select language">{esc(c['short'])} ↓</button><ul class="lang-list">{lang_links}</ul></div></div></div></header>
<nav class="mobile-drawer" id="mobile-drawer">{mobile}</nav>
<main class="about-page"><section class="about-hero"><img src="../{HERO}" alt="{esc(c['image_alt'])}" width="846" height="504" loading="eager" fetchpriority="high"><div class="about-hero__overlay"></div><div class="container about-hero__content reveal"><span class="eyebrow">{esc(c['eyebrow'])}</span><h1>{esc(c['hero'])}</h1><p>{esc(c['intro'])}</p><p class="about-hero__support">{esc(c['support'])}</p><div class="about-actions"><a class="btn btn-primary" href="projects.html">{esc(c['projects'])}</a><a class="btn btn-ghost" href="contact.html">{esc(c['discuss'])}</a></div></div></section>
<section class="section about-story"><div class="container about-story__grid"><div class="about-story__copy reveal"><span class="eyebrow">{esc(c['story_eye'])}</span><h2>{esc(c['story_h'])}</h2>{story}</div><figure class="about-story__media reveal"><img src="../{STORY}" alt="{esc(c['image_alt'])}" width="800" height="800" loading="lazy"></figure></div></section>
<section class="section section--tint about-journey"><div class="container"><header class="about-section-heading reveal"><span class="eyebrow">{esc(c['journey_eye'])}</span><h2>{esc(c['journey_h'])}</h2></header><div class="about-journey__line about-journey__line--five">{timeline}</div></div></section>
<section class="section about-ecosystem"><div class="container"><header class="about-section-heading reveal"><span class="eyebrow">{esc(c['ecosystem_eye'])}</span><h2>{esc(c['ecosystem_h'])}</h2></header><div class="about-ecosystem__grid">{ecosystem}</div></div></section>
<section class="section section--dark about-value"><div class="container"><header class="about-section-heading reveal"><span class="eyebrow">{esc(c['value_eye'])}</span><h2>{esc(c['value_h'])}</h2><p>{esc(c['value_intro'])}</p></header><div class="about-value__grid">{cards(c['value'],'about-value__item')}</div></div></section>
<section class="section about-work"><div class="container"><header class="about-section-heading reveal"><span class="eyebrow">{esc(c['what_eye'])}</span><h2>{esc(c['what_h'])}</h2><p>{esc(c['what_intro'])}</p></header><div class="about-work__grid">{cards(c['caps'],'about-work__item')}</div></div></section>
<section class="section section--dark about-audience"><div class="container"><header class="about-section-heading reveal"><span class="eyebrow">{esc(c['support_eye'])}</span><h2>{esc(c['support_h'])}</h2><p>{esc(c['support_intro'])}</p></header><div class="about-audience__groups reveal"><ul>{people}</ul><ul class="about-audience__spaces">{spaces}</ul></div></div></section>
<section class="section section--tint about-why"><div class="container"><header class="about-section-heading reveal"><span class="eyebrow">{esc(c['why_eye'])}</span><h2>{esc(c['why_h'])}</h2></header><div class="about-why__grid">{cards(c['why'],'about-why__item')}</div></div></section>
<section class="section about-cases"><div class="container"><header class="about-section-heading reveal"><span class="eyebrow">{esc(c['cases_eye'])}</span><h2>{esc(c['cases_h'])}</h2></header><div class="about-cases__grid">{cases}</div><div class="about-actions reveal"><a class="btn btn-primary" href="projects.html">{esc(c['projects'])}</a></div></div></section>
<section class="section section--tint about-vision"><div class="container about-vision__grid"><figure class="about-story__media reveal"><img src="../{STORY}" alt="{esc(c['image_alt'])}" width="800" height="800" loading="lazy"></figure><div class="reveal"><span class="eyebrow">{esc(c['vision_eye'])}</span><h2>{esc(c['vision_h'])}</h2><p>{esc(c['vision_p'])}</p><strong>{esc(c['leader'])}</strong><span>{esc(c['leader_role'])}</span></div></div></section>
<section class="about-closing"><div class="container reveal"><h2>{esc(c['cta_h'])}</h2><p>{esc(c['cta_p'])}</p><div class="about-actions"><a class="btn btn-primary" href="contact.html">{esc(c['discuss'])}</a><a class="btn btn-ghost" href="products.html">{esc(c['explore'])}</a></div></div></section></main>
{footer}<script src="../js/main.js?v=20260716-about"></script></body></html>'''


def main() -> None:
    for lang, copy in ABOUT_V2.items():
        (ROOT / lang / "about.html").write_text(render(lang, copy), encoding="utf-8", newline="\n")
    print("Generated three governed About pages.")


if __name__ == "__main__":
    main()
