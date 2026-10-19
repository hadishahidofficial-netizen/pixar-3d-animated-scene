#!/usr/bin/env python3
"""
Q4 Email Flows — 7-slide Instagram carousel builder.

Design system (locked):
  1080 x 1350, bg #080808, off-white #F4F1EC, single accent orange #E95C24
  Barlow Condensed (display) + Barlow (body), 8% safe margins, film grain.
Renders one PNG per slide into carousel/ at 1080x1350.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "assets", "fonts")
BG_DIR = os.path.join(ROOT, "assets", "bg")
OUT_DIR = os.path.join(ROOT, "carousel")

W, H = 1080, 1350
M = 86                      # 8% margin
COL_W = W - 2 * M           # 908

BG = (8, 8, 8)
PAPER = (244, 241, 236)
ORANGE = (233, 92, 36)
GREY = (138, 133, 126)

FOOTER_BASE = H - M          # 1264
RULE_Y = FOOTER_BASE - 58    # 1206
CONTENT_BOTTOM = RULE_Y - 56  # 1150

_FONT_CACHE = {}


def F(name, size):
    key = (name, size)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(os.path.join(FONT_DIR, name + ".ttf"), size)
    return _FONT_CACHE[key]


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


def cap_h(font):
    b = font.getbbox("H")
    return b[3] - b[1]


def run_width(runs, tracking=0.0):
    w = 0.0
    for text, font, _ in runs:
        if tracking == 0:
            w += font.getlength(text)
        else:
            w += sum(font.getlength(c) for c in text) + tracking * len(text)
    return w


def draw_run(d, x, baseline, runs, tracking=0.0):
    """Draw a baseline-aligned run of (text, font, color) segments."""
    cx = x
    for text, font, color in runs:
        if tracking == 0:
            d.text((cx, baseline), text, font=font, fill=color, anchor="ls")
            cx += font.getlength(text)
        else:
            for ch in text:
                d.text((cx, baseline), ch, font=font, fill=color, anchor="ls")
                cx += font.getlength(ch) + tracking
    return cx


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# --------------------------------------------------------------------------
# photographic base
# --------------------------------------------------------------------------

def photo_panel(img, name, photo_h, crop="top"):
    src = Image.open(os.path.join(BG_DIR, name)).convert("RGB")
    scale = W / src.width
    resized = src.resize((W, max(1, int(round(src.height * scale)))), Image.LANCZOS)
    if crop == "top":
        top = 0
    elif crop == "center":
        top = max(0, (resized.height - photo_h) // 2)
    else:
        top = int(crop)
    panel = resized.crop((0, top, W, min(resized.height, top + photo_h)))
    if panel.height < photo_h:
        panel = panel.resize((W, photo_h), Image.LANCZOS)

    # cinematic grade: slight lift in contrast, cool shadows
    arr = np.asarray(panel).astype(np.float32) / 255.0
    arr = np.clip((arr - 0.5) * 1.06 + 0.5, 0, 1)
    arr[..., 2] = np.clip(arr[..., 2] * 1.02, 0, 1)
    panel = Image.fromarray((arr * 255).astype(np.uint8))

    img.paste(panel, (0, 0))

    # bottom fade into the page colour (long, smooth)
    fade_h = min(520, int(photo_h * 0.62))
    grad = Image.new("L", (1, fade_h))
    gd = ImageDraw.Draw(grad)
    for y in range(fade_h):
        t = y / max(1, fade_h - 1)
        gd.point((0, y), fill=int(255 * (t ** 1.25)))
    grad = grad.resize((W, fade_h))
    fade_layer = Image.new("RGB", (W, fade_h), BG)
    base = img.crop((0, photo_h - fade_h, W, photo_h))
    img.paste(Image.composite(fade_layer, base, grad), (0, photo_h - fade_h))

    # top scrim so the furniture stays legible
    scrim_h = 250
    sgrad = Image.new("L", (1, scrim_h))
    sd = ImageDraw.Draw(sgrad)
    for y in range(scrim_h):
        t = 1 - y / (scrim_h - 1)
        sd.point((0, y), fill=int(255 * 0.62 * (t ** 1.7)))
    sgrad = sgrad.resize((W, scrim_h))
    img.paste(Image.composite(Image.new("RGB", (W, scrim_h), BG), img.crop((0, 0, W, scrim_h)), sgrad), (0, 0))


def finish(img, seed=3):
    arr = np.asarray(img).astype(np.float32)

    # vignette
    gy, gx = np.mgrid[0:H, 0:W]
    nx = (gx - W / 2) / (W / 2)
    ny = (gy - H / 2) / (H / 2)
    vig = 1 - 0.16 * np.clip((nx ** 2 + ny ** 2) * 0.55, 0, 1)
    arr *= vig[..., None]

    # film grain
    rng = np.random.default_rng(seed)
    grain = rng.normal(0, 1, (H, W)).astype(np.float32)
    grain = np.asarray(Image.fromarray(((grain * 0.5 + 0.5) * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32)
    grain = (grain - 127.5) / 127.5
    arr += grain[..., None] * 5.2

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


# --------------------------------------------------------------------------
# furniture / typography blocks
# --------------------------------------------------------------------------

def furniture(img, index, total=7, footer_left="Swipe for more >>>"):
    d = ImageDraw.Draw(img)

    # top-left: orange square + small-caps label
    sq = 16
    d.rectangle([M, 86, M + sq, 86 + sq], fill=ORANGE)
    label_font = F("Barlow-Medium", 18)
    lab_base = 86 + sq - 1
    draw_run(d, M + sq + 13, lab_base, [("CLOTHING BRAND EMAIL", label_font, mix(PAPER, BG, 0.30))],
             tracking=3.1)

    # top-right handle
    handle_font = F("Barlow-Regular", 19)
    d.text((W - M, 86 + sq - 1), "@lvlsmarketing", font=handle_font,
           fill=mix(PAPER, BG, 0.52), anchor="rs")

    # bottom row
    foot_font = F("Barlow-Medium", 19)
    d.text((M, FOOTER_BASE), footer_left, font=foot_font, fill=mix(PAPER, BG, 0.42), anchor="ls")
    d.text((W - M, FOOTER_BASE), f"{index}/{total}", font=foot_font,
           fill=mix(PAPER, BG, 0.42), anchor="rs")

    # hairline rule with a small diamond in the middle
    d.line([(M, RULE_Y), (W - M, RULE_Y)], fill=mix(ORANGE, BG, 0.45), width=1)
    r = 6
    d.polygon([(W // 2, RULE_Y - r), (W // 2 + r, RULE_Y), (W // 2, RULE_Y + r), (W // 2 - r, RULE_Y)],
              fill=ORANGE)


def title_height(size, n_lines, lh=0.87):
    return int(round(size * lh * (n_lines - 1) + size * 0.735))


def fit_title(lines, max_w, max_h, start=232, floor=64, tracking_f=-0.012):
    """Largest display size where every line fits the column and the block fits max_h."""
    for size in range(start, floor - 1, -2):
        tr = tracking_f * size
        widest = 0
        for line in lines:
            runs = []
            for txt, style in line:
                fname = "BarlowCondensed-BoldItalic" if style == "accent" else "BarlowCondensed-Bold"
                runs.append((txt, F(fname, size), PAPER))
            widest = max(widest, run_width(runs, tr))
        if widest <= max_w and title_height(size, len(lines)) <= max_h:
            return size
    return floor


def draw_title(d, lines, size, cap_top, tracking_f=-0.012):
    tr = tracking_f * size
    lh = size * 0.87
    fname = "BarlowCondensed-Bold"
    base0 = cap_top + cap_h(F(fname, size))
    for i, line in enumerate(lines):
        runs = []
        for txt, style in line:
            if style == "accent":
                runs.append((txt, F("BarlowCondensed-BoldItalic", size), ORANGE))
            elif style == "muted":
                runs.append((txt, F("BarlowCondensed-Bold", size), mix(PAPER, BG, 0.42)))
            else:
                runs.append((txt, F("BarlowCondensed-Bold", size), PAPER))
        draw_run(d, M, base0 + i * lh, runs, tr)
    return cap_top + title_height(size, len(lines))


def draw_lede(d, text, top, size=34, color=None, max_w=COL_W, lh=1.34, font="Barlow-Regular"):
    f = F(font, size)
    color = color or mix(PAPER, BG, 0.22)
    lines = wrap(text, f, max_w)
    for i, ln in enumerate(lines):
        d.text((M, top + i * size * lh), ln, font=f, fill=color, anchor="la")
    return top + size * lh * (len(lines) - 1) + size * 1.05


def lede_height(text, size=34, max_w=COL_W, lh=1.34, font="Barlow-Regular"):
    f = F(font, size)
    n = len(wrap(text, f, max_w))
    return int(size * lh * (n - 1) + size * 1.05)


def rows_block(d, rows, top, row_h=74, style="index"):
    """Rows: list of dicts with keys used by the style."""
    for i, row in enumerate(rows):
        y = top + i * row_h
        if i:
            d.line([(M, y), (W - M, y)], fill=mix(PAPER, BG, 0.86), width=1)
        base = y + row_h * 0.62 + 20
        if style == "index":
            d.text((M, base), row["num"], font=F("BarlowCondensed-Medium", 30),
                   fill=mix(PAPER, BG, 0.48), anchor="ls")
            x = M + 62
            x = draw_run(d, x, base, [(row["name"], F("BarlowCondensed-SemiBold", 42), PAPER)],
                         tracking=0.2)
            d.text((x + 16, base), row["note"], font=F("Barlow-Regular", 23),
                   fill=mix(PAPER, BG, 0.40), anchor="ls")
        elif style == "spec":
            d.text((M, base), row["name"], font=F("BarlowCondensed-SemiBold", 40),
                   fill=PAPER, anchor="ls")
            d.text((W - M, base), row["value"], font=F("BarlowCondensed-SemiBold", 38),
                   fill=PAPER, anchor="rs")
        elif style == "time":
            d.text((M, base), row["time"], font=F("BarlowCondensed-Bold", 38),
                   fill=PAPER, anchor="ls")
            d.text((M + 172, base), row["note"], font=F("Barlow-Regular", 26),
                   fill=mix(PAPER, BG, 0.26), anchor="ls")


def cta_button(img, label, top, size=32):
    d = ImageDraw.Draw(img)
    f = F("BarlowCondensed-SemiBold", size)
    tr = 3.0
    tw = run_width([(label, f, PAPER)], tr)
    pad = 46
    bw = min(COL_W, tw + pad * 2)
    bh = 82
    x0 = M
    d.rounded_rectangle([x0, top, x0 + bw, top + bh], radius=bh // 2, fill=PAPER)
    draw_run(d, x0 + (bw - tw) / 2, top + bh / 2 + cap_h(f) / 2,
             [(label, f, (14, 14, 14))], tr)
    return top + bh


# --------------------------------------------------------------------------
# slides
# --------------------------------------------------------------------------

def compose(index, bg_name, photo_h, lines, lede, *, crop="top", title_max_h=340,
            title_start=240, lede_size=37, gap=32, cta=None, footer="Swipe for more >>>",
            rows=None, row_h=76, row_style="index", seed=1, gap_rows=34, gap_cta=34):
    """Shared slide grammar: photo band on top, one bottom-anchored type stack.

    Everything is measured before anything is drawn, so blocks can never collide.
    """
    img = Image.new("RGB", (W, H), BG)
    photo_panel(img, bg_name, photo_h, crop=crop)

    size = fit_title(lines, COL_W, title_max_h, start=title_start)
    th = title_height(size, len(lines))
    lh_ = lede_height(lede, lede_size) if lede else 0
    rows_h = (row_h * (len(rows) - 1) + row_h * 0.62 + 30) if rows else 0

    total = th
    if lede:
        total += gap + lh_
    if rows:
        total += gap_rows + rows_h
    if cta:
        total += gap_cta + 82

    title_top = CONTENT_BOTTOM - total

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    end = draw_title(d, lines, size, title_top)

    if lede:
        end = draw_lede(d, lede, end + gap, size=lede_size, max_w=COL_W)
    if rows:
        rt = end + gap_rows
        rows_block(d, rows, rt, row_h=row_h, style=row_style)
        end = rt + rows_h - 4
    if cta:
        cta_button(img, cta, end + gap_cta)

    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    furniture(img, index, footer_left=footer)
    return finish(img, seed=seed)


def slide_cover(index):
    lines = [[("5 EMAIL", "solid")], [("FLOWS", "accent")]]
    return compose(index, "01-desk.jpg", 700, lines,
                   "every clothing brand needs.",
                   title_max_h=352, title_start=244, lede_size=38, gap=36, seed=11)


def slide_problem(index):
    lines = [[("Q4 IS", "solid")], [("35–40%", "accent")], [("OF YOUR YEAR.", "solid")]]
    return compose(index, "02-hanger.jpg", 700, lines,
                   "Most clothing brands make it in twelve weeks. The smart ones build for it in the other forty.",
                   title_max_h=360, title_start=182, lede_size=36, gap=30, seed=22)


def slide_list(index):
    rows = [
        {"num": "01", "name": "WELCOME", "note": "Turn a first order into a second."},
        {"num": "02", "name": "ABANDONED CART", "note": "Recover the sale you almost lost."},
        {"num": "03", "name": "BROWSE ABANDON", "note": "Catch intent before it cools."},
        {"num": "04", "name": "POST-PURCHASE", "note": "Reviews, referrals, repeat orders."},
        {"num": "05", "name": "WINBACK", "note": "Wake up last season’s customers."},
    ]
    lines = [[("THE 5", "solid")], [("FLOWS.", "accent")]]
    return compose(index, "03-rack.jpg", 548, lines, None, title_max_h=246, title_start=150,
                   rows=rows, row_h=74, row_style="index", seed=33)


def flow_card(img, top, bottom):
    """A light 'document' card on the dark page - echo of the reference analytics shots."""
    d = ImageDraw.Draw(img)
    x0, x1 = M, W - M
    h = bottom - top

    # soft drop shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([x0 - 10, top + 14, x1 + 10, bottom + 22], radius=22, fill=(0, 0, 0, 190))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.paste(Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB"), (0, 0))

    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, top, x1, bottom], radius=10, fill=PAPER)

    ink = (20, 19, 18)
    ink_soft = mix(PAPER, ink, 0.52)
    ink_faint = mix(PAPER, ink, 0.30)

    pad = 42
    head_base = top + 58
    d.text((x0 + pad, head_base - 8), "THE FLOW MAP", font=F("BarlowCondensed-SemiBold", 24),
           fill=ink, anchor="ls")
    d.text((x1 - pad, head_base - 8), "5 FLOWS · LIVE IN 14 DAYS", font=F("Barlow-Medium", 15),
           fill=ink_soft, anchor="rs")
    d.line([(x0 + pad, top + 78), (x1 - pad, top + 78)], fill=mix(PAPER, ink, 0.14), width=1)

    rows = [
        ("WELCOME", "sends instantly", "INSTANT"),
        ("ABANDONED CART", "3 emails, first at 1 hour", "1 HOUR"),
        ("BROWSE ABANDON", "2 emails, first at 4 hours", "4 HOURS"),
        ("POST-PURCHASE", "review request + cross-sell", "7 DAYS"),
        ("WINBACK", "2 emails, no discount", "60 DAYS"),
    ]
    row_h = (bottom - (top + 78) - 26) / len(rows)
    dot_x = x0 + pad + 5
    first_cy = top + 78 + row_h / 2
    last_cy = top + 78 + row_h * (len(rows) - 0.5)
    d.line([(dot_x, first_cy), (dot_x, last_cy)], fill=mix(PAPER, ORANGE, 0.45), width=2)

    for i, (name, note, delay) in enumerate(rows):
        cy = top + 78 + row_h * (i + 0.5)
        r = 5
        d.ellipse([dot_x - r - 3, cy - r - 3, dot_x + r + 3, cy + r + 3], fill=PAPER)
        d.ellipse([dot_x - r, cy - r, dot_x + r, cy + r], fill=ORANGE)
        tx = dot_x + 34
        d.text((tx, cy + 2), name, font=F("BarlowCondensed-SemiBold", 34), fill=ink, anchor="ls")
        nw = F("BarlowCondensed-SemiBold", 34).getlength(name)
        d.text((tx + nw + 14, cy + 1), note, font=F("Barlow-Regular", 19), fill=ink_faint, anchor="ls")
        d.text((x1 - pad, cy + 2), delay, font=F("BarlowCondensed-SemiBold", 30), fill=ink_soft, anchor="rs")
        if i < len(rows) - 1:
            ly = cy + row_h / 2
            d.line([(x0 + pad, ly), (x1 - pad, ly)], fill=mix(PAPER, ink, 0.10), width=1)

    return img


def slide_timing(index):
    """The saveable one: title + light flow-map card (reference-style document on photo)."""
    img = Image.new("RGB", (W, H), BG)
    photo_panel(img, "04-phone.jpg", 372)

    lines = [[("TIMING", "solid")], [("BEATS COPY.", "solid")]]
    size = fit_title(lines, COL_W, 250, start=126)
    title_top = 402

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    end = draw_title(d, lines, size, title_top)
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

    card_top = end + 40
    img = flow_card(img, card_top, CONTENT_BOTTOM)

    furniture(img, index)
    return finish(img, seed=44)


def slide_cart(index):
    rows = [
        {"time": "1 HOUR", "note": "Remind them. No discount, no panic."},
        {"time": "4 HOURS", "note": "Answer the objection they didn’t say."},
        {"time": "24 HOURS", "note": "Add a small incentive. Once."},
    ]
    lines = [[("3 EMAILS.", "solid")], [("ONE CART.", "accent")]]
    return compose(index, "05-parcel.jpg", 600, lines,
                   "The highest-ROI flow in Q4. Build it first.",
                   crop=108, title_max_h=262, title_start=146, lede_size=31, gap=30,
                   rows=rows, row_h=92, row_style="time", seed=55)


def slide_statement(index):
    lines = [[("DON’T JUST", "solid")], [("SURVIVE", "solid"), (" Q4.", "accent")],
             [("OWN IT.", "solid")]]
    return compose(index, "06-fog.jpg", 660, lines,
                   "Build the momentum now and make 2027 your best year yet.",
                   title_max_h=348, title_start=172, lede_size=34, gap=30, seed=66)


def slide_cta(index):
    lines = [[("LET’S BUILD", "solid")], [("YOUR Q4.", "accent")]]
    return compose(index, "07-portrait.jpg", 760, lines,
                   "DM the word FLOWS for the full 5-flow map, free.",
                   title_max_h=306, title_start=188, lede_size=36, gap=30,
                   cta="DM  LVLSMARKETING", footer="Save this post", seed=77)


BUILDERS = [
    ("slide-01", slide_cover, "5 EMAIL FLOWS"),
    ("slide-02", slide_problem, "Q4 IS 35-40% OF YOUR YEAR"),
    ("slide-03", slide_list, "THE 5 FLOWS"),
    ("slide-04", slide_timing, "TIMING BEATS COPY"),
    ("slide-05", slide_cart, "3 EMAILS ONE CART"),
    ("slide-06", slide_statement, "DON’T JUST SURVIVE Q4"),
    ("slide-07", slide_cta, "LET’S BUILD YOUR Q4"),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for i, (slug, fn, title) in enumerate(BUILDERS, start=1):
        img = fn(i)
        path = os.path.join(OUT_DIR, slug + ".png")
        img.save(path, optimize=True)
        print(f"{path}  {title}")


if __name__ == "__main__":
    main()
