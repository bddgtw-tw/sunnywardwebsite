import os
import re

html_blocks = {
    'en': {
        'title': 'The Sunnyward Advantage: Transforming Spaces',
        'subtitle': 'Real impact. Real results. How we solve critical space challenges for our clients.',
        'cases': [
            {
                'meta': 'HOTEL F&B - JOHOR',
                'title': 'Elevating the Dining Experience',
                'challenge': 'Hotel F&B areas often struggle with outdated, mismatched seating that ruins the premium dining atmosphere.',
                'solution': 'By introducing our cohesive, commercial-grade furniture, hotels instantly upgrade their ambiance, leading to higher table turnover and better customer retention.',
                'difference': 'We don’t just sell chairs; we provide aesthetic alignment with extreme durability.'
            },
            {
                'meta': 'WOODFIRE PASIR GUDANG',
                'title': 'Built for High Traffic & Fast Casual',
                'challenge': 'Fast casual dining spaces face immense wear and tear, and cold stainless steel setups feel uninviting.',
                'solution': 'Our heavy-duty, impact-resistant tables and chairs create a warm, inviting destination while withstanding relentless daily use.',
                'difference': 'Engineered for rapid cleaning cycles without compromising on the brand’s visual warmth.'
            },
            {
                'meta': 'TOAST MASTER INTERNATIONAL - JOHOR',
                'title': 'Inspiring Learning & Corporate Courses',
                'challenge': 'Standard, rigid conference furniture creates a stiff, uninspiring environment that drains participant energy.',
                'solution': 'Vibrant, ergonomic seating energizes the room, promoting better focus and engagement during intensive courses.',
                'difference': 'We balance vivid aesthetics with stackable, easy-to-store utility for multi-purpose event spaces.'
            },
            {
                'meta': 'THAI MASSAGE CASES - BUKIT BINTANG',
                'title': 'Crafting Zen Wellness Retreats',
                'challenge': 'A disorganized waiting area with generic seating fails to put guests in a state of relaxation upon arrival.',
                'solution': 'Solid wood lounge sets instantly create a grounding, Zen atmosphere that calms guests the moment they step in.',
                'difference': 'Our solid timber selections provide a reassuring sturdiness and natural warmth that synthetic alternatives simply cannot match.'
            }
        ]
    },
    'tw': {
        'title': 'Sunnyward 的絕對優勢：空間轉型實錄',
        'subtitle': '真實的商業影響力。我們如何解決客戶最棘手的空間挑戰？',
        'cases': [
            {
                'meta': '飯店餐飲空間 - 柔佛 (HOTEL F&B)',
                'title': '重塑頂級用餐體驗',
                'challenge': '飯店的餐飲區域常面臨家具老舊、風格不一致的問題，嚴重影響高級用餐氣氛與品牌價值。',
                'solution': '我們導入了具備高質感的統一家具風格，瞬間提升空間格調，進而帶動翻桌率與顧客回訪率。',
                'difference': '我們不只是賣椅子，而是提供完美契合飯店品牌形象，且具備「商用級高耐用度」的全方位解決方案。'
            },
            {
                'meta': '高人氣連鎖餐廳 - 柔佛 (WOODFIRE & PIZZA MANIA)',
                'title': '專為高客流量量身打造',
                'challenge': '高人氣餐廳面臨極大的家具耗損，而傳統冰冷的不鏽鋼桌椅讓人感到有距離感，缺乏讓人放鬆用餐的溫度。',
                'solution': '透過溫潤木質調與極度耐用的座椅，將快節奏的餐廳轉化為充滿吸引力的用餐目的地，同時能承受每日高強度的磨損。',
                'difference': '我們的家具專為高人流環境設計，不僅設計精美，更具備易清潔、抗衝擊的極致耐用性。'
            },
            {
                'meta': '企業與教育培訓空間 (TOAST MASTER INTERNATIONAL)',
                'title': '激發學習與交流靈感',
                'challenge': '制式且僵硬的會議家具，容易讓學習與交流環境顯得死板，降低參與者的能量與專注力。',
                'solution': '色彩鮮明、符合人體工學的座椅能活化空間氛圍，提升學員在密集課程中的專注力與參與感。',
                'difference': '我們將活潑美學與「可堆疊、易收納」的實用性完美結合，是多功能活動空間的最佳選擇。'
            },
            {
                'meta': '頂級舒壓養生館 - 吉隆坡武吉免登 (THAI MASSAGE)',
                'title': '營造極致放鬆的禪意空間',
                'challenge': '雜亂或使用廉價座椅的等候區，無法讓顧客一進門就卸下心防，進入放鬆狀態。',
                'solution': '原木休閒沙發組瞬間營造出充滿禪意的沉穩氛圍，讓顧客在等待時也能感受頂級體驗。',
                'difference': '我們嚴選的實木材質不僅提供令人安心的穩固感，更帶來廉價合成材質無法比擬的自然溫潤。'
            }
        ]
    },
    'jp': {
        'title': 'Sunnywardの圧倒的な優位性：空間リニューアル実績',
        'subtitle': '確かなビジネスインパクト。お客様の抱える空間の課題をどう解決するか。',
        'cases': [
            {
                'meta': 'ホテル飲食スペース - ジョホール',
                'title': 'プレミアムなダイニング体験の再構築',
                'challenge': 'ホテルの飲食エリアでは、古く統一感のない家具がダイニングの雰囲気やブランド価値を大きく損なうことがあります。',
                'solution': '統一された高級感のあるデザインを導入することで、空間の格調を瞬時に高め、回転率やリピート率の向上に貢献します。',
                'difference': '単に家具を売るのではなく、ホテルブランドに完全に一致し、「商業用レベルの耐久性」を備えたソリューションを提供します。'
            },
            {
                'meta': '人気レストラン - ジョホール (WOODFIRE / PIZZA MANIA)',
                'title': '高トラフィックな環境に特化した設計',
                'challenge': '人気レストランでは家具の消耗が激しく、冷たい印象のステンレス製家具ではリラックスして食事を楽しむ温かみに欠けてしまいます。',
                'solution': '温かみのある木目調と極めて耐久性の高いシートを採用することで、過酷な日常使用に耐えうる魅力的なダイニング空間へと生まれ変わります。',
                'difference': '当社の家具は、美しいデザイン性を保ちながらも、清掃が容易で耐衝撃性に優れた、高トラフィック環境向けの設計です。'
            },
            {
                'meta': '企業研修・学習スペース (TOAST MASTER INTERNATIONAL)',
                'title': '学習意欲とインスピレーションを刺激する',
                'challenge': '画一的で硬い会議用家具は、学習環境を退屈にし、参加者のエネルギーや集中力を奪いがちです。',
                'solution': '鮮やかな色彩と人間工学に基づいた椅子が空間を活性化させ、集中力と参加意欲を高めます。',
                'difference': '活気あるデザインと、スタッキング可能で収納しやすい実用性を両立しており、多目的イベントスペースに最適です。'
            },
            {
                'meta': '高級リラクゼーションサロン - クアラルンプール',
                'title': '至福のリラックス空間を創出',
                'challenge': '雑然とした待合室や安価な椅子では、来店されたお客様をすぐにリラックス状態に導くことができません。',
                'solution': '無垢材のラウンジソファセットが、瞬時に禅の心を感じる落ち着いた雰囲気を醸し出し、待ち時間も上質な体験に変えます。',
                'difference': '厳選された無垢材は、安心感のある頑丈さを提供するだけでなく、安価な合成素材では真似できない自然な温もりをもたらします。'
            }
        ]
    }
}

def build_section(lang_data):
    html = f'''
  <!-- Text Driven Transformation Stories Section -->
  <section class="section text-transformation-section" style="background-color: #F8F6F0; padding: 5rem 0;">
    <div class="container">
      <div class="section-header scroll-reveal text-center" style="margin-bottom: 4rem;">
        <h2 style="font-size: 2.2rem; color: #1a1a1a; margin-bottom: 1rem;">{lang_data['title']}</h2>
        <p style="color: #666; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">{lang_data['subtitle']}</p>
      </div>
      
      <div class="text-cases-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2.5rem;">
'''
    for case in lang_data['cases']:
        html += f'''
        <div class="text-case-card scroll-reveal" style="background: #fff; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border-top: 4px solid var(--copper);">
          <span style="font-size: 0.75rem; font-weight: bold; color: var(--copper); letter-spacing: 1px; text-transform: uppercase;">{case['meta']}</span>
          <h3 style="font-size: 1.4rem; margin: 1rem 0 1.5rem; color: #222;">{case['title']}</h3>
          
          <div style="margin-bottom: 1.2rem;">
            <strong style="display:block; font-size: 0.9rem; color: #333; margin-bottom: 0.3rem;">⚠️ Challenge</strong>
            <p style="font-size: 0.95rem; color: #666; line-height: 1.5;">{case['challenge']}</p>
          </div>
          
          <div style="margin-bottom: 1.2rem;">
            <strong style="display:block; font-size: 0.9rem; color: #333; margin-bottom: 0.3rem;">✨ Transformation</strong>
            <p style="font-size: 0.95rem; color: #666; line-height: 1.5;">{case['solution']}</p>
          </div>
          
          <div>
            <strong style="display:block; font-size: 0.9rem; color: #333; margin-bottom: 0.3rem;">🚀 The Sunnyward Difference</strong>
            <p style="font-size: 0.95rem; color: #666; line-height: 1.5;">{case['difference']}</p>
          </div>
        </div>
'''
    html += f'''
      </div>
    </div>
  </section>
'''
    return html

def update_html(filepath, lang):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove old transformation section
    content = re.sub(r'<!-- Transformation Stories Section -->.*?</section>', '', content, flags=re.DOTALL)
    
    # Inject new text driven section after Case Studies Grid
    target = '</div>\n    </div>\n  </section>'
    if target in content:
        section_html = build_section(html_blocks[lang])
        new_content = content.replace(target, target + '\n' + section_html, 1)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"
update_html(os.path.join(base_path, "en", "projects.html"), "en")
update_html(os.path.join(base_path, "tw", "projects.html"), "tw")
update_html(os.path.join(base_path, "jp", "projects.html"), "jp")
print("Successfully replaced with text-driven Transformation Stories.")
