import os
from PIL import Image, ImageEnhance, ImageOps

# High resolution images provided by the user
images = [
    '/home/raghavan/Downloads/ChatGPT Image Jul 30, 2026, 08_27_17 PM.png',
    '/home/raghavan/Downloads/ChatGPT Image Jul 30, 2026, 08_28_59 PM.png',
    '/home/raghavan/Downloads/ChatGPT Image Jul 30, 2026, 08_30_24 PM.png'
]

out_dir = 'assets'

for i, img_path in enumerate(images):
    print(f"Processing {img_path}...")
    if not os.path.exists(img_path):
        print(f"File not found: {img_path}")
        continue
        
    # Open and convert to RGB (since WebP handles transparency but we are doing color math)
    img = Image.open(img_path).convert("RGBA")
    
    # Mild Color grading for cinematic look
    # Enhance Contrast (+12%)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.12)
    
    # Enhance Saturation (-8%)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.92)
    
    # Instead of numpy, let's use a subtle colorize overlay to warm the highlights
    # and cool the shadows. 
    # Create a warm and cool map
    gray = img.convert("L")
    colored = ImageOps.colorize(gray, black="#000e1f", white="#fff0e0") # Cool shadows, warm highlights
    
    # Blend the original with the colorized version
    img = Image.blend(img.convert("RGB"), colored, alpha=0.15)
    
    # Resize slightly if too large (max width 1600 for crisp webp)
    max_w = 1600
    if img.width > max_w:
        h = int((max_w / img.width) * img.height)
        img = img.resize((max_w, h), Image.Resampling.LANCZOS)
        
    out_path = os.path.join(out_dir, f'detroit_award_v3_{i+1}.webp')
    img.save(out_path, format="WEBP", quality=88)
    print(f"Saved {out_path}")

print("Done processing high-res images.")
