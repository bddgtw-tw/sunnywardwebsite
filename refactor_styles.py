import os
import re

base_dir = r'c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website'

def remove_inline_styles():
    for lang in ['tw', 'en', 'jp']:
        path = os.path.join(base_dir, lang, 'products.html')
        if not os.path.exists(path): continue
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Modal 1: Product Detail
        content = content.replace('style="max-width: 700px; padding: 2rem;"', 'class="modal-content modal__box modal-product-detail"')
        content = content.replace('style="display: flex; gap: 2rem; flex-wrap: wrap; align-items: flex-start;"', 'class="modal-product-layout"')
        content = content.replace('style="flex: 1; min-width: 250px;"', 'class="modal-product-gallery"')
        content = content.replace('style="width: 100%; border-radius: 8px; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"', '')
        content = content.replace('style="flex: 1.2; min-width: 280px;"', 'class="modal-product-info"')
        content = content.replace('style="font-size: 0.75rem; letter-spacing: 0.1em; color: var(--copper);"', 'class="eyebrow modal-product-sku"')
        content = content.replace('style="margin-top: 0.3rem; margin-bottom: 0.8rem; font-size: 1.5rem;"', 'class="modal__title modal-product-title"')
        content = content.replace('style="font-size: 0.85rem; color: #666; margin-bottom: 1.2rem; line-height: 1.6;"', 'class="modal-product-desc"')
        content = content.replace('style="font-size: 0.82rem; line-height: 1.8; border-top: 1px solid #eee; padding-top: 1rem; color: #444;"', 'class="modal-product-meta"')
        content = content.replace('style="margin-top: 1.5rem; border-top: 1px solid #eee; padding-top: 1.2rem;"', 'class="modal-product-specs-wrap"')
        content = content.replace('style="margin-bottom: 0.6rem; font-size: 0.9rem; color: #2e2722;"', 'class="modal-product-specs-title"')
        content = content.replace('style="font-size: 0.82rem; color: #555; padding-left: 1.2rem; line-height: 1.8; margin: 0;"', 'class="modal-product-specs-list"')
        content = content.replace('style="margin-top: 2rem; display: flex; gap: 1rem;"', 'class="modal-product-actions"')
        content = content.replace('style="display:flex; flex-direction:column; gap:.35rem; min-width:120px; font-size:.72rem; font-weight:600; letter-spacing:.08em; text-transform:uppercase;"', 'class="modal-qty-label"')
        content = content.replace('style="padding:.72rem;"', '')
        content = content.replace('style="flex: 1; padding: 0.8rem;"', '')
        
        # Modal 2: RFQ
        content = content.replace('style="max-width: 550px; padding: 2rem;"', 'class="modal-content modal__box modal-rfq"')
        content = content.replace('style="font-weight: 600; color: var(--copper); margin-bottom: 1.2rem;"', 'class="modal__desc rfq-product-info"')
        content = content.replace('style="display: flex; gap: 1rem;"', 'class="rfq-form-row"')
        content = content.replace('style="flex: 1;"', '')
        content = content.replace('style="resize: vertical; font-family: inherit; font-size: 0.85rem; padding: 0.75rem; width: 100%; border: 1px solid #ddd; border-radius: 4px;"', 'class="form-input rfq-textarea"')
        content = content.replace('style="width: 100%; padding: 1rem; margin-top: 0.5rem;"', 'class="btn btn-primary rfq-submit-btn"')
        content = content.replace('style="display: none; text-align: center; padding: 2rem 0;"', '')
        content = content.replace('style="width: 60px; height: 60px; border-radius: 50%; background: #e8f5e9; color: #2e7d32; display: flex; align-items: center; justify-content: center; font-size: 2rem; margin: 0 auto 1.5rem;"', 'class="rfq-success-icon"')
        content = content.replace('style="margin-bottom: 0.8rem; font-size: 1.2rem; color: #2e2722;"', 'class="rfq-success-title"')
        content = content.replace('style="font-size: 0.88rem; color: #666; line-height: 1.6; margin-bottom: 1.5rem;"', 'class="rfq-success-msg"')
        content = content.replace('style="font-size: 0.78rem; display: block; margin-top: 1rem; color: #888;"', 'class="rfq-success-note"')
        content = content.replace('style="padding: 0.75rem 2rem;"', '')
        
        # JS render template
        content = content.replace('style="display:flex; justify-content:space-between; align-items:flex-start;"', 'class="product-card__name-row"')
        content = content.replace('style="font-size:0.68rem; background:#eae5e0; padding:2px 6px; border-radius:4px; font-weight:normal; color:#777;"', 'class="product-card__sku-badge"')
        content = content.replace('style="font-size:0.8rem; margin-top:0.3rem; color:#666; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;"', 'class="product-card__desc-text"')
        content = content.replace('style="font-size:0.72rem; color:#888;"', 'class="product-card__dims-text"')
        content = content.replace('style="font-size:0.7rem;"', '')
        
        # Some generic removals
        content = content.replace('style="padding-top:calc(var(--nav-h) + 4rem); padding-bottom:4rem;"', '')
        content = content.replace('style="margin-top:1rem; max-width:54ch;"', '')
        content = content.replace('style="padding-top:2rem;"', '')
        content = content.replace('style="width:100%; padding:1rem;"', '')
        content = content.replace('style="margin-bottom:4rem;"', '')
        content = content.replace('style="font-size:2.5rem; color:var(--copper);"', '')
        content = content.replace('style="margin-top:0; border-radius:0;"', '')
        content = content.replace('style="padding:0;"', '')
        content = content.replace('style="font-size:0.78rem; padding:0.75rem 1.8rem;"', '')
        content = content.replace('style="cursor: pointer;"', '')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

def append_css():
    css_path = os.path.join(base_dir, 'css', 'style.css')
    if not os.path.exists(css_path): return
    
    css_content = """

/* --- Refactored Components (Products & Modals) --- */
.section--tint { padding-top: calc(var(--nav-h) + 4rem); padding-bottom: 4rem; }
.catalog-header p { margin-top: 1rem; max-width: 54ch; }
.catalog-layout-section { padding-top: 2rem; }

/* Product Detail Modal */
.modal-product-detail { max-width: 900px; padding: 2.5rem; }
.modal-product-layout { display: flex; gap: 2.5rem; align-items: flex-start; }
@media (max-width: 768px) {
  .modal-product-layout { flex-direction: column; gap: 1.5rem; }
}
.modal-product-gallery { flex: 1; min-width: 300px; }
.modal-product-gallery img { width: 100%; border-radius: 8px; object-fit: cover; box-shadow: var(--shadow-sm, 0 4px 12px rgba(0,0,0,0.1)); }
.modal-product-info { flex: 1.2; min-width: 280px; }
.modal-product-sku { font-size: 0.75rem; letter-spacing: 0.1em; color: var(--copper); display: block; }
.modal-product-title { margin-top: 0.4rem; margin-bottom: 0.8rem; font-size: 1.8rem; line-height: 1.2; }
.modal-product-desc { font-size: 0.9rem; color: #555; margin-bottom: 1.5rem; line-height: 1.6; }
.modal-product-meta { font-size: 0.85rem; line-height: 1.8; border-top: 1px solid #eee; padding-top: 1.2rem; color: #444; }
.modal-product-specs-wrap { margin-top: 1.5rem; border-top: 1px solid #eee; padding-top: 1.2rem; }
.modal-product-specs-title { margin-bottom: 0.8rem; font-size: 0.95rem; font-weight: 600; color: #2e2722; }
.modal-product-specs-list { font-size: 0.85rem; color: #555; padding-left: 1.2rem; line-height: 1.8; margin: 0; }
.modal-product-actions { margin-top: 2rem; display: flex; gap: 1rem; }
.modal-qty-label { display: flex; flex-direction: column; gap: 0.4rem; min-width: 120px; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; color: #444; }
.modal-qty-label input { padding: 0.8rem; font-size: 1rem; }
#modal-inquire-btn { flex: 1; padding: 1rem; font-size: 0.95rem; }

/* RFQ Modal */
.modal-rfq { max-width: 650px; padding: 2.5rem; }
.rfq-product-info { font-weight: 600; color: var(--copper); margin-bottom: 1.5rem; font-size: 1.05rem; }
.rfq-form-row { display: flex; gap: 1rem; }
@media (max-width: 500px) {
  .rfq-form-row { flex-direction: column; gap: 0; }
}
.rfq-textarea { resize: vertical; font-family: inherit; font-size: 0.9rem; padding: 0.85rem; width: 100%; border: 1px solid #ddd; border-radius: 4px; }
.rfq-submit-btn { width: 100%; padding: 1rem; margin-top: 1rem; font-size: 1rem; }
.rfq-success-icon { width: 64px; height: 64px; border-radius: 50%; background: #e8f5e9; color: #2e7d32; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto 1.5rem; }
.rfq-success-title { margin-bottom: 1rem; font-size: 1.4rem; color: #2e2722; font-weight: 600; }
.rfq-success-msg { font-size: 0.95rem; color: #555; line-height: 1.6; margin-bottom: 2rem; }
.rfq-success-note { font-size: 0.85rem; display: block; margin-top: 1.2rem; color: #888; }

/* Product Card Enhancements */
.product-card { cursor: pointer; display: flex; flex-direction: column; }
.product-card__name-row { display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; }
.product-card__sku-badge { font-size: 0.65rem; background: #f0ebe6; padding: 2px 8px; border-radius: 4px; font-weight: 600; color: #666; letter-spacing: 0.05em; }
.product-card__desc-text { font-size: 0.85rem; margin-top: 0.5rem; color: #666; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.5; }
.product-card__dims-text { font-size: 0.75rem; color: #888; }
.product-card .btn-arrow { font-size: 0.75rem; padding: 0.3rem 0; }
"""
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write(css_content)

remove_inline_styles()
append_css()
print('Styles refactored.')
