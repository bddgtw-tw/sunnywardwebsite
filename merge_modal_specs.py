import os
import re

def merge_specs_into_meta():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    languages = ['en', 'tw', 'jp']
    
    for lang in languages:
        filepath = os.path.join(base_dir, lang, "products.html")
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Modify HTML Structure
        # Remove the modal-product-specs-wrap block entirely
        specs_wrap_pattern = re.compile(r'\s*<div class="modal-product-specs-wrap">.*?</div>', re.DOTALL)
        content = specs_wrap_pattern.sub('', content)
        
        # Add the specs container inside modal-product-meta
        meta_pattern = re.compile(r'(<div class="modal-product-meta">.*?)(</div>\s*</div>)', re.DOTALL)
        # We append a div for specs inside modal-product-meta
        replacement = r'\1  <div id="modal-product-specs-container"></div>\n          \2'
        
        if '<div id="modal-product-specs-container">' not in content:
            content = meta_pattern.sub(replacement, content, count=1)
            
        # 2. Modify JS Logic
        old_js = """      // Render Specs
      const specsList = document.getElementById('modal-product-specs');
      if (p.specs && p.specs.length > 0) {
          specsList.innerHTML = p.specs.map(spec => `<li>${spec}</li>`).join('');
          specsList.previousElementSibling.style.display = ''; // The h4 or h3 title
          specsList.style.display = '';
      } else {
          specsList.innerHTML = '';
          specsList.previousElementSibling.style.display = 'none';
          specsList.style.display = 'none';
      }"""
        
        new_js = """      // Render Specs directly into meta container
      const specsContainer = document.getElementById('modal-product-specs-container');
      if (p.specs && p.specs.length > 0) {
          specsContainer.innerHTML = p.specs.map(spec => {
              // Try to bold the label if there's a colon
              const colonIndex = spec.indexOf(':') !== -1 ? spec.indexOf(':') : spec.indexOf('：');
              if (colonIndex !== -1) {
                  return `<div><strong>${spec.substring(0, colonIndex + 1)}</strong> <span>${spec.substring(colonIndex + 1).trim()}</span></div>`;
              }
              return `<div><span>• ${spec}</span></div>`;
          }).join('');
      } else {
          specsContainer.innerHTML = '';
      }"""
      
        content = content.replace(old_js, new_js)
        
        # fallback if old_js wasn't exactly matching (maybe it had different spacing)
        # We can also do a regex replace if needed, but since I just wrote it, string replace should work.

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Updated UI layout in {lang}/products.html")

if __name__ == "__main__":
    merge_specs_into_meta()
