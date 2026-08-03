import os
import re

base_dir = r'c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website'

for lang in ['tw', 'jp', 'en']:
    path = os.path.join(base_dir, lang, 'products.html')
    if not os.path.exists(path): continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    def replacer(match):
        body = match.group(1)
        lines = body.strip().split('\n')
        outdoor_idx = -1
        for i, line in enumerate(lines):
            if 'outdoor:' in line:
                outdoor_idx = i
                break
                
        if outdoor_idx != -1:
            outdoor_line = lines.pop(outdoor_idx)
            lines.insert(0, outdoor_line)
            
        new_body = '\n'.join(lines)
        return f'const catTranslations = {{\n{new_body}\n    }};'

    new_content = re.sub(r'const catTranslations = \{(.*?)\};', replacer, content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Reordered {lang}')
