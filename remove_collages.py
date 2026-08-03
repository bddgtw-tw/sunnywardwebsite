import os
import re

def remove_collage_images(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find and remove the uc-img-wrap div completely
    # It looks like:
    # <div class="uc-img-wrap" style="position: relative;">
    #   <div style="position: absolute; ...">Before & After</div>
    #   <img src="../_assets/projects/..." alt="...">
    # </div>
    
    pattern = r'<div class="uc-img-wrap".*?</div>\s*<img src="[^"]*".*?>\s*</div>'
    # Wait, the structure is:
    # <div class="uc-img-wrap" style="position: relative;">
    #   <div style="position: absolute; top: 15px; left: 15px; background: rgba(0,0,0,0.7); color: #fff; padding: 4px 12px; font-size: 0.75rem; font-weight: bold; letter-spacing: 1px; border-radius: 4px; text-transform: uppercase;">Before & After</div>
    #   <img src="../_assets/projects/..." alt="...">
    # </div>
    
    # Let's use a simpler string replacement since we know the exact structure
    
    # Alternative: use regex with re.DOTALL
    pattern = r'<div class="uc-img-wrap".*?</div>\s*</div>'
    # Actually, it's safer to just remove the lines containing uc-img-wrap, the inner div, and the img tag.
    
    lines = content.split('\n')
    new_lines = []
    skip = False
    for line in lines:
        if '<div class="uc-img-wrap"' in line:
            skip = True
        if not skip:
            new_lines.append(line)
        if skip and '</div>' in line and '<img' not in line and 'Before & After' not in line:
            # We found the closing div of uc-img-wrap
            # Wait, the inner div has a closing tag too.
            pass
            
    # Let's use regex with DOTALL to carefully match it.
    new_content = re.sub(r'<div class="uc-img-wrap".*?</div>\s*<img.*?>\s*</div>', '', content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website"
remove_collage_images(os.path.join(base_path, "en", "projects.html"))
remove_collage_images(os.path.join(base_path, "tw", "projects.html"))
remove_collage_images(os.path.join(base_path, "jp", "projects.html"))
print("Successfully removed collage images.")
