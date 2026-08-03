import pypdf
import os

pdf_dir = r"F:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward"
files = [
    "2026 SWA project catalog.pdf",
    "2026 SWA Outdoor Selection Catalog.pdf",
    "2026 Sunnyward Balau wood outdoor furniture catalogue.pdf",
    "2025 Funife Premium Outdoor catalogue A4.pdf",
    "SWA Racking System.pdf"
]

for filename in files:
    path = os.path.join(pdf_dir, filename)
    if not os.path.exists(path):
        print(f"Skipping: {filename} (not found)")
        continue
    
    reader = pypdf.PdfReader(path)
    print(f"\n======================================")
    print(f"FILE: {filename}")
    print(f"Total Pages: {len(reader.pages)}")
    
    # Print first page that has text
    for p_idx in range(min(15, len(reader.pages))):
        text = reader.pages[p_idx].extract_text()
        if text and len(text.strip()) > 30:
            print(f"--- First Text Page found at Page {p_idx+1} ---")
            print(text[:800])
            break
