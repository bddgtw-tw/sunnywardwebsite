import json
import os
import re

base_dir = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"

def is_header(p):
    sku = p.get("sku", "")
    return "Supplier code number" in sku or "SKU" in sku or not sku

def sanitize_en(p):
    if is_header(p): return None
    # Origin
    if "Malaysia" in p.get("origin", ""):
        p["origin"] = "Made in Malaysia"
    # Dims
    if p.get("dims"):
        p["dims"] = p["dims"].replace("約", "Approx. ")
    # Specs
    new_specs = []
    for s in p.get("specs", []):
        if "頂級 Balau 硬木製造" in s:
            new_specs.append("Premium Balau hardwood construction, moisture and corrosion resistant.")
        else:
            s = s.replace("包裝", "Package").replace("箱", "ctn").replace("件", "pc")
            new_specs.append(s)
    p["specs"] = new_specs
    
    # Material
    if "材質：" in p.get("material", ""):
        p["material"] = p["material"].replace("材質：", "Material: ")
    return p

def sanitize_tw(p):
    if is_header(p): return None
    # Origin
    origin = p.get("origin", "")
    if "Malaysia" in origin or "馬來西亞" in origin:
        p["origin"] = "馬來西亞製"
    elif "China" in origin:
        p["origin"] = "中國製"
        
    # Specs
    new_specs = []
    for s in p.get("specs", []):
        s = s.replace("Package:", "包裝：")
        s = s.replace("pc/ctn", "入/箱")
        s = s.replace("Measurement:", "包裝尺寸：")
        s = s.replace("CBM:", "材積(CBM)：")
        s = s.replace("40HQ Capacity:", "40HQ櫃裝載量：")
        new_specs.append(s)
    p["specs"] = new_specs
    
    # Material
    if p.get("material"):
        m = p["material"]
        m = m.replace("OAK Wood Look Aluminum", "橡木紋鋁合金")
        m = m.replace("Main Material: Premium Grade Balau Hardwood (Shorea Wood)", "主材質：頂級 Balau 硬木 (Shorea 木)")
        m = m.replace("Anthracite Aluminum and Glass with ceramic finish", "碳灰色鋁合金與陶瓷玻璃桌面")
        m = m.replace("Anthracite Aluminum w/ Acrylic rope", "碳灰色鋁合金與亞克力編織繩")
        m = m.replace("Anthracite Aluminum w/ Batyline", "碳灰色鋁合金與 Batyline 網布")
        m = m.replace("Anthracite Aluminum", "碳灰色鋁合金")
        m = m.replace("anthracite Aluminum", "碳灰色鋁合金")
        m = m.replace("Greige Aluminum and Glass with ceramic finish", "灰褐色鋁合金與陶瓷玻璃桌面")
        m = m.replace("Aluminum with Greige Max Rope", "鋁合金與灰褐色 Max 編織繩")
        m = m.replace("Light Grey Aluminum", "淺灰色鋁合金")
        m = m.replace("Aluminum Light Grey", "淺灰色鋁合金")
        m = m.replace("Material:", "材質：")
        m = re.sub(r'^[■ ]+', '', m)
        p["material"] = m
        
    # Desc
    if p.get("tab") == "outdoor":
        name = p.get("name", "")
        # Generic TW desc replacing English boilerplate
        if "engineered to meet the highest demands" in p.get("desc", ""):
            p["desc"] = f"{name} 專為高頻率商業環境與精緻工作空間所設計。結合嚴選頂級材質與堅固結構，提供卓越的穩定性與長期耐用性。其簡約俐落的線條能完美融入企業辦公室、會議室、高級咖啡廳及餐飲空間，帶來極致舒適的體驗。"
    return p

def sanitize_jp(p):
    if is_header(p): return None
    # Origin
    origin = p.get("origin", "")
    if "Malaysia" in origin or "馬來西亞" in origin or "マレーシア" in origin:
        p["origin"] = "マレーシア製"
    elif "China" in origin:
        p["origin"] = "中国製"
        
    # Dims
    if p.get("dims"):
        p["dims"] = p["dims"].replace("約", "約 ") # native
    # Specs
    new_specs = []
    for s in p.get("specs", []):
        s = s.replace("Package:", "梱包：")
        s = s.replace("pc/ctn", "個/箱")
        s = s.replace("Measurement:", "梱包サイズ：")
        s = s.replace("CBM:", "容積(CBM)：")
        s = s.replace("40HQ Capacity:", "40HQ積載量：")
        # any chinese left
        s = s.replace("頂級 Balau 硬木製造，防潮防腐蝕", "最高級のバロー材を使用し、耐湿性と耐腐食性に優れています")
        new_specs.append(s)
    p["specs"] = new_specs
    
    # Material
    if p.get("material"):
        m = p["material"]
        m = m.replace("OAK Wood Look Aluminum", "オーク調アルミ")
        m = m.replace("Main Material: Premium Grade Balau Hardwood (Shorea Wood)", "主素材：最高級バロー材（ショレアウッド）")
        m = m.replace("Anthracite Aluminum and Glass with ceramic finish", "アンスラサイトアルミ・セラミックガラス仕上げ")
        m = m.replace("Anthracite Aluminum w/ Acrylic rope", "アンスラサイトアルミ・アクリルロープ")
        m = m.replace("Anthracite Aluminum w/ Batyline", "アンスラサイトアルミ・バティライン")
        m = m.replace("Anthracite Aluminum", "アンスラサイトアルミ")
        m = m.replace("anthracite Aluminum", "アンスラサイトアルミ")
        m = m.replace("Greige Aluminum and Glass with ceramic finish", "グレージュアルミ・セラミックガラス仕上げ")
        m = m.replace("Aluminum with Greige Max Rope", "アルミ・グレージュ Max ロープ")
        m = m.replace("Light Grey Aluminum", "ライトグレーアルミ")
        m = m.replace("Aluminum Light Grey", "ライトグレーアルミ")
        m = m.replace("Material:", "材質：")
        m = m.replace("材質：", "材質：")
        m = re.sub(r'^[■ ]+', '', m)
        p["material"] = m
        
    # Desc
    if p.get("tab") == "outdoor":
        name = p.get("name", "")
        if "engineered to meet the highest demands" in p.get("desc", ""):
            p["desc"] = f"{name} は、利用頻度の高い商業環境や洗練されたワークスペースの厳しい要求に応えるように設計されています。厳選された最高級の素材と堅牢な構造を組み合わせることで、卓越した安定性と長期的な耐久性を実現しています。あらゆる空間にシームレスに溶け込みます。"
    return p

for lang in ['en', 'tw', 'jp']:
    path = os.path.join(base_dir, lang, "products.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        new_data = []
        for p in data:
            if lang == 'en': p = sanitize_en(p)
            elif lang == 'tw': p = sanitize_tw(p)
            elif lang == 'jp': p = sanitize_jp(p)
            
            if p is not None:
                new_data.append(p)
            
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
            
        print(f"Sanitized JSON for {lang}")
