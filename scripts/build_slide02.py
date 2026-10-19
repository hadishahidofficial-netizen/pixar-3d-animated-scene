#!/usr/bin/env python3
"""
Carousel slide 02 — 1080x1350 (4:5). Pure black type slide.

HOOK 01 / 06 · PROBLEM
OPEN ON / THE PAIN
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from poster_kit import (
    ANTON, BLACK, CONTENT_W, CW, CH, DIM, FONTS, GREY, H, INTER, MARGIN,
    OFFWHITE, RED, SS, black_canvas, draw_tracked, fit_display, fit_inter,
    font, px, save, tracked_w,
)

LABEL = "HOOK 01 / 06 · PROBLEM"
line1, line2 = "OPEN ON", "THE PAIN"
support = [
    "The problem your product solves.",
    "Like a hoodie that loses its shape after one wash.",
]
COUNTER = "2/8"
HANDLE = "@lvlsmarketing"

# =========================================================
# ground
# =========================================================
img = black_canvas()
layer = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)

# =========================================================
# vertical rhythm (1x units)
# =========================================================
TRACK_EM = -0.035


def ink_span(f, text, tr):
    """Actual rendered ink offsets (measured from the draw origin) at draw scale."""
    probe = Image.new("L", (CW, px(420)), 0)
    pd = ImageDraw.Draw(probe)
    draw_tracked(pd, (0, px(330)), text, f, 255, tr, "ls")
    cols = np.where(np.asarray(probe).max(0) > 40)[0]
    lo, hi = int(cols.min()), int(cols.max()) + 1
    return lo, hi, hi - lo


# size so the widest line's *ink* fills the measure exactly (fixed point)
size = fit_display([line1, line2], CONTENT_W, TRACK_EM)
for _ in range(8):
    f_head = ImageFont.truetype(str(FONTS / ANTON), px(size))
    tr = px(size) * TRACK_EM
    widest = max(ink_span(f_head, l, tr)[1] - ink_span(f_head, l, tr)[0] for l in (line1, line2))
    new_size = size * px(CONTENT_W) / widest
    if abs(new_size - size) < 0.05:
        size = new_size
        break
    size = new_size

# final, consistent metrics for the size actually drawn
f_head = ImageFont.truetype(str(FONTS / ANTON), px(size))
tr = px(size) * TRACK_EM
_, _, IW1 = ink_span(f_head, line1, tr)
LB1, _, IW1 = ink_span(f_head, line1, tr)
LB2, _, IW2 = ink_span(f_head, line2, tr)
LB1, INK1, LB2, INK2 = LB1 / SS, IW1 / SS, LB2 / SS, IW2 / SS
cap_h = (f_head.getbbox("H")[3] - f_head.getbbox("H")[1]) / SS
LEAD = cap_h + 0.055 * size

label_size = 24
LABEL_BASE = 246
HEAD1_BASE = 618
HEAD2_BASE = HEAD1_BASE + LEAD
BAR_TOP = HEAD2_BASE + 76
BAR_H = 16
sup_size = fit_inter(support, CONTENT_W * 0.95, weight=400)
sup_lead = sup_size * 1.46
SUP1_BASE = BAR_TOP + BAR_H + 78
SUP2_BASE = SUP1_BASE + sup_lead
FOOTER_BASE = 1300

print(f"headline {size:.1f}px  cap {cap_h:.0f}  lead {LEAD:.1f}")
print(f"ink widths {INK1:.1f}/{INK2:.1f}  bearings {LB1:.1f}/{LB2:.1f}  "
      f"measure {CONTENT_W}  support {sup_size:.1f}px")
print(f"head1 cap-top {HEAD1_BASE - cap_h:.0f}  head2 {HEAD2_BASE:.0f}  "
      f"bar {BAR_TOP}-{BAR_TOP + BAR_H}  sup {SUP1_BASE:.0f}/{SUP2_BASE:.0f}  "
      f"empty below {H - SUP2_BASE:.0f}")

# =========================================================
# label
# =========================================================
lab = font(INTER, label_size, 700)
LABEL_TR = px(label_size) * 0.22
draw_tracked(d, (px(MARGIN), px(LABEL_BASE)), LABEL, lab, RED + (255,), LABEL_TR, "ls")

# =========================================================
# headline — left aligned on the margin
# =========================================================
draw_tracked(d, (px(MARGIN - LB1), px(HEAD1_BASE)), line1, f_head, OFFWHITE + (255,), tr, "ls")
draw_tracked(d, (px(MARGIN - LB2), px(HEAD2_BASE)), line2, f_head, RED + (255,), tr, "ls")

# =========================================================
# the thick red bar, spanning the margins
# =========================================================
d.rectangle(
    [px(MARGIN), px(BAR_TOP), px(MARGIN + CONTENT_W), px(BAR_TOP + BAR_H)],
    fill=RED + (255,),
)

# =========================================================
# two support lines, left aligned
# =========================================================
sup = font(INTER, sup_size, 400)
d.text((px(MARGIN), px(SUP1_BASE)), support[0], font=sup, fill=OFFWHITE + (255,), anchor="ls")
d.text((px(MARGIN), px(SUP2_BASE)), support[1], font=sup, fill=OFFWHITE + (255,), anchor="ls")

# =========================================================
# furniture
# =========================================================
fur = font(INTER, 21, 500)
draw_tracked(d, (px(MARGIN), px(FOOTER_BASE)), HANDLE, fur, GREY + (235,), px(0.3), "ls")
draw_tracked(d, (CW - px(MARGIN), px(FOOTER_BASE)), COUNTER, fur, GREY + (235,), px(0.3), "rs")

save(Image.alpha_composite(img, layer), "slide-02")
