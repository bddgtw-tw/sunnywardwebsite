import os
import re

cases_data = {
    'en': [
        {
            'id': 'case-hotel-fb',
            'space': 'fb', 'product': 'chair',
            'meta': 'HOTEL F&B - JOHOR',
            'title': 'Elevating the Hotel Dining Experience',
            'video': '2026.01_kai_restaurant.mp4',
            'base_img': '486466926_1193879656080876_2767098548785792068_n',
            'challenge': 'Hotel F&B areas often struggle with outdated seating that ruins the premium dining atmosphere expected by high-paying guests.',
            'solution': 'By introducing cohesive, commercial-grade furniture, the hotel instantly upgraded its ambiance, leading to increased guest satisfaction.',
            'difference': 'We provide aesthetic alignment combined with extreme durability required for high-traffic hospitality.',
            'quote': '"Sunnyward revitalized our dining area. The premium feel matches our 5-star standard, yet they are incredibly easy to maintain."',
            'author': 'F&B Director', 'company': 'Luxury Hotel, Johor'
        },
        {
            'id': 'case-woodfire',
            'space': 'fb', 'product': 'chair',
            'meta': 'FAST CASUAL - PASIR GUDANG',
            'title': 'Built for High Traffic (Woodfire)',
            'video': '2024.01_family_restaurant.mp4',
            'base_img': '485005693_1188406983294810_676741634435601911_n',
            'challenge': 'Fast casual spaces face immense daily wear. Cold stainless steel setups felt uninviting and deterred customers.',
            'solution': 'Our impact-resistant tables and chairs created a warm, inviting destination while withstanding relentless use.',
            'difference': 'Engineered for rapid cleaning cycles without compromising visual warmth and comfort.',
            'quote': '"We need furniture that can take a beating but still look great. Sunnyward delivered exactly that."',
            'author': 'Operations Manager', 'company': 'Woodfire Pasir Gudang'
        },
        {
            'id': 'case-toastmaster',
            'space': 'office', 'product': 'chair',
            'meta': 'CORPORATE LEARNING - JOHOR',
            'title': 'Inspiring Educational Spaces',
            'video': '2024.11_tsutaya_bookstore.mp4',
            'base_img': '486540137_1194648809337294_8428044945485451315_n',
            'challenge': 'Rigid conference furniture creates a stiff environment that drains participant energy during long sessions.',
            'solution': 'Vibrant, ergonomic seating energized the room, promoting better focus and engagement during intensive courses.',
            'difference': 'We balance vivid aesthetics with stackable, easy-to-store utility for multi-purpose event spaces.',
            'quote': '"Since upgrading our training rooms, we\'ve seen a tangible increase in participant engagement."',
            'author': 'Facilities Director', 'company': 'Toast Master International'
        },
        {
            'id': 'case-massage',
            'space': 'wellness', 'product': 'sofa',
            'meta': 'WELLNESS SPA - KUALA LUMPUR',
            'title': 'Crafting Zen Retreats',
            'video': '2024.05_dragon_ginseng.mp4',
            'base_img': '487230012_1197042165764625_5235377330861897247_n',
            'challenge': 'A disorganized waiting area fails to put guests in a state of relaxation upon arrival.',
            'solution': 'Solid wood lounge sets instantly created a grounding, Zen atmosphere that calms guests.',
            'difference': 'Our solid timber selections provide reassuring sturdiness that synthetic alternatives cannot match.',
            'quote': '"The moment our clients sit in the waiting lounge, they begin to relax. The quality is exceptional."',
            'author': 'Spa Founder', 'company': 'Bukit Bintang Thai Massage'
        },
        {
            'id': 'case-ampang-cafe',
            'space': 'fb', 'product': 'sofa',
            'meta': 'BOUTIQUE CAFE - AMPANG',
            'title': 'Designing the Perfect Coffee Corner',
            'video': '2025.10_ampang_cafe.mp4',
            'base_img': '487987172_1203941861741322_5531705742715616204_n',
            'challenge': 'Creating a cozy yet highly durable cafe interior is difficult when relying on standard residential furniture.',
            'solution': 'We customized compact, stylish cafe tables and plush seating that maximizes space without sacrificing comfort.',
            'difference': 'Tailored dimensions combined with commercial upholstery ensure longevity in a spill-prone environment.',
            'quote': '"Our cafe feels twice as spacious, and customers frequently compliment the comfort of the chairs."',
            'author': 'Cafe Owner', 'company': 'Ampang Artisan Coffee'
        },
        {
            'id': 'case-sushi-plus',
            'space': 'fb', 'product': 'chair',
            'meta': 'HIGH TURNOVER - SUSHI PLUS',
            'title': 'Efficiency Meets Modern Aesthetics',
            'video': '2026.06_sushi_plus_outlet.mp4',
            'base_img': '488205633_1206283328173842_1752346583025989446_n',
            'challenge': 'Sushi restaurants require furniture that allows for rapid turnaround times and frequent wiping without fading.',
            'solution': 'We deployed easy-wipe, stain-resistant booth seating that complements the minimalist Japanese interior design.',
            'difference': 'Advanced material science applied to contract furniture, ensuring zero stain absorption over years of use.',
            'quote': '"The turnover speed increased because cleaning is effortless. Plus, the minimalist design is stunning."',
            'author': 'Branch Manager', 'company': 'Sushi Plus Outlet'
        },
        {
            'id': 'case-noodles',
            'space': 'fb', 'product': 'chair',
            'meta': 'TRADITIONAL DINING - LOCAL EATERY',
            'title': 'Reviving Traditional Eateries',
            'video': '2024.04_noodles_restaurant.mp4',
            'base_img': '488538040_1204903331645175_5225319039366592359_n',
            'challenge': 'Local eateries often rely on flimsy plastic chairs that break easily and look unappealing.',
            'solution': 'We introduced robust, wood-finish metal chairs that preserve the traditional vibe but offer ten times the lifespan.',
            'difference': 'A perfect fusion of nostalgic aesthetics and unbreakable modern engineering.',
            'quote': '"We haven\'t had to replace a single chair in two years. It was the best investment for our restaurant."',
            'author': 'Restaurant Owner', 'company': 'Heritage Noodles Hub'
        },
        {
            'id': 'case-office-outdoor',
            'space': 'office', 'product': 'outdoor',
            'meta': 'CORPORATE OUTDOOR - HEADQUARTERS',
            'title': 'Inspiring Open-Air Workspaces',
            'video': '2024.01_office_outdoor_area.mp4',
            'base_img': '488656602_1204138475054994_4966483650098909681_n',
            'challenge': 'Corporate outdoor patios quickly degrade under sun and rain, making them unusable for employees.',
            'solution': 'Our UV-resistant, weatherproof outdoor lounge sets transformed the patio into a favorite meeting spot.',
            'difference': 'Marine-grade materials guarantee that the furniture will not fade, rust, or warp under extreme weather.',
            'quote': '"Our employees love having meetings outside now. The furniture still looks brand new despite the harsh sun."',
            'author': 'HR Director', 'company': 'Tech Corp HQ'
        },
        {
            'id': 'case-legoland-cafe',
            'space': 'fb', 'product': 'chair',
            'meta': 'THEME PARK DINING - LEGOLAND',
            'title': 'Vibrant & Indestructible Cafeterias',
            'video': '2025.12_legoland_cafeteria.mp4',
            'base_img': '489433395_1207544954714346_7387054704136033221_n',
            'challenge': 'Theme park cafeterias face extreme abuse from thousands of families daily. Safety and color retention are paramount.',
            'solution': 'We installed heavy-duty, vibrant seating with rounded edges, ensuring safety for children and easy maintenance for staff.',
            'difference': 'Color-infused polymers ensure that scratches do not show, maintaining a playful, vibrant look indefinitely.',
            'quote': '"Safety and durability are our top priorities. Sunnyward’s furniture exceeded our strict standards."',
            'author': 'Procurement Head', 'company': 'Legoland Theme Park'
        },
        {
            'id': 'case-waterpark',
            'space': 'public', 'product': 'outdoor',
            'meta': 'RESORT POOLSIDE - LL WATERPARK',
            'title': 'Luxury Resort Lounging',
            'video': '2025.05_ll_waterpark.mp4',
            'base_img': '490092252_1209480437854131_9119969951171433752_n',
            'challenge': 'Poolside loungers constantly suffer from chlorine damage, mold, and broken reclining mechanisms.',
            'solution': 'We supplied premium, quick-dry sunbeds with non-corrosive frames, elevating the resort\'s luxury feel.',
            'difference': 'Breathable mesh fabrics and rust-proof aluminum frames drastically reduce maintenance costs.',
            'quote': '"The loungers are the highlight of our pool area. They look incredibly luxurious and are very comfortable."',
            'author': 'Resort Manager', 'company': 'LL Waterpark Resort'
        }
    ]
}

cases_data['tw'] = [
    {
        'id': 'case-hotel-fb',
        'space': 'fb', 'product': 'chair',
        'meta': '飯店餐飲空間 - 柔佛 (HOTEL F&B)',
        'title': '重塑頂級用餐體驗',
        'video': '2026.01_kai_restaurant.mp4',
        'base_img': '486466926_1193879656080876_2767098548785792068_n',
        'challenge': '飯店的餐飲區域常面臨家具老舊、風格不一致的問題，嚴重破壞高級用餐氣氛與品牌價值。',
        'solution': '我們為其導入了具備高質感的統一家具風格，瞬間提升整體空間格調，帶動翻桌率與顧客回訪率。',
        'difference': '我們不只是賣椅子，而是提供完美契合飯店品牌形象，且具備「商用級高強度耐用度」的全方位解決方案。',
        'quote': '「Sunnyward 徹底為我們的餐廳注入了新生命。家具的高級質感完美符合我們的五星級標準。」',
        'author': '餐飲部總監', 'company': '柔佛頂級飯店'
    },
    {
        'id': 'case-woodfire',
        'space': 'fb', 'product': 'chair',
        'meta': '高人氣快餐品牌 (WOODFIRE)',
        'title': '專為高客流量量身打造',
        'video': '2024.01_family_restaurant.mp4',
        'base_img': '485005693_1188406983294810_676741634435601911_n',
        'challenge': '高人氣快餐店面臨極大的家具耗損。傳統冰冷的不鏽鋼桌椅讓人感到有距離感。',
        'solution': '透過溫潤木質調與極度耐用、抗衝擊的座椅，我們將快節奏的餐廳轉化為充滿吸引力的用餐目的地。',
        'difference': '我們的家具專為高人流環境設計，不僅設計精美，更具備快速清潔的極致實用性。',
        'quote': '「我們需要的是耐操又能兼顧 IG 打卡美感的家具。Sunnyward 完全做到了！」',
        'author': '營運經理', 'company': 'Woodfire Pasir Gudang'
    },
    {
        'id': 'case-toastmaster',
        'space': 'office', 'product': 'chair',
        'meta': '企業與教育培訓空間 (TOAST MASTER)',
        'title': '激發學習與交流靈感',
        'video': '2024.11_tsutaya_bookstore.mp4',
        'base_img': '486540137_1194648809337294_8428044945485451315_n',
        'challenge': '制式且僵硬的會議家具容易讓學習環境顯得死板，迅速消耗參與者的能量與專注力。',
        'solution': '色彩鮮明、符合人體工學的座椅活化了空間氛圍，有效改善坐姿，提升學員的專注力。',
        'difference': '我們將活潑美學與「可堆疊、易收納」的實用性完美結合，是多功能活動空間的最佳選擇。',
        'quote': '「升級培訓室後，我們明顯感受到學員參與度的提升。這批座椅在全天候工作坊中提供極佳支撐。」',
        'author': '設施管理總監', 'company': 'Toast Master International'
    },
    {
        'id': 'case-massage',
        'space': 'wellness', 'product': 'sofa',
        'meta': '頂級舒壓養生館 - 武吉免登',
        'title': '營造極致放鬆的禪意空間',
        'video': '2024.05_dragon_ginseng.mp4',
        'base_img': '487230012_1197042165764625_5235377330861897247_n',
        'challenge': '雜亂或使用輕薄廉價座椅的等候區，無法讓顧客一進門就卸下心防進入放鬆狀態。',
        'solution': '原木休閒沙發組瞬間營造出充滿禪意的沉穩氛圍，讓顧客在等待當下就開始享受頂級體驗。',
        'difference': '我們嚴選的實木材質不仅提供穩固感，更帶來廉價合成材質無法比擬的自然溫潤。',
        'quote': '「當客戶坐在等候區沙發時，他們就已經開始放鬆了。原木品質完美契合我們的養生理念。」',
        'author': '養生館創辦人', 'company': '武吉免登泰式按摩'
    },
    {
        'id': 'case-ampang-cafe',
        'space': 'fb', 'product': 'sofa',
        'meta': '精品咖啡廳 - 安邦 (AMPANG)',
        'title': '打造完美的咖啡角落',
        'video': '2025.10_ampang_cafe.mp4',
        'base_img': '487987172_1203941861741322_5531705742715616204_n',
        'challenge': '一般的居家家具無法承受咖啡廳頻繁的翻桌與液體潑灑，且難以有效利用有限的空間。',
        'solution': '我們客製了緊湊且時尚的咖啡桌與絨布座椅，在不犧牲舒適度的前提下最大化空間利用率。',
        'difference': '商用級防潑水布料與量身打造的尺寸，確保在極易弄髒的環境下依然常保如新。',
        'quote': '「我們的咖啡廳看起來寬敞了一倍，而且客人總是誇獎我們的椅子非常好坐。」',
        'author': '咖啡廳負責人', 'company': 'Ampang Artisan Coffee'
    },
    {
        'id': 'case-sushi-plus',
        'space': 'fb', 'product': 'chair',
        'meta': '高翻桌率餐飲 - 壽司加 (SUSHI PLUS)',
        'title': '高效率與現代美學的結合',
        'video': '2026.06_sushi_plus_outlet.mp4',
        'base_img': '488205633_1206283328173842_1752346583025989446_n',
        'challenge': '壽司餐廳需要能快速清潔的家具，且不能因為頻繁擦拭而導致表面掉色或磨損。',
        'solution': '我們導入了易擦拭、防污漬的卡座沙發，完美融入日式極簡的室內設計風格。',
        'difference': '將先進材料科學應用於商用家具，確保多年高強度使用下依然零污漬殘留。',
        'quote': '「新店鋪的翻桌速度變快了，因為卡座極好清潔。極簡的日式卡座設計很有質感。」',
        'author': '分店經理', 'company': 'Sushi Plus Outlet'
    },
    {
        'id': 'case-noodles',
        'space': 'fb', 'product': 'chair',
        'meta': '傳統在地餐館 - 麵食館',
        'title': '傳統餐館的質感升級',
        'video': '2024.04_noodles_restaurant.mp4',
        'base_img': '488538040_1204903331645175_5225319039366592359_n',
        'challenge': '許多在地小吃店依賴容易斷裂且不美觀的塑膠椅，不僅危險也拉低了店面質感。',
        'solution': '我們引入了擁有原木質感的堅固金屬餐椅，保留了傳統親切的氛圍，但壽命延長了十倍。',
        'difference': '完美融合了復古情懷的美學與現代無堅不摧的工業工程設計。',
        'quote': '「這兩年來我們沒換過半張椅子，這是我們為餐廳做過最棒的投資。」',
        'author': '餐廳老闆', 'company': '傳承麵食館'
    },
    {
        'id': 'case-office-outdoor',
        'space': 'office', 'product': 'outdoor',
        'meta': '企業總部戶外辦公區',
        'title': '激發靈感的露天工作區',
        'video': '2024.01_office_outdoor_area.mp4',
        'base_img': '488656602_1204138475054994_4966483650098909681_n',
        'challenge': '企業的戶外露台家具在日曬雨淋下容易迅速劣化，導致員工不願使用這些空間。',
        'solution': '我們提供抗紫外線、全天候防水的戶外休閒組，將閒置露台轉變為員工最愛的討論區。',
        'difference': '採用航海級防腐材質，保證在極端氣候下不褪色、不生鏽、不變形。',
        'quote': '「員工現在超愛在戶外開會。儘管每天日曬，家具看起來還是像新的一樣。」',
        'author': '人資總監', 'company': '跨國科技企業總部'
    },
    {
        'id': 'case-legoland-cafe',
        'space': 'fb', 'product': 'chair',
        'meta': '主題樂園餐廳 - 樂高樂園',
        'title': '充滿活力且堅不可摧',
        'video': '2025.12_legoland_cafeteria.mp4',
        'base_img': '489433395_1207544954714346_7387054704136033221_n',
        'challenge': '主題樂園餐廳每天要面對成千上萬家庭的「摧殘」，安全性與色彩持久度是首要考量。',
        'solution': '我們安裝了重型且色彩繽紛的圓角座椅，確保孩童安全，同時讓清潔團隊能快速整理。',
        'difference': '獨家注色聚合物技術，刮痕不顯眼，能永久保持充滿活力的視覺效果。',
        'quote': '「安全與耐用是我們的最高原則。Sunnyward 的家具遠超我們嚴苛的標準。」',
        'author': '採購主管', 'company': '樂高樂園 (Legoland)'
    },
    {
        'id': 'case-waterpark',
        'space': 'public', 'product': 'outdoor',
        'meta': '度假村池畔 - LL 水上樂園',
        'title': '奢華的渡假村躺椅體驗',
        'video': '2025.05_ll_waterpark.mp4',
        'base_img': '490092252_1209480437854131_9119969951171433752_n',
        'challenge': '泳池邊的躺椅常因氯水侵蝕而生鏽、發霉，或是傾斜機械結構容易故障。',
        'solution': '我們提供了頂級快乾網布躺椅搭配防腐蝕框架，大幅提升了度假村的奢華度假感。',
        'difference': '透氣抗UV網布與防鏽鋁合金框架，為業者省下巨額的維護與汰換成本。',
        'quote': '「這批躺椅是我們泳池區的最大亮點。看起來極度奢華，而且客人回饋非常舒適。」',
        'author': '度假村經理', 'company': 'LL 水上樂園度假村'
    }
]

cases_data['jp'] = cases_data['en']

filter_strings = {
    'en': {
        'all': 'All Spaces',
        'fb': 'Dining / F&B',
        'office': 'Office & Training',
        'wellness': 'Spa & Wellness',
        'public': 'Resort & Public',
        'all_p': 'All Furniture',
        'chair': 'Contract Chairs',
        'sofa': 'Sofas & Lounges',
        'outdoor': 'Outdoor Collections',
        'heading': 'Global Project Realizations',
        'desc': 'A meticulous overview of how we solve complex space and furniture challenges across 10 commercial projects globally.'
    },
    'tw': {
        'all': '所有空間',
        'fb': '餐飲空間',
        'office': '辦公與教育',
        'wellness': '舒壓養生',
        'public': '渡假與公共',
        'all_p': '所有家具',
        'chair': '商用椅款',
        'sofa': '沙發與雅座',
        'outdoor': '戶外家具',
        'heading': '全球實績案例解析',
        'desc': '探索我們如何透過空間策略與頂級商用家具，解決客戶最棘手的空間痛點。'
    },
    'jp': {
        'all': 'すべての空間',
        'fb': '飲食スペース',
        'office': 'オフィス・研修',
        'wellness': 'スパ・ウェルネス',
        'public': 'リゾート・公共',
        'all_p': 'すべての家具',
        'chair': 'チェア',
        'sofa': 'ソファ',
        'outdoor': 'アウトドア',
        'heading': 'グローバルプロジェクト実積',
        'desc': '戦略的な空間アプローチと最高級の商業用家具を通じて、お客様の切実な課題をいかに解決してきたか。'
    }
}

css_content = """
/* Premium Editorial Layout */
.ultimate-case-section {
  padding: 6rem 0;
  border-bottom: 1px solid #f2efea;
  background-color: #fff;
}
.ultimate-case-section:nth-child(even) {
  background-color: #faf9f6;
}
.ultimate-case-header {
  margin-bottom: 3.5rem;
}
.ultimate-case-header .meta {
  font-size: 0.75rem;
  letter-spacing: 3px;
  color: var(--copper);
  text-transform: uppercase;
  font-weight: 700;
  display: block;
  margin-bottom: 0.5rem;
}
.ultimate-case-header h2 {
  font-family: 'Times New Roman', Times, serif;
  font-size: 3rem;
  color: #111;
  font-weight: normal;
  margin: 0;
}
.ultimate-case-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 5.5rem;
  align-items: flex-start;
}
.uc-visuals {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.uc-video-wrap {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  background: #000;
}
.uc-video-wrap video {
  width: 100%;
  height: auto;
  display: block;
}
.photo-carousel-wrap {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}
.photo-carousel {
  display: flex;
  overflow-x: scroll;
  scroll-snap-type: x mandatory;
  gap: 15px;
  width: 100%;
  scroll-behavior: smooth;
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.photo-carousel::-webkit-scrollbar {
  display: none;
}
.carousel-item {
  flex: 0 0 100%;
  scroll-snap-align: center;
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 16/10;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.carousel-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: none; /* Reset old bad transform */
}
.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #eaeaea;
  color: #333;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  font-size: 1.1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.2s ease;
}
.carousel-btn:hover {
  background: #111;
  color: #fff;
  border-color: #111;
}
.carousel-btn.prev {
  left: -20px;
}
.carousel-btn.next {
  right: -20px;
}
.uc-narrative {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  padding-top: 1rem;
}
.uc-text-block h4 {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--copper);
  margin-bottom: 0.75rem;
  font-weight: 700;
}
.uc-text-block p {
  font-size: 1.1rem;
  line-height: 1.75;
  color: #444;
  margin: 0;
  font-family: system-ui, -apple-system, sans-serif;
}
.uc-testimonial {
  border-top: 1px solid #f2efea;
  padding-top: 2rem;
  margin-top: 1rem;
}
.uc-testimonial p {
  font-family: 'Times New Roman', Times, serif;
  font-size: 1.35rem;
  font-style: italic;
  color: #111;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}
.uc-testimonial .author {
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #333;
}
.uc-testimonial .author span {
  display: block;
  font-weight: normal;
  color: #777;
  text-transform: none;
  letter-spacing: 0;
  margin-top: 0.25rem;
}

/* Glassmorphic Luxury Sticky Filters */
.filter-section {
  padding: 1.5rem 0;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(242, 239, 234, 0.7);
  position: sticky;
  top: 90px;
  z-index: 100;
  transition: all 0.3s ease;
}
.filter-row {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  justify-content: center;
}
.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
  align-items: center;
  position: relative;
}
/* Divider line between Groups */
.filter-row .filter-group:first-child {
  border-bottom: 1px solid #f2efea;
  padding-bottom: 1rem;
  width: 100%;
  max-width: 600px;
}
.filter-btn {
  background: transparent;
  border: none;
  padding: 6px 0;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  cursor: pointer;
  color: #888;
  position: relative;
  transition: color 0.3s ease;
}
.filter-btn::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: var(--copper);
  transition: width 0.3s ease;
}
.filter-btn.active {
  color: #111;
}
.filter-btn.active::after {
  width: 100%;
}
.filter-btn:hover {
  color: var(--copper);
}

/* Luxury Editorial Side Index Navigation */
.scrollspy-dots {
  position: fixed;
  right: 50px;
  top: 55%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  z-index: 1000;
  align-items: flex-end;
}
.spy-dot {
  display: flex;
  align-items: center;
  gap: 15px;
  cursor: pointer;
  height: 20px;
  transition: all 0.3s ease;
  position: relative;
}
/* Visual element: Very thin golden line */
.spy-dot::before {
  content: "";
  width: 15px;
  height: 1px;
  background-color: #ddd;
  transition: all 0.3s ease;
}
/* Label: Thin uppercase index number e.g. 01, 02 */
.spy-dot::after {
  content: attr(data-index);
  font-size: 0.7rem;
  font-family: system-ui, sans-serif;
  font-weight: 600;
  letter-spacing: 1px;
  color: #bbb;
  transition: all 0.3s ease;
}
.spy-dot.active::before {
  width: 35px;
  background-color: var(--copper);
}
.spy-dot.active::after {
  color: var(--copper);
  font-weight: 700;
  transform: scale(1.1);
}
.spy-dot .tooltip {
  position: absolute;
  right: 70px;
  top: 50%;
  transform: translateY(-50%);
  background: #111;
  color: #fff;
  padding: 6px 12px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  border-radius: 2px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease, transform 0.25s ease;
  transform: translateY(-50%) translateX(10px);
}
.spy-dot:hover .tooltip {
  opacity: 1;
  transform: translateY(-50%) translateX(0);
}

/* Transitions for case studies */
.ultimate-case-section {
  opacity: 1;
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.ultimate-case-section.hidden {
  display: none;
  opacity: 0;
  transform: translateY(20px);
}

@media (max-width: 992px) {
  .scrollspy-dots {
    display: none;
  }
  .ultimate-case-grid {
    grid-template-columns: 1fr;
    gap: 4rem;
  }
  .carousel-btn.prev { left: 10px; }
  .carousel-btn.next { right: 10px; }
}
"""

js_code = """
<script>
function scrollCarousel(btn, direction) {
  const wrap = btn.parentElement;
  const carousel = wrap.querySelector('.photo-carousel');
  const scrollAmount = carousel.clientWidth;
  carousel.scrollBy({
    left: direction * scrollAmount,
    behavior: 'smooth'
  });
}

// Global Filter Logic
let activeSpace = 'all';
let activeProduct = 'all';

function filterCases(group, type) {
  // Update buttons state
  const groupContainer = document.querySelector(`.filter-group[data-group="${group}"]`);
  groupContainer.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
  
  // Find clicked button
  event.target.classList.add('active');

  if (group === 'space') activeSpace = type;
  if (group === 'product') activeProduct = type;

  // Filter case blocks
  const sections = document.querySelectorAll('.ultimate-case-section');
  
  sections.forEach(sec => {
    const spaceMatch = activeSpace === 'all' || sec.getAttribute('data-space') === activeSpace;
    const prodMatch = activeProduct === 'all' || sec.getAttribute('data-product') === activeProduct;
    
    if (spaceMatch && prodMatch) {
      sec.classList.remove('hidden');
    } else {
      sec.classList.add('hidden');
    }
  });

  // Re-initialize Scrollspy positions
  updateScrollspyDots();
}

// Scrollspy Dots Logic
function updateScrollspyDots() {
  const container = document.getElementById('scrollspy-dots-container');
  container.innerHTML = '';
  
  const visibleSections = Array.from(document.querySelectorAll('.ultimate-case-section:not(.hidden)'));
  visibleSections.forEach((sec, idx) => {
    const dot = document.createElement('div');
    dot.className = 'spy-dot';
    
    // Format index as 01, 02, etc.
    const displayIndex = String(idx + 1).padStart(2, '0');
    dot.setAttribute('data-index', displayIndex);
    dot.setAttribute('data-target', sec.id);
    
    const tooltip = document.createElement('span');
    tooltip.className = 'tooltip';
    tooltip.textContent = sec.querySelector('h2').textContent;
    dot.appendChild(tooltip);
    
    dot.addEventListener('click', () => {
      sec.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
    
    container.appendChild(dot);
  });
  
  // Trigger intersection check immediately
  triggerIntersectionObserver(visibleSections);
}

function triggerIntersectionObserver(visibleSections) {
  const dots = document.querySelectorAll('.spy-dot');
  const observerOptions = {
    root: null,
    rootMargin: '-30% 0px -45% 0px', // Focused zone in the viewport
    threshold: 0.1
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        dots.forEach(dot => {
          if (dot.getAttribute('data-target') === entry.target.id) {
            dot.classList.add('active');
          } else {
            dot.classList.remove('active');
          }
        });
      }
    });
  }, observerOptions);
  
  visibleSections.forEach(sec => observer.observe(sec));
}

document.addEventListener('DOMContentLoaded', () => {
  updateScrollspyDots();
});
</script>
"""

def inject_css(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Wipe old layout rules
    content = re.sub(r'/\* Ultimate Case Study Section \*/.*', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* Slider Replaced with Navigation Arrows \*/.*', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* Slider Replaced with Navigation Arrows with CSS Masking \*/.*', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* Premium Layout Overhaul \*/.*', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* Filter Control Styling \*/.*', '', content, flags=re.DOTALL)
    content = re.sub(r'/\* Premium Editorial Layout \*/.*', '', content, flags=re.DOTALL)
    
    content += css_content
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(content)

def build_ultimate_layout(lang_data, lang):
    strs = filter_strings[lang]
    
    filter_html = f'''
  <!-- Ultimate Filter Controls -->
  <div class="filter-section">
    <div class="container filter-row">
      <!-- Space Group -->
      <div class="filter-group" data-group="space">
        <button class="filter-btn active" onclick="filterCases('space', 'all')">{strs['all']}</button>
        <button class="filter-btn" onclick="filterCases('space', 'fb')">{strs['fb']}</button>
        <button class="filter-btn" onclick="filterCases('space', 'office')">{strs['office']}</button>
        <button class="filter-btn" onclick="filterCases('space', 'wellness')">{strs['wellness']}</button>
        <button class="filter-btn" onclick="filterCases('space', 'public')">{strs['public']}</button>
      </div>
      <!-- Product Group -->
      <div class="filter-group" data-group="product">
        <button class="filter-btn active" onclick="filterCases('product', 'all')">{strs['all_p']}</button>
        <button class="filter-btn" onclick="filterCases('product', 'chair')">{strs['chair']}</button>
        <button class="filter-btn" onclick="filterCases('product', 'sofa')">{strs['sofa']}</button>
        <button class="filter-btn" onclick="filterCases('product', 'outdoor')">{strs['outdoor']}</button>
      </div>
    </div>
  </div>
  
  <!-- Floating dots for navigation -->
  <div class="scrollspy-dots" id="scrollspy-dots-container"></div>
'''

    html = f'''
  <!-- Ultimate Case Studies Start -->
  <section class="section" style="padding-top: 140px; padding-bottom: 2rem; background: #fff;">
    <div class="container text-center">
      <h1 style="font-size: 3.5rem; font-family: 'Times New Roman', Times, serif; font-weight: normal; margin-bottom: 1rem;">{strs['heading']}</h1>
      <p style="font-size: 1.15rem; color: #666; max-width: 700px; margin: 0 auto; line-height: 1.7;">{strs['desc']}</p>
    </div>
  </section>
  {filter_html}
'''
    for idx, case in enumerate(lang_data):
        video_html = f'''<div class="uc-video-wrap">
            <video src="../_assets/projects/{case['video']}" autoplay loop muted playsinline preload="metadata"></video>
          </div>''' if case.get('video') else ''
        
        b_img = case['base_img']
        carousel_html = f'''
          <div class="photo-carousel-wrap">
            <button class="carousel-btn prev" onclick="scrollCarousel(this, -1)">&#10094;</button>
            <div class="photo-carousel">
              <div class="carousel-item"><img src="../_assets/projects/{b_img}_q1.jpg" alt="Detail 1" loading="lazy"></div>
              <div class="carousel-item"><img src="../_assets/projects/{b_img}_q2.jpg" alt="Detail 2" loading="lazy"></div>
              <div class="carousel-item"><img src="../_assets/projects/{b_img}_q3.jpg" alt="Detail 3" loading="lazy"></div>
              <div class="carousel-item"><img src="../_assets/projects/{b_img}_q4.jpg" alt="Detail 4" loading="lazy"></div>
            </div>
            <button class="carousel-btn next" onclick="scrollCarousel(this, 1)">&#10095;</button>
          </div>
        '''

        html += f'''
  <section class="ultimate-case-section" id="{case['id']}" data-space="{case['space']}" data-product="{case['product']}">
    <div class="container">
      <div class="ultimate-case-header scroll-reveal">
        <span class="meta">{case['meta']}</span>
        <h2>{case['title']}</h2>
      </div>
      
      <div class="ultimate-case-grid">
        
        <!-- Left Side: Interactive Visual Media -->
        <div class="uc-visuals scroll-reveal">
          {video_html}
          {carousel_html}
        </div>
        
        <!-- Right Side: Structured Marketing Copy -->
        <div class="uc-narrative scroll-reveal" style="transition-delay: 0.15s;">
          <div class="uc-text-block">
            <h4>The Challenge</h4>
            <p>{case['challenge']}</p>
          </div>
          <div class="uc-text-block">
            <h4>The Transformation</h4>
            <p>{case['solution']}</p>
          </div>
          <div class="uc-text-block">
            <h4>The Sunnyward Difference</h4>
            <p>{case['difference']}</p>
          </div>
          
          <div class="uc-testimonial">
            <p>{case['quote']}</p>
            <div class="author">
              {case['author']}
              <span>{case['company']}</span>
            </div>
          </div>
        </div>
        
      </div>
    </div>
  </section>
'''
    html += '  <!-- Ultimate Case Studies End -->\n'
    return html

def update_html(filepath, lang):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(r'<script>\s*function scrollCarousel.*?/script>', '', content, flags=re.DOTALL)
    
    start_marker = r'(<nav class="mobile-drawer".*?</nav>)'
    end_marker = r'(<!-- Sticky Inquiry CTA -->)'
    
    match = re.search(start_marker + r'.*?' + end_marker, content, flags=re.DOTALL)
    if match:
        data_to_use = cases_data.get(lang, cases_data['en'])
        new_content = content[:match.end(1)] + '\n' + build_ultimate_layout(data_to_use, lang) + '\n  ' + content[match.start(2):]
        
        new_content = new_content.replace('</body>', js_code + '\n</body>')
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"
inject_css(os.path.join(base_path, "css", "style.css"))
update_html(os.path.join(base_path, "en", "projects.html"), "en")
update_html(os.path.join(base_path, "tw", "projects.html"), "tw")
update_html(os.path.join(base_path, "jp", "projects.html"), "jp")
print("Successfully generated luxury editorial filters and scrollspy index.")
