import os
import shutil
import json
import re

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"
rubberwood_raw = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Solid Rubberwood Photos"
metal_raw = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Stal Kimtar Photos"

rubberwood_dest = os.path.join(repo_dir, "Product_Images", "05_Solid_Rubberwood")
metal_dest = os.path.join(repo_dir, "Product_Images", "06_Metal_Frames")

os.makedirs(rubberwood_dest, exist_ok=True)
os.makedirs(metal_dest, exist_ok=True)

def extract_skus_and_images(raw_dir):
    sku_to_images = {}
    if not os.path.exists(raw_dir):
        return sku_to_images
        
    files = os.listdir(raw_dir)
    for f in files:
        if not f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            continue
            
        # Match pattern: SKU-Suffix.ext
        # e.g., SWFK-B001-1.jpg -> SKU is SWFK-B001, suffix is 1
        # e.g., SWS-100-1.png -> SKU is SWS-100, suffix is 1
        # Some might not have a suffix, e.g., SWS-100.png -> SKU is SWS-100
        name_part, ext = os.path.splitext(f)
        parts = name_part.split('-')
        
        if len(parts) >= 2:
            # Check if last part is a number (suffix)
            if parts[-1].isdigit() or (len(parts[-1]) <= 2 and parts[-1].isalnum()):
                sku = "-".join(parts[:-1])
            else:
                sku = name_part
        else:
            sku = name_part
            
        if sku not in sku_to_images:
            sku_to_images[sku] = []
        sku_to_images[sku].append(f)
        
    return sku_to_images

rubberwood_map = extract_skus_and_images(rubberwood_raw)
metal_map = extract_skus_and_images(metal_raw)

print(f"Extracted {len(rubberwood_map)} Rubberwood SKUs.")
print(f"Extracted {len(metal_map)} Metal Frame SKUs.")

def build_products(sku_map, raw_dir, dest_dir, category_name, rel_dest_path, lang_translations):
    products = []
    
    for sku, imgs in sku_map.items():
        images_paths = []
        
        # Sort and copy images
        for idx, img in enumerate(sorted(imgs)):
            src_path = os.path.join(raw_dir, img)
            _, ext = os.path.splitext(img)
            safe_sku = sku.replace("-", "_").lower()
            suffix = f"_{idx+1}" if len(imgs) > 1 else ""
            new_filename = f"{safe_sku}{suffix}{ext.lower()}"
            
            dest_path = os.path.join(dest_dir, new_filename)
            if not os.path.exists(dest_path):
                shutil.copy2(src_path, dest_path)
                
            # Prepend "../" for localized products.json
            rel_path = f"../{rel_dest_path}/{new_filename}"
            images_paths.append(rel_path)
            
        # Build language-specific names
        name = lang_translations.get("en", f"Component {sku}")
        tw_name = lang_translations.get("tw", f"配件 {sku}")
        jp_name = lang_translations.get("jp", f"部品 {sku}")
        
        product = {
            "id": sku,
            "sku": sku,
            "name": name,
            "brand": "Funife",
            "category": category_name, # e.g. "Rubberwood"
            "sub_category": "Component",
            "collection": "",
            "description": f"Component specifications and configurations for model {sku}.",
            "materials": ["Solid Wood" if "Rubberwood" in category_name else "Steel / Metal"],
            "dimensions": {
                "raw": "Dimensions TBD",
                "w": 0.0,
                "d": 0.0,
                "h": 0.0,
                "unit": ""
            },
            "logistics": {
                "cbm": 0.0,
                "capacity_40hq": 0,
                "package": "",
                "packaging_measurement": ""
            },
            "pricing": {
                "fob_usd": 0.0,
                "msrp": 0.0,
                "jp_price": ""
            },
            "images": images_paths,
            "specs": [],
            "origin": "Malaysia",
            "translations": {
                "tw": {
                    "name": tw_name,
                    "description": f"型號 {sku} 的配件規格與配置款式。"
                },
                "jp": {
                    "name": jp_name,
                    "description": f"型番 {sku} の部品仕様および構成。"
                }
            }
        }
        products.append(product)
        
    return products

# English/Chinese/Japanese placeholders
rubberwood_langs = {
    "en": "Solid Rubberwood Part",
    "tw": "實木橡膠木配件",
    "jp": "ラバーウッド部品"
}
metal_langs = {
    "en": "Stal Kimtar Base/Frame",
    "tw": "金屬鋼底座與腳架",
    "jp": "スチール製フレーム・底座"
}

rubberwood_products = build_products(
    rubberwood_map, rubberwood_raw, rubberwood_dest, 
    "Rubberwood", "Product_Images/05_Solid_Rubberwood", rubberwood_langs
)

metal_products = build_products(
    metal_map, metal_raw, metal_dest, 
    "Metal_Frames", "Product_Images/06_Metal_Frames", metal_langs
)

all_new_products = rubberwood_products + metal_products

# Merge into localized products.json
for lang in ['tw', 'en', 'jp']:
    target_path = os.path.join(repo_dir, lang, "products.json")
    if os.path.exists(target_path):
        with open(target_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            
        is_dict = isinstance(raw_data, dict)
        existing_products = raw_data.get("products", []) if is_dict else raw_data
        
        # Build language customized list
        lang_products = []
        for p in all_new_products:
            lp = p.copy()
            # Override translations if tw or jp
            if lang in ['tw', 'jp'] and "translations" in p:
                lp["name"] = p["translations"][lang]["name"]
                lp["description"] = p["translations"][lang]["description"]
            # remove translations field to keep json clean
            if "translations" in lp:
                del lp["translations"]
            lang_products.append(lp)
            
        new_skus = {item['sku'] for item in lang_products}
        filtered_products = [item for item in existing_products if isinstance(item, dict) and item.get('sku') not in new_skus]
        
        filtered_products.extend(lang_products)
        
        if is_dict:
            raw_data["products"] = filtered_products
            output_data = raw_data
        else:
            output_data = filtered_products
            
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully merged {len(lang_products)} new placeholders into {lang}/products.json.")

# Update HTML files with new categories
def update_html_categories():
    categories_to_add = {
        "tw": 'rubberwood: "實木與橡膠木配件",\n      metal_frames: "五金與鋼鐵腳架",',
        "en": 'rubberwood: "Rubberwood Components",\n      metal_frames: "Steel & Metal Frames",',
        "jp": 'rubberwood: "ラバーウッド部品",\n      metal_frames: "スチール・金属フレーム",'
    }
    
    for lang in ['tw', 'en', 'jp']:
        path = os.path.join(repo_dir, lang, "products.html")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Replace after office_desks line
            if 'rubberwood' not in content:
                content = content.replace(
                    'office_desks: ',
                    f'{categories_to_add[lang]}\n      office_desks: '
                )
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Added rubberwood & metal_frames tabs in {lang}/products.html")

update_html_categories()
