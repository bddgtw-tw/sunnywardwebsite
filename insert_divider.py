import os

def insert_divider():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    languages = ['en', 'tw', 'jp']
    
    for lang in languages:
        filepath = os.path.join(base_dir, lang, "products.html")
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        old_desc = '<p id="modal-product-desc" class="modal-product-desc">Description</p>'
        new_desc = '<p id="modal-product-desc" class="modal-product-desc">Description</p>\n          <hr class="modal-divider">'
        
        content = content.replace(old_desc, new_desc)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Added hr to {lang}/products.html")
        
    # Now let's add CSS to css/index.css
    css_path = os.path.join(base_dir, "css", "index.css")
    if os.path.exists(css_path):
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write("\n\n/* Modal Divider */\n.modal-divider {\n  border: none;\n  border-top: 1px solid var(--border);\n  margin: 1.5rem 0;\n  width: 100%;\n}\n")
        print("Updated index.css")

if __name__ == "__main__":
    insert_divider()
