#!/usr/bin/env python3
import os, re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
img_dir = root / "Product_Images"

file_map = {}
for p in img_dir.glob("**/*"):
    if p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
        rel = p.relative_to(img_dir).as_posix()
        file_map[p.name] = rel

print(f"Built index of {len(file_map)} files in Product_Images")

# Fix all HTML files under en/, tw/, jp/ (including product and project subpages)
for lang in ("en", "tw", "jp"):
    lang_dir = root / lang
    for html_file in lang_dir.rglob("*.html"):
        text = html_file.read_text(encoding="utf-8")

        # Determine correct relative prefix depth
        depth = len(html_file.relative_to(lang_dir).parts) - 1
        prefix = "../" * (depth + 1)

        def fix_src(m):
            src = m.group(1)
            if "Product_Images/" in src:
                fname = src.split("/")[-1]
                if fname in file_map:
                    return f'src="{prefix}Product_Images/{file_map[fname]}"'
            return m.group(0)

        new_text = re.sub(r'src="([^"]*Product_Images/[^"]+)"', fix_src, text)
        if new_text != text:
            html_file.write_text(new_text, encoding="utf-8", newline="\n")
            print(f"Fixed image paths in {html_file.relative_to(root)}")
