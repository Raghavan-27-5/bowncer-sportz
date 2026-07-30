import os
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

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
    
    # Crop slightly if there are weird borders from screenshots (optional, we'll skip unless necessary)
    
    # 1. Sharpening to make low-quality screenshots look crisper
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    # 2. Color grading
    # Enhance Contrast (+20% for a starker editorial look)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.20)
    
    # Enhance Color (+10% to restore lost vibrance, although we'll grayscale them in CSS, 
    # when hovered they will pop beautifully)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.10)
    
    # Resize to a clean 2x resolution for web (retina)
    max_w = 1600
    if img.width > max_w:
        h = int((max_w / img.width) * img.height)
        img = img.resize((max_w, h), Image.Resampling.LANCZOS)
        
    out_path = os.path.join(out_dir, f'detroit_award_v2_{i+1}.webp')
    img.save(out_path, format="WEBP", quality=90) # high quality
    print(f"Saved {out_path}")

print("Done processing images.")
