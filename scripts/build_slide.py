#!/usr/bin/env python3
"""
Carousel slide 01 — 1080x1350 (4:5).

Brutalist "warning poster" over a cinematic dusk photograph.
Rendered at 2x and downsampled so the type stays crisp.

All copy is fixed by the brief; nothing else is drawn.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

W, H = 1080, 1350
SS = 2
CW, CH = W * SS, H * SS

# ---------------- palette ----------------
BLACK = (10, 10, 10)          # #0A0A0A
OFFWHITE = (243, 240, 236)    # primary type
GREY = (150, 147, 144)        # furniture only
RED = (232, 25, 29)           # #E8191D — the single accent

MARGIN = 86                   # ~8% of 1080
CONTENT_W = W - 2 * MARGIN    # 908


def px(v):
    return int(round(v * SS))


def fbm(shape, octaves=6, seed=11, base=5):
    """Multi-octave value noise (bilinear upsample), 0..1."""
    rng = np.random.default_rng(seed)
    h, w = shape
    out = np.zeros(shape, np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        gh = max(2, base * 2 ** o)
        gw = max(2, int(base * 2 ** o * w / h))
        grid = rng.random((gh, gw)).astype(np.float32)
        layer = np.asarray(
            Image.fromarray((grid * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC),
            np.float32,
        ) / 255.0
        out += layer * amp
        total += amp
        amp *= 0.5
    return out / total


# ---------------- type helpers ----------------
def font(path, size, weight=None):
    f = ImageFont.truetype(str(FONTS / path), px(size))
    if weight is not None:
        f.set_variation_by_axes([14, weight])
    return f


def adv(f, text):
    return f.getlength(text)


def tracked_w(f, text, tr):
    return sum(f.getlength(c) for c in text) + tr * max(0, len(text) - 1)


def draw_tracked(d, xy, text, f, fill, tr, anchor="ms"):
    """anchor: horizontal m/l/r + vertical baseline 's'."""
    x, y = xy
    w = tracked_w(f, text, tr)
    if anchor[0] == "m":
        x -= w / 2
    elif anchor[0] == "r":
        x -= w
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill, anchor="ls")
        x += f.getlength(ch) + tr
    return w


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
# 4. faint paper crumple + film grain  (all deltas in 8-bit units)
# =========================================================
height = fbm((CH, CW), octaves=6, seed=11, base=5)
gy, gx = np.gradient(height)
shade = 0.72 * gy + 0.38 * gx
shade /= np.abs(shade).max() + 1e-6
crumple = np.clip(0.5 + shade * 0.55, 0, 1)

Y2, X2 = np.mgrid[0:CH, 0:CW].astype(np.float32)
crease = np.zeros((CH, CW), np.float32)
for ang, off, strength in [(0.55, 0.24, 0.55), (-0.30, 0.66, 0.40), (0.10, 0.86, 0.30)]:
    dd = (X2 / CW) * np.sin(ang) + (Y2 / CH) * np.cos(ang) - off
    crease += np.exp(-(dd ** 2) / (2 * 0.0016 ** 2)) * strength
crease = np.clip(crease, 0, 1)

texture = (crumple - 0.5) * 12.0 + (crease - 0.30) * 3.5   # 8-bit units
arr = arr + (texture * 0.9)[..., None] / 255.0

rng = np.random.default_rng(3)
grain = rng.normal(0, 4.6, (CH, CW, 1)).repeat(3, axis=2)
grain = np.asarray(
    Image.fromarray(np.uint8(np.clip(grain + 128, 0, 255))).filter(ImageFilter.GaussianBlur(0.5)),
    np.float32,
) - 128.0
arr = arr + grain / 255.0

img = Image.fromarray(np.uint8(np.clip(arr, 0, 1) * 255 + 0.5), "RGB").convert("RGBA")

# =========================================================
# 5. type block
# =========================================================
layer = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)

ANTON = "Anton-Regular.ttf"
INTER = "Inter-Variable.ttf"
INTER_IT = "Inter-Variable-Italic.ttf"

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
out = Image.alpha_composite(img, layer).convert("RGB").resize((W, H), Image.LANCZOS)
out.save(OUT / "slide-01.png", optimize=True)
out.resize((360, 450), Image.LANCZOS).save(OUT / "slide-01-thumb.png")
print("saved", OUT / "slide-01.png")
