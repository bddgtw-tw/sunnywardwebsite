import os
from PIL import Image

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website\_assets\projects"

def slice_into_quadrants(image_name):
    img_path = os.path.join(base_path, image_name)
    if not os.path.exists(img_path):
        return
        
    try:
        with Image.open(img_path) as img:
            width, height = img.size
            
            # Define the central area where the photos usually are.
            # Typically top 18% is title, bottom 15% is footer
            top = height * 0.18
            bottom = height * 0.85
            left = width * 0.05
            right = width * 0.95
            
            # Crop the center block
            center_block = img.crop((left, top, right, bottom))
            cw, ch = center_block.size
            
            # Now split into 4 quadrants (2x2 grid)
            # Add a small padding to remove grid lines (e.g. 2%)
            pad_x = cw * 0.02
            pad_y = ch * 0.02
            
            mid_x = cw / 2
            mid_y = ch / 2
            
            q1 = center_block.crop((0, 0, mid_x - pad_x, mid_y - pad_y))
            q2 = center_block.crop((mid_x + pad_x, 0, cw, mid_y - pad_y))
            q3 = center_block.crop((0, mid_y + pad_y, mid_x - pad_x, ch))
            q4 = center_block.crop((mid_x + pad_x, mid_y + pad_y, cw, ch))
            
            base_name = image_name.replace('.jpg', '')
            q1.save(os.path.join(base_path, f"{base_name}_q1.jpg"), quality=90)
            q2.save(os.path.join(base_path, f"{base_name}_q2.jpg"), quality=90)
            q3.save(os.path.join(base_path, f"{base_name}_q3.jpg"), quality=90)
            q4.save(os.path.join(base_path, f"{base_name}_q4.jpg"), quality=90)
            print(f"Successfully sliced {image_name} into 4 photos.")
            
    except Exception as e:
        print(f"Error slicing {image_name}: {e}")

all_jpgs = [f for f in os.listdir(base_path) if f.endswith('_n.jpg') and '_cropped' not in f and '_photo_' not in f and '_q' not in f]

for jpg in all_jpgs:
    slice_into_quadrants(jpg)
