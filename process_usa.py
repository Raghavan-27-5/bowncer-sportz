import os
from PIL import Image, ImageEnhance
import glob

dest_dir = "assets"
os.makedirs(dest_dir, exist_ok=True)

# Define folders and max samples
folders = {
    "boston": 3,
    "california": 7,
    "charlotte": 8,
    "detroit": 4,
    "greensboro": 7,
    "north_carolina": 7
}

def process_img(img_path, out_path, max_dim=1200):
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

total = 0
for city, num_samples in folders.items():
    folder_path = os.path.join("legacy_assets/03_usa_tours", city)
    files = sorted(glob.glob(os.path.join(folder_path, "*")))
    if len(files) > 0:
        step = max(1, len(files) // num_samples)
        subset = files[0::step][:num_samples]
        for i, f in enumerate(subset):
            out_path = os.path.join(dest_dir, f"journey_usa_{city}_{i+1}.webp")
            try:
                process_img(f, out_path)
                print(f"Saved {out_path}")
                total += 1
            except Exception as e:
                print(f"Error processing {f}: {e}")

print(f"Total images processed: {total}")
