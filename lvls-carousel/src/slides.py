"""Slide renderer — draws one 1080x1350 (or 1080x1080 / 1080x1920) LVLS slide."""
from __future__ import annotations

from PIL import Image, ImageDraw

import content
from drawkit import (
    arrow_swipe,
    chip,
    draw_block,
    draw_spaced,
    fit_size,
    ghost_numeral,
    make_background,
    progress_pips,
    rrect,
    spaced_width,
)
from icons import draw_icon, icon_tile
from theme import BRAND, Layout, PALETTES, font, px


# ------------------------------------------------------------------ chrome ---
def chrome(base, dr, L, pal, slide_num="01", total=7, lit=0, label=None):
    m = L.m
    # top accent tab
    dr.rectangle([0, 0, px(150, L.s), px(9, L.s)], fill=pal["accent"])

    # wordmark
    y = L.top_y
    w1 = draw_spaced(dr, (m, y), "LVLS", font("disp", px(30, L.s)), pal["ink"],
                     px(1.6, L.s))
    x2 = m + w1 + px(14, L.s)
    draw_spaced(dr, (x2, y + px(4, L.s)), "AGENCY", font("label", px(19, L.s)),
                pal["ink_dim"], px(3.0, L.s))
    # divider + tagline
    tag_x = m + px(230, L.s)
    dr.line([(tag_x, y + px(4, L.s)), (tag_x, y + px(28, L.s))],
            fill=pal["stroke"], width=max(1, px(1.6, L.s)))
    draw_spaced(dr, (tag_x + px(18, L.s), y + px(7, L.s)), content.HANDLE,
                font("label", px(19, L.s)), pal["ink_faint"], px(1.6, L.s))

    # slide number, right
    draw_spaced(dr, (base.width - m, y + px(3, L.s)), f"{slide_num}/{total:02d}",
                font("num", px(22, L.s)), pal["ink_dim"], px(2.2, L.s), "rm")

    # progress pips
    progress_pips(dr, base.width - m, y + px(56, L.s), total, lit, L.s,
                  pal["accent"], pal["stroke_soft"])
    if label:
        draw_spaced(dr, (m, y + px(46, L.s)), label, font("label", px(19, L.s)),
                    pal["ink_faint"], px(3.0, L.s))

    # hairline rule
    ry = y + px(88, L.s)
    dr.line([(m, ry), (base.width - m, ry)], fill=pal["stroke_soft"],
            width=max(1, px(1.6, L.s)))
    return ry + px(34, L.s)


def footer(base, dr, L, pal, left=None, right=None, y=None):
    """Bottom strip: left label (+icon) ... right label / icon / chevrons."""
    m = L.m
    y = y or base.height - px(118, L.v)
    dr.line([(m, y - px(38, L.v)), (base.width - m, y - px(38, L.v))],
            fill=pal["stroke_soft"], width=max(1, px(1.6, L.s)))
    fs = px(21, L.s)
    tr = px(3.2, L.s)
    isize = px(30, L.s)

    if left:
        x = m
        if left.get("icon"):
            draw_icon(dr, left["icon"], [x, y - px(6, L.v), x + isize, y - px(6, L.v) + isize],
                      pal["accent"], 1.8)
            x += isize + px(14, L.s)
        draw_spaced(dr, (x, y), left["text"], font("label", fs), pal["ink_dim"], tr)

    if right:
        x = base.width - m
        n = right.get("chevrons", 0)
        if n:
            clen = px(24, L.s)
            total_w = clen * 0.62 * (n - 1) + clen * 0.42
            arrow_swipe(dr, x - total_w, y + px(11, L.v), clen, max(3, px(5, L.s)),
                        pal["accent"], heads=n)
            x -= total_w + px(22, L.s)
        if right.get("text"):
            draw_spaced(dr, (x, y), right["text"], font("label", fs), pal["ink_dim"],
                        tr, "rm")
            x -= spaced_width(dr, right["text"], font("label", fs), tr) + px(16, L.s)
        if right.get("icon"):
            x -= isize
            draw_icon(dr, right["icon"], [x, y - px(6, L.v), x + isize, y - px(6, L.v) + isize],
                      pal["accent"], 1.8)


# ------------------------------------------------------------------ cover ----
def render_cover(base, dr, L, pal, sl):
    y = chrome(base, dr, L, pal, sl["num"], lit=0, label=content.POST_DATE)
    m = L.m
    cw = base.width - 2 * m

    # eyebrow row
    box = chip(dr, sl["eyebrow_chip"], (m, y), "label", px(19, L.s),
               pal["surface_strong"], pal["ink"], px(18, L.s), px(12, L.s), px(3.0, L.s),
               outline=pal["stroke"])
    ex = box[2] + px(20, L.s)
    draw_spaced(dr, (ex, box[1] + px(11, L.s)), sl["eyebrow_text"],
                font("label", px(19, L.s)), pal["ink_dim"], px(3.0, L.s))
    y = box[3] + px(56, L.v)

    # headline
    hl_sizes = []
    for i, line in enumerate(sl["headline"]):
        fkey = line["tokens"][0]["font"]
        big = i < 2
        size = fit_size(dr, " ".join(t["text"] for t in line["tokens"]),
                        "disp" if big else "disp_b", cw * (1.0 if big else 0.995),
                        hi=px(152, L.s) if big else px(92, L.s), lo=px(40, L.s))
        hl_sizes.append(size)
    max_size = max(hl_sizes[:2])
    for i, line in enumerate(sl["headline"]):
        big = i < 2
        size = max_size if big else hl_sizes[i]
        toks = []
        for t in line["tokens"]:
            sz = int(round(size * t.get("scale", 1.0)))
            toks.append({
                "text": t["text"], "font": font(t["font"], sz),
                "fill": pal[t["color"]],
                "hl": pal[t["hl"]] if t.get("hl") else None,
                "hl_ink": pal.get("accent_ink") if t.get("hl") else None,
                "tracking": px(-2.0 if big else -0.5, L.s),
            })
        y = draw_block(base, dr, (m, y), toks, cw,
                       leading=0.90 if big else 1.06, seed=i + 2,
                       hl_slant=0.14) + (px(14, L.v) if big else px(6, L.v))

    y += px(46, L.v)

    # the 5 flows list (tall formats) / icon rail (square & shorter)
    if base.height >= 1240:
        draw_spaced(dr, (m, y), sl["list_title"], font("label", px(20, L.s)),
                    pal["ink_faint"], px(4.0, L.s))
        y += px(40, L.v)
        items = [{"icon": ic, "text": name, "idx": i + 1}
                 for i, (name, ic) in enumerate(zip(content.FLOWS, content.FLOW_ICONS))]
        bullet_rows(base, dr, L, pal, items, y, base.height - px(182, L.v),
                    numbered=True, tile_max=px(62, L.s), text_cap=34, tile_frac=0.72,
                    tracking=1.2, max_slot=px(118, L.v))
    else:
        y += px(10, L.v)
        n = len(content.FLOW_ICONS)
        tile = px(92, L.s)
        gap = (cw - n * tile) / (n - 1)
        x = m
        for ic in content.FLOW_ICONS:
            icon_tile(dr, [x, y, x + tile, y + tile], ic, pal["accent"],
                      pal["surface"], pal["stroke"], radius=px(26, L.s), width=1.85)
            x += tile + gap
        y += tile + px(34, L.v)
        draw_spaced(dr, (base.width / 2, y), "the full checklist inside",
                    font("serif", px(44, L.s)), pal["accent_soft"], 0, "cm")

    footer(base, dr, L, pal, sl.get("footer_left"), sl.get("footer_right"))
    return base


def bullet_rows(base, dr, L, pal, items, top, bottom, numbered=False,
                max_slot=None, tile_max=None, text_cap=46, tile_frac=0.60,
                tracking=0.4):
    """Evenly spaced icon+text rows between top and bottom hairline separators."""
    m = L.m
    n = len(items)
    avail = bottom - top
    slot = avail / n
    if max_slot:
        slot = min(slot, max_slot)
    total = slot * n
    start = top + (avail - total) / 2
    tile = min(tile_max or px(88, L.s), slot * tile_frac)
    for i, b in enumerate(items):
        cy = start + slot * i + slot / 2
        icon_tile(dr, [m, cy - tile / 2, m + tile, cy + tile / 2], b["icon"],
                  pal["accent"], pal["surface"], pal["stroke"],
                  radius=px(22, L.s), width=1.85)
        tx = m + tile + px(28, L.s)
        if numbered:
            draw_spaced(dr, (tx, cy - px(14, L.v)), f"{b.get('idx', i + 1):02d}",
                        font("num", px(22, L.s)), pal["ink_faint"], px(1.5, L.s))
            tx += px(64, L.s)
        avail_w = base.width - m - tx - (px(56, L.s) if not numbered else 0)
        sz = fit_size(dr, b["text"], "body_b", avail_w, px(text_cap, L.s), px(18, L.s),
                      px(tracking, L.s))
        if spaced_width(dr, b["text"], font("body_b", sz), px(tracking, L.s)) > avail_w:
            toks = [{"text": b["text"], "font": font("body_b", sz), "fill": pal["ink"],
                     "tracking": px(tracking, L.s)}]
            draw_block(base, dr, (tx, cy - sz * 0.62), toks, avail_w, leading=1.1)
        else:
            draw_spaced(dr, (tx, cy - sz * 0.40), b["text"], font("body_b", sz),
                        pal["ink"], px(tracking, L.s))
        if not numbered:
            draw_spaced(dr, (base.width - m, cy - px(12, L.v)), f"{i + 1:02d}",
                        font("num", px(24, L.s)), pal["ink_faint"], px(1.5, L.s), "rm")
        if i < n - 1:
            ly = start + slot * (i + 1)
            dr.line([(m, ly), (base.width - m, ly)], fill=pal["stroke_soft"],
                    width=max(1, px(1.4, L.s)))
    return start + total


# ------------------------------------------------------------------- flow ----
def render_flow(base, dr, L, pal, sl):
    idx = sl["flow_index"]
    m = L.m
    cw = base.width - 2 * m

    # ghost numeral behind everything, right-anchored so it never crops
    gsize = px(680, L.s)
    gf = font("disp", gsize)
    gw = dr.textlength(sl["num"], font=gf)
    ghost_numeral(base, sl["num"], "disp", gsize,
                  (base.width - m - gw + px(36, L.s), base.height * 0.335),
                  pal["ghost"])
    dr = ImageDraw.Draw(base)

    y = chrome(base, dr, L, pal, sl["num"], lit=idx + 1, label=content.FLOWS[idx])

    # flow tag: tile + kicker + name
    tile = px(96, L.s)
    icon_tile(dr, [m, y, m + tile, y + tile], sl["icon"], pal["accent"],
              pal["surface_strong"], pal["stroke"], radius=px(26, L.s), width=1.8)
    tx = m + tile + px(26, L.s)
    draw_spaced(dr, (tx, y + px(10, L.s)), sl["kicker"], font("label", px(21, L.s)),
                pal["accent"], px(4.6, L.s))
    nsz = fit_size(dr, sl["name"], "body_b", base.width - m - tx, px(48, L.s), px(22, L.s),
                   px(0.6, L.s))
    draw_spaced(dr, (tx, y + px(44, L.s)), sl["name"], font("body_b", nsz), pal["ink"],
                px(0.6, L.s))
    y += tile + px(58, L.v)

    # headline
    for i, line in enumerate(sl["headline"]):
        big = i < 2
        size = fit_size(dr, " ".join(t["text"] for t in line["tokens"]),
                        "disp" if big else "disp_b", cw,
                        hi=px(126, L.s) if big else px(60, L.s), lo=px(30, L.s))
        toks = [{
            "text": t["text"],
            "font": font(t["font"], int(round(size * t.get("scale", 1.0)))),
            "fill": pal[t["color"]],
            "hl": pal[t["hl"]] if t.get("hl") else None,
            "hl_ink": pal.get("accent_ink") if t.get("hl") else None,
            "tracking": px(-1.5 if big else 0, L.s),
        } for t in line["tokens"]]
        y = draw_block(base, dr, (m, y), toks, cw,
                       leading=0.94 if big else 1.12, seed=i + idx * 3 + 5,
                       hl_slant=0.15) + (px(10, L.v) if big else px(0, L.v))

    # bullets, centred in the remaining space
    bullet_rows(base, dr, L, pal, sl["bullets"], y + px(46, L.v),
                base.height - px(190, L.v), max_slot=px(210, L.v),
                tile_max=px(92, L.s), text_cap=44)

    footer(base, dr, L, pal,
           {"icon": "bookmark", "text": "SAVE THIS"},
           {"text": "SWIPE", "chevrons": 3})
    return base


# -------------------------------------------------------------------- cta ----
def render_cta(base, dr, L, pal, sl):
    m = L.m
    cw = base.width - 2 * m
    idx = content.TOTAL_FLOWS

    y = chrome(base, dr, L, pal, sl["num"], lit=idx, label="CALL TO ACTION")

    box = chip(dr, sl["eyebrow_chip"], (m, y), "label", px(19, L.s),
               pal["surface_strong"], pal["ink"], px(18, L.s), px(12, L.s), px(3.0, L.s),
               outline=pal["stroke"])
    draw_spaced(dr, (box[2] + px(20, L.s), box[1] + px(11, L.s)), sl["eyebrow_text"],
                font("label", px(19, L.s)), pal["ink_dim"], px(3.0, L.s))
    y = box[3] + px(50, L.v)

    # DM / AUDIT headline
    for i, line in enumerate(sl["headline"]):
        size = fit_size(dr, line["tokens"][0]["text"], "disp", cw, px(176, L.s), px(60, L.s),
                        px(-3, L.s))
        toks = [{
            "text": t["text"], "font": font("disp", size),
            "fill": pal[t["color"]],
            "hl": pal[t["hl"]] if t.get("hl") else None,
            "hl_ink": pal["accent_ink"] if t.get("hl") else None,
            "tracking": px(-3, L.s),
        } for t in line["tokens"]]
        y = draw_block(base, dr, (m, y), toks, cw, leading=0.96, seed=i + 11) \
            + px(16, L.v)

    y += px(40, L.v)

    # button
    bh = px(116, L.s)
    btn_box = [m, y, base.width - m, y + bh]
    dr.rounded_rectangle([btn_box[0] + px(6, L.s), btn_box[1] + px(9, L.s),
                          btn_box[2] + px(6, L.s), btn_box[3] + px(9, L.s)],
                         radius=px(30, L.s), fill=(0, 0, 0, 60))
    dr.rounded_rectangle(btn_box, radius=px(30, L.s), fill=pal["accent"])
    bsz = fit_size(dr, sl["button"], "disp", cw * 0.62, px(66, L.s), px(28, L.s), px(-1, L.s))
    btw = spaced_width(dr, sl["button"], font("disp", bsz), px(-1, L.s))
    isz = px(56, L.s)
    total_w = btw + px(28, L.s) + isz
    bx = m + (cw - total_w) / 2
    draw_spaced(dr, (bx, y + bh / 2 - bsz * 0.42), sl["button"], font("disp", bsz),
                pal["accent_ink"], px(-1, L.s))
    draw_icon(dr, "send", [bx + btw + px(28, L.s), y + bh / 2 - isz / 2,
                           bx + btw + px(28, L.s) + isz, y + bh / 2 + isz / 2],
              pal["accent_ink"], 1.9)
    y = btn_box[3] + px(22, L.v)
    draw_spaced(dr, (base.width / 2, y), sl["button_note"], font("label", px(18, L.s)),
                pal["ink_faint"], px(2.6, L.s), "cm")
    y += px(48, L.v)

    bullet_rows(base, dr, L, pal, sl["bullets"], y, base.height - px(186, L.v),
                max_slot=px(150, L.v), tile_max=px(80, L.s), text_cap=40)

    footer(base, dr, L, pal, sl.get("footer_left"), sl.get("footer_right"))
    return base


# -------------------------------------------------------------------- api ----
def render_slide(sl, w=1080, h=1350, theme="dark"):
    pal = PALETTES[theme]
    base = make_background(w, h, pal, seed=hash(sl["num"]) % 9973)
    dr = ImageDraw.Draw(base)
    L = Layout(w, h)
    {"cover": render_cover, "flow": render_flow, "cta": render_cta}[sl["kind"]](
        base, dr, L, pal, sl)
    return base.convert("RGB")
