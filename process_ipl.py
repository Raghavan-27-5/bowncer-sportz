import os
from PIL import Image, ImageEnhance
import glob

# Source and Dest
src_dir = "legacy_assets/01_franchise_leagues/ipl"
dest_dir = "assets"
os.makedirs(dest_dir, exist_ok=True)

# Files to skip (low quality)
skip_files = [
    "509224583_3541963922604661_1301448131993646011_n.jpg.jpeg",
    "IMG-20151125-WA0022.png",
    "IMG-20151125-WA0026.png",
    "502465067_3508626532605067_8291096073896224818_n.jpg.jpeg",
    "FB_IMG_1446012565633.png"
]

all_files = sorted(glob.glob(os.path.join(src_dir, "*")))
count = 1

def process_image(img_path, out_path):
    with Image.open(img_path) as img:
        img = img.convert('RGB')
        
        # Resize if too large
        max_dim = 1600
        if img.width > max_dim or img.height > max_dim:
            ratio = min(max_dim/img.width, max_dim/img.height)
            img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
            
        # Color grade: slightly lower saturation, slightly higher contrast (cinematic dark sports editorial)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.85) # desaturate slightly
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.15) # boost contrast
        
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.95) # slightly darken
        
        # Save as webp
        img.save(out_path, "WEBP", quality=80)
        print(f"Saved {out_path} ({os.path.getsize(out_path)//1024} KB)")

for f in all_files:
    basename = os.path.basename(f)
    if basename in skip_files:
        print(f"Skipping {basename} (low quality)")
        continue
        
    out_name = f"journey_ipl_{count}.webp"
    out_path = os.path.join(dest_dir, out_name)
    process_image(f, out_path)
    count += 1
