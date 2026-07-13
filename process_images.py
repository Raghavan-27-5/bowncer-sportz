import os
import subprocess
from PIL import Image, ImageEnhance

REMBG_CMD = "/home/raghavan/projects/bowncer_sportz/venv/bin/rembg"

images = [
    ("/home/raghavan/Downloads/Thiyagarajan_rcb_jersey.jpeg", "assets/thiyagarajan_rcb.webp"),
    ("/home/raghavan/Downloads/arun_karthik.jpeg", "assets/arun_karthik.webp"),
    ("/home/raghavan/Downloads/shiva_vashist.jpeg", "assets/shiva_vashist.webp")
]

for src, dst in images:
    if not os.path.exists(src):
        print(f"Skipping {src}, not found.")
        continue
    
    print(f"Processing {src}...")
    temp_png = dst.replace(".webp", "_temp.png")
    
    # 1. Remove background
    try:
        subprocess.run([REMBG_CMD, "i", src, temp_png], check=True)
    except Exception as e:
        print(f"rembg failed for {src}: {e}")
        continue
        
    # 2. Color grading
    try:
        img = Image.open(temp_png)
        # Apply Brightness
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.97)
        # Apply Contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.12)
        # Apply Color (Saturation)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.92)
        
        # 3. Export as WebP
        img.save(dst, "webp", quality=88)
        os.remove(temp_png)
        print(f"Saved {dst}")
    except Exception as e:
        print(f"Grading failed for {src}: {e}")
