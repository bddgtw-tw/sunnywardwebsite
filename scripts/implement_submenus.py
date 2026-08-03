import os
import re

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"

subcat_css = """
    /* SUB-CATEGORY CHIPS */
    .subcat-menu {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin: 1.5rem 0 2rem 0;
      padding: 0;
      list-style: none;
    }
    .subcat-btn {
      background: rgba(255, 255, 255, 0.6);
      border: 1px solid rgba(224, 218, 209, 0.8);
      padding: 0.5rem 1.2rem;
      border-radius: 30px;
      font-size: 0.85rem;
      font-weight: 500;
      font-family: inherit;
      color: #666;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      backdrop-filter: blur(5px);
    }
    .subcat-btn:hover {
      background: rgba(184, 142, 107, 0.1);
      border-color: #B88E6B;
      color: #B88E6B;
      transform: translateY(-1px);
    }
    .subcat-btn.active {
      background: #B88E6B;
      border-color: #B88E6B;
      color: #fff;
      box-shadow: 0 4px 12px rgba(184, 142, 107, 0.25);
    }
"""

js_injections = {
    "tw": {
        "label_all": "全部顯示",
        "translations": """
    const subcatTranslations = {
      "Mesh Chair": "網眼人體工學椅",
      "Leather Chair": "皮革主管椅",
      "Visitor Chair": "會議與訪客椅",
      "Task Chair": "職員辦公椅",
      "Executive Desk": "主管與總裁桌",
      "Staff Desk": "職員工作位",
      "Storage & Pedestals": "文件櫃與活動櫃",
      "Conference Table": "會議桌系列",
      "Office Table": "一般辦公桌",
      "Benches": "實木長凳",
      "Tabletops": "實木桌板",
      "Wooden Legs": "實木桌腳",
      "Commercial Benches": "商用公共排椅",
      "Metal Bases & Legs": "五金鋼腳座底座",
      "Loveseat": "雙人沙發",
      "Sofa": "多人沙發",
      "Coffee Table": "戶外茶几",
      "Side Table": "戶外邊几",
      "Lounge Chair": "休閒單人椅"
    };
"""
    },
    "en": {
        "label_all": "All Products",
        "translations": """
    const subcatTranslations = {
      "Mesh Chair": "Mesh Ergonomic Chairs",
      "Leather Chair": "Leather Executive Chairs",
      "Visitor Chair": "Conference & Visitor Chairs",
      "Task Chair": "Task Chairs",
      "Executive Desk": "Executive Desks",
      "Staff Desk": "Workstations & Staff Desks",
      "Storage & Pedestals": "Storage & File Cabinets",
      "Conference Table": "Conference Tables",
      "Office Table": "Office Desks",
      "Benches": "Solid Wood Benches",
      "Tabletops": "Solid Wood Tabletops",
      "Wooden Legs": "Solid Wood Legs",
      "Commercial Benches": "Commercial Airport Benches",
      "Metal Bases & Legs": "Steel Bases & Metal Frames",
      "Loveseat": "Loveseats",
      "Sofa": "Sofas",
      "Coffee Table": "Coffee Tables",
      "Side Table": "Side Tables",
      "Lounge Chair": "Lounge Chairs"
    };
"""
    },
    "jp": {
        "label_all": "すべて表示",
        "translations": """
    const subcatTranslations = {
      "Mesh Chair": "メッシュチェア",
      "Leather Chair": "レザーチェア",
      "Visitor Chair": "ビジターチェア",
      "Task Chair": "タスクチェア",
      "Executive Desk": "エグゼクティブデスク",
      "Staff Desk": "ワークステーション",
      "Storage & Pedestals": "キャビネット・収納",
      "Conference Table": "ミーティングテーブル",
      "Office Table": "オフィスデスク",
      "Benches": "木製ベンチ",
      "Tabletops": "木製天板",
      "Wooden Legs": "木製脚",
      "Commercial Benches": "ロビーチェア",
      "Metal Bases & Legs": "スチール脚・フレーム",
      "Loveseat": "ラブシート",
      "Sofa": "ソファ",
      "Coffee Table": "コーヒーテーブル",
      "Side Table": "サイドテーブル",
      "Lounge Chair": "ラウンジチェア"
    };
"""
    }
}

helper_js = """
    // Helper function to render subcategory menu
    function renderSubMenu(categoryKey, products) {
      const subcats = new Set();
      products.forEach(p => {
        const sub = p.sub_category || p.subcat || p.collection;
        if (sub && sub !== 'Component' && sub !== 'General Collection' && sub !== 'Table' && sub !== 'Chair') {
          subcats.add(sub);
        }
      });

      if (subcats.size <= 1) return "";

      let html = `<ul class="subcat-menu">`;
      html += `<li><button class="subcat-btn active" onclick="filterSubCategory('${categoryKey}', 'all', this)">{LABEL_ALL}</button></li>`;
      
      sortedSubcats = Array.from(subcats).sort();
      sortedSubcats.forEach(sub => {
        const trans = subcatTranslations[sub] || sub;
        html += `<li><button class="subcat-btn" onclick="filterSubCategory('${categoryKey}', '${sub}', this)">${trans}</button></li>`;
      });
      html += `</ul>`;
      return html;
    }

    // Filter products grid by subcategory
    function filterSubCategory(categoryKey, subcat, btn) {
      // Toggle active states on chips
      const parent = btn.closest('.product-category-group');
      parent.querySelectorAll('.subcat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Filter products
      const categoryProducts = getVisibleProducts().filter(p => {
        const catMatch = (p.category ? p.category.toLowerCase() : '') === categoryKey;
        if (!catMatch) return false;
        if (subcat === 'all') return true;
        const pSub = p.sub_category || p.subcat || p.collection;
        return pSub === subcat;
      });

      // Re-render grid
      const grid = parent.querySelector('.products-grid');
      if (grid) {
        grid.innerHTML = renderCards(categoryProducts);
      }
    }
"""

def update_products_pages():
    for lang in ['tw', 'en', 'jp']:
        path = os.path.join(repo_dir, lang, "products.html")
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Inject CSS
        if '/* SUB-CATEGORY CHIPS */' not in content:
            # Find </style> and prepend CSS
            content = content.replace('</style>', f'{subcat_css}</style>', 1)
            
        # 2. Inject JS helpers
        if 'function renderSubMenu' not in content:
            # Prepare script block
            lang_js = js_injections[lang]["translations"]
            lang_helpers = helper_js.replace('{LABEL_ALL}', js_injections[lang]["label_all"])
            
            # Place after loadProducts function
            content = content.replace(
                'let allProducts = [];',
                f'let allProducts = [];\n{lang_js}\n{lang_helpers}'
            )
            
        # 3. Update stage grid HTML template inside renderLayout
        old_template = """          stageHtml += `
            <div class="product-category-group ${isActive}" id="cat-${key}">
              <div class="cat-header">
                <h3>${catTranslations[key]}</h3>
                <span class="cat-header-count">精選 ${counts[key]} 款</span>
              </div>
              <div class="products-grid">
                ${renderCards(grouped[key])}
              </div>
            </div>
          `;"""
          
        new_template = """          stageHtml += `
            <div class="product-category-group ${isActive}" id="cat-${key}">
              <div class="cat-header">
                <h3>${catTranslations[key]}</h3>
                <span class="cat-header-count">精選 ${counts[key]} 款</span>
              </div>
              ${renderSubMenu(key, grouped[key])}
              <div class="products-grid">
                ${renderCards(grouped[key])}
              </div>
            </div>
          `;"""
          
        if 'renderSubMenu(key, grouped[key])' not in content:
            # Simple replace
            content = content.replace(
                '${renderCards(grouped[key])}',
                '${renderCards(grouped[key])}' # placeholder, let's do a direct replacement of the block
            )
            # Use raw replace
            # We look for the products-grid wrapper and add renderSubMenu right above it
            content = re.sub(
                r'(<div class="product-category-group.*?<div class="products-grid">)',
                r'\1\n              ${renderSubMenu(key, grouped[key])}',
                content,
                flags=re.DOTALL
            )
            # Actually, let's use exact match replace to be safe
            content = content.replace(
                '<div class="products-grid">',
                '${renderSubMenu(key, grouped[key])}\n              <div class="products-grid">'
            )
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated sub-menu UX in {lang}/products.html")

if __name__ == "__main__":
    update_products_pages()
