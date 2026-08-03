import os
import shutil
import json

data_dir = r"F:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Outdoor furniture product list and photos"
json_file = os.path.join(data_dir, "product_data.json")

# Load the JSON to get the list of SKUs
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract SKUs
skus = [p['supplier_code'] for p in data['products'] if p.get('supplier_code')]

# List all files
files = os.listdir(data_dir)
image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

moved_count = 0
for img in image_files:
    # Find the matching SKU for this image
    matched_sku = None
    for sku in skus:
        if img.startswith(sku):
            matched_sku = sku
            break
            
    if matched_sku:
        # Create folder if it doesn't exist
        sku_dir = os.path.join(data_dir, matched_sku)
        if not os.path.exists(sku_dir):
            os.makedirs(sku_dir)
            
        # Move file
        src = os.path.join(data_dir, img)
        dst = os.path.join(sku_dir, img)
        shutil.move(src, dst)
        moved_count += 1

print(f"Successfully moved {moved_count} images into their respective SKU folders.")
