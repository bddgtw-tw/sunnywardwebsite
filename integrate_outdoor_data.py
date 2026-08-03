import os
import shutil
import json

src_dir = r"F:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\Outdoor furniture product list and photos"
src_json = os.path.join(src_dir, "product_data.json")

dest_base = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"
dest_images_dir = os.path.join(dest_base, "Product_Images", "Outdoor")
dest_data_dir = os.path.join(dest_base, "data")

# Create destination directories
os.makedirs(dest_images_dir, exist_ok=True)
os.makedirs(dest_data_dir, exist_ok=True)

# Read original JSON
with open(src_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data.get("products", [])

copied_folders = 0

for product in products:
    sku = product.get("supplier_code")
    if not sku:
        continue
        
    src_sku_dir = os.path.join(src_dir, sku)
    dest_sku_dir = os.path.join(dest_images_dir, sku)
    
    # If the SKU folder exists in source, copy it to destination
    if os.path.exists(src_sku_dir) and os.path.isdir(src_sku_dir):
        if not os.path.exists(dest_sku_dir):
            shutil.copytree(src_sku_dir, dest_sku_dir)
        copied_folders += 1
        
    # Update image paths in JSON
    updated_images = []
    for img in product.get("images", []):
        # We assume the images array currently just holds filenames
        new_path = f"Product_Images/Outdoor/{sku}/{img}"
        updated_images.append(new_path)
    
    product["images"] = updated_images

# Save updated JSON
dest_json_path = os.path.join(dest_data_dir, "outdoor_products.json")
with open(dest_json_path, 'w', encoding='utf-8') as f:
    json.dump({"products": products}, f, ensure_ascii=False, indent=2)

print(f"Integration complete! Copied {copied_folders} SKU folders.")
print(f"Updated JSON saved to {dest_json_path}")
