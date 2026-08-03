import os
import re

base_dir = r'c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website'

# Fix HTML files
for lang in ['tw', 'jp', 'en']:
    lang_dir = os.path.join(base_dir, lang)
    if not os.path.exists(lang_dir): continue
    
    for filename in os.listdir(lang_dir):
        if not filename.endswith('.html'): continue
        path = os.path.join(lang_dir, filename)
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Fix H1 in contact/projects
        if filename in ['contact.html', 'projects.html']:
            # Find the first <h2> inside section-header and change to <h1>
            content = re.sub(r'(<div class="section-header.*?>\s*<span.*?>.*?</span>\s*)<h2>(.*?)</h2>', r'\1<h1>\2</h1>', content, count=1, flags=re.DOTALL)
            
        # 2. Fix UI Strings for TW
        if lang == 'tw':
            content = content.replace('Toggle menu', '開啟選單')
            content = content.replace('Malaysia (Factory)', '馬來西亞 (工廠)')
            content = content.replace('Singapore (HQ)', '新加坡 (總部)')
            content = content.replace('天然い草疊系列', '天然草編系列')
            content = content.replace('たまゆらの里', '日本和歌山星空帳篷')
            content = content.replace('Balan Hill Glamping', '峇嵐杉丘豪華露營')
            content = content.replace('El Balcon...', 'El Balcon 景觀餐廳')
            
        # 3. Fix UI Strings for JP
        if lang == 'jp':
            content = content.replace('Toggle menu', 'メニューを開く')
            content = content.replace('Malaysia (Factory)', 'マレーシア (工場)')
            content = content.replace('Singapore (HQ)', 'シンガポール (本社)')
            content = content.replace('Contact', 'お問い合わせ')
            content = content.replace('All rights reserved.', '無断転載を禁じます。')
            content = content.replace('Balan Hill Glamping', 'バランヒルグランピング')
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
print('HTML architecture and UI strings updated.')
