import os
import shutil

def copy_catalogs():
    source_dir = r"f:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward"
    target_dir = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website\catalogs"
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    pdfs = [
        "2025 Funife Premium Outdoor catalogue A4.pdf",
        "2026 Sunnyward Balau wood outdoor furniture catalogue.pdf",
        "2026 SWA Office Furniture Specification.pdf",
        "2026 SWA Outdoor Selection Catalog.pdf",
        "2026 SWA project catalog.pdf",
        "SWA Racking System.pdf"
    ]
    
    for pdf in pdfs:
        src = os.path.join(source_dir, pdf)
        # Make filename URL friendly by replacing spaces with underscores
        friendly_name = pdf.replace(" ", "_")
        dst = os.path.join(target_dir, friendly_name)
        
        if os.path.exists(src):
            print(f"Copying {pdf} to {friendly_name}...")
            shutil.copy2(src, dst)
        else:
            print(f"File not found: {src}")

if __name__ == "__main__":
    copy_catalogs()
