import json
import os

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"
all_products_json = os.path.join(repo_dir, "data", "all_products_structured.json")

# Load unified products
with open(all_products_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

office_products = [p for p in data.get("products", []) if p.get("category") == "Office"]

new_items = []
for p in office_products:
    sku = p.get("supplier_code", "")
    if not sku:
        continue
        
    specs = []
    if p.get("package"): specs.append(f"Package: {p.get('package')}")
    if p.get("packaging_measurement"): specs.append(f"Measurement: {p.get('packaging_measurement')}")
    if p.get("cbm"): specs.append(f"CBM: {p.get('cbm')}")
    if p.get("capacity_40hq"): specs.append(f"40HQ Capacity: {p.get('capacity_40hq')}")

    img_path = ""
    if p.get("images") and len(p.get("images")) > 0:
        # Prepend "../" because products.json is inside /tw or /en folders
        img_path = "../" + p["images"][0]
        
    new_item = {
        "sku": sku,
        "name": p.get("name", "Unnamed Office Furniture"),
        "subcat": p.get("collection") or "Office Furniture",
        "tab": "office",
        "dims": p.get("dimensions", ""),
        "desc": p.get("description", ""),
        "specs": specs,
        "material": p.get("description", "").split('\n')[0] if p.get("description") else "",
        "origin": p.get("origin", "Malaysia"),
        "price": str(p.get("fob_usd", "")),
        "jp_price": "",
        "img": img_path
    }
    new_items.append(new_item)

# Update localized products.json
for lang in ['tw', 'en', 'jp']:
    target_path = os.path.join(repo_dir, lang, "products.json")
    if os.path.exists(target_path):
        with open(target_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            
        is_dict = isinstance(raw_data, dict)
        existing_products = raw_data.get("products", []) if is_dict else raw_data
        
        new_skus = {item['sku'] for item in new_items}
        filtered_products = [item for item in existing_products if isinstance(item, dict) and item.get('sku') not in new_skus]
        
        filtered_products.extend(new_items)
        
        if is_dict:
            raw_data["products"] = filtered_products
            output_data = raw_data
        else:
            output_data = filtered_products
        
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"Updated {lang}/products.json with {len(new_items)} office products.")
