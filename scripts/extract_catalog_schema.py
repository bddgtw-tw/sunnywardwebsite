import pypdf
import os
import csv
import re

pdf_path = r"F:\共用雲端硬碟\資料庫\Raw_Product_Data_Sunnyward\2026 SWA Office Furniture Specification.pdf"
output_csv = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website\Sunnyward_Office_Furniture.csv"

# Columns requested by the user
columns = [
    "分類號", "SKU", "EAN", "品牌", "主分類", "子分類", "品名", "尺寸", "件數", "顏色",
    "圖片", "重量(g)", "材質", "產地", "關鍵字", "hashtags", "Meta Description", "商品說明",
    "商品特色", "影片標題", "主題影片", "額外資訊", "注意事項", "使用方式", "品牌資訊",
    "延伸介紹", "社群上的我們", "社群媒體", "產品簡稱", "賣點金句", "主題詞", "零售價(NTD)",
    "預估成本(NTD)", "庫存", "日本零售價", "長", "寬", "高", "含運售價", "新竹貨運運費",
    "超取", "超取費用", "英文圖片名稱", "Flickr照片組", "Google雲端照片位置", "Google封面照片",
    "Google產品選項照片", "中文標籤", "中文標籤圖檔位置", "品牌照片"
]

reader = pypdf.PdfReader(pdf_path)
products = []

print("Total pages:", len(reader.pages))

for page_idx, page in enumerate(reader.pages):
    text = page.extract_text()
    if not text:
        continue
    
    # We want to identify titles like "ST-MN01 Director Table"
    # Patterns look like: ST-XXXX or other alphanumeric prefixes
    # Let's search for lines containing table or furniture names and their dimensions (e.g. 2000W x 1000D x 750H mm)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    current_product = None
    
    for idx, line in enumerate(lines):
        # Look for model codes: e.g., ST-MN01, ST-DM01, ST-LN 01, etc.
        match = re.search(r'\b([A-Z0-9]+-[A-Z0-9\s]+)\b', line)
        if match and ("Table" in line or "Chair" in line or "Cabinet" in line or "Workstation" in line or "Director" in line or "Conference" in line or "Pedestal" in line or "Credenza" in line):
            sku_raw = match.group(1).strip()
            # Clean up space in SKU like "ST-LN 01" to "ST-LN01"
            sku = re.sub(r'\s+', '', sku_raw)
            name = line.strip()
            
            # Find dimensions
            dims = ""
            width = ""
            depth = ""
            height = ""
            
            # Look for dimensions in the next few lines: e.g. "2000W x 1000D x 750H mm"
            for j in range(1, min(4, len(lines) - idx)):
                next_line = lines[idx + j]
                dim_match = re.search(r'(\d+)W\s*x\s*(\d+)D\s*x\s*(\d+)H', next_line, re.IGNORECASE)
                if dim_match:
                    dims = next_line
                    width = dim_match.group(1)
                    depth = dim_match.group(2)
                    height = dim_match.group(3)
                    break
            
            # Extract specs/features
            specs = []
            capture_specs = False
            for j in range(1, min(15, len(lines) - idx)):
                spec_line = lines[idx + j]
                if "Specification" in spec_line:
                    capture_specs = True
                    continue
                if capture_specs:
                    # Stop if we hit another product or categories
                    if re.search(r'\b([A-Z0-9]+-[A-Z0-9\s]+)\b', spec_line) and any(kw in spec_line for kw in ["Table", "Chair", "Cabinet", "Workstation"]):
                        break
                    if "Colour Option" in spec_line or "Color Option" in spec_line:
                        break
                    specs.append(spec_line)
            
            spec_str = " | ".join(specs)
            
            # Formulate basic record
            row_data = {k: "" for k in columns}
            row_data["SKU"] = sku
            row_data["品牌"] = "Sunnyward"
            row_data["主分類"] = "商用家具 / 辦公家具"
            
            # Infer subcategory from name
            subcat = "主管桌" if "Director" in name else "會議桌" if "Conference" in name else "辦公桌" if "Table" in name else "辦公椅" if "Chair" in name else "櫃子" if "Cabinet" in name else "工作站" if "Workstation" in name else "其他辦公家具"
            row_data["子分類"] = subcat
            row_data["品名"] = name
            row_data["尺寸"] = dims
            row_data["長"] = width # W
            row_data["寬"] = depth # D
            row_data["高"] = height # H
            row_data["商品說明"] = f"{name}。專為商業及辦公空間設計之工程級家具。"
            row_data["商品特色"] = spec_str
            row_data["產地"] = "馬來西亞"
            row_data["庫存"] = "客製接單生產"
            row_data["關鍵字"] = f"辦公家具, 主管桌, 會議桌, Sunnyward, {sku}"
            
            products.append(row_data)

# Write to CSV
with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    for prod in products:
        writer.writerow(prod)

print(f"Extraction complete! Extracted {len(products)} products and saved to {output_csv}")
