import pandas as pd
import json
import os
import math

data_dir = r"F:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Outdoor furniture product list and photos"
excel_file = os.path.join(data_dir, "Funife outdoor furniture export product list for Konstrukt.os.xlsx")

# List all image files
files = os.listdir(data_dir)
image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

df = pd.read_excel(excel_file, header=1) # The headers are on the 2nd row (index 1)

products = []
current_collection = None

def clean_val(val):
    if pd.isna(val):
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    return str(val).strip()

for index, row in df.iterrows():
    photo_col = row.iloc[0]
    code = clean_val(row.iloc[1])
    
    if pd.isna(row.iloc[1]) or str(row.iloc[1]).strip() == '' or str(row.iloc[1]) == 'nan':
        # Might be a collection name
        if pd.notna(photo_col) and str(photo_col).strip() != '' and str(photo_col).strip() != 'nan':
            current_collection = str(photo_col).strip()
        continue
    
    # It's a product
    product = {
        "collection": current_collection,
        "supplier_code": code,
        "name": clean_val(row.iloc[2]),
        "description": clean_val(row.iloc[3]),
        "dimensions": clean_val(row.iloc[4]),
        "fob_usd": clean_val(row.iloc[5]),
        "package": clean_val(row.iloc[6]),
        "packaging_measurement": clean_val(row.iloc[7]),
        "cbm": clean_val(row.iloc[8]),
        "capacity_40hq": clean_val(row.iloc[9]),
        "brand": clean_val(row.iloc[10]),
        "supplier": clean_val(row.iloc[11]),
        "origin": clean_val(row.iloc[12]),
        "images": []
    }
    
    # Find matching images
    if code:
        matching_images = [img for img in image_files if img.startswith(code)]
        product["images"] = sorted(matching_images)
        
    products.append(product)

output_file = r"C:\Users\bddgt\.gemini\antigravity\brain\a11d7668-8efd-43c2-81b6-b3ddf730d77e\product_data.json"

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({"products": products}, f, ensure_ascii=False, indent=2)

print(f"Successfully parsed {len(products)} products and saved to JSON.")
