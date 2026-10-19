#!/usr/bin/env python3
"""
Carousel slide 01 — 1080x1350 (4:5).

Brutalist "warning poster" over a cinematic dusk photograph.
Rendered at 2x and downsampled so the type stays crisp.

All copy is fixed by the brief; nothing else is drawn.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from poster_kit import (
    ANTON, ASSETS, BLACK, CONTENT_W, CW, CH, FONTS, GREY, H, INTER, INTER_IT,
    MARGIN, OFFWHITE, OUT, RED, SS, W, add_grain, draw_tracked, font, paper_field,
    px, save, tracked_w,
)


# =========================================================
# 1. photograph -> cover crop 4:5
# =========================================================
src = Image.open(ASSETS / "photo-source.png").convert("RGB")
sw, sh = src.size
target = W / H
if sw / sh > target:
    nw = int(sh * target)
    src = src.crop(((sw - nw) // 2, 0, (sw + nw) // 2, sh))
else:
    nh = int(sw / target)
    src = src.crop((0, (sh - nh) // 2, sw, (sh + nh) // 2))
img = src.resize((CW, CH), Image.LANCZOS)

arr = np.asarray(img, np.float32) / 255.0

# =========================================================
# 2. cool-purple dusk grade (shadow violet, clean highlights)
# =========================================================
lum = arr @ np.array([0.2126, 0.7152, 0.0722], np.float32)
shadow_tint = np.array([0.30, 0.26, 0.46], np.float32)
high_tint = np.array([0.80, 0.78, 0.90], np.float32)
tint = shadow_tint[None, None, :] * (1 - lum)[..., None] + high_tint[None, None, :] * lum[..., None]
arr = np.clip(arr * 0.80 + (arr * tint * 1.28) * 0.20, 0, 1)

# contrast S-curve
arr = np.clip(arr + 0.17 * (arr - 0.5) * (1 - np.abs(arr - 0.5) * 2), 0, 1)
# knock a little saturation out of the tans so the plate stays cool
arr = np.clip(arr * 0.90 + lum[..., None] * 0.10, 0, 1)

# kill the orange/peach horizon glow: warm + bright pixels get pulled to violet-grey
r_, g_, b_ = arr[..., 0], arr[..., 1], arr[..., 2]
warm = np.clip((r_ - b_) * 2.2, 0, 1) * np.clip((lum - 0.28) * 2.6, 0, 1)
warm = (warm * 0.85)[..., None]
cool = arr * np.array([0.80, 0.84, 1.02], np.float32) + np.array([0.0, 0.01, 0.07], np.float32)
arr = np.clip(arr * (1 - warm) + cool * warm, 0, 1)
lum = arr @ np.array([0.2126, 0.7152, 0.0722], np.float32)

# =========================================================
# 3. fade to near-black through the bottom 45% + vignette
# =========================================================
yy = np.linspace(0, 1, CH, dtype=np.float32)[:, None]
xx = np.linspace(0, 1, CW, dtype=np.float32)[None, :]

fade = np.clip((yy - 0.400) / 0.420, 0, 1) ** 0.55 * 0.970
keep = (1 - fade)[..., None]
black = np.array(BLACK, np.float32) / 255.0
arr = arr * keep + black[None, None, :] * (1 - keep)

# soft superellipse panel behind the type block: clears the copy, keeps the edges open
panel = np.exp(-(((xx - 0.5) / 0.44) ** 4 + ((yy - 0.760) / 0.215) ** 4))
arr = arr * (1 - 0.72 * panel[..., None])

r = np.sqrt(((xx - 0.5) * 1.08) ** 2 + ((yy - 0.42) * 0.82) ** 2) / 0.72
arr = arr * np.clip(1 - 0.40 * np.clip(r - 0.40, 0, 2) ** 1.4, 0, 1)[..., None]

# =========================================================
# 4. faint paper crumple + film grain (shared with the black slides)
# =========================================================
arr = arr + (paper_field(amplitude=12.0, crease_amp=3.5) * 0.9)[..., None] / 255.0
arr = add_grain(np.clip(arr, 0, 1), sigma=4.6, seed=3)

img = Image.fromarray(np.uint8(np.clip(arr, 0, 1) * 255 + 0.5), "RGB").convert("RGBA")

# =========================================================
# 5. type block
# =========================================================
layer = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)

line1, line2 = "6 HOOKS THAT", "STOP THE SCROLL"

# --- size the headline to the widest line, inside the content box ---
track_em = -0.035
probe_size = 200
fp = ImageFont.truetype(str(FONTS / ANTON), probe_size)
probe_tr = probe_size * track_em
widest = max(tracked_w(fp, line1, probe_tr), tracked_w(fp, line2, probe_tr))
size = probe_size * (CONTENT_W / widest)          # 1x units

f1 = ImageFont.truetype(str(FONTS / ANTON), px(size))
tr = px(size) * track_em
cap_h = (f1.getbbox("H")[3] - f1.getbbox("H")[1]) / SS   # back to 1x units

# ---- vertical rhythm, all in 1080x1350 units ----
FOOTER_BASE = 1300
PILL_H = 76
PILL_TOP = FOOTER_BASE - 36 - PILL_H              # 1188
BAR_TOP = PILL_TOP - 34                            # 1154
BAR_H = 12
SUP_BASE = BAR_TOP - 30                            # 1124
base2 = SUP_BASE - 46                              # 1078
base1 = base2 - size * 0.865
cap_top = base1 - cap_h
KICKER_BASE = cap_top - 32

print(f"headline {size:.1f}px  cap {cap_h:.0f}  baselines {base1:.0f}/{base2:.0f} "
      f"sup {SUP_BASE} bar {BAR_TOP} pill {PILL_TOP}-{PILL_TOP + PILL_H} footer {FOOTER_BASE}")

# --- kicker ---
kick = font(INTER, 28, 700)
kick_tr = px(28) * 0.27
draw_tracked(d, (CW / 2, px(KICKER_BASE)), "WARNING:", kick, RED + (255,), kick_tr, "ms")

# --- headline: soft dark halo first, for separation from the photo ---
halo = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
hd = ImageDraw.Draw(halo)
for txt, by in ((line1, base1), (line2, base2)):
    draw_tracked(hd, (CW / 2, px(by)), txt, f1, (0, 0, 0, 255), tr, "ms")
halo = halo.filter(ImageFilter.GaussianBlur(px(26)))
halo.putalpha(halo.getchannel("A").point(lambda a: int(a * 0.42)))
layer = Image.alpha_composite(layer, halo)
d = ImageDraw.Draw(layer)

draw_tracked(d, (CW / 2, px(base1)), line1, f1, OFFWHITE + (255,), tr, "ms")
draw_tracked(d, (CW / 2, px(base2)), line2, f1, RED + (255,), tr, "ms")

# --- support line ---
sup = font(INTER_IT, 33, 400)
d.text((CW / 2, px(SUP_BASE)), "on a clothing ad.", font=sup,
       fill=OFFWHITE + (238,), anchor="ms")

# --- the one thick horizontal bar ---
bar_w = px(188)
d.rounded_rectangle(
    [CW / 2 - bar_w / 2, px(BAR_TOP), CW / 2 + bar_w / 2, px(BAR_TOP + BAR_H)],
    radius=px(BAR_H) / 2, fill=RED + (255,),
)

# --- glowing translucent red pill ---
pill_font = font(INTER, 26, 700)
pill_text = "SWIPE FOR ALL 6 >>>"
pill_tr = px(26) * 0.16
tw = tracked_w(pill_font, pill_text, pill_tr)
pill_w = tw + px(104)
x0, x1 = CW / 2 - pill_w / 2, CW / 2 + pill_w / 2
y0, y1 = px(PILL_TOP), px(PILL_TOP + PILL_H)
rad = (y1 - y0) / 2

glow = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
ImageDraw.Draw(glow).rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=RED + (190,))
wide = glow.filter(ImageFilter.GaussianBlur(px(42)))
tight = glow.filter(ImageFilter.GaussianBlur(px(12)))
tight.putalpha(tight.getchannel("A").point(lambda a: int(a * 0.85)))
layer = Image.alpha_composite(layer, wide)
layer = Image.alpha_composite(layer, tight)
d = ImageDraw.Draw(layer)

body = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
ImageDraw.Draw(body).rounded_rectangle([x0, y0, x1, y1], radius=rad, fill=RED + (202,))
layer = Image.alpha_composite(layer, body)
d = ImageDraw.Draw(layer)

d.rounded_rectangle(
    [x0 + px(1.5), y0 + px(1.5), x1 - px(1.5), y1 - px(1.5)],
    radius=rad, outline=(255, 255, 255, 60), width=px(1.4),
)
draw_tracked(d, (CW / 2, (y0 + y1) / 2 + px(9)), pill_text, pill_font,
             (255, 255, 255, 255), pill_tr, "ms")

# --- furniture: handle left, counter right ---
fur = font(INTER, 21, 500)
draw_tracked(d, (px(MARGIN), px(FOOTER_BASE)), "@lvlsmarketing", fur, GREY + (235,), px(0.3), "ls")
draw_tracked(d, (CW - px(MARGIN), px(FOOTER_BASE)), "1/8", fur, GREY + (235,), px(0.3), "rs")

# =========================================================
save(Image.alpha_composite(img, layer), "slide-01")
