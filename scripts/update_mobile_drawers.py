import os
import re

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"

def update_drawers():
    langs = ['tw', 'en', 'jp']
    
    # Text configs for each language
    configs = {
        'tw': {
            'catalog_text': "下載產品型錄",
            'en_style': "color: var(--text-secondary); text-decoration: none;",
            'tw_style': "color: var(--accent); font-weight: bold; text-decoration: none;",
            'jp_style': "color: var(--text-secondary); text-decoration: none;",
            'catalog_action': "open-catalog-btn"
        },
        'en': {
            'catalog_text': "Download Catalog",
            'en_style': "color: var(--accent); font-weight: bold; text-decoration: none;",
            'tw_style': "color: var(--text-secondary); text-decoration: none;",
            'jp_style': "color: var(--text-secondary); text-decoration: none;",
            'catalog_action': "open-catalog-btn"
        },
        'jp': {
            'catalog_text': "カタログをダウンロード",
            'en_style': "color: var(--text-secondary); text-decoration: none;",
            'tw_style': "color: var(--text-secondary); text-decoration: none;",
            'jp_style': "color: var(--accent); font-weight: bold; text-decoration: none;",
            'catalog_action': "open-catalog-btn"
        }
    }
    
    for lang in langs:
        lang_dir = os.path.join(repo_dir, lang)
        if not os.path.exists(lang_dir):
            continue
            
        for file in os.listdir(lang_dir):
            if not file.endswith(".html"):
                continue
                
            path = os.path.join(lang_dir, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Regex to find <nav class="mobile-drawer" id="mobile-drawer">...</nav>
            # Match opening tag, content, and closing tag
            pattern = r'(<nav class="mobile-drawer" id="mobile-drawer">)(.*?)(</nav>)'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                opening_tag = match.group(1)
                links = match.group(2).strip()
                closing_tag = match.group(3)
                
                # Check if we already injected the mobile-drawer-extra
                if 'class="mobile-drawer-extra"' in links:
                    continue
                    
                cfg = configs[lang]
                
                # Special action for catalog download:
                # If page is contact.html, we can redirect to download block or trigger download
                # On contact.html, download button just points to index.html#catalog or opens catalog modal
                # For consistency, we use class="open-catalog-btn" which triggers the modal in main.js!
                extra_html = f"""
    <div class="mobile-drawer-extra" style="margin-top: 2.5rem; display: flex; flex-direction: column; gap: 1.5rem; width: 100%;">
      <button class="btn btn-primary {cfg['catalog_action']}" style="width: 100%;">{cfg['catalog_text']}</button>
      <div class="mobile-lang-links" style="display: flex; gap: 1rem; justify-content: center; align-items: center; width: 100%;">
        <a href="../en/{file}" class="mobile-lang-link" style="font-size: 0.9rem; {cfg['en_style']}">EN</a>
        <span style="color: var(--border);">|</span>
        <a href="../tw/{file}" class="mobile-lang-link" style="font-size: 0.9rem; {cfg['tw_style']}">繁中</a>
        <span style="color: var(--border);">|</span>
        <a href="../jp/{file}" class="mobile-lang-link" style="font-size: 0.9rem; {cfg['jp_style']}">日本語</a>
      </div>
    </div>"""
                
                new_nav_content = links + extra_html
                new_nav = f"{opening_tag}\n    {new_nav_content}\n  {closing_tag}"
                
                content = content.replace(match.group(0), new_nav)
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"Updated mobile drawer in {lang}/{file}")

if __name__ == "__main__":
    update_drawers()
