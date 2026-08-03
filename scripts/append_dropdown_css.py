import os

css_path = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite\css\style.css"

dropdown_css = """
/* SIDEBAR DROPDOWN UX */
.arrow-icon {
  display: inline-block;
  font-size: 0.55rem;
  margin-right: 0.5rem;
  transition: transform var(--t-fast) ease;
  vertical-align: middle;
  opacity: 0.6;
}
.cat-btn.open .arrow-icon {
  transform: rotate(90deg);
}
.subcat-dropdown {
  list-style: none !important;
  padding-left: 1.2rem !important;
  margin: 0.3rem 0 0.8rem 0 !important;
  border-left: 1px solid var(--border) !important;
}
.subcat-dropdown li {
  margin-bottom: 0.25rem !important;
  list-style-type: none !important; /* Force remove default bullets */
}
.subcat-dropdown a {
  font-size: 0.8rem !important;
  color: var(--text-secondary) !important;
  text-decoration: none !important;
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  padding: 0.25rem 0.5rem !important;
  border-radius: 4px !important;
  transition: all var(--t-fast) ease !important;
  font-family: var(--font-sans) !important;
}
.subcat-dropdown a:hover {
  background: rgba(184, 142, 107, 0.08) !important;
  color: var(--accent) !important;
}
.subcat-dropdown a.active {
  color: var(--accent) !important;
  font-weight: 500 !important;
  background: rgba(184, 142, 107, 0.08) !important;
}
.subcat-count {
  font-size: 0.75rem !important;
  color: var(--stone) !important;
  background: none !important;
  padding: 0 !important;
}
.subcat-dropdown a.active .subcat-count {
  color: var(--accent) !important;
}

/* SIDEBAR SEARCH UX */
.sidebar-search {
  position: relative !important;
  margin-bottom: 1.5rem !important;
  width: 100% !important;
  box-sizing: border-box !important;
}
.sidebar-search input {
  width: 100% !important;
  padding: 0.65rem 2.2rem 0.65rem 1rem !important;
  font-size: 0.82rem !important;
  font-family: var(--font-sans) !important;
  color: var(--text-primary) !important;
  border: 1px solid var(--border-strong) !important;
  background: var(--white) !important;
  border-radius: 2px !important;
  outline: none !important;
  box-sizing: border-box !important;
  transition: all var(--t-fast) !important;
}
.sidebar-search input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(184, 142, 107, 0.15) !important;
}
.search-clear-btn {
  position: absolute !important;
  right: 0.8rem !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  cursor: pointer !important;
  color: var(--stone) !important;
  font-size: 0.85rem !important;
  opacity: 0 !important;
  visibility: hidden !important;
  transition: all var(--t-fast) !important;
}
.search-clear-btn.visible {
  opacity: 1 !important;
  visibility: visible !important;
}
.search-clear-btn:hover {
  color: var(--accent) !important;
}
"""

if os.path.exists(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if '/* SIDEBAR DROPDOWN UX */' not in content:
        with open(css_path, 'a', encoding='utf-8') as f:
            f.write(dropdown_css)
        print("Successfully appended dropdown CSS to css/style.css")
    else:
        print("Dropdown CSS already present in css/style.css")
