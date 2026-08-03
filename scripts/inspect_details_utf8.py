import pypdf
import os
import sys

pdf_dir = r"F:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward"

def inspect_pdf(filename, start_page, end_page, out_file):
    path = os.path.join(pdf_dir, filename)
    if not os.path.exists(path):
        out_file.write(f"\nSKIPPED NOT FOUND: {filename}\n")
        return
    reader = pypdf.PdfReader(path)
    out_file.write(f"\n======================================\n")
    out_file.write(f"FILE: {filename} (Pages {start_page} to {end_page})\n")
    for i in range(start_page - 1, min(end_page, len(reader.pages))):
        text = reader.pages[i].extract_text()
        out_file.write(f"--- Page {i+1} ---\n")
        if text:
            out_file.write(text)
            out_file.write("\n")
        else:
            out_file.write("[No text found / scanned image]\n")

with open("inspect_details.txt", "w", encoding="utf-8") as f:
    inspect_pdf("2026 SWA project catalog.pdf", 3, 28, f)
    inspect_pdf("2026 SWA Outdoor Selection Catalog.pdf", 3, 40, f)
    inspect_pdf("2026 Sunnyward Balau wood outdoor furniture catalogue.pdf", 2, 16, f)
    inspect_pdf("2025 Funife Premium Outdoor catalogue A4.pdf", 2, 37, f)
    inspect_pdf("SWA Racking System.pdf", 1, 19, f)

print("Inspection completed, saved to inspect_details.txt")
