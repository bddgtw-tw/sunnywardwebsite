import os
import re

def update_html_files():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    languages = ['en', 'tw', 'jp']
    
    replacements = [
        # Image access (handling empty check)
        (r"b\.img\s*&&\s*b\.img\.trim\(\)", r"b.images && b.images.length > 0"),
        (r"a\.img\s*&&\s*a\.img\.trim\(\)", r"a.images && a.images.length > 0"),
        (r"p\.img\s*&&\s*p\.img\.trim\(\)", r"p.images && p.images.length > 0"),
        (r"src=\"\$\{p\.img\}\"", r"src=\"${p.images[0]}\""),
        (r"p\.img;", r"(p.images && p.images.length > 0 ? p.images[0] : '');"),
        (r"p\.img\s*=", r"(p.images && p.images.length > 0 ? p.images[0] : '') ="),
        
        # Category/Tab mapping
        (r"p\.tab", r"(p.category ? p.category.toLowerCase() : '')"),
        
        # Properties
        (r"\$\{p\.desc\}", r"${p.description}"),
        (r"p\.desc;", r"p.description;"),
        
        (r"\$\{p\.dims\}", r"${p.dimensions ? p.dimensions.raw : ''}"),
        (r"p\.dims;", r"(p.dimensions ? p.dimensions.raw : '');"),
        
        (r"p\.material;", r"(p.materials ? p.materials.join(' | ') : '');"),
        
        # Also need to fix outdoor.html if it has similar logic, but let's focus on products.html
    ]

    for lang in languages:
        filepath = os.path.join(base_dir, lang, "products.html")
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for old, new in replacements:
            content = re.sub(old, new, content)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Updated {lang}/products.html")
        
    # Also update outdoor.html in root
    outdoor_path = os.path.join(base_dir, "outdoor.html")
    if os.path.exists(outdoor_path):
        with open(outdoor_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for old, new in replacements:
            content = re.sub(old, new, content)
            
        with open(outdoor_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated outdoor.html")

if __name__ == "__main__":
    update_html_files()
