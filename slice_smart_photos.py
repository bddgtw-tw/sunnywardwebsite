import os
from PIL import Image

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website\_assets\projects"

def slice_smart(image_name):
    img_path = os.path.join(base_path, image_name)
    if not os.path.exists(img_path):
        return
        
    try:
        with Image.open(img_path) as img:
            width, height = img.size
            
            # Smart Slicing Logic:
            # We crop the right-hand side main content box (roughly 33% to 95% width, 18% to 85% height)
            # This contains the actual photos and avoids the left vertical header banner and title.
            top = height * 0.18
            bottom = height * 0.85
            left = width * 0.32
            right = width * 0.96
            
            main_block = img.crop((left, top, right, bottom))
            mw, mh = main_block.size
            
            # Quadrants with 2.5% padding to slice out grid lines/borders/internal texts
            pad_x = mw * 0.025
            pad_y = mh * 0.025
            
            mid_x = mw / 2
            mid_y = mh / 2
            
            # Crop 4 photos:
            # We also shave off the top 20% of the top quadrant images (q1, q2) 
            # if they contain the big brown "BEFORE" / "AFTER" banners.
            q1_top = (mid_y - pad_y) * 0.20
            q2_top = (mid_y - pad_y) * 0.20
            
            q1 = main_block.crop((0, q1_top, mid_x - pad_x, mid_y - pad_y))
            q2 = main_block.crop((mid_x + pad_x, q2_top, mw, mid_y - pad_y))
            q3 = main_block.crop((0, mid_y + pad_y, mid_x - pad_x, mh))
            q4 = main_block.crop((mid_x + pad_x, mid_y + pad_y, mw, mh))
            
            base_name = image_name.replace('.jpg', '')
            q1.save(os.path.join(base_path, f"{base_name}_q1.jpg"), quality=90)
            q2.save(os.path.join(base_path, f"{base_name}_q2.jpg"), quality=90)
            q3.save(os.path.join(base_path, f"{base_name}_q3.jpg"), quality=90)
            q4.save(os.path.join(base_path, f"{base_name}_q4.jpg"), quality=90)
            print(f"Successfully smart sliced {image_name}")
            
    except Exception as e:
        print(f"Error smart slicing {image_name}: {e}")

all_jpgs = [f for f in os.listdir(base_path) if f.endswith('_n.jpg') and '_cropped' not in f and '_photo_' not in f and '_q' not in f]

for jpg in all_jpgs:
    slice_smart(jpg)
