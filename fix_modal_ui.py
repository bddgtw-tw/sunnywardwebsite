import os
import re

def update_modal_logic():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    languages = ['en', 'tw', 'jp']
    
    # We want to replace the modal data population logic in products.html
    # Specifically, cleaning up the duplicated "Material:" text and removing duplicate sections if necessary.
    
    for lang in languages:
        filepath = os.path.join(base_dir, lang, "products.html")
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # The logic we want to insert replaces the straightforward innerText assignments
        # We will look for:
        old_logic = """      document.getElementById('modal-product-desc').innerText = p.description;
      document.getElementById('modal-product-dims').innerText = (p.dimensions ? p.dimensions.raw : '');
      document.getElementById('modal-product-material').innerText = (p.materials ? p.materials.join(' | ') : '');"""
        
        new_logic = """      // Cleanup description and materials
      let descText = p.description || '';
      let matText = (p.materials && p.materials.length > 0) ? p.materials.join(' | ') : '';
      
      // Remove redundant "Material: " or "材質：" prefixes from material text
      matText = matText.replace(/^(Material|材質|材質)[：:]\\s*/i, '');
      
      // If description contains the material text, don't show it twice
      // We can hide the Materials row in the modal if it's empty or duplicate
      if (matText && descText.includes(matText)) {
          matText = ''; // Hide material row if it's already in description
      } else if (matText && !descText) {
          descText = matText; // If no description, use material as description
          matText = ''; // And hide the material row
      }
      
      document.getElementById('modal-product-desc').innerText = descText;
      document.getElementById('modal-product-dims').innerText = (p.dimensions ? p.dimensions.raw : '');
      document.getElementById('modal-product-material').innerText = matText;
      
      // Hide empty rows in modal (Assuming the parent <p> contains the label and the span)
      const matEl = document.getElementById('modal-product-material');
      if (!matText) {
          if (matEl.parentElement) matEl.parentElement.style.display = 'none';
      } else {
          if (matEl.parentElement) matEl.parentElement.style.display = '';
      }
      
      const dimsEl = document.getElementById('modal-product-dims');
      if (!dimsEl.innerText) {
          if (dimsEl.parentElement) dimsEl.parentElement.style.display = 'none';
      } else {
          if (dimsEl.parentElement) dimsEl.parentElement.style.display = '';
      }
      
      const originEl = document.getElementById('modal-product-origin');
      if (!p.origin) {
          if (originEl.parentElement) originEl.parentElement.style.display = 'none';
      } else {
          if (originEl.parentElement) originEl.parentElement.style.display = '';
      }
      """
        
        content = content.replace(old_logic, new_logic)
        
        # Also clean up the HTML of the modal: if Specs is empty, hide the "Product Features & Specifications" title
        old_specs_logic = """      // Render Specs
      const specsList = document.getElementById('modal-product-specs');
      specsList.innerHTML = p.specs.map(spec => `<li>${spec}</li>`).join('');"""
        
        new_specs_logic = """      // Render Specs
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
        
        content = content.replace(old_specs_logic, new_specs_logic)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Updated UI logic in {lang}/products.html")

if __name__ == "__main__":
    update_modal_logic()
