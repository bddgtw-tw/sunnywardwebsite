import json
import os

base_dir = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"

for lang in ['tw', 'en', 'jp']:
    path = os.path.join(base_dir, lang, "products.json")
    if not os.path.exists(path): continue
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for p in data:
        # Sanitize single and double quotes to avoid JS onclick issues
        if p.get("name"):
            p["name"] = p["name"].replace("'", "’").replace('"', "”")
        if p.get("sku"):
            p["sku"] = p["sku"].replace("'", "’").replace('"', "”")
        
        # Also let's ensure no backticks are present that would break template literals
        if p.get("desc"):
            p["desc"] = p["desc"].replace("`", "'")
            
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Quotes fixed in all JSON files.")
