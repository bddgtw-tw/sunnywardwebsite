import json
import os
import shutil

def get_target_folder(category):
    cat_lower = category.lower()
    if 'office' in cat_lower or 'table' in cat_lower or 'chair' in cat_lower:
        return '01_Office_Furniture'
    elif 'commercial' in cat_lower or 'dining' in cat_lower:
        return '02_Commercial_Furniture'
    elif 'outdoor' in cat_lower:
        return '03_Outdoor_Furniture'
    else:
        return '04_Commercial_Equipment'

def organize_images():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    json_path = os.path.join(base_dir, "data", "all_products_structured.json")
    img_base_dir = os.path.join(base_dir, "Product_Images")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    products = data.get("products", [])
    
    # Ensure target directories exist
    target_folders = [
        "01_Office_Furniture",
        "02_Commercial_Furniture",
        "03_Outdoor_Furniture",
        "04_Commercial_Equipment"
    ]
    for folder in target_folders:
        os.makedirs(os.path.join(img_base_dir, folder), exist_ok=True)
        
    processed_count = 0
    missing_count = 0
    
    for p in products:
        sku = p.get("sku", "")
        if not sku:
            continue
            
        category = p.get("category", "")
        target_folder = get_target_folder(category)
        
        old_images = p.get("images", [])
        new_images = []
        
        for idx, old_img_path in enumerate(old_images):
            # Skip external URLs
            if old_img_path.startswith("http"):
                new_images.append(old_img_path)
                continue
                
            # Clean up the path
            clean_path = old_img_path.replace("../", "").replace("/", "\\")
            if clean_path.startswith("Product_Images\\"):
                clean_path = clean_path.replace("Product_Images\\", "", 1)
                
            source_abs_path = os.path.join(img_base_dir, clean_path)
            
            if os.path.exists(source_abs_path):
                # Determine extension
                _, ext = os.path.splitext(source_abs_path)
                if not ext:
                    ext = ".jpg"
                    
                # New filename: sku_1.jpg, sku_2.jpg
                safe_sku = sku.replace("-", "_").lower()
                suffix = f"_{idx+1}" if len(old_images) > 1 else ""
                new_filename = f"{safe_sku}{suffix}{ext}"
                
                target_rel_path = f"Product_Images/{target_folder}/{new_filename}"
                target_abs_path = os.path.join(img_base_dir, target_folder, new_filename)
                
                # Copy file if it's not already in the exact same place with same name
                if source_abs_path != target_abs_path:
                    try:
                        shutil.copy2(source_abs_path, target_abs_path)
                    except Exception as e:
                        print(f"Error copying {source_abs_path} to {target_abs_path}: {e}")
                        
                new_images.append(target_rel_path)
                processed_count += 1
            else:
                # File not found locally, keep original path but warn
                # print(f"Warning: Image not found - {source_abs_path}")
                new_images.append(old_img_path)
                missing_count += 1
                
        p["images"] = new_images

    # Save updated JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({"products": products}, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully processed and organized {processed_count} local images.")
    if missing_count > 0:
        print(f"Note: {missing_count} images were not found locally (might be URLs or missing files).")
        
    # Re-run json_to_xlsx if it exists
    try:
        import json_to_xlsx
        json_to_xlsx.json_to_xlsx()
    except Exception as e:
        print(f"Could not automatically update XLSX: {e}")

if __name__ == "__main__":
    organize_images()
