import os
import json
import re

base_dir = r'c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website'

def process_lang(lang):
    path = os.path.join(base_dir, lang, 'products.json')
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for p in data:
        # Translate Coffee Table
        if p.get('name') == 'Coffee Table' or 'Coffee Table' in p.get('name', ''):
            if lang == 'tw':
                p['name'] = p['name'].replace('Coffee Table', '茶几')
            elif lang == 'jp':
                p['name'] = p['name'].replace('Coffee Table', 'コーヒーテーブル')
                
        # Fix specs mixed language
        specs = p.get('specs', [])
        new_specs = []
        for s in specs:
            new_s = s
            if 'in' in new_s and 'with' in new_s:
                if lang == 'tw':
                    new_s = re.sub(r'in (.*?) with (.*?)(?=[。\. \n]|$)', r'\1搭配\2', new_s)
                elif lang == 'jp':
                    new_s = re.sub(r'in (.*?) with (.*?)(?=[。\. \n]|$)', r'\1・\2', new_s)
            
            # also replace "Almo木紋" / "Almo木目" etc just in case there's "in Maple 顏色"
            if 'in Maple 顏色' in new_s:
                if lang == 'tw': new_s = new_s.replace('in Maple 顏色', '楓木色')
                elif lang == 'jp': new_s = new_s.replace('in Maple 顏色', 'メープル色')
                
            new_specs.append(new_s)
        p['specs'] = new_specs
        
        # Trim JP dims whitespace
        if lang == 'jp' and p.get('dims'):
            p['dims'] = re.sub(r'約\s+', '約', p['dims'])
            p['dims'] = re.sub(r'約\s*([0-9])', r'約\1', p['dims'])
            
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

for lang in ['tw', 'jp', 'en']:
    process_lang(lang)
    
print('JSON deep clean completed.')
