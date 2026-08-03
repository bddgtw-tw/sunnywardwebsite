import os
import re

base_dir = r'c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website'
for lang in ['tw', 'jp', 'en']:
    path = os.path.join(base_dir, lang, 'products.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Merge double classes: class="A" class="B" -> class="A B"
        content = re.sub(r'class="([^"]+)"\s+class="([^"]+)"', r'class="\1 \2"', content)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed {lang}')
