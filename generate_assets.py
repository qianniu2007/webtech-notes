# -*- coding: utf-8 -*-
"""
Generate the identity images for WebTech Notes:
  - apple-touch-icon.png  180x180
  - favicon-32.png        32x32
  - og-image.jpg          1200x630 (target < 100KB)
Design language matches the site: teal #0d9488 / orange #f97316 / dark #0f172a
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "images")
os.makedirs(IMG, exist_ok=True)

TEAL = (13, 148, 136, 255)
TEAL_DARK = (15, 118, 110, 255)
ORANGE = (249, 115, 22, 255)
DARK = (15, 23, 42, 255)
WHITE = (255, 255, 255, 255)
LIGHT = (204, 251, 241, 255)

FONT_MONO = "C:/Windows/Fonts/consolab.ttf"      # Consolas Bold
FONT_TITLE = "C:/Windows/Fonts/arialbd.ttf"       # Arial Bold (headings)
FONT_SUB = "C:/Windows/Fonts/seguisb.ttf"        # Segoe UI Semibold (subtitles)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(4))


def diagonal_gradient(size, c1, c2):
    """Diagonal gradient background."""
    w, h = size
    img = Image.new("RGBA", size)
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w + y / h) / 2
            px[x, y] = lerp(c1, c2, t)
    return img


def radial_glow(size, center, radius, color, alpha_peak=120):
    """Draw a radial glow on a transparent layer."""
    w, h = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    px = layer.load()
    cx, cy = center
    for y in range(h):
        for x in range(w):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d < radius:
                t = 1 - d / radius
                px[x, y] = (color[0], color[1], color[2], int(alpha_peak * t))
    return layer


def text_center(draw, xy, text, font, fill):
    box = draw.textbbox((0, 0), text, font=font)
    w = box[2] - box[0]
    h = box[3] - box[1]
    draw.text((xy[0] - w / 2, xy[1] - h / 2 - box[1]), text, font=font, fill=fill)


# =========================================================
# 1. Master icon: designed at 512x512, then scaled down
# =========================================================
master = diagonal_gradient((512, 512), TEAL, TEAL_DARK)
# Orange glow in the lower-right corner
glow = radial_glow((512, 512), (470, 470), 320, ORANGE, alpha_peak=150)
master = Image.alpha_composite(master, glow)

d = ImageDraw.Draw(master)
sym_font = ImageFont.truetype(FONT_MONO, 250)
text_center(d, (256, 250), "</>", sym_font, WHITE)
# Small orange dot below
d.ellipse((238, 400, 274, 436), fill=ORANGE)

# Export 180 and 32 (square, no rounded corners)
icon180 = master.resize((180, 180), Image.LANCZOS)
icon180.save(os.path.join(IMG, "apple-touch-icon.png"), optimize=True)

icon32 = master.resize((32, 32), Image.LANCZOS)
icon32.save(os.path.join(IMG, "favicon-32.png"), optimize=True)

# =========================================================
# 2. Open Graph cover image 1200x630
# =========================================================
W, H = 1200, 630
og = Image.new("RGBA", (W, H), DARK)
# Two background glows
og = Image.alpha_composite(og, radial_glow((W, H), (1050, 60), 480, TEAL, alpha_peak=130))
og = Image.alpha_composite(og, radial_glow((W, H), (80, 620), 420, ORANGE, alpha_peak=95))

d = ImageDraw.Draw(og)

# Large symbol decoration on the right (semi-transparent, away from the title)
big_sym = ImageFont.truetype(FONT_MONO, 250)
sym_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sym_layer)
sd.text((868, 300), "</>", font=big_sym, fill=(255, 255, 255, 34))
og = Image.alpha_composite(og, sym_layer)
d = ImageDraw.Draw(og)

# Top pill label
tag_font = ImageFont.truetype(FONT_MONO, 26)
d.rounded_rectangle((90, 96, 330, 146), radius=25, fill=(255, 255, 255, 26),
                    outline=(255, 255, 255, 60), width=2)
d.text((118, 104), "WEBTECH NOTES", font=tag_font, fill=LIGHT)

# Main title (English, large)
title_font = ImageFont.truetype(FONT_TITLE, 128)
d.text((88, 200), "WebTech Notes", font=title_font, fill=WHITE)

# Orange divider
d.rounded_rectangle((92, 372, 300, 384), radius=6, fill=ORANGE)

# Subtitles
sub_font = ImageFont.truetype(FONT_SUB, 42)
d.text((90, 410), "A from-scratch HTML · CSS · JavaScript journal", font=sub_font, fill=(203, 213, 225, 255))
d.text((90, 470), "All hand-written and hosted on GitHub", font=sub_font, fill=(148, 163, 184, 255))

# Bottom URL
url_font = ImageFont.truetype(FONT_MONO, 28)
d.text((90, 556), "webtech-notes", font=url_font, fill=(94, 234, 212, 255))

og_rgb = og.convert("RGB")
og_path = os.path.join(IMG, "og-image.jpg")
# Keep under 100KB: lower the quality step by step
quality = 90
og_rgb.save(og_path, "JPEG", quality=quality, optimize=True)
while os.path.getsize(og_path) > 98 * 1024 and quality > 40:
    quality -= 5
    og_rgb.save(og_path, "JPEG", quality=quality, optimize=True)

# =========================================================
# Output summary
# =========================================================
for name in ["apple-touch-icon.png", "favicon-32.png", "og-image.jpg"]:
    p = os.path.join(IMG, name)
    im = Image.open(p)
    print(f"{name:22s} {im.size[0]}x{im.size[1]:4d}  {os.path.getsize(p)/1024:.1f} KB")
