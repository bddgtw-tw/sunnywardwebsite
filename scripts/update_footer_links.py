import os
import re

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"

def update_footers():
    langs = ['tw', 'en', 'jp']
    
    # Pattern to match onclick="switchCategory('category_key');return false;"
    # Matches href="#" too
    pattern = r'href="#"\s+onclick="switchCategory\(\'(\w+)\'\);\s*return\s+false;"'
    
    for lang in langs:
        lang_dir = os.path.join(repo_dir, lang)
        if not os.path.exists(lang_dir):
            continue
            
        for file in os.listdir(lang_dir):
            if not file.endswith(".html"):
                continue
                
            path = os.path.join(lang_dir, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Replace pattern
            new_content = re.sub(pattern, r'href="products.html?category=\1"', content)
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated footer links in {lang}/{file}")

if __name__ == "__main__":
    update_footers()
