import os
import re

def fix_modal_image_fallback():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    languages = ['en', 'tw', 'jp']
    
    for lang in languages:
        filepath = os.path.join(base_dir, lang, "products.html")
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # We need to replace the modal image logic
        target = "document.getElementById('modal-product-img').src = \"../\" + p.images[0];"
        
        replacement = """
      if (p.images && p.images.length > 0) {
        document.getElementById('modal-product-img').src = "../" + p.images[0];
      } else {
        // Use a generic placeholder base64 or a styled div for missing images in modal
        // For simplicity, we can use a transparent pixel or a generic "pending" text, but since it's an img tag,
        // Let's use a base64 encoded grey image
        document.getElementById('modal-product-img').src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='800'%3E%3Crect width='100%25' height='100%25' fill='%23e9e5de'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='24' fill='%23706b61'%3EIMAGE PENDING%3C/text%3E%3C/svg%3E";
      }
"""
        
        if target in content:
            content = content.replace(target, replacement)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed modal image fallback in {lang}/products.html")
        else:
            print(f"Target logic not found in {lang}/products.html")

if __name__ == "__main__":
    fix_modal_image_fallback()
