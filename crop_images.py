import os
from PIL import Image

def crop_center(image_path, output_path, crop_margins):
    """
    crop_margins is a tuple: (left, top, right, bottom) as percentages of the image dimensions.
    """
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

images_to_crop = [
    '486466926_1193879656080876_2767098548785792068_n.jpg',
    '485005693_1188406983294810_676741634435601911_n.jpg',
    '486540137_1194648809337294_8428044945485451315_n.jpg',
    '487230012_1197042165764625_5235377330861897247_n.jpg'
]

# We will crop 15% from the top (usually title), 15% from bottom (usually footer/logo), and 5% from sides.
margins = (0.05, 0.18, 0.05, 0.18)

for img_name in images_to_crop:
    input_path = os.path.join(base_path, img_name)
    output_path = os.path.join(base_path, img_name.replace('.jpg', '_cropped.jpg'))
    if os.path.exists(input_path):
        crop_center(input_path, output_path, margins)
    else:
        print(f"File not found: {input_path}")
