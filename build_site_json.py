import sys, io, os, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('data/master_products.json', 'r', encoding='utf-8') as f:
    master_products = json.load(f)

print('Master products:', len(master_products))

formatted_products = []
for p in master_products:
    img_path = p['image']
    img_list = [img_path] if img_path else []
    
    formatted_products.append({
        'id': p['variant_id'],
        'sku': p['sku'],
        'color': p['color'],
        'variant_id': p['variant_id'],
        'name': p['name_en'],
        'name_en': p['name_en'],
        'name_tc': p['name_tc'],
        'name_jp': p['name_jp'],
        'category': p['category'],
        'sub_category': p['subcategory'],
        'subcategory': p['subcategory'],
        'collection': p['subcategory'],
        'description': p['description'],
        'materials': [p['material']] if p['material'] != '待補' else [],
        'dimensions': {'raw': p['size']},
        'weight': p['weight'],
        'images': img_list,
        'detail_page': f"products/{p['slug']}.html",
        'frontend_visible': True,
        'frontend_status': 'published',
        'origin': p['origin']
    })

for lang in ['en', 'tw', 'jp']:
    out_file = f'{lang}/products.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump({'source': 'Google Sheet Published_Products', 'products': formatted_products}, f, ensure_ascii=False, indent=2)
    print(f'Wrote {out_file} with {len(formatted_products)} items.')
