import os
import json

def deduplicate_products():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    languages = ['en', 'tw', 'jp']
    
    for lang in languages:
        json_path = os.path.join(base_dir, lang, "products.json")
        if not os.path.exists(json_path):
            continue
            
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        seen_skus = set()
        unique_products = []
        
        # In case it's a dict with 'products'
        products_list = data.get("products", []) if isinstance(data, dict) else data
        
        # We iterate in reverse to keep the LATEST/NEWEST added product (which would be the outdoor ones)
        # Wait, if we keep the latest, we want to iterate normally, but update if seen?
        # Let's keep the LAST occurrence of a SKU because my merge scripts usually appended the new ones.
        # Actually, let's just keep the FIRST occurrence and overwrite with any richer data, OR just keep the last occurrence.
        
        # Let's just do a dictionary keyed by SKU. The last one wins.
        sku_map = {}
        for p in products_list:
            sku = p.get('sku')
            if sku:
                # If it already exists, we prefer the one with images if possible
                if sku in sku_map:
                    old_p = sku_map[sku]
                    # If old has images and new doesn't, keep old's images
                    if old_p.get('images') and not p.get('images'):
                        p['images'] = old_p['images']
                sku_map[sku] = p
            else:
                unique_products.append(p)
                
        # Now rebuild the list
        # We want to maintain order, so let's keep the order of their FIRST appearance
        final_list = []
        seen = set()
        for p in products_list:
            sku = p.get('sku')
            if sku:
                if sku not in seen:
                    final_list.append(sku_map[sku])
                    seen.add(sku)
            else:
                final_list.append(p)
                
        if isinstance(data, dict):
            data['products'] = final_list
        else:
            data = final_list
            
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"Deduplicated {lang}/products.json. Reduced to {len(final_list)} products.")

if __name__ == "__main__":
    deduplicate_products()
