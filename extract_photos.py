import cv2
import numpy as np
import os

base_path = r"c:\Users\bddgt\.gemini\antigravity\scratch\sunnyward-website\_assets\projects"

def extract_photos(image_name):
    img_path = os.path.join(base_path, image_name)
    if not os.path.exists(img_path):
        return []

    # Read image
    img = cv2.imread(img_path)
    if img is None:
        return []
        
    h, w = img.shape[:2]
    
    # Assuming the corners are the background color (e.g. pink, yellow, etc.)
    # We take the top-left corner color (at x=5, y=5 to avoid edge artifacts)
    bg_color = img[5, 5]
    
    # Create a mask of the background color
    # Allow some tolerance for JPEG artifacts
    lower = np.clip(bg_color - 15, 0, 255)
    upper = np.clip(bg_color + 15, 0, 255)
    
    mask = cv2.inRange(img, lower, upper)
    
    # Invert mask so photos are white
    mask_inv = cv2.bitwise_not(mask)
    
    # Apply some morphological operations to close small gaps and remove text
    kernel = np.ones((5,5), np.uint8)
    mask_inv = cv2.erode(mask_inv, kernel, iterations=1)
    mask_inv = cv2.dilate(mask_inv, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(mask_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by area to find the 4 largest ones (which should be the photos)
    # The photos are large, text and logos are small
    photo_rects = []
    for cnt in contours:
        x, y, w_box, h_box = cv2.boundingRect(cnt)
        area = w_box * h_box
        # A photo should be at least 5% of the total image area
        if area > (w * h * 0.05):
            photo_rects.append((x, y, w_box, h_box))
            
    # Sort the rects from top-left to bottom-right
    # Sort by Y first, then X
    # Actually, a simple sort by Y usually groups top row and bottom row.
    photo_rects.sort(key=lambda r: (r[1]//100, r[0]))
    
    extracted_paths = []
    # Crop and save
    base_name = image_name.replace('.jpg', '')
    
    # Ensure we only process if we found some photos (ideally 4, but maybe 2 or 3)
    for idx, (x, y, w_box, h_box) in enumerate(photo_rects[:4]):
        # Crop the photo
        # Add a tiny 2px crop inwards to remove any remaining background border
        cropped = img[y+2:y+h_box-2, x+2:x+w_box-2]
        out_name = f"{base_name}_photo_{idx+1}.jpg"
        out_path = os.path.join(base_path, out_name)
        cv2.imwrite(out_path, cropped)
        extracted_paths.append(out_name)
        print(f"Extracted {out_name}")
        
    return extracted_paths

# Process all original jpgs
all_jpgs = [f for f in os.listdir(base_path) if f.endswith('_n.jpg') and '_cropped' not in f and '_photo_' not in f]

results = {}
for jpg in all_jpgs:
    print(f"Processing {jpg}...")
    photos = extract_photos(jpg)
    results[jpg] = photos

print("Extraction complete.")
