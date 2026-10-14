"""Low-level drawing helpers: backgrounds, typography, chips, highlights."""
from __future__ import annotations

import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from theme import font, px


# ------------------------------------------------------------- backgrounds ---
def make_background(w: int, h: int, pal: dict, seed: int = 7) -> Image.Image:
    """Vertical gradient + accent glow + vignette + fine grain."""
    top = np.array(pal["bg_top"], dtype=np.float32)
    bot = np.array(pal["bg_bottom"], dtype=np.float32)
    t = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None, None]
    t = t ** 1.18
    col = top[None, None, :] * (1 - t) + bot[None, None, :] * t   # (h,1,3)
    arr = np.broadcast_to(col, (h, w, 3)).copy()
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")

    # soft accent glow, upper-right and lower-left
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    ga = pal["glow_alpha"]
    gc = pal["glow"]
    for cx, cy, rad, a in (
        (0.86 * w, 0.06 * h, 0.62 * w, ga),
        (0.06 * w, 0.98 * h, 0.55 * w, int(ga * 0.6)),
    ):
        gd.ellipse(
            [cx - rad, cy - rad, cx + rad, cy + rad],
            fill=(*gc, a),
        )
    glow = glow.filter(ImageFilter.GaussianBlur(radius=0.22 * w))
    img = img.convert("RGBA")
    img.alpha_composite(glow)

    # vignette
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = (xx - w / 2) / (w / 2)
    ny = (yy - h / 2) / (h / 2)
    d = np.sqrt(nx ** 2 + ny ** 2)
    vig = np.clip((d - 0.55) / 0.85, 0, 1) ** 1.6 * pal["vignette"]
    shade = Image.fromarray(vig.astype(np.uint8), "L")
    dark = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    dark.putalpha(shade)
    img.alpha_composite(dark)

    # grain
    rng = np.random.default_rng(seed)
    n = rng.normal(0.0, pal["noise"], size=(h, w)).astype(np.float32)
    base = np.array(img, dtype=np.float32)
    base[:, :, :3] += n[:, :, None]
    base[:, :, 3] = 255
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGBA")

    # faint diagonal hairline texture (top-left corner block)
    tex = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tex)
    step = max(14, px(26, w / 1080))
    line_col = (255, 255, 255, 7) if pal["vignette"] > 40 else (18, 18, 20, 7)
    for i in range(-h, w + h, step):
        td.line([(i, 0), (i + h, h)], fill=line_col, width=1)
    tex = tex.filter(ImageFilter.GaussianBlur(0.4))
    img.alpha_composite(tex)
    return img


# ----------------------------------------------------------------- shapes ---
def rrect(dr: ImageDraw.ImageDraw, box, radius, fill=None, outline=None, width=1):
    dr.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def circle_badge(dr, cx, cy, r, fill=None, outline=None, width=1):
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)


def soft_shadow(base: Image.Image, box, radius, blur, alpha, color=(0, 0, 0)):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(box, radius=radius, fill=(*color, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)


# ------------------------------------------------------------- typography ---
def spaced_width(dr, text, f, tracking):
    if not tracking:
        return dr.textlength(text, font=f)
    return dr.textlength(text, font=f) + tracking * max(0, len(text) - 1)


def draw_spaced(dr, xy, text, f, fill, tracking=0, anchor="la"):
    """Draw text with manual letter-spacing. anchor supports l/c/r + a/t/m."""
    x, y = xy
    total = spaced_width(dr, text, f, tracking)
    halign = anchor[0]
    if halign == "c":
        x -= total / 2
    elif halign == "r":
        x -= total
    valign = anchor[1] if len(anchor) > 1 else "a"
    if valign != "a":
        bb = f.getbbox("Ag")
        cap_h = -bb[1]
        if valign == "m":
            y -= cap_h / 2
        elif valign == "b":
            y -= cap_h
    if not tracking:
        dr.text((x, y), text, font=f, fill=fill, anchor="la")
        return total
    cx = x
    for ch in text:
        dr.text((cx, y), ch, font=f, fill=fill, anchor="la")
        cx += dr.textlength(ch, font=f) + tracking
    return total


def fit_size(dr, text, fkey, max_w, hi, lo=8, tracking=0):
    """Largest font size (<= hi) that fits text in max_w."""
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        if spaced_width(dr, text, font(fkey, mid), tracking) <= max_w:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def wrap_tokens(dr, tokens, max_w):
    """tokens = [ {text, font, fill, hl?, hl_ink?} ] -> list of lines (word dicts)."""
    words = []
    for tok in tokens:
        f = tok["font"]
        tr = tok.get("tracking", 0)
        for i, wd in enumerate(tok["text"].split(" ")):
            if not wd:
                continue
            words.append(
                {
                    "word": wd,
                    "font": f,
                    "fill": tok["fill"],
                    "hl": tok.get("hl"),
                    "hl_ink": tok.get("hl_ink"),
                    "tracking": tr,
                    "space_before": bool(words) or i > 0,
                    "w": spaced_width(dr, wd, f, tr),
                }
            )
    lines, cur, cur_w = [], [], 0.0
    sp = dr.textlength(" ", font=words[0]["font"]) if words else 0
    for wd in words:
        gap = sp if cur else 0
        if cur and cur_w + gap + wd["w"] > max_w:
            lines.append(cur)
            cur, cur_w = [], 0.0
            gap = 0
        cur.append(wd)
        cur_w += gap + wd["w"]
    if cur:
        lines.append(cur)
    return lines


def draw_block(
    base,
    dr,
    xy,
    tokens,
    max_w,
    leading=1.02,
    align="left",
    hl_slant=0.16,
    seed=1,
    hl_pad=None,
):
    """Draw a wrapped, mixed-style paragraph. Returns bottom y."""
    rng = random.Random(seed)
    img = base
    x0, y = xy
    lines = wrap_tokens(dr, tokens, max_w)
    sizes = [max(w["font"].size for w in ln) for ln in lines]
    hl_pad = hl_pad or {}
    for li, ln in enumerate(lines):
        fsize = sizes[li]
        line_h = fsize * leading
        asc, desc = font("disp", fsize).getmetrics()
        # measure line width
        sp = dr.textlength(" ", font=ln[0]["font"])
        lw = sum(w["w"] for w in ln) + sp * (len(ln) - 1)
        if align == "center":
            cx = x0 + (max_w - lw) / 2
        elif align == "right":
            cx = x0 + max_w - lw
        else:
            cx = x0
        # highlight boxes first (behind glyphs); adjacent hl words merge into one run
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        run_x = cx
        positions = []
        for w in ln:
            positions.append((w, run_x))
            run_x += w["w"] + sp
        runs, cur = [], None
        for w, wx in positions:
            if w["hl"]:
                if cur is None:
                    cur = {"hl": w["hl"], "left": wx, "right": wx + w["w"],
                           "font": w["font"]}
                else:
                    cur["right"] = wx + w["w"]
            else:
                if cur:
                    runs.append(cur)
                cur = None
        if cur:
            runs.append(cur)
        for rn in runs:
            fnt = rn["font"]
            bb = fnt.getbbox("Ag")
            top = y + bb[1] - fsize * 0.06
            bot = y + bb[3] + fsize * 0.10
            left = rn["left"] - fsize * 0.075
            right = rn["right"] + fsize * 0.075
            jx = rng.uniform(-1, 1) * fsize * 0.012
            slant = (bot - top) * hl_slant
            ld.polygon(
                [
                    (left + slant + jx, top),
                    (right + slant - jx, top),
                    (right - jx, bot),
                    (left - jx, bot),
                ],
                fill=rn["hl"],
            )
        if runs:
            layer = layer.filter(ImageFilter.GaussianBlur(0.35))
            img.alpha_composite(layer)
        # glyphs
        run_x = cx
        for w in ln:
            fill = w["hl_ink"] if (w["hl"] and w.get("hl_ink")) else w["fill"]
            draw_spaced(dr, (run_x, y), w["word"], w["font"], fill, w["tracking"])
            run_x += w["w"] + sp
        y += line_h
    return y


def ghost_numeral(base, text, fkey, size, xy, fill, angle=0, alpha_scale=1.0):
    """Big low-opacity numeral composited into the background."""
    f = font(fkey, size)
    tmp = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.text(xy, text, font=f, fill=fill, anchor="la")
    if angle:
        tmp = tmp.rotate(angle, resample=Image.BICUBIC, center=(xy[0], xy[1]))
    base.alpha_composite(tmp)


def chip(dr, text, xy, fkey, size, fill, ink, pad_x, pad_y, tracking=0, radius=None,
         outline=None):
    """Pill chip with optically centred tracked text."""
    f = font(fkey, size)
    w = spaced_width(dr, text, f, tracking)
    bb = f.getbbox("AG")
    glyph_h = bb[3] - bb[1]
    x, y = xy
    box = [x, y, x + w + pad_x * 2, y + glyph_h + pad_y * 2]
    r = radius if radius is not None else (box[3] - box[1]) / 2
    if outline:
        dr.rounded_rectangle([box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3],
                             radius=r + 3, outline=outline, width=2)
    dr.rounded_rectangle(box, radius=r, fill=fill)
    ty = y + (box[3] - box[1] - glyph_h) / 2 - bb[1]
    draw_spaced(dr, (x + pad_x, ty), text, f, ink, tracking)
    return box


def arrow_swipe(dr, x, y, length, thick, color, heads=3, gap=None):
    """Triple chevron swipe cue."""
    gap = gap or length * 0.62
    for i in range(heads):
        cx = x + i * gap
        dr.line(
            [(cx, y - length * 0.42), (cx + length * 0.42, y), (cx, y + length * 0.42)],
            fill=color,
            width=thick,
            joint="curve",
        )


def progress_pips(dr, x_right, y, total, active, s, on_color, off_color, label=None,
                  label_font=None, label_color=None):
    """Right-aligned progress bars 01/05."""
    bw, bh, gap = px(34, s), px(9, s), px(9, s)
    x = x_right - (bw * total + gap * (total - 1))
    for i in range(total):
        col = on_color if i <= active else off_color
        rrect(dr, [x, y, x + bw, y + bh], bh / 2, fill=col)
        x += bw + gap
    if label:
        f = label_font or font("label", px(20, s))
        draw_spaced(dr, (x_right, y - px(30, s)), label, f, label_color, px(2.4, s), "rm")
