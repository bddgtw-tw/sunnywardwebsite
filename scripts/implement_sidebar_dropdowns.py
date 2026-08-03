import os
import re

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"

dropdown_css = """
    /* SIDEBAR DROPDOWN UX */
    .arrow-icon {
      display: inline-block;
      font-size: 0.55rem;
      margin-right: 0.5rem;
      transition: transform 0.3s ease;
      vertical-align: middle;
      opacity: 0.6;
    }
    .cat-btn.open .arrow-icon {
      transform: rotate(90deg);
    }
    .subcat-dropdown {
      list-style: none;
      padding-left: 1.2rem;
      margin: 0.3rem 0 0.8rem 0;
      border-left: 1px solid rgba(184, 142, 107, 0.2);
    }
    .subcat-dropdown li {
      margin-bottom: 0.25rem;
    }
    .subcat-dropdown a {
      font-size: 0.8rem;
      color: #666;
      text-decoration: none;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.25rem 0.5rem;
      border-radius: 4px;
      transition: all 0.2s ease;
    }
    .subcat-dropdown a:hover {
      background: rgba(184, 142, 107, 0.08);
      color: #B88E6B;
    }
    .subcat-dropdown a.active {
      color: #B88E6B;
      font-weight: 500;
      background: rgba(184, 142, 107, 0.08);
    }
    .subcat-count {
      font-size: 0.7rem;
      opacity: 0.6;
      background: rgba(0,0,0,0.04);
      padding: 0.1rem 0.3rem;
      border-radius: 10px;
    }
"""

js_translations = {
    "tw": """
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
      "Cabinets & Chests": "收納櫃與抽屜櫃",
      "Dining Tables & Desks": "實木餐桌與書桌",
      "TV Consoles & Sideboards": "電視櫃與多功能邊櫃",
      "Designer Dining Chairs": "設計師餐椅與單椅",
      "Lounge & Accent Chairs": "精品沙發休閒椅",
      "Plastic Chair": "高強度塑料椅",
      "Upholstered Chair": "設計師軟包椅",
      "Wooden Chair": "實木工藝椅",
      "Metal Chair": "金屬防銹餐椅",
      "Bar Stool": "高腳吧檯椅",
      "Counter Stool": "中高度吧檯椅",
      "Adjustable Stool": "可調升降吧椅",
      "Accent Chair": "精品設計單椅",
      "Recliner": "舒適功能躺椅",
      "Armchair": "精品扶手休閒椅",
      "Outdoor Chair": "戶外休閒椅",
      "Outdoor Sofa": "戶外防水沙發",
      "Outdoor Table": "戶外茶几與桌",
      "Loveseat": "雙人沙發",
      "Sofa": "多人沙發",
      "Coffee Table": "戶外茶几",
      "Side Table": "戶外邊几",
      "Lounge Chair": "休閒單人椅"
    };
""",
    "en": """
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
      "Cabinets & Chests": "Cabinets & Chests",
      "Dining Tables & Desks": "Dining Tables & Desks",
      "TV Consoles & Sideboards": "TV Consoles & Sideboards",
      "Designer Dining Chairs": "Designer Dining Chairs",
      "Lounge & Accent Chairs": "Lounge & Accent Chairs",
      "Plastic Chair": "Polypropylene Chairs",
      "Upholstered Chair": "Upholstered Dining Chairs",
      "Wooden Chair": "Wooden Dining Chairs",
      "Metal Chair": "Metal Dining Chairs",
      "Bar Stool": "Bar Stools",
      "Counter Stool": "Counter Stools",
      "Adjustable Stool": "Adjustable Stools",
      "Accent Chair": "Accent Chairs",
      "Recliner": "Recliners & Lounge",
      "Armchair": "Lounge Armchairs",
      "Outdoor Chair": "Outdoor Chairs",
      "Outdoor Sofa": "Outdoor Sofas",
      "Outdoor Table": "Outdoor Tables",
      "Loveseat": "Loveseats",
      "Sofa": "Sofas",
      "Coffee Table": "Coffee Tables",
      "Side Table": "Side Tables",
      "Lounge Chair": "Lounge Chairs"
    };
""",
    "jp": """
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
      "Cabinets & Chests": "キャビネット・チェスト",
      "Dining Tables & Desks": "ダイニングテーブル・デスク",
      "TV Consoles & Sideboards": "テレビ台・サイドボード",
      "Designer Dining Chairs": "デザインダイニングチェア",
      "Lounge & Accent Chairs": "ラウンジチェア",
      "Plastic Chair": "プラスチックチェア",
      "Upholstered Chair": "クッションチェア",
      "Wooden Chair": "木製チェア",
      "Metal Chair": "メタルチェア",
      "Bar Stool": "バースツール",
      "Counter Stool": "カウンタースツール",
      "Adjustable Stool": "昇降スツール",
      "Accent Chair": "アクセントチェア",
      "Recliner": "リクライニングチェア",
      "Armchair": "アームチェア",
      "Outdoor Chair": "アウトドアチェア",
      "Outdoor Sofa": "アウトドアソファ",
      "Outdoor Table": "アウトドアテーブル",
      "Loveseat": "ラブシート",
      "Sofa": "ソファ",
      "Coffee Table": "コーヒーテーブル",
      "Side Table": "サイドテーブル",
      "Lounge Chair": "ラウンジチェア"
    };
"""
}

helper_js = """
    let groupedProductsGlobal = {};

    function renderSidebarDropdown(key, products, subcatCounts) {
      const subcats = new Set();
      products.forEach(p => {
        const sub = p.sub_category || p.subcat || p.collection;
        if (sub && sub !== 'Component' && sub !== 'General Collection' && sub !== 'Table' && sub !== 'Chair') {
          subcats.add(sub);
        }
      });

      if (subcats.size <= 1) return "";

      let html = `<ul class="subcat-dropdown" id="subcat-list-${key}" style="display: none;">`;
      sortedSubcats = Array.from(subcats).sort();
      sortedSubcats.forEach(sub => {
        const trans = subcatTranslations[sub] || sub;
        const subKey = key + "||" + sub;
        const count = subcatCounts[subKey] || 0;
        html += `
          <li>
            <a href="#" onclick="selectSubcat('${key}', '${sub}', this); return false;">
              ${trans} <span class="subcat-count">${count}</span>
            </a>
          </li>
        `;
      });
      html += `</ul>`;
      return html;
    }

    function selectSubcat(categoryKey, subcat, linkEl) {
      const dropdown = linkEl.closest('.subcat-dropdown');
      dropdown.querySelectorAll('a').forEach(a => a.classList.remove('active'));
      linkEl.classList.add('active');

      const filtered = getVisibleProducts().filter(p => {
        const catMatch = (p.category ? p.category.toLowerCase() : '') === categoryKey;
        if (!catMatch) return false;
        const pSub = p.sub_category || p.subcat || p.collection;
        return pSub === subcat;
      });

      const grid = document.getElementById('grid-' + categoryKey);
      if (grid) {
        grid.innerHTML = renderCards(filtered);
      }
    }

    // SEARCH LOGIC
    let searchTimeout = null;
    window.handleSearch = function(query) {
      const q = query.trim();
      const clearBtn = document.getElementById('search-clear-btn');
      if (clearBtn) {
        clearBtn.classList.toggle('visible', q.length > 0);
      }
      
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        performSearch(q);
      }, 250);
    }
    
    function performSearch(q) {
      const stage = document.getElementById('products-stage');
      if (!stage) return;
      
      const qLower = q.toLowerCase();
      
      if (qLower.length === 0) {
        renderLayout();
        const activeBtn = document.querySelector('.cat-btn.active');
        if (activeBtn) {
          const key = activeBtn.id.replace('btn-', '');
          switchCategory(key);
        }
        return;
      }
      
      const results = allProducts.filter(p => {
        const name = (p.name || '').toLowerCase();
        const sku = (p.sku || '').toLowerCase();
        const desc = (p.description || '').toLowerCase();
        const sub = (p.sub_category || p.subcat || p.collection || '').toLowerCase();
        return name.includes(qLower) || sku.includes(qLower) || desc.includes(qLower) || sub.includes(qLower);
      });
      
      let searchTitle = "Search Results";
      let countText = `Found ${results.length} products`;
      let noResultsText = "No products found matching your search.";
      
      const lang = document.documentElement.lang || "en";
      if (lang === "zh-TW" || lang === "tw") {
        searchTitle = "搜尋結果";
        countText = `找到 ${results.length} 筆產品`;
        noResultsText = "沒有找到符合您搜尋的產品。";
      } else if (lang === "ja" || lang === "jp") {
        searchTitle = "検索結果";
        countText = `${results.length} 件の製品が見つかりました`;
        noResultsText = "検索条件に一致する製品が見つかりませんでした。";
      }
      
      document.querySelectorAll('.cat-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.subcat-dropdown').forEach(d => d.style.display = 'none');
      document.querySelectorAll('.arrow-icon').forEach(a => a.style.transform = 'rotate(0deg)');
      
      let html = `
        <div class="product-category-group active" id="search-results-group">
          <div class="category-header">
            <h2>${searchTitle}</h2>
            <p class="category-subtitle">${countText}</p>
          </div>
          <div class="products-grid search-results-grid">
            ${results.length > 0 ? renderCards(results) : `<div class="no-results-msg" style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--stone); font-size: 0.95rem;">${noResultsText}</div>`}
          </div>
        </div>
      `;
      stage.innerHTML = html;
    }
    
    window.clearSearch = function() {
      const input = document.getElementById('product-search');
      if (input) {
        input.value = "";
        handleSearch("");
      }
    }

    // PAGINATION LOGIC
    let displayedCounts = {};
    window.loadMoreProducts = function(catId) {
      displayedCounts[catId] = (displayedCounts[catId] || 24) + 24;
      renderCategoryGrid(catId);
    }
    
    function renderCategoryGrid(catId) {
      const grid = document.getElementById('grid-' + catId);
      if (!grid || !groupedProductsGlobal[catId]) return;
      
      const allCatProducts = groupedProductsGlobal[catId];
      const limit = displayedCounts[catId] || 24;
      const visibleItems = allCatProducts.slice(0, limit);
      
      grid.innerHTML = renderCards(visibleItems);
      
      const container = document.getElementById('load-more-container-' + catId);
      if (container) {
        container.style.display = allCatProducts.length > limit ? 'block' : 'none';
      }
    }
"""

def update_localized_pages():
    for lang in ['tw', 'en', 'jp']:
        path = os.path.join(repo_dir, lang, "products.html")
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Inject CSS
        if '/* SIDEBAR DROPDOWN UX */' not in content:
            content = content.replace('</style>', f'{dropdown_css}</style>', 1)
            
        # 2. Inject JS helpers & translations
        if 'function renderSidebarDropdown' not in content:
            lang_js = js_translations[lang]
            content = content.replace(
                'let allProducts = [];',
                f'let allProducts = [];\n{lang_js}\n{helper_js}'
            )
            
        # 3. Update products-grid container to have dynamic ID in renderLayout()
        content = content.replace(
            '<div class="products-grid">',
            '<div class="products-grid" id="grid-${key}">'
        )
        
        # 4. Update Sidebar list rendering inside renderLayout() to include dropdown toggle arrow
        # Find the original sidebarHtml construction loop and replace it
        old_sidebar_loop = """      visibleCategoryKeys.forEach((key, idx) => {
        const isActive = idx === 0 ? "active" : "";
        const countDisplay = key === "materials" ? "—" : counts[key];
        sidebarHtml += `
          <li>
            <button class="cat-btn ${isActive}" id="btn-${key}" onclick="switchCategory('${key}')">
              ${catTranslations[key]} <span class="cat-count">${countDisplay}</span>
            </button>
          </li>
        `;
      });"""
      
        new_sidebar_loop = """      // Calculate subcategory counts
      const subcatCounts = {};
      visibleProducts.forEach(p => {
        const cat = (p.category ? p.category.toLowerCase() : '');
        const sub = p.sub_category || p.subcat || p.collection;
        if (cat && sub) {
          const subKey = cat + "||" + sub;
          subcatCounts[subKey] = (subcatCounts[subKey] || 0) + 1;
        }
      });
      
      groupedProductsGlobal = grouped;

      visibleCategoryKeys.forEach((key, idx) => {
        const isActive = idx === 0 ? "active" : "";
        const countDisplay = key === "materials" ? "—" : counts[key];
        
        // Check if category has subcategories to show arrow
        const subList = renderSidebarDropdown(key, grouped[key], subcatCounts);
        const hasSub = subList !== "";
        const arrow = hasSub ? '<span class="arrow-icon">&#9654;</span>' : '';
        
        sidebarHtml += `
          <li>
            <button class="cat-btn ${isActive}" id="btn-${key}" onclick="switchCategory('${key}')">
              <span class="cat-text-wrap">${arrow}${catTranslations[key]}</span> 
              <span class="cat-count">${countDisplay}</span>
            </button>
            ${subList}
          </li>
        `;
      });"""
      
        if 'renderSidebarDropdown' not in content or 'groupedProductsGlobal = grouped;' not in content:
            content = content.replace(old_sidebar_loop, new_sidebar_loop)
            
        # 4.5 Inject Search HTML
        if 'class="sidebar-search"' not in content:
            if lang == "tw":
                search_html = """          <div class="sidebar-search">
            <input type="text" id="product-search" placeholder="搜尋產品名稱或型號..." oninput="handleSearch(this.value)">
            <span class="search-clear-btn" id="search-clear-btn" onclick="clearSearch()">✕</span>
          </div>"""
                content = content.replace('<div class="sidebar-title">產品分類</div>', f'<div class="sidebar-title">產品分類</div>\n{search_html}')
            elif lang == "en":
                search_html = """          <div class="sidebar-search">
            <input type="text" id="product-search" placeholder="Search by name or SKU..." oninput="handleSearch(this.value)">
            <span class="search-clear-btn" id="search-clear-btn" onclick="clearSearch()">✕</span>
          </div>"""
                content = content.replace('<div class="sidebar-title">Categories</div>', f'<div class="sidebar-title">Categories</div>\n{search_html}')
            elif lang == "jp":
                search_html = """          <div class="sidebar-search">
            <input type="text" id="product-search" placeholder="製品名や型番で検索..." oninput="handleSearch(this.value)">
            <span class="search-clear-btn" id="search-clear-btn" onclick="clearSearch()">✕</span>
          </div>"""
                content = content.replace('<div class="sidebar-title">カテゴリ</div>', f'<div class="sidebar-title">カテゴリ</div>\n{search_html}')
            
        # 5. Modify switchCategory(id) JS function to manage arrow rotations and dropdown displays
        old_switch_fn = """    function switchCategory(id) {
      document.querySelectorAll('.product-category-group').forEach(g => g.classList.remove('active'));
      document.getElementById('cat-' + id).classList.add('active');
      
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('btn-' + id).classList.add('active');
    }"""
    
        new_switch_fn = """    function switchCategory(id) {
      document.querySelectorAll('.product-category-group').forEach(g => g.classList.remove('active'));
      document.getElementById('cat-' + id).classList.add('active');
      
      document.querySelectorAll('.cat-btn').forEach(b => {
        b.classList.remove('active');
        b.classList.remove('open');
      });
      document.getElementById('btn-' + id).classList.add('active');
      document.getElementById('btn-' + id).classList.add('open');
      
      // Manage dropdowns
      document.querySelectorAll('.subcat-dropdown').forEach(d => d.style.display = 'none');
      const activeDropdown = document.getElementById('subcat-list-' + id);
      if (activeDropdown) {
        activeDropdown.style.display = 'block';
        activeDropdown.querySelectorAll('a').forEach(a => a.classList.remove('active'));
      }
      
      // Reset products grid (with pagination)
      displayedCounts[id] = 24;
      renderCategoryGrid(id);
    }"""
    
        if 'Manage dropdowns' not in content:
            content = content.replace(old_switch_fn, new_switch_fn)

        # 7. Add Category URL Parameter Auto-Selection on load
        old_load_block = """        renderLayout();
        
        // Auto-open product modal if sku parameter is present
        const urlParams = new URLSearchParams(window.location.search);"""

        new_load_block = """        renderLayout();
        
        // Auto-select category if category parameter is present in URL
        const urlParams = new URLSearchParams(window.location.search);
        const catParam = urlParams.get('category') || urlParams.get('cat');
        if (catParam) {
          switchCategory(catParam.toLowerCase());
        }
        
        // Auto-open product modal if sku parameter is present"""
        
        if 'Auto-select category if category parameter' not in content:
            content = content.replace(old_load_block, new_load_block)
            
        # 6. Replace old non-paginated grid stageHtml block
        old_grid_block_tw = """          // Render product cards grid
          stageHtml += `
            <div class="product-category-group ${isActive}" id="cat-${key}">
              <div class="cat-header">
                <h3>${catTranslations[key]}</h3>
                <span class="cat-header-count">精選 ${counts[key]} 款</span>
              </div>
              <div class="products-grid" id="grid-${key}">
                ${renderCards(grouped[key])}
              </div>
            </div>
          `;"""

        new_grid_block_tw = """          // Render product cards grid (Paginated - 24 limit)
          const limit = 24;
          const initialProducts = grouped[key].slice(0, limit);
          const hasMore = grouped[key].length > limit;
          const loadMoreStyle = hasMore ? 'display: block;' : 'display: none;';
          stageHtml += `
            <div class="product-category-group ${isActive}" id="cat-${key}">
              <div class="cat-header">
                <h3>${catTranslations[key]}</h3>
                <span class="cat-header-count">精選 ${counts[key]} 款</span>
              </div>
              <div class="products-grid" id="grid-${key}">
                ${renderCards(initialProducts)}
              </div>
              <div class="load-more-container" id="load-more-container-${key}" style="text-align: center; margin-top: 2rem; ${loadMoreStyle}">
                <button class="btn btn-secondary" id="load-more-${key}" onclick="loadMoreProducts('${key}')" style="padding: 0.65rem 1.8rem; font-size: 0.78rem;">
                  載入更多產品
                </button>
              </div>
            </div>
          `;"""

        old_grid_block_en = """          // Render product cards grid
          stageHtml += `
            <div class="product-category-group ${isActive}" id="cat-${key}">
              <div class="cat-header">
                <h3>${catTranslations[key]}</h3>
                <span class="cat-header-count">Featured ${counts[key]} models</span>
              </div>
              <div class="products-grid" id="grid-${key}">
                ${renderCards(grouped[key])}
              </div>
            </div>
          `;"""

        new_grid_block_en = """          // Render product cards grid (Paginated - 24 limit)
          const limit = 24;
          const initialProducts = grouped[key].slice(0, limit);
          const hasMore = grouped[key].length > limit;
          const loadMoreStyle = hasMore ? 'display: block;' : 'display: none;';
          stageHtml += `
            <div class="product-category-group ${isActive}" id="cat-${key}">
              <div class="cat-header">
                <h3>${catTranslations[key]}</h3>
                <span class="cat-header-count">Featured ${counts[key]} models</span>
              </div>
              <div class="products-grid" id="grid-${key}">
                ${renderCards(initialProducts)}
              </div>
              <div class="load-more-container" id="load-more-container-${key}" style="text-align: center; margin-top: 2rem; ${loadMoreStyle}">
                <button class="btn btn-secondary" id="load-more-${key}" onclick="loadMoreProducts('${key}')" style="padding: 0.65rem 1.8rem; font-size: 0.78rem;">
                  Load More Products
                </button>
              </div>
            </div>
          `;"""

        old_grid_block_jp = """          // Render product cards grid
          stageHtml += `
            <div class="product-category-group ${isActive}" id="cat-${key}">
              <div class="cat-header">
                <h3>${catTranslations[key]}</h3>
                <span class="cat-header-count">厳選 ${counts[key]} モデル</span>
              </div>
              <div class="products-grid" id="grid-${key}">
                ${renderCards(grouped[key])}
              </div>
            </div>
          `;"""

        new_grid_block_jp = """          // Render product cards grid (Paginated - 24 limit)
          const limit = 24;
          const initialProducts = grouped[key].slice(0, limit);
          const hasMore = grouped[key].length > limit;
          const loadMoreStyle = hasMore ? 'display: block;' : 'display: none;';
          stageHtml += `
            <div class="product-category-group ${isActive}" id="cat-${key}">
              <div class="cat-header">
                <h3>${catTranslations[key]}</h3>
                <span class="cat-header-count">厳選 ${counts[key]} モデル</span>
              </div>
              <div class="products-grid" id="grid-${key}">
                ${renderCards(initialProducts)}
              </div>
              <div class="load-more-container" id="load-more-container-${key}" style="text-align: center; margin-top: 2rem; ${loadMoreStyle}">
                <button class="btn btn-secondary" id="load-more-${key}" onclick="loadMoreProducts('${key}')" style="padding: 0.65rem 1.8rem; font-size: 0.78rem;">
                  さらに読み込む
                </button>
              </div>
            </div>
          `;"""

        if lang == "tw":
            content = content.replace(old_grid_block_tw, new_grid_block_tw)
        elif lang == "en":
            content = content.replace(old_grid_block_en, new_grid_block_en)
        elif lang == "jp":
            content = content.replace(old_grid_block_jp, new_grid_block_jp)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully implemented sidebar dropdown accordion menus in {lang}/products.html")

if __name__ == "__main__":
    update_localized_pages()
