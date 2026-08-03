import os
import shutil
import pandas as pd
import json
import math
import re

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"

# Inputs
chair_excel = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Office Chair Photo\2026.7.5 Funife Office_Chairs_KonstruktOS_PU+Mesh.xlsx"
chair_raw_dir = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Office Chair Photo"

furniture_excel = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Office Furniture Photo\2026.7.4 Office Furniture_KonstruktOS_Product_ KOS.xlsx"
furniture_raw_dir = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Office Furniture Photo"

rubberwood_raw = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Solid Rubberwood Photos"
metal_raw = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Stal Kimtar Photos"

# Outputs
img_office_dir = os.path.join(repo_dir, "Product_Images", "01_Office_Furniture")
img_rubberwood_dir = os.path.join(repo_dir, "Product_Images", "05_Solid_Rubberwood")
img_metal_dir = os.path.join(repo_dir, "Product_Images", "06_Metal_Frames")

os.makedirs(img_office_dir, exist_ok=True)
os.makedirs(img_rubberwood_dir, exist_ok=True)
os.makedirs(img_metal_dir, exist_ok=True)

def clean_val(val):
    if pd.isna(val):
        return ""
    if isinstance(val, float) and math.isnan(val):
        return ""
    return str(val).strip()

def parse_dimensions(dim_str):
    if not dim_str:
        return {"raw": ""}
    match = re.search(r'W(\d+(?:\.\d+)?).*?D(\d+(?:\.\d+)?).*?H(\d+(?:\.\d+)?)', dim_str, re.IGNORECASE)
    if match:
        return {
            "raw": dim_str,
            "w": float(match.group(1)),
            "d": float(match.group(2)),
            "h": float(match.group(3)),
            "unit": "mm"
        }
    match2 = re.search(r'(\d+(?:\.\d+)?)\s*[xX*×]\s*(\d+(?:\.\d+)?)', dim_str)
    if match2:
        return {
            "raw": dim_str,
            "w": float(match2.group(1)),
            "d": float(match2.group(2)),
            "h": 0.0,
            "unit": "mm"
        }
    return {"raw": dim_str, "w": 0.0, "d": 0.0, "h": 0.0, "unit": ""}

def get_chair_subcat(name, desc):
    n = (name + " " + desc).lower()
    if "mesh" in n: return "Mesh Chair"
    if "leather" in n or "pu" in n: return "Leather Chair"
    if "visitor" in n or "conference" in n: return "Visitor Chair"
    return "Task Chair"

def get_desk_subcat(name, desc):
    n = (name + " " + desc).lower()
    if "director" in n or "executive" in n or "boss" in n: return "Executive Desk"
    if "workstation" in n or "staff" in n: return "Staff Desk"
    if "cabinet" in n or "storage" in n or "pedestal" in n or "side cabinet" in n: return "Storage & Pedestals"
    if "conference" in n or "meeting" in n: return "Conference Table"
    return "Office Table"

def process_office_excels():
    products = []
    
    # 1. Chairs
    df1 = pd.read_excel(chair_excel, header=1)
    chair_files = [f for f in os.listdir(chair_raw_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    for idx, row in df1.iterrows():
        code = clean_val(row.iloc[1])
        if not code or code == 'Supplier code number':
            continue
        
        name = clean_val(row.iloc[2])
        desc = clean_val(row.iloc[3])
        subcat = get_chair_subcat(name, desc)
        
        product = build_base_product(code, name, desc, "Office_Chairs", subcat, row, chair_raw_dir, chair_files, img_office_dir, "Product_Images/01_Office_Furniture")
        products.append(product)
        
    # 2. Desks
    df2 = pd.read_excel(furniture_excel, header=1)
    furniture_files = [f for f in os.listdir(furniture_raw_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    for idx, row in df2.iterrows():
        code = clean_val(row.iloc[1])
        if not code or code == 'Supplier code number':
            continue
            
        name = clean_val(row.iloc[2])
        desc = clean_val(row.iloc[3])
        subcat = get_desk_subcat(name, desc)
        
        product = build_base_product(code, name, desc, "Office_Desks", subcat, row, furniture_raw_dir, furniture_files, img_office_dir, "Product_Images/01_Office_Furniture")
        products.append(product)
        
    return products

def build_base_product(code, name, desc, category, subcat, row, raw_dir, files_list, dest_dir, rel_dest_path):
    try: cbm = float(row.iloc[9])
    except: cbm = 0.0
    if math.isnan(cbm): cbm = 0.0
        
    try: cap = int(row.iloc[10])
    except: cap = 0
        
    try: fob = float(row.iloc[5])
    except: fob = 0.0
    if math.isnan(fob): fob = 0.0
        
    images_paths = []
    matching_images = [img for img in files_list if img.startswith(code)]
    for i, img in enumerate(sorted(matching_images)):
        src_path = os.path.join(raw_dir, img)
        _, ext = os.path.splitext(img)
        safe_sku = code.replace("-", "_").lower()
        suffix = f"_{i+1}" if len(matching_images) > 1 else ""
        new_filename = f"{safe_sku}{suffix}{ext.lower()}"
        
        dest_path = os.path.join(dest_dir, new_filename)
        if not os.path.exists(dest_path):
            shutil.copy2(src_path, dest_path)
            
        images_paths.append(f"../{rel_dest_path}/{new_filename}")
        
    return {
        "id": code,
        "sku": code,
        "name": name,
        "brand": clean_val(row.iloc[11]) or "Funife",
        "category": category,
        "sub_category": subcat,
        "collection": "",
        "description": desc,
        "materials": [desc.split('\n')[0]] if desc else [],
        "dimensions": parse_dimensions(clean_val(row.iloc[4])),
        "logistics": {
            "cbm": cbm,
            "capacity_40hq": cap,
            "package": clean_val(row.iloc[7]),
            "packaging_measurement": clean_val(row.iloc[8])
        },
        "pricing": {
            "fob_usd": fob,
            "msrp": 0.0,
            "jp_price": ""
        },
        "images": images_paths,
        "specs": [],
        "origin": clean_val(row.iloc[13]) or "Malaysia"
    }

def extract_skus_and_images(raw_dir):
    sku_to_images = {}
    if not os.path.exists(raw_dir):
        return sku_to_images
    for f in os.listdir(raw_dir):
        if not f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            continue
        name_part, ext = os.path.splitext(f)
        parts = name_part.split('-')
        if len(parts) >= 2:
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

def process_unstructured():
    products = []
    
    # 1. Rubberwood
    rw_map = extract_skus_and_images(rubberwood_raw)
    for sku, imgs in rw_map.items():
        subcat = "Dining Tables & Desks"
        if sku.startswith("SWFK-B"): subcat = "Cabinets & Chests"
        elif sku.startswith("SWFK-L"): subcat = "TV Consoles & Sideboards"
        
        images_paths = []
        for i, img in enumerate(sorted(imgs)):
            src_path = os.path.join(rubberwood_raw, img)
            _, ext = os.path.splitext(img)
            safe_sku = sku.replace("-", "_").lower()
            suffix = f"_{i+1}" if len(imgs) > 1 else ""
            new_filename = f"{safe_sku}{suffix}{ext.lower()}"
            dest_path = os.path.join(img_rubberwood_dir, new_filename)
            if not os.path.exists(dest_path):
                shutil.copy2(src_path, dest_path)
            images_paths.append(f"../Product_Images/05_Solid_Rubberwood/{new_filename}")
            
        products.append(build_placeholder_dict(sku, "Rubberwood", subcat, images_paths, "Solid Rubberwood Furniture", "橡膠木實木家具", "ラバーウッド無垢家具"))
        
    # 2. Metal
    m_map = extract_skus_and_images(metal_raw)
    for sku, imgs in m_map.items():
        subcat = "Lounge & Accent Chairs"
        if sku.startswith("SWS-E"): subcat = "Designer Dining Chairs"
        
        images_paths = []
        for i, img in enumerate(sorted(imgs)):
            src_path = os.path.join(metal_raw, img)
            _, ext = os.path.splitext(img)
            safe_sku = sku.replace("-", "_").lower()
            suffix = f"_{i+1}" if len(imgs) > 1 else ""
            new_filename = f"{safe_sku}{suffix}{ext.lower()}"
            dest_path = os.path.join(img_metal_dir, new_filename)
            if not os.path.exists(dest_path):
                shutil.copy2(src_path, dest_path)
            images_paths.append(f"../Product_Images/06_Metal_Frames/{new_filename}")
            
        products.append(build_placeholder_dict(sku, "Metal_Frames", subcat, images_paths, "Steel-Framed Designer Chair", "鋼製腳座設計椅", "スチール脚デザインチェア"))
        
    return products

def build_placeholder_dict(sku, category, subcat, images, en_name, tw_name, jp_name):
    return {
        "id": sku,
        "sku": sku,
        "name": en_name,
        "brand": "Funife",
        "category": category,
        "sub_category": subcat,
        "collection": "",
        "description": f"Component specifications for model {sku}.",
        "materials": ["Solid Wood" if category == "Rubberwood" else "Steel / Metal"],
        "dimensions": {"raw": "Dimensions TBD", "w": 0.0, "d": 0.0, "h": 0.0, "unit": ""},
        "logistics": {"cbm": 0.0, "capacity_40hq": 0, "package": "", "packaging_measurement": ""},
        "pricing": {"fob_usd": 0.0, "msrp": 0.0, "jp_price": ""},
        "images": images,
        "specs": [],
        "origin": "Malaysia",
        "translations": {
            "tw": {"name": f"{tw_name} {sku}", "description": f"型號 {sku} 的規格款式。"},
            "jp": {"name": f"{jp_name} {sku}", "description": f"型番 {sku} の部品仕様。"}
        }
    }

def main():
    print("Reprocessing all databases with smart subcategories...")
    office_products = process_office_excels()
    unstructured_products = process_unstructured()
    
    new_products_pool = office_products + unstructured_products
    
    for lang in ['tw', 'en', 'jp']:
        target_path = os.path.join(repo_dir, lang, "products.json")
        if os.path.exists(target_path):
            with open(target_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
            is_dict = isinstance(raw_data, dict)
            existing_products = raw_data.get("products", []) if is_dict else raw_data
            
            # Map new products with translations
            lang_new_products = []
            for p in new_products_pool:
                lp = p.copy()
                if lang in ['tw', 'jp'] and "translations" in p:
                    lp["name"] = p["translations"][lang]["name"]
                    lp["description"] = p["translations"][lang]["description"]
                if "translations" in lp:
                    del lp["translations"]
                lang_new_products.append(lp)
                
            new_skus = {item['sku'] for item in lang_new_products}
            filtered_products = [item for item in existing_products if isinstance(item, dict) and item.get('sku') not in new_skus]
            filtered_products.extend(lang_new_products)
            
            if is_dict:
                raw_data["products"] = filtered_products
                output_data = raw_data
            else:
                output_data = filtered_products
                
            with open(target_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
                
            print(f"Updated {lang}/products.json with {len(lang_new_products)} office, rubberwood and metal products with sub_category.")

if __name__ == "__main__":
    main()
