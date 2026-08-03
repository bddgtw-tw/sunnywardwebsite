import os
import shutil
import pandas as pd
import json
import math
import re

raw_dir_1 = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Office Chair Photo"
excel_1 = os.path.join(raw_dir_1, "2026.7.5 Funife Office_Chairs_KonstruktOS_PU+Mesh.xlsx")

raw_dir_2 = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Office Furniture Photo"
excel_2 = os.path.join(raw_dir_2, "2026.7.4 Office Furniture_KonstruktOS_Product_ KOS.xlsx")

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"
img_dest_dir = os.path.join(repo_dir, "Product_Images", "01_Office_Furniture")

os.makedirs(img_dest_dir, exist_ok=True)

def clean_val(val):
    if pd.isna(val):
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    return str(val).strip()

def parse_dimensions(dim_str):
    if not dim_str:
        return {"raw": ""}
    
    # Check for W... D... H...
    match = re.search(r'W(\d+(?:\.\d+)?).*?D(\d+(?:\.\d+)?).*?H(\d+(?:\.\d+)?)', dim_str, re.IGNORECASE)
    if match:
        return {
            "raw": dim_str,
            "w": float(match.group(1)),
            "d": float(match.group(2)),
            "h": float(match.group(3)),
            "unit": "mm"
        }
        
    # Check for LxW
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

def process_excel_unified(excel_path, raw_dir, sub_cat):
    print(f"Parsing {excel_path} for unified schema...")
    df = pd.read_excel(excel_path, header=1)
    
    files = os.listdir(raw_dir)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    products = []
    current_collection = None
    
    for index, row in df.iterrows():
        photo_col = row.iloc[0]
        code = clean_val(row.iloc[1])
        
        if pd.isna(row.iloc[1]) or str(row.iloc[1]).strip() == '' or str(row.iloc[1]) == 'nan':
            if pd.notna(photo_col) and str(photo_col).strip() != '' and str(photo_col).strip() != 'nan':
                current_collection = str(photo_col).strip()
            continue
            
        desc = clean_val(row.iloc[3]) or ""
        materials = [desc.split('\n')[0]] if desc else []
        
        cbm_val = row.iloc[9]
        if pd.isna(cbm_val):
            cbm = 0.0
        else:
            try: cbm = float(cbm_val)
            except: cbm = 0.0
            if math.isnan(cbm):
                cbm = 0.0
            
        cap_val = row.iloc[10]
        if pd.isna(cap_val):
            cap = 0
        else:
            try: cap = int(cap_val)
            except: cap = 0
            
        fob_val = row.iloc[5]
        if pd.isna(fob_val):
            fob = 0.0
        else:
            try: fob = float(fob_val)
            except: fob = 0.0
            if math.isnan(fob):
                fob = 0.0
            
        product = {
            "id": code,
            "sku": code,
            "name": clean_val(row.iloc[2]),
            "brand": clean_val(row.iloc[11]) or "Funife",
            "category": "Office",
            "sub_category": sub_cat,
            "collection": current_collection or "",
            "description": desc,
            "materials": materials,
            "dimensions": parse_dimensions(clean_val(row.iloc[4])),
            "logistics": {
                "cbm": cbm,
                "capacity_40hq": cap,
                "package": clean_val(row.iloc[7]) or "",
                "packaging_measurement": clean_val(row.iloc[8]) or ""
            },
            "pricing": {
                "fob_usd": fob,
                "msrp": 0.0,
                "jp_price": ""
            },
            "images": [],
            "specs": [],
            "origin": clean_val(row.iloc[13]) or "Malaysia"
        }
        
        if code:
            matching_images = [img for img in image_files if img.startswith(code)]
            for idx, img in enumerate(sorted(matching_images)):
                src_path = os.path.join(raw_dir, img)
                _, ext = os.path.splitext(img)
                safe_sku = code.replace("-", "_").lower()
                suffix = f"_{idx+1}" if len(matching_images) > 1 else ""
                new_filename = f"{safe_sku}{suffix}{ext.lower()}"
                
                dest_path = os.path.join(img_dest_dir, new_filename)
                if not os.path.exists(dest_path):
                    shutil.copy2(src_path, dest_path)
                    
                # Store relative path for localized products.json
                rel_path = f"../Product_Images/01_Office_Furniture/{new_filename}"
                product["images"].append(rel_path)
                
        products.append(product)
        
    return products

# Process both excels using correct sub-categories
office_chairs = process_excel_unified(excel_1, raw_dir_1, "Chair")
for p in office_chairs:
    p["category"] = "Office_Chairs"

office_furniture = process_excel_unified(excel_2, raw_dir_2, "Table")
for p in office_furniture:
    p["category"] = "Office_Desks"

new_products = office_chairs + office_furniture

# Merge intoLocalized products.json files
for lang in ['tw', 'en', 'jp']:
    target_path = os.path.join(repo_dir, lang, "products.json")
    if os.path.exists(target_path):
        with open(target_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            
        is_dict = isinstance(raw_data, dict)
        existing_products = raw_data.get("products", []) if is_dict else raw_data
        
        new_skus = {item['sku'] for item in new_products}
        filtered_products = [item for item in existing_products if isinstance(item, dict) and item.get('sku') not in new_skus]
        
        filtered_products.extend(new_products)
        
        if is_dict:
            raw_data["products"] = filtered_products
            output_data = raw_data
        else:
            output_data = filtered_products
            
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully integrated {len(new_products)} products into {lang}/products.json in UNIFIED schema.")
