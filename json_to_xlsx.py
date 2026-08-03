import json
import pandas as pd

def json_to_xlsx():
    input_file = "data/all_products_structured.json"
    output_file = "data/Sunnyward_Products_Master.xlsx"

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    products = data.get("products", [])
    
    flattened_data = []
    
    for p in products:
        dims = p.get("dimensions", {})
        if not dims:
            dims = {}
            
        logs = p.get("logistics", {})
        price = p.get("pricing", {})
        
        flat_p = {
            "ID": p.get("id"),
            "SKU": p.get("sku"),
            "Name": p.get("name"),
            "Brand": p.get("brand"),
            "Category": p.get("category"),
            "Sub-Category": p.get("sub_category"),
            "Collection": p.get("collection"),
            "Description": p.get("description"),
            "Materials": "\n".join(p.get("materials", [])),
            "Dimensions (Raw)": dims.get("raw", ""),
            "Dim Width": dims.get("w", ""),
            "Dim Depth": dims.get("d", ""),
            "Dim Height": dims.get("h", ""),
            "Dim Unit": dims.get("unit", ""),
            "CBM": logs.get("cbm", ""),
            "Capacity 40HQ": logs.get("capacity_40hq", ""),
            "Package": logs.get("package", ""),
            "Packaging Meas.": logs.get("packaging_measurement", ""),
            "FOB (USD)": price.get("fob_usd", ""),
            "MSRP": price.get("msrp", ""),
            "JP Price": price.get("jp_price", ""),
            "Specifications": "\n".join(p.get("specs", [])),
            "Origin": p.get("origin"),
            "Images": "\n".join(p.get("images", []))
        }
        flattened_data.append(flat_p)
        
    df = pd.DataFrame(flattened_data)
    
    # Save to excel
    writer = pd.ExcelWriter(output_file, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='All_Products')
    writer.close()
    
    print(f"Successfully exported {len(products)} products to {output_file}")

if __name__ == "__main__":
    json_to_xlsx()
