import os
import json
import re

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"

def get_dining_subcat(name, desc):
    n = (name + " " + desc).lower()
    if "wood" in n or "timber" in n: return "Wooden Chair"
    if "metal" in n or "steel" in n or "iron" in n: return "Metal Chair"
    if "plastic" in n or "pp" in n or "resin" in n or "polypropylene" in n: return "Plastic Chair"
    return "Upholstered Chair"

def get_stool_subcat(name, desc):
    n = (name + " " + desc).lower()
    if "counter" in n: return "Counter Stool"
    if "adjustable" in n or "lift" in n or "swivel" in n: return "Adjustable Stool"
    return "Bar Stool"

def get_lounge_subcat(name, desc):
    n = (name + " " + desc).lower()
    if "accent" in n: return "Accent Chair"
    if "recliner" in n or "ottoman" in n: return "Recliner"
    return "Armchair"

def get_outdoor_subcat(name, desc, old_subcat):
    n = (name + " " + desc + " " + old_subcat).lower()
    if "sofa" in n or "loveseat" in n or "daybed" in n: return "Outdoor Sofa"
    if "table" in n or "desk" in n: return "Outdoor Table"
    if "chair" in n or "bench" in n or "stool" in n: return "Outdoor Chair"
    return "Outdoor Chair"

def extract_collection_name(subcat_str):
    if not subcat_str:
        return ""
    # Look for patterns like "FOUNDATION COLLECTION", "ROPE COLLECTION GREIGE COLOR STOCK"
    s = subcat_str.upper()
    if "COLLECTION" in s:
        # Extract word before COLLECTION
        match = re.search(r'([A-Z0-9_-]+)\s+COLLECTION', s)
        if match:
            return match.group(1).capitalize()
    return ""

def cleanup_products():
    for lang in ['tw', 'en', 'jp']:
        path = os.path.join(repo_dir, lang, "products.json")
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            
        is_dict = isinstance(raw_data, dict)
        products = raw_data.get("products", []) if is_dict else raw_data
        
        cleaned_products = []
        
        for p in products:
            if not isinstance(p, dict):
                continue
                
            cat = p.get("category", "")
            subcat = p.get("sub_category") or p.get("subcat") or ""
            name = p.get("name", "")
            desc = p.get("description") or p.get("desc") or ""
            
            # --- 1. Dining, Stools, Lounge release ---
            if cat in ["Dining", "Stools", "Lounge"]:
                p["frontend_visible"] = True
                if cat == "Dining":
                    p["sub_category"] = get_dining_subcat(name, desc)
                elif cat == "Stools":
                    p["sub_category"] = get_stool_subcat(name, desc)
                elif cat == "Lounge":
                    p["sub_category"] = get_lounge_subcat(name, desc)
                    
            # --- 2. Outdoor cleanup ---
            elif cat == "Outdoor":
                # Save collection name
                col = extract_collection_name(subcat)
                if col:
                    p["collection"] = col
                p["sub_category"] = get_outdoor_subcat(name, desc, subcat)
                
            # --- 3. Old office merge & category redirect ---
            elif cat == "Office":
                # Redirect Office to Office_Desks or Office_Chairs
                n = (name + " " + desc).lower()
                # If it's a chair, move to Office_Chairs
                if "chair" in n or "stool" in n or "seating" in n:
                    p["category"] = "Office_Chairs"
                    # Determine subcat
                    if "mesh" in n: p["sub_category"] = "Mesh Chair"
                    elif "leather" in n or "pu" in n: p["sub_category"] = "Leather Chair"
                    elif "visitor" in n or "conference" in n: p["sub_category"] = "Visitor Chair"
                    else: p["sub_category"] = "Task Chair"
                # Else it's a table/storage, move to Office_Desks
                else:
                    p["category"] = "Office_Desks"
                    if "director" in n or "executive" in n or "boss" in n: p["sub_category"] = "Executive Desk"
                    elif "workstation" in n or "staff" in n: p["sub_category"] = "Staff Desk"
                    elif "cabinet" in n or "storage" in n or "pedestal" in n: p["sub_category"] = "Storage & Pedestals"
                    elif "conference" in n or "meeting" in n: p["sub_category"] = "Conference Table"
                    else: p["sub_category"] = "Office Table"
                    
            # --- 4. Subcat cleanup for existing split categories ---
            elif cat == "Office_Chairs" and subcat in ["Chair", "chair", ""]:
                p["sub_category"] = "Task Chair"
                
            elif cat == "Office_Desks" and subcat in ["Table", "table", ""]:
                p["sub_category"] = "Office Table"
                
            # --- 5. Stal Kimtar redirect to Dining and Lounge ---
            elif cat == "Metal_Frames":
                if subcat == "Designer Dining Chairs":
                    p["category"] = "Dining"
                else:
                    p["category"] = "Lounge"
                
            # Remove any residual old key variants to keep schema unified
            if "subcat" in p:
                del p["subcat"]
            if "tab" in p:
                del p["tab"]
                
            cleaned_products.append(p)
            
        if is_dict:
            raw_data["products"] = cleaned_products
            output_data = raw_data
        else:
            output_data = cleaned_products
            
        # Write back to products.json
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully cleaned database: {lang}/products.json")

if __name__ == "__main__":
    cleanup_products()
