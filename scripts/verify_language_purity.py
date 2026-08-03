import json
import re
from pathlib import Path

base_dir = Path(__file__).resolve().parents[1]

# Whitelist for TW and JP
whitelist = [
    "Sunnyward", "Lagoon", "Mobellio", "Uno", "FRP", "MFC", "SKU", "OAK",
    "Aluminum", "Balau", "Wood", "Shorea", "HQ", "CBM", "Package", 
    "Measurement", "Capacity", "Approx", "Max", "Batyline", "AE", "China"
]

def contains_cjk(text):
    # Regex to match Chinese/Japanese characters
    return bool(re.search(r'[\u4e00-\u9fff\u3040-\u30ff]', text))

def check_en(data):
    errors = []
    for p in data:
        for field in ['name', 'desc', 'origin', 'dims', 'material']:
            val = p.get(field, "")
            if contains_cjk(val):
                errors.append(f"EN JSON - CJK found in {p.get('sku')} [{field}]: {val}")
        for idx, s in enumerate(p.get('specs', [])):
            if contains_cjk(s):
                errors.append(f"EN JSON - CJK found in {p.get('sku')} [specs {idx}]: {s}")
    return errors

def check_tw_jp(data, lang):
    errors = []
    for p in data:
        for field in ['origin', 'material']:
            val = p.get(field, "")
            # Check for English words not in whitelist
            words = re.findall(r'[A-Za-z]+', val)
            for w in words:
                # ignore case for whitelist check
                if w.lower() not in [wl.lower() for wl in whitelist] and w.lower() not in p.get('sku', '').lower() and w.lower() not in p.get('name', '').lower():
                    # We might get false positives, just print them as warnings
                    errors.append(f"WARNING {lang.upper()} JSON - English '{w}' found in {p.get('sku')} [{field}]")
    return errors

all_errors = []
for lang in ['en', 'tw', 'jp']:
    path = base_dir / lang / "products.json"
    if path.exists():
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = data.get("products", [])
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise TypeError(f"Unexpected product catalog shape: {path}")
            
        if lang == 'en':
            all_errors.extend(check_en(data))
        else:
            all_errors.extend(check_tw_jp(data, lang))

if all_errors:
    print("Verification found issues:")
    for e in all_errors:
        print(e)
else:
    print("Verification passed! No language purity issues found.")
