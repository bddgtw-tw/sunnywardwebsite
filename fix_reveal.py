import os
import re

base_dir = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"

for lang in ['en', 'tw', 'jp']:
    path = os.path.join(base_dir, lang, "products.html")
    if not os.path.exists(path):
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove 'reveal' class from products-stage so it doesn't get hidden by default
    content = content.replace('class="products-stage reveal delay-1"', 'class="products-stage"')
    
    # 2. As a fallback, also manually make sure it's revealed in JS
    if "stageContainer.innerHTML = stageHtml;" in content:
        if "stageContainer.classList.add('revealed');" not in content:
            content = content.replace(
                "stageContainer.innerHTML = stageHtml;",
                "stageContainer.innerHTML = stageHtml;\n      stageContainer.classList.add('revealed');"
            )
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed products-stage visibility in all HTML files.")
