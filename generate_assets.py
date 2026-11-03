# -*- coding: utf-8 -*-
"""
生成 Web 学徒手册的身份标识图片：
  - apple-touch-icon.png  180×180
  - favicon-32.png        32×32
  - og-image.jpg          1200×630（目标 <100KB）
设计语言与网站一致：teal #0d9488 / orange #f97316 / dark #0f172a
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

FONT_MONO = "C:/Windows/Fonts/consolab.ttf"   # Consolas Bold
FONT_CN = "C:/Windows/Fonts/msyhbd.ttc"       # 微软雅黑 Bold
FONT_CN_REG = "C:/Windows/Fonts/msyh.ttc"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(4))


def diagonal_gradient(size, c1, c2):
    """对角渐变背景"""
    w, h = size
    img = Image.new("RGBA", size)
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w + y / h) / 2
            px[x, y] = lerp(c1, c2, t)
    return img


def radial_glow(size, center, radius, color, alpha_peak=120):
    """在透明层上画一个径向光晕"""
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
# 1. 主图标：先在 512×512 设计，再缩小导出
# =========================================================
master = diagonal_gradient((512, 512), TEAL, TEAL_DARK)
# 右下角橙色光晕
glow = radial_glow((512, 512), (470, 470), 320, ORANGE, alpha_peak=150)
master = Image.alpha_composite(master, glow)

d = ImageDraw.Draw(master)
sym_font = ImageFont.truetype(FONT_MONO, 250)
text_center(d, (256, 250), "</>", sym_font, WHITE)
# 下方一个小橙点
d.ellipse((238, 400, 274, 436), fill=ORANGE)

# 导出 180 与 32（均为方形，无圆角）
icon180 = master.resize((180, 180), Image.LANCZOS)
icon180.save(os.path.join(IMG, "apple-touch-icon.png"), optimize=True)

icon32 = master.resize((32, 32), Image.LANCZOS)
icon32.save(os.path.join(IMG, "favicon-32.png"), optimize=True)

# =========================================================
# 2. Open Graph 封面图 1200×630
# =========================================================
W, H = 1200, 630
og = Image.new("RGBA", (W, H), DARK)
# 背景两个光晕
og = Image.alpha_composite(og, radial_glow((W, H), (1050, 60), 480, TEAL, alpha_peak=130))
og = Image.alpha_composite(og, radial_glow((W, H), (80, 620), 420, ORANGE, alpha_peak=95))

d = ImageDraw.Draw(og)

# 右侧大符号装饰（半透明，避开标题区）
big_sym = ImageFont.truetype(FONT_MONO, 250)
sym_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sym_layer)
sd.text((868, 300), "</>", font=big_sym, fill=(255, 255, 255, 34))
og = Image.alpha_composite(og, sym_layer)
d = ImageDraw.Draw(og)

# 顶部小标签
tag_font = ImageFont.truetype(FONT_MONO, 26)
d.rounded_rectangle((90, 96, 330, 146), radius=25, fill=(255, 255, 255, 26),
                    outline=(255, 255, 255, 60), width=2)
d.text((118, 104), "WEBTECH NOTES", font=tag_font, fill=LIGHT)

# 主标题（中文，大）
title_font = ImageFont.truetype(FONT_CN, 118)
d.text((88, 200), "Web 学徒手册", font=title_font, fill=WHITE)

# 橙色分隔线
d.rounded_rectangle((92, 372, 300, 384), radius=6, fill=ORANGE)

# 副标题
sub_font = ImageFont.truetype(FONT_CN_REG, 42)
d.text((90, 410), "从零开始的 HTML · CSS · JavaScript", font=sub_font, fill=(203, 213, 225, 255))
d.text((90, 470), "学习成果展示，全部手写并托管在 GitHub", font=sub_font, fill=(148, 163, 184, 255))

# 底部网址
url_font = ImageFont.truetype(FONT_MONO, 28)
d.text((90, 556), "webtech-notes", font=url_font, fill=(94, 234, 212, 255))

og_rgb = og.convert("RGB")
og_path = os.path.join(IMG, "og-image.jpg")
# 控制在 100KB 以内：逐步降低质量
quality = 90
og_rgb.save(og_path, "JPEG", quality=quality, optimize=True)
while os.path.getsize(og_path) > 98 * 1024 and quality > 40:
    quality -= 5
    og_rgb.save(og_path, "JPEG", quality=quality, optimize=True)

# =========================================================
# 输出结果
# =========================================================
for name in ["apple-touch-icon.png", "favicon-32.png", "og-image.jpg"]:
    p = os.path.join(IMG, name)
    im = Image.open(p)
    print(f"{name:22s} {im.size[0]}x{im.size[1]:4d}  {os.path.getsize(p)/1024:.1f} KB")
