import os
import re

repo_dir = r"C:\Users\bddgt\Documents\antigravity\wonderful-volta\sunnywardwebsite"

def split_html_categories():
    # TW
    tw_path = os.path.join(repo_dir, "tw", "products.html")
    with open(tw_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('office: "商用辦公桌椅",', 'office_chairs: "人體工學辦公椅",\n      office_desks: "商用辦公桌與家具",')
    with open(tw_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated tw/products.html")

    # EN
    en_path = os.path.join(repo_dir, "en", "products.html")
    with open(en_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('office: "Office Desks & Chairs",', 'office_chairs: "Office Chairs",\n      office_desks: "Office Desks & Furniture",')
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated en/products.html")

    # JP
    jp_path = os.path.join(repo_dir, "jp", "products.html")
    with open(jp_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('office: "オフィスデスク・オフィスチェア",', 'office_chairs: "オフィスチェア",\n      office_desks: "オフィスデスク・家具",')
    # fallback if different spacing/translation
    if 'office_chairs' not in content:
        content = content.replace('office: "オフィス家具",', 'office_chairs: "オフィスチェア",\n      office_desks: "オフィスデスク・家具",')
    # Fix dining chair translation from "デザインチェア" (design chair) to "ダイニングチェア" (dining chair)
    content = content.replace('dining: "デザインチェア",', 'dining: "ダイニングチェア",')
    with open(jp_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated jp/products.html")

if __name__ == "__main__":
    split_html_categories()
