"""Build the LVLS carousel: PNG exports + an HTML proof sheet + web preview."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content  # noqa: E402
import slides_min  # noqa: E402
from slides import render_slide  # noqa: E402
from theme import OUT_DIR  # noqa: E402

SPECS = [
    # (label, w, h, theme, ext, renderer, note)
    ("feed", 1080, 1350, "dark", "png", "min",
     "Instagram feed 4:5 — PRIMARY (minimal black edition)"),
    ("square", 1080, 1080, "dark", "jpg", "min", "1:1 fallback for feed-grid preview"),
    ("story", 1080, 1920, "dark", "jpg", "min", "9:16 for Stories / Reels cover"),
    ("editorial", 1080, 1350, "dark", "png", "edit",
     "alternate edition — editorial dark (earlier direction)"),
    ("editorial-light", 1080, 1350, "light", "png", "edit",
     "alternate edition — editorial light"),
]


def build(variants=("feed",), out: Path = OUT_DIR):
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for label, w, h, theme, ext, renderer, note in SPECS:
        if label not in variants:
            continue
        d = out / label
        d.mkdir(parents=True, exist_ok=True)
        slides = content.MIN_SLIDES if renderer == "min" else content.SLIDES
        for i, sl in enumerate(slides, start=1):
            img = (slides_min.render_minimal(sl, w, h) if renderer == "min"
                   else render_slide(sl, w, h, theme))
            p = d / f"lvls-email-flows-{label}-{i:02d}.{ext}"
            if ext == "png":
                img.save(p, "PNG", optimize=True)
            else:
                img.save(p, "JPEG", quality=93, optimize=True, progressive=True)
            written.append((p, note))
            print(f"  wrote {p.relative_to(out.parent)}  ({w}x{h}, {theme})")
    return written


def contact_sheet(out: Path, variant="feed", cols=4, thumb_w=520):
    """Grid overview PNG of one variant (handy for approvals / chat share)."""
    from PIL import Image, ImageDraw as ID
    import content as C
    files = sorted((out / variant).glob("*.png"))
    if not files:
        return
    names = ["01 COVER", "02 WELCOME", "03 CART", "04 BROWSE", "05 POST-PURCHASE",
             "06 WINBACK", "07 CTA"]
    rows = (len(files) + cols - 1) // cols
    gap, lab = 26, 46
    tw, th = thumb_w, int(thumb_w * 1350 / 1080)
    W = cols * tw + (cols + 1) * gap
    H = rows * (th + lab) + (rows + 1) * gap
    sheet = Image.new("RGB", (W, H), (11, 11, 12))
    d = ID.Draw(sheet)
    from theme import font as F
    for i, f in enumerate(files):
        r, c = divmod(i, cols)
        x = gap + c * (tw + gap)
        y = gap + r * (th + lab + gap)
        im = Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS)
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + tw, y + 3], fill=(255, 106, 0))
        d.text((x + 2, y + th + 12), names[i] if i < len(names) else f.stem,
               font=F("label", 24), fill=(200, 198, 193))
    p = out / f"contact-sheet-{variant}.jpg"
    sheet.save(p, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"  wrote {p}")


def proof_sheet(out: Path, variants):
    """Single scrollable HTML page showing every rendered slide."""
    out.mkdir(parents=True, exist_ok=True)
    html = ["<!doctype html><html lang='en'><head><meta charset='utf-8'>",
            "<meta name='viewport' content='width=device-width,initial-scale=1'>",
            "<title>LVLS Agency — Email Flows Carousel</title>",
            """<style>
:root{color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:#0b0b0c;color:#f5f3ee;
font-family:ui-sans-serif,system-ui,'Segoe UI',Helvetica,Arial,sans-serif}
header{padding:40px 28px 8px;max-width:1400px;margin:0 auto}
h1{font-size:clamp(22px,3vw,34px);margin:0 0 6px;letter-spacing:-.02em}
.sub{color:#a7a5a0;font-size:14px;line-height:1.6;margin:0 0 4px}
.accent{color:#ff6a00;font-weight:700}
section{max-width:1400px;margin:0 auto;padding:26px 28px 10px}
h2{font-size:13px;letter-spacing:.22em;text-transform:uppercase;color:#a7a5a0;
margin:0 0 14px;font-weight:600}
.rail{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(220px,1fr);
gap:16px;overflow-x:auto;padding-bottom:18px;scroll-snap-type:x mandatory}
.rail img{width:100%;height:auto;display:block;border-radius:10px;
border:1px solid rgba(255,255,255,.12);scroll-snap-align:start;background:#111}
.cap{max-width:900px;background:#131315;border:1px solid rgba(255,255,255,.1);
border-radius:12px;padding:18px 20px;white-space:pre-wrap;font-size:13.5px;
line-height:1.75;color:#d8d5d0}
footer{max-width:1400px;margin:0 auto;padding:26px 28px 60px;color:#6a6967;
font-size:12px;letter-spacing:.08em;text-transform:uppercase}
a{color:#ff6a00}
</style></head><body>""",
            "<header>",
            "<h1>LVLS Agency — <span class='accent'>5 email flows every clothing "
            "brand needs</span></h1>",
            f"<p class='sub'>{content.POST_DATE} · 7 slides · CTA: Save + DM AUDIT<br>"
            "Rendered from code (Pillow) at 1080×1350, 1080×1080 and 1080×1920. "
            "Every size, theme and copy line is editable in <code>src/content.py</code> "
            "and <code>src/theme.py</code>.</p>",
            "</header>"]
    exts = {sp[0]: sp[4] for sp in SPECS}
    for label, w, h, theme, ext, renderer, note in SPECS:
        if label not in variants:
            continue
        html.append(f"<section><h2>{label} · {w}×{h} · {theme} — {note}</h2><div class='rail'>")
        for i in range(1, len(content.SLIDES) + 1):
            rel = f"{label}/lvls-email-flows-{label}-{i:02d}.{exts[label]}"
            html.append(f"<a href='{rel}' download><img src='{rel}' "
                        f"alt='Slide {i}' loading='lazy'></a>")
        html.append("</div></section>")
    html.append("<section><h2>Caption (copy-paste)</h2>"
                f"<div class='cap'>{content.CAPTION}</div></section>")
    html.append("<footer>LVLS Agency · email flows for fashion brands</footer>"
                "</body></html>")
    (out / "index.html").write_text("\n".join(html), encoding="utf-8")
    print(f"  wrote {out / 'index.html'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--variants", default="feed,square,story,editorial,editorial-light",
                    help="comma list of: feed, feed-light, square, story")
    a = ap.parse_args()
    vs = tuple(v.strip() for v in a.variants.split(",") if v.strip())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build(vs)
    proof_sheet(OUT_DIR, vs)
    for v in vs:
        if v in ("feed", "editorial"):
            contact_sheet(OUT_DIR, v)
    print("done.")
