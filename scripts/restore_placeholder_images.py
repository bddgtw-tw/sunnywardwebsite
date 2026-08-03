import os
import json

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"

def restore_placeholders():
    for lang in ['tw', 'en', 'jp']:
        path = os.path.join(repo_dir, lang, "products.json")
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            
        is_dict = isinstance(raw_data, dict)
        products = raw_data.get("products", []) if is_dict else raw_data
        
        count = 0
        for p in products:
            if not isinstance(p, dict):
                continue
                
            dq = p.get("data_quality")
            if dq and "removed_placeholder_images" in dq:
                removed_imgs = dq["removed_placeholder_images"]
                if removed_imgs:
                    # Restore to images if empty
                    if not p.get("images"):
                        p["images"] = list(removed_imgs)
                        count += 1
                        
        if is_dict:
            raw_data["products"] = products
            output_data = raw_data
        else:
            output_data = products
            
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully restored {count} placeholder images in {lang}/products.json")

if __name__ == "__main__":
    restore_placeholders()
