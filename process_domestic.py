import os
from PIL import Image, ImageEnhance
import glob

dest_dir = "assets"
os.makedirs(dest_dir, exist_ok=True)

# Define the folders and how many to sample from each
folders = {
    "legacy_assets/01_franchise_leagues/tnpl": ("tnpl", 3),
    "legacy_assets/01_franchise_leagues/celebrity_cricket_league": ("ccl", 3),
    "legacy_assets/02_tournaments/sanmar_inter_college_tournament": ("sanmar", 2),
    "legacy_assets/02_tournaments/nadigar_sangam_2016": ("nadigar", 3),
    "legacy_assets/02_tournaments/womens_day_cricket_tournament_2015_16": ("womens", 2),
    "legacy_assets/02_tournaments/all_india_advocates_tournament": ("advocates", 2),
    "legacy_assets/02_tournaments/booksellers_league_team": ("booksellers", 3)
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
for folder_path, (prefix, num_samples) in folders.items():
    files = sorted(glob.glob(os.path.join(folder_path, "*")))
    # Pick distributed samples to avoid near-duplicates if they were burst shots
    if len(files) > 0:
        step = max(1, len(files) // num_samples)
        subset = files[0::step][:num_samples]
        for i, f in enumerate(subset):
            out_path = os.path.join(dest_dir, f"journey_domestic_{prefix}_{i+1}.webp")
            try:
                process_img(f, out_path)
                print(f"Saved {out_path}")
                total += 1
            except Exception as e:
                print(f"Error processing {f}: {e}")

print(f"Total images processed: {total}")
