import os
import re

base_dir = r'c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website'

for lang in ['tw', 'en', 'jp']:
    path = os.path.join(base_dir, lang, 'products.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the second catalog modal block
        # The block starts with <!-- CATALOG DOWNLOAD MODAL -->
        # We find that comment and replace everything from it to the next <!-- FOOTER -->
        new_content = re.sub(r'<!-- CATALOG DOWNLOAD MODAL -->.*?<!-- FOOTER -->', '<!-- FOOTER -->', content, flags=re.DOTALL)
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Fixed {lang} duplicate modal')
