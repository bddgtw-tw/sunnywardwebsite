import json
import re

def parse_dimensions(dim_str):
    if not dim_str:
        return None
    
    # Try to extract W, D, H values
    match = re.search(r'W(\d+(?:\.\d+)?).*?D(\d+(?:\.\d+)?).*?H(\d+(?:\.\d+)?)', dim_str, re.IGNORECASE)
    if match:
        return {
            "raw": dim_str,
            "w": float(match.group(1)),
            "d": float(match.group(2)),
            "h": float(match.group(3)),
            "unit": "cm" if "cm" in dim_str.lower() else ""
        }
        
    # Try simple LxW
    match2 = re.search(r'(\d+(?:\.\d+)?)\s*[xX*×]\s*(\d+(?:\.\d+)?)', dim_str)
    if match2:
        return {
            "raw": dim_str,
            "w": float(match2.group(1)),
            "d": float(match2.group(2)),
            "h": 0,
            "unit": "cm" if "cm" in dim_str.lower() else ""
        }
        
    return {"raw": dim_str}

def parse_description_and_materials(desc_str):
    if not desc_str:
        return "", []
    
    materials = []
    desc_lines = []
    
    for line in desc_str.split('\n'):
        line = line.strip()
        if not line:
            continue
        lower_line = line.lower()
        if lower_line.startswith("material:") or lower_line.startswith("seat & back cushion:") or lower_line.startswith("top:"):
            materials.append(line)
        else:
            desc_lines.append(line)
            
    return "\n".join(desc_lines), materials

def process_outdoor_product(old_p, index):
    supplier_code = old_p.get("supplier_code", "").strip()
    if supplier_code == "Supplier code number":
        return None
        
    desc, materials = parse_description_and_materials(old_p.get("description", ""))
    
    p_id = f"{supplier_code}" if supplier_code else f"prod_outdoor_{index}"
    
    try: cbm = float(old_p.get("cbm", 0))
    except: cbm = 0.0
        
    try: cap = int(old_p.get("capacity_40hq", 0))
    except: cap = 0
        
    try: fob = float(old_p.get("fob_usd", 0))
    except: fob = old_p.get("fob_usd", 0)

    return {
        "id": p_id,
        "sku": supplier_code,
        "name": old_p.get("name", "").strip(),
        "brand": old_p.get("brand", "Funife").strip() if old_p.get("brand") else "Funife",
        "category": "Outdoor",
        "sub_category": "",
        "collection": old_p.get("collection", "") or "",
        "description": desc,
        "materials": materials,
        "dimensions": parse_dimensions(old_p.get("dimensions", "")),
        "logistics": {
            "cbm": cbm,
            "capacity_40hq": cap,
            "package": old_p.get("package", ""),
            "packaging_measurement": old_p.get("packaging_measurement", "")
        },
        "pricing": {
            "fob_usd": fob,
            "msrp": 0,
            "jp_price": ""
        },
        "images": old_p.get("images", []),
        "specs": [],
        "origin": old_p.get("origin", "China")
    }

def process_general_product(old_p, index):
    sku = old_p.get("sku", "").strip()
    p_id = f"{sku}" if sku else f"prod_gen_{index}"
    
    desc = old_p.get("desc", "").strip()
    materials = [old_p.get("material", "")] if old_p.get("material") else []
    
    try: price = float(old_p.get("price", 0))
    except: price = 0
    
    images = []
    if old_p.get("img"):
        images.append(old_p.get("img"))
        
    cat = old_p.get("tab", "").capitalize()
    if not cat: cat = "General"

    return {
        "id": p_id,
        "sku": sku,
        "name": old_p.get("name", "").strip(),
        "brand": "Funife", # Default
        "category": cat,
        "sub_category": old_p.get("subcat", ""),
        "collection": "",
        "description": desc,
        "materials": materials,
        "dimensions": parse_dimensions(old_p.get("dims", "")),
        "logistics": {
            "cbm": 0.0,
            "capacity_40hq": 0,
            "package": "",
            "packaging_measurement": ""
        },
        "pricing": {
            "fob_usd": 0,
            "msrp": price,
            "jp_price": old_p.get("jp_price", "")
        },
        "images": images,
        "specs": old_p.get("specs", []),
        "origin": old_p.get("origin", "")
    }

def main():
    unified_products = []
    
    # 1. Process general products (en/products.json)
    try:
        with open("en/products.json", 'r', encoding='utf-8') as f:
            gen_data = json.load(f)
            for i, p in enumerate(gen_data):
                unified = process_general_product(p, i)
                unified_products.append(unified)
        print(f"Processed {len(gen_data)} general products.")
    except Exception as e:
        print(f"Error processing en/products.json: {e}")

    # 2. Process outdoor products (data/outdoor_products.json)
    try:
        with open("data/outdoor_products.json", 'r', encoding='utf-8') as f:
            out_data = json.load(f)
            out_list = out_data.get("products", [])
            for i, p in enumerate(out_list):
                unified = process_outdoor_product(p, i)
                if unified:
                    unified_products.append(unified)
        print(f"Processed {len(out_list)} outdoor products.")
    except Exception as e:
        print(f"Error processing data/outdoor_products.json: {e}")
        
    # Write unified data
    output_file = "data/all_products_structured.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"products": unified_products}, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully processed a total of {len(unified_products)} products.")
    print(f"Saved unified restructured data to {output_file}")

if __name__ == "__main__":
    main()
