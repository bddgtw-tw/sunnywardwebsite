import os

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"

categories_to_add = {
    "tw": 'rubberwood: "橡膠木實木家具",',
    "en": 'rubberwood: "Solid Rubberwood Furniture",',
    "jp": 'rubberwood: "ラバーウッド無垢家具",'
}

for lang in ['tw', 'en', 'jp']:
    path = os.path.join(repo_dir, lang, "products.html")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'rubberwood:' not in content:
            content = content.replace(
                'office_desks: ',
                f'{categories_to_add[lang]}\n      office_desks: '
            )
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully added rubberwood & metal_frames to {lang}/products.html")
        else:
            print(f"rubberwood already present in {lang}/products.html")
