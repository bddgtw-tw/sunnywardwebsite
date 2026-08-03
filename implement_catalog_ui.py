import os
import re

def update_catalog_ui():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    languages = ['en', 'tw', 'jp']
    files = ['index.html', 'products.html', 'projects.html', 'contact.html']
    
    # 1. Remove old hardcoded catalog modal from all HTML files
    # The modal starts with `<div class="modal" id="catalog-modal">`
    # and ends with the matching `</div>`. It has 19 lines in en/products.html.
    # A safe regex is to match up to `<!-- PRODUCT DETAIL MODAL -->` or `<!-- RFQ` or the end of the block.
    # Actually, we can use a non-greedy regex matching `<div class="modal" id="catalog-modal">.*?<!-- PRODUCT DETAIL MODAL -->`
    # or just `<div class="modal" id="catalog-modal">.*?</div>\s*</div>\s*</div>` - wait, counting divs is hard in regex.
    # Instead, we read line by line.
    
    for lang in languages:
        for fname in files:
            filepath = os.path.join(base_dir, lang, fname)
            if not os.path.exists(filepath):
                continue
                
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            new_lines = []
            in_catalog_modal = False
            div_depth = 0
            
            for line in lines:
                if '<div class="modal" id="catalog-modal">' in line:
                    in_catalog_modal = True
                    div_depth = 1
                    continue
                
                if in_catalog_modal:
                    if '<div' in line:
                        div_depth += line.count('<div')
                    if '</div' in line:
                        div_depth -= line.count('</div')
                        
                    if div_depth <= 0:
                        in_catalog_modal = False
                    continue
                    
                new_lines.append(line)
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Cleaned {lang}/{fname}")
            
    # 2. Update js/main.js
    main_js_path = os.path.join(base_dir, "js", "main.js")
    with open(main_js_path, 'r', encoding='utf-8') as f:
        main_js = f.read()
        
    old_js_pattern = re.compile(r'// 8\. CATALOG MODAL.*?(?=\s*// 9\. INTERSECTION OBSERVER)', re.DOTALL)
    
    new_js = """// 8. CATALOG MODAL (Dynamic Multi-step)
  const catalogs = [
    { id: "cat1", name: "2025 Funife Premium Outdoor Catalogue (A4)", file: "../catalogs/2025_Funife_Premium_Outdoor_catalogue_A4.pdf" },
    { id: "cat2", name: "2026 Sunnyward Balau Wood Outdoor Furniture", file: "../catalogs/2026_Sunnyward_Balau_wood_outdoor_furniture_catalogue.pdf" },
    { id: "cat3", name: "2026 SWA Office Furniture Specification", file: "../catalogs/2026_SWA_Office_Furniture_Specification.pdf" },
    { id: "cat4", name: "2026 SWA Outdoor Selection Catalog", file: "../catalogs/2026_SWA_Outdoor_Selection_Catalog.pdf" },
    { id: "cat5", name: "2026 SWA Project Catalog", file: "../catalogs/2026_SWA_project_catalog.pdf" },
    { id: "cat6", name: "SWA Racking System", file: "../catalogs/SWA_Racking_System.pdf" }
  ];

  function createCatalogModal() {
    if (document.getElementById("catalog-modal")) return;
    
    const lang = document.documentElement.lang || "en";
    const t = {
      title: lang === "ja" ? "カタログのダウンロード" : lang === "tw" ? "下載型錄" : "Download Catalog",
      desc1: lang === "ja" ? "ダウンロードするカタログを選択してください（複数選択可）。" : lang === "tw" ? "請選擇您要下載的型錄 (可多選)。" : "Select the catalogs you wish to download (multiple allowed).",
      desc2: lang === "ja" ? "詳細を入力して、選択したPDFを受け取ります。" : lang === "tw" ? "請輸入您的聯絡資訊以取得 PDF。" : "Enter your details to receive the selected PDFs.",
      next: lang === "ja" ? "次へ" : lang === "tw" ? "下一步" : "Next",
      download: lang === "ja" ? "送信してダウンロード" : lang === "tw" ? "送出並下載" : "Send & Download",
      name: lang === "ja" ? "氏名" : lang === "tw" ? "姓名" : "Full Name",
      email: lang === "ja" ? "勤務先メールアドレス" : lang === "tw" ? "公司信箱" : "Business Email",
      back: lang === "ja" ? "戻る" : lang === "tw" ? "返回" : "Back",
      err: lang === "ja" ? "少なくとも1つのカタログを選択してください。" : lang === "tw" ? "請至少選擇一份型錄。" : "Please select at least one catalog.",
      success: lang === "ja" ? "ありがとうございます！ダウンロードが開始されます。" : lang === "tw" ? "感謝填寫！下載即將開始。" : "Thank you! Downloads will begin shortly."
    };

    const modalHTML = `
      <div class="modal" id="catalog-modal">
        <div class="modal-overlay modal__overlay" id="catalog-overlay"></div>
        <div class="modal-content modal__box" style="max-width: 500px;">
          <button class="modal-close modal__close" id="catalog-close">&times;</button>
          <h3 class="modal__title">${t.title}</h3>
          
          <!-- Step 1: Selection -->
          <div id="catalog-step-1">
            <p class="modal__desc">${t.desc1}</p>
            <div class="catalog-list" style="margin-bottom: 2rem; max-height: 300px; overflow-y: auto; text-align: left; background: var(--bg-alt); padding: 1rem; border-radius: 4px;">
              ${catalogs.map(c => `
                <label style="display: flex; align-items: flex-start; gap: 0.75rem; margin-bottom: 0.75rem; cursor: pointer;">
                  <input type="checkbox" name="selected_catalogs" value="${c.file}" style="margin-top: 0.3rem;">
                  <span style="font-size: 0.95rem; line-height: 1.4;">${c.name}</span>
                </label>
              `).join('')}
            </div>
            <button class="btn btn-primary" id="catalog-next-btn" style="width: 100%;">${t.next}</button>
          </div>

          <!-- Step 2: Form -->
          <div id="catalog-step-2" style="display: none;">
            <p class="modal__desc">${t.desc2}</p>
            <form id="catalog-form">
              <div class="form-field" style="text-align: left;">
                <label for="catalog-name" class="form-label">${t.name}</label>
                <input type="text" id="catalog-name" class="form-input" required>
              </div>
              <div class="form-field" style="text-align: left;">
                <label for="catalog-email" class="form-label">${t.email}</label>
                <input type="email" id="catalog-email" class="form-input" required>
              </div>
              <div style="display: flex; gap: 1rem;">
                <button type="button" class="btn btn-ghost" id="catalog-back-btn" style="flex: 1;">${t.back}</button>
                <button type="submit" class="btn btn-primary" style="flex: 2;">${t.download}</button>
              </div>
            </form>
          </div>
          
        </div>
      </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    const modal = document.getElementById("catalog-modal");
    const closeBtn = document.getElementById("catalog-close");
    const overlay = document.getElementById("catalog-overlay");
    const nextBtn = document.getElementById("catalog-next-btn");
    const backBtn = document.getElementById("catalog-back-btn");
    const form = document.getElementById("catalog-form");
    
    const s1 = document.getElementById("catalog-step-1");
    const s2 = document.getElementById("catalog-step-2");

    const close = () => {
      modal.classList.remove("active");
      setTimeout(() => { s1.style.display = 'block'; s2.style.display = 'none'; form.reset(); }, 300);
    };

    closeBtn.addEventListener("click", close);
    overlay.addEventListener("click", close);

    nextBtn.addEventListener("click", () => {
      const selected = document.querySelectorAll('input[name="selected_catalogs"]:checked');
      if (selected.length === 0) {
        alert(t.err);
        return;
      }
      s1.style.display = 'none';
      s2.style.display = 'block';
    });

    backBtn.addEventListener("click", () => {
      s2.style.display = 'none';
      s1.style.display = 'block';
    });

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const selected = document.querySelectorAll('input[name="selected_catalogs"]:checked');
      
      alert(t.success);
      
      selected.forEach((cb, index) => {
        setTimeout(() => {
          const a = document.createElement("a");
          a.href = cb.value;
          a.download = "";
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        }, index * 500); // Stagger downloads
      });
      
      close();
    });
  }

  createCatalogModal();
  document.querySelectorAll(".open-catalog-btn").forEach(b => {
    b.addEventListener("click", e => { 
      e.preventDefault(); 
      document.getElementById("catalog-modal").classList.add("active"); 
    });
  });"""
    
    # We replace the old block with the new dynamic logic
    main_js = old_js_pattern.sub(new_js, main_js)
    
    with open(main_js_path, 'w', encoding='utf-8') as f:
        f.write(main_js)
        
    print("Updated js/main.js with dynamic multi-step modal logic")

if __name__ == "__main__":
    update_catalog_ui()
