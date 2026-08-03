import json
import re
import uuid

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
    # Fallback to just basic splitting if format is like 110x60x40cm
    match2 = re.search(r'(\d+(?:\.\d+)?)\s*[xX*]\s*(\d+(?:\.\d+)?)\s*[xX*]\s*(\d+(?:\.\d+)?)', dim_str)
    if match2:
         return {
            "raw": dim_str,
            "w": float(match2.group(1)),
            "d": float(match2.group(2)),
            "h": float(match2.group(3)),
            "unit": "cm" if "cm" in dim_str.lower() else "m" if "m" in dim_str.lower() else ""
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

def restructure_product(old_p, index):
    supplier_code = old_p.get("supplier_code", "").strip()
    if supplier_code == "Supplier code number": # skip header-like row
        return None
        
    desc, materials = parse_description_and_materials(old_p.get("description", ""))
    
    # Generate ID based on supplier code or use a fallback
    p_id = f"{supplier_code}" if supplier_code else f"prod_auto_{index}"
    
    try:
        cbm = float(old_p.get("cbm", 0))
    except (ValueError, TypeError):
        cbm = 0.0
        
    try:
        capacity_40hq = int(old_p.get("capacity_40hq", 0))
    except (ValueError, TypeError):
        capacity_40hq = 0
        
    try:
        fob = float(old_p.get("fob_usd", 0))
    except (ValueError, TypeError):
        fob = old_p.get("fob_usd", 0)

    new_p = {
        "id": p_id,
        "supplier_code": supplier_code,
        "name": old_p.get("name", "").strip(),
        "brand": old_p.get("brand", "Funife").strip() if old_p.get("brand") else "Funife",
        "category": "Outdoor",
        "collection": old_p.get("collection", "") or "",
        "description": desc,
        "materials": materials,
        "dimensions": parse_dimensions(old_p.get("dimensions", "")),
        "logistics": {
            "cbm": cbm,
            "capacity_40hq": capacity_40hq,
            "package": old_p.get("package", ""),
            "packaging_measurement": old_p.get("packaging_measurement", "")
        },
        "pricing": {
            "fob_usd": fob
        },
        "images": old_p.get("images", [])
    }
    return new_p

def main():
    input_file = "data/outdoor_products.json"
    output_file = "data/outdoor_products_structured.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    old_products = data.get("products", [])
    new_products = []
    
    for i, p in enumerate(old_products):
        restructured = restructure_product(p, i)
        if restructured:
            new_products.append(restructured)
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"products": new_products}, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully processed {len(new_products)} products.")
    print(f"Saved restructured data to {output_file}")

if __name__ == "__main__":
    main()
