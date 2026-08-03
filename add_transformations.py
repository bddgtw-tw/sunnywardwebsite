import os
import re

css_content = """
/* Transformation Stories Section */
.transformation-section {
  padding: 4rem 0;
  background-color: #faf8f5;
}
.transform-header {
  text-align: center;
  margin-bottom: 3rem;
}
.transform-header h2 {
  font-size: 2.2rem;
  margin-bottom: 1rem;
}
.transform-row {
  display: flex;
  align-items: center;
  gap: 3rem;
  margin-bottom: 4rem;
}
.transform-row:nth-child(even) {
  flex-direction: row-reverse;
}
.transform-img-col {
  flex: 1;
  position: relative;
}
.transform-img-col img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}
.transform-text-col {
  flex: 1;
}
.transform-text-col h3 {
  font-size: 1.6rem;
  margin-bottom: 1rem;
  color: var(--copper);
}
.transform-text-col h4 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #333;
}
.transform-text-col p {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #555;
  margin-bottom: 1.5rem;
}
.transform-cta-block {
  text-align: center;
  margin-top: 4rem;
  padding: 3rem;
  background: var(--bg-primary);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}
.transform-cta-block h3 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .transform-row, .transform-row:nth-child(even) {
    flex-direction: column;
    gap: 1.5rem;
  }
}
"""

def inject_css(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'Transformation Stories Section' not in content:
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write(css_content)

html_blocks = {
    'en': {
        'title': 'Why Choose Sunnyward? Transformation Stories',
        'subtitle': 'Real impact. Elevating commercial spaces from ordinary to extraordinary.',
        'q1': 'The Challenge',
        'q2': 'The Transformation',
        'q3': 'The Sunnyward Difference',
        'cta_title': 'Is Your Space Ready for the Next Level of Growth?',
        'cta_desc': 'Join hundreds of satisfied brands who have transformed their environment and elevated their customer experience with Sunnyward.',
        'cta_btn': 'Talk to our Experts',
        'cases': [
            {
                'img': '485005693_1188406983294810_676741634435601911_n.jpg',
                'title': 'Restaurant & Hotel F&B Upgrades',
                'p1': 'Old, mismatched, or broken furniture severely impacts the dining atmosphere and brand value.',
                'p2': 'We bring in a cohesive, premium aesthetic that instantly upgrades the space, leading to higher table turnover and better customer retention.',
                'p3': 'We do not just sell chairs; we provide commercial-grade durability with an aesthetic that perfectly matches your brand identity.'
            },
            {
                'img': '486466926_1193879656080876_2767098548785792068_n.jpg',
                'title': 'High-Traffic Cafeterias (Pizza Mania)',
                'p1': 'Cold stainless steel setups feel uninviting and lack the warmth required for a relaxing meal.',
                'p2': 'By introducing warm wooden tones and comfortable upholstered seating, the cafeteria transforms into an inviting dining destination.',
                'p3': 'Our furniture is engineered for rapid cleaning cycles and extreme durability in high-traffic environments, without compromising on design.'
            },
            {
                'img': '486540137_1194648809337294_8428044945485451315_n.jpg',
                'title': 'Corporate & Learning Spaces (Toastmasters)',
                'p1': 'Standard, rigid conference furniture creates a stiff and uninspiring learning environment.',
                'p2': 'Vibrant, ergonomic seating energizes the room, promoting better focus and engagement during courses.',
                'p3': 'We balance vivid aesthetics with stackable, easy-to-store utility, making our furniture perfect for multi-purpose event spaces.'
            },
            {
                'img': '487230012_1197042165764625_5235377330861897247_n.jpg',
                'title': 'Wellness & Spa Retreats (Thai Massage)',
                'p1': 'A disorganized waiting area with generic seating fails to put guests in a state of relaxation.',
                'p2': 'Solid wood lounge sets instantly create a Zen, grounding atmosphere that calms guests the moment they arrive.',
                'p3': 'Our solid timber selections provide a reassuring sturdiness and natural warmth that cheaper synthetic alternatives simply cannot match.'
            }
        ]
    },
    'tw': {
        'title': '為什麼選擇 Sunnyward？空間改造實錄',
        'subtitle': '真實的商業影響力。將您的商業空間從平凡提升至非凡。',
        'q1': '面臨的痛點',
        'q2': '改造後的效益',
        'q3': '我們的差異化優勢',
        'cta_title': '您的商業空間，準備好迎接下一波成長了嗎？',
        'cta_desc': '加入數百個滿意品牌的行列，透過 Sunnyward 升級您的環境並提升顧客體驗。',
        'cta_btn': '聯絡我們的專案顧問',
        'cases': [
            {
                'img': '485005693_1188406983294810_676741634435601911_n.jpg',
                'title': '飯店與餐飲空間升級',
                'p1': '老舊、風格不一致或損壞的家具會嚴重影響用餐氣氛與品牌價值。',
                'p2': '我們導入了具備高質感的統一家具風格，瞬間提升空間格調，進而帶動翻桌率與顧客回訪率。',
                'p3': '我們不只是賣椅子，而是提供完美契合您品牌形象且具備「商用級耐用度」的全方位解決方案。'
            },
            {
                'img': '486466926_1193879656080876_2767098548785792068_n.jpg',
                'title': '高人氣連鎖餐廳 (Pizza Mania)',
                'p1': '傳統冰冷的不鏽鋼桌椅讓人感到有距離感，缺乏讓人放鬆用餐的溫度。',
                'p2': '透過溫潤木質調與舒適的軟墊座椅，將餐廳轉化為充滿吸引力的用餐目的地。',
                'p3': '我們的家具專為高人流環境設計，不僅設計精美，更具備易清潔、抗磨損的極致耐用性。'
            },
            {
                'img': '486540137_1194648809337294_8428044945485451315_n.jpg',
                'title': '企業與教育培訓空間 (Toastmasters)',
                'p1': '制式且僵硬的會議家具，容易讓學習與交流環境顯得死板且缺乏靈感。',
                'p2': '色彩鮮明、符合人體工學的座椅能活化空間氛圍，提升學員的專注力與參與感。',
                'p3': '我們將活潑美學與可堆疊、易收納的實用性完美結合，是多功能活動空間的最佳選擇。'
            },
            {
                'img': '487230012_1197042165764625_5235377330861897247_n.jpg',
                'title': '頂級舒壓養生館 (Thai Massage)',
                'p1': '雜亂或使用廉價座椅的等候區，無法讓顧客一進門就進入放鬆狀態。',
                'p2': '原木休閒沙發組瞬間營造出充滿禪意的沉穩氛圍，讓顧客在等待時也能感受頂級體驗。',
                'p3': '我們嚴選的實木材質不僅提供令人安心的穩固感，更帶來廉價合成材質無法比擬的自然溫潤。'
            }
        ]
    },
    'jp': {
        'title': 'なぜ Sunnyward が選ばれるのか？ 空間リニューアル実績',
        'subtitle': '確かなビジネスインパクト。平凡な商業空間を非凡な体験へ。',
        'q1': '抱えていた課題',
        'q2': 'リニューアル後の効果',
        'q3': 'Sunnywardの強み',
        'cta_title': '次のステージへ、あなたの空間もアップグレードしませんか？',
        'cta_desc': '何百ものブランドが Sunnyward の家具で空間を刷新し、顧客体験を向上させています。',
        'cta_btn': '専門アドバイザーに相談する',
        'cases': [
            {
                'img': '485005693_1188406983294810_676741634435601911_n.jpg',
                'title': 'ホテル・飲食スペースのアップグレード',
                'p1': '古く統一感のない家具は、ダイニングの雰囲気やブランド価値を大きく損ないます。',
                'p2': '統一された高級感のあるデザインを導入することで、空間の格調を瞬時に高め、回転率やリピート率の向上に貢献します。',
                'p3': '単に家具を売るのではなく、ブランドイメージに完全に一致し、「商業用レベルの耐久性」を備えた総合的なソリューションを提供します。'
            },
            {
                'img': '486466926_1193879656080876_2767098548785792068_n.jpg',
                'title': '人気チェーンレストラン (Pizza Mania)',
                'p1': '冷たい印象のステンレス製テーブルと椅子は、リラックスして食事を楽しむ温かみに欠けていました。',
                'p2': '温かみのある木目調と快適なクッションシートを採用することで、魅力的なダイニング空間へと生まれ変わりました。',
                'p3': '当社の家具は、美しいデザイン性を保ちながらも、清掃が容易で耐摩耗性に優れた、高トラフィック環境向けの設計です。'
            },
            {
                'img': '486540137_1194648809337294_8428044945485451315_n.jpg',
                'title': '企業研修・学習スペース (Toastmasters)',
                'p1': '画一的で硬い会議用家具は、学習環境を退屈にし、インスピレーションを奪いがちです。',
                'p2': '鮮やかな色彩と人間工学に基づいた椅子が空間を活性化させ、受講者の集中力と参加意欲を高めます。',
                'p3': '活気あるデザインと、スタッキング可能で収納しやすい実用性を両立しており、多目的イベントスペースに最適です。'
            },
            {
                'img': '487230012_1197042165764625_5235377330861897247_n.jpg',
                'title': '高級リラクゼーションサロン (Thai Massage)',
                'p1': '雑然とした待合室や安価な椅子では、来店されたお客様をすぐにリラックス状態に導くことができません。',
                'p2': '無垢材のラウンジソファセットが、瞬時に禅の心を感じる落ち着いた雰囲気を醸し出し、待ち時間も上質な体験に変えます。',
                'p3': '厳選された無垢材は、安心感のある頑丈さを提供するだけでなく、安価な合成素材では真似できない自然な温もりをもたらします。'
            }
        ]
    }
}

def build_section(lang_data):
    html = f'''
  <!-- Transformation Stories Section -->
  <section class="section transformation-section">
    <div class="container">
      <div class="transform-header scroll-reveal">
        <h2>{lang_data['title']}</h2>
        <p>{lang_data['subtitle']}</p>
      </div>
      
      <div class="transform-list">
'''
    for case in lang_data['cases']:
        html += f'''
        <div class="transform-row scroll-reveal">
          <div class="transform-img-col">
            <img src="../_assets/projects/{case['img']}" alt="{case['title']} Before and After">
          </div>
          <div class="transform-text-col">
            <h3>{case['title']}</h3>
            <h4>{lang_data['q1']}</h4>
            <p>{case['p1']}</p>
            <h4>{lang_data['q2']}</h4>
            <p>{case['p2']}</p>
            <h4>{lang_data['q3']}</h4>
            <p>{case['p3']}</p>
          </div>
        </div>
'''
    html += f'''
      </div>
      
      <div class="transform-cta-block scroll-reveal">
        <h3>{lang_data['cta_title']}</h3>
        <p style="margin-bottom: 2rem; color:#555;">{lang_data['cta_desc']}</p>
        <a href="contact.html" class="btn btn-primary">{lang_data['cta_btn']}</a>
      </div>
    </div>
  </section>
'''
    return html

def inject_html(html_path, lang):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Inject right after the closing tag of the case studies grid section
    # Find </section> that corresponds to Case Studies Grid
    target = '</div>\n    </div>\n  </section>'
    
    if target in content and 'transformation-section' not in content:
        section_html = build_section(html_blocks[lang])
        new_content = content.replace(target, target + '\n' + section_html, 1)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"
inject_css(os.path.join(base_path, "css", "style.css"))
inject_html(os.path.join(base_path, "en", "projects.html"), "en")
inject_html(os.path.join(base_path, "tw", "projects.html"), "tw")
inject_html(os.path.join(base_path, "jp", "projects.html"), "jp")
print("Successfully injected Transformation Stories.")
