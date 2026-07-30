import os
from PIL import Image, ImageEnhance
import numpy as np

# The 3 specific images provided by the user
images = [
    '/home/raghavan/Pictures/Screenshots/Screenshot from 2026-07-30 19-48-42.png',
    '/home/raghavan/Pictures/Screenshots/Screenshot from 2026-07-30 19-48-55.png',
    '/home/raghavan/Pictures/Screenshots/Screenshot from 2026-07-30 19-49-04.png'
]

out_dir = 'assets'

for i, img_path in enumerate(images):
    print(f"Processing {img_path}...")
    if not os.path.exists(img_path):
        print(f"File not found: {img_path}")
        continue
        
    img = Image.open(img_path).convert("RGBA")
    
    # Color grading
    # Enhance Contrast (+12%)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.12)
    
    # Enhance Saturation (-8%)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.92)
    
    # Cinematic grade
    data = np.array(img).astype(np.float32)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    lum = 0.299*r + 0.587*g + 0.114*b
    lum_mask = lum / 255.0
    
    # Cool shadows / warm highlights
    b_new = b + 15.0 * (1.0 - lum_mask)
    r_new = r + 20.0 * lum_mask
    g_new = g + 10.0 * lum_mask
    
    data[:,:,0] = np.clip(r_new, 0, 255)
    data[:,:,1] = np.clip(g_new, 0, 255)
    data[:,:,2] = np.clip(b_new, 0, 255)
    data[:,:,3] = a
    
    graded_img = Image.fromarray(data.astype(np.uint8), "RGBA")
    
    # Resize slightly if too large (e.g. max width 1200)
    max_w = 1200
    if graded_img.width > max_w:
        h = int((max_w / graded_img.width) * graded_img.height)
        graded_img = graded_img.resize((max_w, h), Image.Resampling.LANCZOS)
        
    out_path = os.path.join(out_dir, f'detroit_award_{i+1}.webp')
    graded_img.save(out_path, format="WEBP", quality=88)
    print(f"Saved {out_path}")

print("Done processing images.")
