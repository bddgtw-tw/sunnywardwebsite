import os
import shutil
import pandas as pd
import json
import math

raw_dir_1 = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Office Chair Photo"
excel_1 = os.path.join(raw_dir_1, "2026.7.5 Funife Office_Chairs_KonstruktOS_PU+Mesh.xlsx")

raw_dir_2 = r"G:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Office Furniture Photo"
excel_2 = os.path.join(raw_dir_2, "2026.7.4 Office Furniture_KonstruktOS_Product_ KOS.xlsx")

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"
img_dest_dir = os.path.join(repo_dir, "Product_Images", "01_Office_Furniture")
json_path = os.path.join(repo_dir, "data", "all_products_structured.json")

os.makedirs(img_dest_dir, exist_ok=True)

def clean_val(val):
    if pd.isna(val):
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    return str(val).strip()

def process_excel(excel_path, raw_dir, category_name):
    print(f"Processing {excel_path}...")
    df = pd.read_excel(excel_path, header=1)
    
    # gather images in raw_dir
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
            
        product = {
            "category": category_name,
            "collection": current_collection,
            "supplier_code": code,
            "name": clean_val(row.iloc[2]),
            "description": clean_val(row.iloc[3]),
            "dimensions": clean_val(row.iloc[4]),
            "fob_usd": clean_val(row.iloc[5]),
            "unit": clean_val(row.iloc[6]),
            "package": clean_val(row.iloc[7]),
            "packaging_measurement": clean_val(row.iloc[8]),
            "cbm": clean_val(row.iloc[9]),
            "capacity_40hq": clean_val(row.iloc[10]),
            "brand": clean_val(row.iloc[11]),
            "supplier": clean_val(row.iloc[12]),
            "origin": clean_val(row.iloc[13]),
            "images": []
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
                    
                rel_path = f"Product_Images/01_Office_Furniture/{new_filename}"
                product["images"].append(rel_path)
                
        products.append(product)
        
    return products

products_1 = process_excel(excel_1, raw_dir_1, "Office")
products_2 = process_excel(excel_2, raw_dir_2, "Office")

new_products = products_1 + products_2

# Merge with existing JSON
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

existing_products = data.get("products", [])
# Remove old office products if they exist to avoid duplicates (based on supplier_code)
existing_codes = {p.get("supplier_code") for p in existing_products}

# Add new ones
added_count = 0
for np in new_products:
    if np["supplier_code"] not in existing_codes:
        existing_products.append(np)
        added_count += 1
    else:
        # Update existing
        for i, ep in enumerate(existing_products):
            if ep.get("supplier_code") == np["supplier_code"]:
                existing_products[i] = np
                added_count += 1
                break

data["products"] = existing_products

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Processed and merged {added_count} office furniture products.")
