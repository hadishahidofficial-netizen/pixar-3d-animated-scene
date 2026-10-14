"""Build the LVLS carousel: PNG exports + an HTML proof sheet + web preview."""
from __future__ import annotations

import argparse
import json
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
    """Interactive HTML previewer: big carousel viewer + deck rails + caption."""
    out.mkdir(parents=True, exist_ok=True)
    decks = []
    for label, w, h, theme, ext, renderer, note in SPECS:
        if label not in variants:
            continue
        files = [f"{label}/lvls-email-flows-{label}-{i:02d}.{ext}"
                 for i in range(1, len(content.SLIDES) + 1)]
        decks.append({"label": label, "note": note, "files": files,
                      "size": f"{w}x{h}"})
    tpl = (Path(__file__).resolve().parent / "preview_template.html").read_text(
        encoding="utf-8")
    html = tpl.replace("__DECKS__", json.dumps(decks)).replace(
        "__CAPTION__", content.CAPTION.replace("&", "&amp;").replace("<", "&lt;"))
    (out / "index.html").write_text(html, encoding="utf-8")
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
