#!/usr/bin/env python3
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ASSETS_DIR = "/home/raghavan/projects/bowncer_sportz/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# Color Palette (Strictly matching DESIGN-SYSTEM.md)
VOID = (7, 8, 10)       # #07080a
VOID2 = (13, 15, 18)    # #0d0f12
EMBER = (226, 56, 10)   # #e2380a
EMBER_GLOW = (255, 86, 34) # #ff5622
GOLD = (201, 161, 90)   # #c9a15a
INK = (244, 241, 234)   # #f4f1ea
INK_DIM = (184, 178, 164) # #b8b2a4
LINE = (244, 241, 234, 35)

def create_gradient_background(width, height, color1, color2):
    base = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(base)
    for y in range(height):
        r = int(color1[0] + (color2[0] - color1[0]) * (y / height))
        g = int(color1[1] + (color2[1] - color1[1]) * (y / height))
        b = int(color1[2] + (color2[2] - color1[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return base

def add_radial_glow(img, center_x, center_y, radius, color, alpha=0.3):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for r in range(radius, 0, -2):
        ratio = r / radius
        current_alpha = int((1.0 - ratio) * 255 * alpha)
        fill_color = (color[0], color[1], color[2], current_alpha)
        draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=fill_color)
    
    img_rgba = img.convert("RGBA")
    result = Image.alpha_composite(img_rgba, overlay)
    return result.convert("RGB")

def add_net_grid(draw, width, height, step=40):
    grid_color = (244, 241, 234, 15)
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

def draw_cricket_ball_graphic(draw, cx, cy, r):
    # Base ball outline/fill in Ember
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(180, 40, 10), outline=EMBER_GLOW, width=3)
    # Seam line
    seam_pts = []
    for angle in range(-90, 91, 5):
        rad = math.radians(angle)
        x = cx + int(r * 0.7 * math.sin(rad))
        y = cy + int(r * math.cos(rad))
        seam_pts.append((x, y))
    if len(seam_pts) > 1:
        draw.line(seam_pts, fill=INK, width=2)
        # Stitch dots
        for x, y in seam_pts[::3]:
            draw.line([(x-2, y-2), (x+2, y+2)], fill=GOLD, width=1)

def generate_featured_thumb():
    w, h = 1280, 720
    img = create_gradient_background(w, h, VOID, VOID2)
    img = add_radial_glow(img, int(w * 0.3), int(h * 0.4), 400, EMBER, alpha=0.35)
    img = add_radial_glow(img, int(w * 0.8), int(h * 0.7), 350, GOLD, alpha=0.25)
    
    img_rgba = img.convert("RGBA")
    draw = ImageDraw.Draw(img_rgba)
    add_net_grid(draw, w, h, step=50)
    
    # Pitch line / seam arc graphics
    draw.line([(0, int(h*0.85)), (w, int(h*0.85))], fill=GOLD, width=3)
    draw.line([(int(w*0.2), 0), (int(w*0.8), h)], fill=(226, 56, 10, 40), width=4)
    
    # Large Cricket Ball Graphic
    draw_cricket_ball_graphic(draw, int(w * 0.75), int(h * 0.4), 110)
    
    # Stumps silhouette
    stump_x = int(w * 0.22)
    stump_y = int(h * 0.45)
    for offset in [-24, 0, 24]:
        draw.rectangle([stump_x + offset - 4, stump_y - 80, stump_x + offset + 4, stump_y + 80], fill=GOLD)
    # Bails
    draw.rectangle([stump_x - 30, stump_y - 86, stump_x + 30, stump_y - 80], fill=INK)
    
    # Overlay gradient for text readability
    rect_overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d_rect = ImageDraw.Draw(rect_overlay)
    d_rect.rectangle([0, 0, w, h], fill=(7, 8, 10, 110))
    d_rect.rectangle([0, int(h*0.5), w, h], fill=(7, 8, 10, 160))
    img_rgba = Image.alpha_composite(img_rgba, rect_overlay)
    
    draw = ImageDraw.Draw(img_rgba)
    
    # Watermark Brand Pill
    draw.rectangle([50, 45, 300, 85], fill=(13, 15, 18, 220), outline=EMBER, width=2)
    draw.text((65, 55), "BOWNCER SPORTZ", fill=INK, font=ImageFont.load_default())
    
    # Featured Tag
    draw.rectangle([50, 110, 290, 145], fill=GOLD)
    draw.text((62, 120), "FEATURED SHOWCASE", fill=VOID, font=ImageFont.load_default())
    
    # Headline / Title Text
    draw.text((50, int(h*0.62)), "PRO BATTING MECHANICS & FAST BOWLING ANALYSIS", fill=INK, font=ImageFont.load_default())
    draw.text((50, int(h*0.68)), "High-speed camera breakdowns of stance, trigger movement & release", fill=INK_DIM, font=ImageFont.load_default())
    draw.text((50, int(h*0.73)), "Coached by S. Thiyagarajan (Ex-IPL RCB, ICC/BCCI Level 1)", fill=GOLD, font=ImageFont.load_default())
    
    # Duration Badge
    draw.rectangle([w - 140, h - 70, w - 40, h - 35], fill=(7, 8, 10, 230), outline=GOLD, width=1)
    draw.text((w - 120, h - 58), "03:45 HD", fill=INK, font=ImageFont.load_default())
    
    # Play Icon Circle overlay
    play_cx, play_cy = int(w * 0.5), int(h * 0.42)
    draw.ellipse([play_cx - 50, play_cy - 50, play_cx + 50, play_cy + 50], fill=EMBER, outline=EMBER_GLOW, width=3)
    draw.polygon([(play_cx - 15, play_cy - 25), (play_cx + 25, play_cy), (play_cx - 15, play_cy + 25)], fill=INK)
    
    output_path = os.path.join(ASSETS_DIR, "showcase_thumb_featured.webp")
    img_rgba.convert("RGB").save(output_path, "WEBP", quality=90)
    print(f"Generated {output_path}")

def generate_secondary_thumb_2():
    w, h = 640, 360
    img = create_gradient_background(w, h, VOID, VOID2)
    img = add_radial_glow(img, int(w * 0.7), int(h * 0.5), 220, EMBER, alpha=0.3)
    img = add_radial_glow(img, int(w * 0.2), int(h * 0.3), 180, GOLD, alpha=0.2)
    
    img_rgba = img.convert("RGBA")
    draw = ImageDraw.Draw(img_rgba)
    add_net_grid(draw, w, h, step=35)
    
    # Spin curve arc graphics
    arc_pts = []
    for deg in range(0, 180, 5):
        rad = math.radians(deg)
        x = int(w * 0.15 + rad * 120)
        y = int(h * 0.7 - math.sin(rad) * 140)
        arc_pts.append((x, y))
    if len(arc_pts) > 1:
        draw.line(arc_pts, fill=EMBER_GLOW, width=3)
    
    draw_cricket_ball_graphic(draw, int(w * 0.72), int(h * 0.45), 55)
    
    # Overlay darkening
    rect_overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d_rect = ImageDraw.Draw(rect_overlay)
    d_rect.rectangle([0, int(h*0.45), w, h], fill=(7, 8, 10, 160))
    img_rgba = Image.alpha_composite(img_rgba, rect_overlay)
    
    draw = ImageDraw.Draw(img_rgba)
    
    # Badge
    draw.rectangle([24, 20, 160, 44], fill=EMBER)
    draw.text((32, 27), "DRILL SPOTLIGHT", fill=INK, font=ImageFont.load_default())
    
    # Title
    draw.text((24, int(h*0.62)), "SPIN BOWLING FLIGHT & VARIATION MASTERCLASS", fill=INK, font=ImageFont.load_default())
    draw.text((24, int(h*0.72)), "Revolutions, drift & seam control protocols", fill=INK_DIM, font=ImageFont.load_default())
    
    # Duration Badge
    draw.rectangle([w - 100, h - 45, w - 20, h - 20], fill=(7, 8, 10, 230), outline=GOLD, width=1)
    draw.text((w - 85, h - 37), "02:10", fill=INK, font=ImageFont.load_default())
    
    # Small Play Button
    play_cx, play_cy = int(w * 0.5), int(h * 0.4)
    draw.ellipse([play_cx - 30, play_cy - 30, play_cx + 30, play_cy + 30], fill=EMBER)
    draw.polygon([(play_cx - 9, play_cy - 14), (play_cx + 14, play_cy), (play_cx - 9, play_cy + 14)], fill=INK)
    
    output_path = os.path.join(ASSETS_DIR, "showcase_thumb_2.webp")
    img_rgba.convert("RGB").save(output_path, "WEBP", quality=90)
    print(f"Generated {output_path}")

def generate_secondary_thumb_3():
    w, h = 640, 360
    img = create_gradient_background(w, h, VOID, VOID2)
    img = add_radial_glow(img, int(w * 0.3), int(h * 0.6), 220, GOLD, alpha=0.3)
    img = add_radial_glow(img, int(w * 0.8), int(h * 0.3), 180, EMBER, alpha=0.25)
    
    img_rgba = img.convert("RGBA")
    draw = ImageDraw.Draw(img_rgba)
    add_net_grid(draw, w, h, step=35)
    
    # Agility cones / reflex dots
    for cx, cy in [(120, 200), (220, 160), (320, 220), (420, 170)]:
        draw.polygon([(cx, cy-25), (cx-20, cy+15), (cx+20, cy+15)], fill=EMBER)
        draw.line([(cx-25, cy+15), (cx+25, cy+15)], fill=GOLD, width=2)
    
    draw_cricket_ball_graphic(draw, int(w * 0.78), int(h * 0.4), 50)
    
    # Overlay darkening
    rect_overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d_rect = ImageDraw.Draw(rect_overlay)
    d_rect.rectangle([0, int(h*0.45), w, h], fill=(7, 8, 10, 160))
    img_rgba = Image.alpha_composite(img_rgba, rect_overlay)
    
    draw = ImageDraw.Draw(img_rgba)
    
    # Badge
    draw.rectangle([24, 20, 190, 44], fill=GOLD)
    draw.text((32, 27), "JUNIOR FOUNDATIONS", fill=VOID, font=ImageFont.load_default())
    
    # Title
    draw.text((24, int(h*0.62)), "AGILITY, CATCHING & REFLEX CONDITIONING FOR KIDS", fill=INK, font=ImageFont.load_default())
    draw.text((24, int(h*0.72)), "Building hand-eye coordination & movement fundamentals (Ages 6+)", fill=INK_DIM, font=ImageFont.load_default())
    
    # Duration Badge
    draw.rectangle([w - 100, h - 45, w - 20, h - 20], fill=(7, 8, 10, 230), outline=GOLD, width=1)
    draw.text((w - 85, h - 37), "01:50", fill=INK, font=ImageFont.load_default())
    
    # Small Play Button
    play_cx, play_cy = int(w * 0.5), int(h * 0.4)
    draw.ellipse([play_cx - 30, play_cy - 30, play_cx + 30, play_cy + 30], fill=EMBER)
    draw.polygon([(play_cx - 9, play_cy - 14), (play_cx + 14, play_cy), (play_cx - 9, play_cy + 14)], fill=INK)
    
    output_path = os.path.join(ASSETS_DIR, "showcase_thumb_3.webp")
    img_rgba.convert("RGB").save(output_path, "WEBP", quality=90)
    print(f"Generated {output_path}")

if __name__ == "__main__":
    generate_featured_thumb()
    generate_secondary_thumb_2()
    generate_secondary_thumb_3()
