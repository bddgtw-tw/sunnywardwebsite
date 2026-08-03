import os

def update_material_logic():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    languages = ['en', 'tw', 'jp']
    
    old_logic = """      // Cleanup description and materials
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
      document.getElementById('modal-product-material').innerText = matText;"""

    new_logic = """      // Cleanup description and materials
      let descText = p.description || '';
      let matText = (p.materials && p.materials.length > 0) ? p.materials.join(' | ') : '';
      
      // 1. Move material info from description to specs if needed
      const descLower = descText.toLowerCase();
      if (descLower.startsWith('material:') || descLower.startsWith('材質:') || descLower.startsWith('材質：')) {
          matText = descText.replace(/\\n/g, ' | ');
          descText = '';
      }
      
      // 2. Remove redundant "Material: " or "材質：" prefixes from material text
      matText = matText.replace(/^(Material|材質)[：:]\\s*/i, '');
      
      // 3. Fallback placeholder for description
      if (!descText || descText.trim() === '') {
          const lang = document.documentElement.lang || "en";
          if (lang === 'tw') {
              descText = "體驗我們精選商用家具系列的極致舒適與設計感，專為耐用與風格而打造，適合各種商業與戶外空間。";
          } else if (lang === 'ja') {
              descText = "耐久性とスタイルを追求したプレミアムな商業用家具コレクションで、究極の快適さとデザインをご体験ください。あらゆる商業空間や屋外スペースに最適です。";
          } else {
              descText = "Experience ultimate comfort and design with our premium commercial furniture collection. Crafted for durability and style, perfect for any contract or outdoor space.";
          }
      }
      
      document.getElementById('modal-product-desc').innerText = descText;
      document.getElementById('modal-product-dims').innerText = (p.dimensions ? p.dimensions.raw : '');
      document.getElementById('modal-product-material').innerText = matText;"""

    for lang in languages:
        filepath = os.path.join(base_dir, lang, "products.html")
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if old_logic in content:
            content = content.replace(old_logic, new_logic)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {lang}/products.html")
        else:
            print(f"Could not find old logic in {lang}/products.html")

if __name__ == "__main__":
    update_material_logic()
