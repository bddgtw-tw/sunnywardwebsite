import os
import re

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"
pattern = re.compile(r'(&copy;\s*\d{4}\s*Sunnyward.*?</p>)', re.IGNORECASE)
replacement = r'\1\n        <p style="font-size: 0.8rem; opacity: 0.6; margin-top: 5px;">Version: <span class="site-version"></span></p>'

for root, dirs, files in os.walk(repo_dir):
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if '<span class="site-version">' not in content:
                new_content = pattern.sub(replacement, content)
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f"Updated footer in {path}")
