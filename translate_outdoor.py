import json
import os
import re

def translate_text(text, lang):
    if not text:
        return text
        
    # Dictionary for translations
    dict_tw = {
        "REVIERA table": "REVIERA 戶外餐桌",
        "REVIERA single chair": "REVIERA 單人休閒椅",
        "REVIERA three seater chair": "REVIERA 三人沙發",
        "Coffe Table": "戶外咖啡桌",
        "Occasional Chair": "休閒單椅",
        "Rect Table": "長方餐桌",
        "Square table": "方型餐桌",
        "Armchair": "扶手椅",
        "Highback Armchair": "高背扶手椅",
        "Extention Table": "延伸餐桌",
        "Sunlounger": "日光躺椅",
        "Side table": "邊桌",
        "Material:": "材質：",
        "Top:": "桌面：",
        "Seat & Back Cushion:": "座墊與靠枕：",
        "Seat & Back:": "座背材質：",
        "OAK Wood Look Aluminum": "橡木紋鋁合金",
        "Acrylic fabric grey color": "灰色壓克力布料",
        "Anthracite Aluminum": "無煙煤色鋁合金",
        "Indian HPL": "印度 HPL 高壓層壓板",
        "Dark Grey": "深灰色",
        "Glass with ceramic finish": "陶瓷飾面玻璃",
        "Teak wood": "柚木",
        "White Aluminum": "白色鋁合金",
        "White color": "白色",
        "Light grey": "淺灰色",
        "Beige Max Rope": "米色 Max 編織繩",
        "Beige color": "米色",
        "Greige Max Rope": "灰褐色 Max 編織繩",
        "Greige": "灰褐色",
        "Charcoal textilene": "炭黑色特斯林網布",
        "Khaki textilene": "卡其色特斯林網布",
        "Olefin fabric dark grey": "深灰色 Olefin 布料",
        "Aluminum with": "鋁合金搭配",
        "Aluminum": "鋁合金",
    }
    
    dict_jp = {
        "REVIERA table": "REVIERA アウトドアテーブル",
        "REVIERA single chair": "REVIERA シングルチェア",
        "REVIERA three seater chair": "REVIERA 3人掛けソファ",
        "Coffe Table": "コーヒーテーブル",
        "Occasional Chair": "ラウンジチェア",
        "Rect Table": "長方形テーブル",
        "Square table": "正方形テーブル",
        "Armchair": "アームチェア",
        "Highback Armchair": "ハイバックアームチェア",
        "Extention Table": "エクステンションテーブル",
        "Sunlounger": "サンラウンジャー",
        "Side table": "サイドテーブル",
        "Material:": "材質：",
        "Top:": "天板：",
        "Seat & Back Cushion:": "シート＆背もたれクッション：",
        "Seat & Back:": "シート＆背もたれ：",
        "OAK Wood Look Aluminum": "オーク木目調アルミニウム",
        "Acrylic fabric grey color": "グレーアクリル生地",
        "Anthracite Aluminum": "アンスラサイトアルミニウム",
        "Indian HPL": "インド産HPL（高圧メラミン）",
        "Dark Grey": "ダークグレー",
        "Glass with ceramic finish": "セラミック仕上げガラス",
        "Teak wood": "チーク材",
        "White Aluminum": "ホワイトアルミニウム",
        "White color": "ホワイト",
        "Light grey": "ライトグレー",
        "Beige Max Rope": "ベージュMaxロープ",
        "Beige color": "ベージュ",
        "Greige Max Rope": "グレージュMaxロープ",
        "Greige": "グレージュ",
        "Charcoal textilene": "チャコールテスリン",
        "Khaki textilene": "カーキテスリン",
        "Olefin fabric dark grey": "ダークグレーオレフィン生地",
        "Aluminum with": "アルミニウム・",
        "Aluminum": "アルミニウム",
    }

    target_dict = dict_tw if lang == 'tw' else dict_jp

    # Simple replace
    result = text
    # Replace longer phrases first
    for k in sorted(target_dict.keys(), key=len, reverse=True):
        result = result.replace(k, target_dict[k])
        
    return result

def main():
    base_dir = "c:/Users/bddgt/.gemini/antigravity/scratch/sunnyward-website"
    languages = ['tw', 'jp']
    
    for lang in languages:
        filepath = os.path.join(base_dir, lang, "products.json")
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        products = data.get("products", [])
        
        for p in products:
            if p.get("category") == "Outdoor":
                # Translate name
                p["name"] = translate_text(p.get("name", ""), lang)
                
                # Translate description
                p["description"] = translate_text(p.get("description", ""), lang)
                
                # Translate materials array
                materials = p.get("materials", [])
                new_materials = [translate_text(m, lang) for m in materials]
                p["materials"] = new_materials
                
                # We can also translate specs if needed, but they are mostly numbers.
                specs = p.get("specs", [])
                new_specs = [translate_text(s, lang) for s in specs]
                p["specs"] = new_specs

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({"products": products}, f, indent=2, ensure_ascii=False)
            
        print(f"Translated outdoor products for {lang}/products.json")

if __name__ == "__main__":
    main()
