import os
import numpy as np
from PIL import Image

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website\_assets\projects"

def get_bg_color(img):
    # Sample 4 corners
    w, h = img.size
    corners = [
        img.getpixel((5, 5)),
        img.getpixel((w - 5, 5)),
        img.getpixel((5, h - 5)),
        img.getpixel((w - 5, h - 5))
    ]
    # Return the most common color (using average or median)
    return np.mean(corners, axis=0)

def is_bg(pixel, bg_color, threshold=30):
    # Check if pixel is close to bg_color
    return np.linalg.norm(np.array(pixel[:3]) - bg_color[:3]) < threshold

def slice_perfect(image_name):
    img_path = os.path.join(base_path, image_name)
    if not os.path.exists(img_path):
        return
        
    try:
        with Image.open(img_path) as img:
            img_rgb = img.convert('RGB')
            w, h = img_rgb.size
            bg_color = get_bg_color(img_rgb)
            
            # Convert image to binary mask: 1 for background, 0 for photos
            mask = np.zeros((h, w), dtype=int)
            for y in range(h):
                for x in range(w):
                    if is_bg(img_rgb.getpixel((x, y)), bg_color):
                        mask[y, x] = 1
            
            # Projection profiles
            col_bg_ratio = np.mean(mask, axis=0) # percentage of background per column
            row_bg_ratio = np.mean(mask, axis=1) # percentage of background per row
            
            # Find photo boundaries
            # Photos start where background ratio drops below 0.95
            photo_cols = np.where(col_bg_ratio < 0.95)[0]
            photo_rows = np.where(row_bg_ratio < 0.95)[0]
            
            if len(photo_cols) == 0 or len(photo_rows) == 0:
                print(f"Could not detect boundaries for {image_name}")
                return
                
            left = photo_cols[0]
            right = photo_cols[-1]
            top = photo_rows[0]
            bottom = photo_rows[-1]
            
            # We add a small safety padding (5px) inside the outer bounds
            left = min(left + 5, w)
            right = max(right - 5, 0)
            top = min(top + 5, h)
            bottom = max(bottom - 5, 0)
            
            # Find vertical gap in the middle region (between 35% and 65% of width)
            mid_w_start = int(left + (right - left) * 0.35)
            mid_w_end = int(left + (right - left) * 0.65)
            # The gap is where the background ratio peaks in the center
            vertical_gap_x = mid_w_start + np.argmax(col_bg_ratio[mid_w_start:mid_w_end])
            
            # Find horizontal gap in the middle region (between 35% and 65% of height)
            mid_h_start = int(top + (bottom - top) * 0.35)
            mid_h_end = int(top + (bottom - top) * 0.65)
            horizontal_gap_y = mid_h_start + np.argmax(row_bg_ratio[mid_h_start:mid_h_end])
            
            # Define padding to shave off borders/background lines in the middle gaps
            pad_x = 8
            pad_y = 8
            
            # Extract the 4 quadrants
            # We shave 10px off the outer edges as well to ensure clean cuts
            q1 = img.crop((left + 5, top + 5, vertical_gap_x - pad_x, horizontal_gap_y - pad_y))
            q2 = img.crop((vertical_gap_x + pad_x, top + 5, right - 5, horizontal_gap_y - pad_y))
            q3 = img.crop((left + 5, horizontal_gap_y + pad_y, vertical_gap_x - pad_x, bottom - 5))
            q4 = img.crop((vertical_gap_x + pad_x, horizontal_gap_y + pad_y, right - 5, bottom - 5))
            
            # Save quadrants
            base_name = image_name.replace('.jpg', '')
            q1.save(os.path.join(base_path, f"{base_name}_q1.jpg"), quality=90)
            q2.save(os.path.join(base_path, f"{base_name}_q2.jpg"), quality=90)
            q3.save(os.path.join(base_path, f"{base_name}_q3.jpg"), quality=90)
            q4.save(os.path.join(base_path, f"{base_name}_q4.jpg"), quality=90)
            
            print(f"Successfully sliced {image_name} perfectly into 4 clean photos.")
            
    except Exception as e:
        print(f"Error slicing {image_name}: {e}")

all_jpgs = [f for f in os.listdir(base_path) if f.endswith('_n.jpg') and '_cropped' not in f and '_photo_' not in f and '_q' not in f]

for jpg in all_jpgs:
    slice_perfect(jpg)
