import os
from PIL import Image

def crop_center(image_path, output_path, crop_margins):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            left = width * crop_margins[0]
            top = height * crop_margins[1]
            right = width * (1 - crop_margins[2])
            bottom = height * (1 - crop_margins[3])
            
            cropped_img = img.crop((left, top, right, bottom))
            cropped_img.save(output_path, quality=90)
            print(f"Successfully cropped {os.path.basename(image_path)}")
    except Exception as e:
        print(f"Error cropping {image_path}: {e}")

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website\_assets\projects"

# Get all original jpgs
all_jpgs = [f for f in os.listdir(base_path) if f.endswith('.jpg') and not f.endswith('_cropped.jpg')]

margins = (0.05, 0.18, 0.05, 0.18)

for img_name in all_jpgs:
    input_path = os.path.join(base_path, img_name)
    output_path = os.path.join(base_path, img_name.replace('.jpg', '_cropped.jpg'))
    if not os.path.exists(output_path):
        crop_center(input_path, output_path, margins)
