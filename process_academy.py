import os
from PIL import Image, ImageEnhance
import glob

dest_dir = "assets"
os.makedirs(dest_dir, exist_ok=True)

# Process Bengaluru (Pick 10 files max to save time and space, let's just pick the first 10 for simplicity, or rather I will pick a diverse set)
bengaluru_files = sorted(glob.glob("legacy_assets/04_training_camps/bengaluru/*"))
# Since they are mostly WhatsApp/Facebook quality (~30-60KB), we just resize to max 800px and color grade
bengaluru_subset = bengaluru_files[0:30:3][:10] # pick 10 diverse files

def process_img(img_path, out_path, max_dim=800):
    with Image.open(img_path) as img:
        img = img.convert('RGB')
        
        if img.width > max_dim or img.height > max_dim:
            ratio = min(max_dim/img.width, max_dim/img.height)
            img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
            
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.85)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.15)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.95)
        
        img.save(out_path, "WEBP", quality=80)

print("--- Processing Bengaluru ---")
for i, f in enumerate(bengaluru_subset):
    out_path = os.path.join(dest_dir, f"journey_academy_ben_{i+1}.webp")
    process_img(f, out_path)
    print(f"Saved {out_path}")

print("\n--- Processing Inauguration ---")
inaug_files = sorted(glob.glob("legacy_assets/05_academy/inauguration/*"))
for i, f in enumerate(inaug_files):
    out_path = os.path.join(dest_dir, f"journey_academy_inaug_{i+1}.webp")
    process_img(f, out_path, max_dim=600) # low res compact strip
    print(f"Saved {out_path}")

print("\n--- Processing Kana Gallery ---")
kana_files = sorted(glob.glob("legacy_assets/05_academy/kana_gallery/*"))
for i, f in enumerate(kana_files):
    with Image.open(f) as img:
        res = f"{img.width}x{img.height}"
        print(f"Kana file: {os.path.basename(f)} | Resolution: {res}")
        
    out_path = os.path.join(dest_dir, f"journey_academy_kana_{i+1}.webp")
    process_img(f, out_path, max_dim=1600) # Keep them larger if they are high res
    print(f"Saved {out_path}")

