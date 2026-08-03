import json
import os
import copy

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def sync_language_jsons():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    master_json_path = os.path.join(base_dir, "data", "all_products_structured.json")
    
    master_data = load_json(master_json_path)
    master_products = master_data.get("products", [])
    
    languages = ['en', 'tw', 'jp']
    
    for lang in languages:
        old_lang_path = os.path.join(base_dir, lang, "products.json")
        old_products = load_json(old_lang_path)
        
        # Build translation map
        trans_map = {}
        # some json might just be a list directly, some might be {"products": []}
        old_list = old_products.get("products", []) if isinstance(old_products, dict) else old_products
        
        for p in old_list:
            sku = p.get("sku")
            if sku:
                trans_map[sku] = {
                    "name": p.get("name", ""),
                    "desc": p.get("desc", ""),
                    "specs": p.get("specs", []),
                    "material": p.get("material", "")
                }
                
        new_lang_products = []
        for master_p in master_products:
            # Create a deep copy of the master product
            new_p = copy.deepcopy(master_p)
            sku = new_p.get("sku")
            
            # If we have translations for this SKU, apply them
            if sku in trans_map:
                t = trans_map[sku]
                if t["name"]: new_p["name"] = t["name"]
                if t["desc"]: new_p["description"] = t["desc"]
                if t["specs"]: new_p["specs"] = t["specs"]
                
                # Material mapping
                # If master has parsed materials, and translated material exists,
                # we might just replace it or append. 
                # Let's replace the materials array with the translated string as a single item if it exists and is meaningful.
                if t["material"]:
                    new_p["materials"] = [t["material"]]
            
            new_lang_products.append(new_p)
            
        # Save back
        save_json(old_lang_path, {"products": new_lang_products})
        print(f"Successfully synchronized {lang}/products.json ({len(new_lang_products)} items)")

if __name__ == "__main__":
    sync_language_jsons()
