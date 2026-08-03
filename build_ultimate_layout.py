import os
import re

css_content = """
/* Ultimate Case Study Section */
.ultimate-case-section {
  padding: 6rem 0;
  border-bottom: 1px solid #eaeaea;
}
.ultimate-case-section:nth-child(even) {
  background-color: #faf9f6;
}
.ultimate-case-header {
  text-align: center;
  margin-bottom: 4rem;
}
.ultimate-case-header h2 {
  font-family: 'Times New Roman', Times, serif;
  font-size: 2.8rem;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}
.ultimate-case-header .meta {
  font-size: 0.85rem;
  letter-spacing: 2px;
  color: var(--copper);
  text-transform: uppercase;
  font-weight: 600;
}
.ultimate-case-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: flex-start;
}
.uc-visuals {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
.uc-video-wrap, .uc-img-wrap {
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  background: #000;
}
.uc-video-wrap video, .uc-img-wrap img {
  width: 100%;
  height: auto;
  display: block;
}
.uc-narrative {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}
.uc-text-block h4 {
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: #1a1a1a;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.uc-text-block h4::before {
  content: "";
  display: block;
  width: 20px;
  height: 2px;
  background-color: var(--copper);
}
.uc-text-block p {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #555;
}
.uc-testimonial {
  background: #fff;
  padding: 2.5rem;
  border-left: 4px solid var(--copper);
  box-shadow: 0 5px 20px rgba(0,0,0,0.04);
  margin-top: 1rem;
}
.uc-testimonial p {
  font-size: 1.15rem;
  font-style: italic;
  color: #222;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}
.uc-testimonial .author {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1a1a1a;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.uc-testimonial .author span {
  display: block;
  font-size: 0.8rem;
  color: #888;
  font-weight: normal;
  margin-top: 0.2rem;
}

@media (max-width: 992px) {
  .ultimate-case-grid {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
}
"""

def inject_css(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'Ultimate Case Study Section' not in content:
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write(css_content)

html_data = {
    'en': {
        'title': 'Global Project Realizations',
        'intro_desc': 'Discover how we solve critical space challenges for our clients through comprehensive case studies combining visual proof and real outcomes.',
        'cases': [
            {
                'meta': 'HOTEL F&B - JOHOR',
                'title': 'Elevating the Hotel Dining Experience',
                'video': '2026.01_kai_restaurant.mp4',
                'img': '486466926_1193879656080876_2767098548785792068_n.jpg',
                'challenge': 'Hotel F&B areas often struggle with outdated, mismatched seating that ruins the premium dining atmosphere expected by high-paying guests.',
                'solution': 'By introducing our cohesive, commercial-grade furniture, the hotel instantly upgraded its ambiance, leading to a noticeable increase in table turnover and guest satisfaction.',
                'difference': 'We don’t just sell chairs; we provide aesthetic alignment combined with extreme durability required for high-traffic hospitality.',
                'quote': '"Sunnyward completely revitalized our dining area. The premium feel of the furniture matches our 5-star standard, yet they are incredibly easy for our staff to maintain."',
                'author': 'F&B Director',
                'company': 'Luxury Hotel, Johor'
            },
            {
                'meta': 'FAST CASUAL - PASIR GUDANG',
                'title': 'Built for High Traffic (Woodfire)',
                'video': '2024.01_family_restaurant.mp4',
                'img': '485005693_1188406983294810_676741634435601911_n.jpg',
                'challenge': 'Fast casual dining spaces face immense daily wear and tear. Previous cold stainless steel setups felt uninviting and deterred customers from staying.',
                'solution': 'Our heavy-duty, impact-resistant tables and comfortable chairs created a warm, inviting destination while easily withstanding relentless daily use.',
                'difference': 'Engineered for rapid cleaning cycles without compromising on the brand’s visual warmth and customer comfort.',
                'quote': '"We need furniture that can take a beating but still look great on Instagram. Sunnyward delivered exactly that. Our customers love the new vibe."',
                'author': 'Operations Manager',
                'company': 'Woodfire Pasir Gudang'
            },
            {
                'meta': 'CORPORATE LEARNING - JOHOR',
                'title': 'Inspiring Educational Spaces',
                'video': '2024.11_tsutaya_bookstore.mp4',
                'img': '486540137_1194648809337294_8428044945485451315_n.jpg',
                'challenge': 'Standard, rigid conference furniture creates a stiff, uninspiring environment that quickly drains participant energy during long training sessions.',
                'solution': 'Vibrant, ergonomic seating energized the room, promoting better posture, focus, and engagement during intensive corporate courses.',
                'difference': 'We balance vivid aesthetics with stackable, easy-to-store utility, making it the perfect solution for multi-purpose event spaces.',
                'quote': '"Since upgrading our training rooms, we\'ve seen a tangible increase in participant engagement. The chairs are not only beautiful but incredibly supportive for all-day workshops."',
                'author': 'Facilities Director',
                'company': 'Toast Master International'
            },
            {
                'meta': 'WELLNESS SPA - KUALA LUMPUR',
                'title': 'Crafting Zen Retreats',
                'video': '2024.05_dragon_ginseng.mp4',
                'img': '487230012_1197042165764625_5235377330861897247_n.jpg',
                'challenge': 'A disorganized waiting area with generic, lightweight seating fails to put guests in a state of relaxation upon arrival.',
                'solution': 'Solid wood lounge sets instantly created a grounding, Zen atmosphere that calms guests the moment they step into the spa.',
                'difference': 'Our solid timber selections provide a reassuring sturdiness and natural warmth that cheaper synthetic alternatives simply cannot match.',
                'quote': '"The moment our clients sit in the waiting lounge, they begin to relax. The quality and natural feel of the wood perfectly complement our wellness philosophy."',
                'author': 'Spa Founder',
                'company': 'Bukit Bintang Thai Massage'
            }
        ]
    },
    'tw': {
        'title': '全方位深度案例解析',
        'subtitle': 'The Ultimate Case Studies',
        'intro_desc': '探索我們如何透過空間策略與頂級商用家具，解決客戶最棘手的痛點。透過最真實的改造前後對比與現場實景影像，見證商業價值的真實提升。',
        'cases': [
            {
                'meta': '飯店餐飲空間 - 柔佛 (HOTEL F&B)',
                'title': '重塑頂級用餐體驗',
                'video': '2026.01_kai_restaurant.mp4',
                'img': '486466926_1193879656080876_2767098548785792068_n.jpg',
                'challenge': '飯店的餐飲區域常面臨家具老舊、風格不一致的問題，這會嚴重破壞高消費顧客所期待的高級用餐氣氛與品牌價值。',
                'solution': '我們為其導入了具備高質感的統一家具風格，瞬間提升整體空間格調，不僅讓環境煥然一新，更帶動了翻桌率與顧客回訪率。',
                'difference': '我們不只是賣椅子，而是提供完美契合飯店品牌形象，且具備「商用級高強度耐用度」的全方位解決方案。',
                'quote': '「Sunnyward 徹底為我們的餐廳注入了新生命。家具的高級質感完美符合我們的五星級標準，同時對員工來說又非常容易清潔與維護。」',
                'author': '餐飲部總監',
                'company': '柔佛頂級飯店'
            },
            {
                'meta': '高人氣快餐品牌 (WOODFIRE)',
                'title': '專為高客流量量身打造',
                'video': '2024.01_family_restaurant.mp4',
                'img': '485005693_1188406983294810_676741634435601911_n.jpg',
                'challenge': '高人氣快餐店面臨極大的家具耗損。而過去傳統冰冷的不鏽鋼桌椅讓人感到有距離感，無法吸引顧客久留。',
                'solution': '透過溫潤木質調與極度耐用、抗衝擊的座椅，我們將快節奏的餐廳轉化為充滿吸引力的用餐目的地，同時能完美承受每日的高強度磨損。',
                'difference': '我們的家具專為高人流環境設計，不僅設計精美，更具備快速清潔、抗磨損的極致實用性。',
                'quote': '「我們需要的是耐操又能兼顧 Instagram 打卡美感的家具。Sunnyward 完全做到了，我們的顧客非常喜歡現在的氛圍！」',
                'author': '營運經理',
                'company': 'Woodfire Pasir Gudang'
            },
            {
                'meta': '企業與教育培訓空間 (TOAST MASTER)',
                'title': '激發學習與交流靈感',
                'video': '2024.11_tsutaya_bookstore.mp4',
                'img': '486540137_1194648809337294_8428044945485451315_n.jpg',
                'challenge': '制式且僵硬的會議家具，容易讓學習與交流環境顯得死板，在長時間的培訓課程中迅速消耗參與者的能量與專注力。',
                'solution': '色彩鮮明、符合人體工學的座椅活化了空間氛圍，有效改善坐姿，並大幅提升學員在密集課程中的專注力與參與感。',
                'difference': '我們將活潑美學與「可堆疊、易收納」的實用性完美結合，絕對是多功能活動空間的最佳選擇。',
                'quote': '「自從升級了培訓室的設備後，我們明顯感受到學員參與度的提升。這批座椅不僅美觀，在全天候的工作坊中更能提供極佳的支撐力。」',
                'author': '設施管理總監',
                'company': 'Toast Master International'
            },
            {
                'meta': '頂級舒壓養生館 - 武吉免登 (THAI MASSAGE)',
                'title': '營造極致放鬆的禪意空間',
                'video': '2024.05_dragon_ginseng.mp4',
                'img': '487230012_1197042165764625_5235377330861897247_n.jpg',
                'challenge': '雜亂或使用輕薄廉價座椅的等候區，無法展現專業度，也無法讓顧客一進門就卸下心防進入放鬆狀態。',
                'solution': '原木休閒沙發組瞬間營造出充滿禪意與接地氣的沉穩氛圍，讓顧客在踏入養生館等待的當下，就已經開始享受頂級體驗。',
                'difference': '我們嚴選的實木材質不僅提供令人安心的穩固感，更帶來廉價合成材質絕對無法比擬的自然溫潤與高級感。',
                'quote': '「當客戶坐在等候區的沙發上時，他們就已經開始放鬆了。原木的品質與觸感完美契合我們的養生理念。」',
                'author': '養生館創辦人',
                'company': '武吉免登泰式按摩'
            }
        ]
    },
    'jp': {
        'title': '究極のケーススタディ',
        'subtitle': 'The Ultimate Case Studies',
        'intro_desc': '戦略的な空間アプローチと最高級の商業用家具を通じて、お客様の切実な課題をいかに解決してきたか。ビフォーアフターと実際の映像を交えた総合的な事例をご覧ください。',
        'cases': [
            {
                'meta': 'ホテル飲食スペース - ジョホール',
                'title': 'プレミアムなダイニング体験の再構築',
                'video': '2026.01_kai_restaurant.mp4',
                'img': '486466926_1193879656080876_2767098548785792068_n.jpg',
                'challenge': 'ホテルの飲食エリアでは、古く統一感のない家具が、高価格帯のお客様が期待する高級なダイニングの雰囲気やブランド価値を大きく損なっていました。',
                'solution': '統一された高級感のあるデザインを導入することで、空間の格調を瞬時に高め、結果として回転率やゲスト満足度の顕著な向上に繋がりました。',
                'difference': '単に家具を売るのではなく、ホテルブランドに完全に一致し、高トラフィック環境に必須の「商業用レベルの耐久性」を備えたソリューションを提供します。',
                'quote': '「Sunnyward は当ホテルのダイニングエリアを完全に蘇らせました。家具の高級感は5つ星の基準に合致しているだけでなく、スタッフにとってもメンテナンスが非常に容易です。」',
                'author': 'F&Bディレクター',
                'company': 'ラグジュアリーホテル（ジョホール）'
            },
            {
                'meta': '人気ファストカジュアル (WOODFIRE)',
                'title': '高トラフィックな環境に特化した設計',
                'video': '2024.01_family_restaurant.mp4',
                'img': '485005693_1188406983294810_676741634435601911_n.jpg',
                'challenge': '人気のファストカジュアル店では家具の消耗が激しく、以前の冷たい印象のステンレス製家具では、リラックスできる温かみに欠けていました。',
                'solution': '温かみのある木目調と極めて耐久性の高いシートを採用することで、過酷な日常使用に耐えうる、魅力的で居心地の良いダイニング空間へと生まれ変わりました。',
                'difference': 'ブランドの視覚的な温かみを損なうことなく、迅速な清掃サイクルと耐衝撃性に優れた設計を実現しています。',
                'quote': '「タフでありながら Instagram 映えする家具が必要でした。Sunnyward はまさにそれを提供してくれました。お客様も新しい雰囲気を気に入っています。」',
                'author': 'オペレーションマネージャー',
                'company': 'Woodfire Pasir Gudang'
            },
            {
                'meta': '企業研修・学習スペース (TOAST MASTER)',
                'title': '学習意欲とインスピレーションを刺激する',
                'video': '2024.11_tsutaya_bookstore.mp4',
                'img': '486540137_1194648809337294_8428044945485451315_n.jpg',
                'challenge': '画一的で硬い会議用家具は、学習環境を退屈にし、長時間の研修セッションでは参加者のエネルギーや集中力を急速に奪いがちです。',
                'solution': '鮮やかな色彩と人間工学に基づいた椅子が空間を活性化させ、正しい姿勢を保ちながら、集中力と参加意欲を大幅に高めました。',
                'difference': '活気あるデザインと、スタッキング可能で収納しやすい実用性を両立しており、多目的イベントスペースに最適なソリューションです。',
                'quote': '「研修室の設備をアップグレードして以来、参加者の関与が目に見えて向上しました。椅子は美しいだけでなく、終日のワークショップでも素晴らしいサポートを提供してくれます。」',
                'author': 'ファシリティディレクター',
                'company': 'Toast Master International'
            },
            {
                'meta': '高級リラクゼーション - クアラルンプール',
                'title': '至福の禅リトリート空間を創出',
                'challenge': '雑然とした待合室や安価で軽い椅子では、来店されたお客様をすぐにリラックス状態に導くことができず、専門性も伝わりません。',
                'solution': '無垢材のラウンジソファセットが、瞬時に地に足の着いた禅の落ち着いた雰囲気を醸し出し、スパに足を踏み入れた瞬間から上質な体験を提供します。',
                'difference': '厳選された無垢材は、安心感のある頑丈さを提供するだけでなく、安価な合成素材では真似できない自然な温もりと高級感をもたらします。',
                'quote': '「お客様が待合ラウンジに座った瞬間から、リラックスし始めます。木材の品質と自然な感触が、私たちのウェルネス哲学と完璧に調和しています。」',
                'author': 'スパ創設者',
                'company': 'ブキッビンタン タイマッサージ'
            }
        ]
    }
}

def build_ultimate_layout(lang_data):
    html = f'''
  <!-- Ultimate Case Studies Start -->
  <section class="section" style="padding-top: 140px; padding-bottom: 2rem; background: #fff;">
    <div class="container text-center">
      <h1 style="font-size: 3rem; margin-bottom: 1rem;">{lang_data['title']}</h1>
      <p style="font-size: 1.1rem; color: #666; max-width: 700px; margin: 0 auto;">{lang_data['intro_desc']}</p>
    </div>
  </section>
'''
    for idx, case in enumerate(lang_data['cases']):
        video_html = f'''<div class="uc-video-wrap">
            <video src="../_assets/projects/{case['video']}" autoplay loop muted playsinline></video>
          </div>''' if case.get('video') else ''
        html += f'''
  <section class="ultimate-case-section">
    <div class="container">
      <div class="ultimate-case-header scroll-reveal">
        <span class="meta">{case['meta']}</span>
        <h2>{case['title']}</h2>
      </div>
      
      <div class="ultimate-case-grid">
        
        <!-- Visuals Column -->
        <div class="uc-visuals scroll-reveal">
          {video_html}
          <div class="uc-img-wrap" style="position: relative;">
            <div style="position: absolute; top: 15px; left: 15px; background: rgba(0,0,0,0.7); color: #fff; padding: 4px 12px; font-size: 0.75rem; font-weight: bold; letter-spacing: 1px; border-radius: 4px; text-transform: uppercase;">Before & After</div>
            <img src="../_assets/projects/{case.get('img', '')}" alt="{case['title']} Transformation">
          </div>
        </div>
        
        <!-- Narrative Column -->
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
    
    # We are going to replace everything from the first <section> tag after <nav id="mobile-drawer"> 
    # up to the Sticky Inquiry CTA
    
    start_marker = r'(<nav class="mobile-drawer".*?</nav>)'
    end_marker = r'(<!-- Sticky Inquiry CTA -->)'
    
    match = re.search(start_marker + r'.*?' + end_marker, content, flags=re.DOTALL)
    if match:
        new_content = content[:match.end(1)] + '\n' + build_ultimate_layout(html_data[lang]) + '\n  ' + content[match.start(2):]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"
inject_css(os.path.join(base_path, "css", "style.css"))
update_html(os.path.join(base_path, "en", "projects.html"), "en")
update_html(os.path.join(base_path, "tw", "projects.html"), "tw")
update_html(os.path.join(base_path, "jp", "projects.html"), "jp")
print("Successfully replaced with Ultimate Case Studies layout.")
