import os

def add_cache_buster():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    languages = ['en', 'tw', 'jp']
    
    for lang in languages:
        filepath = os.path.join(base_dir, lang, "products.html")
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Add cache buster to fetch
        target = "await fetch('./products.json');"
        replacement = "await fetch('./products.json?v=' + new Date().getTime());"
        
        if target in content:
            content = content.replace(target, replacement)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added cache-buster to {lang}/products.html")
        else:
            print(f"Target not found in {lang}/products.html")

if __name__ == "__main__":
    add_cache_buster()
