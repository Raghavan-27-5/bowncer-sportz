import os
from rembg import remove
from PIL import Image, ImageEnhance
import numpy as np

input_path = 'assets/thiyagarajan_rcb.webp'

# 1. Remove background
print("Removing background...")
with open(input_path, 'rb') as i:
    input_img = i.read()
    output_img_bytes = remove(input_img)

# Convert to PIL Image
import io
img = Image.open(io.BytesIO(output_img_bytes)).convert("RGBA")

# 2. Color grading
print("Color grading...")
# Enhance Contrast (+12%)
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.12)

# Enhance Saturation (-8%)
enhancer = ImageEnhance.Color(img)
img = enhancer.enhance(0.92)

# Cool shadows / Warm highlights
# We will convert the image to numpy array to do a simple color curve
data = np.array(img).astype(np.float32)

# Split channels (R, G, B, A)
r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

# Calculate luminance (roughly) to distinguish shadows vs highlights
lum = 0.299*r + 0.587*g + 0.114*b
lum_mask = lum / 255.0

# Shadows (low luminance) get more Blue, less Red
# Highlights (high luminance) get more Red, less Blue
# Cool shadows: increase blue by up to 15 in darkest areas
# Warm highlights: increase red by up to 20 in brightest areas, increase green by 10

# B = B + 15 * (1 - lum_mask)
b_new = b + 15.0 * (1.0 - lum_mask)
# R = R + 20 * lum_mask
r_new = r + 20.0 * lum_mask
# G = G + 10 * lum_mask
g_new = g + 10.0 * lum_mask

# Recombine and clip
data[:,:,0] = np.clip(r_new, 0, 255)
data[:,:,1] = np.clip(g_new, 0, 255)
data[:,:,2] = np.clip(b_new, 0, 255)
data[:,:,3] = a # Alpha untouched

graded_img = Image.fromarray(data.astype(np.uint8), "RGBA")

# 3. Export at 3 breakpoints (480, 960, 1920)
print("Exporting breakpoints...")
widths = [480, 960, 1920]

original_w, original_h = graded_img.size

for w in widths:
    if w > original_w:
        w_to_use = original_w
    else:
        w_to_use = w
        
    h_to_use = int((w_to_use / original_w) * original_h)
    
    resized = graded_img.resize((w_to_use, h_to_use), Image.Resampling.LANCZOS)
    # Convert RGBA to RGB with void background (since it's meant for a dark sports editorial)
    # Wait, if we removed the background, we should probably keep it transparent so the website background shows through!
    # But WebP supports transparency. So just save as RGBA WebP.
    
    out_path = f'assets/thiyagarajan_rcb_{w_to_use}w.webp'
    resized.save(out_path, format="WEBP", quality=85)
    print(f"Saved {out_path}")

print("Done processing image.")
