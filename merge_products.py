import json
import os

# Paths
base_dir = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"
outdoor_json_path = os.path.join(base_dir, "data", "outdoor_products.json")

# Load outdoor products
with open(outdoor_json_path, 'r', encoding='utf-8') as f:
    outdoor_data = json.load(f)

new_items = []
for p in outdoor_data.get("products", []):
    if not p.get("supplier_code"):
        continue
        
    specs = []
    if p.get("package"): specs.append(f"Package: {p.get('package')}")
    if p.get("packaging_measurement"): specs.append(f"Measurement: {p.get('packaging_measurement')}")
    if p.get("cbm"): specs.append(f"CBM: {p.get('cbm')}")
    if p.get("capacity_40hq"): specs.append(f"40HQ Capacity: {p.get('capacity_40hq')}")

    img_path = ""
    if p.get("images") and len(p.get("images")) > 0:
        # outdoor JSON already has "Product_Images/Outdoor/...", we just need to prepend "../" 
        # since the products.json is inside tw/ or en/ which is one level down.
        img_path = "../" + p["images"][0]
        
    new_item = {
        "sku": p.get("supplier_code", ""),
        "name": p.get("name", "Unnamed Outdoor Furniture"),
        "subcat": p.get("collection", "Outdoor Furniture"),
        "tab": "outdoor",
        "dims": p.get("dimensions", ""),
        "desc": p.get("description", ""),
        "specs": specs,
        "material": p.get("description", "").split('\n')[0] if p.get("description") else "",
        "origin": p.get("origin", "China"),
        "price": str(p.get("fob_usd", "")),
        "jp_price": "",
        "img": img_path
    }
    new_items.append(new_item)

# Update each locale's products.json
for lang in ['tw', 'en', 'jp']:
    target_path = os.path.join(base_dir, lang, "products.json")
    if os.path.exists(target_path):
        with open(target_path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            
        # Optional: Prevent duplicates if we run this twice.
        # Filter out existing items that have tab == 'outdoor' if they match our SKUs, 
        # but to be safe, just remove all 'outdoor' items first to do a clean replace,
        # or assume we only append if SKU not present.
        
        # We will remove existing outdoor items that match these SKUs to prevent duplication
        new_skus = {item['sku'] for item in new_items}
        filtered_data = [item for item in existing_data if item.get('sku') not in new_skus]
        
        filtered_data.extend(new_items)
        
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=2)
            
        print(f"Updated {target_path} with {len(new_items)} outdoor products.")

