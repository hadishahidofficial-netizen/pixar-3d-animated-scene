"""Hand-built line icons drawn on a 24x24 grid, scaled to any box."""
from __future__ import annotations

from PIL import ImageDraw

from theme import font

G = 24.0


def _t(box, pt):
    x0, y0, x1, y1 = box
    s = min(x1 - x0, y1 - y0) / G
    ox = x0 + ((x1 - x0) - s * G) / 2
    oy = y0 + ((y1 - y0) - s * G) / 2
    return (ox + pt[0] * s, oy + pt[1] * s), s


class Pen:
    """Stroke wrapper: coordinates live on a 24-unit grid, widths scale with the box."""

    def __init__(self, dr: ImageDraw.ImageDraw, box, color, width, bg=None):
        self.dr, self.box, self.color = dr, box, color
        self.bg = bg
        _, self.s = _t(box, (0, 0))
        self.w = max(1.4, width * self.s)

    def disc(self, c, r, fill):
        x, y = self.t(c)
        rr = r * self.s
        self.dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=fill)

    def t(self, pt):
        p, _ = _t(self.box, pt)
        return p

    def line(self, a, b, width=None):
        self.dr.line([self.t(a), self.t(b)], fill=self.color,
                     width=int(round(width or self.w)), joint="curve")

    def poly(self, pts, width=None, closed=False):
        seq = [self.t(p) for p in pts]
        if closed:
            seq.append(seq[0])
        self.dr.line(seq, fill=self.color, width=int(round(width or self.w)), joint="curve")

    def circle(self, c, r, width=None, fill=None):
        x, y = self.t(c)
        rr = r * self.s
        self.dr.ellipse([x - rr, y - rr, x + rr, y + rr], outline=fill or self.color,
                        fill=fill, width=int(round(width or self.w)))

    def arc(self, c, r, a0, a1, width=None):
        x, y = self.t(c)
        rr = r * self.s
        self.dr.arc([x - rr, y - rr, x + rr, y + rr], start=a0, end=a1,
                    fill=self.color, width=int(round(width or self.w)))

    def dot(self, c, r=0.95):
        x, y = self.t(c)
        rr = r * self.s
        self.dr.ellipse([x - rr, y - rr, x + rr, y + rr], fill=self.color)

    def glyph(self, pt, text, size_units, fkey="disp_b", anchor="la"):
        f = font(fkey, max(6, int(round(size_units * self.s))))
        self.dr.text(self.t(pt), text, font=f, fill=self.color, anchor=anchor)


# ------------------------------------------------------------------- icons ---
def envelope(p):
    p.poly([(3, 6.6), (21, 6.6), (21, 17.8), (3, 17.8)], closed=True)
    p.line((3.5, 7.3), (12, 13.2))
    p.line((20.5, 7.3), (12, 13.2))


def bag(p):
    p.poly([(5.2, 8.4), (18.8, 8.4), (17.7, 20.4), (6.3, 20.4)], closed=True)
    p.arc((12, 8.4), 3.4, 180, 360)


def tag(p):
    p.poly([(4.6, 4.6), (12.8, 4.6), (19.8, 11.6), (11.6, 19.8), (4.6, 12.8)], closed=True)
    p.circle((8.4, 8.4), 1.35)


def clock(p):
    p.circle((12, 12.4), 7.9)
    p.line((12, 12.4), (12, 7.6))
    p.line((12, 12.4), (15.5, 14.5))


def question(p):
    p.arc((12, 9.4), 4.3, 205, 340)
    p.poly([(16.0, 11.3), (15.0, 13.5), (12.3, 14.5), (12.3, 16.5)])
    p.dot((12.3, 19.7), 1.1)


def eye(p):
    p.poly([(2.6, 12), (6.4, 8.2), (10.6, 6.6), (13.4, 6.6), (17.6, 8.2), (21.4, 12)])
    p.poly([(2.6, 12), (6.4, 15.8), (10.6, 17.4), (13.4, 17.4), (17.6, 15.8), (21.4, 12)])
    p.circle((12, 12), 3.1)
    p.dot((12, 12), 1.2)


def tshirt(p):
    p.poly([
        (8.4, 4.2), (4.0, 6.2), (2.6, 10.6), (5.9, 11.9), (5.9, 20.2),
        (18.1, 20.2), (18.1, 11.9), (21.4, 10.6), (20.0, 6.2), (15.6, 4.2),
        (14.1, 5.9), (12.0, 6.7), (9.9, 5.9),
    ], closed=True)


def heart(p):
    p.arc((8.6, 9.4), 3.5, 180, 360)
    p.arc((15.4, 9.4), 3.5, 180, 360)
    p.line((5.1, 9.4), (12.0, 18.9))
    p.line((18.9, 9.4), (12.0, 18.9))


def sparkle(p):
    p.poly([(12, 3.2), (13.6, 10.4), (20.8, 12), (13.6, 13.6), (12, 20.8),
            (10.4, 13.6), (3.2, 12), (10.4, 10.4)], closed=True)


def label(p):
    p.poly([(8.2, 4.6), (20.4, 4.6), (20.4, 19.4), (8.2, 19.4), (3.6, 12)], closed=True)
    p.circle((7.5, 12), 1.25)
    p.line((11.6, 9.4), (17.2, 9.4), width=p.w * 0.8)
    p.line((11.6, 14.4), (15.2, 14.4), width=p.w * 0.8)


def moon(p):
    """Solid crescent: disc minus an offset disc punched with the tile colour."""
    p.disc((11.4, 12.6), 7.9, p.color)
    p.disc((15.6, 9.0), 6.9, p.bg or p.color)


def zzz(p):
    p.glyph((3.4, 4.4), "Z", 8.6, anchor="la")
    p.glyph((10.6, 9.6), "Z", 7.0, anchor="la")
    p.glyph((16.6, 14.2), "Z", 5.6, anchor="la")


def bookmark(p):
    p.poly([(6.4, 3.4), (17.6, 3.4), (17.6, 20.6), (12.0, 16.4), (6.4, 20.6)], closed=True)


def share(p):
    p.poly([(13.6, 7.6), (18.0, 3.4), (22.2, 7.8)], width=p.w)
    p.line((18.0, 3.8), (18.0, 13.2))
    p.poly([(6.2, 10.4), (6.2, 20.4), (19.6, 20.4), (19.6, 15.2)])


def chat(p):
    p.poly([(3.4, 5.2), (20.6, 5.2), (20.6, 15.8), (11.6, 15.8), (7.2, 20.0),
            (7.2, 15.8), (3.4, 15.8)], closed=True)
    p.dot((8.4, 10.5), 1.1)
    p.dot((12.0, 10.5), 1.1)
    p.dot((15.6, 10.5), 1.1)


def flow(p):
    p.circle((5.8, 6.2), 2.6)
    p.circle((18.2, 12.0), 2.6)
    p.circle((5.8, 17.8), 2.6)
    p.line((8.4, 7.0), (15.6, 11.2))
    p.line((15.6, 12.8), (8.4, 17.0))


def magnet(p):
    p.arc((12, 12.6), 7.4, 180, 360)
    p.line((4.6, 12.6), (4.6, 19.8))
    p.line((19.4, 12.6), (19.4, 19.8))
    p.line((4.6, 16.4), (8.4, 16.4), width=p.w * 0.8)
    p.line((15.6, 16.4), (19.4, 16.4), width=p.w * 0.8)


def send(p):
    p.poly([(3.0, 12.0), (21.0, 4.2), (14.2, 20.8), (11.6, 13.8)], closed=True)
    p.line((11.6, 13.8), (21.0, 4.2), width=p.w * 0.8)


ICONS = {
    "envelope": envelope, "bag": bag, "tag": tag, "clock": clock,
    "question": question, "eye": eye, "tshirt": tshirt, "heart": heart,
    "sparkle": sparkle, "label": label, "moon": moon, "zzz": zzz,
    "bookmark": bookmark, "share": share, "chat": chat, "flow": flow,
    "magnet": magnet, "send": send,
}


def draw_icon(dr, name, box, color, width=1.75, bg=None):
    ICONS[name](Pen(dr, box, color, width, bg=bg))


def icon_tile(dr, box, icon, color, tile_fill, tile_stroke, radius, width=1.75,
              inset=0.30):
    """Rounded tile with a centred icon."""
    x0, y0, x1, y1 = box
    dr.rounded_rectangle(box, radius=radius, fill=tile_fill, outline=tile_stroke,
                         width=max(2, int(round((x1 - x0) * 0.014))))
    pad = (x1 - x0) * inset
    draw_icon(dr, icon, [x0 + pad, y0 + pad, x1 - pad, y1 - pad], color, width,
              bg=tile_fill)
