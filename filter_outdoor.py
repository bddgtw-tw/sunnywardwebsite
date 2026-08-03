import json
import os

base_dir = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"
outdoor_json_path = os.path.join(base_dir, "data", "outdoor_products.json")

with open(outdoor_json_path, 'r', encoding='utf-8') as f:
    outdoor_data = json.load(f)
    
valid_skus = set()
for p in outdoor_data.get("products", []):
    sku = p.get("supplier_code", "")
    if sku and "Supplier code number" not in sku and "SKU" not in sku:
        valid_skus.add(sku)

print(f"Found {len(valid_skus)} valid outdoor SKUs from Excel.")

for lang in ['en', 'tw', 'jp']:
    path = os.path.join(base_dir, lang, "products.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        old_count = len(data)
        new_data = []
        for p in data:
            if p.get("tab") == "outdoor":
                if p.get("sku") in valid_skus:
                    new_data.append(p)
            else:
                new_data.append(p)
                
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
            
        print(f"{lang.upper()}: Reduced from {old_count} to {len(new_data)} items. Outdoor items: {len([p for p in new_data if p.get('tab') == 'outdoor'])}")
