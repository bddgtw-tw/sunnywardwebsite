import pypdf
import os

pdf_dir = r"F:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward"

def inspect_pdf(filename, start_page, end_page):
    path = os.path.join(pdf_dir, filename)
    if not os.path.exists(path):
        return
    reader = pypdf.PdfReader(path)
    print(f"\n======================================")
    print(f"FILE: {filename} (Pages {start_page} to {end_page})")
    for i in range(start_page - 1, min(end_page, len(reader.pages))):
        text = reader.pages[i].extract_text()
        print(f"--- Page {i+1} ---")
        if text:
            print(text[:1500])
        else:
            print("[No text found / scanned image]")

print("INSPECTING DETAILS:")
inspect_pdf("2026 SWA project catalog.pdf", 3, 10)
inspect_pdf("2026 SWA Outdoor Selection Catalog.pdf", 3, 15)
inspect_pdf("2026 Sunnyward Balau wood outdoor furniture catalogue.pdf", 2, 8)
inspect_pdf("2025 Funife Premium Outdoor catalogue A4.pdf", 2, 8)
inspect_pdf("SWA Racking System.pdf", 2, 8)
