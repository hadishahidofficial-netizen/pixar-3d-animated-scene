#!/usr/bin/env python3
"""
Shared machinery for the "warning poster" carousel slides.

Palette, grid, font loading, letter-spaced type, paper texture and grain.
Slides render at 2x and are downsampled for crisp edges.
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

# palette ---------------------------------------------------------------
BLACK = (10, 10, 10)          # #0A0A0A
OFFWHITE = (243, 240, 236)    # primary type
DIM = (198, 195, 191)         # second-tier white
GREY = (150, 147, 144)        # furniture only
RED = (232, 25, 29)           # #E8191D — the single accent

MARGIN = 86                   # ~8% of 1080
CONTENT_W = W - 2 * MARGIN    # 908

ANTON = "Anton-Regular.ttf"
INTER = "Inter-Variable.ttf"
INTER_IT = "Inter-Variable-Italic.ttf"


def px(v):
    return int(round(v * SS))


def font(name, size, weight=None):
    f = ImageFont.truetype(str(FONTS / name), px(size))
    if weight is not None:
        f.set_variation_by_axes([14, weight])
    return f


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


def fit_display(texts, max_w, track_em=-0.035, probe=200):
    """Size (1x units) at which the widest of `texts` exactly fills max_w."""
    fp = ImageFont.truetype(str(FONTS / ANTON), probe)
    probe_tr = probe * track_em
    widest = max(tracked_w(fp, t, probe_tr) for t in texts)
    return probe * (max_w / widest)


def fit_inter(texts, max_w, weight=400, italic=False, probe=40):
    """Largest Inter size (1x units, <= probe) at which all lines fit max_w."""
    f = ImageFont.truetype(str(FONTS / (INTER_IT if italic else INTER)), probe)
    f.set_variation_by_axes([14, weight])
    widest = max(f.getlength(t) for t in texts)
    return min(probe, probe * (max_w / widest))


# texture ---------------------------------------------------------------
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


def paper_field(seed=11, amplitude=8.0, crease_amp=6.0):
    """Faint crumple shading + a few long fold creases, in 8-bit units."""
    height = fbm((CH, CW), octaves=6, seed=seed, base=5)
    gy, gx = np.gradient(height)
    shade = 0.72 * gy + 0.38 * gx
    shade = shade / (np.abs(shade).max() + 1e-6)
    crumple = np.clip(0.5 + shade * 0.55, 0, 1)

    Y2, X2 = np.mgrid[0:CH, 0:CW].astype(np.float32)
    crease = np.zeros((CH, CW), np.float32)
    folds = [
        (0.62, 0.24, 0.55, 0.0030),
        (-0.34, 0.68, 0.42, 0.0038),
        (0.08, 0.90, 0.30, 0.0046),
        (-0.72, 0.44, 0.26, 0.0050),
    ]
    for ang, off, strength, width in folds:
        dd = (X2 / CW) * np.sin(ang) + (Y2 / CH) * np.cos(ang) - off
        crease += np.exp(-(dd ** 2) / (2 * width ** 2)) * strength
    crease = np.clip(crease, 0, 1)

    broad = (fbm((CH, CW), octaves=4, seed=seed + 5, base=2) - 0.5) * 2.4
    return (crumple - 0.5) * amplitude + (crease - 0.30) * crease_amp + broad


def add_grain(arr, sigma=4.2, seed=3):
    rng = np.random.default_rng(seed)
    grain = rng.normal(0, sigma, (CH, CW, 1)).repeat(3, axis=2)
    grain = np.asarray(
        Image.fromarray(np.uint8(np.clip(grain + 128, 0, 255))).filter(ImageFilter.GaussianBlur(0.5)),
        np.float32,
    ) - 128.0
    return arr + grain / 255.0


def black_canvas():
    """#0A0A0A with a very faint paper-crumple texture and grain."""
    base = np.full((CH, CW, 3), np.array(BLACK, np.float32) / 255.0, np.float32)
    base = base + (paper_field(amplitude=8.5, crease_amp=7.0) * 0.95)[..., None] / 255.0
    base = add_grain(np.clip(base, 0, 1), sigma=3.6, seed=5)

    # keep the corners dead-black so the frame reads as pure #0A0A0A at the edges
    yy = np.linspace(0, 1, CH, dtype=np.float32)[:, None]
    xx = np.linspace(0, 1, CW, dtype=np.float32)[None, :]
    edge = np.clip(1 - 6 * np.minimum(np.minimum(xx, 1 - xx), np.minimum(yy, 1 - yy)), 0, 1)
    base = base * (1 - edge[..., None]) + (np.array(BLACK, np.float32) / 255.0) * edge[..., None]

    return Image.fromarray(np.uint8(np.clip(base, 0, 1) * 255 + 0.5), "RGB").convert("RGBA")


def save(img, name):
    out = img.convert("RGB").resize((W, H), Image.LANCZOS)
    path = OUT / f"{name}.png"
    out.save(path, optimize=True)
    out.resize((324, 405), Image.LANCZOS).save(OUT / f"{name}-thumb.png")
    print("saved", path)
    return out
