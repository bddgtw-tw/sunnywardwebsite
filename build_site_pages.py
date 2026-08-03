import sys, io, os, json, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Index Product_Images folder
img_base = r'F:\共用雲端硬碟\公司營運資料架構\80_B2B_網站與行銷專區\Website_Sunnyward\Product_Images'
all_files = []
for root, dirs, files in os.walk(img_base):
    for f in files:
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, r'F:\共用雲端硬碟\公司營運資料架構\80_B2B_網站與行銷專區\Website_Sunnyward').replace('\\', '/')
            all_files.append((rel_p, f))

with open('data/published_products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

def clean_slug(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

processed_products = []
slug_counts = {}

for p in products:
    sku = p['sku'].strip()
    color = p['color'].strip()
    var_id = p['variant_id'].strip() or f'{sku}-{color}'
    
    name_en = p['name_en'].strip()
    name_tc = p['name_tc'].strip()
    name_jp = p['name_jp'].strip()
    
    if sku in name_en: name_en = name_en.replace(sku, '').strip()
    if sku in name_tc: name_tc = name_tc.replace(sku, '').strip()
    if sku in name_jp: name_jp = name_jp.replace(sku, '').strip()
    
    sku_matches = [f for f in all_files if f'{sku}_' in f[1] or f'{sku}-' in f[1] or sku == f[1].split('.')[0] or f'_{sku}/' in f[0] or f'/{sku}/' in f[0]]
    color_matches = [f for f in sku_matches if f'_{color}_' in f[1] or f'_{color}.' in f[1] or f'-{color}_' in f[1] or f'-{color}.' in f[1]]
    
    # Product cards use a representative product view, not detail/operation diagrams.
    # Keep the agreed priority: main -> front -> view -> scene -> other.
    def image_priority(item):
        filename = item[1].lower()
        for rank, token in enumerate(('_main', '_front', '_view', '_scene')):
            if token in filename:
                return rank
        return 99

    matched_img = ''
    if color_matches:
        matched_img = sorted(color_matches, key=image_priority)[0][0]
    elif sku_matches:
        matched_img = sorted(sku_matches, key=image_priority)[0][0]
    
    # Ensure unique slug
    base_slug = clean_slug(f'{sku}-{color}-{name_en}')
    if base_slug in slug_counts:
        slug_counts[base_slug] += 1
        slug = f"{base_slug}-{slug_counts[base_slug]}"
    else:
        slug_counts[base_slug] = 1
        slug = base_slug
        
    processed_products.append({
        'variant_id': var_id,
        'sku': sku,
        'color': color,
        'slug': slug,
        'category': p['category'].strip(),
        'subcategory': p['subcategory'].strip(),
        'name_en': name_en,
        'name_tc': name_tc,
        'name_jp': name_jp,
        'image': matched_img,
        'image_id': p['Image_ID'].strip(),
        'size': p['size_WxDxH_cm'].strip() or '待補',
        'material': p['material'].strip() or '待補',
        'weight': p['weight_kg'].strip() or '待補',
        'origin': p['origin'].strip() or '待補',
        'description': p['description'].strip() or '待補',
        'features': p['features'].strip() or '待補'
    })

with open('data/master_products.json', 'w', encoding='utf-8') as f:
    json.dump(processed_products, f, ensure_ascii=False, indent=2)

print('Updated data/master_products.json with unique slugs. Total items:', len(processed_products))

# Re-generate HTML
created_pages = 0
for p in processed_products:
    for lang in ['en', 'tw', 'jp']:
        out_dir = os.path.join(lang, 'products')
        os.makedirs(out_dir, exist_ok=True)
        file_path = os.path.join(out_dir, f"{p['slug']}.html")
        
        lang_code = 'en' if lang == 'en' else ('zh-TW' if lang == 'tw' else 'ja')
        name = p['name_en'] if lang == 'en' else (p['name_tc'] if lang == 'tw' else p['name_jp'])
        img_src = f"../../{p['image']}" if p['image'] else '../../images/placeholder.png'
        
        html = f"""<!DOCTYPE html>
<html lang="{lang_code}">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{name} | Sunnyward</title>
<meta content="{p['description'][:150]}" name="description"/>
<link href="../../css/style.css?v=20260730-b2b" rel="stylesheet"/>
</head>
<body>
<header id="site-header">
<div class="nav-container">
<a class="logo" href="../index.html">SUNNYWARD<span>.</span></a>
<ul class="nav-menu">
<li><a class="nav-link" href="../index.html">Home</a></li>
<li><a class="nav-link active" href="../products.html">Products</a></li>
<li><a class="nav-link" href="../projects.html">Projects</a></li>
<li><a class="nav-link" href="../contact.html">Contact</a></li>
</ul>
<div class="nav-actions">
<div class="lang-dropdown">
<button class="lang-current" type="button">{lang.upper()} ▾</button>
<ul class="lang-list">
<li><a href="../../en/products/{p['slug']}.html">English</a></li>
<li><a href="../../tw/products/{p['slug']}.html">繁中</a></li>
<li><a href="../../jp/products/{p['slug']}.html">日本語</a></li>
</ul>
</div>
</div>
</div>
</header>
<main class="verified-product-page">
<div class="container">
<nav aria-label="Breadcrumb" class="product-breadcrumb">
<a href="../index.html">Home</a><span>/</span><a href="../products.html">Products</a><span>/</span><span>{name}</span>
</nav>
<section class="verified-product-hero">
<div class="verified-product-gallery">
<figure><img alt="{name}" decoding="async" height="450" loading="eager" src="{img_src}" width="600"/></figure>
</div>
<div class="verified-product-summary">
<span class="eyebrow">{p['category'].upper()} — {p['subcategory'].upper()}</span>
<h1>{name}</h1>
<p class="verified-product-sku">SKU: {p['sku']} | Color: {p['color']}</p>
<p class="verified-product-intro">{p['description']}</p>
<a class="btn btn-primary" href="../contact.html?product={p['sku']}">Request project quotation</a>
</div>
</section>
<section class="verified-product-details">
<div>
<h3>Product Specifications</h3>
<dl>
<dt>Size (WxDxH cm)</dt><dd>{p['size']}</dd>
<dt>Material</dt><dd>{p['material']}</dd>
<dt>Weight (kg)</dt><dd>{p['weight']}</dd>
<dt>Origin</dt><dd>{p['origin']}</dd>
</dl>
</div>
<div>
<h3>Features</h3>
<p>{p['features']}</p>
</div>
</section>
</div>
</main>
</body>
</html>"""
        with open(file_path, 'w', encoding='utf-8') as pf:
            pf.write(html)
        created_pages += 1

print(f"Done. Successfully generated {created_pages} HTML files for all 531 items.")
