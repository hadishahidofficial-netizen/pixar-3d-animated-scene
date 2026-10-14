"""MINIMAL BLACK edition — bottom-weighted layout per the approved reference.

Black canvas, tiny tracked meta top, centred icon + micro-copy, hairline rule
with an orange diamond, then a bottom-anchored title block with orange italic
accents and numbered bullets.
"""
from __future__ import annotations

from PIL import Image, ImageDraw

import content
from drawkit import draw_spaced, fit_size, spaced_width
from icons import draw_icon
from theme import font, px

BG = (13, 13, 13)
INK = (242, 242, 240)
DIM = (150, 150, 148)
DIM2 = (104, 104, 102)
RULE = (58, 58, 58)
ORANGE = (255, 77, 0)


def _bg(w, h):
    img = Image.new("RGBA", (w, h), (*BG, 255))
    return img


def _chevrons(dr, x_right, y, n, size, color, width):
    """Orange >>> chevrons ending at x_right."""
    gap = size * 0.78
    x = x_right - (gap * (n - 1) + size * 0.5)
    for i in range(n):
        cx = x + i * gap
        dr.line([(cx, y - size * 0.5), (cx + size * 0.5, y), (cx, y + size * 0.5)],
                fill=color, width=width, joint="curve")
    return x


def render_minimal(sl, w=1080, h=1350):
    img = _bg(w, h)
    dr = ImageDraw.Draw(img)
    s = w / 1080.0
    v = h / 1350.0
    m = px(64, s)

    # ---------------------------------------------------------- top meta ---
    ty = px(64, v)
    sq = px(13, s)
    dr.rectangle([m, ty + px(4, v), m + sq, ty + px(4, v) + sq], fill=ORANGE)
    draw_spaced(dr, (m + sq + px(16, s), ty), sl["label"], font("label", px(19, s)),
                INK, px(3.4, s))
    draw_spaced(dr, (w - m, ty), content.HANDLE, font("label", px(19, s)), DIM2,
                px(1.6, s), "rm")

    # ------------------------------------------------- centred icon+micro ---
    cy = h * 0.335
    isz = px(74, s)
    draw_icon(dr, sl["icon"], [w / 2 - isz / 2, cy - isz / 2, w / 2 + isz / 2, cy + isz / 2],
              ORANGE, 1.7, bg=BG)
    y = cy + isz / 2 + px(30, v)
    for i, line in enumerate(sl["micro"]):
        col = DIM if i == 0 else DIM2
        draw_spaced(dr, (w / 2, y), line.upper(), font("label", px(18, s)), col,
                    px(3.2, s), "cm")
        y += px(30, v)

    # --------------------------------------------- rule + diamond + title ---
    rule_y = h - px(470, v) if h >= 1240 else h * 0.60
    dr.line([(m, rule_y), (w - m, rule_y)], fill=RULE, width=max(1, px(1.6, s)))
    d = px(9, s)
    dr.polygon([(w / 2, rule_y - d), (w / 2 + d, rule_y), (w / 2, rule_y + d),
                (w / 2 - d, rule_y)], fill=ORANGE)

    y = rule_y + px(52, v)
    cw = w - 2 * m

    # title lines
    for li, line in enumerate(sl["title"]):
        big = li == 0 and len(sl["title"]) > 1
        single = len(sl["title"]) == 1
        cap = px(96, s) if big else (px(84, s) if single else px(58, s))
        text = "".join(t for t, _ in line)
        fkey = "blk_it" if False else "head"
        size = fit_size(dr, text, "head", cw, cap, px(30, s))
        # measure segment widths at that size
        widths = [spaced_width(dr, t, font("head" if st in ("w", "w2") else "blk_it", size),
                               0) for t, st in line]
        # second (lowercase) line uses Bold / Black-Italic pair
        if line and line[0][1] in ("w2", "a2"):
            widths = [spaced_width(dr, t, font("bold" if st == "w2" else "blk_it", size),
                                   0) for t, st in line]
        total = sum(widths)
        x = m
        for (t, st), wd in zip(line, widths):
            if st == "w":
                f = font("head", size)
            elif st == "w2":
                f = font("bold", size)
            else:
                f = font("blk_it", size)
            dr.text((x, y), t, font=f, fill=ORANGE if st in ("a", "a2") else INK)
            x += wd
        y += size * (1.06 if not big else 1.02) + px(6, v)

    # bullets / lines
    y += px(26, v)
    n = len(sl["lines"])
    if n:
        numbered = sl["num"] != "07"
        lh = px(52, v)
        for i, segs in enumerate(sl["lines"]):
            x = m
            if numbered:
                nf = font("cond_bi", px(24, s))
                num = f"{i + 1:02d}"
                dr.text((x, y + px(6, v)), num, font=nf, fill=ORANGE)
                x += spaced_width(dr, num, nf, 0) + px(20, s)
            avail = w - m - x
            size = fit_size(dr, "".join(t for t, _ in segs), "body_b", avail,
                            px(36, s), px(18, s))
            for t, st in segs:
                f = font("cond_bi" if st == "a" else "body_b", size)
                dr.text((x, y), t, font=f, fill=ORANGE if st == "a" else INK)
                x += spaced_width(dr, t, f, 0)
            y += lh
        y += px(10, v)

    # ------------------------------------------------------------- footer ---
    fy = h - px(64, v)
    if sl.get("button"):
        draw_spaced(dr, (m, fy - px(4, v)), "LVLS AGENCY", font("label", px(19, s)),
                    DIM, px(3.2, s))
        bf = font("head", px(30, s))
        bw = spaced_width(dr, sl["button"], bf, 0)
        pad = px(30, s)
        bh = px(64, s)
        bx1 = w - m
        bx0 = bx1 - (bw + pad * 2)
        dr.rectangle([bx0, fy - bh / 2 - px(6, v), bx1, fy + bh / 2 - px(6, v)],
                     fill=ORANGE)
        dr.text((bx0 + pad, fy - bh / 2 - px(6, v) + (bh - px(30, s)) / 2 - px(2, s)),
                sl["button"], font=bf, fill=BG)
    else:
        swipe = sl.get("swipe") or "Swipe"
        x = w - m
        clen = px(20, s)
        cx = _chevrons(dr, x, fy + px(8, v), 3, clen, ORANGE, max(3, px(4, s)))
        draw_spaced(dr, (cx - px(16, s), fy - px(4, v)), swipe, font("bold", px(24, s)),
                    INK, 0, "rm")
    return img.convert("RGB")
